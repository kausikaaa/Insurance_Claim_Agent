"""Comprehensive tests for embedding generation module."""

import pytest
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from embedding_generator import (
    generate_embeddings,
    get_embedding_metadata,
    InvalidChunkError,
    EmbeddingError,
    ModelLoadError
)


class TestBasicFunctionality:
    """Test basic embedding generation functionality."""
    
    def test_single_chunk_embedding(self):
        """Test embedding generation for a single chunk."""
        chunks = ["This is a test insurance policy document."]
        embeddings = generate_embeddings(chunks)
        
        assert isinstance(embeddings, list)
        assert len(embeddings) == 1
        assert isinstance(embeddings[0], list)
        assert len(embeddings[0]) == 384
        assert all(isinstance(val, float) for val in embeddings[0])
    
    def test_multiple_chunks_embedding(self):
        """Test embedding generation for multiple chunks."""
        chunks = [
            "Flood damage is covered under this policy.",
            "Hospitalization expenses are included.",
            "Premium payments are due monthly."
        ]
        embeddings = generate_embeddings(chunks)
        
        assert isinstance(embeddings, list)
        assert len(embeddings) == 3
        assert all(isinstance(emb, list) for emb in embeddings)
        assert all(len(emb) == 384 for emb in embeddings)
    
    def test_empty_list_returns_empty(self):
        """Test that empty list returns empty embeddings."""
        chunks = []
        embeddings = generate_embeddings(chunks)
        
        assert embeddings == []
        assert isinstance(embeddings, list)
    
    def test_none_input_raises_error(self):
        """Test that None input raises InvalidChunkError."""
        with pytest.raises(InvalidChunkError) as exc_info:
            generate_embeddings(None)
        assert "cannot be None" in str(exc_info.value)
    
    def test_invalid_type_raises_error(self):
        """Test that invalid input type raises InvalidChunkError."""
        with pytest.raises(InvalidChunkError):
            generate_embeddings("not a list")
        
        with pytest.raises(InvalidChunkError):
            generate_embeddings(123)
        
        with pytest.raises(InvalidChunkError):
            generate_embeddings({"key": "value"})
    
    def test_return_type_is_list(self):
        """Test that return type is always a list."""
        chunks = ["Some text here"]
        result = generate_embeddings(chunks)
        assert isinstance(result, list)


class TestInputValidation:
    """Test input validation and error handling."""
    
    def test_list_with_non_string_raises_error(self):
        """Test that list with non-string elements raises error."""
        with pytest.raises(InvalidChunkError) as exc_info:
            generate_embeddings([123, "valid string"])
        assert "must be a string" in str(exc_info.value)
    
    def test_list_with_empty_string_raises_error(self):
        """Test that list with empty string raises error."""
        with pytest.raises(InvalidChunkError) as exc_info:
            generate_embeddings([""])
        assert "empty or whitespace-only" in str(exc_info.value)
    
    def test_list_with_whitespace_only_raises_error(self):
        """Test that list with whitespace-only string raises error."""
        with pytest.raises(InvalidChunkError) as exc_info:
            generate_embeddings(["   "])
        assert "empty or whitespace-only" in str(exc_info.value)
    
    def test_mixed_valid_and_invalid_raises_error(self):
        """Test that mixed valid and invalid chunks raises error."""
        with pytest.raises(InvalidChunkError):
            generate_embeddings(["valid text", 123, "more valid text"])


class TestEmbeddingProperties:
    """Test properties of generated embeddings."""
    
    def test_embedding_dimension_is_384(self):
        """Test that all embeddings have dimension 384."""
        chunks = ["Text one", "Text two", "Text three"]
        embeddings = generate_embeddings(chunks)
        
        for embedding in embeddings:
            assert len(embedding) == 384
    
    def test_embeddings_are_floats(self):
        """Test that embedding values are floats."""
        chunks = ["Sample insurance policy text"]
        embeddings = generate_embeddings(chunks)
        
        for embedding in embeddings:
            assert all(isinstance(val, float) for val in embedding)
    
    def test_embeddings_are_non_zero(self):
        """Test that embeddings contain non-zero values."""
        chunks = ["Insurance coverage details"]
        embeddings = generate_embeddings(chunks)
        
        for embedding in embeddings:
            assert any(val != 0.0 for val in embedding)
    
    def test_embeddings_have_reasonable_magnitude(self):
        """Test that embedding values are in reasonable range."""
        chunks = ["Policy terms and conditions"]
        embeddings = generate_embeddings(chunks)
        
        for embedding in embeddings:
            for val in embedding:
                assert -10.0 <= val <= 10.0


