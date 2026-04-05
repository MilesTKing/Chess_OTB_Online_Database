from hdfs import InsecureClient

client = InsecureClient("http://namenode:9870", user="root")

client.makedirs("/chess-data/raw/lichess", permission=755)

client.upload(
    "/chess-data/raw/lichess",
    "/app/data/raw/lichess/reduced_lichess.pgn",
    overwrite=True
)