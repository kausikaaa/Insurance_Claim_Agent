"""Comprehensive tests for FAISS vector store module."""

import pytest
import sys
import os
import shutil
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from faiss_store import (
    build_faiss,
    save_index,
    load_index,
    get_index_metadata,
    FAISSVectorStore,
    InvalidEmbeddingError,
    IndexSaveError,
    IndexLoadError,
    VectorStoreError
)
from embedding_generator import generate_embeddings


class TestBasicFunctionality:
    """Test basic FAISS functionality."""
    
    def test_build_simple_index(self):
        """Test building a simple FAISS index."""
        chunks = ["This is a test", "Another test chunk"]
        embeddings = [[0.1] * 384, [0.2] * 384]
        
        store = build_faiss(chunks, embeddings)
        
        assert isinstance(store, FAISSVectorStore)
        assert len(store.chunks) == 2
        assert store.dimension == 384
    
    def test_search_returns_results(self):
        """Test that search returns results."""
        chunks = ["Flood damage coverage", "Fire insurance policy"]
        embeddings = [[0.1] * 384, [0.9] * 384]
        
        store = build_faiss(chunks, embeddings)
        query_emb = [0.1] * 384
        
        results = store.similarity_search(query_emb, top_k=1)
        
        assert len(results) == 1
        assert isinstance(results[0], str)
    
    def test_search_returns_correct_order(self):
        """Test that search returns results in ranked order."""
        chunks = ["Text A", "Text B", "Text C"]
        embeddings = [[0.1] * 384, [0.5] * 384, [0.9] * 384]
        
        store = build_faiss(chunks, embeddings)
        query_emb = [0.1] * 384
        
        results = store.similarity_search(query_emb, top_k=3)
        
        assert len(results) == 3
        assert results[0] == "Text A"


class TestInputValidation:
    """Test input validation and error handling."""
    
    def test_none_chunks_raises_error(self):
        """Test that None chunks raises error."""
        with pytest.raises(InvalidEmbeddingError) as exc_info:
            build_faiss(None, [[0.1] * 384])
        assert "cannot be none" in str(exc_info.value).lower()
    
    def test_none_embeddings_raises_error(self):
        """Test that None embeddings raises error."""
        with pytest.raises(InvalidEmbeddingError) as exc_info:
            build_faiss(["chunk"], None)
        assert "cannot be none" in str(exc_info.value).lower()
    
    def test_empty_chunks_and_embeddings_raises_error(self):
        """Test that empty chunks and embeddings raises error."""
        with pytest.raises(InvalidEmbeddingError) as exc_info:
            build_faiss([], [])
        assert "empty" in str(exc_info.value).lower()
    
    def test_mismatched_lengths_raises_error(self):
        """Test that mismatched chunk and embedding counts raises error."""
        chunks = ["chunk1", "chunk2"]
        embeddings = [[0.1] * 384]
        
        with pytest.raises(InvalidEmbeddingError) as exc_info:
            build_faiss(chunks, embeddings)
        assert "does not match" in str(exc_info.value).lower()
    
    def test_invalid_embedding_dimension_raises_error(self):
        """Test that inconsistent embedding dimensions raises error."""
        chunks = ["chunk1", "chunk2"]
        embeddings = [[0.1] * 384, [0.2] * 128]
        
        with pytest.raises(InvalidEmbeddingError) as exc_info:
            build_faiss(chunks, embeddings)
        assert "dimension" in str(exc_info.value).lower()
    
    def test_non_string_chunk_raises_error(self):
        """Test that non-string chunks raise error."""
        chunks = ["valid", 123]
        embeddings = [[0.1] * 384, [0.2] * 384]
        
        with pytest.raises(InvalidEmbeddingError) as exc_info:
            build_faiss(chunks, embeddings)
        assert "must be a string" in str(exc_info.value).lower()
    
    def test_empty_chunk_raises_error(self):
        """Test that empty chunks raise error."""
        chunks = ["valid", ""]
        embeddings = [[0.1] * 384, [0.2] * 384]
        
        with pytest.raises(InvalidEmbeddingError) as exc_info:
            build_faiss(chunks, embeddings)
        assert "empty" in str(exc_info.value).lower()


