from fastapi import FastAPI, Query

from app.models.ask_request import AskRequest

from app.services.gemini_service import GeminiService
from app.services.rag_service import RAGService
from app.services.kafka_consumer_service import KafkaConsumerService


app = FastAPI()


gemini = GeminiService()

rag_service: RAGService
kafka_service: KafkaConsumerService


@app.on_event("startup")
def startup_event():

    global rag_service
    global kafka_service

    rag_service = RAGService()

    kafka_service = KafkaConsumerService()

    kafka_service.start()

    print("====================================")
    print("ARC AI Service Started")
    print("====================================")


@app.get("/")
def home():

    return {
        "message": "ARC AI Service Running"
    }


@app.post("/generate/api")
def generate_api(
    request: AskRequest,
    top_k: int = Query(5),
):
    print("=" * 60)
    print(request.repository_id)
    print(type(request.repository_id))
    print("=" * 60)
    
    prompt = rag_service.generate_prompt(
        repository_id=request.repository_id,
        question=request.question,
        top_k=top_k,
    )

    answer = gemini.generate(
        prompt,
        n_predict=1024,
    )

    return {
        "answer": answer
    }