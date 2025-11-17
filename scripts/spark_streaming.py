from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

# -----------------------------
# 1. SPARK SESSION WITH KAFKA SUPPORT
# -----------------------------
spark = (
    SparkSession.builder
    .appName("AmazonReviewsStreaming")
    .master("local[*]")
    .config("spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
            "org.apache.kafka:kafka-clients:3.7.0")
    .config("spark.streaming.stopGracefullyOnShutdown", "true")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("🚀 Spark Streaming Consumer Started...\n")

# -----------------------------
# 2. SCHEMA FOR INCOMING JSON
# -----------------------------
schema = StructType() \
    .add("marketplace", StringType()) \
    .add("customer_id", StringType()) \
    .add("review_id", StringType()) \
    .add("product_id", StringType()) \
    .add("product_parent", StringType()) \
    .add("product_title", StringType()) \
    .add("star_rating", IntegerType()) \
    .add("review_body", StringType()) \
    .add("review_date", StringType())


# -----------------------------
# 3. READ STREAM FROM KAFKA
# -----------------------------
df_raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "amazon_reviews")
    .option("startingOffsets", "earliest")
    .load()
)

# Convert binary to string
df_str = df_raw.selectExpr("CAST(value AS STRING) as json")

# Parse nested JSON
df_parsed = df_str.select(from_json(col("json"), schema).alias("data")).select("data.*")


# -----------------------------
# 4. WRITE TO CONSOLE (TEST)
# -----------------------------
query = (
    df_parsed.writeStream
    .format("console")
    .option("truncate", False)
    .outputMode("append")
    .start()
)

query.awaitTermination()
