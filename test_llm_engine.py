"""
test_llm_engine.py
Comprehensive test suite for LLM Engine (Module 2)

Run with:
    pytest test_llm_engine.py -v
"""

import pytest
import logging
from Insurance_Claim_Agent.llm_engine import LLMEngine, LLMResponse, LLMEngineError


@pytest.fixture
def mock_engine():
    """Fixture providing a mock LLM engine for testing."""
    return LLMEngine(model_name="gemma:2b", use_mock=True)


@pytest.fixture
def sample_insurance_prompt():
    """Fixture providing a sample insurance policy prompt."""
    return """You are an Insurance Claim Assistant.

POLICY CONTEXT:
Flood damage is covered under Section 4.2 of the policy with a maximum coverage amount of INR 5,00,000.

QUESTION:
Is flood damage covered?

ANSWER:"""


# TEST 1: Valid Prompt Test
def test_valid_prompt_generates_response(mock_engine, sample_insurance_prompt):
    """Verify that a valid prompt generates a successful response."""
    response = mock_engine.generate(sample_insurance_prompt)
    
    assert isinstance(response, LLMResponse)
    assert response.success is True
    assert response.response_text
    assert len(response.response_text) > 0


# TEST 2: Empty Prompt Test
def test_empty_prompt_raises_error(mock_engine):
    """Verify that an empty prompt raises LLMEngineError."""
    with pytest.raises(LLMEngineError) as exc_info:
        mock_engine.generate("")
    
    assert "must not be empty" in str(exc_info.value).lower()


# TEST 3: None Prompt Test
def test_none_prompt_raises_error(mock_engine):
    """Verify that None as prompt raises LLMEngineError."""
    with pytest.raises(LLMEngineError) as exc_info:
        mock_engine.generate(None)
    
    assert "must be a string" in str(exc_info.value).lower()


# TEST 4: Mock Mode Test
def test_mock_mode_works_without_ollama():
    """Verify that mock mode works without Ollama installation."""
    engine = LLMEngine(model_name="gemma:2b", use_mock=True)
    
    assert engine._use_mock is True
    response = engine.generate("What is insurance?")
    assert response.success is True


# TEST 5: Response Structure Test
def test_response_structure_is_valid(mock_engine, sample_insurance_prompt):
    """Verify that LLMResponse contains all required fields."""
    response = mock_engine.generate(sample_insurance_prompt)
    
    assert hasattr(response, "response_text")
    assert hasattr(response, "model_name")
    assert hasattr(response, "response_length")
    assert hasattr(response, "success")
    
    assert isinstance(response.response_text, str)
    assert isinstance(response.model_name, str)
    assert isinstance(response.response_length, int)
    assert isinstance(response.success, bool)
    
    assert response.response_length == len(response.response_text)


# TEST 6: Health Check Test
def test_health_check_returns_boolean(mock_engine):
    """Verify that health_check() returns a valid boolean."""
    result = mock_engine.health_check()
    
    assert isinstance(result, bool)
    assert result is True


# TEST 7: Insurance Question Test
def test_insurance_question_with_relevant_context(mock_engine):
    """Verify insurance questions with relevant context get appropriate answers."""
    prompt = """POLICY CONTEXT:
Flood damage is covered under Section 4.2 with maximum coverage of INR 5,00,000.

QUESTION:
Is flood damage covered?"""
    
    response = mock_engine.generate(prompt)
    
    assert response.success is True
    assert len(response.response_text) > 20


# TEST 8: Unsupported Question Test
def test_unsupported_question(mock_engine):
    """Verify unrelated questions get handled properly."""
    prompt = """POLICY CONTEXT:
Section 3.1 covers hospitalisation for accidental injuries only.

QUESTION:
What is my bank balance?"""
    
    response = mock_engine.generate(prompt)
    
    assert response.success is True
    assert len(response.response_text) > 0


# TEST 9: Logging Verification Test
def test_logging_is_generated(mock_engine, sample_insurance_prompt, caplog):
    """Verify that proper logs are generated during LLM operations."""
    with caplog.at_level(logging.INFO):
        response = mock_engine.generate(sample_insurance_prompt)
    
    assert len(caplog.records) > 0


# TEST 10: Multiple Request Stability Test
def test_multiple_requests_stability(mock_engine):
    """Verify engine handles multiple consecutive requests reliably."""
    test_prompts = [
        "Is flood damage covered?",
        "What is the claim limit?",
        "How to file a claim?",
        "Is fire damage covered?",
        "What documents are needed?",
        "What is the deductible?",
        "Is theft covered?",
        "What is the policy period?",
        "How to contact support?",
        "Is earthquake damage covered?"
    ]
    
    responses = []
    
    for i, prompt in enumerate(test_prompts, 1):
        response = mock_engine.generate(prompt)
        
        assert response.success is True
        assert len(response.response_text) > 0
        assert response.model_name == "gemma:2b"
        
        responses.append(response)
    
    assert len(responses) == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
