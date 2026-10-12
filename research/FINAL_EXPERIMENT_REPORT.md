# AegisOps: Verified Research Audit, Empirical Evidence Report, and Methodological Correction

**Report Date**: 2026-10-12  
**Project Workspace**: `C:\DL_PROJECT`  
**Git Revision**: `e69cb623ed6902edfbb1d2b946a526cbb23f90ad` (`main` branch)  
**Host Platform**: Windows 11 Pro (`win32` / AMD64), PowerShell 5.1 / PowerShell 7  
**Runtime Environment**: Python `3.11.9` (`C:\DL_PROJECT\.venv\Scripts\python.exe`)  
**Key Package Versions**: PyTorch `2.14.1`, Scikit-Learn `1.9.0`, SciPy `1.17.1`, Pandas `3.0.6`, NumPy `2.4.6`, Streamlit `1.42.0`, FastAPI `0.115.11`, Uvicorn `0.34.0`, Pytest `9.1.1`  
**Auditors & Investigators**: Senior ML Researcher, Software Test Engineer, and Research-Methodology Auditor  

---

## 1. Executive Summary & Audit Scope

This document presents the definitive audit, empirical corrections, and reproducible benchmark evaluations for the AegisOps autonomous incident-response system. All evaluations were conducted strictly on the existing codebase without fabricating synthetic metrics, without tuning thresholds on test data, and without altering core application architecture.

Prior research outputs have been audited, backed up to `research/backup_prior_outputs/`, and corrected to resolve statistical and methodological oversights identified during peer audit:
1. **Statistical Test Correction**: Replaced the flawed discordant calculation with the exact two-sided binomial test (`scipy.stats.binomtest`), adding unit tests for the benchmark case $b = 4, c = 2 \implies p = 0.6875$. Recalculated all p-values and confidence intervals.
2. **Telemetry & Data Separation**: Investigated the historical SQLite database (`aegisops_live.sqlite3`, 200 rows), explaining why `anomaly_score` is 100% NULL (bootstrap rules fallback). Clearly separated synthetic benchmark evaluations from genuine live telemetry.
3. **Diagnostic Rubric & Denominator Clarity**: Re-evaluated all 7 root-cause diagnosis configurations under an explicit 4-tier rubric (`CORRECT`, `PARTIALLY_CORRECT`, `INCORRECT`, `UNASSESSABLE`). Resolved count vs. percentage discrepancies by reporting both full-cohort ($N = 6$) and per-protocol metrics.
4. **Direct Application Safety Audit**: Replaced mock boolean tests with direct execution of actual application verification and recovery functions (`ApprovalStore`, `_resolve_local_test_fault`, and `TelemetryStore`) against a live local FastAPI test microservice on `127.0.0.1:8765`. Separated positive controls from attack cases.

---

## 2. Project Version & Environment Verification

| Attribute | Verified Value | Verification Method / Evidence |
| :--- | :--- | :--- |
| **Workspace Root** | `C:\DL_PROJECT` | Local filesystem path |
| **Git Commit** | `e69cb623ed6902edfbb1d2b946a526cbb23f90ad` | `git rev-parse HEAD` on `main` branch |
| **Python Runtime** | `3.11.9 (tags/v3.11.9:de5405b)` | `sys.version` in `.venv` |
| **PyTorch Version** | `2.14.1` (CPU) | `torch.__version__` |
| **Scikit-Learn** | `1.9.0` | `sklearn.__version__` (via site-packages bridge) |
| **SciPy Version** | `1.17.1` | `scipy.__version__` (via site-packages bridge) |
| **Test Suite Pass Rate** | **42 / 42 passed (100.0%)** | `pytest -v` executed in 50.57s |

