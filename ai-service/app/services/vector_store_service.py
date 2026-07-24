import os
import time

from pymilvus import (
    connections,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType,
    utility,
    Index,
)

from app.embeddings.embedder import Embedder

class VectorStoreService:

    def __init__(
        self,
        dim: int = None,
        collection_name: str = None,
    ):

        self.embedder = Embedder()

        self.milvus_host = os.getenv(
            "MILVUS_HOST",
            "localhost"
        )

        self.milvus_port = os.getenv(
            "MILVUS_PORT",
            "19530"
        )

        self.dim = dim or int(
            os.getenv(
                "VECTOR_DIM",
                "1024"
            )
        )

        self.collection_name = (
            collection_name
            or os.getenv(
                "MILVUS_COLLECTION_NAME",
                "ims_embeddings"
            )
        )

        connections.connect(
            alias="default",
            host=self.milvus_host,
            port=self.milvus_port,
        )

        fields = [

            FieldSchema(
                name="chunk_id",
                dtype=DataType.VARCHAR,
                max_length=64,
                is_primary=True,
            ),

            FieldSchema(
                name="repository_id",
                dtype=DataType.INT64,
            ),

            FieldSchema(
                name="content",
                dtype=DataType.VARCHAR,
                max_length=8000,
            ),

            FieldSchema(
                name="filename",
                dtype=DataType.VARCHAR,
                max_length=256,
            ),

            FieldSchema(
                name="embedding",
                dtype=DataType.FLOAT_VECTOR,
                dim=self.dim,
            ),

            FieldSchema(
                name="meta_embedding",
                dtype=DataType.FLOAT_VECTOR,
                dim=self.dim,
            ),
        ]

        schema = CollectionSchema(
            fields,
            description="ARC Repository Embeddings"
        )

        if not utility.has_collection(self.collection_name):

            self.collection = Collection(
                self.collection_name,
                schema=schema,
            )

            index_params = {
                "index_type": "IVF_FLAT",
                "metric_type": "IP",
                "params": {
                    "nlist": 128
                }
            }

            Index(
                self.collection,
                "embedding",
                index_params,
            )

            Index(
                self.collection,
                "meta_embedding",
                index_params,
            )

            print(f"Created collection : {self.collection_name}")

        else:

            self.collection = Collection(
                self.collection_name
            )

            print(f"Loaded collection : {self.collection_name}")

        self.collection.load()


    def store_batch(
    self,
    requests: list,
    flush: bool = False,
):

        if not requests:
            print("No requests received.")
            return

        total_start = time.perf_counter()

        print("\n" + "=" * 90)
        print(f"PROCESSING BATCH ({len(requests)} chunks)")
        print("=" * 90)
        

        start = time.perf_counter()

        texts = [
            request["content"]
            for request in requests
        ]

        embeddings = self.embedder.embed_batch(texts)

        print(
            f"✅ Content embeddings : {time.perf_counter() - start:.3f} sec"
        )

        start = time.perf_counter()

        metadata_list = [
            {
                **request.get("metadata", {}),
                "repository_id": request["repository_id"],
                "chunk_id": request["chunk_id"],
            }
            for request in requests
        ]

        meta_embeddings = self.embedder.embed_metadata_batch(
            metadata_list
        )

        print(
            f"✅ Metadata embeddings : {time.perf_counter() - start:.3f} sec"
        )

        start = time.perf_counter()

        rows = [
            {
                "chunk_id": request["chunk_id"],
                "repository_id": request["repository_id"],
                "content": request["content"],
                "filename": metadata.get("filename", ""),
                "embedding": embedding,
                "meta_embedding": meta_embedding,
            }
            for request, metadata, embedding, meta_embedding in zip(
                requests,
                metadata_list,
                embeddings,
                meta_embeddings,
            )
        ]

        print(
            f"✅ Row preparation : {time.perf_counter() - start:.3f} sec"
        )        

        start = time.perf_counter()

        self.collection.insert(rows)

        print(
            f"✅ Milvus insert : {time.perf_counter() - start:.3f} sec"
        )

        if flush:

            start = time.perf_counter()

            self.collection.flush()

            print(
                f"✅ Milvus flush : {time.perf_counter() - start:.3f} sec"
            )

        print(
            f"\n🎯 TOTAL store_batch() : {time.perf_counter() - total_start:.3f} sec"
        )

        print("=" * 90 + "\n")

    def count_documents(self):
        return self.collection.num_entities


    def get_repository_documents(
        self,
        repository_id: int,
        limit: int = 20,
    ):

        expr = f"repository_id == {repository_id}"

        results = self.collection.query(
            expr=expr,
            output_fields=[
                "content",
                "filename",
                "meta_embedding",
            ],
            limit=limit,
        )

        documents = [
            r["content"]
            for r in results
        ]

        metadata = [

            {
                "filename": r["filename"],
                "meta_embedding": r["meta_embedding"],
            }

            for r in results

        ]

        return {

            "documents": documents,

            "metadatas": metadata,

        }

    def get_all_docs(
        self,
        repository_id: int,
    ):

        repository_documents = (
            self.get_repository_documents(
                repository_id,
                limit=1000,
            )
        )

        return repository_documents.get(
            "documents",
            []
        )    