class TestPersistence:
    """Test save and load functionality."""
    
    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create temporary directory for tests."""
        test_dir = tmp_path / "test_vector_store"
        yield str(test_dir)
        if test_dir.exists():
            shutil.rmtree(test_dir)
    
    def test_save_index(self, temp_dir):
        """Test saving index to disk."""
        chunks = ["Test chunk 1", "Test chunk 2"]
        embeddings = [[0.1] * 384, [0.2] * 384]
        
        store = build_faiss(chunks, embeddings)
        save_index(store, temp_dir)
        
        assert os.path.exists(os.path.join(temp_dir, "faiss_index"))
        assert os.path.exists(os.path.join(temp_dir, "chunks.pkl"))
    
    def test_load_index(self, temp_dir):
        """Test loading index from disk."""
        chunks = ["Test chunk 1", "Test chunk 2"]
        embeddings = [[0.1] * 384, [0.2] * 384]
        
        store = build_faiss(chunks, embeddings)
        save_index(store, temp_dir)
        
        loaded_store = load_index(temp_dir)
        
        assert isinstance(loaded_store, FAISSVectorStore)
        assert len(loaded_store.chunks) == 2
        assert loaded_store.dimension == 384
    
    def test_search_after_load(self, temp_dir):
        """Test that search still works after load."""
        chunks = ["Flood coverage", "Fire insurance"]
        embeddings = [[0.1] * 384, [0.9] * 384]
        
        store = build_faiss(chunks, embeddings)
        save_index(store, temp_dir)
        
        loaded_store = load_index(temp_dir)
        query_emb = [0.1] * 384
        results = loaded_store.similarity_search(query_emb, top_k=1)
        
        assert len(results) == 1
        assert "Flood" in results[0]
    
    def test_load_nonexistent_directory_raises_error(self):
        """Test that loading from nonexistent directory raises error."""
        with pytest.raises(IndexLoadError) as exc_info:
            load_index("nonexistent_directory_xyz")
        assert "does not exist" in str(exc_info.value).lower()
    
    def test_save_none_vectorstore_raises_error(self, temp_dir):
        """Test that saving None vectorstore raises error."""
        with pytest.raises(IndexSaveError):
            save_index(None, temp_dir)


class TestChunkMapping:
    """Test chunk mapping and retrieval."""
    
    def test_correct_chunk_retrieval(self):
        """Test that correct chunks are retrieved."""
        chunks = [
            "Flood damage is covered",
            "Fire damage excluded",
            "Medical expenses included"
        ]
        embeddings = [[0.1] * 384, [0.5] * 384, [0.9] * 384]
        
        store = build_faiss(chunks, embeddings)
        query_emb = [0.9] * 384
        
        results = store.similarity_search(query_emb, top_k=1)
        
        assert results[0] == "Medical expenses included"
    
    def test_order_preserved(self):
        """Test that chunk order is preserved."""
        chunks = [f"Chunk {i}" for i in range(10)]
        embeddings = [[float(i) / 10] * 384 for i in range(10)]
        
        store = build_faiss(chunks, embeddings)
        
        assert store.chunks == chunks
    
    def test_chunk_mapping_survives_save_load(self, tmp_path):
        """Test that chunk mapping survives save/load."""
        test_dir = str(tmp_path / "test_store")
        
        chunks = ["First", "Second", "Third"]
        embeddings = [[0.1] * 384, [0.5] * 384, [0.9] * 384]
        
        store = build_faiss(chunks, embeddings)
        save_index(store, test_dir)
        
        loaded_store = load_index(test_dir)
        query_emb = [0.5] * 384
        results = loaded_store.similarity_search(query_emb, top_k=1)
        
        assert "Second" in results[0]
        
        shutil.rmtree(test_dir)


class TestSimilaritySearch:
    """Test similarity search functionality."""
    
    def test_string_query_works(self):
        """Test that string query works directly."""
        from embedding_generator import generate_embeddings
        
        chunks = [
            "This policy covers flood damage to your property",
            "Medical expenses for hospitalization are included",
            "Fire insurance coverage details"
        ]
        
        embeddings = generate_embeddings(chunks)
        store = build_faiss(chunks, embeddings)
        
        results = store.similarity_search("flood damage", top_k=1)
        
        assert len(results) == 1
        assert "flood" in results[0].lower()
    
    def test_embedding_query_still_works(self):
        """Test backward compatibility with embedding queries."""
        from embedding_generator import generate_embeddings
        
        chunks = [
            "Flood damage is covered under this policy",
            "Hospital bills and medical treatment costs are reimbursed"
        ]
        
        embeddings = generate_embeddings(chunks)
        store = build_faiss(chunks, embeddings)
        
        query_emb = generate_embeddings(["flood coverage"])[0]
        results = store.similarity_search(query_emb, top_k=1)
        
        assert len(results) == 1
        assert "flood" in results[0].lower()
    
    def test_flood_query_returns_flood_chunk(self):
        """Test that flood query returns flood-related chunk."""
        from embedding_generator import generate_embeddings
        
        chunks = [
            "This policy covers flood damage to your property",
            "Medical expenses for hospitalization are included",
            "Fire insurance coverage details"
        ]
        
        embeddings = generate_embeddings(chunks)
        store = build_faiss(chunks, embeddings)
        
        results = store.similarity_search("flood damage coverage", top_k=1)
        
        assert "flood" in results[0].lower()
    
    def test_medical_query_returns_medical_chunk(self):
        """Test that medical query returns medical-related chunk."""
        from embedding_generator import generate_embeddings
        
        chunks = [
            "Flood damage is covered under this policy",
            "Hospital bills and medical treatment costs are reimbursed",
            "Fire damage exclusions apply"
        ]
        
        embeddings = generate_embeddings(chunks)
        store = build_faiss(chunks, embeddings)
        
        results = store.similarity_search("hospitalization medical expenses", top_k=1)
        
        assert "medical" in results[0].lower() or "hospital" in results[0].lower()
    
    def test_top_k_limits_results(self):
        """Test that top_k parameter limits results."""
        chunks = [f"Chunk {i}" for i in range(10)]
        embeddings = [[float(i)] * 384 for i in range(10)]
        
        store = build_faiss(chunks, embeddings)
        results = store.similarity_search("test query", top_k=3)
        
        assert len(results) == 3
    
    def test_none_query_raises_error(self):
        """Test that None query raises error."""
        chunks = ["Test"]
        embeddings = [[0.1] * 384]
        
        store = build_faiss(chunks, embeddings)
        
        with pytest.raises(InvalidEmbeddingError):
            store.similarity_search(None)
    
    def test_empty_string_query_raises_error(self):
        """Test that empty string query raises error."""
        chunks = ["Test"]
        embeddings = [[0.1] * 384]
        
        store = build_faiss(chunks, embeddings)
        
        with pytest.raises(InvalidEmbeddingError) as exc_info:
            store.similarity_search("")
        assert "empty" in str(exc_info.value).lower()
    
    def test_wrong_dimension_query_raises_error(self):
        """Test that wrong dimension query raises error."""
        chunks = ["Test"]
        embeddings = [[0.1] * 384]
        
        store = build_faiss(chunks, embeddings)
        query_emb = [0.1] * 128
        
        with pytest.raises(InvalidEmbeddingError) as exc_info:
            store.similarity_search(query_emb)
        assert "dimension" in str(exc_info.value).lower()


class TestLargeDataset:
    """Test handling of large datasets."""
    
    def test_hundred_chunks(self):
        """Test building index with 100+ chunks."""
        chunks = [f"Insurance policy clause {i}" for i in range(150)]
        embeddings = [[float(i % 10) / 10] * 384 for i in range(150)]
        
        store = build_faiss(chunks, embeddings)
        
        assert len(store.chunks) == 150
        assert store.index.ntotal == 150
    
    def test_search_large_dataset(self):
        """Test search on large dataset."""
        chunks = [f"Document section {i}" for i in range(100)]
        embeddings = [[float(i % 10) / 10] * 384 for i in range(100)]
        
        store = build_faiss(chunks, embeddings)
        query_emb = [0.5] * 384
        
        results = store.similarity_search(query_emb, top_k=10)
        
        assert len(results) == 10
        assert all(isinstance(r, str) for r in results)


class TestIntegrationWithPipeline:
    """Test integration with complete pipeline."""
    
    def test_full_pipeline_pdf_to_faiss(self):
        """Test complete pipeline from PDF to FAISS."""
        from pdf_loader import load_pdf
        from text_cleaner import clean_text
        from chunker import create_chunks
        from embedding_generator import generate_embeddings
        from pdf_generator import generate_all_test_pdfs
        
        pdf_dir = Path(__file__).parent / "sample_pdfs"
        generate_all_test_pdfs(str(pdf_dir))
        
        pdf_path = str(pdf_dir / "single_page.pdf")
        
        raw_text = load_pdf(pdf_path)
        cleaned_text = clean_text(raw_text)
        chunks = create_chunks(cleaned_text, chunk_size=200, chunk_overlap=50)
        
        if chunks:
            embeddings = generate_embeddings(chunks)
            store = build_faiss(chunks, embeddings)
            
            assert isinstance(store, FAISSVectorStore)
            assert len(store.chunks) == len(chunks)
            assert store.dimension == 384
    
    def test_pipeline_with_search(self):
        """Test complete pipeline with search functionality."""
        from embedding_generator import generate_embeddings
        
        chunks = [
            "Policy covers comprehensive auto insurance",
            "Liability coverage up to $100,000",
            "Collision coverage included"
        ]
        
        embeddings = generate_embeddings(chunks)
        store = build_faiss(chunks, embeddings)
        
        # Test with string query
        results = store.similarity_search("car insurance liability", top_k=2)
        
        assert len(results) == 2
        assert any("Liability" in r for r in results)


class TestMetadata:
    """Test metadata functionality."""
    
    def test_metadata_calculation(self):
        """Test that metadata is calculated correctly."""
        chunks = ["Chunk 1", "Chunk 2", "Chunk 3"]
        embeddings = [[0.1] * 384, [0.2] * 384, [0.3] * 384]
        
        store = build_faiss(chunks, embeddings)
        metadata = get_index_metadata(store)
        
        assert metadata['total_chunks'] == 3
        assert metadata['embedding_dimension'] == 384
        assert metadata['index_size'] == 3
    
    def test_empty_metadata(self):
        """Test metadata for None store."""
        metadata = get_index_metadata(None)
        
        assert metadata['total_chunks'] == 0
        assert metadata['embedding_dimension'] == 0
        assert metadata['index_size'] == 0


class TestReturnTypes:
    """Test return type validation."""
    
    def test_build_returns_vectorstore(self):
        """Test that build_faiss returns FAISSVectorStore."""
        chunks = ["Test"]
        embeddings = [[0.1] * 384]
        
        store = build_faiss(chunks, embeddings)
        
        assert isinstance(store, FAISSVectorStore)
    
    def test_search_returns_list_of_strings(self):
        """Test that search returns list of strings."""
        chunks = ["Chunk 1", "Chunk 2"]
        embeddings = [[0.1] * 384, [0.2] * 384]
        
        store = build_faiss(chunks, embeddings)
        query_emb = [0.1] * 384
        results = store.similarity_search(query_emb)
        
        assert isinstance(results, list)
        assert all(isinstance(r, str) for r in results)
    
    def test_metadata_returns_dict(self):
        """Test that metadata returns dictionary."""
        chunks = ["Test"]
        embeddings = [[0.1] * 384]
        
        store = build_faiss(chunks, embeddings)
        metadata = get_index_metadata(store)
        
        assert isinstance(metadata, dict)
        assert 'total_chunks' in metadata
        assert 'embedding_dimension' in metadata
        assert 'index_size' in metadata


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
