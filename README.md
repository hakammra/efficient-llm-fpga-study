# Qwen2.5 Quantization Benchmark

A small, reproducible CPU inference study comparing three GGUF formats of the same Qwen2.5-0.5B-Instruct model: FP16, Q8_0, and Q4_K_M.

**Status:** One complete, audited benchmark pass: 20 common prompts per format, 60 saved runs in total. This is an exploratory comparison on one computer, not a general ranking of model quality or speed.

## Question and method

How do the three formats compare in **model file size**, **observed CPU timing**, and **responses** to a small common prompt set?

All runs used the same `llama.cpp` CPU build, four threads, zero GPU layers, a 2048-token context, a 96-token output cap, temperature zero, and seed 42. Raw terminal transcripts and structured records are saved under [`results/raw/`](results/raw/). The [audit script](llm/audit_results.py) checked all 60 records against their transcripts and prompt keys. The [analysis script](analysis/analyze_results.py) produces the [summary table](results/processed/benchmark_summary.csv) and [comparison plot](analysis/plots/benchmark_tradeoffs.png).

The [prompt set](benchmarks/prompts.json) covers mathematics, factual questions, basic reasoning, instruction following, programming, and summarization. Seventeen prompts per format have strict exact-answer checks; three summaries per format remain for manual review. See the [benchmark guide](benchmarks/README.md) and [results guide](results/README.md).

## Results

| Format | GGUF file size (MiB) | Median reported generation (tokens/s) | Median whole process (s) | Strict exact checks |
| --- | ---: | ---: | ---: | ---: |
| FP16 | 1207.8 | 16.3 | 4.798 | 9/17 |
| Q8_0 | 644.4 | 31.9 | 4.167 | 8/17 |
| Q4_K_M | 468.6 | 34.2 | 4.216 | 10/17 |

**Main observation:** Q4_K_M used about 61% less disk space than FP16 and had about 2.1 times its median reported generation rate in this pass. Q8_0 had the shortest median whole-process duration, but its 0.049-second difference from Q4_K_M is too small to treat as a reliable win. The exact-check counts do **not** establish an answer-quality ranking: the set is small, formatting differences count as failures, and summaries are unscored.

The file sizes are **disk sizes**, not measured peak RAM. Whole-process time includes startup, model loading, prompt processing, and generation; it is different from generation tokens per second. Each prompt/model pair was run once in a fixed order on one CPU, so repeated, counterbalanced trials are needed for stronger speed claims. Peak RAM, separate loading time, time to first token, and energy were not measured.

## Reproduce and learn

- [Setup walkthrough for Command Prompt and Git Bash](docs/setup_walkthrough.md)
- [LLM runner and audit instructions](llm/README.md)
- [Analysis and plot instructions](analysis/README.md)
- [Quantization basics](docs/quantization.md) and [LLM basics](docs/llm_basics.md)
- [Progress and provenance](PROGRESS.md) and [meeting explanation](docs/interview_notes.md)

The model files and `llama.cpp` executable belong under Git-ignored `.local/`; they are not part of the repository. The baseline used the official [Qwen GGUF files](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF) and [`llama.cpp` release b10938](https://github.com/ggml-org/llama.cpp/releases/tag/b10938). See [LICENSE](LICENSE) for this repository's code and documentation; the model and backend retain their own licenses.
