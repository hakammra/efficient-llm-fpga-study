# Signed INT8 arithmetic study

`rtl/mac_int8.sv` describes a clocked multiply-accumulate unit. When `valid_in` is high at a rising clock edge, it computes `accumulator <- accumulator + a*b` and raises `valid_out` for that accepted operation. `clear` sets the sum to zero and takes priority over `valid_in`; active-low `rst_n` resets the state asynchronously. When neither `clear` nor `valid_in` is active, the sum holds.

The operands are signed 8-bit two's-complement numbers in `[-128, 127]`. Their product needs 16 signed bits. The 16-bit product is explicitly sign-extended into the 32-bit accumulator. A 32-bit accumulator can still overflow after enough operations; this design uses two's-complement wraparound, not saturation. For example, repeated `127*127` additions eventually exceed its range.

`rtl/dot_product_int8.sv` computes `a0*w0 + a1*w1 + a2*w2 + a3*w3`. Four multipliers operate in parallel; two pairwise sums feed a final sum, which is captured on a rising clock edge when `valid_in` is high. The output holds otherwise. Its maximum is `4*(-128)*(-128) = 65536`; its minimum is `4*(-128)*127 = -65024`. An 18-bit signed output covers both limits; 17 bits would not cover the maximum. Parallel arithmetic offers one accepted four-term vector per clock edge if timing is met, but no clock-frequency or physical throughput measurement exists.

These circuits demonstrate arithmetic, not Qwen or Q4_K_M execution. They do not load GGUF weights, perform scaling or requantization, or implement a transformer.

## Software and Command Prompt steps

Use Icarus Verilog to compile and run the SystemVerilog testbench. The [MSYS2 UCRT64 package](https://packages.msys2.org/packages/mingw-w64-ucrt-x86_64-iverilog) provides `iverilog.exe` and `vvp.exe`. If MSYS2 is installed, open its **UCRT64** terminal and run:

```bash
pacman -S --needed mingw-w64-ucrt-x86_64-iverilog
```

Then open Command Prompt and run:

```cmd
cd /d C:\Users\abdul\Documents\efficient-llm-fpga-study
set "PATH=C:\msys64\ucrt64\bin;%PATH%"
where iverilog
iverilog -V
fpga\scripts\run_mac.cmd
fpga\scripts\run_dot_product.cmd
```

The scripts compile with `iverilog -g2012`, run with `vvp`, and write VCD waveforms under `fpga\waveforms\`. The MAC testbench checks 510 cases plus reset. The dot-product testbench checks 507 cases plus reset. Open the VCD files in GTKWave, if available, to inspect operands, products, sums, `valid_in`, and `valid_out`. Waveforms and simulator build products are ignored by Git.

Each testbench checks directed positive, negative, zero, and signed-boundary cases, 500 reproducible pseudo-random vectors, and reset. The MAC also tests clear and hold; the dot product tests hold. Separate integer references calculate expected answers and `$fatal` stops on a mismatch. Passing simulation demonstrates functional agreement on those vectors; it does not establish FPGA timing, area, power, or board operation.

## Verification and synthesis evidence

Windows Device Guard blocked the local MSYS2 `iverilog.exe`. The same checked-in sources were instead compiled and simulated by the [successful Ubuntu GitHub Actions run](https://github.com/hakammra/efficient-llm-fpga-study/actions/runs/36339039843). Its simulation, generic Yosys synthesis, and artifact-upload steps all completed successfully. The run artifact contains test logs, synthesis logs, and VCD waveforms. The shell commands are in `scripts/run_simulations.sh` and `scripts/run_synthesis.sh`; the workflow is `.github/workflows/hdl.yml`. See [hardware evidence](../results/hardware/README.md).

Yosys synthesized generic RTL on a GitHub-hosted Linux machine. This is not a Cyclone IV target mapping: no DE0-Nano resources, achievable FPGA clock frequency, power, or energy were measured. No physical FPGA board was used.
