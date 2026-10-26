# AegisOps: Master Research Checklist & Categorical Governance

> **Supersession notice (2026-10-15):** This checklist preserves historical phase-completion and prior review status. The current release decision is **NOT READY — MATERIAL CONTRADICTIONS OR RENDERING BLOCKERS REMAIN** pending faithful rendered-manuscript review, author/venue confirmation, and final provenance closure. Historical "READY FOR SUPERVISOR REVIEW" entries below are not the current release verdict.

**Document Version**: 2.4.0 (Calibration-Independence & Statistical Validity Re-Audit Update)  
**Verification Date**: October 14, 2026<br>
**Auditor**: Senior Research Supervisor, ML Engineer & Reproducibility Auditor  
**Scope**: Status determination of all research phases, Experiment D readiness, scientific validity, external benchmark validation, and manuscript readiness.  
**Standardized Status Taxonomy**:
- `COMPLETED` — Directly supported by verified empirical evidence.
- `IN PROGRESS` — Partially implemented or verified.
- `NEEDS VERIFICATION` — Evidence is insufficient or contradictory.
- `BLOCKED` — Requires a human decision, missing data, approval, or an unresolved prerequisite.
- `NOT STARTED` — No substantive work or evidence exists.

---

## 1. Master Research Phase Status Dashboard

| Research Phase | Description | Standardized Status | Primary Supporting Evidence | What Remains |
| :---: | :--- | :---: | :--- | :--- |
| **Phase 1** | Repository Inventory & Environment Baseline | **COMPLETED** | [`research/audits/REPOSITORY_AUDIT.md`](REPOSITORY_AUDIT.md), [`research/audits/TEST_RESULTS.md`](TEST_RESULTS.md) | Baseline locked. Maintain `.venv` dependency isolation. |
| **Phase 2** | Dataset, Telemetry & Episode Reconciliation | **COMPLETED** | [`research/audits/reconciliation_gate_20261012/DATA_ROW_RECONCILIATION.csv`](reconciliation_gate_20261012/DATA_ROW_RECONCILIATION.csv) | Reconciled 200-row telemetry and 169 fault sample census. Complete. |
| **Phase 3** | Anomaly Detection Benchmark (Experiment A) | **COMPLETED** | [`research/raw/detection_predictions.csv`](../raw/detection_predictions.csv), [`research/STATISTICAL_AUDIT.md`](../STATISTICAL_AUDIT.md) | $N=320$ synthetic windows evaluated; exact McNemar $p = 2.17 \times 10^{-19}$ verified. Complete. |
| **Phase 4** | Root-Cause Diagnosis Benchmark (Experiment B) | **IN PROGRESS** | [`research/raw/diagnosis_predictions.csv`](../raw/diagnosis_predictions.csv), [`research/audits/reconciliation_gate_20261012/DIAGNOSIS_RECONCILIATION.md`](reconciliation_gate_20261012/DIAGNOSIS_RECONCILIATION.md) | Pilot benchmark complete ($7 \times 6 = 42$); large-scale cohort ($N \ge 100$) deferred to future work. |
| **Phase 5** | Execution Boundary Safety Evaluation (Experiment C) | **COMPLETED** | [`research/raw/safety_test_results.csv`](../raw/safety_test_results.csv), [`approval.py`](../../approval.py) | 16-case boundary taxonomy verified; 100% attack containment (11/11). Complete. |
| **Phase 6** | Unified Reproducibility Pipeline & Manifest | **COMPLETED** | [`research/run_all.py`](../run_all.py), [`research/MANIFEST_SHA256.json`](../MANIFEST_SHA256.json) | Historical baseline execution (`run_all.py` in 53.6s, exit 0). Note: `run_all.py` was subsequently updated for Path 3 bounded claims and was not rerun during the latest audit to preserve frozen artifacts. |
| **Phase 7** | Manuscript Synthesis & Publication Readiness (Path 3 Bounded Claims) | **COMPLETED** | [`research/paper/AEGISOPS_RESEARCH_PAPER.md`](../paper/AEGISOPS_RESEARCH_PAPER.md), [`research/paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`](../paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md), [`research/paper/FINAL_EVIDENCE_AUDIT.md`](../paper/FINAL_EVIDENCE_AUDIT.md), [`research/paper/CANONICAL_METRIC_RECONCILIATION.md`](../paper/CANONICAL_METRIC_RECONCILIATION.md) | Bounded manuscript reconciled against all machine-readable evidence; ready for supervisor review. |
| **Phase 8** | Reproducibility Closure & Manuscript Consistency | **COMPLETED** | [`research/audits/STATISTICAL_INTEGRITY_AND_INGESTION_PREFLIGHT.md`](STATISTICAL_INTEGRITY_AND_INGESTION_PREFLIGHT.md), [`research/audits/PRE_PHASE9_EVIDENCE_INTEGRITY_GATE.md`](PRE_PHASE9_EVIDENCE_INTEGRITY_GATE.md) | IF threshold resolved (-0.018694); AnoMod selected; Protocol v1.1.0 frozen. Complete. |
| **Phase 9** | External Benchmark Validation (AnoMod Execution) | **EXCLUDED (DEFERRED)** | [`research/audits/BOUNDED_CLAIMS_DECISION.md`](BOUNDED_CLAIMS_DECISION.md), [`research/audits/EXPERIMENT_D_FINAL_SUPERVISOR_DECISION.md`](EXPERIMENT_D_FINAL_SUPERVISOR_DECISION.md) | Formally excluded from immediate manuscript under Path 3 Bounded-Claims Policy due to sequence-length mismatch ($W=24$ vs $0$) and zero-shot domain shift ($e \approx 59.19$ vs $\tau = 0.7094$, an $\approx 83.4\times$ / $>80\times$ domain shift). Production execution deferred to future work. |

