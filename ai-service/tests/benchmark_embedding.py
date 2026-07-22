import time
from sentence_transformers import SentenceTransformer

# -------------------------
# 1. Import timing
# -------------------------
start = time.time()
from sentence_transformers import SentenceTransformer
print(f"Import: {time.time() - start:.2f} sec")

# -------------------------
# 2. Model loading timing
# -------------------------
MODEL_PATH = "/models/bge-m3"

start = time.time()
model = SentenceTransformer(MODEL_PATH)
print(f"Model load: {time.time() - start:.2f} sec")

# -------------------------
# 3. Create realistic chunks
# -------------------------

# 400 words
paragraph = (
    "Artificial intelligence is transforming industries by enabling machines "
    "to learn from data make predictions automate repetitive tasks improve "
    "decision making and assist developers in building intelligent software "
) * 25   # ~425 words

dummy = [paragraph] * 27

print("\nBenchmark Information")
print("----------------------")
print(f"Chunks: {len(dummy)}")
print(f"Words per chunk: {len(dummy[0].split())}")
print(f"Characters per chunk: {len(dummy[0])}")

# -------------------------
# 4. Inference timing
# -------------------------
start = time.time()

embeddings = model.encode(
    dummy,
    batch_size=32,
    show_progress_bar=True
)

print("\nResults")
print("----------------------")
print(f"Inference: {time.time() - start:.2f} sec")
print(f"Embeddings generated: {len(embeddings)}")
print(f"Embedding dimension: {len(embeddings[0])}")