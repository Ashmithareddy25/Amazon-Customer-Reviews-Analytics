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
    sample_df = df.sample(frac=frac, random_state=42)
    print(f"✅ Sampled {len(sample_df)} rows out of {len(df)}")
    return sample_df

# Get all .tsv.gz files
all_files = glob.glob(os.path.join(RAW_DIR, "*.tsv"))



samples = []
for file in tqdm(all_files, desc="Sampling from files"):
    try:
        samples.append(read_and_sample(file))
    except Exception as e:
        print(f"⚠️ Skipped {file} due to error: {e}")

# Combine all samples
if samples:
    combined = pd.concat(samples, ignore_index=True)
    out_path = os.path.join(SAMPLE_DIR, "amazon_reviews_sample.parquet")
    combined.to_parquet(out_path, index=False)
    print(f"\n✅ Wrote combined sample to {out_path} with {len(combined):,} rows.\n")
else:
    print("⚠️ No samples created. Check your input files.")
