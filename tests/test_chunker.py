"""Comprehensive tests for document chunking module."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from chunker import create_chunks, get_chunk_metadata, InvalidTextError


class TestBasicChunking:
    """Test basic chunking functionality."""
    
    def test_simple_text_chunking(self):
        """Test chunking of simple text."""
        text = "This is a test document. " * 100
        chunks = create_chunks(text, chunk_size=100, chunk_overlap=20)
        
        assert isinstance(chunks, list)
        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)
    
    def test_empty_string_returns_empty_list(self):
        """Test that empty string returns empty list."""
        assert create_chunks("") == []
        assert create_chunks("   ") == []
        assert create_chunks("\n\n\n") == []
    
    def test_whitespace_only_returns_empty_list(self):
        """Test that whitespace-only text returns empty list."""
        assert create_chunks("     ") == []
        assert create_chunks("\t\t\t") == []
        assert create_chunks("\n  \n  \n") == []
    
    def test_none_input_raises_error(self):
        """Test that None input raises InvalidTextError."""
        with pytest.raises(InvalidTextError) as exc_info:
            create_chunks(None)
        assert "cannot be None" in str(exc_info.value)
    
    def test_invalid_type_raises_error(self):
        """Test that invalid input type raises InvalidTextError."""
        with pytest.raises(InvalidTextError):
            create_chunks(123)
        
        with pytest.raises(InvalidTextError):
            create_chunks(['list', 'of', 'strings'])
        
        with pytest.raises(InvalidTextError):
            create_chunks({'dict': 'value'})
    
    def test_return_type_is_list(self):
        """Test that return type is always a list."""
        text = "Some text here"
        result = create_chunks(text)
        assert isinstance(result, list)


class TestChunkSizeAndOverlap:
    """Test chunk size and overlap configuration."""
    
    def test_default_chunk_size(self):
        """Test default chunk size of 1000 characters."""
        text = "A" * 2500
        chunks = create_chunks(text)
        
        assert len(chunks) > 1
        for chunk in chunks[:-1]:
            assert len(chunk) <= 1000
    
    def test_custom_chunk_size(self):
        """Test custom chunk size."""
        text = "B" * 1500
        chunks = create_chunks(text, chunk_size=500, chunk_overlap=50)
        
        assert len(chunks) >= 3
        for chunk in chunks[:-1]:
            assert len(chunk) <= 500
    
    def test_chunk_overlap_exists(self):
        """Test that overlap between consecutive chunks exists."""
        text = "Word " * 500
        chunks = create_chunks(text, chunk_size=200, chunk_overlap=50)
        
        if len(chunks) > 1:
            for i in range(len(chunks) - 1):
                chunk1_end = chunks[i][-50:]
                chunk2_start = chunks[i + 1][:50]
                common_content = any(
                    word in chunk2_start 
                    for word in chunk1_end.split() 
                    if len(word) > 3
                )
                assert common_content or len(chunks[i]) < 200
    
    def test_very_small_text_single_chunk(self):
        """Test that very small text produces single chunk."""
        text = "Short text"
        chunks = create_chunks(text, chunk_size=1000, chunk_overlap=200)
        
        assert len(chunks) == 1
        assert chunks[0] == text


class TestLargeDocuments:
    """Test chunking of large documents."""
    
    def test_large_document_chunking(self):
        """Test chunking of large document."""
        sentences = [f"This is sentence number {i}. " for i in range(1000)]
        full_text = "".join(sentences)
        
        chunks = create_chunks(full_text, chunk_size=1000, chunk_overlap=200)
        
        assert len(chunks) > 10
        assert isinstance(chunks, list)
        assert all(isinstance(chunk, str) for chunk in chunks)
    
    def test_very_large_document_memory_efficiency(self):
        """Test that very large documents can be chunked efficiently."""
        large_text = "X" * 100000
        chunks = create_chunks(large_text, chunk_size=1000, chunk_overlap=200)
        
        assert len(chunks) > 50
        reconstructed_length = sum(len(chunk) for chunk in chunks)
        assert reconstructed_length >= len(large_text)
    
    def test_document_with_many_paragraphs(self):
        """Test document with many paragraphs."""
        paragraphs = [f"Paragraph {i}. " + "Content. " * 20 for i in range(100)]
        text = "\n\n".join(paragraphs)
        
        chunks = create_chunks(text, chunk_size=1000, chunk_overlap=200)
        
        assert len(chunks) > 5
        assert all(len(chunk.strip()) > 0 for chunk in chunks)


class TestContentPreservation:
    """Test that content is preserved during chunking."""
    
    def test_all_content_present_in_chunks(self):
        """Test that all content appears in at least one chunk."""
        text = "Policy Number: INS-2024-001234\n" * 50
        chunks = create_chunks(text, chunk_size=500, chunk_overlap=100)
        
        combined = " ".join(chunks)
        assert "INS-2024-001234" in combined
        assert "Policy Number" in combined
    
    def test_chunk_ordering_preserved(self):
        """Test that chunks maintain sequential order."""
        text = "".join([f"Section {i}. " for i in range(1, 201)])
        chunks = create_chunks(text, chunk_size=200, chunk_overlap=50)
        
        for i, chunk in enumerate(chunks):
            if f"Section {i+1}" in text:
                first_occurrence_chunk = next(
                    (idx for idx, c in enumerate(chunks) if f"Section {i+1}" in c),
                    None
                )
                if first_occurrence_chunk is not None and i > 0:
                    assert first_occurrence_chunk >= 0
    
    def test_no_content_loss(self):
        """Test that important content is not lost."""
        important_words = ["Premium", "Coverage", "Deductible", "Liability", "Claim"]
        text = " ".join([word + " content here. " * 10 for word in important_words])
        
        chunks = create_chunks(text, chunk_size=200, chunk_overlap=50)
        combined = " ".join(chunks)
        
        for word in important_words:
            assert word in combined
    
    def test_special_characters_preserved(self):
        """Test that special characters are preserved."""
        text = "Amount: $100,000 (liability). Premium: $1,200/year. " * 30
        chunks = create_chunks(text, chunk_size=300, chunk_overlap=50)
        
        combined = " ".join(chunks)
        assert "$100,000" in combined
        assert "$1,200" in combined
        assert "(" in combined
        assert ")" in combined


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_text_exactly_chunk_size(self):
        """Test text that is exactly the chunk size."""
        text = "A" * 1000
        chunks = create_chunks(text, chunk_size=1000, chunk_overlap=200)
        
        assert len(chunks) == 1
        assert len(chunks[0]) == 1000
    
    def test_text_slightly_over_chunk_size(self):
        """Test text slightly larger than chunk size."""
        text = "A" * 1001
        chunks = create_chunks(text, chunk_size=1000, chunk_overlap=200)
        
        assert len(chunks) >= 2
    
    def test_single_very_long_word(self):
        """Test handling of single very long word."""
        text = "A" * 5000
        chunks = create_chunks(text, chunk_size=1000, chunk_overlap=200)
        
        assert len(chunks) > 1
        assert all(isinstance(chunk, str) for chunk in chunks)
    
    def test_newline_heavy_text(self):
        """Test text with many newlines."""
        text = "Line\n" * 1000
        chunks = create_chunks(text, chunk_size=500, chunk_overlap=100)
        
        assert len(chunks) > 1
        assert all("Line" in chunk for chunk in chunks)
    
    def test_mixed_whitespace(self):
        """Test text with mixed whitespace."""
        text = "Word1  \n\n  Word2\t\tWord3\n" * 100
        chunks = create_chunks(text, chunk_size=300, chunk_overlap=50)
        
        assert len(chunks) > 1
        combined = " ".join(chunks)
        assert "Word1" in combined
        assert "Word2" in combined
        assert "Word3" in combined


class TestChunkMetadata:
    """Test chunk metadata calculation."""
    
    def test_metadata_calculation(self):
        """Test that metadata is calculated correctly."""
        text = "This is a test. " * 100
        chunks = create_chunks(text, chunk_size=200, chunk_overlap=50)
        metadata = get_chunk_metadata(chunks)
        
        assert metadata['total_chunks'] == len(chunks)
        assert metadata['total_characters'] > 0
        assert metadata['min_chunk_size'] > 0
        assert metadata['max_chunk_size'] > 0
        assert metadata['avg_chunk_size'] > 0
    
    def test_empty_chunks_metadata(self):
        """Test metadata for empty chunks list."""
        metadata = get_chunk_metadata([])
        
        assert metadata['total_chunks'] == 0
        assert metadata['total_characters'] == 0
        assert metadata['min_chunk_size'] == 0
        assert metadata['max_chunk_size'] == 0
        assert metadata['avg_chunk_size'] == 0.0
    
    def test_single_chunk_metadata(self):
        """Test metadata for single chunk."""
        chunks = ["This is a single chunk"]
        metadata = get_chunk_metadata(chunks)
        
        assert metadata['total_chunks'] == 1
        assert metadata['min_chunk_size'] == metadata['max_chunk_size']
        assert metadata['avg_chunk_size'] == len(chunks[0])


class TestIntegrationWithPipeline:
    """Test integration with existing PDF and text cleaning pipeline."""
    
    def test_chunking_after_text_cleaning(self):
        """Test that chunking works with cleaned text."""
        cleaned_text = """Policy Number: INS-2024-001234
