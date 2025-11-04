import pandas as pd
import os

# Path to your dataset
DATA_PATH = os.path.join("data", "sample", "amazon_reviews_sample.parquet")

# Read dataset
print("📥 Loading dataset...")
df = pd.read_parquet(DATA_PATH)
print(f"✅ Loaded {len(df)} rows")

# Clean data
df = df.dropna(subset=["review_body", "star_rating"])
df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
df = df[df["star_rating"].between(1, 5)]

# Preview cleaned data
print(df.head())

# Save cleaned file for dashboard
CLEANED_PATH = os.path.join("data", "sample", "amazon_reviews_cleaned.parquet")
df.to_parquet(CLEANED_PATH, index=False)
print(f"💾 Cleaned data saved to: {CLEANED_PATH}")