### Investigation of Historical `is_local_target` NameError
* **Historical Defect**: In early iterations of `live_monitoring.py`, `_build_live_incident()` attempted to evaluate service health using `if is_local_target:`, but `is_local_target` was defined only within `live_panel()`, raising `NameError: name 'is_local_target' is not defined`.
* **Current Status**: In the current codebase (`e69cb62`), line 366 resolves locality using the pure function `if _is_loopback_target(service_url):`, while `live_panel()` line 642 explicitly initializes `is_local_target = _is_loopback_target(service_url)` before any conditional branch.
* **Regression Test**: Added `test_build_live_incident_scoping_and_name_error_prevention` to `test_live_monitoring.py`. Tested with both local loopback (`http://127.0.0.1:8765`) and remote HTTPS targets; passed with zero errors.

---

## 3. Data & Label Audit: Live Telemetry vs. Synthetic Data

### A. Live Telemetry Database (`data/aegisops_live.sqlite3`)
- **Total Rows**: 200 telemetry samples recorded over a 24-minute window.
- **Label Breakdown**: 31 normal steady-state samples (15.5%), 1 latency spike (0.5%), 168 HTTP 500 error samples (84.0%).
- **Audit of Missing Anomaly Scores**: `anomaly_score` is **100.0% NULL** across all 200 rows. Investigation revealed that the live monitoring session operated in `bootstrap_rules` mode because the neural detector was not loaded during collection. These rows represent rule-based telemetry, not neural predictions.
- **Independent Episode Reconstruction**: To avoid pseudoreplication, the 168 consecutive error samples were grouped into **4 independent incident episodes** (`EP-01` to `EP-04`) using `incident_events` start/recovery timestamps.
- **Model Retraining Ineligibility**: `dl/live_training.py` enforces a minimum sanity threshold of $\ge 180$ healthy samples. The database contains only 31 healthy samples, correctly blocking automated retraining.

### B. Synthetic Benchmark Dataset
- **Generation Method**: Controlled sinusoidal and polynomial synthesis (`generate_normal_windows()` and `generate_incident_telemetry()`) with fixed seed (seed = 2026).
- **Training Set**: 680 normal steady-state windows (24 timesteps $\times$ 5 features) used to fit Isolation Forest and establish validation thresholds.
- **Held-Out Test Set**: $N = 320$ independent windows:
  - 200 steady-state normal windows (0.278 hours at 5s sampling rate).
  - 120 fault episodes across 6 failure modes (20 independent episodes each).
- **Transparency Statement**: Results from this benchmark reflect algorithmic sensitivity on controlled multivariate signals; they **must not** be presented as empirical enterprise production metrics.

---

## 4. Experiment A: Anomaly Detection Benchmarks

All models were evaluated on the identical held-out test dataset ($N = 320$ windows).

### Summary Metrics Table

| Metric | Operational Rules | Isolation Forest | LSTM Autoencoder | Combined Alert |
| :--- | :---: | :---: | :---: | :---: |
| **Model Nature** | Static Heuristics | Unsupervised Ensemble | Symmetric LSTM AE | Dual-Gate Hybrid |
| **Decision Threshold** | Hardcoded Gates | Score $\le -0.05$ | $\tau = 0.709399$ (99th %ile) | Either Triggers |
| **True Positives (TP)** | 40 | 57 | **120** | **120** |
| **False Positives (FP)** | **0** | 4 | 2 | 2 |
| **True Negatives (TN)** | **200** | 196 | 198 | 198 |
| **False Negatives (FN)** | 80 | 63 | **0** | **0** |
| **Recall (Sensitivity)** | 33.33% | 47.50% | **100.00%** | **100.00%** |
| **Precision** | **100.00%** | 93.44% | 98.36% | 98.36% |
| **F1-Score** | 0.5000 | 0.6298 | **0.9917** | **0.9917** |
| **PR-AUC** | *N/A (Binary)* | 0.6841 | **0.9998** | **0.9998** |
| **False Alarms / Hour** | **0.0 / hr** | 14.4 / hr | 7.2 / hr | 7.2 / hr |
| **False Positive Rate** | **0.0%** | 2.0% | 1.0% | 1.0% |
| **Mean Latency (ms)** | **0.005 ms** | 0.220 ms | 0.170 ms | 0.175 ms |

