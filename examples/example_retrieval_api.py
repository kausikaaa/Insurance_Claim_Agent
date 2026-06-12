"""Example: How LLM teams should use the Retrieval API."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from retriever import retrieve


def main():
    """
    Demonstrate the simple retrieve() API for LLM teams.
    
    NO need to:
    - Load PDFs
    - Clean text
    - Chunk documents
    - Generate embeddings
    - Manage FAISS indexes
    
    Just call retrieve() with your query!
    """
    
    print("=" * 80)
    print("RETRIEVAL API - SIMPLE EXAMPLE FOR LLM TEAMS")
    print("=" * 80)
    
    print("\nThis is the ONLY function you need:")
    print("  from retriever import retrieve")
    print("  chunks = retrieve('your query here')")
    
    print("\n" + "=" * 80)
    print("EXAMPLE QUERIES")
    print("=" * 80)
    
    # Example 1: Simple query
    print("\n[Example 1] Simple query")
    print("-" * 80)
    query1 = "What is covered for flood damage?"
    print(f"Query: '{query1}'")
    
    results = retrieve(query1, k=2)
    print(f"\nRetrieved {len(results)} relevant chunks:\n")
    for i, chunk in enumerate(results, 1):
        print(f"{i}. {chunk[:120]}...")
    
    # Example 2: Different query
    print("\n" + "-" * 80)
    print("[Example 2] Claims process query")
    print("-" * 80)
    query2 = "How do I file an insurance claim?"
    print(f"Query: '{query2}'")
    
    results = retrieve(query2, k=2)
    print(f"\nRetrieved {len(results)} relevant chunks:\n")
    for i, chunk in enumerate(results, 1):
        print(f"{i}. {chunk[:120]}...")
    
    # Example 3: Cost-related query
    print("\n" + "-" * 80)
    print("[Example 3] Cost query")
    print("-" * 80)
    query3 = "What is the deductible?"
    print(f"Query: '{query3}'")
    
    results = retrieve(query3, k=2)
    print(f"\nRetrieved {len(results)} relevant chunks:\n")
    for i, chunk in enumerate(results, 1):
        print(f"{i}. {chunk[:120]}...")
    
    # Example 4: Using in LLM context
    print("\n" + "=" * 80)
    print("HOW TO USE WITH LLM")
    print("=" * 80)
    
    user_question = "Is flood damage covered and what is the limit?"
    print(f"\nUser asks: '{user_question}'")
    
    # Step 1: Retrieve relevant context
    context_chunks = retrieve(user_question, k=3)
    
    # Step 2: Build context for LLM
    context = "\\n\\n".join(context_chunks)
    
    # Step 3: Create LLM prompt
    prompt = f"""Based on the following insurance policy information, answer the user's question.

Context:
{context}

User Question: {user_question}

Answer:"""
    
    print("\n[Step 1] Retrieved context from knowledge base")
    print(f"[Step 2] Combined {len(context_chunks)} chunks into context")
    print("[Step 3] Created LLM prompt with context")
    
    print("\nPrompt preview:")
    print("-" * 80)
    print(prompt[:400] + "...")
    
    print("\n" + "=" * 80)
    print("THAT'S IT!")
    print("=" * 80)
    print("""
No need to worry about:
  [X] PDF loading
  [X] Text cleaning
  [X] Chunking
  [X] Embeddings
  [X] FAISS indexes
  [X] Vector similarity

Just use:
  [OK] retrieve(query, k=3)

And you get relevant context for your LLM!
""")


if __name__ == "__main__":
    main()
