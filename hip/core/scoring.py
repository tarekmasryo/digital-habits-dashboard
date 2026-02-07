from __future__ import annotations

import numpy as np


def compute_risk_from_features(params: dict) -> float:
    logit_val = (
        0.62 * (params["screen"] - 7)
        + 0.58 * (params["stress"] - 5.5)
        + 0.52 * (params["anxiety"] - 5)
        + 0.48 * (params["depression"] - 4.5)
        - 0.46 * (params["sleep"] - 7.5)
        - 0.42 * (params["wellbeing"] - 8)
        - 0.38 * (params["mood"] - 7.5)
        - 0.35 * (params["energy"] - 7.8)
        + 0.22 * ((params["unlocks"] - 110) / 60.0)
        + 0.18 * ((params["social"] - 165) / 70.0)
        - 0.15 * ((params["exercise"] - 40) / 35.0)
        - 0.12 * ((params["outdoor"] - 55) / 55.0)
        + 0.2 * (params["loneliness"] - 4.5)
        - 0.18 * (params["social_support"] - 7)
    )
    return float(np.clip(1.0 / (1.0 + np.exp(-logit_val)), 0.01, 0.99))
