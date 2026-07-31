from typing import List

from app.chunking.chunk_config import ChunkConfig
from app.embeddings.tokenizer import getTokenizer
from app.chunking.token_chunk import TokenChunk

class TokenAwareChunker:
    def __init__(self):
        self.tokenizer = getTokenizer()
        self.config = ChunkConfig()

    def chunk(self, text: str) -> List[TokenChunk]:
        
        if not text or not text.strip():
            return []

        token_ids = self.tokenizer.encode(
            text,
            add_special_tokens=False
        )

        chunks: list[TokenChunk] = []

        start = 0
        step = self.config.chunk_size - self.config.overlap

        while start < len(token_ids):

            end = min(
                start + self.config.chunk_size,
                len(token_ids)
            )

            chunk_ids = token_ids[start:end]

            chunk_text = self.tokenizer.decode(
                chunk_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False
            )

            chunks.append(
                TokenChunk(
                    token_ids=chunk_ids,
                    text=chunk_text
                )
            )

            if end == len(token_ids):
                break

            start += step

        print("=" * 50)
        print("TOKEN AWARE CHUNKING")
        print("=" * 50)
        print(f"Total tokens : {len(token_ids)}")
        print(f"Chunk size   : {self.config.chunk_size}")
        print(f"Overlap      : {self.config.overlap}")
        print(f"Chunks       : {len(chunks)}")
        print("=" * 50)
        
        return chunks

