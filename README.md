# 🚀 ARC — Autonomous Repository Companion

> **AI-powered Repository Understanding, Semantic Code Search & Retrieval-Augmented Generation (RAG)**

---

## ✨ Overview

ARC (Autonomous Repository Companion) is an AI-powered developer assistant that indexes software repositories, performs semantic code search, and generates context-aware responses using Retrieval-Augmented Generation (RAG).

The project is designed for **local-first AI development**, combining semantic search, vector databases, ONNX Runtime, and local LLM inference into a scalable microservice architecture.

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
                 REST APIs           |           Kafka
                                     |
                +--------------------+--------------------+
                |                                         |
                ▼                                         ▼
      +----------------------+                +----------------------+
      |   FastAPI AI Service |<-------------->|        Milvus        |
      |                      |                |   Vector Database    |
      +----------+-----------+                +----------+-----------+
                 |                                       |
                 |                                       |
                 ▼                                       |
      BAAI BGE-Base-en-v1.5 (ONNX Runtime)               |
                 |                                       |
                 +---------------------------------------+
                                 |
                                 ▼
                     DeepSeek Local LLM
```

---

# ⚡ Features

- ✅ Semantic Code Search
- ✅ Repository Indexing
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Hybrid Content + Metadata Retrieval
- ✅ Kafka-based Indexing Pipeline
- ✅ Milvus Vector Database
- ✅ ONNX Runtime Optimized Inference
- ✅ Local LLM Integration
- ✅ Spring Boot Backend
- ✅ React Frontend

---

# 🛠️ Tech Stack

## 🎨 Frontend

- React
- Vite
- Tailwind CSS

## ☕ Backend

- Java 21
- Spring Boot
- Spring Security
- Spring Data JPA
- PostgreSQL

## 🤖 AI Service

- FastAPI
- ONNX Runtime
- HuggingFace Tokenizers
- NumPy
- Kafka
- Milvus
- DeepSeek Local LLM

---

# 🧠 Embedding Pipeline

### Embedding Model

```text
BAAI/bge-base-en-v1.5
```

### Inference Engine

```text
ONNX Runtime (CPU)
```

### Embedding Dimension

```text
768
```

### Maximum Context Length

```text
512 Tokens
```

### ONNX Output

```text
last_hidden_state
```

### Pooling Strategy

```text
CLS Pooling
embedding = last_hidden_state[:, 0, :]
```

### Optimization Techniques

- ✅ Singleton Tokenizer
- ✅ Singleton ONNX Session
- ✅ Dynamic Input Detection
- ✅ Dynamic Output Detection
- ✅ Automatic `token_type_ids` Support
- ✅ CLS Pooling
- ✅ Batch Inference
- ✅ L2 Normalization
- ✅ ONNX Runtime Graph Optimization
- ✅ Multi-threaded CPU Execution

---

# 📦 Repository Indexing Pipeline

```text
Repository
      │
      ▼
Repository Scanner
      │
      ▼
Chunk Generator
      │
      ▼
Kafka
      │
      ▼
AI Service
      │
      ├────────► Content Embeddings
      │
      └────────► Metadata Embeddings
                    │
                    ▼
               Milvus Storage
```

Each indexed chunk stores:

- 📄 Repository ID
- 📂 File Path
- 📃 Filename
- 🏷️ Extension
- 🧠 Content Embedding
- 📝 Metadata Embedding
- 📌 Chunk Information

---

# 🔍 Retrieval Pipeline

```text
User Query
      │
      ▼
Query Embedding
      │
      ▼
Milvus Similarity Search
      │
      ├────────► Content Score
      │
      └────────► Metadata Score
                     │
                     ▼
            Weighted Final Score
                     │
                     ▼
             Top Ranked Chunks
                     │
                     ▼
               DeepSeek LLM
```

Ranking combines:

- 🎯 Semantic Similarity
- 📄 Metadata Similarity

---

# ⚙️ ONNX Runtime Optimizations

The embedding engine uses:

- 🚀 Singleton Model Loading
- 🚀 Singleton Tokenizer
- 🚀 Singleton ONNX Session
- 🚀 ORT_ENABLE_ALL Graph Optimization
- 🚀 CPU Execution Provider
- 🚀 Dynamic Batch Processing
- 🚀 Automatic Input Adaptation
- 🚀 Automatic Output Adaptation
- 🚀 L2 Normalized Embeddings

---

# 📁 Project Structure

```text
ARC
│
├── ai-service/
│   ├── app/
│   ├── tests/
│   ├── models/
│   └── Dockerfile
│
├── backend-java/
│
├── frontend/
│
├── models/
│
├── repositories/
│
└── docker-compose.yml
```

---

# 📋 Prerequisites

- 🐳 Docker Desktop
- 🐳 Docker Compose
- ☕ Java 21
- 🐍 Python 3.10+
- 📦 Node.js 18+
- 🌿 Git

---

# 🔧 Environment Variables

```env
LLM_MODEL_PATH=

LOCAL_EMBEDDING_MODEL_PATH=
ONNX_MODEL_PATH=

VECTOR_DIM=768

MILVUS_HOST=
MILVUS_PORT=

KAFKA_BOOTSTRAP_SERVERS=

POSTGRES_HOST=
POSTGRES_PORT=

EMBEDDING_MAX_LENGTH=512
```

---

# ▶️ Running ARC

Start all services

```bash
docker compose up -d
```

Stop all services

```bash
docker compose down
```

---

# 📈 Performance

### Previous Embedding Model

| Model | Embedding Size | Typical Batch Time |
|---------|---------------|-------------------:|
| BGE-M3 | 1024 | ~220 sec |

### Current Embedding Model

| Model | Embedding Size | Typical Batch Time |
|---------|---------------|-------------------:|
| BGE-Base-en-v1.5 | 768 | ~24 sec |

### Improvements

- ⚡ ~9× Faster Repository Indexing
- ⚡ Reduced Embedding Dimension (1024 → 768)
- ⚡ Reduced Metadata Embedding Time
- ⚡ Lower Memory Usage
- ⚡ Better CPU Inference Performance

### Trade-off

The migration significantly improves indexing performance while introducing a slight decrease in semantic retrieval quality. Future work includes improving retrieval quality through reranking and better chunking strategies.

---

# 🎯 Roadmap

- ⏳ Cross-Encoder Reranking
- ⏳ Hybrid Lexical + Semantic Search
- ⏳ Better Chunking Strategy
- ⏳ AI Response Cache
- ⏳ Automatic Code Editing
- ⏳ Multi-Repository Search
- ⏳ Improved Retrieval Quality

---

# 📜 License

This project is intended for educational and research purposes.