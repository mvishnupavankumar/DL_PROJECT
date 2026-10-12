# AegisOps — Anomaly Detection Discrepancies and Evidence Conflicts

**Audit Date**: 2026-10-12  
**Audit Scope**: Anomaly Detection Experiment A, Raw Prediction Artifacts, and Publication Figures  
**Auditor**: Senior ML Experiment Auditor & Software Testing Specialist  
**Status**: Discrepancies Formally Documented, Reconciled, and Traced to Source Code  

---

## 1. Executive Summary of Discrepancies

A comprehensive inspection of `research/experiments/run_experiment_a.py`, `research/results/detection_predictions.csv`, `research/results/detection_metrics.csv`, `research/figures/FIGURE_CAPTIONS.md`, and the two binary PNG image assets (`detection_confusion_matrices.png` and `detection_comparison.png`) identified six critical discrepancies and reporting conflicts:

1. **Operational Rules Recall Inconsistency (120/120 vs. 40/120)**: The generated figures and CSVs report 100.0% recall ($120/120$ TP), while earlier narrative reports and `FIGURE_CAPTIONS.md` report 33.3% recall ($40/120$ TP).
2. **PR-AUC Metric Validity for Binary Rules**: `detection_metrics.csv` reports a PR-AUC of 1.0 for Operational Rules, which is a methodological artifact of evaluating step-function binary flags rather than continuous decision scores.
3. **False Alarms per Hour Projection vs. Measurement**: False alarms per hour (7.2 for LSTM, 14.4 for IF) were presented in narrative summaries as measured continuous monitoring rates, whereas they are mathematical linear extrapolations of single-window FPR.
4. **Caption Text vs. Image Graphic Contradiction**: `research/figures/FIGURE_CAPTIONS.md` explicitly describes Figure 1 as showing 40/120 TP (33.3% recall), while the actual image `detection_confusion_matrices.png` displays 120/120 TP (100.0% recall).
5. **Figure Generation Reproducibility Deficit**: Neither `run_experiment_a.py` nor `run_all.py` contains the code to draw or render the PNG figures. The two PNG files are static binary assets.
6. **Combined Detector Redundancy on Benchmark**: The Combined Detector's prediction vector is identical to the LSTM Autoencoder's prediction vector across all 320 evaluation windows, meaning the benchmark provides zero empirical evidence of additive sensitivity.

---

## 2. Discrepancy Details and Root-Cause Analysis

### Discrepancy 1: Operational Rules 120/120 TP vs. 40/120 TP

- **Conflicting Claims**:
  - `detection_metrics.csv` & `detection_predictions.csv`: Operational Rules $\text{TP} = 120, \text{FN} = 0, \text{Recall} = 100.0\%$.
  - `detection_confusion_matrices.png` (Top-Left quadrant): $\text{TP} = 120, \text{FN} = 0, \text{Recall} = 1.000$.
  - `detection_comparison.png` (Operational Rules bar): $\text{Recall} = 1.00, \text{F1} = 1.00$.
  - Earlier Audit Reports (`FINAL_EXPERIMENT_REPORT.md` line 77, `FIGURE_CAPTIONS.md` line 14): Operational Rules $\text{TP} = 40, \text{FN} = 80, \text{Recall} = 33.33\%$.
- **Source Code Investigation**:
  In `research/experiments/run_experiment_a.py` (lines 84–93):
  ```python
  def evaluate_operational_rules(window: np.ndarray) -> tuple[bool, str]:
      latest = window[-1]
      cpu, mem, lat, err, disk = latest[0], latest[1], latest[2], latest[3], latest[4]
      reasons = []
      if mem >= 95.0: reasons.append("memory_pct >= 95")
      if lat >= 1000.0: reasons.append("latency_ms >= 1000")
      if err > 0.5: reasons.append("error_rate_pct > 0.5")   # <-- KEY CONDITION
      if cpu >= 90.0: reasons.append("cpu_pct >= 90")
      if disk >= 95.0: reasons.append("disk_pct >= 95")
      return (len(reasons) > 0, "; ".join(reasons))
  ```
- **Root Cause**:
  In `dl/anomaly_detector.py` (lines 73–102), every synthetic incident injection modifies the error rate feature (`window[-tail:, 3]`) such that at step 23, `err > 0.5%` is true for 100% of incident windows:
  - INC-1001: Error rate reaches 28.0% ($> 0.5\%$)
  - INC-1002: Error rate reaches 55.0% ($> 0.5\%$)
  - INC-1003: Error rate reaches 14.0% ($> 0.5\%$)
  - INC-1004: Error rate reaches 20.0% ($> 0.5\%$)
  - INC-1005: Error rate reaches 24.0% ($> 0.5\%$)
  - INC-1006: Error rate reaches 16.0% ($> 0.5\%$)
  Because `err > 0.5%` was included in `evaluate_operational_rules`, the rules caught all 120 incidents ($100.0\%$ recall).
- **Origin of 40/120 TP (33.3%)**:
  If the HTTP probe error rate condition is removed and thresholds are applied strictly to host/service physical resources (`latency >= 1000`, `cpu >= 90`, `mem >= 95`, `disk >= 95`):
  - INC-1001 (Lat 760 ms, CPU 43%, RAM 53%, Disk 49%): **MISSED** (0/20)
  - INC-1002 (Lat 1250 ms $\ge 1000$ ms): **FLAGGED** (20/20)
  - INC-1003 (Lat 380 ms, CPU 99% $\ge 90\%$): **FLAGGED** (20/20)
  - INC-1004 (Lat 260 ms, Disk 99.5% $\ge 95\%$): **FLAGGED** (20/20)
  - INC-1005 (Lat 280 ms, CPU 40%, RAM 54%, Disk 49%): **MISSED** (0/20)
  - INC-1006 (Lat 1150 ms $\ge 1000$ ms): **FLAGGED** (20/20)
  *Note on historical 40 TP vs. 80 TP*: An earlier preliminary script tested only `latency >= 1000` and `memory >= 95` (which flagged only INC-1002 and INC-1006, yielding $20 + 20 = 40$ TP, 33.3% recall). When CPU $\ge 90\%$ and Disk $\ge 95\%$ are added, resource rules catch 80 TP (66.7%). When HTTP `err > 0.5%` is added, it catches 120 TP (100.0%).
