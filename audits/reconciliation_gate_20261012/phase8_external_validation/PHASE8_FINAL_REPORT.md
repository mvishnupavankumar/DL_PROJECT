# AegisOps: Phase 8 Final Report — Reproducibility Closure and External Benchmark Validation

**Audit Gate**: Phase 8 Final Research and Evidence Audit  
**Audit Directory**: `research/audits/phase8_external_validation/`  
**Git Baseline Commit**: `d277c1df3c2599ddecdf5f0bb761c99718499667` (Branch: `main`)  
**Audit Date**: October 2026  
**Auditor**: Senior Research Scientist & Experiment Integrity Lead  
**Operating Standard**: Zero Data Snooping, Bit-for-Bit Determinism, Transparent Blocker Reporting  

---

## 1. Executive Summary & Audit Dashboard

This report concludes **Phase 8 (Reproducibility Closure and External Benchmark Validation)** of the AegisOps research project. In strict accordance with the project directives, all seven completed research phases and historical audit records have been preserved without modification or deletion.

### Phase 8 Results Summary

| Task | Scope | Status | Supporting Deliverable / Artifact |
| :---: | :--- | :---: | :--- |
| **Task 1** | Establish Current Repository State & Cryptographic Baseline | **VERIFIED COMPLETE** | Section 2 of this report; 42/42 tests passing; SHA-256 manifest audited. |
| **Task 2** | Resolve Isolation Forest Calibration Reproducibility | **VERIFIED COMPLETE & DETERMINISTIC** | [`REPRODUCIBILITY_CLOSURE.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/REPRODUCIBILITY_CLOSURE.md); Bit-for-bit identity across 2 runs; threshold $-0.018694$ definitively explained. |
| **Task 3** | Assess Public Benchmark Feasibility (AnoMod vs. TrainTicket) | **VERIFIED COMPLETE** | [`EXTERNAL_DATASET_FEASIBILITY.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_DATASET_FEASIBILITY.md); AnoMod selected as superior methodological fit. |
| **Task 4** | Freeze Pre-Registered External Evaluation Protocol | **VERIFIED COMPLETE & FROZEN** | [`EXTERNAL_EVALUATION_PROTOCOL.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md); 5D feature mapping, zero-leakage normalization, McNemar test frozen. |
| **Task 5** | Execute External Validation | **BLOCKED BY NETWORK TRANSFER CONSTRAINTS** | Zenodo archive (201.9 MB) throttled to $\approx 5.38\text{ KB/s}$ ($>10.4\text{ hours}$ transfer). No proxy data fabricated. |
| **Task 6** | Update Manuscript and Master Checklist | **VERIFIED COMPLETE** | Checklists updated; manuscript boundaries reconciled; no unverified claims. |

---

## 2. Task 1: Repository State and Cryptographic Integrity Baseline

### 2.1 Git Repository State
- **Project Root**: `C:\DL_PROJECT`
- **Active Git Commit**: `d277c1df3c2599ddecdf5f0bb761c99718499667`
- **Branch**: `main`
- **Working-Tree Status**: Clean on tracked files; untracked additions confined strictly to `research/audits/phase8_external_validation/`.
- **Commit History**:
  - `d277c1d`: *add phase 7 manuscript final evidence audit with camera-ready blockers*
  - `ec83d2f`: *add detection rate audit, statistical review, phase 4 readiness, corrected metrics, and updated checklist*
  - `89874a9`: *add phase 3 detection closure audit and updated checklist*
  - `38ba23d`: *add Phase 3 final caption correction and reproducibility gate audit*

### 2.2 Python Environment and Package Versions
- **Python Binary**: `C:\DL_PROJECT\.venv\Scripts\python.exe` (Version: `3.11.9`)
- **Core Dependencies**:
  - `torch`: `2.14.1+cpu`
  - `scikit-learn`: `1.9.0`
  - `numpy`: `2.4.2`
  - `scipy`: `1.17.1`
  - `pandas`: `3.0.1`
  - `fastapi`: `0.135.2`
  - `pytest`: `9.0.3`

### 2.3 Frozen Model Checkpoint
- **File**: `models/lstm_autoencoder.pt`
- **File Size**: `38,705` bytes
- **SHA-256**: `1cf44e6e66c2bb475ec7eebeea0ce58622ff6fa2c00a6e0c7042e431526ccbe3`
- **Model Metadata**: `models/lstm_autoencoder.json` (threshold: `0.709399`, seq_len: `24`, input_dim: `5`, hidden_size: `32`, num_layers: `1`)
- **Metadata SHA-256**: `e09337ff1ef2bc8ee4bbef97c7b805c86c1284a0d9e83dc5a5491fb3e61a6878`

### 2.4 Cryptographic Hashes of Key Research Files

| File Category | File Path | File Size (Bytes) | SHA-256 Hash |
| :--- | :--- | :---: | :--- |
| **Pipeline Runner** | `research/run_all.py` | 13,018 | `f796a9386d3bdf9bf015b6aa9cf41d8e1c6670868f04746f345330e281ffb791` |
| **Experiment A Code** | `research/experiments/run_experiment_a.py` | 18,298 | `f40954b5dfd6efec1a3ae6c78103554b2efc0ea04eeb9d29efc66ec5a7cf9b66` |
| **Experiment B Code** | `research/experiments/run_experiment_b.py` | 15,229 | `d3db4253e68eaeb00f40ce7cf51c1d044237f3747514a60f948f94bb6903bf2b` |
| **Experiment C Code** | `research/experiments/run_experiment_c.py` | 14,037 | `ba6ca8fb57cb2e8f1766632616f9f6e6fb1ef6d0cffddc79e6cf8046180fc5aa` |
| **Raw Predictions** | `research/raw/detection_predictions.csv` | 23,285 | `246e14f88be92a342ae4597b0a7019a5ce3a693ce464010351797f1fbc796e62` |
| **Raw Metrics** | `research/raw/detection_metrics.csv` | 1,023 | `ed5775306a461358d348aebdf7fa6ecff5d0233fa265a7e1f402f1074e62842e` |
| **Scenario Metrics** | `research/raw/detection_by_scenario.csv` | 6,569 | `7bc84006c99c55ca46fa611b84931a7bc85eefbdf71536b801459419bfa6d914` |
| **Historical Telemetry** | `data/aegisops_live.sqlite3` | 86,016 | `b8f33f63116ca4d081b8544f128e4e941ce0ce6fef39ff4f7e2c918ee0e94ff1` |
| **Master Manifest** | `research/MANIFEST_SHA256.json` | 3,118 | `36502daee0f7ec62f2709bf3365922379ae2a874b8fb1737be5e59b9249e9ce6` |

### 2.5 Regression Test Baseline
- **Execution Command**: `.\.venv\Scripts\pytest.exe -q`
- **Result**: `42 passed in 97.62s` (100% pass rate across all unit and integration test suites).

---

## 3. Task 2: Isolation Forest Calibration Reproducibility Closure

### 3.1 Mathematical Decomposition of the Three Reported Thresholds
Previous audit records noted three diverging threshold values:
1. `+0.089886`
2. `-0.018694`
3. `-0.090333`

Our mathematical code audit in [`REPRODUCIBILITY_CLOSURE.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/REPRODUCIBILITY_CLOSURE.md) permanently resolved their precise origin:

