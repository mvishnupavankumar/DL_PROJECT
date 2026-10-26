# 00 — Manuscript Evidence Gate & Consistency Protocol

**Audit Date**: 2026-10-12  
**Lead Auditor**: Senior ML Systems Researcher & Statistical Reviewer  
**Target Document**: Pre-flight verification for [`research/paper/AEGISOPS_RESEARCH_PAPER.md`](file:///c:/DL_PROJECT/research/paper/AEGISOPS_RESEARCH_PAPER.md)  
**Primary Evidence Root**: [`research/audit_reconciliation/`](file:///c:/DL_PROJECT/research/audit_reconciliation/)

---

## 1. Executive Purpose & Gate Mandate

Before authoring the camera-ready research manuscript, every statistical claim, unit of analysis, metric denominator, and architectural assertion must pass this **Evidence Gate**. This protocol enforces strict adherence to audited empirical evidence, prohibiting ungrounded novelty claims, artificial metric inflation, or conflation of synthetic benchmarks with live production performance.

---

## 2. Ten-Point Methodological & Statistical Audit

### Point 1: Data Modalities & Sampling Semantics
- **Historical Telemetry Rows ($N = 200$)**: Sequential physical samples recorded in [`data/aegisops_live.sqlite3`](file:///c:/DL_PROJECT/data/aegisops_live.sqlite3) from `2026-10-11T07:12:16Z` to `10:15:37Z`. Contains 31 normal rows and 169 fault-labelled rows (1 latency, 168 error).
- **Historical Alert Episodes ($N = 4$)**: Temporal clusters of continuous anomalous state logged in [`research/exports/incident_episodes.csv`](file:///c:/DL_PROJECT/research/exports/incident_episodes.csv) (EP-01 and EP-02 workstation RAM excursions; EP-03 latency spike; EP-04 continuous error burst).
- **Synthetic Evaluation Windows ($N = 320$)**: Algorithmic benchmark units ($\mathbf{X} \in \mathbb{R}^{24 \times 5}$) synthesized via mathematical sine baselines and deterministic fault ramps in [`research/raw/detection_predictions.csv`](file:///c:/DL_PROJECT/research/raw/detection_predictions.csv) (200 normal windows, 120 fault episodes across 6 scenarios).
- **Gate Verdict**: **STRICTLY SEPARATED**. Manuscript text must never describe synthetic windows as "production incident tickets" or conflate historical database cold-start logging with neural model evaluation.

### Point 2: Exact Experimental Units of Analysis
- **Experiment A (Detection Recall)**: The **fault episode window** ($N = 120$).
- **Experiment A (Normal False Alarms)**: The **steady-state sequence window** ($N = 200$).
- **Experiment B (Diagnosis Accuracy)**: The **architectural failure scenario** ($N = 6$).
- **Experiment C (Safety Containment)**: The **adversarial boundary trial** ($N = 11$).
- **Gate Verdict**: **STANDARDIZED**. All denominators in tables, text, and statistical tests cite these exact experimental units.

### Point 3: Independence and Clustering Qualification
- **Experiment A**: Replicates were synthesized using explicitly disjoint seeds: normal windows used `seed=2026`; the 120 incident windows used unique scenario-replicate seeds `3001` through `3120`. These seeds establish separate random realizations, but they do not establish 120 independent production incidents: the fault windows remain clustered within six canonical scenario archetypes (20 replicates each) that share generation logic and fault dynamics.
- **Experiment B**: Evaluates 6 distinct architectural failure scenarios (INC-1001 to INC-1006). Repeated evaluations of the same 6 scenarios across 7 configurations ($7 \times 6 = 42$) must be treated as paired repeated-measures, not 42 independent trials.
- **Experiment C**: Evaluates discrete requests against clean, isolated SQLite fixtures and a fresh local microservice thread.
- **Gate Verdict**: **QUALIFIED**. Pseudoreplication across time-series strides or repeated scenario scoring is excluded, but window-level results remain descriptive because incident replicates are clustered by archetype.

### Point 4: Sensitivity-Difference Interval for Paired Predictions
- In Experiment A, the LSTM Autoencoder and Isolation Forest were evaluated on the **identical 120 fault episodes**. Observations are paired.
- Discordant pairs: $b = 63$ (LSTM detected, IsoForest missed), $c = 0$ (IsoForest detected, LSTM missed).
- Paired difference in sensitivity:
  $$\Delta = \frac{b - c}{N} = \frac{63 - 0}{120} = \mathbf{+0.5250}$$
- **Wald Paired Difference 95% CI**:
  $$\text{SE}(\Delta) = \frac{\sqrt{(b + c) - \frac{(b - c)^2}{N}}}{N} = \frac{\sqrt{63 - \frac{63^2}{120}}}{120} = \frac{\sqrt{63 - 33.075}}{120} = \frac{\sqrt{29.925}}{120} \approx 0.04558$$
  $$\text{CI}_{95\%} = 0.5250 \pm 1.96 \times 0.04558 = \mathbf{[+0.4357, +0.6143]}$$
- **Exact McNemar p-value**: $p = 2 \times (0.5)^{63} = \mathbf{2.168 \times 10^{-19}}$ ($p < 0.001$).
- **Gate Verdict**: **QUALIFIED DESCRIPTIVE**. The exact binomial p-value and paired Wald interval describe paired synthetic-window outcomes under independent-window assumptions; neither is cluster-robust nor population-generalizable across production incidents.

### Point 5: Validity of Precision-Recall AUC (PR-AUC)
- **LSTM Autoencoder**: Uses continuous reconstruction-error scores. Applying the runner's documented `precision_recall_curve` plus trapezoidal `auc(recall, precision)` method to the current raw rows yields PR-AUC = **1.0000**; average precision is a distinct statistic. The prior 0.9998 value is not reproducible from the current score table.
- **Isolation Forest**: Uses continuous inverted decision-function scores. Trapezoidal PR-AUC = **0.9056**.
- **Operational Rules (Static)**: Continuous score is unavailable (discrete Boolean threshold), so PR-AUC is **UNAVAILABLE** in the comparative manuscript table. The historical runner mechanically emitted binary-score values; they are not comparable continuous rankings.
- **Combined Detector**: Hybrid discrete/continuous gate. PR-AUC is reported as **N/A** because a monotonic continuous scoring function does not exist.
- **Gate Verdict**: **VERIFIED**. No invalid continuous ranking claims are asserted for discrete rule combinations.

### Point 6: Operational False Alarms per Hour
- The former arithmetic projection $\text{FPR} \times (3600 / 5)$ and its 7.2/14.4 labels are superseded historical calculations, not current results.
- **Gate Verdict**: **UNAVAILABLE**. Non-overlapping synthetic batch windows do not measure continuous streaming alarm rate or alert deduplication. Active manuscript tables and figures must report only window-level FPR and mark operational false alarms per hour `UNAVAILABLE`.

### Point 7: Combined Detector Empirical Benefit Disclosure
- On the synthetic benchmark, the Combined Detector achieves identical classification counts to the standalone LSTM Autoencoder (120 TP, 2 FP, 198 TN, 0 FN).
- **Gate Verdict**: **QUALIFIED DISCLOSURE REQUIRED**. The manuscript must openly acknowledge that on this specific benchmark, the combined detector provides zero additive statistical sensitivity over the standalone LSTM. Its justification is architectural (guaranteeing deterministic zero-latency tripping on hard threshold excursions while providing deep temporal drift detection).

### Point 8: Power Analysis & Sample Size Constraints
- Diagnostic cohort: $N = 6$ ground-truth scenarios.
- Statistical power for $\Delta = 20\%$ at $\alpha = 0.05$: **$1 - \beta \approx 0.14$**.
- **Gate Verdict**: **BOUNDED**. Experiment B must be reported strictly as an exploratory pilot feasibility benchmark. Comparative asymptotic superiority claims between agent architectures are prohibited.

### Point 9: Accounting for Failed and Omitted API Calls
- Ground-truth catalog contains 6 scenarios.
- In raw LLM trials, Config 5 omitted INC-1002 (timeout) and Config 7 omitted INC-1004 (rate limit).
- **Gate Verdict**: **INTENT-TO-TREAT (ITT) MANDATORY**. All tables must report both Full-Cohort Intent-to-Treat ($N=6$, omitted cases scored 0) and Completed-Case Per-Protocol ($N=5$) metrics. Multi-Agent Full achieved 83.3% ITT ($5/6$) vs. Multi-Agent No-DL 66.7% ITT ($4/6$).

### Point 10: Local Application Execution Boundary
- All Experiment C safety tests were executed against `http://127.0.0.1:8765` using atomic SQLite locking (`BEGIN IMMEDIATE`) on disposable test fixtures.
- **Gate Verdict**: **CONFINED**. The manuscript must state that safety guarantees apply within the AegisOps application execution harness on loopback interfaces, not as distributed Byzantine consensus across multi-tenant enterprise clusters.

---

## 3. Evidence Gate Sign-Off

All ten consistency dimensions have been verified against raw machine-readable records. Drafting of [`research/paper/AEGISOPS_RESEARCH_PAPER.md`](file:///c:/DL_PROJECT/research/paper/AEGISOPS_RESEARCH_PAPER.md) is cleared to proceed.
