import onnxruntime as ort
from pathlib import Path
from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
print("ROOT:", ROOT)
print(".env exists:", (ROOT / ".env").exists())
print("MODEL_PATH:", os.getenv("ONNX_MODEL_PATH"))
MODEL_PATH = os.getenv("ONNX_MODEL_PATH")

session = ort.InferenceSession(
    MODEL_PATH,
    providers=[
        "CPUExecutionProvider"
    ]
)

print("=" * 60)
print("ONNX Runtime Version:", ort.__version__)
print("=" * 60)

print("\nINPUTS")
print("-" * 60)

for inp in session.get_inputs():
    print(f"Name: {inp.name}")
    print(f"Shape: {inp.shape}")
    print(f"Type: {inp.type}")
    print()

print("\nOUTPUTS")
print("-" * 60)

for out in session.get_outputs():
    print(f"Name: {out.name}")
    print(f"Shape: {out.shape}")
    print(f"Type: {out.type}")
    print()