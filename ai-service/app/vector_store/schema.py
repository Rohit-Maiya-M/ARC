from pymilvus import (
    CollectionSchema,
    DataType,
    FieldSchema,
)


def create_schema(dim: int) -> CollectionSchema:
    """
    Creates the Milvus collection schema for embedded code chunks.
    """

    fields = [

        FieldSchema(
            name="chunk_id",
            dtype=DataType.VARCHAR,
            max_length=128,
            is_primary=True,
        ),

        FieldSchema(
            name="repository_id",
            dtype=DataType.VARCHAR,
            max_length=64,
        ),

        FieldSchema(
            name="repository_name",
            dtype=DataType.VARCHAR,
            max_length=256,
        ),

        FieldSchema(
            name="file_id",
            dtype=DataType.VARCHAR,
            max_length=64,
        ),

        FieldSchema(
            name="file_name",
            dtype=DataType.VARCHAR,
            max_length=256,
        ),

        FieldSchema(
            name="relative_path",
            dtype=DataType.VARCHAR,
            max_length=1024,
        ),

        FieldSchema(
            name="language",
            dtype=DataType.VARCHAR,
            max_length=32,
        ),

        FieldSchema(
            name="symbol_name",
            dtype=DataType.VARCHAR,
            max_length=256,
        ),

        FieldSchema(
            name="symbol_type",
            dtype=DataType.VARCHAR,
            max_length=64,
        ),

        FieldSchema(
            name="symbol_path",
            dtype=DataType.VARCHAR,
            max_length=1024,
        ),

        FieldSchema(
            name="chunk_index",
            dtype=DataType.INT64,
        ),

        FieldSchema(
            name="symbol_chunk_index",
            dtype=DataType.INT64,
        ),

        FieldSchema(
            name="line_start",
            dtype=DataType.INT64,
        ),

        FieldSchema(
            name="line_end",
            dtype=DataType.INT64,
        ),

        FieldSchema(
            name="token_start",
            dtype=DataType.INT64,
        ),

        FieldSchema(
            name="token_end",
            dtype=DataType.INT64,
        ),

        FieldSchema(
            name="token_count",
            dtype=DataType.INT64,
        ),

        FieldSchema(
            name="content_hash",
            dtype=DataType.VARCHAR,
            max_length=64,
        ),

        FieldSchema(
            name="content",
            dtype=DataType.VARCHAR,
            max_length=32768,
        ),

        FieldSchema(
            name="embedding",
            dtype=DataType.FLOAT_VECTOR,
            dim=dim,
        ),
    ]

    return CollectionSchema(
        fields=fields,
        description="ARC Code Chunks",
    )


def get_index_params() -> dict:
    """
    Returns the Milvus index configuration.
    """

    return {
        "index_type": "IVF_FLAT",
        "metric_type": "IP",
        "params": {
            "nlist": 128,
        },
    }