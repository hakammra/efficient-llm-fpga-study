# Setup walkthrough: download and run the model yourself

This guide is meant to be followed and explained, not memorized as a black box. Run commands from the repository root: `C:\Users\abdul\Documents\efficient-llm-fpga-study`. The model and executable already downloaded on this computer are under `.local/`, so you can begin at **Check the files**. Use the download sections when reproducing the setup from a clean copy.

## What is being downloaded?

There are two separate downloads:

1. **`llama.cpp` CPU program:** the official Windows x64 release [b10938](https://github.com/ggml-org/llama.cpp/releases/tag/b10938). `llama-cli.exe` is the program that loads model weights and generates text. We selected its CPU package because this project does not need CUDA, and WinGet was not available on this machine.
2. **Qwen model file:** `qwen2.5-0.5b-instruct-q4_k_m.gguf` from the [official Qwen repository](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/blob/main/qwen2.5-0.5b-instruct-q4_k_m.gguf). The GGUF file contains quantized model weights, tokenizer data, and metadata. It is data consumed by `llama-cli.exe`, not a program to execute.

The pinned program is build `b10938-f1e44dcc1`. The Qwen file is 491,400,032 bytes and the [published SHA256](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/blob/main/qwen2.5-0.5b-instruct-q4_k_m.gguf) is `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`. The model URL below uses `main`; checking the hash is what identifies the exact bytes downloaded.

`.local/` is listed in `.gitignore`. The GitHub repository will contain instructions and small result files, not the 491 MB model or the backend ZIP.

## Choose your terminal

**Command Prompt (CMD)** is the Windows terminal that uses backslashes in paths and double quotes around a prompt with spaces. **Git Bash** is a Bash-like terminal installed with Git for Windows; it uses forward slashes. It is not an FPGA tool or a Linux installation. **PowerShell** is a third Windows shell; the initial setup commands were run there and are in [llm/README.md](../llm/README.md). The program and model are the same in all three shells.

### Command Prompt: reproduce from a clean copy

Open Command Prompt and enter these lines separately:

```bat
cd /d C:\Users\abdul\Documents\efficient-llm-fpga-study
python --version
git --version
if not exist .local\downloads mkdir .local\downloads
if not exist .local\tools mkdir .local\tools
if not exist .local\models mkdir .local\models
curl.exe -L --fail --output .local\downloads\llama-b10938-bin-win-cpu-x64.zip "https://github.com/ggml-org/llama.cpp/releases/download/b10938/llama-b10938-bin-win-cpu-x64.zip"
if not exist .local\tools\llama-b10938 mkdir .local\tools\llama-b10938
tar.exe -xf .local\downloads\llama-b10938-bin-win-cpu-x64.zip -C .local\tools\llama-b10938
.local\tools\llama-b10938\llama-cli.exe --version
curl.exe -L --fail --output .local\models\qwen2.5-0.5b-instruct-q4_k_m.gguf "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf?download=true"
certutil.exe -hashfile .local\models\qwen2.5-0.5b-instruct-q4_k_m.gguf SHA256
```

`cd /d` changes both drive and directory. `curl.exe` downloads a URL: `-L` follows redirects, `--fail` reports HTTP errors, and `--output` chooses the local filename. `tar.exe -xf` extracts the ZIP into the directory named by `-C`. `certutil.exe -hashfile ... SHA256` calculates a fingerprint of the model file; compare it with the published value above before running inference.

### Git Bash: reproduce from a clean copy

Open Git Bash and enter these lines separately:

```bash
cd /c/Users/abdul/Documents/efficient-llm-fpga-study
python --version
git --version
mkdir -p .local/downloads .local/tools/llama-b10938 .local/models
curl.exe -L --fail --output .local/downloads/llama-b10938-bin-win-cpu-x64.zip 'https://github.com/ggml-org/llama.cpp/releases/download/b10938/llama-b10938-bin-win-cpu-x64.zip'
tar.exe -xf .local/downloads/llama-b10938-bin-win-cpu-x64.zip -C .local/tools/llama-b10938
./.local/tools/llama-b10938/llama-cli.exe --version
curl.exe -L --fail --output .local/models/qwen2.5-0.5b-instruct-q4_k_m.gguf 'https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf?download=true'
certutil.exe -hashfile .local/models/qwen2.5-0.5b-instruct-q4_k_m.gguf SHA256
```

Here `./` means “run the executable in this relative directory.” The Git Bash on this computer has no `sha256sum`; Windows `certutil.exe` works from both shells. The version and hash commands were tested in each shell. The original download was performed once from PowerShell, so the download lines above are reproducibility instructions rather than a second download.

## Check the files and run inference

If the downloads already exist, check the backend version and model hash, then run one inference command. You should see build `b10938-f1e44dcc1`, the SHA256 above, and a response. These exact inference commands were tested in CMD and Git Bash on 2026-09-23; each returned `Paris` and exit code 0.

**Command Prompt:**

```bat
.local\tools\llama-b10938\llama-cli.exe --version
certutil.exe -hashfile .local\models\qwen2.5-0.5b-instruct-q4_k_m.gguf SHA256
.local\tools\llama-b10938\llama-cli.exe -m .local\models\qwen2.5-0.5b-instruct-q4_k_m.gguf -p "What is the capital of France? Reply with one word." -n 16 -t 4 -ngl 0 -c 2048 --temp 0 --seed 42 --single-turn --no-display-prompt --color off
```

**Git Bash:**

```bash
./.local/tools/llama-b10938/llama-cli.exe --version
certutil.exe -hashfile .local/models/qwen2.5-0.5b-instruct-q4_k_m.gguf SHA256
./.local/tools/llama-b10938/llama-cli.exe -m .local/models/qwen2.5-0.5b-instruct-q4_k_m.gguf -p "What is the capital of France? Reply with one word." -n 16 -t 4 -ngl 0 -c 2048 --temp 0 --seed 42 --single-turn --no-display-prompt --color off
```

### What each inference option means

| Option | Meaning | Why it is here |
| --- | --- | --- |
| `-m FILE` | Model path | Loads the downloaded GGUF. |
| `-p TEXT` | Prompt | Sends the same text to the model. Quotes keep spaces together as one argument. |
| `-n 16` | Maximum new tokens | Prevents a long response during this setup check. |
| `-t 4` | CPU threads | Records how much CPU parallel work the program may use. |
| `-ngl 0` | GPU layers | Requests CPU-only inference. |
| `-c 2048` | Context capacity in tokens | Holds the prompt and generated text. |
| `--temp 0` | Sampling temperature | Uses a deterministic next-token choice in this run. |
| `--seed 42` | Random seed | Records a further reproducibility setting. |
| `--single-turn` | End after one reply | Avoids staying in a chat loop. |
| `--no-display-prompt` | Hide prompt display during generation | Keeps generation display simpler. |
| `--color off` | Disable terminal colors | Makes copied output easier to read. |

A **token** is a unit from the model's tokenizer, not necessarily a word. **Autoregressive inference** predicts the next token, adds it to the context, and repeats. The `-n 16` cap therefore limits new tokens, not words. `llama.cpp` prints prompt and generation token rates, but one short check is not a reliable benchmark. The [raw setup outputs](../results/README.md) include an incorrect arithmetic answer as well as the successful setup check.

## How to explain this in an interview

> I downloaded a pinned CPU-only `llama.cpp` Windows release and the Qwen2.5-0.5B-Instruct Q4_K_M GGUF from their official repositories. I verified the executable version and matched the model's SHA256 to the publisher's fingerprint. I then ran `llama-cli` with four CPU threads, zero GPU layers, fixed context and output limits, and temperature zero. The run showed that the local inference path worked. It was a smoke test, not a quality or speed benchmark; one earlier arithmetic prompt was answered incorrectly, which motivated explicit checks in the later comparison.

You should be able to answer these follow-ups in your own words:

- **Why two downloads?** The executable performs inference; the GGUF supplies model weights and tokenizer metadata.
- **Why check SHA256?** It checks that the local file has the expected bytes. It does not by itself prove a model's quality.
- **Why CPU-only?** It keeps the planned comparisons on the same accessible backend and avoids GPU setup differences.
- **What is Q4_K_M?** A specific blockwise quantized GGUF weight format; it is not the same thing as the planned plain INT8 MAC circuit.
- **Why keep an incorrect answer?** A working inference system can still answer incorrectly, so objective prompts need answer checks and raw outputs must be preserved.
