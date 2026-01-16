# DNA BLAST Web Application - Serverless

A serverless DNA BLAST search application deployed on AWS Lambda with automated CI/CD.

## 🌐 Live Demo

**Coming soon** - Will be deployed after first push to main branch.

## 🚀 Features

- ✅ Accepts DNA sequences in FASTA format
- ✅ Validates input before submission
- ✅ Searches NCBI's nucleotide database (blastn against nt)
- ✅ Displays results in clean, sortable table
- ✅ Serverless architecture (AWS Lambda)
- ✅ Automated CI/CD pipeline (GitHub Actions)
- ✅ File upload support

## 🏗️ Architecture

GitHub → GitHub Actions → AWS Lambda + API Gateway → NCBI BLAST


## 💻 Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/dna-blast-app.git
cd dna-blast-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
Visit http://localhost:5000

🧪 Testing
# Run tests
python test_validation.py
📦 Deployment
Manual Deployment
# Install Serverless Framework
npm install -g serverless
npm install --save-dev serverless-python-requirements

# Configure AWS credentials
aws configure

# Deploy
serverless deploy --stage prod
Automatic Deployment (CI/CD)
Every push to
main
branch automatically:

✅ Runs tests
✅ Deploys to AWS Lambda
✅ Updates live application
🛠️ Tech Stack
Backend: Python 3.11, Flask, Biopython
Cloud: AWS Lambda, API Gateway
Frontend: HTML, Bootstrap 5, Vanilla JavaScript
CI/CD: GitHub Actions
IaC: Serverless Framework
💰 Cost
AWS Lambda free tier: 1M requests/month + 400,000 GB-seconds compute.

Estimated cost for demo usage: $0.00/month ✅

📝 Design Decisions
Serverless Architecture: Chose Lambda for cost-efficiency and auto-scaling
Single Repository: All code (app + infrastructure + CI/CD) in one place
Biopython: Used official NCBI BLAST API wrapper for reliability
Bootstrap: Clean, responsive UI without custom CSS complexity
Vanilla JavaScript: No framework overhead for simple interactivity
🔐 Security
HTTPS enabled via API Gateway
CORS configured for secure cross-origin requests
AWS credentials stored as GitHub Secrets
Input validation prevents malformed requests
📄 License
MIT License

