"""The flaw deltas that drive the critique narrative (notebook Section 6).

Each function turns raw metrics into the before/after numbers the report cites.
"""

from __future__ import annotations

import numpy as np


def flaw1_inflation(f1_with_dupes: float, f1_deduped: float) -> float:
    """F1 inflation attributable to duplicate contamination (A0 - A1)."""
    return float(f1_with_dupes - f1_deduped)


def flaw2_drop(f1_random_deduped: float, f1_temporal: float) -> float:
    """F1 drop from the honest temporal split vs the deduped random split (A1 - B0)."""
    return float(f1_random_deduped - f1_temporal)


def total_honest_gap(f1_source: float, f1_temporal: float) -> float:
    """Total gap between the source headline and honest evaluation (A0 - B0)."""
    return float(f1_source - f1_temporal)


def novel_attack_share(train_labels, test_labels, benign: str = "BENIGN") -> float:
    """Fraction of test *attack* flows whose class never appears among train attack flows.

    On CICIDS2017's temporal split this is ~1.0: Friday's attacks (DDoS/PortScan/Botnet) are
    unseen in Mon-Thu training -- the real driver of the performance collapse.
    """
    train = np.asarray(train_labels)
    test = np.asarray(test_labels)
    seen = set(train[train != benign])
    test_attacks = test[test != benign]
    if test_attacks.size == 0:
        return float("nan")
    novel = np.array([lbl not in seen for lbl in test_attacks])
    return float(novel.mean())
