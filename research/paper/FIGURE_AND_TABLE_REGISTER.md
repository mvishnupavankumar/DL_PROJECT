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
| **Figure A.1** (Supplementary) | `research/paper/figures/detection_confusion_matrices.png` | PNG (27.9 KB) | `research/experiments/run_experiment_a.py` -> `research/figures/detection_confusion_matrices.png` | $N = 320$ sequence windows (200 normal, 120 fault across 6 classes) | **VERIFIED**: Displays 4 contingency matrices: Operational Rules (40 TP, 80 FN, 200 TN, 0 FP); Isolation Forest (57 TP, 63 FN, 196 TN, 4 FP); LSTM AE (120 TP, 0 FN, 198 TN, 2 FP); Combined (120 TP, 0 FN, 198 TN, 2 FP). |
| **Figure A.2** (Supplementary) | `research/paper/figures/detection_comparison.png` | PNG (16.8 KB) | `research/experiments/run_experiment_a.py` -> `research/figures/detection_comparison.png` | $N = 320$ sequence windows (200 normal, 120 fault across 6 classes) | **VERIFIED**: Bar charts showing Recall (Rules: 33.3%, IF: 47.5%, LSTM: 100.0%, Combined: 100.0%), Precision, F1-Score, and Mean Latency (Rules: 0.01 ms, IF: 1.84 ms, LSTM: 0.17 ms, Combined: 0.18 ms). |

---

## 3. Results Tables Register

| Table ID | Table Title | Primary Source Artifact | Generator Script | Experimental Unit & Sample Size | Reported Values & Reconciliation Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Table 1** | Comprehensive Anomaly Detection Benchmark Results | `research/exports/experiment_a_results.csv`, `research/exports/experiment_a_predictions.csv` | `research/experiments/run_experiment_a.py` | 24-step normalized sequence window ($N = 320$: $200$ normal, $120$ fault) | **VERIFIED**: TP, FP, TN, FN, Recall, Precision, Specificity, F1, FPR, FA/hr, PR-AUC, Latency. Captures both physical resource rules (Recall: 33.3%) and full operational rules with error rate gate (Recall: 100.0%). |
| **Table 2** | Diagnostic Evaluation Across Configurations | `research/exports/experiment_b_results.csv` | `research/experiments/run_experiment_b.py` | Canonical Incident Scenario ($N = 6$ scenarios across 7 configurations = 42 evaluations) | **VERIFIED**: Reports Intent-to-Treat ($N=6$) strict and lenient accuracies: Live LLM Multi-Agent + DL = 83.3% strict ($5/6$), 100.0% lenient ($6/6$); Live LLM Multi-Agent No-DL = 66.7% strict ($4/6$); Offline heuristics reported faithfully. |
| **Table 3** | Scenario-by-Scenario Diagnostic Breakdown | `research/exports/experiment_b_results.csv` | `research/experiments/run_experiment_b.py` | Individual Incidents `INC-1001` through `INC-1006` | **VERIFIED**: Maps ground truth fault modes to predicted root causes and reconstruction attribution signals. Identifies deadlock (`INC-1006`) as lenient match. |
| **Table 4** | Safety, Governance, and Execution Boundary Test Suite | `research/exports/experiment_c_results.csv`, `tests/test_approval_barrier.py` | `research/experiments/run_experiment_c.py` | Discrete Safety Test Case ($N = 16$ evaluations) | **VERIFIED**: Disaggregates 11 adversarial attacks ($11/11$ blocked, 100.0%, Wilson CI $[0.741, 1.000]$), 2 precondition failures, 1 false-recovery probe check, and 2 positive controls. |

---

## 4. Verification Check of Discrepancies and Clarifications

1. **Unit of Analysis**:
   - In Table 1, the unit of analysis is explicitly a 24-step sequence window ($N = 320$), not individual telemetry sampling rows ($N = 7,680$).
   - In Table 2, the unit of analysis is a canonical incident scenario ($N = 6$), not 42 independent outage events.
   - In Table 4, the unit of analysis is a distinct security test evaluation ($N = 16$).
2. **False Alarms per Hour**:
   - Explicitly documented as a nominal rate calculated as $\text{FPR} \times 720$ discrete evaluation intervals per hour under steady-state conditions, not a longitudinal live-monitoring empirical tally.
3. **Combined Detector Redundancy**:
   - Acknowledged in Table 1 that the Combined Detector's discrete metrics match the LSTM Autoencoder identically on this benchmark ($120$ TP, $2$ FP). Its inclusion is defended on architectural defense-in-depth principles rather than additive sensitivity.
4. **Safety Denominators**:
   - Table 4 corrects prior narrative conflations by distinguishing 11 adversarial attacks from 5 precondition/control cases.
