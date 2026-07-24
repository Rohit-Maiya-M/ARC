import os
import numpy as np
from pymilvus import connections, Collection
from app.embeddings.embedder import Embedder

class RetrievalService:
    def __init__(self, collection_name: str = None, dim: int = None):
        self.embedder = Embedder()

        self.milvus_host = os.getenv("MILVUS_HOST", "localhost")
        self.milvus_port = os.getenv("MILVUS_PORT", "19530")
        self.collection_name = collection_name or os.getenv("MILVUS_COLLECTION_NAME", "ims_embeddings")
        self.dim = dim or int(os.getenv("VECTOR_DIM", "1024"))
                
        self.default_min_score = float(os.getenv("RETRIEVAL_MIN_SCORE", "0.30"))
        self.default_max_tokens = int(os.getenv("RETRIEVAL_MAX_TOKENS", "4000"))
        
        connections.connect("default", host=self.milvus_host, port=self.milvus_port)
        self.collection = Collection(self.collection_name)

    def search(self, repository_id: int, query: str, top_k: int = 5,
               min_score: float = None,
               max_tokens: int = None,
               alpha: float = 0.7, beta: float = 0.3):
                
        score_threshold = min_score if min_score is not None else self.default_min_score
        token_limit = max_tokens if max_tokens is not None else self.default_max_tokens

        query_embedding = self.embedder.embed(query)
        
        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param={"metric_type": "IP", "params": {"nprobe": 32}},
            limit=30,  
            expr=f"repository_id == {repository_id}",
            output_fields=["content", "filename", "meta_embedding"]
        )

        selected, total_tokens = [], 0
        query_meta_embedding = self.embedder.embed_metadata(
            {
                "filename": query,
                "path": "",
                "extension": "",
            }
        )

        for hit in results[0]:
            text_score = hit.distance
            
            if text_score < score_threshold:
                continue

            doc = hit.entity.get("content")
            meta_embedding = hit.entity.get("meta_embedding")
            filename = hit.entity.get("filename")

            token_count = len(doc.split())
            if total_tokens + token_count > token_limit:
                break

            meta_score = 0.0

            if meta_embedding is not None:
                meta_score = float(
                    np.dot(query_meta_embedding, meta_embedding)
                )

            combined_score = alpha * text_score + beta * meta_score

            print(f"Text={text_score:.4f}, Meta={meta_score:.4f}, Final={combined_score:.4f}, File={filename}")

            selected.append((doc, combined_score))
            total_tokens += token_count

        selected.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in selected[:top_k]]