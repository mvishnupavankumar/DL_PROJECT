# AegisOps — Rule Baseline Finalization and Discrepancy Resolution Report

**Audit Path**: `research/audits/rule_baseline_finalization_20261012/DETECTION_DISCREPANCIES.md`  
**Audit Date**: 2026-10-12  
**Target Git Commit**: `e7b8d58c67c514d7a86c67efd1bfbf29f95d85d7`  
**Auditor**: Senior ML Experiment Auditor & Software Testing Specialist  
**Status**: All Rule Baseline Definitions Finalized, Reconciled, and Verified  

---

## 1. Final Definition of the Three Rule Baselines

To eliminate all ambiguity across previous audit notes, research reports, and manuscript drafts, we establish and verify three distinct operational rule baselines evaluated on identical $N = 320$ sequence windows ($N_{\text{norm}} = 200, N_{\text{fault}} = 120$ across 6 failure modes):

| Baseline Name | Formal Operational Definition | Features Evaluated | Evaluated Thresholds |
| :--- | :--- | :--- | :--- |
| **Narrow Rules** | Minimal threshold checks monitoring primary host degradation | Latency, Memory | $\text{latency\_ms} \ge 1000 \lor \text{memory\_pct} \ge 95.0$ |
| **Resource-Only Rules** | Full physical host and probe resource saturation | Latency, Memory, CPU, Disk | $\text{latency\_ms} \ge 1000 \lor \text{memory\_pct} \ge 95.0 \lor \text{cpu\_pct} \ge 90.0 \lor \text{disk\_pct} \ge 95.0$ |
| **Full Operational Rules** | Complete runtime operational guardrails (physical + HTTP status) | Latency, Memory, CPU, Disk, Error Rate | $\text{Resource-Only} \lor \text{error\_rate\_pct} > 0.5$ |

---

## 2. Resolution of the 40/120 vs. 80/120 Discrepancy

### The Root Cause of Prior Narrative Friction
Across prior audit notes, conflicting descriptions emerged: some texts cited **40/120 TP (33.3% recall)** while others cited **80/120 TP (66.7% recall)**. Our audit of `dl/anomaly_detector.py:generate_incident_telemetry` and `research/experiments/run_experiment_a.py` reveals the exact mathematical origin:

1. **Narrow Rules ($40 / 120$ TP, 33.33% Recall)**:
   - Evaluates only `latency >= 1000` and `memory >= 95`.
   - In `dl/anomaly_detector.py`:
     - `INC-1001` (Payment API): Max latency is 760 ms ($< 1000$ ms), memory is normal $\to$ **0/20 detected (MISSED)**.
     - `INC-1002` (Customer DB): Max latency reaches 1250 ms ($\ge 1000$ ms) $\to$ **20/20 detected (CAUGHT)**.
     - `INC-1003` (CPU Saturation): Max latency is 380 ms ($< 1000$ ms), memory is 91% ($< 95\%$) $\to$ **0/20 detected (MISSED)**.
     - `INC-1004` (Disk Capacity): Max latency is 260 ms ($< 1000$ ms), memory is normal $\to$ **0/20 detected (MISSED)**.
     - `INC-1005` (Auth Failures): Max latency is 280 ms ($< 1000$ ms), memory is normal $\to$ **0/20 detected (MISSED)**.
     - `INC-1006` (Internal API): Max latency reaches 1150 ms ($\ge 1000$ ms) $\to$ **20/20 detected (CAUGHT)**.
   - **Total Caught**: $20 + 20 = \mathbf{40 / 120}$ ($\text{FN} = 80$).
   - *Verdict*: 40/120 is the exact empirical result for **Narrow Rules**. Conflating this narrow subset with "resource-only" caused the first discrepancy.

2. **Resource-Only Rules ($80 / 120$ TP, 66.67% Recall)**:
   - Evaluates all physical resources: `latency >= 1000`, `memory >= 95`, `cpu >= 90`, and `disk >= 95`.
   - In addition to INC-1002 and INC-1006:
     - `INC-1003` (CPU Saturation): CPU ramps to 99% ($\ge 90\%$) $\to$ **20/20 detected (CAUGHT)**.
     - `INC-1004` (Disk Capacity): Disk ramps to 99.5% ($\ge 95\%$) $\to$ **20/20 detected (CAUGHT)**.
     - `INC-1001` and `INC-1005` still lack physical resource saturation $\to$ **0/20 detected (MISSED)**.
   - **Total Caught**: $20 + 20 + 20 + 20 = \mathbf{80 / 120}$ ($\text{FN} = 40$).
   - *Verdict*: 80/120 is the exact empirical result for **Resource-Only Rules**.

3. **Full Operational Rules ($120 / 120$ TP, 100.0% Recall)**:
   - Adds `error_rate_pct > 0.5%`.
   - In our synthetic test harness, all 6 scenarios elevate the probe error rate above 0.5% (between 14% and 55%).
   - **Total Caught**: $\mathbf{120 / 120}$ ($\text{FN} = 0$).
   - *Verdict*: 120/120 is the exact empirical result for **Full Operational Rules**, which is what `run_experiment_a.py` implemented and what was plotted in `detection_confusion_matrices.png`.

