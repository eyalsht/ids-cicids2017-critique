# Source Article — The Work We Critique

## Selected Source ✅

**Title:** Evaluation of Machine Learning Techniques for Traffic Flow-Based Intrusion Detection
**Authors:** María Rodríguez, Álvaro Alesanco, Lorena Mehavilla, José García
**Venue:** *Sensors*, MDPI — peer-reviewed open-access journal
**DOI:** 10.3390/s22239326
**Published:** November 30, 2022
**URL:** https://www.mdpi.com/1424-8220/22/23/9326
**Full text (free):** https://www.mdpi.com/1424-8220/22/23/9326/htm
**PDF (free):** https://www.mdpi.com/1424-8220/22/23/9326/pdf

## Why This Is the Ideal Source

This is a **peer-reviewed journal article** in a legitimate indexed journal (Sensors, MDPI,
ISSN 1424-8220), not just a blog post. This satisfies the HW requirement for "article"
and actually makes our critique more academically serious — we are not just disproving
a GitHub notebook, we are disproving a published paper.

The paper evaluates ML techniques on CICIDS2017 using Weka and concludes:
> "tree-based techniques (PART, J48, and random forest) have turned out to be the most
> efficient with **F1 values above 0.999** (average obtained in the complete dataset)"

Our project reproduces this in Python/sklearn, confirms the 0.999 figure — then shows
exactly why it is wrong using Engelen et al. (2021) as counter-evidence.

## Key Claims to Disprove

| Claim | Quote from paper | Our counter-test |
|-------|-----------------|-----------------|
| F1 > 0.999 | "F1 values above 0.999 (average obtained in the complete dataset)" | Show F1 drops after dedup + temporal split |
| RF appropriate for IDS | "tree-based ML techniques may be appropriate in the flow-based intrusion detection problem" | Show Heartbleed/Infiltration recall ≈ 0 |
| Complete dataset approach valid | "joint file obtained from the CICIDS2017 dataset includes 2,830,743 traffic flows" | Show mixing all days = temporal leakage |

## Methodology They Used (the flaws)

- **Tool:** Weka (not Python) — we reproduce in Python/sklearn for verifiability
- **Split:** Random split on the joint concatenated dataset of all 5 days — no temporal awareness
- **Deduplication:** Not mentioned anywhere in the paper
- **Metrics:** Macro F1 average across all classes — no per-class breakdown for rare attacks
- **Classes:** Treats Heartbleed (11 samples) the same as DoS Hulk (230,000 samples) in macro average

## The Three Flaws (mapped to Engelen 2021)

**Flaw 1 — Temporal leakage:**
The paper creates a "joint file" of all 5 days, then splits randomly. Monday benign traffic
mixes with Friday PortScan in both train and test. Engelen et al. (2021) showed this is
methodologically incorrect for IDS evaluation.

**Flaw 2 — Duplicate contamination:**
CICIDS2017 has ~250k duplicate rows. The paper does not mention deduplication.
With a random split on the joint file, duplicate rows appear in both train and test,
inflating all metrics (Engelen et al., 2021).

**Flaw 3 — Macro F1 hides rare-class failure:**
Reporting "F1 > 0.999" as a macro average on a dataset with 11 Heartbleed samples
and 2.27M BENIGN samples is statistically misleading. A model that never detects
Heartbleed still achieves F1 ≈ 0.999 macro because BENIGN and DoS dominate.

## What We Do Instead (the reproduction + correction)

1. **Reproduce:** Load same CICIDS2017 CSVs, concatenate all days, random split → confirm F1 ≈ 0.999 with RF
2. **Correct Flaw 1:** Apply temporal split (Mon–Thu train, Fri test) → show F1 drop
3. **Correct Flaw 2:** Deduplicate before split → show additional F1 drop
4. **Correct Flaw 3:** Show per-class breakdown → Heartbleed recall ≈ 0

## Citation for Our Report

```bibtex
@article{rodriguez2022evaluation,
  title     = {Evaluation of Machine Learning Techniques for Traffic
               Flow-Based Intrusion Detection},
  author    = {Rodríguez, María and Alesanco, Álvaro and
               Mehavilla, Lorena and García, José},
  journal   = {Sensors},
  volume    = {22},
  number    = {23},
  pages     = {9326},
  year      = {2022},
  publisher = {MDPI},
  doi       = {10.3390/s22239326},
  url       = {https://www.mdpi.com/1424-8220/22/23/9326}
}
```

## Counter-Evidence (our weapon)

```bibtex
@inproceedings{engelen2021troubleshooting,
  title     = {Troubleshooting an Intrusion Detection Dataset:
               the CICIDS2017 Case Study},
  author    = {Engelen, Gints and Rimmer, Vera and Joosen, Wouter},
  booktitle = {2021 IEEE Security and Privacy Workshops (SPW)},
  pages     = {7--12},
  year      = {2021},
  doi       = {10.1109/SPW53761.2021.00009}
}
```

## Note on Code Reproduction

The original paper uses **Weka** (Java GUI tool) — no Python code available.
This means we build our own Python/sklearn reproduction from their methodology description.
This is actually fine and standard — the HW says "reproduce the proposed solution",
which we do by implementing their pipeline (same dataset, same RF, same random split)
and confirming their reported metrics before critiquing them.

Our implementation advantage: Python notebooks are more transparent, reproducible,
and inspectable than Weka experiments — another point in our favor during the critique.
