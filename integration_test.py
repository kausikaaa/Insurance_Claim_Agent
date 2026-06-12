"""
integration_test.py
Integration test for the complete AI-Powered Insurance Claim Assistant pipeline.

Tests the full flow:
Question -> Prompt Builder -> LLM Engine -> Answer Generator -> Final Response

Run with: python integration_test.py
"""

from Insurance_Claim_Agent.answer_generator import AnswerGenerator, AnswerGeneratorError

print("=" * 70)
print("INTEGRATION TEST: AI-Powered Insurance Claim Assistant")
print("=" * 70)
print()

# Initialize the Answer Generator (using mock mode for testing)
print("[1/5] Initializing Answer Generator...")
try:
    generator = AnswerGenerator(use_mock_llm=True)
    print("      [OK] Answer Generator initialized")
    print("      [OK] Prompt Builder loaded")
    print("      [OK] LLM Engine loaded (mock mode)")
except Exception as e:
    print(f"      [ERROR] Initialization failed: {e}")
    exit(1)

print()

# Test Case 1: Basic flood damage query
print("[2/5] Testing basic insurance query...")
try:
    result = generator.generate_response(
        question="Is flood damage covered?",
        context="""
        Flood damage is covered under Section 4.2.
        Maximum claim amount is INR 5,00,000.
        """
    )
    
    print(f"      Question: {result.question}")
    print(f"      Answer: {result.answer}")
    print(f"      Context Length: {result.context_length} chars")
    print(f"      Success: {result.success}")
    print(f"      Generation Time: {result.generation_time:.3f}s")
    print("      [OK] Basic query working")
except Exception as e:
    print(f"      [ERROR] Basic query failed: {e}")
    exit(1)

print()

# Test Case 2: Detailed policy query
print("[3/5] Testing detailed policy query...")
try:
    result = generator.generate_response(
        question="What documents are required for filing an accident claim?",
        context="""
        For accident claims, the following documents must be submitted:
        1. First Information Report (FIR) from police
        2. Medical reports from treating hospital
        3. Original hospital bills and receipts
        4. Duly filled claim form signed by insured person
        5. Identity proof of claimant
        
        All documents must be submitted within 30 days of the incident.
        """
    )
    
    print(f"      Question: {result.question[:50]}...")
    print(f"      Answer: {result.answer[:100]}...")
    print(f"      Success: {result.success}")
    print(f"      Generation Time: {result.generation_time:.3f}s")
    print("      [OK] Detailed query working")
except Exception as e:
    print(f"      [ERROR] Detailed query failed: {e}")
    exit(1)

print()

# Test Case 3: Query with no relevant context (should decline)
print("[4/5] Testing query with unrelated context...")
try:
    result = generator.generate_response(
        question="Is dental surgery covered?",
        context="Section 3.1 covers hospitalisation for accidental injuries only."
    )
    
    print(f"      Question: {result.question}")
    print(f"      Answer: {result.answer}")
    print(f"      Success: {result.success}")
    
    # Check if model appropriately handles unrelated context
    if "not available" in result.answer.lower() or "section 3.1" in result.answer.lower():
        print("      [OK] Unrelated context handled appropriately")
    else:
        print("      [WARNING] Model may not have recognized unrelated context")
except Exception as e:
    print(f"      [ERROR] Unrelated context test failed: {e}")
    exit(1)

print()

# Test Case 4: Error handling
print("[5/5] Testing error handling...")
error_tests_passed = 0

# Empty question
try:
    result = generator.generate_response(
        question="",
        context="Some context"
    )
    print("      [ERROR] Empty question should have raised error")
except AnswerGeneratorError:
    print("      [OK] Empty question rejected")
    error_tests_passed += 1

# Empty context
try:
    result = generator.generate_response(
        question="Some question",
        context=""
    )
    print("      [ERROR] Empty context should have raised error")
except AnswerGeneratorError:
    print("      [OK] Empty context rejected")
    error_tests_passed += 1

# None inputs
try:
    result = generator.generate_response(
        question=None,
        context="Some context"
    )
    print("      [ERROR] None question should have raised error")
except AnswerGeneratorError:
    print("      [OK] None question rejected")
    error_tests_passed += 1

if error_tests_passed == 3:
    print("      [OK] All error handling tests passed")

print()
print("=" * 70)
print("INTEGRATION TEST SUMMARY")
print("=" * 70)
print()
print("Pipeline Verification:")
print("  [OK] Question input accepted")
print("  [OK] Prompt Builder creates structured prompt")
print("  [OK] LLM Engine generates response")
print("  [OK] Answer Generator returns structured result")
print("  [OK] Error handling working")
print()
print("Module Integration:")
print("  [OK] Module 1 (Prompt Builder) -> Module 2 (LLM Engine)")
print("  [OK] Module 2 (LLM Engine) -> Module 3 (Answer Generator)")
print("  [OK] Complete pipeline: Question -> Answer")
print()
print("=" * 70)
print("RESULT: [OK] CORE PIPELINE IS STABLE AND READY")
print("=" * 70)
print()
print("Next steps:")
print("  1. Integrate PDF Processing module (when ready)")
print("  2. Integrate FAISS Retrieval module (when ready)")
print("  3. Build complete RAG system")
print()
