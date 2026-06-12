"""Utility to dynamically generate test PDF files."""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path


def create_single_page_pdf(output_path: str) -> None:
    """
    Create a single-page PDF with sample insurance policy text.
    
    Args:
        output_path: Path where the PDF should be created.
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "Insurance Policy Document")
    
    c.setFont("Helvetica", 12)
    y_position = height - 150
    
    text_lines = [
        "Policy Number: INS-2024-001234",
        "Policy Holder: John Doe",
        "Coverage Type: Comprehensive Auto Insurance",
        "Effective Date: January 1, 2024",
        "Expiration Date: December 31, 2024",
        "",
        "Coverage Details:",
        "- Liability Coverage: $100,000",
        "- Collision Coverage: $50,000",
        "- Comprehensive Coverage: $50,000",
        "- Medical Payments: $10,000",
        "",
        "This is a valid insurance policy document for testing purposes."
    ]
    
    for line in text_lines:
        c.drawString(100, y_position, line)
        y_position -= 20
    
    c.save()


def create_multi_page_pdf(output_path: str) -> None:
    """
    Create a multi-page PDF with sample insurance policy text.
    
    Args:
        output_path: Path where the PDF should be created.
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Page 1
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "Insurance Policy Document - Page 1")
    
    c.setFont("Helvetica", 12)
    y_position = height - 150
    
    page1_text = [
        "Policy Number: INS-2024-005678",
        "Policy Holder: Jane Smith",
        "Coverage Type: Home Insurance",
        "Effective Date: March 1, 2024",
        "Expiration Date: February 28, 2025",
        "",
        "Section 1: Property Coverage",
        "- Dwelling: $300,000",
        "- Other Structures: $30,000",
        "- Personal Property: $150,000",
        "- Loss of Use: $60,000"
    ]
    
    for line in page1_text:
        c.drawString(100, y_position, line)
        y_position -= 20
    
    c.showPage()
    
    # Page 2
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "Insurance Policy Document - Page 2")
    
    c.setFont("Helvetica", 12)
    y_position = height - 150
    
    page2_text = [
        "Section 2: Liability Coverage",
        "- Personal Liability: $300,000",
        "- Medical Payments: $5,000",
        "",
        "Section 3: Additional Coverages",
        "- Fire Department Charges: $500",
        "- Debris Removal: Included",
        "- Trees and Shrubs: $5,000",
        "",
        "This multi-page policy document contains all terms and conditions.",
        "For questions, contact your insurance agent."
    ]
    
    for line in page2_text:
        c.drawString(100, y_position, line)
        y_position -= 20
    
    c.showPage()
    
    # Page 3
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "Insurance Policy Document - Page 3")
    
    c.setFont("Helvetica", 12)
    y_position = height - 150
    
    page3_text = [
        "Section 4: Deductibles and Premiums",
        "- Annual Premium: $1,200",
        "- Deductible: $1,000",
        "",
        "Section 5: Claims Process",
        "To file a claim, contact us at 1-800-INSURANCE",
        "Claims must be filed within 60 days of the incident.",
        "",
        "This document is valid and binding upon signature."
    ]
    
    for line in page3_text:
        c.drawString(100, y_position, line)
        y_position -= 20
    
    c.save()


def create_empty_pdf(output_path: str) -> None:
    """
    Create a PDF with no extractable text (blank page).
    
    Args:
        output_path: Path where the PDF should be created.
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    c.showPage()
    c.save()


def create_corrupted_pdf(output_path: str) -> None:
    """
    Create a corrupted PDF file with invalid content.
    
    Args:
        output_path: Path where the PDF should be created.
    """
    with open(output_path, 'w') as f:
        f.write("%PDF-1.4\n")
        f.write("This is not valid PDF content\n")
        f.write("Just garbage data to simulate corruption\n")
        f.write("%%EOF\n")


def generate_all_test_pdfs(output_dir: str) -> None:
    """
    Generate all test PDF files in the specified directory.
    
    Args:
        output_dir: Directory where test PDFs should be created.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    create_single_page_pdf(str(output_path / "single_page.pdf"))
    create_multi_page_pdf(str(output_path / "multi_page.pdf"))
    create_empty_pdf(str(output_path / "empty.pdf"))
    create_corrupted_pdf(str(output_path / "corrupted.pdf"))


if __name__ == "__main__":
    generate_all_test_pdfs("tests/sample_pdfs")
    print("Test PDFs generated successfully!")
