"""
Simple tests for FASTA validation logic
Run with: python test_validation.py
"""

from app.services.fasta import validate_fasta

def test_valid_fasta():
    fasta = ">test\nATCGATCGATCGATCGATCG"
    is_valid, error, sequences = validate_fasta(fasta)
    assert is_valid is True
    assert error is None
    assert len(sequences) == 1
    print("✓ Valid FASTA test passed")


def test_empty_input():
    """
    Backend defensive test.
    Note: UI prevents empty submissions; this test guards direct API usage.
    """
    is_valid, error, sequences = validate_fasta("")
    assert is_valid is False
    assert sequences == []
    print("✓ Empty input test passed")


def test_missing_header():
    """Test sequence without FASTA header"""
    fasta = "ATCGATCGATCGATCGATCG"
    is_valid, error, sequences = validate_fasta(fasta)
    assert is_valid is False
    assert error is not None
    assert "fasta" in error.lower()
    assert sequences == []
    print("✓ Missing header test passed")

def test_invalid_characters():
    fasta = ">test\nATCGXYZ"
    is_valid, error, sequences = validate_fasta(fasta)
    assert is_valid is False
    assert "Invalid characters" in error
    print("✓ Invalid characters test passed")


def test_empty_sequence():
    fasta = ">test\n"
    is_valid, error, sequences = validate_fasta(fasta)
    assert is_valid is False
    print("✓ Empty sequence test passed")


def test_multiline_fasta():
    fasta = """>seq1
ATTGAACGCTGGCGGCAGGCTTAACACATGCAAGTCGAGCGGGGGAAGG
TAGCTTGCTACTGGACCTAGCGGCGGACGGGTGAGTAATGCTTAGGAA"""
    is_valid, error, sequences = validate_fasta(fasta)
    assert is_valid is True
    assert len(sequences) == 1
    print("✓ Multiline FASTA test passed")


def test_lowercase_dna():
    fasta = ">test\natcgatcgatcgatcgatcg"
    is_valid, error, sequences = validate_fasta(fasta)
    assert is_valid is True
    print("✓ Lowercase DNA test passed")


def test_with_n_character():
    fasta = ">test\nATCGNNATCGATCGNNATCG"
    is_valid, error, sequences = validate_fasta(fasta)
    assert is_valid is True
    print("✓ DNA with N character test passed")

def test_multiple_fasta_sequences():
    """Test FASTA input containing multiple sequences"""
    fasta = """>seq1
    ATCGATCGATCGATCGATCG
    >seq2
    GCTAGCTAGCTAGCTAGCTA
    """

    is_valid, error, sequences = validate_fasta(fasta)

    assert is_valid is True
    assert error is None
    assert isinstance(sequences, list)
    assert len(sequences) == 2

    print("✓ Multiple FASTA sequences test passed")


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
        test_with_n_character,
        test_multiple_fasta_sequences
    ]

    failed = 0
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1

    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")
