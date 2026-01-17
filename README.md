# DNA BLAST Search Web Application

A lightweight web application for submitting DNA sequences in FASTA format and running **NCBI BLAST (blastn)** searches using **Biopython**.
Designed as a clean demo project showcasing modular frontend architecture and a simple Flask backend.

---

## Features

- 🧬 Accepts DNA sequences via:
  - Text input (FASTA format)
  - FASTA file upload (.fasta, .fa, .txt)
- ✅ FASTA format and nucleotide validation
- 🔬 Runs `blastn` against NCBI `core_nt` database
- ⚡ Processes **multiple sequences sequentially** with streaming results
- 📊 Displays BLAST hits in sortable, readable tables
- 🧩 Modular JavaScript architecture (API, state, UI, results)
- 🎨 Styled with Bootstrap 5

---

## Tech Stack

### Backend
- Python 3
- Flask
- Biopython (`NCBIWWW`, `NCBIXML`)
- certifi (SSL compatibility)

### Frontend
- Vanilla JavaScript (modular pattern)
- Bootstrap 5
- HTML5 / CSS3

## Design Decisions

- The app supports a single FASTA sequence per submission, which matches common BLAST usage and keeps the interface simple.
- BLAST queries are submitted sequentially to respect NCBI usage guidelines.
- Biopython is used both for FASTA parsing and BLAST submission to ensure correctness.
- Bootstrap is used for lightweight styling without additional frontend frameworks.

---

## Project Structure
project-root/
│
├── app/
│ ├── init.py
│ ├── routes/
│ │ └── blast_routes.py
│ ├── services/
│ │ └── blast_service.py
│ ├── utils/
│ │ └── fasta_validator.py
│ └── config.py
│
├── static/
│ ├── css/style.css
│ └── js/
│ ├── api.js # API communication layer
│ ├── state.js # Central app state
│ ├── dom.js # DOM references
│ ├── ui-helpers.js # UI utilities
│ ├── file-handler.js # File upload logic
│ ├── results.js # BLAST results rendering
│ └── main.js # App controller
│
├── templates/
│ └── index.html
│
├── run.py
├── requirements.txt
└── README.md


---

## Installation & Setup

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Run the app
python run.py


Visit:

http://127.0.0.1:5001

How It Works (High-Level)

User submits FASTA text or file

/blast endpoint:

validates FASTA

parses multiple sequences

Frontend streams sequences one-by-one

/blast_single:

submits each sequence to NCBI BLAST

parses XML results

Results appear as soon as each sequence finishes

Notes

Uses NCBI public BLAST API (no local database)

Designed for demo / educational use

NCBI rate limits apply (avoid large batches)


## Testing

A small standalone test file is included to validate FASTA input handling.

To run the FASTA validation tests:

```bash
python test_validation.py

---
##
Future Improvements

Background task queue (Celery / RQ)

Accession links to NCBI

Result export (CSV)

Local BLAST support


