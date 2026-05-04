# 🧠 Health Intelligence Platform (HIP)

[![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-FF4B4B)](https://streamlit.io/)
[![Made by Tarek Masryo](https://img.shields.io/badge/Made%20by-Tarek%20Masryo-blue)](https://github.com/tarekmasryo)

### 🤖 Decision-ready insights from digital behavior & wellbeing signals

**Health Intelligence Platform** is a production-structured **Streamlit dashboard** that uses synthetic behavioral and wellbeing signals to produce **risk scoring**, **segments**, **threshold policies**, and **exportable cohort reports**.

---

## ✨ What you get

- ✅ **Executive KPIs** (population snapshot + key rates)
- ✅ **Risk scoring** (`risk_score`) + configurable **threshold** → `flagged_for_review`
- ✅ **Risk segments** (demographics × behavior slices)
- ✅ **Scoring diagnostics** (ROC / PR / confusion matrix + threshold trade-offs on simulated labels)
- ✅ **Scenario simulator** (what-if sliders to see risk movement)
- ✅ **Cohort exports** (downloadable cohort CSVs)

---

## 🧩 Project overview

| Component | Description |
|:--|:--|
| **Dashboard** | Streamlit app for executive KPIs, risk segments, trends, simulation, and reports |
| **Core logic** | Reusable Python package for scoring, metrics, insights, and data utilities |
| **Tests** | Pytest suite for core logic and entrypoint checks |
| **Tooling** | Ruff formatter/linter plus optional pre-commit hooks |

---

## 🧠 Scoring, labels, and thresholds

The dashboard uses simulated behavioral and wellbeing data.

- `risk_score` is a transparent scoring-policy output between 0 and 1.
- `high_risk` is a synthetic outcome label sampled from the generated risk probability.
- The sidebar threshold controls operational flagging for review:
  - `flagged_for_review = risk_score >= threshold`

The diagnostics are intended to explain threshold trade-offs and scoring behavior on simulated data. They are not clinical validation metrics and should not be interpreted as medical evidence.

---

## 📸 Dashboard preview

### 1️⃣ AI Health Intelligence — Hero Overview

<p align="center">
  <img src="assets/ai-health-hero.png" alt="Hero overview with KPIs" />
</p>

### 2️⃣ Policy Insights Cards

<p align="center">
  <img src="assets/ai-insights-cards.png" alt="Policy insight cards" />
</p>

### 3️⃣ Executive Risk Overview

<p align="center">
  <img src="assets/executive-risk-overview.png" alt="Risk distribution and segments" />
</p>

### 4️⃣ 90-Day Population Health Trends

<p align="center">
  <img src="assets/population-health-trends.png" alt="Population-level trends" />
</p>

### 5️⃣ Demographic Risk Breakdown

<p align="center">
  <img src="assets/demographic-risk-breakdown.png" alt="Demographic slices" />
</p>

### 6️⃣ Digital Behavior & Activity Balance

<p align="center">
  <img src="assets/digital-behavior-balance.png" alt="Behavior analytics" />
</p>

### 7️⃣ Scoring Diagnostics & Correlations

<p align="center">
  <img src="assets/model-insights-and-correlations.png" alt="Scoring diagnostics and correlations" />
</p>

### 8️⃣ Scenario Simulator — Individual Risk Profile

<p align="center">
  <img src="assets/scenario-simulator.png" alt="Scenario simulator" />
</p>

---

## 🚀 Quick start

```bash
# Clone
git clone https://github.com/tarekmasryo/health-intelligence-platform.git
cd health-intelligence-platform

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
#   .\.venv\Scripts\Activate.ps1
# macOS/Linux:
#   source .venv/bin/activate

# Install runtime dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

Open: **http://localhost:8501**

---

## 🧪 Dev workflow

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

### Format

```bash
python -m ruff format .
python -m ruff format --check .
```

### Lint

```bash
python -m ruff check .
```

### Tests

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -q
```

Windows PowerShell:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD="1"
pytest -q
```

> 💡 On Windows, if `ruff` is not recognized as a command, use `python -m ruff ...`.

---

## 📁 Repo structure

```text
.
├── app.py                  # Streamlit entrypoint (thin wrapper)
├── hip/                    # Main package (core + web)
│   ├── __init__.py
│   ├── core/               # Scoring, metrics, insights, data utilities
│   └── web/                # Streamlit UI, layout, tabs, styles
├── tests/                  # Pytest suite
├── assets/                 # README screenshots
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

### 🧠 Why `hip/` exists

`hip/` makes the project:

- **importable** — clean package boundaries instead of one large script
- **testable** — core logic can be tested without the Streamlit runtime
- **maintainable** — scoring, metrics, and UI code are separated

---

## 🛠️ Common fix: Windows launcher error

If you unzip or copy the project and it contains an old `.venv`, you may see errors referencing a previous path.

Fix:

1. Delete `.venv`
2. Create a fresh virtual environment:

```bash
python -m venv .venv
```

3. Reinstall dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## 📎 Companion Notebook

A companion Kaggle notebook can be linked here when published.

Suggested companion flow:

```text
EDA → feature engineering → baseline modeling → dashboard handoff
```

---

## 📄 License

Apache License 2.0. See [LICENSE](LICENSE).

---

## ⚠️ Disclaimer

Educational / portfolio use only — simulated data, not medical advice, clinical diagnosis, or a validated healthcare product.