- **Audit Verdict**:
  Both numbers represent legitimate algorithmic definitions, but conflating them without explicit qualifying labels caused severe narrative confusion. The research paper must explicitly define both variants.

---

### Discrepancy 2: PR-AUC Reporting on Binary Predictions

- **Conflicting Records**:
  `detection_metrics.csv` line 2 reports `pr_auc = 1.0` for Operational Rules.
- **Root Cause**:
  In `run_experiment_a.py` (lines 109, 131):
  ```python
  "rule_score": float(rule_flag)
  ```
  `rule_score` takes only two discrete values ($0.0$ and $1.0$). When passed to `sklearn.metrics.precision_recall_curve`, it evaluates thresholds at $\infty, 1.0, 0.0$. Because all 120 positive cases have `rule_score = 1.0` and all 200 normal cases have `rule_score = 0.0`, precision is $1.0$ at recall $1.0$, producing an artificial trapezoidal AUC of $1.0000$.
- **Audit Verdict**:
  PR-AUC is mathematically defined for continuous probability scores or rank-order decision functions. Reporting PR-AUC for binary rule flags is misleading. In the revised tables, Operational Rules PR-AUC must be marked **`N/A`**.

---

### Discrepancy 3: Projected vs. Measured False Alarms per Hour

- **Conflicting Narrative**:
  Prior narrative reports stated: "The system exhibited 7.2 false alarms per hour during continuous live monitoring."
- **Empirical Reality**:
  - The evaluation dataset contains exactly $N_{\text{norm}} = 200$ static sequence windows generated with `seed=2026`.
  - The LSTM Autoencoder misclassified exactly $2$ normal windows ($\text{FP} = 2, \text{TN} = 198$).
  - Single-window False Positive Rate: $\text{FPR} = 2 / 200 = 0.0100$ ($1.0\%$).
  - Telemetry sampling interval is $\Delta t = 5$ seconds, yielding $3600 / 5 = 720$ windows per hour.
  - Linear extrapolation: $0.0100 \times 720 = 7.20$ false alarms/hour.
- **Audit Verdict**:
  $7.2$ false alarms/hour is a **nominal linear projection**, not an empirically measured monitoring count. It must be explicitly labeled as a projection based on the 1.0% single-window error rate.

---

### Discrepancy 4: `FIGURE_CAPTIONS.md` Inconsistency with PNG Figures

- **Conflict**:
  `research/figures/FIGURE_CAPTIONS.md` line 14:
  > "- **Top Left**: Operational Rules Baseline. Exhibits zero false alarms on steady-state normal data (200/200 TN), but misses gradual and compound degradation faults (40/120 TP, 33.3% recall)."
  However, `detection_confusion_matrices.png` (Top Left quadrant) physically renders:
  > "Operational Rules: Prec: 1.000 | Rec: 1.000 | F1: 1.000"
  > "Act Normal: TN 200, FP 0 | Act Incident: FN 0, TP 120"
- **Root Cause**:
  The author of `FIGURE_CAPTIONS.md` wrote the text intending to explain why static rules are insufficient in theory (using the 40/120 resource-only concept), but the figure was rendered directly from `detection_metrics.csv` where `run_experiment_a.py` had evaluated full rules (120/120 TP).
- **Audit Verdict**:
  The caption in `FIGURE_CAPTIONS.md` was objectively false with respect to the image it claimed to describe. The updated caption and manuscript text must accurately describe the image while documenting the dual definition.

---

### Discrepancy 5: Reproducibility Deficit for PNG Figures

- **Conflict**:
  `research/run_all.py` claims to reproduce all experimental outputs.
- **Inspection**:
  - `run_all.py` calls `run_experiment_a.py`, `evaluate_diagnosis_rubric.py`, `run_experiment_c.py`, and `update_manifest.py`.
  - `run_experiment_a.py` computes metrics and saves CSVs, but **contains zero PIL drawing code**.
  - Lines 12 of `run_experiment_a.py` has an unused import: `from PIL import Image, ImageDraw`.
  - Running `run_all.py` does not regenerate `detection_confusion_matrices.png` or `detection_comparison.png`.
- **Audit Verdict**:
  The figures are static binary assets. Their plotted values match `detection_metrics.csv`, but the rendering code is absent from the execution pipeline.

---

### Discrepancy 6: Combined Alert Benchmark Redundancy

- **Conflict**:
  Early project claims suggested that the Combined Detector provided enhanced sensitivity over the stand-alone LSTM Autoencoder.
- **Inspection of `detection_predictions.csv`**:
  - For all 320 rows, `combined_flag == lstm_flag`.
  - Number of rows where `combined_flag != lstm_flag`: **0**.
  - Number of rows where `rule_flag == 1` and `lstm_flag == 0`: **0**.
- **Audit Verdict**:
  Because the LSTM Autoencoder achieved 100.0% recall ($120/120$) on this benchmark, adding rule alerts could not increase true positives. Because the rules had 0 false positives on normal data, adding them did not increase false alarms. Thus, the Combined Detector is mathematically identical to the LSTM Autoencoder on this specific benchmark. Its justification is architectural (defense-in-depth and zero-latency fast-path), not benchmark performance gain.
