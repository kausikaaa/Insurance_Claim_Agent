"""Example usage of the PDF loader module."""

from pdf_loader import load_pdf
from exceptions import PDFLoadError
from pdf_generator import generate_all_test_pdfs
import os


def main():
    """Demonstrate PDF loading functionality."""
    print("Generating sample PDFs...")
    generate_all_test_pdfs("tests/sample_pdfs")
    print("Sample PDFs generated.\n")
    
    pdf_path = "tests/sample_pdfs/single_page.pdf"
    
    try:
        text = load_pdf(pdf_path)
        print(f"Successfully extracted text from: {pdf_path}")
        print(f"Text length: {len(text)} characters")
        print("\nFirst 500 characters:")
        print("-" * 80)
        print(text[:500])
        print("-" * 80)
        
    except PDFLoadError as e:
        print(f"Error loading PDF: {e}")
    
    print("\n" + "=" * 80)
    print("Testing multi-page PDF...")
    print("=" * 80)
    
    multi_page_path = "tests/sample_pdfs/multi_page.pdf"
    try:
        text = load_pdf(multi_page_path)
        print(f"Successfully extracted text from: {multi_page_path}")
        print(f"Text length: {len(text)} characters")
        print(f"Number of lines: {len(text.split(chr(10)))}")
        
    except PDFLoadError as e:
        print(f"Error loading PDF: {e}")


if __name__ == "__main__":
    main()
