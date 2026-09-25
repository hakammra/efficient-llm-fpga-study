# Benchmark analysis

The script reads the saved `benchmark_*` JSON records and their paired stdout transcripts, checks them against the common prompts and fixed settings, and generates tables and a plot. It does not run the models again, and a repository clone does not need the GGUF files to reproduce these summaries. The original `python llm\audit_results.py` additionally compares recorded file sizes with the local GGUF files when they are present.

## Reproduce in Command Prompt

Start in the repository root:

```cmd
cd /d C:\Users\abdul\Documents\efficient-llm-fpga-study
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe analysis\analyze_results.py
```

The first two setup commands are needed only once. Later, rerun the final command after changing benchmark records. For additional complete, audited repeats, use `--runs 2` (or the actual number of repeats).

Outputs:

- `results/processed/benchmark_summary.csv` and `.json`: size, exact-check totals, and medians by model.
- `results/processed/strict_failures.csv`: expected and actual responses for each exact-check failure.
- `results/processed/manual_review.md`: unscored summary responses with space for your review.
- `analysis/plots/benchmark_tradeoffs.png`: three comparisons from the measured records.

`MiB = bytes / 1,048,576`. Each timing bar is the median of the saved per-prompt measurements for that model, and the process duration includes startup and model loading. The token rates are reported by llama.cpp. One repeat per prompt/model pair and a fixed model order limit any speed ranking. An exact check also tests requested output format; the summaries have no numerical quality score. RAM use, separate load time, and time to first token were not measured, so the script produces no plots for them.
