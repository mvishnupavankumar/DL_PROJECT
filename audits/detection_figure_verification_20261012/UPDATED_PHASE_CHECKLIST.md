# AegisOps — Updated Research Lifecycle Phase Checklist

**Document Path**: `research/audits/detection_figure_verification_20261012/UPDATED_PHASE_CHECKLIST.md`  
**Audit Date**: 2026-10-12  
**Target Commit**: `e7b8d58c67c514d7a86c67efd1bfbf29f95d85d7` (Branch: `main`)  
**Auditor**: Senior ML Experiment Auditor & Software Testing Specialist  

---

## 1. Phase Status Overview

| Phase | Phase Name | Status | Key Deliverables & Evidence |
| :---: | :--- | :---: | :--- |
| **Phase 1** | Repository Audit & Evidence Inventory | **COMPLETE** | Full code and asset inventory established; Git commit and working-tree verified; SHA-256 manifest audited. |
| **Phase 2** | Data & Label Reconciliation | **COMPLETE** | Disambiguated 200 historical SQLite rows (`anomaly_score = NULL`) from 320 evaluation windows; disproved 175-sample inflation claim. |
| **Phase 3** | Detection Evidence & Figure Verification | **COMPLETE** | Reconciled 120/120 vs. 40/120 rules discrepancy; verified PNG figures against raw CSV; recomputed PR-AUC and McNemar tests ($p = 2.17 \times 10^{-19}$ and $b=4, c=2 \implies p=0.6875$). |
| **Phase 4** | Diagnosis Evidence Reconciliation | **COMPLETE** | Resolved $N=6$ scenario cohort vs. 42 evaluation runs; audited Groq live LLM vs. offline fallback; evaluated Intent-to-Treat denominators. |
| **Phase 5** | Safety Evidence Reconciliation | **COMPLETE** | Disaggregated 16 test cases: 11 adversarial attacks ($11/11$ blocked, 100%), 2 precondition checks, 1 verification probe, 2 controls. |
| **Phase 6** | Statistical Analysis & Master Audit | **COMPLETE** | Formal hypothesis testing executed; power constraints ($1 - \beta \approx 0.14$) documented; paired intervals verified. |
| **Phase 7** | Full Manuscript & Submission Package | **COMPLETE** | Full 11-section publication manuscript authored in `research/paper/AEGISOPS_RESEARCH_PAPER.md` with registers, checklists, and diagram sources. |

---

## 2. Phase 3 Verification Detailed Sign-Off

- [x] **Raw Predictions Verification**:
  - `research/results/detection_predictions.csv` and `research/raw/detection_predictions.csv` confirmed identical ($N = 320$: 200 normal, 120 fault across 6 classes).
- [x] **Independent Metric Recomputation**:
  - Completed and documented in `DETECTION_METRIC_RECALCULATION.csv`.
- [x] **Operational Rules Discrepancy Resolved**:
  - Full operational rules (with `err > 0.5%`) catch 120/120 TP (100.0% recall).
  - Physical resource rules (without HTTP error rate) catch 40/120 TP (33.3% recall).
  - Both definitions documented in `DETECTION_DISCREPANCIES.md` and reconciled in the manuscript.
- [x] **Figure Accuracy Confirmed**:
  - Plotted confusion matrices and bar charts in `research/figures/` match `detection_metrics.csv` with 100% numerical accuracy.
  - Figure caption error in `FIGURE_CAPTIONS.md` identified and documented.
- [x] **Combined Detector Logic Verified**:
  - Perfectly matches `rule_flag | lstm_flag` with 0 mismatches across all 320 rows.
  - Redundancy on synthetic benchmark documented.
- [x] **Statistical Testing Verified**:
  - McNemar exact binomial test: $b=63, c=0 \implies p = 2.168 \times 10^{-19}$ (Edwards $\chi^2 = 61.02$).
  - Paired sensitivity difference: $\Delta = +0.5250$, 95% Wald CI $[+0.4357, +0.6143]$.
  - Normal false alarm comparison: $b=4, c=2 \implies p = 0.6875$ (not significant).

---

## 3. Preserved Scientific Boundaries & Non-Negotiables

1. **No Data Tampering**: No raw prediction files, thresholds, or test labels were altered.
2. **No Model Retraining**: Checkpoint `models/lstm_autoencoder.pt` remains frozen.
3. **No Unchecked Claims**: Projected false alarms/hour ($7.2$) are explicitly qualified as linear projections from 1.0% single-window error rates, not continuous live monitoring tallies.
4. **Figure Code Reproducibility Note**: Documented that `run_all.py` does not generate the PNG figures and that they are preserved as static binary assets.

---

## 4. Single Next Action Required

The single next action required to proceed is:
**Author and add a dedicated reproducible figure generation script (`research/experiments/plot_detection_figures.py`) so that the two publication PNG figures can be programmatically regenerated from `research/results/detection_predictions.csv` within `research/run_all.py`, closing the static-asset reproducibility gap.**
