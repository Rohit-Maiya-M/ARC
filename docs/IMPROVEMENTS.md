chunk_id                UUID (PK)

repository_id           UUID
repository_name         VARCHAR(256)

file_id                 UUID
file_name               VARCHAR(256)
relative_path           VARCHAR(1024)

language                VARCHAR(32)
extension               VARCHAR(32)

symbol_path             VARCHAR(512)
symbol_name             VARCHAR(256)
symbol_type             VARCHAR(64)

chunk_index             INT32
chunk_count             INT32

symbol_chunk_index      INT32
symbol_chunk_count      INT32

token_start             INT32
token_end               INT32
token_count             INT32

line_start              INT32
line_end                INT32

content_hash            VARCHAR(64)

content                 VARCHAR(8000)

embedding               FLOAT_VECTOR(768)
meta_embedding          FLOAT_VECTOR(768)

I actually **would not touch the Spring Boot side first**.

From the architecture we've built over the last few days, Spring Boot has one responsibility:

```text
Receive ZIP
↓

Extract Repository

↓

Read Files

↓

Send RepositoryFile to Kafka
```

Spring should remain completely **language agnostic**.

It should **never know** what a Java class is, what a Python function is, or what a Rust trait is.

---

## Why the chunker belongs in Python

Right now your FastAPI service is responsible for:

* Embeddings
* Milvus
* Retrieval
* LLM
* Aider (future)

Tree-sitter naturally belongs here too.

The new pipeline becomes:

```text
Spring Boot
────────────────────────

ZIP Upload

↓

Repository Scanner

↓

RepositoryFile

↓

Kafka

────────────────────────
        │
        ▼

FastAPI
────────────────────────

Language Detection

↓

Tree-sitter

↓

Symbol Extraction

↓

Token-aware Chunking

↓

Embeddings

↓

Milvus
```

Now your entire AI pipeline lives in one service.

---

# Why not Spring?

Imagine six months from now you add

* Java
* Python
* Go
* Rust
* Kotlin
* TypeScript
* C#
* C++
* Swift

If parsing happens in Spring:

```
Spring Boot

↓

Java Parser

↓

Python Parser

↓

Go Parser

↓

Rust Parser

...
```

Now your backend suddenly depends on ten language parsers.

That's the opposite of separation of concerns.

---

# Python already has everything

Think about what FastAPI already owns.

```
Tokenizer

↓

Chunker

↓

Embeddings

↓

Milvus

↓

LLM

↓

Aider
```

Tree-sitter is simply another preprocessing step.

---

# I would slightly rename the module

Instead of

```
chunking/
```

I'd rename it

```
indexing/
```

because it is doing much more than chunking.

For example:

```
app/

    indexing/

        language_detector.py

        parser_factory.py

        symbol_extractor.py

        symbol_chunker.py

        token_chunker.py

        models.py
```

Notice there isn't a "TreeSitterChunker."

There are separate responsibilities.

---

# Proposed Architecture

```
RepositoryFile

↓

LanguageDetector

↓

ParserFactory

↓

Language Parser

↓

SymbolExtractor

↓

SymbolChunker

↓

EmbeddingService

↓

Milvus
```

Each module has one job.

---

# Phase 1

The very first thing I would implement is

```
LanguageDetector
```

Nothing else.

Input

```
RepositoryService.java
```

Output

```
language = java
```

or

```
language = python
```

or

```
language = javascript
```

This is extremely easy.

---

# Phase 2

Then

```
ParserFactory
```

Example

```python
language = "java"

↓

return JavaParser()
```

or

```python
language = "python"

↓

return PythonParser()
```

or

```python
language = "go"

↓

return GoParser()
```

---

# Phase 3

Only then do we install Tree-sitter.

I'd install only one language first:

```
Java
```

because ARC itself is written in Java.

---

# Directory after Java support

```
indexing/

    language_detector.py

    parser_factory.py

    java_parser.py

    symbol_chunker.py

    token_chunker.py
```

Once Java works

add

```
python_parser.py
```

Then

```
typescript_parser.py
```

and so on.

---

# Don't download 20 parsers today

This is probably the biggest piece of advice I'd give.

Don't install every parser.

Implement one completely.

I'd do

```
Java
```

first.

Once you're happy with the design,

adding Python becomes about **100–200 lines**, not redesigning the architecture.

---

## My recommended roadmap

```
✅ Step 1
Create app/indexing/
```

↓

```
✅ Step 2
LanguageDetector
```

↓

```
✅ Step 3
ParserFactory
```

↓

```
✅ Step 4
Install Tree-sitter core
```

↓

```
✅ Step 5
Install ONLY Java grammar
```

↓

```
✅ Step 6
Extract

Class

Method

Constructor

Interface

Enum
```

↓

```
✅ Step 7
Convert symbols into chunks
```

↓

```
✅ Step 8
If symbol >384 tokens

↓

Token split
```

↓

```
✅ Step 9
Generate embeddings
```

↓

```
✅ Step 10
Milvus
```

---

I think this is the cleanest path because **the architecture stabilizes after Java**. Every additional language then plugs into the same `ParserFactory` and `SymbolExtractor` interfaces, rather than forcing changes throughout the pipeline. That's the kind of extensible design that will serve ARC well as you expand language support and integrate Aider.


program
│
└── class_declaration
    │
    ├── modifiers
    │
    ├── identifier (HelloWorld)
    │
    └── class_body
         │
         └── method_declaration
              │
              ├── modifiers
              ├── void_type
              ├── identifier (hello)
              ├── formal_parameters
              └── block
                    │
                    └── expression_statement
                          │
                          └── method_invocation
                                │
                                ├── field_access
                                │
                                └── argument_list


✅ Detect class_declaration

↓

🔜 Find identifier child

↓

🔜 Create first CodeSymbol (Class)

↓

🔜 Detect method_declaration

↓

🔜 Create second CodeSymbol (Method)

↓

🔜 Add constructors

↓

🔜 Add interfaces

↓

🔜 Add enums

↓

🔜 Add records

↓

✅ JavaParser complete                                