# AegisOps Manuscript Finalization Plan (Path 3 Bounded Claims)

**Document Identifier**: `AEGISOPS-PLAN-MANUSCRIPT-FINALIZATION`  
**Date**: October 13, 2026  
**Author**: Senior ML Research Supervisor & Scientific Auditor  
**Repository**: `C:\DL_PROJECT`  
**Git HEAD**: `d277c1df3c2599ddecdf5f0bb761c99718499667`  
**Status**: Active Production Plan for Manuscript Sign-Off  

---

## 1. Overview and Core Scope Alignment

This document outlines the systematic finalization workflow for [`research/paper/AEGISOPS_RESEARCH_PAPER.md`](file:///c:/DL_PROJECT/research/paper/AEGISOPS_RESEARCH_PAPER.md) under the ratified **Path 3: Bounded-Claims Policy** ([`BOUNDED_CLAIMS_DECISION.md`](file:///c:/DL_PROJECT/research/audits/BOUNDED_CLAIMS_DECISION.md)).

### Strategic Policy Parameters:
1. **Confirmatory Scope**: Bounded strictly to verified experiments:
   - **Experiment A**: Synthetic Anomaly Detection Benchmark ($N = 320$ windows; $120$ fault, $200$ normal).
   - **Experiment B**: Root-Cause Diagnosis Pilot ($N = 6$ canonical incident scenarios).
   - **Experiment C**: Security Boundary Execution Barrier ($N = 16$ evaluations; $11$ attacks, $2$ preconditions, $1$ probe, $2$ controls).
   - **System Verification**: Reproducibility, SHA-256 manifests, and bit-for-bit numerical determinism ($5.55 \times 10^{-17}$ max diff).
2. **Excluded Scope**:
   - Confirmatory external deep-learning validation on AnoMod is **formally excluded** from immediate paper claims due to sequence-length mismatch ($W=24$ vs $W=8$) and severe zero-shot domain shift ($100\%$ nominal false alarm rate).
   - AnoMod is discussed strictly as a pre-registered benchmark and future work target.
3. **No Unsubstantiated Superiority**:
   - Multi-agent LLM is presented as a flexible fallback synthesizer, explicitly disclosing that deterministic rules achieved 100% accuracy in 0.01 ms vs LLM 83.33% in 4.78s.
   - Combined detector is presented as architectural defense-in-depth, explicitly disclosing zero additive statistical sensitivity on the synthetic benchmark.

---

## 2. Section-by-Section Mapping & Drafting Readiness

| # | Target Paper Section | Current State in Manuscript | Verified Evidence Source | Action Required for Finalization | Drafting Readiness |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **1** | **Abstract** | Fully written ([`AEGISOPS_RESEARCH_PAPER.md:11-18`](file:///c:/DL_PROJECT/research/paper/AEGISOPS_RESEARCH_PAPER.md#L11-L18)). Accurately summarizes Experiments A, B, C with sample sizes, $p$-values, and explicit caveats. | [`MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`](file:///c:/DL_PROJECT/research/paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md) (CLM-01 through CLM-07, CLM-12, CLM-16) | Verify wording matches exact metrics in Table 1, 2, 4. Ensure no reference to completed external validation. | **READY** |
| **2** | **Introduction & Problem Motivation** | Fully written (§1, lines 21–58). Covers incident lifecycle bottlenecks: diagnostic ambiguity, remediation risk, verification neglect, reproducibility deficits. | Code architecture in `collectors/`, `models/`, `agents.py`, `approval.py`, `live_monitoring.py` | Verify that research questions RQ1–RQ4 align strictly with synthetic detection, pilot diagnosis, safety barrier, and closed-loop integration. | **READY** |
| **3** | **Related Work & Literature Survey** | Fully written (§2, lines 60–128). Covers multivariate anomaly detection, AIOps root cause analysis, LLM agent workflows, automated remediation safety. | 16 peer-reviewed references with verified DOIs and arXiv IDs (Audibert, Liu, Malhotra, Ping, Su, Zhang, Wu). | Verify citation formatting. Confirm AnoMod citation (Ping et al., 2026) is framed as related benchmark work, not completed validation. | **READY** |
| **4** | **Research Gap & Bounded Claims** | Fully written (§3 & §4, lines 130–215). Details the disconnect between open-loop detectors and active remediation. | [`BOUNDED_CLAIMS_DECISION.md`](file:///c:/DL_PROJECT/research/audits/BOUNDED_CLAIMS_DECISION.md), [`MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`](file:///c:/DL_PROJECT/research/paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md) | Ensure contribution bullet points emphasize architectural integration, two-man-rule barrier, and reproducible closed-loop validation. | **READY** |
| **5** | **Proposed Methodology & Novelty** | Fully written (§4, lines 175–218). Dual-gate detection formulation, feature reconstruction attribution, supervisor synthesis, atomic approval. | Mathematical formulations in [`AEGISOPS_RESEARCH_PAPER.md`](file:///c:/DL_PROJECT/research/paper/AEGISOPS_RESEARCH_PAPER.md); model definitions in `dl/anomaly_detector.py` | Verify parameter count is stated as **3,733 parameters** (correcting historical 3,605). | **READY (Text Update)** |
| **6** | **System Architecture & Data Flow** | Fully written (§5, lines 220–358). Contains Figures 1, 2, and 3 in Mermaid syntax illustrating data flow, agent interactions, and approval barriers. | [`FIGURE_AND_TABLE_INDEX.md`](file:///c:/DL_PROJECT/research/paper/FIGURE_AND_TABLE_INDEX.md), [`approval.py`](file:///c:/DL_PROJECT/approval.py), [`live_monitoring.py`](file:///c:/DL_PROJECT/live_monitoring.py) | Verify Mermaid syntax renders cleanly. Confirm loopback HTTP boundary (`127.0.0.1:8765`) and SQLite storage are highlighted. | **READY** |
| **7** | **Algorithms & Pseudocode** | Fully written (§5.3 & §5.4, lines 280–355). Algorithm 1: Dual-Gate Anomaly Detection & Attribution; Algorithm 2: Approval-Gated Remediation. | Implementation in [`dl/anomaly_detector.py`](file:///c:/DL_PROJECT/dl/anomaly_detector.py) and [`approval.py`](file:///c:/DL_PROJECT/approval.py) | Review mathematical notation in Algorithm 1 ($\mathbf{x}_t \in \mathbb{R}^5$, $\tau = 0.709399$) and Algorithm 2 (UUIDv4 token, 300s TTL). | **READY** |
| **8** | **Experimental Datasets & Protocols** | Fully written (§6, lines 360–428). Defines Experiment A ($N=320$), Experiment B ($N=6$), Experiment C ($N=16$), metrics, and evaluation baselines. | [`CORRECTED_DETECTION_METRICS.csv`](file:///c:/DL_PROJECT/research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv), [`diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_predictions.csv), [`safety_test_results.csv`](file:///c:/DL_PROJECT/research/raw/safety_test_results.csv) | Ensure 3 rule baselines (Narrow, Resource-Only, Full Operational) are explicitly defined. Reaffirm that operational alarms/hr is unavailable. | **READY** |
| **9** | **Results & Comparison Tables** | Fully written (§7, §8, §9, lines 430–655). Contains Table 1 (Detection), Table 2 (RCA), Table 3 (Attribution), Table 4 (Safety), Table 5 (Stats), Fig A.1, A.2. | Machine-readable CSVs in `research/raw/` and `research/audits/` | Cross-check every table cell against `MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`. Confirm exact matches with zero discrepancies. | **READY** |
| **10** | **Statistical Analysis & Uncertainty** | Fully written (§10, lines 660–718). Paired McNemar test, scenario-level Wilcoxon signed-rank test, Wilson score CIs. | [`STATISTICAL_ASSUMPTION_REVIEW.md`](file:///c:/DL_PROJECT/research/audits/detection_rate_and_phase4_gate_20261012/STATISTICAL_ASSUMPTION_REVIEW.md) | Disclose that window McNemar ($p = 2.17 \times 10^{-19}$) is descriptive due to temporal clustering; scenario Wilcoxon ($p = 0.03125$) is primary inference. | **READY** |
| **11** | **Discussion & Threats to Validity** | Fully written (§11, lines 720–778). Covers synthetic domain gap, cold-start telemetry, RCA sample size ($1-\beta \approx 0.14$), security boundary limits. | [`MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`](file:///c:/DL_PROJECT/research/paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md) (CLM-15, CLM-18, CLM-19, CLM-20) | Re-verify that external AnoMod evaluation is transparently documented as excluded from confirmatory claims due to sequence length & domain shift. | **READY** |
| **12** | **Conclusion & Future Work** | Fully written (§12, lines 780–792). Summarizes contributions and outlines future work. | Research Roadmap | Confirm Future Work targets: (1) high-frequency external microservice telemetry; (2) on-premise SLMs; (3) streaming deduplication. | **READY** |
| **13** | **References** | Fully written (§References, lines 795–812). 16 verified references with complete DOIs, authors, years, and venue metadata. | [`REFERENCE_VERIFICATION.md`](file:///c:/DL_PROJECT/research/paper/REFERENCE_VERIFICATION.md) | Verify all 16 citations are referenced in the body text. Zero hallucinated citations. | **READY** |

---

## 3. Figures and Tables Verification Register

| Identifier | Description | Source File / Generating Script | Verification Status | Action Required |
| :--- | :--- | :--- | :---: | :--- |
| **Figure 1** | System Architecture & Closed-Loop Flow | Textual Mermaid in §5.1 | **VERIFIED** | Confirm layout rendering and boundary labels (`127.0.0.1:8765`). |
| **Figure 2** | Two-Stage Detection & 4-Agent Pipeline | Textual Mermaid in §5.2 | **VERIFIED** | Confirm dual-gate logic and feature attribution handoff arrows. |
| **Figure 3** | Two-Man Rule Approval & Probe Flow | Textual Mermaid in §5.3 | **VERIFIED** | Confirm token generation, TTL timer, and loopback probe verification. |
| **Figure A.1** | Anomaly Detection Confusion Matrices (4-panel) | [`research/figures/detection_confusion_matrices.png`](file:///c:/DL_PROJECT/research/figures/detection_confusion_matrices.png) | **VERIFIED** | Confirm PNG exists and matches Table 1 TP/FP/TN/FN counts. |
| **Figure A.2** | Comparative Detection Bar Charts | [`research/figures/detection_comparison.png`](file:///c:/DL_PROJECT/research/figures/detection_comparison.png) | **VERIFIED** | Confirm PNG exists and plots Rules, IF, LSTM, and Combined accurately. |
| **Table 1** | Anomaly Detection Performance Benchmark | [`CORRECTED_DETECTION_METRICS.csv`](file:///c:/DL_PROJECT/research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv) | **VERIFIED** | Verify 7 rows: Narrow, Resource, Full Rules, IF, LSTM, Combined, plus metadata. |
| **Table 2** | RCA Performance Across 7 Configurations | [`research/raw/diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_predictions.csv) | **VERIFIED** | Verify strict and lenient accuracy percentages for all 7 configurations. |
| **Table 3** | Scenario-by-Scenario Diagnostic Breakdown | [`research/exports/incident_scenarios.csv`](file:///c:/DL_PROJECT/research/exports/incident_scenarios.csv) | **VERIFIED** | Verify `INC-1001` through `INC-1006` root causes and signal attributions. |
| **Table 4** | Execution Boundary Security Test Suite | [`research/raw/safety_test_results.csv`](file:///c:/DL_PROJECT/research/raw/safety_test_results.csv) | **VERIFIED** | Verify 11 attacks ($100\%$), 2 preconditions, 1 probe, 2 controls. |
| **Table 5** | Hypothesis Testing & Confidence Intervals | [`STATISTICAL_ASSUMPTION_REVIEW.md`](file:///c:/DL_PROJECT/research/audits/detection_rate_and_phase4_gate_20261012/STATISTICAL_ASSUMPTION_REVIEW.md) | **VERIFIED** | Verify McNemar $\chi^2$, Wilcoxon $W=0.0$, and Wilson Score CIs. |

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
   - *Requirement*: Table 1 and Section 7 must present all three rule baselines: Narrow Rules (33.33%), Resource-Only Rules (66.67%), and Full Operational Rules (100.0%).
   - *Verification*: Table 1 contains explicit rows for each rule definition.
4. **Criterion QC-4 (Operational Alarm Rate Integrity)**:
   - *Requirement*: Operational false alarms per hour must be marked `UNAVAILABLE` in Table 1 and text.
   - *Verification*: No unqualified claim of "7.2 false alarms/hour" exists in the manuscript.
5. **Criterion QC-5 (No LLM Superiority Claim)**:
   - *Requirement*: Section 8 and Abstract must state that deterministic rules achieved 100.0% accuracy in 0.01 ms vs LLM 83.33% in 4.78s, explicitly refuting LLM superiority on this suite.
   - *Verification*: Text explicitly discloses low sample size ($N=6$, $1-\beta \approx 0.14$) and rubric keyword overlap.
6. **Criterion QC-6 (Security Boundary Precision)**:
   - *Requirement*: Section 9 must state that safety barriers apply within the local application runtime and loopback HTTP boundary (`127.0.0.1:8765`).
   - *Verification*: Text prohibits extrapolating boundary guarantees to OS kernel or cloud control planes.
7. **Criterion QC-7 (Automated Test Regression Cleanliness)**:
   - *Requirement*: Repository regression test suite must pass 100% cleanly without errors or skips.
   - *Verification*: `pytest test_experiment_d_harness.py` passes 40/40 tests; full repository passes 105/105 tests.
