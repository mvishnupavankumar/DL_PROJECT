# AegisOps: Phase 9 External Validation Readiness and Execution Plan

**Audit Gate**: Phase 9 Readiness & Dataset Ingestion Gate  
**Audit File**: `research/audits/PHASE9_EXTERNAL_VALIDATION_READINESS.md`  
**Git Baseline Commit**: `d277c1df3c2599ddecdf5f0bb761c99718499667` (Branch: `main`)  
**Audit Date**: October 2026  
**Auditor**: Senior Research Scientist, Reproducibility Auditor & Methodology Reviewer  

---

## 1. Executive Summary & Readiness Objective

The objective of Phase 9 is to bridge the synthetic-to-production domain gap by executing the frozen external evaluation protocol against the **AnoMod** public benchmark.

In Phase 8:
- Candidate feasibility was established and AnoMod was selected over TrainTicket.
- The external evaluation protocol was pre-registered and frozen in [`research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md).
- Direct single-stream transfer was blocked due to Zenodo traffic rate-limiting ($\approx 5.38\text{ KB/s}$, requiring $>10.4\text{ hours}$).

This document establishes:
1. Formal validation of external dataset feasibility and feature derivation.
2. The standardized 6-stage external validation lifecycle.
3. An ordered, resumable, integrity-checked execution plan for obtaining and parsing AnoMod without risking partial-archive corruption or premature execution.

---

## 2. External Dataset Feasibility and Feature Derivation Validation

### 2.1 Official Dataset Provenance
- **Dataset Title**: AnoMod: A Dataset for Anomaly Detection and Root Cause Analysis in Microservice Systems
- **Authors**: Ke Ping, Hamza Bin Mazhar, Yuqing Wang, Ying Song, Mika V. Mäntylä (University of Oulu)
- **Publication**: Proceedings of the 23rd IEEE/ACM International Conference on Mining Software Repositories (MSR '26), pp. 677–681
- **Archive URL**: `https://zenodo.org/records/18342898/files/AnoMod.zip`
- **Permanent DOI**: `10.5281/zenodo.18342898`
- **License**: Creative Commons Attribution 4.0 International (CC-BY-4.0)
- **Archive File Size**: `201,917,396` bytes ($\approx 192.56\text{ MiB} \approx 201.9\text{ MB}$)
- **Disk Space Precondition**: Audited on Drive `C:`: **938.69 GB free** (exceeds required 800 MB footprint by $>1,100\times$).

---

### 2.2 Telemetry Modalities and 5-Dimensional Feature Derivation
AnoMod packages five synchronized modalities: Prometheus Metrics, Application Logs, Jaeger Distributed Traces, Client API Responses, and Code Coverage. 

To evaluate AegisOps' 5D multivariate pipeline ($\mathbf{x}_t \in \mathbb{R}^5$), features are derived directly from the API Gateway / Frontend Entrypoint service (`nginx-web-server` for SocialNetwork; `ts-ui-dashboard` for TrainTicket) and client API logs:

| AegisOps Feature | Required Dimension | AnoMod Modality & Raw Field | Derivation & Calculation Method | Unit / Scale |
| :--- | :--- | :--- | :--- | :--- |
| **$x_t^{(1)}$: `cpu_pct`** | Node/Container CPU | Prometheus `metrics/*.csv`:<br>`container_cpu_usage_seconds_total` | Per-second rate over 1-minute rolling window: `rate(cpu_usage[1m]) * 100` | Percentage $[0.0, 100.0]$ |
| **$x_t^{(2)}$: `memory_pct`** | Container RAM | Prometheus `metrics/*.csv`:<br>`container_memory_working_set_bytes` | Working set divided by container spec limit: `(mem_working_set / spec_limit) * 100` | Percentage $[0.0, 100.0]$ |
| **$x_t^{(3)}$: `disk_pct`** | Storage I/O | Prometheus `metrics/*.csv`:<br>`container_fs_writes_bytes_total` | Write throughput rate normalized against nominal maximum observed during warmup | Normalized $[0.0, 100.0]$ |
| **$x_t^{(4)}$: `latency_ms`** | Request Latency | Client API `api_responses/response_time.log` | P95 request latency observed by client test runner over the time window | Milliseconds ($\mathbb{R}_{\ge 0}$) |
| **$x_t^{(5)}$: `error_rate_pct`** | Service Errors | Client API `api_responses/*.log` | Fraction of HTTP response status codes $\ge 400$ during the window | Percentage $[0.0, 1.0]$ |

---

### 2.3 Sampling Intervals, Temporal Dilation, and Missingness
1. **Sampling Frequency Alignment**:
   - AnoMod Prometheus metrics are scraped at $\Delta t = 15\text{ seconds}$. Client API logs are timestamped continuously at millisecond resolution.
   - AegisOps was calibrated with sequence length $W = 24$ at $\Delta t = 5\text{ s}$ ($120\text{ s}$ horizon).
   - In accordance with the frozen protocol, telemetry will be aligned via **linear interpolation resampling to $\Delta t = 5\text{ seconds}$**, preserving the identical temporal input dimension ($\mathbf{X}_i \in \mathbb{R}^{24 \times 5}$) of the frozen PyTorch model.
2. **Missingness Handling**:
   - If a container metric is temporarily absent during a restart or crash, forward-fill is permitted up to 2 intervals ($30\text{ s}$); sequences with $>30\text{ s}$ missing contiguous metrics are excluded in accordance with Section 3.3 of the protocol.
3. **Nominal Warmup and Zero Data Leakage**:
   - Each AnoMod scenario begins with an undisturbed nominal steady-state phase ($\ge 15\text{ minutes}$, typically $60\text{ steps}$ at 15s).
   - Normalization bounds ($\mathbf{x}_{\min}^{\text{ext}}, \mathbf{x}_{\max}^{\text{ext}}$) and calibration thresholds ($\tau^{\text{ext}}$) must be calculated **exclusively on $t < t_{\text{fault}}$**. Zero test or fault-injection samples may be exposed to calibration.

---

### 2.4 Statistical Unit of Analysis & Treatment of Dependent Windows
- In continuous time-series evaluations, sliding windows within an ongoing incident are autocorrelated.
- To prevent pseudo-replication:
  1. Window-level sensitivity will be reported with explicit acknowledgement of within-episode temporal dependence.
  2. The primary statistical hypothesis test ($H_0: p_{\text{LSTM}}^{\text{ext}} = p_{\text{IF}}^{\text{ext}}$) will be evaluated using the **scenario-level exact Wilcoxon signed-rank test** across distinct, independent failure scenarios ($N_{\text{scenarios}} \ge 20$).

---

### 2.5 Independence of RCA Ground Truth and Evaluation Rubric
- Root-cause ground truth in AnoMod is established strictly by the ChaosBlade / ChaosMesh injection operator configurations (e.g., target container `user-service`, fault type `cpu_contention`).
- The LLM diagnostic prompt will receive strictly parsed runtime logs, traces, and neural reconstruction error attribution vectors without scenario IDs, ground-truth labels, or target hints.
- Rubric scoring will evaluate semantic correspondence against the operator's ground-truth tuple `(fault_type, target_service)` without circular prompt leakage.

---

## 3. The 6-Stage External Benchmark Validation Lifecycle

To prevent premature claims of completion, the external evaluation process is partitioned into six distinct, verifiable stages:

```
+---------------------------------------------------------------------------------------------------------+
|                                6-STAGE EXTERNAL VALIDATION LIFECYCLE                                    |
+---------------------------------------------------------------------------------------------------------+
| Stage 1: Protocol Pre-Registration & Freezing                     [STATUS: VERIFIED COMPLETE]           |
|          - Formal hypotheses, feature mappings, inclusion rules frozen in EXTERNAL_EVALUATION_PROTOCOL.md  |
+---------------------------------------------------------------------------------------------------------+
| Stage 2: Resumable Dataset Download & Integrity Verification      [STATUS: PENDING - PHASE 9 READY]     |
|          - Resumable transfer of AnoMod.zip; SHA-256 hash verification against Zenodo metadata.         |
+---------------------------------------------------------------------------------------------------------+
| Stage 3: Archive Extraction & Schema Feature Validation           [STATUS: PENDING - POST STAGE 2]      |
|          - Unpack to data/external/anomod/raw/; verify 5 modalities; construct 5D telemetry matrix.     |
+---------------------------------------------------------------------------------------------------------+
| Stage 4: Execution of Frozen Anomaly Detection & RCA Protocol      [STATUS: PENDING - POST STAGE 3]      |
|          - Run frozen LSTM AE, Isolation Forest, and Rules baselines; execute multi-agent diagnostic run.|
+---------------------------------------------------------------------------------------------------------+
| Stage 5: Independent Verification of Predictions & Statistics     [STATUS: PENDING - POST STAGE 4]      |
|          - Machine-readable raw predictions, confusion matrices, and exact McNemar/Wilcoxon tests.      |
+---------------------------------------------------------------------------------------------------------+
| Stage 6: Manuscript Synthesis & Final Evidence Gate Pass          [STATUS: PENDING - POST STAGE 5]      |
|          - Publish Experiment D in paper; reconcile evidence matrix; evaluate camera-ready readiness.   |
+---------------------------------------------------------------------------------------------------------+
```

---

## 4. Ordered Execution Plan for Next Executable Action

### 4.1 Step 1: Deploy Resumable Ingestion Script
Create [`research/scripts/ingest_anomod.py`](file:///c:/DL_PROJECT/research/scripts/ingest_anomod.py) implementing:
- **Target URL**: `https://zenodo.org/records/18342898/files/AnoMod.zip`
- **Destination Path**: `data/external/anomod/AnoMod.zip`
- **Partial Download Handling**: Uses HTTP `Range: bytes=START-` headers to resume broken downloads.
- **Backoff & Retry Policy**: Max 20 retries with exponential backoff ($2\text{s}, 4\text{s}, 8\text{s}, \dots, 60\text{s}$) upon connection reset or rate-limit responses (HTTP 429).
- **Chunk Size**: $64\text{ KB}$ chunk streaming with progress tracking.

### 4.2 Step 2: Cryptographic Archive Verification
- Compute SHA-256 and MD5 of downloaded `AnoMod.zip`.
- Query Zenodo API (`https://zenodo.org/api/records/18342898`) to match remote checksum.
- **Stop Condition 1**: If checksum fails after completed transfer, delete corrupt archive, log error, and abort.

### 4.3 Step 3: Safe Extraction and Provenance Recording
- Extract `AnoMod.zip` into `data/external/anomod/raw/`.
- Verify presence of `SocialNetwork/` and `TrainTicket/` scenario trees.
- Generate `data/external/anomod/MANIFEST.json` containing SHA-256 hashes of all extracted scenario CSVs and logs.
- **Stop Condition 2**: If extracted directory lacks Prometheus `metrics/` or client `api_responses/` logs, abort and document schema blocker.

### 4.4 Step 4: Execute Feature Extraction and Telemetry Parsing
- Execute `research/experiments/parse_anomod_telemetry.py` to produce standardized 5D telemetry matrices and ground-truth scenario annotations in `data/external/anomod/processed/`.
- Validate that nominal warmup contains $\ge 60$ contiguous 15s steps without missing metrics.

### 4.5 Step 5: Execute Frozen Experiment D Protocol
- Execute `research/experiments/run_experiment_d.py` adhering strictly to [`EXTERNAL_EVALUATION_PROTOCOL.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md).
- Output:
  - `research/raw/external_anomod_predictions.csv`
  - `research/raw/external_anomod_metrics.csv`
  - `research/figures/external_anomod_comparison.png`

---

## 5. Formal Phase 9 Readiness Verdict

- **Readiness Status**: **READY FOR RESUMABLE DATASET INGESTION (STAGE 2)**.
- **Prerequisites Satisfied**:
  - [x] Disk space verified ($>938\text{ GB}$ available).
  - [x] Official dataset provenance, DOI, and license confirmed.
  - [x] 5D feature derivation mathematically specified.
  - [x] Evaluation protocol frozen prior to test ingestion.
  - [x] Resumable transfer architecture designed.
- **Immediate Next Executable Action**: Author and launch `research/scripts/ingest_anomod.py` to initiate the background resumable download of `AnoMod.zip`.

---

## 6. Epistemic Evidence Classification

To ensure scientific defensibility, all determinations in this readiness review are classified into four distinct evidentiary tiers:

### 6.1 Verified Facts (Directly inspected and confirmed in this session)
1. **Zenodo Publication Record**: Verified that AnoMod is published under Zenodo record `18342898`, DOI `10.5281/zenodo.18342898`, CC-BY-4.0 license, with official archive name `AnoMod.zip` (201,917,396 bytes).
2. **Local Storage Capacity**: Verified via `Get-PSDrive C` that local disk has 938.69 GB free space, exceeding the archive footprint by $>1,100\times$.
3. **Frozen Pre-Registration**: Verified that `EXTERNAL_EVALUATION_PROTOCOL.md` (hash `e5a31a98...`) was authored and frozen prior to test-set ingestion.
4. **Bandwidth Throttling Reality**: Verified via empirical HTTP probe that unauthenticated downloads are capped at $\approx 5.38\text{ KB/s}$, requiring resumable transfer logic rather than monolithic downloads.

### 6.2 Inherited Claims (Accepted from published papers and prior audit phases)
1. **AnoMod Multimodal Synchronization**: Accepted from Ping et al. (MSR 2026) that Prometheus metrics, Jaeger traces, application logs, and client API logs are synchronized via universal NTP timestamps across scenarios.
2. **Chaos Injection Fidelity**: Accepted from AnoMod documentation that ChaosMesh/ChaosBlade injections were isolated per scenario run with full cleanup between iterations.

### 6.3 Inferences (Deductions supported by evidence but requiring external confirmation)
1. **Resampling Fidelity**: Inferred that linear interpolation from 15s to 5s preserves sufficient gradient structure for the frozen LSTM Autoencoder without introducing artificial high-frequency artifacts.
2. **Entrypoint Representativeness**: Inferred that client-facing API gateway telemetry captures end-to-end service degradation across downstream container failures.

### 6.4 Unresolved Questions (Active blockers and knowledge boundaries)
1. **Transfer Duration & Completion**: Will Zenodo sustain the multi-hour transfer without dropping HTTP keep-alive connections or hitting quota ceilings?
2. **Post-Extraction Schema Alignment**: Will all scenario directories contain complete Prometheus CSV columns matching the theoretical schema mapping, or are some columns missing across specific chaos runs?
3. **External Model Generalization**: Does the frozen synthetic LSTM checkpoint require domain fine-tuning on AnoMod warmup data, or does zero-shot inference succeed out-of-the-box?
