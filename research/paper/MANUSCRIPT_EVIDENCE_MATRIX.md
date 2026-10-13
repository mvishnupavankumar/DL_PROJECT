# AegisOps: Manuscript Evidence Matrix & Scientific Verification Trace

**Document Path**: `research/paper/MANUSCRIPT_EVIDENCE_MATRIX.md`  
**Git Baseline**: `ec83d2fe501ba50f56839944ba7bd6347544f585` (Branch: `main`)  
**Audit Standard**: Strict Empirical Grounding, Reproducibility Gate, and Evidence Integrity Protocol  
**Date**: October 2026  

---

## 1. Overview and Audit Mandate

This evidence matrix establishes the traceability between every quantitative claim, planned figure, table, and architectural conclusion in [`research/paper/AEGISOPS_RESEARCH_PAPER.md`](file:///c:/DL_PROJECT/research/paper/AEGISOPS_RESEARCH_PAPER.md) and its primary machine-readable source artifact. 

### Mandatory Reporting Principles:
1. **Zero Evidence Hallucination**: No metric, sample size, or baseline is asserted without a direct machine-readable artifact or executable test verification.
2. **Explicit Evidence Typology**: Every claim is classified by modality: Synthetic Benchmark, Historical Cold-Start, Live-LLM API, Offline Deterministic Mock, or Local Security Boundary Test.
3. **Disclosure of Limitations and Bounded Scope**: Claims of superiority, generalization, or zero-cost automation are strictly qualified; negative findings, sample constraints, and statistical power limits are fully disclosed.

---

## 2. Evidence Taxonomy and Experimental Units

| Modality Code | Evidence Class | Unit of Analysis | Total Sample Size ($N$) | Primary Source Location | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SYN-DET** | Synthetic Anomaly Detection Benchmark | 24-step normalized window ($\mathbf{X} \in \mathbb{R}^{24 \times 5}$) | $N = 320$ windows (200 normal, 120 fault) | [`research/raw/detection_predictions.csv`](file:///c:/DL_PROJECT/research/raw/detection_predictions.csv), [`research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv`](file:///c:/DL_PROJECT/research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv) | Verified & Recomputed |
| **HIST-COLD** | Historical Cold-Start Telemetry | 5-second physical observation row | $N = 200$ rows (31 normal, 169 alert across 4 episodes) | [`data/aegisops_live.sqlite3`](file:///c:/DL_PROJECT/data/aegisops_live.sqlite3), [`research/exports/incident_episodes.csv`](file:///c:/DL_PROJECT/research/exports/incident_episodes.csv) | Verified |
| **LIVE-LLM** | Live Groq Cloud API Diagnostic Inference | Multi-turn Agent Workflow on Incident Scenario | $N = 6$ canonical incident scenarios (3 live configs: 18 trials) | [`research/raw/diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_predictions.csv), [`research/exports/experiment_b_results.csv`](file:///c:/DL_PROJECT/research/exports/experiment_b_results.csv) | Verified (Omissions accounted) |
| **OFFLINE-MOCK** | Deterministic Offline Diagnostic Heuristics | Rule / Heuristic Analysis on Incident Episode | $N = 6$ canonical scenarios (4 offline configs: 24 trials) | [`research/raw/diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_predictions.csv) | Verified |
| **SAFETY-BOUND** | Local Execution Barrier Security Trials | Discrete HTTP / Payload Invocation Probe | $N = 16$ test cases (11 attacks, 2 preconditions, 1 probe, 2 controls) | [`research/raw/safety_test_results.csv`](file:///c:/DL_PROJECT/research/raw/safety_test_results.csv), [`tests/test_approval_barrier.py`](file:///c:/DL_PROJECT/tests/test_approval_barrier.py) | Verified (100% pass) |

---

## 3. Quantitative Claims and Figures Evidence Matrix

### 3.1 Figures and Architecture Diagrams

| Figure Identifier | Exact Claim / Caption Content | Primary Source Artifact | Sample Size ($N$) | Modality | Limitations & Required Wording | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Figure 1** | System Architecture & Closed-Loop Telemetry Dataflow | Hand-authored Mermaid from `collectors/system_metrics.py`, `models/lstm_autoencoder.py`, `agents.py`, `approval.py`, `live_monitoring.py` | Full codebase architecture | Code Architecture | Must clearly delineate loopback HTTP boundary (`127.0.0.1:8765`), SQLite state storage, and human approval requirement. | **VERIFIED** |
| **Figure 2** | Two-Stage Detection and Four-Agent Diagnostic Pipeline | Hand-authored Mermaid from `models/lstm_autoencoder.py`, `dl/anomaly_detector.py`, `agents.py` | Full detection-diagnosis pipeline | Code Architecture | Must illustrate dual-gate trigger ($\tau=0.709399$), feature reconstruction MSE attribution handoff, and supervisor synthesis. | **VERIFIED** |
| **Figure 3** | Two-Man Rule Approval and Remediation Verification Flow | Hand-authored Mermaid from `approval.py`, `live_monitoring.py` | Remediation execution workflow | Code Architecture | Must illustrate atomic `BEGIN IMMEDIATE` transaction locking, UUIDv4 nonce, 300s TTL, and `/probe` verification. | **VERIFIED** |
| **Figure A.1** | Anomaly Detection Confusion Matrices (4-panel) | [`research/figures/detection_confusion_matrices.png`](file:///c:/DL_PROJECT/research/figures/detection_confusion_matrices.png), [`research/experiments/plot_detection_figures.py`](file:///c:/DL_PROJECT/research/experiments/plot_detection_figures.py) | $N = 320$ windows | **SYN-DET** | Panel (a) plots Full Operational Rules (TP=120, FP=0, TN=200, FN=0). Caption must explicitly state performance on synthetic windows. | **VERIFIED** |
| **Figure A.2** | Anomaly Detection Comparative Performance (Recall, Precision, F1, Latency) | [`research/figures/detection_comparison.png`](file:///c:/DL_PROJECT/research/figures/detection_comparison.png), [`research/experiments/plot_detection_figures.py`](file:///c:/DL_PROJECT/research/experiments/plot_detection_figures.py) | $N = 320$ windows | **SYN-DET** | Bar chart showing Rules (100.0% full operational recall), IF (47.5%), LSTM (100.0%), Combined (100.0%). Narrow and Resource-Only rules detailed in text. | **VERIFIED** |

---

### 3.2 Tables and Benchmark Data

| Table Identifier | Target Table Title | Source Machine-Readable File | Sample Size ($N$) | Evidence Modality | Specific Metric Values & Constraints | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Table 1** | Comprehensive Anomaly Detection Benchmark Results | [`research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv`](file:///c:/DL_PROJECT/research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv) | $N = 320$ sequence windows ($200$ normal, $120$ fault) | **SYN-DET** | Must present **all three rule baselines**: Narrow (Recall 33.33%, 40/120), Resource-Only (Recall 66.67%, 80/120), Full Operational (Recall 100.0%, 120/120). FPR: Rules 0.0%, IF 2.0% (4/200), LSTM 1.0% (2/200). FA/hr marked **UNAVAILABLE**. | **VERIFIED** |
| **Table 2** | Root-Cause Diagnostic Performance Across Seven Configurations | [`research/raw/diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_predictions.csv), [`research/exports/experiment_b_results.csv`](file:///c:/DL_PROJECT/research/exports/experiment_b_results.csv) | $N = 6$ canonical incident scenarios ($7 \times 6 = 42$ evaluations) | **LIVE-LLM** & **OFFLINE-MOCK** | Intent-to-Treat strict accuracies: Rule Baseline 100.0% ($6/6$), Multi-Agent Full Live LLM 83.33% ($5/6$), Multi-Agent No-DL 66.7% ($4/6$). Disclose rubric leakage and $N=6$ low power ($1-\beta \approx 0.14$). No LLM superiority claimed. | **VERIFIED** |
| **Table 3** | Scenario-by-Scenario Diagnostic Breakdown and Signal Attribution | [`research/raw/diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_predictions.csv), [`research/exports/incident_scenarios.csv`](file:///c:/DL_PROJECT/research/exports/incident_scenarios.csv) | $N = 6$ failure scenarios (`INC-1001` through `INC-1006`) | **LIVE-LLM** & **OFFLINE-MOCK** | Discloses that `INC-1006` (Deadlock) scored Lenient Match due to rubric phrasing. Maps per-feature reconstruction attribution to root causes. | **VERIFIED** |
| **Table 4** | Safety, Governance, and Execution Boundary Test Suite | [`research/raw/safety_test_results.csv`](file:///c:/DL_PROJECT/research/raw/safety_test_results.csv), [`research/raw/safety_metrics.csv`](file:///c:/DL_PROJECT/research/raw/safety_metrics.csv) | $N = 16$ discrete tests | **SAFETY-BOUND** | Disaggregates: 11 adversarial attacks ($11/11$ blocked, 100.0%, 95% Wilson CI $[0.7412, 1.0000]$), 2 precondition checks, 1 verification probe, 2 controls. Local loopback boundary only. | **VERIFIED** |
| **Table 5** | Statistical Hypothesis Testing and Paired Performance Intervals | [`research/audits/detection_rate_and_phase4_gate_20261012/STATISTICAL_ASSUMPTION_REVIEW.md`](file:///c:/DL_PROJECT/research/audits/detection_rate_and_phase4_gate_20261012/STATISTICAL_ASSUMPTION_REVIEW.md) | $N = 120$ paired fault windows; $N=6$ failure classes | **SYN-DET** | Window-level McNemar test: $p = 2.168 \times 10^{-19}$, paired diff $\Delta = +0.5250$, 95% CI $[+0.4357, +0.6143]$ (descriptive, clustered windows). Cluster-adjusted scenario-level Wilcoxon signed-rank test: $W = 0.0, p = 0.03125$, $\Delta_{\text{median}} = +0.600$ (minimum attainable $p = 2/64$). | **VERIFIED** |

---

## 4. Key Quantitative Statements and Scientific Assertions

| Assertion Key | Manuscript Statement | Supporting Data / Artifact | Evidence Type | Mandated Qualification & Phrasing |
| :--- | :--- | :--- | :--- | :--- |
| **ST-01** | LSTM Autoencoder detects 100% of synthetic incident windows (120/120) with 2 false positives (1.0% FPR). | `CORRECTED_DETECTION_METRICS.csv` (Row: LSTM Autoencoder) | **SYN-DET** | Must explicitly state: "evaluated on a synthetic benchmark of 320 windows (200 normal steady-state, 120 fault episodes across 6 classes)". Cannot claim zero misses on wild production telemetry. |
| **ST-02** | Isolation Forest detects 57/120 fault windows (47.50% recall) with 4 false positives (2.0% FPR). | `CORRECTED_DETECTION_METRICS.csv` (Row: Isolation Forest) | **SYN-DET** | Must state: "Isolation Forest missed gradual memory leaks and complex concurrency degradations lacking single-point outliers." |
| **ST-03** | Rule baseline performance spans three distinct operational definitions: Narrow (33.33%), Resource-Only (66.67%), Full Operational (100.0%). | `run_experiment_a.py` and `CORRECTED_DETECTION_METRICS.csv` | **SYN-DET** | Must clearly distinguish the three definitions. The 100% recall of Full Operational Rules depends entirely on the synthetic HTTP error rate spike injected in all 6 failure modes. |
| **ST-04** | Combined Detector achieves identical classification counts to standalone LSTM (120 TP, 2 FP, 198 TN, 0 FN). | `CORRECTED_DETECTION_METRICS.csv` (Row: Combined Alert) | **SYN-DET** | Must state: "The combined detector provided zero additive statistical sensitivity on this benchmark; its justification is architectural defense-in-depth." |
| **ST-05** | False-alarm frequency is reported as False-Positive Window Rate ($1.0\%$), not measured operational false alarms per hour. | `WINDOW_EXPOSURE_AND_ALARM_RATE_AUDIT.md` | **SYN-DET** | Must state: "Operational alarms per hour is marked UNAVAILABLE because multiplying FPR by 720 assumes continuous streaming observations without alert deduplication." |
| **ST-06** | Paired difference in sensitivity between LSTM and Isolation Forest is statistically significant ($p < 10^{-18}$ window-level; $p = 0.03125$ scenario-level). | `STATISTICAL_ASSUMPTION_REVIEW.md` | **SYN-DET** | Window-level McNemar test ($p = 2.168 \times 10^{-19}$) assumes independent windows (descriptive; 120 windows are clustered across 6 scenarios). Exact scenario-level Wilcoxon signed-rank test yields $W=0.0, p=0.03125$ (minimum attainable $p=2/64$). Small $p$-values reflect synthetic separation, not cross-system generalization. |
| **ST-07** | Live Multi-Agent LLM achieved 83.33% Intent-to-Treat strict diagnostic accuracy (5/6 scenarios). | `diagnosis_predictions.csv` | **LIVE-LLM** | Must state: "The deterministic rule-based baseline achieved 100.0% strict accuracy in 0.01 ms. The multi-agent LLM did not outperform the rule baseline, and $N=6$ represents an exploratory pilot feasibility trial with low power ($1-\beta \approx 0.14$) and rubric test-set leakage." |
| **ST-09** | Calibration threshold for Isolation Forest ($\tau = -0.018694$). | `CORRECTED_DETECTION_METRICS.csv` and `REPRODUCIBILITY_CLOSURE.md` | **SYN-DET** | Resolved in Phase 8: active deterministic pipeline threshold is $\tau = -0.018694$ ($q=0.99$ on negated decision function with contamination=0.01). Prior cited $+0.089886$ was an un-negated quantile and $-0.090333$ was text transcription drift. |

---

## 5. Unresolved or Bounded Claims Register

| Area / Scope | Unresolved or Bounded Claim | Reason for Limitation | Mandated Paper Treatment |
| :--- | :--- | :--- | :--- |
| **Operational False Alarms / Hour** | Measuring production false-alarm rate in alarms/hour. | Benchmark comprises 200 non-overlapping 24-step windows; no streaming deduplication window was implemented. | Explicitly report as **UNAVAILABLE**. Prohibit multiplying window FPR by 720 without qualifying it as a synthetic non-operational ceiling. |
| **Production Telemetry Generalization** | Generalization to wild enterprise microservices. | Dataset is synthetically simulated with mathematical noise and deterministic failure ramps. | Limit claims to "synthetic benchmark evaluation"; call for validation against external real-world traces (e.g., TrainTicket, SocialNetwork). |
| **LLM Diagnostic Superiority** | Claiming Multi-Agent LLMs outperform classical expert heuristics. | Rule baseline achieved 6/6 (100.0%) in 0.01 ms vs LLM 5/6 (83.33%) in 4.78s. | Emphatically state that LLM did **not** demonstrate superiority over deterministic rules on this 6-scenario suite; discuss LLMs as flexible fallback synthesizers. |
| **Sample Size in RCA** | Statistical generalization of root-cause diagnosis. | Evaluated on $N=6$ canonical failure modes. | Explicitly disclose low statistical power ($1-\beta \approx 0.14$) and rubric keyword overlap with scenario definitions. |
| **Enterprise Security Scope** | Multi-cluster or multi-tenant security guarantees. | Experiments evaluated on loopback interface (`127.0.0.1:8765`) and local SQLite database. | Explicitly bound claims to the local application runtime boundary; do not claim defense against OS kernel exploitation or compromised cloud control planes. |

---

## 6. Verification Sign-Off

Every numerical claim in the above matrix has been cross-checked against machine-readable files in `research/raw/`, `research/results/`, and `research/audits/detection_rate_and_phase4_gate_20261012/`. 

Authoring of [`research/paper/AEGISOPS_RESEARCH_PAPER.md`](file:///c:/DL_PROJECT/research/paper/AEGISOPS_RESEARCH_PAPER.md) must strictly align with the exact metrics, sample sizes, and required qualifications detailed in this matrix.
