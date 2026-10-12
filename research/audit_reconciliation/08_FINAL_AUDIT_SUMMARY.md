# 08 — Final Audit Summary

**Audit Date**: 2026-10-12  
**Auditor**: Senior ML Experiment Auditor, Python Research Engineer, Statistical Reviewer & Software Testing Specialist  
**Target Repository**: `C:\DL_PROJECT`  
**Audit Directory**: [`research/audit_reconciliation/`](file:///c:/DL_PROJECT/research/audit_reconciliation/)  
**Git Commit**: `8aff34c8249bcef10a3ecc63d7f347f3f0fbb4ef` (Branch: `main`)

---

## 1. What Was Inspected

A comprehensive, multi-layer inspection was conducted across all assets in the repository:
1. **Database & Exports**:
   - [`data/aegisops_live.sqlite3`](file:///c:/DL_PROJECT/data/aegisops_live.sqlite3) (86,016 bytes, SHA-256: `b8f33f63116ca4d081b8544f128e4e941ce0ce6fef39ff4f7e2c918ee0e94ff1`).
   - [`research/exports/telemetry.csv`](file:///c:/DL_PROJECT/research/exports/telemetry.csv), [`incident_episodes.csv`](file:///c:/DL_PROJECT/research/exports/incident_episodes.csv), [`incident_events.csv`](file:///c:/DL_PROJECT/research/exports/incident_events.csv).
2. **Model & Metadata**:
   - [`models/lstm_autoencoder.pt`](file:///c:/DL_PROJECT/models/lstm_autoencoder.pt) (19,893 bytes, SHA-256: `df867ce96bf423f03b87441fc9a957270d4944fa734b41a546da9b57564619d0`).
   - [`models/lstm_autoencoder.json`](file:///c:/DL_PROJECT/models/lstm_autoencoder.json) (hyperparameters: `input_dim=5, hidden_dim=32, seq_len=24, threshold=0.709399`).
3. **Machine-Readable Raw Predictions**:
   - [`research/raw/detection_predictions.csv`](file:///c:/DL_PROJECT/research/raw/detection_predictions.csv) ($N = 320$ windows).
   - [`research/raw/diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_predictions.csv) ($42$ evaluations across 6 ground-truth incidents).
   - [`research/raw/safety_test_results.csv`](file:///c:/DL_PROJECT/research/raw/safety_test_results.csv) ($N = 16$ test cases).
4. **Experiment Code & Evaluators**:
   - [`research/experiments/run_experiment_a.py`](file:///c:/DL_PROJECT/research/experiments/run_experiment_a.py) (Anomaly detection benchmark).
   - [`research/experiments/run_experiment_b.py`](file:///c:/DL_PROJECT/research/experiments/run_experiment_b.py) (Root-cause diagnosis runner).
   - [`research/experiments/generate_diagnosis_audit.py`](file:///c:/DL_PROJECT/research/experiments/generate_diagnosis_audit.py) (Standardized 4-tier rubric evaluator).
   - [`research/experiments/run_safety_audit.py`](file:///c:/DL_PROJECT/research/experiments/run_safety_audit.py) (Safety and recovery harness).
   - [`research/results/generate_statistical_analysis.py`](file:///c:/DL_PROJECT/research/results/generate_statistical_analysis.py) (Statistical test calculator).
   - [`research/run_all.py`](file:///c:/DL_PROJECT/research/run_all.py) (Unified reproducibility runner).
5. **Application Subsystems**:
   - [`approval.py`](file:///c:/DL_PROJECT/approval.py) (`ApprovalStore`, atomic SQLite locking).
   - [`agents.py`](file:///c:/DL_PROJECT/agents.py) (`GroqAgent`, `IncidentAgents`, `_local_root_cause`).
   - [`live_monitoring.py`](file:///c:/DL_PROJECT/live_monitoring.py) (collector, probe, recovery functions).
   - [`collectors/system_metrics.py`](file:///c:/DL_PROJECT/collectors/system_metrics.py) (URL validation, loopback checks).
   - [`demo_service/main.py`](file:///c:/DL_PROJECT/demo_service/main.py) (FastAPI target service).
6. **Publication Figures & Captions**:
   - [`research/figures/detection_confusion_matrices.png`](file:///c:/DL_PROJECT/research/figures/detection_confusion_matrices.png).
   - [`research/figures/detection_comparison.png`](file:///c:/DL_PROJECT/research/figures/detection_comparison.png).
   - [`research/figures/FIGURE_CAPTIONS.md`](file:///c:/DL_PROJECT/research/figures/FIGURE_CAPTIONS.md).

---

## 2. What Was Independently Recomputed

1. **Telemetry Class Census & Episode Tracing**:
   - Database total rows: exactly 200.
   - Normal rows: exactly 31.
   - Fault rows: exactly 169 (1 latency + 168 continuous error samples).
   - Workstation RAM excursions: EP-01 (4 samples), EP-02 (21 samples).
2. **Experiment A Anomaly Detection Metrics ($N = 320$)**:
   - Operational Rules (Implemented): $\text{TP}=120, \text{FP}=0, \text{TN}=200, \text{FN}=0$, Recall=100.0%, F1=1.0000.
   - Operational Rules (Physical Resource): $\text{TP}=40, \text{FP}=0, \text{TN}=200, \text{FN}=80$, Recall=33.3%, F1=0.5000.
   - Isolation Forest: $\text{TP}=57, \text{FP}=4, \text{TN}=196, \text{FN}=63$, Recall=47.5%, Precision=93.4%, F1=0.6298.
   - LSTM Autoencoder: $\text{TP}=120, \text{FP}=2, \text{TN}=198, \text{FN}=0$, Recall=100.0%, Precision=98.4%, F1=0.9917.
   - Combined Alert: $\text{TP}=120, \text{FP}=2, \text{TN}=198, \text{FN}=0$, Recall=100.0%, Precision=98.4%, F1=0.9917.
   - Exact McNemar Binomial Test (LSTM vs. IsoForest): $p = \mathbf{2.168 \times 10^{-19}}$ ($p < 0.001$).
   - Edwards Continuity-Corrected $\chi^2$: $\mathbf{61.02}$ ($p = 5.66 \times 10^{-15}$).
   - Paired Sensitivity Difference: $\Delta = \mathbf{+0.5250}$ (95% Wald CI: $[+0.4350, +0.6150]$).
   - Normal False Alarm Exact Test ($b=4, c=2$): $p = \mathbf{0.6875}$ (not statistically significant).
3. **Experiment B Diagnosis Metrics ($7 \text{ configs} \times 6 \text{ incidents} = 42$)**:
   - Multi-Agent Full (Live LLM, with DL): 83.3% strict ITT ($5/6$), 100.0% lenient ($6/6$).
   - Multi-Agent No-DL (Live LLM, without DL): 66.7% strict ITT ($4/6$), 83.3% lenient ($5/6$).
   - Single-Agent (Live LLM, with DL): 66.7% strict ITT ($4/6$).
   - Offline String Heuristic: Rule Baseline 100% ($6/6$); Offline with DL 50% ($3/6$) due to rule ordering.
4. **Experiment C Security Metrics ($N = 16$)**:
   - Adversarial Attack Containment: 11/11 (100.0%, 95% Wilson CI: $[0.7412, 1.0000]$).
   - Precondition Execution Safety: 2/2 (100.0%, 95% Wilson CI: $[0.3424, 1.0000]$).
   - Recovery Verification Integrity: 1/1 (100.0%, 95% Wilson CI: $[0.2065, 1.0000]$).
   - Positive Controls: 2/2 (100.0%, 95% Wilson CI: $[0.3424, 1.0000]$).
   - Unauthorized Execution Rate: 0.0% ($0/11$).
   - Replay Attack Rejection Rate: 100.0% ($1/1$).

---

## 3. Discrepancies Resolved

1. **Dataset Episode Count Discrepancy**: Reconciled the claimed 175 samples (28, 7, 98, 42) with the true 169 database fault rows (1 latency + 168 error). Traced row-by-row in `DATA_ROW_RECONCILIATION.csv`.
2. **Operational Rules Inconsistency**: Resolved the 33.3% recall (Figure 1) vs. 100.0% recall (Table) discrepancy by identifying the resource-only physical thresholds vs. end-to-end HTTP error rate condition.
3. **Diagnosis Evaluation Cohort**: Debunked the myth of 42 independent incidents; established the true factorial design of 7 configurations evaluated across the same 6 ground-truth incidents.
4. **Diagnosis With-DL vs. Without-DL Comparison**: Identified that prior claims of 100% without-DL were caused by dropping difficult or rate-limited cases from the denominator. On matched Intent-to-Treat, with-DL achieves 83.3% vs. 66.7% without-DL.
5. **Safety Evidence Taxonomy**: Resolved the monolithic "14/14 blocked attacks" claim into a rigorous 4-tier taxonomy: 11 attacks, 2 failure checks, 1 verification probe, and 2 positive controls.
6. **Binomial Calculation Bug**: Verified correction of the McNemar test defect ($b=4, c=2 \implies p=0.6875$, not $0.03125$).

---

## 4. Unresolved Discrepancies & Inherent Limitations

1. **Historical Telemetry Anomaly Scores**: `anomaly_score` is 100% NULL across all 200 rows in `data/aegisops_live.sqlite3`. This cannot and should not be modified; it reflects bootstrap rule mode and must be disclosed honestly.
2. **Host vs. Process Telemetry Coupling**: CPU and RAM metrics reflect the developer Windows workstation running background tasks, not the isolated microservice.
3. **Diagnostic Sample Size Ceiling**: The incident catalog contains exactly 6 scenarios ($N = 6$), yielding statistical power of only 14%. Comparative asymptotic significance cannot be claimed.
4. **Synthetic Telemetry Domain Gap**: Algorithmic superiority of the LSTM is demonstrated on synthetic sinusoids and polynomial ramps; real-world production telemetry validation remains future work.

---

## 5. Files Created in This Audit

All new audit files were authored into [`research/audit_reconciliation/`](file:///c:/DL_PROJECT/research/audit_reconciliation/):
1. `01_REPOSITORY_AND_EVIDENCE_INVENTORY.md` (Repository & evidence inventory)
2. `02_DATA_AND_LABEL_RECONCILIATION.md` (Dataset census & row-level reconciliation)
3. `03_DETECTION_METRIC_RECONCILIATION.md` (Exp A metrics recomputation)
4. `04_DIAGNOSIS_RECONCILIATION.md` (Exp B 7-configuration evaluation & ITT metrics)
5. `05_SAFETY_EVIDENCE_RECONCILIATION.md` (Exp C 16-case security taxonomy)
6. `06_STATISTICAL_AND_REPRODUCIBILITY_AUDIT.md` (Statistical testing & reproducibility)
7. `07_UPDATED_MASTER_CHECKLIST.md` (Updated 7-phase master research checklist)
8. `08_FINAL_AUDIT_SUMMARY.md` (This master summary report)

---

## 6. Commands Actually Executed

Every command executed during this audit was non-destructive and tracked:

| # | Exact Executed Command | CWD | Exit Code | Observed Output / Effect |
| :---: | :--- | :--- | :---: | :--- |
| 1 | `git status; git rev-parse HEAD; git branch --show-current; git log -n 3 --oneline` | `C:\DL_PROJECT` | `0` | Recorded clean working tree at commit `8aff34c8249bcef10a3ecc63d7f347f3f0fbb4ef` on branch `main`. |
| 2 | `.\.venv\Scripts\python.exe --version; .\.venv\Scripts\pip.exe list` | `C:\DL_PROJECT` | `0` | Recorded Python 3.11.9 and all 130 installed packages. |
| 3 | `.\.venv\Scripts\python.exe -m pytest -q` | `C:\DL_PROJECT` | `0` | Passed all 42 tests across 8 test suites in 17.11s. |
| 4 | `.\.venv\Scripts\python.exe research/run_all.py` | `C:\DL_PROJECT` | `0` | Full pipeline executed in 53.6s (42 tests, Exp A, rubric audit, Exp C, statistics, manifest). |
| 5 | `powershell -Command "Get-FileHash research\raw\* | Select-Object Algorithm, Hash, Path"` | `C:\DL_PROJECT` | `0` | Verified SHA-256 hashes of all raw prediction and metric files. |
| 6 | Database queries on `data/aegisops_live.sqlite3` | `C:\DL_PROJECT` | `0` | Verified 200 telemetry samples, 11 incident events, 0 recovery approvals. |

---

## 7. Execution Failures Documented

1. **Host Python Global Interpreter Failure**: Running `python -m pytest -q` with global Python failed on `test_live_monitoring.py` due to `ModuleNotFoundError: No module named 'streamlit'`. Resolved by requiring execution within `.venv\Scripts\python.exe`.
2. **Prior Live Groq Cloud LLM Dropouts**: During the original execution of `run_experiment_b.py`, free-tier Groq API rate limits and timeouts caused INC-1002 (Config 5) and INC-1004 (Config 7) to fail. Resolved by implementing standardized Intent-to-Treat accounting.

---

## 8. Revised Master Checklist Status

- **Phase 1 (Repository Inventory & Baseline)**: **VERIFIED COMPLETE**
- **Phase 2 (Dataset & Episode Reconciliation)**: **VERIFIED COMPLETE**
- **Phase 3 (Anomaly Detection Benchmark)**: **VERIFIED COMPLETE**
- **Phase 4 (Root-Cause Diagnosis Benchmark)**: **VERIFIED COMPLETE**
- **Phase 5 (Execution Boundary Safety)**: **VERIFIED COMPLETE**
- **Phase 6 (Reproducibility Pipeline & Manifest)**: **VERIFIED COMPLETE**
- **Phase 7 (Research-Paper Completion)**: **NOT STARTED** (Ready for authoring)

---

## 9. Next Three Highest-Priority Actions

1. **Action 1: Author Camera-Ready Manuscript (Phase 7)**:
   Draft the complete research paper incorporating the reconciled metrics:
   - Report dual-definition rules baseline (33.3% physical vs. 100% error-rate).
   - Report Intent-to-Treat diagnosis metrics (83.3% Full vs. 66.7% No-DL) with explicit disclosure of $N=6$ pilot power constraints.
   - Report 11/11 attacks blocked with Wilson CI $[0.7412, 1.0000]$.
2. **Action 2: Embed Verified Figures & Reconciled Captions**:
   Embed Figures 1 and 2 in the manuscript, updating Figure 1's caption to explain the operational distinction between physical resource monitoring and late-stage error alerting.
3. **Action 3: Compile Complete Submission Package**:
   Perform final cross-referencing between manuscript text, machine-readable CSVs, and [`research/MANIFEST_SHA256.json`](file:///c:/DL_PROJECT/research/MANIFEST_SHA256.json).

---

## 10. Clear Distinction of Research Evidence

| Category | Item Description | Supporting Evidence File |
| :--- | :--- | :--- |
| **Verified Fact** | SQLite DB contains 200 rows: 31 normal, 1 latency, 168 error. | [`data/aegisops_live.sqlite3`](file:///c:/DL_PROJECT/data/aegisops_live.sqlite3), [`DATA_ROW_RECONCILIATION.csv`](file:///c:/DL_PROJECT/research/audits/reconciliation_gate_20261012/DATA_ROW_RECONCILIATION.csv) |
| **Verified Fact** | Historical DB contains zero neural inferences (`anomaly_score = NULL`). | [`data/aegisops_live.sqlite3`](file:///c:/DL_PROJECT/data/aegisops_live.sqlite3), [`02_DATA_AND_LABEL_RECONCILIATION.md`](file:///c:/DL_PROJECT/research/audit_reconciliation/02_DATA_AND_LABEL_RECONCILIATION.md) |
| **Verified Fact** | LSTM Autoencoder achieves 100% recall on 120 synthetic fault episodes vs. 47.5% for IsoForest ($p = 2.168 \times 10^{-19}$). | [`research/raw/detection_predictions.csv`](file:///c:/DL_PROJECT/research/raw/detection_predictions.csv), [`03_DETECTION_METRIC_RECONCILIATION.md`](file:///c:/DL_PROJECT/research/audit_reconciliation/03_DETECTION_METRIC_RECONCILIATION.md) |
| **Verified Fact** | Multi-Agent Full LLM achieves 83.3% strict ITT accuracy across all 6 ground-truth incidents. | [`research/raw/diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_predictions.csv), [`04_DIAGNOSIS_RECONCILIATION.md`](file:///c:/DL_PROJECT/research/audit_reconciliation/04_DIAGNOSIS_RECONCILIATION.md) |
| **Verified Fact** | Execution boundary blocks 11/11 adversarial attacks and safely aborts 2/2 precondition checks. | [`research/raw/safety_test_results.csv`](file:///c:/DL_PROJECT/research/raw/safety_test_results.csv), [`05_SAFETY_EVIDENCE_RECONCILIATION.md`](file:///c:/DL_PROJECT/research/audit_reconciliation/05_SAFETY_EVIDENCE_RECONCILIATION.md) |
| **Verified Fact** | Unified runner `run_all.py` passes 42 tests and generates manifest in 53.6s. | Execution trace, [`research/MANIFEST_SHA256.json`](file:///c:/DL_PROJECT/research/MANIFEST_SHA256.json) |
| **Disproven Claim** | "Historical DB contains 4 reconstructed episodes with 28, 7, 98, 42 samples." | Disproven: Database has 1 latency sample and 1 continuous 168-sample error burst. |
| **Disproven Claim** | "Multi-Agent without DL achieved 100% accuracy vs. with DL 83.3%." | Disproven: Without DL dropped INC-1004. On matched ITT, with DL is 83.3% vs. 66.7%. |
| **Disproven Claim** | "14 of 14 attacks blocked." | Disproven: Conflated 2 failure precondition checks and 1 verification check with attacks. Attacks blocked is 11/11. |
| **Unresolved Boundary** | Generalization to live multi-cloud enterprise production telemetry. | Outside scope of local benchmark; documented as primary future work. |
