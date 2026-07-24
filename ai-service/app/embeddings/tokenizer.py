import os
from pathlib import Path

from transformers import AutoTokenizer

model_path = os.getenv("LOCAL_EMBEDDING_MODEL_PATH")

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