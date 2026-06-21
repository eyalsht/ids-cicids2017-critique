# CICIDS2017 Dataset Inventory

> `MachineLearningCVE/` (Kaggle `chethuhn/network-intrusion-dataset`). The published
> release ships **8** CSV files, not 5: Thursday and Friday are split across multiple
> captures. Row counts are from `pd.read_csv` (notebook §1.1); the weekday is derived
> from each filename. Generated during Phase 2.

## Per-file inventory

| File | Weekday | Size | Rows |
|---|---|---:|---:|
| `Monday-WorkingHours.pcap_ISCX.csv` | Monday | 168 MB | 529,918 |
| `Tuesday-WorkingHours.pcap_ISCX.csv` | Tuesday | 128 MB | 445,909 |
| `Wednesday-workingHours.pcap_ISCX.csv` | Wednesday | 214 MB | 692,703 |
| `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv` | Thursday | 49 MB | 170,366 |
| `Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv` | Thursday | 79 MB | 288,602 |
| `Friday-WorkingHours-Morning.pcap_ISCX.csv` | Friday | 55 MB | 191,033 |
| `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv` | Friday | 73 MB | 286,467 |
| `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` | Friday | 73 MB | 225,745 |
| **Total** | | **~844 MB** | **2,830,743** |

## Per-weekday roll-up (temporal-split groups)

| Weekday | `day` | Rows | Role in temporal split (Strategy B) |
|---|---:|---:|---|
| Monday | 0 | 529,918 | train |
| Tuesday | 1 | 445,909 | train |
| Wednesday | 2 | 692,703 | train |
| Thursday | 3 | 458,968 | train |
| Friday | 4 | 703,245 | **test** |

Total = 2,830,743 rows — matches the figure reported by Rodríguez et al. (2022).

## Notes

- The 8-file layout (vs. the simplified 5-file layout in older docs) is handled by
  `weekday_from_filename()` in notebook §1.1 (case-insensitive prefix match — the
  Wednesday file uses a lowercase `workingHours`).
- After Inf→NaN cleanup, 2,867 rows are dropped, leaving 2,827,876 rows.
- Exact duplicates: 307,078 (10.86%) — retained in Phase 2, deduplicated only in
  Strategy B (see `figures/dedup_stats.txt`).
