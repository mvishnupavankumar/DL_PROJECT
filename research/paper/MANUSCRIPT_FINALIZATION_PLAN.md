# AegisOps Manuscript Finalization Plan (Path 3 Bounded Claims)

**Document Identifier**: `AEGISOPS-PLAN-MANUSCRIPT-FINALIZATION`  
**Date**: October 13, 2026  
**Author**: Senior ML Research Supervisor & Scientific Auditor  
**Repository**: `C:\DL_PROJECT`  
**Current Repository HEAD**: `a32713c30a8ddca1425d44b1afbaf6d55a64c276` (Branch: `publish/research-without-external-dataset`; Historical Baseline Commit: `d277c1df3c2599ddecdf5f0bb761c99718499667`)
**Status**: Active Production Plan for Manuscript Sign-Off  

---

## 1. Overview and Core Scope Alignment

This document outlines the systematic finalization workflow for [`research/paper/AEGISOPS_RESEARCH_PAPER.md`](AEGISOPS_RESEARCH_PAPER.md) under the ratified **Path 3: Bounded-Claims Policy** ([`BOUNDED_CLAIMS_DECISION.md`](../../research/audits/BOUNDED_CLAIMS_DECISION.md)).

### Strategic Policy Parameters:
1. **Confirmatory Scope**: Bounded strictly to verified experiments:
   - **Experiment A**: Synthetic Anomaly Detection Benchmark ($N = 320$ windows; $120$ fault, $200$ normal).
   - **Experiment B**: Root-Cause Diagnosis Pilot ($N = 6$ canonical incident scenarios).
   - **Experiment C**: Security Boundary Execution Barrier ($N = 16$ evaluations; $11$ attacks, $2$ preconditions, $1$ probe, $2$ controls).
   - **System Verification**: SHA-256 manifests and numerical reproducibility within the measured floating-point tolerance ($5.55 \times 10^{-17}$ maximum score difference; zero alert-flag disagreements).
2. **Excluded Scope**:
   - Confirmatory external deep-learning validation on AnoMod is **formally excluded** from immediate paper claims due to sequence-length mismatch ($W=24$ vs $W=8$) and severe zero-shot domain shift ($100\%$ nominal false alarm rate).
   - AnoMod is discussed strictly as a pre-registered benchmark and future work target.
3. **No Unsubstantiated Superiority**:
   - Multi-agent LLM is presented as a flexible fallback synthesizer, explicitly disclosing that deterministic rules achieved 100% accuracy in 0.01 ms vs LLM 83.33% in 23.19s.
   - Combined detector is presented as architectural defense-in-depth, explicitly disclosing zero additive statistical sensitivity on the synthetic benchmark.

---

## 2. Section-by-Section Mapping & Drafting Readiness

