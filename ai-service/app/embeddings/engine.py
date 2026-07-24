import os
import multiprocessing
import onnxruntime as ort
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parents[3]
load_dotenv(ROOT / ".env")

model_path = os.getenv("ONNX_MODEL_PATH")

if model_path and not Path(model_path).exists():
    local_model = ROOT / "models" / "bge-base-en-v1.5" / "onnx" / "model.onnx"
    if local_model.exists():
        model_path = str(local_model)

cpu_count = multiprocessing.cpu_count()

session_options = ort.SessionOptions()

session_options.graph_optimization_level = (
    ort.GraphOptimizationLevel.ORT_ENABLE_ALL
)

session_options.intra_op_num_threads = cpu_count
session_options.inter_op_num_threads = 1

session_options.enable_mem_pattern = True
session_options.enable_cpu_mem_arena = True
session_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL

session_options.log_severity_level = 3

session = ort.InferenceSession(
    model_path,
    sess_options=session_options,
    providers=["CPUExecutionProvider"]
)

print("\n" + "=" * 90)
print("ONNX RUNTIME CONFIGURATION")
print("=" * 90)
print(f"Model Path              : {model_path}")
print(f"Execution Provider      : {session.get_providers()}")
print(f"CPU Threads             : {cpu_count}")
print(f"Intra-op Threads        : {session_options.intra_op_num_threads}")
print(f"Inter-op Threads        : {session_options.inter_op_num_threads}")
print(f"Execution Mode          : SEQUENTIAL")
print(f"Graph Optimization      : ORT_ENABLE_ALL")
print("=" * 90 + "\n")


def getSession():
    return session