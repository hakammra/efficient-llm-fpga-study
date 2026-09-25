# Signed INT8 MAC study

`rtl/mac_int8.sv` describes a clocked multiply-accumulate unit. When `valid_in` is high at a rising clock edge, it computes `accumulator <- accumulator + a*b` and raises `valid_out` for that accepted operation. `clear` sets the sum to zero and takes priority over `valid_in`; active-low `rst_n` resets the state asynchronously. When neither `clear` nor `valid_in` is active, the sum holds.

The operands are signed 8-bit two's-complement numbers in `[-128, 127]`. Their product needs 16 signed bits. The 16-bit product is explicitly sign-extended into the 32-bit accumulator. A 32-bit accumulator can still overflow after enough operations; this design uses two's-complement wraparound, not saturation. For example, repeated `127*127` additions eventually exceed its range. This is an arithmetic demonstration, not a Qwen or Q4_K_M implementation.

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
```

The script compiles with `iverilog -g2012`, runs with `vvp`, and writes `fpga\waveforms\mac_int8.vcd`. A successful run should print `PASS: 510 MAC cases plus reset checks`. Open the VCD in GTKWave, if available, to inspect `a`, `b`, `product`, `accumulator`, `valid_in`, `valid_out`, and `clear`. The waveform and simulator build products are ignored by Git.

The testbench checks directed positive, negative, zero, and signed-boundary cases, clear and hold behavior, 500 reproducible pseudo-random pairs, and reset. It uses a separate integer reference and stops with `$fatal` on any mismatch. A passing simulation demonstrates functional agreement on those vectors; it does not establish FPGA timing, area, power, or board operation.

**Verification status:** Icarus Verilog was installed through MSYS2 on the development machine, but Windows Device Guard blocked `iverilog.exe` when invoked. The simulation has therefore **not run successfully on this machine**, and no passing result or waveform is claimed. An approved simulator installation or a machine that permits Icarus is needed to complete runtime verification. `where iverilog` confirms a path only; `iverilog -V` confirms whether the executable can actually start.
