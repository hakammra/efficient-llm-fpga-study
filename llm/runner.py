"""Run one saved CPU inference trial for the Day 2 benchmark."""

import json
import re
import subprocess
import time

from config import (
    CONTEXT_TOKENS,
    GPU_LAYERS,
    LLAMA_CLI,
    MAX_NEW_TOKENS,
    MODELS,
    ROOT,
    SEED,
    TEMPERATURE,
    THREADS,
)
from evaluation import check_response


def run_one(item, model_name, run_number):
    """Run one prompt/model/repeat, retaining its transcript and JSON record."""
    if model_name not in MODELS:
        raise ValueError(f"Unknown model: {model_name}")
    if run_number < 1:
        raise ValueError("run_number must be at least 1")

    run_tag = f"day02_bench_{model_name.lower()}_{item['id']}_run{run_number:02d}"
    raw_path = ROOT / "results" / "raw" / f"{run_tag}_stdout.txt"
    record_path = ROOT / "results" / "raw" / f"{run_tag}_record.json"

    if raw_path.exists() and record_path.exists():
        print(f"Skipping saved run: {run_tag}", flush=True)
        return None
    if raw_path.exists() or record_path.exists():
        raise FileExistsError(f"Incomplete run files for {run_tag}; inspect them before retrying")

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

    print(f"Running {run_tag}...", flush=True)
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
    raw_path.write_text(result.stdout, encoding="utf-8")

    output = result.stdout.replace("\r\n", "\n")
    marker = f"> {item['prompt']}\n"
    if marker not in output:
        raise RuntimeError(f"Prompt marker not found; inspect {raw_path}")
    after_prompt = output.split(marker, 1)[1]
    if "\n[ Prompt:" not in after_prompt:
        raise RuntimeError(f"Timing marker not found; inspect {raw_path}")
    response = after_prompt.split("\n[ Prompt:", 1)[0].strip()

    timing = re.search(
        r"\[\s*Prompt:\s*([0-9]+(?:\.[0-9]+)?)\s+t/s\s*\|\s*Generation:\s*([0-9]+(?:\.[0-9]+)?)\s+t/s\s*\]",
        output,
    )
    prompt_tps = float(timing.group(1)) if timing else None
    generation_tps = float(timing.group(2)) if timing else None
    build = re.search(r"^build\s*:\s*(\S+)", output, re.MULTILINE)
    correct = check_response(item, response) if result.returncode == 0 else False

    record = {
        "model": model_name,
        "model_size_bytes": MODELS[model_name].stat().st_size,
        "prompt_id": item["id"],
        "category": item["category"],
        "prompt": item["prompt"],
        "response": response,
        "check": item["check"],
        "expected": item["expected"],
        "correct": correct,
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
        "llama_build": build.group(1) if build else None,
        "raw_stdout_file": str(raw_path.relative_to(ROOT)),
        "stderr": result.stderr,
    }
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    print(
        f"{run_tag}: exit={result.returncode}, correct={correct}, "
        f"time={elapsed:.3f}s, response={response!r}",
        flush=True,
    )
    return record
