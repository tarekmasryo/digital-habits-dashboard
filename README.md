# 🧠 Health Intelligence Platform (HIP)

[![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-FF4B4B)](https://streamlit.io/)
[![Made by Tarek Masryo](https://img.shields.io/badge/Made%20by-Tarek%20Masryo-blue)](https://github.com/tarekmasryo)

### 🤖 Decision-ready insights from digital behavior & wellbeing signals

**Health Intelligence Platform** is a production-structured **Streamlit dashboard** that uses synthetic behavioral and wellbeing signals to produce:
**risk scoring**, **segments**, **threshold policies**, and **exportable cohort reports**.

---

## ✨ What you get

✅ **Executive KPIs** (population snapshot + key rates)  
✅ **Risk scoring** (`risk_score`) + configurable **threshold** → `high_risk`  
✅ **Risk segments** (demographics × behavior slices)  
✅ **Model performance** (ROC / PR / confusion matrix + threshold trade-offs)  
✅ **Intervention simulator** (what-if sliders to see risk movement)  
✅ **Cohort exports** (downloadable cohort CSVs)

---

## 🧩 Project overview

| Component | Description |
|:--|:--|
| **Dashboard** | Streamlit app for executive KPIs, risk segments, trends, simulation & reports |
| **Core logic** | Reusable Python package: scoring, metrics, insights, data utilities |
| **Tests** | Pytest suite for core + entrypoint checks |
| **Tooling** | Ruff formatter/linter + optional pre-commit hooks |

---

## 🧠 Scoring & labels

The app uses a continuous **risk score**:

- `risk_score` is computed from behavioral + wellbeing features
- `high_risk` is derived by applying a configurable threshold:
  - `high_risk = (risk_score >= threshold)`

This makes the dashboard **decision-oriented**: you can tune the threshold to balance **coverage vs. false positives**.

---

## 📸 Dashboard preview

### 1️⃣ AI Health Intelligence — Hero Overview
<p align="center">
  <img src="assets/ai-health-hero.png" alt="Hero overview with KPIs" />
</p>

### 2️⃣ AI-Powered Insights Cards
<p align="center">
  <img src="assets/ai-insights-cards.png" alt="AI-powered insight cards" />
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

### 7️⃣ Model Insights & Correlations
<p align="center">
  <img src="assets/model-insights-and-correlations.png" alt="Model insights and correlations" />
</p>

### 8️⃣ Scenario Simulator — Individual Risk Profile
<p align="center">
  <img src="assets/scenario-simulator.png" alt="Intervention simulator" />
</p>

---

## 🚀 Quick start

```bash
# Clone
git clone https://github.com/tarekmasryo/health-intelligence-platform.git
cd health-intelligence-platform

# Create venv
python -m venv .venv

# Activate venv
# Windows PowerShell:
#   .\.venv\Scripts\Activate.ps1
# macOS/Linux:
#   source .venv/bin/activate

# Install runtime deps
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

Open: **http://localhost:8501**

---

## 🧪 Dev workflow (format • lint • tests)

```bash
python -m pip install -r requirements-dev.txt
```

### 🧼 Format
```bash
python -m ruff format .
python -m ruff format --check .
```

### 🧯 Lint
```bash
python -m ruff check .
```

### ✅ Tests
```bash
pytest -q
```

> 💡 On Windows, if `ruff` is not recognized as a command, always use `python -m ruff ...`

---

## 📁 Repo structure

```
.
├── app.py                  # Streamlit entrypoint (thin wrapper)
├── hip/                    # Main package (core + web)
│   ├── __init__.py
│   ├── core/               # scoring, metrics, insights, data utilities
│   └── web/                # Streamlit UI (layout, tabs, styles)
├── tests/                  # pytest suite
├── assets/                 # README screenshots
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

### 🧠 Why `hip/` exists
`hip/` makes the project:
- **importable** (clean boundaries instead of a single giant script)
- **testable** (core logic can be tested without Streamlit runtime)
- **maintainable** (core logic separated from UI)

---

## 🛠️ Common fix (Windows launcher error)

If you unzip/copy the project and it contains an old `.venv`, you may see errors referencing a previous path.
Fix:
1) Delete `.venv`
2) Create a fresh one:
```bash
python -m venv .venv
```
3) Reinstall dependencies.

---

## 📎 Companion Notebook (optional)

- Kaggle notebook (EDA → FE → Modeling):  
  https://www.kaggle.com/code/tarekmasryo/predicting-wellbeing-risk

---

## 📄 License

Apache License 2.0. See [LICENSE](LICENSE).

---

## ⚠️ Disclaimer
Educational / research only — not medical advice or clinical diagnosis.
