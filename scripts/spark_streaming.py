import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, when
from functools import reduce

# Folder paths
INPUT_FOLDER = "data/stream_input/"
OUTPUT_CSV = "data/output_csv/"
OUTPUT_PARQUET = "data/output_parquet/"

# Ensure folders exist
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_CSV, exist_ok=True)
os.makedirs(OUTPUT_PARQUET, exist_ok=True)

# Start Spark
spark = SparkSession.builder \
    .appName("Amazon Reviews - File Streaming Pipeline") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("==============================================")
print(" Spark Streaming Started...")
print(f" Watching folder: {INPUT_FOLDER}")
print("==============================================\n")

# ----------------------------------------------------------------------
# 1. READ STREAMING TEXT FILES
# ----------------------------------------------------------------------

raw_stream = spark.readStream \
    .format("text") \
    .load(INPUT_FOLDER)

# ----------------------------------------------------------------------
# 2. SPLIT TEXT → STRUCTURED COLUMNS
# Format: product_id | rating | review_text
# ----------------------------------------------------------------------

json_df = raw_stream.select(
    split(col("value"), "\\|")[0].alias("product_id"),
    split(col("value"), "\\|")[1].cast("int").alias("rating"),
    split(col("value"), "\\|")[2].alias("review_text")
)

# ----------------------------------------------------------------------
# 3. SENTIMENT ANALYSIS (WORKING VERSION)
# ----------------------------------------------------------------------

positive_words = ["good", "great", "excellent", "love", "amazing", "awesome", "fantastic"]
negative_words = ["bad", "terrible", "worst", "hate", "awful", "poor"]

# Create OR conditions
positive_condition = reduce(lambda a, b: a | b, [col("review_text").rlike(w) for w in positive_words])
negative_condition = reduce(lambda a, b: a | b, [col("review_text").rlike(w) for w in negative_words])

sentiment_df = json_df.withColumn(
    "sentiment",
    when(positive_condition, "positive")
    .when(negative_condition, "negative")
    .otherwise("neutral")
)

# ----------------------------------------------------------------------
# 4. WRITE STREAM TO CONSOLE (LIVE OUTPUT)
# ----------------------------------------------------------------------

console_query = sentiment_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

# ----------------------------------------------------------------------
# 5. WRITE STREAM TO CSV
# ----------------------------------------------------------------------

csv_query = sentiment_df.writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("header", True) \
    .option("path", OUTPUT_CSV) \
    .option("checkpointLocation", OUTPUT_CSV + "_checkpoint") \
    .start()

# ----------------------------------------------------------------------
# 6. WRITE STREAM TO PARQUET
# ----------------------------------------------------------------------

parquet_query = sentiment_df.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", OUTPUT_PARQUET) \
    .option("checkpointLocation", OUTPUT_PARQUET + "_checkpoint") \
    .start()

# Wait for stream to run forever
console_query.awaitTermination()
csv_query.awaitTermination()
parquet_query.awaitTermination()
