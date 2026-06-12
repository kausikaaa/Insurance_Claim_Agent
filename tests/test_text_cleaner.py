"""Comprehensive tests for text cleaning module."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from text_cleaner import (
    clean_text,
    get_cleaning_stats,
    _normalize_line_endings,
    _normalize_whitespace,
    _remove_excessive_blank_lines,
    _remove_page_numbers,
    _remove_repeated_headers_footers,
    _find_repeated_sequences,
    _is_valid_header_footer_sequence,
    _filter_repeated_sequences
)
from config import CleaningConfig, DEFAULT_CONFIG


class TestBasicCleaning:
    """Test basic text cleaning operations."""
    
    def test_empty_string_returns_empty(self):
        """Test that empty string returns empty string."""
        assert clean_text("") == ""
        assert clean_text("   ") == ""
        assert clean_text("\n\n\n") == ""
    
    def test_whitespace_normalization(self):
        """Test removal of extra spaces between words."""
        text = "This  has   extra    spaces"
        result = clean_text(text)
        assert "  " not in result
        assert "This has extra spaces" in result
    
    def test_leading_trailing_whitespace_removal(self):
        """Test removal of leading and trailing whitespace."""
        text = "   Content here   "
        result = clean_text(text)
        assert result == "Content here"
    
    def test_tab_normalization(self):
        """Test that tabs are normalized to single spaces."""
        text = "Word1\t\tWord2\t\t\tWord3"
        result = clean_text(text)
        assert "\t" not in result
        assert "Word1 Word2 Word3" in result
    
    def test_line_ending_normalization(self):
        """Test normalization of different line endings."""
        text = "Line1\r\nLine2\rLine3\nLine4"
        result = clean_text(text)
        assert "\r\n" not in result
        assert "\r" not in result
        lines = result.split("\n")
        assert len(lines) == 4
    
    def test_excessive_blank_lines_removal(self):
        """Test removal of multiple consecutive blank lines."""
        text = "Line1\n\n\n\n\nLine2"
        result = clean_text(text)
        assert "\n\n\n" not in result
        assert "Line1" in result
        assert "Line2" in result
    
    def test_trailing_whitespace_on_lines(self):
        """Test removal of trailing whitespace on individual lines."""
        text = "Line1   \nLine2  \t\nLine3"
        result = clean_text(text)
        lines = result.split("\n")
        for line in lines:
            assert not line.endswith(" ")
            assert not line.endswith("\t")


class TestPageNumberRemoval:
    """Test page number removal functionality."""
    
    def test_simple_page_number_removal(self):
        """Test removal of simple page numbers."""
        text = "Content\n1\nMore content\n2\nEven more"
        result = clean_text(text)
        lines = result.split("\n")
        assert "1" not in [line.strip() for line in lines]
        assert "2" not in [line.strip() for line in lines]
        assert "Content" in result
    
    def test_page_word_with_number_removal(self):
        """Test removal of 'Page X' format."""
        text = "Content\nPage 1\nMore content\nPage 2\nEnd"
        result = clean_text(text)
        assert "Page 1" not in result
        assert "Page 2" not in result
        assert "Content" in result
    
    def test_page_x_of_y_removal(self):
        """Test removal of 'Page X of Y' format."""
        text = "Content\nPage 1 of 10\nMore\nPage 2 of 10\nEnd"
        result = clean_text(text)
        assert "Page 1 of 10" not in result
        assert "Page 2 of 10" not in result
        assert "Content" in result
    
    def test_x_of_y_format_removal(self):
        """Test removal of 'X of Y' format."""
        text = "Content\n1 of 10\nMore\n2 of 10\nEnd"
        result = clean_text(text)
        lines = [line.strip() for line in result.split("\n")]
        assert "1 of 10" not in lines
        assert "2 of 10" not in lines
    
    def test_bracketed_page_numbers_removal(self):
        """Test removal of bracketed page numbers."""
        text = "Content\n[ 1 ]\nMore\n[ 2 ]\nEnd"
        result = clean_text(text)
        assert "[ 1 ]" not in result
        assert "[ 2 ]" not in result
    
    def test_dashed_page_numbers_removal(self):
        """Test removal of dashed page numbers."""
        text = "Content\n- 1 -\nMore\n- 2 -\nEnd"
        result = clean_text(text)
        assert "- 1 -" not in result
        assert "- 2 -" not in result
    
    def test_preserve_numbers_in_content(self):
        """Test that numbers within content are preserved."""
        text = "The policy covers 1 million dollars in liability"
        result = clean_text(text)
        assert "1 million" in result
        assert "liability" in result


class TestHeaderFooterRemoval:
    """Test repeated header and footer removal."""
    
    def test_repeated_header_removal(self):
        """Test removal of repeated headers."""
        text = """INSURANCE POLICY
