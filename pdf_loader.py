"""PDF text extraction module using pdfplumber."""

import os
from pathlib import Path
from typing import Optional
import pdfplumber

from exceptions import (
    PDFNotFoundError,
    InvalidPDFError,
    CorruptedPDFError,
    EmptyPDFError,
    PDFPermissionError
)


def load_pdf(file_path: str) -> str:
    """
    Load a PDF and return all extracted text as a single string.
    
    Args:
        file_path: Path to the PDF file to load.
        
    Returns:
        Extracted text from all pages as a single string.
        
    Raises:
        PDFNotFoundError: If the file does not exist.
        InvalidPDFError: If the file is not a valid PDF.
        CorruptedPDFError: If the PDF is corrupted or unreadable.
        EmptyPDFError: If the PDF contains no extractable text.
        PDFPermissionError: If there are insufficient permissions to read the file.
    """
    _validate_file_exists(file_path)
    _validate_file_extension(file_path)
    _validate_file_permissions(file_path)
    
    extracted_text = _extract_text_from_pdf(file_path)
    
    if not extracted_text.strip():
        raise EmptyPDFError(f"PDF contains no extractable text: {file_path}")
    
    return extracted_text


def _validate_file_exists(file_path: str) -> None:
    """Verify that the file exists."""
    if not os.path.exists(file_path):
        raise PDFNotFoundError(f"File not found: {file_path}")


def _validate_file_extension(file_path: str) -> None:
    """Verify that the file has a .pdf extension."""
    if not file_path.lower().endswith('.pdf'):
        raise InvalidPDFError(f"File is not a PDF: {file_path}")


def _validate_file_permissions(file_path: str) -> None:
    """Verify that the file can be read."""
    if not os.access(file_path, os.R_OK):
        raise PDFPermissionError(f"Insufficient permissions to read file: {file_path}")


def _extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from all pages of the PDF.
    
    Args:
        file_path: Path to the PDF file.
        
    Returns:
        Combined text from all pages.
        
    Raises:
        InvalidPDFError: If the file cannot be opened as a PDF.
        CorruptedPDFError: If the PDF is corrupted during reading.
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            if not pdf.pages:
                return ""
            
            page_texts = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    page_texts.append(text)
            
            return "\n".join(page_texts)
            
    except pdfplumber.pdfminer.pdfparser.PDFSyntaxError as e:
        raise InvalidPDFError(f"Invalid PDF format: {file_path}") from e
    except pdfplumber.pdfminer.pdfdocument.PDFException as e:
        raise CorruptedPDFError(f"Corrupted or unreadable PDF: {file_path}") from e
    except Exception as e:
        if "password" in str(e).lower() or "encrypted" in str(e).lower():
            raise PDFPermissionError(f"PDF is password-protected: {file_path}") from e
        raise CorruptedPDFError(f"Error reading PDF: {file_path}") from e
