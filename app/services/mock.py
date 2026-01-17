def create_mock_result(sequence):
    return {
        "query_id": "mock_sequence",
        "query_length": len(sequence),
        "hits": [
            {
                "accession": "CP199108.1",
                "title": "Acinetobacter baumannii chromosome",
                "percent_identity": 100.0,
                "alignment_length": len(sequence),
                "e_value": 0.0,
                "score": 1000,
                "length": 3894465,
                "identities": len(sequence),
                "gaps": 0
            }
        ]
    }
