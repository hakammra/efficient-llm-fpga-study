# Study workflow

The same Qwen2.5-0.5B-Instruct model is represented in three GGUF formats: FP16, Q8_0, and Q4_K_M. `llama.cpp` runs each format on the same CPU with the same 20 prompts and fixed settings. The runner saves raw transcripts and structured records; the audit checks provenance and answers; the analysis script produces tables and a plot. This is a CPU inference comparison.
