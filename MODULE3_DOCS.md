# Module 3: Answer Generator - Documentation

## Overview

The Answer Generator is the orchestration layer that combines Module 1 (Prompt Builder) and Module 2 (LLM Engine) to generate insurance policy answers from user questions and retrieved context.

## Architecture

```
User Question + Policy Context
         ↓
    AnswerGenerator
         ↓
  [1] Input Validation
         ↓
  [2] PromptBuilder.build_prompt()
         ↓
  [3] LLMEngine.generate()
         ↓
  [4] AnswerResult (with timing)
         ↓
    Structured Answer
```

## Installation

Already included in the project. No additional dependencies required.

## Quick Start

```python
from answer_generator import AnswerGenerator

# Initialize (mock mode for testing without Ollama)
generator = AnswerGenerator(use_mock_llm=True)

# Generate answer
result = generator.generate_response(
    question="Is flood damage covered?",
    context="Flood damage is covered under Section 4.2..."
)

print(result.answer)
print(f"Generation time: {result.generation_time:.3f}s")
```

## API Reference

### AnswerGenerator Class

```python
AnswerGenerator(
    model_name: str = "gemma:2b",
    temperature: float = 0.3,
    use_mock_llm: bool = True
)
```

**Parameters:**
- `model_name` - LLM model identifier (e.g., "gemma:2b", "llama2")
- `temperature` - Sampling temperature (0.0-1.0), lower = more deterministic
- `use_mock_llm` - If True, uses mock LLM (no Ollama required)

**Methods:**

#### generate_response()

```python
generate_response(question: str, context: str) -> AnswerResult
```

Generates an insurance policy answer from a question and context.

**Args:**
- `question` - User's insurance-related question (non-empty string)
- `context` - Relevant policy text from retrieval system (non-empty string)

**Returns:**
- `AnswerResult` dataclass with fields:
  - `question` (str) - The input question
  - `answer` (str) - Generated answer
  - `context_length` (int) - Character count of context
  - `success` (bool) - Whether generation succeeded
  - `generation_time` (float) - Total time in seconds

**Raises:**
- `AnswerGeneratorError` - If validation fails, prompt building fails, or LLM generation fails

### AnswerResult Dataclass

```python
@dataclass
class AnswerResult:
    question: str
    answer: str
    context_length: int
    success: bool
    generation_time: float
```

### AnswerGeneratorError Exception

Custom exception raised when answer generation fails.

```python
try:
    result = generator.generate_response("", "context")
except AnswerGeneratorError as e:
    print(f"Generation failed: {e}")
```

## Usage Examples

### Basic Usage

```python
from answer_generator import AnswerGenerator

generator = AnswerGenerator(use_mock_llm=True)

result = generator.generate_response(
    question="Is flood damage covered?",
    context="Flood damage is covered under Section 4.2 with maximum coverage of INR 5,00,000."
)

print(f"Q: {result.question}")
print(f"A: {result.answer}")
print(f"Time: {result.generation_time:.3f}s")
```

### Batch Processing

```python
questions = [
    ("Is fire damage covered?", "Fire damage is covered under Section 3.1."),
    ("What is the claim limit?", "The claim limit is INR 10,00,000."),
    ("What documents are needed?", "Submit FIR, bills, and claim form."),
]

for question, context in questions:
    result = generator.generate_response(question, context)
    print(f"{question} -> {result.answer[:50]}...")
```

### Error Handling

```python
from answer_generator import AnswerGeneratorError

try:
    result = generator.generate_response(
        question="",  # Invalid: empty
        context="Some context"
    )
except AnswerGeneratorError as e:
    print(f"Error: {e}")
```

### With Real LLM (Ollama)

```python
# Requires Ollama installed and running
generator = AnswerGenerator(
    model_name="gemma:2b",
    temperature=0.3,
    use_mock_llm=False  # Use real LLM
)

result = generator.generate_response(
    question="Is flood damage covered?",
    context="Flood damage is covered..."
)
```

## Integration with RAG System

When FAISS retrieval is ready:

```python
from answer_generator import AnswerGenerator
from faiss_retriever import retrieve_context  # Future module

generator = AnswerGenerator(use_mock_llm=True)

# User asks question
user_question = "Is flood damage covered?"

# Retrieve relevant context from FAISS
context = retrieve_context(user_question)  # Returns policy text

# Generate answer
result = generator.generate_response(
    question=user_question,
    context=context
)

print(result.answer)
```

## Testing

Run the test suite:

```bash
pytest test_answer_generator.py -v
```

Run with logs:

```bash
pytest test_answer_generator.py -v --log-cli-level=INFO
```

### Test Coverage

- ✅ Valid question + valid context
- ✅ Empty question error handling
- ✅ Empty context error handling
- ✅ Invalid input types (None, int, etc.)
- ✅ Successful answer generation
- ✅ Mock mode compatibility
- ✅ Response structure validation
- ✅ Comprehensive error handling
- ✅ Multiple request stability (10 consecutive)
- ✅ Logging verification
- ✅ Full integration test (Modules 1+2+3)

All 12 tests pass successfully.

## Performance

Typical performance in mock mode:
- Single request: ~0.001-0.003 seconds
- Batch of 10 requests: ~0.015 seconds
- Average: ~0.001-0.002 seconds per request

Real LLM performance depends on model size and hardware.

## Logging

The module generates comprehensive logs:

```
[INFO] AnswerGenerator - Answer generation started | question_length=50 | context_length=159
[INFO] PromptBuilder - Prompt built | question_chars=50 | context_chars=159
[INFO] LLMEngine - Sending request to LLM | model=gemma:2b | prompt_length=902
[INFO] LLMEngine - Response received | model=gemma:2b | response_length=155
[INFO] AnswerGenerator - Answer generation completed | time=0.003s | answer_length=155
```

## Error Scenarios

| Scenario | Exception | Message |
|----------|-----------|---------|
| Empty question | `AnswerGeneratorError` | "Question must not be empty." |
| Empty context | `AnswerGeneratorError` | "Context must not be empty." |
| None question | `AnswerGeneratorError` | "Question must be a string, got NoneType." |
| None context | `AnswerGeneratorError` | "Context must be a string, got NoneType." |
| Prompt building fails | `AnswerGeneratorError` | "Prompt building failed: ..." |
| LLM generation fails | `AnswerGeneratorError` | "LLM generation failed: ..." |

## Configuration

### Temperature Settings

```python
# More deterministic (recommended for insurance)
generator = AnswerGenerator(temperature=0.3)

# More creative
generator = AnswerGenerator(temperature=0.7)

# Completely deterministic
generator = AnswerGenerator(temperature=0.0)
```

### Model Selection

```python
# Fast, lightweight
generator = AnswerGenerator(model_name="gemma:2b")

# Better accuracy
generator = AnswerGenerator(model_name="gemma:7b")

# Alternative family
generator = AnswerGenerator(model_name="llama2")
```

## Project Status

✅ **Module 1 (Prompt Builder)** - Complete  
✅ **Module 2 (LLM Engine)** - Complete  
✅ **Module 3 (Answer Generator)** - Complete  
⏳ **Module 4 (PDF Processing + FAISS)** - Pending (other team)  
⏳ **Module 5 (End-to-end RAG)** - Future

## Next Steps

1. Integrate with PDF processing module
2. Integrate with FAISS retrieval module
3. Build complete RAG pipeline
4. Add evaluation metrics
5. Deploy to production

## License

Internal project - AI-Powered Insurance Claim Assistant
