from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType
from pyspark.sql.functions import from_json, col, current_timestamp

spark = SparkSession.builder.appName("AmazonReviewStreaming").getOrCreate()

schema = StructType() \
    .add("product_id", StringType()) \
    .add("product_title", StringType()) \
    .add("star_rating", IntegerType()) \
    .add("review_body", StringType()) \
    .add("verified_purchase", StringType()) \
    .add("review_date", StringType()) \
    .add("product_category", StringType())

raw_df = spark.readStream.format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

json_df = raw_df.select(from_json(col("value"), schema).alias("data")).select("data.*")
json_df = json_df.withColumn("timestamp", current_timestamp())

query = json_df.writeStream.outputMode("append").format("console").option("truncate", False).start()
query.awaitTermination()
