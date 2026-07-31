from app.prompts.repository_prompt_builder import RepositoryPromptBuilder
from app.vector_store.retrieval_service import RetrievalService


class RAGService:

    def __init__(self):

        self.retriever = RetrievalService()

    def generate_prompt(
        self,
        repository_id: str,
        question: str,
        top_k: int = 5,
    ) -> str:
        """
        Builds the final prompt for Gemini using retrieved repository context.
        """

        search_results = self.retriever.search(
            repository_id=repository_id,
            query=question,
            top_k=top_k,
        )

        prompt = RepositoryPromptBuilder.build(
            question=question,
            search_results=search_results,
        )

        return prompt