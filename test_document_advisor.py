"""
test_document_advisor.py
Comprehensive test suite for Document Advisor (Module 5)

Tests document recommendations, error handling, and integration scenarios.

Run with:
    pytest test_document_advisor.py -v
"""

import pytest
import logging
from Insurance_Claim_Agent.document_advisor import DocumentAdvisor, DocumentRecommendation, DocumentAdvisorError


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture
def advisor():
    """Fixture providing a Document Advisor instance."""
    return DocumentAdvisor()


# ==============================================================================
# TEST CASE 1: Flood Damage Documents
# ==============================================================================

def test_flood_damage_documents(advisor):
    """
    TEST 1: Flood Damage Documents
    
    Verify that flood damage claim returns correct document list.
    
    Given: A flood damage claim type
    When: get_required_documents() is called
    Then: Returns flood-specific documents
    """
    result = advisor.get_required_documents("Flood Damage")
    
    assert isinstance(result, DocumentRecommendation)
    assert result.claim_type == "Flood Damage"
    assert result.success is True
    assert len(result.required_documents) > 0
    
    # Verify specific documents
    assert "Insurance Policy Copy" in result.required_documents
    assert "Claim Form" in result.required_documents
    assert "Photographs of Damage" in result.required_documents
    assert "Government Flood Report" in result.required_documents
    assert "Identity Proof" in result.required_documents
    
    # Verify optional documents exist
    assert len(result.optional_documents) > 0
    assert len(result.notes) > 0
    
    print(f"\nRequired: {result.required_documents}")
    print(f"Optional: {result.optional_documents}")


# ==============================================================================
# TEST CASE 2: Vehicle Accident Documents
# ==============================================================================

def test_vehicle_accident_documents(advisor):
    """
    TEST 2: Vehicle Accident Documents
    
    Verify that vehicle accident claim returns correct documents.
    """
    result = advisor.get_required_documents("Vehicle Accident")
    
    assert result.claim_type == "Vehicle Accident"
    assert result.success is True
    
    # Verify specific vehicle accident documents
    assert "FIR Copy" in result.required_documents
    assert "Driving License" in result.required_documents
    assert "RC Book" in result.required_documents
    assert "Accident Photos" in result.required_documents
    
    print(f"\nRequired: {result.required_documents}")


# ==============================================================================
# TEST CASE 3: Theft Documents
# ==============================================================================

def test_theft_documents(advisor):
    """
    TEST 3: Theft Documents
    
    Verify that theft claim returns correct documents.
    """
    result = advisor.get_required_documents("Theft Claim")
    
    assert result.claim_type == "Theft Claim"
    assert result.success is True
    
    # Verify theft-specific documents
    assert "FIR Copy" in result.required_documents
    assert "Identity Proof" in result.required_documents
    
    print(f"\nRequired: {result.required_documents}")


# ==============================================================================
# TEST CASE 4: Hospitalization Documents
# ==============================================================================

def test_hospitalization_documents(advisor):
    """
    TEST 4: Hospitalization Documents
    
    Verify that hospitalization claim returns correct documents.
    """
    result = advisor.get_required_documents("Hospitalization Claim")
    
    assert result.claim_type == "Hospitalization Claim"
    assert result.success is True
    
    # Verify medical documents
    assert "Medical Bills" in result.required_documents
    assert "Discharge Summary" in result.required_documents
    assert "Doctor Reports" in result.required_documents
    
    print(f"\nRequired: {result.required_documents}")


# ==============================================================================
# TEST CASE 5: Fire Damage Documents
# ==============================================================================

def test_fire_damage_documents(advisor):
    """
    TEST 5: Fire Damage Documents
    
    Verify that fire damage claim returns correct documents.
    """
    result = advisor.get_required_documents("Fire Damage")
    
    assert result.claim_type == "Fire Damage"
    assert result.success is True
    
    # Verify fire-specific documents
    assert "Fire Department Report" in result.required_documents
    assert "Photographs of Damage" in result.required_documents
    
    print(f"\nRequired: {result.required_documents}")


# ==============================================================================
# TEST CASE 6: Unknown Claim Type
# ==============================================================================

def test_unknown_claim_type_returns_generic(advisor):
    """
    TEST 6: Unknown Claim Type
    
    Verify that unknown claim types return generic document list.
    
    Given: An unknown/unsupported claim type
    When: get_required_documents() is called
    Then: Returns generic document requirements
    """
    result = advisor.get_required_documents("Alien Invasion Damage")
    
    assert result.claim_type == "Alien Invasion Damage"
    assert result.success is True
    
    # Should return generic requirements
    assert "Insurance Policy Copy" in result.required_documents
    assert "Claim Form" in result.required_documents
    assert "Identity Proof" in result.required_documents
    
    # Should never return empty list
    assert len(result.required_documents) > 0
    
    print(f"\nGeneric Required: {result.required_documents}")


# ==============================================================================
# TEST CASE 7: Empty Claim Type
# ==============================================================================

def test_empty_claim_type_raises_error(advisor):
    """
    TEST 7: Empty Claim Type
    
    Verify that empty claim type raises DocumentAdvisorError.
    """
    with pytest.raises(DocumentAdvisorError) as exc_info:
        advisor.get_required_documents("")
    
    assert "claim type" in str(exc_info.value).lower()
    assert "empty" in str(exc_info.value).lower()
    
    print(f"\nCaught expected error: {exc_info.value}")


# ==============================================================================
# TEST CASE 8: None Claim Type
# ==============================================================================

