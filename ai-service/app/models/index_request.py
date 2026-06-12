from pydantic import BaseModel

class IndexRequest(BaseModel):
    
    chunk_id: str

    repository_id: int

    content: str

    metadata: dict