Content page 1
INSURANCE POLICY
Content page 2
INSURANCE POLICY
Content page 3"""
        result = clean_text(text)
        count = result.count("INSURANCE POLICY")
        assert count <= 1
    
    def test_repeated_footer_removal(self):
        """Test removal of repeated footers."""
        text = """Content page 1
Confidential Document
Content page 2
Confidential Document
Content page 3
Confidential Document"""
        result = clean_text(text)
        count = result.count("Confidential Document")
        assert count <= 1
    
    def test_multi_line_header_removal(self):
        """Test removal of multi-line repeated headers."""
        text = """ACME Insurance
Policy Document
Content 1
ACME Insurance
Policy Document
Content 2
ACME Insurance
Policy Document
Content 3"""
        result = clean_text(text)
        count = result.count("ACME Insurance")
        assert count <= 1
    
    def test_preserve_unique_content(self):
        """Test that unique content is preserved."""
        text = """Header Text
Unique content line 1
Header Text
Unique content line 2
Header Text
Unique content line 3"""
        result = clean_text(text)
        assert "Unique content line 1" in result
        assert "Unique content line 2" in result
        assert "Unique content line 3" in result
    
    def test_no_removal_if_not_repeated_enough(self):
        """Test that text appearing only once is not removed."""
        text = """Single occurrence header
Content here
Different text
More content"""
        result = clean_text(text)
        assert "Single occurrence header" in result
        assert "Content here" in result


class TestMixedArtifactRemoval:
    """Test removal of mixed artifacts."""
    
    def test_combined_page_numbers_and_headers(self):
        """Test removal of both page numbers and headers."""
        text = """Page 1
COMPANY HEADER
Policy content here
Page 2
COMPANY HEADER
More policy content
Page 3
COMPANY HEADER
Final content"""
        result = clean_text(text)
        assert "Page 1" not in result
        assert "Page 2" not in result
        assert "Page 3" not in result
        count = result.count("COMPANY HEADER")
        assert count <= 1
        assert "Policy content here" in result
    
    def test_headers_footers_and_page_numbers(self):
        """Test removal of headers, footers, and page numbers."""
        text = """HEADER
Content 1
Footer Line
1
HEADER
Content 2
Footer Line
2"""
        result = clean_text(text)
        lines = [line.strip() for line in result.split("\n") if line.strip()]
        assert "1" not in lines
        assert "2" not in lines
        assert any("Content 1" in line for line in lines)
        assert any("Content 2" in line for line in lines)
    
    def test_excessive_whitespace_with_artifacts(self):
        """Test removal of whitespace along with artifacts."""
        text = """Page 1   

HEADER   

Content    with    spaces

Footer  

2"""
        result = clean_text(text)
        assert "Page 1" not in result
        assert "   " not in result
        assert "\n\n\n" not in result
        assert "Content with spaces" in result


class TestContentPreservation:
    """Test that actual content is preserved."""
    
    def test_preserve_policy_numbers(self):
        """Test that policy numbers are preserved."""
        text = "Policy Number: INS-2024-001234\nCoverage: Full"
        result = clean_text(text)
        assert "INS-2024-001234" in result
        assert "Coverage: Full" in result
    
    def test_preserve_dates(self):
        """Test that dates are preserved."""
        text = "Effective Date: January 1, 2024\nExpiration: December 31, 2024"
        result = clean_text(text)
        assert "January 1, 2024" in result
        assert "December 31, 2024" in result
    
    def test_preserve_dollar_amounts(self):
        """Test that dollar amounts are preserved."""
        text = "Coverage: $100,000\nDeductible: $1,000"
        result = clean_text(text)
        assert "$100,000" in result
        assert "$1,000" in result
    
    def test_preserve_paragraphs(self):
        """Test that paragraph structure is preserved."""
        text = """First paragraph with content.

