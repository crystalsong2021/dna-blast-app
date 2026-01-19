"""
FASTA validation utilities.

Validates FASTA format, sequence length, and allowed IUPAC nucleotide
codes as accepted by NCBI BLAST (blastn).
"""

from Bio import SeqIO
from io import StringIO

# Allow IUPAC nucleotide ambiguity codes and gap characters ('-')
# Gap characters are commonly present in aligned or consensus FASTA files
# and are tolerated by NCBI BLAST.
VALID_NTS = set("ATCGNRYSWKMBDHV-")

def validate_fasta(fasta_text):
    if not fasta_text.strip().startswith(">"):
        return False, "Invalid FASTA format", []

    records = list(SeqIO.parse(StringIO(fasta_text), "fasta"))
    if not records:
        return False, "No sequences found", []

    sequences = []
    for record in records:
        seq = str(record.seq).upper()
        if not set(seq).issubset(VALID_NTS):
            return False, f"Invalid characters in {record.id}", []

        if len(seq) < 20:
            return False, f"Sequence {record.id} too short", []

        sequences.append({
            "id": record.id,
            "sequence": seq,
            "description": record.description
        })

    return True, None, sequences

