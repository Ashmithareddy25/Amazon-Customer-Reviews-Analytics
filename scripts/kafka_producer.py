import csv
import json
import time
from kafka import KafkaProducer

CSV_FILE = "data/processed/cleaned_reviews.csv"
TOPIC = "reviews_stream"

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("🚀 Kafka Producer connected!")
print("📤 Streaming data to Kafka...")

with open(CSV_FILE, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    
    for i, row in enumerate(reader):
        producer.send(TOPIC, row)
        
        if i % 5000 == 0:
            print(f"Sent {i} messages...")
            time.sleep(0.2)

print("🎉 Streaming complete!")
producer.flush()
producer.close()
