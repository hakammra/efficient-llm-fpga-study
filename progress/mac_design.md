# Signed INT8 MAC design and verification

## What was done

- Added a clocked signed INT8 MAC with a 16-bit signed product and 32-bit signed accumulator.
- Defined reset, clear, input-valid, and output-valid behavior in the RTL and hardware guide.
- Added a self-checking testbench with ten directed cases, 500 reproducible pseudo-random cases, reset checks, `$fatal` on mismatch, and VCD output.
- Added a Command Prompt runner using `iverilog -g2012` and `vvp`.

## Verification state

The source and testbench were reviewed, but the HDL simulator did not start on this machine. Icarus Verilog was installed through the existing MSYS2 installation; Windows Device Guard blocked `iverilog.exe`, including an attempted run outside the restricted workspace process. Therefore there is no passing HDL test or waveform yet. Run the documented command with an approved simulator before citing functional verification in an interview.

## Concepts to explain

INT8 signed operands range from -128 to 127. A multiplication can produce a value as large as 16384, so the product uses 16 signed bits. Sign extension preserves negative products when adding to the 32-bit accumulator. The accumulator can still overflow under enough additions and wraps in two's-complement arithmetic. The testbench calculates a separate expected sum and checks the DUT after each clock edge. No physical FPGA operation is claimed.
