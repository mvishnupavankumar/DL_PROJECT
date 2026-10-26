# AegisOps: External Benchmark Evaluation Protocol (Pre-Registration)

**Document Path**: `research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md`  
**Git Baseline Commit**: `d277c1df3c2599ddecdf5f0bb761c99718499667` (Branch: `main`)  
**Target External Benchmark**: **AnoMod** (MSR 2026, Zenodo DOI: `10.5281/zenodo.18342898`)  
**Audit Standard**: Pre-Registered Evaluation Protocol & Scientific Integrity Guardrail  
**Date**: October 2026  
**Status**: **FROZEN PROTOCOL (AWAITS LOCAL DATASET INGESTION)**  

---

## 1. Objective and Pre-Registration Scope

This document specifies the exact, frozen evaluation protocol for validating the AegisOps anomaly detection and root-cause diagnosis pipelines against the external **AnoMod** benchmark. 

### Core Protocol Principles:
1. **Zero Data Snooping / Leakage**: Feature mappings, normalization procedures, baseline definitions, and calibration quantiles are established strictly prior to evaluating external test sets.
2. **Strict Separation of Experiments**: The original synthetic benchmark (Experiment A, Experiment B, Experiment C) remains frozen as a distinct study. External validation results will be reported in a dedicated, separately versioned section (e.g., *Experiment D: External Benchmark Validation*).
3. **No Threshold Tuning on Test Labels**: Anomaly detection thresholds on external data must be calibrated exclusively on nominal warmup sequences, never on labelled incident episodes.
4. **Transparent Blocker Reporting**: If external transfer or schema constraints prevent immediate automated execution, the protocol documents the exact operational prerequisites rather than manufacturing synthetic proxies.

---

## 2. Research Questions and Formal Hypotheses

### Research Questions for External Validation
- **RQ1-ext (Out-of-Distribution Generalization)**: *Does the AegisOps multivariate LSTM Autoencoder architecture generalize to real-world containerized microservice telemetry from AnoMod, outperforming static threshold rules and Isolation Forests on realistic multi-service faults?*
- **RQ2-ext (Cross-Modal Attributed RCA)**: *Does providing neural reconstruction error vectors across container metrics improve multi-agent LLM root-cause localization accuracy over unstructured container logs alone in a complex microservice topology?*

### Formal Statistical Hypotheses (RQ1-ext)
Let $p_{\text{LSTM}}^{\text{ext}}$ and $p_{\text{IF}}^{\text{ext}}$ denote the sensitivity (recall) of the LSTM Autoencoder and Isolation Forest on paired external fault episodes:
$$\begin{aligned}
H_0^{\text{ext}} &: p_{\text{LSTM}}^{\text{ext}} = p_{\text{IF}}^{\text{ext}} \quad (\text{No sensitivity difference on external benchmark}) \\
H_1^{\text{ext}} &: p_{\text{LSTM}}^{\text{ext}} \ne p_{\text{IF}}^{\text{ext}} \quad (\text{Statistically significant difference on external benchmark})
\end{aligned}$$

---

## 3. Dataset Specification and Inclusion/Exclusion Criteria