---

## 2. Categorical Governance Breakdown

### Category I: Implementation Readiness

| Requirement / Component | Standardized Status | Evidence Path | What Remains |
| :--- | :---: | :--- | :--- |
| **Checkpoint Loader & Contract** | **COMPLETED** | `dl/anomaly_detector.py`, `test_experiment_d_harness.py:test_checkpoint_loads_and_eval_mode` | Bit-for-bit SHA-256 match (`1cf44e6e...`), eval mode, 3,733 params. Complete. |
| **SocialNetwork 5-D Telemetry Extraction** | **COMPLETED** | `run_experiment_d.py:139-222`, `test_extract_sn_telemetry_synthetic_fixture` | 15s epoch grid aggregation, trace latency & error rate. Complete. |
| **TrainTicket Telemetry Extraction** | **COMPLETED** | `run_experiment_d.py:225-315`, `test_extract_tt_telemetry_synthetic_fixture` | Prometheus counter deltas, SkyWalking trace parser. Complete. |
| **Contiguous Window Construction** | **COMPLETED** | `run_experiment_d.py:335-389`, `test_build_contiguous_windows_strictly_consecutive` | Rejects missing intervals, strict $\Delta t = 15.0\text{s}$ consecutive steps. Complete. |
| **Chronological Split & Purge Gap** | **COMPLETED** | `run_experiment_d.py:391-432`, `test_partition_normal_series_chronologically_disjoint` | Pre-windowing 70/30 split with 7-step (105s) purge gap; zero shared timestamps. Complete. |
| **Baseline Detection Rules** | **COMPLETED** | `run_experiment_d.py:102-135`, `test_narrow_rules_baseline`, `test_resource_rules_baseline` | Narrow, Resource-Only, and Full Operational rule evaluators verified. Complete. |
| **Isolation Forest Pipeline** | **COMPLETED** | `run_experiment_d.py:552-559`, `test_isolation_forest_fitting_restricted_to_normal_data` | 100 trees, contamination 0.01, fit strictly on nominal calibration data. Complete. |
| **Production Execution Loop** | **COMPLETED** | `run_experiment_d.py:687-779`, `test_run_evaluation_pipeline_sandbox` | `run_production_experiment_d()` connects scenario loading to evaluation and output validation. Complete. |
| **Fail-Closed Execution CLI Guards** | **COMPLETED** | `run_experiment_d.py:896-926`, `test_fail_closed_cli_unauthorized_exit_code_2`, `test_fail_closed_cli_unratified_exit_code_3` | Refuses execution without `--authorized` (code 2) and without ratification file (code 3). Complete. |
| **Automated Harness Test Suite** | **COMPLETED** | `test_experiment_d_harness.py`, `research/audits/EXPERIMENT_D_TEST_RESULTS.md` | 40/40 tests passing in 10.22s. Complete. |
| **Repository Regression Suite** | **COMPLETED** | Full repository test suite in `.venv` (`task-3502.log`) | Distinguishes historical baseline (107/107 in 77.56s, `task-3108.log`) from latest reported working-tree run (107/107 in 99.50s, `task-3502.log`). No test runs re-executed for document edits. Complete. |

