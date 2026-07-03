import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
AI_SERVICE_DIR = ROOT_DIR / "ai-service"
BACKEND_DIR = ROOT_DIR / "backend-java"

sys.path.insert(0, str(AI_SERVICE_DIR))
from app.config import settings  # noqa: E402


def _require_path(value: str | None, label: str) -> Path:
    if not value:
        raise RuntimeError(f"{label} is not configured. Add it to ai-service/.env.")
    path = Path(value)
    if not path.exists():
        raise RuntimeError(f"{label} does not exist: {path}")
    return path


def _start_process(name: str, command: list[str], cwd: Path) -> subprocess.Popen:
    print(f"[ARC] Starting {name}...")
    return subprocess.Popen(
        command,
        cwd=str(cwd),
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,  # critical for clean Ctrl+C
    )


def main():
    llama_server_path = _require_path(settings.LLAMA_SERVER_PATH, "LLAMA_SERVER_PATH")
    llm_model_path = _require_path(settings.LLM_MODEL_PATH, "LLM_MODEL_PATH")

    llama_workdir = (
        Path(settings.LLAMA_SERVER_WORKDIR)
        if settings.LLAMA_SERVER_WORKDIR
        else llama_server_path.parent
    )
    if not llama_workdir.exists():
        raise RuntimeError(f"LLAMA_SERVER_WORKDIR does not exist: {llama_workdir}")

    python_path = AI_SERVICE_DIR / ".venv310" / "Scripts" / "python.exe"
    if not python_path.exists():
        python_path = Path(sys.executable)

    processes: list[subprocess.Popen] = []

    try:
        processes.append(
            _start_process(
                "DeepSeek llama-server",
                [
                    str(llama_server_path),
                    "-m",
                    str(llm_model_path),
                    "--port",
                    str(settings.LLM_SERVER_PORT),
                    "--n-gpu-layers",
                    str(settings.LLAMA_N_GPU_LAYERS),
                    "--ctx-size",
                    str(settings.LLAMA_CTX_SIZE),
                    "--threads",
                    str(settings.LLAMA_THREADS),
                ],
                llama_workdir,
            )
        )

        processes.append(
            _start_process(
                "FastAPI AI service",
                [
                    str(python_path),
                    "-m",
                    "uvicorn",
                    "app.main:app",
                    "--host",
                    settings.FASTAPI_HOST,
                    "--port",
                    str(settings.FASTAPI_PORT),
                ],
                AI_SERVICE_DIR,
            )
        )

        processes.append(
            _start_process(
                "Spring Boot backend",
                [str(BACKEND_DIR / "mvnw.cmd"), "spring-boot:run"],
                BACKEND_DIR,
            )
        )

        print("[ARC] All services started. Press Ctrl+C to stop them.")

        while all(process.poll() is None for process in processes):
            time.sleep(1)

        for process in processes:
            if process.poll() is not None:
                print(f"[ARC] A service exited with code {process.returncode}.")
                break

    except KeyboardInterrupt:
        print("\n[ARC] Stopping services...")

    finally:
        # First try graceful shutdown
        for process in processes:
            if process.poll() is None:
                try:
                    process.send_signal(signal.CTRL_BREAK_EVENT)
                except Exception:
                    process.terminate()

        time.sleep(2)

        # Force kill if still alive
        for process in processes:
            if process.poll() is None:
                process.kill()


if __name__ == "__main__":
    main()
