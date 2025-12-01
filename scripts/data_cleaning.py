import pandas as pd
import glob
import os

RAW_PATH = "data/raw/*.tsv"
OUTPUT_PATH = "data/processed/cleaned_reviews.csv"

# Limit number of files to process (set to None for all files)
MAX_FILES = 5  # Process only first 5 files to avoid memory issues

def clean_data():
    print("\n🚀 Starting STREAMING cleaning (write chunks directly to disk)...")

    files = glob.glob(RAW_PATH)
    if MAX_FILES:
        files = files[:MAX_FILES]
    print(f"📂 Processing {len(files)} raw files.\n")

    CHUNK_SIZE = 25000  # Smaller chunks for memory efficiency
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    first_write = True
    total_rows = 0

    for file in files:
        print(f"📥 Processing file in chunks: {file}")

        try:
            for chunk in pd.read_csv(
                file,
                sep="\t",
                chunksize=CHUNK_SIZE,
                dtype=str,
                on_bad_lines="skip",
                encoding="utf-8",
                encoding_errors="replace"
            ):
                # Convert numeric column safely
                chunk["star_rating"] = pd.to_numeric(chunk["star_rating"], errors="coerce")

                # Clean date column
                chunk["review_date"] = pd.to_datetime(chunk["review_date"], errors="coerce")

                # Drop rows with invalid values
                chunk = chunk.dropna(subset=["star_rating", "review_body"])

                # Write to CSV (append mode after first write)
                chunk.to_csv(
                    OUTPUT_PATH,
                    mode='w' if first_write else 'a',
                    header=first_write,
                    index=False
                )
                first_write = False
                total_rows += len(chunk)

        except Exception as e:
            print(f"⚠️ Error processing {file}: {e}")
            continue

    print("\n🎉 Streaming cleaning finished!")
    print(f"📁 Saved → {OUTPUT_PATH}")
    print(f"📊 Total rows → {total_rows:,}")

if __name__ == "__main__":
    clean_data()
