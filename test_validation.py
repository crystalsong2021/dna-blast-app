"""
Simple tests for FASTA validation logic
Run with: python test_validation.py
"""

from app import validate_fasta

def test_valid_fasta():
    """Test valid FASTA input"""
    fasta = ">test\nATCGATCGATCG"
    is_valid, result = validate_fasta(fasta)
    assert is_valid == True, "Valid FASTA should pass"
    print("✓ Valid FASTA test passed")

def test_empty_input():
    """Test empty input"""
    is_valid, error = validate_fasta("")
    assert is_valid == False, "Empty input should fail"
    assert "Empty input" in error
    print("✓ Empty input test passed")

def test_missing_header():
    """Test sequence without header"""
    fasta = "ATCGATCGATCG"
    is_valid, error = validate_fasta(fasta)
    assert is_valid == False, "Missing header should fail"
    assert "must start with" in error
    print("✓ Missing header test passed")

def test_invalid_characters():
    """Test invalid DNA characters"""
    fasta = ">test\nATCGXYZ"
    is_valid, error = validate_fasta(fasta)
    assert is_valid == False, "Invalid characters should fail"
    assert "invalid DNA characters" in error
    print("✓ Invalid characters test passed")

def test_empty_sequence():
    """Test header with no sequence"""
    fasta = ">test\n"
    is_valid, error = validate_fasta(fasta)
    assert is_valid == False, "Empty sequence should fail"
    print("✓ Empty sequence test passed")

def test_multiline_fasta():
    """Test valid multiline FASTA"""
    fasta = """>NC_009085_A1S_r15
ATTGAACGCTGGCGGCAGGCTTAACACATGCAAGTCGAGCGGGGGAAGGTAGCTTGCTAC
TGGACCTAGCGGCGGACGGGTGAGTAATGCTTAGGAATCTGCCTATTAGTGGGGGACAAC"""
    is_valid, result = validate_fasta(fasta)
    assert is_valid == True, "Multiline FASTA should pass"
    print("✓ Multiline FASTA test passed")

def test_lowercase_dna():
    """Test lowercase DNA characters"""
    fasta = ">test\natcgatcg"
    is_valid, result = validate_fasta(fasta)
    assert is_valid == True, "Lowercase DNA should pass"
    print("✓ Lowercase DNA test passed")

def test_with_n_character():
    """Test DNA with N (unknown base)"""
    fasta = ">test\nATCGNNATCG"
    is_valid, result = validate_fasta(fasta)
    assert is_valid == True, "DNA with N should pass"
    print("✓ DNA with N character test passed")

if __name__ == "__main__":
    print("Running FASTA validation tests...\n")

    tests = [
        test_valid_fasta,
        test_empty_input,
        test_missing_header,
        test_invalid_characters,
        test_empty_sequence,
        test_multiline_fasta,
        test_lowercase_dna,
        test_with_n_character
    ]

    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1

    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")

    if failed == 0:
        print("All tests passed! ✓")
    else:
        print(f"{failed} test(s) failed ✗")