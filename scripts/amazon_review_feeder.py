import time
import pandas as pd
import os

SOURCE = "data/processed/cleaned_reviews.csv"
DEST = "data/stream_input/"
CHUNK_SIZE = 1000   # number of reviews per batch
SLEEP_TIME = 2      # seconds between batches

os.makedirs(DEST, exist_ok=True)

df = pd.read_csv(SOURCE)

print("Starting continuous review streaming...")
print(f"Total reviews: {len(df)}")
print("Streaming reviews into:", DEST)

batch_number = 1
start = 0

while start < len(df):
    end = start + CHUNK_SIZE
    chunk = df.iloc[start:end]

    filename = f"{DEST}/batch_{batch_number}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        for _, row in chunk.iterrows():
            product = str(row["product_id"])
            rating = str(row["star_rating"])
            review = str(row["review_body"]).replace("|", " ")
            f.write(f"{product}|{rating}|{review}\n")

    print(f"📦 Written batch {batch_number} ({len(chunk)} reviews)")
    
    batch_number += 1
    start = end
    
    time.sleep(SLEEP_TIME)

print("✔ ALL reviews streamed.")
