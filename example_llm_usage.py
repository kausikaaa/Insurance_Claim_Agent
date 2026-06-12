"""
example_llm_usage.py
Demonstrates LLM Engine usage in isolation and integrated with Prompt Builder.
"""

from Insurance_Claim_Agent.prompt_builder import PromptBuilder
from Insurance_Claim_Agent.llm_engine import LLMEngine, LLMEngineError


def main() -> None:
    print("=" * 70)
    print("DEMO: LLM Engine Module")
    print("=" * 70)

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    engine = LLMEngine(
        model_name="gemma:2b",  # Change to "llama2" or "gemma:7b" as needed
        temperature=0.3,
        timeout=60,
    )

    # ------------------------------------------------------------------
    # Step 1: Health Check
    # ------------------------------------------------------------------
    print("\n[1] Running health check...")
    if not engine.health_check():
        print("❌ Health check failed. Ensure Ollama is running:")
        print("   - Start Ollama: ollama serve")
        print("   - Pull model: ollama pull gemma:2b")
        return

    print("✅ Health check passed. Model is ready.\n")

    # ------------------------------------------------------------------
    # Step 2: Standalone LLM call (without Prompt Builder)
    # ------------------------------------------------------------------
    print("=" * 70)
    print("[2] Standalone LLM generation (simple prompt)")
    print("=" * 70)

    simple_prompt = "What is insurance? Answer in one sentence."

    try:
        response = engine.generate(simple_prompt)
        print(f"Model: {response.model_name}")
        print(f"Response Length: {response.response_length} chars")
        print(f"Success: {response.success}")
        print(f"\nResponse:\n{response.response_text}\n")
    except LLMEngineError as exc:
        print(f"❌ Error: {exc}")
        return

    # ------------------------------------------------------------------
    # Step 3: Full integration with Prompt Builder
    # ------------------------------------------------------------------
    print("=" * 70)
    print("[3] Full RAG Flow: Prompt Builder + LLM Engine")
    print("=" * 70)

    builder = PromptBuilder()

    # Simulate retrieved context from FAISS
    question = "Is flood damage covered under my insurance policy?"
    context = (
        "Flood damage is covered under Section 4.2 of the policy "
        "with a maximum coverage amount of INR 5,00,000. "
        "The claim must be filed within 30 days of the incident."
    )

    # Build the structured prompt
    prompt_result = builder.build_prompt(question=question, context=context)

    print(f"\nUser Question: {question}")
    print(f"Context Length: {prompt_result.context_length} chars")
    print("\nFormatted Prompt (first 200 chars):")
    print(prompt_result.prompt[:200] + "...\n")

    # Generate response
    try:
        llm_response = engine.generate(prompt_result.prompt)
        print("=" * 70)
        print("LLM RESPONSE")
        print("=" * 70)
        print(llm_response.response_text)
        print("\n" + "=" * 70)
        print(f"Model: {llm_response.model_name}")
        print(f"Response Length: {llm_response.response_length} chars")
        print(f"Success: {llm_response.success}")
    except LLMEngineError as exc:
        print(f"❌ Generation failed: {exc}")

    # ------------------------------------------------------------------
    # Step 4: Test with unrelated context (should say "not available")
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("[4] Negative Test: Unrelated Context")
    print("=" * 70)

    question2 = "Is dental surgery covered?"
    context2 = "Section 3.1 covers hospitalisation for accidental injuries only."

    prompt_result2 = builder.build_prompt(question=question2, context=context2)

    try:
        llm_response2 = engine.generate(prompt_result2.prompt)
        print(f"\nUser Question: {question2}")
        print(f"Context: {context2}")
        print("\nLLM Response:")
        print(llm_response2.response_text)
        print("\nExpected: Model should say 'Information not available in the policy document.'")
    except LLMEngineError as exc:
        print(f"❌ Error: {exc}")

    # ------------------------------------------------------------------
    # Step 5: Error handling (empty prompt)
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("[5] Error Handling: Empty Prompt")
    print("=" * 70)

    try:
        engine.generate("")
    except LLMEngineError as exc:
        print(f"✅ Caught expected error: {exc}")


if __name__ == "__main__":
    main()
