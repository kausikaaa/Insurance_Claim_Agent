"""FAISS vector store module for searchable knowledge base creation."""

import os
import pickle
from pathlib import Path
from typing import List, Tuple, Optional, Union
import numpy as np
import faiss


class VectorStoreError(Exception):
    """Base exception for vector store errors."""
    pass


class InvalidEmbeddingError(VectorStoreError):
    """Raised when embeddings are invalid."""
    pass


class IndexSaveError(VectorStoreError):
    """Raised when index fails to save."""
    pass


class IndexLoadError(VectorStoreError):
    """Raised when index fails to load."""
    pass


class FAISSVectorStore:
    """
    FAISS-based vector store for semantic search.
    
    Attributes:
        index: FAISS index for similarity search.
        chunks: List of text chunks corresponding to embeddings.
        dimension: Dimensionality of embeddings (384 for all-MiniLM-L6-v2).
    """
    
    def __init__(self, index: faiss.Index, chunks: List[str], dimension: int):
        """
        Initialize FAISS vector store.
        
        Args:
            index: FAISS index.
            chunks: List of text chunks.
            dimension: Embedding dimension.
        """
        self.index = index
        self.chunks = chunks
        self.dimension = dimension
    
    def similarity_search(
        self, 
        query: Union[str, List[float]], 
        top_k: int = 5
    ) -> List[str]:
        """
        Search for most similar chunks using query text or embedding.
        
        Args:
            query: Natural language query string OR precomputed embedding vector.
            top_k: Number of results to return (default: 5).
            
        Returns:
            List of most similar chunks in ranked order.
            
        Raises:
            InvalidEmbeddingError: If query is invalid.
            
        Examples:
            >>> # Using text query
            >>> results = store.similarity_search("flood damage", top_k=5)
            >>> # Using precomputed embedding
            >>> results = store.similarity_search([0.1, 0.2, ...], top_k=5)
        """
        if query is None:
            raise InvalidEmbeddingError("Query cannot be None")
        
        # Handle string query - generate embedding internally
        if isinstance(query, str):
            if not query.strip():
                raise InvalidEmbeddingError("Query string cannot be empty")
            
            try:
                from embedding_generator import generate_embeddings
                query_embedding = generate_embeddings([query])[0]
            except Exception as e:
                raise InvalidEmbeddingError(f"Failed to generate query embedding: {str(e)}")
        
        # Handle list/array query - use directly
        elif isinstance(query, (list, np.ndarray)):
            query_embedding = query
        
        else:
            raise InvalidEmbeddingError(
                f"Query must be string, list, or array, got {type(query).__name__}"
            )
        
        # Convert to numpy array for FAISS
        query_array = np.array([query_embedding], dtype=np.float32)
        
        if query_array.shape[1] != self.dimension:
            raise InvalidEmbeddingError(
                f"Query embedding dimension {query_array.shape[1]} does not match "
                f"index dimension {self.dimension}"
            )
        
        top_k = min(top_k, len(self.chunks))
        
        if top_k == 0:
            return []
        
        distances, indices = self.index.search(query_array, top_k)
        
        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.chunks):
                results.append(self.chunks[idx])
        
        return results


