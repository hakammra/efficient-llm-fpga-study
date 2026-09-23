"""Day 2 benchmark entry point. Add the model/prompt loop in main()."""

from config import MODELS
from evaluation import load_prompts, validate_prompts
from runner import run_one


def main():
    prompts = load_prompts()
    validate_prompts(prompts)
    print(f"Validated {len(prompts)} prompts and {len(MODELS)} model variants.")

    # Next hands-on step: loop over prompts and MODELS, calling run_one().


if __name__ == "__main__":
    main()
