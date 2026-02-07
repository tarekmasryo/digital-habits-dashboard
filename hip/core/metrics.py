from __future__ import annotations

import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    roc_auc_score,
)


def calculate_metrics(df_metrics: pd.DataFrame, threshold: float = 0.5) -> dict[str, float]:
    y_true = df_metrics["high_risk"].values
    y_score = df_metrics["risk_score"].values
    y_pred = (y_score >= threshold).astype(int)

    auc = roc_auc_score(y_true, y_score)
    ap = average_precision_score(y_true, y_score)
    brier = brier_score_loss(y_true, y_score)
    cm = confusion_matrix(y_true, y_pred)

    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
    else:
        tn = fp = fn = tp = 0

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

    return {
        "auc": auc,
        "ap": ap,
        "brier": brier,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "specificity": specificity,
        "tp": int(tp),
        "fp": int(fp),
        "tn": int(tn),
        "fn": int(fn),
    }
