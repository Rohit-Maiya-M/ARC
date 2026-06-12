class RepositoryPromptBuilder:

    @staticmethod
    def build(
        question: str,
        context_chunks: list[str]
    ):
        context = "\n\n".join(
            context_chunks
        )

        return f"""
You are a repository analysis assistant.

Context:
{context}

User Question:
{question}

Provide a concise answer in English.
Do not repeat the prompt.
Do not invent information.
""" 

    @staticmethod
    def build_summary(
        context_chunks: list[str]
    ):
        context = "\n\n".join(
            context_chunks
        )

        return f"""
You are a senior software architect analyzing a source code repository.

Repository Context:
{context}

Write a concise repository summary in English.
Include:
- Project type
- Main frameworks and libraries
- Key dependencies
- High-level architecture
- Important modules
- Overall purpose

Use only the repository context.
Do not invent information.
Do not repeat the prompt.
"""