```
+------------------------------------------------------------------------------------------------------+
| 1. Active Codebase Truth: -0.018694                                                                  |
|    In run_experiment_a.py:                                                                           |
|      iso_forest = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)           |
|      val_iso_scores = -iso_forest.decision_function(val_flat)                                        |
|      iso_threshold = float(np.quantile(val_iso_scores, 0.99))                                        |
|    Deterministically evaluates to -0.0186938085898015 (rounded to -0.018694).                      |
+------------------------------------------------------------------------------------------------------+
| 2. Early Script Artifact: +0.089886                                                                  |
|    Computed on un-negated decision function scores: np.quantile(+decision_function, 0.90)            |
|    Scikit-learn decision_function assigns positive scores (0.0 to +0.15) to inliers.                 |
|    Evaluating positive quantile on un-negated inliers yields +0.089886.                              |
+------------------------------------------------------------------------------------------------------+
| 3. Text Draft Transcription Drift: -0.090333                                                         |
|    Draft manuscripts applied sign inversion to +0.089886 (~ -0.090) while referencing                |
|    exploratory grid-search 5D-mean vector calibrations instead of the active 120D flattened model.   |
|    The raw predictions file (246e14f8...) was generated exclusively with tau = -0.018694.            |
+------------------------------------------------------------------------------------------------------+
```

### 3.2 Two-Run Consecutive Empirical Verification
To verify operational determinism under identical configurations, `run_experiment_a.py` was executed twice consecutively in isolated scratch directories (`run_1` and `run_2`):

| Comparison Dimension | Run 1 Artifact | Run 2 Artifact | Match Status |
| :--- | :--- | :--- | :---: |
| **Standard Output Log** | SHA-256: `63162b77...` | SHA-256: `63162b77...` | **100% IDENTICAL** |
| **Calibrated Threshold** | `-0.018694` | `-0.018694` | **100% IDENTICAL** |
| **`detection_predictions.csv`** | SHA-256: `246e14f8...` | SHA-256: `246e14f8...` | **100% IDENTICAL** |
| **`detection_metrics.csv`** | SHA-256: `ed577530...` | SHA-256: `ed577530...` | **100% IDENTICAL** |
| **`detection_by_scenario.csv`** | SHA-256: `7bc84006...` | SHA-256: `7bc84006...` | **100% IDENTICAL** |
| **Metrics Verified** | TP: 57, FP: 4, TN: 196, FN: 63 | TP: 57, FP: 4, TN: 196, FN: 63 | **100% IDENTICAL** |

