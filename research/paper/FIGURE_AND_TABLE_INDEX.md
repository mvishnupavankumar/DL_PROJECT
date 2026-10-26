# AegisOps: Figure and Table Cross-Verification Index

**Document Path**: `research/paper/FIGURE_AND_TABLE_INDEX.md`<br>
**Associated Manuscript**: [AEGISOPS_RESEARCH_PAPER.md](AEGISOPS_RESEARCH_PAPER.md)<br>
**Git Baseline**: `ec83d2fe501ba50f56839944ba7bd6347544f585` (Branch: `main`)<br>
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
| **Figure 3** | Scope-Bound Approval and Remediation Verification Flow | Hand-authored from `approval.py`, `live_monitoring.py` | Architecture Mermaid Specification | Nonce (UUIDv4), TTL (300s), `BEGIN IMMEDIATE` lock, `/probe` health check, and audit trail in `remediation_audit`. | **VERIFIED**: Matches implementation in `approval.py` and `tests/test_approval_barrier.py`. |
| **Figure A.1** | Anomaly Detection Confusion Matrices (4-Panel Benchmark) | [`research/figures/detection_confusion_matrices.png`](../figures/detection_confusion_matrices.png), [`research/paper/figures/detection_confusion_matrices.png`](figures/detection_confusion_matrices.png) | [`research/experiments/plot_detection_figures.py`](../experiments/plot_detection_figures.py) | **(a) Full Operational Rules**: TP=120, FP=0, TN=200, FN=0<br>**(b) Isolation Forest**: TP=57, FP=4, TN=196, FN=63<br>**(c) LSTM Autoencoder**: TP=120, FP=2, TN=198, FN=0<br>**(d) Combined Detector**: TP=120, FP=2, TN=198, FN=0 | **VERIFIED**: Plotted matrices match `CORRECTED_DETECTION_METRICS.csv` exactly. Caption in `FIGURE_CAPTIONS.md` explicitly notes synthetic benchmark evaluation and distinguishes rule variants. |
| **Figure A.2** (supplementary; excluded from release distribution) | Comparative Anomaly Detection Performance Metrics | [`research/figures/detection_comparison.png`](../figures/detection_comparison.png), [`research/paper/figures/detection_comparison.png`](figures/detection_comparison.png) | [`research/experiments/plot_detection_figures.py`](../experiments/plot_detection_figures.py) | **Recall**: Rules 100.0%, IF 47.50%, LSTM 100.0%, Combined 100.0%<br>**Precision**: Rules 100.0%, IF 93.44%, LSTM 98.36%, Combined 98.36%<br>**F1-Score**: Rules 1.0000, IF 0.6298, LSTM 0.9917, Combined 0.9917<br>**Latency**: Rules 0.01 ms, IF 1.84 ms, LSTM 0.17 ms, Combined 0.18 ms | **BLOCKED FOR RELEASE**: visual inspection found stale FA/hr labels (IF 14.4; LSTM/Combined 7.2) even though the active evidence classifies operational FA/hr as UNAVAILABLE. The image is not embedded in the manuscript and was left unaltered; regenerate only under separately authorized evidence-preserving figure maintenance. |
| **Figure A.2** (Release Candidate) | Audited Detection Comparison | [`research/exports/detection_comparison_release.png`](../exports/detection_comparison_release.png) | [`research/exports/generate_detection_comparison_release.ps1`](../exports/generate_detection_comparison_release.ps1) | **Recall**: Rules 100.00%, IF 47.50%, LSTM 100.00%, Combined 100.00%<br>**Precision**: Rules 100.00%, IF 93.44%, LSTM 98.36%, Combined 98.36%<br>**F1-Score**: Rules 1.0000, IF 0.6298, LSTM 0.9917, Combined 0.9917<br>**Measured mean batch latency**: Rules 0.01 ms, IF 1.84 ms, LSTM 0.17 ms, Combined 0.18 ms | **VERIFIED FOR RELEASE FIGURE CONTENT**: SHA-256 `701bd163df34d3acd965b55adf913798b23041e327016dbc5b0c30fa108dc69c`; visual inspection passed. Operational FA/hr is `UNAVAILABLE`, and no unverified Narrow/Resource result is plotted. |

