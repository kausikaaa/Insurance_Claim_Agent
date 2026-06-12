"""
example_usage.py
Demonstrates the three key usage scenarios for PromptBuilder.
"""

from Insurance_Claim_Agent.prompt_builder import PromptBuilder, PromptBuilderError


def main() -> None:
    builder = PromptBuilder()

    # ------------------------------------------------------------------
    # Scenario 1: Context contains the answer
    # ------------------------------------------------------------------
    result = builder.build_prompt(
        question="Is flood damage covered under my insurance policy?",
        context=(
            "Flood damage is covered under Section 4.2 of the policy "
            "with a maximum coverage amount of INR 5,00,000. "
            "The claim must be filed within 30 days of the incident."
        ),
    )
    print("=" * 60)
    print("SCENARIO 1 — Context available")
    print("=" * 60)
    print(result.prompt)
    print(f"\n[Meta] context_length={result.context_length}\n")

    # ------------------------------------------------------------------
    # Scenario 2: Context is unrelated — model should say "not available"
    # ------------------------------------------------------------------
    result2 = builder.build_prompt(
        question="Is dental surgery covered?",
        context="Section 3.1 covers hospitalisation for accidental injuries only.",
    )
    print("=" * 60)
    print("SCENARIO 2 — Unrelated context (model must decline)")
    print("=" * 60)
    print(result2.prompt)

    # ------------------------------------------------------------------
    # Scenario 3: Invalid input — exception handling
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("SCENARIO 3 — Empty question (expects PromptBuilderError)")
    print("=" * 60)
    try:
        builder.build_prompt(question="", context="Some policy text.")
    except PromptBuilderError as exc:
        print(f"Caught expected error: {exc}")


if __name__ == "__main__":
    main()
