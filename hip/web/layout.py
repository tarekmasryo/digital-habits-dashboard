from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from hip.core.filtering import FilterState
from hip.web.state import AppState, DisplayState


def render_sidebar(df: pd.DataFrame) -> AppState:
    is_cat_age = pd.api.types.is_categorical_dtype(df["age_group"]) if "age_group" in df else False
    age_options = (
        [str(x) for x in df["age_group"].cat.categories]
        if is_cat_age
        else sorted(df["age_group"].dropna().astype(str).unique().tolist())
    )
    occupation_options = sorted(df["occupation"].dropna().astype(str).unique().tolist())

    with st.sidebar:
        st.markdown(
            """
    <div style='text-align: center; padding: 20px;'>
        <h1 style='font-size: 2.5rem; margin: 0; color: white;'>🧬</h1>
        <h3 style='margin: 10px 0; color: white;'>AI Health Intelligence</h3>
        <p style='color: rgba(255,255,255,0.7); font-size: 0.9rem;'>Advanced analytics for digital wellbeing</p>
    </div>
    """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown("### 🎯 Risk Configuration")
        threshold = st.slider(
            "Risk Classification Threshold",
            min_value=0.1,
            max_value=0.9,
            value=0.5,
            step=0.05,
            help="Adjust sensitivity for high-risk classification",
        )

        st.markdown("---")
        st.markdown("### 🔍 Advanced Filters")

        selected_segments = st.multiselect(
            "Risk Segments",
            options=["Low Risk", "Moderate Risk", "High Risk"],
            default=["Low Risk", "Moderate Risk", "High Risk"],
        )

        selected_age_groups = st.multiselect(
            "Age Demographics",
            options=age_options,
            default=age_options,
        )

        selected_gender = st.multiselect(
            "Gender",
            options=["Male", "Female", "Other"],
            default=["Male", "Female", "Other"],
        )

        selected_occupation = st.multiselect(
            "Occupation Type",
            options=occupation_options,
            default=occupation_options,
        )

        screen_time_range = st.slider(
            "Screen Time (hours/day)",
            min_value=0.0,
            max_value=18.0,
            value=(0.0, 18.0),
            step=0.5,
        )

        stress_range = st.slider(
            "Stress Level Range",
            min_value=1.0,
            max_value=10.0,
            value=(1.0, 10.0),
            step=0.5,
        )

        st.markdown("---")
        st.markdown("### 📊 Display Preferences")

        show_animations = st.checkbox("Enable Animations", value=True)
        show_insights = st.checkbox("Policy Insights", value=True)
        real_time_mode = st.checkbox("Real-Time Mode (UI only)", value=False)

        st.markdown("---")
        st.markdown("### 📥 Data Export")

        export_format = st.selectbox("Export Format", ["CSV", "JSON"])

        if st.button("📊 Export Dataset", width="stretch"):
            if export_format == "CSV":
                data = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download CSV",
                    data=data,
                    file_name=f"health_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    width="stretch",
                )
            elif export_format == "JSON":
                data = df.to_json(orient="records", indent=2).encode("utf-8")
                st.download_button(
                    "⬇️ Download JSON",
                    data=data,
                    file_name=f"health_data_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    width="stretch",
                )

    filters = FilterState(
        threshold=threshold,
        selected_segments=selected_segments,
        selected_age_groups=selected_age_groups,
        selected_gender=selected_gender,
        selected_occupation=selected_occupation,
        screen_time_range=screen_time_range,
        stress_range=stress_range,
    )
    display = DisplayState(
        show_animations=show_animations,
        show_insights=show_insights,
        real_time_mode=real_time_mode,
    )
    return AppState(filters=filters, display=display)


