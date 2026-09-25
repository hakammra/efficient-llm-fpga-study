# Project progress

| Milestone | Status | Evidence |
| --- | --- | --- |
| Environment setup and Q4_K_M baseline | Complete | [Setup log](progress/environment_setup.md), [raw output](results/raw/baseline_q4.txt) |
| Common prompt set and three-format CPU benchmark | Complete: 60 runs audited, raw responses preserved | [Benchmark log](progress/llm_benchmark.md), [results](results/README.md), [audit script](llm/audit_results.py) |
| Comparative analysis and plots | Complete: 60 records processed, figure generated | [Analysis guide](analysis/README.md), [summary](results/processed/benchmark_summary.csv), [figure](analysis/plots/benchmark_tradeoffs.png) |
| Signed INT8 MAC simulation | RTL and testbench written; runtime verification pending because Device Guard blocks the simulator | [Hardware guide](fpga/README.md), [RTL](fpga/rtl/mac_int8.sv), [testbench](fpga/tb/mac_int8_tb.sv) |
| Parallel dot product and optional synthesis | Planned | [Hardware plan](fpga/README.md) |
| Integration and interview preparation | Planned | [Interview notes](docs/interview_notes.md) |

Model files remain excluded from Git. Pilot runs are preserved separately from the audited 60-run batch. The next hardware verification step is to run `fpga\scripts\run_mac.cmd` using an approved simulator installation, then inspect the VCD waveform.
