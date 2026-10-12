# AegisOps — Phase 3 Rule Baseline Finalization and Verification Checklist

**Document Path**: `research/audits/rule_baseline_finalization_20261012/UPDATED_PHASE_CHECKLIST.md`  
**Audit Date**: 2026-10-12  
**Target Commit**: `e7b8d58c67c514d7a86c67efd1bfbf29f95d85d7`  
**Auditor**: Senior ML Experiment Auditor & Software Testing Specialist  

---

## 1. Audit Deliverables and Status

| Deliverable | Path | Status | Verification Notes |
| :--- | :--- | :---: | :--- |
| **Recalculated Baseline Table** | `research/audits/rule_baseline_finalization_20261012/DETECTION_METRIC_RECALCULATION.csv` | **COMPLETE** | Unambiguously details Narrow Rules (40 TP), Resource-Only Rules (80 TP), and Full Operational Rules (120 TP) alongside model baselines. |
| **Discrepancy Resolution Report** | `research/audits/rule_baseline_finalization_20261012/DETECTION_DISCREPANCIES.md` | **COMPLETE** | Traces 40/120 vs. 80/120 to exact feature subsets, resolves caption conflict, and documents Combined Detector redundancy. |
| **Reproducible Figure Generator** | `research/experiments/plot_detection_figures.py` | **COMPLETE** | Pillow-based visualization engine regenerating `detection_confusion_matrices.png` and `detection_comparison.png`. |
| **Pipeline Integration** | `research/run_all.py` | **COMPLETE** | Wired into Step 2; runs in 51.4s, passes all 42 tests, updates `MANIFEST_SHA256.json`. |

---

## 2. Check Verification Matrix

- [x] **Check 1: Three Separate Baselines Evaluated**:
  - Narrow Rules (Latency $\ge 1000$ ms, Memory $\ge 95\%$): $\text{TP}=40, \text{FN}=80$ (33.33% recall).
  - Resource-Only Rules (Latency $\ge 1000$ ms, Memory $\ge 95\%$, CPU $\ge 90\%$, Disk $\ge 95\%$): $\text{TP}=80, \text{FN}=40$ (66.67% recall).
  - Full Operational Rules (All resource rules + Error Rate $> 0.5\%$): $\text{TP}=120, \text{FN}=0$ (100.0% recall).
- [x] **Check 2: 40/120 vs. 80/120 Discrepancy Formally Resolved**:
  - 40/120 is the exact outcome of Narrow Rules (catches INC-1002 and INC-1006).
  - 80/120 is the exact outcome of Resource-Only Rules (catches INC-1002, INC-1003, INC-1004, and INC-1006).
  - Prior texts conflated the two by loosely referring to Narrow Rules as "resource-only". Both definitions are now formally segregated and documented.
- [x] **Check 3: Combined Detector Verified**:
  - Implements `rule_flag or lstm_flag` with 0 mismatches across 320 evaluation rows.
  - Zero additive sensitivity on this benchmark ($\text{TP}=120, \text{FP}=2$, identical to LSTM alone).
- [x] **Check 4: Figure Generation Reproducibility Closed**:
  - Implemented `research/experiments/plot_detection_figures.py`.
  - Both figures regenerate cleanly and sync to `research/paper/figures/`.
- [x] **Check 5: Test Regression Verified**:
  - Pytest regression suite: 42 passed in 15.84s (100%).
  - Full pipeline `run_all.py`: Exited with code 0 in 51.4s.

---

## 3. Single Remaining Action Before Phase 3 Sign-Off

The single remaining action before formal Phase 3 sign-off is:
**Update `research/figures/FIGURE_CAPTIONS.md` to correct the obsolete line 14 caption text (which claimed Figure 1 displayed 40/120 TP) so that the caption precisely describes the Full Operational Rules (120/120 TP) plotted in Figure 1 while explicitly noting the Narrow (40/120) and Resource-Only (80/120) variants.**
