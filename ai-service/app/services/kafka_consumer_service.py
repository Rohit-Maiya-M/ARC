import json
import threading
from kafka import KafkaConsumer
from app.services.vector_store_service import VectorStoreService

class KafkaConsumerService:
    def __init__(self, topic: str = "arc.index", bootstrap_servers: list = ["localhost:9092"]):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.consumer = None
        self.vector_store_service = None
        self.thread = None

    def ensure_services(self):
        if self.vector_store_service is None:
            self.vector_store_service = VectorStoreService(dim=1024, collection_name = "ims_embeddings")
    
    def _consume_messages(self):
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="arc-consumer-group",
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