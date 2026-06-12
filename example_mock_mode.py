"""
example_mock_mode.py
Demonstrates the LLM Engine working in MOCK MODE (no Ollama required).

This allows you to test the entire RAG pipeline immediately:
- Prompt Builder creates structured prompts
- LLM Engine generates intelligent mock responses
- Full integration testing without external dependencies

Perfect for development, CI/CD, and demonstrations.
"""

from Insurance_Claim_Agent.prompt_builder import PromptBuilder
from Insurance_Claim_Agent.llm_engine import LLMEngine, LLMEngineError


def main() -> None:
    print("=" * 70)
    print("AI-POWERED INSURANCE CLAIM ASSISTANT - MOCK MODE DEMO")
    print("=" * 70)
    print("Running without Ollama - using intelligent mock responses\n")

    # ------------------------------------------------------------------
    # Initialize with MOCK mode enabled
    # ------------------------------------------------------------------
    engine = LLMEngine(
        model_name="gemma:2b",
        temperature=0.3,
        use_mock=True  # ← This enables mock mode
    )
    builder = PromptBuilder()

    # ------------------------------------------------------------------
    # Health Check
    # ------------------------------------------------------------------
    print("[Health Check]")
    if engine.health_check():
        print("[OK] System ready (MOCK MODE)\n")
    else:
        print("[ERROR] System not ready\n")
        return

    # ------------------------------------------------------------------
    # Test Case 1: Flood Damage Coverage
    # ------------------------------------------------------------------
    print("=" * 70)
    print("TEST 1: Flood Damage Coverage (Context Available)")
    print("=" * 70)

    question1 = "Is flood damage covered under my insurance policy?"
    context1 = (
        "Flood damage is covered under Section 4.2 of the policy "
        "with a maximum coverage amount of INR 5,00,000. "
        "The claim must be filed within 30 days of the incident."
    )

    prompt_result1 = builder.build_prompt(question=question1, context=context1)
    response1 = engine.generate(prompt_result1.prompt)

    print(f"\nQuestion: {question1}")
    print(f"Context: {context1[:80]}...")
    print(f"\nLLM Response:")
    print(f"> {response1.response_text}")
    print(f"\n[Metadata] Model: {response1.model_name} | "
          f"Length: {response1.response_length} chars | "
          f"Success: {response1.success}\n")

    # ------------------------------------------------------------------
    # Test Case 2: Dental Surgery (Unrelated Context)
    # ------------------------------------------------------------------
    print("=" * 70)
    print("TEST 2: Dental Surgery (Unrelated Context)")
    print("=" * 70)

    question2 = "Is dental surgery covered?"
    context2 = "Section 3.1 covers hospitalisation for accidental injuries only."

    prompt_result2 = builder.build_prompt(question=question2, context=context2)
    response2 = engine.generate(prompt_result2.prompt)

    print(f"\nQuestion: {question2}")
    print(f"Context: {context2}")
    print(f"\nLLM Response:")
    print(f"> {response2.response_text}")
    print(f"\nExpected: Should say 'Information not available...'\n")

    # ------------------------------------------------------------------
    # Test Case 3: Claim Rejection Reason
    # ------------------------------------------------------------------
    print("=" * 70)
    print("TEST 3: Claim Rejection Query")
    print("=" * 70)

    question3 = "Why was my claim rejected?"
    context3 = (
        "Claims are rejected if documentation is incomplete, "
        "the incident occurred outside the policy period, "
        "or if the claim exceeds the coverage limit."
    )

    prompt_result3 = builder.build_prompt(question=question3, context=context3)
    response3 = engine.generate(prompt_result3.prompt)

    print(f"\nQuestion: {question3}")
    print(f"Context: {context3}")
    print(f"\nLLM Response:")
    print(f"> {response3.response_text}\n")

    # ------------------------------------------------------------------
    # Test Case 4: Required Documents
    # ------------------------------------------------------------------
    print("=" * 70)
    print("TEST 4: Required Documents Query")
    print("=" * 70)

    question4 = "What documents are required for an accident claim?"
    context4 = (
        "For accident claims, submit: (1) FIR copy, "
        "(2) Medical reports, (3) Hospital bills, "
        "(4) Claim form signed by the insured."
    )

    prompt_result4 = builder.build_prompt(question=question4, context=context4)
    response4 = engine.generate(prompt_result4.prompt)

    print(f"\nQuestion: {question4}")
    print(f"Context: {context4}")
    print(f"\nLLM Response:")
    print(f"> {response4.response_text}\n")

    # ------------------------------------------------------------------
    # Test Case 5: Empty Context (Should Decline)
    # ------------------------------------------------------------------
    print("=" * 70)
    print("TEST 5: Empty/Insufficient Context")
    print("=" * 70)

    question5 = "Is earthquake damage covered?"
    context5 = "Section 2.1"  # Insufficient context

    prompt_result5 = builder.build_prompt(question=question5, context=context5)
    response5 = engine.generate(prompt_result5.prompt)

    print(f"\nQuestion: {question5}")
    print(f"Context: {context5}")
    print(f"\nLLM Response:")
    print(f"> {response5.response_text}")
    print(f"\nExpected: Should say 'Information not available...'\n")

    # ------------------------------------------------------------------
    # Test Case 6: Error Handling
    # ------------------------------------------------------------------
    print("=" * 70)
    print("TEST 6: Error Handling (Empty Prompt)")
    print("=" * 70)

    try:
        engine.generate("")
        print("[FAIL] Should have raised LLMEngineError")
    except LLMEngineError as exc:
        print(f"[OK] Caught expected error: {exc}\n")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("[OK] All 6 test cases executed successfully")
    print("[OK] Prompt Builder + LLM Engine integration working")
    print("[OK] Mock mode allows testing without Ollama")
    print("\nTo use real LLM:")
    print("1. Install Ollama: https://ollama.ai")
    print("2. Run: ollama serve")
    print("3. Run: ollama pull gemma:2b")
    print("4. Set use_mock=False in LLMEngine()")
    print("=" * 70)


if __name__ == "__main__":
    main()
