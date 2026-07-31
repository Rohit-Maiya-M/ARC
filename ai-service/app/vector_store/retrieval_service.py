import os

from app.embeddings.embedder import Embedder
from app.vector_store.milvus_service import MilvusService

class RetrievalService:

    def __init__(self):

        self.embedder = Embedder()
        self.vector_store = MilvusService()

        self.default_top_k = int(
            os.getenv(
                "RETRIEVAL_TOP_K",
                "10",
            )
        )

    def search(
        self,
        repository_id: str,
        query: str,
        top_k: int | None = None,
    ):

        top_k = top_k or self.default_top_k

        print("=" * 60)
        print("Repository ID :", repository_id)
        print("Question      :", query)

        query_embedding = self.embedder.embed(query)

        hits = self.vector_store.search(
            embedding=query_embedding,
            expr=f'repository_id == "{repository_id}"',
            top_k=top_k,
        )

        print("Retrieved Hits:", len(hits))

        for hit in hits:
            print(hit.distance)

        print("=" * 60)

        return hits