class TestConsistency:
    """Test consistency of embedding generation."""
    
    def test_same_text_produces_identical_embeddings(self):
        """Test that same text produces identical embeddings."""
        text = "This is an insurance policy document"
        
        embeddings1 = generate_embeddings([text])
        embeddings2 = generate_embeddings([text])
        
        assert len(embeddings1) == len(embeddings2)
        assert len(embeddings1[0]) == len(embeddings2[0])
        
        for val1, val2 in zip(embeddings1[0], embeddings2[0]):
            assert abs(val1 - val2) < 1e-6
    
    def test_multiple_calls_use_cached_model(self):
        """Test that multiple calls don't reload the model."""
        chunks1 = ["First batch of text"]
        chunks2 = ["Second batch of text"]
        
        embeddings1 = generate_embeddings(chunks1)
        embeddings2 = generate_embeddings(chunks2)
        
        assert len(embeddings1) == 1
        assert len(embeddings2) == 1
        assert len(embeddings1[0]) == 384
        assert len(embeddings2[0]) == 384
    
    def test_order_preservation(self):
        """Test that embedding order matches input order."""
        chunks = ["First", "Second", "Third"]
        embeddings = generate_embeddings(chunks)
        
        assert len(embeddings) == len(chunks)
        
        for i, chunk in enumerate(chunks):
            single_embedding = generate_embeddings([chunk])
            for val1, val2 in zip(embeddings[i], single_embedding[0]):
                assert abs(val1 - val2) < 1e-6


class TestDifferentContent:
    """Test that different content produces different embeddings."""
    
    def test_different_texts_produce_different_embeddings(self):
        """Test that different texts produce different embeddings."""
        chunks = [
            "Flood damage is covered",
            "Fire damage is excluded"
        ]
        embeddings = generate_embeddings(chunks)
        
        similarity = sum(
            v1 * v2 for v1, v2 in zip(embeddings[0], embeddings[1])
        )
        
        assert embeddings[0] != embeddings[1]
        assert similarity < 1.0
    
    def test_semantically_similar_texts_have_high_similarity(self):
        """Test that semantically similar texts have similar embeddings."""
        chunks = [
            "The policy covers water damage",
            "Water damage is included in coverage"
        ]
        embeddings = generate_embeddings(chunks)
        
        def cosine_similarity(vec1, vec2):
            dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
            norm1 = sum(v * v for v in vec1) ** 0.5
            norm2 = sum(v * v for v in vec2) ** 0.5
            return dot_product / (norm1 * norm2)
        
        similarity = cosine_similarity(embeddings[0], embeddings[1])
        assert similarity > 0.5
    
    def test_dissimilar_texts_have_low_similarity(self):
        """Test that dissimilar texts have low similarity."""
        chunks = [
            "Insurance premium payment",
            "Quantum physics theories"
        ]
        embeddings = generate_embeddings(chunks)
        
        def cosine_similarity(vec1, vec2):
            dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
            norm1 = sum(v * v for v in vec1) ** 0.5
            norm2 = sum(v * v for v in vec2) ** 0.5
            return dot_product / (norm1 * norm2)
        
        similarity = cosine_similarity(embeddings[0], embeddings[1])
        assert similarity < 0.8


class TestLargeInput:
    """Test handling of large numbers of chunks."""
    
    def test_ten_chunks(self):
        """Test generation with 10 chunks."""
        chunks = [f"Insurance policy clause number {i}" for i in range(10)]
        embeddings = generate_embeddings(chunks)
        
        assert len(embeddings) == 10
        assert all(len(emb) == 384 for emb in embeddings)
    
    def test_hundred_chunks(self):
        """Test generation with 100 chunks."""
        chunks = [f"Policy section {i} describes coverage details" for i in range(100)]
        embeddings = generate_embeddings(chunks)
        
        assert len(embeddings) == 100
        assert all(len(emb) == 384 for emb in embeddings)
        assert all(isinstance(emb, list) for emb in embeddings)
    
    def test_large_batch_performance(self):
        """Test that large batches are handled efficiently."""
        chunks = [f"Document chunk {i}" for i in range(50)]
        embeddings = generate_embeddings(chunks)
        
        assert len(embeddings) == 50
        assert all(len(emb) == 384 for emb in embeddings)


