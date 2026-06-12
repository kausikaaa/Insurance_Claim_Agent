"""
test_claim_analyzer.py
Comprehensive test suite for Claim Eligibility Analyzer (Module 4)

Tests business rule application, confidence scoring, error handling,
and integration scenarios for insurance claim analysis.

Run with:
    pytest test_claim_analyzer.py -v
"""

import pytest
import logging
from datetime import datetime
from Insurance_Claim_Agent.claim_analyzer import ClaimAnalyzer, ClaimAnalysisResult, ClaimAnalyzerError


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture
def analyzer():
    """Fixture providing a Claim Analyzer instance."""
    return ClaimAnalyzer()


# ==============================================================================
# TEST CASE 1: Covered Claim
# ==============================================================================

def test_covered_claim_returns_likely_eligible(analyzer):
    """
    TEST 1: Covered Claim
    
    Verify that claims with positive coverage indicators are marked as eligible.
    
    Given: A flood damage claim with explicit coverage language
    When: analyze_claim() is called
    Then: Status is "Likely Eligible" with high confidence
    """
    result = analyzer.analyze_claim(
        claim_type="Flood Damage",
        policy_context="Flood damage is covered under Section 4.2 of this policy."
    )
    
    assert isinstance(result, ClaimAnalysisResult)
    assert result.status == "Likely Eligible"
    assert result.confidence >= 0.70
    assert result.success is True
    assert result.claim_type == "Flood Damage"
    assert len(result.reason) > 0
    assert isinstance(result.analyzed_at, datetime)
    
    print(f"\nStatus: {result.status}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reason: {result.reason}")


# ==============================================================================
# TEST CASE 2: Excluded Claim
# ==============================================================================

def test_excluded_claim_returns_likely_not_eligible(analyzer):
    """
    TEST 2: Excluded Claim
    
    Verify that claims with exclusion language are marked as ineligible.
    
    Given: A cosmetic surgery claim with explicit exclusion
    When: analyze_claim() is called
    Then: Status is "Likely Not Eligible" with high confidence
    """
    result = analyzer.analyze_claim(
        claim_type="Cosmetic Surgery",
        policy_context="Cosmetic procedures are excluded from coverage under this policy."
    )
    
    assert result.status == "Likely Not Eligible"
    assert result.confidence >= 0.70
    assert result.success is True
    assert "excluded" in result.reason.lower() or "not" in result.reason.lower()
    
    print(f"\nStatus: {result.status}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reason: {result.reason}")


# ==============================================================================
# TEST CASE 3: Ambiguous Claim
# ==============================================================================

def test_ambiguous_claim_requires_manual_review(analyzer):
    """
    TEST 3: Ambiguous Claim
    
    Verify that claims with conditional language require manual review.
    
    Given: A claim with conditional coverage language
    When: analyze_claim() is called
    Then: Status is "Requires Manual Review"
    """
    result = analyzer.analyze_claim(
        claim_type="Special Medical Procedure",
        policy_context="Coverage depends on prior authorization and medical necessity."
    )
    
    assert result.status == "Requires Manual Review"
    assert 0.50 <= result.confidence <= 0.80
    assert result.success is True
    
    print(f"\nStatus: {result.status}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reason: {result.reason}")


# ==============================================================================
# TEST CASE 4: Empty Claim Type
# ==============================================================================

def test_empty_claim_type_raises_error(analyzer):
    """
    TEST 4: Empty Claim Type
    
    Verify that empty claim type raises ClaimAnalyzerError.
    
    Given: An empty claim type string
    When: analyze_claim() is called
    Then: ClaimAnalyzerError is raised
    """
    with pytest.raises(ClaimAnalyzerError) as exc_info:
        analyzer.analyze_claim(
            claim_type="",
            policy_context="Some policy context"
        )
    
    assert "claim type" in str(exc_info.value).lower()
    assert "empty" in str(exc_info.value).lower()
    
    print(f"\nCaught expected error: {exc_info.value}")


# ==============================================================================
# TEST CASE 5: Empty Context
# ==============================================================================

