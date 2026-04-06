# Project Description
This project designs a distributed batch-processing system for large-scale chess game analytics. 
It consolidates and normalizes chess game archives from multiple sources, including online play 
(Lichess PGN archives) and historical professional databases, in order to consolidate key information such as opening
frequencies correlation to skill rating.

## Setup:
1. Move directories in docs/MockData to root/data. They contain truncated game data from actual runs.
   - The lichess data can be downloaded from https://database.lichess.org/#standard_games; files can be up to 900GB when unzipped, so I recommend using the example data.
2. Install and setup docker-compose if docker desktop or compose plugin if not already installed on device https://docs.docker.com/compose/install/
## How To Run:
1. Run file reduction script (Not required for example run)

## Environment Setup:
1. The environment is set up in dockerfile and docker compose yaml. Do not alter them.
## How To Run:
1. Run file reduction script (Not required for example run)
```
python src/ingestion/reduce_file.py
```
2. Build and run docker container
```
docker-compose up --build
```
## Project Status:
Currently, the file acquisition, file parsing tools, and storage system are all functional. The schema of data storage is roughly defined, but will likely be adjusted before the final version. Likewise, the data acquisition works as of now, but will likely be optimized in the future.
Other functionality that must also be done: the ingested data must still be normalized and cleaned.