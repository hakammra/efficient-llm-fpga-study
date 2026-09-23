# Project progress

| Milestone | Status | Evidence |
| --- | --- | --- |
| Environment setup and Q4_K_M baseline | Complete | [Setup log](progress/environment_setup.md), [raw output](results/raw/baseline_q4.txt) |
| Common prompt set and three-format CPU benchmark | Complete: 60 runs audited, raw responses preserved | [Benchmark log](progress/llm_benchmark.md), [results](results/README.md), [audit script](llm/audit_results.py) |
| Comparative analysis and plots | Planned | [Analysis plan](analysis/README.md) |
| Signed INT8 MAC simulation | Planned | [Hardware plan](fpga/README.md) |
| Parallel dot product and optional synthesis | Planned | [Hardware plan](fpga/README.md) |
| Integration and interview preparation | Planned | [Interview notes](docs/interview_notes.md) |

The GitHub remote is configured and the completed setup and benchmark milestones have been pushed. Model files remain excluded from Git. Pilot runs are preserved separately from the audited 60-run batch; analysis and plots are the next research step.
