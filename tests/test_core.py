import pandas as pd

from hip.core.data import generate_advanced_data
from hip.core.insights import generate_ai_insights
from hip.core.metrics import calculate_metrics


def test_generate_advanced_data_basic():
    data = generate_advanced_data(n_users=200, seed=7, now=pd.Timestamp("2026-02-07"))
    assert data.population.shape[0] == 200
    assert {"risk_score", "high_risk", "risk_segment"}.issubset(set(data.population.columns))
    assert data.time_series.shape[0] > 0
    assert data.hourly.shape[0] > 0


def test_metrics_and_insights_roundtrip():
    data = generate_advanced_data(n_users=500, seed=3, now=pd.Timestamp("2026-02-07"))
    df_metrics = data.population
    metrics = calculate_metrics(df_metrics, threshold=0.5)
    assert "auc" in metrics
    assert "precision" in metrics
    insights = generate_ai_insights(data.population, metrics)
    assert isinstance(insights, list)
    assert len(insights) > 0
    assert all("title" in x and "text" in x for x in insights)


def test_generated_risk_segments_are_reasonably_balanced():
    data = generate_advanced_data(n_users=5000, seed=42, now=pd.Timestamp("2026-02-07"))
    shares = data.population["risk_segment"].value_counts(normalize=True)

    assert 0.25 <= shares.get("Low Risk", 0.0) <= 0.60
    assert 0.20 <= shares.get("Moderate Risk", 0.0) <= 0.50
    assert 0.10 <= shares.get("High Risk", 0.0) <= 0.35
