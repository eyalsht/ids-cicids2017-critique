# Known Limitations

Honest disclosure of this study's limitations and scoping decisions. A documented limitation is
a sign of rigor; an undisclosed one a reader discovers is a flaw.

| # | Limitation | Severity | Note / mitigation |
|---|---|---|---|
| 1 | The source paper publishes **no training code** (Weka GUI); our reproduction is a faithful re-implementation of its described Random-Forest + random-split pipeline, not a rerun of the authors' exact experiment. | Low | We match the headline (macro-F1 0.9987 vs the paper's >0.999). Treated as a finding in Report §5. |
| 2 | **Rare attack classes are statistically un-evaluable.** Heartbleed (2), SQL Injection (4), and Infiltration (7) have single-digit test supports after deduplication, so their per-class recall is not a meaningful estimate. | Medium | Reported explicitly as un-evaluable rather than as success/failure (Report §2 Flaw 3; notebook §4.4). This *is* the point of Flaw 3. |
| 3 | **The temporal split is also a cross-attack-type split.** CICIDS2017 segregates attacks by day, so no clean temporal split shares attack *types* between train (Mon–Thu) and test (Fri); 100% of Friday's attacks are novel classes. | Medium | We frame Strategy B as a near-zero-day generalization test, not a pure leakage test, and isolate duplicate leakage separately (Flaw 1 decomposition). |
| 4 | **Single random seed (`RANDOM_STATE = 42`).** We do not report variance across seeds or cross-validation folds for the headline numbers. | Low | The effects measured are large (51-pp gap) relative to typical seed variance; seeds are fixed for exact reproducibility. |
| 5 | **Flow-only feature space.** CICFlowMeter statistics omit payload content, per-host connection-rate context, and port-entropy signals that could help detect novel attacks. | Low | Listed as concrete future features in Report §4. |
| 6 | **Duplicate count depends on the column basis.** §1.4 counts exact duplicates over the 78 raw columns (307,078 / 10.86%); the modeling mask (§4.0) counts over the 40 engineered features (307,991 / 10.89%). | Low | Both reported; §1.4 raw figure is treated as canonical (Report §2; notebook §4.0 markdown). |
| 7 | **SMOTE on flow features is heuristic.** Interpolating between network-flow vectors can create points that are not physically realizable flows. | Low | SMOTE is applied to the training split only, capped per class, and excludes ultra-rare classes; class-weight is provided as a no-SMOTE cross-check (notebook §4.7). |
| 8 | **`src/ids_critique/` mirrors the notebook's core helpers** as a unit-tested library; the notebook itself remains the primary, self-contained analysis artifact and embeds equivalent logic inline for narrative clarity. | Low | The package is independently tested (`tests/`); it is the canonical, reusable implementation of the stateless helpers. |
