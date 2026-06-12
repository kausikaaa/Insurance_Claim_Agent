"""
claim_analyzer.py
Module 4: Claim Eligibility Analyzer for AI-Powered Insurance Claim Assistant

Provides preliminary claim eligibility assessment based on policy context.
Uses business rules to determine likelihood of claim approval.

Note: This is a preliminary assessment tool, not a legal decision system.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


@dataclass
class ClaimAnalysisResult:
    """Structured result from claim eligibility analysis."""
    claim_type: str
    status: Literal["Likely Eligible", "Likely Not Eligible", "Requires Manual Review"]
    confidence: float
    reason: str
    analyzed_at: datetime
    success: bool


class ClaimAnalyzerError(Exception):
    """Raised when claim analysis fails."""


class ClaimAnalyzer:
    """
    Analyzes claim eligibility based on policy context using business rules.

    Provides preliminary assessment with confidence scores and human-readable
    explanations. Results indicate likelihood, not final decisions.

    Possible Statuses:
    - "Likely Eligible": Policy context suggests claim should be covered
    - "Likely Not Eligible": Policy context suggests claim is excluded
    - "Requires Manual Review": Context is ambiguous or incomplete

    Example:
        >>> analyzer = ClaimAnalyzer()
        >>> result = analyzer.analyze_claim(
        ...     claim_type="Flood Damage",
        ...     policy_context="Flood damage is covered under Section 4.2."
        ... )
        >>> print(result.status)
        "Likely Eligible"
    """

    # Business rule keywords
    _POSITIVE_KEYWORDS = [
        "covered", "eligible", "included", "payable", "entitled",
        "approved", "reimbursable", "compensable", "insured"
    ]

    _NEGATIVE_KEYWORDS = [
        "excluded", "not covered", "rejected", "ineligible", "denied",
        "not eligible", "not included", "not payable", "prohibited",
        "not insured", "exempted", "not reimbursable"
    ]

    _AMBIGUOUS_KEYWORDS = [
        "may be covered", "subject to", "depends on", "conditional",
        "requires approval", "prior authorization", "case by case",
        "at discretion", "under certain conditions", "may require"
    ]

    def __init__(self) -> None:
        """Initialize the Claim Analyzer."""
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info("ClaimAnalyzer initialized")

    def analyze_claim(
        self,
        claim_type: str,
        policy_context: str
    ) -> ClaimAnalysisResult:
        """
        Analyze claim eligibility based on policy context.

        Uses business rules to assess likelihood of claim approval:
        1. Checks for positive coverage indicators
        2. Checks for explicit exclusions
        3. Checks for ambiguous/conditional language
        4. Calculates confidence score
        5. Generates human-readable explanation

        Args:
            claim_type: Type of claim (e.g., "Flood Damage", "Surgery")
            policy_context: Relevant policy text describing coverage

        Returns:
            ClaimAnalysisResult with status, confidence, and reasoning

        Raises:
            ClaimAnalyzerError: If inputs are invalid or analysis fails
        """
        try:
            # Step 1: Validate inputs
            self._validate_inputs(claim_type, policy_context)

            self._logger.info(
                "Claim analysis started | claim_type=%s | context_length=%d",
                claim_type,
                len(policy_context),
            )

            # Step 2: Normalize text for analysis
            context_lower = policy_context.lower()
            claim_lower = claim_type.lower()

            # Step 3: Apply business rules
            status, confidence, reason = self._apply_business_rules(
                claim_type=claim_type,
                claim_lower=claim_lower,
                context_lower=context_lower,
                policy_context=policy_context,
            )

            # Step 4: Create result
            result = ClaimAnalysisResult(
                claim_type=claim_type,
                status=status,
                confidence=confidence,
                reason=reason,
                analyzed_at=datetime.now(),
                success=True,
            )

            self._logger.info(
                "Claim analysis completed | status=%s | confidence=%.2f",
                status,
                confidence,
            )

            return result

        except ClaimAnalyzerError:
            raise

        except Exception as exc:
            error_msg = f"Unexpected error during claim analysis: {exc}"
            self._logger.error(error_msg)
            raise ClaimAnalyzerError(error_msg) from exc

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_inputs(self, claim_type: str, policy_context: str) -> None:
        """Validate claim type and policy context."""
        if not isinstance(claim_type, str):
            raise ClaimAnalyzerError(
                f"Claim type must be a string, got {type(claim_type).__name__}."
            )

        if not isinstance(policy_context, str):
            raise ClaimAnalyzerError(
                f"Policy context must be a string, got {type(policy_context).__name__}."
            )

        if not claim_type.strip():
            raise ClaimAnalyzerError("Claim type must not be empty.")

        if not policy_context.strip():
            raise ClaimAnalyzerError("Policy context must not be empty.")

    def _apply_business_rules(
        self,
        claim_type: str,
        claim_lower: str,
        context_lower: str,
        policy_context: str,
    ) -> tuple[str, float, str]:
        """
        Apply business rules to determine eligibility status.

        Returns:
            Tuple of (status, confidence, reason)
        """
        # Check for explicit exclusions first (highest priority)
        negative_matches = [
            kw for kw in self._NEGATIVE_KEYWORDS if kw in context_lower
        ]

        if negative_matches:
            return self._build_negative_result(
                claim_type, negative_matches, policy_context
            )

        # Check for ambiguous/conditional language
        ambiguous_matches = [
            kw for kw in self._AMBIGUOUS_KEYWORDS if kw in context_lower
        ]

        if ambiguous_matches:
            return self._build_ambiguous_result(
                claim_type, ambiguous_matches, policy_context
            )

        # Check for positive coverage indicators
        positive_matches = [
            kw for kw in self._POSITIVE_KEYWORDS if kw in context_lower
        ]

        if positive_matches:
            return self._build_positive_result(
                claim_type, positive_matches, policy_context
            )

        # No clear indicators - requires manual review
        return (
            "Requires Manual Review",
            0.50,
            f"Policy context for '{claim_type}' does not contain clear coverage indicators. Manual review recommended."
        )

    def _build_positive_result(
        self,
        claim_type: str,
        matches: list[str],
        policy_context: str,
    ) -> tuple[str, float, str]:
        """Build result for likely eligible claims."""
        # Base confidence on number of positive indicators
        base_confidence = 0.70
        confidence_boost = min(len(matches) * 0.10, 0.25)
        confidence = min(base_confidence + confidence_boost, 0.95)

        # Extract relevant sentence for reason
        sentences = policy_context.split('.')
        relevant_sentence = next(
            (s.strip() for s in sentences if any(kw in s.lower() for kw in matches)),
            policy_context[:150]
        )

        reason = (
            f"'{claim_type}' appears to be covered based on policy language. "
            f"Context indicates: {relevant_sentence}"
        )

        return "Likely Eligible", confidence, reason

    def _build_negative_result(
        self,
        claim_type: str,
        matches: list[str],
        policy_context: str,
    ) -> tuple[str, float, str]:
        """Build result for likely ineligible claims."""
        # High confidence for explicit exclusions
        base_confidence = 0.75
        confidence_boost = min(len(matches) * 0.10, 0.20)
        confidence = min(base_confidence + confidence_boost, 0.95)

        # Extract relevant sentence
        sentences = policy_context.split('.')
        relevant_sentence = next(
            (s.strip() for s in sentences if any(kw in s.lower() for kw in matches)),
            policy_context[:150]
        )

        reason = (
            f"'{claim_type}' appears to be excluded from coverage. "
            f"Policy states: {relevant_sentence}"
        )

        return "Likely Not Eligible", confidence, reason

    def _build_ambiguous_result(
        self,
        claim_type: str,
        matches: list[str],
        policy_context: str,
    ) -> tuple[str, float, str]:
        """Build result for ambiguous claims requiring manual review."""
        # Moderate confidence for ambiguous cases
        confidence = 0.65

        # Extract relevant sentence
        sentences = policy_context.split('.')
        relevant_sentence = next(
            (s.strip() for s in sentences if any(kw in s.lower() for kw in matches)),
            policy_context[:150]
        )

        reason = (
            f"'{claim_type}' coverage is conditional or requires additional review. "
            f"Policy indicates: {relevant_sentence}"
        )

        return "Requires Manual Review", confidence, reason
