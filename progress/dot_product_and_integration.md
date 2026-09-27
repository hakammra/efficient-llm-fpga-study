# Parallel dot product and integration

## Implementation

- Added four signed INT8 multipliers in parallel, pairwise additions, and a registered 18-bit signed result.
- Verified the output width against the positive extreme of 65536 and negative extreme of -65024.
- Added a self-checking testbench with seven directed cases, 500 reproducible pseudo-random vectors, and reset checks.
- Added vendor-independent Icarus simulation and generic Yosys synthesis scripts, plus an Ubuntu GitHub Actions workflow.

## Evidence

The [verification workflow](https://github.com/hakammra/efficient-llm-fpga-study/actions/runs/36339039843) reports successful MAC and dot-product simulation, generic synthesis for both modules, and uploaded logs/waveforms. The local Windows Icarus executable was blocked by Device Guard. The GitHub run is the evidence for functional simulation. No physical FPGA resource, frequency, power, or energy result was measured.

## Integration conclusion

The CPU experiment observed smaller GGUF files and higher reported generation rates for the quantized variants in one exploratory pass. The strict exact-check differences are small and confounded by formatting, so they do not establish quality ranking. The HDL experiment demonstrates correct signed reduced-precision sum-of-products arithmetic on exercised vectors. It does not implement Qwen inference or directly map Q4_K_M. The research connection is the arithmetic pattern, with scaling, memory movement, and target-specific implementation remaining for future work.
