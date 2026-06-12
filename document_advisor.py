"""
document_advisor.py
Module 5: Document Advisor for AI-Powered Insurance Claim Assistant

Recommends required and optional documents based on claim type.
Provides document checklists to help users prepare claim submissions.
"""

import logging
from dataclasses import dataclass
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


@dataclass
class DocumentRecommendation:
    """Structured document recommendation for a claim type."""
    claim_type: str
    required_documents: List[str]
    optional_documents: List[str]
    notes: str
    success: bool


class DocumentAdvisorError(Exception):
    """Raised when document recommendation fails."""


class DocumentAdvisor:
    """
    Recommends required and optional documents based on claim type.

    Maintains a knowledge base of document requirements for common
    insurance claim types. Provides generic recommendations for
    unknown claim types.

    Example:
        >>> advisor = DocumentAdvisor()
        >>> result = advisor.get_required_documents("Flood Damage")
        >>> print(result.required_documents)
        ['Insurance Policy Copy', 'Claim Form', ...]
    """

    # Document requirements database
    _CLAIM_DOCUMENTS = {
        "flood damage": {
            "required": [
                "Insurance Policy Copy",
                "Claim Form",
                "Photographs of Damage",
                "Government Flood Report",
                "Identity Proof"
            ],
            "optional": [
                "Repair Estimates",
                "Witness Statements"
            ],
            "notes": "Additional documents may be requested during claim processing."
        },
        "vehicle accident": {
            "required": [
                "Insurance Policy Copy",
                "Claim Form",
                "FIR Copy",
                "Driving License",
                "RC Book",
                "Accident Photos"
            ],
            "optional": [
                "Medical Bills (if injuries)",
                "Witness Statements",
                "Police Investigation Report"
            ],
            "notes": "Submit all documents within 48 hours of the accident."
        },
        "theft claim": {
            "required": [
                "Insurance Policy Copy",
                "Claim Form",
                "FIR Copy",
                "Identity Proof"
            ],
            "optional": [
                "List of Stolen Items",
                "Purchase Receipts",
                "Witness Statements"
            ],
            "notes": "FIR must be filed within 24 hours of discovering the theft."
        },
        "hospitalization claim": {
            "required": [
                "Insurance Policy Copy",
                "Medical Bills",
                "Discharge Summary",
                "Doctor Reports",
                "Identity Proof"
            ],
            "optional": [
                "Diagnostic Test Reports",
                "Prescription Receipts",
                "Hospital Registration Documents"
            ],
            "notes": "Pre-authorization required for planned hospitalizations."
        },
        "fire damage": {
            "required": [
                "Insurance Policy Copy",
                "Claim Form",
                "Fire Department Report",
                "Photographs of Damage"
            ],
            "optional": [
                "Repair Estimates",
                "List of Damaged Items",
                "Property Valuation Report"
            ],
            "notes": "Fire Department report is mandatory for all fire damage claims."
        },
        "medical emergency": {
            "required": [
                "Insurance Policy Copy",
                "Medical Bills",
                "Doctor Reports",
                "Emergency Room Documents",
                "Identity Proof"
            ],
            "optional": [
                "Ambulance Bills",
                "Diagnostic Reports",
                "Treatment Receipts"
            ],
            "notes": "Emergency claims must be intimated within 24 hours."
        },
        "property damage": {
            "required": [
                "Insurance Policy Copy",
                "Claim Form",
                "Photographs of Damage",
                "Police Report (if applicable)",
                "Identity Proof"
            ],
            "optional": [
                "Repair Estimates",
                "Property Survey Report",
                "Witness Statements"
            ],
            "notes": "Document all damage with clear photographs from multiple angles."
        }
    }

    # Generic requirements for unknown claim types
    _GENERIC_DOCUMENTS = {
        "required": [
            "Insurance Policy Copy",
            "Claim Form",
            "Identity Proof"
        ],
        "optional": [
            "Supporting Documents",
            "Relevant Reports"
        ],
        "notes": "Please contact customer service for specific document requirements for your claim type."
    }

    def __init__(self) -> None:
        """Initialize the Document Advisor."""
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info("DocumentAdvisor initialized")

    def get_required_documents(self, claim_type: str) -> DocumentRecommendation:
        """
        Get required and optional documents for a claim type.

        Uses a knowledge base of common claim types to provide document
        checklists. Returns generic requirements for unknown claim types.

        Args:
            claim_type: Type of insurance claim (e.g., "Flood Damage")

        Returns:
            DocumentRecommendation with required/optional documents and notes

        Raises:
            DocumentAdvisorError: If claim_type is invalid
        """
        self._logger.info("Document recommendation requested | claim_type=%s", claim_type)

        try:
            # Validate input
            self._validate_claim_type(claim_type)

            # Normalize claim type (case-insensitive matching)
            claim_type_normalized = claim_type.strip().lower()

            # Find matching documents
            if claim_type_normalized in self._CLAIM_DOCUMENTS:
                doc_info = self._CLAIM_DOCUMENTS[claim_type_normalized]
                self._logger.info(
                    "Document recommendation found | claim_type=%s | required_count=%d",
                    claim_type,
                    len(doc_info["required"])
                )
            else:
                # Return generic requirements for unknown claim types
                doc_info = self._GENERIC_DOCUMENTS
                self._logger.info(
                    "Unknown claim type, using generic documents | claim_type=%s",
                    claim_type
                )

            # Build result
            result = DocumentRecommendation(
                claim_type=claim_type,
                required_documents=doc_info["required"].copy(),
                optional_documents=doc_info["optional"].copy(),
                notes=doc_info["notes"],
                success=True
            )

            return result

        except DocumentAdvisorError:
            raise

        except Exception as exc:
            error_msg = f"Unexpected error during document recommendation: {exc}"
            self._logger.error(error_msg)
            raise DocumentAdvisorError(error_msg) from exc

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_claim_type(self, claim_type: str) -> None:
        """Validate claim type input."""
        if not isinstance(claim_type, str):
            raise DocumentAdvisorError(
                f"Claim type must be a string, got {type(claim_type).__name__}."
            )

        if not claim_type.strip():
            raise DocumentAdvisorError("Claim type must not be empty.")
