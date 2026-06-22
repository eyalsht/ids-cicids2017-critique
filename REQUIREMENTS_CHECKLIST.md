# Requirements Checklist

Traceability of every assignment requirement (course project brief) to where it is satisfied
in this repository. A ticked box means the item exists in the tree, not that it is planned.

Legend: ✅ done · location = report section / notebook section / file.

---

## Source selection criteria
| Requirement | Status | Where |
|---|---|---|
| Topic within the allowed list (Intrusion Detection Systems) | ✅ | Source: Rodríguez et al. 2022, *Sensors* MDPI |
| Source clearly defines a problem | ✅ | Report §1 |
| Source proposes a solution | ✅ | Report §1 |
| Includes an implementation / repository | ✅ | No public code (Weka GUI) — re-implemented by us; Report §5 |
| Provides data / enough info to reproduce | ✅ | CICIDS2017 (Kaggle + UNB); Report §5, README |

## PDF report — required sections
| # | Section | Status | Where |
|---|---|---|---|
| 1 | Summary of the Source (problem, importance, solution, dataset, methodology) | ✅ | `report/report.pdf` §1 |
| 2 | Critical Evaluation (claims, evidence, methodology, weaknesses, conclusions) | ✅ | §2 (three-flaw framework + verdict table) |
| 3 | Feature Engineering Analysis (transforms, redundancy, meaningfulness, extra features) | ✅ | §4 |
| 4 | Reproducibility Analysis (runs? deps? hidden preprocessing? overall) | ✅ | §5 |
| 5 | Experimental Results (experiments, modifications, models, metrics, results) | ✅ | §6 (+ per-metric math discussion) |
| 6 | Conclusions (findings, lessons, strengths/weaknesses, future work) | ✅ | §8 |
| 7 | Executive Summary (~1 page) | ✅ | §9 |
| 8 | Summing It Up (problem, source, dataset, methodology, findings, claims held?, insights, recommendation, conclusion) | ✅ | §10 |
| — | Written in English, PDF | ✅ | `report/report.pdf` (LaTeX/MiKTeX) |

## Python notebook — required content
| # | Section | Status | Where |
|---|---|---|---|
| 1 | Data Loading (load, inspect, size, types, temporal, missing, column/index sanity, single-value/duplicate features) | ✅ | notebook §1 |
| 2 | EDA (distributions, missing, outliers, temporal, crosstab, **justified Spearman correlation**, class imbalance/prevalence, visualizations) | ✅ | notebook §2 |
| 3 | Feature Engineering (encoding+why, scaling, creation, selection, dim. reduction) | ✅ | notebook §3 |
| 4 | Model Training (≥2 models — we train 4: RF, XGBoost, Isolation Forest, RF/class-weight) | ✅ | notebook §4 |
| 5 | Evaluation (every metric: math definition + cyber interpretation; justify chosen/excluded) | ✅ | notebook §5 + Report §6 |
| 6 | Error Analysis (failures, error patterns, cyber implications, FP/FN tradeoff) | ✅ | notebook §6 |
| — | Complete, executable, clearly documented; runs top-to-bottom | ✅ | notebook (nbconvert, 0 errors / 0 warnings) |

## Code quality
| Requirement | Status | Where |
|---|---|---|
| Short, focused functions | ✅ | `src/ids_critique/` |
| Meaningful variable names | ✅ | `src/ids_critique/` |
| No unnecessary loops; proper pandas/numpy/sklearn | ✅ | `src/ids_critique/` (vectorized) |
| Clear separation: preprocessing / EDA / training / evaluation | ✅ | `src/ids_critique/{data,features,evaluate,critique}.py` |
| English comments; no duplicated code | ✅ | `src/ids_critique/` |
| Fixed random seeds | ✅ | `src/ids_critique/config.py` (`RANDOM_STATE = 42`) |
| Train/test split or cross-validation | ✅ | notebook §4 (stratified + temporal split) |
| Automated tests | ✅ | `tests/` (pytest; dataset-independent unit tests) |

## Submission requirements
| Requirement | Status | Where |
|---|---|---|
| Public GitHub repo | ✅ | github.com/eyalsht/ids-cicids2017-critique |
| PDF report | ✅ | `report/report.pdf` |
| Python notebook | ✅ | `notebooks/ids_cicids2017_critique.ipynb` |
| Supporting code files | ✅ | `src/ids_critique/`, `tests/` |
| README: description / source link / original repo / execution / dataset | ✅ | `README.md` |
| Repo link emailed to examiner | ⬜ | at submission (Eyal) |

## Grading rubric coverage (100 pts)
| Component | Pts | Primary evidence |
|---|---|---|
| Problem Understanding & Source Selection | 10 | Report §1; README; `references/source_article.md` |
| Summary Quality | 15 | Report §1 |
| **Critical Evaluation of the Author's Claims** | **20** | Report §2 (three flaws, measured deltas, verdict table) |
| Feature Engineering Analysis | 10 | Report §4; notebook §3; `src/ids_critique/features.py` |
| Exploratory Data Analysis | 15 | Report §3; notebook §2; figures 01–06 |
| Model Training & Comparison | 15 | Report §6; notebook §4; figures 12–14 |
| Evaluation & Error Analysis | 10 | Report §6–§7; notebook §5–§6; figures 09–13 |
| Code Quality & Software Engineering | 5 | `src/ids_critique/`, `tests/`, `uv`, ruff-clean, fixed seeds |
