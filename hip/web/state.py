from __future__ import annotations

from dataclasses import dataclass

from hip.core.filtering import FilterState


@dataclass(frozen=True)
class DisplayState:
    show_animations: bool
    show_insights: bool
    real_time_mode: bool


@dataclass(frozen=True)
class AppState:
    filters: FilterState
    display: DisplayState