---

## 3. Tables Cross-Verification Index

### Table 1: Comprehensive Anomaly Detection Benchmark Results
- **Source Artifact**: [`research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv`](../audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv)
- **Experimental Unit**: 24-step normalized sequence window ($\mathbf{X} \in \mathbb{R}^{24 \times 5}$)
- **Sample Count**: $N = 320$ windows ($200$ normal steady-state, $120$ incident episodes across 6 classes)
- **Verified Values Cross-Check Table**:

| Model Variant | TP | FP | TN | FN | Recall | Precision | Specificity | F1-Score | FPR (Window) | FA/hr | PR-AUC | Mean Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Narrow Rules** (historical comparator; not independently recalculated from current raw predictions) | 40 | 0 | 200 | 80 | 33.33% | 100.00% | 100.00% | 0.5000 | 0.00% | UNAVAILABLE | UNAVAILABLE | 0.01 ms |
| **Resource-Only Rules** (historical comparator; not independently recalculated from current raw predictions) | 80 | 0 | 200 | 40 | 66.67% | 100.00% | 100.00% | 0.8000 | 0.00% | UNAVAILABLE | UNAVAILABLE | 0.01 ms |
| **Full Operational Rules** (+ error $\ge$ 0.5%) | 120 | 0 | 200 | 0 | 100.00% | 100.00% | 100.00% | 1.0000 | 0.00% | UNAVAILABLE | UNAVAILABLE | 0.01 ms |
| **Isolation Forest** (Calibrated $\tau = -0.018694$) | 57 | 4 | 196 | 63 | 47.50% | 93.44% | 98.00% | 0.6298 | 2.00% | UNAVAILABLE | 0.9056 | 1.84 ms |
| **LSTM Autoencoder** (Calibrated $\tau = 0.709399$) | 120 | 2 | 198 | 0 | 100.00% | 98.36% | 99.00% | 0.9917 | 1.00% | UNAVAILABLE | 1.0000 | 0.17 ms |
| **Combined Alert** (Full Rules $\lor$ LSTM AE) | 120 | 2 | 198 | 0 | 100.00% | 98.36% | 99.00% | 0.9917 | 1.00% | UNAVAILABLE | N/A | 0.18 ms |

*Status*: **VERIFIED & CONCORDANT**. All values match `CORRECTED_DETECTION_METRICS.csv` to 4 decimal places.

---

### Table 2: Diagnostic Evaluation Across Seven Configurations
- **Source Artifact**: [`research/raw/diagnosis_predictions.csv`](../raw/diagnosis_predictions.csv), [`research/raw/diagnosis_metrics.csv`](../raw/diagnosis_metrics.csv)
- **Experimental Unit**: Canonical incident scenario ($N = 6$ failure scenarios)
- **Total Evaluations**: $7 \text{ configurations} \times 6 \text{ scenarios} = 42 \text{ evaluations}$
- **Verified Values Cross-Check Table**:

| Config ID | Architecture Description | Inference Engine | Strict Acc (ITT $N=6$) | Strict Acc (Completed Cases) | Lenient Acc ($N=6$) | Mean Completed-Case Pipeline Latency | API Cost |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Config 1** | Rule-Based Baseline | Deterministic Python Regex | **100.00%** ($6/6$) | **100.00%** ($6/6$) | **100.00%** ($6/6$) | **0.01 ms** | Not measured |
| **Config 2** | Single-Agent (Offline) | Deterministic Offline Heuristic | 50.00% ($3/6$) | 50.00% ($3/6$) | 50.00% ($3/6$) | 0.03 ms | Not measured |
| **Config 3** | Multi-Agent Full (Offline) | Deterministic Offline Heuristic + DL | 50.00% ($3/6$) | 50.00% ($3/6$) | 50.00% ($3/6$) | 0.57 ms | Not measured |
| **Config 4** | Multi-Agent No-DL (Offline) | Deterministic Offline Heuristic (Log-Only) | 100.00% ($6/6$) | 100.00% ($6/6$) | 100.00% ($6/6$) | 0.11 ms | Not measured |
| **Config 5** | Single-Agent (Live Groq LLM) | Groq Cloud API (`openai/gpt-oss-20b`) | 66.67% ($4/6$) | 80.00% ($4/5$) | 66.67% ($4/6$) | 3.04 s | Not measured |
| **Config 6** | Multi-Agent Full (+ DL Handoff) | Groq Cloud API (`openai/gpt-oss-20b`) + DL MSE | 83.33% ($5/6$) | 83.33% ($5/6$) | 100.00% ($6/6$) | 23.19 s | Not measured |
| **Config 7** | Multi-Agent No-DL (Live Groq LLM) | Groq Cloud API (`openai/gpt-oss-20b`) (Log-Only) | 66.67% ($4/6$) | 80.00% ($4/5$) | 83.33% ($5/6$) | 19.28 s | Not measured |

