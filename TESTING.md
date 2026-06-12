# Testing Guide for LLM Engine Module

## Installation

Install test dependencies:

```bash
pip install pytest pytest-cov
```

## Running Tests

### Run All Tests

```bash
pytest test_llm_engine.py -v
```

### Run with Detailed Logs

```bash
pytest test_llm_engine.py -v --log-cli-level=INFO
```

### Run Specific Test

```bash
pytest test_llm_engine.py::test_valid_prompt_generates_response -v
```

### Run with Coverage Report

```bash
pytest test_llm_engine.py --cov=llm_engine --cov-report=html
```

### Run with Output

```bash
pytest test_llm_engine.py -v -s
```

## Test Cases Included

| # | Test Name | Purpose |
|---|-----------|---------|
| 1 | test_valid_prompt_generates_response | Valid prompt returns successful response |
| 2 | test_empty_prompt_raises_error | Empty prompt raises LLMEngineError |
| 3 | test_none_prompt_raises_error | None prompt raises LLMEngineError |
| 4 | test_mock_mode_works_without_ollama | Mock mode works without Ollama |
| 5 | test_response_structure_is_valid | Response has all required fields |
| 6 | test_health_check_returns_boolean | Health check returns boolean |
| 7 | test_insurance_question_with_relevant_context | Relevant context produces answer |
| 8 | test_unsupported_question | Unrelated questions handled properly |
| 9 | test_logging_is_generated | Logs are generated during operations |
| 10 | test_multiple_requests_stability | 10 consecutive requests succeed |

## Expected Results

All 10 tests should **PASS** when running in mock mode.

Example output:

```
test_llm_engine.py::test_valid_prompt_generates_response PASSED
test_llm_engine.py::test_empty_prompt_raises_error PASSED
test_llm_engine.py::test_none_prompt_raises_error PASSED
test_llm_engine.py::test_mock_mode_works_without_ollama PASSED
test_llm_engine.py::test_response_structure_is_valid PASSED
test_llm_engine.py::test_health_check_returns_boolean PASSED
test_llm_engine.py::test_insurance_question_with_relevant_context PASSED
test_llm_engine.py::test_unsupported_question PASSED
test_llm_engine.py::test_logging_is_generated PASSED
test_llm_engine.py::test_multiple_requests_stability PASSED

========== 10 passed in 0.XX s ==========
```

## Continuous Integration

Add to CI/CD pipeline:

```yaml
- name: Run Tests
  run: pytest test_llm_engine.py -v --cov=llm_engine
```

## Troubleshooting

### If pytest not found

```bash
pip install pytest
```

### If tests fail

1. Check that llm_engine.py is in the same directory
2. Check that prompt_builder.py is in the same directory
3. Run with -v -s flags for detailed output

### If import errors

```bash
# Ensure you're in the project directory
cd c:\Users\rssri\Desktop\INSURANCECLAIMAGENT
python -m pytest test_llm_engine.py -v
```

## Test Coverage

To generate HTML coverage report:

```bash
pytest test_llm_engine.py --cov=llm_engine --cov-report=html
```

Open `htmlcov/index.html` in browser to view detailed coverage.

## Quality Assurance Checklist

- [x] All 10 required test cases implemented
- [x] Pytest fixtures for reusable components
- [x] Error handling tests
- [x] Mock mode tests (no Ollama required)
- [x] Response structure validation
- [x] Logging verification
- [x] Stability testing (10 consecutive requests)
- [x] Configuration validation
- [x] Descriptive test names and docstrings
- [x] Production-quality assertions

## Status

**Module 2 Test Suite:** ✅ Complete and Ready for Execution
