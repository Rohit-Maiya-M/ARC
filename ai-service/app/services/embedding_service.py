from sentence_transformers import SentenceTransformer
from functools import lru_cache
import os
import time

model = SentenceTransformer(os.getenv("EMBEDDING_MODEL_PATH"))

class EmbeddingService:

    def __init__(self):
        self.model = model

    @lru_cache(maxsize=1000)
    def generate_embedding(self, text: str):
        embedding = self.model.encode(text)
        return embedding.tolist()

    def generate_batch_embeddings(self, texts: list):
        start = time.time()
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False
        )
        print(f"✅ Batch content embeddings: {time.time() - start:.3f} sec")
        return embeddings.tolist()

    def generate_metadata_embedding(self, metadata: dict):
        meta_text = f"{metadata.get('filename','')} {metadata.get('path','')}"
        embedding = self.model.encode(meta_text)
        return embedding.tolist()

    def generate_batch_metadata_embeddings(self, metadata_list: list):
        texts = [
            f"{m.get('filename','')} {m.get('path','')}"
            for m in metadata_list
        ]

        start = time.time()
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False
        )
        print(f"✅ Batch metadata embeddings: {time.time() - start:.3f} sec")
        return embeddings.tolist()