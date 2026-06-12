# ARC / Autonomous Repository Companion

## Overview

A multi-service repository that combines:

- ai-service — FastAPI AI backend that indexes repositories, generates embeddings, and serves RAG/LLM queries.
- backend-java — Spring Boot Java backend using Spring WebMVC, Spring Security, Spring Data JPA, and PostgreSQL runtime support.
- frontend — React + Vite UI with Tailwind integration.
- docker — Docker container definitions for local deployment.
- models, repositories, `indexed/` — storage for model files, repository data, and indexed artifacts.

## Architecture

- AI service drives vector search and retrieval over repository data.
- A local `llama-server` binary is launched from run_all.py.
- The Java backend exposes application APIs.
- The React frontend consumes backend endpoints and user flows.

## Prerequisites

- Python 3.10+ (project uses .venv310)
- Java 21
- Node.js 18+ and npm
- Git
- PostgreSQL or compatible DB for backend runtime
- DeepSeek `llama-server` binary and local model files
- .env configured from .env.example

## Setup

1. Copy environment file
   ```powershell
   cd ai-service
   copy .env.example .env
   ```

2. Edit .env:
   - `LLM_MODEL_PATH`
   - `EMBEDDING_MODEL_PATH`
   - `LLAMA_SERVER_PATH`
   - `CHROMA_DB_PATH`
   - `LLM_SERVER_PATH`
   - Optional runtime tuning values

3. Prepare Python environment
   ```powershell
   cd ai-service
   python -m venv .venv310
   .venv310\Scripts\activate
   pip install fastapi uvicorn python-dotenv chromadb pydantic
   ```

4. Prepare frontend
   ```powershell
   cd frontend
   npm install
   ```

5. Prepare backend
   - The backend uses Maven wrapper in backend-java
   - Java version defined in pom.xml is `21`

## Run

### Run all services together
```powershell
python scripts/run_all.py
```

This launches:
- DeepSeek llama server
- FastAPI AI service
- Spring Boot backend

### Run AI service only
```powershell
cd ai-service
.venv310\Scripts\activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Run backend only
```powershell
cd backend-java
.\mvnw.cmd spring-boot:run
```

### Run frontend only
```powershell
cd frontend
npm run dev
```

## Key Endpoints

AI service exposes:
- `GET /`
- `POST /embed`
- `POST /index`
- `GET /count`
- `POST /search`
- `POST /ask`
- `POST /summary`

## Useful Paths

- ai-service — AI service source and vector DB
- backend-java — Java backend application
- frontend — React/Vite frontend
- docker — container deployment artifacts
- run_all.py — orchestrates startup of all local services

## Notes

- pom.xml depends on Spring Boot 4.0.6 and Java 21.
- package.json uses React 19, Vite, Tailwind, and ESLint.
- ai-service expects model binaries and a running local llama server.

