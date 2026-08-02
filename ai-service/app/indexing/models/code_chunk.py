from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CodeChunk:

    repository_id: str
    repository_name: str

    file_id: str
    file_name: str
    relative_path: str

    language: str

    symbol_name: str
    symbol_type: str
    symbol_path: str

    chunk_index: int
    chunk_count: int

    symbol_chunk_index: int
    symbol_chunk_count: int

    token_start: int
    token_end: int
    token_count: int

    line_start: int
    line_end: int

    content_hash: str
    content: str