class TestMetadata:
    """Test embedding metadata calculation."""
    
    def test_metadata_calculation(self):
        """Test that metadata is calculated correctly."""
        chunks = ["Text one", "Text two", "Text three"]
        embeddings = generate_embeddings(chunks)
        metadata = get_embedding_metadata(embeddings)
        
        assert metadata['total_embeddings'] == 3
        assert metadata['embedding_dimension'] == 384
        assert metadata['total_vectors'] == 3
    
    def test_empty_embeddings_metadata(self):
        """Test metadata for empty embeddings list."""
        metadata = get_embedding_metadata([])
        
        assert metadata['total_embeddings'] == 0
        assert metadata['embedding_dimension'] == 0
        assert metadata['total_vectors'] == 0
    
    def test_single_embedding_metadata(self):
        """Test metadata for single embedding."""
        chunks = ["Single chunk"]
        embeddings = generate_embeddings(chunks)
        metadata = get_embedding_metadata(embeddings)
        
        assert metadata['total_embeddings'] == 1
        assert metadata['embedding_dimension'] == 384
        assert metadata['total_vectors'] == 1
    
    def test_metadata_return_type(self):
        """Test that metadata returns a dictionary."""
        chunks = ["Sample text"]
        embeddings = generate_embeddings(chunks)
        metadata = get_embedding_metadata(embeddings)
        
        assert isinstance(metadata, dict)
        assert 'total_embeddings' in metadata
        assert 'embedding_dimension' in metadata
        assert 'total_vectors' in metadata


class TestIntegrationWithPipeline:
    """Test integration with existing pipeline components."""
    
    def test_embeddings_after_chunking(self):
        """Test generating embeddings from chunked text."""
        from chunker import create_chunks
        
        text = """Insurance Policy Document
        
        Section 1: Coverage Information
        This policy provides comprehensive coverage for property damage.
        
        Section 2: Terms and Conditions
        All claims must be filed within 30 days of the incident.
        """ * 3
        
        chunks = create_chunks(text, chunk_size=200, chunk_overlap=50)
        embeddings = generate_embeddings(chunks)
        
        assert len(embeddings) == len(chunks)
        assert all(len(emb) == 384 for emb in embeddings)
    
    def test_complete_pipeline_pdf_to_embeddings(self):
        """Test complete pipeline from PDF to embeddings."""
        from pdf_loader import load_pdf
        from text_cleaner import clean_text
        from chunker import create_chunks
        from pdf_generator import generate_all_test_pdfs
        
        pdf_dir = Path(__file__).parent / "sample_pdfs"
        generate_all_test_pdfs(str(pdf_dir))
        
        pdf_path = str(pdf_dir / "single_page.pdf")
        
        raw_text = load_pdf(pdf_path)
        cleaned_text = clean_text(raw_text)
        chunks = create_chunks(cleaned_text, chunk_size=500, chunk_overlap=100)
        
        if chunks:
            embeddings = generate_embeddings(chunks)
            
            assert len(embeddings) == len(chunks)
            assert all(len(emb) == 384 for emb in embeddings)
            assert all(isinstance(emb, list) for emb in embeddings)
    
    def test_realistic_insurance_document_embedding(self):
        """Test embedding generation for realistic insurance content."""
        chunks = [
            "Policy Number: INS-2024-001234. Coverage Type: Comprehensive.",
            "Premium: $1,200 annually. Deductible: $500 per claim.",
            "This policy covers fire, theft, and natural disasters.",
            "Exclusions: War, nuclear events, intentional damage."
        ]
        
        embeddings = generate_embeddings(chunks)
        
        assert len(embeddings) == 4
        assert all(len(emb) == 384 for emb in embeddings)
        
        for i in range(len(embeddings) - 1):
            assert embeddings[i] != embeddings[i + 1]


class TestReturnTypes:
    """Test return type validation."""
    
    def test_return_type_always_list(self):
        """Test that return type is always a list."""
        assert isinstance(generate_embeddings([]), list)
        
        chunks = ["text"]
        assert isinstance(generate_embeddings(chunks), list)
    
    def test_embeddings_are_lists_of_floats(self):
        """Test that embeddings are lists of floats."""
        chunks = ["Sample text for embedding"]
        embeddings = generate_embeddings(chunks)
        
        assert isinstance(embeddings, list)
        assert all(isinstance(emb, list) for emb in embeddings)
        assert all(isinstance(val, float) for emb in embeddings for val in emb)
    
    def test_metadata_return_type_is_dict(self):
        """Test that metadata returns a dictionary."""
        chunks = ["Test"]
        embeddings = generate_embeddings(chunks)
        metadata = get_embedding_metadata(embeddings)
        
        assert isinstance(metadata, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
