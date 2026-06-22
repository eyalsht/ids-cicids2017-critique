"""Feature-engineering helpers (notebook Section 3): skew, log1p, correlation pruning.

All transforms are stateless, so applying them per train/test split cannot leak information.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def high_skew_features(df: pd.DataFrame, threshold: float = 3.0) -> list[str]:
    """Numeric columns whose absolute skewness exceeds ``threshold`` (candidates for log1p)."""
    numeric = df.select_dtypes(include=np.number)
    skew = numeric.skew(numeric_only=True).abs()
    return skew[skew > threshold].index.tolist()


def apply_log1p(frame: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Apply ``log1p`` to ``cols`` in place on a copy, skipping any column with negatives.

    ``log1p`` compresses right-skewed flow features; it is undefined for values < -1, so we
    guard by skipping columns that contain negative values. Stateless => no leakage.
    """
    out = frame.copy()
    for col in cols:
        if col in out.columns and (out[col] < 0).sum() == 0:
            out[col] = np.log1p(out[col])
    return out


def correlated_pairs(corr: pd.DataFrame, threshold: float = 0.95) -> list[tuple[str, str]]:
    """Return feature pairs whose absolute correlation exceeds ``threshold`` (upper triangle)."""
    pairs: list[tuple[str, str]] = []
    cols = corr.columns
    mask = np.triu(np.ones(corr.shape, dtype=bool), k=1)
    for i, j in zip(*np.where(mask), strict=True):
        if abs(corr.iat[i, j]) > threshold:
            pairs.append((cols[i], cols[j]))
    return pairs


def features_to_drop(corr: pd.DataFrame, threshold: float = 0.95) -> list[str]:
    """Greedy redundancy pruning: from each over-correlated pair, drop the later column.

    Deterministic and order-stable: for every pair (a, b) with |corr| > threshold we mark ``b``
    for removal, so a single representative of each correlated cluster survives.
    """
    drop: set[str] = set()
    for a, b in correlated_pairs(corr, threshold):
        if a not in drop:
            drop.add(b)
    return [c for c in corr.columns if c in drop]