---

### Category II: Scientific Validity & Data Integrity

| Scientific Dimension | Standardized Status | Evidence Path | What Remains |
| :--- | :---: | :--- | :--- |
| **Frozen Checkpoint Preservation** | **COMPLETED** | `models/lstm_autoencoder.pt`, `test_checkpoint_weights_remain_strictly_frozen` | Zero parameter changes during evaluation. Complete. |
| **Normalization Contract Alignment** | **RECONCILED (DOMAIN SHIFT PROVEN)** | `EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md`, `scratch_test_zero_shot.py` | Model contract verified as `("cpu_pct", "memory_pct", "latency_ms", "error_rate_pct", "disk_pct")`. Applying frozen training scaler to real nominal traffic produces severe domain shift ($e \approx 59.19$ vs $\tau = 0.7094$), resulting in 100% nominal false alarms (19/19 windows). |
| **Zero Imputation Safeguard** | **COMPLETED** | `run_experiment_d.py:209-221`, `test_build_contiguous_windows_rejects_missing_latency` | Zero latency is never imputed for idle traffic intervals ($N_{\text{req}} = 0$). Buffer reset enforced. Complete. |
| **Temporal Continuity Verification** | **COMPLETED** | `research/audits/experiment_d_temporal_eligibility_audit.json`, `EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md` | Empirical audit confirmed 19 eligible $W=8$ windows in SN Normal Baseline across 3 runs (lengths 11, 11, 18); $W=24$ yields 0 eligible windows. Complete. |
| **Calibration Leakage Prevention** | **SCOPED (EXP A VERIFIED; EXP D BLOCKED/EXCLUDED)** | `models/lstm_autoencoder.json`, `research/audits/EXPERIMENT_D_CALIBRATION_INDEPENDENCE_AUDIT.md`, `research/audits/BOUNDED_CLAIMS_DECISION.md` | **Experiment A**: Fully supported; $\tau = 0.709399$ calibrated on $N=150$ independent nominal validation sequences with zero test/label contamination.<br>**Experiment D**: Unexecuted harness contains known circular calibration leakage defect (`run_experiment_d.py:550,566` reused validation for threshold tuning and evaluation). Formally unexecuted and deferred under Path 3. |
| **Threshold Calibration Sample Size** | **RECONCILED (WINDOW TRACEABILITY VERIFIED)** | `EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md` | Reconciled historical ~2 vs actual 8 validation windows: raw 80-row split (70/30, purge 7) captures 15 contiguous rows of Run 3 ($15 - 8 + 1 = 8$ windows). Highly dependent (87.5% overlap). |
| **Statistical Dependence Caveat** | **METHODOLOGY RECONCILED** | `EXPERIMENT_D_ZERO_SHOT_IMPLEMENTATION_PLAN.md` | Confirmatory McNemar test on overlapping windows withdrawn; plan requires scenario-level paired tests ($N=12$) and Wilson CIs for nominal rates. |
| **Scenario Cohort Statistical Power** | **CLAIMS DOWNGRADED** | `EXPERIMENT_D_HUMAN_METHOD_DECISION_V2.md` | Confirmatory hypotheses downgraded to exploratory domain-transfer sensitivity claims. |

---

### Category III: External Benchmark Evaluation (AnoMod)

