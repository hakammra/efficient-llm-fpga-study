# LLM study

Day 1 verifies that one official Qwen Q4_K_M GGUF can generate a response on CPU. The repeatable three-variant benchmark belongs to Day 2.

For a command-by-command explanation and tested CMD/Git Bash equivalents, read [the Day 1 setup walkthrough](../docs/day01_setup_walkthrough.md).

## Windows baseline setup

Run these commands in PowerShell from the repository root. `winget install llama.cpp` is the simple official option where WinGet exists. On the Day 1 machine it was absent, so the following pinned official CPU release was used instead.

```powershell
New-Item -ItemType Directory -Path .local/downloads,.local/tools,.local/models -Force | Out-Null
curl.exe -L --fail --output .local/downloads/llama-b10938-bin-win-cpu-x64.zip https://github.com/ggml-org/llama.cpp/releases/download/b10938/llama-b10938-bin-win-cpu-x64.zip
Expand-Archive .local/downloads/llama-b10938-bin-win-cpu-x64.zip .local/tools/llama-b10938 -Force
& .local/tools/llama-b10938/llama-cli.exe --version
curl.exe -L --fail --output .local/models/qwen2.5-0.5b-instruct-q4_k_m.gguf 'https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf?download=true'
Get-FileHash .local/models/qwen2.5-0.5b-instruct-q4_k_m.gguf -Algorithm SHA256
```

The [official Qwen file page](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/blob/main/qwen2.5-0.5b-instruct-q4_k_m.gguf) lists SHA256 `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`. Confirm that the downloaded file matches before inference. A mismatch means the file must be downloaded again or the upstream file changed. The baseline download is excluded from Git.

## One CPU inference check

```powershell
& .local/tools/llama-b10938/llama-cli.exe -m .local/models/qwen2.5-0.5b-instruct-q4_k_m.gguf -p 'What is the capital of France? Reply with one word.' -n 16 -t 4 -ngl 0 -c 2048 --temp 0 --seed 42 --single-turn --no-display-prompt --color off
```

`-ngl 0` requests no GPU layers; `-t 4` fixes the CPU thread count for this check. `-n 16` caps generated tokens. `-c 2048` sets the context window. Temperature zero selects the highest-scoring next token at each step, reducing sampling randomness. The seed is recorded as a further runtime setting. A successful response confirms the local inference path works; it does not establish benchmark performance or model quality.

The Day 1 run returned `Paris` and exited successfully. Two earlier raw runs are also retained: the first answer hit its 64-token cap, and the second returned `15` for `5 + 2 * 3` (correct value `11`). This small model's mistake is a useful reason to use objective checks in the later comparison. `llama.cpp` displayed prompt and generation rates during these runs, but they are not treated as comparable benchmark findings.

On Day 2, the harness uses identical prompt text and generation settings for FP16, Q8_0, and Q4_K_M, retains full responses, and captures the CLI's prompt and generation rates. Each record includes the backend build, model file size, and runtime settings; model hashes are documented in `progress/day02.md`. Machine details and run-order limitations are documented alongside the results.

## Day 2 preparation checks

From the repository root in Command Prompt:

```bat
python llm\config.py
python llm\evaluation.py
```

`config.py` checks the local executable, prompt file, and three model paths. `evaluation.py` loads the shared JSON, validates its fields and unique IDs, and demonstrates exact-answer checking. The exact check strips outer whitespace only; manual-summary tasks return `None` and require the full response to be saved. These commands validate preparation, not model performance.

`runner.py` contains `run_one(item, model_name, run_number)`, which launches one inference, saves the raw transcript and structured record, and uses a `day02_bench_` filename prefix so batch runs stay separate from pilot runs. Fully saved runs are skipped on restart; a partial saved run stops for inspection. `benchmark.py` validates the 20 prompts and loops over all three models once per prompt.

From the repository root in Command Prompt, run `python llm\benchmark.py` to run or resume the batch. Then run `python llm\audit_results.py` to verify all 60 first-pass records against their transcripts and print descriptive medians. The audit accepts `--runs N` when additional numbered trials have been completed. Existing first-pass files are never overwritten by a rerun.
