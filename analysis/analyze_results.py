"""Audit saved runs and create reproducible tables and figures."""

import argparse
import csv
import json
import os
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cache = ROOT / ".local" / "matplotlib-cache"
cache.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(cache))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


sys.path.insert(0, str(ROOT / "llm"))

from audit_results import audit_one  # noqa: E402
from config import MODELS  # noqa: E402
from evaluation import load_prompts, validate_prompts  # noqa: E402


def audited_records(repeats):
    prompts = load_prompts()
    validate_prompts(prompts)
    records = []
    problems = []
    for run_number in range(1, repeats + 1):
        for prompt in prompts:
            for model in MODELS:
                record, errors = audit_one(prompt, model, run_number, verify_model_file=False)
                problems.extend(errors)
                if record is not None:
                    records.append(record)
    builds = {record["llama_build"] for record in records}
    if len(builds) != 1:
        problems.append(f"Expected one llama.cpp build; found {sorted(builds)}")
    if problems:
        raise ValueError("Audit failed:\n" + "\n".join(problems))
    return prompts, records


def summarize(records):
    rows = []
    for model in MODELS:
        group = [record for record in records if record["model"] == model]
        exact = [record for record in group if record["check"] == "exact"]
        manual = [record for record in group if record["check"] == "manual"]
        sizes = {record["model_size_bytes"] for record in group}
        if len(sizes) != 1:
            raise ValueError(f"Inconsistent file sizes for {model}: {sizes}")
        size = sizes.pop()
        rows.append(
            {
                "model": model,
                "model_size_bytes": size,
                "model_size_mib": round(size / (1024**2), 2),
                "record_count": len(group),
                "exact_passes": sum(record["correct"] is True for record in exact),
                "exact_checks": len(exact),
                "manual_reviews": len(manual),
                "median_whole_process_seconds": round(
                    statistics.median(record["whole_process_seconds"] for record in group), 3
                ),
                "median_prompt_tokens_per_second": round(
                    statistics.median(record["prompt_tokens_per_second"] for record in group), 2
                ),
                "median_generation_tokens_per_second": round(
                    statistics.median(record["generation_tokens_per_second"] for record in group), 2
                ),
            }
        )
    return rows


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row[field] for field in fields} for row in rows)


def write_manual_review(path, prompts, records):
    lines = [
        "# Manual summary review",
        "",
        "These responses are unscored. For each prompt, compare factual faithfulness, coverage,",
        "and the requested one-sentence format. Record your observations before making a",
        "quality claim. Repeat runs are shown separately when present.",
        "",
    ]
    for prompt in prompts:
        if prompt["check"] != "manual":
            continue
        lines += [f"## {prompt['id']}", "", f"**Prompt:** {prompt['prompt']}", ""]
        for record in records:
            if record["prompt_id"] != prompt["id"]:
                continue
            lines += [f"### {record['model']} — run {record['run_number']}", ""]
            lines.extend("> " + part for part in record["response"].splitlines())
            lines += ["", "Review notes:", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def make_plots(rows, path, repeats):
    labels = [row["model"] for row in rows]
    colors = ["#4263a5", "#19a092", "#e88b40"]
    metrics = [
        ("model_size_mib", "Model file size", "MiB"),
        ("median_generation_tokens_per_second", "Generation rate", "tokens/s"),
        ("median_whole_process_seconds", "Whole-process time", "seconds"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.5), layout="constrained")
    for ax, (key, title, units) in zip(axes, metrics):
        values = [row[key] for row in rows]
        bars = ax.bar(labels, values, color=colors, width=0.65)
        ax.set_title(title)
        ax.set_ylabel(units)
        ax.set_ylim(0, max(values) * 1.22)
        ax.bar_label(bars, fmt="%.1f", padding=3)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.18)
        ax.set_axisbelow(True)
    fig.suptitle("Qwen2.5-0.5B-Instruct CPU benchmark", fontsize=15)
    fig.text(
        0.5,
        -0.025,
        f"{repeats} run(s) per prompt and model; medians across all records. "
        "Whole-process time includes startup and loading.",
        ha="center",
        fontsize=9,
    )
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=1, help="repeats per prompt and model")
    args = parser.parse_args()
    if args.runs < 1:
        parser.error("--runs must be at least 1")

    prompts, records = audited_records(args.runs)
    rows = summarize(records)
    output = ROOT / "results" / "processed"
    plots = ROOT / "analysis" / "plots"
    output.mkdir(parents=True, exist_ok=True)
    plots.mkdir(parents=True, exist_ok=True)
    write_csv(output / "benchmark_summary.csv", rows, list(rows[0]))
    (output / "benchmark_summary.json").write_text(
        json.dumps(
            {
                "source": "results/raw/benchmark_*_record.json and paired transcripts",
                "llama_build": records[0]["llama_build"],
                "runs_per_prompt_model": args.runs,
                "prompt_count": len(prompts),
                "record_count": len(records),
                "notes": [
                    "Strict exact checks include formatting requirements.",
                    "Manual summaries are unscored.",
                    "Whole-process time includes startup and model loading.",
                    "Peak RAM, load time, and time to first token were not measured.",
                ],
                "models": rows,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    exact_failures = [
        record for record in records if record["check"] == "exact" and record["correct"] is False
    ]
    write_csv(
        output / "strict_failures.csv",
        exact_failures,
        ["model", "prompt_id", "run_number", "expected", "response", "raw_stdout_file"],
    )
    write_manual_review(output / "manual_review.md", prompts, records)
    make_plots(rows, plots / "benchmark_tradeoffs.png", args.runs)
    print(f"Audited {len(records)} records from one llama.cpp build.")
    for row in rows:
        print(
            f"{row['model']}: {row['model_size_mib']:.1f} MiB, "
            f"exact {row['exact_passes']}/{row['exact_checks']}, "
            f"generation {row['median_generation_tokens_per_second']:.1f} t/s, "
            f"process {row['median_whole_process_seconds']:.3f} s"
        )
    print("Wrote results/processed/ and analysis/plots/benchmark_tradeoffs.png")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(str(error)) from error
