# AegisOps: Public Benchmark Feasibility and Candidate Assessment

**Audit Gate**: Phase 8 Public Benchmark Assessment  
**Audit Directory**: `research/audits/phase8_external_validation/`  
**Git Baseline Commit**: `d277c1df3c2599ddecdf5f0bb761c99718499667` (Branch: `main`)  
**Target Candidates**: **AnoMod** (MSR 2026 / Zenodo) vs. **TrainTicket** (FudanSELab / Open-Source Repositories)  
**Date**: October 2026  
**Status**: **FEASIBILITY AUDIT COMPLETE; CANDIDATE METHODOLOGICAL FIT DETERMINED**  

---

## 1. Executive Summary & Assessment Mandate

The primary limitation documented in the AegisOps Phase 7 manuscript is the **synthetic-to-production domain gap**: all experimental evaluations in Experiment A and Experiment B relied upon synthetic telemetry simulated via mathematical sinusoidal baselines and deterministic fault ramps. 

To evaluate whether AegisOps generalizes to external microservice telemetry, this audit assesses two prominent public benchmark datasets:
1. **AnoMod** (Ping et al., MSR 2026; Zenodo DOI: `10.5281/zenodo.18342898`): A multimodal anomaly dataset specifically built for anomaly detection and root-cause analysis across two distributed microservice systems.
2. **TrainTicket** (FudanSELab / academic research forks): A widely-used open-source railway ticketing benchmark application comprising 40+ microservices with chaos engineering injection frameworks.

In accordance with strict audit rules, this feasibility review evaluates each candidate across eight standardized operational and methodological criteria before authorizing external execution.

---

## 2. In-Depth Comparative Candidate Assessment

### 2.1 Candidate 1: AnoMod (MSR 2026)