def test_empty_context_raises_error(analyzer):
    """
    TEST 5: Empty Context
    
    Verify that empty policy context raises ClaimAnalyzerError.
    
    Given: An empty policy context string
    When: analyze_claim() is called
    Then: ClaimAnalyzerError is raised
    """
    with pytest.raises(ClaimAnalyzerError) as exc_info:
        analyzer.analyze_claim(
            claim_type="Fire Damage",
            policy_context=""
        )
    
    assert "context" in str(exc_info.value).lower()
    assert "empty" in str(exc_info.value).lower()
    
    print(f"\nCaught expected error: {exc_info.value}")


# ==============================================================================
# TEST CASE 6: Invalid Input Types
# ==============================================================================

def test_invalid_claim_type_raises_error(analyzer):
    """
    TEST 6a: Invalid Input Types - Claim Type
    
    Verify that non-string claim type raises ClaimAnalyzerError.
    """
    with pytest.raises(ClaimAnalyzerError) as exc_info:
        analyzer.analyze_claim(
            claim_type=None,
            policy_context="Some context"
        )
    
    assert "claim type" in str(exc_info.value).lower()
    assert "string" in str(exc_info.value).lower()
    
    print(f"\nCaught expected error: {exc_info.value}")


def test_invalid_context_type_raises_error(analyzer):
    """
    TEST 6b: Invalid Input Types - Context
    
    Verify that non-string context raises ClaimAnalyzerError.
    """
    with pytest.raises(ClaimAnalyzerError) as exc_info:
        analyzer.analyze_claim(
            claim_type="Fire Damage",
            policy_context=12345
        )
    
    assert "context" in str(exc_info.value).lower()
    assert "string" in str(exc_info.value).lower()
    
    print(f"\nCaught expected error: {exc_info.value}")


# ==============================================================================
# TEST CASE 7: Confidence Score Validation
# ==============================================================================

def test_confidence_score_validation(analyzer):
    """
    TEST 7: Confidence Score Validation
    
    Verify that confidence scores are within valid range (0.0-1.0).
    
    Given: Various claim scenarios
    When: analyze_claim() is called
    Then: Confidence is between 0.0 and 1.0
    """
    test_cases = [
        ("Flood Damage", "Flood damage is covered and payable."),
        ("Theft", "Theft is not covered and excluded."),
        ("Surgery", "Surgery coverage depends on prior approval."),
        ("Fire Damage", "Fire damage."),  # Minimal context
    ]
    
    for claim_type, context in test_cases:
        result = analyzer.analyze_claim(claim_type, context)
        
        assert 0.0 <= result.confidence <= 1.0, \
            f"Confidence {result.confidence} out of range for {claim_type}"
        assert isinstance(result.confidence, float), \
            f"Confidence must be float, got {type(result.confidence)}"
        
        print(f"\n{claim_type}: confidence={result.confidence:.2f} (valid)")


# ==============================================================================
# TEST CASE 8: Response Structure Validation
# ==============================================================================

def test_response_structure_validation(analyzer):
    """
    TEST 8: Response Structure Validation
    
    Verify that ClaimAnalysisResult contains all required fields.
    
    Given: A valid claim analysis
    When: Result is returned
    Then: All fields exist with correct types
    """
    result = analyzer.analyze_claim(
        claim_type="Medical Treatment",
        policy_context="Medical treatment is covered under this policy."
    )
    
    # Verify all fields exist
    assert hasattr(result, "claim_type")
    assert hasattr(result, "status")
    assert hasattr(result, "confidence")
    assert hasattr(result, "reason")
    assert hasattr(result, "analyzed_at")
    assert hasattr(result, "success")
    
    # Verify field types
    assert isinstance(result.claim_type, str)
    assert isinstance(result.status, str)
    assert isinstance(result.confidence, float)
    assert isinstance(result.reason, str)
    assert isinstance(result.analyzed_at, datetime)
    assert isinstance(result.success, bool)
    
    # Verify status is one of the valid options
    assert result.status in [
        "Likely Eligible",
        "Likely Not Eligible",
        "Requires Manual Review"
    ]
    
    print(f"\nResponse structure validated:")
    print(f"  - claim_type: {result.claim_type}")
    print(f"  - status: {result.status}")
    print(f"  - confidence: {result.confidence:.2f}")
    print(f"  - reason: {result.reason[:50]}...")
    print(f"  - analyzed_at: {result.analyzed_at}")
    print(f"  - success: {result.success}")


