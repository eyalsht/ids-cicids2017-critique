"""Unit tests for ids_critique.features (no dataset required)."""

import numpy as np
import pandas as pd

from ids_critique.features import (
    apply_log1p,
    correlated_pairs,
    features_to_drop,
    high_skew_features,
)


def test_high_skew_features_flags_skewed_column():
    rng = np.random.default_rng(0)
    df = pd.DataFrame(
        {
            "skewed": np.concatenate([np.zeros(990), np.full(10, 1e6)]),  # heavy right tail
            "normal": rng.normal(size=1000),
        }
    )
    flagged = high_skew_features(df, threshold=3.0)
    assert "skewed" in flagged
    assert "normal" not in flagged


def test_apply_log1p_transforms_and_guards_negatives():
    df = pd.DataFrame({"pos": [0.0, 9.0], "neg": [-1.0, 5.0]})
    out = apply_log1p(df, ["pos", "neg"])
    # positive column transformed: log1p(9) = ln(10)
    assert np.isclose(out["pos"].iloc[1], np.log(10.0))
    assert np.isclose(out["pos"].iloc[0], 0.0)
    # negative-containing column skipped (unchanged)
    assert out["neg"].tolist() == [-1.0, 5.0]
    # original untouched
    assert df["pos"].tolist() == [0.0, 9.0]


def test_correlated_pairs_and_features_to_drop():
    base = np.arange(100.0)
    df = pd.DataFrame(
        {
            "a": base,
            "b": base * 2 + 1,  # perfectly correlated with a
            "c": np.cos(base),  # uncorrelated
        }
    )
    corr = df.corr(method="spearman")
    pairs = correlated_pairs(corr, threshold=0.95)
    assert ("a", "b") in pairs
    drop = features_to_drop(corr, threshold=0.95)
    assert drop == ["b"]  # keep one representative of the correlated cluster
