import pandas as pd
import glob
import os

RAW_DIR = "data/raw"
OUTPUT_PATH = "data/processed/cleaned_reviews.csv"

MAX_FILES = None  # process all files

def load_file(file_path, chunk_size=25000):
    """Load CSV, TSV (chunked) or Parquet (full)."""
    if file_path.endswith(".parquet"):
        print(f"📥 Loading Parquet file: {file_path}")
        df = pd.read_parquet(file_path)
        return [df]  # return list for consistency

    if file_path.endswith(".csv"):
        print(f"📥 Loading CSV file in chunks: {file_path}")
        return pd.read_csv(
            file_path,
            chunksize=chunk_size,
            dtype=str,
            on_bad_lines="skip",
            encoding="utf-8",
            encoding_errors="replace"
        )

    if file_path.endswith(".tsv"):
        print(f"📥 Loading TSV file in chunks: {file_path}")
        return pd.read_csv(
            file_path,
            sep="\t",
            chunksize=chunk_size,
            dtype=str,
            on_bad_lines="skip",
            encoding="utf-8",
            encoding_errors="replace"
        )

    raise ValueError(f"❌ Unsupported file format: {file_path}")

def clean_data():
    print("\n🚀 Starting data cleaning ...")

    # List only valid data files (skip .gitkeep and hidden files)
    files = [
    os.path.join(RAW_DIR, f)
    for f in os.listdir(RAW_DIR)
    if not f.startswith(".")  # ignore .gitkeep and hidden files
       and (f.endswith(".parquet") or f.endswith(".csv") or f.endswith(".tsv"))
       ]

    if MAX_FILES:
        files = files[:MAX_FILES]
    print(f"📂 Found {len(files)} raw files.\n")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    first_write = True
    total_rows = 0

    for file in files:
        loaders = load_file(file)

        for chunk in loaders:
            # Clean columns
            if "star_rating" in chunk.columns:
                chunk["star_rating"] = pd.to_numeric(chunk["star_rating"], errors="coerce")

            if "review_date" in chunk.columns:
                chunk["review_date"] = pd.to_datetime(chunk["review_date"], errors="coerce")

            # Drop invalid rows
            valid_cols = [col for col in ["star_rating", "review_body"] if col in chunk.columns]
            chunk = chunk.dropna(subset=valid_cols)

            # Write to cleaned CSV
            chunk.to_csv(
                OUTPUT_PATH,
                mode='w' if first_write else 'a',
                header=first_write,
                index=False
            )

            first_write = False
            total_rows += len(chunk)

    print("\n🎉 Cleaning finished!")
    print(f"📁 Saved → {OUTPUT_PATH}")
    print(f"📊 Total rows → {total_rows:,}")

if __name__ == "__main__":
    clean_data()
