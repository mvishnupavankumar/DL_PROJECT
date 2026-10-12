# AegisOps: Phase 3 Figure Caption Verification and Reconciliation

**Date**: 2026-10-12  
**Audit Directory**: `research/audits/phase3_final_reproducibility_20261012/`  
**Reference Document**: `research/figures/FIGURE_CAPTIONS.md`  
**Data Sources**:
- `research/results/detection_predictions.csv` ($N = 320$ rows)
- `research/results/detection_metrics.csv`
- `research/figures/detection_confusion_matrices.png`
- `research/figures/detection_comparison.png`

---

## 1. Caption Reconciliation and Rule Baseline Distinction

### 1.1 Resolution of Figure 1 Top-Left Quadrant
In earlier drafts, Figure 1's top-left quadrant was captioned with the Narrow Rules results (40/120 TP, 33.3% recall), while the actual image rendered from the automated runner plotted the Full Operational Rules results (120/120 TP, 100.0% recall, 0 FP, 200 TN).

`research/figures/FIGURE_CAPTIONS.md` has been corrected to explicitly describe the plotted **Full Operational Rules** while providing the exact comparative ablation breakdown across all three rule variants:

| Rule Baseline Variant | Included Thresholds | TP | FP | TN | FN | Precision | Recall | F1-Score | Scenarios Detected |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Narrow Rules** | $\text{latency} \ge 1000\,\text{ms} \lor \text{memory} \ge 95\%$ | 40 | 0 | 200 | 80 | 100.0% | 33.33% | 0.5000 | INC-1002 (DB outage), INC-1006 (timeouts) |
| **Resource-Only Rules** | $\text{latency} \ge 1000\,\text{ms} \lor \text{memory} \ge 95\% \lor \text{CPU} \ge 90\% \lor \text{disk} \ge 95\%$ | 80 | 0 | 200 | 40 | 100.0% | 66.67% | 0.8000 | INC-1002, INC-1003 (CPU sat), INC-1004 (disk cap), INC-1006 |
| **Full Operational Rules** | Resource rules $+$ $\text{error\_rate} > 0.5\%$ | **120** | **0** | **200** | **0** | **100.0%** | **100.0%** | **1.0000** | **All 6 scenarios** (INC-1001 through INC-1006) |

### 1.2 Quadrant-by-Quadrant Verification (Figure 1)

1. **Top-Left (Full Operational Rules)**:
   - Plotted: $\text{TN} = 200, \text{FP} = 0, \text{FN} = 0, \text{TP} = 120$
   - Metrics: Precision = 1.000, Recall = 1.000, F1 = 1.000
   - Machine-readable match: Exact match with `rule_flag` column in `detection_predictions.csv`.
2. **Top-Right (Isolation Forest)**:
   - Plotted: $\text{TN} = 196, \text{FP} = 4, \text{FN} = 63, \text{TP} = 57$
   - Metrics: Precision = 0.934, Recall = 0.475, F1 = 0.630
   - Machine-readable match: Exact match with `iso_flag` column in `detection_predictions.csv`.
3. **Bottom-Left (LSTM Autoencoder)**:
   - Plotted: $\text{TN} = 198, \text{FP} = 2, \text{FN} = 0, \text{TP} = 120$
   - Metrics: Precision = 0.984, Recall = 1.000, F1 = 0.992
   - Machine-readable match: Exact match with `lstm_flag` column in `detection_predictions.csv`.
4. **Bottom-Right (Combined Alert — Rules OR LSTM)**:
   - Plotted: $\text{TN} = 198, \text{FP} = 2, \text{FN} = 0, \text{TP} = 120$
   - Metrics: Precision = 0.984, Recall = 1.000, F1 = 0.992
   - Machine-readable match: Exact match with `combined_flag` column in `detection_predictions.csv`.
   - Overlap note: Zero incremental detection sensitivity over Full Operational Rules alone on this benchmark.

---

## 2. Figure 2 Verification (`detection_comparison.png`)

Figure 2 compares Precision, Recall, F1-Score, and False Alarms/Hour:
- **Full Operational Rules**: Prec = 1.00, Rec = 1.00, F1 = 1.00, FA/hr = 0.0
- **Isolation Forest**: Prec = 0.93, Rec = 0.48, F1 = 0.63, FA/hr = 14.4
- **LSTM Autoencoder**: Prec = 0.98, Rec = 1.00, F1 = 0.99, FA/hr = 7.2
- **Combined Alert**: Prec = 0.98, Rec = 1.00, F1 = 0.99, FA/hr = 7.2

All plotted bars and labels match the machine-readable values in `detection_metrics.csv` to 2 decimal places.

---

## 3. Methodological Scope and Real-World Disclaimer

Both figure captions explicitly include the following mandatory caveat:
> *Methodological Scope Disclaimer*: These synthetic benchmark results do not claim or establish real-world operational performance. In real-world microservice deployments, telemetry noise, uninstrumented failure modes, partial outages, and shifting baseline traffic can cause threshold breaches on healthy services and allow novel faults to evade fixed threshold rules.
