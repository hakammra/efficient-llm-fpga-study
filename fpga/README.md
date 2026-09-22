# FPGA and digital hardware study (planned for Days 4–5)

The first design will be a clocked signed INT8 multiply-accumulate unit: `result = accumulator + a × b`. A self-checking SystemVerilog testbench will cover signed boundary cases and random inputs, and produce a VCD waveform. The next design will compute a four-term signed INT8 dot product in parallel. Simulation verifies logic against a software reference; it does not demonstrate physical FPGA operation. Optional Yosys synthesis will be labeled as generic logic statistics, not Cyclone IV resource use.

No RTL, simulation, waveform, or synthesis result exists on Day 1.
