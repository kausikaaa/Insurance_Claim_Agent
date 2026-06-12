"""Example usage of the text cleaning module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "phase1_pdf_ingestion"))

from pdf_loader import load_pdf
from pdf_generator import generate_all_test_pdfs
from text_cleaner import clean_text, get_cleaning_stats


def main():
    """Demonstrate text cleaning functionality."""
    print("=" * 80)
    print("PHASE 2: TEXT CLEANING DEMONSTRATION")
    print("=" * 80)
    
    print("\nGenerating sample PDFs...")
    pdf_dir = Path(__file__).parent.parent / "phase1_pdf_ingestion" / "tests" / "sample_pdfs"
    generate_all_test_pdfs(str(pdf_dir))
    print("Sample PDFs generated.\n")
    
    pdf_path = str(pdf_dir / "multi_page.pdf")
    
    print(f"Loading PDF: {pdf_path}")
    raw_text = load_pdf(pdf_path)
    print(f"Raw text extracted: {len(raw_text)} characters\n")
    
    print("-" * 80)
    print("RAW TEXT (first 500 characters):")
    print("-" * 80)
    print(raw_text[:500])
    print("-" * 80)
    
    print("\nCleaning text...")
    cleaned_text = clean_text(raw_text)
    
    print("\n" + "-" * 80)
    print("CLEANED TEXT (first 500 characters):")
    print("-" * 80)
    print(cleaned_text[:500])
    print("-" * 80)
    
    stats = get_cleaning_stats(raw_text, cleaned_text)
    
    print("\n" + "=" * 80)
    print("CLEANING STATISTICS")
    print("=" * 80)
    print(f"Original length:      {stats['original_length']} characters")
    print(f"Cleaned length:       {stats['cleaned_length']} characters")
    print(f"Characters removed:   {stats['characters_removed']}")
    print(f"Original lines:       {stats['original_lines']}")
    print(f"Cleaned lines:        {stats['cleaned_lines']}")
    print(f"Lines removed:        {stats['lines_removed']}")
    print("=" * 80)
    
    print("\nDemonstrating with simulated messy text...")
    messy_text = """
    
    
Page 1

INSURANCE POLICY DOCUMENT

Policy Number: INS-2024-001234
    
    
Coverage   Details   Here

Page 2

INSURANCE POLICY DOCUMENT

More policy information
    
    
    Footer Text Here
    
1

Page 3

INSURANCE POLICY DOCUMENT

Additional  terms   and    conditions

    Footer Text Here
    
2
    """
    
    print("\n" + "-" * 80)
    print("MESSY TEXT:")
    print("-" * 80)
    print(messy_text)
    print("-" * 80)
    
    cleaned_messy = clean_text(messy_text)
    
    print("\n" + "-" * 80)
    print("CLEANED MESSY TEXT:")
    print("-" * 80)
    print(cleaned_messy)
    print("-" * 80)
    
    messy_stats = get_cleaning_stats(messy_text, cleaned_messy)
    print(f"\nRemoved {messy_stats['characters_removed']} characters")
    print(f"Removed {messy_stats['lines_removed']} lines")


if __name__ == "__main__":
    main()
