"""Check saved benchmark runs against prompts, settings, and raw transcripts."""

import argparse
import json
import re
import statistics
from pathlib import Path, PureWindowsPath

from config import (
    CONTEXT_TOKENS,
    GPU_LAYERS,
    MAX_NEW_TOKENS,
    MODELS,
    ROOT,
    SEED,
    TEMPERATURE,
    THREADS,
)
from evaluation import load_prompts, validate_prompts


TIMING_PATTERN = re.compile(
    r"\[\s*Prompt:\s*([0-9]+(?:\.[0-9]+)?)\s+t/s\s*\|\s*"
    r"Generation:\s*([0-9]+(?:\.[0-9]+)?)\s+t/s\s*\]"
)


def audit_one(item, model_name, run_number, verify_model_file=True):
    tag = f"benchmark_{model_name.lower()}_{item['id']}_run{run_number:02d}"
    record_path = ROOT / "results" / "raw" / f"{tag}_record.json"
    raw_path = ROOT / "results" / "raw" / f"{tag}_stdout.txt"
    errors = []
    if not record_path.is_file() or not raw_path.is_file():
        return None, [f"{tag}: missing record or transcript"]

    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"{tag}: unreadable JSON: {exc}"]
    raw = raw_path.read_text(encoding="utf-8").replace("\r\n", "\n")

    expected_fields = {
        "model": model_name,
        "prompt_id": item["id"],
        "category": item["category"],
        "prompt": item["prompt"],
        "check": item["check"],
        "expected": item["expected"],
        "threads": THREADS,
        "gpu_layers": GPU_LAYERS,
        "context_tokens": CONTEXT_TOKENS,
        "max_new_tokens": MAX_NEW_TOKENS,
        "temperature": TEMPERATURE,
        "seed": SEED,
        "run_number": run_number,
        "exit_code": 0,
    }
    if verify_model_file:
        expected_fields["model_size_bytes"] = MODELS[model_name].stat().st_size
    elif not isinstance(record.get("model_size_bytes"), int) or record["model_size_bytes"] <= 0:
        errors.append(f"{tag}: invalid recorded model size")
    for key, expected in expected_fields.items():
        if record.get(key) != expected:
            errors.append(f"{tag}: {key} mismatch")
    recorded_raw = record.get("raw_stdout_file")
    if not isinstance(recorded_raw, str) or PureWindowsPath(recorded_raw).as_posix() != raw_path.relative_to(ROOT).as_posix():
        errors.append(f"{tag}: raw_stdout_file mismatch")

    marker = f"> {item['prompt']}\n"
    if marker not in raw or "\n[ Prompt:" not in raw.split(marker, 1)[-1]:
        errors.append(f"{tag}: response markers missing from transcript")
    else:
        response = raw.split(marker, 1)[1].split("\n[ Prompt:", 1)[0].strip()
        if record.get("response") != response:
            errors.append(f"{tag}: response differs from transcript")
        correct = response == item["expected"] if item["check"] == "exact" else None
        if record.get("correct") != correct:
            errors.append(f"{tag}: correctness check mismatch")

    timing = TIMING_PATTERN.search(raw)
    if timing is None:
        errors.append(f"{tag}: token rates missing from transcript")
    else:
        if record.get("prompt_tokens_per_second") != float(timing.group(1)):
            errors.append(f"{tag}: prompt rate mismatch")
        if record.get("generation_tokens_per_second") != float(timing.group(2)):
            errors.append(f"{tag}: generation rate mismatch")

    build = re.search(r"^build\s*:\s*(\S+)", raw, re.MULTILINE)
    if build is None or record.get("llama_build") != build.group(1):
        errors.append(f"{tag}: llama build mismatch")
    model_line = re.search(r"^model\s*:\s*(.+)$", raw, re.MULTILINE)
    if model_line is None:
        errors.append(f"{tag}: loaded model path mismatch")
    elif verify_model_file and Path(model_line.group(1).strip()) != MODELS[model_name]:
        errors.append(f"{tag}: loaded model path mismatch")
    elif not verify_model_file and PureWindowsPath(model_line.group(1).strip()).name != MODELS[model_name].name:
        errors.append(f"{tag}: loaded model filename mismatch")
    if record.get("stderr"):
        errors.append(f"{tag}: nonempty stderr")
    if not isinstance(record.get("whole_process_seconds"), (int, float)) or record["whole_process_seconds"] <= 0:
        errors.append(f"{tag}: invalid whole-process time")
    return record, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=1, help="repeats expected per prompt and model (default: 1)")
    args = parser.parse_args()
    if args.runs < 1:
        parser.error("--runs must be at least 1")

    prompts = load_prompts()
    validate_prompts(prompts)
    records = []
    errors = []
    for run_number in range(1, args.runs + 1):
        for item in prompts:
            for model_name in MODELS:
                record, problems = audit_one(item, model_name, run_number)
                errors.extend(problems)
                if record is not None:
                    records.append(record)

    expected_count = len(prompts) * len(MODELS) * args.runs
    print(f"Checked {len(records)}/{expected_count} records; issues: {len(errors)}")
    for problem in errors:
        print("ISSUE:", problem)
    if errors:
        return 1

    builds = {r["llama_build"] for r in records}
    if len(builds) != 1:
        print("ISSUE: multiple llama.cpp builds in one batch:", sorted(builds))
        return 1
    print("llama.cpp build:", next(iter(builds)))

    for model_name in MODELS:
        group = [r for r in records if r["model"] == model_name]
        exact = [r for r in group if r["check"] == "exact"]
        manual = [r for r in group if r["check"] == "manual"]
        passed = sum(r["correct"] is True for r in exact)
        process_median = statistics.median(r["whole_process_seconds"] for r in group)
        prompt_median = statistics.median(r["prompt_tokens_per_second"] for r in group)
        generation_median = statistics.median(r["generation_tokens_per_second"] for r in group)
        print(
            f"{model_name}: exact {passed}/{len(exact)}, manual {len(manual)}, "
            f"median process {process_median:.3f} s, "
            f"prompt {prompt_median:.1f} t/s, generation {generation_median:.1f} t/s"
        )
    print("Exact checks include requested formatting; manual summaries remain unscored.")
    print("Whole-process time includes startup and model loading.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