---

## 3. Comparative Metric Synthesis Table

All metrics independently recomputed over the exact 320 evaluation windows:

| Method | TP | FP | TN | FN | Precision (95% CI) | Recall (95% CI) | F1-Score | Spec | FPR | FA/hr |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Narrow Rules** | 40 | 0 | 200 | 80 | 1.0000 [0.912, 1.000] | 0.3333 [0.254, 0.424] | 0.5000 | 1.0000 | 0.0% | 0.0 |
| **Resource-Only Rules** | 80 | 0 | 200 | 40 | 1.0000 [0.954, 1.000] | 0.6667 [0.578, 0.745] | 0.8000 | 1.0000 | 0.0% | 0.0 |
| **Full Operational Rules**| 120 | 0 | 200 | 0 | 1.0000 [0.969, 1.000] | 1.0000 [0.969, 1.000] | 1.0000 | 1.0000 | 0.0% | 0.0 |
| **Isolation Forest** | 57 | 4 | 196 | 63 | 0.9344 [0.843, 0.974] | 0.4750 [0.388, 0.564] | 0.6298 | 0.9800 | 2.0% | 14.4 |
| **LSTM Autoencoder** | 120 | 2 | 198 | 0 | 0.9836 [0.942, 0.996] | 1.0000 [0.969, 1.000] | 0.9917 | 0.9900 | 1.0% | 7.2 |
| **Combined Alert** | 120 | 2 | 198 | 0 | 0.9836 [0.942, 0.996] | 1.0000 [0.969, 1.000] | 0.9917 | 0.9900 | 1.0% | 7.2 |

---

## 4. Paired Hypothesis Testing Matrix (vs. Isolation Forest and LSTM)

- **Paired Comparisons against Isolation Forest ($N_{\text{fault}} = 120, \text{TP}_{\text{IF}} = 57$)**:
  - *Narrow Rules vs. IsoForest*: $a=9, b=31, c=48, d=32 \implies p = 0.0712, \Delta = -0.1417$ (Isolation Forest outperforms Narrow Rules, though difference does not reach $\alpha = 0.05$).
  - *Resource-Only Rules vs. IsoForest*: $a=41, b=39, c=16, d=24 \implies p = 0.0027, \Delta = +0.1917$ (Resource-Only Rules significantly outperforms Isolation Forest, $p < 0.01$).
  - *Full Operational Rules vs. IsoForest*: $a=57, b=63, c=0, d=0 \implies p = 2.17 \times 10^{-19}, \Delta = +0.5250$.
- **Paired Comparisons of LSTM Autoencoder against Rule Baselines**:
  - *LSTM vs. Narrow Rules*: $a=40, b=80, c=0, d=0 \implies p = 1.65 \times 10^{-24}, \Delta = +0.6667$.
  - *LSTM vs. Resource-Only Rules*: $a=80, b=40, c=0, d=0 \implies p = 1.82 \times 10^{-12}, \Delta = +0.3333$.
  - *LSTM vs. Full Operational Rules*: $a=120, b=0, c=0, d=0 \implies p = 1.0000, \Delta = +0.0000$.

---

## 5. Combined Detector Analysis & Benchmark Redundancy

- **Alert Logic**:
  $$\text{Combined Alert} = \text{Rule Alert} \lor \text{LSTM Anomaly}$$
- **Verification on Benchmark ($N = 320$)**:
  - Across all 320 windows, `combined_flag == (rule_flag | lstm_flag)` holds with **0 mismatches**.
  - On normal windows ($N = 200$), rules trigger 0 alarms, while LSTM triggers 2. Combined alert inherits 2 false alarms ($\text{FP} = 2, \text{FPR} = 1.0\%$).
  - On fault windows ($N = 120$), LSTM triggers on all 120 windows ($\text{TP} = 120$). Because LSTM sensitivity is already 100.0%, adding rule alerts adds 0 true positives.
- **Scientific Conclusion**:
  On this synthetic benchmark, the Combined Detector provides **zero additive sensitivity** over the stand-alone LSTM Autoencoder. Its inclusion is justified strictly on architectural grounds (defense-in-depth against model drift and sub-millisecond fast-path triage), not empirical benchmark advantage.

---

## 6. Closing the Figure Reproducibility Deficit

- **Implemented Solution**:
  Created `research/experiments/plot_detection_figures.py`, a dedicated Pillow-based visualization engine that loads `research/results/detection_predictions.csv` and renders:
  1. `research/figures/detection_confusion_matrices.png` (1000x750)
  2. `research/figures/detection_comparison.png` (950x550)
  and synchronizes them to `research/paper/figures/`.
- **Integration**:
  Wired into Step 2 of `research/run_all.py`. Both figures now regenerate automatically during pipeline execution, matching all recorded metrics.
