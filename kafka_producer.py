import pandas as pd
from kafka import KafkaProducer
import json
import time

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Load the dataset
df = pd.read_csv("cleaned_l2_orderbook.csv")

# Convert 'ts_event' to string and filter by time range
df['ts_event'] = df['ts_event'].astype(str)
df = df[df['ts_event'].between("13:36:32", "13:45:14")]

# Optional: sort by timestamp
df = df.sort_values(by='ts_event')

print("📡 Starting Kafka data stream...")

for idx, row in df.iterrows():
    snapshot = {
        "timestamp": row["ts_event"],               # changed from ts_event
        "venue_id": row["publisher_id"],            # changed from venue
        "ask_price": float(row["ask_px_00"]),       # changed from ask_px
        "ask_size": int(row["ask_sz_00"])           # changed from ask_sz
    }
    producer.send("mock_l1_stream", value=snapshot)
    print(f"📤 Sent: {snapshot}")
    time.sleep(0.01)

print("✅ Kafka data stream completed.")
