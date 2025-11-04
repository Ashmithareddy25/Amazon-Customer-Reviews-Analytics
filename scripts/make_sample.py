import pandas as pd
import glob
import os
from tqdm import tqdm

RAW_DIR = "data/raw"
SAMPLE_DIR = "data/sample"
os.makedirs(SAMPLE_DIR, exist_ok=True)

def read_and_sample(file_path, frac=0.01):
    print(f"📂 Reading {os.path.basename(file_path)} ...")
    df = pd.read_csv(file_path, sep='\t', on_bad_lines='skip', low_memory=False)

    # Keep only relevant columns
    keep_cols = [col for col in df.columns if col in [
        "product_id", "product_title", "star_rating",
        "review_body", "verified_purchase", "review_date", "product_category"
    ]]
    df = df[keep_cols]

    # 🔧 Convert data types safely
    if "star_rating" in df.columns:
        df["star_rating"] = pd.to_numeric(df["star_rating"], errors="coerce").fillna(0).astype(int)
    if "review_date" in df.columns:
        df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    if "verified_purchase" in df.columns:
        df["verified_purchase"] = df["verified_purchase"].astype(str)

    # Take 1% random sample (adjust if needed)
    sample_df = df.sample(frac=frac, random_state=42)
    print(f"✅ Sampled {len(sample_df)} rows out of {len(df)} from {os.path.basename(file_path)}")
    return sample_df

# Collect all .tsv files
all_files = glob.glob(os.path.join(RAW_DIR, "*.tsv"))
samples = []

for file in tqdm(all_files, desc="Sampling from files"):
    try:
        samples.append(read_and_sample(file))
    except Exception as e:
        print(f"⚠️ Skipped {file} due to error: {e}")

# Combine and save
if samples:
    combined = pd.concat(samples, ignore_index=True)
    out_path = os.path.join(SAMPLE_DIR, "amazon_reviews_sample.parquet")

    print(f"\n🧹 Cleaning combined data types before saving ...")
    # Final cleanup before saving to parquet
    combined["star_rating"] = pd.to_numeric(combined["star_rating"], errors="coerce").fillna(0).astype(int)
    combined["verified_purchase"] = combined["verified_purchase"].astype(str)

    combined.to_parquet(out_path, index=False)
    print(f"✅ Wrote combined sample to {out_path} with {len(combined):,} rows.\n")
else:
    print("⚠️ No samples created. Check your input files.")
