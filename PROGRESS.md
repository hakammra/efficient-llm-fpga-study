# Project progress

| Milestone | Status | Evidence |
| --- | --- | --- |
| Environment setup and Q4_K_M baseline | Complete | [Setup log](progress/environment_setup.md), [raw output](results/raw/baseline_q4.txt) |
| Common prompt set and three-format CPU benchmark | Complete: 60 runs audited, raw responses preserved | [Benchmark log](progress/llm_benchmark.md), [results](results/README.md), [audit script](llm/audit_results.py) |
| Comparative analysis and plots | Complete: 60 records processed, figure generated | [Analysis guide](analysis/README.md), [summary](results/processed/benchmark_summary.csv), [figure](analysis/plots/benchmark_tradeoffs.png) |
| Study explanation | Complete: conclusion and limitations documented | [Interview notes](docs/interview_notes.md), [overview](README.md) |

Model files remain excluded from Git. Pilot runs are preserved separately from the audited 60-run batch. The next research steps are repeated CPU trials, direct memory measurements, and broader response evaluation.