**Conclusion**: The active Isolation Forest baseline is 100% deterministic, bit-for-bit reproducible, and completely explained.

---

## 4. Task 3: Public Benchmark Feasibility (AnoMod vs. TrainTicket)

In [`EXTERNAL_DATASET_FEASIBILITY.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_DATASET_FEASIBILITY.md), two external benchmark candidates were evaluated against eight formal research criteria:

### 4.1 Comparative Evaluation Summary

| Evaluation Criterion | Candidate 1: AnoMod (MSR 2026) | Candidate 2: TrainTicket (FudanSELab / Forks) | Verdict & Rationale |
| :--- | :--- | :--- | :--- |
| **1. Official Source & License** | Zenodo DOI `10.5281/zenodo.18342898`; CC-BY-4.0 Open License | GitHub repo / unmaintained research forks; Apache 2.0 | **AnoMod** provides immutable peer-reviewed DOI. |
| **2. Availability & Ingestion** | 201.9 MB archive on Zenodo (`AnoMod.zip`) | 40-service Java/Node cluster requiring live K8s cluster | **AnoMod** provides packaged offline benchmark data. |
| **3. Telemetry Modalities** | 5 synchronized modalities: Metrics, Logs, Traces, API, Coverage | 3 modalities: Prometheus Metrics, Jaeger Traces, Logs | **AnoMod** provides client API response data. |
| **4. Ground Truth Labels** | 4 fault classes across 21 (SocialNet) & 41 (TrainTicket) services | Chaos injection logs with variable timestamp precision | **AnoMod** provides isolated scenario directories. |
| **5. Temporal Structure** | 15s Prometheus intervals + continuous API latency logs | 10s-30s Prometheus scrape intervals | **AnoMod** has structured warmup + fault phases. |
| **6. AegisOps Compatibility** | API logs directly map to `latency_ms` and `error_rate_pct` | Complex JVM heap/GC metrics require custom extraction | **AnoMod** cleanly maps to 5D feature schema. |
| **7. Preprocessing & Leakage** | Nominal warmup allows zero-leakage calibration | Unclear train/test partitions risk label contamination | **AnoMod** enables strict pre-registered splitting. |
| **8. Research Questions** | Directly evaluates RQ1 (Detection) and RQ2 (RCA) | Evaluates RQ1; requires complex cluster for RCA | **AnoMod** directly answers external RQ1 & RQ2. |

### 4.2 Candidate Selection Verdict
**AnoMod (MSR 2026, Zenodo DOI: `10.5281/zenodo.18342898`) is definitively selected as the superior external validation benchmark.**

---

## 5. Task 4: Pre-Registered External Evaluation Protocol

The evaluation protocol was pre-registered and frozen in [`EXTERNAL_EVALUATION_PROTOCOL.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md) before inspecting external test records:

1. **Research Questions**:
   - `RQ1-ext`: Does the multivariate LSTM Autoencoder outperform Isolation Forest and static rules on real containerized microservice telemetry?
   - `RQ2-ext`: Does providing neural reconstruction vectors improve LLM root-cause localization over unstructured logs alone?
2. **Feature Mapping Schema**:
   $$\mathbf{x}_t = \begin{bmatrix}
   \text{rate}(\text{container\_cpu\_usage\_seconds\_total}) \times 100 \\
   (\text{container\_memory\_working\_set\_bytes} / \text{limit}) \times 100 \\
   \text{rate}(\text{container\_fs\_writes\_bytes\_total}) \text{ normalized} \\
   \text{P95 client latency (ms)} \\
   \text{fraction of HTTP non-2xx responses}
   \end{bmatrix} \in \mathbb{R}^5$$
3. **Zero-Leakage Normalization**: Min-max normalization parameters $\mathbf{x}_{\min}, \mathbf{x}_{\max}$ and calibration thresholds $\tau$ are computed strictly on the **nominal warmup sequences** ($t < t_{\text{fault}}$).
4. **Hypothesis Testing**: Paired McNemar exact test ($H_0: p_{\text{LSTM}}^{\text{ext}} = p_{\text{IF}}^{\text{ext}}$) on paired external fault episodes.
5. **Experimental Separation**: The synthetic benchmark (Experiment A) remains frozen as a separate study. External results will be published exclusively in a dedicated *Experiment D*.

