# DNA BLAST Search Web Application

Lightweight web app for submitting DNA sequences in FASTA format and running NCBI BLAST (blastn) using Biopython. Designed as a demo with a simple Flask backend and a modular vanilla-JS frontend.

**Repository:** https://github.com/crystalsong2021/dna-blast-app

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

dna-blast-app/
├── app/                          # Flask application package
│   ├── __init__.py               # Flask app factory / initialization
│   ├── config.py                 # Environment & NCBI settings
│   ├── routes.py                 # API endpoints
│   ├── services/                 # Business logic & helpers
│   │   ├── blast.py              # Biopython + NCBI interaction (uses blast_cache/)
│   │   ├── cache.py              # Simple caching utilities
│   │   ├── fasta.py              # FASTA parsing / validation
│   │   └── mock.py               # Mock helpers for tests/dev
│   ├── static/                   # Static assets served by Flask
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       ├── api.js            # Fetch/XHR helpers for backend endpoints (/blast, /blast_single)
│   │       ├── dom.js            # Centralized DOM selectors and element references
│   │       ├── file-handler.js   # File input, drag/drop, read and validate FASTA files
│   │       ├── main.js           # App entrypoint: event wiring, submit flow, orchestration
│   │       ├── results.js        # Render result tabs, tables and incremental updates per-sequence
│   │       ├── state.js          # Client-side state management and simple data helpers
│   │       └── ui-helpers.js     # Small UI utilities (alerts, progress bar, escape/output helpers)
│   └── templates/
│       └── index.html
├── blast_cache/                  # Local cache directory for BLAST results (JSON files keyed by sequence hash)
├── tests/                        # pytest-discovered tests and test data
│   ├── test_validation.py
│   └── data/
│       └── test_sequence.fasta
├── run.py                        # Simple local entrypoint (optional)
├── requirements.txt
└── README.md

Notes
- blast_cache/ is the local cache used by app/services/blast.py to store/read BLAST results and avoid repeated NCBI queries.

```
---

## Installation (macOS / Linux)

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository**
```bash
   git clone https://github.com/crystalsong2021/dna-blast-app.git
   cd dna-blast-app
```

2. **Create and activate virtual environment**
```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate   # On Windows
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```


## Running the Application

**Option 1: Using Flask CLI (recommended)**
```bash
export FLASK_APP=app          # On macOS/Linux
export FLASK_ENV=development  # Optional: enables debug mode
flask run --port 5001
```

**Option 2: Using Python module**
```bash
python -m flask run --app app --port 5001
```

**Option 3: Using run.py**
```bash
python run.py
```

Then open your browser to: **http://localhost:5001**

## Configuration

The app uses environment variables for configuration:
- `FLASK_ENV`: Set to `development` for debug mode
- See `app/config.py` for NCBI-specific settings

## Testing
```bash
pytest tests/
```

## Features

- Upload FASTA files or paste sequences directly
- Run BLAST searches against NCBI databases
- View results in organized tabs per sequence
- Local caching to avoid redundant NCBI queries

---

## How it works (high-level)

1. User provides FASTA text or uploads a FASTA file.
2. Frontend posts FASTA to /blast which validates and returns the parsed sequence list.
3. Frontend sends each sequence to /blast_single sequentially.
4. Each /blast_single response is rendered immediately as it arrives (incremental tabs).
5. Backend uses Biopython to call NCBI BLAST and parse XML results.

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
