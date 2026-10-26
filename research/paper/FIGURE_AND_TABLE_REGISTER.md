# AegisOps: Figure and Table Evidence Register

**Document Path**: `research/paper/FIGURE_AND_TABLE_REGISTER.md`  
**Associated Manuscript**: `research/paper/AEGISOPS_RESEARCH_PAPER.md`  
**Audit Baseline**: Audited Repository Baseline (`8aff34c8`)  
**Status**: Verified & Reconciled  

---

## 1. Register Overview

This document provides a complete audit registry for every figure, diagram, and table included in the AegisOps research manuscript. Each entry details the artifact identifier, caption, raw data source, generator script, sample size ($N$), defined experimental unit, and reconciliation status.

---

## 2. Figures and Diagrams Register

| Figure ID | Artifact Path | Format | Generator / Source | Experimental Unit & Sample Size | Verification Status & Reconciled Values |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Figure 1** | `research/paper/figures/architecture_dataflow.mmd` | Mermaid / Vector | Hand-authored from system code paths: `collectors/system_metrics.py`, `models/lstm_autoencoder.py`, `agents.py`, `approval.py`, `live_monitoring.py` | Full Architecture (5 functional layers, 15 components) | **VERIFIED**: Reflects exact runtime component boundaries, SQLite transactional locks, loopback endpoints, and verification probes. |
| **Figure 2** | `research/paper/figures/detection_diagnosis_workflow.mmd` | Mermaid / Vector | Hand-authored from `models/lstm_autoencoder.py`, `agents.py`, and `research/experiments/run_experiment_a.py` | Detection to Diagnosis Workflow ($W=24$ sequence buffer to 4-agent pipeline) | **VERIFIED**: Shows dual-gate threshold checks ($\tau = 0.709399$), per-feature MSE attribution injection into `InvestigatorAgent`, and candidate class schema. |
| **Figure 3** | `research/paper/figures/approval_recovery_workflow.mmd` | Mermaid / Vector | Hand-authored from `approval.py` and `live_monitoring.py` | Remediation & Governance Lifecycle (Ticket creation to post-probe verification) | **VERIFIED**: Documents UUIDv4 nonce, TTL ($300$s), atomic `BEGIN IMMEDIATE` lock, loopback allowlist, `/probe` verification, and audit persistence. |
| **Figure A.1** (Supplementary) | `research/figures/detection_confusion_matrices.png` | PNG (27.9 KB) | `research/experiments/run_experiment_a.py` -> `research/figures/detection_confusion_matrices.png` | $N = 320$ sequence windows (200 normal, 120 fault across 6 classes) | **VERIFIED**: Displays 4 contingency matrices: Full Operational Rules (120 TP, 0 FN, 200 TN, 0 FP); Isolation Forest (57 TP, 63 FN, 196 TN, 4 FP); LSTM AE (120 TP, 0 FN, 198 TN, 2 FP); Combined (120 TP, 0 FN, 198 TN, 2 FP). |
| **Figure A.2** (Supplementary; excluded from release distribution) | `research/figures/detection_comparison.png` | PNG (16.8 KB) | `research/experiments/run_experiment_a.py` -> `research/figures/detection_comparison.png` | $N = 320$ sequence windows (200 normal, 120 fault across 6 classes) | **BLOCKED FOR RELEASE**: Bars match the named detector metrics, but visual inspection found stale operational FA/hr labels (IF 14.4; LSTM/Combined 7.2). The active evidence classifies operational FA/hr as UNAVAILABLE. The unembedded historical PNG was preserved and must not be distributed until regenerated under separately authorized figure maintenance. |
| **Figure A.2** (Release Candidate) | `research/exports/detection_comparison_release.png` | PNG (66.7 KB); SHA-256 `701bd163df34d3acd965b55adf913798b23041e327016dbc5b0c30fa108dc69c` | `research/exports/generate_detection_comparison_release.ps1`; fixed audited values from `FINAL_RAW_CSV_RECALCULATION.txt`, no experiment runner or inference | $N = 320$ sequence windows (200 normal, 120 fault across 6 archetypes) | **VERIFIED FOR RELEASE FIGURE CONTENT**: Full Rules, IF, LSTM, and Combined only; precision/recall/F1 and measured batch mean latency are legible and match the audit. Operational FA/hr is explicitly `UNAVAILABLE`; no Narrow/Resource historical comparators are plotted. Original Figure A.2 remains excluded. |

