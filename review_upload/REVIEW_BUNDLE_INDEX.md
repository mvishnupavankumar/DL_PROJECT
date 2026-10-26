# AegisOps: Independent Review Bundles Index & Verification Manifest

**Location**: `C:\DL_PROJECT\review_upload`  
**Date**: October 14, 2026  
**Auditor**: Senior ML Research Supervisor, Statistical Auditor & Reproducibility Reviewer  
**Repository Working Tree**: `C:/DL_PROJECT`  
**Git Branch**: `publish/research-without-external-dataset`  
**Git HEAD**: `a32713c30a8ddca1425d44b1afbaf6d55a64c276`  
**Historical Audited Baseline Commit**: `ec83d2fe501ba50f56839944ba7bd6347544f585` (on `main`)  
**Standard**: Upload-Ready Review Bundle Packaging & Read-Only Preservation  

---

## 1. Executive Summary & Review Bundle Register

Three upload-ready review ZIP archives have been generated from the active working tree of `C:\DL_PROJECT` to facilitate exhaustive, independent evaluation of the AegisOps research project. Every archive was generated in read-only mode without staging, committing, or altering existing repository assets.

All three bundles were independently verified via automated CRC32 checksum inspection (`zipfile.testzip()`), confirming zero extraction errors.

| Bundle Name | Primary Purpose | File Size (Bytes) | File Size (KB) | Entries Count | SHA-256 Checksum | Integrity Status |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: |
| `01_manuscript_and_evidence.zip` | Complete manuscript, figure assets, canonical raw CSVs, derived results, and SHA-256 manifest | 186,721 | 182.34 KB | 36 | `75bd73d1f537dfb0b825a8535020e0fcfe2e88434891011b48c29db4fe4b0367` | **VERIFIED VALID** (Zero CRC Errors) |
| `02_source_code_and_tests.zip` | Application source modules, automated test suites, experiment runners, scripts, frozen model checkpoint, and verified test logs | 148,519 | 145.04 KB | 59 | `ba3735cb1413300783e7e4e765519d8811dd8e38b1c7ad15f6b592909064aa30` | **VERIFIED VALID** (Zero CRC Errors) |
| `03_audits_and_git_changes.zip` | Master handoff, seven-phase checklist, integrity reconciliation, Experiment D audits, and captured Git status/diff patches | 641,766 | 626.72 KB | 115 | `ed6da11cfb659d8df0b8b9261eb63f5786ce77b6d433c3dd4ae08ce1d35d626c` | **VERIFIED VALID** (Zero CRC Errors) |

---

## 2. Excluded Categories and Rationale

In strict compliance with repository hygiene, artifact safety, and upload size standards, the following asset categories were intentionally excluded from all bundles:

| Excluded Category | Specific Path / Patterns | Technical Rationale for Exclusion |
| :--- | :--- | :--- |
| **Git Metadata** | `.git/` tree, hooks, index | Redundant and bulky; repository state is fully captured via `git status`, branch/HEAD records, and diff patches in Bundle 3. |
| **Python Virtual Environment** | `.venv/` tree (1.2 GB) | Machine-specific binaries, compiled C-extensions, and site-packages. Dependencies are specified portably in `requirements.txt`. |
| **Bytecode & Test Caches** | `__pycache__/`, `.pytest_cache/` | Ephemeral runtime artifacts; re-created deterministically on test execution. |
| **Environment Secrets** | `.env` | Contains local development environment variables; security standard forbids archiving credentials. `SECURITY.md` and `.env.example` are provided. |
| **Runtime SQLite Databases** | `data/aegisops_live.sqlite3`, `data/safety_telemetry.sqlite3`, `data/safety_test_store.sqlite3` | Live telemetry databases (86 KB - 2.5 MB) containing runtime locks and WAL logs. Recreated deterministically by test harnesses. Schema is audited in `DATABASE_AUDIT.md`. |
| **External Benchmark Archive** | `data/external/anomod/` (38,349 files, >200 MB), `AnoMod.zip` | Excluded under the Supervisor-Ratified Path 3 Bounded-Claims Policy; external validation is excluded from immediate manuscript claims and deferred to future work. Provenance is preserved in `ANOMOD_DATASET_INSPECTION.md`. |
| **Historical Backup Files** | `*.bak` files (e.g. `live_monitoring.py.*.bak`, `telemetry_store.py.*.bak`) | Obsolete pre-fix backups superseded by current tracked code. |
| **Packaging Staging Folders** | `review_upload/` | Self-referential recursion prevention. |