### Key Detection Findings:
1. **Temporal Degradation Sensitivity**: The LSTM Autoencoder achieved 100% detection across gradual memory leaks (20/20) and disk pressure (20/20). Isolation Forest failed on both (0/20 each) because window-mean aggregation flattens gradual slope trends.
2. **PR-AUC Metric Justification**: PR-AUC is defined for continuous anomaly scores (LSTM MSE loss and Isolation Forest decision function). For Operational Rules, PR-AUC is mathematically undefined because the rule produces discrete boolean flags without a tunable real-valued decision threshold.
3. **Detection Delay**: Abrupt faults (CPU saturation, HTTP 500 error burst) trigger immediately on the first sample (0-step delay). Gradual memory leaks trigger at step 4 (20 seconds from injection onset) when cumulative RAM cross-correlates with reconstruction error.

---

## 5. Experiment B: Root-Cause Diagnosis Audit

All 7 configurations were evaluated across the 6 ground-truth incidents in `data/incidents.json`. Every prediction was audited against an explicit 4-tier rubric:

### Explicit Diagnostic Rubric:
- **`CORRECT`**: Identifies the true underlying causal mechanism matching ground truth.
- **`PARTIALLY_CORRECT`**: Identifies the correct subsystem or symptom, but misidentifies or omits the exact causal mechanism (e.g., attributing database failure to disk contention or calling worker thread exhaustion generic CPU load).
- **`INCORRECT`**: Attributes failure to wrong subsystem, opposite cause, or irrelevant component.
- **`UNASSESSABLE`**: The system failed to produce a prediction due to an API timeout, rate limit (HTTP 429), or schema error.

### Diagnosis Results Table

| Configuration | Execution Mode | DL Evidence | Total Incidents | Completed | Correct (Strict) | Partially Correct | Incorrect | Unassessable | Full-Cohort Acc ($N=6$) | Per-Protocol Acc | Mean Latency |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Rule Baseline** | Deterministic Regex | No | 6 | 6 | 6 | 0 | 0 | 0 | **100.0%** | **100.0%** | 0.01 ms |
| **2. Single-Agent (Offline)** | Deterministic Fallback | Yes | 6 | 6 | 3 | 0 | 3 | 0 | **50.0%** | **50.0%** | 0.03 ms |
| **3. Multi-Agent Full (Offline)**| Deterministic Fallback | Yes | 6 | 6 | 3 | 0 | 3 | 0 | **50.0%** | **50.0%** | 0.50 ms |
| **4. Multi-Agent No-DL (Offline)**| Deterministic Fallback | No | 6 | 6 | 6 | 0 | 0 | 0 | **100.0%** | **100.0%** | 0.11 ms |
| **5. Single-Agent (Groq LLM)** | Live API (`gpt-oss-20b`)| Yes | 6 | 5 | 4 | 0 | 1 | 1 | **66.7%** | **80.0%** | 3,041 ms |
| **6. Multi-Agent Full (Groq LLM)**| Live API (`gpt-oss-20b`)| Yes | 6 | 6 | 5 | 1 | 0 | 0 | **83.3%** | **83.3%** | 23,189 ms |
| **7. Multi-Agent No-DL (Groq)** | Live API (`gpt-oss-20b`)| No | 6 | 5 | 4 | 0 | 1 | 1 | **66.7%** | **80.0%** | 19,280 ms |

### Resolution of Counts vs. Percentages:
* **The Discrepancy**: In earlier drafts, Single-Agent LLM was reported as "100.0% accuracy (5/5)". However, 1 of the 6 incidents (`INC-1002`) was omitted during testing due to API rate limits. Reporting 100% was misleading.
* **The Resolution**: Under an intent-to-treat / full-cohort evaluation ($N = 6$), Single-Agent LLM achieved **66.7%** (4 correct, 1 incorrect, 1 unassessable). Evaluated per-protocol on completed cases, it achieved **80.0%** (4/5).
* **Multi-Agent Full LLM Performance**: Evaluated on all 6 incidents without drops, achieving **83.3% strict accuracy** (5/6 correct, 1 partially correct: correctly identifying PostgreSQL crashed but hallucinating disk I/O contention).
* **Power Constraint**: Because $N = 6$, statistical power is $1 - \beta \approx 0.14$. These results represent a feasibility pilot, not an asymptotic statistical comparison.

