# AegisOps — Phase 3 Anomaly Detection Evidence Verification Report

**Audit Path**: `research/audits/detection_figure_verification_20261012/DETECTION_FIGURE_VERIFICATION.md`  
**Audit Date**: 2026-10-12  
**Target Git Commit**: `e7b8d58c67c514d7a86c67efd1bfbf29f95d85d7` (Branch: `main`)  
**Auditor**: Senior ML Experiment Auditor, Python Research Engineer, Statistical Reviewer  
**Audited Artifacts**:
- `research/experiments/run_experiment_a.py`
- `research/results/detection_predictions.csv` & `research/raw/detection_predictions.csv`
- `research/results/detection_metrics.csv` & `research/raw/detection_metrics.csv`
- `research/results/detection_by_scenario.csv`
- `research/figures/detection_confusion_matrices.png`
- `research/figures/detection_comparison.png`
- `research/figures/FIGURE_CAPTIONS.md`
- `live_monitoring.py`
- `dl/anomaly_detector.py`

---

## 1. Executive Summary & Verification Verdict

We have completed an independent verification of the anomaly detection evaluation artifacts, comparing the two supplied figure image assets against raw prediction records, statistical tests, and underlying source code.

### Core Verification Findings:
1. **Raw Predictions Integrity**: Both `research/results/detection_predictions.csv` and `research/raw/detection_predictions.csv` are bitwise identical ($24,357$ bytes, SHA-256: `95585a085d7db31a9862fe46d46927da8e8c148286a1170942c7e42d765a04e5`). They contain exactly $N = 320$ rows with 320 unique sample IDs (200 normal, 120 fault).
2. **Figure Consistency with Raw Predictions**: Both supplied PNG figures (`detection_confusion_matrices.png` and `detection_comparison.png`) **accurately depict the metrics stored in `detection_metrics.csv` and computed by `run_experiment_a.py`**.
3. **The 120/120 vs. 40/120 True Positive Divergence**: The figures depict Operational Rules as achieving $120/120$ TP (100.0% recall) because `run_experiment_a.py` included the HTTP probe error rate condition (`err > 0.5%`). The earlier narrative report of $40/120$ TP (33.3% recall) was based on evaluating strict resource-only physical thresholds (`latency >= 1000`, `memory >= 95`).
4. **Figure Caption Contradiction**: `research/figures/FIGURE_CAPTIONS.md` erroneously claims Figure 1 shows "40/120 TP, 33.3% recall", directly contradicting the physical graphic which shows "TP 120, FN 0, Rec: 1.000".
5. **Figure Code Reproducibility**: The two PNG figures are static binary files. The code to generate them was omitted from `run_experiment_a.py` and `run_all.py` (which only contains an unused PIL import).
6. **Combined Detector Redundancy**: The Combined Detector matches the LSTM Autoencoder identically on all 320 windows ($120$ TP, $2$ FP, F1 $= 0.9917$). Combining rules with the neural model provided zero additional sensitivity on this synthetic benchmark.

---

## 2. Check 1: Exact Dataset Counts, Unique IDs, and Class Balance

Inspected `research/results/detection_predictions.csv`:

| Dimension | Count | Details & Verification Citation |
| :--- | :---: | :--- |
| **Total Rows** | 320 | Evaluated on line 140 of `run_experiment_a.py` |
| **Unique Sample IDs** | 320 | `NORM-001` to `NORM-200` ($n = 200$), and `INC-1001-REP-01` to `INC-1006-REP-20` ($n = 120$) |
| **Negative Labels (`ground_truth == 0`)** | 200 | Synthetic normal steady-state windows generated via `generate_normal_windows(200, seed=2026)` |
| **Positive Labels (`ground_truth == 1`)** | 120 | Injected incident windows generated via `generate_incident_telemetry` ($6 \times 20 = 120$) |
| **Class Balance** | 62.5% Neg / 37.5% Pos | Standard benchmark split with moderate positive representation |

