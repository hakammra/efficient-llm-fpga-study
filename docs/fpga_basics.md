# FPGA basics for the hardware study

An **FPGA** is a reconfigurable digital circuit. A **LUT** implements a small logic function; a **flip-flop** stores one bit across clock cycles; a **DSP block** is dedicated arithmetic hardware; **BRAM** is on-chip block memory. HDL describes circuits that can be simulated and synthesized into these resources.

A **MAC** multiplies two operands and adds the product to an accumulator. A **dot product** sums several such products. **Signed fixed-width arithmetic** interprets the highest bit as a sign bit and has a limited range. An INT8 multiplication can require 16 bits; accumulating several products requires more bits or a documented overflow policy.

**Parallelism** uses several operators at once. **Pipelining** inserts registers between stages so different inputs can occupy different stages simultaneously. Throughput is results per unit time; latency is time from one input to its result. Pipelining can improve achievable clock rate or throughput at the cost of added registers and latency, but any frequency claim requires timing evidence.

**Simulation** executes the HDL model and checks functional outputs. **Synthesis** maps HDL to a logic representation and reports inferred resources. Physical FPGA implementation, timing, and power measurements would require a target board and appropriate tools. None is available for this study. The MAC source and testbench are in `fpga/`; the local simulator could not run because Windows Device Guard blocked it.
