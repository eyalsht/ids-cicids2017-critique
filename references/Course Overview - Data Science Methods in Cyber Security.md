# Data Science Methods in Cyber Security — Course Overview

> **Course:** Data Science Methods in Cyber Security (University of Haifa)
> **What this is:** A clean, conceptual walkthrough of the course's 27 lecture decks — what each topic *is*, the methods it offers, and how it's used in security. Written as a learning reference and as durable project context (not as exam-cram material; a separate exam-revision summary covers that).
> **Through-line:** The course teaches a data-science workflow for defending systems — understand the data, find what's abnormal, group and compare behaviour, model it, keep the models trustworthy, and feed conclusions back into defenses. The final "Pipeline" lecture stitches all of it together.

> *Note on sourcing:* these notes were built from the text on the slides. Diagrams, charts, and image-rendered equations aren't captured, so a few figure-heavy formulas are described rather than typeset. The ordering is thematic (foundations → core methods → trustworthy AI → security domain → capstone), not necessarily the calendar order taught.

---

## Table of Contents

**Part 1 — Foundations: Security Context & Statistics**
1. [Introduction to Machine Learning in Cybersecurity](#introduction-to-machine-learning-in-cybersecurity)
2. [Statistics Toolkit](#statistics-toolkit)
3. [Positive Definite Matrices and Ellipsoids](#positive-definite-matrices-and-ellipsoids)
4. [Categorical Data](#categorical-data)
5. [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
6. [EDA Revisited — A Deeper Look at the Data](#eda-revisited--a-deeper-look-at-the-data)
7. [Goodness of Fit — Evaluating Models](#goodness-of-fit--evaluating-models)

**Part 2 — Core ML & Data Analysis Methods**
8. [Clustering](#clustering)
9. [Segmentation Analysis](#segmentation-analysis)
10. [Abnormality Detection](#abnormality-detection)
11. [Time Series Analysis](#time-series-analysis)
12. [Graph Theory](#graph-theory)
13. [Natural Language Processing](#natural-language-processing)
14. [Reinforcement Learning](#reinforcement-learning)

**Part 3 — Trustworthy & Advanced AI**
15. [Adversarial Attacks in Machine Learning](#adversarial-attacks-in-machine-learning)
16. [Explainability](#explainability)
17. [Fair AI](#fair-ai)
18. [Differential Privacy](#differential-privacy)
19. [Federated Learning](#federated-learning)
20. [Securing AI / Content Safety](#securing-ai--content-safety)

**Part 4 — Cybersecurity Domain & Operations**
21. [Security Operations Center (SOC)](#security-operations-center-soc)
22. [Zero Trust](#zero-trust)
23. [Honeypots](#honeypots)
24. [Social Engineering](#social-engineering)
25. [Zero-Day Attacks](#zero-day-attacks)
26. [Dictionary Attacks & Password Security](#dictionary-attacks--password-security)

**Capstone**
27. [Pipeline — Putting It Together](#pipeline--putting-it-together)

---

# Part 1 — Foundations: Security Context & Statistics

## Introduction to Machine Learning in Cybersecurity

This opening lecture sets the security backdrop for the whole course: the threat landscape, the main attack families, the basic defenses, and where data science fits in. The framing that matters most is the last point — in most real deployments, **ML is an alert layer that flags potential threats for a human to judge, not an autonomous actor**. The CISO (not the model) holds final decision authority.

**The security picture it establishes**
- **Security objectives** — Confidentiality, Integrity, Availability (the CIA triad), plus Authenticity and Non-repudiation.
- **What a security program is made of** — People (professionals, users, attackers), Processes (policies), and Technology (firewalls, antivirus, IDS).
- **Malware families** — viruses (self-replicating), trojans (disguised), ransomware (encrypt + extort), spyware (steal info), worms (self-propagating).
- **Availability attacks** — DoS / DDoS, split into volume-based (UDP/ICMP flood), protocol (SYN flood), and application-layer (HTTP flood, Slowloris); large attacks ride on botnets (e.g. Mirai).
- **Social engineering** — phishing, spear phishing, vishing, baiting, impersonation, pretexting, tailgating, quid pro quo.
- **Web/app attacks** — SQL injection (union/error/blind; prevented chiefly by parameterized queries), XSS (injecting scripts into a trusted site).
- **Network/crypto basics** — packet sniffing (passive vs active; Wireshark/Tcpdump); public vs private keys and PKI (RSA as the canonical asymmetric algorithm); MFA ("something you know/have/are"); HTTP (port 80, plaintext) vs HTTPS (port 443, TLS + CA certificates).
- **Team colors** — Blue (defend), Red (attack/pen-test), Purple (collaborative).
- **Deep vs dark web** — deep = unindexed content; dark = an intentionally hidden subset reached via Tor.

**Why it's here:** everything later in the course is a data-science technique applied to detecting or understanding one of these threats.

---

## Statistics Toolkit

A refresher on the statistics the rest of the course leans on: describing data, testing hypotheses, and finding outliers in one and many dimensions. The security payoff is anomaly detection — thresholding on traffic, user behaviour, or transaction features to surface attacks and fraud.

**Describing data**
- **Central tendency** — mean (best for roughly normal data, sensitive to outliers), median (robust, for skewed data), mode (for categorical/nominal data).
- **Dispersion** — variance (mean squared deviation) and standard deviation (its root); robust alternatives are MAD (median absolute deviation) and IQR (Q3 − Q1).
- **Shape** — skewness (asymmetry; Pearson skew = (mean − mode)/SD or 3(mean − median)/SD) and kurtosis ("tailedness" — how often extreme values occur).

**Inference**
- **Null hypothesis (H₀)** — the default "no effect" assumption you reject or fail to reject.
- **p-value** — strength of evidence against H₀ (p < 0.05 is conventionally "strong"). Crucially, it is *not* the probability that H₀ is true.

**Multivariate structure & outliers**
- **Covariance** — how two variables move together; generalizes to the covariance matrix.
- **PCA** — finds orthogonal axes of maximum variance for dimensionality reduction (counters the curse of dimensionality). Pipeline: center → covariance matrix → eigenvectors/values → sort → select → project.
- **The 68-95-99.7 rule** for normal data, and three one-dimensional outlier rules: distance from the mean in SDs, from the median in MADs, or beyond Q1/Q3 by a multiple of IQR (k = 3 is common).
- **Mahalanobis distance** — D(x) = √((x−μ)ᵀ Σ⁻¹ (x−μ)) — a multivariate outlier score that accounts for correlations between features, which plain Euclidean distance ignores.

**In security:** mean+SD thresholds on minute-by-minute traffic flag DDoS or abnormal usage; Mahalanobis distance flags anomalous multi-feature behaviour that no single feature would reveal.

---

## Positive Definite Matrices and Ellipsoids

The geometric companion to the statistics lecture: it explains *why* the covariance-based outlier methods work by interpreting quadratic forms as ellipsoids. This is the mathematical backbone behind Mahalanobis distance and PCA.

**The core ideas**
- A **quadratic form** xᵀAx maps a vector to a scalar; with symmetric A the geometry is smooth.
- A matrix is **positive definite** when xᵀAx > 0 for all non-zero x — equivalently, all its eigenvalues are positive. Such a matrix defines a valid notion of distance.
- The set xᵀAx = 1 is an **ellipsoid**. Eigen-decomposition A = QΛQᵀ separates it into a rotation (Q, the axis directions) and a scaling (Λ, the eigenvalues).
- The **covariance ellipsoid** (x−μ)ᵀ Σ⁻¹ (x−μ) = 1 is centered at the mean μ with its shape set by Σ. Axis lengths equal √(eigenvalues of Σ) — i.e. the standard deviation along each principal direction.

**Outlier interpretation:** a point's Mahalanobis distance is how far outside the confidence ellipsoid it sits. Since the squared distance follows a χ² distribution, you can pick a statistical cutoff (95% / 99%) to declare anomalies. Because covariance itself is sensitive to outliers, robust estimators are preferred in practice.

---

## Categorical Data

How to handle features that are labels rather than numbers — and the statistics, encodings, and privacy ideas that go with them. This lecture also introduces power-law distributions and k-anonymity, both of which recur later.

**Concepts**
- **Nominal vs ordinal** — nominal has no order (colors, countries); ordinal has a meaningful order (education level, ratings).
- **The numeric-looking trap** — IDs, phone numbers, ZIP codes and product codes *look* numeric but are categorical; doing arithmetic on them is meaningless.
- **Parametric vs non-parametric statistics** — parametric tests assume a distribution (t-test, ANOVA, linear regression: efficient but assumption-sensitive); non-parametric tests assume little (Mann-Whitney, Wilcoxon, chi-squared, Spearman: robust but less powerful on small samples). Useful pairings: t-test ↔ Mann-Whitney, linear regression ↔ Spearman.
- **Segmentation** — splitting data into subsets (demographic, behavioral, geographic, temporal); smaller segments show bigger effects but weaker significance.
- **Power-law / scale-free distributions** — a few extreme values and a long tail of small ones (Pareto 80/20); they appear as a straight line on a log-log plot. Scale-free *networks* are robust to random failure but fragile under targeted attack.
- **k-Anonymity** — each record is indistinguishable from at least k−1 others on its quasi-identifiers.

**Methods**
- **Encodings** — one-hot (binary columns), label (integers, when order matters), count (by frequency), and mean/target encoding (category → mean of target; risks overfitting, so use smoothing/noise/cross-validation).
- **Association measures** — the chi-squared test (significance of association in a contingency table; also detects distribution shift) and Cramér's V (association strength, 0 to 1). Independence means P(A∩B) = P(A)·P(B).
- **k-anonymity techniques** — generalization (ranges), suppression (remove), perturbation (add noise).

**In security:** a sudden change in a value distribution or crosstab structure can signal an attack; a crosstab between username and password can reveal aliasing. k-anonymity protects against re-identification but is limited by high dimensionality and external knowledge.

---

## Exploratory Data Analysis (EDA)

EDA is the disciplined "look before you model" step, framed here for security: you often find threats in metadata and traffic patterns before any formal model is built.

**Concepts**
- **EDA** — analyzing data visually and statistically to find patterns, anomalies, and insights before modeling; it informs model choice, reporting, and maintenance.
- **Context dependence** — the same value can be an outlier in one setting and normal in another, so the method must fit the context.
- **Security data sources** — logs/audit trails, network traffic, authentication records, file-access records.
- **Meta / file analysis** — examine file *properties* (name, size, timing, source, author) rather than content.
- **Network-based detection** — watch traffic for unusual patterns, malicious payloads, and unrecognized protocols/ports.

**Practical signals**
- **File-name red flags** — double extensions (`document.pdf.exe`), typosquatting (`ph1shing.docx`), random strings (`a5f8g3t2.dat`), executables wearing innocent names (`family_photo.jpg.exe`).
- **Role-vs-activity cross-checks** — comparing a version-control or company-hierarchy graph against who's actually acting (HR adding code → possible insider threat).
- **Topic modeling (LDA)** — do filenames in a folder share a sensible topic, or does one not belong?

**In security:** EDA on metadata, file properties, and traffic catches intrusions, exfiltration, and DDoS early, and supports continuous monitoring and data governance.

---

## EDA Revisited — A Deeper Look at the Data

A second EDA pass that goes deeper into cleaning, representing, and correlating data — including the temporal pitfalls that matter enormously in security.

**The EDA process** — collection → cleaning → exploration → feature engineering → hypothesis testing → reporting.

**Data-quality checks**
- Duplicates (do they make sense?), single-value features (useless), and features with almost as many distinct values as rows (likely an index).
- **Missing values** — count them, then ask *why* they're missing and whether missingness is itself informative before imputing.
- **Special / sentinel values** — 0, −1, 255 (FF), or midnight 1 Jan 1970 often carry hidden meaning. A classic artifact: imputing missing dates to 0 produces a suspicious spike at the Unix epoch.

**Representing and relating data**
- **Feature vectors** turn unstructured text/images/audio into numbers — text via Bag of Words, TF-IDF, or Word2Vec; images via CNN features. Scale or standardize so features are comparable.
- **Correlation measures** — Pearson (linear), Spearman (monotonic, rank-based, outlier-robust), Kendall τ (ordinal), Phi (two dichotomous categoricals), and PPS (Predictive Power Score: captures non-linear, asymmetric predictive power). **Correlation never implies causation** (ice cream vs shark attacks).
- **Temporal features** — use only features known at prediction time; mind time zones, DST, holidays, and seasonality. Tools: seasonal decomposition, rolling mean/STD, and Chebyshev's inequality for anomaly bounds.

**In security:** structural time constraints make great anomaly detectors — no email arrives from the future, an action can't precede its prerequisite, and the recurring 1/1/1970 timestamp is a data-quality red flag.

---

## Goodness of Fit — Evaluating Models

How to tell whether a model is actually good — with heavy emphasis on why accuracy is the wrong metric for the rare-event problems that dominate security.

**Concepts**
- **Why accuracy misleads** — when positives are rare (fraud, intrusion, cancer), a model that always predicts "negative" scores high accuracy while being useless.
- **Confusion matrix** — TP/FP/TN/FN, the basis for every classification metric.
- **Overfitting vs underfitting** — overfit = great on training, poor on new data (too complex / too little data); underfit = poor on both (too simple). Managed with regularization, cross-validation, early stopping, and more data.

**Metrics**
- **Precision and recall** — recall (TPR) = TP/(TP+FN); FPR = FP/(FP+TN).
- **F1** — harmonic mean of precision and recall.
- **MCC (Matthews Correlation Coefficient)** — correlation between truth and prediction (−1 to +1), robust to imbalance.
- **ROC / AUC** — plots TPR vs FPR across thresholds; AUC = 1 perfect, 0.5 random, < 0.5 worse than chance. Threshold-independent and robust to imbalance.
- **Regression metrics** — MSE (penalizes large errors), R² (vs a constant baseline).
- **Regularization** — L1 (Lasso), L2 (Ridge), dropout; plus data augmentation and early stopping.
- **Validation** — train/test split (stratified for imbalance) and k-fold cross-validation; avoid data leakage.

**In security:** because attacks are rare, prefer F1/MCC/AUC over accuracy. With temporal data, always train on the past and test on the future, using only features known at prediction time. Multiclass setups model different attack types; "general recall" asks whether you narrowed the threat to a small candidate set.

---

# Part 2 — Core ML & Data Analysis Methods

## Clustering

Unsupervised grouping — finding structure when you have no labels, which is the normal situation in threat discovery. The lecture covers the main algorithm families and how to validate the clusters you get.

**Concepts**
- **Hard vs soft** — hard clustering puts each point in exactly one group (K-Means, hierarchical); soft assigns probabilistic membership (Fuzzy C-Means, GMM).
- **Families** — partitioning (K-Means), density-based (DBSCAN), hierarchical (agglomerative/divisive), model-based (GMM), and spectral (eigenvectors of a similarity matrix).

**Algorithms**
- **K-Means** — initialize K centroids → assign points to nearest → recompute centroids → repeat. Choose K with the elbow method. Weaknesses: sensitive to initialization, assumes spherical equal-size clusters. Variants: K-Means++, Mini-Batch.
- **DBSCAN** — density-based with parameters ε (radius) and MinPts; labels points as core, border, or noise. Strengths: finds arbitrary shapes, handles noise, needs no K. Weaknesses: hard to tune, struggles with varying density. Variants: OPTICS, HDBSCAN.
- **Hierarchical** — builds a dendrogram (agglomerative bottom-up or divisive top-down); cut it to choose the number of clusters. Linkages: single, complete, average, Ward. Costly and noise-sensitive.
- **GMM** — models data as a mixture of Gaussians with mixing weights and covariances, fit by Expectation-Maximization; gives soft assignments.
- **ANOVA** — used here to *validate* clusters: its F-statistic (between-group variance / within-group variance) tests whether cluster means genuinely differ.

**In security:** anomaly detection, attack attribution (grouping signatures), malware clustering, insider-threat and user-behaviour analysis, zero-day discovery, and incident prioritization.

---

## Segmentation Analysis

Two complementary ideas under one roof: segmentation as a *defensive network architecture*, and the *statistics of comparing distributions* across segments.

**Network segmentation (the defense)**
- Dividing a network into isolated zones limits lateral movement and shrinks the attack surface. Zones group resources of similar function/trust, enforced by firewalls, IDS, auth, and encryption.
- **Micro-segmentation** pushes this down to individual devices/workloads (common in cloud), limiting the "blast radius" of any breach.

**Comparing distributions (the statistics)**
- **KL divergence** — D_KL(P‖Q) = Σ P(x)·log(P(x)/Q(x)); non-negative and **asymmetric**. **Jensen-Shannon divergence** is its symmetric version.
- **Kolmogorov-Smirnov test** — D = max|EDF − CDF|, the largest gap between empirical and theoretical distributions.
- **Earth Mover's (Wasserstein) distance** — the minimum "cost × mass moved" to turn one distribution into another.
- **Laplace (add-one) smoothing** — adds a constant to counts so zero-probability events don't break estimates.
- **Effect size vs significance** — magnitude of a difference vs whether it's unlikely to be chance; you need both. (90 heads / 10 tails is "more unfair" than 2/0 because of sample size.) A Simpson's-paradox-style caution: small populations produce extreme rates in both directions for no real reason. There's also a lag-vs-stability trade-off: more significance needs more data and so more reporting delay.

**In security:** segmentation contains threats; distribution-comparison metrics detect behaviour/data drift across time, regions, or clusters — an early signal of anomalies.

---

## Abnormality Detection

A dedicated survey of anomaly detection — the central technique of the course — across statistical, ML, deep-learning, and time-series methods, plus the conceptual vocabulary for talking about rare events.

**Conceptual framing**
- **Long tail vs outliers** — a long tail is many expected low-frequency items; outliers are individual points far from the rest.
- **Tail events, outliers, and Black Swans** — tail events are rare extreme occurrences; a *Black Swan* (Taleb) is unpredictable, rare, and high-impact (beware the "turkey before Thanksgiving" inductive fallacy); a *Grey Swan* is foreseeable but high-impact.
- **Epistemic vs aleatory uncertainty** — epistemic comes from lack of knowledge (reducible with more data/better models); aleatory is inherent randomness (handled with probabilistic models, Monte Carlo, redundancy).

**Methods**
- **Statistical** — Z-score, Mahalanobis distance, Chebyshev's inequality.
- **Isolation Forest** — randomly partitions the space; anomalies get isolated in fewer splits. Scales well in high dimensions, needs no feature scaling; weak on strongly clustered data.
- **One-Class SVM** — learns a boundary around normal data (the kernel can be swapped for a neural net → deep one-class).
- **Local Outlier Factor (LOF)** — compares a point's local density to its neighbours'; it's *local*, not global ("neighbours 2 km away: normal in Alaska, abnormal in NYC").
- **PCA / Autoencoders** — reconstruct the input; high reconstruction error = anomaly (autoencoders are the neural analog of PCA).
- **GANs** — the discriminator flags out-of-distribution data.
- **Time-series** — moving average, moving STD, differencing, cumulative sums, and SARIMA.

**In security:** earlier threat detection and reduced dwell time — abnormal logins, privilege escalation, unusual data access, malware and ransomware campaigns, credential harvesting, and DDoS traffic spikes.

---

## Time Series Analysis

Forecasting and characterizing data ordered in time — essential because logs, traffic, and system metrics are all time series, and their order carries information.

**Concepts**
- **Information flow** — data moves past → future; the past is known and the future isn't. This is *why* you never shuffle a time series and always train before you test.
- **Properties** — regularity (even intervals), stability (consistent statistics), lumpiness (uneven activity), and **stationarity** (constant mean/variance/autocovariance — required by ARIMA, tested with the Augmented Dickey-Fuller test).
- **Decomposition** — trend, seasonality, cyclic component, and residual; combined additively (Y = T+S+R, constant variation) or multiplicatively (Y = T×S×R, variation that scales with level).
- **Memory & complexity** — the Hurst exponent (H = 0.5 random walk, > 0.5 trending, < 0.5 mean-reverting) and entropy measures.

**Models**
- **ARIMA(p,d,q)** — autoregression (p, read from PACF) + integration/differencing (d, for stationarity) + moving average (q, read from ACF). **SARIMA** adds seasonal terms.
- **ARCH/GARCH** — model time-varying volatility (volatility clustering) that ARIMA's constant-variance assumption can't.
- **Deep models** — RNN/LSTM/GRU (LSTM gates handle long-term dependencies and vanishing gradients) and Transformers (self-attention, parallel, long-range).
- **Tree ensembles** — Random Forest (bagging) and XGBoost (boosting) for feature-engineered tabular forecasting.

**In security:** predicting failures, anomalies, and resource needs from network and system telemetry.

---

## Graph Theory

Graphs model relationships — between hosts, users, permissions, and indicators — which makes them a natural fit for security. The lecture builds from fundamentals to graph cuts, community detection, and graph neural networks.

**Fundamentals**
- A graph is vertices plus edges; varieties include directed/undirected, weighted, bipartite, complete, trees/forests, and DAGs.
- Key quantities: degree, paths and cycles, connectivity and components, **centrality** (degree, betweenness, closeness — finds chokepoint nodes), and cliques (maximal clique, clique number).
- Two classic distinctions: **Eulerian** (use every edge once) vs **Hamiltonian** (visit every vertex once) paths, and the friendship paradox (your neighbours have more neighbours than you do, on average).

**Methods**
- **Representations** — adjacency matrix (O(1) lookup, O(n²) space), adjacency list (O(n+e), good for traversal), and edge list.
- **Traversal** — BFS (level by level, queue) vs DFS (deep then backtrack, stack).
- **Graph cuts** — the Max-Flow Min-Cut theorem (max flow = min cut); algorithms include Ford-Fulkerson and Edmonds-Karp.
- **Community detection** — modularity-based, hierarchical, spectral, and density-based. Spectral clustering uses the Laplacian L = D − A and the Fiedler vector to split non-convex clusters.
- **GNNs** — learn node embeddings by message passing (GCN, GAT); used for node classification, link prediction, and graph classification.

**In security:** network graphs (hosts/routers), access graphs (users/permissions), attack graphs (breach paths), and threat-intel graphs (IPs/hashes/domains). Applications include intrusion detection via anomalous subgraphs, threat hunting, attack-path analysis (patch by shortest attack path), insider-threat detection via community structure, and malware detection via API-call graphs. Tools: NetworkX, Neo4j, MITRE ATT&CK.

---

## Natural Language Processing

Turning unstructured text — threat reports, emails, dark-web chatter, logs — into structured signal, and understanding the obfuscation attacks that target text filters.

**Concepts**
- **NLP** converts text into structured insight via tokenization, named-entity recognition, sentiment analysis, and topic modeling.
- **IOCs (Indicators of Compromise)** — IPs, domains, hashes, malware names, CVE IDs, threat actors — extracted with **NER** (rule/CRF/Bi-LSTM/BERT pipelines feeding a knowledge graph).
- **Bag of Words** counts words but discards order, so it fails on negation ("good, not bad").
- **Word embeddings** are dense vectors capturing meaning, enabling ML on otherwise sparse text.
- **Topic modeling** (LDA, NMF, LSA) discovers latent themes.
- **Obfuscation attacks** — homoglyphs (Cyrillic р vs Latin p) and LLM hallucination (confident fabrication) round out the threat side.

**Methods**
- **Levenshtein (edit) distance** — minimum single-character edits to transform one string into another (kitten → sitting = 3); extensions handle transpositions and short names.
- **TF-IDF** — TF × IDF (IDF = log(N/n_t)) highlights rare-but-meaningful terms.
- **Bayesian spam filtering** — Bayes' theorem updates P(spam | features) from labeled data.
- **Transformers / BERT** — self-attention and bidirectional contextual embeddings.

**In security:** threat-intel extraction, phishing detection (urgency/misspelling patterns), dark-web monitoring, SOC automation, and malware detection. Attackers evade text filters with misspellings (`passw0rd`), spacing (`p.a.s.s.w.o.r.d`), and homoglyphs; defenses normalize/canonicalize text, use fuzzy matching, and apply adversarial training. The broader attack taxonomy — evasion (mislead at inference) vs poisoning (corrupt training), white-box vs black-box — is introduced here and expanded in the adversarial-attacks lecture.

---

## Reinforcement Learning

Learning by trial and error against an environment — useful for adaptive defenses that must keep adjusting to a changing adversary.

**Concepts**
- **Multi-Armed Bandit (MAB)** — choose among "arms" with unknown reward distributions to maximize cumulative reward; the toy model for the **exploration vs exploitation** trade-off (try new options to learn vs exploit known good ones).
- **Regret** — the gap between your reward and the optimum; an alternative objective to minimize.
- **RL framework** — agent, environment, actions, rewards, states, transitions. A **policy** is the agent's strategy, a **value function** the expected reward of a state, and a **Q-function** the expected reward of an action in a state.
- **Model-based vs model-free** — build a predictive model of the environment vs learn directly from experience (simpler, flexible).
- **Sparse reward** — infrequent/delayed feedback makes credit assignment hard; addressed with curriculum learning, intrinsic motivation, hierarchical RL, and imitation learning.

**Methods**
- **Q-Learning** — model-free, off-policy; a Q-table of state-action values updated via the Bellman equation, with learning rate α.
- **ε-Greedy** — explore randomly with probability ε, otherwise pick the best-known action.
- **DQN** — Q-learning with a neural network for large state spaces (where a Q-table can't scale).
- **Policy gradients** optimize the policy directly. **A/B testing** is contrasted as a related controlled-experiment framework.

**In security:** intrusion detection, vulnerability/patch prioritization, and adaptive security policies that adjust in real time to the threat landscape.

---

# Part 3 — Trustworthy & Advanced AI

## Adversarial Attacks in Machine Learning

When ML is part of a defense, the model itself becomes a target. This lecture maps how attackers manipulate models across the lifecycle and how to defend — including in federated settings.

**Attack types**
- **Adversarial (evasion) attack** — a small, human-imperceptible perturbation of an input that flips the model's decision at inference time.
- **Poisoning attack** — injecting bad data during *training* so the model learns wrong associations; hard to distinguish from ordinary noise/overfitting.
- **Model extraction / theft** — querying a black-box API to train a surrogate that clones it (threatening IP and enabling further attacks).
- **Byzantine attack** — malicious participants in a distributed/federated system corrupt the shared model (label/gradient flipping, backdoors), after the Byzantine Generals' Problem.
- **Knowledge axes** — white-box vs black-box, targeted vs non-targeted, and **transferability** (an example crafted for one model often fools others).

**Methods & defenses**
- **FGSM (Fast Gradient Sign Method)** — the canonical gradient-based attack: x_adv = x + ε·sign(∇ₓ J(θ,x,y)).
- **Krum** — a Byzantine-robust aggregation rule that picks the gradient closest to the honest majority; **Multi-Krum**, Trimmed Mean, coordinate-wise Median, and Bulyan are relatives.
- **General defenses** — adversarial training, defensive distillation, input preprocessing, ensembles, anomaly detection on inputs/queries, rate limiting, watermarking, and output obfuscation.

**In security:** these are real attacks on deployed prediction systems, with physical consequences against industrial control systems. Detecting model extraction mirrors intrusion detection — query logging, behaviour profiling, canary traps. Federated/distributed ML and LLMs are especially exposed.

---

## Explainability

Black-box models need to be interpretable to be trusted, audited, and acted upon — and explanations connect to the deeper question of causation.

**Concepts**
- **Levels of explanation** — model-level (the whole model), feature-level (which features matter), and instance-level (why this one prediction); and the global vs local distinction.
- **Inherently interpretable models** — linear regression, decision trees, rule-based models — trade some performance for transparency.
- **Correlation, not causation** — SHAP and LIME explain *associations*; genuine cause-effect needs causal inference.
- **Redundancy** — duplicate or highly-correlated features add no information, encourage overfitting, and actually break SHAP/LIME.

**Methods**
- **LIME** — explains one prediction by perturbing the instance, querying the model, and fitting a simple local surrogate. Model-agnostic but sample-hungry and sensitive to the perturbation scheme.
- **SHAP** — attributes importance via Shapley values from cooperative game theory (a feature's average marginal contribution over all coalitions). Strong theoretical basis, but costly, baseline-sensitive, and degrades under redundancy.
- **Detecting/handling redundancy** — correlation matrices, Variance Inflation Factor (VIF > 10 = high multicollinearity); feature selection (RFE, Lasso) and dimensionality reduction (PCA, t-SNE, autoencoders).
- **Causal inference** — Granger causality (does past X improve prediction of future Y?), RCTs (the gold standard), and quasi-experimental methods (Difference-in-Differences, Instrumental Variables, Regression Discontinuity).

**In security:** explanations justify updating a firewall rule, support reporting to executives, and help trace *why* an alert fired.

---

## Fair AI

Algorithms can encode and amplify bias; this lecture covers what fairness means, where bias comes from, and the statistical paradoxes that hide or manufacture it.

**Concepts**
- **Fairness definitions** — demographic parity (equal outcomes), equal opportunity (equal true-positive rates), individual fairness (similar people treated similarly), calibration (equal reliability). These conflict — you can't satisfy all at once, and there's a fairness-accuracy trade-off.
- **Sources of unfairness** — historical bias, skewed representation, label/feedback-loop bias, and aggregate metrics that hide subgroup disparities.
- **Proxy features** — neutral-seeming features correlated with protected attributes (zip code → race), so naively dropping a feature can backfire.
- **Statistical paradoxes** — Simpson's (a subgroup trend reverses when groups are combined — the Berkeley admissions case), Berkson's (selection bias creates a false correlation), and Benford's Law (in many natural datasets the leading digit is 1 about 30% of the time; P(d) = log₁₀(1 + 1/d)).

**Methods**
- **Mitigation by stage** — pre-processing (reweighing, sampling), in-processing (fair training objectives), post-processing (adjusting predictions).
- **Auditing** — disaggregated metrics, statistical parity, disparate impact, subgroup and adversarial testing. Tools: AIF360, Fairlearn.

**In security:** Berkson's paradox shows up because IDS/security logs only record *detected* incidents, producing spurious correlations and poor generalization. Benford's Law is a fraud/anomaly red flag in logs and transactions (a spike in ports starting 8/9 may indicate spoofing) — a flag, not proof. Averaging can mask risk that's concentrated in off-hours or specific groups.

---

## Differential Privacy

A mathematically rigorous way to learn from sensitive data without exposing individuals — increasingly the industry standard for privacy-preserving analytics.

**Concepts**
- **Differential Privacy (DP)** — adds calibrated random noise so that group-level analysis stays accurate while individual records are protected. Formally, P[M(D₁) ∈ S] ≤ e^ε · P[M(D₂) ∈ S] for datasets differing in one record.
- **ε (privacy budget)** — smaller ε means stronger privacy but more noise and less utility; this is the central knob.
- **Central vs local DP** — noise added server-side after collection vs on the user's device before data leaves it.
- **k-anonymity** (contrast) — simpler and interpretable, but vulnerable to background-knowledge/linkage attacks.

**Methods**
- **Laplace mechanism** — noise for numeric query results.
- **Exponential mechanism** — probabilistic selection for non-numeric outputs/recommendations.
- **Randomized response** — the survey trick where respondents randomize their answer (the drug-use example: "yes" stays yes, "no" flips to yes half the time), so aggregates are recoverable but no individual is exposed.
- **Advanced** — DP-SGD (private ML training), Secure Multi-Party Computation. Tools: Google RAPPOR, Apple local DP, diffprivlib / SmartNoise.

**In security & beyond:** protects healthcare, survey, and telemetry data against re-identification and linkage; deployed by Apple, Google, and Microsoft; supports GDPR/HIPAA compliance. Rule of thumb: k-anonymity for static releases, DP for interactive queries.

---

## Federated Learning

Train a shared model across many devices without ever centralizing the raw data — privacy and a smaller attack surface as an architectural property.

**Concepts**
- **Federated Learning (FL)** — devices train locally and share only *model updates*, never raw data; the server aggregates them into an improved global model.
- **Why it helps** — there's no central data store to breach, and the model doesn't expose raw records (contrast with centralized training, which is a single point of failure).
- **Secure-sum intuition** — the motivating example where students compute an average grade without revealing any individual's value.

**Methods**
- **FL workflow (4 steps)** — (1) the server sends the global model to devices; (2) each device trains on its local data; (3) devices send back updates; (4) the server aggregates them.
- **Complementary privacy tools** — k-anonymity (generalization/suppression/perturbation, evaluated by re-identification risk and information loss), differential privacy, and homomorphic encryption (compute on encrypted data).

**In security:** because anomalous updates can indicate a malicious participant, FL connects directly to Byzantine robustness and Krum from the adversarial lecture. Challenges: communication overhead, device heterogeneity, and limited explainability.

---

## Securing AI / Content Safety

The safety risks specific to generative AI and LLMs — and the defenses, grounding techniques, and risk-assessment process used to manage them.

**Risks**
- **Offensive content** — toxic or biased output from unfiltered training data and weak alignment.
- **Hallucination** — fluent but wrong/fabricated output. Four types: intrinsic (internal fabrication), extrinsic (conflicts with external facts), factuality (false stated as true), contextual (misuses the input).
- **Prompt injection** — direct (malicious user input overrides system instructions) and indirect (a malicious instruction hidden in external content the model later reads — email, HTML, filenames). Indirect is harder to detect.
- **Jailbreak** — coaxing the model into ignoring its safety rules.

**Defenses**
- **Grounding & RAG** — anchor outputs to verifiable sources. Retrieval-Augmented Generation pairs a retriever (vector search over a knowledge base) with the generator, adding domain knowledge without retraining and making output traceable — the primary fix for hallucination.
- **Fit for purpose** — outputs appropriate to audience, tone, and the system's role.
- **Layered safety** — content filtering and toxicity detection, system-prompt isolation/hardening, input sanitization, structured (vs free-text) prompts, adversarial training and red-teaming, pre- and post-output moderation, logging, sandboxing untrusted content, and human oversight.

**In security:** prompt injection and jailbreaks are AI-specific attack vectors causing data leakage and policy violations — especially dangerous in healthcare, law, and finance. The lecture's risk-assessment case study (a weather-forecast tool) classifies systems as **Restricted I/O** (low risk) vs **Open I/O** (high risk) and works through concrete mitigations like disabling the AI during severe-weather alerts and framing outputs as suggestions.

---

# Part 4 — Cybersecurity Domain & Operations

## Security Operations Center (SOC)

The operational heart of defense: the team and tooling that monitor, detect, and respond to incidents in real time.

**The SOC**
- A centralized team of analysts, engineers, and responders. **Tiers**: Tier 1 (alert triage), Tier 2 (deep investigation), Tier 3 (threat hunting & malware analysis), plus managers, threat-intel analysts, and incident responders.
- **Operating models** — in-house, managed (MSSP), hybrid, or virtual.
- **Maturity levels (0–4)** — from no SOC, through basic/manual and developing/some-automation, to mature/24-7 and advanced/threat-hunting.

**Tooling**
- **SIEM** (Security Information and Event Management) — real-time analysis of security alerts. Pipeline: collect logs → normalize → apply correlation rules → alert.
- **SOAR** — automates and orchestrates response workflows. SIEM detects; SOAR responds — they're complementary.
- **Data lake** — a central repository for raw structured/semi/unstructured data (schema-on-read), versus a data warehouse (structured, schema-on-write, for BI). A neglected lake degrades into a "data swamp."
- Tools: Splunk, IBM QRadar, ArcSight, LogRhythm, ELK, Microsoft Sentinel; UEBA is a key trend.

**In security:** centralized visibility, earlier detection, faster incident response, and compliance/forensics support. Log indicators worth watching: failed logins, unexpected reboots, traffic/CPU spikes, sensitive-file access, and log tampering. The perennial challenge is alert fatigue and tuning out false positives.

---

## Zero Trust

A security model that abandons the trusted-perimeter assumption: verify everything, every time.

**Concepts**
- **"Never trust, always verify"** — strict identity verification for every user and device regardless of network location; assume the perimeter is already breached.
- **Three principles** — verify explicitly; least-privilege access (just-in-time, just-enough); assume breach (segment to minimize blast radius).
- **Supporting ideas** — micro-segmentation (isolated zones), continuous authentication (context/risk-based rather than static), and new attack surfaces like IoMT (Internet of Medical Things).

**Methods & applications**
- **Graph-based Zero Trust** — model users/devices/apps/data as nodes and their relationships as edges; trust becomes edge weight, centrality (e.g. PageRank) finds influential/vulnerable nodes, and trust decays over time. Decisions run as graph queries (Cypher/Gremlin on Neo4j or AWS Neptune); anomalies surface through community detection and time-aware structural changes.
- **Healthcare** — protects EHRs and connected devices, aiding HIPAA/GDPR compliance.
- **Automotive** — cryptographic IDs per ECU, micro-segmentation (infotainment vs drive systems), V2X message authentication; standards ISO/SAE 21434 and UNECE WP.29.

**Why graphs:** they capture the multi-hop relational context needed for fine-grained, explainable, real-time access decisions — e.g. a 3 AM login from an unknown device gets flagged, challenged with MFA, and alerted.

---

## Honeypots

Deception as defense: deliberately attractive fake systems that let you observe attackers, combined with the detection tooling around them.

**Concepts**
- **Honeypot** — a fake, vulnerable-looking system with no real data; bait to observe attacker behaviour. Goals: detection, analysis, diversion, deception.
- **Interaction level** — low (emulates a few services; low risk, easy) vs high (full OS/shell; higher risk, more learning). A **honeynet** chains many honeypots to mimic a whole organization.
- **IDS vs IPS** — an IDS detects and alerts (passive, out of the traffic path); an IPS detects and blocks (active, inline). Variants: NIDS (network) vs HIDS (host), and signature- vs anomaly-based detection.

**Methods & tools**
- **Attack-analysis pipeline** — detection (IDS/IPS) → deception & logging (honeypots) → aggregation & correlation (SIEM) → threat intelligence (enrichment).
- Honeypot tools: Kippo/Cowrie (SSH/Telnet), Dionaea (malware collection), Honeyd. IDS/IPS tools: Snort, Suricata, Zeek/Bro, OSSEC.

**In security:** honeypots reveal attacker passwords, tools (Nmap, Hydra), dropped malware, and contacted IPs; combined with IDS/IPS and SIEM they expose multi-stage attacks (scan → brute-force → exploit) and cut false positives through correlation. Note the false-positive (legit flagged) vs false-negative (malicious missed) distinction, and the ethical line — a honeypot must observe, not entrap, and must never become a launchpad.

---

## Social Engineering

Attacks that target people rather than machines — and how data science helps defend against them.

**Concepts**
- **Social engineering** — manipulating human error to extract credentials, access, or clicks; "hacking people, not computers."
- **Psychological levers** — authority, urgency, reciprocity, social proof.
- **Methods** — phishing, spear phishing, vishing (voice), smishing (SMS), tailgating, baiting; plus platform-specific scams (romance/catfishing on dating sites, fake recruiters and "application fees" on job sites).
- **Digital footprint** — the data you leave online: active (intentionally posted) vs passive (cookies, IP, photo metadata).

**Data-science defenses**
- **Behavioral analysis** — detect login/device/timing deviations (account takeover).
- **NLP** — classify phishing language (urgency, info requests).
- **Anomaly detection** — Isolation Forest, One-Class SVM, autoencoders.
- **Graph analysis** — interaction graphs to spot fake accounts, bots, and coordinated campaigns.
- **Supervised learning** — Random Forests, gradient boosting, neural nets on labeled scam data.
- **User risk scoring** — combine behaviour, communication, history, and footprint into a dynamic score that triggers extra verification.

**In security:** defense is layered — technical (email filtering, sandboxing, MFA, SIEM, EDR) plus human (training, phishing simulations, reporting culture). Real systems: Gmail spam filtering, LinkedIn bot detection, PayPal risk analysis. Notable cases: Twitter (2020), Target (2013), Kevin Mitnick. ML pitfalls here are imbalanced data, the false-positive/negative balance, adversarial learning, and privacy (handled via federated learning and differential privacy).

---

## Zero-Day Attacks

The advanced-threat lecture: exploits no one has a patch for yet, plus the ML detection methods and the families of stealthy malware that accompany them.

**Concepts**
- **Zero-day** — exploiting a vulnerability unknown to the vendor ("zero" days to fix it); with no signature, it slips past traditional AV/IDS. Lifecycle: discovery → weaponization → exploitation → disclosure → patch → post-patch exploitation.
- **SCADA / ICS** — industrial control systems (sensors, PLCs, RTUs, HMI); attacks here cause *physical* damage.
- **Backdoor** — a hidden bypass of authentication (malware-installed or developer-left); lifecycle insertion → dormancy → activation → exfiltration. An **ML-model backdoor** is training-time poisoning that implants behaviour triggered by a specific input.
- **Spyware** — covert info-gathering malware. **C2 (Command and Control)** — the channel between a compromised host and the attacker for remote control and exfiltration.

**Methods**
- **ML zero-day detection** — Isolation Forest, autoencoders, and One-Class SVM (anomaly); LSTM (sequential behaviour); GNNs (user-device-action relationships); DBSCAN (new attack types); Random Forest/XGBoost (when labels exist).
- **ML-backdoor defenses** — Activation Clustering, Spectral Signatures, Neural Cleanse (reverse-engineer the trigger), STRIP (perturb input, watch output entropy), and Fine-Pruning.
- **C2 evasion (to detect)** — Domain Generation Algorithms, fast-flux DNS, abuse of legitimate cloud services, and fileless/LOLBin techniques.

**In security:** defenses are rapid patching, Zero Trust, defense-in-depth, EDR, threat hunting, and bug bounties. Landmark SCADA cases: Stuxnet (2010), BlackEnergy (2015 Ukraine grid), Triton (2017), Oldsmar (2021). ML detection's downsides are high false positives, a need for domain feedback, and vulnerability to adversarial ML.

---

## Dictionary Attacks & Password Security

A wide lecture anchored on password attacks, covering how passwords are stored, the full family of attacks against them, and adjacent privacy topics.

**Attacks**
- **Dictionary attack** — guesses from a list of common/leaked passwords; more focused than brute force.
- **Brute force** — tries every combination; slow but eventually cracks short/weak passwords.
- **Rainbow table** — precomputed hash → plaintext tables; defeated by salting.
- **Credential stuffing** — replays breached username/password pairs across sites (exploiting reuse), via botnets and proxies.
- **Phishing / URL phishing** — fake sites and links that harvest credentials.

**Defenses & storage**
- **Hash + salt** — a one-way hash maps plaintext to a fixed digest; a random salt makes each hash unique, defeating precomputation. Use strong algorithms (bcrypt, SHA-256) with key stretching.
- **Account protection** — strong/complex password policies, lockout after N failures, MFA/2FA, rate limiting, monitoring. A strong password is ≥ 12 chars, mixed character classes, unique, ideally via a password manager.
- **Cookie security** — session hijacking, XSS, MitM, CSRF, and cookie poisoning are mitigated with HTTPS and the SameSite, HttpOnly, and Secure flags.
- **Privacy tools** — VPNs (AES-256, no-logs, kill switch) and incognito mode add privacy, though incognito only stops *local* history (ISPs and sites still track).

**In security:** the flagship case is the LinkedIn 2012 breach (6.5M unsalted passwords cracked). Other cases: Reddit (2018) and Spotify (2020) credential stuffing; Google Docs (2017) phishing. The practical takeaway is matching each attack to its countermeasure — dictionary → lockout + rate-limit, rainbow → salt, credential stuffing → MFA + unique passwords, phishing → training + filtering.

---

# Capstone

## Pipeline — Putting It Together

The closing lecture assembles every technique into a single end-to-end workflow for data-science-driven security. It's presented as a scaffold to adapt per project, not a fixed recipe — which makes it the most useful single artifact for framing a project.

**The pipeline stages, in order:**

1. **Systems** — survey the file system (names, sizes, types), web info, protocols, and version control; establish data governance.
2. **Meta-data** — data size and types, missing data, special/sentinel values.
3. **Data statistics** — central tendencies, correlation/association, distributions, duplication, single/multi-value features, dimensionality reduction.
4. **Abnormality detection** — single- and multi-feature; always ask *why* a point is abnormal.
5. **Clustering** — group the data, interpret the groups, and examine points that fall outside every cluster.
6. **Segment analysis** — by feature, by time, and by domain knowledge.
7. **Further investigation** — NLP (topics, sentiment, language style) and graphs (information flow, hierarchy, network, weak points) where the data supports them.
8. **Models** — choose suitable models, judge information gained and goodness of fit, and require explainability.
9. **Reporting** — visuals, summary statistics, and the subjects that need investigation.
10. **Improving** — feed conclusions back: update firewall rules, retrain models, separate components, adopt federated learning.

**The big picture:** this is the course in one diagram — understand the data, find the abnormal, group and compare it, investigate with NLP and graphs, model it responsibly, report, and loop the findings back into the defenses. Every earlier lecture is one stage or tool inside this loop.

---

*End of overview — 27 lectures, organized as a conceptual reference and project context.*