---

## 3. Check 2: Independent Recomputation of Core Classification Metrics

Every metric was independently recomputed from `detection_predictions.csv` using Python 3.11:

| Detector | TP | FP | TN | FN | Precision (PPV) | Recall (Sensitivity) | Specificity (TNR) | F1-Score | FPR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Operational Rules (Implemented)** | 120 | 0 | 200 | 0 | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **0.0000** |
| **Operational Rules (Resource-Only)** | 40 | 0 | 200 | 80 | **1.0000** | **0.3333** | **1.0000** | **0.5000** | **0.0000** |
| **Isolation Forest Baseline** | 57 | 4 | 196 | 63 | **0.9344** | **0.4750** | **0.9800** | **0.6298** | **0.0200** |
| **LSTM Autoencoder (Frozen Live)** | 120 | 2 | 198 | 0 | **0.9836** | **1.0000** | **0.9900** | **0.9917** | **0.0100** |
| **Combined Alert (Rules OR LSTM)** | 120 | 2 | 198 | 0 | **0.9836** | **1.0000** | **0.9900** | **0.9917** | **0.0100** |

*Verification Citation*: Verified bitwise against `research/results/detection_metrics.csv` and `research/audits/detection_figure_verification_20261012/DETECTION_METRIC_RECALCULATION.csv`.

---

## 4. Check 3 & 4: Operational Rules Logic and The 120/120 vs. 40/120 Discrepancy

### Investigation of `run_experiment_a.py`:
In `run_experiment_a.py` (lines 84–93):
```python
def evaluate_operational_rules(window: np.ndarray) -> tuple[bool, str]:
    latest = window[-1]
    cpu, mem, lat, err, disk = latest[0], latest[1], latest[2], latest[3], latest[4]
    reasons = []
    if mem >= 95.0: reasons.append("memory_pct >= 95")
    if lat >= 1000.0: reasons.append("latency_ms >= 1000")
    if err > 0.5: reasons.append("error_rate_pct > 0.5")  # Evaluated on HTTP error rate
    if cpu >= 90.0: reasons.append("cpu_pct >= 90")
    if disk >= 95.0: reasons.append("disk_pct >= 95")
    return (len(reasons) > 0, "; ".join(reasons))
```

### Why the Screenshot Reports 120/120:
In `dl/anomaly_detector.py:generate_incident_telemetry`, all 6 incident scenarios have their error rate feature (`index 3`) elevated above 0.5% during the fault tail:
- INC-1001: Error rate reaches 28.0%
- INC-1002: Error rate reaches 55.0%
- INC-1003: Error rate reaches 14.0%
- INC-1004: Error rate reaches 20.0%
- INC-1005: Error rate reaches 24.0%
- INC-1006: Error rate reaches 16.0%

Because `err > 0.5%` was active, all 120 fault sequences triggered `evaluate_operational_rules`. Consequently, the raw CSV records 120 TP, and the screenshot `detection_confusion_matrices.png` displays 120/120 TP.

### Why an Earlier Report Described 40/120:
In an earlier exploratory phase, the rule baseline was evaluated without error rate signals, testing strictly physical resource degradation (`latency >= 1000`, `memory >= 95`). Under that definition:
- Only INC-1002 (latency 1250 ms) and INC-1006 (latency 1150 ms) exceeded the 1000 ms threshold.
- The remaining four scenarios had latencies between 260 ms and 760 ms and memory below 95%, yielding $20 + 20 = 40$ TP and 80 FN ($33.3\%$ recall).
- The author of `FIGURE_CAPTIONS.md` erroneously retained this earlier physical-rules text while committing the full-rules image.

---

## 5. Check 5: Combined Detector Logical OR Verification

We tested the condition:
$$\text{combined\_flag}_i = \text{rule\_flag}_i \lor \text{lstm\_flag}_i \quad \forall i \in \{1, \dots, 320\}$$
- **Total Rows Evaluated**: 320
- **Mismatches Observed**: **0** (100.0% perfect logical OR identity)

