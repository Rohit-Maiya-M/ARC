from app.indexing.chunking.semantic_chunker import SemanticChunker
from app.indexing.chunking.token_window import TokenWindow
from app.indexing.chunking.constants import MIN_CHUNK_SIZE


def test_no_merge_when_single_window():

    chunker = SemanticChunker()

    token_ids = list(range(100))

    windows = [
        TokenWindow(
            token_start=0,
            token_end=100,
            token_ids=token_ids,
        )
    ]

    optimized = chunker.optimize(
        token_ids,
        windows,
    )

    assert len(optimized) == 1


def test_no_merge_when_last_window_large():

    chunker = SemanticChunker()

    token_ids = list(range(600))

    windows = [
        TokenWindow(
            token_start=0,
            token_end=384,
            token_ids=token_ids[:384],
        ),
        TokenWindow(
            token_start=320,
            token_end=600,
            token_ids=token_ids[320:600],
        ),
    ]

    optimized = chunker.optimize(
        token_ids,
        windows,
    )

    assert len(optimized) == 2


def test_merge_last_small_window():

    chunker = SemanticChunker()

    token_ids = list(range(500))

    windows = [
        TokenWindow(
            token_start=0,
            token_end=384,
            token_ids=token_ids[:384],
        ),
        TokenWindow(
            token_start=320,
            token_end=350,
            token_ids=token_ids[320:350],
        ),
    ]

    optimized = chunker.optimize(
        token_ids,
        windows,
    )

    assert len(optimized) == 1

    merged = optimized[0]

    assert merged.token_start == 0
    assert merged.token_end == 350
    assert merged.token_count == 350