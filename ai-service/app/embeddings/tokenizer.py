import os
from pathlib import Path
from dotenv import load_dotenv
from transformers import AutoTokenizer

ROOT = Path(__file__).parents[3]
load_dotenv(ROOT / ".env")

model_path = Path(os.getenv("LOCAL_EMBEDDING_MODEL_PATH"))

if not model_path.exists():
    model_path = ROOT / "models" / "bge-base-en-v1.5"

model_path = str(model_path)

if not model_path:
    raise RuntimeError("LOCAL_EMBEDDING_MODEL_PATH is not set.")

if not Path(model_path).exists():
    raise FileNotFoundError(
        f"Embedding model not found: {model_path}"
    )

tokenizer = AutoTokenizer.from_pretrained(
    model_path,
    use_fast=True,
    local_files_only=True
)

print("\n" + "=" * 90)
print("TOKENIZER")
print("=" * 90)
print(f"Model Path      : {model_path}")
print(f"Tokenizer Class : {tokenizer.__class__.__name__}")
print(f"Fast Tokenizer  : {tokenizer.is_fast}")
print(f"Vocab Size      : {tokenizer.vocab_size}")
print(f"Model Max Length: {tokenizer.model_max_length}")
print("=" * 90 + "\n")


def getTokenizer():
    return tokenizer