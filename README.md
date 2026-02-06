# 🧠 Health Intelligence Platform

[![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-FF4B4B)](https://streamlit.io/)
[![Made by Tarek Masryo](https://img.shields.io/badge/Made%20by-Tarek%20Masryo-blue)](https://github.com/tarekmasryo)

### Decision-ready insights from behavioral and wellbeing signals 🤖

An interactive **Streamlit dashboard** + a complete data science workflow examining how screen time and digital behavior relate to psychological wellbeing — including anxiety, depression, stress, happiness, focus, and productivity.

Includes a tabular dataset of **3,500 participant records** with **24 research-inspired features**, plus a companion notebook for **EDA, feature engineering, modeling, and explainability**.

---

## 🔎 Important Note on Scoring

Psychological and behavioral indicators  
(e.g., `anxiety_score`, `depression_score`, `stress_level`, `happiness_score`, `focus_score`, `productivity_score`, `digital_dependence_score`)  
are generated as **continuous scores modeled on a broad 0–100 range**, **not** fixed **0–10 Likert items**.

This provides richer variance and makes the dataset more suitable for ML modeling and behavioral analytics.

---

## 🧩 Project Overview

| Component | Description |
|:--|:--|
| **Dashboard** | Streamlit app for executive KPIs, risk segments, trends, and scenario simulation. |
| **Dataset** | 24 variables covering demographics, digital activity, and wellbeing indicators. |
| **Notebook** | Full ML pipeline (EDA → Feature Engineering → Modeling → Explainability). |
| **Models** | Logistic Regression · Random Forest · XGBoost (GPU-ready). |
| **Goal** | Predict elevated wellbeing risk from behavioral and psychological patterns. |

---

## 📊 Dataset Summary

| Metric | Value |
|:--|:--|
| Rows | **3,500** |
| Columns | **24** |
| Target | **high_risk_flag** |
| Type | Tabular (CSV) |

---

## 🧠 Feature Groups

### 🧬 Demographics
Age · Gender · Region · Income Level · Education Level

### 💻 Digital Behavior
Daily Screen Time · Phone Unlocks · Notifications · Social Media Hours · Study Time

### 🧘 Wellbeing Indicators
Anxiety · Depression · Stress · Happiness · Focus · Productivity

### ⚠️ Risk Indicator
`high_risk_flag` — a binary label derived via a **multi-factor wellbeing score** combining digital intensity, emotional state, and cognitive balance.

---

## 📘 Target Definition

The target variable **`high_risk_flag`** represents individuals with increased wellbeing vulnerability.  
It is defined using a scoring rule that blends:

- High digital activity (screen time, notifications, unlocks)
- Elevated stress/anxiety levels
- Lower happiness/focus scores

Approximate distribution: **15–20% high-risk**.

---

## 📸 Dashboard Preview

### 1️⃣ AI Health Intelligence — Hero Overview
<p align="center">
  <img src="assets/ai-health-hero.png" alt="Health Intelligence Platform — Hero overview with key KPIs" />
</p>

---

### 2️⃣ AI-Powered Insights Cards
<p align="center">
  <img src="assets/ai-insights-cards.png" alt="AI-powered insights cards for risk, stress, digital exposure, and model performance" />
</p>

---

### 3️⃣ Executive Risk Overview
<p align="center">
  <img src="assets/executive-risk-overview.png" alt="Risk score distribution and risk segment donut chart" />
</p>

---

### 4️⃣ 90-Day Population Health Trends
<p align="center">
  <img src="assets/population-health-trends.png" alt="90-day trends for screen time, stress, wellbeing, sleep, high-risk population, and engagement" />
</p>

---

### 5️⃣ Demographic Risk Breakdown
<p align="center">
  <img src="assets/demographic-risk-breakdown.png" alt="Age, gender, location, and occupation risk distributions" />
</p>

---

### 6️⃣ Digital Behavior & Activity Balance
<p align="center">
  <img src="assets/digital-behavior-balance.png" alt="Hourly activity patterns, app usage, digital interaction metrics, and physical activity balance" />
</p>

---

### 7️⃣ Model Insights & Correlations
<p align="center">
  <img src="assets/model-insights-and-correlations.png" alt="Feature importance and relationships such as screen time vs sleep and stress vs wellbeing" />
</p>

---

### 8️⃣ Scenario Simulator — Individual Risk Profile
<p align="center">
  <img src="assets/scenario-simulator.png" alt="Scenario simulator with sliders, risk score, risk category, and radar profile view" />
</p>

---

## 📎 Companion Notebook

The end-to-end analysis and modeling notebook is available on Kaggle:

- **Predicting Wellbeing Risk (EDA → FE → Modeling → Explainability)**  
  https://www.kaggle.com/code/tarekmasryo/predicting-wellbeing-risk

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/tarekmasryo/health-intelligence-platform.git
cd health-intelligence-platform

# Create venv
python -m venv .venv

# Activate venv
# Windows PowerShell:
#   .\.venv\Scripts\Activate.ps1
# Windows CMD:
#   .\.venv\Scripts\activate.bat
# macOS/Linux:
#   source .venv/bin/activate

# Upgrade pip (recommended)
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

Open: **http://localhost:8501**

---

## 📁 Repo Structure

- `app.py` — Streamlit dashboard entry point
- `assets/` — dashboard screenshots used in the README
- `requirements.txt` — runtime dependencies

---

## ⚠️ Disclaimer

This project is for educational and research purposes only.  
It is **not** a medical diagnostic tool and should not be used for clinical decision-making.
