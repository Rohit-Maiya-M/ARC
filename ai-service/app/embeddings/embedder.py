import os
import numpy as np

from app.embeddings.engine import getSession
from app.embeddings.tokenizer import getTokenizer
from app.embeddings.models.embedded_chunk import EmbeddedChunk
from app.indexing.models.code_chunk import CodeChunk

MAX_LENGTH = int(
    os.getenv(
        "EMBEDDING_MAX_LENGTH",
        "512",
    )
)

ENABLE_TOKEN_DEBUG = (
    os.getenv(
        "ENABLE_TOKEN_DEBUG",
        "false",
    ).lower() == "true"
)

tokenizer = getTokenizer()
session = getSession()


class Embedder:

    def __init__(self):

        self.tokenizer = tokenizer
        self.session = session

    def _encode(
        self,
        texts,
    ):

        single_input = isinstance(
            texts,
            str,
        )

        if single_input:
            texts = [texts]

        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=MAX_LENGTH,
            return_tensors="np",
        )

        session_inputs = {
            "input_ids": inputs["input_ids"],
            "attention_mask": inputs["attention_mask"],
        }

        if "token_type_ids" in inputs:
            session_inputs["token_type_ids"] = (
                inputs["token_type_ids"]
            )

        outputs = self.session.run(
            None,
            session_inputs,
        )

        output_names = [
            output.name
            for output in self.session.get_outputs()
        ]

        if "sentence_embedding" in output_names:

            embeddings = outputs[
                output_names.index(
                    "sentence_embedding"
                )
            ]

        elif "last_hidden_state" in output_names:

            last_hidden_state = outputs[
                output_names.index(
                    "last_hidden_state"
                )
            ]

            # CLS Pooling
            embeddings = last_hidden_state[:, 0, :]

        else:

            raise RuntimeError(
                f"Unsupported ONNX outputs: {output_names}"
            )

        norms = np.linalg.norm(
            embeddings,
            axis=1,
            keepdims=True,
        )

        norms = np.where(
            norms == 0,
            1e-12,
            norms,
        )

        embeddings = embeddings / norms

        if single_input:
            return embeddings[0]

        return embeddings

    def embed(
        self,
        text: str,
    ):

        return self._encode(text).tolist()

    def embed_batch(
        self,
        texts: list[str],
        debug: bool = True,
    ):

        texts = [
            text.strip()
            for text in texts
            if text and text.strip()
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

            word_counts = [
                len(text.split())
                for text in texts
            ]

            char_counts = [
                len(text)
                for text in texts
            ]

            print(f"Min words : {min(word_counts)}")
            print(f"Max words : {max(word_counts)}")
            print(
                f"Avg words : "
                f"{sum(word_counts)/len(word_counts):.2f}"
            )

            print(f"Min chars : {min(char_counts)}")
            print(f"Max chars : {max(char_counts)}")
            print(
                f"Avg chars : "
                f"{sum(char_counts)/len(char_counts):.2f}"
            )

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
                            add_special_tokens=True,
                        )["input_ids"]

                    )

                    for text in texts
                ]

                print("\nTOKEN STATISTICS")
                print("-" * 90)

                print(
                    f"Min tokens : {min(token_lengths)}"
                )

                print(
                    f"Max tokens : {max(token_lengths)}"
                )

                print(
                    f"Avg tokens : "
                    f"{sum(token_lengths)/len(token_lengths):.2f}"
                )

                longest_idx = max(
                    range(len(token_lengths)),
                    key=token_lengths.__getitem__,
                )

                print(
                    f"Longest chunk index : {longest_idx}"
                )

                print(
                    f"Longest chunk tokens: "
                    f"{token_lengths[longest_idx]}"
                )

                print("-" * 90)

        embeddings = self._encode(texts)

        if debug:

            print()
            print(
                f"Embeddings : {len(embeddings)}"
            )

            print(
                f"Dimension  : {embeddings.shape[1]}"
            )

            print("=" * 90)

        return embeddings.tolist()

    def embed_chunks(
        self,
        chunks: list[CodeChunk],
    ) -> list[EmbeddedChunk]:

        if not chunks:
            return []

        embeddings = self.embed_batch(
            [
                chunk.content
                for chunk in chunks
            ],
            debug=False,
        )

        return [
            EmbeddedChunk(
                chunk=chunk,
                embedding=embedding,
            )
            for chunk, embedding in zip(
                chunks,
                embeddings,
            )
        ]