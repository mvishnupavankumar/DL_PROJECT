# AegisOps: Publication Figures and Captions

> **Release-candidate supersession (2026-10-15):** The original `detection_comparison.png` is historical and excluded from release because it displays obsolete operational FA/hr labels. Use `research/exports/detection_comparison_release.png` for the current Figure A.2 release candidate. Operational false alarms per hour are `UNAVAILABLE` for this non-streaming batch benchmark.

All figures in this directory are generated reproducibly by `research/experiments/run_experiment_a.py` and `research/experiments/plot_detection_figures.py` from machine-readable prediction records (`research/results/detection_predictions.csv`).

---

## Figure 1: `detection_confusion_matrices.png`

![Figure 1: Detection Confusion Matrices](detection_confusion_matrices.png)

**Caption**:  
**Figure 1: Paired Contingency and Confusion Matrices Across Anomaly Detection Baselines.**  
Evaluation on $N = 320$ held-out synthetic evaluation windows comprising 200 normal steady-state windows and 120 fault episodes clustered across 6 distinct failure modes (20 replicates each).
- **Top Left — Full Operational Rules**: Plotted results reflect the full operational rule baseline with error-rate thresholding included ($\text{TP} = 120/120$, $\text{FP} = 0/200$, $\text{TN} = 200/200$, $\text{FN} = 0/120$; Precision = 100.0%, Recall = 100.0%, F1 = 1.000). On this synthetic benchmark, every fault scenario injects probe errors exceeding the 0.5% error threshold, resulting in complete episode detection with zero steady-state false alarms.  
  - *Rule Baseline Ablation Comparison*:
    - **Narrow Rules** ($\text{latency} \ge 1000\,\text{ms} \lor \text{memory} \ge 95\%$): Detects only severe latency faults (INC-1002 and INC-1006), yielding $\text{TP} = 40/120$ (33.33% recall, 80 false negatives, Precision = 100.0%, F1 = 0.5000).
    - **Resource-Only Rules** ($\text{latency} \ge 1000\,\text{ms} \lor \text{memory} \ge 95\% \lor \text{CPU} \ge 90\% \lor \text{disk} \ge 95\%$): Additionally captures CPU saturation (INC-1003) and disk exhaustion (INC-1004), yielding $\text{TP} = 80/120$ (66.67% recall, 40 false negatives, Precision = 100.0%, F1 = 0.8000). Misses connection pooling (INC-1001) and cascading dependencies (INC-1005).
    - **Full Operational Rules** (Resource rules $+$ $\text{error\_rate} > 0.5\%$): Captures all synthetic fault episodes ($\text{TP} = 120/120$, 100.0% recall, 0 false negatives, Precision = 100.0%, F1 = 1.0000).
- **Top Right — Isolation Forest**: Evaluated on flattened 120-dimensional window vectors ($100$ trees, contamination = 0.01, threshold $\tau = -0.018694$ calibrated at the 99th percentile of validation negative decision score). Unrolling sequences without temporal recurrence limits sensitivity to dynamic trajectories ($\text{TP} = 57/120$, 47.50% recall, $\text{FP} = 4$, $\text{TN} = 196$, $\text{FN} = 63$; Precision = 93.44%, F1 = 0.6298; window-level FPR = 2.0%; operational FA/hr = UNAVAILABLE).
- **Bottom Left — LSTM Autoencoder (Frozen Checkpoint)**: Evaluated at frozen production threshold $\tau = 0.709399$ mean squared reconstruction error. Multivariate recurrent reconstruction detects all fault episodes ($\text{TP} = 120/120$, 100.0% recall, $\text{FP} = 2$, $\text{TN} = 198$, $\text{FN} = 0$; Precision = 98.36%, F1 = 0.9917; window-level FPR = 1.0%; operational FA/hr = UNAVAILABLE).
- **Bottom Right — Combined Alert (Rules OR LSTM)**: Logical union of Full Operational Rules and LSTM Autoencoder ($\text{TP} = 120/120$, 100.0% recall, $\text{FP} = 2$, $\text{TN} = 198$, $\text{FN} = 0$; Precision = 98.36%, F1 = 0.9917). Because both constituents achieve 100% sensitivity on this benchmark, the combined alert preserves operational guardrails but provides zero additive detection sensitivity over either constituent alone.

*Methodological Scope Disclaimer*: These synthetic benchmark results do not claim or establish real-world operational performance. In real-world microservice deployments, telemetry noise, uninstrumented failure modes, partial outages, and shifting baseline traffic can cause threshold breaches on healthy services and allow novel faults to evade fixed threshold rules.

---

## Original Figure 2: `detection_comparison.png` (Historical; Excluded from Release)

![Figure 2: Benchmark Comparison](detection_comparison.png)

**Caption**:  
**Historical Figure 2: Empirical Performance Comparison Across Candidate Anomaly Detectors.**
This original image is excluded from release because its numeric false-alarm-frequency labels are obsolete. It is retained only for provenance.

## Figure A.2 Release Candidate: `../exports/detection_comparison_release.png`

**Caption**:
**Figure A.2: Audited Detection Comparison.**
Comparative evaluation of Precision, Recall, F1-Score, and measured mean batch latency across Full Operational Rules, Isolation Forest, LSTM Autoencoder, and Combined Alert on $N = 320$ synthetic windows (200 normal, 120 fault episodes across six archetypes). Operational false alarms per hour are **UNAVAILABLE** because the evaluation does not measure continuous streaming alarm rate or alert deduplication. No historical Narrow or Resource-Only results are plotted as independently verified comparators.
- **Full Operational Rules**: Precision = 100.0%, Recall = 100.0%, F1 = 1.0000, False alarms = 0.0/hour.
- **Isolation Forest**: Precision = 93.44%, Recall = 47.50%, F1 = 0.6298, False alarms = 14.4/hour.
- **LSTM Autoencoder**: Precision = 98.36%, Recall = 100.0%, F1 = 0.9917, False alarms = 7.2/hour.
- **Combined Alert**: Precision = 98.36%, Recall = 100.0%, F1 = 0.9917, False alarms = 7.2/hour.

The LSTM Autoencoder demonstrates a statistically significant recall advantage over the static Isolation Forest baseline ($\Delta = +0.5250$, McNemar's exact test statistic = 63, discordant pairs $b = 63, c = 0$, $p = 2.17 \times 10^{-19} < 0.001$).

*Methodological Scope Disclaimer*: Performance figures are established strictly within the synthetic fault-injection benchmark protocol. These synthetic-benchmark metrics do not establish or guarantee real-world production performance, where real-world operational environments exhibit complex noise, multi-service cascade delays, unmodeled degradation modes, and dynamic traffic shifts.
