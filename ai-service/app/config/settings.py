from dotenv import load_dotenv

import os
from urllib.parse import urlparse


load_dotenv()


LLM_MODEL_PATH = os.getenv(
    "LLM_MODEL_PATH"
)

EMBEDDING_MODEL_PATH = os.getenv(
    "EMBEDDING_MODEL_PATH"
)

LLAMA_SERVER_PATH = os.getenv(
    "LLAMA_SERVER_PATH"
)

CHROMA_DB_PATH = os.getenv(
    "CHROMA_DB_PATH"
)

LLM_SERVER_PATH = os.getenv(
    "LLM_SERVER_PATH"
)

LLAMA_SERVER_WORKDIR = os.getenv(
    "LLAMA_SERVER_WORKDIR"
)

LLAMA_N_GPU_LAYERS = int(
    os.getenv(
        "LLAMA_N_GPU_LAYERS",
        "999"
    )
)

LLAMA_CTX_SIZE = int(
    os.getenv(
        "LLAMA_CTX_SIZE",
        "4096"
    )
)

LLAMA_THREADS = int(
    os.getenv(
        "LLAMA_THREADS",
        "8"
    )
)

FASTAPI_HOST = os.getenv(
    "FASTAPI_HOST",
    "127.0.0.1"
)

FASTAPI_PORT = int(
    os.getenv(
        "FASTAPI_PORT",
        "8000"
    )
)


def _resolve_llm_server_port() -> int:
    parsed_url = urlparse(
        LLM_SERVER_PATH or ""
    )

    return parsed_url.port or 8081


LLM_SERVER_PORT = int(
    os.getenv(
        "LLM_SERVER_PORT",
        str(
            _resolve_llm_server_port()
        )
    )
)
