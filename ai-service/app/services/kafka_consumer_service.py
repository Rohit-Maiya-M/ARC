import json
import os
import threading

from kafka import KafkaConsumer

from app.indexing.models.repository_file import RepositoryFile
from app.indexing.repository_indexer import RepositoryIndexer
from app.vector_store.milvus_service import MilvusService


class KafkaConsumerService:

    def __init__(
        self,
        topic: str | None = None,
        bootstrap_servers: list[str] | None = None,
    ):

        env_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

        default_servers = (
            [env_servers]
            if env_servers
            else ["arc-kafka:9092"]
        )

        self.topic = (
            topic
            or os.getenv(
                "KAFKA_INDEX_TOPIC",
                "arc.index",
            )
        )

        self.bootstrap_servers = (
            bootstrap_servers
            or default_servers
        )

        self.consumer_group = os.getenv(
            "KAFKA_CONSUMER_GROUP",
            "arc-consumer-group",
        )

        self.consumer = None
        self.thread = None

        self.indexer = RepositoryIndexer()
        self.milvus = MilvusService()

    def _consume_messages(self):

        self.consumer = KafkaConsumer(

            self.topic,

            bootstrap_servers=self.bootstrap_servers,

            auto_offset_reset="earliest",

            enable_auto_commit=True,

            group_id=self.consumer_group,

            value_deserializer=lambda x: x.decode("utf-8"),
        )

        print(
            f"✅ Listening to Kafka topic '{self.topic}'..."
        )

        for message in self.consumer:

            try:

                payload = json.loads(
                    message.value
                )

                repository_file = RepositoryFile(

                    repository_id=payload["repository_id"],
                    repository_name=payload["repository_name"],

                    file_id=payload["file_id"],
                    file_name=payload["file_name"],

                    relative_path=payload["relative_path"],
                    extension=payload["extension"],

                    content=payload["content"],
                )

                embedded_chunks = self.indexer.index(
                    repository_file
                )

                self.milvus.insert(
                    embedded_chunks
                )

                print(
                    f"✅ Indexed {repository_file.relative_path}"
                )

            except Exception as e:

                print(
                    f"❌ Error processing message: {e}"
                )

    def start(self):

        self.thread = threading.Thread(
            target=self._consume_messages,
            daemon=True,
        )

        self.thread.start()