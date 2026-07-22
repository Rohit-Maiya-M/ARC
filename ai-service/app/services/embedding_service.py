from sentence_transformers import SentenceTransformer
from functools import lru_cache
import os
import time
import torch
import platform

print("\n" + "=" * 90)
print("EMBEDDING SERVICE STARTUP")
print("=" * 90)

load_start = time.perf_counter()

model = SentenceTransformer(os.getenv("EMBEDDING_MODEL_PATH"))

load_elapsed = time.perf_counter() - load_start

print(f"Model object id      : {id(model)}")
print(f"Model load time      : {load_elapsed:.2f} sec")
print(f"Embedding dimension  : {model.get_embedding_dimension()}")
print(f"CPU count            : {os.cpu_count()}")
print(f"Torch version        : {torch.__version__}")
print(f"Torch threads        : {torch.get_num_threads()}")
print(f"Torch interop threads: {torch.get_num_interop_threads()}")
print(f"Model path           : {os.getenv('EMBEDDING_MODEL_PATH')}")
print(f"Platform             : {platform.platform()}")

for var in (
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    print(f"{var:20}: {os.getenv(var)}")

print("=" * 90 + "\n")


class EmbeddingService:

    def __init__(self):
        self.model = model

        print(f"EmbeddingService using model id: {id(self.model)}")
        print(f"Max sequence length            : {self.model.max_seq_length}")
        print(f"Tokenizer                      : {type(self.model.tokenizer).__name__}")

    @lru_cache(maxsize=1000)
    def generate_embedding(self, text: str):
        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )
        return embedding.tolist()

    def generate_batch_embeddings(self, texts: list):

        # -------------------------------------------------------------
        # Remove empty chunks
        # -------------------------------------------------------------
        texts = [
            t.strip()
            for t in texts
            if t and t.strip()
        ]

        print("\n" + "=" * 90)
        print("CONTENT EMBEDDING DEBUG")
        print("=" * 90)

        print(f"Chunks: {len(texts)}")

        if not texts:
            print("No valid chunks.")
            return []

        word_counts = [len(t.split()) for t in texts]
        char_counts = [len(t) for t in texts]

        print(f"Min words : {min(word_counts)}")
        print(f"Max words : {max(word_counts)}")
        print(f"Avg words : {sum(word_counts)/len(word_counts):.2f}")

        print(f"Min chars : {min(char_counts)}")
        print(f"Max chars : {max(char_counts)}")
        print(f"Avg chars : {sum(char_counts)/len(char_counts):.2f}")

        print("\nFirst chunk preview (500 chars)")
        print("-" * 90)
        print(texts[0][:500])
        print("-" * 90)

        # -------------------------------------------------------------
        # Token statistics
        # -------------------------------------------------------------
        tokenizer = self.model.tokenizer

        token_lengths = []

        for text in texts:
            ids = tokenizer(
                text,
                truncation=False,
                add_special_tokens=True
            )["input_ids"]

            token_lengths.append(len(ids))

        print("\nTOKEN STATISTICS")
        print("-" * 90)
        print(f"Min tokens : {min(token_lengths)}")
        print(f"Max tokens : {max(token_lengths)}")
        print(f"Avg tokens : {sum(token_lengths)/len(token_lengths):.2f}")

        longest_idx = max(
            range(len(token_lengths)),
            key=lambda i: token_lengths[i]
        )

        print(f"Longest chunk index : {longest_idx}")
        print(f"Longest chunk tokens: {token_lengths[longest_idx]}")
        print("-" * 90)

        # -------------------------------------------------------------
        # Encode
        # -------------------------------------------------------------
        start = time.perf_counter()

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        elapsed = time.perf_counter() - start

        print()
        print(f"encode() took : {elapsed:.2f} sec")
        print(f"Embeddings    : {len(embeddings)}")
        print(f"Dimension     : {len(embeddings[0])}")
        print("=" * 90)

        return embeddings.tolist()

    def generate_metadata_embedding(self, metadata: dict):

        meta_text = (
            f"{metadata.get('filename','')} "
            f"{metadata.get('path','')} "
            f"{metadata.get('extension','')}"
        )

        embedding = self.model.encode(
            meta_text,
            normalize_embeddings=True
        )

        return embedding.tolist()

    def generate_batch_metadata_embeddings(self, metadata_list: list):

        texts = [
            (
                f"{m.get('filename','')} "
                f"{m.get('path','')} "
                f"{m.get('extension','')}"
            )
            for m in metadata_list
        ]

        print("\n" + "=" * 90)
        print("METADATA EMBEDDING DEBUG")
        print("=" * 90)

        start = time.perf_counter()

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        elapsed = time.perf_counter() - start

        print(f"Metadata encode() took : {elapsed:.2f} sec")
        print("=" * 90)

        return embeddings.tolist()