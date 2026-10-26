# AegisOps Technical Audits & Decisions Index

**Directory Path**: `research/audits/`  
**Current Branch**: `publish/research-without-external-dataset`  
**Git HEAD**: `a32713c30a8ddca1425d44b1afbaf6d55a64c276`  

This directory contains the complete technical audit trail, supervisory decisions, protocol proposals, and verification evidence produced during the research lifecycle of AegisOps.

---

## 1. Master Status & Operational Handoff Documents

These documents represent the active supervisory review and operational baseline for the project:

- [`AEGISOPS_MASTER_RESEARCH_HANDOFF.md`](AEGISOPS_MASTER_RESEARCH_HANDOFF.md): Master research handoff document establishing the complete scientific status matrix, invariant contract, and reproducibility handoff.
- [`UPDATED_SEVEN_PHASE_CHECKLIST.md`](UPDATED_SEVEN_PHASE_CHECKLIST.md): Master research checklist (v2.3.0) tracking implementation readiness, scientific validity, external evaluation, manuscript readiness, and QC acceptance criteria (QC-1 through QC-8).

---

## 2. Supervisory Decisions & Governance Records

Official gate decisions and supervisory policy ratifications:

- [`BOUNDED_CLAIMS_DECISION.md`](BOUNDED_CLAIMS_DECISION.md): **RATIFIED SUPERVISORY DECISION**. Formalizes Path 3 (Bounded-Claims Paper Finalization), bounding immediate manuscript claims to synthetic Experiment A, pilot Experiment B, and safety Experiment C.
- [`EXPERIMENT_D_FINAL_SUPERVISOR_DECISION.md`](EXPERIMENT_D_FINAL_SUPERVISOR_DECISION.md): Human decision package evaluating Paths 1, 2, and 3, leading to the adoption of Path 3.
- [`EXPERIMENT_D_FINAL_METHOD_DECISION.md`](EXPERIMENT_D_FINAL_METHOD_DECISION.md): Comprehensive synthesis of methodological options and blocking rationale.
- [`EXPERIMENT_D_HUMAN_DECISION_PACKET.md`](EXPERIMENT_D_HUMAN_DECISION_PACKET.md): Initial decision packet on windowing yield and normalization options.
- [`EXPERIMENT_D_HUMAN_METHOD_DECISION_V2.md`](EXPERIMENT_D_HUMAN_METHOD_DECISION_V2.md): Decision packet v2.0 reconciling reporting modalities.
- [`EXPERIMENT_D_READINESS_VERDICT.md`](EXPERIMENT_D_READINESS_VERDICT.md): Formal execution gate verdict and operational boundary.
- [`PHASE_1_VERDICT.md`](PHASE_1_VERDICT.md): Initial Phase 1 verification verdict (manifest file).

---

## 3. Forensic Audits of Experiment D & Benchmark Ingestion

In-depth technical investigations into external validation on the AnoMod benchmark:

- [`EXPERIMENT_D_CALIBRATION_INDEPENDENCE_AUDIT.md`](EXPERIMENT_D_CALIBRATION_INDEPENDENCE_AUDIT.md): Forensic proof of circular calibration/evaluation leakage (`v_win` reuse) and near-zero variance collapse in the unexecuted harness.
- [`EXPERIMENT_D_STATISTICAL_VALIDITY_REAUDIT.md`](EXPERIMENT_D_STATISTICAL_VALIDITY_REAUDIT.md): Analysis of window-level autocorrelation (87.5% overlap), scenario-level statistical power, and extreme class imbalance.
- [`EXPERIMENT_D_SEQUENCE_COMPATIBILITY_DECISION.md`](EXPERIMENT_D_SEQUENCE_COMPATIBILITY_DECISION.md): Forensic proof of sequence-length mismatch ($W=24$ model contract vs 0 eligible contiguous windows in AnoMod).
- [`EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md`](EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md): Demonstration of zero-shot domain shift ($e \approx 59.19$ vs $\tau = 0.7094$, an $\approx 83.4\times$ shift; 19/19 false alarms on off-contract $W=8$ diagnostic data).
- [`EXPERIMENT_D_ZERO_SHOT_IMPLEMENTATION_PLAN.md`](EXPERIMENT_D_ZERO_SHOT_IMPLEMENTATION_PLAN.md): Pre-execution zero-shot transfer architecture and dependency analysis.
- [`EXPERIMENT_D_DECISION_PACKET_VERIFICATION.md`](EXPERIMENT_D_DECISION_PACKET_VERIFICATION.md): Independent audit verification of decision packet calculations.
- [`EXPERIMENT_D_IMPLEMENTATION_REVIEW.md`](EXPERIMENT_D_IMPLEMENTATION_REVIEW.md): Code audit of `run_experiment_d.py` call graph and contiguous window buffer.
- [`EXPERIMENT_D_PREFLIGHT_AND_HARNESS_GATE.md`](EXPERIMENT_D_PREFLIGHT_AND_HARNESS_GATE.md): Harness execution gate report and defect resolution.
- [`EXPERIMENT_D_PROTOCOL_RECONCILIATION.md`](EXPERIMENT_D_PROTOCOL_RECONCILIATION.md): Standalone clause-by-clause protocol reconciliation matrix.
- [`EXPERIMENT_D_READINESS_REAUDIT.md`](EXPERIMENT_D_READINESS_REAUDIT.md): Comprehensive re-audit of harness readiness and gating.
- [`EXPERIMENT_D_REMEDIATION_CHANGELOG.md`](EXPERIMENT_D_REMEDIATION_CHANGELOG.md): Chronological record of 6 defects remediated in the harness.
- [`EXPERIMENT_D_REQUIREMENTS_TRACEABILITY.md`](EXPERIMENT_D_REQUIREMENTS_TRACEABILITY.md): Mapping of requirements REQ-01 through REQ-10 to code, tests, and evidence.
- [`EXPERIMENT_D_STATISTICAL_ACCEPTANCE_CRITERIA.md`](EXPERIMENT_D_STATISTICAL_ACCEPTANCE_CRITERIA.md): Pre-registered hypotheses (H1, H2) and multiple-testing corrections.
- [`EXPERIMENT_D_TEST_RESULTS.md`](EXPERIMENT_D_TEST_RESULTS.md): Empirical test results for all 40 harness unit tests.
- [`ANOMOD_DATASET_INSPECTION.md`](ANOMOD_DATASET_INSPECTION.md): Inspection of unpacked AnoMod files (38,349 files verified, MD5 `30c58351...`).
- [`STATISTICAL_INTEGRITY_AND_INGESTION_PREFLIGHT.md`](STATISTICAL_INTEGRITY_AND_INGESTION_PREFLIGHT.md): Preflight audit of ingestion pipeline and mathematical threshold stability.
- [`PRE_PHASE9_EVIDENCE_INTEGRITY_GATE.md`](PRE_PHASE9_EVIDENCE_INTEGRITY_GATE.md): Pre-Phase 9 readiness gate review.
- [`PHASE9_EXTERNAL_VALIDATION_READINESS.md`](PHASE9_EXTERNAL_VALIDATION_READINESS.md): Initial readiness review for external validation.
- [`PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md`](PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md): Proposed 8-dimension amendment (v1.2.0, unapproved/frozen).
- [`experiment_d_temporal_eligibility_audit.json`](experiment_d_temporal_eligibility_audit.json): Machine-readable window yield audit across all 26 scenarios.

