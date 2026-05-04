from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class GeneratedData:
    population: pd.DataFrame
    time_series: pd.DataFrame
    hourly: pd.DataFrame


def generate_advanced_data(
    n_users: int = 5000, seed: int = 42, now: pd.Timestamp | None = None
) -> GeneratedData:
    rng = np.random.default_rng(seed)
    ts_now = pd.Timestamp.now() if now is None else now

    user_id = np.arange(1, n_users + 1)
    age = rng.integers(15, 75, size=n_users)
    age_group = pd.cut(
        age,
        bins=[14, 22, 30, 40, 50, 60, 75],
        labels=["Gen Z", "Millennials", "Young Adults", "Middle Age", "Senior", "Elderly"],
    )
    gender = rng.choice(["Male", "Female", "Other"], size=n_users, p=[0.48, 0.48, 0.04])
    location = rng.choice(["Urban", "Suburban", "Rural"], size=n_users, p=[0.55, 0.35, 0.10])
    occupation = rng.choice(
        ["Student", "Professional", "Healthcare", "Tech", "Retired", "Other"],
        size=n_users,
        p=[0.20, 0.30, 0.15, 0.20, 0.10, 0.05],
    )

    screen_hours = np.clip(rng.normal(7.2, 2.5, size=n_users), 1.0, 18.0)
    sleep_hours = np.clip(
        7.8 - 0.35 * (screen_hours - 7) + rng.normal(0, 0.9, size=n_users),
        3.0,
        12.0,
    )

    stress = np.clip(
        5.5 + 0.65 * (screen_hours - 7) + rng.normal(0, 1.3, size=n_users),
        1,
        10,
    )
    anxiety = np.clip(
        5.0 + 0.55 * stress + rng.normal(0, 1.1, size=n_users),
        1,
        10,
    )
    depression = np.clip(
        4.5 + 0.45 * stress + 0.3 * anxiety + rng.normal(0, 1.2, size=n_users),
        1,
        10,
    )
    focus = np.clip(
        8.0 - 0.45 * (screen_hours - 7) - 0.35 * stress + rng.normal(0, 0.9, size=n_users),
        1,
        10,
    )
    wellbeing = np.clip(
        8.2 - 0.45 * stress + 0.45 * (sleep_hours - 7.5) + rng.normal(0, 0.8, size=n_users),
        1,
        10,
    )
    mood = np.clip(
        7.5 - 0.35 * stress + 0.25 * wellbeing + rng.normal(0, 1.0, size=n_users),
        1,
        10,
    )
    energy = np.clip(
        7.8 - 0.3 * stress + 0.4 * (sleep_hours - 7.5) + rng.normal(0, 0.9, size=n_users),
        1,
        10,
    )

    phone_unlocks = np.clip(
        rng.normal(110 + 15 * (screen_hours - 7), 35, size=n_users),
        10,
        400,
    ).astype(int)
    notifications = np.clip(
        rng.normal(95 + 12 * (screen_hours - 7), 32, size=n_users),
        5,
        350,
    ).astype(int)
    social_minutes = np.clip(
        rng.normal(165 + 18 * (screen_hours - 7), 55, size=n_users),
        5,
        480,
    ).astype(int)
    gaming_minutes = np.clip(
        rng.normal(70 + 10 * (screen_hours - 7), 40, size=n_users),
        0,
        360,
    ).astype(int)
    work_minutes = np.clip(
        rng.normal(220, 80, size=n_users),
        0,
        600,
    ).astype(int)

    exercise_minutes = np.clip(
        rng.normal(40 - 2.5 * (screen_hours - 7), 28, size=n_users),
        0,
        200,
    ).astype(int)
    outdoor_time = np.clip(
        rng.normal(55 - 3.5 * (screen_hours - 7), 35, size=n_users),
        0,
        280,
    ).astype(int)

    bmi = np.clip(rng.normal(24.5 + 0.3 * (screen_hours - 7), 4.5, size=n_users), 16, 45)
    heart_rate = np.clip(
        rng.normal(72 + 2 * stress, 10, size=n_users),
        50,
        120,
    ).astype(int)
    steps_daily = np.clip(
        rng.normal(7500 - 300 * (screen_hours - 7), 2500, size=n_users),
        1000,
        20000,
    ).astype(int)

    social_support = np.clip(
        rng.normal(7.0 - 0.2 * stress, 1.5, size=n_users),
        1,
        10,
    )
    loneliness = np.clip(
        rng.normal(4.5 + 0.4 * stress - 0.5 * social_support, 1.8, size=n_users),
        1,
        10,
    )

    raw_signal = (
        0.62 * (screen_hours - 7)
        + 0.58 * (stress - 5.5)
        + 0.52 * (anxiety - 5)
        + 0.48 * (depression - 4.5)
        - 0.46 * (sleep_hours - 7.5)
        - 0.42 * (wellbeing - 8)
        - 0.38 * (mood - 7.5)
        - 0.35 * (energy - 7.8)
        + 0.22 * ((phone_unlocks - 110) / 60)
        + 0.18 * ((social_minutes - 165) / 70)
        - 0.15 * ((exercise_minutes - 40) / 35)
        - 0.12 * ((outdoor_time - 55) / 55)
        + 0.20 * (loneliness - 4.5)
        - 0.18 * (social_support - 7)
    )

    logit = -2.0 + 0.30 * raw_signal + rng.normal(0, 0.60, size=n_users)
    risk_score = 1.0 / (1.0 + np.exp(-logit))
    risk_score = np.clip(risk_score, 0.01, 0.99)
    high_risk = (rng.random(n_users) < risk_score).astype(int)

    risk_segment = pd.cut(
        risk_score,
        bins=[0.0, 0.40, 0.75, 1.0],
        labels=["Low Risk", "Moderate Risk", "High Risk"],
    )

    last_active = ts_now - pd.to_timedelta(rng.integers(0, 45, size=n_users), unit="D")
    engagement_score = np.clip(
        rng.normal(7.8 - 0.25 * (screen_hours - 7), 1.6, size=n_users),
        1,
        10,
    )

    seeking_help = rng.choice([0, 1], size=n_users, p=[0.7, 0.3])
    medication = rng.choice([0, 1], size=n_users, p=[0.8, 0.2])

    df = pd.DataFrame(
        {
            "user_id": user_id,
            "age": age,
            "age_group": age_group,
            "gender": gender,
            "location": location,
            "occupation": occupation,
            "screen_hours": screen_hours.round(2),
            "sleep_hours": sleep_hours.round(2),
            "stress": stress.round(1),
            "anxiety": anxiety.round(1),
            "depression": depression.round(1),
            "focus": focus.round(1),
            "wellbeing": wellbeing.round(1),
            "mood": mood.round(1),
            "energy": energy.round(1),
            "phone_unlocks": phone_unlocks,
            "notifications": notifications,
            "social_minutes": social_minutes,
            "gaming_minutes": gaming_minutes,
            "work_minutes": work_minutes,
            "exercise_minutes": exercise_minutes,
            "outdoor_time": outdoor_time,
            "bmi": bmi.round(1),
            "heart_rate": heart_rate,
            "steps_daily": steps_daily,
            "social_support": social_support.round(1),
            "loneliness": loneliness.round(1),
            "seeking_help": seeking_help,
            "medication": medication,
            "risk_score": risk_score,
            "high_risk": high_risk,
            "risk_segment": risk_segment,
            "last_active": last_active,
            "engagement_score": engagement_score.round(1),
        }
    )

    dates = pd.date_range(end=ts_now, periods=90, freq="D")
    time_series = pd.DataFrame(
        {
            "date": dates,
            "avg_screen": 7.0 + np.sin(np.arange(90) / 7) * 1.8 + rng.normal(0, 0.4, 90),
            "avg_stress": 5.8 + np.sin(np.arange(90) / 10) * 1.4 + rng.normal(0, 0.4, 90),
            "avg_wellbeing": 7.8 - np.sin(np.arange(90) / 10) * 1.2 + rng.normal(0, 0.4, 90),
            "high_risk_count": (
                800 + np.sin(np.arange(90) / 7) * 120 + rng.normal(0, 40, 90)
            ).astype(int),
            "avg_sleep": 7.5 - np.sin(np.arange(90) / 12) * 0.8 + rng.normal(0, 0.3, 90),
            "engagement": 7.5 + np.sin(np.arange(90) / 8) * 1.0 + rng.normal(0, 0.3, 90),
        }
    )

    hours = list(range(24))
    hourly = pd.DataFrame(
        {
            "hour": hours,
            "screen_time": [25 if h < 6 else 55 + 20 * np.sin((h - 6) / 3.5) for h in hours],
            "notifications": [12 if h < 6 else 35 + 18 * np.sin((h - 6) / 3.8) for h in hours],
            "stress": [3.5 if h < 6 else 5.5 + 2.5 * np.sin((h - 10) / 3.2) for h in hours],
            "energy": [4 if h < 6 else 7.5 - 1.5 * np.sin((h - 14) / 4) for h in hours],
        }
    )

    return GeneratedData(population=df, time_series=time_series, hourly=hourly)
