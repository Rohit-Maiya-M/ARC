from app.embeddings.tokenizer import getTokenizer
from app.indexing.chunking.hash_util import sha256
from app.indexing.models.code_chunk import CodeChunk
from app.indexing.models.code_symbol import CodeSymbol
from app.indexing.chunking.semantic_chunker import SemanticChunker
from app.indexing.models.repository_file import RepositoryFile

from app.indexing.chunking.constants import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

from app.indexing.chunking.token_window import TokenWindow
from app.indexing.chunking.line_tracker import LineTracker


class SymbolChunker:

    def __init__(self):
        self.tokenizer = getTokenizer()
        self.line_tracker = LineTracker()
        self.semantic_chunker = SemanticChunker()

    def chunk(
        self,
        repository_file: RepositoryFile,
        symbols: list[CodeSymbol],
    ) -> list[CodeChunk]:
        """
        Convert CodeSymbols into CodeChunks.
        """

        chunks: list[CodeChunk] = []

        for symbol in symbols:
            chunks.extend(
                self._chunk_symbol(
                    repository_file=repository_file,
                    symbol=symbol,
                )
            )

        return chunks

    def _chunk_symbol(
        self,
        repository_file: RepositoryFile,
        symbol: CodeSymbol,
    ) -> list[CodeChunk]:
        """
        Split a single CodeSymbol into one or more CodeChunks.
        """

        if not symbol.content.strip():
            return []

        encoding = self.tokenizer(
            symbol.content,
            add_special_tokens=False,
            return_offsets_mapping=True,
            truncation=False,
            max_length=None,
        )

        token_ids = encoding["input_ids"]
        offset_mapping = encoding["offset_mapping"]

        windows = self._split_windows(token_ids)

        windows = self.semantic_chunker.optimize(
            token_ids,
            windows,
        )

        chunks: list[CodeChunk] = []

        chunk_count = len(windows)

        for chunk_index, window in enumerate(windows):
            chunks.append(
                self._build_chunk(
                    repository_file=repository_file,
                    symbol=symbol,
                    window=window,
                    offset_mapping=offset_mapping,
                    chunk_index=chunk_index,
                    chunk_count=chunk_count,
                )
            )

        return chunks

    def _split_windows(
            self,
            token_ids: list[int],
    ) -> list[TokenWindow]:
        """
        Split token ids into overlapping windows.
        """

        if not token_ids:
            return []

        if CHUNK_OVERLAP >= CHUNK_SIZE:
            raise ValueError(
                "CHUNK_OVERLAP must be smaller than CHUNK_SIZE."
            )

        windows: list[TokenWindow] = []

        step = CHUNK_SIZE - CHUNK_OVERLAP

        start = 0

        while start < len(token_ids):

            end = min(
                start + CHUNK_SIZE,
                len(token_ids),
            )

            windows.append(
                TokenWindow(
                    token_start=start,
                    token_end=end,
                    token_ids=token_ids[start:end],
                )
            )

            if end >= len(token_ids):
                break

            start += step

        return windows

    def _build_chunk(
        self,
        repository_file: RepositoryFile,
        symbol: CodeSymbol,
        window: TokenWindow,
        offset_mapping: list[tuple[int, int]],
        chunk_index: int,
        chunk_count: int,
    ) -> CodeChunk:
        """
        Build a CodeChunk from a TokenWindow.
        """

        start_char = offset_mapping[window.token_start][0]
        end_char = offset_mapping[window.token_end - 1][1]

        chunk_content = symbol.content[start_char:end_char]

        line_start, line_end = self.line_tracker.get_line_range(
            text=symbol.content,
            offset_mapping=offset_mapping,
            token_start=window.token_start,
            token_end=window.token_end,
        )

        line_start += symbol.start_line - 1
        line_end += symbol.start_line - 1

        return CodeChunk(

            repository_id=repository_file.repository_id,
            repository_name=repository_file.repository_name,

            file_id=repository_file.file_id,
            file_name=repository_file.file_name,
            relative_path=repository_file.relative_path,

            language=symbol.language,

            symbol_name=symbol.symbol_name,
            symbol_type=symbol.symbol_type,
            symbol_path=symbol.symbol_path,

            chunk_index=chunk_index,
            chunk_count=chunk_count,

            symbol_chunk_index=chunk_index,
            symbol_chunk_count=chunk_count,

            token_start=window.token_start,
            token_end=window.token_end,
            token_count=window.token_count,

            line_start=line_start,
            line_end=line_end,

            content_hash=sha256(chunk_content),
            content=chunk_content,
        )