| Lifecycle Stage | Standardized Status | Evidence Path | What Remains |
| :--- | :---: | :--- | :--- |
| **Stage 1: Protocol Pre-Registration** | **COMPLETED** | `research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md` | Protocol v1.1.0 frozen. Complete. |
| **Stage 2: Archive Ingestion & Provenance** | **COMPLETED** | `data/external/anomod/transfer_provenance.json`, `research/scripts/ingest_anomod.py` | 201,917,396 bytes acquired; MD5 `30c58351...` matched Zenodo record. Complete. |
| **Stage 3: Extraction & Schema Validation** | **COMPLETED** | `data/external/anomod/unpacked/extraction_manifest.json`, `research/audits/ANOMOD_DATASET_INSPECTION.md` | 38,349 items unpacked; schema and features verified. Complete. |
| **Stage 4: Harness Construction & Code Audit** | **COMPLETED** | `research/audits/EXPERIMENT_D_IMPLEMENTATION_REVIEW.md`, `research/audits/EXPERIMENT_D_READINESS_REAUDIT.md` | Call graph, contiguous windowing, purge gap, and ratification gate built and tested. Complete. |
| **Stage 4.5: Scientific Decision Gate** | **RESOLVED VIA PATH 3** | `research/audits/BOUNDED_CLAIMS_DECISION.md`, `research/audits/EXPERIMENT_D_FINAL_SUPERVISOR_DECISION.md` | Supervisor ratified Path 3 (Bounded-Claims Paper Finalization). External LSTM validation on AnoMod is formally excluded from confirmatory paper claims due to sequence-length mismatch ($W=24$ vs $W=8$) and domain shift. Production execution remains blocked/deferred for future work. Complete. |
| **Stage 5: Production Experiment D Execution** | **EXCLUDED (DEFERRED TO FUTURE WORK)** | `research/audits/BOUNDED_CLAIMS_DECISION.md` | Excluded from immediate manuscript scope. Protocol v1.1.0 remains frozen; Protocol Amendment v1.2.0 unapproved. Production execution not executed. Complete. |
| **Stage 6: Manuscript Reconciliation** | **IN PROGRESS (PATH 3 ACTIVE)** | `research/paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`, `research/paper/MANUSCRIPT_FINALIZATION_PLAN.md` | Active finalization: reconciling all manuscript sections to verified synthetic, pilot, and safety evidence under 11 bounded-claims policies. |

---

### Category IV: Manuscript Readiness (Path 3 Bounded Claims)

| Paper Section / Component | Standardized Status | Evidence Path | What Remains |
| :--- | :---: | :--- | :--- |
| **Section 1–5: Intro, Related Work, Formulation, Methodology & Architecture** | **COMPLETED** | `research/paper/AEGISOPS_RESEARCH_PAPER.md` §1–§5 | Authored and internally verified. |
| **Section 6: Experimental Datasets & Protocols** | **COMPLETED** | `research/paper/AEGISOPS_RESEARCH_PAPER.md` §6 | Exp A ($N=320$), Exp B ($N=6$), Exp C ($N=16$) protocol definitions verified. |
| **Section 7: Anomaly Detection Results (Experiment A)** | **COMPLETED** | `research/paper/AEGISOPS_RESEARCH_PAPER.md` §7 | Bounded synthetic experiment results verified ($N=320$; 100% recall, 1.0% FPR, 3 rule baselines). |
| **Section 8: Root-Cause Diagnosis Results (Experiment B)** | **COMPLETED** | `research/paper/AEGISOPS_RESEARCH_PAPER.md` §8 | Pilot benchmark reported ($N=6$; strict vs lenient rubric, $1-\beta \approx 0.14$, no LLM superiority). |
| **Section 9: Execution Boundary Safety (Experiment C)** | **COMPLETED** | `research/paper/AEGISOPS_RESEARCH_PAPER.md` §9 | 16-case boundary safety evaluation reported (100% containment; localhost scope). |
| **Section 10: Statistical Analysis & Uncertainty** | **COMPLETED** | `research/paper/AEGISOPS_RESEARCH_PAPER.md` §10 | Window McNemar descriptive, scenario Wilcoxon primary ($N=6, W=0.0, p=0.03125$). |
| **Section 11 & 12: Discussion, Limitations (AnoMod Preflight §11.4) & Future Work** | **RE-SCOPED (FUTURE WORK)** | `research/paper/AEGISOPS_RESEARCH_PAPER.md` §11, §12 | Excluded from confirmatory claims; positioned strictly as pre-registered benchmark target for future work. |
| **Manuscript Review Package** | **READY FOR SUPERVISOR REVIEW** | `research/paper/MANUSCRIPT_FINALIZATION_PLAN.md`, `research/paper/FINAL_EVIDENCE_AUDIT.md` | Quality-control checklist (QC-1 through QC-8) fully completed; manuscript review package ready for supervisor review under Path 3 Bounded Claims. Camera-ready submission status formally deferred until visual PDF layout proofing. |

