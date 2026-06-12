from fastapi import FastAPI

from app.services.embedding_service import (
    EmbeddingService
)

from app.models.embedding_request import (
    EmbeddingRequest
)

from app.models.embedding_response import (
    EmbeddingResponse
)

from app.services.vector_store_service import (
    VectorStoreService
)

from app.models.index_request import (
    IndexRequest
)

from app.services.retrieval_service import (
    RetrievalService
)

from app.models.query_request import (
    QueryRequest
)

from app.models.ask_request import (
    AskRequest
)

from app.models.summary_request import (
    SummaryRequest
)

from app.services.rag_service import (
    RAGService
)




app = FastAPI()
embedding_service = EmbeddingService()
retrieval_service = RetrievalService()
vector_store_service = VectorStoreService()
rag_service = RAGService()

@app.get("/")
def home():
    return {
        "message": "ARC AI Service Running"
    }

@app.post("/embed")
def generate_embedding(
    request: EmbeddingRequest
) -> EmbeddingResponse:
    embedding = (
        embedding_service.generate_embedding(
            request.text
        )
    )

    return EmbeddingResponse(
        embedding=embedding
    )

@app.post("/index")
def index_chunk(
        request: IndexRequest
):

    embedding = (
        embedding_service.generate_embedding(
            request.content
        )
    )

    vector_store_service.store_embedding(
        chunk_id=request.chunk_id,
        repository_id=request.repository_id,
        content=request.content,
        embedding=embedding,
        metadata=request.metadata
    )

    return {
        "status": "indexed",
        "chunk_id": request.chunk_id
    }


@app.get("/count")
def count_chunks():

    return {
        "count":
            vector_store_service.count_documents()
    }

@app.post("/search")
def search_repository(
        request: QueryRequest
):

    query_embedding = (
        embedding_service.generate_embedding(
            request.query
        )
    )

    results = (
        retrieval_service.search(
            query_embedding
        )
    )

    return results

@app.post("/ask")
def ask(
        request: AskRequest
):

    answer = rag_service.ask(
        request.repository_id,
        request.question   
    )

    return {
        "answer": answer
    }

@app.post("/summary")
def summarize_repository(
        request: SummaryRequest
):

    summary = rag_service.summarize(
        request.repository_id
    )

    return {
        "summary": summary
    }