### 3.1 Target Dataset Version
- **Dataset Name**: AnoMod (v1.0.0)
- **Publication**: Proceedings of the 23rd IEEE/ACM International Conference on Mining Software Repositories (MSR '26)
- **Permanent Identifier**: Zenodo record `18342898` (DOI: `10.5281/zenodo.18342898`)
- **Underlying Systems**: SocialNetwork (21 microservices) and TrainTicket (41 microservices)

### 3.2 Inclusion Criteria
To be included in the external validation cohort, an AnoMod scenario run must satisfy:
1. **Multimodal Synchronization**: Must contain synchronously timestamped Prometheus metrics (`metrics/`), application logs (`logs/`), and client API response logs (`api_responses/`).
2. **Unambiguous Ground Truth**: Must possess an explicit anomaly injection timestamp ($t_{\text{fault}}$), target container identifier, and failure category documented in the run metadata.
3. **Sufficient Nominal Warmup**: Must contain at least $15\text{ minutes}$ of uninterrupted, nominal steady-state operation prior to fault activation to establish sliding-window calibration baselines.

### 3.3 Exclusion Criteria
A scenario run will be excluded if:
1. Missing Prometheus metric files or corrupted CSV formatting.
2. Injected faults caused total node crash or hypervisor termination, resulting in zero metric samples during the fault window.
3. Overlapping or cascading faults where multiple independent injections occurred simultaneously without intermediate system reset.

---

## 4. Feature Mapping and Preprocessing Pipeline

### 4.1 Schema Reconciliation: Multi-Service to 5-Dimensional Representation
AegisOps operates over a 5-dimensional observation vector $\mathbf{x}_t \in \mathbb{R}^5$. To bridge the gap between AnoMod's multi-container Prometheus metric store and the AegisOps pipeline, metrics will be mapped from the **API Gateway / Frontend Entrypoint Service** (e.g., `nginx-web-server` in SocialNetwork; `ts-ui-dashboard` in TrainTicket) along with cluster aggregates:

| AegisOps Feature | Semantic Description | AnoMod Prometheus / API Metric Mapping | Unit / Scale |
| :--- | :--- | :--- | :--- |
| **$x_t^{(1)}$: `cpu_pct`** | Node / Container CPU Utilization | `rate(container_cpu_usage_seconds_total{container="entrypoint"}[1m]) * 100` | Percentage $[0.0, 100.0]$ |
| **$x_t^{(2)}$: `memory_pct`** | Container Memory Utilization | `(container_memory_working_set_bytes / container_spec_memory_limit_bytes) * 100` | Percentage $[0.0, 100.0]$ |
| **$x_t^{(3)}$: `disk_pct`** | Node Disk I/O Utilization | `rate(container_fs_writes_bytes_total[1m])` normalized to nominal max | Normalized $[0.0, 100.0]$ |
| **$x_t^{(4)}$: `latency_ms`** | Client-Observed Request Latency | P95 latency recorded in `api_responses/response_time.log` | Milliseconds ($\mathbb{R}_{\ge 0}$) |
| **$x_t^{(5)}$: `error_rate_pct`** | Client-Observed HTTP Error Rate | Fraction of non-2xx HTTP responses in `api_responses/` | Fraction $[0.0, 1.0]$ |

### 4.2 Temporal Alignment and Resampling
- **Sampling Rate Conversion**: AnoMod Prometheus scrapes are collected at $\Delta t = 15\text{ seconds}$. Telemetry will be resampled to $\Delta t = 5\text{ seconds}$ via linear interpolation, or sliding window length will be set to $W = 8$ steps (preserving the $120\text{-second}$ temporal horizon: $8 \times 15\text{s} = 120\text{s}$).
- **Normalization Protocol**:
  Min-max normalization parameters $\mathbf{x}_{\min}^{\text{ext}}, \mathbf{x}_{\max}^{\text{ext}}$ will be computed **strictly on the nominal warmup partition** ($t < t_{\text{fault}}$):
  $$\tilde{\mathbf{x}}_t = \frac{\mathbf{x}_t - \mathbf{x}_{\min}^{\text{ext}}}{\mathbf{x}_{\max}^{\text{ext}} - \mathbf{x}_{\min}^{\text{ext}} + \epsilon}$$
  Zero test-set or fault-period data will be used to compute normalization bounds.

---

## 5. Partitioning, Baselines, and Threshold Selection

### 5.1 Dataset Partitioning
For each evaluated external microservice system (SocialNetwork / TrainTicket):
1. **Nominal Warmup Partition (70%)**: Unaffected steady-state traffic used exclusively to fit normalization scalers and calibrate anomaly thresholds.
2. **Nominal Validation Partition (30%)**: Unaffected steady-state sequences used to verify false-positive rates.
3. **Evaluation Fault Partition (100% held-out)**: All active fault injection windows across all valid scenario runs.

### 5.2 Baseline Detector Configurations
1. **Narrow Rules Baseline**:
   $$\hat{y}_t^{\text{narrow}} = \mathbb{I}\left( x_t^{(4)} \ge 1000.0 \lor x_t^{(2)} \ge 95.0 \right)$$
2. **Resource-Only Rules Baseline**:
   $$\hat{y}_t^{\text{resource}} = \mathbb{I}\left( x_t^{(1)} \ge 90.0 \lor x_t^{(2)} \ge 95.0 \lor x_t^{(3)} \ge 95.0 \lor x_t^{(4)} \ge 1000.0 \right)$$
3. **Full Operational Rules Baseline**:
   $$\hat{y}_t^{\text{full}} = \mathbb{I}\left( x_t^{(1)} \ge 90.0 \lor x_t^{(2)} \ge 95.0 \lor x_t^{(3)} \ge 95.0 \lor x_t^{(4)} \ge 1000.0 \lor x_t^{(5)} > 0.005 \right)$$
4. **Isolation Forest Baseline**:
   - Fitted on nominal warmup partition with $k = 100$ trees, `contamination=0.01`, `random_state=42`.
   - Threshold $\tau_{\text{IF}}^{\text{ext}}$ calibrated at 99th percentile of negated decision scores on nominal validation.
5. **AegisOps LSTM Autoencoder**:
   - Option A (Zero-Shot Direct Transfer): Frozen PyTorch weights (`models/lstm_autoencoder.pt`) evaluated directly on min-max normalized external sequences. Threshold $\tau_{\text{LSTM}}^{\text{ext}}$ recalibrated at 99th percentile of nominal validation reconstruction errors.
   - Option B (Fine-Tuned Transfer): Model weights fine-tuned on nominal external warmup data for 5 epochs if severe architectural domain shift occurs. (Must be reported as a separate, explicitly labeled variant).

---

## 6. Primary Evaluation Metrics & Statistical Testing

### 6.1 Evaluation Metrics
- **True Positives (TP)**: Number of fault episode windows correctly flagged ($y = 1, \hat{y} = 1$).
- **False Positives (FP)**: Number of nominal windows incorrectly flagged ($y = 0, \hat{y} = 1$).
- **True Negatives (TN)**: Number of nominal windows correctly unflagged ($y = 0, \hat{y} = 0$).
- **False Negatives (FN)**: Number of fault episode windows missed ($y = 1, \hat{y} = 0$).
- **Episode Sensitivity (Recall)**: $\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$.
- **False-Positive Window Rate ($\text{FPR}_{\text{window}}$)**: $\text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}$.
- **Precision, Specificity, F1-Score, and PR-AUC**.
- **Operational False Alarms / Hour**: Marked `UNAVAILABLE` unless a continuous streaming deduplication harness is implemented.

