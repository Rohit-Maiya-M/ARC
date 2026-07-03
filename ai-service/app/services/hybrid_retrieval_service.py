# hybrid_retrieval_service.py
import numpy as np
from rank_bm25 import BM25Okapi
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.utils.reranker import rerank

class HybridRetrievalService:
    def __init__(self, corpus_docs: list, dim: int = 1024):
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService(dim)
        
        tokenized_corpus = [doc.split() for doc in corpus_docs]
        self.bm25 = BM25Okapi(tokenized_corpus)
        self.corpus_docs = corpus_docs

    def hybrid_search(self, query: str, repository_id: int, top_k: int = 5):        
        query_embedding = self.embedding_service.generate_embedding(query)
        results = self.vector_store_service.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param={"metric_type": "L2", "params": {"nprobe": 10}},
            limit=top_k * 6,
            expr=f"repository_id == {repository_id}",
            output_fields=["content", "filename"]
        )
        embedding_hits = results[0]
        
        max_dist = max(hit.distance for hit in embedding_hits) if embedding_hits else 1.0
        embedding_results = {
            hit.entity.get("content"): 1.0 - (hit.distance / max_dist)
            for hit in embedding_hits
        }
        
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_results = {doc: score for doc, score in zip(self.corpus_docs, bm25_scores)}
        
        combined = {}
        for doc, score in bm25_results.items():
            combined[doc] = 0.3 * score
        for doc, score in embedding_results.items():
            combined[doc] = combined.get(doc, 0) + 0.7 * score

        candidates = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        candidate_docs = [doc for doc, _ in candidates[:top_k * 6]]

        reranked = rerank(query, candidate_docs, top_k=top_k)

        print("\n=== Hybrid Retrieval Debug Log ===")
        for doc in candidate_docs:
            bm25_score = bm25_results.get(doc, 0.0)
            emb_score = embedding_results.get(doc, 0.0)
            combined_score = combined.get(doc, 0.0)
            print(f"\n--- Candidate ---")
            print(f"Snippet: {doc[:120]}...")
            print(f"BM25: {bm25_score:.4f}, Embedding: {emb_score:.4f}, Combined: {combined_score:.4f}")
        
        return reranked


