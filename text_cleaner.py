"""Text cleaning module for insurance policy documents."""

import re
from typing import List, Set, Dict
from collections import Counter
from config import CleaningConfig, DEFAULT_CONFIG


def clean_text(raw_text: str, config: CleaningConfig = DEFAULT_CONFIG) -> str:
    """
    Clean and normalize extracted PDF text.
    
    Args:
        raw_text: Raw text extracted from PDF.
        config: Configuration object with cleaning rules.
        
    Returns:
        Cleaned and normalized text.
    """
    if not raw_text or not raw_text.strip():
        return ""
    
    text = raw_text
    text = _normalize_line_endings(text)
    text = _remove_page_numbers(text, config)
    text = _remove_repeated_headers_footers(text, config)
    text = _normalize_whitespace(text, config)
    text = _remove_excessive_blank_lines(text)
    text = text.strip()
    
    return text


def _normalize_line_endings(text: str) -> str:
    """
    Normalize line endings to Unix style (LF).
    
    Args:
        text: Input text with potentially mixed line endings.
        
    Returns:
        Text with normalized line endings.
    """
    text = text.replace('\r\n', '\n')
    text = text.replace('\r', '\n')
    return text


def _normalize_whitespace(text: str, config: CleaningConfig) -> str:
    """
    Normalize whitespace by removing extra spaces and tabs.
    
    Args:
        text: Input text.
        config: Configuration object.
        
    Returns:
        Text with normalized whitespace.
    """
    for pattern, replacement in config.WHITESPACE_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def _remove_excessive_blank_lines(text: str) -> str:
    """
    Remove multiple consecutive blank lines, keeping at most one.
    
    Args:
        text: Input text.
        
    Returns:
        Text with excessive blank lines removed.
    """
    lines = text.split('\n')
    result = []
    prev_blank = False
    
    for line in lines:
        is_blank = not line.strip()
        if is_blank:
            if not prev_blank:
                result.append(line)
            prev_blank = True
        else:
            result.append(line)
            prev_blank = False
    
    return '\n'.join(result)


def _remove_page_numbers(text: str, config: CleaningConfig) -> str:
    """
    Remove page number artifacts from text.
    
    Args:
        text: Input text.
        config: Configuration object.
        
    Returns:
        Text with page numbers removed.
    """
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        is_page_number = False
        
        for pattern in config.PAGE_NUMBER_PATTERNS:
            if pattern.match(line):
                is_page_number = True
                break
        
        if not is_page_number:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def _remove_repeated_headers_footers(text: str, config: CleaningConfig) -> str:
    """
    Detect and remove repeated headers and footers algorithmically.
    
    Args:
        text: Input text.
        config: Configuration object.
        
    Returns:
        Text with repeated headers and footers removed.
    """
    lines = text.split('\n')
    
    if len(lines) < 3:
        return text
    
    repeated_sequences = _find_repeated_sequences(lines, config)
    
    if not repeated_sequences:
        return text
    
    cleaned_lines = _filter_repeated_sequences(lines, repeated_sequences)
    
    return '\n'.join(cleaned_lines)


def _find_repeated_sequences(lines: List[str], config: CleaningConfig) -> Set[tuple]:
    """
    Find repeated line sequences that appear multiple times.
    
    Args:
        lines: List of text lines.
        config: Configuration object.
        
    Returns:
        Set of tuples representing repeated sequences.
    """
    repeated = set()
    sequence_counter = Counter()
    
    for seq_length in range(1, config.MAX_HEADER_FOOTER_LINE_COUNT + 1):
        for i in range(len(lines) - seq_length + 1):
            sequence = tuple(lines[i:i + seq_length])
            
            if _is_valid_header_footer_sequence(sequence, config):
                sequence_counter[sequence] += 1
    
    for sequence, count in sequence_counter.items():
        if count >= config.MIN_HEADER_FOOTER_OCCURRENCES:
            repeated.add(sequence)
    
    return repeated


def _is_valid_header_footer_sequence(sequence: tuple, config: CleaningConfig) -> bool:
    """
    Check if a sequence is a valid header/footer candidate.
    
    Args:
        sequence: Tuple of lines.
        config: Configuration object.
        
    Returns:
        True if valid candidate, False otherwise.
    """
    if not sequence:
        return False
    
    non_empty_lines = [line for line in sequence if line.strip()]
    
    if not non_empty_lines:
        return False
    
    for line in non_empty_lines:
        stripped = line.strip()
        if len(stripped) > 100:
            return False
        if len(stripped.split()) > 15:
            return False
    
    return True


def _filter_repeated_sequences(lines: List[str], repeated_sequences: Set[tuple]) -> List[str]:
    """
    Filter out repeated sequences from lines while preserving first occurrence.
    
    Args:
        lines: List of text lines.
        repeated_sequences: Set of repeated sequences to remove.
        
    Returns:
        Filtered list of lines.
    """
    if not repeated_sequences:
        return lines
    
    sorted_sequences = sorted(repeated_sequences, key=len, reverse=True)
    
    kept_lines = [True] * len(lines)
    first_occurrence_kept = {}
    
    for sequence in sorted_sequences:
        seq_len = len(sequence)
        occurrence_count = 0
        
        i = 0
        while i <= len(lines) - seq_len:
            if tuple(lines[i:i + seq_len]) == sequence:
                occurrence_count += 1
                
                if occurrence_count > 1:
                    for j in range(i, i + seq_len):
                        kept_lines[j] = False
                    i += seq_len
                else:
                    i += seq_len
            else:
                i += 1
    
    result = [line for i, line in enumerate(lines) if kept_lines[i]]
    
    return result


def get_cleaning_stats(raw_text: str, cleaned_text: str) -> Dict[str, int]:
    """
    Calculate statistics about the cleaning process.
    
    Args:
        raw_text: Original raw text.
        cleaned_text: Cleaned text.
        
    Returns:
        Dictionary with cleaning statistics.
    """
    return {
        'original_length': len(raw_text),
        'cleaned_length': len(cleaned_text),
        'original_lines': len(raw_text.split('\n')),
        'cleaned_lines': len(cleaned_text.split('\n')),
        'characters_removed': len(raw_text) - len(cleaned_text),
        'lines_removed': len(raw_text.split('\n')) - len(cleaned_text.split('\n'))
    }
