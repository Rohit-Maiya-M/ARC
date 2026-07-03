import torch
from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "BAAI/bge-reranker-large",
    device="cuda" if torch.cuda.is_available() else "cpu"
)

import numpy as np

def rerank(question: str, docs: list, top_k: int = 5) -> list:
    if not docs:
        return []

    pairs = [(question, doc) for doc in docs]
    scores = reranker.predict(pairs)
    
    min_score, max_score = np.min(scores), np.max(scores)
    if max_score > min_score:  # avoid divide-by-zero
        norm_scores = (scores - min_score) / (max_score - min_score)
    else:
        norm_scores = np.zeros_like(scores)
    
    for doc, raw, norm in zip(docs, scores, norm_scores):
        print("\n--- Candidate ---")
        print(f"Doc snippet: {doc[:120]}...")
        print(f"Raw reranker score: {raw:.4f}, Normalized: {norm:.4f}")

    reranked = sorted(zip(docs, norm_scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in reranked[:top_k]]
