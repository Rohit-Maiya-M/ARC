from app.indexing.chunking.symbol_chunker import SymbolChunker
from app.indexing.models.code_symbol import CodeSymbol


def test_empty_symbol():

    chunker = SymbolChunker()

    symbol = CodeSymbol(
        language="java",
        symbol_name="empty",
        symbol_type="method",
        symbol_path="empty",

        start_line=1,
        start_column=0,
        end_line=1,
        end_column=0,

        start_byte=0,
        end_byte=0,

        content="",
    )

    chunks = chunker.chunk([symbol])

    assert chunks == []


def test_small_symbol_generates_one_chunk():

    chunker = SymbolChunker()

    content = "public void test() { int a = 10; }"

    symbol = CodeSymbol(
        language="java",
        symbol_name="test",
        symbol_type="method",
        symbol_path="test",

        start_line=1,
        start_column=0,
        end_line=1,
        end_column=10,

        start_byte=0,
        end_byte=len(content),

        content=content,
    )

    chunks = chunker.chunk([symbol])

    assert len(chunks) == 1

    assert chunks[0].symbol_name == "test"

    assert chunks[0].token_count > 0


def test_large_symbol_generates_multiple_chunks():

    chunker = SymbolChunker()

    body = "int a = 10;\n" * 500

    content = (
        "public void test() {\n"
        + body +
        "\n}"
    )

    symbol = CodeSymbol(
        language="java",
        symbol_name="test",
        symbol_type="method",
        symbol_path="test",

        start_line=1,
        start_column=0,
        end_line=1000,
        end_column=1,

        start_byte=0,
        end_byte=len(content),

        content=content,
    )

    chunks = chunker.chunk([symbol])

    assert len(chunks) > 1

    for chunk in chunks:

        assert chunk.token_count > 0

        assert chunk.content_hash != ""