*Status*: **VERIFIED & CONCORDANT**. Omissions accounted for: Config 5 omitted INC-1002 and Config 7 omitted INC-1004 (timeout/rate limit). Discloses that multi-agent LLM did not outperform rule baseline. API cost is **Not measured** because token counts, provider billing records, applicable pricing, and a reproducible calculation are unavailable.

---

### Table 3: Scenario-by-Scenario Diagnostic Breakdown
- **Source Artifact**: `research/raw/diagnosis_predictions.csv`
- **Experimental Unit**: Ground-truth incident ticket (`INC-1001` through `INC-1006`)
- **Verified Values Cross-Check Table**:

| Incident ID | Ground-Truth Fault Class | Synthetic Fault Signature | Primary Attributed Feature | Live LLM Predicted Cause | Strict Match | Lenient Match |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **INC-1001** | Database connection pool exhaustion | Latency & HTTP 500 spike; pool ceiling | `latency_ms` & `error_rate_pct` | Database connection pool exhaustion caused all connections to be in use, preventing new database connections and resulting in HTTP 500 responses. | 1 (True) | 1 (True) |
| **INC-1002** | Database service stopped | TCP refused; latency spike to 1250ms | `latency_ms` & `error_rate_pct` | PostgreSQL service crashed due to abnormal disk I/O contention (high disk usage and latency) | 0 (False)* | 1 (True) |
| **INC-1003** | Worker service thread exhaustion causing sustained CPU saturation | CPU ramp to 99% + memory to 91% | `cpu_pct` | Worker-service thread explosion or infinite loop consuming CPU | 1 (True) | 1 (True) |
| **INC-1004** | Runaway application log growth consumed disk capacity | Disk capacity monotonic ramp to 99.5% | `disk_pct` | Disk full caused by oversized application log file and lack of log rotation | 1 (True) | 1 (True) |
| **INC-1005** | Incorrect OAuth issuer configuration | HTTP 500 auth token validation errors | `error_rate_pct` | OAuth2 provider misconfiguration (issuer URL mismatch) | 1 (True) | 1 (True) |
| **INC-1006** | Broken service route between service-a and service-b | Downstream API timeout & packet drops | `latency_ms` | Network connectivity issue (CNI plugin packet drops or misconfigured network policy) | 1 (True) | 1 (True) |

*\*Note: INC-1002 received strict score 0 because the LLM attributed the database stoppage to abnormal disk I/O contention rather than a service shutdown; lenient scoring accepted database outage as an operationally aligned domain.*

*Status*: **VERIFIED & CONCORDANT**.

---

### Table 4: Safety, Governance, and Execution Boundary Test Suite
- **Source Artifact**: `research/raw/safety_test_results.csv`, `research/raw/safety_metrics.csv`
- **Experimental Unit**: Discrete invocation request ($N = 16$ test cases)
- **Verified Values Cross-Check Table**:

