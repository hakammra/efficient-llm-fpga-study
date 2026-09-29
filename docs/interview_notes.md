# How to explain the quantization study

## A short explanation

"I compared FP16, Q8_0, and Q4_K_M versions of the same Qwen2.5-0.5B-Instruct model on one CPU. I used the same 20 prompts and fixed `llama.cpp` settings, saved all 60 responses and timings, and audited the records. Q4_K_M had the smallest file and the highest reported generation rate in this one pass. The prompt set and single run per prompt are too limited to rank answer quality or make a general speed claim."

## If asked for numbers

| Format | File size | Median generation rate | Median whole-process time | Strict exact matches |
| --- | ---: | ---: | ---: | ---: |
| FP16 | 1207.8 MiB | 16.3 tokens/s | 4.798 s | 9/17 |
| Q8_0 | 644.4 MiB | 31.9 tokens/s | 4.167 s | 8/17 |
| Q4_K_M | 468.6 MiB | 34.2 tokens/s | 4.216 s | 10/17 |

The remaining three prompts per format were summaries left for manual review. Strict matching includes formatting, so these counts are not general model-accuracy scores.

## Likely follow-up questions

**Why use the same model and prompts?** To reduce differences caused by model architecture or task selection. The formats can still use different storage layouts and backend kernels, so this is a comparison of whole software configurations.

**What is quantization?** It stores approximate weights with lower precision and scale information. A smaller model can reduce disk storage and sometimes memory traffic, but may alter outputs. Speed depends on the CPU backend and workload.

**Does Q4_K_M mean every parameter occupies four bits?** No. It is a blockwise GGUF quantization format with scales, metadata, and potentially different formats across tensors. Compare the actual file sizes.

**Why can the fastest generation rate differ from the shortest whole-process time?** Whole-process time includes program startup, model loading, prompt processing, and answer generation. Reported generation tokens per second describes only one phase.

**What are the main limitations?** One computer, one run per prompt/model pair, fixed run order, a small prompt set, and strict formatting-sensitive checks. Peak RAM, separate load time, time to first token, and energy were not measured.

## Useful next experiment

Repeat the CPU runs in a counterbalanced model order and measure peak process RAM, loading time, time to first token, and output-token count. Add more prompts and a carefully defined manual review protocol before making stronger quality claims.
