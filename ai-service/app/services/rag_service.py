from app.services.vector_store_service import VectorStoreService
from app.prompts.repository_prompt_builder import RepositoryPromptBuilder
from app.services.retrieval_service import RetrievalService

class RAGService:
    def __init__(self):                
        self.vector_store_service = VectorStoreService()


    def generatePrompt(self, repository_id: int, question: str, top_k: int = 5):        
        retriever = RetrievalService()
        final_docs = retriever.search(repository_id, question, top_k=top_k)    
        prompt = RepositoryPromptBuilder.build(question, final_docs)
        return prompt    