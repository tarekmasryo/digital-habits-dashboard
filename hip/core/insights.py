from __future__ import annotations

import pandas as pd


def generate_ai_insights(df_view: pd.DataFrame, metrics: dict):
    insights = []

    if len(df_view) == 0:
        return insights

    high_risk_pct = (df_view["risk_segment"] == "High Risk").mean() * 100
    if high_risk_pct > 35:
        insights.append(
            {
                "type": "danger",
                "title": "🚨 CRITICAL: High Risk Alert",
                "text": f"{high_risk_pct:.1f}% of monitored population in high-risk category. Systematic intervention programs are recommended.",
                "priority": "critical",
            }
        )
    elif high_risk_pct > 25:
        insights.append(
            {
                "type": "warning",
                "title": "⚠️ WARNING: Elevated Risk Levels",
                "text": f"{high_risk_pct:.1f}% high-risk users detected. Targeted support strategies are advised.",
                "priority": "high",
            }
        )

    high_risk_screen = df_view[df_view["risk_segment"] == "High Risk"]["screen_hours"].mean()
    low_risk_screen = df_view[df_view["risk_segment"] == "Low Risk"]["screen_hours"].mean()
    if high_risk_screen - low_risk_screen > 2.5:
        insights.append(
            {
                "type": "info",
                "title": "📱 Digital Exposure Correlation",
                "text": f"High-risk cohort shows {high_risk_screen - low_risk_screen:.1f}h higher daily screen time compared to low-risk users.",
                "priority": "medium",
            }
        )

    avg_sleep = df_view["sleep_hours"].mean()
    if avg_sleep < 6.5:
        critical_sleep = (df_view["sleep_hours"] < 6).sum()
        insights.append(
            {
                "type": "warning",
                "title": "😴 Sleep Deficit Detected",
                "text": f"Population average sleep: {avg_sleep:.1f}h. {critical_sleep:,} users are below 6 hours.",
                "priority": "high",
            }
        )

    avg_stress = df_view["stress"].mean()
    avg_anxiety = df_view["anxiety"].mean()
    if avg_stress > 6.5 or avg_anxiety > 6.5:
        insights.append(
            {
                "type": "warning",
                "title": "🧠 Mental Health Stress Indicators",
                "text": f"Elevated psychological metrics: Stress {avg_stress:.1f}/10, Anxiety {avg_anxiety:.1f}/10.",
                "priority": "high",
            }
        )

    if metrics["auc"] > 0.88:
        insights.append(
            {
                "type": "success",
                "title": "✅ Model Performance: Strong Signal",
                "text": f"Predictive performance on this dataset is strong (AUC: {metrics['auc']:.3f}). Risk stratification is internally consistent with the available features.",
                "priority": "low",
            }
        )
    elif metrics["auc"] < 0.75:
        insights.append(
            {
                "type": "warning",
                "title": "⚠️ Model Performance Warning",
                "text": f"AUC {metrics['auc']:.3f} is below the preferred range for reliable screening. Consider recalibration or feature refinement.",
                "priority": "medium",
            }
        )

    avg_loneliness = df_view["loneliness"].mean()
    if avg_loneliness > 6.0:
        insights.append(
            {
                "type": "warning",
                "title": "👥 Social Isolation Signal",
                "text": f"Average loneliness score: {avg_loneliness:.1f}/10. Social support and engagement may be helpful.",
                "priority": "medium",
            }
        )

    avg_exercise = df_view["exercise_minutes"].mean()
    if avg_exercise < 25:
        sedentary_count = (df_view["exercise_minutes"] < 15).sum()
        insights.append(
            {
                "type": "info",
                "title": "🏃 Physical Activity Deficit",
                "text": f"Average exercise: {avg_exercise:.0f} min/day. {sedentary_count:,} users show very low activity.",
                "priority": "medium",
            }
        )

    return sorted(
        insights,
        key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3}[x["priority"]],
    )