| # | Target Paper Section | Current State in Manuscript | Verified Evidence Source | Action Required for Finalization | Drafting Readiness |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **1** | **Abstract** | Fully written ([`AEGISOPS_RESEARCH_PAPER.md:11-18`](AEGISOPS_RESEARCH_PAPER.md#L11-L18)). Accurately summarizes Experiments A, B, C with sample sizes, $p$-values, and explicit caveats. | [`MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`](MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md) (CLM-01 through CLM-07, CLM-12, CLM-16) | Verify wording matches exact metrics in Table 1, 2, 4. Ensure no reference to completed external validation. | **READY** |
| **2** | **Introduction & Problem Motivation** | Fully written (§1, lines 21–58). Covers incident lifecycle bottlenecks: diagnostic ambiguity, remediation risk, verification neglect, reproducibility deficits. | Code architecture in `collectors/`, `models/`, `agents.py`, `approval.py`, `live_monitoring.py` | Verify that research questions RQ1–RQ4 align strictly with synthetic detection, pilot diagnosis, safety barrier, and closed-loop integration. | **READY** |
| **3** | **Related Work & Literature Survey** | Fully written (§2, lines 60–128). Covers multivariate anomaly detection, AIOps root cause analysis, LLM agent workflows, automated remediation safety. | 16 peer-reviewed references with verified DOIs and arXiv IDs (Audibert, Liu, Malhotra, Ping, Su, Zhang, Wu). | Verify citation formatting. Confirm AnoMod citation (Ping et al., 2026) is framed as related benchmark work, not completed validation. | **READY** |
| **4** | **Research Gap & Bounded Claims** | Fully written (§3 & §4, lines 130–215). Details the disconnect between open-loop detectors and active remediation. | [`BOUNDED_CLAIMS_DECISION.md`](../../research/audits/BOUNDED_CLAIMS_DECISION.md), [`MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`](MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md) | Ensure contribution bullet points emphasize architectural integration, scope-bound human approval barrier, and reproducible closed-loop validation. | **READY** |
| **5** | **Proposed Methodology & Novelty** | Fully written (§4, lines 175–218). Dual-gate detection formulation, feature reconstruction attribution, supervisor synthesis, atomic approval. | Mathematical formulations in [`AEGISOPS_RESEARCH_PAPER.md`](AEGISOPS_RESEARCH_PAPER.md); model definitions in `dl/anomaly_detector.py` | Verify parameter count is stated as **3,733 parameters** (correcting historical 3,605). | **READY (Text Update)** |
| **6** | **System Architecture & Data Flow** | Fully written (§5, lines 220–358). Contains Figures 1, 2, and 3 in Mermaid syntax illustrating data flow, agent interactions, and approval barriers. | [`FIGURE_AND_TABLE_INDEX.md`](FIGURE_AND_TABLE_INDEX.md), [`approval.py`](../../approval.py), [`live_monitoring.py`](../../live_monitoring.py) | Verify Mermaid syntax renders cleanly. Confirm loopback HTTP boundary (`127.0.0.1:8765`) and SQLite storage are highlighted. | **READY** |
| **7** | **Algorithms & Pseudocode** | Fully written (§5.3 & §5.4, lines 280–355). Algorithm 1: Dual-Gate Anomaly Detection & Attribution; Algorithm 2: Approval-Gated Remediation. | Implementation in [`dl/anomaly_detector.py`](../../dl/anomaly_detector.py) and [`approval.py`](../../approval.py) | Review mathematical notation in Algorithm 1 ($\mathbf{x}_t \in \mathbb{R}^5$, $\tau = 0.709399$) and Algorithm 2 (UUIDv4 token, 300s TTL). | **READY** |
| **8** | **Experimental Datasets & Protocols** | Fully written and corrected against the final raw-CSV audit. | `research/raw/` CSVs and `FINAL_RAW_CSV_RECALCULATION.txt` | Full Rules are verified; Narrow/Resource figures are historical comparators with an explicit source limitation. | **CORRECTED** |
| **9** | **Results & Comparison Tables** | Tables aligned to the final raw-CSV audit. | Machine-readable CSVs in `research/raw/` and `research/audits/` | LSTM PR-AUC corrected to 1.0000; diagnosis and safety denominators reconciled; final visual/reference review remains. | **CORRECTED — FINAL MANUAL REVIEW REQUIRED** |
| **10** | **Statistical Analysis & Uncertainty** | Fully written (§10, lines 660–718). Paired McNemar test, scenario-level Wilcoxon signed-rank test, Wilson score CIs. | [`STATISTICAL_ASSUMPTION_REVIEW.md`](../../research/audits/detection_rate_and_phase4_gate_20261012/STATISTICAL_ASSUMPTION_REVIEW.md) | Disclose that window McNemar ($p = 2.17 \times 10^{-19}$) is descriptive due to temporal clustering; scenario Wilcoxon ($p = 0.03125$) is post-hoc exploratory, not confirmatory inference. | **CORRECTED — FINAL MANUAL REVIEW REQUIRED** |
| **11** | **Discussion & Threats to Validity** | Fully written (§11, lines 720–778). Covers synthetic domain gap, cold-start telemetry, RCA sample size ($1-\beta \approx 0.14$), security boundary limits. | [`MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`](MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md) (CLM-15, CLM-18, CLM-19, CLM-20) | Re-verify that external AnoMod evaluation is transparently documented as excluded from confirmatory claims due to sequence length & domain shift. | **READY** |
| **12** | **Conclusion & Future Work** | Fully written (§12, lines 780–792). Summarizes contributions and outlines future work. | Research Roadmap | Confirm Future Work targets: (1) high-frequency external microservice telemetry; (2) on-premise SLMs; (3) streaming deduplication. | **READY** |
| **13** | **References** | Fully written (§References, lines 795–812). 16 verified references with complete DOIs, authors, years, and venue metadata. | [`REFERENCE_VERIFICATION.md`](REFERENCE_VERIFICATION.md) | Verify all 16 citations are referenced in the body text. Zero hallucinated citations. | **READY** |

---

## 3. Figures and Tables Verification Register

