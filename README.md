# 🚀 ARC — Autonomous Repository Companion

> **AI-powered Repository Understanding, Semantic Code Search & Retrieval-Augmented Generation (RAG)**

---

## ✨ Overview

ARC (Autonomous Repository Companion) is an AI-powered developer assistant that indexes entire software repositories, performs semantic code search, and generates context-aware responses using Retrieval-Augmented Generation (RAG).

Unlike traditional keyword search, ARC understands the **semantic meaning** of source code, documentation, SQL files, configuration files, and project structure.

---

# 🏗️ System Architecture

```text
                          +----------------------+
                          |   React Frontend     |
                          +----------+-----------+
                                     |
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
         BAAI BGE-M3 (ONNX Runtime)                      |
                 |                                       |
                 +---------------------------------------+
                                 |
                                 ▼
                     DeepSeek Local LLM
```

---

# ⚡ Features

✅ Semantic Code Search

✅ Repository Indexing

✅ Retrieval-Augmented Generation (RAG)

✅ Hybrid Content + Metadata Search

✅ Milvus Vector Database

✅ Kafka-based Indexing Pipeline

✅ ONNX Runtime Optimized Embeddings

✅ Local LLM Inference

✅ Spring Boot Backend

✅ React Frontend

---

# 🛠️ Tech Stack

## 🎨 Frontend

- React
- Vite
- Tailwind CSS

---

## ☕ Backend

- Java 21
- Spring Boot
- Spring Security
- Spring Data JPA
- PostgreSQL

---

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
BAAI/bge-m3
```

### Inference Engine

```text
ONNX Runtime (CPU)
```

### Embedding Dimension

```text
1024
```

### Output

```text
sentence_embedding
```

### Optimization Techniques

- ✅ Singleton Tokenizer
- ✅ Singleton ONNX Session
- ✅ Dynamic Batch Encoding
- ✅ L2 Normalization
- ✅ ONNX Runtime Graph Optimization
- ✅ Multi-threaded CPU Inference

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
              Top Ranked Results
                     │
                     ▼
               DeepSeek LLM
```

The final ranking combines:

- 🎯 Semantic similarity
- 📄 Metadata similarity

to improve retrieval accuracy.

---

# ⚙️ ONNX Runtime Optimizations

The embedding engine includes:

- 🚀 Singleton Model Loading
- 🚀 Singleton Tokenizer
- 🚀 Singleton ONNX Session
- 🚀 ORT_ENABLE_ALL Graph Optimization
- 🚀 CPU Execution Provider
- 🚀 Dynamic Batch Processing
- 🚀 Normalized Embeddings

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

VECTOR_DIM=1024

MILVUS_HOST=
MILVUS_PORT=

KAFKA_BOOTSTRAP_SERVERS=

POSTGRES_HOST=
POSTGRES_PORT=

EMBEDDING_MAX_LENGTH=1024
```

---

# ▶️ Running ARC

Start the complete system

```bash
docker compose up -d
```

Stop the system

```bash
docker compose down
```

---

# 📈 Performance Optimizations

The BGE-M3 pipeline includes:

- ⚡ ONNX Runtime Optimizations
- ⚡ Dynamic Batch Encoding
- ⚡ Multi-threaded CPU Inference
- ⚡ Cached Tokenizer
- ⚡ Cached ONNX Session
- ⚡ Optimized Milvus Batch Inserts

---

# 🎯 Roadmap

- ⏳ Faster Embedding Models
- ⏳ Hybrid Lexical + Semantic Search
- ⏳ Cross-Encoder Reranking
- ⏳ Better Chunking Strategy
- ⏳ Automatic Code Editing
- ⏳ AI Response Cache
- ⏳ Multi-Repository Search

---

# 📜 License

This project is intended for educational and research purposes.