"""Document chunking module for splitting text into overlapping segments."""

from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingError(Exception):
    """Base exception for chunking errors."""
    pass


class InvalidTextError(ChunkingError):
    """Raised when input text is invalid."""
    pass


def create_chunks(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[str]:
    """
    Split text into overlapping chunks for efficient retrieval.
    
    Args:
        text: Cleaned document text to be chunked.
        chunk_size: Maximum size of each chunk in characters (default: 1000).
        chunk_overlap: Number of overlapping characters between chunks (default: 200).
        
    Returns:
        List of text chunks in sequential order.
        
    Raises:
        InvalidTextError: If text is None or not a string.
        
    Examples:
        >>> text = "This is a long document that needs to be split..."
        >>> chunks = create_chunks(text)
        >>> len(chunks)
        5
    """
    if text is None:
        raise InvalidTextError("Text cannot be None")
    
    if not isinstance(text, str):
        raise InvalidTextError(f"Text must be a string, got {type(text).__name__}")
    
    if not text.strip():
        return []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_text(text)
    
    return chunks


def get_chunk_metadata(chunks: List[str]) -> dict:
    """
    Calculate metadata about the chunking results.
    
    Args:
        chunks: List of text chunks.
        
    Returns:
        Dictionary containing chunk statistics.
    """
    if not chunks:
        return {
            'total_chunks': 0,
            'total_characters': 0,
            'min_chunk_size': 0,
            'max_chunk_size': 0,
            'avg_chunk_size': 0.0
        }
    
    chunk_sizes = [len(chunk) for chunk in chunks]
    
    return {
        'total_chunks': len(chunks),
        'total_characters': sum(chunk_sizes),
        'min_chunk_size': min(chunk_sizes),
        'max_chunk_size': max(chunk_sizes),
        'avg_chunk_size': sum(chunk_sizes) / len(chunks)
    }
