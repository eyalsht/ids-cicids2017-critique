"""The IDS metric suite (notebook Section 5).

Recall-aware metrics matter here because the data is ~80/20 imbalanced and a missed attack
(false negative) costs more than a false alarm (false positive).
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    fbeta_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)


def macro_f1(y_true, y_pred) -> float:
    """Macro-averaged F1 -- the source paper's headline metric."""
    return float(f1_score(y_true, y_pred, average="macro", zero_division=0))


def binary_metrics(y_true, y_pred, y_score=None) -> dict[str, float]:
    """Full binary IDS metric suite as a dict.

    Includes accuracy (reported but flagged as misleading under imbalance), precision, recall,
    F1, F-beta(2) (recall-weighted), MCC (robust to imbalance), and ROC-AUC when scores given.
    """
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "fbeta2": float(fbeta_score(y_true, y_pred, beta=2, zero_division=0)),
        "mcc": float(matthews_corrcoef(y_true, y_pred)),
    }
    metrics["roc_auc"] = float(roc_auc_score(y_true, y_score)) if y_score is not None else float("nan")
    return metrics


def always_benign_accuracy(y_true) -> float:
    """Accuracy of a trivial 'predict BENIGN (0) for everything' baseline.

    Demonstrates why accuracy is misleading: this detector catches nothing yet scores high.
    """
    y = np.asarray(y_true)
    return float((y == 0).mean())
