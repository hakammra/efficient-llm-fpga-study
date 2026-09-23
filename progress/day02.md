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

## What I learned

- A prompt file can be valid JSON while still containing missing fields or unclear questions; structural and content checks are both needed.
- Exact-answer tasks need clear output constraints. Summaries can have multiple good wordings and need response preservation for manual review.

## Experimental results

- FP16 GGUF: 1,266,425,696 bytes; SHA256 `8e0ae26000627ed62de0e78e41860af70094558b9d2913385c842a6aa06cf3fc`.
- Q8_0 GGUF: 675,710,816 bytes; SHA256 `ca59ca7f13d0e15a8cfa77bd17e65d24f6844b554a7b6c12e07a5f89ff76844e`.
- Q4_K_M GGUF was verified on Day 1. These are file properties, not inference performance results.
- No three-variant inference benchmark has been run yet.

## Problems encountered

- Some user-drafted reasoning questions depended on imprecise thresholds or outside knowledge. They were reworded as self-contained puzzles.

## Decisions made

- Use the same `benchmarks/prompts.json` for every model variant.
- Keep exact answers as strings and subjective summaries as `expected: null` with `check: "manual"`.
- Keep GGUF files in ignored `.local/models/`; commit the prompt set and documentation only.

## Next steps

- Teach and implement the benchmark harness in small pieces with the user.
- Smoke-test each variant, then run the full prompt set using fixed CPU settings and preserve raw responses.
- Commit and push the benchmark implementation and measured outputs only after they have been checked.
