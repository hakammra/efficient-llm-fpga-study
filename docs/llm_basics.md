# LLM basics for this study

- **Token:** A unit of text recognized by the model's tokenizer. A token can be a word, word part, punctuation mark, or other text fragment. Token counts are not word counts.
- **Tokenizer:** Converts text into token IDs and converts generated token IDs back to text. The same tokenizer must be used when comparing variants of one model.
- **Embedding:** A learned vector associated with a token ID. It gives later layers a numerical representation to process.
- **Transformer:** A stack of layers that combines attention with other learned transformations. The model's parameters are the learned numerical weights in those layers.
- **Self-attention:** A mechanism that lets each token use information from other tokens in the current context. For causal text generation, it can use earlier tokens but not future generated tokens.
- **Autoregressive inference:** The model predicts one next token, appends it to the context, and repeats. Prompt processing reads the existing context; generation then produces tokens sequentially.
- **Parameter:** One learned value in the model, usually a weight. `0.5B` means roughly half a billion parameters, not a file size.

In many transformer components, vectors are multiplied by weight matrices. Each output element is a sum of products. That arithmetic motivates the later MAC and dot-product study, though the HDL here is far too small to execute the model.
