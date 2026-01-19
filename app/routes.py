"""
Main routes for the DNA BLAST web application.

- Uses Flask Blueprint to organize endpoints.
- Serves frontend template and handles BLAST API calls.
- Integrates FASTA validation and BLAST service modules.
"""

from flask import Blueprint, render_template, request, jsonify
from .services.fasta import validate_fasta
from .services.blast import run_blast

# Blueprint for main app routes
bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    """Render the main page (index.html) for user input."""
    return render_template("index.html")


@bp.route("/blast", methods=["POST"])
def blast():
    """
    Handle bulk FASTA submission (text field or file upload).

    - Validates FASTA format using validate_fasta()
    - Returns a JSON list of sequences for frontend processing
    """
    fasta_text = request.form.get("fasta_text", "").strip()
    fasta_file = request.files.get("fasta_file")

    if fasta_file and fasta_file.filename:
        fasta_content = fasta_file.read().decode("utf-8")
    elif fasta_text:
        fasta_content = fasta_text
    else:
        return jsonify(success=False, error="No sequence provided")

    valid, error, sequences = validate_fasta(fasta_content)
    if not valid:
        return jsonify(success=False, error=error)

    return jsonify(success=True, sequences=sequences)


@bp.route("/blast_single", methods=["POST"])
def blast_single():
    """
    Handle BLAST search for a single sequence.

    - Receives JSON: sequence and sequence_id
    - Calls run_blast() from blast service
    - Returns JSON with top hits and details
    """
    data = request.get_json()
    sequence = data.get("sequence")
    sequence_id = data.get("sequence_id")

    if not sequence:
        return jsonify(success=False, error="No sequence provided")

    success, result = run_blast(sequence)
    if not success:
        return jsonify(success=False, error=result)

    return jsonify(
        success=True,
        sequence_id=sequence_id,
        query_length=result["query_length"],
        hits=result["hits"],
    )
