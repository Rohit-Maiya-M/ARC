# 🚀 ARC — Autonomous Repository Companion

> **AI-powered Repository Understanding using Semantic Code Search and Retrieval-Augmented Generation (RAG)**

---

# ✨ Overview

ARC (Autonomous Repository Companion) is an AI-powered repository analysis platform that enables developers to understand large Java codebases through semantic search and Retrieval-Augmented Generation (RAG).

Instead of searching source code using traditional keyword matching, ARC parses repositories into semantic code chunks, generates vector embeddings using ONNX Runtime, indexes them inside Milvus, and retrieves only the most relevant code before generating answers with Google's Gemini model.

The project follows a microservice architecture built using Spring Boot, FastAPI, Kafka, and Milvus.

---

# 🏗️ System Architecture

```text
                             +----------------------+
                             |   React Frontend     |
                             +----------+-----------+
                                        |
                                        ▼
                             +----------------------+
                             | Spring Boot Backend  |
                             +----------+-----------+
                                        |
                          Upload Repository (.zip)
                                        |
                                        ▼
                             Repository Extraction
                                        |
                                        ▼
                              Repository Scanner
                                        |
                                        ▼
                              Repository File Reader
                                        |
                                        ▼
                                 Kafka Producer
                                        |
                                        ▼
                          +---------------------------+
                          |   FastAPI AI Service      |
                          +---------------------------+
                                        |
                                        ▼
                             Kafka Consumer
                                        |
                                        ▼
                           Tree-sitter Java Parser
                                        |
                                        ▼
                           Semantic Code Chunking
                                        |
                                        ▼
                   BAAI/bge-base-en-v1.5 (ONNX Runtime)
                                        |
                                        ▼
                             Milvus Vector Database
                                        |
                                        ▼
                            Semantic Vector Retrieval
                                        |
                                        ▼
                             Repository Prompt Builder
                                        |
                                        ▼
                             Gemini 2.5 Flash API
                                        |
                                        ▼
                           Context-Aware AI Response
```

---

# ⚡ Features

- ✅ Java Repository Analysis
- ✅ Automatic Repository Upload & Extraction
- ✅ Tree-sitter Java Parsing
- ✅ Semantic Code Chunking
- ✅ ONNX Runtime Embedding Generation
- ✅ Milvus Vector Database
- ✅ Kafka-based Asynchronous Indexing
- ✅ Semantic Code Search
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Context-aware AI Answers
- ✅ Repository Isolation using UUIDs
- ✅ Spring Boot + FastAPI Microservices
- ✅ Dockerized Deployment

---

# 🛠️ Tech Stack

## 🎨 Frontend

- React
- Vite
- TailwindCSS
- TypeScript

---

## ☕

Backend

- Java 21
- Spring Boot
- Spring Security
- Spring Data JPA
- Hibernate
- PostgreSQL

---

## 🤖 AI Service

- FastAPI
- Tree-sitter
- ONNX Runtime
- HuggingFace Tokenizers
- NumPy
- Kafka
- Milvus
- Google Gemini 2.5 Flash

---

## 🐳 Infrastructure

- Docker
- Docker Compose
- Kafka
- Milvus
- PostgreSQL

---

# 🧠 Repository Indexing Pipeline

```text
Repository (.zip)
        │
        ▼
Spring Boot Upload
        │
        ▼
ZIP Extraction
        │
        ▼
Repository Scanner
        │
        ▼
Repository File Reader
        │
        ▼
Kafka Producer
        │
        ▼
Kafka Consumer
        │
        ▼
Tree-sitter Java Parser
        │
        ▼
Semantic Chunk Generator
        │
        ▼
ONNX Embedding Generator
        │
        ▼
Milvus Vector Storage
```

Each indexed chunk stores:

- Repository UUID
- Repository Name
- File Name
- Relative Path
- Programming Language
- Symbol Name
- Symbol Type
- Symbol Path
- Chunk Index
- Line Range
- Token Range
- Token Count
- Source Code
- SHA-256 Content Hash
- 768-Dimensional Embedding

