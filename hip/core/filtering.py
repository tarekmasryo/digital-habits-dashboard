from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class FilterState:
    threshold: float
    selected_segments: list[str]
    selected_age_groups: list[str]
    selected_gender: list[str]
    selected_occupation: list[str]
    screen_time_range: tuple[float, float]
    stress_range: tuple[float, float]


def apply_filters(df: pd.DataFrame, state: FilterState) -> tuple[pd.DataFrame, bool]:
    mask = (
        df["risk_segment"].isin(state.selected_segments)
        & df["age_group"].isin(state.selected_age_groups)
        & df["gender"].isin(state.selected_gender)
        & df["occupation"].isin(state.selected_occupation)
        & (df["screen_hours"] >= state.screen_time_range[0])
        & (df["screen_hours"] <= state.screen_time_range[1])
        & (df["stress"] >= state.stress_range[0])
        & (df["stress"] <= state.stress_range[1])
    )
    df_filtered = df[mask].copy()
    no_filter_data = len(df_filtered) == 0
    return df_filtered, no_filter_data
