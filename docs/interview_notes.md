# Interview notes

## A 30-second explanation

"I built a small reproducible study linking LLM quantization to digital arithmetic. I ran the same 20 prompts on FP16, Q8_0, and Q4_K_M versions of Qwen2.5-0.5B-Instruct with llama.cpp on one CPU, preserved every response, and generated plots from audited records. Then I implemented a signed INT8 MAC and a four-term parallel dot product in SystemVerilog, verified both with self-checking simulations, and ran generic synthesis. The HDL is an arithmetic demonstration; it does not run Qwen on an FPGA."

## A two-minute explanation

"My question was how precision affects storage, observed CPU speed, and answers for one small model, and how lower-precision arithmetic connects to hardware. I used three official GGUF variants of the same Qwen model and the same 20-prompt set. All 60 CPU runs used four threads, no GPU layers, a 2048-token context, a 96-token output cap, temperature zero, and seed 42. I saved the full model outputs and structured timings, then audited all 60 records against the transcripts and prompt keys."

"The FP16 file is 1207.8 MiB, Q8_0 is 644.4 MiB, and Q4_K_M is 468.6 MiB. Median reported generation rates were 16.3, 31.9, and 34.2 tokens per second respectively. Median whole-process durations were 4.798, 4.167, and 4.216 seconds. Q4_K_M is much smaller and showed a higher generation rate in this pass, but the total duration does not rank the same way. The prompt set and one run per pair are too small for a broad quality or stable speed claim. Strict exact checks were 9, 8, and 10 passes out of 17; these include formatting, and the three summaries per format remain unscored."

"On the hardware side, I designed a clocked signed INT8 MAC with a 16-bit product and 32-bit accumulator, then a four-multiplier dot product with an 18-bit signed sum. Both passed directed and pseudo-random self-checking simulations on an Ubuntu runner; Yosys also completed generic synthesis. I have not measured a physical FPGA. Q4_K_M's blockwise GGUF format is not directly implemented by the INT8 RTL. The common idea is sums of products in neural-network layers."

## If asked about your familiarity

- **FPGAs:** "I have introductory exposure from a DE0-Nano UART university project. I understand clocked RTL, simulation, testbenches, and basic FPGA resources. For this study I built and verified MAC and dot-product RTL; I have not yet done board-level implementation or timing closure for it."
- **LLMs:** "I understand inference at a practical introductory level: tokenization, transformer layers, attention, weights, and generation. I used Qwen GGUF variants through llama.cpp and built a controlled benchmark. I have not trained or designed an LLM."

## Technical questions to be ready for

**Why use the same model family and prompts?** To reduce confounding from architecture and task differences. The formats still differ in storage representation and potentially backend kernels, so the result is a system-level comparison.

**Does Q4_K_M mean every parameter occupies four bits?** No. It is a blockwise GGUF quantization format with scales, metadata, and some tensors possibly stored differently. Compare actual file sizes rather than multiplying parameter count by four bits.

**What is the difference between generation rate and whole-process time?** The former is llama.cpp's reported output-token rate; the latter measures process startup, model loading, prompt processing, and answer generation together. A higher generation rate need not yield the shortest total duration.

**What does 10/17 mean?** Ten responses matched the expected strings exactly. It is not an overall accuracy score: formatting mistakes count as failures, the set is small, and subjective summaries were left for manual review.

**Why a 16-bit product and 18-bit dot-product result?** Signed INT8 ranges from -128 to 127. One product reaches 16384, fitting signed 16 bits. Four such positive products reach 65536, one above signed 17-bit maximum 65535, so the four-term sum needs 18 signed bits.

**What does the MAC accumulator do?** On an accepted rising edge it adds a sign-extended product to a 32-bit signed register. Clear wins over valid input; reset is active-low. The 32-bit sum wraps on overflow rather than saturating.

**What was verified?** The testbenches compared RTL outputs with independent integer references over directed boundaries, zero, sign combinations, reset/hold behavior, and 500 reproducible pseudo-random vectors per module. GitHub Actions reported both simulations and generic Yosys synthesis successful. These are functional and generic-logic checks, not physical FPGA measurements.

**How does this relate to LLM inference?** Matrix-vector and matrix-matrix operations contain many multiply-accumulate sums. Reduced precision can lower storage and change arithmetic costs. A real accelerator also needs format-specific dequantization or requantization, data movement, memory hierarchy, control, and target-specific timing and power analysis; none of those are implemented here.

## Questions to ask a researcher

1. Which current problem in efficient LLM inference or EDA would be useful for an undergraduate to reproduce or prototype?
2. Would a focused next step be more valuable on the measurement side (repeatable latency, memory, and quality evaluation) or hardware side (a target-specific quantized dot-product kernel)?
3. What target platform, model format, and evaluation metric would make a small collaboration result meaningful?
4. Which background topic should I study first to contribute effectively: quantization mathematics, FPGA memory/dataflow, timing closure, or LLM inference software?

## A realistic next experiment

Repeat CPU runs with counterbalanced model order and measure peak process RAM, loading time, time to first token, and output-token count. In parallel, choose a specific quantized matrix-vector kernel, define scale and accumulator semantics, and synthesize it for a named FPGA target. Compare correctness and target reports before making performance claims. Ask the researcher which of these directions best matches their group's work.