### Explanation of Observed Results:
In `detection_predictions.csv`:
- On normal data ($N = 200$): `rule_flag` is 0 on all 200 rows. `lstm_flag` is 1 on 2 rows (`NORM-012` and `NORM-113`). Therefore, `combined_flag` is 1 on exactly those 2 rows (inheriting 2 false positives).
- On fault data ($N = 120$): `lstm_flag` is 1 on all 120 rows. `rule_flag` is 1 on all 120 rows. Therefore, `combined_flag` is 1 on all 120 rows (inheriting 120 true positives).
- **Benchmark Redundancy**: Because the LSTM Autoencoder achieved 100.0% recall, the Combined Detector is indistinguishable from the LSTM Autoencoder on this test set. The Combined architecture is justified by operational defense-in-depth, not by additive benchmark metrics.

---

## 6. Check 6: Continuous-Score Availability and PR-AUC Validity

| Detector | Continuous Score Column | Score Nature | Computed PR-AUC | Reporting Verdict |
| :--- | :--- | :--- | :---: | :--- |
| **Operational Rules** | `rule_score` | Binary values ($0.0$ and $1.0$) | $1.0000$ (Step AUC) | **INVALID**: Misleading to report PR-AUC for binary rules. Must report **N/A**. |
| **Isolation Forest** | `iso_score` | Negative decision function ($\mathbb{R}$) | **$0.9056$** | **VALID**: Computed from 320 continuous isolation scores. |
| **LSTM Autoencoder** | `lstm_score` | Window Mean Squared Error ($\mathbb{R}_{\ge 0}$) | **$0.9998$** ($0.999757$) | **VALID**: Computed from continuous reconstruction errors. |
| **Combined Alert** | None | Discrete Boolean logic | None | **VALID N/A**: No continuous score exists. |

---

## 7. Check 7: False Positive Rates vs. Projected False Alarms per Hour

- **Empirically Observed False Alarms ($N_{\text{norm}} = 200$)**:
  - Operational Rules: $0 / 200$ ($\text{FPR} = 0.0000$, 95% Wilson CI $[0.0000, 0.0183]$)
  - LSTM Autoencoder: $2 / 200$ ($\text{FPR} = 0.0100$, 95% Wilson CI $[0.0027, 0.0357]$)
  - Isolation Forest: $4 / 200$ ($\text{FPR} = 0.0200$, 95% Wilson CI $[0.0078, 0.0504]$)
  - Combined Alert: $2 / 200$ ($\text{FPR} = 0.0100$, 95% Wilson CI $[0.0027, 0.0357]$)
- **Extrapolation Calculation**:
  With sampling interval $\Delta t = 5$ seconds, there are $3600 / 5 = 720$ intervals per hour:
  $$\text{Nominal FA/hr} = \text{FPR} \times 720$$
  - Operational Rules: $0.0 \times 720 = \mathbf{0.0}$
  - LSTM Autoencoder: $0.0100 \times 720 = \mathbf{7.2}$
  - Isolation Forest: $0.0200 \times 720 = \mathbf{14.4}$
- **Audit Requirement**:
  These figures must be presented as **projections from the static test set**, not as empirical measurements from a continuous longitudinal monitoring run.

---

## 8. Check 8: Synthetic Test Generation, Random Seeds, and Case Independence

- **Normal Data Generation**:
  `generate_normal_windows(200, seed=2026)` in `run_experiment_a.py`.
  - Independent random phase, baseline CPU/RAM/Disk, and Gaussian noise.
  - Evaluation seed `2026` is strictly disjoint from training seed `42`.
- **Fault Data Generation**:
  `generate_incident_telemetry(inc_id, seed=rep_seed)` where `rep_seed` increments from 3001 to 3120 ($n = 20$ replicates per scenario).
  - Each replicate generates an independent background base window with a distinct seed before applying the deterministic fault slope.
  - All 120 incident windows have distinct sample IDs (`INC-1001-REP-01` to `INC-1006-REP-20`).
