from pyspark.sql import SparkSession
import logging
from src.processing.game_schema import schema
from pyspark.sql.functions import col
from pyspark.sql.functions import split
from pyspark.sql.functions import abs as spark_abs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chess-pipeline")
handler = logging.FileHandler("/app/logs/pipeline.log")
logger.addHandler(handler)

spark = SparkSession.builder \
    .appName("Process PGN") \
    .master("local[*]") \
    .config("spark.driver.memory", "6g") \
    .config("spark.executor.memory", "6g") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.6.1") \
    .config("spark.mongodb.write.connection.uri", "mongodb://mongodb:27017/chess.games") \
    .getOrCreate()
sc = spark.sparkContext


def split_games(partition):
    buffer = ""
    for line in partition:
        if "[Event" in line and buffer:
            yield buffer
            buffer = line + "\n"
        else:
            buffer += line + "\n"
    if buffer:
        yield buffer


import re


def normalize_time_control(tc):
    if not tc or tc in ["-", "?", ""]:
        return None
    try:
        tc = tc.lower()
        # Lichess format: min + bonus_time
        if "+" in tc and "/" not in tc and tc.replace("+", "").isdigit():
            base, inc = tc.split("+")
            return f"{int(base) // 60}+{int(inc)}"

        # fide format: "40/7200:3600"
        if "/" in tc:
            main_part = tc.split(":")[0]
            seconds = int(main_part.split("/")[1])
            return f"{seconds // 60}+0"

        # Weird text formats: 25 minutes 30 seconds
        minutes_match = re.search(r'(\d+)\s*(min|minutes)', tc)
        seconds_match = re.search(r'(\d+)\s*(sec|seconds)', tc)

        if minutes_match:
            minutes = int(minutes_match.group(1))
            increment = int(seconds_match.group(1)) if seconds_match else 0
            return f"{minutes}+{increment}"

        # Only seconds: 500
        if tc.isdigit():
            return f"{int(tc) // 60}+0"

    except:
        return None

    return None


def safe_int(value):
    try:
        return int(value)
    except:
        return None


def parse_partition(partition):
    for pgn_text in partition:
        try:
            lines = pgn_text.split("\n")
            headers = {}
            moves_section = False
            moves_raw = []

            for line in lines:
                if line.startswith("["):
                    header = line.split(" ", 1)[0][1:]
                    try:
                        header_value = line.split('"')[1]
                    except:
                        header_value = None
                    headers[header] = header_value
                elif line.strip():
                    moves_section = True

                if moves_section:
                    moves_raw.append(line)

            moves_str = " ".join(moves_raw)

            tokens = moves_str.split()
            moves = [
                t for t in tokens
                if not t[0].isdigit() and t not in ["1-0", "0-1", "1/2-1/2", "*"]
            ]

            raw_time_control = headers.get("TimeControl")
            normalized_time_control = normalize_time_control(raw_time_control)

            site = (headers.get("Site") or "").lower()
            event = (headers.get("Event") or "").lower()

            if "lichess" in site:
                rating_type = "lichess"
            elif "online" in event:
                rating_type = "online"
            else:
                rating_type = "otb"

            yield {
                "Event": headers.get("Event"),
                "UTC_Date": headers.get("UTCDate"),
                "UTC_Time": headers.get("UTCTime"),
                "Time_Control": normalized_time_control,
                "White_Player": headers.get("White"),
                "Black_Player": headers.get("Black"),
                "White_Elo": safe_int(headers.get("WhiteElo")),
                "Black_Elo": safe_int(headers.get("BlackElo")),
                "Result": headers.get("Result"),
                "Moves": moves,
                "Move_Count": len(moves),
                "ECO": headers.get("ECO"),
                "Round": safe_int(headers.get("Round")),
                "Rating_Type": rating_type
            }

        except Exception:
            continue


data_files_path = "hdfs://namenode:9000/chess-data/raw/"

logger.info(f"Loading data files.")

raw_rdd = sc.textFile(
    f"{data_files_path}**/*.pgn",
    minPartitions=12  # Typically at 4*processors = 48. 12 for example data small size.
)

logger.info("Splitting games")
games_rdd = raw_rdd.mapPartitions(split_games)
logger.info("Parsing games")
parsed_rdd = games_rdd.mapPartitions(parse_partition)
logger.info("Creating Dataframes")

df = spark.createDataFrame(parsed_rdd, schema=schema)
df.show(5, truncate=False)

# Perform transformations
logger.info("Performing transformations")
df = df.filter(col("Move_Count") > 10)
# Keeps games no null Elo for very old historical games sake.
df = df.filter(
    (col("White_Elo").isNull()) |
    (col("Black_Elo").isNull()) |
    (spark_abs(col("White_Elo") - col("Black_Elo")) < 300)
)
# Write to parquet files to hdfs
logger.info("Writing parquet files to hdfs")
df = df.withColumn("year", split("UTC_Date", "\\.")[0]) \
    .withColumn("month", split("UTC_Date", "\\.")[1])
df = df.coalesce(2) # Typically "df = df.repartition(12)". Set at 2 for example data small size
df.write \
    .mode("append") \
    .partitionBy("year", "month") \
    .parquet("hdfs://namenode:9000/chess-data/processed/games")

rows = df.take(5)
logger.info(f"Sample rows: {rows}")
spark.stop()
logger.info("PGN processing complete")
