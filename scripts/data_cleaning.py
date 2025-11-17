import pandas as pd
import os
import glob
import pyarrow as pa
import pyarrow.parquet as pq

RAW_PATH = "data/raw/"
OUTPUT_PATH = "data/sample/amazon_reviews_cleaned.parquet"

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

print("📥 Loading raw Amazon review files...")

tsv_files = glob.glob(os.path.join(RAW_PATH, "*.tsv"))

if not tsv_files:
    raise FileNotFoundError("❌ No TSV files found in data/raw/.")

print(f"Found {len(tsv_files)} files.")

writer = None

# Force a global schema (same for every chunk)
schema = pa.schema([
    ("marketplace", pa.string()),
    ("customer_id", pa.int64()),
    ("review_id", pa.string()),
    ("product_id", pa.string()),
    ("product_parent", pa.int64()),
    ("product_title", pa.string()),
    ("product_category", pa.string()),
    ("star_rating", pa.int32()),
    ("helpful_votes", pa.int64()),
    ("total_votes", pa.int64()),
    ("vine", pa.string()),
    ("verified_purchase", pa.string()),
    ("review_headline", pa.string()),
    ("review_body", pa.string()),
    ("review_date", pa.timestamp("ns")),
    ("review_length", pa.int64()),
    ("verified_flag", pa.int64()),
    ("helpful_ratio", pa.float64()),
    ("year", pa.int32()),
    ("month", pa.int32()),
    ("sentiment_score", pa.float64()),
    ("is_helpful", pa.int64())
])

# Process in chunks
for file in tsv_files:
    print(f"➡️ Processing file: {file}")

    for chunk in pd.read_csv(
        file,
        sep="\t",
        on_bad_lines="skip",
        low_memory=False,
        chunksize=100_000
    ):
        # Drop missing essentials
        chunk = chunk.dropna(subset=["review_body", "star_rating"])

        # Convert star rating
        chunk["star_rating"] = pd.to_numeric(chunk["star_rating"], errors="coerce")
        chunk = chunk.dropna(subset=["star_rating"])
        chunk["star_rating"] = chunk["star_rating"].astype(int)
        chunk = chunk[chunk["star_rating"].between(1, 5)]

        # Date
        chunk["review_date"] = pd.to_datetime(chunk["review_date"], errors="coerce")

        # ENGINEERING
        chunk["review_length"] = chunk["review_body"].astype(str).apply(lambda x: len(x.split()))
        chunk["verified_flag"] = chunk["verified_purchase"].apply(lambda x: 1 if x == "Y" else 0)

        # FORCE helpful_votes & total_votes numeric
        chunk["helpful_votes"] = pd.to_numeric(chunk["helpful_votes"], errors="coerce").fillna(0).astype("int64")
        chunk["total_votes"] = pd.to_numeric(chunk["total_votes"], errors="coerce").fillna(0).astype("int64")

        # Derived columns
        chunk["helpful_ratio"] = chunk["helpful_votes"] / (chunk["total_votes"] + 1)
        chunk["year"] = chunk["review_date"].dt.year.astype("Int32")
        chunk["month"] = chunk["review_date"].dt.month.astype("Int32")
        chunk["sentiment_score"] = 0.0
        chunk["is_helpful"] = chunk["helpful_votes"].apply(lambda x: 1 if x > 0 else 0)

        # Convert chunk to Arrow Table with schema
        table = pa.Table.from_pandas(chunk, schema=schema, preserve_index=False)

        if writer is None:
            writer = pq.ParquetWriter(OUTPUT_PATH, schema)

        writer.write_table(table)

# Close the writer
if writer:
    writer.close()

print("🎉 Chunked cleaning + Parquet writing COMPLETED SUCCESSFULLY!")
print(f"📂 Cleaned dataset saved at: {OUTPUT_PATH}")
