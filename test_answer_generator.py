"""
test_answer_generator.py
Comprehensive test suite for Answer Generator (Module 3)

Tests orchestration between Prompt Builder and LLM Engine,
error handling, response structure, and integration scenarios.

Run with:
    pytest test_answer_generator.py -v
"""

import pytest
import logging
import time
from Insurance_Claim_Agent.answer_generator import AnswerGenerator, AnswerResult, AnswerGeneratorError


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture
def generator():
    """Fixture providing an Answer Generator in mock mode."""
    return AnswerGenerator(use_mock_llm=True)


@pytest.fixture
def valid_question():
    """Fixture providing a valid insurance question."""
    return "Is flood damage covered under my insurance policy?"


@pytest.fixture
def valid_context():
    """Fixture providing valid policy context."""
    return (
        "Flood damage is covered under Section 4.2 of the policy "
        "with a maximum coverage amount of INR 5,00,000. "
        "The claim must be filed within 30 days of the incident."
    )


# ==============================================================================
# TEST CASE 1: Valid Question + Valid Context
# ==============================================================================

def test_valid_question_and_context_generates_answer(generator, valid_question, valid_context):
    """
    TEST 1: Valid Question + Valid Context
    
    Verify that valid inputs generate a successful answer.
    
    Given: A valid insurance question and policy context
    When: generate_response() is called
    Then: Returns AnswerResult with success=True and non-empty answer
    """
    result = generator.generate_response(
        question=valid_question,
        context=valid_context,
    )
    
    assert isinstance(result, AnswerResult), "Must return AnswerResult object"
    assert result.success is True, "success flag must be True"
    assert result.answer, "answer must not be empty"
    assert len(result.answer) > 0, "answer must contain content"
    assert result.question == valid_question, "question must match input"
    assert result.context_length == len(valid_context), "context_length must match"
    assert result.generation_time >= 0.001, "generation_time must be at least 0.001s"
    
    print(f"\nGenerated answer: {result.answer[:100]}...")
    print(f"Generation time: {result.generation_time:.3f}s")


# ==============================================================================
# TEST CASE 2: Empty Question
# ==============================================================================

def test_empty_question_raises_error(generator, valid_context):
    """
    TEST 2: Empty Question
    
    Verify that an empty question raises AnswerGeneratorError.
    
    Given: An empty question string
    When: generate_response() is called
    Then: AnswerGeneratorError is raised
    """
    with pytest.raises(AnswerGeneratorError) as exc_info:
        generator.generate_response(question="", context=valid_context)
    
    assert "question" in str(exc_info.value).lower(), \
        "Error message should mention question"
    assert "empty" in str(exc_info.value).lower(), \
        "Error message should mention empty"
    
    print(f"\nCaught expected error: {exc_info.value}")


# ==============================================================================
# TEST CASE 3: Empty Context
# ==============================================================================

def test_empty_context_raises_error(generator, valid_question):
    """
    TEST 3: Empty Context
    
    Verify that an empty context raises AnswerGeneratorError.
    
    Given: An empty context string
    When: generate_response() is called
    Then: AnswerGeneratorError is raised
    """
    with pytest.raises(AnswerGeneratorError) as exc_info:
        generator.generate_response(question=valid_question, context="")
    
    assert "context" in str(exc_info.value).lower(), \
        "Error message should mention context"
    assert "empty" in str(exc_info.value).lower(), \
        "Error message should mention empty"
    
    print(f"\nCaught expected error: {exc_info.value}")


# ==============================================================================
# TEST CASE 4: Invalid Input Types
# ==============================================================================

def test_invalid_question_type_raises_error(generator, valid_context):
    """
    TEST 4a: Invalid Input Types - Question
    
    Verify that non-string question raises AnswerGeneratorError.
    """
    with pytest.raises(AnswerGeneratorError) as exc_info:
        generator.generate_response(question=None, context=valid_context)
    
    assert "question" in str(exc_info.value).lower()
    assert "string" in str(exc_info.value).lower()
    
    print(f"\nCaught expected error: {exc_info.value}")


def test_invalid_context_type_raises_error(generator, valid_question):
    """
    TEST 4b: Invalid Input Types - Context
    
    Verify that non-string context raises AnswerGeneratorError.
    """
    with pytest.raises(AnswerGeneratorError) as exc_info:
        generator.generate_response(question=valid_question, context=123)
    
    assert "context" in str(exc_info.value).lower()
    assert "string" in str(exc_info.value).lower()
    
    print(f"\nCaught expected error: {exc_info.value}")


