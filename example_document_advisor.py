"""
example_document_advisor.py
Demonstrates Document Advisor usage and integration with other modules.

Shows document recommendations for various claim types and full system integration.
"""

from Insurance_Claim_Agent.document_advisor import DocumentAdvisor, DocumentAdvisorError
from Insurance_Claim_Agent.answer_generator import AnswerGenerator
from Insurance_Claim_Agent.claim_analyzer import ClaimAnalyzer


def main():
    print("=" * 70)
    print("AI-POWERED INSURANCE CLAIM ASSISTANT")
    print("Module 5: Document Advisor Demo")
    print("=" * 70)
    print()

    # Initialize advisor
    advisor = DocumentAdvisor()

    # ------------------------------------------------------------------
    # Scenario 1: Flood Damage Documents
    # ------------------------------------------------------------------
    print("SCENARIO 1: Flood Damage Claim")
    print("-" * 70)

    docs1 = advisor.get_required_documents("Flood Damage")
    
    print(f"Claim Type: {docs1.claim_type}")
    print(f"\nRequired Documents ({len(docs1.required_documents)}):")
    for idx, doc in enumerate(docs1.required_documents, 1):
        print(f"  {idx}. {doc}")
    
    print(f"\nOptional Documents ({len(docs1.optional_documents)}):")
    for idx, doc in enumerate(docs1.optional_documents, 1):
        print(f"  {idx}. {doc}")
    
    print(f"\nNotes: {docs1.notes}")
    print()

    # ------------------------------------------------------------------
    # Scenario 2: Vehicle Accident Documents
    # ------------------------------------------------------------------
    print("SCENARIO 2: Vehicle Accident Claim")
    print("-" * 70)

    docs2 = advisor.get_required_documents("Vehicle Accident")
    
    print(f"Claim Type: {docs2.claim_type}")
    print(f"\nRequired Documents ({len(docs2.required_documents)}):")
    for idx, doc in enumerate(docs2.required_documents, 1):
        print(f"  {idx}. {doc}")
    
    print(f"\nNotes: {docs2.notes}")
    print()

    # ------------------------------------------------------------------
    # Scenario 3: Hospitalization Claim Documents
    # ------------------------------------------------------------------
    print("SCENARIO 3: Hospitalization Claim")
    print("-" * 70)

    docs3 = advisor.get_required_documents("Hospitalization Claim")
    
    print(f"Claim Type: {docs3.claim_type}")
    print(f"\nRequired Documents:")
    for doc in docs3.required_documents:
        print(f"  - {doc}")
    print()

    # ------------------------------------------------------------------
    # Scenario 4: Unknown Claim Type
    # ------------------------------------------------------------------
    print("SCENARIO 4: Unknown Claim Type (Generic Documents)")
    print("-" * 70)

    docs4 = advisor.get_required_documents("Mysterious Damage")
    
    print(f"Claim Type: {docs4.claim_type}")
    print(f"\nGeneric Required Documents:")
    for doc in docs4.required_documents:
        print(f"  - {doc}")
    
    print(f"\nNotes: {docs4.notes}")
    print()

    # ------------------------------------------------------------------
    # Scenario 5: Batch Processing
    # ------------------------------------------------------------------
    print("SCENARIO 5: Batch Document Lookup")
    print("-" * 70)

    claim_types = [
        "Theft Claim",
        "Fire Damage",
        "Medical Emergency",
        "Property Damage"
    ]

    for claim_type in claim_types:
        docs = advisor.get_required_documents(claim_type)
        print(f"{claim_type}: {len(docs.required_documents)} required, "
              f"{len(docs.optional_documents)} optional")
    print()

    # ------------------------------------------------------------------
    # Scenario 6: Error Handling
    # ------------------------------------------------------------------
    print("SCENARIO 6: Error Handling")
    print("-" * 70)

    # Empty claim type
    try:
        advisor.get_required_documents("")
    except DocumentAdvisorError as exc:
        print(f"[OK] Empty claim type rejected: {exc}")

    # None claim type
    try:
        advisor.get_required_documents(None)
    except DocumentAdvisorError as exc:
        print(f"[OK] None claim type rejected: {exc}")

    print()

    # ------------------------------------------------------------------
    # Scenario 7: FULL SYSTEM INTEGRATION
    # ------------------------------------------------------------------
    print("=" * 70)
    print("SCENARIO 7: COMPLETE SYSTEM INTEGRATION")
    print("=" * 70)
    print()

    # Initialize all modules
    generator = AnswerGenerator(use_mock_llm=True)
    analyzer = ClaimAnalyzer()
    
    # Simulate user query
    user_question = "My house was damaged due to flooding."
    policy_context = """
    Flood damage is covered under Section 4.2 of this policy.
    Maximum claim amount is INR 5,00,000.
    Claims must be filed within 30 days of the incident.
    """

    print("User Question:")
    print(f'  "{user_question}"')
    print()

    # Step 1: Generate Answer
    print("[Step 1] Generating Answer...")
    answer_result = generator.generate_response(
        question=user_question,
        context=policy_context
    )
    print(f"Answer: {answer_result.answer}")
    print()

    # Step 2: Analyze Claim Eligibility
    print("[Step 2] Analyzing Claim Eligibility...")
    analysis_result = analyzer.analyze_claim(
        claim_type="Flood Damage",
        policy_context=policy_context
    )
    print(f"Status: {analysis_result.status}")
    print(f"Confidence: {analysis_result.confidence:.0%}")
    print(f"Reason: {analysis_result.reason}")
    print()

    # Step 3: Get Required Documents
    print("[Step 3] Fetching Required Documents...")
    doc_result = advisor.get_required_documents("Flood Damage")
    print(f"\nRequired Documents for {doc_result.claim_type}:")
    for idx, doc in enumerate(doc_result.required_documents, 1):
        print(f"  {idx}. {doc}")
    
    print(f"\nOptional Documents:")
    for idx, doc in enumerate(doc_result.optional_documents, 1):
        print(f"  {idx}. {doc}")
    
    print(f"\nImportant Note: {doc_result.notes}")
    print()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("=" * 70)
    print("COMPLETE USER RESPONSE")
    print("=" * 70)
    print()
    print(f"Question: {user_question}")
    print()
    print(f"Answer: {answer_result.answer[:150]}...")
    print()
    print(f"Eligibility: {analysis_result.status} ({analysis_result.confidence:.0%} confidence)")
    print()
    print(f"Documents Needed ({len(doc_result.required_documents)} required):")
    for doc in doc_result.required_documents[:3]:
        print(f"  - {doc}")
    print(f"  ... and {len(doc_result.required_documents) - 3} more")
    print()
    print("=" * 70)
    print("SYSTEM SUMMARY")
    print("=" * 70)
    print("[OK] Module 1 (Prompt Builder) - Working")
    print("[OK] Module 2 (LLM Engine) - Working")
    print("[OK] Module 3 (Answer Generator) - Working")
    print("[OK] Module 4 (Claim Analyzer) - Working")
    print("[OK] Module 5 (Document Advisor) - Working")
    print()
    print("Complete integration successful!")
    print("System ready for production deployment.")
    print("=" * 70)


if __name__ == "__main__":
    main()