def render_hero() -> None:
    st.markdown(
        """
<div class='hero-section'>
    <div style='text-align: center;'>
        <h1 class='hero-title'>🧬 AI Health Intelligence Platform</h1>
        <p class='hero-subtitle'>
            Decision-ready analytics for simulated digital wellbeing risk patterns
        </p>
        <p style='color: rgba(255,255,255,0.6); font-size: 0.95rem; margin-top: 15px;'>
            Risk scoring • Threshold policies • Scenario-based cohort review
        </p>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_kpis(plot_df: pd.DataFrame, metrics: dict[str, float], threshold: float) -> None:
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        total_users = len(plot_df)
        st.markdown(
            f"""
    <div class='metric-card'>
        <div class='metric-icon'>👥</div>
        <div class='metric-value'>{total_users:,}</div>
        <div class='metric-label'>Active Users</div>
        <div class='metric-change'>Monitoring scope</div>
    </div>
    """,
            unsafe_allow_html=True,
        )

    with col2:
        high_risk_count = (plot_df["risk_segment"] == "High Risk").sum()
        high_risk_pct = (high_risk_count / len(plot_df) * 100) if len(plot_df) > 0 else 0
        st.markdown(
            f"""
    <div class='metric-card'>
        <div class='metric-icon'>🚨</div>
        <div class='metric-value'>{high_risk_count:,}</div>
        <div class='metric-label'>High Risk</div>
        <div class='metric-change'>{high_risk_pct:.1f}% of population</div>
    </div>
    """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
    <div class='metric-card'>
        <div class='metric-icon'>🎯</div>
        <div class='metric-value'>{metrics["auc"]:.3f}</div>
        <div class='metric-label'>Policy AUC</div>
        <div class='metric-change'>Scoring diagnostics</div>
    </div>
    """,
            unsafe_allow_html=True,
        )

    with col4:
        avg_screen = plot_df["screen_hours"].mean()
        screen_delta = avg_screen - 7.0
        st.markdown(
            f"""
    <div class='metric-card'>
        <div class='metric-icon'>📱</div>
        <div class='metric-value'>{avg_screen:.1f}h</div>
        <div class='metric-label'>Avg Screen Time</div>
        <div class='metric-change'>{"↑" if screen_delta > 0 else "↓"} {abs(screen_delta):.1f}h vs baseline</div>
    </div>
    """,
            unsafe_allow_html=True,
        )

    with col5:
        avg_wellbeing = plot_df["wellbeing"].mean()
        st.markdown(
            f"""
    <div class='metric-card'>
        <div class='metric-icon'>💚</div>
        <div class='metric-value'>{avg_wellbeing:.1f}</div>
        <div class='metric-label'>Wellbeing Score</div>
        <div class='metric-change'>Out of 10.0</div>
    </div>
    """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Precision", f"{metrics['precision']:.1%}", f"F1: {metrics['f1']:.3f}")

    with col2:
        st.metric(
            "Recall",
            f"{metrics['recall']:.1%}",
            f"Specificity: {metrics['specificity']:.3f}",
        )

    with col3:
        if "flagged_for_review" in plot_df.columns:
            flagged_series = plot_df["flagged_for_review"]
        elif "flagged" in plot_df.columns:
            flagged_series = plot_df["flagged"]
        elif "risk_score" in plot_df.columns:
            flagged_series = (plot_df["risk_score"] >= threshold).astype(int)
        else:
            flagged_series = 0

        flagged_pct = float(getattr(flagged_series, "mean", lambda: 0.0)())
        st.metric("Flagged Users", f"{flagged_pct:.1%}", f"At threshold {threshold:.2f}")

    with col4:
        avg_stress = plot_df["stress"].mean()
        st.metric(
            "Avg Stress",
            f"{avg_stress:.1f}/10",
            f"Anxiety: {plot_df['anxiety'].mean():.1f}/10",
        )


def render_ai_insights(insights: list[dict[str, str]] | None, max_items: int = 6) -> None:
    """Render short AI insight cards.

    Defensive by design: callers may pass None or a wrong type.
    """
    if insights is None:
        return
    if not isinstance(insights, list):
        try:
            insights = list(insights)
        except Exception:
            return
    if not insights:
        return

    try:
        max_items = int(max_items)
    except Exception:
        max_items = 6

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
    <div class='section-header'>
        <div class='section-icon'>🤖</div>
        <div>
            <div class='section-title'>Policy Insights</div>
            <div class='section-subtitle'>Scoring-policy signals and review guidance</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    for insight in insights[:max_items]:
        alert_class = ""
        if insight.get("type") == "warning":
            alert_class = "insight-warning"
        elif insight.get("type") == "danger":
            alert_class = "insight-danger"

        st.markdown(
            f"""
        <div class='insight-card {alert_class}'>
            <div class='insight-title'>{insight["title"]}</div>
            <div class='insight-text'>{insight["text"]}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
