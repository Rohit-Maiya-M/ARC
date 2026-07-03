# tests/consumer.py
from fastapi import FastAPI
from kafka import KafkaConsumer
from pymilvus import connections
import json
import threading
from app.services.vector_store_service import VectorStoreService

app = FastAPI()

vector_store_service = None

def ensure_services():
    global vector_store_service
    if vector_store_service is None:
        vector_store_service = VectorStoreService(dim=1024, collection_name="test_collection")

def consume_messages():
    consumer = KafkaConsumer(
        "arc.index",
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="arc-consumer-group",        
        value_deserializer=lambda x: x.decode("utf-8")
    )

    print("✅ Listening to Kafka topic 'arc.index'...")
    ensure_services()
    for message in consumer:        
        batch = json.loads(message.value)
        requests = batch["requests"]
        vector_store_service.store_batch(requests)
        print(f"✅ Processed batch with {len(requests)} items from Kafka")

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=consume_messages, daemon=True)
    thread.start()
