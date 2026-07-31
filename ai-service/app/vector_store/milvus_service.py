import os

from pymilvus import (
    Collection,
    connections,
    utility,
)

from app.vector_store.schema import (
    create_schema,
    get_index_params,
)
from app.indexing.chunking.hash_util import sha256
from app.embeddings.models.embedded_chunk import EmbeddedChunk

class MilvusService:

    def __init__(
        self,
        dim: int | None = None,
        collection_name: str | None = None,
    ):

        self.milvus_host = os.getenv(
            "MILVUS_HOST",
            "milvus",
        )

        self.milvus_port = os.getenv(
            "MILVUS_PORT",
            "19530",
        )

        self.dim = dim or int(
            os.getenv(
                "VECTOR_DIM",
                "768",
            )
        )

        self.collection_name = (
            collection_name
            or os.getenv(
                "MILVUS_COLLECTION_NAME",
                "code_chunks",
            )
        )

        connections.connect(
            alias="default",
            host=self.milvus_host,
            port=self.milvus_port,
        )

        if utility.has_collection(self.collection_name):

            self.collection = Collection(
                self.collection_name,
            )

            print(
                f"✅ Loaded collection : {self.collection_name}"
            )

        else:

            self.collection = Collection(
                name=self.collection_name,
                schema=create_schema(self.dim),
            )

            self.collection.create_index(
                field_name="embedding",
                index_params=get_index_params(),
            )

            print(
                f"✅ Created collection : {self.collection_name}"
            )

        self.collection.load()

    def insert(
        self,
        embedded_chunks: list[EmbeddedChunk],
        flush: bool = False,
    ) -> None:
        """
        Inserts embedded code chunks into Milvus.
        """

        if not embedded_chunks:
            return

        entities = [
            self._to_entity(embedded)
            for embedded in embedded_chunks
        ]

        self.collection.insert(entities)

        if flush:
            self.collection.flush()

    def _to_entity(
        self,
        embedded: EmbeddedChunk,
    ) -> dict:
        """
        Converts an EmbeddedChunk into a Milvus entity.
        """

        chunk = embedded.chunk

        chunk_id = sha256(
            (
                f"{chunk.repository_id}:"
                f"{chunk.relative_path}:"
                f"{chunk.symbol_path}:"
                f"{chunk.chunk_index}"
            )
        )

        return {

            "chunk_id": chunk_id,

            "repository_id": chunk.repository_id,
            "repository_name": chunk.repository_name,

            "file_id": chunk.file_id,
            "file_name": chunk.file_name,
            "relative_path": chunk.relative_path,

            "language": chunk.language,

            "symbol_name": chunk.symbol_name,
            "symbol_type": chunk.symbol_type,
            "symbol_path": chunk.symbol_path,

            "chunk_index": chunk.chunk_index,
            "symbol_chunk_index": chunk.symbol_chunk_index,

            "line_start": chunk.line_start,
            "line_end": chunk.line_end,

            "token_start": chunk.token_start,
            "token_end": chunk.token_end,
            "token_count": chunk.token_count,

            "content_hash": chunk.content_hash,
            "content": chunk.content,

            "embedding": embedded.embedding,
        }

    def count(self) -> int:
        return self.collection.num_entities


    def delete_repository(
        self,
        repository_id: str,
    ):
        self.collection.delete(
            expr=f'repository_id == "{repository_id}"'
        )

        self.collection.flush()

    def query_repository(
        self,
        repository_id: str,
    ):
        return self.collection.query(
            expr=f'repository_id == "{repository_id}"',
            output_fields=["*"],
        )

    def search(
        self,
        embedding: list[float],
        expr: str,
        top_k: int = 10,
    ):
        """
        Performs a vector similarity search.
        """

        results = self.collection.search(
            data=[embedding],
            anns_field="embedding",
            param={
                "metric_type": "IP",
                "params": {
                    "nprobe": 32,
                },
            },
            limit=top_k,
            expr=expr,
            output_fields=[
                "repository_id",
                "repository_name",

                "file_id",
                "file_name",
                "relative_path",

                "language",

                "symbol_name",
                "symbol_type",
                "symbol_path",

                "chunk_index",
                "symbol_chunk_index",

                "line_start",
                "line_end",

                "token_start",
                "token_end",
                "token_count",

                "content_hash",
                "content",
            ],
        )

        return results[0]