| Test Cohort | Case Count | Target Mechanism Tested | Expected Safety Response | Observed Execution Result | Success Rate | 95% Wilson CI |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: |
| **Adversarial Invocations** | 11 | Missing ticket (`TC-ATT-01`), expired approval (`TC-ATT-02`), invalid phrase (`TC-ATT-03`), action mismatch (`TC-ATT-04`), target mismatch (`TC-ATT-05`), incident mismatch (`TC-ATT-06`), consumed ticket replay (`TC-ATT-07`), rejected ticket (`TC-ATT-08`), remote HTTPS boundary (`TC-ATT-09`), remote HTTP (`TC-ATT-10`), embedded credentials (`TC-ATT-11`) | `ApprovalError` / `RuntimeError` / `ValueError`; zero state mutation | Blocked at execution boundary; zero arbitrary execution | **100.0%** ($11/11$) | $[0.7412, 1.0000]$ |
| **Precondition Validations** | 2 | Target service offline (`TC-FAIL-01`), no active fault (`TC-FAIL-02`) | Abort execution before remediation command dispatch | Clean abort with state logged as PRECONDITION_FAILED | **100.0%** ($2/2$) | $[0.3424, 1.0000]$ |
| **Verification Probes** | 1 | Degraded service after attempted recovery (`TC-VERIF-01`) | Rollback / escalate ticket to HUMAN_REQUIRED | Fake recovery rejected; ticket escalated | **100.0%** ($1/1$) | $[0.2065, 1.0000]$ |
| **Positive Controls** | 2 | Legitimate valid approved remediation commands (`TC-POS-01`, `TC-AUDIT-01`) | Execute authorized template; write audit record | Executed successfully; full SQLite audit trail | **100.0%** ($2/2$) | $[0.3424, 1.0000]$ |

*Status*: **VERIFIED & CONCORDANT**. Disaggregates adversarial attacks from control probes. Bounded strictly to local application execution boundary. Mean attack check latency: 11.32 ms.

---

### Supporting Statistical Analysis S1: Hypothesis Testing and Uncertainty Intervals (Not a Manuscript Table)
- **Source Artifact**: [`research/audits/detection_rate_and_phase4_gate_20261012/STATISTICAL_ASSUMPTION_REVIEW.md`](../audits/detection_rate_and_phase4_gate_20261012/STATISTICAL_ASSUMPTION_REVIEW.md)
- **Experimental Units**: Paired window outcomes ($N = 120$ fault windows) & Cluster failure modes ($N = 6$ failure scenarios)
- **Verified Values Cross-Check Table**:

| Statistical Test | Comparison Target | Sample Unit ($N$) | Test Statistic | Exact $p$-Value | Effect Size / Interval | Methodological Validity Notes |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **Exact McNemar Test** | LSTM Autoencoder vs Isolation Forest | $N = 120$ paired fault windows | $b = 63, c = 0$ | $p = 2.168 \times 10^{-19}$ | $\Delta = +0.5250$ | Descriptive at window level ($N=120$). Caveat: Clustered within 6 scenarios (20 replicates each). |
| **Wald Paired Difference CI** | LSTM Autoencoder vs Isolation Forest | $N = 120$ paired fault windows | $\text{SE} \approx 0.0456$ | N/A | $95\%\ \text{CI}: [+0.4357, +0.6143]$ | Quantifies sensitivity difference on 120 synthetic fault windows. |
| **Wilcoxon Signed-Rank Test** | LSTM Autoencoder vs Isolation Forest | $N = 6$ failure classes (clustered) | $W = 0.0$ | $p = 0.03125$ | $\Delta_{\text{median}} = +0.600$ | Exploratory scenario-level paired analysis ($N = 6$) treating scenarios as summary units to address window clustering. Statistically significant at $\alpha = 0.05$ (minimum possible two-sided $p = 2/64 = 0.03125$). |
| **Wilson Score Interval** | Adversarial Boundary Containment | $N = 11$ adversarial attacks | $k = 11$ | N/A | $95\%\ \text{CI}: [0.7412, 1.0000]$ | Asymmetric binomial interval reflecting small-sample containment. |

*Status*: **VERIFIED & CONCORDANT**. Both window-level and exploratory scenario-level paired tests reported with full transparency.

---

## 4. Final Consistency Verification Sign-Off

The four manuscript tables and five figure entries have been cross-checked against source code, raw predictions, and corrected metric files. Supporting Statistical Analysis S1 is an audit/index artifact, not a manuscript table. Definitions, sample counts, contingency cells, and rounding are concordant within the documented evidence limits.
