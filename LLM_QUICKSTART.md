# Quick Start Guide: Retrieval API for LLM Teams

## TL;DR

```python
from retriever import retrieve

# That's it! Just call retrieve() with your query
chunks = retrieve("Is flood damage covered?")

# Use chunks as context for your LLM
for chunk in chunks:
    print(chunk)
```

---

## Installation

No additional dependencies needed. The system is ready to use.

---

## Basic Usage

### 1. Import the function

```python
from retriever import retrieve
```

### 2. Retrieve context

```python
# Get top 3 results (default)
chunks = retrieve("What is the coverage limit?")

# Get more results
chunks = retrieve("What is the coverage limit?", k=5)

# Get fewer results
chunks = retrieve("What is the coverage limit?", k=1)
```

### 3. Use in your LLM prompt

```python
user_question = "Is flood damage covered?"

# Retrieve relevant context
context_chunks = retrieve(user_question, k=3)
context = "\n\n".join(context_chunks)

# Build LLM prompt
prompt = f"""Answer the question based on this context.

Context:
{context}

Question: {user_question}

Answer:"""

# Send to your LLM
response = your_llm.generate(prompt)
```

---

## Complete RAG Example

```python
from retriever import retrieve

def build_rag_prompt(user_question: str, k: int = 3) -> str:
    """
    Build a RAG prompt with retrieved context.
    
    Args:
        user_question: User's question
        k: Number of context chunks to retrieve
        
    Returns:
        Complete prompt ready for LLM
    """
    # Retrieve relevant chunks
    chunks = retrieve(user_question, k=k)
    
    # Build context
    context = "\n\n---\n\n".join(chunks)
    
    # Build prompt
    prompt = f"""You are an insurance policy assistant. Answer the user's question based on the following policy information.

Policy Information:
{context}

User Question: {user_question}

Instructions:
- Answer based only on the provided policy information
- If the information is not in the context, say so
- Be concise and accurate
- Quote specific sections when relevant

Answer:"""
    
    return prompt


# Usage
if __name__ == "__main__":
    question = "What is the deductible amount?"
    prompt = build_rag_prompt(question)
    
    # Send prompt to your LLM API
    # response = openai.ChatCompletion.create(...)
    # response = anthropic.messages.create(...)
    # response = bedrock.invoke_model(...)
```

---

## Error Handling

```python
from retriever import retrieve, InvalidQueryError, VectorStoreNotFoundError, RetrievalError

try:
    chunks = retrieve(user_query)
    
except InvalidQueryError:
    print("Please provide a valid question")
    
except VectorStoreNotFoundError:
    print("Knowledge base not available")
    
except RetrievalError as e:
    print(f"Retrieval failed: {e}")
```

---

## Common Patterns

### Pattern 1: Multi-turn Conversation

```python
conversation_history = []

def handle_user_message(user_message: str) -> str:
    # Retrieve context for current message
    chunks = retrieve(user_message, k=3)
    context = "\n\n".join(chunks)
    
    # Build prompt with conversation history
    prompt = f"""Context: {context}

Conversation:
{conversation_history}

User: {user_message}
Assistant:"""
    
    response = llm.generate(prompt)
    
    # Update history
    conversation_history.append(f"User: {user_message}")
    conversation_history.append(f"Assistant: {response}")
    
    return response
```

### Pattern 2: Fact Verification

```python
def verify_claim(claim: str) -> dict:
    """Verify a claim against policy documents."""
    
    # Retrieve relevant policy sections
    evidence = retrieve(claim, k=5)
    
    # Check if claim is supported
    context = " ".join(evidence)
    
    return {
        "claim": claim,
        "evidence": evidence,
        "supported": check_claim_in_context(claim, context)
    }
```

### Pattern 3: Query Expansion

```python
def retrieve_with_expansion(query: str, k: int = 3) -> list:
    """Retrieve with query expansion for better results."""
    
    # Get results for original query
    results = retrieve(query, k=k)
    
    # Optionally expand query and get more results
    expanded_query = expand_query(query)  # Your expansion logic
    additional_results = retrieve(expanded_query, k=k//2)
    
    # Combine and deduplicate
    all_results = results + [r for r in additional_results if r not in results]
    
    return all_results[:k]
```

---

## Performance Tips

### ✅ DO

- **Reuse the same process**: The vectorstore and model are cached globally
- **Call retrieve() multiple times**: Each call is fast (~15ms)
- **Use appropriate k values**: Start with k=3, adjust based on results

### ❌ DON'T

- **Don't reload the module repeatedly**: Keep imports at module level
- **Don't recreate the process**: Each process has its own cache
- **Don't use extremely large k**: k>20 rarely helps and increases latency

---

## Troubleshooting

### "VectorStoreNotFoundError"

**Problem**: Knowledge base not found

**Solution**: Ensure the `vector_store/` directory exists with:
- `faiss_index` file
- `chunks.pkl` file

These are created during the document ingestion phase.

---

### Empty Results

**Problem**: `retrieve()` returns empty list

**Solution**: 
- Check if query is meaningful
- Try different phrasing
- Check if documents were indexed correctly

---

### Irrelevant Results

**Problem**: Retrieved chunks not relevant to query

**Solution**:
- Rephrase query to be more specific
- Increase k to get more options
- Check document quality/chunking

---

## API Reference

### retrieve(query: str, k: int = 3) -> List[str]

**Parameters**:
- `query` (str): Natural language query or question
- `k` (int, optional): Number of results to return (default: 3)

**Returns**:
- `List[str]`: List of relevant text chunks, ranked by similarity

**Raises**:
- `InvalidQueryError`: Query is None, empty, or invalid type
- `VectorStoreNotFoundError`: Knowledge base cannot be loaded
- `RetrievalError`: Other retrieval failures

**Example**:
```python
chunks = retrieve("What is covered?", k=5)
```

---

## What You DON'T Need to Know

The following are handled automatically:

- ❌ PDF loading and parsing
- ❌ Text cleaning and preprocessing
- ❌ Document chunking strategy
- ❌ Embedding model selection
- ❌ Embedding generation
- ❌ Vector database (FAISS) operations
- ❌ Similarity calculations
- ❌ Index management
- ❌ Model caching

**Just focus on building great LLM applications!**

---

## Support

For issues or questions:
1. Check the verification document: `PHASE6_VERIFICATION.md`
2. Review examples in: `examples/example_retrieval_api.py`
3. Run tests to verify setup: `python test_retriever.py`

---

## Next Steps

1. ✅ Import `retrieve` from `retriever`
2. ✅ Call `retrieve(your_query)`
3. ✅ Use results in your LLM prompt
4. ✅ Build amazing applications!

**Happy building! 🚀**
