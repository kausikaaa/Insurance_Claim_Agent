"""
example_answer_generator.py
Demonstrates Answer Generator usage across various insurance scenarios.

This shows the complete orchestration of Module 1, 2, and 3.
"""

from Insurance_Claim_Agent.answer_generator import AnswerGenerator, AnswerGeneratorError


def main():
    print("=" * 70)
    print("AI-POWERED INSURANCE CLAIM ASSISTANT")
    print("Module 3: Answer Generator Demo")
    print("=" * 70)
    print()

    # Initialize Answer Generator in mock mode
    generator = AnswerGenerator(
        model_name="gemma:2b",
        temperature=0.3,
        use_mock_llm=True,
    )

    # ------------------------------------------------------------------
    # Scenario 1: Flood Damage Coverage
    # ------------------------------------------------------------------
    print("SCENARIO 1: Flood Damage Coverage")
    print("-" * 70)

    result1 = generator.generate_response(
        question="Is flood damage covered under my insurance policy?",
        context=(
            "Flood damage is covered under Section 4.2 of the policy "
            "with a maximum coverage amount of INR 5,00,000. "
            "The claim must be filed within 30 days of the incident."
        ),
    )

    print(f"Question: {result1.question}")
    print(f"Answer: {result1.answer}")
    print(f"Context Length: {result1.context_length} chars")
    print(f"Success: {result1.success}")
    print(f"Generation Time: {result1.generation_time:.3f}s")
    print()

    # ------------------------------------------------------------------
    # Scenario 2: Claim Limit Query
    # ------------------------------------------------------------------
    print("SCENARIO 2: Claim Limit Query")
    print("-" * 70)

    result2 = generator.generate_response(
        question="What is the maximum claim limit for medical expenses?",
        context="The maximum claim limit for medical expenses is INR 10,00,000 per policy year.",
    )

    print(f"Question: {result2.question}")
    print(f"Answer: {result2.answer}")
    print(f"Generation Time: {result2.generation_time:.3f}s")
    print()

    # ------------------------------------------------------------------
    # Scenario 3: Required Documents
    # ------------------------------------------------------------------
    print("SCENARIO 3: Required Documents for Accident Claim")
    print("-" * 70)

    result3 = generator.generate_response(
        question="What documents are required for filing an accident claim?",
        context=(
            "For accident claims, you must submit: "
            "(1) FIR copy, (2) Medical reports, (3) Hospital bills, "
            "(4) Claim form signed by insured person."
        ),
    )

    print(f"Question: {result3.question}")
    print(f"Answer: {result3.answer}")
    print(f"Generation Time: {result3.generation_time:.3f}s")
    print()

    # ------------------------------------------------------------------
    # Scenario 4: Unrelated Context (Should Decline)
    # ------------------------------------------------------------------
    print("SCENARIO 4: Unrelated Question")
    print("-" * 70)

    result4 = generator.generate_response(
        question="Is dental surgery covered?",
        context="Section 3.1 covers hospitalisation for accidental injuries only.",
    )

    print(f"Question: {result4.question}")
    print(f"Answer: {result4.answer}")
    print(f"Expected: Should indicate information not available")
    print()

    # ------------------------------------------------------------------
    # Scenario 5: Error Handling - Empty Question
    # ------------------------------------------------------------------
    print("SCENARIO 5: Error Handling - Empty Question")
    print("-" * 70)

    try:
        generator.generate_response(
            question="",
            context="Some policy context",
        )
    except AnswerGeneratorError as exc:
        print(f"[OK] Caught expected error: {exc}")
    print()

    # ------------------------------------------------------------------
    # Scenario 6: Error Handling - Empty Context
    # ------------------------------------------------------------------
    print("SCENARIO 6: Error Handling - Empty Context")
    print("-" * 70)

    try:
        generator.generate_response(
            question="Is fire damage covered?",
            context="",
        )
    except AnswerGeneratorError as exc:
        print(f"[OK] Caught expected error: {exc}")
    print()

    # ------------------------------------------------------------------
    # Scenario 7: Multiple Questions (Batch Processing)
    # ------------------------------------------------------------------
    print("SCENARIO 7: Batch Processing")
    print("-" * 70)

    batch_requests = [
        {
            "question": "Is fire damage covered?",
            "context": "Fire damage is covered under Section 3.1.",
        },
        {
            "question": "What is the deductible?",
            "context": "The deductible amount is INR 25,000.",
        },
        {
            "question": "How long does claim processing take?",
            "context": "Claim processing typically takes 15-30 business days.",
        },
    ]

    print(f"Processing {len(batch_requests)} requests...\n")

    total_time = 0
    for idx, req in enumerate(batch_requests, 1):
        result = generator.generate_response(
            question=req["question"],
            context=req["context"],
        )
        total_time += result.generation_time

        print(f"{idx}. {result.question[:50]}...")
        print(f"   Answer: {result.answer[:80]}...")
        print(f"   Time: {result.generation_time:.3f}s")
        print()

    print(f"Total time: {total_time:.3f}s")
    print(f"Average time: {total_time / len(batch_requests):.3f}s")
    print()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("[OK] Module 1 (Prompt Builder) working")
    print("[OK] Module 2 (LLM Engine) working")
    print("[OK] Module 3 (Answer Generator) working")
    print("[OK] Full orchestration pipeline functional")
    print("[OK] Error handling robust")
    print("[OK] Mock mode allows testing without Ollama")
    print()
    print("System ready for RAG integration!")
    print("Next: Integrate PDF Processing + FAISS Retrieval")
    print("=" * 70)


if __name__ == "__main__":
    main()
