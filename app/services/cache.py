"""
BLAST result caching.

Stores parsed BLAST results on disk using
SHA-256 hashes of sequences to prevent
repeated NCBI submissions.
"""

import json
import hashlib
from pathlib import Path

CACHE_DIR = Path("blast_cache")
CACHE_DIR.mkdir(exist_ok=True)

def sequence_hash(sequence: str) -> str:
    """Generate a stable hash for a DNA sequence"""
    return hashlib.sha256(sequence.encode("utf-8")).hexdigest()

def cache_path(sequence: str) -> Path:
    return CACHE_DIR / f"{sequence_hash(sequence)}.json"

def load_from_cache(sequence: str):
    path = cache_path(sequence)
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_to_cache(sequence: str, data: dict):
    path = cache_path(sequence)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
