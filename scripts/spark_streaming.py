"""
Streaming Pipeline for Amazon Reviews (Pure Python/Pandas)
Reads batch files from stream_input/ and outputs processed data to output_csv/ and output_parquet/

This version uses pure Python and Pandas for Windows compatibility (no Hadoop required).
"""

import os
import sys
import time
import glob
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

# Folder paths - Use absolute paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FOLDER = os.path.join(BASE_DIR, "data", "stream_input")
OUTPUT_CSV = os.path.join(BASE_DIR, "data", "output_csv")
OUTPUT_PARQUET = os.path.join(BASE_DIR, "data", "output_parquet")
CHECKPOINT_FILE = os.path.join(BASE_DIR, "data", "checkpoints", "processed_files.json")

# Ensure folders exist
for folder in [INPUT_FOLDER, OUTPUT_CSV, OUTPUT_PARQUET, os.path.dirname(CHECKPOINT_FILE)]:
    os.makedirs(folder, exist_ok=True)

print("=" * 60)
print(" STREAMING PIPELINE (Pure Python/Pandas)")
print("=" * 60)
print(f" Input:    {INPUT_FOLDER}")
print(f" CSV Out:  {OUTPUT_CSV}")
print(f" Parquet:  {OUTPUT_PARQUET}")
print("=" * 60)

# Sentiment words for analysis
POSITIVE_WORDS = {"good", "great", "excellent", "love", "amazing", "awesome", 
                  "fantastic", "best", "perfect", "wonderful", "happy", "satisfied",
                  "recommend", "beautiful", "quality", "pleased", "works"}
NEGATIVE_WORDS = {"bad", "terrible", "worst", "hate", "awful", "poor", 
                  "horrible", "broken", "waste", "disappointed", "useless", "defective",
                  "return", "refund", "cheap", "fail", "doesn't work", "not working"}

def analyze_sentiment(text):
    """Analyze sentiment of text using keyword matching"""
    if pd.isna(text) or text is None:
        return "neutral"
    text_lower = str(text).lower()
    pos_count = sum(1 for w in POSITIVE_WORDS if w in text_lower)
    neg_count = sum(1 for w in NEGATIVE_WORDS if w in text_lower)
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"

def load_checkpoint():
    """Load list of already processed files"""
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, 'r') as f:
                data = json.load(f)
                return set(data.get('processed_files', []))
        except:
            return set()
    return set()

def save_checkpoint(processed_files):
    """Save list of processed files"""
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump({
            'processed_files': list(processed_files),
            'last_updated': datetime.now().isoformat()
        }, f)

def get_next_batch_number():
    """Get next batch number based on existing files"""
    existing_csv = glob.glob(os.path.join(OUTPUT_CSV, "spark_batch_*.csv"))
    if not existing_csv:
        return 1
    numbers = []
    for f in existing_csv:
        try:
            num = int(os.path.basename(f).replace("spark_batch_", "").replace(".csv", ""))
            numbers.append(num)
        except:
            pass
    return max(numbers) + 1 if numbers else 1

def process_file(filepath):
    """Process a single batch file and return DataFrame"""
    records = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        try:
                            records.append({
                                'product_id': parts[0],
                                'rating': int(parts[1]) if parts[1].isdigit() else 3,
                                'review_text': parts[2] if len(parts) > 2 else ''
                            })
                        except:
                            pass
    except Exception as e:
        print(f"  ⚠️ Error reading {filepath}: {e}")
    
    if records:
        df = pd.DataFrame(records)
        df['sentiment'] = df['review_text'].apply(analyze_sentiment)
        df['processed_at'] = datetime.now().isoformat()
        return df
    return None

