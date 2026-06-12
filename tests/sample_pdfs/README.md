# Sample PDFs Directory

Place your test PDF files in this directory for testing the PDF loader module.

## Recommended Test Files

To fully test the module, include the following types of PDFs:

1. **single_page.pdf** - A simple single-page PDF document
2. **multi_page.pdf** - A PDF with multiple pages
3. **empty.pdf** - A PDF with no extractable text (optional)
4. **corrupted.pdf** - A corrupted or malformed PDF file (optional)

You can create or download sample PDF files and place them here for testing.

## Running Tests

Once you have sample PDFs in this directory, run:

```bash
pytest tests/test_pdf_loader.py -v
```

The tests will automatically discover and test available PDF files.
