"""Unit tests for ids_critique.data (no dataset required)."""

import numpy as np
import pandas as pd

from ids_critique.data import (
    count_duplicates,
    count_inf,
    duplicate_subset,
    replace_inf_with_nan,
    strip_column_names,
    weekday_from_filename,
)

# The 8 real CICIDS2017 day-files and their expected weekday codes.
DAY_FILES = {
    "Monday-WorkingHours.pcap_ISCX.csv": 0,
    "Tuesday-WorkingHours.pcap_ISCX.csv": 1,
    "Wednesday-workingHours.pcap_ISCX.csv": 2,  # lowercase 'w' on purpose
    "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv": 3,
    "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv": 3,
    "Friday-WorkingHours-Morning.pcap_ISCX.csv": 4,
    "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv": 4,
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv": 4,
}


def test_weekday_from_filename_maps_all_eight_files():
    for fname, code in DAY_FILES.items():
        assert weekday_from_filename(fname) == code


def test_weekday_from_filename_handles_paths_and_unknowns():
    assert weekday_from_filename("data/MachineLearningCVE/Friday-x.csv") == 4
    assert weekday_from_filename("Saturday-WorkingHours.csv") is None
    assert weekday_from_filename("random.csv") is None


def test_strip_column_names():
    df = pd.DataFrame({" Flow Duration ": [1], "Label": ["BENIGN"]})
    out = strip_column_names(df)
    assert list(out.columns) == ["Flow Duration", "Label"]
    assert " Flow Duration " in df.columns  # original untouched


def test_replace_inf_and_count_inf():
    df = pd.DataFrame({"a": [1.0, np.inf, -np.inf], "b": [0.0, 1.0, 2.0]})
    assert count_inf(df) == 2
    cleaned = replace_inf_with_nan(df)
    assert cleaned["a"].isna().sum() == 2
    assert count_inf(cleaned) == 0


def test_duplicate_subset_excludes_tags():
    df = pd.DataFrame({"f1": [1], "Label": ["BENIGN"], "day": [0], "day_name": ["Monday"]})
    assert duplicate_subset(df) == ["f1", "Label"]


def test_count_duplicates_ignores_tag_columns():
    # Two rows identical in features+label but differing only in tag columns -> still a duplicate.
    df = pd.DataFrame(
        {
            "f1": [1, 1, 2],
            "Label": ["BENIGN", "BENIGN", "ATTACK"],
            "day": [0, 4, 0],
            "day_name": ["Monday", "Friday", "Monday"],
        }
    )
    assert count_duplicates(df) == 1
