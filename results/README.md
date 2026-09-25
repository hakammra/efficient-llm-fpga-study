# Results

`raw/` holds direct outputs and per-run records; `processed/` holds derived summaries, exact-check failures, and responses for manual review. `analysis/analyze_results.py` generates these files and the plot from the measured batch. Keep units, runtime settings, and provenance next to measurements. The setup phase contains only Q4_K_M smoke-test outputs, not a comparison. `baseline_q4.txt` is the final one-word check. `baseline_q4_attempt1.txt` hit its output cap; `baseline_q4_attempt2.txt` contains an incorrect arithmetic answer. They are preserved to make the exploratory process visible.

The initial Q4_K_M `math_01` pilot has a full CLI stdout transcript and a structured JSON record. Its whole-process time includes program startup and model loading. The CLI-reported prompt and generation rates are single-run observations. Neither this pilot nor the setup checks are three-model benchmark results.

The filename-tagged pilot runs retain separate Q4_K_M records for `math_01` and `instruction_01`. The latter's exact check is false: the raw transcript shows that the model repeated `Qualification` instead of reversing it. Keep incorrect responses in the dataset; they are evidence for the accuracy comparison.

The Q8_0 `instruction_01` pilot also failed its exact check, returning `Qualiitiation`. The batch runner writes separate files with a `benchmark_` prefix. Pilot observations are excluded from the batch comparison.

## First complete pass

The user ran all 20 prompts once per variant on CPU with four threads, zero GPU layers, context 2048, output cap 96, temperature zero, and seed 42. `python llm\audit_results.py` checked 60/60 JSON records against their raw transcripts, model paths, fixed settings, and the prompt answer keys; it found no issues. All exits were zero and stderr was empty. The llama.cpp build was `b10938-f1e44dcc1`.

| Model | File size (bytes) | Strict exact checks | Manual summaries | Median whole-process (s) | Median prompt (tokens/s) | Median generation (tokens/s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FP16 | 1,266,425,696 | 9/17 | 3 | 4.798 | 134.9 | 16.3 |
| Q8_0 | 675,710,816 | 8/17 | 3 | 4.167 | 99.0 | 31.9 |
| Q4_K_M | 491,400,032 | 10/17 | 3 | 4.216 | 82.0 | 34.2 |

These are descriptive medians from one run per prompt/model pair. Whole-process time includes program startup and model loading, while the CLI rates describe the prompt and generation phases. Output length and task type vary across prompts. Strict exact checking includes requested formatting; for example, all variants answered `Ohm` where the prompt requested lowercase `ohm`. The nine summaries are saved for manual review and have no accuracy score yet. Repeated trials are needed before making stable speed claims.

The machine's CPU is an Intel Core i7-8650U. The loop ran FP16, then Q8_0, then Q4_K_M for each prompt; this fixed order may affect timing. The files report model sizes on disk, not measured peak RAM use.

Separate model loading time, peak process RAM, time to first token, and model-only inference latency were not reliably captured. No values are inferred for those metrics from the whole-process duration or the printed token rates.

## Processed outputs

Run `.venv\Scripts\python.exe analysis\analyze_results.py` from the repository root to regenerate `processed/benchmark_summary.csv`, `processed/benchmark_summary.json`, `processed/strict_failures.csv`, `processed/manual_review.md`, and `analysis/plots/benchmark_tradeoffs.png`. The script checks each record against its prompt and raw transcript before calculating results. It can regenerate outputs without local GGUF files. Follow [the analysis guide](../analysis/README.md) for Command Prompt setup and interpretation.
