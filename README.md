# 🚀 ARC — Autonomous Repository Companion

> **AI-powered Repository Understanding using Semantic Code Search and Retrieval-Augmented Generation (RAG)**

---

# ✨ Overview

ARC (Autonomous Repository Companion) is an AI-powered repository analysis platform that enables developers to understand large Java codebases through semantic search and Retrieval-Augmented Generation (RAG).

Instead of relying on traditional keyword-based search, ARC parses repositories into semantic code chunks, generates vector embeddings using ONNX Runtime, indexes them in Milvus, and retrieves the most relevant code before generating context-aware answers using Google's Gemini model.

The project follows a microservice architecture built with Spring Boot, FastAPI, Apache Kafka, and Milvus.

---

# 🏗️ System Architecture

```text
                             +----------------------+
                             |   Next.js Frontend   |
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

# ✨ Features

- Java Repository Analysis
- Automatic ZIP Repository Upload
- Tree-sitter Java Parsing
- Semantic Code Chunking
- ONNX Runtime Embedding Generation
- Milvus Vector Database
- Kafka-based Asynchronous Indexing
- Semantic Code Search
- Retrieval-Augmented Generation (RAG)
- Context-aware AI Answers
- Repository Isolation using UUIDs
- Spring Boot + FastAPI Microservices
- Dockerized Deployment

---

# 🛠️ Tech Stack

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

## Backend

- Java 21
- Spring Boot
- Spring Security
- Spring Data JPA
- Hibernate
- PostgreSQL

## AI Service

- FastAPI
- Tree-sitter
- ONNX Runtime
- HuggingFace Tokenizers
- NumPy
- Apache Kafka
- Milvus
- Google Gemini 2.5 Flash

## Infrastructure

- Docker
- Docker Compose
- PostgreSQL
- Apache Kafka
- Milvus

---

# 📁 Project Structure

```text
ARC/
│
├── ai-service/
├── backend-java/
├── arc-studio/
├── models/
├── ARC-Repositories/
├── docker-compose.yml
├── .env.example
├── README.md
└── .gitignore
```

---

# 📋 Prerequisites

Before running ARC, install:

- Docker Desktop
- Docker Compose
- Git

For local development:

- Java 21
- Python 3.10+
- Node.js 20+

---

# 📦 Installation

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/ARC.git
cd ARC
```

---

## 2. Download the Embedding Model

ARC uses the **BAAI/bge-base-en-v1.5** embedding model.

Download the model and place it inside:

```text
models/
└── bge-base-en-v1.5/
    ├── config.json
    ├── tokenizer.json
    ├── tokenizer_config.json
    ├── vocab.txt
    ├── special_tokens_map.json
    └── onnx/
        └── model.onnx
```

> **Note**
>
> The embedding model is **not included** in this repository because of its size.

---

## 3. Configure Environment Variables

Copy:

```text
.env.example
```

to

```text
.env
```

and update the required values.

At minimum configure:

- GEMINI_API_KEY
- POSTGRES_PASSWORD
- NEXT_PUBLIC_API_URL (if deploying remotely)

---

## 4. Configure Spring Boot

Copy:

```text
backend-java/src/main/resources/application.properties.example
```

to

```text
backend-java/src/main/resources/application.properties
```

Update any values if necessary.

When using Docker Compose, most configuration is automatically supplied through environment variables.

---

# ▶️ Running ARC

Build and start all services

```bash
docker compose up --build
```

Run in detached mode

```bash
docker compose up -d --build
```

Stop all services

```bash
docker compose down
```

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
- 768-dimensional Embedding

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

# ⚙️ ONNX Runtime Optimizations

ARC optimizes embedding generation using:

- Singleton Tokenizer
- Singleton ONNX Session
- Dynamic Input Detection
- Dynamic Output Detection
- CLS Pooling
- Batch Inference
- L2 Normalization
- Graph Optimization
- Multi-threaded CPU Execution

---

# 📈 Current Capabilities

- Java Repository Indexing
- Semantic Repository Search
- AI-powered Repository Question Answering
- Context-aware Code Understanding
- Repository-level Isolation
- Dockerized Deployment
- Microservice Architecture

---

# 🚧 Roadmap

- Cross-Encoder Reranking
- Multi-language Support
- Hybrid Lexical + Semantic Search
- Repository Summarization
- AI Response Cache
- Automatic Code Editing
- Multi-Repository Search
- Incremental Repository Indexing

---

# 📜 License

This project is intended for educational, research, and learning purposes.