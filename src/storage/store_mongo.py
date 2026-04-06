from pyspark.sql import SparkSession
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mongo-loader")

spark = SparkSession.builder \
    .appName("Save Files to MongoDB") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.6.1") \
    .config("spark.mongodb.write.connection.uri", "mongodb://mongodb:27017/chess.games") \
    .getOrCreate()

logger.info("Reading processed files from HDFS")

df = spark.read.parquet("hdfs://namenode:9000/chess-data/processed/games")
df = df.repartition(8)

logger.info("Uploading files")

df.write \
    .format("mongodb") \
    .mode("append") \
    .save()

logger.info("Upload complete")

spark.stop()