from hdfs import InsecureClient

client = InsecureClient('http://localhost:9870', user='root')

# Create directory
client.makedirs('/chess-data/raw/lichess')

# Upload file
client.upload('/chess-data/raw/lichess', '../../data/raw/lichess/reduced_lichess.pgn', overwrite=True)
client.upload('/chess-data/raw/OTB_databases', '../../data/raw/OTB_databases/LumbrasGigaBase2025-06.db3', overwrite=True)