---

## 3. Comprehensive Bundle Content Inventory

### Bundle: `01_manuscript_and_evidence.zip`
- **File Path**: `C:\DL_PROJECT\review_upload\01_manuscript_and_evidence.zip`
- **File Size**: 186,721 bytes (182.34 KB)
- **Uncompressed Size**: 433,360 bytes
- **SHA-256**: `75bd73d1f537dfb0b825a8535020e0fcfe2e88434891011b48c29db4fe4b0367`
- **Total Files**: 36

<details>
<summary>Click to expand complete inventory of 36 files in 01_manuscript_and_evidence.zip</summary>

```text
research/paper/00_MANUSCRIPT_EVIDENCE_GATE.md
research/paper/AEGISOPS_RESEARCH_PAPER.md
research/paper/BOUNDED_CLAIMS_DECISION.md
research/paper/CANONICAL_METRIC_RECONCILIATION.md
research/paper/FIGURE_AND_TABLE_INDEX.md
research/paper/FIGURE_AND_TABLE_REGISTER.md
research/paper/FINAL_EVIDENCE_AUDIT.md
research/paper/FINAL_MANUSCRIPT_CHECKLIST.md
research/paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md
research/paper/MANUSCRIPT_EVIDENCE_MATRIX.md
research/paper/MANUSCRIPT_FINALIZATION_PLAN.md
research/paper/REFERENCES_VERIFICATION.md
research/paper/REFERENCE_VERIFICATION.md
research/paper/figures/approval_recovery_workflow.mmd
research/paper/figures/architecture_dataflow.mmd
research/paper/figures/detection_comparison.png
research/paper/figures/detection_confusion_matrices.png
research/paper/figures/detection_diagnosis_workflow.mmd
research/raw/detection_by_scenario.csv
research/raw/detection_metrics.csv
research/raw/detection_predictions.csv
research/raw/diagnosis_metrics.csv
research/raw/diagnosis_predictions.csv
research/raw/safety_metrics.csv
research/raw/safety_test_results.csv
research/results/detection_by_scenario.csv
research/results/detection_metrics.csv
research/results/detection_predictions.csv
research/results/diagnosis_metrics.csv
research/results/diagnosis_predictions.csv
research/results/generate_statistical_analysis.py
research/results/safety_metrics.csv
research/results/safety_test_results.csv
research/results/statistical_analysis.md
research/MANIFEST_SHA256.json
BUNDLE_1_README.md
```
</details>

---

### Bundle: `02_source_code_and_tests.zip`
- **File Path**: `C:\DL_PROJECT\review_upload\02_source_code_and_tests.zip`
- **File Size**: 148,519 bytes (145.04 KB)
- **Uncompressed Size**: 457,757 bytes
- **SHA-256**: `ba3735cb1413300783e7e4e765519d8811dd8e38b1c7ad15f6b592909064aa30`
- **Total Files**: 59

<details>
<summary>Click to expand complete inventory of 59 files in 02_source_code_and_tests.zip</summary>

