import pyspark.sql.functions as F
from pyspark.sql import SparkSession

# ------------------------------------------------------------------
# 1. CREATE SPARK SESSION
# ------------------------------------------------------------------
spark = SparkSession.builder \
    .appName("AmazonReviewsIngestion") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .getOrCreate()

print("\n🚀 Spark Session Started Successfully!")
print("📂 Loading cleaned dataset...\n")

# ------------------------------------------------------------------
# 2. LOAD CLEANED CSV (safe options)
# ------------------------------------------------------------------
df = spark.read.csv(
    "data/processed/cleaned_reviews.csv",
    header=True,
    inferSchema=True,
    escape='"',
    multiLine=True
)

print(f"📊 Loaded Rows: {df.count()}")
print("🧪 Sample Data:")
df.show(5, truncate=False)

# ------------------------------------------------------------------
# 3. FIX review_date COLUMN – SAFE CASTING
# ------------------------------------------------------------------
print("\n🔧 Cleaning and fixing review_date column...")

df = df.withColumn(
    "review_date_parsed",
    F.to_date("review_date", "yyyy-MM-dd")
)

df = df.filter(df.review_date_parsed.isNotNull())

print(f"📊 Valid rows after date fix: {df.count()}")

# Add review_length column early
df = df.withColumn("review_length", F.length(F.col("review_body")))
df.createOrReplaceTempView("reviews")

# ------------------------------------------------------------------
# 4. MONTHLY REVIEW TREND
# ------------------------------------------------------------------
print("\n📈 Generating Monthly Review Trend...")

monthly = spark.sql("""
    SELECT 
        date_format(review_date_parsed, 'yyyy-MM') AS month,
        COUNT(*) AS review_count
    FROM reviews
    GROUP BY 1
    ORDER BY 1
""")

monthly.show(20)
monthly.write.mode("overwrite").csv("data/processed/spark_output/monthly_reviews")
print("✔ Saved → monthly_reviews")

# ------------------------------------------------------------------
# 5. AVERAGE RATING PER PRODUCT
# ------------------------------------------------------------------
print("\n⭐ Generating Average Rating per Product...")

avg_ratings = df.groupBy("product_id") \
    .agg(F.avg("star_rating").alias("avg_rating")) \
    .orderBy(F.col("avg_rating").desc())

avg_ratings.show(20)
avg_ratings.write.mode("overwrite").csv("data/processed/spark_output/avg_ratings")
print("✔ Saved → avg_ratings")

# ------------------------------------------------------------------
# 6. REVIEW LENGTH VS RATING
# ------------------------------------------------------------------
print("\n📝 Generating Review Length Analysis...")

review_length_stats = df.groupBy("star_rating") \
    .agg(
        F.avg("review_length").alias("avg_review_length"),
        F.max("review_length").alias("max_review_length"),
        F.min("review_length").alias("min_review_length")
    ).orderBy("star_rating")

review_length_stats.show()
review_length_stats.write.mode("overwrite").csv("data/processed/spark_output/review_length_stats")
print("✔ Saved → review_length_stats")

# ------------------------------------------------------------------
# 7. COMPLEX QUERY (REPLACED helpful_votes QUERY)
# ------------------------------------------------------------------
print("\n🧠 Extracting Top Longest Reviews (instead of helpful reviews)...")

top_reviews = spark.sql("""
    SELECT 
        product_id,
        product_title,
        review_body,
        star_rating,
        review_length
    FROM reviews
    ORDER BY review_length DESC
    LIMIT 20
""")

top_reviews.show(20)
top_reviews.write.mode("overwrite").csv("data/processed/spark_output/top_longest_reviews")
print("✔ Saved → top_longest_reviews")

# ------------------------------------------------------------------
# 8. DONE
# ------------------------------------------------------------------
print("\n🎉 SPARK INGESTION COMPLETED SUCCESSFULLY!")
spark.stop()
