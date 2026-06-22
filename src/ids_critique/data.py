"""Data-loading and cleaning primitives for CICIDS2017.

These mirror the notebook's Section 1 logic. They are deliberately small and pure so they can
be unit-tested without the (gitignored, multi-GB) dataset.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ids_critique.config import WEEKDAY_ORDER

# Tag columns the notebook adds; never part of the feature/duplicate basis.
TAG_COLUMNS = ("day", "day_name")


def weekday_from_filename(filename: str) -> int | None:
    """Return the ordinal weekday (Mon=0..Fri=4) for a CICIDS2017 day-file.

    The published dataset ships 8 CSVs (Thursday and Friday are split across captures) with
    inconsistent casing (e.g. ``Wednesday-workingHours``). We match case-insensitively on the
    weekday prefix so all 8 files map onto the 5 weekdays. Returns ``None`` if no weekday
    prefix is found.
    """
    stem = filename.rsplit("/", 1)[-1].lower()
    for name, code in WEEKDAY_ORDER.items():
        if stem.startswith(name):
            return code
    return None


def strip_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from column names (a known CICIDS2017 quirk)."""
    out = df.copy()
    out.columns = out.columns.str.strip()
    return out


def replace_inf_with_nan(df: pd.DataFrame) -> pd.DataFrame:
    """Replace +/-Inf with NaN (CICFlowMeter emits Inf in rate columns). Non-mutating."""
    return df.replace([np.inf, -np.inf], np.nan)


def count_inf(df: pd.DataFrame) -> int:
    """Total number of +/-Inf cells across numeric columns."""
    numeric = df.select_dtypes(include=np.number)
    return int(np.isinf(numeric.to_numpy()).sum())


def duplicate_subset(df: pd.DataFrame) -> list[str]:
    """Columns that define an exact-duplicate flow: everything except the added tag columns."""
    return [c for c in df.columns if c not in TAG_COLUMNS]


def count_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> int:
    """Count exact-duplicate rows over ``subset`` (default: all non-tag columns)."""
    subset = subset if subset is not None else duplicate_subset(df)
    return int(df.duplicated(subset=subset).sum())
