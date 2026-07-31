from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parents[3]
load_dotenv(ROOT / ".env")

@dataclass(frozen=True)
class ChunkConfig:
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "384"))
    overlap: int = int(os.getenv("CHUNK_OVERLAP", "64"))