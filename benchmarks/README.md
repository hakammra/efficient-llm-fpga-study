# Prompt benchmark

`prompts.json` contains 20 fixed prompts across basic reasoning (4), mathematics (4), programming (3), instruction following (3), factual questions (3), and summarization (3). Each model variant will receive the same prompts in the same form.

Each entry has a unique `id`, `category`, `prompt`, `check`, and `expected`. `check: "exact"` means the task has a short objective answer stored as a string in `expected`. `check: "manual"` means there can be several reasonable responses, so `expected` is `null` and the full model response must be retained for human comparison. The Day 2 harness will define and record any text normalization before scoring exact answers.

This is an exploratory quality and efficiency comparison, not a rigorous model-intelligence evaluation. The prompt set has been checked for JSON syntax, required fields, unique IDs, and answer-key consistency. No three-model inference benchmark has been run yet.
