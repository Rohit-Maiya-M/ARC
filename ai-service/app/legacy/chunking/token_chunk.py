from dataclasses import dataclass
from typing import List

@dataclass
class TokenChunk:
    token_ids: List[int]
    text: str