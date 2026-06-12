"""Standalone script to generate test PDFs."""

from pdf_generator import generate_all_test_pdfs


if __name__ == "__main__":
    print("Generating test PDF files...")
    generate_all_test_pdfs("tests/sample_pdfs")
    print("\nTest PDFs created successfully in tests/sample_pdfs/:")
    print("  - single_page.pdf (1 page with insurance policy content)")
    print("  - multi_page.pdf (3 pages with insurance policy content)")
    print("  - empty.pdf (blank PDF with no text)")
    print("  - corrupted.pdf (invalid PDF for error testing)")
    print("\nYou can now run: pytest tests/test_pdf_loader.py -v")
