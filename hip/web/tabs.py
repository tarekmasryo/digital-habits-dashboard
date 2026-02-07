from __future__ import annotations

from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from sklearn.metrics import confusion_matrix, precision_recall_curve, roc_curve

from hip.core.metrics import calculate_metrics
from hip.core.scoring import compute_risk_from_features


def render_executive_dashboard(
    plot_df: pd.DataFrame, time_series_df: pd.DataFrame, hourly_df: pd.DataFrame, threshold: float
) -> None:
    st.markdown(
        """
    <div class='section-header'>
        <div class='section-icon'>📊</div>
        <div>
            <div class='section-title'>Population Health Overview</div>
            <div class='section-subtitle'>Comprehensive metrics and trend analysis</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("#### Risk Score Distribution & Segmentation")
        fig = px.histogram(
            plot_df,
            x="risk_score",
            color="risk_segment",
            nbins=60,
            color_discrete_map={
                "Low Risk": "#10b981",
                "Moderate Risk": "#f59e0b",
                "High Risk": "#ef4444",
            },
            labels={"risk_score": "Risk Score", "count": "User Count"},
        )
        fig.add_vline(
            x=threshold,
            line_dash="dash",
            line_color="#ffffff",
            line_width=3,
            annotation_text=f"Threshold: {threshold:.2f}",
            annotation_position="top right",
        )
        fig.update_layout(
            height=450,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff", size=12),
            margin=dict(l=40, r=20, t=20, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Risk Segment Distribution")
        segment_counts = plot_df["risk_segment"].value_counts()
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=segment_counts.index,
                    values=segment_counts.values,
                    hole=0.6,
                    marker=dict(
                        colors=["#10b981", "#f59e0b", "#ef4444"],
                        line=dict(color="rgba(0,0,0,0.5)", width=3),
                    ),
                    textfont=dict(size=15, color="#fff"),
                    textposition="outside",
                )
            ]
        )
        fig.update_layout(
            height=450,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff", size=12),
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 90-Day Population Health Trends")

    fig = make_subplots(
        rows=2,
        cols=3,
        subplot_titles=(
            "Screen Time Trajectory",
            "Stress Evolution",
            "Wellbeing Index",
            "High-Risk Population",
            "Sleep Patterns",
            "Engagement Metrics",
        ),
        vertical_spacing=0.12,
        horizontal_spacing=0.08,
    )

    fig.add_trace(
        go.Scatter(
            x=time_series_df["date"],
            y=time_series_df["avg_screen"],
            mode="lines",
            name="Screen Time",
            line=dict(color="#3b82f6", width=3),
            fill="tozeroy",
            fillcolor="rgba(59,130,246,0.3)",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=time_series_df["date"],
            y=time_series_df["avg_stress"],
            mode="lines",
            name="Stress",
            line=dict(color="#ef4444", width=3),
            fill="tozeroy",
            fillcolor="rgba(239,68,68,0.3)",
        ),
        row=1,
        col=2,
    )

    fig.add_trace(
        go.Scatter(
            x=time_series_df["date"],
            y=time_series_df["avg_wellbeing"],
            mode="lines",
            name="Wellbeing",
            line=dict(color="#10b981", width=3),
            fill="tozeroy",
            fillcolor="rgba(16,185,129,0.3)",
        ),
        row=1,
        col=3,
    )

    fig.add_trace(
        go.Bar(
            x=time_series_df["date"],
            y=time_series_df["high_risk_count"],
            name="High-Risk Users",
            marker=dict(color="#f59e0b"),
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=time_series_df["date"],
            y=time_series_df["avg_sleep"],
            mode="lines+markers",
            name="Sleep",
            line=dict(color="#8b5cf6", width=3),
            fill="tozeroy",
            fillcolor="rgba(139,92,246,0.3)",
        ),
        row=2,
        col=2,
    )

    fig.add_trace(
        go.Scatter(
            x=time_series_df["date"],
            y=time_series_df["engagement"],
            mode="lines",
            name="Engagement",
            line=dict(color="#ec4899", width=3),
            fill="tozeroy",
            fillcolor="rgba(236,72,153,0.3)",
        ),
        row=2,
        col=3,
    )

    fig.update_layout(
        height=700,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff", size=11),
        margin=dict(l=40, r=20, t=50, b=40),
        showlegend=False,
    )

    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("#### Age Distribution (Avg Risk)")
        age_risk = plot_df.groupby("age_group")["risk_score"].mean().reset_index()
        fig = px.bar(
            age_risk,
            x="age_group",
            y="risk_score",
            color="risk_score",
            color_continuous_scale=["#10b981", "#f59e0b", "#ef4444"],
        )
        fig.update_layout(
            height=350,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Gender Distribution")
        gender_counts = plot_df["gender"].value_counts()
        fig = px.bar(
            x=gender_counts.index,
            y=gender_counts.values,
            color=gender_counts.index,
            color_discrete_map={
                "Male": "#3b82f6",
                "Female": "#ec4899",
                "Other": "#8b5cf6",
            },
        )
        fig.update_layout(
            height=350,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("#### Location Distribution")
        location_counts = plot_df["location"].value_counts()
        fig = px.pie(
            values=location_counts.values,
            names=location_counts.index,
            color_discrete_sequence=["#3b82f6", "#8b5cf6", "#10b981"],
            hole=0.4,
        )
        fig.update_layout(
            height=350,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("#### Occupation (Avg Risk)")
        occ_risk = plot_df.groupby("occupation")["risk_score"].mean().sort_values(ascending=False)
        fig = px.bar(
            x=occ_risk.values,
            y=occ_risk.index,
            orientation="h",
            color=occ_risk.values,
            color_continuous_scale=["#10b981", "#f59e0b", "#ef4444"],
        )
        fig.update_layout(
            height=350,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)


def render_advanced_risk_assessment(
    plot_df: pd.DataFrame, df_metrics: pd.DataFrame, metrics: dict[str, float], threshold: float
) -> None:
    st.markdown(
        """
    <div class='section-header'>
        <div class='section-icon'>🎯</div>
        <div>
            <div class='section-title'>Advanced Risk Assessment</div>
            <div class='section-subtitle'>Deep dive into risk factors and correlations</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown("#### Multi-Factor Correlation Matrix")
        corr_cols = [
            "screen_hours",
            "sleep_hours",
            "stress",
            "anxiety",
            "depression",
            "wellbeing",
            "mood",
            "energy",
            "social_support",
            "loneliness",
            "risk_score",
        ]
        corr_matrix = plot_df[corr_cols].corr()

        fig = go.Figure(
            data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale=[[0, "#ef4444"], [0.5, "#f3f4f6"], [1, "#10b981"]],
                text=corr_matrix.values.round(2),
                texttemplate="%{text}",
                textfont={"size": 10},
                colorbar=dict(title="Correlation"),
            )
        )
        fig.update_layout(
            height=550,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff", size=10),
            margin=dict(l=120, r=40, t=20, b=120),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Risk Distribution by Segment")
        fig = go.Figure()
        for segment in ["Low Risk", "Moderate Risk", "High Risk"]:
            data = plot_df[plot_df["risk_segment"] == segment]["risk_score"]
            color = {
                "Low Risk": "#10b981",
                "Moderate Risk": "#f59e0b",
                "High Risk": "#ef4444",
            }[segment]
            fig.add_trace(go.Box(y=data, name=segment, marker_color=color, boxmean="sd"))
        fig.update_layout(
            height=550,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            yaxis_title="Risk Score",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Confusion Matrix Analysis")
        cm = confusion_matrix(
            df_metrics["high_risk"].values,
            (df_metrics["risk_score"].values >= threshold).astype(int),
        )
        if cm.shape == (2, 2):
            tn, fp, fn, tp = cm.ravel()
        else:
            tn = fp = fn = tp = 0

        cm_display = [[tn, fp], [fn, tp]]
        fig = go.Figure(
            data=go.Heatmap(
                z=cm_display,
                x=["Predicted Negative", "Predicted Positive"],
                y=["Actual Negative", "Actual Positive"],
                text=cm_display,
                texttemplate="%{text}",
                textfont={"size": 24},
                colorscale=[[0, "#1e293b"], [1, "#3b82f6"]],
                showscale=False,
            )
        )
        fig.update_layout(
            height=450,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff", size=13),
            margin=dict(l=100, r=20, t=20, b=80),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### ROC Curve Analysis")
        fpr, tpr, _ = roc_curve(df_metrics["high_risk"].values, df_metrics["risk_score"].values)
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=fpr,
                y=tpr,
                mode="lines",
                name=f"ROC (AUC = {metrics['auc']:.3f})",
                line=dict(color="#3b82f6", width=4),
                fill="tozeroy",
                fillcolor="rgba(59,130,246,0.3)",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode="lines",
                name="Random Classifier",
                line=dict(color="#64748b", width=2, dash="dash"),
            )
        )
        fig.update_layout(
            height=450,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Risk Factor Importance (Conceptual)")

    features = [
        "Screen Time",
        "Stress",
        "Sleep Quality",
        "Anxiety",
        "Depression",
        "Wellbeing",
        "Social Support",
        "Loneliness",
        "Phone Unlocks",
        "Social Media",
        "Exercise",
        "Outdoor Time",
    ]
    importance = [0.62, 0.58, 0.46, 0.52, 0.48, 0.42, 0.18, 0.2, 0.22, 0.18, 0.15, 0.12]

    fig = px.bar(
        x=importance,
        y=features,
        orientation="h",
        color=importance,
        color_continuous_scale=["#64748b", "#3b82f6", "#8b5cf6", "#ec4899"],
    )
    fig.update_layout(
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        xaxis_title="Relative Importance (Model Coefficients)",
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    sample = (
        plot_df.sample(n=min(2000, len(plot_df)), random_state=42) if len(plot_df) > 0 else plot_df
    )

    with col1:
        st.markdown("#### Screen Time vs Sleep")
        if len(sample) > 0:
            fig = px.scatter(
                sample,
                x="screen_hours",
                y="sleep_hours",
                color="risk_score",
                size="stress",
                color_continuous_scale=["#10b981", "#f59e0b", "#ef4444"],
                hover_data=["stress", "wellbeing", "age"],
            )
            fig.update_layout(
                height=450,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Stress vs Wellbeing")
        if len(sample) > 0:
            fig = px.scatter(
                sample,
                x="stress",
                y="wellbeing",
                color="risk_segment",
                size="risk_score",
                color_discrete_map={
                    "Low Risk": "#10b981",
                    "Moderate Risk": "#f59e0b",
                    "High Risk": "#ef4444",
                },
                hover_data=["screen_hours", "sleep_hours", "depression"],
            )
            fig.update_layout(
                height=450,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
            st.plotly_chart(fig, use_container_width=True)


def render_behavioral_analytics(plot_df: pd.DataFrame, hourly_df: pd.DataFrame) -> None:
    st.markdown(
        """
    <div class='section-header'>
        <div class='section-icon'>📱</div>
        <div>
            <div class='section-title'>Digital Behavior Analysis</div>
            <div class='section-subtitle'>Usage patterns and lifestyle correlations</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Circadian Activity Patterns")
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=hourly_df["hour"],
            y=hourly_df["screen_time"],
            name="Screen Time",
            mode="lines+markers",
            line=dict(color="#3b82f6", width=3),
            fill="tozeroy",
            fillcolor="rgba(59,130,246,0.3)",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=hourly_df["hour"],
            y=hourly_df["notifications"],
            name="Notifications",
            mode="lines+markers",
            line=dict(color="#f59e0b", width=2),
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=hourly_df["hour"],
            y=hourly_df["stress"],
            name="Stress Level",
            mode="lines+markers",
            line=dict(color="#ef4444", width=2, dash="dash"),
        ),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(
            x=hourly_df["hour"],
            y=hourly_df["energy"],
            name="Energy Level",
            mode="lines",
            line=dict(color="#10b981", width=2, dash="dot"),
        ),
        secondary_y=True,
    )

    fig.update_layout(
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        hovermode="x unified",
    )

    fig.update_xaxes(title_text="Hour of Day", showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(
        title_text="Activity Level",
        secondary_y=False,
        showgrid=True,
        gridcolor="rgba(255,255,255,0.1)",
    )
    fig.update_yaxes(title_text="Psychological Metrics", secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### App Usage Distribution")
        usage_data = pd.DataFrame(
            {
                "Category": ["Social Media", "Work/Study", "Gaming", "Entertainment", "Other"],
                "Minutes": [
                    plot_df["social_minutes"].mean(),
                    plot_df["work_minutes"].mean(),
                    plot_df["gaming_minutes"].mean(),
                    80,
                    45,
                ],
            }
        )
        fig = px.pie(
            usage_data,
            values="Minutes",
            names="Category",
            color_discrete_sequence=[
                "#3b82f6",
                "#10b981",
                "#8b5cf6",
                "#ec4899",
                "#64748b",
            ],
            hole=0.5,
        )
        fig.update_layout(
            height=400,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Digital Interaction Metrics")
        interaction_data = (
            plot_df.groupby("risk_segment")
            .agg({"phone_unlocks": "mean", "notifications": "mean"})
            .reset_index()
        )

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=interaction_data["risk_segment"],
                y=interaction_data["phone_unlocks"],
                name="Phone Unlocks",
                marker_color="#3b82f6",
            )
        )
        fig.add_trace(
            go.Bar(
                x=interaction_data["risk_segment"],
                y=interaction_data["notifications"],
                name="Notifications",
                marker_color="#f59e0b",
            )
        )
        fig.update_layout(
            height=400,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            barmode="group",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("#### Physical Activity Balance")
        balance_data = pd.DataFrame(
            {
                "Activity": ["Exercise", "Outdoor", "Screen Time"],
                "Minutes": [
                    plot_df["exercise_minutes"].mean(),
                    plot_df["outdoor_time"].mean(),
                    plot_df["screen_hours"].mean() * 60,
                ],
            }
        )
        fig = px.bar(
            balance_data,
            x="Activity",
            y="Minutes",
            color="Activity",
            color_discrete_sequence=["#10b981", "#8b5cf6", "#ef4444"],
        )
        fig.update_layout(
            height=400,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Population Health Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        high_screen = len(plot_df[plot_df["screen_hours"] > 10])
        st.metric(
            "Excessive Screen Use",
            f"{high_screen:,}",
            f"{(high_screen / len(plot_df) * 100):.1f}% of users",
        )

    with col2:
        sleep_deficit = len(plot_df[plot_df["sleep_hours"] < 6])
        st.metric(
            "Sleep Deficit",
            f"{sleep_deficit:,}",
            f"{(sleep_deficit / len(plot_df) * 100):.1f}% critical",
        )

    with col3:
        high_stress = len(plot_df[plot_df["stress"] > 7])
        st.metric(
            "High Stress",
            f"{high_stress:,}",
            f"{(high_stress / len(plot_df) * 100):.1f}% elevated",
        )

    with col4:
        sedentary = len(plot_df[plot_df["exercise_minutes"] < 20])
        st.metric(
            "Sedentary Lifestyle",
            f"{sedentary:,}",
            f"{(sedentary / len(plot_df) * 100):.1f}% inactive",
        )


def render_model_performance(
    plot_df: pd.DataFrame,
    df_metrics: pd.DataFrame,
    metrics: dict[str, float],
    threshold: float,
    metrics_scope: str,
) -> None:
    st.markdown(
        """
    <div class='section-header'>
        <div class='section-icon'>🔬</div>
        <div>
            <div class='section-title'>ML Model Performance</div>
            <div class='section-subtitle'>Evaluation and diagnostics on the current cohort</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    metrics_data = [
        ("AUC-ROC", metrics["auc"], "🎯"),
        ("Precision", metrics["precision"], "🔍"),
        ("Recall", metrics["recall"], "📊"),
        ("F1 Score", metrics["f1"], "⚡"),
        ("Brier Score", metrics["brier"], "📈"),
    ]

    for i, (label, value, icon) in enumerate(metrics_data):
        with [col1, col2, col3, col4, col5][i]:
            st.markdown(
                f"""
            <div class='metric-card'>
                <div class='metric-icon'>{icon}</div>
                <div class='metric-value'>{value:.3f}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.caption(f"Analysis scope: {metrics_scope}")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Threshold Optimization Curve")
        thresholds = np.linspace(0.1, 0.9, 60)
        precision_scores = []
        recall_scores = []
        f1_scores = []

        for t in thresholds:
            temp_metrics = calculate_metrics(df_metrics, t)
            precision_scores.append(temp_metrics["precision"])
            recall_scores.append(temp_metrics["recall"])
            f1_scores.append(temp_metrics["f1"])

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=thresholds,
                y=precision_scores,
                mode="lines",
                name="Precision",
                line=dict(color="#10b981", width=3),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=thresholds,
                y=recall_scores,
                mode="lines",
                name="Recall",
                line=dict(color="#3b82f6", width=3),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=thresholds,
                y=f1_scores,
                mode="lines",
                name="F1 Score",
                line=dict(color="#8b5cf6", width=3),
            )
        )
        fig.add_vline(
            x=threshold,
            line_dash="dash",
            line_color="#f59e0b",
            line_width=3,
            annotation_text=f"Current: {threshold:.2f}",
        )
        fig.update_layout(
            height=450,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            xaxis_title="Decision Threshold",
            yaxis_title="Score",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Precision-Recall Curve")
        precision_vals, recall_vals, _ = precision_recall_curve(
            df_metrics["high_risk"].values, df_metrics["risk_score"].values
        )
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=recall_vals,
                y=precision_vals,
                mode="lines",
                name=f"PR Curve (AP = {metrics['ap']:.3f})",
                line=dict(color="#8b5cf6", width=4),
                fill="tozeroy",
                fillcolor="rgba(139,92,246,0.3)",
            )
        )
        fig.update_layout(
            height=450,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            xaxis_title="Recall",
            yaxis_title="Precision",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Model Calibration Analysis")

    df_cal = df_metrics.copy()
    df_cal["score_bin"] = pd.qcut(df_cal["risk_score"], q=10, duplicates="drop")
    cal_stats = (
        df_cal.groupby("score_bin")
        .agg({"risk_score": "mean", "high_risk": "mean", "user_id": "count"})
        .reset_index()
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=cal_stats["risk_score"],
            y=cal_stats["high_risk"],
            mode="markers+lines",
            name="Observed Rate",
            marker=dict(size=cal_stats["user_id"] / 25, color="#3b82f6"),
            line=dict(color="#3b82f6", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Perfect Calibration",
            line=dict(color="#10b981", width=2, dash="dash"),
        )
    )
    fig.update_layout(
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        xaxis_title="Predicted Risk Score",
        yaxis_title="Observed Event Rate",
    )
    st.plotly_chart(fig, use_container_width=True)


def render_intervention_simulator(
    plot_df: pd.DataFrame, real_time_mode: bool, threshold: float
) -> None:
    st.markdown(
        """
    <div class='section-header'>
        <div class='section-icon'>🧪</div>
        <div>
            <div class='section-title'>Interactive Risk Simulator</div>
            <div class='section-subtitle'>Test behavioral interventions and quantify risk impact</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    df = plot_df

    if real_time_mode:
        st.markdown(
            """
        <div style='background: rgba(34,197,94,0.1); padding: 14px 18px; border-radius: 10px;
                    border-left: 4px solid #22c55e; margin-bottom: 14px;'>
            <span style='color:#bbf7d0; font-size:0.9rem;'>
                Real-time mode enabled — use this simulator as a live what-if console for new profiles.
            </span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
    <div style='background: rgba(59,130,246,0.12); padding: 20px; border-radius: 12px;
                border-left: 4px solid #3b82f6; margin: 16px 0;'>
        <strong>How this works:</strong><br>
        1) Configure a single user profile using the sliders below.<br>
        2) The risk engine predicts mental health risk in real-time based on the inputs.<br>
        3) Intervention scenarios show how small changes shift the risk curve.
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("##### 📱 Digital Behavior")
        sim_screen = st.slider("Screen Time (hours/day)", 1.0, 18.0, 7.0, 0.5, key="sim_screen")
        sim_unlocks = st.slider("Phone Unlocks/day", 10, 400, 110, 5, key="sim_unlocks")
        _sim_notifications = st.slider("Notifications/day", 5, 350, 95, 5, key="sim_notif")
        sim_social = st.slider("Social Media (min/day)", 5, 480, 165, 10, key="sim_social")
        _sim_gaming = st.slider("Gaming (min/day)", 0, 360, 70, 10, key="sim_gaming")

    with col2:
        st.markdown("##### 😴 Health & Wellbeing")
        sim_sleep = st.slider("Sleep (hours/day)", 3.0, 12.0, 7.5, 0.5, key="sim_sleep")
        sim_stress = st.slider("Stress Level (1-10)", 1.0, 10.0, 5.5, 0.5, key="sim_stress")
        sim_anxiety = st.slider("Anxiety Level (1-10)", 1.0, 10.0, 5.0, 0.5, key="sim_anxiety")
        sim_depression = st.slider("Depression (1-10)", 1.0, 10.0, 4.5, 0.5, key="sim_depression")
        sim_wellbeing = st.slider("Wellbeing (1-10)", 1.0, 10.0, 8.0, 0.5, key="sim_wellbeing")
        sim_mood = st.slider("Mood (1-10)", 1.0, 10.0, 7.5, 0.5, key="sim_mood")
        sim_energy = st.slider("Energy (1-10)", 1.0, 10.0, 7.8, 0.5, key="sim_energy")

    with col3:
        st.markdown("##### 🏃 Physical & Social")
        sim_exercise = st.slider("Exercise (min/day)", 0, 200, 40, 5, key="sim_exercise")
        sim_outdoor = st.slider("Outdoor Time (min/day)", 0, 280, 55, 10, key="sim_outdoor")
        sim_social_support = st.slider(
            "Social Support (1-10)", 1.0, 10.0, 7.0, 0.5, key="sim_social_support"
        )
        sim_loneliness = st.slider("Loneliness (1-10)", 1.0, 10.0, 4.5, 0.5, key="sim_loneliness")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset to Population Baseline", use_container_width=True):
            st.rerun()

    base_features = {
        "screen": sim_screen,
        "sleep": sim_sleep,
        "stress": sim_stress,
        "anxiety": sim_anxiety,
        "depression": sim_depression,
        "wellbeing": sim_wellbeing,
        "mood": sim_mood,
        "energy": sim_energy,
        "unlocks": sim_unlocks,
        "social": sim_social,
        "exercise": sim_exercise,
        "outdoor": sim_outdoor,
        "loneliness": sim_loneliness,
        "social_support": sim_social_support,
    }

    scenario_risk = compute_risk_from_features(base_features)
    scenario_segment = (
        "Low Risk"
        if scenario_risk < 0.30
        else "Moderate Risk"
        if scenario_risk < 0.60
        else "High Risk"
    )
    scenario_flagged = "Yes" if scenario_risk >= threshold else "No"
    percentile = 0.0
    if not df.empty and "risk_score" in df.columns:
        percentile = float((df["risk_score"] < scenario_risk).mean() * 100.0)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🎯 Simulation Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        color_risk = (
            "#ef4444" if scenario_risk > 0.6 else "#f59e0b" if scenario_risk > 0.3 else "#10b981"
        )
        st.markdown(
            f"""
        <div class='metric-card'>
            <div class='metric-label'>PREDICTED RISK SCORE</div>
            <div class='metric-value' style='color: {color_risk};'>
                {scenario_risk:.3f}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        segment_color = {
            "Low Risk": "#10b981",
            "Moderate Risk": "#f59e0b",
            "High Risk": "#ef4444",
        }[scenario_segment]
        st.markdown(
            f"""
        <div class='metric-card'>
            <div class='metric-label'>RISK CATEGORY</div>
            <div class='metric-value' style='color: {segment_color}; font-size: 2rem;'>
                {scenario_segment}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        flag_color = "#ef4444" if scenario_flagged == "Yes" else "#10b981"
        st.markdown(
            f"""
        <div class='metric-card'>
            <div class='metric-label'>INTERVENTION FLAG</div>
            <div class='metric-value' style='color: {flag_color}; font-size: 2.5rem;'>
                {scenario_flagged}
            </div>
            <div class='metric-change'>At threshold {threshold:.2f}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
        <div class='metric-card'>
            <div class='metric-label'>POPULATION PERCENTILE</div>
            <div class='metric-value'>{percentile:.0f}th</div>
            <div class='metric-change'>Risk ranking vs full population</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 📊 Scenario vs Population Averages")

        comparison_data = pd.DataFrame(
            {
                "Metric": [
                    "Screen Time",
                    "Sleep",
                    "Stress",
                    "Anxiety",
                    "Wellbeing",
                    "Exercise (×10min)",
                    "Social Support",
                ],
                "Your Scenario": [
                    sim_screen,
                    sim_sleep,
                    sim_stress,
                    sim_anxiety,
                    sim_wellbeing,
                    sim_exercise / 10.0,
                    sim_social_support,
                ],
                "Population Avg": [
                    df["screen_hours"].mean(),
                    df["sleep_hours"].mean(),
                    df["stress"].mean(),
                    df["anxiety"].mean(),
                    df["wellbeing"].mean(),
                    df["exercise_minutes"].mean() / 10.0,
                    df["social_support"].mean(),
                ]
                if len(df) > 0
                else [0, 0, 0, 0, 0, 0, 0],
            }
        )

        fig_comp = go.Figure()
        fig_comp.add_trace(
            go.Bar(
                x=comparison_data["Metric"],
                y=comparison_data["Your Scenario"],
                name="Your Scenario",
                marker_color="#3b82f6",
            )
        )
        fig_comp.add_trace(
            go.Bar(
                x=comparison_data["Metric"],
                y=comparison_data["Population Avg"],
                name="Population Average",
                marker_color="#64748b",
            )
        )
        fig_comp.update_layout(
            height=430,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            barmode="group",
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    with col_right:
        st.markdown("#### 🧬 Profile Radar View")

        radar_categories = [
            "Screen Load",
            "Sleep",
            "Stress",
            "Anxiety",
            "Wellbeing",
            "Exercise",
            "Social Support",
        ]

        radar_values = [
            min(sim_screen / 1.8, 10.0),
            min(sim_sleep * 1.2, 10.0),
            sim_stress,
            sim_anxiety,
            sim_wellbeing,
            min(sim_exercise / 12.0, 10.0),
            sim_social_support,
        ]

        radar_categories += radar_categories[:1]
        radar_values += radar_values[:1]

        fig_radar = go.Figure()
        fig_radar.add_trace(
            go.Scatterpolar(
                r=radar_values,
                theta=radar_categories,
                fill="toself",
                name="Scenario profile",
                line=dict(color="#3b82f6", width=3),
                fillcolor="rgba(59,130,246,0.35)",
            )
        )
        fig_radar.update_layout(
            height=430,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    gridcolor="rgba(148,163,184,0.4)",
                ),
                angularaxis=dict(gridcolor="rgba(148,163,184,0.4)"),
            ),
            showlegend=False,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🧭 Quick Intervention What-If Scenarios")

    digital_reset = base_features.copy()
    digital_reset["screen"] = max(1.0, digital_reset["screen"] - 2.0)
    digital_reset["social"] = max(5.0, digital_reset["social"] - 60.0)
    digital_reset["unlocks"] = max(10.0, digital_reset["unlocks"] - 40.0)
    digital_reset["exercise"] = min(200.0, digital_reset["exercise"] + 20.0)
    risk_digital = compute_risk_from_features(digital_reset)

    sleep_reset = base_features.copy()
    sleep_reset["sleep"] = min(12.0, sleep_reset["sleep"] + 1.5)
    sleep_reset["stress"] = max(1.0, sleep_reset["stress"] - 1.0)
    sleep_reset["anxiety"] = max(1.0, sleep_reset["anxiety"] - 0.5)
    risk_sleep = compute_risk_from_features(sleep_reset)

    holistic = base_features.copy()
    holistic["screen"] = max(1.0, holistic["screen"] - 1.5)
    holistic["sleep"] = min(12.0, holistic["sleep"] + 1.0)
    holistic["exercise"] = min(200.0, holistic["exercise"] + 25.0)
    holistic["outdoor"] = min(280.0, holistic["outdoor"] + 30.0)
    holistic["loneliness"] = max(1.0, holistic["loneliness"] - 1.0)
    holistic["social_support"] = min(10.0, holistic["social_support"] + 1.0)
    risk_holistic = compute_risk_from_features(holistic)

    col1, col2, col3 = st.columns(3)

    def render_intervention_card(title: str, risk_new: float):
        delta = risk_new - scenario_risk
        color = "#10b981" if delta < 0 else "#f59e0b" if abs(delta) < 0.01 else "#ef4444"
        sign = "+" if delta >= 0 else "−"
        st.markdown(
            f"""
        <div class='metric-card'>
            <div class='metric-label'>{title}</div>
            <div class='metric-value' style='font-size: 2.1rem; color: {color};'>
                {risk_new:.3f}
            </div>
            <div class='metric-change'>
                Δ risk: {sign}{abs(delta):.3f}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col1:
        render_intervention_card("Digital Reset (−2h screen, −60min social)", risk_digital)
    with col2:
        render_intervention_card("Sleep Protocol (+1.5h sleep, ↓ stress)", risk_sleep)
    with col3:
        render_intervention_card("Holistic Plan (screen, sleep, exercise, social)", risk_holistic)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📈 Sensitivity: Risk vs Screen Time (other factors fixed)")

    screen_min = max(1.0, sim_screen - 3.0)
    screen_max = min(18.0, sim_screen + 3.0)
    screen_grid = np.linspace(screen_min, screen_max, 40)
    risk_grid = []

    for s_val in screen_grid:
        tmp = base_features.copy()
        tmp["screen"] = float(s_val)
        risk_grid.append(compute_risk_from_features(tmp))

    fig_sens = go.Figure()
    fig_sens.add_trace(
        go.Scatter(
            x=screen_grid,
            y=risk_grid,
            mode="lines",
            name="Risk vs Screen Time",
            line=dict(color="#3b82f6", width=4),
            fill="tozeroy",
            fillcolor="rgba(59,130,246,0.25)",
        )
    )
    fig_sens.add_vline(
        x=sim_screen,
        line_dash="dash",
        line_color="#f59e0b",
        line_width=3,
        annotation_text=f"Current: {sim_screen:.1f}h",
        annotation_position="top right",
    )
    fig_sens.update_layout(
        height=430,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        xaxis_title="Screen Time (hours/day)",
        yaxis_title="Predicted Risk",
    )
    fig_sens.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.14)")
    fig_sens.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.14)")
    st.plotly_chart(fig_sens, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 💡 AI-Generated Recommendations")

    recommendations = []

    if sim_screen > 10:
        recommendations.append(
            (
                "danger",
                "🔴 Screen time is well above healthy limits. Introduce strict boundaries, offline blocks, and app usage limits.",
            )
        )
    elif sim_screen > 8:
        recommendations.append(
            (
                "warning",
                "🟡 High digital exposure detected. Add app time caps and at least one daily offline block of 60–90 minutes.",
            )
        )

    if sim_sleep < 6:
        recommendations.append(
            (
                "danger",
                "🔴 Severe sleep deficit. Establish a consistent sleep schedule, limit screens before bedtime, and consider medical follow-up if problems persist.",
            )
        )
    elif sim_sleep < 7:
        recommendations.append(
            (
                "warning",
                "🟡 Sleep is below the recommended range. Aim for 30–60 additional minutes for the next two weeks and track consistency.",
            )
        )

    if sim_stress > 7 or sim_anxiety > 7:
        recommendations.append(
            (
                "danger",
                "🔴 Elevated psychological stress and anxiety. Structured support (for example, counseling or therapy) may be beneficial.",
            )
        )

    if sim_exercise < 20:
        recommendations.append(
            (
                "warning",
                "🟡 Physical activity is low. Target at least 30 minutes of light-to-moderate movement on most days.",
            )
        )

    if sim_loneliness > 6:
        recommendations.append(
            (
                "warning",
                "🟡 Social isolation signals detected. Strengthening connections through community activities or regular check-ins may help.",
            )
        )

    if sim_wellbeing > 7.5 and sim_stress < 5.5 and sim_exercise > 30 and sim_sleep >= 7:
        recommendations.append(
            (
                "success",
                "🟢 Overall balance looks healthy. Continue tracking digital habits and maintaining the current protective lifestyle factors.",
            )
        )

    if not recommendations:
        recommendations.append(
            (
                "success",
                "🟢 Metrics are balanced. Maintain current routines and review again after any major lifestyle changes.",
            )
        )

    for rec_type, rec_text in recommendations:
        bg_color = {
            "danger": "rgba(239,68,68,0.15)",
            "warning": "rgba(245,158,11,0.15)",
            "success": "rgba(16,185,129,0.15)",
        }[rec_type]
        border_color = {
            "danger": "#ef4444",
            "warning": "#f59e0b",
            "success": "#10b981",
        }[rec_type]
        st.markdown(
            f"""
        <div style='background: {bg_color}; padding: 15px; border-radius: 10px;
                    border-left: 4px solid {border_color}; margin: 8px 0;'>
            <p style='color: white; margin: 0; font-size: 1rem;'>{rec_text}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_clinical_reports(plot_df: pd.DataFrame) -> None:
    st.markdown(
        """
    <div class='section-header'>
        <div class='section-icon'>🏥</div>
        <div>
            <div class='section-title'>Clinical Intelligence Reports</div>
            <div class='section-subtitle'>High-risk users and summary indicators</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 🚨 Critical Risk Users - Priority List")

    if len(plot_df) > 0:
        top_risk = plot_df.nlargest(
            30,
            "risk_score",
        )[
            [
                "user_id",
                "age",
                "gender",
                "occupation",
                "risk_score",
                "risk_segment",
                "screen_hours",
                "sleep_hours",
                "stress",
                "anxiety",
                "depression",
                "wellbeing",
                "social_support",
                "loneliness",
                "last_active",
            ]
        ].copy()

        top_risk["risk_score"] = top_risk["risk_score"].round(3)
        top_risk["screen_hours"] = top_risk["screen_hours"].round(1)
        top_risk["sleep_hours"] = top_risk["sleep_hours"].round(1)
        top_risk["days_inactive"] = (pd.Timestamp.now() - top_risk["last_active"]).dt.days

        st.dataframe(
            top_risk.drop(columns=["last_active"]),
            use_container_width=True,
            height=500,
        )

        if st.button("📄 Export High-Risk Report (CSV)", use_container_width=False):
            csv_data = top_risk.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Report",
                data=csv_data,
                file_name=f"high_risk_users_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
            )
    else:
        st.info("No users in current filtered view.")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Risk Distribution Summary")
        if len(plot_df) > 0:
            risk_summary = (
                plot_df["risk_segment"].value_counts().rename_axis("risk_segment").to_frame("count")
            )
            risk_summary["percentage"] = (risk_summary["count"] / len(plot_df) * 100).round(1)
            st.dataframe(risk_summary, use_container_width=True)
        else:
            st.write("No data available for summary.")

    with col2:
        st.markdown("#### Mental Health Averages")
        if len(plot_df) > 0:
            mental_health_avg = (
                plot_df[
                    [
                        "stress",
                        "anxiety",
                        "depression",
                        "wellbeing",
                        "mood",
                        "energy",
                    ]
                ]
                .mean()
                .round(2)
                .to_frame(name="Average Score")
            )
            st.dataframe(mental_health_avg, use_container_width=True)
        else:
            st.write("No data available for summary.")

    with col3:
        st.markdown("#### Behavioral Metrics")
        if len(plot_df) > 0:
            behavior_avg = (
                plot_df[
                    [
                        "screen_hours",
                        "phone_unlocks",
                        "notifications",
                        "social_minutes",
                        "gaming_minutes",
                        "exercise_minutes",
                        "outdoor_time",
                        "steps_daily",
                    ]
                ]
                .mean()
                .round(2)
                .to_frame(name="Average Value")
            )
            st.dataframe(behavior_avg, use_container_width=True)
        else:
            st.write("No data available for summary.")
