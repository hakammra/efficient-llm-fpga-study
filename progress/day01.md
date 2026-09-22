# Day 1 — 2026-09-23

## Goals

- Create the local Git repository and documentation skeleton.
- Inspect Python, Git, `llama.cpp`, WinGet, GitHub CLI, and planned FPGA tools.
- Verify one official Qwen2.5-0.5B-Instruct Q4_K_M CPU inference run.
- Learn the basic LLM and quantization vocabulary.

## Work completed

- Initialized `main` as a local Git repository.
- Created the README and documentation skeleton with separate measured, simulated, and conceptual claims.
- Verified Python 3.14.7 and Git 2.55.0.windows.5.
- Downloaded the official `llama.cpp` Windows x64 CPU release b10938 and ran `llama-cli --version`: build `b10938-f1e44dcc1`.
- Downloaded the official Qwen Q4_K_M GGUF (491,400,032 bytes), verified its SHA256, and ran three short local CPU inference checks. The final one-word check returned `Paris` and exited with code 0.
- Wrote introductory notes for tokens, tokenization, embeddings, transformers, attention, autoregressive inference, quantization, and FPGA arithmetic.

## What I learned

- A tokenizer maps text to token IDs. A transformer processes token representations using learned weights and causal self-attention, then generates one new token at a time.
- GGUF packages model tensors and metadata for `llama.cpp`. Quantization reduces weight precision, but formats such as Q4_K_M need scales and block-specific handling.
- A successful inference call shows the software path is working; it does not establish model accuracy or a reliable performance comparison.

## Experimental results

- Host: Windows x64 build 26200; Intel Core i7-8650U; 8 logical processors; 15.92 GiB physical RAM.
- Backend: `llama.cpp` CPU build b10938 (`f1e44dcc1`). Parameters for final check: 4 CPU threads, 0 GPU layers, 2048-token context, 16-token output cap, temperature 0, seed 42.
- Model: Qwen2.5-0.5B-Instruct Q4_K_M, 491,400,032 bytes, SHA256 `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`.
- Final smoke prompt: `What is the capital of France? Reply with one word.` Raw response: `Paris`. Exit code: 0. Full CLI output: [`results/raw/day01_q4_baseline.txt`](../results/raw/day01_q4_baseline.txt).
- The exploratory arithmetic prompt `Compute 5 + 2 * 3` returned `15`; the correct answer is `11`. The earlier MAC explanation was cut off by the output cap. Both raw outputs remain under `results/raw/`.
- These three runs were not controlled repeats, so their printed token rates are not used as comparative benchmark results.

## Problems encountered

- `winget`, `gh`, `llama.cpp`, CMake, Icarus Verilog, and Yosys were not on `PATH` initially. WinGet was unavailable, so the pinned official CPU ZIP was used.
- The GitHub `releases/latest` endpoint identified a package release without Windows binaries. The numbered b10938 release supplied the needed CPU binary.
- Initial WMI queries for machine information were denied; CPU information came from the Windows registry and RAM from the .NET `ComputerInfo` API.
- The first two prompts showed that a functional model can produce incomplete or incorrect content. The final baseline prompt was simplified to check the inference path.

## Decisions made

- Keep executables, model weights, caches, and generated waveforms out of Git via `.gitignore`.
- Use the official Qwen GGUF repository for all future variants and pin/record hashes and backend version.
- Keep Day 2 benchmarking separate from the Day 1 smoke test; do not use these prompt rates as benchmark evidence.
- Keep the FPGA design vendor-independent and label simulation and generic synthesis honestly.

## Next steps

- On Day 2, define the shared prompt set and build a measurement harness for FP16, Q8_0, and Q4_K_M.
- Create a GitHub repository named `efficient-llm-fpga-study` through the GitHub website (without adding a README, license, or `.gitignore` there), then run:

```powershell
git remote add origin https://github.com/<YOUR-USERNAME>/efficient-llm-fpga-study.git
git push -u origin main
```

`gh` is unavailable and no remote is configured, so Day 1 was committed locally but not pushed.