# ==============================================================================
# TEST CASE 5: Successful Answer Generation
# ==============================================================================

def test_successful_answer_generation_workflow(generator):
    """
    TEST 5: Successful Answer Generation
    
    Verify complete workflow from question to answer.
    
    Given: Multiple insurance scenarios
    When: generate_response() is called for each
    Then: All return successful answers
    """
    test_cases = [
        {
            "question": "Is flood damage covered?",
            "context": "Flood damage is covered under Section 4.2 with maximum coverage of INR 5,00,000.",
        },
        {
            "question": "What is the claim limit?",
            "context": "The claim limit is INR 10,00,000 per policy year.",
        },
        {
            "question": "What documents are required?",
            "context": "Required documents: FIR copy, medical reports, hospital bills, claim form.",
        },
    ]
    
    for idx, case in enumerate(test_cases, 1):
        result = generator.generate_response(
            question=case["question"],
            context=case["context"],
        )
        
        assert result.success is True, f"Case {idx} should succeed"
        assert len(result.answer) > 0, f"Case {idx} should have answer"
        
        print(f"\nCase {idx}: {case['question'][:40]}...")
        print(f"  Answer: {result.answer[:80]}...")


# ==============================================================================
# TEST CASE 6: Mock Mode Compatibility
# ==============================================================================

def test_mock_mode_compatibility():
    """
    TEST 6: Mock Mode Compatibility
    
    Verify that Answer Generator works in mock mode without Ollama.
    
    Given: Answer Generator initialized with use_mock_llm=True
    When: generate_response() is called
    Then: Works without Ollama dependency
    """
    generator = AnswerGenerator(
        model_name="gemma:2b",
        temperature=0.3,
        use_mock_llm=True,
    )
    
    result = generator.generate_response(
        question="Is fire damage covered?",
        context="Fire damage is covered under Section 3.1.",
    )
    
    assert result.success is True, "Mock mode should work"
    assert result.answer, "Mock mode should generate answer"
    
    print(f"\nMock mode working correctly")
    print(f"Answer: {result.answer}")


# ==============================================================================
# TEST CASE 7: Response Structure Validation
# ==============================================================================

def test_response_structure_validation(generator, valid_question, valid_context):
    """
    TEST 7: Response Structure Validation
    
    Verify AnswerResult contains all required fields with correct types.
    
    Given: A valid answer generation
    When: Result is returned
    Then: All fields exist with correct types
    """
    result = generator.generate_response(
        question=valid_question,
        context=valid_context,
    )
    
    # Verify all fields exist
    assert hasattr(result, "question"), "Must have question field"
    assert hasattr(result, "answer"), "Must have answer field"
    assert hasattr(result, "context_length"), "Must have context_length field"
    assert hasattr(result, "success"), "Must have success field"
    assert hasattr(result, "generation_time"), "Must have generation_time field"
    
    # Verify field types
    assert isinstance(result.question, str), "question must be string"
    assert isinstance(result.answer, str), "answer must be string"
    assert isinstance(result.context_length, int), "context_length must be int"
    assert isinstance(result.success, bool), "success must be boolean"
    assert isinstance(result.generation_time, float), "generation_time must be float"
    
    # Verify field values
    assert result.context_length > 0, "context_length must be positive"
    assert result.generation_time >= 0.001, "generation_time must be at least 0.001s"
    
    print(f"\nResponse structure validated:")
    print(f"  - question: {type(result.question).__name__}")
    print(f"  - answer: {type(result.answer).__name__} (length: {len(result.answer)})")
    print(f"  - context_length: {result.context_length}")
    print(f"  - success: {result.success}")
    print(f"  - generation_time: {result.generation_time:.3f}s")


# ==============================================================================
# TEST CASE 8: Error Handling
# ==============================================================================