---

## 3. Results Tables Register

| Table ID | Table Title | Primary Source Artifact | Generator Script | Experimental Unit & Sample Size | Reported Values & Reconciliation Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Table 1** | Comprehensive Anomaly Detection Benchmark Results | `research/raw/detection_metrics.csv`, `research/raw/detection_predictions.csv` | `research/experiments/run_experiment_a.py` | 24-step normalized sequence window ($N = 320$: $200$ normal, $120$ fault) | **CORRECTED**: Full Rules, IF, LSTM, and Combined counts are verified; LSTM trapezoidal PR-AUC is 1.0000. Narrow (33.33%) and Resource-Only (66.67%) are explicitly historical comparator outputs because their flags are absent from the current prediction CSV. PR-AUC for binary rules and FA/hr are marked UNAVAILABLE. |
| **Table 2** | Diagnostic Evaluation Across Configurations | `research/raw/diagnosis_metrics.csv`, `research/raw/diagnosis_predictions.csv` | `research/experiments/generate_diagnosis_audit.py` | Canonical Incident Scenario ($N = 6$ scenarios across 7 configurations = 42 evaluations) | **VERIFIED**: Reports Intent-to-Treat ($N=6$) strict and lenient accuracies: Live LLM Multi-Agent + DL = 83.33% strict ($5/6$), 100.0% lenient ($6/6$); Live LLM Multi-Agent No-DL = 66.67% strict ($4/6$); Completed-case accuracies (4/5 = 80.00% for Configs 5 and 7); Offline heuristics reported faithfully. Model provider: `openai/gpt-oss-20b` via Groq Cloud API. |
| **Table 3** | Scenario-by-Scenario Diagnostic Breakdown | `research/raw/diagnosis_predictions.csv` | `research/experiments/generate_diagnosis_audit.py` | Individual Incidents `INC-1001` through `INC-1006` | **VERIFIED**: Maps ground truth fault modes to predicted root causes and reconstruction attribution signals. Identifies database service stopped (`INC-1002`) as the strict failure (scored lenient match due to disk contention attribution); `INC-1006` passed strict match. |
| **Table 4** | Safety, Governance, and Execution Boundary Test Suite | `research/raw/safety_metrics.csv`, `research/raw/safety_test_results.csv` | `research/experiments/run_safety_audit.py` | Discrete Safety Test Case ($N = 16$ evaluations) | **VERIFIED**: Disaggregates 11 adversarial attacks ($11/11$ blocked, 100.0%, Wilson CI $[0.7412, 1.0000]$), 2 precondition failures, 1 false-recovery probe check, and 2 positive controls. Mean attack check latency 11.32 ms. |

---

## 4. Verification Check of Discrepancies and Clarifications

1. **Unit of Analysis**:
   - In Table 1, the unit of analysis is explicitly a 24-step sequence window ($N = 320$), not individual telemetry sampling rows ($N = 7,680$).
   - In Table 2, the unit of analysis is a canonical incident scenario ($N = 6$), not 42 independent outage events.
   - In Table 4, the unit of analysis is a distinct security test evaluation ($N = 16$).
2. **False Alarms per Hour**:
   - Explicitly marked as **UNAVAILABLE** because non-overlapping batch evaluation does not support continuous streaming rate extrapolation without alert deduplication; the old nominal calculation ($\text{FPR} \times 720$) is superseded.
3. **Combined Detector Redundancy**:
   - Acknowledged in Table 1 that the Combined Detector's discrete metrics match the LSTM Autoencoder identically on this benchmark ($120$ TP, $2$ FP). Its inclusion is defended on architectural defense-in-depth principles rather than additive sensitivity.
4. **Safety Denominators**:
   - Table 4 corrects prior narrative conflations by distinguishing 11 adversarial attacks from 5 precondition/control cases.
