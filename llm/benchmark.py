import subprocess
import time
import re
import json

from config import (
    ROOT, LLAMA_CLI, MODELS, THREADS, GPU_LAYERS,
    CONTEXT_TOKENS, MAX_NEW_TOKENS, TEMPERATURE, SEED,
)
from evaluation import load_prompts, validate_prompts, check_response

prompts = load_prompts()
validate_prompts(prompts)
item = prompts[1]

model_name = "Q4_K_M"
run_number = 1
run_tag = f"day02_{model_name.lower()}_{item['id']}_run{run_number:02d}"
raw_path = ROOT / "results" / "raw" / f"{run_tag}_stdout.txt"
record_path = ROOT / "results" / "raw" / f"{run_tag}_record.json"
if raw_path.exists() or record_path.exists():
    raise FileExistsError(f"Run files already exist for {run_tag}; increase run_number")

command = [
    str(LLAMA_CLI),
    "-m", str(MODELS[model_name]),
    "-p", item["prompt"],
    "-n", str(MAX_NEW_TOKENS),
    "-t", str(THREADS),
    "-ngl", str(GPU_LAYERS),
    "-c", str(CONTEXT_TOKENS),
    "--temp", str(TEMPERATURE),
    "--seed", str(SEED),
    "--single-turn",
    "--no-display-prompt",
    "--color", "off",
]

start = time.perf_counter()
result = subprocess.run(
    command,
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
    timeout=120,
)
elapsed = time.perf_counter() - start


print("Prompt:", item["id"])
print("Exit code:", result.returncode)
print("Whole-process time (s):", round(elapsed, 3))
raw_path.write_text(result.stdout, encoding="utf-8")

text = result.stdout.replace("\r\n", "\n")
marker = f"> {item['prompt']}\n"
if marker not in text:
    raise RuntimeError(f"Prompt marker not found; inspect {raw_path}")

after_prompt = text.split(marker, 1)[1]
if "\n[ Prompt:" not in after_prompt:
    raise RuntimeError(f"Timing marker not found; inspect {raw_path}")

response = after_prompt.split("\n[ Prompt:", 1)[0].strip()

timing = re.search(
    r"\[\s*Prompt:\s*([0-9]+(?:\.[0-9]+)?)\s+t/s\s*\|\s*Generation:\s*([0-9]+(?:\.[0-9]+)?)\s+t/s\s*\]",
    text,
)

if timing is None:
    prompt_tps = None
    generation_tps = None
else:
    prompt_tps = float(timing.group(1))
    generation_tps = float(timing.group(2))

record = {
    "model": model_name,
    "model_size_bytes": MODELS[model_name].stat().st_size,
    "prompt_id": item["id"],
    "category": item["category"],
    "prompt": item["prompt"],
    "response": response,
    "check": item["check"],
    "expected": item["expected"],
    "correct": check_response(item, response),
    "exit_code": result.returncode,
    "whole_process_seconds": round(elapsed, 3),
    "prompt_tokens_per_second": prompt_tps,
    "generation_tokens_per_second": generation_tps,
    "threads": THREADS,
    "gpu_layers": GPU_LAYERS,
    "context_tokens": CONTEXT_TOKENS,
    "max_new_tokens": MAX_NEW_TOKENS,
    "temperature": TEMPERATURE,
    "seed": SEED,
    "run_number": run_number,
    "raw_stdout_file": str(raw_path.relative_to(ROOT)),
}

record_path.write_text(
    json.dumps(record, indent=2) + "\n",
    encoding="utf-8",
)
print("Structured record saved:", record_path)

print("Raw output saved:", raw_path)
print("Model response:", repr(response))
print("Exact check:", check_response(item, response))
print("STDERR:", repr(result.stderr))
print("Prompt speed (tokens/s):", prompt_tps)
print("Generation speed (tokens/s):", generation_tps)
