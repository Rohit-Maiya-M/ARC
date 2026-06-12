from app.vectordb.chroma_client import (
    collection
)

class RetrievalService:

    def search(
            self,
            query_embedding: list,
            repository_id: int,
            top_k: int = 1               
    ):
        results = collection.query(
            query_embeddings=[
                query_embedding
            ],

            where={
                "repository_id":
                str(
                    repository_id
                )
            },

            n_results=top_k        
        )

        return results