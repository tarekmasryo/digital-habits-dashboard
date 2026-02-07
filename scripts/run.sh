#!/usr/bin/env bash
set -euo pipefail

# Run the Streamlit app from the project root
# Usage:
#   bash scripts/run.sh

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment (.venv)..."
  python -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install -U pip
pip install -r requirements.txt

python -m streamlit run app.py
