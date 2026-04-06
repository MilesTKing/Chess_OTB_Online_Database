import chess.pgn
import io
from pyspark.sql import SparkSession
import logging
from src.processing.game_schema import schema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chess-pipeline")
handler = logging.FileHandler("/app/logs/pipeline.log")
logger.addHandler(handler)

spark = SparkSession.builder \
    .appName("Process PGN") \
    .master("local[*]") \
    .config("spark.driver.memory", "6g") \
    .config("spark.executor.memory", "6g") \
    .config("spark.jars.packages","org.mongodb.spark:mongo-spark-connector_2.12:10.6.1") \
    .config("spark.mongodb.write.connection.uri", "mongodb://mongodb:27017/chess.games") \
    .getOrCreate()
sc = spark.sparkContext 
# -------------------------------
# Split PGN into games
# -------------------------------
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

# -------------------------------
# Parse PGN
# -------------------------------
def parse_game(pgn_text):
    try:
        game = chess.pgn.read_game(io.StringIO(pgn_text))
        if game is None:
            return None

        headers = game.headers

        moves = []
        node = game
        while node.variations:
            node = node.variation(0)
            moves.append(node.move.uci())

        return {
            "Event": headers.get("Event"),
            "UTC_Date": headers.get("UTCDate"),
            "UTC_Time": headers.get("UTCTime"),
            "Time_Control": headers.get("TimeControl"),
            "White_Player": headers.get("White"),
            "Black_Player": headers.get("Black"),
            "White_Elo": int(headers.get("WhiteElo")) if headers.get("WhiteElo") else None,
            "Black_Elo": int(headers.get("BlackElo")) if headers.get("BlackElo") else None,
            "Result": headers.get("Result"),
            "Moves": moves,
            "Move_Count": len(moves),
            "Eco": headers.get("ECO"),
        }

    except Exception:
        return None


# -------------------------------
# Main
# -------------------------------

raw_rdd = sc.textFile(
    "hdfs://namenode:9000/chess-data/raw/pgn/super_reduced_lichess.pgn",
    minPartitions=100
)
logger.info("Splitting games")
games_rdd = raw_rdd.mapPartitions(split_games)
logger.info("Parsing games")
parsed_rdd = games_rdd.map(parse_game).filter(lambda x: x is not None)
logger.info("Creating Dataframes")

schema = schema

df = spark.createDataFrame(parsed_rdd, schema=schema)
df.printSchema()
df.show(5,truncate=False)
# -------------------------------
# Filters / transformations
# -------------------------------
# df = df.filter(df.num_moves > 10)

# -------------------------------
# Write to MongoDB
# -------------------------------
df.write.format("mongodb") \
    .mode("append") \
    .save()


rows = df.take(5)
logger.info(f"Sample rows: {rows}")
spark.stop()
logger.info("PGN processing complete")