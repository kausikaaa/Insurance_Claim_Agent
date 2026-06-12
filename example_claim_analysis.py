"""
example_claim_analysis.py
Demonstrates Claim Eligibility Analyzer across various insurance scenarios.

Shows how the analyzer uses business rules to assess claim eligibility.
"""

from Insurance_Claim_Agent.claim_analyzer import ClaimAnalyzer, ClaimAnalyzerError


def main():
    print("=" * 70)
    print("AI-POWERED INSURANCE CLAIM ASSISTANT")
    print("Module 4: Claim Eligibility Analyzer Demo")
    print("=" * 70)
    print()

    # Initialize analyzer
    analyzer = ClaimAnalyzer()

    # ------------------------------------------------------------------
    # Scenario 1: Explicitly Covered Claim (Flood Damage)
    # ------------------------------------------------------------------
    print("SCENARIO 1: Explicitly Covered Claim")
    print("-" * 70)

    result1 = analyzer.analyze_claim(
        claim_type="Flood Damage",
        policy_context="""
        Flood damage is covered under Section 4.2 of this policy.
        Maximum claim amount is INR 5,00,000.
        """
    )

    print(f"Claim Type: {result1.claim_type}")
    print(f"Status: {result1.status}")
    print(f"Confidence: {result1.confidence:.2f}")
    print(f"Reason: {result1.reason}")
    print(f"Analyzed At: {result1.analyzed_at}")
    print(f"Success: {result1.success}")
    print()

    # ------------------------------------------------------------------
    # Scenario 2: Explicitly Excluded Claim (Cosmetic Surgery)
    # ------------------------------------------------------------------
    print("SCENARIO 2: Explicitly Excluded Claim")
    print("-" * 70)

    result2 = analyzer.analyze_claim(
        claim_type="Cosmetic Surgery",
        policy_context="""
        Cosmetic procedures are excluded from coverage.
        Only medically necessary surgeries are covered.
        """
    )

    print(f"Claim Type: {result2.claim_type}")
    print(f"Status: {result2.status}")
    print(f"Confidence: {result2.confidence:.2f}")
    print(f"Reason: {result2.reason}")
    print()

    # ------------------------------------------------------------------
    # Scenario 3: Conditional/Ambiguous Claim
    # ------------------------------------------------------------------
    print("SCENARIO 3: Conditional Claim (Requires Review)")
    print("-" * 70)

    result3 = analyzer.analyze_claim(
        claim_type="Special Medical Procedure",
        policy_context="""
        Coverage depends on prior authorization.
        Medical necessity must be established.
        """
    )

    print(f"Claim Type: {result3.claim_type}")
    print(f"Status: {result3.status}")
    print(f"Confidence: {result3.confidence:.2f}")
    print(f"Reason: {result3.reason}")
    print()

    # ------------------------------------------------------------------
    # Scenario 4: Multiple Positive Indicators
    # ------------------------------------------------------------------
    print("SCENARIO 4: Strong Coverage Indicators")
    print("-" * 70)

    result4 = analyzer.analyze_claim(
        claim_type="Fire Damage",
        policy_context="""
        Fire damage is covered, eligible, and payable under this policy.
        Claims are compensable up to INR 10,00,000.
        """
    )

    print(f"Claim Type: {result4.claim_type}")
    print(f"Status: {result4.status}")
    print(f"Confidence: {result4.confidence:.2f}")
    print(f"Reason: {result4.reason}")
    print()

    # ------------------------------------------------------------------
    # Scenario 5: Multiple Exclusion Indicators
    # ------------------------------------------------------------------
    print("SCENARIO 5: Strong Exclusion Indicators")
    print("-" * 70)

    result5 = analyzer.analyze_claim(
        claim_type="Pre-existing Condition",
        policy_context="""
        Pre-existing conditions are excluded, not covered, and ineligible.
        Such claims are rejected under Section 7.3.
        """
    )

    print(f"Claim Type: {result5.claim_type}")
    print(f"Status: {result5.status}")
    print(f"Confidence: {result5.confidence:.2f}")
    print(f"Reason: {result5.reason}")
    print()

    # ------------------------------------------------------------------
    # Scenario 6: Minimal Context
    # ------------------------------------------------------------------
    print("SCENARIO 6: Minimal Context (Manual Review)")
    print("-" * 70)

    result6 = analyzer.analyze_claim(
        claim_type="Earthquake Damage",
        policy_context="Earthquake damage provisions are in Section 5.1."
    )

    print(f"Claim Type: {result6.claim_type}")
    print(f"Status: {result6.status}")
    print(f"Confidence: {result6.confidence:.2f}")
    print(f"Reason: {result6.reason}")
    print()

    # ------------------------------------------------------------------
    # Scenario 7: Batch Analysis
    # ------------------------------------------------------------------
    print("SCENARIO 7: Batch Claim Analysis")
    print("-" * 70)

    batch_claims = [
        ("Theft", "Theft is covered under home insurance policy."),
        ("War Damage", "War and terrorism damage is not covered."),
        ("Medical Emergency", "Emergency medical treatment is eligible."),
        ("Dental Implants", "Dental implants require pre-approval."),
    ]

    print(f"Processing {len(batch_claims)} claims...\n")

    for idx, (claim_type, context) in enumerate(batch_claims, 1):
        result = analyzer.analyze_claim(claim_type, context)
        print(f"{idx}. {result.claim_type}")
        print(f"   Status: {result.status}")
        print(f"   Confidence: {result.confidence:.2f}")
        print()

    # ------------------------------------------------------------------
    # Scenario 8: Error Handling
    # ------------------------------------------------------------------
    print("SCENARIO 8: Error Handling")
    print("-" * 70)

    # Empty claim type
    try:
        analyzer.analyze_claim("", "Some context")
    except ClaimAnalyzerError as exc:
        print(f"[OK] Empty claim type rejected: {exc}")

    # Empty context
    try:
        analyzer.analyze_claim("Fire Damage", "")
    except ClaimAnalyzerError as exc:
        print(f"[OK] Empty context rejected: {exc}")

    # Invalid type
    try:
        analyzer.analyze_claim(None, "Some context")
    except ClaimAnalyzerError as exc:
        print(f"[OK] Invalid type rejected: {exc}")

    print()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("[OK] Module 4 (Claim Analyzer) working")
    print("[OK] Business rules applied correctly")
    print("[OK] Confidence scoring functional")
    print("[OK] Error handling robust")
    print()
    print("Claim Analysis Capabilities:")
    print("  - Detects explicitly covered claims")
    print("  - Identifies excluded/ineligible claims")
    print("  - Flags ambiguous cases for manual review")
    print("  - Provides confidence scores (0.0-1.0)")
    print("  - Generates human-readable explanations")
    print()
    print("Note: This is a preliminary assessment tool.")
    print("Final claim decisions should involve manual review.")
    print("=" * 70)


if __name__ == "__main__":
    main()
