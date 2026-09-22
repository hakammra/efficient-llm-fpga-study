# Architecture map

The project has two paths. The **measured CPU path** runs the same Qwen2.5-0.5B-Instruct model in three GGUF precision variants. The **simulated hardware path** studies signed INT8 MACs and dot products in vendor-independent HDL. They meet at the arithmetic idea `y = Σ(wᵢ × xᵢ)`, which appears in neural-network layers. The hardware path does not decode GGUF or run a transformer.
