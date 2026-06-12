"""Example demonstrating the complete PDF-to-Chunks pipeline."""

import sys
from pathlib import Path

from pdf_loader import load_pdf
from pdf_generator import generate_all_test_pdfs
from text_cleaner import clean_text, get_cleaning_stats
from chunker import create_chunks, get_chunk_metadata


def main():
    """Demonstrate the complete pipeline: PDF → Text → Cleaned Text → Chunks."""
    print("=" * 80)
    print("INSURANCE CLAIM AGENT - COMPLETE PIPELINE DEMONSTRATION")
    print("=" * 80)
    
    # Phase 0: Generate sample PDFs
    print("\n[Phase 0] Generating sample PDFs...")
    pdf_dir = Path(__file__).parent / "tests" / "sample_pdfs"
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
    
    print("\nRaw text preview (first 300 characters):")
    print("-" * 80)
    print(raw_text[:300])
    print("-" * 80)
    
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
    
    print("\nCleaned text preview (first 300 characters):")
    print("-" * 80)
    print(cleaned_text[:300])
    print("-" * 80)
    
    # Phase 3: Document Chunking
    print("\n" + "=" * 80)
    print("[Phase 3] DOCUMENT CHUNKING")
    print("=" * 80)
    
    print("\nCreating overlapping chunks...")
    chunks = create_chunks(cleaned_text, chunk_size=1000, chunk_overlap=200)
    
    chunk_metadata = get_chunk_metadata(chunks)
    print(f"[OK] Chunks created: {chunk_metadata['total_chunks']}")
    print(f"     Total characters in chunks: {chunk_metadata['total_characters']}")
    print(f"     Min chunk size: {chunk_metadata['min_chunk_size']}")
    print(f"     Max chunk size: {chunk_metadata['max_chunk_size']}")
    print(f"     Avg chunk size: {chunk_metadata['avg_chunk_size']:.2f}")
    
    print("\n" + "-" * 80)
    print("CHUNK PREVIEWS")
    print("-" * 80)
    
    for i, chunk in enumerate(chunks[:3], 1):
        print(f"\nChunk {i} ({len(chunk)} characters):")
        print("-" * 40)
        print(chunk[:200] + "..." if len(chunk) > 200 else chunk)
    
    if len(chunks) > 3:
        print(f"\n... and {len(chunks) - 3} more chunks")
    
    # Summary
    print("\n" + "=" * 80)
    print("PIPELINE SUMMARY")
    print("=" * 80)
    print(f"Input:  PDF file with {len(raw_text)} characters")
    print(f"Step 1: Extracted raw text")
    print(f"Step 2: Cleaned to {len(cleaned_text)} characters")
    print(f"Step 3: Split into {len(chunks)} searchable chunks")
    print(f"Output: Ready for vector search and retrieval")
    print("=" * 80)
    
    # Demonstrate chunk overlap
    if len(chunks) > 1:
        print("\n" + "=" * 80)
        print("CHUNK OVERLAP DEMONSTRATION")
        print("=" * 80)
        print("\nShowing overlap between consecutive chunks:")
        print("\nEnd of Chunk 1 (last 100 chars):")
        print("-" * 40)
        print(chunks[0][-100:])
        print("\nStart of Chunk 2 (first 100 chars):")
        print("-" * 40)
        print(chunks[1][:100])
        print("\n[OK] Notice the overlapping content between chunks")
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
