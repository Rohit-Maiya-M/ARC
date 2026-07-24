import time
from app.embeddings.embedder import Embedder

embedder = Embedder()

print("\n" + "=" * 90)
print("FUNCTIONAL TEST")
print("=" * 90)

tests = [
    "",
    "Hello World",
    "The quick brown fox jumps over the lazy dog.",
    "Spring Boot REST API with JWT authentication.",
    "Milvus is an open-source vector database.",
    "こんにちは नमस्ते مرحبا 😀 Spring Boot",
    "public class UserService {\n    public void save(User user) {}\n}",
    " ".join(["Artificial Intelligence"] * 500),
]

for i, text in enumerate(tests, start=1):

    print(f"\nTest {i}")
    print("-" * 90)

    preview = text[:80].replace("\n", "\\n")
    print("Input :", preview)

    start = time.perf_counter()

    embedding = embedder.embed(text)

    elapsed = time.perf_counter() - start

    print(f"Time      : {elapsed:.4f} sec")
    print(f"Dimension : {len(embedding)}")

    print(f"Min value : {min(embedding):.6f}")
    print(f"Max value : {max(embedding):.6f}")

    norm = sum(x * x for x in embedding) ** 0.5
    print(f"L2 Norm   : {norm:.6f}")

print("\n" + "=" * 90)
print("ALL TESTS PASSED")
print("=" * 90)