"""Embedding generation module for converting text chunks to vector embeddings."""

from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingError(Exception):
    """Base exception for embedding generation errors."""
    pass


class ModelLoadError(EmbeddingError):
    """Raised when the embedding model fails to load."""
    pass


class InvalidChunkError(EmbeddingError):
    """Raised when input chunks are invalid."""
    pass


_model_cache = None


def _get_model() -> SentenceTransformer:
    """
    Get or load the sentence transformer model (singleton pattern).
    
    Returns:
        Loaded SentenceTransformer model.
        
    Raises:
        ModelLoadError: If model fails to load.
    """
    global _model_cache
    
    if _model_cache is None:
        try:
            _model_cache = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        except Exception as e:
            raise ModelLoadError(f"Failed to load embedding model: {str(e)}") from e
    
    return _model_cache


def generate_embeddings(chunks: List[str]) -> List[List[float]]:
    """
    Generate vector embeddings for text chunks using sentence-transformers.
    
    Args:
        chunks: List of text chunks to embed.
        
    Returns:
        List of embeddings, where each embedding is a list of floats.
        Each embedding has 384 dimensions (all-MiniLM-L6-v2 model).
        
    Raises:
        InvalidChunkError: If chunks is None, not a list, or contains invalid elements.
        EmbeddingError: If embedding generation fails.
        
    Examples:
        >>> chunks = ["This is a test", "Another chunk"]
        >>> embeddings = generate_embeddings(chunks)
        >>> len(embeddings)
        2
        >>> len(embeddings[0])
        384
    """
    if chunks is None:
        raise InvalidChunkError("Chunks cannot be None")
    
    if not isinstance(chunks, list):
        raise InvalidChunkError(f"Chunks must be a list, got {type(chunks).__name__}")
    
    if not chunks:
        return []
    
    for i, chunk in enumerate(chunks):
        if not isinstance(chunk, str):
            raise InvalidChunkError(
                f"Chunk at index {i} must be a string, got {type(chunk).__name__}"
            )
        if not chunk.strip():
            raise InvalidChunkError(f"Chunk at index {i} is empty or whitespace-only")
    
    try:
        model = _get_model()
        embeddings_array = model.encode(chunks, convert_to_numpy=True)
        embeddings_list = embeddings_array.tolist()
        return embeddings_list
        
    except (ModelLoadError, InvalidChunkError):
        raise
    except Exception as e:
        raise EmbeddingError(f"Failed to generate embeddings: {str(e)}") from e


def get_embedding_metadata(embeddings: List[List[float]]) -> dict:
    """
    Calculate metadata about the embeddings.
    
    Args:
        embeddings: List of embedding vectors.
        
    Returns:
        Dictionary containing embedding statistics.
    """
    if not embeddings:
        return {
            'total_embeddings': 0,
            'embedding_dimension': 0,
            'total_vectors': 0
        }
    
    return {
        'total_embeddings': len(embeddings),
        'embedding_dimension': len(embeddings[0]) if embeddings else 0,
        'total_vectors': len(embeddings)
    }