```text
README.md
SECURITY.md
WINDOWS_DEPLOYMENT.md
agents.py
app.py
approval.py
config.py
live_monitoring.py
requirements.txt
research_automation.py
research_pipeline.py
simulator.py
collectors/README.md
collectors/__init__.py
collectors/system_metrics.py
collectors/worker.py
demo_service/__init__.py
demo_service/main.py
dl/__init__.py
dl/anomaly_detector.py
dl/evaluate_detector.py
dl/live_training.py
dl/train_from_csv.py
dl/train_model.py
storage/__init__.py
storage/telemetry_store.py
test_agents.py
test_anomaly_detector.py
test_approval.py
test_experiment_d_harness.py
test_ingest_anomod.py
test_live_monitoring.py
test_research_instrumentation.py
test_simulator.py
test_statistical_audit.py
test_target_security.py
test_workflow.py
research/experiments/EXPERIMENT_A.md
research/experiments/EXPERIMENT_B.md
research/experiments/EXPERIMENT_C.md
research/experiments/generate_diagnosis_audit.py
research/experiments/plot_detection_figures.py
research/experiments/run_experiment_a.py
research/experiments/run_experiment_b.py
research/experiments/run_experiment_c.py
research/experiments/run_experiment_d.py
research/experiments/run_safety_audit.py
research/scripts/audit_temporal_eligibility.py
research/scripts/ingest_anomod.py
research/scripts/smoke_test_checkpoint.py
models/lstm_autoencoder.pt
models/lstm_autoencoder.json
test_logs/task-3502.log
test_logs/task-3108.log
test_logs/task-3429.log
test_logs/task-3284.log
test_logs/pytest_run.log
test_logs/TEST_LOGS_PROVENANCE.md
BUNDLE_2_README.md
```
</details>

---

### Bundle: `03_audits_and_git_changes.zip`
- **File Path**: `C:\DL_PROJECT\review_upload\03_audits_and_git_changes.zip`
- **File Size**: 641,766 bytes (626.72 KB)
- **Uncompressed Size**: 1,607,224 bytes
- **SHA-256**: `ed6da11cfb659d8df0b8b9261eb63f5786ce77b6d433c3dd4ae08ce1d35d626c`
- **Total Files**: 115

<details>
<summary>Click to expand complete inventory of 115 files in 03_audits_and_git_changes.zip</summary>

