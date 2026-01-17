"""
BLAST service.

Submits DNA sequences to NCBI BLAST (blastn / core_nt),
parses XML output, and returns normalized hit data.
Includes disk-backed caching to avoid redundant calls.
"""

from Bio.Blast import NCBIWWW, NCBIXML
from .cache import load_from_cache, save_to_cache

def run_blast(sequence: str):
    """
    Run BLAST with disk caching.
    """

    #Check cache first
    cached = load_from_cache(sequence)
    if cached:
        print("✅ BLAST cache hit")
        return True, cached

    print("Cache miss – submitting BLAST to NCBI")

    try:
        result_handle = NCBIWWW.qblast(
            program="blastn",
            database="core_nt",
            sequence=sequence,
            hitlist_size=10
        )

        blast_record = NCBIXML.read(result_handle)
        result_handle.close()

        hits = []
        for alignment in blast_record.alignments:
            if alignment.hsps:
                hsp = alignment.hsps[0]

                percent_identity = round(
                    (hsp.identities / hsp.align_length) * 100, 2
                )

                hits.append({
                    "title": alignment.title,
                    "accession": alignment.accession,
                    "length": alignment.length,
                    "percent_identity": percent_identity,
                    "alignment_length": hsp.align_length,
                    "e_value": hsp.expect,
                    "score": hsp.score,
                    "identities": hsp.identities,
                    "gaps": hsp.gaps,
                })

        result = {
            "query_id": blast_record.query,
            "query_length": blast_record.query_length,
            "hits": hits,
        }

        #Save to cache
        save_to_cache(sequence, result)
        print("BLAST result cached")

        return True, result

    except Exception as e:
        return False, f"BLAST failed: {str(e)}"
