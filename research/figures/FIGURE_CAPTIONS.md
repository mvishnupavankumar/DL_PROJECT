# AegisOps: Publication Figures and Captions

All figures in this directory are generated reproducibly by `research/experiments/run_experiment_a.py` and saved at high resolution.

---

## Figure 1: `detection_confusion_matrices.png`

![Figure 1: Detection Confusion Matrices](detection_confusion_matrices.png)

**Caption**:  
**Figure 1: Paired Contingency and Confusion Matrices Across Anomaly Detection Baselines.**  
Evaluation on $N = 320$ held-out independent windows comprising 200 normal steady-state windows and 120 fault episodes across 6 distinct failure modes (20 replicates each).  
- **Top Left**: Operational Rules Baseline. Exhibits zero false alarms on steady-state normal data (200/200 TN), but misses gradual and compound degradation faults (40/120 TP, 33.3% recall).
- **Top Right**: Isolation Forest ($k = 100$ trees, contamination = 0.05). Flattening window sequences into feature means limits temporal sensitivity (57/120 TP, 47.5% recall; 4 false alarms).
- **Bottom Left**: LSTM Autoencoder (Frozen live checkpoint, threshold $\tau = 0.709399$). Captures multivariate temporal dependencies with 100.0% episode recall (120/120 TP) and 2 false alarms (7.2 false alarms/hour, 1.0% FPR).
- **Bottom Right**: Combined Detector (LSTM Autoencoder OR Operational Guardrails). Preserves 100.0% recall while retaining operational safety guardrails.

---

## Figure 2: `detection_comparison.png`

![Figure 2: Benchmark Comparison](detection_comparison.png)

**Caption**:  
**Figure 2: Empirical Performance Comparison Across Detection Architectures.**  
Side-by-side comparison of Episode-level Recall (%), Precision (%), F1-Score, and Mean Inference Latency (ms) evaluated on identical held-out test windows. The LSTM Autoencoder significantly outperforms the static Isolation Forest baseline ($\Delta = +0.5250$, McNemar's exact test $p = 2.17 \times 10^{-19} < 0.001$) while executing well within real-time operational budgets (mean inference latency: 0.17 ms per 24-step sequence).
