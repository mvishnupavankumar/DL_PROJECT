# AegisOps: Anomaly Detection Evidence Reconciliation (Task 2)

**Audit Date**: 2026-10-12  
**Auditor**: Senior ML Researcher & Experiment Audit Lead  
**Scope**: Full statistical, methodological, and algorithmic reconciliation of Experiment A (Anomaly Detection).  
**Primary Files Inspected**:
- [`research/raw/detection_predictions.csv`](file:///c:/DL_PROJECT/research/raw/detection_predictions.csv)
- [`research/raw/detection_metrics.csv`](file:///c:/DL_PROJECT/research/raw/detection_metrics.csv)
- [`research/experiments/run_experiment_a.py`](file:///c:/DL_PROJECT/research/experiments/run_experiment_a.py)
- [`research/figures/FIGURE_CAPTIONS.md`](file:///c:/DL_PROJECT/research/figures/FIGURE_CAPTIONS.md)
- [`research/STATISTICAL_AUDIT.md`](file:///c:/DL_PROJECT/research/STATISTICAL_AUDIT.md)
- [`research/FINAL_EXPERIMENT_REPORT.md`](file:///c:/DL_PROJECT/research/FINAL_EXPERIMENT_REPORT.md)

---

## 1. Metric and Confusion Matrix Regeneration from Raw Predictions

All metrics were regenerated directly from [`research/raw/detection_predictions.csv`](file:///c:/DL_PROJECT/research/raw/detection_predictions.csv) ($N = 320$ test windows: 200 normal steady-state windows + 120 injected fault windows across 6 architectural scenarios, 20 replicates each).

### Empirical 2x2 Contingency Tables

#### A. Operational Rules Baseline (`rule_flag`)
```
                   Actual Normal (0)    Actual Fault (1)
Pred Normal (0)          200 (TN)              0 (FN)
Pred Anomaly (1)           0 (FP)            120 (TP)
```
- **Observed Counts**: $\text{TP} = 120$, $\text{FP} = 0$, $\text{TN} = 200$, $\text{FN} = 0$
- **Precision**: $\frac{120}{120 + 0} = 1.0000$ (95% Wilson CI: $[0.9690, 1.0000]$)
- **Recall**: $\frac{120}{120 + 0} = 1.0000$ (95% Wilson CI: $[0.9690, 1.0000]$)
- **F1-Score**: $1.0000$
- **False Alarm Rate**: $0.0\%$ ($0.0$ false alarms/hour)

#### B. Isolation Forest Baseline (`iso_flag`)
```
                   Actual Normal (0)    Actual Fault (1)
Pred Normal (0)          196 (TN)             63 (FN)
Pred Anomaly (1)           4 (FP)             57 (TP)
```
- **Observed Counts**: $\text{TP} = 57$, $\text{FP} = 4$, $\text{TN} = 196$, $\text{FN} = 63$
- **Precision**: $\frac{57}{57 + 4} = 0.9344$ (95% Wilson CI: $[0.8432, 0.9742]$)
- **Recall**: $\frac{57}{57 + 63} = 0.4750$ (95% Wilson CI: $[0.3878, 0.5637]$)
- **F1-Score**: $0.6298$
- **PR-AUC**: $0.9056$
- **False Alarm Rate**: $\frac{4}{200} = 2.0\%$ ($14.4$ false alarms/hour)

#### C. LSTM Autoencoder (`lstm_flag`, Frozen Checkpoint)
```
                   Actual Normal (0)    Actual Fault (1)
Pred Normal (0)          198 (TN)              0 (FN)
Pred Anomaly (1)           2 (FP)            120 (TP)
```
- **Observed Counts**: $\text{TP} = 120$, $\text{FP} = 2$, $\text{TN} = 198$, $\text{FN} = 0$
- **Precision**: $\frac{120}{120 + 2} = 0.9836$ (95% Wilson CI: $[0.9422, 0.9955]$)
- **Recall**: $\frac{120}{120 + 0} = 1.0000$ (95% Wilson CI: $[0.9690, 1.0000]$)
- **F1-Score**: $0.9917$
- **PR-AUC**: $0.9998$
- **False Alarm Rate**: $\frac{2}{200} = 1.0\%$ ($7.2$ false alarms/hour)

#### D. Combined Dual-Gate Alert (`combined_flag` = `rule_flag` OR `lstm_flag`)
```
                   Actual Normal (0)    Actual Fault (1)
Pred Normal (0)          198 (TN)              0 (FN)
Pred Anomaly (1)           2 (FP)            120 (TP)
```
- **Observed Counts**: $\text{TP} = 120$, $\text{FP} = 2$, $\text{TN} = 198$, $\text{FN} = 0$
- **Precision**: $0.9836$ (95% Wilson CI: $[0.9422, 0.9955]$)
- **Recall**: $1.0000$ (95% Wilson CI: $[0.9690, 1.0000]$)
- **F1-Score**: $0.9917$
- **PR-AUC**: Undefined (hybrid discrete/continuous decision function)
- **False Alarm Rate**: $1.0\%$ ($7.2$ false alarms/hour)

---

## 2. Investigation of the Operational Rules Discrepancy

### The Discrepancy Identified
In prior documentation ([`FINAL_EXPERIMENT_REPORT.md`](file:///c:/DL_PROJECT/research/FINAL_EXPERIMENT_REPORT.md) Table line 69 and [`FIGURE_CAPTIONS.md`](file:///c:/DL_PROJECT/research/figures/FIGURE_CAPTIONS.md) line 14), Operational Rules was reported as:
$$\text{TP} = 40, \quad \text{FN} = 80, \quad \text{Recall} = 33.33\%, \quad \text{Precision} = 100.0\%, \quad \text{F1} = 0.5000$$
Whereas in [`research/raw/detection_predictions.csv`](file:///c:/DL_PROJECT/research/raw/detection_predictions.csv) and [`research/raw/detection_metrics.csv`](file:///c:/DL_PROJECT/research/raw/detection_metrics.csv), Operational Rules achieves:
$$\text{TP} = 120, \quad \text{FN} = 0, \quad \text{Recall} = 100.0\%, \quad \text{Precision} = 100.0\%, \quad \text{F1} = 1.0000$$

### Technical Root Cause
The discrepancy stems from two different definitions of the operational rule baseline in the experiment code:

1. **Strict Static Metric Gate (The Historical/Reported Definition)**:
   In the conceptual design of AegisOps, operational rules detect threshold excursions on physical system resources:
   - $\text{latency} \ge 1000\,\text{ms}$
   - $\text{cpu} \ge 90\%$
   - $\text{memory} \ge 95\%$
   - $\text{disk} \ge 95\%$
   Under this strict physical threshold definition:
   - Only scenarios with catastrophic latency excursions (INC-1002 with latency 1250ms, and INC-1006 with latency 1150ms) exceed the 1000ms threshold.
   - Each scenario has 20 replicates: $20 + 20 = 40$ True Positives.
   - The remaining 4 scenarios (INC-1001, INC-1003, INC-1004, INC-1005) have latencies between 260ms and 760ms (well below 1000ms), and CPU/RAM/Disk metrics below 95% in their initial stages, resulting in 80 False Negatives ($40/120 = 33.33\%$ recall).

2. **Permissive Error-Rate Gate (The Implemented Script Definition in `run_experiment_a.py`)**:
   In [`research/experiments/run_experiment_a.py`](file:///c:/DL_PROJECT/research/experiments/run_experiment_a.py) lines 84–93:
   ```python
   def evaluate_operational_rules(window: np.ndarray) -> tuple[bool, str]:
       latest = window[-1]
       cpu, mem, lat, err, disk = latest[0], latest[1], latest[2], latest[3], latest[4]
       reasons = []
       if mem >= 95.0: reasons.append("memory_pct >= 95")
       if lat >= 1000.0: reasons.append("latency_ms >= 1000")
       if err > 0.5: reasons.append("error_rate_pct > 0.5")  # <-- Trigger!
       if cpu >= 90.0: reasons.append("cpu_pct >= 90")
       if disk >= 95.0: reasons.append("disk_pct >= 95")
       return (len(reasons) > 0, "; ".join(reasons))
   ```
   Because `generate_incident_telemetry()` in `dl/anomaly_detector.py` models all 6 failure modes with synthetic error rates between $1.0\%$ and $55.0\%$ at the tail step, the condition `err > 0.5` is satisfied for **all 120 fault episodes**.
   Consequently, the executable code produces $\text{TP} = 120$, while the manuscript/report narrative described the strict latency/resource threshold behavior ($\text{TP} = 40$).

### Reconciliation Verdict
Both numbers are mathematically grounded under their respective definitions:
- Under **Resource-Only Operational Thresholds** (excluding downstream error rate), Operational Rules recall is **$33.33\%$** ($\text{TP} = 40, \text{FN} = 80$).
- Under **End-to-End Operational Guardrails** (including `error_rate_pct > 0.5%`), Operational Rules recall is **$100.0\%$** ($\text{TP} = 120, \text{FN} = 0$).
- In all scientific reporting, this distinction must be made explicit. The value of the LSTM Autoencoder is in detecting **early sub-threshold anomalies** before explicit HTTP 500 error cascades manifest.

---

## 3. Audit of the Combined Detector

The Combined Detector applies a logical disjunction ($\text{Alert} = \text{Rule} \lor \text{LSTM}$):
- **Sensitivity Preservation**: Because the LSTM Autoencoder achieves $\text{TP} = 120 / 120$ ($100.0\%$ recall), the combined detector also achieves $100.0\%$ recall regardless of whether the operational rule achieves $33.3\%$ or $100.0\%$.
- **False Alarm Inheritance**: The operational rule produces $0$ false alarms on normal steady-state windows ($\text{FP} = 0$). The LSTM Autoencoder produces $2$ false alarms on normal windows ($\text{FP} = 2$). The combined detector inherits exactly the $2$ false alarms of the LSTM Autoencoder ($1.0\%$ FPR, $7.2$ false alarms/hour).
- **Practical Engineering Rationale**: The combined detector guarantees that deterministic hard thresholds (e.g., immediate 500 error burst) trigger instantaneously with zero neural inference latency, while the LSTM Autoencoder provides temporal sensitivity to subtle multivariate drift.

---

## 4. Methodological Audit

### A. Test-Set Independence
- **Training Partition**: Synthesized using `generate_normal_windows(n_windows=800, seed=42)` ($85\%$ train = 680 windows, $15\%$ val = 120 windows).
- **Test Set**: Synthesized using `generate_normal_windows(n_windows=200, seed=2026)` with an explicitly disjoint seed ($2026$).
- **Incident Scenarios**: Synthesized with replicate-specific seeds ($3001$ to $3120$) using `generate_incident_telemetry()`.
- **Finding**: There is zero sample overlap or data leakage between the training/validation sets and the test set.

### B. Synthetic Data Generation vs. Live Deployment
- The 120 fault windows are generated synthetically using sinusoidal baseline dynamics with Gaussian noise and deterministic fault ramps.
- They do **not** represent 120 independent live production outages.
- **Unit of Analysis**: The unit of analysis is the **24-step sequence window** ($N = 320$), not enterprise incident tickets.

### C. Threshold Provenance
- **LSTM Autoencoder Threshold ($\tau = 0.709399$)**: Calibrated at the 99th percentile of reconstruction loss on the 120 validation windows.
- **Isolation Forest Threshold ($-0.0543$)**: Calibrated at the 99th percentile of negative decision scores on the identical 120 validation windows.
- **Operational Rules**: Static industry-standard operational heuristics ($90\%$ CPU, $95\%$ RAM, $1000\,\text{ms}$ latency, $0.5\%$ error rate, $95\%$ disk).

### D. Paired Statistical Hypothesis Testing Justification
- **Recall Comparison (LSTM vs. Isolation Forest, $N = 120$ fault episodes)**:
  - Both Detect: $a = 57$
  - LSTM Only Detects: $b = 63$
  - IsoForest Only Detects: $c = 0$
  - Neither Detects: $d = 0$
  - Exact Two-Sided Binomial Test:
    $$p = 2 \times (0.5)^{63} = \mathbf{2.168 \times 10^{-19}} \quad (p < 0.001)$$
  - Edwards Continuity-Corrected $\chi^2$:
    $$\chi^2 = \frac{(|63 - 0| - 1)^2}{63} = \frac{62^2}{63} = \mathbf{61.02} \quad (p = 5.66 \times 10^{-15})$$
  - Paired Difference in Recall:
    $$\Delta = \frac{63 - 0}{120} = \mathbf{+0.5250} \quad \left(95\% \text{ Wald CI}: [+0.4350, +0.6150]\right)$$
  - **Verdict**: The paired statistical test is completely justified by the raw predictions and demonstrates confirmatory superiority of the LSTM Autoencoder over Isolation Forest on multivariate temporal faults.

- **False Alarm Comparison on Normal Data ($N = 200$ windows)**:
  - Isolation Forest alarms only: $b = 4$
  - LSTM alarms only: $c = 2$
  - Exact Two-Sided Binomial Test:
    $$p = \mathbf{0.6875} \quad (p > 0.05)$$
  - **Verdict**: The difference in false alarms ($2$ vs. $4$) is not statistically significant.