```text
research/audits/AEGISOPS_MASTER_RESEARCH_HANDOFF.md
research/audits/ANOMOD_DATASET_INSPECTION.md
research/audits/BOUNDED_CLAIMS_DECISION.md
research/audits/DATABASE_AUDIT.md
research/audits/DATA_ROW_RECONCILIATION.csv
research/audits/DETECTION_RECONCILIATION.md
research/audits/DIAGNOSIS_RECONCILIATION.md
research/audits/EVIDENCE_RECONCILIATION_REPORT.md
research/audits/EXPERIMENT_D_CALIBRATION_INDEPENDENCE_AUDIT.md
research/audits/EXPERIMENT_D_DECISION_PACKET_VERIFICATION.md
research/audits/EXPERIMENT_D_FINAL_METHOD_DECISION.md
research/audits/EXPERIMENT_D_FINAL_SUPERVISOR_DECISION.md
research/audits/EXPERIMENT_D_HUMAN_DECISION_PACKET.md
research/audits/EXPERIMENT_D_HUMAN_METHOD_DECISION_V2.md
research/audits/EXPERIMENT_D_IMPLEMENTATION_REVIEW.md
research/audits/EXPERIMENT_D_PREFLIGHT_AND_HARNESS_GATE.md
research/audits/EXPERIMENT_D_PROTOCOL_RECONCILIATION.md
research/audits/EXPERIMENT_D_READINESS_REAUDIT.md
research/audits/EXPERIMENT_D_READINESS_VERDICT.md
research/audits/EXPERIMENT_D_REMEDIATION_CHANGELOG.md
research/audits/EXPERIMENT_D_REQUIREMENTS_TRACEABILITY.md
research/audits/EXPERIMENT_D_SEQUENCE_COMPATIBILITY_DECISION.md
research/audits/EXPERIMENT_D_STATISTICAL_ACCEPTANCE_CRITERIA.md
research/audits/EXPERIMENT_D_STATISTICAL_VALIDITY_REAUDIT.md
research/audits/EXPERIMENT_D_TEST_RESULTS.md
research/audits/EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md
research/audits/EXPERIMENT_D_ZERO_SHOT_IMPLEMENTATION_PLAN.md
research/audits/FINAL_REPOSITORY_INTEGRITY_RECONCILIATION.md
research/audits/MANUSCRIPT_CONSISTENCY_AUDIT.md
research/audits/MODEL_AND_EXECUTION_AUDIT.md
research/audits/PHASE8_CHECKLIST_RECONCILIATION.md
research/audits/PHASE9_EXTERNAL_VALIDATION_READINESS.md
research/audits/PHASE_1_VERDICT.md
research/audits/PIPELINE_REPRODUCIBILITY.md
research/audits/PRE_PHASE9_EVIDENCE_INTEGRITY_GATE.md
research/audits/PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md
research/audits/README.md
research/audits/REPOSITORY_AUDIT.md
research/audits/SAFETY_RECONCILIATION.md
research/audits/STATISTICAL_INTEGRITY_AND_INGESTION_PREFLIGHT.md
research/audits/TEST_RESULTS.md
research/audits/UPDATED_SEVEN_PHASE_CHECKLIST.md
research/audits/experiment_d_temporal_eligibility_audit.json
research/audits/2026-10-12/DATABASE_AUDIT.md
research/audits/2026-10-12/MODEL_AND_EXECUTION_AUDIT.md
research/audits/2026-10-12/PHASE_1_VERDICT.md
research/audits/2026-10-12/REPOSITORY_AUDIT.md
research/audits/2026-10-12/TEST_RESULTS.md
research/audits/detection_closure_gate_20261012/COMMAND_LOGS_AND_EXIT_CODES.md
research/audits/detection_closure_gate_20261012/DETECTION_FIGURE_VERIFICATION.md
research/audits/detection_closure_gate_20261012/DETECTION_METRIC_RECONCILIATION.md
research/audits/detection_closure_gate_20261012/ISOLATION_FOREST_REPRODUCIBILITY.md
research/audits/detection_closure_gate_20261012/RECOMPUTED_DETECTION_METRICS.csv
research/audits/detection_closure_gate_20261012/TWO_RUN_REPRODUCIBILITY_COMPARISON.csv
research/audits/detection_closure_gate_20261012/UPDATED_SEVEN_PHASE_CHECKLIST.md
research/audits/detection_closure_gate_20261012/figures/detection_comparison.png
research/audits/detection_closure_gate_20261012/figures/detection_confusion_matrices.png
research/audits/detection_figure_verification_20261012/DETECTION_DISCREPANCIES.md
research/audits/detection_figure_verification_20261012/DETECTION_FIGURE_VERIFICATION.md
research/audits/detection_figure_verification_20261012/DETECTION_METRIC_RECALCULATION.csv
research/audits/detection_figure_verification_20261012/UPDATED_PHASE_CHECKLIST.md
research/audits/detection_rate_and_phase4_gate_20261012/COMMAND_LOGS_AND_HASHES.md
research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv
research/audits/detection_rate_and_phase4_gate_20261012/PHASE4_READINESS_REVIEW.md
research/audits/detection_rate_and_phase4_gate_20261012/STATISTICAL_ASSUMPTION_REVIEW.md
research/audits/detection_rate_and_phase4_gate_20261012/UPDATED_SEVEN_PHASE_CHECKLIST.md
research/audits/detection_rate_and_phase4_gate_20261012/WINDOW_EXPOSURE_AND_ALARM_RATE_AUDIT.md
research/audits/phase3_final_reproducibility_20261012/FIGURE_CAPTION_VERIFICATION.md
research/audits/phase3_final_reproducibility_20261012/ISOLATION_FOREST_REPRODUCIBILITY_AUDIT.md
research/audits/phase3_final_reproducibility_20261012/TWO_RUN_REPRODUCIBILITY_COMPARISON.csv
research/audits/phase3_final_reproducibility_20261012/UPDATED_PHASE_CHECKLIST.md
research/audits/phase3_final_reproducibility_20261012/run_1/detection_by_scenario_run1.csv
research/audits/phase3_final_reproducibility_20261012/run_1/detection_comparison_run1.png
research/audits/phase3_final_reproducibility_20261012/run_1/detection_confusion_matrices_run1.png
research/audits/phase3_final_reproducibility_20261012/run_1/detection_metrics_run1.csv
research/audits/phase3_final_reproducibility_20261012/run_1/detection_predictions_run1.csv
research/audits/phase3_final_reproducibility_20261012/run_1/stdout.log
research/audits/phase3_final_reproducibility_20261012/run_2/detection_by_scenario_run2.csv
research/audits/phase3_final_reproducibility_20261012/run_2/detection_comparison_run2.png
research/audits/phase3_final_reproducibility_20261012/run_2/detection_confusion_matrices_run2.png
research/audits/phase3_final_reproducibility_20261012/run_2/detection_metrics_run2.csv
research/audits/phase3_final_reproducibility_20261012/run_2/detection_predictions_run2.csv
research/audits/phase3_final_reproducibility_20261012/run_2/stdout.log
research/audits/phase8_external_validation/EXTERNAL_DATASET_FEASIBILITY.md
research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md
research/audits/phase8_external_validation/PHASE8_FINAL_REPORT.md
research/audits/phase8_external_validation/REPRODUCIBILITY_CLOSURE.md
research/audits/phase8_external_validation/run_1/detection_by_scenario.csv
research/audits/phase8_external_validation/run_1/detection_metrics.csv
research/audits/phase8_external_validation/run_1/detection_predictions.csv
research/audits/phase8_external_validation/run_1/stdout.log
research/audits/phase8_external_validation/run_2/detection_by_scenario.csv
research/audits/phase8_external_validation/run_2/detection_metrics.csv
research/audits/phase8_external_validation/run_2/detection_predictions.csv
research/audits/phase8_external_validation/run_2/stdout.log
research/audits/reconciliation_gate_20261012/DATA_ROW_RECONCILIATION.csv
research/audits/reconciliation_gate_20261012/DETECTION_RECONCILIATION.md
research/audits/reconciliation_gate_20261012/DIAGNOSIS_RECONCILIATION.md
research/audits/reconciliation_gate_20261012/EVIDENCE_RECONCILIATION_REPORT.md
research/audits/reconciliation_gate_20261012/PIPELINE_REPRODUCIBILITY.md
research/audits/reconciliation_gate_20261012/SAFETY_RECONCILIATION.md
research/audits/reconciliation_gate_20261012/UPDATED_SEVEN_PHASE_CHECKLIST.md
research/audits/rule_baseline_finalization_20261012/DETECTION_DISCREPANCIES.md
research/audits/rule_baseline_finalization_20261012/DETECTION_METRIC_RECALCULATION.csv
research/audits/rule_baseline_finalization_20261012/UPDATED_PHASE_CHECKLIST.md
git_records/GIT_BRANCH_AND_HEAD.txt
git_records/GIT_DIFF_CHECK.txt
git_records/GIT_STATUS_PORCELAIN_V2.txt
git_records/GIT_STATUS_SHORT.txt
git_records/diffs/GIT_DIFF_ALL.patch
git_records/diffs/GIT_DIFF_CODE.patch
git_records/diffs/GIT_DIFF_DOCS.patch
git_records/diffs/GIT_DIFF_RAW_CSVS.patch
git_records/diffs/GIT_DIFF_RESULTS_CSVS.patch
BUNDLE_3_README.md
```
</details>

