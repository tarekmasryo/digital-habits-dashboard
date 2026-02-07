# Run the Streamlit app from the project root
# Usage:
#   .\scripts\run.ps1

$ErrorActionPreference = "Stop"

if (!(Test-Path ".venv")) {
  Write-Host "Creating virtual environment (.venv)..." -ForegroundColor Cyan
  python -m venv .venv
}

Write-Host "Activating venv..." -ForegroundColor Cyan
. .\.venv\Scripts\Activate.ps1

Write-Host "Installing dependencies..." -ForegroundColor Cyan
python -m pip install -U pip
pip install -r requirements.txt

Write-Host "Starting Streamlit..." -ForegroundColor Green
python -m streamlit run app.py
