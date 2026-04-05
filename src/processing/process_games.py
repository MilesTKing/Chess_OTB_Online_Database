import chess.pgn
import io
import logging
from pyspark.sql import SparkSession


# -------------------------------
# 1. Spark setup
# -------------------------------
logging.basicConfig(level=logging.INFO)

spark = SparkSession.builder \
    .appName("Chess Data Processing") \
    .master("local[*]") \
    .config("spark.driver.memory", "6g") \
    .config("spark.executor.memory", "6g") \
    .getOrCreate()

sc = spark.sparkContext


# -------------------------------
# 2. Read raw PGN from HDFS
# -------------------------------
raw_rdd = sc.textFile(
    "hdfs://namenode:9000/chess-data/raw/lichess/reduced_lichess.pgn",
    minPartitions=100
)


# -------------------------------
# 3. Split into individual games
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


games_rdd = raw_rdd.mapPartitions(split_games)


# -------------------------------
# 4. Parse each game
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
            "event": headers.get("Event"),
            "white": headers.get("White"),
            "black": headers.get("Black"),
            "result": headers.get("Result"),
            "moves": moves,
            "num_moves": len(moves)
        }

    except Exception:
        return None


parsed_rdd = games_rdd.map(parse_game).filter(lambda x: x is not None)


# -------------------------------
# 5. Convert to DataFrame
# -------------------------------
df = spark.createDataFrame(parsed_rdd)


# -------------------------------
# 6. Clean data
# -------------------------------
df = df.filter(df.num_moves > 0)


# -------------------------------
# 7. Write to HDFS
# -------------------------------
df.write.mode("overwrite").parquet(
    "hdfs://namenode:9000/chess-data/processed/games"
)


# -------------------------------
# 8. Stop Spark
# -------------------------------
spark.stop()

print("done")