| Assessment Criterion | Technical Details & Empirical Findings |
| :--- | :--- |
| **1. Official Source & License** | - **Primary Publication**: Ke Ping, Hamza Bin Mazhar, Yuqing Wang, Ying Song, Mika V. Mäntylä (2026). *AnoMod: A Dataset for Anomaly Detection and Root Cause Analysis in Microservice Systems*. In Proceedings of the 23rd IEEE/ACM International Conference on Mining Software Repositories (MSR '26).<br>- **Repository**: `https://github.com/EvoTestOps/AnoMod`<br>- **Archive & DOI**: Zenodo record `18342898` (DOI: `10.5281/zenodo.18342898`).<br>- **License**: Creative Commons Attribution 4.0 International (CC-BY-4.0). |
| **2. Availability & Download Requirements** | - **Archive File**: `AnoMod.zip` on Zenodo (`201,917,396` bytes $\approx 192.5\text{ MiB}$).<br>- **Bandwidth & Access**: Zenodo applies aggressive bot protection and throttles unauthenticated downloads via `curl.exe` to $\approx 5.38\text{ KB/s}$ (empirically tested via HTTP range requests). Full archive transfer requires an estimated $>10\text{ hours}$ of sustained transfer, with planned infrastructure maintenance outages scheduled.<br>- **Pre-packaged Availability**: Dataset is not pre-packaged in the local repository workspace. |
| **3. Telemetry Modalities & Feature Fields** | - **Modalities**: 5 synchronized modalities: (1) Prometheus Metrics, (2) Application Logs, (3) Jaeger/SkyWalking Traces, (4) Client API responses, (5) Code Coverage Reports (gcov/JaCoCo).<br>- **Metrics Tracked**: Container-level Prometheus time-series: `container_cpu_usage_seconds_total`, `container_memory_working_set_bytes`, network transmit/receive bytes, disk read/write bytes, and HTTP request durations. |
| **4. Ground-Truth Incident Labels & Scenarios** | - **Failure Classes**: 4 distinct categories: Performance-level (CPU contention, memory leaks, packet loss), Service-level (service crashes, container stops), Database-level (cache misses, slow queries, connection starvation), and Code-level (artificial delays, injected exceptions).<br>- **Scenarios**: Systematic injections across 21 services in SocialNetwork and 41 services in TrainTicket using ChaosMesh/ChaosBlade configurations. Injections are isolated into per-scenario folders with clean baseline resets between runs. |
| **5. Sampling Frequency & Temporal Structure** | - **Sampling Interval**: Telemetry is sampled at standard Prometheus intervals ($\Delta t \approx 15\text{ seconds}$).<br>- **Temporal Structure**: Each scenario run features a baseline nominal phase followed by an active anomaly injection window. Missing data occurs during container restarts. |
| **6. Compatibility with AegisOps Feature Pipeline** | - **Feature Dimensionality**: AegisOps expects a single 5-dimensional vector $\mathbf{x}_t = [\text{cpu}, \text{mem}, \text{disk}, \text{latency}, \text{error}]^\top \in \mathbb{R}^5$ representing a unified service observation.<br>- **Dimensionality Mismatch**: AnoMod provides hundreds of metric time-series across dozens of discrete containers. Ingestion requires an aggregation step (e.g., isolating the API gateway / frontend service or computing cluster-wide mean/max aggregations).<br>- **Sampling Rate Mismatch**: AegisOps was calibrated with sequence length $W = 24$ at $\Delta t = 5\text{ s}$ ($120\text{ s}$ horizon). In AnoMod, 24 steps at $\Delta t = 15\text{ s}$ represents $360\text{ s}$, creating a $3\times$ temporal dilation domain shift. |
| **7. Preprocessing & Leakage Risks** | - **Normalization**: Ingestion requires domain-specific min-max normalization. Using AegisOps' synthetic mean/std parameters (`models/lstm_autoencoder.json`) on raw Prometheus container metrics will induce immediate out-of-distribution reconstruction loss.<br>- **Leakage Prevention**: Normalization parameters must be calculated strictly on AnoMod's nominal warmup sequences, preserving test set isolation. |
| **8. Research Questions Evaluated** | - **RQ1 (Detection Efficacy)**: YES (evaluates whether temporal models detect realistic container degradation).<br>- **RQ2 (Combined Gating)**: YES (evaluates rules vs. neural detection on multi-service telemetry).<br>- **RQ3 (Multi-Agent RCA)**: YES (rich logs and traces allow testing multi-agent root-cause diagnosis).<br>- **RQ4 (Remediation Safety)**: NO (AnoMod is a static observational dataset; it does not provide a live loopback execution endpoint with an approval barrier). |

---

### 2.2 Candidate 2: TrainTicket (FudanSELab & Academic Forks)

| Assessment Criterion | Technical Details & Empirical Findings |
| :--- | :--- |
| **1. Official Source & License** | - **Primary Upstream**: FudanSELab/train-ticket (`https://github.com/FudanSELab/train-ticket`).<br>- **License**: Apache License 2.0.<br>- **Research Forks**: `lizeyan/train-ticket` (ESEC/FSE 2022 fault localization benchmark), and various fragmented Zenodo archives. |
| **2. Availability & Download Requirements** | - **Deployment Complexity**: Upstream TrainTicket is an executable microservice application (41 microservices across Java, Node.js, Python, Go) requiring a multi-node Kubernetes cluster, Prometheus, Jaeger, and load generators.<br>- **Pre-collected Datasets**: Academic forks publish CSV telemetry dumps, but these are often unmaintained, lack standardized manifests, or have broken download links. |
| **3. Telemetry Modalities & Feature Fields** | - **Modalities**: Prometheus metrics, Jaeger traces, and Logback container logs.<br>- **Metrics Tracked**: Host and container CPU/memory, JVM garbage collection pauses, HTTP request latencies, and TCP socket counts. |
| **4. Ground-Truth Incident Labels & Scenarios** | - **Failure Classes**: Chaos engineering fault scripts (CPU hog, network delay, packet drop, process kill).<br>- **Labels**: Fault injection start/end timestamps recorded in chaos operator logs. |
| **5. Sampling Frequency & Temporal Structure** | - **Sampling Interval**: Configurable via Prometheus scrape intervals (typically 10s to 30s).<br>- **Temporal Structure**: Long-running continuous execution traces with interleaved background traffic from JMeter scripts. |
| **6. Compatibility with AegisOps Feature Pipeline** | - **Dimensionality Mismatch**: Requires manual extraction and mapping of entrypoint service metrics (`ts-ui-dashboard` or API Gateway) to construct an analogous 5-variable vector.<br>- **Temporal Horizon**: Mismatched sliding window dynamics due to non-standardized sampling frequencies. |
| **7. Preprocessing & Leakage Risks** | - High risk of missing values during container crashes. Uncurated research forks frequently omit explicit test/train partition splits, risking label contamination during threshold calibration. |
| **8. Research Questions Evaluated** | - Can evaluate RQ1 and RQ3 if fully parsed; cannot evaluate RQ4 (no execution gate integration). |

---

## 3. Comparative Summary and Candidate Selection

| Dimension | AnoMod (MSR 2026) | TrainTicket (FudanSELab / Forks) | Preferred Candidate | Methodological Rationale |
| :--- | :---: | :---: | :---: | :--- |
| **Standardization & Curation** | High (Zenodo DOI, MSR '26 peer-reviewed) | Moderate / Fragmented across forks | **AnoMod** | Formally documented, immutable DOI with standardized folders per failure scenario. |
| **Licensing** | CC-BY-4.0 (Open Research) | Apache 2.0 | **AnoMod** | Clear open-science redistribution license. |
| **Modalities Covered** | 5 synchronized modalities (Metrics, Logs, Traces, API, Coverage) | 3 modalities (Metrics, Logs, Traces) | **AnoMod** | Uniquely includes client API response observations (status codes, latencies) matching AegisOps' synthetic probe structure. |
| **Feature Mapping Feasibility** | Direct mapping from API responses + gateway container metrics | Requires parsing complex distributed JVM metrics | **AnoMod** | API response logs directly map to AegisOps' `latency_ms` and `error_rate_pct`. |
| **Execution Feasibility** | Static benchmark evaluation | Requires spinning up a 40-container K8s cluster | **AnoMod** | Evaluates observational data without massive infrastructure deployment. |

### Final Selection Verdict:
**AnoMod (MSR 2026, Zenodo DOI: `10.5281/zenodo.18342898`) is selected as the primary public benchmark for external validation.** It provides the highest methodological rigor, standardized scenario folders, and synchronized API/metric telemetry.

---

## 4. Current Operational Blockers and Constraints

While AnoMod is the methodologically superior candidate, an empirical inspection revealed two significant operational blockers that must be transparently documented:

1. **Bandwidth Throttling and Network Transfer Blocker**:
   - The complete AnoMod archive (`AnoMod.zip`) is 201.9 MB (201,917,396 bytes).
   - Zenodo's production endpoints enforce automated traffic rate-limiting, restricting download throughput via `curl.exe` to $\approx 5.38\text{ KB/s}$. 
   - At this rate, downloading the full 201.9 MB archive would require **$>10.4\text{ hours}$** of uninterrupted transfer.
   - Furthermore, Zenodo has posted an active notice of planned infrastructure maintenance on October 13th (06:00 UTC), posing high disconnection risks.
2. **Architectural Domain Shift (Multi-Service to Single-Host Model)**:
   - The frozen AegisOps PyTorch LSTM Autoencoder (`models/lstm_autoencoder.pt`) was trained strictly on 5 normalized host metrics sampled at 5-second intervals.
   - Feeding raw multi-container Prometheus metrics into the frozen model without domain-specific recalibration of normalization scalars would cause 100% false alarms due to feature magnitude shifts.

---

## 5. Feasibility Verdict & Recommended Path Forward

- **Public Benchmark Feasibility**: **ESTABLISHED & DOCUMENTED**. AnoMod is formally selected as the optimal public benchmark.
- **Immediate Execution Status**: **BLOCKED BY EXTERNAL ARCHIVE TRANSFER CONSTRAINTS (>10 HOUR DOWNLOAD HORIZON)**.
- **Methodological Safeguard**: In accordance with user instructions (*"If external validation is blocked, document the exact reason and required inputs; preserve the current manuscript as a bounded experimental report; do not manufacture a successful validation result"*), we will:
  1. Author a fully frozen, pre-registered **External Evaluation Protocol** (`EXTERNAL_EVALUATION_PROTOCOL.md`) defining the exact feature mapping, calibration rules, and hypothesis tests.
  2. Preserve the active manuscript as a bounded experimental study on synthetic telemetry.
  3. Preclude artificial or simulated "external validation" results.