---

## 3. Active Quality-Control Tasks & Measurable Acceptance Criteria (Supervisor Directive QC-1 to QC-8)

The following quality-control tasks govern final manuscript sign-off per the Supervisor Directive:

| Task ID | Quality Control Task | Measurable Acceptance Criterion | Standardized Status | Verification Evidence |
| :---: | :--- | :--- | :---: | :--- |
| **QC-1** | Detection Metric Reconciliation | Table 1, matrix, and handoff concordant with raw predictions ($N=320$): IF (57 TP, 4 FP, 196 TN, 63 FN), LSTM (120 TP, 2 FP, 198 TN, 0 FN), Full Rules (120 TP, 0 FP, 200 TN, 0 FN); McNemar $b=63, c=0, p=2.168 \times 10^{-19}$. | **COMPLETED** | `research/raw/detection_predictions.csv`, `research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv`, manuscript Table 1, and handoff Section D. |
| **QC-2** | Windowing & Statistical Independence | Clarify 24-step non-overlapping discrete windows; qualify window-level McNemar test as descriptive; establish scenario-level Wilcoxon test ($W=0.0, p=0.03125$) as exploratory inference; note Full Rules error-rate predicate overlap. | **COMPLETED** | Manuscript Section 3, Section 6.1, Section 10, Section 11.4; `WINDOW_EXPOSURE_AND_ALARM_RATE_AUDIT.md`; `STATISTICAL_ASSUMPTION_REVIEW.md`. |
| **QC-3** | Frozen Model Contract | Feature order verified as `(cpu_pct, memory_pct, latency_ms, error_rate_pct, disk_pct)`; Z-score normalization; latent dimension $h=16$ ($\mathbb{R}^{16}$); 3,733 PyTorch parameters; SHA-256 `1cf44e6e...`; threshold $\tau=0.709399$ calibrated on $N=150$ held-out nominal validation sequences (not training data); Exp D excluded. | **COMPLETED** | `models/lstm_autoencoder.json`, `models/lstm_autoencoder.pt`, `dl/anomaly_detector.py`, manuscript Section 4.3, Section 5.2, Figure 2, Algorithm 1. |
| **QC-4** | Root-Cause Diagnosis Consistency | 42 rubric evaluations across 7 configs $\times$ 6 canonical scenarios; Config 1 (Rule-based: 100% strict), Config 6 (Multi-Agent Full: 83.33% strict ITT, 100% lenient), Config 5 & 7 (66.67% strict ITT, 80.00% completed-cases, 1 omitted call each); deterministic rules 100% strict in 0.01 ms vs LLM 83.33% in 23.19 s; low power ($1-\beta \approx 0.14$), rubric overlap, and lack of provider wire logs disclosed. | **COMPLETED** | `research/raw/diagnosis_predictions.csv`, `research/raw/diagnosis_metrics.csv`, manuscript Table 2, Table 3, Section 8.1; no claim of LLM superiority. |
| **QC-5** | Safety Claims & Governance Terminology | 16 test cases: 11 attacks (`TC-ATT-01` to `11`), 2 precondition checks (`TC-FAIL-01, 02`), 1 probe (`TC-VERIF-01`), 2 controls (`TC-POS-01`, `TC-AUDIT-01`); 100% containment of 11 attacks (Wilson CI $[0.7412, 1.0000]$); local boundary `127.0.0.1:8765`; NIST SP 800-53 control AC-3(2) dual authorization guidelines; SQLite atomic locks/WAL, not immutable ledger. | **COMPLETED** | `research/raw/safety_test_results.csv`, manuscript Table 4, Section 2.4, Section 4.7, Section 9.1; `approval.py`. |
| **QC-6** | Abstract, Conclusions & Contributions | Disclose synthetic Exp A, exploratory pilot Exp B, local safety Exp C, zero additive sensitivity of combined detector, deterministic baseline outperforming LLM, external validation excluded as future work; human-gated operational framework. | **COMPLETED** | Manuscript Abstract, Section 1, Section 11, Section 12; contributions strictly aligned with empirical evidence. |
| **QC-7** | References & Technical Correctness | 16 citations (13 peer-reviewed, 1 NIST standard, 2 preprints/workshops) verified with verified author lists (Ping et al., Lee et al., Schmidhuber restored) and DOIs; mathematical notation $\mathbf{x}_t \in \mathbb{R}^5$, threshold inequalities $MSE > \tau$, confusion matrices, Mermaid figures (Figures 1, 2, 3), Algorithms 1, 2, 3 aligned with code. | **COMPLETED** | Manuscript References, Section 3, Section 5, Figures 1-3, Algorithms 1-3; `REFERENCE_VERIFICATION.md`, `CANONICAL_METRIC_RECONCILIATION.md`. |
| **QC-8** | Reproducibility & Regression Verification | Automated test suite execution records: Historical baseline passed 107/107 tests in 77.56s (`task-3108.log`); latest reported working-tree run passed 107/107 repository tests in 99.50s (`task-3502.log`, exit code 0); focused suite passed 18/18 tests in 30.18s (`task-3429.log`) and 11.20s (`task-3284.log`); historical artifact SHA-256 manifest verified (17/22 artifacts matched bit-for-bit; 5 intentional diffs trace to audited diagnosis/safety classifications and metric recomputations). No tests or pipeline commands were rerun during documentation reviews. | **COMPLETED** | Documented audit trail across regression runs on active working tree; zero regressions; zero test skips or failures. |

