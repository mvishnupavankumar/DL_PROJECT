# AegisOps: Command Execution Logs and Exit Codes

**Audit Gate**: Phase 3 Detection Evidence Closure and Master Checklist Update  
**Audit Date**: 2026-10-12  
**Audit Directory**: `research/audits/detection_closure_gate_20261012/`  
**Environment**: Python 3.11.9 (`.venv`), Windows 10/11, Git branch `main` (`ec83d2f`)

---

## 1. Unified Research Runner (`research/run_all.py`)

- **Command Line**: `.\.venv\Scripts\python.exe research/run_all.py`
- **Working Directory**: `c:\DL_PROJECT`
- **Execution Timestamp**: 2026-10-12T14:13:30+05:30
- **Elapsed Time**: 52.7 seconds
- **Exit Code**: **`0`**

### Captured Output Log
```text
================================================================================
AEGISOPS UNIFIED EXPERIMENT & REPRODUCIBILITY SUITE
================================================================================

[Step 1/5] Running Pytest Regression Suite (42 tests)...
..........................................                               [100%]
42 passed in 16.67s

[Step 2/5] Running Experiment A (Anomaly Detection & Figure Generation)...
======================================================================
EXPERIMENT A: ANOMALY DETECTION EVALUATION
======================================================================
Loaded LSTM Autoencoder (Threshold: 0.709399)
Calibrated Isolation Forest Threshold (99th pct on val): -0.018694
Held-out test set: 200 normal windows, 120 incident windows
Saved raw test predictions: C:\DL_PROJECT\research\results\detection_predictions.csv
Saved detection metrics: C:\DL_PROJECT\research\results\detection_metrics.csv
Saved scenario breakdown: C:\DL_PROJECT\research\results\detection_by_scenario.csv
Saved confusion matrices figure: C:\DL_PROJECT\research\figures\detection_confusion_matrices.png
Saved comparison chart figure: C:\DL_PROJECT\research\figures\detection_comparison.png
Synced generated figures to C:\DL_PROJECT\research\paper\figures

[Step 3/5] Running Experiment B (Diagnosis Rubric Evaluation)...
[OUTPUT] Saved rubric-annotated diagnosis predictions: C:\DL_PROJECT\research\raw\diagnosis_predictions.csv
[OUTPUT] Saved diagnosis summary metrics: C:\DL_PROJECT\research\raw\diagnosis_metrics.csv
                     configuration  ...  per_protocol_accuracy
0           1. Rule-based Baseline  ...                 1.0000
1        2. Single-Agent (Offline)  ...                 0.5000
2    3. Multi-Agent Full (Offline)  ...                 0.5000
3   4. Multi-Agent No-DL (Offline)  ...                 1.0000
4       5. Single-Agent (Groq LLM)  ...                 0.6667
5   6. Multi-Agent Full (Groq LLM)  ...                 0.8333
6  7. Multi-Agent No-DL (Groq LLM)  ...                 0.6667

[Step 4/5] Running Experiment C (Safety & Verification Audit)...
===========================================================================
AEGISOPS: RUNNING SAFETY, AUTHORIZATION & RECOVERY AUDIT
Testing ACTUAL application verification & recovery functions
===========================================================================
[INIT] Local disposable FastAPI service running at http://127.0.0.1:8765
[PASS] TC-POS-01 (POSITIVE_CONTROL): Full end-to-end approval, execution, and health restoration
[PASS] TC-ATT-01 (ATTACK_CASE): Consume non-existent ticket ID
[PASS] TC-ATT-02 (ATTACK_CASE): Consume expired ticket
[PASS] TC-ATT-03 (ATTACK_CASE): Approve with invalid confirmation phrase
[PASS] TC-ATT-04 (ATTACK_CASE): Consume with modified action ID
[PASS] TC-ATT-05 (ATTACK_CASE): Consume with modified target URL
[PASS] TC-ATT-06 (ATTACK_CASE): Consume with modified incident ID
[PASS] TC-ATT-07 (ATTACK_CASE): Replay consumed approval ticket
[PASS] TC-ATT-08 (ATTACK_CASE): Consume explicitly rejected ticket
[PASS] TC-ATT-09 (ATTACK_CASE): Execute recovery on remote HTTPS endpoint
[PASS] TC-ATT-10 (ATTACK_CASE): Register remote plaintext HTTP target
[PASS] TC-ATT-11 (ATTACK_CASE): Register target with embedded credentials
[PASS] TC-FAIL-01 (ATTACK_CASE): Execute recovery on unreachable local port
[PASS] TC-FAIL-02 (ATTACK_CASE): Execute recovery when no fault is active
[PASS] TC-VERIF-01 (ATTACK_CASE): Service remains unhealthy after attempted recovery
[PASS] TC-AUDIT-01 (POSITIVE_CONTROL): Independent SQLite audit record verification
[TEARDOWN] Local test service halted successfully.
[OUTPUT] Saved per-case safety test results: C:\DL_PROJECT\research\raw\safety_test_results.csv
[OUTPUT] Saved safety metrics: C:\DL_PROJECT\research\raw\safety_metrics.csv
[OUTPUT] Saved comprehensive safety evaluation report: C:\DL_PROJECT\research\SAFETY_EVALUATION.md

[Step 5/5] Generating Statistical Analysis & Checksum Manifest...
Saved formal statistical analysis: c:\DL_PROJECT\research\results\statistical_analysis.md
Generating SHA-256 Artifact & Model Manifest...
Saved manifest: C:\DL_PROJECT\research\MANIFEST_SHA256.json

================================================================================
ALL EXPERIMENTS AND AUDITS COMPLETED SUCCESSFULLY IN 52.7 SECONDS
================================================================================
```

---

## 2. Two-Run Deterministic Reproducibility Verification

- **Command Line**: `.\.venv\Scripts\python.exe scratch/run_two_run_reproducibility.py`
- **Exit Code**: **`0`**
- **Results**:
  - Run 1 Isolation Forest Threshold: `-0.018694`
  - Run 2 Isolation Forest Threshold: `-0.018694`
  - Match: **`True`** ($\Delta = 0.000000$)
  - Predictions CSV Diff: 0 row differences, 0 column differences (320 rows identical)
  - Figure A.1 SHA-256 Match: **`True`** (`0784db0ef9c62667...`)
  - Figure A.2 SHA-256 Match: **`True`** (`ad1935fa98d5a48f...`)

---

## 3. Metric Recomputation and Separate Figure Generation

- **Command Line**: `.\.venv\Scripts\python.exe scratch/recompute_and_verify_all.py`
- **Exit Code**: **`0`**
- **Output Artifacts Generated**:
  - `research/audits/detection_closure_gate_20261012/RECOMPUTED_DETECTION_METRICS.csv`
  - `research/audits/detection_closure_gate_20261012/figures/detection_confusion_matrices.png`
  - `research/audits/detection_closure_gate_20261012/figures/detection_comparison.png`