- **Potential Dependence / Limitation**:
  While each window has independent background noise, the fault ramp functions are deterministic within each scenario class. Therefore, the 20 replicates within a class are exchangeable synthetic variations, not completely unrelated real-world outages.

---

## 9. Check 9: Paired Statistical Hypothesis Testing

Because models were evaluated on the exact same $N_{\text{fault}} = 120$ fault windows and $N_{\text{norm}} = 200$ normal windows, observations are paired.

### A. Paired Sensitivity Comparison (LSTM AE vs. Isolation Forest, $N_{\text{fault}} = 120$)
- **Contingency Counts**:
  - $a = 57$ (Both detected)
  - $b = 63$ (LSTM detected, IsoForest missed)
  - $c = 0$ (IsoForest detected, LSTM missed)
  - $d = 0$ (Both missed)
- **Exact Two-Tailed Binomial Test on Discordant Pairs ($b=63, c=0$)**:
  $$p = 2 \times (0.5)^{63} \approx 2.168 \times 10^{-19} \quad (p < 0.001)$$
- **Edwards Continuity-Corrected $\chi^2$ Statistic**:
  $$\chi^2 = \frac{(|63 - 0| - 1)^2}{63 + 0} = \frac{62^2}{63} = 61.0159 \quad (p = 5.66 \times 10^{-15})$$
- **Paired Sensitivity Difference ($\Delta$)**:
  $$\hat{\Delta} = \frac{b - c}{120} = \frac{63 - 0}{120} = +0.5250$$
  $$\text{SE}(\hat{\Delta}) = \sqrt{\frac{(b + c) - (b - c)^2 / 120}{120^2}} = \sqrt{\frac{63 - 33.075}{14400}} \approx 0.0456$$
  $$95\% \text{ Wald CI} = 0.5250 \pm 1.96 \times 0.0456 = [+0.4357, +0.6143]$$

### B. Discordant False Alarm Comparison on Normal Data ($N_{\text{norm}} = 200$)
- **Contingency Counts**:
  - Both alarmed: $0$
  - IsoForest alarmed only ($b$): $4$ (`NORM-058`, `NORM-071`, `NORM-142`, `NORM-188`)
  - LSTM alarmed only ($c$): $2$ (`NORM-012`, `NORM-113`)
  - Neither alarmed: $194$
- **Exact Two-Tailed Binomial Test ($b=4, c=2$)**:
  $$p = \text{binomtest}(4, 6, 0.5) = 0.6875$$
- **Finding**:
  On $N = 200$ normal windows, the difference in false alarms between Isolation Forest (4) and LSTM (2) is not statistically significant ($p = 0.6875 > 0.05$). This definitively identifies where the $p = 0.6875$ statistic in `statistical_analysis.md` originated.

---

## 10. Check 10: Figure Regeneration Confirmation

- **Can the figures be regenerated from `detection_predictions.csv`?**
  **YES**. The values displayed on both images match `detection_predictions.csv` and `detection_metrics.csv` with 100% numerical fidelity:
  - `detection_confusion_matrices.png`: Exactly matches the 4 confusion matrices (Top-Left: 200, 0, 0, 120; Top-Right: 196, 4, 63, 57; Bottom-Left: 198, 2, 0, 120; Bottom-Right: 198, 2, 0, 120).
  - `detection_comparison.png`: Exactly matches Precision (1.00, 0.93, 0.98, 0.98), Recall (1.00, 0.47, 1.00, 1.00), F1 (1.00, 0.63, 0.99, 0.99), and FA/hr (0.0, 14.4, 7.2, 7.2).
- **Missing Asset**: The script to render the figures from the CSV is missing from the repository. The figures must either be preserved as audited static assets or supplemented by a dedicated plotting script.
