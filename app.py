from flask import Flask, render_template, request, jsonify
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
from io import StringIO

app = Flask(__name__)

def validate_fasta(fasta_text):
    """
    Validate FASTA format and return sequences.
    Returns: (is_valid, sequences_list_or_error_message)
    """
    if not fasta_text or not fasta_text.strip():
        return False, "Empty input"

    if not fasta_text.strip().startswith('>'):
        return False, "FASTA format must start with '>'"

    try:
        fasta_io = StringIO(fasta_text)
        sequences = list(SeqIO.parse(fasta_io, "fasta"))

        if not sequences:
            return False, "No valid sequences found"

        valid_dna = set('ATCGNatcgn')
        for seq in sequences:
            seq_str = str(seq.seq)
            if not all(c in valid_dna for c in seq_str):
                return False, f"Sequence '{seq.id}' contains invalid DNA characters"
            if len(seq_str) == 0:
                return False, f"Sequence '{seq.id}' is empty"

        return True, sequences

    except Exception as e:
        return False, f"FASTA parsing error: {str(e)}"

def perform_blast(sequence):
    """
    Perform BLAST search using NCBI web service.
    """
    try:
        import ssl
        import urllib.request

        # Create an SSL context that doesn't verify certificates (for development)
        ssl._create_default_https_context = ssl._create_unverified_context

        result_handle = NCBIWWW.qblast(
            program="blastn",
            database="nt",
            sequence=str(sequence.seq),
            hitlist_size=10,
            expect=10.0
        )

        blast_records = NCBIXML.parse(result_handle)
        blast_record = next(blast_records)

        return blast_record

    except Exception as e:
        print(f"BLAST error: {str(e)}")
        return None
        
def parse_blast_results(blast_record):
    """
    Parse BLAST record into a list of hit dictionaries.
    """
    hits = []

    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            percent_identity = (hsp.identities / hsp.align_length) * 100

            hit = {
                'title': alignment.title,
                'accession': alignment.accession,
                'length': alignment.length,
                'percent_identity': round(percent_identity, 2),
                'alignment_length': hsp.align_length,
                'e_value': hsp.expect,
                'score': hsp.score,
                'identities': hsp.identities,
                'gaps': hsp.gaps
            }
            hits.append(hit)

    return hits

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blast', methods=['POST'])
def blast():
    try:
        fasta_text = request.form.get('fasta_text', '')
        print(f"Received fasta_text: {repr(fasta_text)}")
        print(f"First char: {repr(fasta_text[0] if fasta_text else 'empty')}")
        if 'fasta_file' in request.files:
            file = request.files['fasta_file']
            if file.filename != '':
                fasta_text = file.read().decode('utf-8')

        is_valid, result = validate_fasta(fasta_text)

        if not is_valid:
            return jsonify({
                'success': False,
                'error': result
            })

        sequences = result

        if len(sequences) == 0:
            return jsonify({
                'success': False,
                'error': 'No sequences found'
            })

        sequence = sequences[0]
        blast_record = perform_blast(sequence)

        if blast_record is None:
            return jsonify({
                'success': False,
                'error': 'BLAST search failed. Please try again.'
            })

        hits = parse_blast_results(blast_record)

        return jsonify({
            'success': True,
            'query_id': sequence.id,
            'query_length': len(sequence.seq),
            'hits': hits
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)