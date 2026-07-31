import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parents[3]
load_dotenv(ROOT / ".env")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "384"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "64"))

MIN_CHUNK_SIZE = int(os.getenv("MIN_CHUNK_SIZE", "128"))
MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", "512"))