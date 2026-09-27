# Project progress

| Milestone | Status | Evidence |
| --- | --- | --- |
| Environment setup and Q4_K_M baseline | Complete | [Setup log](progress/environment_setup.md), [raw output](results/raw/baseline_q4.txt) |
| Common prompt set and three-format CPU benchmark | Complete: 60 runs audited, raw responses preserved | [Benchmark log](progress/llm_benchmark.md), [results](results/README.md), [audit script](llm/audit_results.py) |
| Comparative analysis and plots | Complete: 60 records processed, figure generated | [Analysis guide](analysis/README.md), [summary](results/processed/benchmark_summary.csv), [figure](analysis/plots/benchmark_tradeoffs.png) |
| Signed INT8 MAC simulation | Complete: self-checking simulation passed on Ubuntu | [Hardware guide](fpga/README.md), [RTL](fpga/rtl/mac_int8.sv), [evidence](results/hardware/README.md) |
| Parallel dot product and generic synthesis | Complete: self-checking simulation and generic synthesis passed on Ubuntu | [Dot-product RTL](fpga/rtl/dot_product_int8.sv), [testbench](fpga/tb/dot_product_int8_tb.sv), [evidence](results/hardware/README.md) |
| Integration and meeting preparation | Complete: project conclusion and technical explanations documented | [Interview notes](docs/interview_notes.md), [overview](README.md) |

Model files remain excluded from Git. Pilot runs are preserved separately from the audited 60-run batch. The local Icarus executable was blocked by Windows Device Guard, so the checked-in HDL was verified through GitHub Actions on Ubuntu. The next research steps are repeated CPU trials and a target-aware hardware study.
