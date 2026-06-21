# IDS CICIDS2017 Critique

**Reproducing — and debunking — a "99% F1" Random Forest intrusion-detection tutorial.**

Final project for **Data Science Methods in Cyber Security** (Dr. Uri Itai, University of
Haifa). Student: **Eyal Steinmetz**. Submission deadline: **Friday, 10 July 2026, 23:59**.

---

## TL;DR

A popular class of tutorials trains a Random Forest on the **CICIDS2017** dataset and reports
**F1 ≥ 0.99**. We reproduce that number — then show it is an artifact of three documented
flaws, using the peer-reviewed IEEE paper *Engelen et al. (2021)* as counter-evidence:

1. **Duplicate contamination** — ~250k duplicate flows leak across a random train/test split.
2. **Temporal-split violation** — random splitting mixes Monday→Friday traffic; a real IDS only
   sees *past* traffic. We use a temporal split (train Mon–Thu, test Fri).
3. **Aggregate metrics hide rare-class failure** — macro F1 stays high while recall on rare
   attacks (Heartbleed, Infiltration, SQL Injection) collapses toward zero.

When we correct the methodology, the headline F1 drops materially and dangerous attacks go
undetected — so the original claim is **not supported** as a statement about real-world IDS
performance.

---

## The Critique in One Picture

```
CLAIM:  RF on CICIDS2017 → F1 ≈ 0.999
   └─ reproduce (random split, raw data)         → F1 ≈ 0.999   ✅ confirmed
   └─ remove duplicates           (Flaw 1)       → F1 drops
   └─ temporal split Mon–Thu/Fri  (Flaw 2)       → F1 drops further
   └─ per-class recall            (Flaw 3)       → Heartbleed recall ≈ 0
VERDICT: claim is a measurement artifact, not real-world IDS performance.
```

---

## Models & Strategies

- **Models:** Random Forest (reproduce + baseline), XGBoost (improved), Isolation Forest
  (unsupervised anomaly detection).
- **Strategy A** — random split on raw data (reproduces the source's inflated numbers).
- **Strategy B** — deduplicate + temporal split + SMOTE(train only) + per-class metrics (honest).

---

## Repository Structure

```
.
├── README.md                 this file
├── notebooks/                ids_cicids2017_critique.ipynb  (analysis notebook)
├── figures/                  generated plots
├── report/                   report.pdf  (final write-up)
├── references/               source_article.md, assignment, supporting papers
├── pyproject.toml            dependencies (uv) + ruff config
└── data/                     ⛔ git-ignored — you place the CICIDS2017 CSVs here
```

---

## Getting the Data (manual step)

The dataset is large (~2.8 GB) and **not** committed. Download CICIDS2017 and place the
pre-extracted CSV features here:

```
data/MachineLearningCVE/
├── Monday-WorkingHours.pcap_ISCX.csv
├── Tuesday-WorkingHours.pcap_ISCX.csv
├── Wednesday-WorkingHours.pcap_ISCX.csv
├── Thursday-WorkingHours.pcap_ISCX.csv
└── Friday-WorkingHours.pcap_ISCX.csv
```

- Official source: https://www.unb.ca/cic/datasets/ids-2017.html
- Or the `MachineLearningCSV` mirror on Kaggle.

---

## Reproducing (planned — Phase 1+)

> Tooling is `uv` + `ruff`. Exact commands finalized when the environment is set up in Phase 1.

```bash
# 1. install dependencies into a uv-managed environment
uv sync

# 2. place the dataset (see "Getting the Data" above)

# 3. launch the notebook and run top-to-bottom (Restart & Run All)
uv run jupyter lab notebooks/ids_cicids2017_critique.ipynb
```

All randomness is fixed via `RANDOM_STATE = 42`. The notebook is designed to run cleanly
top-to-bottom with no errors or warnings.

---

## Key References

- **Engelen, G., Rimmer, V., & Joosen, W. (2021).** *Troubleshooting an Intrusion Detection
  Dataset: the CICIDS2017 Case Study.* IEEE SPW, pp. 7–12.
  https://intrusion-detection.distrinet-research.be/WTMC2021/  ← our counter-evidence.
- **Lanvin, M. et al. (2022).** *Errors in the CICIDS2017 Dataset…* CRiSIS 2022.
- **Sharafaldin, I. et al. (2018).** *Toward Generating a New Intrusion Detection Dataset…*
  ICISSP 2018.  ← original CICIDS2017 paper (RF F1 = 0.9997).
- **Source tutorial under critique:** see [`references/source_article.md`](references/source_article.md)
  *(to be confirmed)*.

---

## Project Status

Early stage — repository scaffold and research notes are in place; the analysis notebook and
the written report follow.

---

*Academic project. Dataset and references belong to their respective authors.*