### 6.2 Statistical Testing
- **Window-Level Test**: Paired exact McNemar test with Edwards continuity correction on discordant pairs $(b, c)$.
- **Scenario-Level Test (Cluster Adjustment)**: Exact Wilcoxon signed-rank test across paired failure scenario sensitivities, treating the scenario (not the window) as the primary sampling unit.

---

## 7. Current Execution Blocker and Protocol Status

### Protocol Status: **FROZEN & PRE-REGISTERED**
The protocol above is formally frozen in the repository.

### Execution Blocker:
Direct execution of this protocol is currently **blocked** by:
1. **Zenodo Bandwidth Throttling**: The raw `AnoMod.zip` archive is $201.9\text{ MB}$, and unauthenticated transfer via Zenodo's production endpoint is throttled to $\approx 5.38\text{ KB/s}$, requiring $>10.4\text{ hours}$ of download time.
2. **Infrastructure Requirements**: Downstream TrainTicket chaos execution requires a live 40-container Kubernetes deployment.

In accordance with scientific reporting rules, AegisOps does **not** simulate or fabricate synthetic proxy data to mimic AnoMod. This protocol will be executed when the full dataset archive has been mirrored or transferred in an offline batch workflow.

---

## 8. Protocol Amendment Log

### Amendment v1.1.0 (Ratified October 2026)
**Audit Reference**: [`research/audits/STATISTICAL_INTEGRITY_AND_INGESTION_PREFLIGHT.md`](file:///c:/DL_PROJECT/research/audits/STATISTICAL_INTEGRITY_AND_INGESTION_PREFLIGHT.md)  
**Status**: **FROZEN & RATIFIED PRIOR TO TEST SET INGESTION**

1. **Dimension 3 (Disk Utilization vs Throughput)**: Upstream Prometheus metric `container_fs_writes_bytes_total` measures disk write throughput, not capacity saturation. Under Amendment v1.1.0, Dimension 3 strictly maps to true disk capacity utilization (`(container_fs_usage_bytes / container_fs_limit_bytes) * 100` or host `system_disk_usage_percent.csv` in $[0.0, 100.0]\%$). Write throughput is relegated to secondary sensitivity analysis.
2. **Dimension 4 (Latency Unit Scaling)**: Upstream Prometheus response times are recorded in raw seconds. Amendment v1.1.0 mandates multiplying raw seconds by $1000.0$ to produce `latency_ms`, aligning with AegisOps' model input calibration.
3. **Dimension 5 (Error Rate Representation)**: Upstream error rates recorded as decimal fractions ($[0.0, 1.0]$) must be multiplied by $100.0$ to yield `error_rate_pct` in $[0.0, 100.0]\%$. Error rate strictly measures HTTP 5xx server errors / total requests.
4. **Sampling & Resampling Strategy**: Primary evaluation will evaluate native 15-second observation steps ($W = 8$ steps for 120-second sliding horizon). Linear interpolation to 5-second steps ($W = 24$) is retained as an explicit sensitivity analysis.
5. **Host vs Service Attribution Boundary**: Node-level metrics (Dimensions 1–3) reflect the aggregate container environment, whereas latency and error metrics (Dimensions 4–5) reflect client-facing microservices. The evaluation framework explicitly documents that host-level resource stress does not uniquely localize root cause to an individual service without distributed tracing or container attribution.
6. **Leakage-Free Calibration**: Normal baseline calibration windows will be drawn exclusively from the initial nominal run period prior to fault injection start times ($t < t_{\text{fault}}$). No fault-window telemetry will be exposed to threshold calibration.
