# AegisOps Experiment D: Human Method Decision Package v2.0

**Document ID**: `AEGISOPS-DECISION-PACKET-V2`  
**Date**: October 13, 2026  
**Auditor**: Independent ML Research Engineer, Statistical Auditor & Reproducibility Reviewer  
**Repository**: `C:\DL_PROJECT`  
**Git HEAD**: `d277c1df3c2599ddecdf5f0bb761c99718499667`  
**Working Tree Status**: Modified / Uncommitted audit files (Pre-execution gate locked)  
**Final Audit Verdict**: `READY FOR HUMAN METHOD DECISION`  
**Production Experiment D Status**: **STRICTLY BLOCKED PENDING SUPERVISOR AUTHORIZATION**  

---

## 1. Context and Purpose of this Package

This decision package provides the human research supervisor with a complete, verified scientific foundation to resolve the methodology for **Experiment D (External Benchmark Validation on AnoMod)**.

### Prior State
- `EXPERIMENT_D_CALIBRATION_INDEPENDENCE_AUDIT.md` placed Experiment D into `BLOCKED — CALIBRATION OR STATISTICAL VALIDITY DEFECT` because `run_experiment_d.py` used the same 8 held-out validation windows to calibrate the 99th percentile threshold and evaluate false positive rates, circularly guaranteeing $0.0\%$ false alarms.
- The supervisor proposed investigating **Option C (Zero-shot transfer using frozen training preprocessing and threshold)** combined with **Option D (Exploratory claim restrictions)**.

### Current Reconciled State
1. **Model Contract Fully Reconciled**: Feature order, normalization vectors, architecture, tensor shapes, reconstruction loss formulas, and threshold semantics are verified against source code and raw checkpoint weights.
2. **Feature Order Discrepancy Resolved**: The true order is `("cpu_pct", "memory_pct", "latency_ms", "error_rate_pct", "disk_pct")`. The legacy protocol table in v1.1.0 §4.1 contained a fatal typo swapping disk with latency/error.
3. **Window Counts Reconciled**: SocialNetwork `Normal_Baseline` contains 80 grid points, 57 complete points, clustering into 3 runs of lengths 11, 11, and 18 intervals. These produce exactly 19 eligible $W=8$ sliding windows. A 70/30 chronological split on raw series with a 7-step purge gap produces 5 calibration windows and 8 validation windows. For $W=24$, there are 0 valid windows.
4. **Zero-Shot Domain Shift Empirically Proven**: Evaluating the frozen synthetic scaler and threshold on the 19 nominal windows yields a **100% false alarm rate (19/19 windows flagged)** due to severe domain shift between synthetic training constants and Kubernetes microservice baselines.

---

## 2. Proposed Combined Methodology: Option C + Option D

### Core Tenets of the Combined Proposal:
1. **Zero-Shot Normalization (Option C)**:
   - Disallow fitting any normalization scalers on target external data.
   - Standardize inputs strictly using the frozen synthetic training moments:
     $$\boldsymbol{\mu} = [42.06, 53.97, 76.89, 0.24, 48.27], \quad \boldsymbol{\sigma} = [5.79, 3.56, 6.09, 0.055, 4.34]$$
2. **Explicit Acknowledgment of Domain Shift**:
   - Because the synthetic training distribution does not align with Kubernetes microservices, applying the frozen threshold ($\tau = 0.709399$) flags 100% of nominal windows as anomalous.
   - Rather than masking this with post-hoc target tuning, report this result transparently as an empirical limitation of synthetic-to-real transfer.
