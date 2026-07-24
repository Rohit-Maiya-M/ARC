# app/main.py
from fastapi import FastAPI, Query
from app.services.vector_store_service import VectorStoreService
from app.services.retrieval_service import RetrievalService
from app.services.rag_service import RAGService
from app.services.gemini_service import GeminiService
from app.services.kafka_consumer_service import KafkaConsumerService
from app.models.index_request import IndexRequest
from app.models.query_request import QueryRequest
from app.models.ask_request import AskRequest
from app.models.summary_request import SummaryRequest
from app.models.embedding_request import EmbeddingRequest
from app.models.embedding_response import EmbeddingResponse
from app.models.index_batch_request import IndexBatchRequest


app = FastAPI()

gemini = GeminiService()


vector_store_service = None
retrieval_service = None
rag_service = None
kafka_service = None

def ensure_services():
    global rag_service, kafka_service
    if rag_service is None:
        rag_service = RAGService()
    if kafka_service is None:
        kafka_service = KafkaConsumerService()

@app.get("/")
def home():
    return {"message": "ARC AI Service Running"}


@app.post("/summary")
def summarize_repository(request: SummaryRequest):
    ensure_services()
    summary = rag_service.summarize(request.repository_id)
    return {"summary": summary}

@app.post("/generate/api")
def generate_api(request: AskRequest, top_k: int = Query(5)):
    ensure_services()
    prompt = rag_service.generatePrompt(request.repository_id, request.question, top_k=top_k)
    answer = gemini.generate(prompt, n_predict=1024)
    return {"answer": answer}


@app.on_event("startup")
def startup_event():
    ensure_services()
    kafka_service.start()