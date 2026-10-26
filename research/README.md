# AegisOps Research Workspace & Directory Guide

**Repository Root**: `C:\DL_PROJECT`  
**Current Branch**: `publish/research-without-external-dataset`  
**Git HEAD**: `a32713c30a8ddca1425d44b1afbaf6d55a64c276`  
**Active Python Runtime**: `C:\DL_PROJECT\.venv\Scripts\python.exe` (Python 3.11.9, PyTorch 2.14.1+cpu)  
**Standard**: Path 3 Bounded-Claims Policy & Non-Negotiable Research Integrity Rules  

---

## 1. Quick Navigation: Authoritative Documents

| Document Role | File Path | Status | Key Description |
| :--- | :--- | :---: | :--- |
| **Authoritative Manuscript** | [`research/paper/AEGISOPS_RESEARCH_PAPER.md`](paper/AEGISOPS_RESEARCH_PAPER.md) | **ACTIVE** | Primary academic research paper formatted for systems & empirical ML venues. |
| **Canonical Metric Reconciliation** | [`research/paper/CANONICAL_METRIC_RECONCILIATION.md`](paper/CANONICAL_METRIC_RECONCILIATION.md) | **ACTIVE** | Authoritative empirical cross-document reconciliation matrix and test provenance. |
| **Master Research Handoff** | [`research/audits/AEGISOPS_MASTER_RESEARCH_HANDOFF.md`](audits/AEGISOPS_MASTER_RESEARCH_HANDOFF.md) | **ACTIVE** | Comprehensive technical status, invariant register, and reproducibility handoff. |
| **Master Research Checklist** | [`research/audits/UPDATED_SEVEN_PHASE_CHECKLIST.md`](audits/UPDATED_SEVEN_PHASE_CHECKLIST.md) | **ACTIVE** | Master Seven-Phase Checklist (v2.3.0) with QC-1 through QC-8 acceptance criteria. |
| **Reference Verification Audit** | [`research/paper/REFERENCE_VERIFICATION.md`](paper/REFERENCE_VERIFICATION.md) | **ACTIVE** | Verification of all 16 bibliographic entries with persistent DOIs and author registers. |
| **Claim-to-Evidence Matrix** | [`research/paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`](paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md) | **ACTIVE** | Traceability matrix for all 21 manuscript claims (CLM-01 through CLM-21). |

---

## 2. Directory Structure and Architectural Roles

