"""Comprehensive Phase 1-5 integration test."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Import all phases
from pdf_loader import load_pdf
from pdf_generator import generate_all_test_pdfs
from text_cleaner import clean_text
from chunker import create_chunks
from embedding_generator import generate_embeddings
from faiss_store import build_faiss, save_index, load_index


def test_complete_pipeline():
    """Test complete pipeline from PDF to searchable FAISS index."""
    print("=" * 80)
    print("PHASE 1-5 INTEGRATION TEST")
    print("=" * 80)
    
    # Setup
    pdf_dir = Path(__file__).parent / "tests" / "sample_pdfs"
    generate_all_test_pdfs(str(pdf_dir))
    pdf_path = str(pdf_dir / "multi_page.pdf")
    
    # Phase 1: PDF Ingestion
    print("\n[Phase 1] PDF Ingestion...")
    raw_text = load_pdf(pdf_path)
    assert len(raw_text) > 0
    print(f"  [OK] Extracted {len(raw_text)} characters")
    
    # Phase 2: Text Cleaning
    print("\n[Phase 2] Text Cleaning...")
    cleaned_text = clean_text(raw_text)
    assert len(cleaned_text) > 0
    print(f"  [OK] Cleaned to {len(cleaned_text)} characters")
    
    # Phase 3: Document Chunking
    print("\n[Phase 3] Document Chunking...")
    chunks = create_chunks(cleaned_text, chunk_size=300, chunk_overlap=50)
    assert len(chunks) > 0
    print(f"  [OK] Created {len(chunks)} chunks")
    
    # Phase 4: Embedding Generation
    print("\n[Phase 4] Embedding Generation...")
    embeddings = generate_embeddings(chunks)
    assert len(embeddings) == len(chunks)
    assert len(embeddings[0]) == 384
    print(f"  [OK] Generated {len(embeddings)} embeddings (384-dim)")
    
    # Phase 5: FAISS Knowledge Base
    print("\n[Phase 5] FAISS Knowledge Base...")
    store = build_faiss(chunks, embeddings)
    assert store is not None
    print(f"  [OK] Built FAISS index with {len(chunks)} vectors")
    
    # Test string query
    print("\n[Test] String Query Search...")
    results = store.similarity_search("property coverage", top_k=2)
    assert len(results) > 0
    assert isinstance(results[0], str)
    print(f"  [OK] String query returned {len(results)} results")
    print(f"     Top result: {results[0][:80]}...")
    
    # Test vector query
    print("\n[Test] Vector Query Search...")
    query_emb = generate_embeddings(["insurance policy"])[0]
    results2 = store.similarity_search(query_emb, top_k=2)
    assert len(results2) > 0
    assert isinstance(results2[0], str)
    print(f"  [OK] Vector query returned {len(results2)} results")
    print(f"     Top result: {results2[0][:80]}...")
    
    # Test persistence
    print("\n[Test] Persistence...")
    save_index(store, "test_vector_store")
    print("  [OK] Saved index to disk")
    
    loaded_store = load_index("test_vector_store")
    print("  [OK] Loaded index from disk")
    
    results3 = loaded_store.similarity_search("liability coverage", top_k=1)
    assert len(results3) > 0
    print(f"  [OK] Search after load works: {results3[0][:80]}...")
    
    # Cleanup
    import shutil
    shutil.rmtree("test_vector_store")
    
    print("\n" + "=" * 80)
    print("ALL INTEGRATION TESTS PASSED")
    print("=" * 80)
    print("\n[OK] Phase 1: PDF Ingestion - WORKING")
    print("[OK] Phase 2: Text Cleaning - WORKING")
    print("[OK] Phase 3: Document Chunking - WORKING")
    print("[OK] Phase 4: Embedding Generation - WORKING")
    print("[OK] Phase 5: FAISS Knowledge Base - WORKING")
    print("\n[OK] String queries - WORKING")
    print("[OK] Vector queries - WORKING")
    print("[OK] Save/Load persistence - WORKING")
    print("[OK] End-to-end pipeline - WORKING")
    print("\nSTATUS: ALL SYSTEMS OPERATIONAL")


if __name__ == "__main__":
    test_complete_pipeline()
