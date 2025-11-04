import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType
from pyspark.sql.functions import from_json, col, current_timestamp

# ==============================================================
# ⚙️ Absolute Hadoop-free Spark session
# ==============================================================

os.environ.pop("HADOOP_HOME", None)
os.environ.pop("HADOOP_CONF_DIR", None)
os.environ["SPARK_LOCAL_DIRS"] = r"D:\spark_local_tmp"
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

spark = (
    SparkSession.builder
    .appName("AmazonReviewStreaming_HadoopFree")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "1")
    .config("spark.sql.warehouse.dir", r"D:\spark_local_tmp\warehouse")
    .config("spark.driver.extraJavaOptions", "-Djava.library.path=")
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.RawLocalFileSystem")
    .config("spark.sql.streaming.checkpointLocation", r"D:\spark_local_tmp\checkpoints")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")
print("✅ Spark Streaming session started in Hadoop-FREE mode!\n")

# ==============================================================
# Schema
# ==============================================================

schema = (
    StructType()
    .add("product_id", StringType())
    .add("product_title", StringType())
    .add("star_rating", IntegerType())
    .add("review_body", StringType())
    .add("verified_purchase", StringType())
    .add("review_date", StringType())
    .add("product_category", StringType())
)

# ==============================================================
# Socket stream
# ==============================================================

raw_df = (
    spark.readStream.format("socket")
    .option("host", "localhost")
    .option("port", 9999)
    .load()
)

json_df = (
    raw_df.select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
    .withColumn("timestamp", current_timestamp())
)

agg_df = (
    json_df.groupBy("product_category")
    .agg({"star_rating": "avg", "*": "count"})
    .withColumnRenamed("avg(star_rating)", "avg_rating")
    .withColumnRenamed("count(1)", "review_count")
)

# ==============================================================
# Custom foreachBatch writer (pure Python)
# ==============================================================

def process_batch(batch_df, batch_id):
    out_dir = r"D:\spark_output_batches"
    os.makedirs(out_dir, exist_ok=True)
    out_file = f"{out_dir}\\batch_{batch_id}.csv"

    if batch_df.count() > 0:
        pdf = batch_df.toPandas()
        pdf.to_csv(out_file, index=False, encoding="utf-8")
        print(f"\n💾 Batch {batch_id} written to {out_file}")
        print(pdf)
    else:
        print(f"\n⚠️ Empty batch {batch_id}")

query = (
    agg_df.writeStream
    .outputMode("complete")
    .foreachBatch(process_batch)
    .trigger(processingTime="5 seconds")
    .start()
)

try:
    while query.isActive:
        time.sleep(5)
except KeyboardInterrupt:
    print("\n🛑 Stopping stream.")
    query.stop()
    spark.stop()
