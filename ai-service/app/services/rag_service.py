from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.vector_store_service import VectorStoreService
from app.prompts.repository_prompt_builder import RepositoryPromptBuilder
from app.services.hybrid_retrieval_service import HybridRetrievalService
from app.services.retrieval_service import RetrievalService

class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.llm_service = LLMService()
        self.vector_store_service = VectorStoreService()

    def ask(self, repository_id: int, question: str, top_k: int = 5):        
        hybrid_retriever = HybridRetrievalService(
            self.vector_store_service.get_all_docs(repository_id)
        )
        documents = hybrid_retriever.hybrid_search(question, repository_id, top_k=top_k)

        prompt = RepositoryPromptBuilder.build(question, documents)
        print("\n===== PROMPT =====\n")
        print(prompt)

        answer = self.llm_service.generate(prompt)
        return answer

    def generatePrompt(self, repository_id: int, question: str, top_k: int = 5):        
        retriever = RetrievalService()
        final_docs = retriever.search(repository_id, question, top_k=top_k)
    
        prompt = RepositoryPromptBuilder.build(question, final_docs)
        return prompt


    def summarize(self, repository_id: int):
        repository_documents = self.vector_store_service.get_repository_documents(
            repository_id=repository_id,
            limit=20
        )
        documents = repository_documents.get("documents", [])
        if not documents:
            return "No indexed content found for this repository."

        prompt = RepositoryPromptBuilder.build_summary(documents)
        print("\n===== SUMMARY PROMPT =====\n")
        print(prompt)

        return self.llm_service.generate(prompt, n_predict=512)