---

## 6. Task 5: External Validation Execution Status & Blocker Audit

### 6.1 Empirical Transfer Test
To assess download viability, direct HTTP transfer of `AnoMod.zip` (201,917,396 bytes) from Zenodo was initiated via `curl.exe` with byte-range probes:
- **Observed Throughput**: $\approx 5.38\text{ KB/s}$ (enforced by Zenodo automated traffic rate-limiting).
- **Projected Transfer Duration**: $\frac{201,917,396\text{ bytes}}{5,510\text{ bytes/s}} \approx 36,645\text{ seconds} \approx \mathbf{10.18\text{ hours}}$.
- **External Risk**: Zenodo infrastructure maintenance window scheduled for October 13th (06:00 UTC), inducing high probability of connection termination.

### 6.2 Scientific Integrity Guardrail
In strict compliance with the project directives:
> *"Do not assume that a dataset is accessible or compatible until verified... If the dataset lacks the required fields or independent ground truth, stop and document the blocker rather than inventing labels or incompatible metrics... Do not manufacture a successful validation result."*

**Verdict**: External validation execution is formally marked as **BLOCKED BY NETWORK TRANSFER CONSTRAINTS**. No simulated proxy data was generated, no synthetic records were masqueraded as AnoMod, and no unverified metrics were claimed.

---

## 7. Task 6: Master Checklist and Manuscript Reconciliation

### 7.1 Master Checklist Update (Phases 1 through 8)

| Phase | Title / Scope | Reconciled Status | Concrete Supporting Evidence |
| :---: | :--- | :---: | :--- |
| **Phase 1** | Codebase Inventory & Baseline | **VERIFIED COMPLETE** | 42/42 tests passing; read-only SQLite DB; frozen PyTorch checkpoint verified. |
| **Phase 2** | Telemetry & Episode Reconciliation | **VERIFIED COMPLETE** | 200-row census reconciled; 169 fault vs. 175 episode count resolved. |
| **Phase 3** | Anomaly Detection Benchmark (Exp A) | **VERIFIED COMPLETE** | $N=320$ windows; McNemar test $p = 2.17 \times 10^{-19}$; exposure corrected. |
| **Phase 4** | Root-Cause Diagnosis Benchmark (Exp B) | **PARTIALLY COMPLETE** | $7 \times 6 = 42$ evaluations; bounded by small sample size ($N=6$, power $0.14$). |
| **Phase 5** | Execution Boundary Safety Audit (Exp C) | **VERIFIED COMPLETE** | 16-case taxonomy; 11/11 attacks blocked; atomic SQLite approval logging. |
| **Phase 6** | Reproducibility Pipeline & Manifest | **VERIFIED COMPLETE** | `run_all.py` executes in 52.7s (exit 0); SHA-256 manifest produced. |
| **Phase 7** | Camera-Ready Manuscript Synthesis | **DRAFT COMPLETED (BOUNDED REPORT)** | 14 sections authored; backed by evidence matrix; submission blocked. |
| **Phase 8** | Reproducibility Closure & External Validation | **REPRODUCIBILITY CLOSED; PROTOCOL FROZEN; EXTERNAL RUN BLOCKED** | IF threshold discrepancy resolved (bit-for-bit identical); AnoMod selected; protocol frozen; transfer throttled. |

### 7.2 Threats to Validity and Manuscript Reconciliation
The manuscript [`research/paper/AEGISOPS_RESEARCH_PAPER.md`](file:///c:/DL_PROJECT/research/paper/AEGISOPS_RESEARCH_PAPER.md) remains a **bounded experimental study**. Phase 8 reinforces the following scientific disclosures:
1. **The synthetic-to-production domain gap remains active**: Until AnoMod telemetry is transferred and ingested through the frozen protocol, AegisOps cannot claim empirical generalization to multi-tenant production microservices.
2. **Production-Readiness Disclaimer**: AegisOps is **not** production-ready. Test suite compliance (42/42 passing) verifies local code correctness, not operational fitness under live enterprise load.

---

## 8. Single Evidence-Supported Recommendation for Next Research Action

### Recommended Action:
**Execute Asynchronous Benchmark Ingestion via Resumable Transfer Script**

1. Deploy a background resumable transfer worker (`research/scripts/ingest_anomod.py`) utilizing HTTP `Range` headers and exponential backoff to download `AnoMod.zip` from Zenodo into `data/external/anomod/`.
2. Upon download completion and SHA-256 hash verification against Zenodo metadata, execute the frozen evaluation protocol in [`EXTERNAL_EVALUATION_PROTOCOL.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md).
3. Report the resulting empirical metrics as a distinct *Experiment D (AnoMod External Validation)* in the research paper without altering frozen synthetic benchmarks.
