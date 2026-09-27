# Hardware verification evidence

The [HDL verification workflow, run 36339039843](https://github.com/hakammra/efficient-llm-fpga-study/actions/runs/36339039843) completed successfully for commit `de3bc2d`. GitHub reports success for the following job steps:

- Install Icarus Verilog and Yosys on Ubuntu 24.04.
- Compile and execute the self-checking signed INT8 MAC testbench: 10 directed and 500 reproducible pseudo-random cases, plus reset checks.
- Compile and execute the self-checking four-term signed INT8 dot-product testbench: 7 directed and 500 reproducible pseudo-random cases, plus reset checks.
- Run generic Yosys synthesis for both RTL modules.
- Upload simulation logs, synthesis logs, and VCD waveforms as the `hdl-evidence` artifact.

Both testbenches call `$fatal` on any mismatch, so a successful simulation step means they ran to completion without a detected mismatch. The GitHub Actions page and its artifact are the primary evidence. GitHub's unauthenticated API exposed the job and step status but denied log and artifact downloads here; this repository does not copy or invent detailed cell counts.

Simulation verifies behavior on the exercised vectors. Generic synthesis checks that the modules can be mapped to generic logic. Neither establishes target-specific FPGA utilization, frequency, power, or energy. Windows Device Guard blocked the installed local Icarus executable, so these results were obtained on GitHub's Linux runner.
