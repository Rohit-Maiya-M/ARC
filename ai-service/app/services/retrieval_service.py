# app/services/retrieval_service.py
import numpy as np
from pymilvus import connections, Collection
from app.services.embedding_service import EmbeddingService

class RetrievalService:
    def __init__(self, collection_name: str = "ims_embeddings", dim: int = 1024):
        self.embedding_service = EmbeddingService()
        connections.connect("default", host="127.0.0.1", port="19530")
        self.collection = Collection(collection_name)

    def search(self, repository_id: int, query: str, top_k: int = 5,
               min_score: float = 0.30,  # Lowered to 0.30 to allow multiple code chunks to pass
               max_tokens: int = 4000,
               alpha: float = 0.7, beta: float = 0.3):
        
        query_embedding = self.embedding_service.generate_embedding(query)
        
        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param={"metric_type": "IP", "params": {"nprobe": 32}},
            limit=30,  
            expr=f"repository_id == {repository_id}",
            output_fields=["content", "filename", "meta_embedding"]
        )

        selected, total_tokens = [], 0
        query_meta_embedding = self.embedding_service.generate_embedding(query)

        for hit in results[0]:
            text_score = hit.distance
            
            if text_score < min_score:
                continue

            doc = hit.entity.get("content")
            meta_embedding = hit.entity.get("meta_embedding")
            filename = hit.entity.get("filename")

            token_count = len(doc.split())
            if total_tokens + token_count > max_tokens:
                break

            meta_score = 0.0
            if meta_embedding is not None:
                meta_score = float(
                    np.dot(query_meta_embedding, meta_embedding) /
                    (np.linalg.norm(query_meta_embedding) * np.linalg.norm(meta_embedding))
                )

            combined_score = alpha * text_score + beta * meta_score

            print(f"Text={text_score:.4f}, Meta={meta_score:.4f}, Final={combined_score:.4f}, File={filename}")

            selected.append((doc, combined_score))
            total_tokens += token_count

        selected.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in selected[:top_k]]