from dataclasses import dataclass

from app.indexing.models.code_chunk import CodeChunk


@dataclass(slots=True, frozen=True)
class EmbeddedChunk:

    chunk: CodeChunk

    embedding: list[float]