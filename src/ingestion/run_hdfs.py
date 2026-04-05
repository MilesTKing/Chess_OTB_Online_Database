from hdfs import InsecureClient

client = InsecureClient("http://namenode:9870", user="root")

client.makedirs("/chess-data/raw/pgn", permission=755)

client.upload(
    "/chess-data/raw/pgn",
    "/app/data/raw/pgn/super_reduced_lichess.pgn",
    overwrite=True
)