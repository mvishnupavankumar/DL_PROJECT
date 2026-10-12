# AegisOps: Figure and Table Cross-Verification Index

**Document Path**: `research/paper/FIGURE_AND_TABLE_INDEX.md`  
**Associated Manuscript**: [`research/paper/AEGISOPS_RESEARCH_PAPER.md`](file:///c:/DL_PROJECT/research/paper/AEGISOPS_RESEARCH_PAPER.md)  
**Git Baseline**: `ec83d2fe501ba50f56839944ba7bd6347544f585` (Branch: `main`)  
**Audit Standard**: Exhaustive Machine-Readable Reconciliation & Cross-Validation Gate  
**Date**: October 2026  

---

## 1. Overview and Cross-Verification Standard

This index validates every figure, table, caption, and quantitative entry in the research manuscript against the underlying machine-readable outputs in `research/raw/`, `research/results/`, and `research/audits/detection_rate_and_phase4_gate_20261012/`.

### Strict Reconciliation Criteria:
1. **Zero Discrepancy**: Plotted numbers, contingency tables, sample counts, and percentages must match the machine-readable metrics exactly.
2. **Standardized Terminology**: Rule baselines must be explicitly partitioned into *Narrow Rules*, *Resource-Only Rules*, and *Full Operational Rules*.
3. **Corrected Denominators**: False alarms are strictly reported as False-Positive Window Rate ($\text{FPR}_{\text{window}}$); continuous operational false alarms per hour is marked `UNAVAILABLE`.
4. **Sample Attribution**: Sample sizes ($N=320$ for detection windows; $N=6$ for incident scenarios; $N=16$ for safety test cases) must be explicitly stated in all captions and table notes.

---

## 2. Figures Cross-Verification Index

| Figure ID | Caption Title | Underlying Machine-Readable Artifact | Generator Script | Plotted Metric Values | Reconciliation Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Figure 1** | System Architecture and Closed-Loop Telemetry Dataflow | Hand-authored from runtime code: `collectors/system_metrics.py`, `models/lstm_autoencoder.py`, `agents.py`, `approval.py`, `live_monitoring.py` | Architecture Mermaid Specification | 5 functional layers, 15 components, SQLite atomic locks, loopback HTTP (`127.0.0.1:8765`), `/probe` verification. | **VERIFIED**: Accurately depicts actual production component boundaries and dataflow. |
| **Figure 2** | Two-Stage Anomaly Detection to Multi-Agent Diagnosis Workflow | Hand-authored from `models/lstm_autoencoder.py`, `dl/anomaly_detector.py`, `agents.py` | Architecture Mermaid Specification | Buffer $W=24$, threshold $\tau=0.709399$, per-feature MSE vector handoff to `InvestigatorAgent`, multi-agent synthesis. | **VERIFIED**: Reflects exact feature attribution handoff and 4-agent collaboration pipeline. |
| **Figure 3** | Two-Man Rule Approval and Remediation Verification Flow | Hand-authored from `approval.py`, `live_monitoring.py` | Architecture Mermaid Specification | Nonce (UUIDv4), TTL (300s), `BEGIN IMMEDIATE` lock, `/probe` health check, and audit trail in `remediation_audit`. | **VERIFIED**: Matches implementation in `approval.py` and `tests/test_approval_barrier.py`. |
| **Figure A.1** | Anomaly Detection Confusion Matrices (4-Panel Benchmark) | [`research/figures/detection_confusion_matrices.png`](file:///c:/DL_PROJECT/research/figures/detection_confusion_matrices.png), [`research/paper/figures/detection_confusion_matrices.png`](file:///c:/DL_PROJECT/research/paper/figures/detection_confusion_matrices.png) | [`research/experiments/plot_detection_figures.py`](file:///c:/DL_PROJECT/research/experiments/plot_detection_figures.py) | **(a) Full Operational Rules**: TP=120, FP=0, TN=200, FN=0<br>**(b) Isolation Forest**: TP=57, FP=4, TN=196, FN=63<br>**(c) LSTM Autoencoder**: TP=120, FP=2, TN=198, FN=0<br>**(d) Combined Detector**: TP=120, FP=2, TN=198, FN=0 | **VERIFIED**: Plotted matrices match `CORRECTED_DETECTION_METRICS.csv` exactly. Caption in `FIGURE_CAPTIONS.md` explicitly notes synthetic benchmark evaluation and distinguishes rule variants. |
| **Figure A.2** | Comparative Anomaly Detection Performance Metrics | [`research/figures/detection_comparison.png`](file:///c:/DL_PROJECT/research/figures/detection_comparison.png), [`research/paper/figures/detection_comparison.png`](file:///c:/DL_PROJECT/research/paper/figures/detection_comparison.png) | [`research/experiments/plot_detection_figures.py`](file:///c:/DL_PROJECT/research/experiments/plot_detection_figures.py) | **Recall**: Rules 100.0%, IF 47.50%, LSTM 100.0%, Combined 100.0%<br>**Precision**: Rules 100.0%, IF 93.44%, LSTM 98.36%, Combined 98.36%<br>**F1-Score**: Rules 1.0000, IF 0.6298, LSTM 0.9917, Combined 0.9917<br>**Latency**: Rules 0.01 ms, IF 1.84 ms, LSTM 0.17 ms, Combined 0.18 ms | **VERIFIED**: Plotted bars correspond exactly to Full Operational Rules, Isolation Forest, LSTM Autoencoder, and Combined Detector in `CORRECTED_DETECTION_METRICS.csv`. Narrow and Resource-Only rules documented in accompanying text. |

---

## 3. Tables Cross-Verification Index

### Table 1: Comprehensive Anomaly Detection Benchmark Results
- **Source Artifact**: [`research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv`](file:///c:/DL_PROJECT/research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv)
- **Experimental Unit**: 24-step normalized sequence window ($\mathbf{X} \in \mathbb{R}^{24 \times 5}$)
- **Sample Count**: $N = 320$ windows ($200$ normal steady-state, $120$ incident episodes across 6 classes)
- **Verified Values Cross-Check Table**:

| Model Variant | TP | FP | TN | FN | Recall | Precision | Specificity | F1-Score | FPR (Window) | FA/hr | PR-AUC | Mean Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Narrow Rules** (lat $\ge$ 1000, mem $\ge$ 95) | 40 | 0 | 200 | 80 | 33.33% | 100.00% | 100.00% | 0.5000 | 0.00% | UNAVAILABLE | 0.3333 | 0.01 ms |
| **Resource-Only Rules** (+ cpu $\ge$ 90, disk $\ge$ 95) | 80 | 0 | 200 | 40 | 66.67% | 100.00% | 100.00% | 0.8000 | 0.00% | UNAVAILABLE | 0.6667 | 0.01 ms |
| **Full Operational Rules** (+ error $\ge$ 0.5%) | 120 | 0 | 200 | 0 | 100.00% | 100.00% | 100.00% | 1.0000 | 0.00% | UNAVAILABLE | 1.0000 | 0.01 ms |
| **Isolation Forest** (Calibrated $\tau = -0.090333$) | 57 | 4 | 196 | 63 | 47.50% | 93.44% | 98.00% | 0.6298 | 2.00% | UNAVAILABLE | 0.9056 | 1.84 ms |
| **LSTM Autoencoder** (Calibrated $\tau = 0.709399$) | 120 | 2 | 198 | 0 | 100.00% | 98.36% | 99.00% | 0.9917 | 1.00% | UNAVAILABLE | 0.9998 | 0.17 ms |
| **Combined Alert** (Full Rules $\lor$ LSTM AE) | 120 | 2 | 198 | 0 | 100.00% | 98.36% | 99.00% | 0.9917 | 1.00% | UNAVAILABLE | N/A | 0.18 ms |

*Status*: **VERIFIED & CONCORDANT**. All values match `CORRECTED_DETECTION_METRICS.csv` to 4 decimal places.

---

### Table 2: Diagnostic Evaluation Across Seven Configurations
- **Source Artifact**: [`research/raw/diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_predictions.csv), [`research/exports/experiment_b_results.csv`](file:///c:/DL_PROJECT/research/exports/experiment_b_results.csv)
- **Experimental Unit**: Canonical incident scenario ($N = 6$ failure scenarios)
- **Total Evaluations**: $7 \text{ configurations} \times 6 \text{ scenarios} = 42 \text{ evaluations}$
- **Verified Values Cross-Check Table**:

| Config ID | Architecture Description | Inference Engine | Strict Acc (ITT $N=6$) | Strict Acc (Comp $N=5$) | Lenient Acc ($N=6$) | Mean Latency | Token / API Cost |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Config 1** | Zero-Shot ReAct (Single Agent) | Offline Heuristic Mock | 33.33% ($2/6$) | 33.33% ($2/6$) | 50.00% ($3/6$) | 0.01 ms | $0.00 |
| **Config 2** | Two-Agent Pipeline (No DL) | Offline Heuristic Mock | 50.00% ($3/6$) | 50.00% ($3/6$) | 66.67% ($4/6$) | 0.01 ms | $0.00 |
| **Config 3** | Four-Agent Pipeline (No DL) | Offline Heuristic Mock | 66.67% ($4/6$) | 66.67% ($4/6$) | 83.33% ($5/6$) | 0.01 ms | $0.00 |
| **Config 4** | Four-Agent Pipeline (+ DL Handoff) | Offline Heuristic Mock | 83.33% ($5/6$) | 83.33% ($5/6$) | 100.00% ($6/6$) | 0.01 ms | $0.00 |
| **Config 5** | Multi-Agent Live LLM (No DL) | Groq Cloud (Llama-3-70b) | 66.67% ($4/6$) | 80.00% ($4/5$) | 83.33% ($5/6$) | 3.82 s | ~$0.012 / incident |
| **Config 6** | Multi-Agent Live LLM (+ DL Full) | Groq Cloud (Llama-3-70b) | 83.33% ($5/6$) | 83.33% ($5/6$) | 100.00% ($6/6$) | 4.78 s | ~$0.018 / incident |
| **Config 7** | Deterministic Rule-Based Baseline | Python Regex / Thresholds | **100.00%** ($6/6$) | **100.00%** ($6/6$) | **100.00%** ($6/6$) | **0.01 ms** | **$0.00** |

*Status*: **VERIFIED & CONCORDANT**. Omissions accounted for: Config 5 omitted INC-1002 (timeout); Config 7 evaluated all 6. Discloses that multi-agent LLM did not outperform rule baseline.

---

### Table 3: Scenario-by-Scenario Diagnostic Breakdown
- **Source Artifact**: [`research/raw/diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_predictions.csv), [`research/exports/incident_scenarios.csv`](file:///c:/DL_PROJECT/research/exports/incident_scenarios.csv)
- **Experimental Unit**: Ground-truth incident ticket (`INC-1001` through `INC-1006`)
- **Verified Values Cross-Check Table**:

| Incident ID | Ground-Truth Fault Class | Synthetic Signature | Primary Attributed Feature | Live LLM Predicted Cause | Strict Match | Lenient Match |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **INC-1001** | Pod OOMKilled | Memory ramp to 99% + crash | `memory_usage_pct` (MSE: 5.42) | Out-of-Memory / Heap Exhaustion | 1 (True) | 1 (True) |
| **INC-1002** | Redis Cache Latency Spike | P99 latency ramp to 1800ms | `p99_latency_ms` (MSE: 8.11) | Downstream Cache Timeout / Latency | 1 (True) | 1 (True) |
| **INC-1003** | Postgres Connection Exhaustion | 500 error spike + connection cap | `error_rate_pct` (MSE: 4.88) | Database Connection Pool Exhaustion | 1 (True) | 1 (True) |
| **INC-1004** | Kafka Disk Saturation | Disk usage to 98% + write fail | `disk_usage_pct` (MSE: 6.30) | Persistent Storage / Disk Saturation | 1 (True) | 1 (True) |
| **INC-1005** | CPU Throttling Under Load | CPU capped at 95% + latency | `cpu_usage_pct` (MSE: 7.02) | CPU Cgroup Throttling | 1 (True) | 1 (True) |
| **INC-1006** | Threadpool Deadlock | CPU drop to 2% + latency spike | `p99_latency_ms` (MSE: 3.75) | Concurrency Block / Deadlock Contention | 0 (False)* | 1 (True) |

*\*Note*: `INC-1006` received strict score 0 due to exact keyword criteria in the rubric requiring "deadlock" as primary token; lenient criteria accepted "threadpool contention" as an architectural synonym.

*Status*: **VERIFIED & CONCORDANT**.

---

### Table 4: Safety, Governance, and Execution Boundary Test Suite
- **Source Artifact**: [`research/raw/safety_test_results.csv`](file:///c:/DL_PROJECT/research/raw/safety_test_results.csv), [`research/raw/safety_metrics.csv`](file:///c:/DL_PROJECT/research/raw/safety_metrics.csv)
- **Experimental Unit**: Discrete invocation request ($N = 16$ test cases)
- **Verified Values Cross-Check Table**:

| Test Cohort | Case Count | Target Mechanism Tested | Expected Safety Response | Observed Execution Result | Success Rate | 95% Wilson CI |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: |
| **Adversarial Invocations** | 11 | Direct `/apply` bypass, shell injection (`rm -rf`), invalid nonce, expired TTL (>300s), modified action payload, unapproved ticket | HTTP 403 Forbidden / HTTP 400 Bad Request; zero state mutation | Blocked at execution boundary; zero arbitrary execution | **100.0%** ($11/11$) | $[0.7412, 1.0000]$ |
| **Precondition Validations** | 2 | Dependency down, service unresponsive | Abort execution before remediation command dispatch | Clean abort with state logged as PRECONDITION_FAILED | **100.0%** ($2/2$) | $[0.3424, 1.0000]$ |
| **Verification Probes** | 1 | Mocked recovery verification probe failure | Rollback / escalate ticket to HUMAN_REQUIRED | Fake recovery rejected; ticket escalated | **100.0%** ($1/1$) | $[0.2065, 1.0000]$ |
| **Positive Controls** | 2 | Legitimate valid approved remediation commands | Execute authorized template; write audit record | Executed successfully; full SQLite audit trail | **100.0%** ($2/2$) | $[0.3424, 1.0000]$ |

*Status*: **VERIFIED & CONCORDANT**. Disaggregates adversarial attacks from control probes. Bounded strictly to local application execution boundary.

---

### Table 5: Statistical Hypothesis Testing and Uncertainty Intervals
- **Source Artifact**: [`research/audits/detection_rate_and_phase4_gate_20261012/STATISTICAL_ASSUMPTION_REVIEW.md`](file:///c:/DL_PROJECT/research/audits/detection_rate_and_phase4_gate_20261012/STATISTICAL_ASSUMPTION_REVIEW.md)
- **Experimental Units**: Paired window outcomes ($N = 120$ fault windows) & Cluster failure modes ($N = 6$ failure scenarios)
- **Verified Values Cross-Check Table**:

| Statistical Test | Comparison Target | Sample Unit ($N$) | Test Statistic | Exact $p$-Value | Effect Size / Interval | Methodological Validity Notes |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **Exact McNemar Test** | LSTM Autoencoder vs Isolation Forest | $N = 120$ paired fault windows | $b = 63, c = 0$ | $p = 2.168 \times 10^{-19}$ | $\Delta = +0.5250$ | Assumes cross-window independence. Valid at window unit of analysis. |
| **Wald Paired Difference CI** | LSTM Autoencoder vs Isolation Forest | $N = 120$ paired fault windows | $\text{SE} \approx 0.0456$ | N/A | $95\%\ \text{CI}: [+0.4357, +0.6143]$ | Quantifies sensitivity difference on 120 synthetic fault episodes. |
| **Wilcoxon Signed-Rank Test** | LSTM Autoencoder vs Isolation Forest | $N = 6$ failure classes (clustered) | $W = 0.0$ | $p = 0.03125$ | $\Delta_{\text{median}} = +0.525$ | Cluster-adjusted test treating scenarios as primary sampling unit. Statistically significant at $\alpha = 0.05$. |
| **Wilson Score Interval** | Adversarial Boundary Containment | $N = 11$ adversarial attacks | $k = 11$ | N/A | $95\%\ \text{CI}: [0.7412, 1.0000]$ | Asymmetric binomial interval reflecting small-sample containment. |

*Status*: **VERIFIED & CONCORDANT**. Both window-level and cluster-adjusted tests reported with full transparency.

---

## 4. Final Consistency Verification Sign-Off

All 5 tables and 5 figures have been cross-checked against source code, raw predictions, and corrected metric files. Definitions, sample counts, contingency cells, and rounding are 100% concordant across the research deliverables.
