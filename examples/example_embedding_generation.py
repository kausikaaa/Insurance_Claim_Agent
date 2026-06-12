"""Example demonstrating the complete PDF-to-Embeddings pipeline."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_loader import load_pdf
from pdf_generator import generate_all_test_pdfs
from text_cleaner import clean_text, get_cleaning_stats
from chunker import create_chunks, get_chunk_metadata
from embedding_generator import generate_embeddings, get_embedding_metadata


def main():
    """Demonstrate the complete pipeline: PDF → Text → Cleaned → Chunks → Embeddings."""
    print("=" * 80)
    print("INSURANCE CLAIM AGENT - COMPLETE PIPELINE WITH EMBEDDINGS")
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
    print(f"     Lines: {len(raw_text.split(chr(10)))}")
    
    # Phase 2: Text Cleaning
    print("\n" + "=" * 80)
    print("[Phase 2] TEXT CLEANING")
    print("=" * 80)
    
    print("\nCleaning extracted text...")
    cleaned_text = clean_text(raw_text)
    
    cleaning_stats = get_cleaning_stats(raw_text, cleaned_text)
    print(f"[OK] Text cleaned: {len(cleaned_text)} characters")
    print(f"     Characters removed: {cleaning_stats['characters_removed']}")
    print(f"     Lines removed: {cleaning_stats['lines_removed']}")
    
    # Phase 3: Document Chunking
    print("\n" + "=" * 80)
    print("[Phase 3] DOCUMENT CHUNKING")
    print("=" * 80)
    
    print("\nCreating overlapping chunks...")
    chunks = create_chunks(cleaned_text, chunk_size=500, chunk_overlap=100)
    
    chunk_metadata = get_chunk_metadata(chunks)
    print(f"[OK] Chunks created: {chunk_metadata['total_chunks']}")
    print(f"     Total characters in chunks: {chunk_metadata['total_characters']}")
    print(f"     Avg chunk size: {chunk_metadata['avg_chunk_size']:.2f}")
    
    # Phase 4: Embedding Generation
    print("\n" + "=" * 80)
    print("[Phase 4] EMBEDDING GENERATION")
    print("=" * 80)
    
    print("\nGenerating vector embeddings...")
    print("(This may take a moment on first run as the model downloads...)")
    embeddings = generate_embeddings(chunks)
    
    embedding_metadata = get_embedding_metadata(embeddings)
    print(f"[OK] Embeddings generated: {embedding_metadata['total_embeddings']}")
    print(f"     Embedding dimension: {embedding_metadata['embedding_dimension']}")
    print(f"     Total vectors: {embedding_metadata['total_vectors']}")
    
    # Show embedding samples
    print("\n" + "-" * 80)
    print("EMBEDDING SAMPLES")
    print("-" * 80)
    
    for i in range(min(3, len(embeddings))):
        print(f"\nChunk {i+1} ({len(chunks[i])} chars): \"{chunks[i][:60]}...\"")
        print(f"Embedding vector (first 10 dimensions):")
        print(f"  [{', '.join([f'{v:.4f}' for v in embeddings[i][:10]])}...]")
    
    # Summary
    print("\n" + "=" * 80)
    print("COMPLETE PIPELINE SUMMARY")
    print("=" * 80)
    print(f"Input:    PDF file")
    print(f"Phase 1:  Extracted {len(raw_text)} characters")
    print(f"Phase 2:  Cleaned to {len(cleaned_text)} characters")
    print(f"Phase 3:  Split into {len(chunks)} chunks")
    print(f"Phase 4:  Generated {len(embeddings)} embeddings (384-dim vectors)")
    print(f"Output:   Ready for vector database storage and semantic search")
    print("=" * 80)
    
    # Demonstrate semantic similarity
    if len(embeddings) >= 2:
        print("\n" + "=" * 80)
        print("SEMANTIC SIMILARITY DEMONSTRATION")
        print("=" * 80)
        
        def cosine_similarity(vec1, vec2):
            dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
            norm1 = sum(v * v for v in vec1) ** 0.5
            norm2 = sum(v * v for v in vec2) ** 0.5
            return dot_product / (norm1 * norm2)
        
        print("\nSimilarity between consecutive chunks:")
        for i in range(min(3, len(embeddings) - 1)):
            sim = cosine_similarity(embeddings[i], embeddings[i + 1])
            print(f"Chunk {i+1} <-> Chunk {i+2}: {sim:.4f}")
        
        print("\nNote: Higher values (closer to 1.0) indicate more semantic similarity")
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
