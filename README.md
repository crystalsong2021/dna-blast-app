# DNA BLAST Search Web Application

Lightweight web app for submitting DNA sequences in FASTA format and running NCBI BLAST (blastn) using Biopython. Designed as a demo with a simple Flask backend and a modular vanilla-JS frontend.

---

## Features

- Accepts DNA sequences via text input (FASTA) or FASTA file upload (.fasta, .fa, .txt)
- FASTA format and nucleotide validation
- Sequential BLAST submissions with incremental rendering of results
- Safe DOM updates to reduce XSS risk
- Modular frontend: api.js, state.js, dom.js, ui-helpers.js, file-handler.js, results.js, main.js

---

## Tech Stack

- Python 3, Flask
- Biopython (NCBIWWW, NCBIXML)
- Vanilla JavaScript, Bootstrap 5
- certifi (SSL compatibility)

---

## Project structure

```
app/
├── __init__.py               # Flask app factory / initialization
├── config.py                 # Environment & NCBI settings
├── routes.py                 # API endpoints
├── services/
│   ├── blast.py              # Biopython + NCBI interaction
│   ├── cache.py              # Simple caching utilities
│   ├── fasta.py              # FASTA parsing / validation
│   └── mock.py               # Mock helpers for tests/dev
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── api.js
│       ├── dom.js
│       ├── file-handler.js
│       ├── main.js
│       ├── results.js
│       ├── state.js
│       └── ui-helpers.js
└── templates/
    └── index.html
    
```
Other files (root)
- requirements.txt
- README.md

---

## Installation (macOS / Linux)

1. Create and activate virtualenv
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the app (Flask)
```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run --port 5001
```
or
```bash
python -m flask run --app app --port 5001
```

Open: http://127.0.0.1:5001

Notes: these commands expect app/__init__.py to expose an app factory or app object. If your entrypoint differs, run the script you use locally (for example: python run.py).

---

## How it works (high-level)

1. User provides FASTA text or uploads a FASTA file.
2. Frontend posts FASTA to /blast which validates and returns the parsed sequence list.
3. Frontend sends each sequence to /blast_single sequentially.
4. Each /blast_single response is rendered immediately as it arrives (incremental tabs).
5. Backend uses Biopython to call NCBI BLAST and parse XML results.

---

## Testing

If present, run the FASTA validation test:
```bash
python test_validation.py
```
Or run your test suite (pytest) if configured:
```bash
pytest
```

---
### BLAST Integration

Sequences are submitted to NCBI BLAST using Biopython’s `NCBIWWW.qblast` API
(`blastn` against the `core_nt` database). By default, `qblast` returns results
in XML format, which are parsed using `Bio.Blast.NCBIXML`.

This follows the recommended usage pattern in the Biopython documentation:
- https://biopython.org/docs/latest/api/Bio.Blast.NCBIWWW.html
- https://biopython.org/docs/latest/Tutorial/chapter_blast.html

---
### Design Decisions & Limitations

- BLAST queries are executed synchronously for simplicity. In a production
  environment, these would be handled asynchronously to avoid blocking the
  web server.
- Only the top HSP per alignment is displayed to keep results readable.
- Multi-sequence FASTA files are validated but processed sequentially.
- Client-side validation prevents empty submissions; server-side validation
  exists as a safety net.
---
## Notes & Recommendations

- Default behavior limits top hits to protect against long runtimes and NCBI rate limits. Make hit count configurable with a reasonable server-side cap.
- The handler.py adapter (for AWS Lambda) is optional — remove it if not used.
- For heavy usage, use a background queue (Celery/RQ) and/or a local BLAST installation.

---
