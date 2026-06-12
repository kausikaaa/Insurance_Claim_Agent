"""Example demonstrating the complete PDF-to-FAISS Knowledge Base pipeline."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_loader import load_pdf
from pdf_generator import generate_all_test_pdfs
from text_cleaner import clean_text, get_cleaning_stats
from chunker import create_chunks, get_chunk_metadata
from embedding_generator import generate_embeddings, get_embedding_metadata
from faiss_store import build_faiss, save_index, load_index, get_index_metadata


def main():
    """Demonstrate the complete pipeline: PDF → FAISS Knowledge Base → Search."""
    print("=" * 80)
    print("INSURANCE CLAIM AGENT - COMPLETE KNOWLEDGE BASE PIPELINE")
    print("=" * 80)
    
    # Phase 0: Generate sample PDFs
    print("\n[Phase 0] Generating sample PDFs...")
    pdf_dir = Path(__file__).parent.parent / "tests" / "sample_pdfs"
    generate_all_test_pdfs(str(pdf_dir))
    print("[OK] Sample PDFs generated")
    
    # Phase 1: PDF Ingestion
    print("\n" + "=" * 80)
    print("[Phase 1] PDF INGESTION")
    print("=" * 80)
    
    pdf_path = str(pdf_dir / "multi_page.pdf")
    print(f"\nLoading PDF: {pdf_path}")
    
    raw_text = load_pdf(pdf_path)
    print(f"[OK] Raw text extracted: {len(raw_text)} characters")
    
    # Phase 2: Text Cleaning
    print("\n" + "=" * 80)
    print("[Phase 2] TEXT CLEANING")
    print("=" * 80)
    
    cleaned_text = clean_text(raw_text)
    cleaning_stats = get_cleaning_stats(raw_text, cleaned_text)
    print(f"[OK] Text cleaned: {len(cleaned_text)} characters")
    print(f"     Characters removed: {cleaning_stats['characters_removed']}")
    
    # Phase 3: Document Chunking
    print("\n" + "=" * 80)
    print("[Phase 3] DOCUMENT CHUNKING")
    print("=" * 80)
    
    chunks = create_chunks(cleaned_text, chunk_size=300, chunk_overlap=50)
    chunk_metadata = get_chunk_metadata(chunks)
    print(f"[OK] Chunks created: {chunk_metadata['total_chunks']}")
    print(f"     Avg chunk size: {chunk_metadata['avg_chunk_size']:.2f}")
    
    # Phase 4: Embedding Generation
    print("\n" + "=" * 80)
    print("[Phase 4] EMBEDDING GENERATION")
    print("=" * 80)
    
    embeddings = generate_embeddings(chunks)
    embedding_metadata = get_embedding_metadata(embeddings)
    print(f"[OK] Embeddings generated: {embedding_metadata['total_embeddings']}")
    print(f"     Embedding dimension: {embedding_metadata['embedding_dimension']}")
    
    # Phase 5: FAISS Knowledge Base Creation
    print("\n" + "=" * 80)
    print("[Phase 5] FAISS KNOWLEDGE BASE CREATION")
    print("=" * 80)
    
    print("\nBuilding FAISS index...")
    vectorstore = build_faiss(chunks, embeddings)
    
    index_metadata = get_index_metadata(vectorstore)
    print(f"[OK] FAISS index built: {index_metadata['total_chunks']} chunks indexed")
    print(f"     Index size: {index_metadata['index_size']} vectors")
    
    # Save index to disk
    print("\nSaving index to disk...")
    save_index(vectorstore, "vector_store")
    print("[OK] Index saved to 'vector_store/' directory")
    
    # Load index from disk
    print("\nLoading index from disk...")
    loaded_store = load_index("vector_store")
    print("[OK] Index loaded successfully")
    
    # Demonstrate semantic search
    print("\n" + "=" * 80)
    print("SEMANTIC SEARCH DEMONSTRATION")
    print("=" * 80)
    
    queries = [
        "property coverage details",
        "liability insurance amount",
        "claims filing process"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n[Query {i}] \"{query}\"")
        print("-" * 80)
        
        results = loaded_store.similarity_search(query, top_k=2)
        
        for j, result in enumerate(results, 1):
            print(f"\nResult {j}:")
            print(f"  {result[:150]}..." if len(result) > 150 else f"  {result}")
    
    # Summary
    print("\n" + "=" * 80)
    print("COMPLETE PIPELINE SUMMARY")
    print("=" * 80)
    print(f"Input:    PDF file")
    print(f"Phase 1:  Extracted {len(raw_text)} characters")
    print(f"Phase 2:  Cleaned to {len(cleaned_text)} characters")
    print(f"Phase 3:  Split into {len(chunks)} chunks")
    print(f"Phase 4:  Generated {len(embeddings)} embeddings (384-dim)")
    print(f"Phase 5:  Built FAISS index with {index_metadata['total_chunks']} vectors")
    print(f"Output:   Searchable knowledge base ready for queries")
    print("=" * 80)
    
    # Demonstrate persistence
    print("\n" + "=" * 80)
    print("PERSISTENCE DEMONSTRATION")
    print("=" * 80)
    print("\nThe knowledge base is now saved to disk.")
    print("You can load it anytime without reprocessing the PDF:")
    print("\n  from faiss_store import load_index")
    print("  store = load_index('vector_store')")
    print("  results = store.similarity_search('your query here')")
    print("\nNo need to:")
    print("  - Re-extract PDF text")
    print("  - Re-clean text")
    print("  - Re-chunk documents")
    print("  - Re-generate embeddings")
    print("\nJust load and search!")
    print("=" * 80)
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
