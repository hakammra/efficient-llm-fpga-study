"""Run every Day 2 prompt once for each of the three model variants."""

from config import MODELS
from evaluation import load_prompts, validate_prompts
from runner import run_one


def main():
    prompts = load_prompts()
    validate_prompts(prompts)
    print(f"Validated {len(prompts)} prompts and {len(MODELS)} model variants.")

    for item in prompts:
        for model_name in MODELS:
            run_one(item, model_name, 1)


if __name__ == "__main__":
    main()