def test_error_handling_coverage(generator):
    """
    TEST 8: Error Handling
    
    Verify comprehensive error handling for various failure scenarios.
    """
    # Test empty question
    with pytest.raises(AnswerGeneratorError):
        generator.generate_response("", "Some context")
    
    # Test empty context
    with pytest.raises(AnswerGeneratorError):
        generator.generate_response("Some question", "")
    
    # Test None question
    with pytest.raises(AnswerGeneratorError):
        generator.generate_response(None, "Some context")
    
    # Test None context
    with pytest.raises(AnswerGeneratorError):
        generator.generate_response("Some question", None)
    
    # Test whitespace-only question
    with pytest.raises(AnswerGeneratorError):
        generator.generate_response("   ", "Some context")
    
    # Test whitespace-only context
    with pytest.raises(AnswerGeneratorError):
        generator.generate_response("Some question", "   ")
    
    print("\nAll error scenarios handled correctly")


# ==============================================================================
# TEST CASE 9: Multiple Request Stability
# ==============================================================================

def test_multiple_request_stability(generator):
    """
    TEST 9: Multiple Request Stability
    
    Verify stable operation across multiple consecutive requests.
    
    Given: An Answer Generator
    When: 10 consecutive requests are made
    Then: All succeed without degradation
    """
    requests = [
        ("Is flood damage covered?", "Flood damage is covered under Section 4.2."),
        ("What is the claim limit?", "The claim limit is INR 10,00,000 per year."),
        ("How to file a claim?", "File claims online or at branch offices."),
        ("Is fire damage covered?", "Fire damage is covered under Section 3.1."),
        ("What documents are needed?", "Submit FIR, bills, and claim form."),
        ("Is theft covered?", "Theft is covered under Section 5.3."),
        ("What is the deductible?", "The deductible is INR 25,000."),
        ("Is earthquake damage covered?", "Earthquake damage is not covered."),
        ("How long does processing take?", "Processing takes 15-30 business days."),
        ("Can I track my claim?", "Track claims via online portal or helpline."),
    ]
    
    results = []
    
    for idx, (question, context) in enumerate(requests, 1):
        result = generator.generate_response(question=question, context=context)
        
        assert result.success is True, f"Request {idx} should succeed"
        assert len(result.answer) > 0, f"Request {idx} should have answer"
        assert result.generation_time > 0, f"Request {idx} should have valid time"
        
        results.append(result)
    
    assert len(results) == 10, "Should process all 10 requests"
    
    avg_time = sum(r.generation_time for r in results) / len(results)
    
    print(f"\nSuccessfully processed {len(results)} consecutive requests")
    print(f"Average generation time: {avg_time:.3f}s")
    print("No crashes or memory issues detected")


# ==============================================================================
# TEST CASE 10: Logging Verification
# ==============================================================================

def test_logging_verification(generator, valid_question, valid_context, caplog):
    """
    TEST 10: Logging Verification
    
    Verify that appropriate logs are generated during answer generation.
    
    Given: A generator with logging enabled
    When: generate_response() is called
    Then: Logs contain key information
    """
    with caplog.at_level(logging.INFO):
        result = generator.generate_response(
            question=valid_question,
            context=valid_context,
        )
    
    assert len(caplog.records) > 0, "Logs should be generated"
    
    log_messages = [record.message for record in caplog.records]
    log_text = " ".join(log_messages)
    
    # Verify key log messages
    assert "started" in log_text.lower() or "generation" in log_text.lower(), \
        "Should log generation start"
    assert "completed" in log_text.lower() or "success" in log_text.lower(), \
        "Should log completion"
    
    print(f"\nLogs generated: {len(caplog.records)} entries")
    for record in caplog.records[:5]:
        print(f"  [{record.levelname}] {record.message}")


# ==============================================================================
# BONUS TEST: Integration Test
# ==============================================================================

def test_full_integration_modules_1_2_3():
    """
    BONUS: Full Integration Test
    
    Verify complete integration of all three modules.
    """
    generator = AnswerGenerator(use_mock_llm=True)
    
    result = generator.generate_response(
        question="Is flood damage covered under my policy?",
        context=(
            "Flood damage is covered under Section 4.2 of the policy "
            "with a maximum coverage amount of INR 5,00,000. "
            "The claim must be filed within 30 days."
        ),
    )
    
    assert result.success is True
    assert "flood" in result.answer.lower() or "covered" in result.answer.lower()
    assert result.generation_time < 5.0, "Should complete in reasonable time"
    
    print(f"\nFull integration test passed")
    print(f"Question: {result.question}")
    print(f"Answer: {result.answer}")
    print(f"Time: {result.generation_time:.3f}s")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
