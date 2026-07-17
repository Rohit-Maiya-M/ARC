import os
import json
import threading
from kafka import KafkaConsumer
from app.services.vector_store_service import VectorStoreService

class KafkaConsumerService:
    def __init__(self, topic: str = None, bootstrap_servers: list = None):
        # Resolve array elements from env configurations cleanly
        env_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        default_servers = [env_servers] if env_servers else ["arc-kafka:9092"]
        
        self.topic = topic or os.getenv("KAFKA_INDEX_TOPIC", "arc.index")
        self.bootstrap_servers = bootstrap_servers or default_servers
        self.consumer_group = os.getenv("KAFKA_CONSUMER_GROUP", "arc-consumer-group")
        
        self.consumer = None
        self.vector_store_service = None
        self.thread = None

    def ensure_services(self):
        if self.vector_store_service is None:
            # Let VectorStoreService load its own parameterized parameters
            self.vector_store_service = VectorStoreService()
    
    def _consume_messages(self):
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id=self.consumer_group,
            value_deserializer=lambda x: x.decode("utf-8")
        )

        print(f"✅ Listening to Kafka topic '{self.topic}'...")
        self.ensure_services()
        for message in self.consumer:
            try:
                batch = json.loads(message.value)
                requests = batch["requests"]
                self.vector_store_service.store_batch(requests)
                print(f"✅ Processed batch with {len(requests)} items from Kafka")
            except Exception as e:
                print(f"❌ Error processing message: {e}")
        
    def start(self):
        self.thread = threading.Thread(target=self._consume_messages, daemon=True)
        self.thread.start()