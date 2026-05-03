# Project Description
This project designs a distributed batch-processing system for large-scale chess game analytics.   
It consolidates and normalizes chess game archives from multiple sources, including online play   
(Lichess PGN archives) and historical professional databases, in order to consolidate key information such as opening  
frequencies correlation to skill rating.
# Technology Choices
 I used a local instance of the Hadoop File System for the robust replication factor for the data 
 integrity of the large, manually downloaded data files. For processing, I used Spark for the parallel 
 processing capabilities. The processed games are stored as parquet files to significantly reduce the 
 overall storage size and to make the large game files into smaller chunks to make them more manageable.
 I selected MongoDB as my database to enable querying because it allows for flexible data storage for 
 games with a wide variety of headers and move notation. I used Docker to provide a robust runtime
 for the local HDFS instance and to simplify networking between HDFS, Spark, and MongoDB.
## Setup:
1. Move directories in docs/MockData to root/data/raw. They contain truncated game data from actual runs.
   - The lichess data can be downloaded from https://database.lichess.org/#standard_games; files can be up to 900GB when unzipped, so I recommend using the example data.
   - The over the board data can be downloaded at https://lumbrasgigabase.com/en/download-in-pgn-format-en/
2. Install and setup Docker Desktop https://www.docker.com/get-started/
3. Open Docker Desktop to run Docker engine
## Environment Setup:
1. The environment is set up in dockerfile and docker compose yaml. Do not alter them.

## How To Run
1. Run file reduction script (Not required for example run).
```  
python src/ingestion/reduce_file.py  
```  
2. Build and run docker container in project terminal
```  
docker compose up --build  
```  
3. More succinct logs than in terminal can be found in logs/pipeline.logs.
4. To see example of data stored in MongoDB, run:
```  
python src/storage/test_mongo.py  
```  
## Output Description
The pipeline ultimately produces a Mongodb database that contains the transformed data which can be queried according to the schema.
The schema below reflects the data stored in each parquet and Mongodb record for each game. 
The given fields were selected to give as much relevant information as possible while 
If desired, each processed record can easily be extracted back into pgn format, as shown in the example below.

### Schema

| Field | Data Type | Nullable |
|---|---|----------|
|Event|String| Yes      |
|UTC_Date|String| Yes      |
|UTC_Time|String| Yes      |
|Time_Control|String| Yes      |
|White_Player|String| No       |
|Black_Player|String| No       |
|White_Elo|Integer| Yes      |
|Black_Elo|Integer| Yes      |
|Result|String| No       |
|Moves|String Array| No       |
|Move_Count|Integer| Yes      |
|ECO|String| Yes      |
|Round|String| Yes      |
|Rating_Type|String| No       |

### Sample Output
![Example Transformation](docs/Screenshots/Transformation_Example.png "Example Transformation")
## Project Status
The data pipeline has been implemented end to end. Monthly lichess archive files can range from 200-900GB, 
which makes automating the pipeline from data collection to processing improbable. 

## Acknowledgements
My name is Miles King. At the time of the project's initial completion, I am a senior undergraduate Computer Science
student at Kennesaw State University. This pipeline was a part of a semester long assignment for a Big Data course
which demonstrates some of the skills developed in the course.