3. **Exploratory Claim Scope (Option D)**:
   - Formally withdraw Confirmatory Hypothesis H-D1 (which claimed statistical superiority via McNemar's test).
   - Re-frame all external benchmark findings as **Exploratory Finding E-D1** (Descriptive fault sensitivity and domain-transfer characteristics).
4. **Rigorous Dependence Treatment**:
   - Disallow treating overlapping sliding windows ($87.5\%$ data overlap) as independent samples.
   - Aggregate evaluations at the scenario level ($N=12$ independent fault episodes).
   - Compute nominal false alarm uncertainty via Wilson 95% Score Confidence Intervals ($N=19$ windows).

---

## 3. Prerequisite Checklist for Supervisor Approval

Before Experiment D code can be modified or executed, the human research supervisor must approve the following 4 decisions:

```
[ ] DECISION 1: PROTOCOL RATIFICATION
    Formally ratify Protocol Amendment v1.2.0, correcting the feature order from
    (cpu, mem, disk, lat, err) to (cpu, mem, lat, err, disk) to match the frozen checkpoint.

[ ] DECISION 2: SEQUENCE LENGTH POLICY
    Formally approve evaluating on W=8 windows (120s temporal span at 15s sampling)
    with the W=24 checkpoint, acknowledging that the model was trained on W=24
    (120s span at 5s sampling) and documenting the score distribution shift.

[ ] DECISION 3: REPORTING MODALITY FOR ZERO-SHOT TRANSFER
    Select the reporting modality for the zero-shot external benchmark:
    ( ) Modality 3A (Strict Zero-Shot): Report frozen threshold results (acknowledging
        100% nominal false alarm rate as evidence of synthetic-to-real domain shift).
    ( ) Modality 3B (Threshold-Free Ranking): Report continuous ROC-AUC and PR-AUC
        curves to evaluate detection ranking ability without committing to an invalid threshold.
    ( ) Modality 3C (Target-Calibrated Exploratory): Re-calibrate threshold on nominal
        warmup (Option B) under strictly exploratory labeling, with zero confirmatory claims.

[ ] DECISION 4: CONFIRMATORY HYPOTHESIS WITHDRAWAL
    Formally withdraw Confirmatory Hypothesis H-D1 (McNemar superiority on external data)
    and replace it with Exploratory Finding E-D1 in the manuscript evidence matrix.
```

---

## 4. Audit Evidence and Traceability Record

### 4.1 Environment and Files Inspected
- **Git Commit**: `d277c1df3c2599ddecdf5f0bb761c99718499667`
- **Files Inspected**:
  - [`models/lstm_autoencoder.pt`](file:///C:/DL_PROJECT/models/lstm_autoencoder.pt) (SHA-256: `1cf44e6e82e459f543fcace25334f3076b76c77a357d46f65c11e3c44fd382de`)
  - [`models/lstm_autoencoder.json`](file:///C:/DL_PROJECT/models/lstm_autoencoder.json)
  - [`dl/anomaly_detector.py`](file:///C:/DL_PROJECT/dl/anomaly_detector.py) (Lines 14-32, 105-188, 239-254)
  - [`research/experiments/run_experiment_d.py`](file:///C:/DL_PROJECT/research/experiments/run_experiment_d.py) (Lines 40-222, 320-432, 500-580, 685-760)
  - [`research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md`](file:///C:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md) (v1.1.0 §4.1)
  - [`research/audits/PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md`](file:///C:/DL_PROJECT/research/audits/PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md)
  - [`research/audits/experiment_d_temporal_eligibility_audit.json`](file:///C:/DL_PROJECT/research/audits/experiment_d_temporal_eligibility_audit.json)
  - [`data/external/anomod/unpacked/SN_data/metric_data/Normal_Baseline_20251103_220228_metrics_2025-11-03_22-22-55/`](file:///C:/DL_PROJECT/data/external/anomod/unpacked/SN_data/metric_data/Normal_Baseline_20251103_220228_metrics_2025-11-03_22-22-55)

### 4.2 Scripts Executed and Test Results
All commands were executed in isolated scratch scripts without mutating production code:
1. `research/audits/scratch_inspect_checkpoint.py`:
   - Extracted weights, means, stds, thresholds, feature list, and training loss from `models/lstm_autoencoder.pt`. Verified strict match with `dl/anomaly_detector.py`.
2. `research/audits/scratch_score_semantics.py`:
   - Verified that `detect()` enforces $W=24$ and crashes on $W=8$. Verified score shift between $W=8$ ($0.339$) and $W=24$ ($0.239$).
3. `research/audits/scratch_trace_nominal.py` & `scratch_intervals_map.py`:
   - Mapped all 80 raw intervals in SocialNetwork Normal Baseline. Verified 23 missing trace intervals, 57 complete intervals, 3 contiguous runs (lengths 11, 11, 18), 19 eligible $W=8$ windows, and 0 eligible $W=24$ windows.
   - Verified chronological 70/30 split: 56 calib rows (5 windows), 7 purge rows, 17 val rows (8 windows).
4. `research/audits/scratch_test_zero_shot.py`:
   - Evaluated frozen training scaler and threshold on the 19 nominal windows. Produced mean reconstruction loss of $59.19$ vs threshold $0.7094$, resulting in 100% false alarms (19/19 windows flagged).

---

## 5. Final Audit Verdict

`READY FOR HUMAN METHOD DECISION`

**Conditions of this Verdict**:
- The model contract, feature order, window counts, and zero-shot mechanics are fully reconciled and supported by empirical evidence.
- Production execution of Experiment D (`run_experiment_d.py --authorized`) remains **STRICTLY BLOCKED**.
- No production files, metrics CSV, predictions CSV, or ratification records have been modified.

---

## 6. Single Most Important Decision Required

> ### Primary Decision for the Human Research Supervisor:
> **Which reporting modality should be adopted for Experiment D in the manuscript:**
> 1. **Modality 3A (Pure Zero-Shot Transfer)**: Run frozen weights, frozen scaler, and frozen threshold, reporting the expected ~100% nominal false alarm rate as a transparent finding of synthetic-to-real domain shift; OR
> 2. **Modality 3B (Threshold-Free Ranking Evaluation)**: Run frozen weights and scaler, but report continuous ROC-AUC / PR-AUC curves to evaluate whether the autoencoder ranks faults above normal traffic without committing to an unusable threshold; OR
> 3. **Modality 3C (Target-Calibrated Exploratory Analysis)**: Calibrate the threshold on nominal warmup telemetry (Option B) under strictly exploratory labeling, explicitly acknowledging target adaptation?
