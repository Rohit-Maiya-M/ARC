from app.vectordb.chroma_client import (
    collection
)

class VectorStoreService:    

    def __init__(self):
        self.collection = collection

    def store_embedding(
            self,
            chunk_id: str,
            repository_id: int,
            content: str,
            embedding: list,
            metadata: dict
    ):
        metadata = {
            **metadata,

            "repository_id": 
                str(
                    repository_id
                )
        }

        self.collection.add(
            ids = [
                chunk_id
            ],
            documents=[
                content
            ],
            embeddings=[
                embedding
            ],
            metadatas=[
                metadata
            ]
        )
    
    def count_documents(self):

        return self.collection.count()

    def get_repository_documents(
            self,
            repository_id: int,
            limit: int = 20
    ):
        return self.collection.get(
            where={
                "repository_id":
                str(
                    repository_id
                )
            },
            limit=limit,
            include=[
                "documents",
                "metadatas"
            ]
        )