| Identifier | Description | Source File / Generating Script | Verification Status | Action Required |
| :--- | :--- | :--- | :---: | :--- |
| **Figure 1** | System Architecture & Closed-Loop Flow | Textual Mermaid in §5.1 | **VERIFIED** | Confirm layout rendering and boundary labels (`127.0.0.1:8765`). |
| **Figure 2** | Two-Stage Detection & 4-Agent Pipeline | Textual Mermaid in §5.2 | **VERIFIED** | Confirm dual-gate logic and feature attribution handoff arrows. |
| **Figure 3** | Scope-Bound Human Approval & Probe Flow | Textual Mermaid in §5.3 | **VERIFIED** | Confirm token generation, TTL timer, and loopback probe verification. |
| **Figure A.1** | Anomaly Detection Confusion Matrices (4-panel) | [`research/figures/detection_confusion_matrices.png`](../../research/figures/detection_confusion_matrices.png) | **VERIFIED** | Confirm PNG exists and matches Table 1 TP/FP/TN/FN counts. |
| **Original Figure A.2** | Historical Comparative Detection Bar Chart | [`research/figures/detection_comparison.png`](../../research/figures/detection_comparison.png) | **BLOCKED FROM RELEASE** | Preserve for provenance only: it displays obsolete operational FA/hr labels. Release use requires the separately generated replacement figure. |
| **Figure A.2 Release Candidate** | Audited Comparative Detection Bar Chart | [`research/exports/detection_comparison_release.png`](../exports/detection_comparison_release.png) | **VERIFIED FOR FIGURE CONTENT** | Use only after final rendered-manuscript review. It contains Full Rules, IF, LSTM, and Combined values, measured batch latency, and explicit `UNAVAILABLE` operational FA/hr. |
| **Table 1** | Anomaly Detection Performance Benchmark | [`CORRECTED_DETECTION_METRICS.csv`](../../research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv) | **VERIFIED** | Verify 7 rows: Narrow, Resource, Full Rules, IF, LSTM, Combined, plus metadata. |
| **Table 2** | RCA Performance Across 7 Configurations | [`research/raw/diagnosis_predictions.csv`](../../research/raw/diagnosis_predictions.csv) | **VERIFIED** | Verify strict and lenient accuracy percentages for all 7 configurations. |
| **Table 3** | Scenario-by-Scenario Diagnostic Breakdown | [`research/exports/incident_scenarios.csv`](../../research/exports/incident_scenarios.csv) | **VERIFIED** | Verify `INC-1001` through `INC-1006` root causes and signal attributions. |
| **Table 4** | Execution Boundary Security Test Suite | [`research/raw/safety_test_results.csv`](../../research/raw/safety_test_results.csv) | **VERIFIED** | Verify 11 attacks ($100\%$), 2 preconditions, 1 probe, 2 controls. |
| **Supporting Analysis S1** (not a manuscript table) | Hypothesis Testing & Confidence Intervals | [`STATISTICAL_ASSUMPTION_REVIEW.md`](../../research/audits/detection_rate_and_phase4_gate_20261012/STATISTICAL_ASSUMPTION_REVIEW.md) | **VERIFIED WITH QUALIFICATION** | Retain McNemar as descriptive, Wilcoxon as post-hoc exploratory, and Wilson intervals as binomial synthetic-sample intervals. |

---

## 4. Measurable Quality-Control Acceptance Criteria

Before authorial sign-off and final camera-ready packaging, the manuscript must satisfy the following 7 measurable acceptance criteria:

1. **Criterion QC-1 (Parameter Count Consistency)**:
   - *Requirement*: Every reference to the LSTM Autoencoder parameter count must state **3,733 parameters** (or 3.7k parameters).
   - *Verification*: Grep for `3,605` across `research/paper/` must return 0 matches.
2. **Criterion QC-2 (Zero External Validation Claims)**:
   - *Requirement*: The manuscript body, abstract, tables, and conclusion must NOT claim completed external benchmark validation of the LSTM Autoencoder on AnoMod.
   - *Verification*: AnoMod must be mentioned only in Related Work and Threats to Validity / Future Work as a pre-registered benchmark target.
3. **Criterion QC-3 (Rule Baseline Differentiation)**:
   - *Requirement*: Table 1 distinguishes Full Operational Rules (verified from current raw predictions) from Narrow (33.33%) and Resource-Only (66.67%) historical comparator outputs.
   - *Verification*: The source limitation appears beside the historical comparator rows.
4. **Criterion QC-4 (Operational Alarm Rate Integrity)**:
   - *Requirement*: Operational false alarms per hour must be marked `UNAVAILABLE` in Table 1 and text.
   - *Verification*: No unqualified claim of "7.2 false alarms/hour" exists in the manuscript.
5. **Criterion QC-5 (No LLM Superiority Claim)**:
   - *Requirement*: Section 8 and Abstract must state that deterministic rules achieved 100.0% accuracy in 0.01 ms vs LLM 83.33% in 23.19s, explicitly refuting LLM superiority on this suite.
   - *Verification*: Text explicitly discloses low sample size ($N=6$, $1-\beta \approx 0.14$) and rubric keyword overlap.
6. **Criterion QC-6 (Security Boundary Precision)**:
   - *Requirement*: Section 9 must state that safety barriers apply within the local application runtime and loopback HTTP boundary (`127.0.0.1:8765`).
   - *Verification*: Text prohibits extrapolating boundary guarantees to OS kernel or cloud control planes.
7. **Criterion QC-7 (Automated Test Regression Cleanliness)**:
   - *Requirement*: Repository regression test suite must pass 100% cleanly without errors or skips.
   - *Verification*: `pytest test_experiment_d_harness.py` passes 40/40 tests; full repository passes 107/107 tests.

### Phase 18 release-control reconciliation (2026-10-18)

The seven criteria above are retained as historical plan acceptance criteria. They use QC identifiers that overlap with a different eight-item supervisory-audit taxonomy in `FINAL_EVIDENCE_AUDIT.md`; neither historical identifier set should be used alone as the current publication gate. `PHASE18_CANONICAL_MANUSCRIPT_RELEASE_CHECKLIST.md` supplies the current stable `REL-01` through `REL-12` release controls, including the current full-suite result, rendering readiness, provenance, metadata, and independent-release-decision requirements. It preserves this plan and prior evidence rather than renumbering historical findings.
