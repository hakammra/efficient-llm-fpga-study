from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LLAMA_CLI = ROOT / ".local" / "tools" / "llama-b10938" / "llama-cli.exe"
PROMPTS_FILE = ROOT / "benchmarks" / "prompts.json"

MODELS = {
    "FP16": ROOT / ".local" / "models" / "qwen2.5-0.5b-instruct-fp16.gguf",
    "Q8_0": ROOT / ".local" / "models" / "qwen2.5-0.5b-instruct-q8_0.gguf",
    "Q4_K_M": ROOT / ".local" / "models" / "qwen2.5-0.5b-instruct-q4_k_m.gguf",
}

THREADS = 4
GPU_LAYERS = 0
CONTEXT_TOKENS = 2048
MAX_NEW_TOKENS = 96
TEMPERATURE = 0
SEED = 42

if __name__ == "__main__":
    print("llama-cli:", LLAMA_CLI.exists())
    print("prompts:", PROMPTS_FILE.exists())
    for name, path in MODELS.items():
        print(name, "exists:", path.exists())