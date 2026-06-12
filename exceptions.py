"""Custom exceptions for PDF loading operations."""


class PDFLoadError(Exception):
    """Base exception for PDF loading errors."""
    pass


class PDFNotFoundError(PDFLoadError):
    """Raised when the PDF file is not found."""
    pass


class InvalidPDFError(PDFLoadError):
    """Raised when the file is not a valid PDF."""
    pass


class CorruptedPDFError(PDFLoadError):
    """Raised when the PDF file is corrupted or unreadable."""
    pass


class EmptyPDFError(PDFLoadError):
    """Raised when the PDF contains no extractable text."""
    pass


class PDFPermissionError(PDFLoadError):
    """Raised when there are insufficient permissions to read the PDF."""
    pass