```text
research/
├── README.md                      # This directory guide and research navigation map
├── MANIFEST_SHA256.json           # Cryptographic SHA-256 hash manifest of 22 research artifacts
├── run_all.py                     # Unified experiment and reproducibility pipeline runner
├── statistical_tests.py           # Statistical test formulations (paired McNemar, Wilcoxon)
├── DATA_AND_LABEL_AUDIT.md        # Telemetry data and label audit (manifest file)
├── FINAL_EXPERIMENT_REPORT.md     # Consolidated synthetic experiment report (manifest file)
├── PROJECT_VERSION_AND_ENVIRONMENT.md # Runtime environment specification (manifest file)
├── SAFETY_EVALUATION.md           # Remediation safety evaluation report (manifest file)
├── STATISTICAL_AUDIT.md           # Statistical formulation audit (manifest file)
│
├── paper/                         # Publication manuscript, figures, tables & reviews
│   ├── AEGISOPS_RESEARCH_PAPER.md # Authoritative publication paper
│   ├── CANONICAL_METRIC_RECONCILIATION.md # Authoritative metric reconciliation matrix
│   ├── REFERENCE_VERIFICATION.md  # Active verified bibliography audit
│   ├── REFERENCES_VERIFICATION.md # Historical bibliographic draft (labeled [SUPERSEDED])
│   ├── MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md # Active Path 3 claim-to-evidence matrix
│   ├── MANUSCRIPT_EVIDENCE_MATRIX.md # Historical baseline claim matrix
│   ├── FIGURE_AND_TABLE_INDEX.md  # Comprehensive figure and table cross-verification index
│   ├── FIGURE_AND_TABLE_REGISTER.md # Manuscript figure and table registry
│   ├── FINAL_EVIDENCE_AUDIT.md    # Formal evidence audit
│   ├── FINAL_MANUSCRIPT_CHECKLIST.md # Submission readiness checklist
│   ├── MANUSCRIPT_FINALIZATION_PLAN.md # Finalization plan (QC-1 to QC-8)
│   ├── 00_MANUSCRIPT_EVIDENCE_GATE.md # Evidence gate document
│   ├── BOUNDED_CLAIMS_DECISION.md # Pointer stub to supervisory decision
│   └── figures/                   # Architectural Mermaid diagrams (.mmd) and benchmark PNGs
│
├── raw/                           # Primary research records (preserved bit-for-bit)
│   ├── detection_predictions.csv  # N=320 test sequence predictions (200 normal + 120 fault)
│   ├── detection_metrics.csv      # Baseline comparison metrics (IF, LSTM, 3 Rules)
│   ├── detection_by_scenario.csv  # Scenario-level detection breakdown (N=6 scenarios)
│   ├── diagnosis_predictions.csv  # N=42 pilot RCA rubric evaluations (7 configs x 6 scenarios)
│   ├── diagnosis_metrics.csv      # Diagnostic accuracy and latency metrics
│   ├── safety_test_results.csv    # N=16 security boundary probe results (11 attacks, 2 checks, 1 probe, 2 controls)
│   └── safety_metrics.csv         # Boundary containment rates and check latency
│
├── results/                       # Derived metrics, outputs & reproducible generators
│   ├── generate_statistical_analysis.py # Independent statistical calculation script
│   ├── statistical_analysis.md    # Analytical output of statistical test script
│   └── *.csv                      # Mirror copies of experiment metrics and predictions
│
├── experiments/                   # Experiment implementations and test runners
│   ├── run_experiment_a.py        # Experiment A: Anomaly detection benchmark runner
│   ├── run_experiment_b.py        # Experiment B: Root-cause diagnosis benchmark runner
│   ├── run_experiment_c.py        # Experiment C: Execution boundary safety runner
│   ├── run_experiment_d.py        # Experiment D: Guarded external benchmark harness (unexecuted)
│   ├── run_safety_audit.py        # Standalone safety audit runner (16 test cases)
│   ├── generate_diagnosis_audit.py# Offline diagnosis audit evaluation script
│   ├── plot_detection_figures.py  # Figure generation script for detection benchmarks
│   ├── EXPERIMENT_A.md            # Experiment A specification
│   ├── EXPERIMENT_B.md            # Experiment B specification
│   └── EXPERIMENT_C.md            # Experiment C specification
│
├── scripts/                       # Dataset utilities & validation scripts
│   ├── ingest_anomod.py           # External AnoMod dataset ingestion and extraction utility
│   ├── audit_temporal_eligibility.py # Temporal continuity and sliding window yield auditor
│   └── smoke_test_checkpoint.py   # Checkpoint parameter, mode, and weight immutability test
│
├── audits/                        # Technical audits, decisions & gate reports
│   ├── README.md                  # Comprehensive index of all 41 audit documents
│   ├── AEGISOPS_MASTER_RESEARCH_HANDOFF.md # Master research handoff document
│   ├── UPDATED_SEVEN_PHASE_CHECKLIST.md # Master research checklist (v2.3.0)
│   ├── BOUNDED_CLAIMS_DECISION.md # Supervisory Path 3 ratification decision
│   ├── EXPERIMENT_D_*.md          # Forensic audits of Experiment D and external validation
│   ├── DATABASE_AUDIT.md          # SQLite database schema validation (manifest file)
│   ├── REPOSITORY_AUDIT.md        # Repository code audit (manifest file)
│   ├── MODEL_AND_EXECUTION_AUDIT.md # Model execution audit (manifest file)
│   ├── TEST_RESULTS.md            # Test execution audit (manifest file)
│   ├── PHASE_1_VERDICT.md         # Phase 1 completion verdict (manifest file)
│   └── [Gate Archives]            # Historical timestamped gate directories (preserved)
│
└── [Historical Archives]          # Retained historical baselines and prior audit snapshots
    ├── audit/                     # Early Phase 1 audits (DATA_AUDIT, LEAKAGE_AUDIT, PROJECT_AUDIT)
    ├── audit_reconciliation/      # Phase 2 audit reconciliation reports (01 through 08)
    ├── backup_prior_outputs/      # Prior experiment output backups
    ├── commands_and_logs/         # Historical reproduction logs and command records
    ├── controlled_experiment/     # Historical experiment protocol backups and readiness logs
    ├── exports/                   # Exported CSV telemetry and incident episodes
    └── figures/                   # Original detection figure exports
```

---

## 3. Scientific Invariants and Bounded-Claims Policy

1. **Frozen Checkpoint Contract**:
   - Model File: `models/lstm_autoencoder.pt` (SHA-256: `1cf44e6e82e459f543fcace25334f3076b76c77a357d46f65c11e3c44fd382de`).
   - Architecture: 3,733 PyTorch parameters (Encoder: 1,472; Decoder: 2,176; Output: 85).
   - Input Contract: 24-step normalized sequences ($\mathbf{X} \in \mathbb{R}^{24 \times 5}$) sampled at 5-second intervals ($\Delta t = 5\text{s}$, 120s window).
   - Features: `(cpu_pct, memory_pct, latency_ms, error_rate_pct, disk_pct)` with Z-score normalization.
   - Decision Threshold: $\tau = 0.7093990445137024$ (calibrated on $N=150$ held-out nominal validation windows).
2. **Canonical Benchmark Findings**:
   - Experiment A ($N=320$): Full Operational Rules (100% recall), LSTM AE (100% recall, 1.0% FPR), Isolation Forest (47.50% recall, 2.0% FPR).
   - Statistical Separation: Paired window-level exact McNemar $p = 2.168 \times 10^{-19}$ ($b=63, c=0$, descriptive); scenario-level Wilcoxon $W = 0.0, p = 0.03125$ ($N=6$, exploratory).
   - Experiment B ($N=6$): Live LLM Multi-Agent reached 83.33% strict / 100% lenient; deterministic rules reached 100% strict in 0.01 ms; LLM superiority is not claimed.
   - Experiment C ($N=16$): 100% attack containment (11/11 attacks blocked; Wilson CI $[0.7412, 1.0000]$) on localhost loopback interface.
3. **External Benchmark Status (Experiment D)**:
   - Production Experiment D remains **UNEXECUTED and DEFERRED** under Path 3.
   - Temporal resolution incompatibility ($\Delta t = 5$s vs. $15$s) and circular calibration leakage in the unexecuted harness (`v_win` reuse in lines 550 and 566) are fully documented.
