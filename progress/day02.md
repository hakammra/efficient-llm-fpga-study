# Day 2 — in progress

## Goals

- Obtain the official Qwen2.5-0.5B-Instruct FP16 and Q8_0 GGUF files alongside Day 1's Q4_K_M file.
- Build a shared set of about 20 prompts with objective answer keys where appropriate.
- Implement and run a repeatable CPU benchmark across all three variants, keeping raw responses and runtime settings.

## Work completed

- The user downloaded FP16 and Q8_0 in Command Prompt and verified their published hashes. I independently checked both local files and hashes.
- Created and reviewed a 20-prompt JSON dataset: 4 mathematics, 4 basic reasoning, 3 programming, 3 instruction following, 3 factual, and 3 summarization prompts.
- Tightened three reasoning questions to make their rules explicit and avoid reliance on outside facts. Marked summaries for manual review instead of assigning invented accuracy scores.
- Validated JSON syntax, required fields, check types, unique IDs, category counts, and the reverse-string answer key.
- Added `llm/config.py` for shared model paths and runtime settings, and `llm/evaluation.py` to load prompts, validate entries, and check exact answers while leaving summaries for manual review.
- Built a first `llm/benchmark.py` pilot that launches `llama-cli` for one Q4_K_M prompt, saves the full stdout transcript, extracts the model response, parses the CLI-reported token rates, and writes a structured JSON record.
- Added model, prompt ID, and run number to the output filenames. Ran `math_01` and `instruction_01` with Q4_K_M using the same settings, preserving each raw transcript and JSON record.
- Ran the same `instruction_01` pilot with Q8_0, then extracted the one-run logic into `llm/runner.py`. The `llm/benchmark.py` entry point now validates inputs and awaits the full prompt/model loop.

## What I learned

- A prompt file can be valid JSON while still containing missing fields or unclear questions; structural and content checks are both needed.
- Exact-answer tasks need clear output constraints. Summaries can have multiple good wordings and need response preservation for manual review.

## Experimental results

- FP16 GGUF: 1,266,425,696 bytes; SHA256 `8e0ae26000627ed62de0e78e41860af70094558b9d2913385c842a6aa06cf3fc`.
- Q8_0 GGUF: 675,710,816 bytes; SHA256 `ca59ca7f13d0e15a8cfa77bd17e65d24f6844b554a7b6c12e07a5f89ff76844e`.
- Q4_K_M GGUF was verified on Day 1. These are file properties, not inference performance results.
- No three-variant inference benchmark has been run yet.
- The single Q4_K_M `math_01` pilot record reports response `42`, exact check `true`, exit code 0, whole-process time 4.759 s, prompt rate 76.3 tokens/s, and generation rate 24.3 tokens/s. These are one-run observations from `results/raw/day02_q4_math_01_record.json`, not comparative statistics. Earlier manual runs of the same pilot reported whole-process times 2.476 s and 5.283 s, illustrating run-to-run variation.
- The latest saved filename-tagged Q4_K_M `math_01` run returned `42` (exact check `true`) in 2.937 s. The `instruction_01` run returned `Qualification` unchanged (exact check `false`; expected `noitacifilauQ`) in 3.835 s. The raw transcript confirms the model response, so the failure is retained as measured behavior rather than changing the answer key. These remain individual pilot runs, not a three-variant comparison.
- The Q8_0 `instruction_01` pilot returned `Qualiitiation` (exact check `false`) in 4.820 s. Its raw transcript confirms the response. Two failed pilots on one prompt do not establish a model-quality or speed ranking.

## Problems encountered

- Some user-drafted reasoning questions depended on imprecise thresholds or outside knowledge. They were reworded as self-contained puzzles.
- The pilot still requires manually selecting one model and one prompt. Its run-tagged filenames distinguish those cases, and the script now refuses to overwrite an existing run; a repeated run needs a new run number.
- The full benchmark loop and repeated trials have not run yet. `runner.py` separates its output files from the pilots with a `day02_bench_` prefix, skips fully saved runs on restart, and stops on incomplete saved runs for inspection.

## Decisions made

- Use the same `benchmarks/prompts.json` for every model variant.
- Keep exact answers as strings and subjective summaries as `expected: null` with `check: "manual"`.
- Keep GGUF files in ignored `.local/models/`; commit the prompt set and documentation only.

## Next steps

- Have the user add the prompt/model loop to `llm/benchmark.py` and run the full prompt set using fixed CPU settings.
- Review raw outputs and structured records, then add repeated trials and a measured summary.
