# Source Article — The Tutorial We Critique

> **Status: PLACEHOLDER — to be confirmed in Phase 0/1 (open decision for Eyal).**
> Once a specific tutorial is locked, fill the "Confirmed Source" block with verbatim claims
> and reported metrics. Until then, the fallback target is the original CICIDS2017 paper.

---

## Selection Criteria

A good source article for our critique:

1. **Public & reproducible** — Towards Data Science, Kaggle, Medium, or a GitHub notebook.
2. **Uses CICIDS2017** — specifically the `MachineLearningCVE` CSV flow features.
3. **Claims F1 / accuracy ≥ 0.99 with Random Forest** (the claim we test).
4. **Has a concrete code artifact** we can point to and reproduce.
5. **High visibility** (claps / stars / forks / citations) — the more cited, the more impactful
   the critique.

> The article must report **aggregate** metrics only (no per-class recall) and use a
> **random** train/test split on **un-deduplicated** data — otherwise our three-flaw narrative
> does not apply to *it* (we'd then critique the canonical paper instead).

---

## Search Queries to Run (Phase 1)

```
site:towardsdatascience.com cicids2017 intrusion detection random forest 99
site:github.com cicids2017 random forest notebook stars
site:kaggle.com cicids2017 random forest 0.99 f1
"CICIDS2017" "Random Forest" "99%" intrusion detection notebook
```

Evaluate the top hits against the selection criteria; prefer one with a runnable notebook and
a clearly stated F1/accuracy number.

---

## Confirmed Source (fill when locked)

```
Title:        <…>
Author:       <…>
Platform:     <Towards Data Science | Kaggle | GitHub | Medium>
URL:          <…>
Date:         <…>
Code link:    <…>
Popularity:   <claps / stars / forks / citations>
```

### Verbatim claims (quote exactly, with location)

> "<paste the exact sentence(s) claiming high performance>"  — (URL, section/paragraph)

### Reported metrics (as stated by the author)

| Metric | Value (claimed) | Split used | Dedup? | Per-class? |
|---|---|---|---|---|
| Accuracy | <…> | random | <no?> | <no?> |
| Macro F1 | <…> | random | <no?> | <no?> |
| Precision | <…> | | | |
| Recall | <…> | | | |

### Methodology gaps to confirm (these enable our critique)
- [ ] Random split (not temporal)?
- [ ] No deduplication before split?
- [ ] Aggregate metrics only (no per-class recall)?
- [ ] No discussion of class imbalance?
- [ ] No discussion of CICFlowMeter Inf/negative artifacts?

---

## Fallback Source (if no tutorial is locked in time)

> **Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018).** *Toward Generating a New
> Intrusion Detection Dataset and Intrusion Traffic Characterization.* ICISSP 2018.

Reported (Random Forest): **Precision = 0.9998, Recall = 0.9996, F1 = 0.9997** (aggregate).
This is public, unambiguous, and exhibits exactly the methodology we critique. A representative
tutorial can be cited as a secondary illustration of how the claim propagates.

---

## Counter-Evidence (our weapon)

> **Engelen, G., Rimmer, V., & Joosen, W. (2021).** *Troubleshooting an Intrusion Detection
> Dataset: the CICIDS2017 Case Study.* IEEE Security and Privacy Workshops (SPW), pp. 7–12.
> https://intrusion-detection.distrinet-research.be/WTMC2021/

```bibtex
@inproceedings{engelen2021troubleshooting,
  title={Troubleshooting an Intrusion Detection Dataset: the CICIDS2017 Case Study},
  author={Engelen, Gints and Rimmer, Vera and Joosen, Wouter},
  booktitle={2021 IEEE Security and Privacy Workshops (SPW)},
  pages={7--12},
  year={2021},
  organization={IEEE}
}
```

> **Lanvin, M. et al. (2022).** *Errors in the CICIDS2017 Dataset and the Significant
> Differences in Detection Performances It Makes.* CRiSIS 2022.
