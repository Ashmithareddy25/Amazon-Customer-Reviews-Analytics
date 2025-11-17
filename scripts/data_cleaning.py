import pandas as pd
import glob
import os

RAW_PATH = "data/raw/*.tsv"
OUTPUT_PATH = "data/processed/cleaned_reviews.csv"

def clean_data():
    print("\n🚀 Starting CHUNK-BASED cleaning...")

    files = glob.glob(RAW_PATH)
    print(f"📂 Found {len(files)} raw files.\n")

    cleaned_chunks = []
    CHUNK_SIZE = 50000

    for file in files:
        print(f"📥 Processing file in chunks: {file}")

        for chunk in pd.read_csv(
            file,
            sep="\t",
            chunksize=CHUNK_SIZE,
            dtype=str,
            on_bad_lines="skip"
        ):
            # Convert numeric column safely
            chunk["star_rating"] = pd.to_numeric(chunk["star_rating"], errors="coerce")

            # Clean date column
            chunk["review_date"] = pd.to_datetime(chunk["review_date"], errors="coerce")

            # Drop rows with invalid values
            chunk = chunk.dropna(subset=["star_rating", "review_body"])

            cleaned_chunks.append(chunk)

    print("\n🔗 Combining all chunks...")
    df = pd.concat(cleaned_chunks, ignore_index=True)

    df.drop_duplicates(inplace=True)

    print("💾 Saving cleaned CSV...")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\n🎉 Chunk cleaning finished!")
    print(f"📁 Saved → {OUTPUT_PATH}")
    print(f"📊 Total rows → {len(df):,}")

if __name__ == "__main__":
    clean_data()