def build_faiss(chunks: List[str], embeddings: List[List[float]]) -> FAISSVectorStore:
    """
    Build FAISS vector store from chunks and embeddings.
    
    Args:
        chunks: List of text chunks.
        embeddings: List of embedding vectors corresponding to chunks.
        
    Returns:
        FAISSVectorStore object with searchable index.
        
    Raises:
        InvalidEmbeddingError: If inputs are invalid or mismatched.
        VectorStoreError: If index creation fails.
        
    Examples:
        >>> chunks = ["Text 1", "Text 2"]
        >>> embeddings = [[0.1, 0.2, ...], [0.3, 0.4, ...]]
        >>> store = build_faiss(chunks, embeddings)
        >>> results = store.similarity_search(query_emb, top_k=5)
    """
    if chunks is None:
        raise InvalidEmbeddingError("Chunks cannot be None")
    
    if embeddings is None:
        raise InvalidEmbeddingError("Embeddings cannot be None")
    
    if not isinstance(chunks, list):
        raise InvalidEmbeddingError(f"Chunks must be a list, got {type(chunks).__name__}")
    
    if not isinstance(embeddings, list):
        raise InvalidEmbeddingError(f"Embeddings must be a list, got {type(embeddings).__name__}")
    
    if len(chunks) == 0 and len(embeddings) == 0:
        raise InvalidEmbeddingError("Cannot build index with empty chunks and embeddings")
    
    if len(chunks) != len(embeddings):
        raise InvalidEmbeddingError(
            f"Chunk count ({len(chunks)}) does not match embedding count ({len(embeddings)})"
        )
    
    for i, chunk in enumerate(chunks):
        if not isinstance(chunk, str):
            raise InvalidEmbeddingError(
                f"Chunk at index {i} must be a string, got {type(chunk).__name__}"
            )
        if not chunk.strip():
            raise InvalidEmbeddingError(f"Chunk at index {i} is empty or whitespace-only")
    
    if len(embeddings) == 0:
        raise InvalidEmbeddingError("Cannot build index with empty embeddings")
    
    dimension = len(embeddings[0])
    
    for i, emb in enumerate(embeddings):
        if not isinstance(emb, (list, np.ndarray)):
            raise InvalidEmbeddingError(
                f"Embedding at index {i} must be list or array, got {type(emb).__name__}"
            )
        if len(emb) != dimension:
            raise InvalidEmbeddingError(
                f"Embedding at index {i} has dimension {len(emb)}, expected {dimension}"
            )
    
    try:
        embeddings_array = np.array(embeddings, dtype=np.float32)
        
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings_array)
        
        return FAISSVectorStore(index, chunks, dimension)
        
    except Exception as e:
        raise VectorStoreError(f"Failed to build FAISS index: {str(e)}") from e


def save_index(vectorstore: FAISSVectorStore, directory: str = "vector_store") -> None:
    """
    Save FAISS index and chunks to disk.
    
    Args:
        vectorstore: FAISSVectorStore object to save.
        directory: Directory path to save index (default: "vector_store").
        
    Raises:
        IndexSaveError: If save operation fails.
        
    Examples:
        >>> store = build_faiss(chunks, embeddings)
        >>> save_index(store, "vector_store")
    """
    if vectorstore is None:
        raise IndexSaveError("VectorStore cannot be None")
    
    if not isinstance(vectorstore, FAISSVectorStore):
        raise IndexSaveError(
            f"VectorStore must be FAISSVectorStore, got {type(vectorstore).__name__}"
        )
    
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        index_path = os.path.join(directory, "faiss_index")
        chunks_path = os.path.join(directory, "chunks.pkl")
        
        faiss.write_index(vectorstore.index, index_path)
        
        with open(chunks_path, 'wb') as f:
            pickle.dump({
                'chunks': vectorstore.chunks,
                'dimension': vectorstore.dimension
            }, f)
        
    except Exception as e:
        raise IndexSaveError(f"Failed to save index: {str(e)}") from e


def load_index(directory: str = "vector_store") -> FAISSVectorStore:
    """
    Load FAISS index and chunks from disk.
    
    Args:
        directory: Directory path containing saved index (default: "vector_store").
        
    Returns:
        FAISSVectorStore object with restored index and chunks.
        
    Raises:
        IndexLoadError: If load operation fails.
        
    Examples:
        >>> store = load_index("vector_store")
        >>> results = store.similarity_search(query_emb, top_k=5)
    """
    if not os.path.exists(directory):
        raise IndexLoadError(f"Directory does not exist: {directory}")
    
    index_path = os.path.join(directory, "faiss_index")
    chunks_path = os.path.join(directory, "chunks.pkl")
    
    if not os.path.exists(index_path):
        raise IndexLoadError(f"FAISS index file not found: {index_path}")
    
    if not os.path.exists(chunks_path):
        raise IndexLoadError(f"Chunks file not found: {chunks_path}")
    
    try:
        index = faiss.read_index(index_path)
        
        with open(chunks_path, 'rb') as f:
            data = pickle.load(f)
            chunks = data['chunks']
            dimension = data['dimension']
        
        return FAISSVectorStore(index, chunks, dimension)
        
    except Exception as e:
        raise IndexLoadError(f"Failed to load index: {str(e)}") from e


def get_index_metadata(vectorstore: FAISSVectorStore) -> dict:
    """
    Get metadata about the FAISS index.
    
    Args:
        vectorstore: FAISSVectorStore object.
        
    Returns:
        Dictionary containing index statistics.
    """
    if vectorstore is None:
        return {
            'total_chunks': 0,
            'embedding_dimension': 0,
            'index_size': 0
        }
    
    return {
        'total_chunks': len(vectorstore.chunks),
        'embedding_dimension': vectorstore.dimension,
        'index_size': vectorstore.index.ntotal
    }
