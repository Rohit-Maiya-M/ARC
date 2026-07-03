# app/services/vector_store_service.py
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility, Index
from app.services.embedding_service import EmbeddingService

class VectorStoreService:
    def __init__(self, dim: int = 1024, collection_name: str = "ims_embeddings"):
        self.embedding_service = EmbeddingService()
        connections.connect("default", host="127.0.0.1", port="19530")

        fields = [
            FieldSchema(name="chunk_id", dtype=DataType.VARCHAR, max_length=64, is_primary=True),
            FieldSchema(name="repository_id", dtype=DataType.INT64),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=8000),
            FieldSchema(name="filename", dtype=DataType.VARCHAR, max_length=256),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="meta_embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
        ]
        schema = CollectionSchema(fields, description="ARC repository embeddings")

        self.collection_name = collection_name
        if not utility.has_collection(self.collection_name):
            self.collection = Collection(self.collection_name, schema)

            index_params = {
                "index_type": "IVF_FLAT",
                "metric_type": "IP", 
                "params": {"nlist": 128}
            }
            Index(self.collection, "embedding", index_params)
            Index(self.collection, "meta_embedding", index_params)
        else:
            self.collection = Collection(self.collection_name)

        self.collection.load()

    def store_embedding(self, chunk_id: str, repository_id: int, content: str, embedding: list, metadata: dict):
        metadata = {**metadata, "repository_id": repository_id, "chunk_id": chunk_id}
        meta_embedding = self.embedding_service.generate_metadata_embedding(metadata)

        self.collection.insert([{
            "chunk_id": chunk_id,
            "repository_id": repository_id,
            "content": content,
            "filename": metadata.get("filename", ""),
            "embedding": embedding,
            "meta_embedding": meta_embedding
        }])
        self.collection.flush()

    def store_batch(self, requests: list):
        embeddings = [self.embedding_service.generate_embedding(r["content"]) for r in requests]
        meta_embeddings = [
            self.embedding_service.generate_metadata_embedding(
                {**r.get("metadata", {}), "repository_id": r["repository_id"], "chunk_id": r["chunk_id"]}
            )
            for r in requests
        ]

        rows = []
        for r, emb, meta_emb in zip(requests, embeddings, meta_embeddings):
            rows.append({
                "chunk_id": r["chunk_id"],
                "repository_id": r["repository_id"],
                "content": r["content"],
                "filename": r.get("metadata", {}).get("filename", ""),
                "embedding": emb,
                "meta_embedding": meta_emb
            })

        self.collection.insert(rows)
        self.collection.flush()

    def count_documents(self):
        return self.collection.num_entities

    def get_repository_documents(self, repository_id: int, limit: int = 20):
        expr = f"repository_id == {repository_id}"
        results = self.collection.query(
            expr=expr,
            output_fields=["content", "filename", "meta_embedding"],
            limit=limit
        )
        docs = [r["content"] for r in results]
        metas = [{"filename": r["filename"], "meta_embedding": r["meta_embedding"]} for r in results]
        return {"documents": docs, "metadatas": metas}

    def get_all_docs(self, repository_id: int):
        repository_documents = self.get_repository_documents(repository_id, limit=1000)
        return repository_documents.get("documents", [])