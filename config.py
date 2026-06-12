"""Configuration for text cleaning operations."""

import re
from typing import List, Pattern


class CleaningConfig:
    """Configuration class for text cleaning rules and patterns."""
    
    PAGE_NUMBER_PATTERNS: List[Pattern] = [
        re.compile(r'^\s*Page\s+\d+\s*$', re.IGNORECASE | re.MULTILINE),
        re.compile(r'^\s*Page\s+\d+\s+of\s+\d+\s*$', re.IGNORECASE | re.MULTILINE),
        re.compile(r'^\s*\d+\s+of\s+\d+\s*$', re.MULTILINE),
        re.compile(r'^\s*\[\s*\d+\s*\]\s*$', re.MULTILINE),
        re.compile(r'^\s*-\s*\d+\s*-\s*$', re.MULTILINE),
        re.compile(r'^\s*\d+\s*$', re.MULTILINE),
    ]
    
    WHITESPACE_PATTERNS: List[tuple] = [
        (re.compile(r'[ \t]+'), ' '),
        (re.compile(r'\n{3,}'), '\n\n'),
        (re.compile(r'[ \t]+\n'), '\n'),
        (re.compile(r'\n[ \t]+'), '\n'),
    ]
    
    MIN_HEADER_FOOTER_OCCURRENCES: int = 2
    
    MIN_LINE_LENGTH_FOR_CONTENT: int = 10
    
    MAX_HEADER_FOOTER_LINE_COUNT: int = 5
    
    SIMILARITY_THRESHOLD: float = 0.85


DEFAULT_CONFIG = CleaningConfig()
