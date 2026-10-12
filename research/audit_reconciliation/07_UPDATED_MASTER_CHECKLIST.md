# 07 — Updated Master Research Checklist

**Document Version**: 2.1.0 (Phase 2 Evidence Reconciliation Audit)  
**Audit Date**: 2026-10-12  
**Auditor**: Senior Research Scientist & Experiment Integrity Lead  
**Scope**: Status evaluation of Phases 1 through 7 based strictly on verified raw evidence.

---

## Executive Phase Status Matrix

| Phase | Phase Title | Status | Supporting Primary Evidence | Next Required Action |
| :---: | :--- | :---: | :--- | :--- |
| **Phase 1** | Repository Audit & Stabilization | **VERIFIED COMPLETE** | [`research/audits/REPOSITORY_AUDIT.md`](file:///c:/DL_PROJECT/research/audits/REPOSITORY_AUDIT.md); 42/42 tests passing; read-only SQLite & PyTorch model verified. | Maintain read-only preservation of baseline assets. |
| **Phase 2** | Data & Label Validation | **VERIFIED COMPLETE** | [`research/audits/reconciliation_gate_20261012/DATA_ROW_RECONCILIATION.csv`](file:///c:/DL_PROJECT/research/audits/reconciliation_gate_20261012/DATA_ROW_RECONCILIATION.csv); 200 rows reconciled; 169 vs. 175 discrepancy resolved. | Accurately cite row-level mapping in manuscript Section 4. |
| **Phase 3** | Anomaly-Detection Experiment | **VERIFIED COMPLETE** | [`research/raw/detection_predictions.csv`](file:///c:/DL_PROJECT/research/raw/detection_predictions.csv) ($N=320$); exact McNemar $p = 2.17 \times 10^{-19}$ verified. | Report both physical and error-rate baseline rule definitions. |
| **Phase 4** | Root-Cause Diagnosis Experiment | **VERIFIED COMPLETE** | [`research/raw/diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_predictions.csv); factorial design ($7 \times 6 = 42$) mapped; ITT metrics verified. | Report as descriptive pilot benchmark with $N=6$ power limitations. |
| **Phase 5** | Safety & Recovery Experiment | **VERIFIED COMPLETE** | [`research/raw/safety_test_results.csv`](file:///c:/DL_PROJECT/research/raw/safety_test_results.csv); 16-case taxonomy reconciled; loopback containment confirmed. | Report 11/11 attacks blocked with Wilson CI $[0.741, 1.000]$. |
| **Phase 6** | Statistical Validation & Reproducibility | **VERIFIED COMPLETE** | [`research/run_all.py`](file:///c:/DL_PROJECT/research/run_all.py) executed (exit code 0, 53.6s); SHA-256 manifest produced. | Document virtual environment prerequisite and static figure assets. |
| **Phase 7** | Research-Paper Completion | **NOT STARTED** | Gated pending final user authorization to begin manuscript synthesis. | Author camera-ready research paper integrating audited findings. |

---

## Granular Phase Checklist & Evidence Tracing

### Phase 1: Repository Audit and Stabilization
- **Item 1.1**: Codebase inventory & dependency map  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: [`research/audits/REPOSITORY_AUDIT.md`](file:///c:/DL_PROJECT/research/audits/REPOSITORY_AUDIT.md), [`research/audit_reconciliation/01_REPOSITORY_AND_EVIDENCE_INVENTORY.md`](file:///c:/DL_PROJECT/research/audit_reconciliation/01_REPOSITORY_AND_EVIDENCE_INVENTORY.md).
- **Item 1.2**: Regression test suite baseline  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: Pytest execution log (`42 passed in 17.11s` in `.venv`).
- **Item 1.3**: Frozen model checkpoint preservation  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: `models/lstm_autoencoder.pt` (SHA-256: `df867ce9...`, size: 19,893 B).
- **Item 1.4**: Historical SQLite database protection  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: `data/aegisops_live.sqlite3` (SHA-256: `b8f33f63...`, size: 86,016 B).

### Phase 2: Data and Label Validation
- **Item 2.1**: SQLite schema and sample census  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: 200 rows verified (31 normal, 1 latency, 168 error).
- **Item 2.2**: 169 vs. 175 episode count reconciliation  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: [`research/audits/reconciliation_gate_20261012/DATA_ROW_RECONCILIATION.csv`](file:///c:/DL_PROJECT/research/audits/reconciliation_gate_20261012/DATA_ROW_RECONCILIATION.csv); proven that 175 was an error in prior narrative grouping transition rows into episodes.
- **Item 2.3**: Anomaly score provenance audit  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: 100% of historical DB rows confirmed collected under bootstrap rules (`anomaly_score = NULL`).
- **Item 2.4**: Pseudoreplication mitigation in telemetry  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: 168 consecutive error samples collapsed into a single continuous injection episode (EP-04).

### Phase 3: Anomaly-Detection Experiment (Experiment A)
- **Item 3.1**: Recomputation of confusion matrices & metrics  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: [`research/raw/detection_predictions.csv`](file:///c:/DL_PROJECT/research/raw/detection_predictions.csv), [`research/raw/detection_metrics.csv`](file:///c:/DL_PROJECT/research/raw/detection_metrics.csv).
- **Item 3.2**: Operational rules baseline reconciliation  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: Reconciled resource-only definition (33.3% recall) vs. error-rate definition (100% recall).
- **Item 3.3**: Threshold calibration & test-set independence  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: LSTM threshold calibrated on 120 validation windows (seed=42); test set synthesized with seed=2026 and scenario seeds 3001–3120. Zero leakage.
- **Item 3.4**: Paired statistical hypothesis testing  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: McNemar exact binomial test ($p = 2.168 \times 10^{-19}$), continuity-corrected $\chi^2 = 61.02$.

### Phase 4: Root-Cause Diagnosis Experiment (Experiment B)
- **Item 4.1**: Factorial design vs. 42 incidents reconciliation  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: 7 configurations evaluated across 6 ground-truth incidents ($7 \times 6 = 42$).
- **Item 4.2**: Separation of offline deterministic vs. live LLM  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: Disclosed regex heuristic fallback (`_local_root_cause`) in offline mode vs. Groq LLM API.
- **Item 4.3**: Intent-to-treat vs. completed-case metrics  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: Identified omitted cases (Config 5 dropped INC-1002; Config 7 dropped INC-1004); ITT accuracy computed as 83.3% (Multi-Agent Full) vs. 66.7% (Multi-Agent No-DL).
- **Item 4.4**: Statistical power disclosure  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: Formal power analysis showing $N=6 \implies 1-\beta \approx 0.14$; framed strictly as a pilot feasibility benchmark.

### Phase 5: Safety and Recovery Experiment (Experiment C)
- **Item 5.1**: Case total reconciliation  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: Reconciled 16-case inventory into 11 attacks, 2 failure checks, 1 verification probe, and 2 positive controls.
- **Item 5.2**: Boundary enforcement verification  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: 11/11 attacks blocked (100.0%, 95% Wilson CI: $[0.7412, 1.0000]$).
- **Item 5.3**: Production function testing on disposable harness  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: Verified against `approval.ApprovalStore` (`BEGIN IMMEDIATE` locking) on loopback `127.0.0.1:8765`.

### Phase 6: Statistical Validation and Reproducibility
- **Item 6.1**: Statistical helper audit & exact benchmark check  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: Benchmarked $b=4, c=2 \implies p=0.6875$ verified and passing in `test_statistical_audit.py`.
- **Item 6.2**: End-to-end pipeline execution  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: `research/run_all.py` executed successfully (exit code 0, 53.6s, 42 tests passed).
- **Item 6.3**: SHA-256 artifact manifest generation  
  *Status*: **VERIFIED COMPLETE**  
  *Evidence*: `research/MANIFEST_SHA256.json` regenerated for 22 artifacts.

### Phase 7: Research-Paper Completion
- **Item 7.1**: Manuscript synthesis adhering to reconciled evidence  
  *Status*: **NOT STARTED**  
  *Next Required Action*: Author camera-ready research paper integrating all audited findings.
- **Item 7.2**: Publication figures embedding & verification  
  *Status*: **NOT STARTED**  
  *Next Required Action*: Embed Figures 1 and 2 with reconciled dual-definition captions.
- **Item 7.3**: Final submission package & review  
  *Status*: **NOT STARTED**  
  *Next Required Action*: Final proofreading against audit standards.

---

## Overall Readiness Verdict for Manuscript Synthesis

**READINESS VERDICT**: **READY FOR PHASE 7 MANUSCRIPT AUTHORING**

### Prioritized Remaining Blockers:
1. **Zero Technical or Experimental Blockers**: All empirical evidence, test results, statistical metrics, and security evaluations are 100% reconciled and captured in machine-readable records.
2. **Procedural Blocker**: Formal user sign-off to begin Phase 7 manuscript drafting.