---

## 4. Foundation Audits (Required for Manifest Reproducibility)

These files are tracked by `research/MANIFEST_SHA256.json` and verified by `research/run_all.py`:

- [`DATABASE_AUDIT.md`](DATABASE_AUDIT.md): Schema validation of `data/aegisops_live.sqlite3` (86,016 bytes).
- [`REPOSITORY_AUDIT.md`](REPOSITORY_AUDIT.md): Repository code and structure inventory.
- [`MODEL_AND_EXECUTION_AUDIT.md`](MODEL_AND_EXECUTION_AUDIT.md): Frozen checkpoint verification (3,733 parameters, weight immutability).
- [`TEST_RESULTS.md`](TEST_RESULTS.md): Baseline test execution report.
- [`PHASE_1_VERDICT.md`](PHASE_1_VERDICT.md): Baseline Phase 1 completion verdict.

---

## 5. Earlier Phase Reconciliation Audits

Evidence reconciliation reports from earlier project phases:

- [`DATA_ROW_RECONCILIATION.csv`](DATA_ROW_RECONCILIATION.csv): 200-row telemetry mapping resolving the 169 true fault samples vs 175 episode artifact discrepancy.
- [`DETECTION_RECONCILIATION.md`](DETECTION_RECONCILIATION.md): Mathematical reconciliation of detection metrics and thresholds.
- [`DIAGNOSIS_RECONCILIATION.md`](DIAGNOSIS_RECONCILIATION.md): Diagnostic accuracy reconciliation across 7 configurations.
- [`SAFETY_RECONCILIATION.md`](SAFETY_RECONCILIATION.md): Execution boundary safety gate reconciliation.
- [`EVIDENCE_RECONCILIATION_REPORT.md`](EVIDENCE_RECONCILIATION_REPORT.md): Summary evidence reconciliation report.
- [`PIPELINE_REPRODUCIBILITY.md`](PIPELINE_REPRODUCIBILITY.md): Pipeline execution and reproduction trace.
- [`MANUSCRIPT_CONSISTENCY_AUDIT.md`](MANUSCRIPT_CONSISTENCY_AUDIT.md): Initial manuscript consistency audit.
- [`PHASE8_CHECKLIST_RECONCILIATION.md`](PHASE8_CHECKLIST_RECONCILIATION.md): Phase 8 checklist reconciliation.

---

## 6. Historical Gate Archives (Preserved Directories)

These directories contain historical snapshots preserved for provenance and reproducibility:

- [`2026-10-12/`](2026-10-12/): Initial Phase 1 audit snapshot (exact duplicate copies of foundation audits).
- [`reconciliation_gate_20261012/`](reconciliation_gate_20261012/): Phase 2 reconciliation gate snapshot (exact duplicate copies of reconciliation files).
- [`detection_closure_gate_20261012/`](detection_closure_gate_20261012/): Detection closure gate records and recomputed metrics.
- [`detection_figure_verification_20261012/`](detection_figure_verification_20261012/): Detection figure verification audit.
- [`detection_rate_and_phase4_gate_20261012/`](detection_rate_and_phase4_gate_20261012/): Phase 4 gate records, corrected metrics, and window exposure audit.
- [`phase3_final_reproducibility_20261012/`](phase3_final_reproducibility_20261012/): Two-run reproducibility test records for Phase 3.
- [`phase8_external_validation/`](phase8_external_validation/): Phase 8 baseline external evaluation protocol (v1.1.0 frozen) and feasibility report.
- [`rule_baseline_finalization_20261012/`](rule_baseline_finalization_20261012/): Rule baseline finalization records and recalculated metrics.
