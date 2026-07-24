# import os
# import time
# import platform
# import psutil
# import torch
# from sentence_transformers import SentenceTransformer

# # ==========================================================
# # Configuration
# # ==========================================================

# from dotenv import load_dotenv
# from pathlib import Path

# ROOT = Path(__file__).resolve().parents[3]
# load_dotenv(ROOT / ".env")

# MODEL_PATH = os.getenv("LOCAL_EMBEDDING_MODEL_PATH", "/models/bge-m3")

# TEST_SENTENCE = (
#     "ARC is an AI-powered code understanding platform that uses "
#     "semantic search, vector databases, and retrieval augmented generation."
# )

# # ==========================================================
# # System Information
# # ==========================================================

# print("=" * 80)
# print("PYTORCH EMBEDDING BENCHMARK")
# print("=" * 80)

# print(f"Platform         : {platform.platform()}")
# print(f"Python           : {platform.python_version()}")
# print(f"Torch            : {torch.__version__}")
# print(f"CPU Count        : {os.cpu_count()}")
# print(f"Torch Threads    : {torch.get_num_threads()}")
# print(f"Model Path       : {MODEL_PATH}")
# print()

# process = psutil.Process()

# # ==========================================================
# # Load Model
# # ==========================================================

# print("Loading model...")

# start = time.perf_counter()

# model = SentenceTransformer(MODEL_PATH)

# load_time = time.perf_counter() - start

# print(f"Model Load Time  : {load_time:.3f} sec")
# print(f"Embedding Dim    : {model.get_embedding_dimension()}")
# print()

# # ==========================================================
# # Helper
# # ==========================================================

# def benchmark(name, texts, runs=5):
#     times = []

#     # Warmup
#     model.encode(
#         texts,
#         normalize_embeddings=True,
#         batch_size=32
#     )

#     for _ in range(runs):
#         start = time.perf_counter()

#         model.encode(
#             texts,
#             normalize_embeddings=True,
#             batch_size=32
#         )

#         elapsed = time.perf_counter() - start
#         times.append(elapsed)

#     avg = sum(times) / len(times)

#     print(f"{name}")
#     print("-" * 40)
#     print(f"Batch Size      : {len(texts)}")
#     print(f"Average Time    : {avg:.4f} sec")
#     print(f"Per Sentence    : {avg/len(texts):.6f} sec")
#     print()

# # ==========================================================
# # Benchmarks
# # ==========================================================

# benchmark("Single Sentence", [TEST_SENTENCE])

# benchmark("Batch x10", [TEST_SENTENCE] * 10)

# benchmark("Batch x100", [TEST_SENTENCE] * 100)

# benchmark("Batch x1000", [TEST_SENTENCE] * 1000)

# # ==========================================================
# # Memory Usage
# # ==========================================================

# memory = process.memory_info().rss / (1024 * 1024)

# print("=" * 80)
# print(f"Resident Memory : {memory:.2f} MB")
# print("=" * 80)

# # docker compose exec ai-service python benchmark_pytorch.py