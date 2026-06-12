from sentence_transformers import SentenceTransformer
from app.config import settings

model = SentenceTransformer(
            settings.EMBEDDING_MODEL_PATH
        )

class EmbeddingService:

    def __init__(self):

        self.model = model

    def generate_embedding(
            self,
            text: str
    ):
        
        embedding = self.model.encode(text)

        return embedding.tolist()