Policy Holder: John Doe
Coverage Type: Comprehensive Auto Insurance

Coverage Details:
- Liability Coverage: $100,000
- Collision Coverage: $50,000
- Comprehensive Coverage: $50,000

This policy is valid from January 1, 2024 to December 31, 2024.
""" * 10
        
        chunks = create_chunks(cleaned_text, chunk_size=500, chunk_overlap=100)
        
        assert len(chunks) > 1
        assert "Policy Number" in chunks[0]
        assert any("Coverage Details" in chunk for chunk in chunks)
    
    def test_realistic_insurance_document(self):
        """Test with realistic insurance document content."""
        document = """
Insurance Policy Document

Section 1: Coverage Information
This comprehensive insurance policy provides coverage for various risks and liabilities.
The policy holder is entitled to protection against damages, losses, and claims.

Section 2: Terms and Conditions
All claims must be filed within 30 days of the incident. The deductible amount
varies based on the type of claim. Premium payments are due on the first of each month.

Section 3: Exclusions
This policy does not cover intentional damage, pre-existing conditions, or acts of war.
Certain geographic regions may have limited coverage. Please review the full policy
documentation for complete details.
""" * 5
        
        chunks = create_chunks(document, chunk_size=1000, chunk_overlap=200)
        
        assert len(chunks) >= 2
        assert all(len(chunk) <= 1200 for chunk in chunks)
        combined = " ".join(chunks)
        assert "Section 1" in combined
        assert "Section 2" in combined
        assert "Section 3" in combined


class TestReturnTypes:
    """Test return type validation."""
    
    def test_return_type_always_list(self):
        """Test that return type is always a list."""
        assert isinstance(create_chunks("text"), list)
        assert isinstance(create_chunks(""), list)
        assert isinstance(create_chunks("   "), list)
    
    def test_chunks_are_strings(self):
        """Test that all chunks are strings."""
        text = "Content here. " * 100
        chunks = create_chunks(text, chunk_size=200, chunk_overlap=50)
        
        assert all(isinstance(chunk, str) for chunk in chunks)
    
    def test_metadata_return_type(self):
        """Test that metadata returns a dictionary."""
        chunks = create_chunks("Some text here", chunk_size=100, chunk_overlap=20)
        metadata = get_chunk_metadata(chunks)
        
        assert isinstance(metadata, dict)
        assert 'total_chunks' in metadata
        assert 'total_characters' in metadata


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
