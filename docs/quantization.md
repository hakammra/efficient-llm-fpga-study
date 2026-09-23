# Quantization basics

**FP16** stores a floating-point value in 16 bits. It is a useful high-precision GGUF baseline for this study, though it is not the original full-precision training representation.

**INT8** and **INT4** are signed integer representations with 8 and 4 bits per value respectively. A quantized value normally needs a scale (and sometimes other metadata) to approximate its original real value. Quantization introduces rounding error, so outputs may change. Different formats use different block layouts and overhead.

**Q8_0** and **Q4_K_M** are specific `llama.cpp` GGUF weight formats. Q4_K_M mixes quantization choices across tensors and stores scale information; it is not simply an array of signed INT4 values. GGUF is a model container carrying tensors and metadata such as tokenizer information. The simple INT8 HDL circuit planned here is a teaching example of low-precision arithmetic, not a circuit that consumes Q4_K_M tensors directly.

Fewer stored bits can reduce file size and memory traffic. Whether inference is faster depends on the CPU backend, dequantization, caching, and other implementation details. The Day 2 benchmark recorded file sizes and one pass of CPU timings; Day 3 will analyze the measured trade-offs. Memory traffic and energy were not measured.