Second paragraph with more content.

Third paragraph here."""
        result = clean_text(text)
        assert "First paragraph" in result
        assert "Second paragraph" in result
        assert "Third paragraph" in result
    
    def test_preserve_list_items(self):
        """Test that list items are preserved."""
        text = """Coverage includes:
- Liability
- Collision
- Comprehensive"""
        result = clean_text(text)
        assert "Liability" in result
        assert "Collision" in result
        assert "Comprehensive" in result


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_very_short_text(self):
        """Test handling of very short text."""
        text = "Hi"
        result = clean_text(text)
        assert result == "Hi"
    
    def test_only_page_numbers(self):
        """Test text containing only page numbers."""
        text = "1\n2\n3\n4\n5"
        result = clean_text(text)
        assert result == ""
    
    def test_only_whitespace_variations(self):
        """Test text with only various whitespace."""
        text = "   \t\t\n\n\n   \t  "
        result = clean_text(text)
        assert result == ""
    
    def test_special_characters_preserved(self):
        """Test that special characters are preserved."""
        text = "Coverage: $100,000 (including 5% discount)"
        result = clean_text(text)
        assert "$" in result
        assert "(" in result
        assert ")" in result
        assert "%" in result
    
    def test_numbers_in_middle_of_sentences(self):
        """Test that inline numbers are preserved."""
        text = "The policy covers 3 types of claims with 100% coverage"
        result = clean_text(text)
        assert "3 types" in result
        assert "100%" in result


class TestStatisticsFunction:
    """Test the cleaning statistics function."""
    
    def test_stats_calculation(self):
        """Test that statistics are calculated correctly."""
        raw = "Line1\n\n\nLine2   \nPage 1\nLine3"
        cleaned = clean_text(raw)
        stats = get_cleaning_stats(raw, cleaned)
        
        assert stats['original_length'] > 0
        assert stats['cleaned_length'] > 0
        assert stats['original_lines'] > 0
        assert stats['cleaned_lines'] > 0
        assert stats['characters_removed'] >= 0
        assert stats['lines_removed'] >= 0
    
    def test_stats_with_no_cleaning(self):
        """Test statistics when no cleaning is performed."""
        text = "Simple text"
        cleaned = clean_text(text)
        stats = get_cleaning_stats(text, cleaned)
        
        assert stats['characters_removed'] >= 0
        assert stats['lines_removed'] >= 0


class TestHelperFunctions:
    """Test individual helper functions."""
    
    def test_normalize_line_endings_windows(self):
        """Test Windows line ending normalization."""
        text = "Line1\r\nLine2\r\nLine3"
        result = _normalize_line_endings(text)
        assert "\r\n" not in result
        assert result.count("\n") == 2
    
    def test_normalize_line_endings_mac(self):
        """Test Mac line ending normalization."""
        text = "Line1\rLine2\rLine3"
        result = _normalize_line_endings(text)
        assert "\r" not in result
        assert result.count("\n") == 2
    
    def test_is_valid_header_footer_sequence(self):
        """Test header/footer sequence validation."""
        valid = ("HEADER TEXT",)
        invalid_long = ("This is a very long line with more than one hundred characters that should not be considered a header or footer",)
        
        assert _is_valid_header_footer_sequence(valid, DEFAULT_CONFIG)
        assert not _is_valid_header_footer_sequence(invalid_long, DEFAULT_CONFIG)
    
    def test_find_repeated_sequences(self):
        """Test finding repeated sequences."""
        lines = ["HEADER", "Content1", "HEADER", "Content2", "HEADER", "Content3"]
        repeated = _find_repeated_sequences(lines, DEFAULT_CONFIG)
        assert len(repeated) > 0


class TestReturnTypes:
    """Test return type validation."""
    
    def test_return_type_is_string(self):
        """Test that clean_text always returns a string."""
        assert isinstance(clean_text("test"), str)
        assert isinstance(clean_text(""), str)
        assert isinstance(clean_text("   "), str)
    
    def test_stats_return_type_is_dict(self):
        """Test that get_cleaning_stats returns a dictionary."""
        stats = get_cleaning_stats("raw", "clean")
        assert isinstance(stats, dict)
        assert 'original_length' in stats
        assert 'cleaned_length' in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
