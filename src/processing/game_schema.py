from pyspark.sql.types import *

schema = StructType([
    StructField("Event", StringType(), True),
    StructField("UTC_Date", StringType(), True),
    StructField("UTC_Time", StringType(), True),
    StructField("Time_Control", StringType(), True),
    StructField("White_Player", StringType(), True),
    StructField("Black_Player", StringType(), True),
    StructField("White_Elo", IntegerType(), True),
    StructField("Black_Elo", IntegerType(), True),
    StructField("Result", StringType(), True),
    StructField("Moves", ArrayType(StringType()), True),
    StructField("Move_Count", IntegerType(), True),
    StructField("ECO", StringType(), True),
    StructField("Round", StringType(), True),
    StructField("Rating_Type", StringType(), True),
])