def run_streaming(max_batches=None, batch_size=5, interval=5, continuous=True):
    """
    Run the streaming pipeline
    
    Args:
        max_batches: Maximum number of batches to process (None = unlimited)
        batch_size: Number of input files per batch
        interval: Seconds between batch processing
        continuous: If True, keep running. If False, process existing files once.
    """
    processed_files = load_checkpoint()
    batch_number = get_next_batch_number()
    batches_processed = 0
    total_records = 0
    
    print(f"\n📊 Starting from batch {batch_number}")
    print(f"   Already processed: {len(processed_files)} files")
    
    # Get all input files
    all_input_files = sorted(glob.glob(os.path.join(INPUT_FOLDER, "batch_*.txt")))
    print(f"   Total input files: {len(all_input_files)}")
    
    # Filter to unprocessed files
    unprocessed_files = [f for f in all_input_files if os.path.basename(f) not in processed_files]
    print(f"   Unprocessed files: {len(unprocessed_files)}")
    
    if not unprocessed_files:
        print("\n✅ All files have been processed!")
        return
    
    print(f"\n🚀 Starting streaming... (Ctrl+C to stop)")
    print(f"   Processing {batch_size} files every {interval} seconds\n")
    
    try:
        while True:
            # Get next batch of unprocessed files
            files_to_process = unprocessed_files[:batch_size]
            
            if not files_to_process:
                if continuous:
                    print(f"\r⏳ Waiting for new files... ({len(processed_files)} processed)", end='', flush=True)
                    time.sleep(interval)
                    # Refresh file list
                    all_input_files = sorted(glob.glob(os.path.join(INPUT_FOLDER, "batch_*.txt")))
                    unprocessed_files = [f for f in all_input_files if os.path.basename(f) not in processed_files]
                    continue
                else:
                    break
            
            # Process batch
            print(f"\n{'='*50}")
            print(f"📦 Batch {batch_number}: Processing {len(files_to_process)} files...")
            
            batch_dfs = []
            for filepath in files_to_process:
                df = process_file(filepath)
                if df is not None and len(df) > 0:
                    batch_dfs.append(df)
                processed_files.add(os.path.basename(filepath))
            
            if batch_dfs:
                # Combine all DataFrames
                combined_df = pd.concat(batch_dfs, ignore_index=True)
                record_count = len(combined_df)
                total_records += record_count
                
                # Write to CSV
                csv_path = os.path.join(OUTPUT_CSV, f"spark_batch_{batch_number}.csv")
                combined_df.to_csv(csv_path, index=False)
                print(f"  ✅ CSV: {csv_path} ({record_count} rows)")
                
                # Write to Parquet
                parquet_path = os.path.join(OUTPUT_PARQUET, f"spark_batch_{batch_number}.parquet")
                combined_df.to_parquet(parquet_path, index=False)
                print(f"  ✅ Parquet: {parquet_path}")
                
                # Show stats
                sentiment_counts = combined_df['sentiment'].value_counts().to_dict()
                avg_rating = combined_df['rating'].mean()
                print(f"  📊 Avg Rating: {avg_rating:.2f}")
                print(f"  📊 Sentiment: {sentiment_counts}")
                
                # Show sample
                print(f"\n  Sample data:")
                print(combined_df[['product_id', 'rating', 'sentiment']].head(3).to_string(index=False))
                
                batch_number += 1
                batches_processed += 1
            
            # Save checkpoint
            save_checkpoint(processed_files)
            
            # Remove processed files from list
            unprocessed_files = unprocessed_files[batch_size:]
            
            # Check max batches
            if max_batches and batches_processed >= max_batches:
                print(f"\n✅ Reached max batches ({max_batches})")
                break
            
            # Wait before next batch
            if continuous or unprocessed_files:
                time.sleep(interval)
                
    except KeyboardInterrupt:
        print("\n\n⏹️ Stopping stream...")
    
    # Final report
    csv_files = glob.glob(os.path.join(OUTPUT_CSV, "spark_batch_*.csv"))
    parquet_files = glob.glob(os.path.join(OUTPUT_PARQUET, "spark_batch_*.parquet"))
    
    print("\n" + "=" * 60)
    print(" STREAMING COMPLETE")
    print("=" * 60)
    print(f" Batches processed:     {batches_processed}")
    print(f" Total records:         {total_records}")
    print(f" CSV files created:     {len(csv_files)}")
    print(f" Parquet files created: {len(parquet_files)}")
    print(f" Files tracked:         {len(processed_files)}")
    print("=" * 60)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Amazon Reviews Streaming Pipeline")
    parser.add_argument("--batches", type=int, default=None, help="Max batches to process (default: unlimited)")
    parser.add_argument("--batch-size", type=int, default=5, help="Files per batch (default: 5)")
    parser.add_argument("--interval", type=int, default=5, help="Seconds between batches (default: 5)")
    parser.add_argument("--once", action="store_true", help="Process existing files once and exit")
    
    args = parser.parse_args()
    
    run_streaming(
        max_batches=args.batches,
        batch_size=args.batch_size,
        interval=args.interval,
        continuous=not args.once
    )
