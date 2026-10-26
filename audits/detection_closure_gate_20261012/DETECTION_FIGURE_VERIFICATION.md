# AegisOps: Detection Figure Verification Report

**Audit Gate**: Phase 3 Detection Evidence Closure and Master Checklist Update  
**Audit Date**: 2026-10-12  
**Audit Directory**: `research/audits/detection_closure_gate_20261012/`  
**Inspected Artifacts**:
- Figure A.1: `research/figures/detection_confusion_matrices.png` ($1000 \times 750$ px)
- Figure A.2: `research/figures/detection_comparison.png` ($950 \times 550$ px)
- Dedicated Audit Outputs: `research/audits/detection_closure_gate_20261012/figures/`
- Prediction Records: `research/results/detection_predictions.csv` ($N = 320$ rows)
- Machine-Readable Metrics: `research/results/detection_metrics.csv`
- Generator Script: `research/experiments/plot_detection_figures.py`

---

## 1. Executive Summary & Verification Verdict

Both Figure A.1 and Figure A.2 have been independently verified against the raw machine-readable prediction records (`research/results/detection_predictions.csv`).
1. **100% Numerical Concordance**: Every cell in Figure A.1 ($2 \times 2$ matrices for all four plotted models) and every bar/label in Figure A.2 matches the underlying prediction data without deviation.
2. **Dynamic Generation**: `research/experiments/plot_detection_figures.py` dynamically evaluates contingency tables and derived metrics directly from the loaded DataFrame, eliminating hardcoded plotting values.
3. **Retention of Prior Figures**: The canonical publication figures in `research/figures/` remain intact and synchronized with `research/paper/figures/`. Independent verified copies have been generated and archived in `research/audits/detection_closure_gate_20261012/figures/`.
4. **Caption Alignment**: `research/figures/FIGURE_CAPTIONS.md` precisely reflects the plotted Full Operational Rules (120/120 TP) while formally contrasting them with the Narrow (40/120 TP) and Resource-Only (80/120 TP) ablation configurations.

---

## 2. Figure A.1 Quadrant-by-Quadrant Verification

Figure A.1 presents paired contingency matrices across $N = 320$ held-out test windows (200 normal steady-state windows and 120 incident windows across 6 failure modes, 20 replicates each).

```
+------------------------------------+------------------------------------+
|  Top Left: Full Operational Rules  |    Top Right: Isolation Forest     |
|  TN: 200        FP: 0              |    TN: 196        FP: 4            |
|  FN: 0          TP: 120            |    FN: 63         TP: 57           |
|  Prec: 1.000 | Rec: 1.000 | F1: 1.0|    Prec: 0.934 | Rec: 0.475 | F1: 0.630|
+------------------------------------+------------------------------------+
|  Bottom Left: LSTM Autoencoder     |    Bottom Right: Combined Alert    |
|  TN: 198        FP: 2              |    TN: 198        FP: 2            |
|  FN: 0          TP: 120            |    FN: 0          TP: 120          |
|  Prec: 0.984 | Rec: 1.000 | F1: 0.9|    Prec: 0.984 | Rec: 1.000 | F1: 0.992|
+------------------------------------+------------------------------------+
```

### Detailed Breakdown
1. **Top-Left: Full Operational Rules**:
   - Column: `rule_flag`
   - Plotted: $\text{TN} = 200$, $\text{FP} = 0$, $\text{FN} = 0$, $\text{TP} = 120$
   - Summary: Precision = 1.000, Recall = 1.000, F1 = 1.000
   - Reconciliation Note: The rule definition includes `error_rate_pct > 0.5`. Because all 6 synthetic failure scenarios inject HTTP probe errors well exceeding 0.5%, all 120 incident windows trigger.
2. **Top-Right: Isolation Forest Baseline**:
   - Column: `iso_flag`
   - Model: $k = 100$ trees, contamination = 0.01, threshold $\tau = -0.018694$ (calibrated on 99th percentile of validation negative decision score)
   - Plotted: $\text{TN} = 196$, $\text{FP} = 4$, $\text{FN} = 63$, $\text{TP} = 57$
   - Summary: Precision = 0.934 ($57 / 61 = 0.9344$), Recall = 0.475 ($57 / 120 = 0.4750$), F1 = 0.630 ($0.6298$)
   - Error Rates: False Positive Rate = $2.0\%$ ($4 / 200$), False Alarms/hr = $14.40$
3. **Bottom-Left: LSTM Autoencoder (Frozen Checkpoint)**:
   - Column: `lstm_flag`
   - Model: Frozen checkpoint `models/lstm_autoencoder.pt`, threshold $\tau = 0.709399$
   - Plotted: $\text{TN} = 198$, $\text{FP} = 2$, $\text{FN} = 0$, $\text{TP} = 120$
   - Summary: Precision = 0.984 ($120 / 122 = 0.9836$), Recall = 1.000 ($120 / 120 = 1.0000$), F1 = 0.992 ($0.9917$)
   - Error Rates: False Positive Rate = $1.0\%$ ($2 / 200$), False Alarms/hr = $7.20$
4. **Bottom-Right: Combined Alert (Rules OR LSTM)**:
   - Column: `combined_flag`
   - Definition: `rule_flag or lstm_flag`
   - Plotted: $\text{TN} = 198$, $\text{FP} = 2$, $\text{FN} = 0$, $\text{TP} = 120$
   - Summary: Precision = 0.984, Recall = 1.000, F1 = 0.992
   - Redundancy Note: Since Full Operational Rules already triggers on all 120 fault episodes, the logical OR introduces zero additive incident sensitivity over the LSTM or rules alone on this benchmark.

---

## 3. Figure A.2 Performance Comparison Verification

Figure A.2 provides a grouped bar chart comparing Precision, Recall, F1-Score, and False Alarms/Hour across candidate architectures:

| Plotted Candidate | Precision | Recall | F1-Score | False Alarms / Hour | CSV Concordance |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Full Operational Rules** | 1.00 | 1.00 | 1.00 | FA/hr: 0.0 | **Exact Match** |
| **Isolation Forest** | 0.93 | 0.48 | 0.63 | FA/hr: 14.4 | **Exact Match** |
| **LSTM Autoencoder** | 0.98 | 1.00 | 0.99 | FA/hr: 7.2 | **Exact Match** |
| **Combined Alert** | 0.98 | 1.00 | 0.99 | FA/hr: 7.2 | **Exact Match** |

- **Y-Axis**: Linear scale from $0.0$ to $1.0$ with gridlines at $0.2, 0.4, 0.6, 0.8, 1.0$.
- **False Alarm Frequency**: Plotted beneath detector group names; exactly equals $\text{FPR} \times 720\text{ steps/hr}$.

---

## 4. Methodological Scope & Disclaimer Verification

Both figures and their captions strictly adhere to scientific reporting boundaries:
- The synthetic benchmark nature of the evaluation is explicitly declared.
- No claim is made that 100% recall on synthetic fault episodes establishes real-world operational reliability.
