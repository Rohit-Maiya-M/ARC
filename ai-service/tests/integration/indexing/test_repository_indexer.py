from app.indexing.models.repository_file import RepositoryFile
from app.indexing.repository_indexer import RepositoryIndexer

from tests.utils.resource_loader import load_resource


def test_repository_indexer_extracts_embedded_chunks():

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

    # --------------------------------------------------
    # First indexing
    # --------------------------------------------------

    print("\n========== FIRST INDEX ==========")

    embedded_chunks = indexer.index(
        repository_file
    )

    # --------------------------------------------------
    # Second indexing
    # --------------------------------------------------

    print("\n========== SECOND INDEX ==========")

    embedded_chunks_second = indexer.index(
        repository_file
    )

    # Both runs should produce the same result
    assert len(embedded_chunks_second) == len(embedded_chunks)

    # --------------------------------------------------
    # Basic checks
    # --------------------------------------------------

    assert len(embedded_chunks) == 4

    names = [
        embedded.chunk.symbol_name
        for embedded in embedded_chunks
    ]

    types = [
        embedded.chunk.symbol_type
        for embedded in embedded_chunks
    ]

    assert "Example" in names
    assert "hello" in names
    assert "add" in names

    assert "class" in types
    assert "constructor" in types
    assert types.count("method") == 2

    # --------------------------------------------------
    # Embedding checks
    # --------------------------------------------------

    for embedded in embedded_chunks:

        assert embedded.embedding is not None
        assert len(embedded.embedding) == 768

    # --------------------------------------------------
    # Class chunk
    # --------------------------------------------------

    example = next(
        embedded.chunk
        for embedded in embedded_chunks
        if embedded.chunk.symbol_name == "Example"
        and embedded.chunk.symbol_type == "class"
    )

    assert example.line_start == 1
    assert example.line_end >= example.line_start

    assert example.chunk_index == 0
    assert example.symbol_chunk_index == 0

    assert example.token_count > 0
    assert example.token_end > example.token_start

    assert example.content_hash != ""

    assert "public class Example" in example.content

    # --------------------------------------------------
    # Method chunk
    # --------------------------------------------------

    hello = next(
        embedded.chunk
        for embedded in embedded_chunks
        if embedded.chunk.symbol_name == "hello"
    )

    assert hello.symbol_type == "method"
    assert hello.symbol_path == "Example/hello"

    assert hello.line_start > example.line_start
    assert hello.line_end >= hello.line_start

    assert hello.token_count > 0

    assert "public void hello" in hello.content

    # --------------------------------------------------
    # Constructor chunk
    # --------------------------------------------------

    constructor = next(
        embedded.chunk
        for embedded in embedded_chunks
        if embedded.chunk.symbol_type == "constructor"
    )

    assert constructor.symbol_name == "Example"
    assert constructor.symbol_path == "Example/Example"

    # --------------------------------------------------
    # Every chunk
    # --------------------------------------------------

    for embedded in embedded_chunks:

        chunk = embedded.chunk

        assert chunk.language == "java"

        assert chunk.token_count > 0

        assert chunk.line_end >= chunk.line_start

        assert chunk.content.strip() != ""

        assert chunk.content_hash != ""