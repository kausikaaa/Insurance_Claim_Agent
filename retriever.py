"""Retrieval API layer for LLM integration - Phase 6."""

from typing import List
from faiss_store import load_index, FAISSVectorStore


class RetrievalError(Exception):
    """Base exception for retrieval errors."""
    pass


class InvalidQueryError(RetrievalError):
    """Raised when query is invalid."""
    pass


class VectorStoreNotFoundError(RetrievalError):
    """Raised when vector store is not found."""
    pass


_vectorstore_cache = None


def _get_vectorstore(directory: str = "vector_store") -> FAISSVectorStore:
    """
    Get or load the FAISS vectorstore (singleton pattern).
    
    Args:
        directory: Directory containing the saved vectorstore.
        
    Returns:
        Loaded FAISSVectorStore object.
        
    Raises:
        VectorStoreNotFoundError: If vectorstore cannot be loaded.
    """
    global _vectorstore_cache
    
    if _vectorstore_cache is None:
        try:
            _vectorstore_cache = load_index(directory)
        except Exception as e:
            raise VectorStoreNotFoundError(
                f"Failed to load vector store from '{directory}': {str(e)}"
            ) from e
    
    return _vectorstore_cache


def retrieve(query: str, k: int = 3) -> List[str]:
    """
    Retrieve relevant document chunks for a given query.
    
    This is the ONLY public function the LLM team should use.
    It handles all internal operations: loading vectorstore,
    generating embeddings, and running FAISS similarity search.
    
    Args:
        query: Natural language query string.
        k: Number of top results to return (default: 3).
        
    Returns:
        List of most relevant text chunks, ranked by similarity (best first).
        
    Raises:
        InvalidQueryError: If query is None, empty, or invalid type.
        VectorStoreNotFoundError: If vectorstore cannot be loaded.
        RetrievalError: If retrieval fails for any other reason.
        
    Examples:
        >>> chunks = retrieve("Is flood damage covered?")
        >>> chunks = retrieve("What is the coverage limit?", k=5)
        >>> for chunk in chunks:
        ...     print(chunk)
    """
    if query is None:
        raise InvalidQueryError("Query cannot be None")
    
    if not isinstance(query, str):
        raise InvalidQueryError(f"Query must be a string, got {type(query).__name__}")
    
    if not query.strip():
        raise InvalidQueryError("Query cannot be empty or whitespace-only")
    
    try:
        vectorstore = _get_vectorstore()
        results = vectorstore.similarity_search(query, top_k=k)
        return results
        
    except (InvalidQueryError, VectorStoreNotFoundError):
        raise
    except Exception as e:
        raise RetrievalError(f"Retrieval failed: {str(e)}") from e
