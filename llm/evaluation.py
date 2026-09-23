import json
from collections import Counter

from config import PROMPTS_FILE


def load_prompts():
    """Read the shared prompt list from JSON."""
    with PROMPTS_FILE.open(encoding="utf-8") as file:
        return json.load(file)


REQUIRED_FIELDS = {"id", "category", "prompt", "check", "expected"}
CATEGORIES = {
    "mathematics", "basic_reasoning", "programming",
    "instruction_following", "factual", "summarization",
}


def validate_prompts(prompts):
    """Reject missing fields, duplicate IDs, and invalid evaluation rules."""
    if not isinstance(prompts, list) or not prompts:
        raise ValueError("Prompts must be a nonempty list")

    seen_ids = set()
    for number, item in enumerate(prompts, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Prompt {number} must be an object")

        missing = REQUIRED_FIELDS - item.keys()
        if missing:
            raise ValueError(f"Prompt {number} is missing: {sorted(missing)}")

        if not isinstance(item["id"], str) or not item["id"].strip():
            raise ValueError(f"Prompt {number} has an empty ID")
        if item["id"] in seen_ids:
            raise ValueError(f"Duplicate ID: {item['id']}")
        seen_ids.add(item["id"])

        if item["category"] not in CATEGORIES:
            raise ValueError(f"Invalid category for {item['id']}")
        if not isinstance(item["prompt"], str) or not item["prompt"].strip():
            raise ValueError(f"Empty prompt for {item['id']}")

        if item["check"] == "exact":
            if not isinstance(item["expected"], str) or not item["expected"].strip():
                raise ValueError(f"Missing exact answer for {item['id']}")
        elif item["check"] == "manual":
            if item["expected"] is not None:
                raise ValueError(f"Manual answer must be null for {item['id']}")
        else:
            raise ValueError(f"Invalid check type for {item['id']}")


def check_response(item, response):
    """Strip outer whitespace, then check exact tasks; return None for manual ones."""
    if item["check"] == "manual":
        return None
    return response.strip() == item["expected"]


if __name__ == "__main__":
    prompts = load_prompts()
    validate_prompts(prompts)
    print("Validation passed")
    print("Prompt count:", len(prompts))
    print("First prompt ID:", prompts[0]["id"])

    counts = Counter(item["category"] for item in prompts)
    for category, count in sorted(counts.items()):
        print(category, count)

    math_prompt = next(p for p in prompts if p["id"] == "math_01")
    summary_prompt = next(p for p in prompts if p["id"] == "summary_01")

    print("Correct answer:", check_response(math_prompt, "42\n"))
    print("Wrong answer:", check_response(math_prompt, "41"))
    print("Manual review:", check_response(summary_prompt, "A short summary."))