### Phase 17 bounded update (2026-10-17)

- **Live quality-only pilot:** **GATE 1 CLOSED.** Phase 17 prepared `research/exports/live_lstm/phase15/PHASE17_OWNER_APPROVAL_REQUEST.md` and reassessed the gate. No human authorization record was present; no collection, target access, configuration change, database mutation, or live-performance analysis occurred.
- **Prescribed isolated harness regression:** **40/40 passed** with `--basetemp .pytest_tmp_phase17` after the default pytest temporary root was inaccessible. This is focused evidence only; the historical/full-suite record was not re-run in Phase 17.
- **Manuscript release:** **BLOCKED FOR CAMERA-READY RELEASE.** Source-level bounded-claims QC found no new claim strengthening, but no reproducible DOCX/PDF generation or page-level rendered inspection is available. See `research/paper/PHASE17_MANUSCRIPT_QC_REPORT.md`.

### Phase 18 release consistency and regression update (2026-10-18)

- **Canonical release controls:** `research/paper/PHASE18_CANONICAL_MANUSCRIPT_RELEASE_CHECKLIST.md` now governs current release readiness with stable `REL-01` through `REL-12` identifiers. It reconciles, without rewriting, the overlapping historical seven-item and eight-item QC taxonomies.
- **Current full regression:** **PASS — 116/116** root-suite tests passed in 65.70 seconds with exit code 0 using the Windows virtual environment and a workspace-local pytest temporary directory. This is test-suite evidence only; it does not execute Experiment D or establish live performance.
- **Release state:** **BLOCKED.** The current blockers are reproducible DOCX/PDF generation, every-page visual inspection, selected-release provenance, author/venue metadata, AnoMod bibliographic closure or an accepted limitation, and independent release sign-off. Live LSTM detection performance remains **UNMEASURED**.