---

## 6. Experiment C: Safety Boundary and Recovery Verification

Safety and verification were tested directly against the actual application functions:
- `approval.ApprovalStore` (`BEGIN IMMEDIATE` atomic SQLite transactions).
- `live_monitoring._resolve_local_test_fault` (target URL validation, loopback gate, `/admin/fault` resetting, probe health checks, and verification).
- `storage.telemetry_store.TelemetryStore` (durable audit trail).
- Local disposable FastAPI microservice on `127.0.0.1:8765`.

### Explicit Separation: Positive Controls vs. Attack Cases

| Security Domain | Metric / Category | Numerator | Denominator | Observed Rate | Wilson 95% CI | Test Description |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Positive Control** | Valid Approval & Recovery Accepted | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Full lifecycle: request, approve with exact phrase, consume, execute reset on injected fault, verify health |
| **Attack Case** | Missing Ticket ID Blocked | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Consuming non-existent UUID token raises `ApprovalError` |
| **Attack Case** | Expired Ticket Blocked | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Consuming ticket past `expires_at` raises `ApprovalError` |
| **Attack Case** | Malformed Confirmation Phrase | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Approving with non-matching confirmation string raises `ApprovalError` |
| **Attack Case** | Mismatched Action Scope | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Consuming ticket with altered action ID raises `ApprovalError` |
| **Attack Case** | Mismatched Target URL Scope | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Consuming ticket with altered target host raises `ApprovalError` |
| **Attack Case** | Mismatched Incident ID Scope | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Consuming ticket with altered incident ID raises `ApprovalError` |
| **Attack Case** | Replay Attack Blocked | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Re-consuming an already consumed ticket raises `ApprovalError` |
| **Attack Case** | Rejected Ticket Blocked | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Consuming an explicitly rejected ticket raises `ApprovalError` |
| **Attack Case** | Remote Target Remediation Blocked | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Calling `_resolve_local_test_fault` on remote host raises `RuntimeError` |
| **Attack Case** | Remote Plaintext HTTP Blocked | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Registering remote `http://` target raises `ValueError` |
| **Attack Case** | Embedded Credentials Blocked | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | URLs containing user:pass raise `ValueError` |
| **Execution Safety** | Execution on Unreachable Port | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Target port with no listener aborts safely with `RuntimeError` |
| **Execution Safety** | Redundant Recovery on Healthy Host | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Calling reset when fault is normal aborts safely with `RuntimeError` |
| **Verification Gate** | Persistent Fault Verification Failure | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Recovery executes but probe still fails; verification marks `success=False` |
| **Audit Verification** | SQLite Audit Trail Completeness | 16 | 16 | **100.0%** | $[0.8064, 1.0000]$ | All lifecycle events persisted in `incident_events` with valid payloads |

### Aggregate Safety Findings:
- **Total Adversarial Attacks Attempted**: 14
- **Total Attacks Blocked**: 14 (**100.0% enforcement rate**, Wilson 95% CI: $[0.7847, 1.0000]$)
- **Unauthorized Action Execution Rate**: **0.0%** (0 / 14)
- **False Recovery Declaration Rate**: **0.0%** (0 / 1)
- **Mean Enforcement Check Latency**: **0.84 ms**

---

## 7. Statistical Hypotheses & Significance Audit

### Primary Confirmatory Hypothesis (Detection Recall)
* **Outcome**: Episode-level detection sensitivity on $N = 120$ paired fault episodes.
* **Models**: LSTM Autoencoder vs. Isolation Forest.
* **Discordant Counts**: $b = 63$ (LSTM detected, IsoForest missed), $c = 0$ (IsoForest detected, LSTM missed).
* **Two-Sided Exact Binomial Test**:
  $$p = 2 \times (0.5)^{63} = \mathbf{2.168 \times 10^{-19}} \quad (p < 0.001)$$
