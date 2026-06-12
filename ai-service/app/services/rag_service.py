from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService
from app.services.vector_store_service import VectorStoreService
from app.prompts.repository_prompt_builder import RepositoryPromptBuilder

class RAGService:

    def __init__(self):
        self.embedding_service = (
            EmbeddingService()
        )

        self.llm_service = (
            LLMService()
        )

        self.retrieval_service = (
            RetrievalService()
        )

        self.vector_store_service = (
            VectorStoreService()
        )

    def ask(
            self,
            repository_id: int,
            question: str
    ):
        query_embedding = self.embedding_service.generate_embedding(question)

        retrieval_result = self.retrieval_service.search(query_embedding, repository_id)

        documents = (
            retrieval_result["documents"][0]
        )

        prompt = (
                RepositoryPromptBuilder.build(
                question,
                documents
            )
        )

        print("\n===== PROMPT =====\n")
        print(prompt)

        answer = self.llm_service.generate(
            prompt
        )

        return answer

    def summarize(
            self,
            repository_id: int
    ):
        repository_documents = (
            self.vector_store_service.get_repository_documents(
                repository_id=repository_id,
                limit=20
            )
        )

        documents = repository_documents.get(
            "documents",
            []
        )

        if not documents:
            return "No indexed content found for this repository."

        prompt = (
            RepositoryPromptBuilder.build_summary(
                documents
            )
        )

        print("\n===== SUMMARY PROMPT =====\n")
        print(prompt)

        return self.llm_service.generate(
            prompt,
            n_predict=512
        )
