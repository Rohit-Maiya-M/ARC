import os
import platform
import time

import numpy as np
import onnxruntime as ort

from app.embeddings.engine import getSession
from app.embeddings.tokenizer import getTokenizer


MAX_LENGTH = int(os.getenv("EMBEDDING_MAX_LENGTH", "512"))
ENABLE_TOKEN_DEBUG = (
    os.getenv("ENABLE_TOKEN_DEBUG", "false").lower() == "true"
)

print("\n" + "=" * 90)
print("EMBEDDING SERVICE STARTUP")
print("=" * 90)

load_start = time.perf_counter()

tokenizer = getTokenizer()
session = getSession()

load_elapsed = time.perf_counter() - load_start

print(f"Tokenizer id        : {id(tokenizer)}")
print(f"Session id          : {id(session)}")
print(f"Model load time     : {load_elapsed:.2f} sec")
embedding_dim = (
    session.get_outputs()[0].shape[-1]
    if session.get_outputs()[0].shape[-1] is not None
    else "Unknown"
)
print(f"Embedding dimension : {embedding_dim}")
print(f"CPU count           : {os.cpu_count()}")
print(f"ONNX Runtime        : {ort.__version__}")
print(f"Platform            : {platform.platform()}")

print(f"Providers           : {session.get_providers()}")
print(f"Inputs              : {[i.name for i in session.get_inputs()]}")
print(f"Outputs             : {[o.name for o in session.get_outputs()]}")
print(f"Max Length          : {MAX_LENGTH}")

print("=" * 90 + "\n")


class Embedder:

    def __init__(self):
        self.tokenizer = tokenizer
        self.session = session

        print(f"Embedder tokenizer id : {id(self.tokenizer)}")
        print(f"Embedder session id   : {id(self.session)}")

    def _encode(self, texts):

        single_input = isinstance(texts, str)

        if single_input:
            texts = [texts]

        t0 = time.perf_counter()

        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=MAX_LENGTH,
            return_tensors="np"
        )

        t1 = time.perf_counter()

        print(
            f"Batch size : {inputs['input_ids'].shape[0]} | "
            f"Sequence length : {inputs['input_ids'].shape[1]}"
        )

        session_inputs = {
            "input_ids": inputs["input_ids"],
            "attention_mask": inputs["attention_mask"],
        }

        if "token_type_ids" in inputs:
            session_inputs["token_type_ids"] = inputs["token_type_ids"]

        outputs = self.session.run(
            None,
            session_inputs
        )

        t2 = time.perf_counter()

        output_names = [o.name for o in self.session.get_outputs()]

        if "sentence_embedding" in output_names:
            sentence_embedding_index = output_names.index("sentence_embedding")
            embeddings = outputs[sentence_embedding_index]

        elif "last_hidden_state" in output_names:
            last_hidden_state_index = output_names.index("last_hidden_state")
            last_hidden_state = outputs[last_hidden_state_index]

            # CLS Pooling
            embeddings = last_hidden_state[:, 0, :]

        else:
            raise RuntimeError(
                f"Unsupported ONNX outputs: {output_names}"
            )

        norms = np.linalg.norm(
            embeddings,
            axis=1,
            keepdims=True
        )

        norms = np.where(norms == 0, 1e-12, norms)

        embeddings = embeddings / norms

        t3 = time.perf_counter()

        print(
            f"Tokenizer : {t1 - t0:.3f} sec | "
            f"ONNX : {t2 - t1:.3f} sec | "
            f"Normalize : {t3 - t2:.3f} sec"
        )

        if single_input:
            return embeddings[0]

        return embeddings


    def embed(self, text: str):
        return self._encode(text).tolist()

    def embed_batch(self, texts: list, debug: bool = True):

        texts = [
            t.strip()
            for t in texts
            if t and t.strip()
        ]

        if not texts:
            if debug:
                print("No valid chunks.")
            return []

        if debug:

            print("\n" + "=" * 90)
            print("CONTENT EMBEDDING DEBUG")
            print("=" * 90)

            print(f"Chunks: {len(texts)}")

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

            if ENABLE_TOKEN_DEBUG:

                token_lengths = [
                    len(
                        self.tokenizer(
                            text,
                            truncation=False,
                            add_special_tokens=True
                        )["input_ids"]
                    )
                    for text in texts
                ]

                print("\nTOKEN STATISTICS")
                print("-" * 90)
                print(f"Min tokens : {min(token_lengths)}")
                print(f"Max tokens : {max(token_lengths)}")
                print(f"Avg tokens : {sum(token_lengths)/len(token_lengths):.2f}")

                longest_idx = max(
                    range(len(token_lengths)),
                    key=token_lengths.__getitem__
                )

                print(f"Longest chunk index : {longest_idx}")
                print(f"Longest chunk tokens: {token_lengths[longest_idx]}")
                print("-" * 90)

        start = time.perf_counter()

        embeddings = self._encode(texts)

        if debug:

            elapsed = time.perf_counter() - start

            print()
            print(f"encode() took : {elapsed:.2f} sec")
            print(f"Embeddings    : {len(embeddings)}")
            print(f"Dimension     : {embeddings.shape[1]}")
            print("=" * 90)

        return embeddings.tolist()

    def embed_metadata(self, metadata: dict):

        meta_text = " ".join(
            filter(
                None,
                [
                    metadata.get("filename", ""),
                    metadata.get("path", ""),
                    metadata.get("extension", "")
                ]
            )
        )

        return self._encode(meta_text).tolist()

    def embed_metadata_batch(self, metadata_list: list, debug: bool = True):

        texts = [
            " ".join(
                filter(
                    None,
                    [
                        m.get("filename", ""),
                        m.get("path", ""),
                        m.get("extension", "")
                    ]
                )
            )
            for m in metadata_list
        ]

        if debug:

            print("\n" + "=" * 90)
            print("METADATA EMBEDDING DEBUG")
            print("=" * 90)

        start = time.perf_counter()

        embeddings = self._encode(texts)

        if debug:

            elapsed = time.perf_counter() - start

            print(f"Metadata encode() took : {elapsed:.2f} sec")
            print("=" * 90)

        return embeddings.tolist()