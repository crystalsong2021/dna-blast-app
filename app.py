from flask import Flask, render_template, request, jsonify
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
from io import StringIO
import ssl
import certifi
import hashlib
import json
import os

app = Flask(__name__)

# Create cache directory
CACHE_DIR = 'blast_cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Enable/disable cache (set to True for testing, False for production)
ENABLE_MOCK_DATA = False

def create_ssl_context():
    """Create SSL context for NCBI API calls"""
    return ssl.create_default_context(cafile=certifi.where())

ssl._create_default_https_context = create_ssl_context


def get_cache_key(sequence):
    """Generate cache key from sequence"""
    return hashlib.md5(sequence.encode()).hexdigest()


def get_cached_result(sequence):
    """Get cached BLAST result if available"""
    if not ENABLE_MOCK_DATA:
        return None

    cache_key = get_cache_key(sequence)
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")

    if os.path.exists(cache_file):
        print(f"Cache hit! Loading cached result for sequence...")
        with open(cache_file, 'r') as f:
            return json.load(f)
    return None


def save_to_cache(sequence, result):
    """Save BLAST result to cache"""
    if not ENABLE_MOCK_DATA:
        return

    cache_key = get_cache_key(sequence)
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")

    with open(cache_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Result cached for future use")


def create_mock_result(sequence):
    """Create mock BLAST result for testing"""
    return {
        'query_id': 'test_sequence',
        'query_length': len(sequence),
        'hits': [
            {
                'title': 'gi|3056091481|gb|CP199108.1| Acinetobacter baumannii strain ABO22-A116 chromosome, complete genome',
                'accession': 'CP199108.1',
                'length': 3894465,
                'percent_identity': 100.0,
                'alignment_length': len(sequence),
                'e_value': 0.0,
                'score': 1000,
                'identities': len(sequence),
                'gaps': 0
            },
            {
                'title': 'gi|2897312456|ref|NZ_CP094651.1| Acinetobacter baumannii strain FDAARGOS_1706 chromosome, complete genome',
                'accession': 'NZ_CP094651.1',
                'length': 3912381,
                'percent_identity': 99.8,
                'alignment_length': len(sequence) - 2,
                'e_value': 1.2e-180,
                'score': 995,
                'identities': len(sequence) - 2,
                'gaps': 0
            },
            {
                'title': 'gi|2547891234|gb|CP045110.1| Acinetobacter baumannii strain AB43 chromosome, complete genome',
                'accession': 'CP045110.1',
                'length': 3889567,
                'percent_identity': 99.5,
                'alignment_length': len(sequence) - 5,
                'e_value': 3.7e-175,
                'score': 988,
                'identities': len(sequence) - 5,
                'gaps': 2
            },
            {
                'title': 'gi|1987654321|ref|NZ_CP027528.1| Acinetobacter baumannii strain AR_0083 chromosome, complete genome',
                'accession': 'NZ_CP027528.1',
                'length': 3901234,
                'percent_identity': 98.9,
                'alignment_length': len(sequence) - 8,
                'e_value': 5.4e-168,
                'score': 975,
                'identities': len(sequence) - 8,
                'gaps': 3
            },
            {
                'title': 'gi|1567892345|gb|CP012004.1| Acinetobacter baumannii strain AB307-0294 chromosome, complete genome',
                'accession': 'CP012004.1',
                'length': 3976747,
                'percent_identity': 98.2,
                'alignment_length': len(sequence) - 12,
                'e_value': 2.1e-162,
                'score': 965,
                'identities': len(sequence) - 12,
                'gaps': 5
            },
            {
                'title': 'gi|1345678901|ref|NZ_CP020597.1| Acinetobacter baumannii strain HWBA8 chromosome, complete genome',
                'accession': 'NZ_CP020597.1',
                'length': 3867456,
                'percent_identity': 97.8,
                'alignment_length': len(sequence) - 15,
                'e_value': 8.9e-158,
                'score': 955,
                'identities': len(sequence) - 15,
                'gaps': 7
            },
            {
                'title': 'gi|987654321|gb|CP018664.1| Acinetobacter baumannii strain LAC-4 chromosome, complete genome',
                'accession': 'CP018664.1',
                'length': 3945678,
                'percent_identity': 96.5,
                'alignment_length': len(sequence) - 20,
                'e_value': 3.2e-150,
                'score': 940,
                'identities': len(sequence) - 20,
                'gaps': 10
            },
            {
                'title': 'gi|765432109|ref|NZ_CP016300.1| Acinetobacter baumannii strain MDR-TJ chromosome, complete genome',
                'accession': 'NZ_CP016300.1',
                'length': 3912345,
                'percent_identity': 95.8,
                'alignment_length': len(sequence) - 25,
                'e_value': 1.5e-145,
                'score': 930,
                'identities': len(sequence) - 25,
                'gaps': 12
            },
            {
                'title': 'gi|543210987|gb|CP015121.1| Acinetobacter baumannii strain XH386 chromosome, complete genome',
                'accession': 'CP015121.1',
                'length': 3889012,
                'percent_identity': 94.2,
                'alignment_length': len(sequence) - 32,
                'e_value': 6.7e-138,
                'score': 915,
                'identities': len(sequence) - 32,
                'gaps': 15
            },
            {
                'title': 'gi|321098765|ref|NZ_CP012952.1| Acinetobacter baumannii strain BJAB0715 chromosome, complete genome',
                'accession': 'NZ_CP012952.1',
                'length': 3956789,
                'percent_identity': 92.5,
                'alignment_length': len(sequence) - 40,
                'e_value': 2.8e-130,
                'score': 895,
                'identities': len(sequence) - 40,
                'gaps': 18
            }
        ]
    }


def validate_fasta(fasta_text):
    """
    Validate FASTA format and DNA sequence.
    Returns: (is_valid, error_message, sequences_list)
    """
    if not fasta_text or fasta_text.strip() == '':
        return False, "Empty sequence provided", []

    if not fasta_text.strip().startswith('>'):
        return False, "Invalid FASTA format. Sequence must start with '>'", []

    try:
        fasta_io = StringIO(fasta_text)
        records = list(SeqIO.parse(fasta_io, "fasta"))

        if len(records) == 0:
            return False, "No valid sequence found in FASTA format", []

        sequences = []
        valid_nucleotides = set('ATCGNRYSWKMBDHV-')

        for record in records:
            sequence = str(record.seq).upper()
            sequence_set = set(sequence)

            if not sequence_set.issubset(valid_nucleotides):
                invalid_chars = sequence_set - valid_nucleotides
                return False, f"Invalid characters in sequence '{record.id}': {', '.join(invalid_chars)}", []

            if len(sequence) < 20:
                return False, f"Sequence '{record.id}' too short ({len(sequence)}bp). Minimum is 20bp", []

            sequences.append({
                'id': record.id,
                'sequence': sequence,
                'description': record.description
            })

        return True, None, sequences

    except Exception as e:
        return False, f"Error parsing FASTA format: {str(e)}", []


def run_blast(sequence):
    """
    Submit sequence to NCBI BLAST and parse results.
    Returns: (success, data_or_error)
    """
    # Check cache first
    cached_result = get_cached_result(sequence)
    if cached_result:
        return True, cached_result

    # For testing: return mock data instead of calling NCBI
    if ENABLE_MOCK_DATA:
        print("Creating mock result for testing...")
        import time
        time.sleep(2)  # Simulate API delay
        result = create_mock_result(sequence)
        save_to_cache(sequence, result)
        return True, result

    # Real NCBI BLAST call (when ENABLE_MOCK_DATA = False)
    try:
        print(f"Submitting BLAST query (length: {len(sequence)}bp)...")

        result_handle = NCBIWWW.qblast(
            program="blastn",
            database="core_nt",
            sequence=sequence,
            hitlist_size=10
        )

        print("BLAST query submitted. Parsing results...")

        blast_record = NCBIXML.read(result_handle)
        result_handle.close()

        hits = []
        for alignment in blast_record.alignments:
            if alignment.hsps:
                hsp = alignment.hsps[0]
                percent_identity = (hsp.identities / hsp.align_length) * 100

                hits.append({
                    'title': alignment.title,
                    'accession': alignment.accession,
                    'length': alignment.length,
                    'percent_identity': round(percent_identity, 2),
                    'alignment_length': hsp.align_length,
                    'e_value': hsp.expect,
                    'score': hsp.score,
                    'identities': hsp.identities,
                    'gaps': hsp.gaps
                })

        print(f"BLAST completed. Found {len(hits)} hits.")

        result = {
            'query_id': blast_record.query,
            'query_length': blast_record.query_length,
            'hits': hits
        }

        # Cache the result
        save_to_cache(sequence, result)

        return True, result

    except Exception as e:
        print(f"BLAST error: {str(e)}")
        return False, f"BLAST search failed: {str(e)}"


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/blast', methods=['POST'])
def blast():
    """Handle BLAST submission from text or file input"""
    try:
        fasta_text = request.form.get('fasta_text', '').strip()
        fasta_file = request.files.get('fasta_file')

        # Determine input source
        if fasta_file and fasta_file.filename:
            print(f"Processing file: {fasta_file.filename}")
            fasta_content = fasta_file.read().decode('utf-8')
        elif fasta_text:
            print("Processing text input")
            fasta_content = fasta_text
        else:
            return jsonify({
                'success': False,
                'error': 'No sequence provided'
            })

        # Validate FASTA
        is_valid, error_msg, sequences = validate_fasta(fasta_content)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg
            })

        # Return sequences for processing
        return jsonify({
            'success': True,
            'sequences': sequences,
            'total_sequences': len(sequences)
        })

    except Exception as e:
        print(f"Error in /blast: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })


@app.route('/blast_single', methods=['POST'])
def blast_single():
    """Run BLAST for a single sequence"""
    try:
        data = request.get_json()
        sequence_id = data.get('sequence_id')
        sequence = data.get('sequence')

        if not sequence:
            return jsonify({
                'success': False,
                'error': 'No sequence provided'
            })

        # Run BLAST
        success, result = run_blast(sequence)

        if success:
            return jsonify({
                'success': True,
                'sequence_id': sequence_id,
                'query_length': result['query_length'],
                'hits': result['hits']
            })
        else:
            return jsonify({
                'success': False,
                'error': result
            })

    except Exception as e:
        print(f"Error in /blast_single: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })


@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    """Clear all cached results"""
    try:
        import shutil
        if os.path.exists(CACHE_DIR):
            shutil.rmtree(CACHE_DIR)
            os.makedirs(CACHE_DIR)
        return jsonify({
            'success': True,
            'message': 'Cache cleared successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


if __name__ == '__main__':
    print("Starting Flask BLAST application...")
    print(f"Cache enabled: {ENABLE_MOCK_DATA}")
    print("Navigate to http://127.0.0.1:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
from flask import Flask, render_template, request, jsonify
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
from io import StringIO
import ssl
import certifi

app = Flask(__name__)

def create_ssl_context():
    """Create SSL context for NCBI API calls"""
    return ssl.create_default_context(cafile=certifi.where())

ssl._create_default_https_context = create_ssl_context


def validate_fasta(fasta_text):
    """
    Validate FASTA format and DNA sequence.
    Returns: (is_valid, error_message, sequences_list)
    """
    if not fasta_text or fasta_text.strip() == '':
        return False, "Empty sequence provided", []

    if not fasta_text.strip().startswith('>'):
        return False, "Invalid FASTA format. Sequence must start with '>'", []

    try:
        fasta_io = StringIO(fasta_text)
        records = list(SeqIO.parse(fasta_io, "fasta"))

        if len(records) == 0:
            return False, "No valid sequence found in FASTA format", []

        sequences = []
        valid_nucleotides = set('ATCGNRYSWKMBDHV-')

        for record in records:
            sequence = str(record.seq).upper()
            sequence_set = set(sequence)

            if not sequence_set.issubset(valid_nucleotides):
                invalid_chars = sequence_set - valid_nucleotides
                return False, f"Invalid characters in sequence '{record.id}': {', '.join(invalid_chars)}", []

            if len(sequence) < 20:
                return False, f"Sequence '{record.id}' too short ({len(sequence)}bp). Minimum is 20bp", []

            sequences.append({
                'id': record.id,
                'sequence': sequence,
                'description': record.description
            })

        return True, None, sequences

    except Exception as e:
        return False, f"Error parsing FASTA format: {str(e)}", []


def run_blast(sequence):
    """
    Submit sequence to NCBI BLAST and parse results.
    Returns: (success, data_or_error)
    """
    try:
        print(f"Submitting BLAST query (length: {len(sequence)}bp)...")

        result_handle = NCBIWWW.qblast(
            program="blastn",
            database="core_nt",
            sequence=sequence,
            hitlist_size=10
        )

        print("BLAST query submitted. Parsing results...")

        blast_record = NCBIXML.read(result_handle)
        result_handle.close()

        hits = []
        for alignment in blast_record.alignments:
            if alignment.hsps:
                hsp = alignment.hsps[0]
                percent_identity = (hsp.identities / hsp.align_length) * 100

                hits.append({
                    'title': alignment.title,
                    'accession': alignment.accession,
                    'length': alignment.length,
                    'percent_identity': round(percent_identity, 2),
                    'alignment_length': hsp.align_length,
                    'e_value': hsp.expect,
                    'score': hsp.score,
                    'identities': hsp.identities,
                    'gaps': hsp.gaps
                })

        print(f"BLAST completed. Found {len(hits)} hits.")

        return True, {
            'query_id': blast_record.query,
            'query_length': blast_record.query_length,
            'hits': hits
        }

    except Exception as e:
        print(f"BLAST error: {str(e)}")
        return False, f"BLAST search failed: {str(e)}"


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/blast', methods=['POST'])
def blast():
    """Handle BLAST submission from text or file input"""
    try:
        fasta_text = request.form.get('fasta_text', '').strip()
        fasta_file = request.files.get('fasta_file')

        # Determine input source
        if fasta_file and fasta_file.filename:
            print(f"Processing file: {fasta_file.filename}")
            fasta_content = fasta_file.read().decode('utf-8')
        elif fasta_text:
            print("Processing text input")
            fasta_content = fasta_text
        else:
            return jsonify({
                'success': False,
                'error': 'No sequence provided'
            })

        # Validate FASTA
        is_valid, error_msg, sequences = validate_fasta(fasta_content)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg
            })

        # Return sequences for processing
        return jsonify({
            'success': True,
            'sequences': sequences,
            'total_sequences': len(sequences)
        })

    except Exception as e:
        print(f"Error in /blast: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })


@app.route('/blast_single', methods=['POST'])
def blast_single():
    """Run BLAST for a single sequence"""
    try:
        data = request.get_json()
        sequence_id = data.get('sequence_id')
        sequence = data.get('sequence')

        if not sequence:
            return jsonify({
                'success': False,
                'error': 'No sequence provided'
            })

        # Run BLAST
        success, result = run_blast(sequence)

        if success:
            return jsonify({
                'success': True,
                'sequence_id': sequence_id,
                'query_length': result['query_length'],
                'hits': result['hits']
            })
        else:
            return jsonify({
                'success': False,
                'error': result
            })

    except Exception as e:
        print(f"Error in /blast_single: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })


if __name__ == '__main__':
    print("Starting Flask BLAST application...")
    print("Navigate to http://127.0.0.1:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)