from __future__ import annotations

import streamlit as st

from hip.core.data import GeneratedData, generate_advanced_data
from hip.core.filtering import apply_filters
from hip.core.insights import generate_ai_insights
from hip.core.metrics import calculate_metrics
from hip.web.layout import render_ai_insights, render_hero, render_kpis, render_sidebar
from hip.web.styles import apply_global_styles
from hip.web.tabs import (
    render_advanced_risk_assessment,
    render_behavioral_analytics,
    render_clinical_reports,
    render_executive_dashboard,
    render_intervention_simulator,
    render_model_performance,
)


@st.cache_data(show_spinner=False)
def get_data(n_users: int, seed: int) -> GeneratedData:
    return generate_advanced_data(n_users=n_users, seed=seed)


def run() -> None:
    st.set_page_config(
        page_title="AI Health Intelligence Platform",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    data = get_data(n_users=5000, seed=42)
    state = render_sidebar(data.population)

    apply_global_styles(disable_animations=not state.display.show_animations)

    filtered_df, no_filter_data = apply_filters(data.population, state.filters)
    plot_df = filtered_df.copy() if not no_filter_data else data.population.copy()

    df_metrics = plot_df if plot_df["high_risk"].nunique() >= 2 else data.population.copy()
    metrics_scope = "Filtered Data" if df_metrics is plot_df else "Full Population"
    metrics = calculate_metrics(df_metrics, threshold=state.filters.threshold)

    insights = generate_ai_insights(plot_df, metrics)

    render_hero()
    render_kpis(plot_df, metrics, state.filters.threshold)
    if state.display.show_insights:
        render_ai_insights(insights)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "📊 Executive Dashboard",
            "🎯 Risk Analytics",
            "🧠 Behavioral Insights",
            "📈 Model Performance",
            "💡 Intervention Simulator",
            "🏥 Clinical Reports",
        ]
    )

    with tab1:
        render_executive_dashboard(plot_df, data.time_series, data.hourly, state.filters.threshold)

    with tab2:
        render_advanced_risk_assessment(plot_df, df_metrics, metrics, state.filters.threshold)

    with tab3:
        render_behavioral_analytics(plot_df, data.hourly)

    with tab4:
        render_model_performance(
            plot_df, df_metrics, metrics, state.filters.threshold, metrics_scope
        )

    with tab5:
        render_intervention_simulator(
            plot_df, state.display.real_time_mode, state.filters.threshold
        )

    with tab6:
        render_clinical_reports(plot_df)
