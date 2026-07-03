from sentence_transformers import SentenceTransformer
from app.config import settings
from functools import lru_cache

model = SentenceTransformer(settings.EMBEDDING_MODEL_PATH)

class EmbeddingService:

    def __init__(self):
        self.model = model

    @lru_cache(maxsize=1000)
    def generate_embedding(self, text: str):
        embedding = self.model.encode(text)
        return embedding.tolist()

    def generate_metadata_embedding(self, metadata: dict):        
        meta_text = f"{metadata.get('filename','')} {metadata.get('path','')}"
        embedding = self.model.encode(meta_text)
        return embedding.tolist()