def test_none_claim_type_raises_error(advisor):
    """
    TEST 8: None Claim Type
    
    Verify that None claim type raises DocumentAdvisorError.
    """
    with pytest.raises(DocumentAdvisorError) as exc_info:
        advisor.get_required_documents(None)
    
    assert "claim type" in str(exc_info.value).lower()
    assert "string" in str(exc_info.value).lower()
    
    print(f"\nCaught expected error: {exc_info.value}")


# ==============================================================================
# TEST CASE 9: Invalid Input Type
# ==============================================================================

def test_invalid_input_type_raises_error(advisor):
    """
    TEST 9: Invalid Input Type
    
    Verify that non-string claim type raises DocumentAdvisorError.
    """
    with pytest.raises(DocumentAdvisorError) as exc_info:
        advisor.get_required_documents(12345)
    
    assert "claim type" in str(exc_info.value).lower()
    assert "string" in str(exc_info.value).lower()
    
    print(f"\nCaught expected error: {exc_info.value}")


# ==============================================================================
# TEST CASE 10: Response Structure Validation
# ==============================================================================

def test_response_structure_validation(advisor):
    """
    TEST 10: Response Structure Validation
    
    Verify that DocumentRecommendation contains all required fields.
    """
    result = advisor.get_required_documents("Flood Damage")
    
    # Verify all fields exist
    assert hasattr(result, "claim_type")
    assert hasattr(result, "required_documents")
    assert hasattr(result, "optional_documents")
    assert hasattr(result, "notes")
    assert hasattr(result, "success")
    
    # Verify field types
    assert isinstance(result.claim_type, str)
    assert isinstance(result.required_documents, list)
    assert isinstance(result.optional_documents, list)
    assert isinstance(result.notes, str)
    assert isinstance(result.success, bool)
    
    # Verify list contents
    assert len(result.required_documents) > 0, "Required documents must not be empty"
    assert all(isinstance(doc, str) for doc in result.required_documents)
    assert all(isinstance(doc, str) for doc in result.optional_documents)
    
    print(f"\nResponse structure validated:")
    print(f"  - claim_type: {result.claim_type}")
    print(f"  - required_documents: {len(result.required_documents)} items")
    print(f"  - optional_documents: {len(result.optional_documents)} items")
    print(f"  - notes: {len(result.notes)} chars")
    print(f"  - success: {result.success}")


# ==============================================================================
# TEST CASE 11: Logging Verification
# ==============================================================================

def test_logging_verification(advisor, caplog):
    """
    TEST 11: Logging Verification
    
    Verify that appropriate logs are generated during document recommendation.
    """
    with caplog.at_level(logging.INFO):
        result = advisor.get_required_documents("Fire Damage")
    
    assert len(caplog.records) > 0, "Logs should be generated"
    
    log_messages = [record.message for record in caplog.records]
    log_text = " ".join(log_messages)
    
    assert "document" in log_text.lower() or "recommendation" in log_text.lower()
    
    print(f"\nLogs generated: {len(caplog.records)} entries")
    for record in caplog.records[:3]:
        print(f"  [{record.levelname}] {record.message}")


# ==============================================================================
# TEST CASE 12: Multiple Request Stability
# ==============================================================================

def test_multiple_request_stability(advisor):
    """
    TEST 12: Multiple Request Stability
    
    Verify stable operation across multiple consecutive requests.
    """
    claim_types = [
        "Flood Damage",
        "Vehicle Accident",
        "Theft Claim",
        "Hospitalization Claim",
        "Fire Damage",
        "Medical Emergency",
        "Property Damage",
        "Unknown Type 1",
        "Unknown Type 2",
        "Some Random Claim"
    ]
    
    results = []
    
    for idx, claim_type in enumerate(claim_types, 1):
        result = advisor.get_required_documents(claim_type)
        
        assert result.success is True, f"Request {idx} should succeed"
        assert len(result.required_documents) > 0, f"Request {idx} should have documents"
        assert len(result.notes) > 0, f"Request {idx} should have notes"
        
        results.append(result)
    
    assert len(results) == 10, "Should process all 10 requests"
    
    print(f"\nSuccessfully processed {len(results)} consecutive requests")
    print(f"Average required documents: {sum(len(r.required_documents) for r in results) / len(results):.1f}")


# ==============================================================================
# BONUS TESTS
# ==============================================================================

def test_case_insensitive_matching(advisor):
    """
    BONUS TEST: Case Insensitive Matching
    
    Verify that claim type matching is case-insensitive.
    """
    # Test various cases
    result1 = advisor.get_required_documents("FLOOD DAMAGE")
    result2 = advisor.get_required_documents("flood damage")
    result3 = advisor.get_required_documents("Flood Damage")
    result4 = advisor.get_required_documents("FlOoD DaMaGe")
    
    # All should return the same documents
    assert result1.required_documents == result2.required_documents
    assert result2.required_documents == result3.required_documents
    assert result3.required_documents == result4.required_documents
    
    print(f"\nCase-insensitive matching verified")


def test_no_empty_document_lists(advisor):
    """
    BONUS TEST: No Empty Lists
    
    Verify that required_documents is never empty.
    """
    test_types = [
        "Flood Damage",
        "Unknown Claim",
        "Random Type",
        "Fire Damage"
    ]
    
    for claim_type in test_types:
        result = advisor.get_required_documents(claim_type)
        assert len(result.required_documents) > 0, \
            f"Required documents should never be empty for {claim_type}"
    
    print(f"\nAll claim types return non-empty document lists")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
