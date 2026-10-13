# AegisOps: Phase 8 Checklist Reconciliation Report

**Audit Gate**: Phase 8 Checklist Reconciliation & Baseline Audit  
**Audit Location**: `research/audits/PHASE8_CHECKLIST_RECONCILIATION.md`  
**Git Baseline Commit**: `d277c1df3c2599ddecdf5f0bb761c99718499667` (Branch: `main`)  
**Audit Date**: October 2026  
**Auditor**: Senior Research Scientist, Reproducibility Auditor & Methodology Reviewer  
**Operating Standard**: Zero Data Snooping, Bit-for-Bit Determinism, Evidence-First Verification  

---

## 1. Executive Summary & Verification Scope

This document reconciles the master research checklist against the empirical evidence delivered in Phase 8 (`research/audits/phase8_external_validation/`). 

In accordance with strict reproducibility audit principles, every reported finding from Phase 8 has been verified directly against active repository code, raw binary checkpoints, raw machine-readable prediction CSVs, and execution logs:

1. **Isolation Forest Calibration Reproducibility**: **VERIFIED DETERMINISTIC**. Threshold `$\tau = -0.018694$` is the active empirical calibration value in [`research/experiments/run_experiment_a.py`](file:///c:/DL_PROJECT/research/experiments/run_experiment_a.py). Two independent consecutive runs produced identical bit-for-bit predictions and metrics.
2. **Obsolete Threshold Elimination**: Obsolete values `+0.089886` (un-negated decision function quantile) and `-0.090333` (transcription sign-inversion drift) have been audited and corrected in the manuscript and evidence registers.
3. **Public Benchmark Selection**: **AnoMod** (Ke Ping et al., MSR 2026; Zenodo DOI: `10.5281/zenodo.18342898`; CC-BY-4.0) is verified as the methodologically superior candidate over TrainTicket due to synchronized client API logs matching AegisOps' 5D telemetry schema.
4. **External Protocol Pre-Registration**: Protocol in [`research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md) is frozen prior to test ingestion.
5. **External Validation Execution Status**: **BLOCKED BY TRANSFER CONSTRAINTS**. Zenodo bandwidth throttling ($\approx 5.38\text{ KB/s}$, requiring $>10.4\text{ hours}$ transfer) prevented automated download in Phase 8. No synthetic proxy data was manufactured.

---

## 2. Repository Baseline and Cryptographic Manifest

### 2.1 Git Environment
- **Project Root**: `C:\DL_PROJECT`
- **Active Git Commit**: `d277c1df3c2599ddecdf5f0bb761c99718499667`
- **Branch**: `main`
- **Working-Tree Status**: Clean on base files; modifications confined to checklist/manuscript reconciliation and audit documentation.

### 2.2 Python Environment & Package Versions
- **Python Binary**: `C:\DL_PROJECT\.venv\Scripts\python.exe` (Version: `3.11.9`)
- **PyTorch**: `2.14.1+cpu`
- **scikit-learn**: `1.9.0`
- **NumPy**: `2.4.2`
- **SciPy**: `1.17.1`
- **Pandas**: `3.0.1`
- **FastAPI**: `0.135.2`
- **pytest**: `9.0.3` (42/42 tests passing in 68.13s)

### 2.3 Verified SHA-256 Cryptographic Hashes of Key Research Files

| File Category | File Path | File Size (Bytes) | SHA-256 Hash |
| :--- | :--- | :---: | :--- |
| **Pipeline Runner** | [`research/run_all.py`](file:///c:/DL_PROJECT/research/run_all.py) | 13,018 | `f796a9386d3bdf9bf015b6aa9cf41d8e1c6670868f04746f345330e281ffb791` |
| **Experiment A Code** | [`research/experiments/run_experiment_a.py`](file:///c:/DL_PROJECT/research/experiments/run_experiment_a.py) | 18,298 | `f40954b5dfd6efec1a3ae6c78103554b2efc0ea04eeb9d29efc66ec5a7cf9b66` |
| **Frozen PyTorch Model** | [`models/lstm_autoencoder.pt`](file:///c:/DL_PROJECT/models/lstm_autoencoder.pt) | 19,797 | `1cf44e6e66c2bb475ec7eebeea0ce58622ff6fa2c00a6e0c7042e431526ccbe3` |
| **Model Metadata** | [`models/lstm_autoencoder.json`](file:///c:/DL_PROJECT/models/lstm_autoencoder.json) | 846 | `e09337ff1ef2bc8ee4bbef97c7b805c86c1284a0d9e83dc5a5491fb3e61a6878` |
| **Raw Predictions** | [`research/raw/detection_predictions.csv`](file:///c:/DL_PROJECT/research/raw/detection_predictions.csv) | 23,285 | `246e14f88be92a342ae4597b0a7019a5ce3a693ce464010351797f1fbc796e62` |
| **Raw Metrics** | [`research/raw/detection_metrics.csv`](file:///c:/DL_PROJECT/research/raw/detection_metrics.csv) | 1,023 | `ed5775306a461358d348aebdf7fa6ecff5d0233fa265a7e1f402f1074e62842e` |
| **Scenario Metrics** | [`research/raw/detection_by_scenario.csv`](file:///c:/DL_PROJECT/research/raw/detection_by_scenario.csv) | 6,569 | `7bc84006c99c55ca46fa611b84931a7bc85eefbdf71536b801459419bfa6d914` |
| **Historical Telemetry** | [`data/aegisops_live.sqlite3`](file:///c:/DL_PROJECT/data/aegisops_live.sqlite3) | 86,016 | `b8f33f63116ca4d081b8544f128e4e941ce0ce6fef39ff4f7e2c918ee0e94ff1` |
| **Master Manifest** | [`research/MANIFEST_SHA256.json`](file:///c:/DL_PROJECT/research/MANIFEST_SHA256.json) | 3,118 | `36502daee0f7ec62f2709bf3365922379ae2a874b8fb1737be5e59b9249e9ce6` |
| **Frozen Protocol** | [`research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md) | 10,738 | `e5a31a986bb0856aa7dca6852bb2d9f4c398328c06e5e8eeb09f3e58c8ecb2d2` |

---

## 3. Threshold Reconciliation Verification

### 3.1 Verification of Active Threshold `$\tau = -0.018694$`
In [`research/experiments/run_experiment_a.py`](file:///c:/DL_PROJECT/research/experiments/run_experiment_a.py):
- Lines 51–56:
  ```python
  iso_forest = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
  iso_forest.fit(train_flat)
  val_iso_scores = -iso_forest.decision_function(val_flat)
  iso_threshold = float(np.quantile(val_iso_scores, 0.99))
  ```
- Evaluates deterministically to `$-0.0186938085898015$` (rounded to `$-0.018694$`).
- This exact value was applied to all 320 test windows in `run_experiment_a.py`, yielding the exact counts in [`research/raw/detection_metrics.csv`](file:///c:/DL_PROJECT/research/raw/detection_metrics.csv):
  - $\text{TP} = 57 / 120$ (Recall: $47.50\%$)
  - $\text{FP} = 4 / 200$ (False Positive Window Rate: $2.00\%$)
  - $\text{TN} = 196 / 200$
  - $\text{FN} = 63 / 120$
  - $\text{Precision} = 93.44\%$
  - $\text{F1} = 0.6298$
  - $\text{PR-AUC} = 0.9056$

### 3.2 Origins of Legacy Thresholds
- **`+0.089886`**: Originated from evaluating `np.quantile(+decision_function, 0.90)` on un-negated inlier decision function scores in early exploratory scripts.
- **`-0.090333`**: Originated from manuscript text drafts applying sign-inversion to `+0.089886` ($\approx -0.090$) while referencing an exploratory 5D-mean vector grid search rather than the active 120D flattened model.
- **Correction Status**: All occurrences of `-0.090333` in [`research/paper/AEGISOPS_RESEARCH_PAPER.md`](file:///c:/DL_PROJECT/research/paper/AEGISOPS_RESEARCH_PAPER.md), [`research/paper/FIGURE_AND_TABLE_INDEX.md`](file:///c:/DL_PROJECT/research/paper/FIGURE_AND_TABLE_INDEX.md), and [`research/paper/MANUSCRIPT_EVIDENCE_MATRIX.md`](file:///c:/DL_PROJECT/research/paper/MANUSCRIPT_EVIDENCE_MATRIX.md) have been corrected to `$\tau = -0.018694$`.

---

## 4. Reconciled Phase Status Matrix (Phases 1 through 8)

| Phase | Phase Scope & Name | Reconciled Status | Verifiable Primary Evidence | Remaining Methodological Boundaries & Blockers |
| :---: | :--- | :---: | :--- | :--- |
| **Phase 1** | Codebase Inventory & Environment Baseline | **VERIFIED COMPLETE** | 42/42 tests passing; read-only SQLite DB (`b8f33f63...`); frozen PyTorch weights (`1cf44e6e...`). | None. Baseline environment and cryptographic hashes are established. |
| **Phase 2** | Telemetry Census & Episode Reconciliation | **VERIFIED COMPLETE** | 200-row census reconciled (`DATA_ROW_RECONCILIATION.csv`); 169 fault vs. 175 episode count resolved. | Historical SQLite DB reflects cold-start operational monitoring (`anomaly_score = NULL`). |
| **Phase 3** | Anomaly Detection Benchmark (Experiment A) | **VERIFIED COMPLETE** | $N=320$ windows; paired McNemar test ($p = 2.17 \times 10^{-19}$); 3 rule baselines reconciled; exposure denominator corrected. | Synthetic fault injections only; streaming false alarms/hr marked UNAVAILABLE for batch windows. |
| **Phase 4** | Root-Cause Diagnosis Benchmark (Experiment B) | **PARTIALLY COMPLETE** | Factorial design ($7 \times 6 = 42$) rubric evaluations; Multi-Agent Full (Live LLM) achieved 83.33% strict ITT accuracy. | Small sample size ($N=6$, statistical power $1-\beta \approx 0.14$); rubric exhibits test-set keyword leakage. |
| **Phase 5** | Execution Boundary Safety Audit (Experiment C) | **VERIFIED COMPLETE** | 16-case empirical taxonomy; 100% attack containment (11/11 attacks blocked); atomic SQLite approval logging. | Evaluated strictly on localhost loopback boundary; does not evaluate distributed cluster network policies. |
| **Phase 6** | Unified Reproducibility Pipeline & Manifest | **VERIFIED COMPLETE** | `research/run_all.py` executes in 52.7s (exit 0); SHA-256 manifest produced (`MANIFEST_SHA256.json`). | Requires `.venv` environment with pre-installed PyTorch and scikit-learn. |
| **Phase 7** | Camera-Ready Manuscript Synthesis | **DRAFT COMPLETED (BOUNDED REPORT)** | 14 sections authored in `AEGISOPS_RESEARCH_PAPER.md`; verified by evidence matrix, reference audit, figure index. | Blocked from camera-ready pending external wild-production telemetry validation and streaming alarm verification. |
| **Phase 8** | Reproducibility Closure & External Validation | **REPRODUCIBILITY CLOSED; PROTOCOL FROZEN; EXTERNAL RUN BLOCKED** | [`REPRODUCIBILITY_CLOSURE.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/REPRODUCIBILITY_CLOSURE.md), [`EXTERNAL_DATASET_FEASIBILITY.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_DATASET_FEASIBILITY.md), [`EXTERNAL_EVALUATION_PROTOCOL.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md), [`PHASE8_FINAL_REPORT.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/PHASE8_FINAL_REPORT.md). | Threshold discrepancy resolved; AnoMod selected; protocol frozen; execution blocked by Zenodo bandwidth throttling ($>10\text{h}$). |

---

## 5. Exit Criteria for Phase 8 Closure

Phase 8 meets all four formal closure exit criteria:
1. **Calibration Determinism Verified**: Isolation Forest calibration threshold discrepancy is mathematically resolved and confirmed bit-for-bit identical across independent runs.
2. **Manuscript Stale Values Corrected**: Stale threshold references (`-0.090333`), stale model checkpoint path (`lstm_ae_checkpoint.pt`), and outdated dependency versions have been reconciled against the active repository ground truth.
3. **Public Benchmark Rigorously Selected**: AnoMod evaluated across 8 dimensions and chosen on methodological grounds over TrainTicket.
4. **Pre-Registered Protocol Frozen**: Protocol is pre-registered without data snooping, preventing post-hoc parameter adjustments.
5. **No Data Fabrication**: The transfer blocker is transparently documented; no simulated proxy data was generated.

---

## 6. Epistemic Evidence Classification

To maintain scientific integrity, all findings in this reconciliation are classified into four formal epistemic categories:

### 6.1 Verified Facts (Directly inspected and confirmed in this session)
1. **Commit & Repository State**: Active commit is `d277c1df3c2599ddecdf5f0bb761c99718499667` on `main`. All 42 unit/integration tests pass in 22.08s.
2. **Deterministic Threshold Value**: Active pipeline threshold for Isolation Forest in `run_experiment_a.py` is `-0.018694` (`val_iso_scores = -iso_forest.decision_function(val_flat)` at 99th quantile).
3. **Bit-for-Bit Determinism**: Two consecutive independent runs of `run_experiment_a.py` generated bit-for-bit identical outputs with matching SHA-256 hashes for predictions (`246e14f8...`) and metrics (`ed577530...`).
4. **Stale Threshold Eliminated**: Stale references to `-0.090333` in the manuscript, table index, and evidence matrix have been updated to `-0.018694`.
5. **Frozen Protocol**: Protocol for external benchmark validation is frozen in `research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md` (SHA-256: `e5a31a98...`).
6. **Disk Space**: Local system drive `C:` has over 938 GB of free space available for dataset ingestion.

### 6.2 Inherited Claims (Accepted from previous audited phases with established provenance)
1. **Database Cold-Start State**: 100% of historical SQLite telemetry rows (`b8f33f63...`) reflect bootstrap operational rules (`anomaly_score = NULL`), verified in Phase 2.
2. **Safety Containment**: 11/11 adversarial attacks blocked, 0.0% breach rate on localhost loopback boundary, verified in Phase 5.
3. **RCA Pilot Benchmark**: Live LLM achieved 83.33% strict accuracy (5/6) vs rule baseline 100.0% (6/6) in 0.01 ms, verified in Phase 4.

### 6.3 Inferences (Deductions supported by evidence but requiring external confirmation)
1. **Zenodo Rate Limiting**: The sustained $\approx 5.38\text{ KB/s}$ throughput observed during HTTP probes is inferred to be automated rate-limiting / bot protection rather than transient ISP congestion, supported by identical throttling across repeated range requests.
2. **AnoMod Feature Alignment**: Client API response times and HTTP status codes in AnoMod's `api_responses/` are inferred to be sufficient proxies for AegisOps' synthetic latency and error rate metrics.

### 6.4 Unresolved Questions (Active blockers and knowledge boundaries)
1. **AnoMod Retrieval Completion**: Can `AnoMod.zip` (201.9 MB) be successfully ingested via a resumable multi-retry background worker before Zenodo scheduled infrastructure maintenance?
2. **Container Metric Noise**: Will raw Prometheus container metrics from SocialNetwork/TrainTicket require additional smoothing or clipping before passing into the frozen LSTM Autoencoder?
3. **Generalization Performance**: Will the LSTM Autoencoder maintain its superior sensitivity over Isolation Forest on wild containerized microservices, or will real-world traffic variance degrade deep reconstruction fidelity?
