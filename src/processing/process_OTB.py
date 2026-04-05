from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, size, lit
from pyspark.sql.functions import abs
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chess-pipeline")
handler = logging.FileHandler("/app/logs/pipeline.log")
logger.addHandler(handler)
# -------------------------------
# Spark setup (with SQLite JDBC)
# -------------------------------
spark = SparkSession.builder \
    .appName("Process OTB Database") \
    .master("local[*]") \
    .config("spark.driver.memory", "6g") \
    .config("spark.executor.memory", "6g") \
    .config( "spark.jars.packages","org.xerial:sqlite-jdbc:3.45.1.0,""org.mongodb.spark:mongo-spark-connector_2.12:10.6.1") \
    .config("spark.mongodb.write.connection.uri", "mongodb://mongodb:27017/chess.games") \
    .getOrCreate()

# -------------------------------
# Read SQLite via JDBC
# -------------------------------
logger.info("\n Processing OTB data.\n Reading sqlite data")
sqlite_df = spark.read.format("jdbc") \
    .option("url", "jdbc:sqlite:/app/data/raw/OTB_databases/LumbrasGigaBase2025-06.db3") \
    .option("dbtable", "games") \
    .option("driver", "org.sqlite.JDBC") \
    .load()


# -------------------------------
# Transform to unified schema
# -------------------------------
df = sqlite_df \
    .withColumn("moves", split(col("moves"), " ")) \
    .withColumn("num_moves", size(col("moves"))) \
    .withColumn("source", lit("otb")) \
    .withColumn("year", lit(None).cast("int")) \
    .withColumn("month", lit(None).cast("int")) \
    .withColumnRenamed("White", "white") \
    .withColumnRenamed("Black", "black") \
    .withColumnRenamed("Result", "result") \
    .withColumnRenamed("Event", "event") \
    .withColumnRenamed("WhiteElo", "white_elo") \
    .withColumnRenamed("BlackElo", "black_elo")


# -------------------------------
# Filters
# -------------------------------
logger.info("Filtering min moves.")
df = df.filter(col("num_moves") > 10)

# df = df.filter(
#     (col("white_elo").isNull()) |
#     (col("black_elo").isNull()) |
#     (abs(col("white_elo") - col("black_elo")) < 400)
# )

rows = df.take(5)
logger.info(f"Sample rows: {rows}")
# -------------------------------
# Write to MongoDB
# -------------------------------
df.write.format("mongodb") \
    .mode("append") \
    .save()

spark.stop()
print("OTB processing complete")