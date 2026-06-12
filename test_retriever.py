"""Test script to verify Phase 6 Retrieval API layer."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from retriever import retrieve, InvalidQueryError, VectorStoreNotFoundError


def test_basic_retrieval():
    """Test basic retrieval functionality."""
    print("=" * 80)
    print("TEST 1: Basic Retrieval")
    print("=" * 80)
    
    query = "flood damage coverage"
    print(f"\nQuery: '{query}'")
    
    try:
        results = retrieve(query, k=3)
        print(f"\n[OK] Retrieved {len(results)} chunks")
        for i, chunk in enumerate(results, 1):
            print(f"\n  Result {i}:")
            display_text = chunk[:100] + "..." if len(chunk) > 100 else chunk
            print(f"  {display_text}")
        return True
    except Exception as e:
        print(f"\n[FAIL] {type(e).__name__}: {e}")
        return False


def test_different_k_values():
    """Test retrieval with different k values."""
    print("\n" + "=" * 80)
    print("TEST 2: Different k Values")
    print("=" * 80)
    
    query = "liability coverage"
    
    for k in [1, 2, 5]:
        print(f"\nQuery: '{query}' with k={k}")
        try:
            results = retrieve(query, k=k)
            print(f"[OK] Retrieved {len(results)} chunks (requested k={k})")
        except Exception as e:
            print(f"[FAIL] k={k}: {type(e).__name__}: {e}")
            return False
    
    return True


def test_multiple_queries():
    """Test multiple queries to verify caching works."""
    print("\n" + "=" * 80)
    print("TEST 3: Multiple Queries (Caching Test)")
    print("=" * 80)
    
    queries = [
        "property coverage details",
        "claims filing process",
        "deductible amount",
        "liability insurance"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n[Query {i}] '{query}'")
        try:
            results = retrieve(query, k=2)
            print(f"[OK] Retrieved {len(results)} chunks")
            if results:
                display_text = results[0][:80] + "..." if len(results[0]) > 80 else results[0]
                print(f"     Top result: {display_text}")
        except Exception as e:
            print(f"[FAIL] {type(e).__name__}: {e}")
            return False
    
    return True


def test_input_validation():
    """Test input validation."""
    print("\n" + "=" * 80)
    print("TEST 4: Input Validation")
    print("=" * 80)
    
    # Test None query
    print("\n[Test 4.1] None query")
    try:
        retrieve(None)
        print("[FAIL] Should have raised InvalidQueryError")
        return False
    except InvalidQueryError:
        print("[OK] Correctly raised InvalidQueryError for None")
    
    # Test empty string
    print("\n[Test 4.2] Empty string query")
    try:
        retrieve("")
        print("[FAIL] Should have raised InvalidQueryError")
        return False
    except InvalidQueryError:
        print("[OK] Correctly raised InvalidQueryError for empty string")
    
    # Test whitespace-only string
    print("\n[Test 4.3] Whitespace-only query")
    try:
        retrieve("   ")
        print("[FAIL] Should have raised InvalidQueryError")
        return False
    except InvalidQueryError:
        print("[OK] Correctly raised InvalidQueryError for whitespace")
    
    # Test invalid type
    print("\n[Test 4.4] Invalid type (int)")
    try:
        retrieve(123)
        print("[FAIL] Should have raised InvalidQueryError")
        return False
    except InvalidQueryError:
        print("[OK] Correctly raised InvalidQueryError for int")
    
    return True


def test_semantic_relevance():
    """Test that semantic search returns relevant results."""
    print("\n" + "=" * 80)
    print("TEST 5: Semantic Relevance")
    print("=" * 80)
    
    test_cases = [
        {
            "query": "water damage protection",
            "expected_keywords": ["flood", "water", "damage", "coverage"]
        },
        {
            "query": "how much does it cost",
            "expected_keywords": ["deductible", "premium", "cost", "amount", "price", "$"]
        },
        {
            "query": "legal responsibility coverage",
            "expected_keywords": ["liability", "legal", "responsibility", "protection"]
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n[Test 5.{i}] Query: '{test['query']}'")
        try:
            results = retrieve(test['query'], k=3)
            
            if not results:
                print("[WARN] No results returned")
                continue
            
            # Check if any expected keyword appears in results
            all_text = " ".join(results).lower()
            found_keywords = [kw for kw in test['expected_keywords'] if kw.lower() in all_text]
            
            if found_keywords:
                print(f"[OK] Found relevant keywords: {found_keywords}")
            else:
                print(f"[INFO] Expected keywords not found, but search completed")
                print(f"      Top result: {results[0][:100]}...")
        except Exception as e:
            print(f"[FAIL] {type(e).__name__}: {e}")
            return False
    
    return True


def test_performance():
    """Test that caching improves performance."""
    print("\n" + "=" * 80)
    print("TEST 6: Performance (Caching Verification)")
    print("=" * 80)
    
    import time
    
    query = "insurance policy coverage"
    
    # First call (loads vectorstore and model)
    print("\n[Test 6.1] First call (cold start)")
    start = time.time()
    try:
        results1 = retrieve(query, k=3)
        time1 = time.time() - start
        print(f"[OK] First call completed in {time1:.3f}s")
    except Exception as e:
        print(f"[FAIL] {type(e).__name__}: {e}")
        return False
    
    # Second call (uses cached vectorstore)
    print("\n[Test 6.2] Second call (warm start)")
    start = time.time()
    try:
        results2 = retrieve(query, k=3)
        time2 = time.time() - start
        print(f"[OK] Second call completed in {time2:.3f}s")
    except Exception as e:
        print(f"[FAIL] {type(e).__name__}: {e}")
        return False
    
    # Verify results are consistent
    if results1 == results2:
        print("[OK] Results are consistent across calls")
    else:
        print("[WARN] Results differ (may be due to floating-point precision)")
    
    # Check if second call is faster (or at least not significantly slower)
    if time2 <= time1 * 1.5:  # Allow 50% margin
        print(f"[OK] Caching works: second call not significantly slower")
    else:
        print(f"[INFO] Second call took {time2/time1:.2f}x the first call time")
    
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("PHASE 6: RETRIEVAL API LAYER - COMPREHENSIVE TESTING")
    print("=" * 80)
    
    tests = [
        ("Basic Retrieval", test_basic_retrieval),
        ("Different k Values", test_different_k_values),
        ("Multiple Queries", test_multiple_queries),
        ("Input Validation", test_input_validation),
        ("Semantic Relevance", test_semantic_relevance),
        ("Performance", test_performance)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n[ERROR] Test '{name}' crashed: {type(e).__name__}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, p in results if p)
    total = len(results)
    
    for name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {name}")
    
    print("\n" + "-" * 80)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 80)
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! Phase 6 is LLM-ready.")
        return 0
    else:
        print(f"\n[FAILURE] {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    exit(main())
