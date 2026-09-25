# Comparative analysis

## What was done

- Read the 60 saved benchmark records and paired transcripts; reused the existing prompt and settings audit without requiring local GGUF files for this analysis.
- Calculated per-model file size, strict exact-check totals, and medians of whole-process time, prompt rate, and generation rate.
- Generated CSV/JSON summaries, a strict-failure table, an unscored summary-review worksheet, and a three-panel comparison figure.
- Confirmed that RAM, separate loading time, and time to first token were not measured and omitted those plots.

## What the measurements mean

The FP16 model file is 1207.8 MiB, Q8_0 is 644.4 MiB, and Q4_K_M is 468.6 MiB. Their median generation rates across 20 prompts are 16.3, 31.9, and 34.2 tokens/s respectively. Their median whole-process durations are 4.798, 4.167, and 4.216 seconds. Whole-process duration includes startup and model loading; it is not the time to generate only the answer. One run per prompt/model pair and the fixed run order limit speed conclusions. The exact checks include formatting, and manual summaries are unscored.

## Reproduction

From Command Prompt in the repository root, run `.venv\Scripts\python.exe analysis\analyze_results.py`. The script reports the audited record count and regenerates files in `results/processed/` and `analysis/plots/`.
