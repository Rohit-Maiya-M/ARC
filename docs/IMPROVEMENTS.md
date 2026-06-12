# ARC Improvements

## Repository Summary

- Added FastAPI `POST /summary` with a repository-scoped `repository_id` request.
- Added ChromaDB repository document lookup using stored `repository_id` metadata.
- Added a dedicated repository summary prompt that asks for project type, frameworks, dependencies, high-level architecture, important modules, and overall purpose.
- Added Spring Boot endpoint `POST /repositories/{repositoryId}/summary`.
- Added Spring DTOs and AI service client integration for summary generation.

## LLM Output Cleanup

- Centralized small LLM response cleanup in `LLMService`.
- Removes common generated prefixes such as `Answer:` and `Summary:`.
- Trims trailing stop markers such as `END OF ANSWER`.
- Allows summary generation to use a larger `n_predict` than normal question answering.

## All-In-One Local Runtime

- Added `scripts/run_all.py` to start all local services together:
  - DeepSeek through `llama-server.exe`
  - FastAPI AI service
  - Spring Boot backend
- The runner reads paths and runtime options through `ai-service/app/config/settings.py`.
- `settings.py` loads those values from `ai-service/.env`, so model and executable paths are not hardcoded in source.
- Added `ai-service/.env.example` to document the required local environment variables.

## Repository Hygiene

- Added a root `.gitignore` for local secrets, virtual environments, Chroma data, Maven targets, `node_modules`, frontend builds, and generated local repository/model data.
