
schema = StructType([
    StructField("source", StringType(), True),
    StructField("event", StringType(), True),
    StructField("white", StringType(), True),
    StructField("black", StringType(), True),
    StructField("result", StringType(), True),
    StructField("moves", ArrayType(StringType()), True),
    StructField("num_moves", IntegerType(), True),
    StructField("white_elo", IntegerType(), True),
    StructField("black_elo", IntegerType(), True),
    StructField("year", IntegerType(), True),
    StructField("month", IntegerType(), True),
])