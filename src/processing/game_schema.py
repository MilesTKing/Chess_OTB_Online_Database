from pyspark.sql.types import *

schema = StructType([
    StructField("Event", StringType(), True),
    StructField("UTC_Date", StringType(), True),
    StructField("UTC_Time", StringType(), True),
    StructField("Time_Control", StringType(), False),
    StructField("White_Player", StringType(), False),
    StructField("Black_Player", StringType(), False),
    StructField("White_Elo", IntegerType(), True),
    StructField("Black_Elo", IntegerType(), True),
    StructField("Result", StringType(), False),
    StructField("Moves", ArrayType(StringType()), False),
    StructField("Move_Count", IntegerType(), False),
    StructField("ECO", StringType(), True),
])

