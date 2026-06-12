"""Comprehensive tests for PDF loader module."""

import os
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_loader import load_pdf
from exceptions import (
    PDFNotFoundError,
    InvalidPDFError,
    CorruptedPDFError,
    EmptyPDFError,
    PDFPermissionError
)
from pdf_generator import generate_all_test_pdfs


class TestPDFLoader:
    """Test suite for PDF loading functionality."""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_test_pdfs(self):
        """Generate test PDFs before running tests."""
        sample_pdfs_dir = Path(__file__).parent / "sample_pdfs"
        generate_all_test_pdfs(str(sample_pdfs_dir))
        yield
    
    @pytest.fixture
    def sample_pdfs_dir(self):
        """Get the sample PDFs directory path."""
        return Path(__file__).parent / "sample_pdfs"
    
    def test_nonexistent_file_raises_not_found_error(self):
        """Test that loading a nonexistent file raises PDFNotFoundError."""
        with pytest.raises(PDFNotFoundError) as exc_info:
            load_pdf("nonexistent_file.pdf")
        assert "not found" in str(exc_info.value).lower()
    
    def test_non_pdf_file_raises_invalid_pdf_error(self, tmp_path):
        """Test that loading a non-PDF file raises InvalidPDFError."""
        text_file = tmp_path / "test.txt"
        text_file.write_text("This is not a PDF")
        
        with pytest.raises(InvalidPDFError) as exc_info:
            load_pdf(str(text_file))
        assert "not a pdf" in str(exc_info.value).lower()
    
    def test_corrupted_pdf_raises_corrupted_error(self, tmp_path):
        """Test that loading a corrupted PDF raises CorruptedPDFError."""
        corrupted_pdf = tmp_path / "corrupted.pdf"
        corrupted_pdf.write_text("%PDF-1.4\nGarbage data that is not a valid PDF")
        
        with pytest.raises((InvalidPDFError, CorruptedPDFError)) as exc_info:
            load_pdf(str(corrupted_pdf))
    
    def test_empty_pdf_raises_empty_error(self, sample_pdfs_dir):
        """Test that a PDF with no extractable text raises EmptyPDFError."""
        empty_pdf = sample_pdfs_dir / "empty.pdf"
        
        with pytest.raises(EmptyPDFError) as exc_info:
            load_pdf(str(empty_pdf))
        assert "no extractable text" in str(exc_info.value).lower()
    
    def test_single_page_pdf_extraction(self, sample_pdfs_dir):
        """Test extraction from a single-page PDF."""
        single_page_pdf = sample_pdfs_dir / "single_page.pdf"
        
        text = load_pdf(str(single_page_pdf))
        assert isinstance(text, str)
        assert len(text) > 0
        assert text.strip()
        assert "Insurance Policy Document" in text
        assert "Policy Number" in text
    
    def test_multi_page_pdf_extraction(self, sample_pdfs_dir):
        """Test extraction from a multi-page PDF."""
        multi_page_pdf = sample_pdfs_dir / "multi_page.pdf"
        
        text = load_pdf(str(multi_page_pdf))
        assert isinstance(text, str)
        assert len(text) > 0
        assert text.strip()
        assert "Page 1" in text
        assert "Page 2" in text
        assert "Page 3" in text
        assert "Property Coverage" in text
        assert "Liability Coverage" in text
    
    def test_text_content_accuracy(self, sample_pdfs_dir):
        """Test that extracted text contains expected content."""
        single_page_pdf = sample_pdfs_dir / "single_page.pdf"
        text = load_pdf(str(single_page_pdf))
        
        assert "INS-2024-001234" in text
        assert "John Doe" in text
        assert "Comprehensive Auto Insurance" in text
        assert "Liability Coverage" in text
    
    def test_multi_page_text_combination(self, sample_pdfs_dir):
        """Test that text from multiple pages is properly combined."""
        multi_page_pdf = sample_pdfs_dir / "multi_page.pdf"
        text = load_pdf(str(multi_page_pdf))
        
        assert isinstance(text, str)
        lines = text.split('\n')
        assert len(lines) > 10
    
    def test_invalid_path_types(self):
        """Test that invalid path types are handled properly."""
        with pytest.raises(Exception):
            load_pdf("")
    
    def test_directory_path_raises_error(self, tmp_path):
        """Test that passing a directory path raises an error."""
        with pytest.raises((PDFNotFoundError, InvalidPDFError)):
            load_pdf(str(tmp_path))


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_pdf_with_special_characters_in_path(self, tmp_path):
        """Test handling PDFs with special characters in file path."""
        special_dir = tmp_path / "test folder with spaces"
        special_dir.mkdir()
        pdf_path = special_dir / "test file.pdf"
        
        with pytest.raises((PDFNotFoundError, InvalidPDFError, CorruptedPDFError)):
            load_pdf(str(pdf_path))
    
    def test_relative_path_handling(self):
        """Test that relative paths work correctly."""
        with pytest.raises(PDFNotFoundError):
            load_pdf("./does_not_exist.pdf")
    
    def test_absolute_path_handling(self):
        """Test that absolute paths work correctly."""
        with pytest.raises(PDFNotFoundError):
            load_pdf("C:\\does_not_exist.pdf")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
