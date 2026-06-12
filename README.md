# Insurance Claim Agent

Production-ready document processing pipeline for insurance policy documents.

## Overview

This system provides a complete pipeline for processing insurance policy PDFs:

1. **Phase 1: PDF Ingestion** - Extract text from PDF files
2. **Phase 2: Text Cleaning** - Normalize and clean extracted text
3. **Phase 3: Document Chunking** - Split text into searchable chunks
4. **Phase 4: Embedding Generation** - Convert chunks to vector embeddings

## Features

- Extract text from single-page and multi-page PDFs
- Remove page numbers, headers, and footers automatically
- Normalize whitespace and line endings
- Split documents into overlapping chunks for efficient retrieval
- Generate 384-dimensional vector embeddings using sentence-transformers
- Comprehensive error handling with custom exceptions
- Type hints and docstrings throughout
- Full test coverage with pytest (116 tests)
- Dynamic test data generation

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Complete Pipeline

```python
from pdf_loader import load_pdf
from text_cleaner import clean_text
from chunker import create_chunks
from embedding_generator import generate_embeddings

# Load PDF
raw_text = load_pdf("policy.pdf")

# Clean text
cleaned_text = clean_text(raw_text)

# Create chunks
chunks = create_chunks(cleaned_text, chunk_size=1000, chunk_overlap=200)

# Generate embeddings
embeddings = generate_embeddings(chunks)

print(f"Created {len(embeddings)} vector embeddings (384-dim)")
```

### Phase 1: PDF Ingestion

```python
from pdf_loader import load_pdf

try:
    text = load_pdf("path/to/policy.pdf")
    print(f"Extracted {len(text)} characters")
except PDFLoadError as e:
    print(f"Error: {e}")
```

### Phase 2: Text Cleaning

```python
from text_cleaner import clean_text, get_cleaning_stats

raw_text = "Your   messy    PDF   text\n\n\n\nPage 1\nMore text"
cleaned = clean_text(raw_text)

stats = get_cleaning_stats(raw_text, cleaned)
print(f"Removed {stats['characters_removed']} characters")
```

### Phase 3: Document Chunking

```python
from chunker import create_chunks, get_chunk_metadata

text = "Your cleaned document text..."
chunks = create_chunks(text, chunk_size=1000, chunk_overlap=200)

metadata = get_chunk_metadata(chunks)
print(f"Total chunks: {metadata['total_chunks']}")
print(f"Avg chunk size: {metadata['avg_chunk_size']:.2f}")
```

### Phase 4: Embedding Generation

```python
from embedding_generator import generate_embeddings, get_embedding_metadata

chunks = ["Insurance policy text...", "More policy content..."]
embeddings = generate_embeddings(chunks)

metadata = get_embedding_metadata(embeddings)
print(f"Generated {metadata['total_embeddings']} embeddings")
print(f"Embedding dimension: {metadata['embedding_dimension']}")
```

## Running Tests

Run all tests:
```bash
pytest tests/ -v
```

Run specific phase tests:
```bash
pytest tests/test_pdf_loader.py -v           # Phase 1: 13 tests
pytest tests/test_text_cleaner.py -v         # Phase 2: 40 tests
pytest tests/test_chunker.py -v              # Phase 3: 30 tests
pytest tests/test_embedding_generator.py -v  # Phase 4: 33 tests
```

## Running Examples

Complete pipeline demonstration:
```bash
python examples/example_complete_pipeline.py
python examples/example_embedding_generation.py
```

Individual phase examples:
```bash
python examples/example_pdf_ingestion.py
python examples/example_text_cleaning.py
```

## Project Structure

```
insurance_claim_agent/
│
├── pdf_loader.py               # Phase 1: PDF text extraction
├── text_cleaner.py             # Phase 2: Text normalization
├── chunker.py                  # Phase 3: Document chunking
├── embedding_generator.py      # Phase 4: Vector embeddings
├── config.py                   # Configuration for text cleaning
├── exceptions.py               # Custom exception classes
├── pdf_generator.py            # Test PDF generation utility
├── generate_test_pdfs.py       # Standalone PDF generator script
│
├── examples/
│   ├── example_pdf_ingestion.py       # Phase 1 example
│   ├── example_text_cleaning.py       # Phase 2 example
│   ├── example_complete_pipeline.py   # Phases 1-3 example
│   └── example_embedding_generation.py # Complete pipeline example
│
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
│
└── tests/
    ├── __init__.py
    ├── test_pdf_loader.py           # Phase 1 tests (13 tests)
    ├── test_text_cleaner.py         # Phase 2 tests (40 tests)
    ├── test_chunker.py              # Phase 3 tests (30 tests)
    ├── test_embedding_generator.py  # Phase 4 tests (33 tests)
    └── sample_pdfs/                 # Auto-generated test PDFs
        └── README.md
```