---

## 4. Verification and Review Instructions

### How to Unpack and Review:
1. **Manuscript & Quantitative Verification (Bundle 1)**:
   - Unpack `01_manuscript_and_evidence.zip`.
   - Review `research/paper/AEGISOPS_RESEARCH_PAPER.md` against `CANONICAL_METRIC_RECONCILIATION.md` and raw CSV records in `research/raw/`.
   - Cross-check Table 1, Table 2, Table 3, Table 4, and Table 5 against `FIGURE_AND_TABLE_INDEX.md`.

2. **Code & Regression Execution (Bundle 2)**:
   - Unpack `02_source_code_and_tests.zip` into a clean Python 3.11 environment.
   - Run `pip install -r requirements.txt`.
   - Inspect `test_logs/TEST_LOGS_PROVENANCE.md` to review the recorded 107-test and 18-test clean execution logs.
   - Run `pytest test_experiment_d_harness.py` to confirm the 40 harness preflight contract checks.

3. **Audits & Integrity Validation (Bundle 3)**:
   - Unpack `03_audits_and_git_changes.zip`.
   - Inspect `research/audits/FINAL_REPOSITORY_INTEGRITY_RECONCILIATION.md` for the complete 22-artifact manifest verification and reconciliation.
   - Inspect `git_records/diffs/` to review line-by-line working-tree modifications.

**Final Status**: All three bundles are fully verified, self-contained, and ready for independent human review.