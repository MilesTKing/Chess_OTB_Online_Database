import chess.pgn as chess
import pyspark
from pyspark.sql import SparkSession
from hdfs import InsecureClient


def split_games(partition):
    print("in function.")
    buffer = ""
    for line in partition:
        print("line.")
        if "[Event" in line and buffer: 
            yield buffer
            buffer = ""
        else:
            buffer += line + "\n"
    if buffer:
        yield buffer
        
client = InsecureClient('http://localhost:9870', user='root')
spark = SparkSession.builder \
    .appName("Chess Data Processing") \
    .master("local[*]") \
    .config("spark.driver.memory", "6g") \
    .config("spark.executor.memory", "6g") \
    .getOrCreate()
spark = spark.sparkContext

raw_games = spark.textFile(
    "hdfs://namenode:9000/chess-data/raw/lichess/reduced_lichess.pgn",
    minPartitions=100
)
print("poopie")

raw_games.mapPartitions(split_games)

def parse_game(pgn_text):
    try:
        game = chess.read_game(pgn_text)
        print(str(game))
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

    except Exception as e:
        return None

parsed_rdd = raw_games.map(parse_game)
