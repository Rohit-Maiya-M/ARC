import chromadb
from app.config import settings

client = chromadb.PersistentClient(
    path = settings.CHROMA_DB_PATH
)

collection = client.get_or_create_collection(
    name = "arc_repository_chunks"
)