# ==============================================================================
# TEST CASE 9: Logging Verification
# ==============================================================================

def test_logging_verification(analyzer, caplog):
    """
    TEST 9: Logging Verification
    
    Verify that appropriate logs are generated during analysis.
    
    Given: A claim analyzer with logging enabled
    When: analyze_claim() is called
    Then: Logs contain analysis information
    """
    with caplog.at_level(logging.INFO):
        result = analyzer.analyze_claim(
            claim_type="Accident",
            policy_context="Accident claims are covered."
        )
    
    assert len(caplog.records) > 0, "Logs should be generated"
    
    log_messages = [record.message for record in caplog.records]
    log_text = " ".join(log_messages)
    
    assert "started" in log_text.lower() or "analysis" in log_text.lower()
    assert "completed" in log_text.lower() or "status" in log_text.lower()
    
    print(f"\nLogs generated: {len(caplog.records)} entries")
    for record in caplog.records[:3]:
        print(f"  [{record.levelname}] {record.message}")


# ==============================================================================
# TEST CASE 10: Multiple Analysis Stability
# ==============================================================================

def test_multiple_analysis_stability(analyzer):
    """
    TEST 10: Multiple Analysis Stability
    
    Verify stable operation across multiple consecutive analyses.
    
    Given: A claim analyzer
    When: 10 consecutive analyses are performed
    Then: All succeed without degradation
    """
    test_claims = [
        ("Flood Damage", "Flood damage is covered."),
        ("Fire Damage", "Fire damage is covered."),
        ("Theft", "Theft is excluded."),
        ("Earthquake", "Earthquake damage is not covered."),
        ("Surgery", "Surgery requires approval."),
        ("Medical Treatment", "Medical treatment is payable."),
        ("Dental Work", "Dental work is excluded."),
        ("Vision Care", "Vision care depends on plan."),
        ("Prescription Drugs", "Prescription drugs are covered."),
        ("Cosmetic Procedure", "Cosmetic procedures are not eligible."),
    ]
    
    results = []
    
    for idx, (claim_type, context) in enumerate(test_claims, 1):
        result = analyzer.analyze_claim(claim_type, context)
        
        assert result.success is True, f"Analysis {idx} should succeed"
        assert result.status in ["Likely Eligible", "Likely Not Eligible", "Requires Manual Review"]
        assert 0.0 <= result.confidence <= 1.0
        assert len(result.reason) > 0
        
        results.append(result)
    
    assert len(results) == 10, "Should process all 10 analyses"
    
    print(f"\nSuccessfully processed {len(results)} consecutive analyses")
    print(f"Status distribution:")
    print(f"  - Likely Eligible: {sum(1 for r in results if r.status == 'Likely Eligible')}")
    print(f"  - Likely Not Eligible: {sum(1 for r in results if r.status == 'Likely Not Eligible')}")
    print(f"  - Requires Manual Review: {sum(1 for r in results if r.status == 'Requires Manual Review')}")


# ==============================================================================
# BONUS TESTS
# ==============================================================================

def test_multiple_positive_keywords_increase_confidence(analyzer):
    """
    BONUS TEST: Multiple Keywords
    
    Verify that multiple positive keywords increase confidence.
    """
    # Single keyword
    result1 = analyzer.analyze_claim(
        "Claim A",
        "This claim is covered."
    )
    
    # Multiple keywords
    result2 = analyzer.analyze_claim(
        "Claim B",
        "This claim is covered, eligible, and payable."
    )
    
    assert result2.confidence >= result1.confidence, \
        "Multiple keywords should increase or maintain confidence"
    
    print(f"\nSingle keyword confidence: {result1.confidence:.2f}")
    print(f"Multiple keywords confidence: {result2.confidence:.2f}")


def test_negative_keywords_override_positive(analyzer):
    """
    BONUS TEST: Keyword Priority
    
    Verify that negative keywords take priority over positive ones.
    """
    result = analyzer.analyze_claim(
        "Mixed Claim",
        "While some procedures are covered, cosmetic surgery is excluded."
    )
    
    assert result.status == "Likely Not Eligible", \
        "Exclusion keywords should take priority"
    
    print(f"\nStatus: {result.status}")
    print(f"Reason: {result.reason}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
