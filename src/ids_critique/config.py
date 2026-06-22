"""Project-wide constants. Single source of truth for the random seed and split key."""

from __future__ import annotations

# Fixed everywhere for exact reproducibility.
RANDOM_STATE = 42

# Ordinal weekday encoding used as the temporal-split key (Mon=0 .. Fri=4).
# CICIDS2017 segregates attacks by day, so this ordering defines the honest
# train (<=3, Mon-Thu) / test (==4, Fri) partition.
WEEKDAY_ORDER: dict[str, int] = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
}

# Temporal split: days <= TRAIN_MAX_DAY are training, the rest is test.
TRAIN_MAX_DAY = 3  # Monday-Thursday
