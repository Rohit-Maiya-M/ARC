class RepositoryPromptBuilder:

    @staticmethod
    def build(
        question: str,
        search_results,
    ):

        contexts = []

        for hit in search_results:

            entity = hit.entity

            contexts.append(
                f"""
File: {entity.get("relative_path")}
Symbol: {entity.get("symbol_path")}
Lines: {entity.get("line_start")}-{entity.get("line_end")}

{entity.get("content")}
""".strip()
            )

        context = "\n\n".join(contexts)

        return f"""
You are a repository analysis assistant.

Repository Context:

{context}

User Question:

{question}

Instructions:
- Answer only using the repository context.
- If the answer is not present, say you cannot determine it.
- Do not invent information.
- Keep the answer concise.
"""
    @staticmethod
    def build_summary(search_results):

        contexts = []

        for hit in search_results:

            entity = hit.entity

            contexts.append(entity.get("content"))

        context = "\n\n".join(contexts)

        return f"""
You are a senior software architect.

Repository Context:

{context}

Write a concise repository summary.

Include:
- Project type
- Frameworks
- Dependencies
- Architecture
- Important modules
- Overall purpose

Only use the repository context.
Do not invent information.
"""