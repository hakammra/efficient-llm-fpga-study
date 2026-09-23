# Results

`raw/` holds direct outputs and per-run records; `processed/` will hold derived summaries. Keep units, runtime settings, and provenance next to measurements. Plots will be generated from measured files. Day 1 contains only Q4_K_M smoke-test outputs, not a comparison. `day01_q4_baseline.txt` is the final one-word check. `day01_q4_baseline_attempt1.txt` hit its output cap; `day01_q4_baseline_attempt2.txt` contains an incorrect arithmetic answer. They are preserved to make the exploratory process visible.

The Day 2 Q4_K_M `math_01` pilot has a full CLI stdout transcript and a structured JSON record. Its whole-process time includes program startup and model loading. The CLI-reported prompt and generation rates are single-run observations. Neither this pilot nor the Day 1 checks are three-model benchmark results.

The filename-tagged Day 2 pilot runs retain separate Q4_K_M records for `math_01` and `instruction_01`. The latter's exact check is false: the raw transcript shows that the model repeated `Qualification` instead of reversing it. Keep incorrect responses in the dataset; they are evidence for the accuracy comparison.

The Q8_0 `instruction_01` pilot also failed its exact check, returning `Qualiitiation`. The planned batch runner writes separate files with a `day02_bench_` prefix. Pilot observations are not included in the batch comparison.