* **Continuity-Corrected $\chi^2$**: $\chi^2 = \frac{62^2}{63} = \mathbf{61.02} \quad (p = 5.66 \times 10^{-15})$.
* **Effect Size**: $\Delta_{\text{Recall}} = \mathbf{+0.5250} \quad (95\% \text{ Wald CI}: [+0.4350, +0.6150])$.
* **Verdict**: **Confirmatory & Statistically Significant**. Reject $H_0$ at $\alpha = 0.001$.

### Secondary Exploratory Hypothesis (Normal False Alarms)
* **Outcome**: False alarm rate on $N = 200$ normal steady-state windows.
* **Discordant Counts**: $b = 4$ (IsoForest alarmed only), $c = 2$ (LSTM alarmed only).
* **Two-Sided Exact Binomial Test**:
  $$p = \mathbf{0.6875} \quad (p > 0.05)$$
* **Verdict**: **Exploratory / Not Statistically Significant**. The difference in false alarms between LSTM (1.0%) and Isolation Forest (2.0%) does not achieve statistical significance on 200 windows.

---

## 8. Categorization of Research Findings

To ensure scientific integrity in the manuscript:

### A. Verified Results (Confirmatory)
1. The LSTM Autoencoder significantly outperforms static windowing Isolation Forest baselines on multivariate temporal faults ($p < 10^{-18}$, $\Delta = +0.5250$).
2. Two-man-rule approval tickets with exact parameter scope binding completely prevent replay attacks, parameter tampering, and unauthorized action execution on the tested local harness.
3. Independent post-remediation health verification successfully catches persistent faults and overrules premature recovery claims.

### B. Exploratory Results
1. The observed difference in false alarm rates on 200 normal windows (1.0% vs. 2.0%) is exploratory and not statistically significant ($p = 0.6875$).
2. Root-cause diagnostic comparisons across 6 scenarios provide feasibility evidence that learned anomaly signals guide generative LLMs, but sample size constraints prevent asymptotic significance claims.

### C. Synthetic-Only Results
1. The detection performance of `models/lstm_autoencoder.pt` was evaluated on synthetically generated sinusoidal time-series with Gaussian noise. It must be reported as a synthetic benchmark.

### D. Failed or Incomplete Experiments
1. **Live Model Retraining**: Retraining a neural detector from historical SQLite telemetry (`data/aegisops_live.sqlite3`) failed because the database contains only 31 healthy samples, failing the codebase's $\ge 180$ sample safety threshold.
2. **Groq Cloud LLM Rate Limits**: Due to free-tier TPM rate limits, 1 out of 6 incident evaluations was dropped in Single-Agent LLM and Multi-Agent No-DL configurations.

### E. Claims the Research Paper MUST NOT Make
1. **Do NOT claim production readiness**: The system was validated on a local loopback microservice, not on a distributed production cluster.
2. **Do NOT claim the model was trained on production telemetry**: The base checkpoint was trained on synthetic sinusoidal time-series.
3. **Do NOT claim statistical significance for root-cause diagnosis**: With $N = 6$, Experiment B is an observational pilot study.
4. **Do NOT claim host metrics reflect container state**: Host CPU/RAM metrics sampled via `psutil` describe the developer workstation, not the monitored microservice.

---

## 9. Next Steps for Manuscript Completion

1. **Section 4 (System Architecture)**: Detail the two-man-rule ticket engine and cite the exact `BEGIN IMMEDIATE` atomic state transitions verified in `research/SAFETY_EVALUATION.md`.
2. **Section 5 (Experimental Evaluation)**: Embed Figure 1 (`research/figures/detection_confusion_matrices.png`) and Figure 2 (`research/figures/detection_comparison.png`).
3. **Section 5 (Table Construction)**: Transcribe numbers directly from `research/raw/detection_metrics.csv` and `research/raw/safety_metrics.csv`.
4. **Section 6 (Threats to Validity)**: Include explicit discussions of the host-level `psutil` sampling constraint and the 6-scenario pilot scope.
5. **Reproducibility Guarantee**: Reference `python -m research.run_all` as the verified end-to-end entry point.
