from app.indexing.models.repository_file import RepositoryFile
from app.indexing.repository_indexer import RepositoryIndexer
from app.vector_store.milvus_service import MilvusService

from tests.utils.resource_loader import load_resource


def test_milvus_insert():


    repository_file = RepositoryFile(
        repository_id="repo1",
        repository_name="ARC",

        file_id="file1",
        file_name="Example.java",

        relative_path="src/Example.java",
        extension=".java",

        content=load_resource(
            "java",
            "Example.java",
        ),
    )

    indexer = RepositoryIndexer()

    milvus = MilvusService()


    milvus.delete_repository(
        repository_file.repository_id
    )


    embedded_chunks = indexer.index(
        repository_file
    )

    assert len(embedded_chunks) > 0

    milvus.insert(
        embedded_chunks
    )

    rows = milvus.query_repository(
        repository_file.repository_id
    )

    assert len(rows) == len(embedded_chunks)

    for row in rows:

        assert row["repository_id"] == "repo1"
        assert row["repository_name"] == "ARC"

        assert row["file_id"] == "file1"
        assert row["file_name"] == "Example.java"
        assert row["relative_path"] == "src/Example.java"

        assert row["language"] == "java"

        assert row["symbol_name"] != ""
        assert row["symbol_type"] != ""
        assert row["symbol_path"] != ""

        assert row["chunk_index"] >= 0

        assert row["line_start"] > 0
        assert row["line_end"] >= row["line_start"]

        assert row["token_start"] >= 0
        assert row["token_end"] > row["token_start"]

        assert row["token_count"] > 0

        assert row["content"] != ""
        assert row["content_hash"] != ""

        assert len(row["embedding"]) == 768

    class_chunk = next(
        row
        for row in rows
        if row["symbol_name"] == "Example"
        and row["symbol_type"] == "class"
    )

    assert "public class Example" in class_chunk["content"]

    hello_chunk = next(
        row
        for row in rows
        if row["symbol_name"] == "hello"
    )

    assert hello_chunk["symbol_type"] == "method"
    assert hello_chunk["symbol_path"] == "Example/hello"
    assert "public void hello" in hello_chunk["content"]

    constructor_chunk = next(
        row
        for row in rows
        if row["symbol_type"] == "constructor"
    )

    assert constructor_chunk["symbol_name"] == "Example"
    assert constructor_chunk["symbol_path"] == "Example/Example"

    milvus.delete_repository(
        repository_file.repository_id
    )