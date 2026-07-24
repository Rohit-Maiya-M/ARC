from pathlib import Path
from transformers import AutoTokenizer
import onnxruntime as ort

ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = ROOT / "models" / "bge-m3"
ONNX_PATH = MODEL_DIR / "onnx" / "model.onnx"

print("Model Directory:", MODEL_DIR)
print("ONNX File:", ONNX_PATH)

tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))

session = ort.InferenceSession(
    str(ONNX_PATH),
    providers=["CPUExecutionProvider"]
)

text = "Hello World rock"

inputs = tokenizer(
    text,
    padding=True,
    truncation=True,
    return_tensors="np"
)

print("\nINPUTS")
print("=" * 60)

for key, value in inputs.items():
    print(f"{key}")
    print(value)
    print("Shape:", value.shape)
    print("Dtype:", value.dtype)
    print()

outputs = session.run(
    None,
    {
        "input_ids": inputs["input_ids"],
        "attention_mask": inputs["attention_mask"]
    }
)

for i, output in enumerate(outputs):
    print(f"\nOUTPUT {i}")
    print("=" * 60)
    print(output)
    print("Shape:", output.shape)
    print("Dtype:", output.dtype)

from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import numpy as np

print("\n" + "=" * 60)
print("PyTorch vs ONNX Comparison")
print("=" * 60)

# Load the same model with SentenceTransformer
st_model = SentenceTransformer(str(MODEL_DIR))

# Generate PyTorch embedding
pytorch_embedding = st_model.encode(
    text,
    convert_to_numpy=True,
    normalize_embeddings=False
)

# ONNX embedding
onnx_embedding = outputs[1][0]

# Metrics
cosine_similarity = 1 - cosine(pytorch_embedding, onnx_embedding)
max_abs_diff = np.max(np.abs(pytorch_embedding - onnx_embedding))
mean_abs_diff = np.mean(np.abs(pytorch_embedding - onnx_embedding))

print(f"Cosine Similarity : {cosine_similarity:.10f}")
print(f"Max Abs Difference: {max_abs_diff:.10f}")
print(f"Mean Abs Difference: {mean_abs_diff:.10f}")