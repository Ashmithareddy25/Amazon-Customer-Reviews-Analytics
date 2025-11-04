import pandas as pd
import glob
import os
from tqdm import tqdm

RAW_DIR = "data/raw"          # ✅ path to all TSVs
SAMPLE_DIR = "data/sample"
os.makedirs(SAMPLE_DIR, exist_ok=True)

def read_and_sample(file_path, frac=0.01):
    print(f"📂 Reading {os.path.basename(file_path)} ...")
    df = pd.read_csv(file_path, sep='\t', on_bad_lines='skip', low_memory=False)
    keep_cols = [c for c in df.columns if c in [
        "product_id", "product_title", "star_rating",
        "review_body", "verified_purchase", "review_date", "product_category"
    ]]
    df = df[keep_cols]
    sample_df = df.sample(frac=frac, random_state=42)
    print(f"✅ Sampled {len(sample_df)} of {len(df)}")
    return sample_df

all_files = glob.glob(os.path.join(RAW_DIR, "*.tsv"))
samples = [read_and_sample(f) for f in tqdm(all_files, desc="Sampling files")]

if samples:
    combined = pd.concat(samples, ignore_index=True)
    out_path = os.path.join(SAMPLE_DIR, "amazon_reviews_sample.parquet")
    combined.to_parquet(out_path, index=False)
    print(f"\n✅ Saved {len(combined):,} rows → {out_path}")
