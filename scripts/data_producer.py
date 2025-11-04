import socket, time, json, pandas as pd

SAMPLE_PATH = "data/sample/amazon_reviews_sample.parquet"
HOST, PORT = "localhost", 9999

print("📂 Loading dataset...")
df = pd.read_parquet(SAMPLE_PATH)
print(f"✅ Loaded {len(df):,} reviews for streaming.\n")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"🚀 Producer started on {HOST}:{PORT}")
conn, addr = server.accept()
print(f"✅ Spark connected from {addr}\n")

for _, row in df.iterrows():
    record = row.to_dict()
    conn.send((json.dumps(record) + "\n").encode("utf-8"))
    print("📤 Sent:", record.get("product_title", "Unknown"))
    time.sleep(1)