---

# 🔍 Retrieval-Augmented Generation Pipeline

```text
Developer Question
        │
        ▼
Query Embedding
        │
        ▼
Milvus Semantic Search
        │
        ▼
Top-K Relevant Chunks
        │
        ▼
Repository Prompt Builder
        │
        ▼
Gemini 2.5 Flash
        │
        ▼
AI Generated Answer
```

Retrieval uses:

- Semantic Vector Similarity
- Repository UUID Filtering
- Top-K Retrieval
- Symbol-aware Code Chunks

---

# 🧠 Embedding Pipeline

### Embedding Model

```
BAAI/bge-base-en-v1.5
```

### Inference Engine

```
ONNX Runtime (CPU)
```

### Embedding Dimension

```
768
```

### Maximum Context Length

```
512 Tokens
```

### Embedding Workflow

```text
Source Code
      │
      ▼
Tokenizer
      │
      ▼
ONNX Runtime
      │
      ▼
CLS Pooling
      │
      ▼
L2 Normalization
      │
      ▼
768-D Embedding
```

---

# ⚙️ ONNX Runtime Optimizations

ARC optimizes embedding generation using:

- Singleton Tokenizer
- Singleton ONNX Session
- Dynamic Input Detection
- Dynamic Output Detection
- Automatic token_type_ids Support
- CLS Pooling
- Batch Inference
- L2 Normalization
- Graph Optimization (ORT_ENABLE_ALL)
- Multi-threaded CPU Execution

---

# 📁 Project Structure

```text
ARC
│
├── ai-service/
│   ├── app/
│   │   ├── embeddings/
│   │   ├── indexing/
│   │   ├── parsers/
│   │   ├── prompts/
│   │   ├── services/
│   │   ├── vector_store/
│   │   └── main.py
│   │
│   └── Dockerfile
│
├── backend-java/
│
├── arc-studio/
│
├── models/
│
├── ARC-Repositories/
│
├── docker-compose.yml
│
└── README.md
```

---

# 📋 Prerequisites

- Docker Desktop
- Docker Compose
- Java 21
- Python 3.10+
- Node.js 18+
- Git

---

# 🔧 Environment Variables

```env
GEMINI_API_KEY=

LOCAL_EMBEDDING_MODEL_PATH=
ONNX_MODEL_PATH=

VECTOR_DIM=768

MILVUS_HOST=
MILVUS_PORT=

KAFKA_BOOTSTRAP_SERVERS=
KAFKA_INDEX_TOPIC=
KAFKA_CONSUMER_GROUP=

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

EMBEDDING_MAX_LENGTH=512
```

---

# ▶️ Running ARC

Start all services

```bash
docker compose up --build
```

Stop services

```bash
docker compose down
```

---

# 📈 Performance

## Repository Indexing

| Stage | Typical Time |
|--------|-------------:|
| Tree-sitter Parsing | ~0.01 s |
| Semantic Chunking | ~0.02 s |
| ONNX Embedding | ~0.10 s |
| Milvus Storage | ~4–5 s |

---

## Question Answering

| Stage | Typical Time |
|--------|-------------:|
| Query Embedding | ~0.04 s |
| Milvus Retrieval | ~0.04 s |
| Prompt Construction | <0.01 s |
| Gemini Response | ~2–3 s |

---

# 🎯 Current Capabilities

- Java Repository Indexing
- Java Semantic Search
- AI-powered Repository Question Answering
- Context-aware Code Understanding
- Repository-level Isolation
- Dockerized Deployment
- Microservice Architecture

---

# 🚧 Roadmap

- Cross-Encoder Reranking
- Multi-language Support (Python, JavaScript, TypeScript)
- Hybrid Lexical + Semantic Search
- Repository Summarization
- AI Response Cache
- Automatic Code Editing
- Multi-Repository Search
- Incremental Repository Indexing

---

# 📜 License

This project is intended for educational, research, and learning purposes.