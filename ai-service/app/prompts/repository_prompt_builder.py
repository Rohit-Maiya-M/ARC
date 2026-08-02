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
Repository : {entity.get("repository_name")}

File Path  : {entity.get("relative_path")}

Language   : {entity.get("language")}

Symbol     : {entity.get("symbol_path")}

Lines      : {entity.get("line_start")}-{entity.get("line_end")}

Code:

{entity.get("content")}
""".strip()
            )

        context = "\n\n" + "=" * 80 + "\n\n".join(contexts)

        return f"""
You are ARC, an AI software engineering assistant specialized in repository analysis.

Your task is to answer questions ONLY using the retrieved repository context.

========================
Repository Context
========================

{context}

========================
User Question
========================

{question}

========================
Instructions
========================

1. Use ONLY the provided repository context.

2. Never invent files, classes, methods, packages, or functionality that are not present.

3. If the answer cannot be determined from the retrieved context, explicitly say:
   "I cannot determine this from the retrieved repository context."

4. When available, include:
   - File path
   - Class name
   - Method name
   - Symbol path
   - Line numbers

5. If the question asks "where", always mention the complete file path.

6. If the question asks "how", explain the execution flow step by step.

7. If the question asks "why", explain the purpose using the retrieved code.

8. If multiple files participate in the implementation, explain their relationship.

9. If multiple implementations are retrieved, summarize each before giving the final answer.

10. Keep the answer technical and repository-specific.

11. Use bullet points or numbered lists whenever they improve readability.

12. Include short code snippets only when they help explain the answer.

13. Never answer using outside knowledge.

Provide the best possible answer based only on the repository context.
"""

    @staticmethod
    def build_summary(search_results):

        contexts = []

        for hit in search_results:

            entity = hit.entity

            contexts.append(
                f"""
File Path : {entity.get("relative_path")}

Language  : {entity.get("language")}

Symbol    : {entity.get("symbol_path")}

{entity.get("content")}
""".strip()
            )

        context = "\n\n".join(contexts)

        return f"""
You are ARC, an AI software architect.

Using ONLY the repository context below, produce a repository summary.

========================
Repository Context
========================

{context}

========================
Summary Requirements
========================

Write a structured summary containing:

1. Project Overview

2. Primary Programming Language

3. Frameworks and Libraries

4. Overall Architecture

5. Major Packages

6. Important Classes

7. Important Services

8. Controllers

9. Data Access Layer

10. Security Components

11. Configuration Files

12. Main Features

13. Repository Organization

14. Observations

Rules:

- Use only the provided repository context.
- Do not invent missing information.
- If something is not present, explicitly state that it could not be determined.
- Organize the summary using headings and bullet points.
"""