## Phase 1: PDF Ingestion

### Features
- Extract text from PDFs using pdfplumber
- Support for multi-page documents
- Comprehensive validation and error handling
- Dynamic test PDF generation

### Error Handling
- `PDFNotFoundError` - File does not exist
- `InvalidPDFError` - File is not a valid PDF
- `CorruptedPDFError` - PDF is corrupted or unreadable
- `EmptyPDFError` - PDF contains no extractable text
- `PDFPermissionError` - Insufficient permissions to read file

## Phase 2: Text Cleaning

### Features
- Remove leading/trailing whitespace
- Normalize multiple spaces to single spaces
- Remove excessive blank lines
- Normalize line endings (Windows/Mac/Unix)
- Remove page number artifacts (algorithmic)
- Detect and remove repeated headers (algorithmic)
- Detect and remove repeated footers (algorithmic)
- Preserve actual content and structure

### Cleaning Rules

**Whitespace Normalization:**
- Multiple spaces/tabs → single space
- Trailing whitespace removed from lines
- Leading/trailing document whitespace removed

**Page Number Removal:**
- Simple numbers: `1`, `2`, `3`
- Page prefix: `Page 1`, `Page 2`
- Page X of Y: `Page 1 of 10`
- X of Y format: `1 of 10`
- Bracketed: `[ 1 ]`
- Dashed: `- 1 -`

**Header/Footer Detection:**
- Algorithmically detects repeated sequences
- Single-line and multi-line support
- Minimum 2 occurrences required
- First occurrence preserved
- No hardcoded text patterns

## Phase 3: Document Chunking

### Features
- Split documents into overlapping chunks
- Uses LangChain's RecursiveCharacterTextSplitter
- Configurable chunk size and overlap
- Preserves content ordering
- Handles documents of any size
- Returns metadata about chunks

### Configuration
- Default chunk size: 1000 characters
- Default overlap: 200 characters
- Separators: `\n\n`, `\n`, ` `, ``

### Error Handling
- `InvalidTextError` - Invalid input type or None

## Phase 4: Embedding Generation

### Features
- Generate 384-dimensional vector embeddings
- Uses sentence-transformers/all-MiniLM-L6-v2 model
- Efficient batch processing
- Model caching (singleton pattern)
- Handles documents of any size
- Returns metadata about embeddings

### Configuration
- Model: sentence-transformers/all-MiniLM-L6-v2
- Embedding dimension: 384
- Runs locally (no API calls)

### Error Handling
- `InvalidChunkError` - Invalid input chunks
- `ModelLoadError` - Model loading failure
- `EmbeddingError` - General embedding errors

## Pipeline Architecture

```
┌─────────────┐
│  PDF File   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Phase 1: Ingestion │  load_pdf()
│  - Extract text     │
│  - Validate PDF     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Phase 2: Cleaning  │  clean_text()
│  - Remove artifacts │
│  - Normalize text   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Phase 3: Chunking  │  create_chunks()
│  - Split text       │
│  - Create overlap   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Phase 4: Embedding │  generate_embeddings()
│  - Generate vectors │
│  - 384 dimensions   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Vector Embeddings  │
│  Ready for Vector DB│
└─────────────────────┘
```

## Requirements

- Python 3.7+
- pdfplumber 0.11.0 (PDF extraction)
- pytest 7.4.3 (testing)
- reportlab 4.0.7 (test PDF generation)
- langchain-text-splitters 0.3.5 (text chunking)
- sentence-transformers 3.3.1 (vector embeddings)

## Testing

**Total: 116 tests**

- Phase 1: 13 tests (PDF loading)
- Phase 2: 40 tests (Text cleaning)
- Phase 3: 30 tests (Document chunking)
- Phase 4: 33 tests (Embedding generation)

All tests use dynamically generated data - no mocked outputs or hardcoded expectations.

## Design Principles

1. **Production-ready**: Full error handling, type hints, docstrings
2. **Clean architecture**: Separation of concerns, reusable components
3. **Dynamic operation**: No hardcoded content or mock data
4. **Comprehensive testing**: 116 tests covering all functionality
5. **Extensible**: Easy to add new phases or modify existing ones
6. **Local execution**: All models run locally, no API dependencies

## Use Cases

- Insurance policy document processing
- Legal document analysis
- Contract parsing and search
- Knowledge base construction
- RAG (Retrieval Augmented Generation) preparation
- Semantic search implementation
- Document similarity analysis

## Next Steps

This system now provides:
- ✅ Vector embedding generation
- Ready for vector database storage (Pinecone, Weaviate, ChromaDB)
- Ready for semantic search implementation
- Ready for question answering systems
- Ready for document comparison
- Ready for automated claim processing

## License

MIT License
