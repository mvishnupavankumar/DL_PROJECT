# AegisOps — Pre-Phase-9 Evidence Integrity Gate

**Audit Document**: `research/audits/PRE_PHASE9_EVIDENCE_INTEGRITY_GATE.md`  
**Repository Root**: `C:\DL_PROJECT`  
**Audit Date**: October 12, 2026  
**Auditor**: Senior Research Scientist & Reproducibility Reviewer  
**Scope**: Pre-ingestion evidence reconciliation, synthetic detection metric reconciliation, external schema verification, and Phase 9 dataset transfer authorization.

---

## 1. Executive Gate Decision

```
================================================================================
FINAL GATE DECISION:
>>> PASS — SAFE TO BEGIN DATA INGESTION <<<
================================================================================
```

### Gate Assessment Summary
1. **Synthetic Detection Baseline Reconciled**: All conflicting metrics across LSTM Autoencoder, Isolation Forest, and rule baselines have been traced to raw machine-readable predictions (`detection_predictions.csv`). The historical `TP=118` claim is proven to be an unverified conversational transcription error; the authoritative empirical result is **TP=120, FP=2, TN=198, FN=0** ($F_1 = 0.9917$).
2. **Calibration Procedures Confirmed**:
   - Isolation Forest threshold is deterministically verified at $\tau = -0.018694$ (negated decision function, 99th percentile, 120D flattened).
   - LSTM Autoencoder threshold is verified at $\tau = 0.709399$ (99th percentile of 150 held-out normal validation sequence errors; the historical "95th percentile" claim is refuted by code and metadata).
3. **External Dataset Schema Audited Against Upstream Code**: The official AnoMod collection pipeline (`collect_metric.sh`, `fetch_prometheus_metrics.py`, `README.md`) was inspected directly. Critical schema corrections—including distinguishing true disk utilization from write throughput, scaling seconds to milliseconds for latency, and scaling fractional HTTP 5xx ratios to percentages—are formally incorporated into **Protocol Amendment v1.1.0**.
4. **Data Ingestion Invariant Preserved**: In strict compliance with instructions, **no external dataset download or extraction was executed during this audit**.

---

## 2. Repository Baseline and Cryptographic Snapshot

### 2.1 Git Repository State
* **Current Commit**: `d277c1df3c2599ddecdf5f0bb761c99718499667`
* **Commit Subject**: `"Manuscript Completion and Final Evidence Gate"`
* **Current Branch**: `main`
* **Working-Tree Status**:
  * Modified:
    * `research/audits/UPDATED_SEVEN_PHASE_CHECKLIST.md`
    * `research/audits/detection_rate_and_phase4_gate_20261012/UPDATED_SEVEN_PHASE_CHECKLIST.md`
    * `research/paper/AEGISOPS_RESEARCH_PAPER.md`
    * `research/paper/FIGURE_AND_TABLE_INDEX.md`
    * `research/paper/MANUSCRIPT_EVIDENCE_MATRIX.md`
  * Untracked:
    * `research/audits/MANUSCRIPT_CONSISTENCY_AUDIT.md`
    * `research/audits/PHASE8_CHECKLIST_RECONCILIATION.md`
    * `research/audits/PHASE9_EXTERNAL_VALIDATION_READINESS.md`
    * `research/audits/phase8_external_validation/`
    * `research/audits/PRE_PHASE9_EVIDENCE_INTEGRITY_GATE.md` (this report)

### 2.2 Active Environment Versions
* **Python Runtime**: `3.11.9` (`c:\DL_PROJECT\.venv\Scripts\python.exe`)
* **PyTorch**: `2.14.1+cpu`
* **scikit-learn**: `1.9.0`
* **NumPy**: `2.2.6`
* **Pandas**: `2.2.2`
* **pytest**: `8.4.1`

### 2.3 Cryptographic Hash Inventory (Current Files vs. Historical Manifests)

| Artifact Category | Relative File Path | Size (Bytes) | Authoritative SHA-256 Hash | Provenance / Status |
| :--- | :--- | :---: | :--- | :--- |
| **Raw Predictions** | `research/results/detection_predictions.csv` | 24,357 | `246e14f8b84b8b89cbfce180fd7722ae82820f516894aa5dd11462866d10cfbb` | Verified Authoritative (Matches `research/raw/` bit-for-bit) |
| **Raw Predictions (Backup)** | `research/raw/detection_predictions.csv` | 24,357 | `246e14f8b84b8b89cbfce180fd7722ae82820f516894aa5dd11462866d10cfbb` | Verified Frozen Copy |
| **Metric Summary** | `research/results/detection_metrics.csv` | 568 | `ed5775303f74156d844dc0068db4328e2237fc935a2bca260d613571083de57e` | Matches `MANIFEST_SHA256.json` |
| **Corrected Metric Registry** | `research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv` | 1,251 | `0dec30a21b954d8e7041b51dc4bb98800685130963a8459523f04c9993255452` | Verified Historical Audit Gate |
| **Model Checkpoint** | `models/lstm_autoencoder.pt` | 19,797 | `1cf44e6e82e459f543fcace25334f3076b76c77a357d46f65c11e3c44fd382de` | Matches `MANIFEST_SHA256.json` |
| **Model Metadata** | `models/lstm_autoencoder.json` | 846 | `24826b053833b08e80fb84e7e694adfad5b4a1124d935ccf3e3cd4f575eb045f` | Matches `MANIFEST_SHA256.json` |
| **Manuscript** | `research/paper/AEGISOPS_RESEARCH_PAPER.md` | 71,894 | `b80235c5d6c0b16797725b04b5b479adec8562c07f51d7ce44bca996b17cd544` | Reconciled Active Manuscript |
| **Figure & Table Index** | `research/paper/FIGURE_AND_TABLE_INDEX.md` | 14,369 | `3739d0add22c72f72021bdb3e780fffc48f919d9bae9047fcc26d11ed86aea70` | Reconciled Active Index |
| **Manuscript Evidence Matrix** | `research/paper/MANUSCRIPT_EVIDENCE_MATRIX.md` | 14,728 | `293529f0a721a0e1135bca9756581bc3cd478b9dbd71cd6ed51ceb824c3dd59b` | Reconciled Matrix |
| **Phase 8 Reconciliation Audit** | `research/audits/PHASE8_CHECKLIST_RECONCILIATION.md` | 14,160 | `101ed84224d5c3a81ea71a7724a0e012a46770ff43f158f94e6ea9f02d0c39b9` | Current Session Audit |
| **Manuscript Consistency Audit** | `research/audits/MANUSCRIPT_CONSISTENCY_AUDIT.md` | 15,497 | `77299354c4094204bb5dd0ffd54dbcae27068de2128c1a2c3759f2bd30f60c31` | Current Session Audit |
| **Phase 9 Readiness Audit** | `research/audits/PHASE9_EXTERNAL_VALIDATION_READINESS.md` | 14,503 | `fe501dacb330d24eff11efce0ebe7207b7332c09d7d8bcde1ab2f83feca54bf3` | Current Session Audit |
| **Master Checklist** | `research/audits/UPDATED_SEVEN_PHASE_CHECKLIST.md` | 15,153 | `1aa82ca1ca6e302a89f8c8b91de0c6a4d38ba0302fbd748b15b9eab689b4dd25` | Current Master Checklist (v2.1.0) |

---

## 3. Resolution of Synthetic Detection Inconsistencies

### 3.1 Recomputation from Raw Predictions (`detection_predictions.csv`, $N = 320$)
All detector metrics were independently recomputed directly from the 320 rows of `detection_predictions.csv` (200 ground-truth normal windows, 120 injected incident windows):

```python
# Direct confusion matrix calculation on detection_predictions.csv
yt = df["ground_truth"].values  # 200 normal (0), 120 incident (1)
```

| Method / Gate Column | True Positive (TP) | False Positive (FP) | True Negative (TN) | False Negative (FN) | Precision | Recall (Sensitivity) | F1-Score | Continuous PR-AUC | False-Positive Window Rate ($\text{FPR}_{\text{win}}$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Narrow Rules** (`narrow_rule_flag`) | 40 | 0 | 200 | 80 | 1.0000 | 0.3333 | 0.5000 | N/A | 0.00% |
| **Resource-Only Rules** (`resource_rule_flag`) | 80 | 0 | 200 | 40 | 1.0000 | 0.6667 | 0.8000 | N/A | 0.00% |
| **Full Operational Rules** (`rule_flag`) | 120 | 0 | 200 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.00% |
| **Isolation Forest** (`iso_flag`) | 57 | 4 | 196 | 63 | 0.9344 | 0.4750 | 0.6298 | 0.9056 | 2.00% |
| **LSTM Autoencoder** (`lstm_flag`) | **120** | **2** | **198** | **0** | **0.9836** | **1.0000** | **0.9917** | **0.9998** | **1.00%** |
| **Combined Alert** (`combined_flag`) | 120 | 2 | 198 | 0 | 0.9836 | 1.0000 | 0.9917 | N/A | 1.00% |

### 3.2 Resolution of the "TP=118 vs. TP=120" Discrepancy
* **Origin of Discrepancy**: In an intermediate conversational summary, an assistant turn inadvertently recorded `"LSTM: TP=118, FP=2, F1=0.983. IsoForest: TP=118, FP=4"`.
* **Empirical Audit**: An inspection of the authoritative predictions (`research/results/detection_predictions.csv`, lines 2–322) proves that:
  - There are exactly **120** positive ground-truth incident windows ($y = 1$).
  - For `lstm_flag`, every single one of the 120 incident windows was flagged ($y_{\text{pred}} = 1$).
  - Hence, $\text{TP} = 120$ and $\text{FN} = 0$, giving an episode recall of $120 / 120 = 100.0\%$.
  - For `iso_flag`, only 57 of the 120 incident windows were flagged. Hence $\text{TP} = 57$ and $\text{FN} = 63$, giving a recall of $57 / 120 = 47.50\%$.
* **Verdict**: **TP=120 is the sole empirically valid result**. The `TP=118` claim is completely absent from all raw data files, metric CSVs, figures, and manuscript text. It is marked as an **erroneous chat hallucination** and permanently expunged.

### 3.3 Resolution of the LSTM Calibration Percentile Discrepancy
* **Conflicting Claims**: Some previous reports asserted the LSTM reconstruction error threshold was calibrated at the "95th percentile on 40 validation sequences".
* **Source Code Verification**: In [dl/anomaly_detector.py](file:///c:/DL_PROJECT/dl/anomaly_detector.py#L236-L254):
  ```python
  threshold = float(np.quantile(val_scores, 0.99))
  checkpoint["threshold_method"] = "99th percentile of held-out normal reconstruction error"
  ```
* **Artifact Metadata Verification**: In [models/lstm_autoencoder.json](file:///c:/DL_PROJECT/models/lstm_autoencoder.json#L34-L37):
  ```json
  "training_windows": 850,
  "validation_windows": 150,
  "threshold": 0.7093990445137024,
  "threshold_method": "99th percentile of held-out normal reconstruction error"
  ```
* **Verdict**: Calibration was performed on **150 held-out normal sequences** at the **99th percentile (0.99 quantile)**, yielding $\tau = 0.709399$. The "95th percentile / 40 sequences" claim was an inherited conversational misconception, now formally refuted and corrected.

### 3.4 Isolation Forest Score Direction and Threshold Determinism
* **Score Convention**: The active pipeline in [run_experiment_a.py](file:///c:/DL_PROJECT/research/experiments/run_experiment_a.py#L182-L191) applies **negated decision scores**:
  $$\text{score} = -\text{decision\_function}(X)$$
  where higher scores indicate greater anomaly.
* **Active Threshold**: Calibrated as `np.quantile(-iso_forest.decision_function(val_flat), 0.99)` on 200 normal training sequences (flattened 120D, seed=42), yielding $\tau = -0.01869408252273673$.
* **Two-Run Bit-for-Bit Determinism**: Two full end-to-end executions produced identical thresholds ($-0.018694$) and identical predictions for all 320 evaluation windows.
* **Historical Stale Values**:
  - $+0.089886$: Produced by early un-negated quantile calculations. Obsolete.
  - $-0.090333$: Stale textual transcription drift. Fully eliminated from the manuscript.

### 3.5 Formal Hypothesis Testing Reconciliation
* **Paired McNemar's Test** ($N = 120$ paired incident episodes):
  - Contingency table: $a = 57$ (both detected), $b = 63$ (LSTM detected, IsoForest missed), $c = 0$ (IsoForest detected, LSTM missed), $d = 0$ (both missed).
  - Exact two-sided binomial $p$-value: $p = 2 \times (0.5)^{63} = 2.168 \times 10^{-19}$.
  - Effect size: $\Delta_{\text{Recall}} = +0.5250$ (95% Wilson CI: $[+0.4357, +0.6143]$).
* **Cluster-Adjusted Scenario Wilcoxon Signed-Rank Test** ($N = 6$ failure scenarios):
  - Scenario recall vector (LSTM): $[1.0, 1.0, 1.0, 1.0, 1.0, 1.0]$.
  - Scenario recall vector (IsoForest): $[0.0, 0.0, 0.85, 1.0, 0.0, 1.0]$.
  - Wilcoxon statistic: $W = 0.0, p = 0.03125$.
* **Normal Window False Alarms** ($N = 200$):
  - Discordant pairs: $b = 4$ (IsoForest only), $c = 2$ (LSTM only). Exact binomial $p = 0.6875$ (difference not statistically significant at $\alpha = 0.05$).

---

## 4. External Dataset Compatibility & Schema Mapping Audit

### 4.1 Authoritative Dataset Profile
* **Dataset Candidate**: **AnoMod** (Microservices Benchmark Suite)
* **Authors**: Ke Ping, Hamza Bin Mazhar, Yuqing Wang, Ying Song, Mika V. Mäntylä (Univ. of Helsinki / Univ. of Oulu)
* **Conference**: Proceedings of the 23rd IEEE/ACM International Conference on Mining Software Repositories (MSR '26)
* **Preprint**: `arXiv:2601.22881`
* **Permanent DOI**: `10.5281/zenodo.18342898`
* **Official Archive URL**: `https://zenodo.org/records/18342898/files/AnoMod.zip?download=1`
* **Archive Filename**: `AnoMod.zip`
* **Archive Size**: `201,917,396` bytes ($\approx 192.5\text{ MiB}$)
* **License**: Creative Commons Attribution 4.0 International (**CC-BY-4.0**)
* **Integrity Source**: Zenodo InvenioRDM record metadata MD5 manifest and preview headers.

### 4.2 In-Depth Feature Schema Audit Against Upstream Code
The upstream data collection scripts in `SN_collection-scripts/Dataset/metric_data/collect_metric.sh` and `fetch_prometheus_metrics.py` were audited to establish the exact metric definitions:

```bash
# Extract from AnoMod upstream collect_metric.sh:
python3 ./fetch_prometheus_metrics.py --query "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))" \
  --output "$OUTPUT_DIR/microservice_latency_p95.csv" --hours 24 --step 15s

python3 ./fetch_prometheus_metrics.py --query "sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (service) / sum(rate(http_requests_total[5m])) by (service)" \
  --output "$OUTPUT_DIR/microservice_error_rate.csv" --hours 24 --step 15s

python3 ./fetch_prometheus_metrics.py --query "100 * (1 - (node_filesystem_avail_bytes{mountpoint=\"/\"} / node_filesystem_size_bytes{mountpoint=\"/\"}))" \
  --output "$OUTPUT_DIR/system_disk_usage_percent.csv" --hours 24 --step 15s

python3 ./fetch_prometheus_metrics.py --query "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)" \
  --output "$OUTPUT_DIR/system_cpu_usage.csv" --hours 24 --step 15s
```

Based on this ground-truth inspection, five critical schema discrepancies were identified and resolved:

#### 1. Resolution of Disk Metric Conflation (Write Throughput vs. Capacity Utilization)
* **Problem**: In `EXTERNAL_EVALUATION_PROTOCOL.md` (v1.0.0), `disk_pct` was specified as `rate(container_fs_writes_bytes_total[1m]) normalized to nominal max`. This equated **disk write throughput (bytes/second)** with **disk capacity utilization (percentage)** without justification.
* **Resolution**: The collection script collects **both**:
  - `system_disk_usage_percent.csv`: Direct filesystem utilization: $100 \times \left(1 - \frac{\text{avail}}{\text{size}}\right)$. This is a true percentage in $[0.0, 100.0]$, perfectly matching AegisOps' synthetic `disk_pct` semantic.
  - `system_disk_write_bytes.csv`: Write throughput in bytes/s.
* **Rule**: The primary mapping for `disk_pct` **must use `system_disk_usage_percent.csv`**. If I/O burstiness is evaluated as a secondary modality, `system_disk_io_time.csv` or normalized throughput must be evaluated as an explicitly designated separate feature, not silently substituted.

#### 2. CPU Normalization and Units
* **Container-Level vs. Node-Level**:
  - Container metric `container_cpu_usage_seconds_total` measures cumulative core seconds. Applying `rate(...)[1m]` yields cores consumed (unbounded; can exceed 1.0 or 100 on multi-core systems).
  - Node exporter metric `system_cpu_usage.csv` computes $100 - \text{idle} \times 100$, which is natively bounded in $[0.0, 100.0]\%$.
* **Rule**: For entrypoint service evaluation, container CPU rate must be divided by the container's CPU quota/limit (`container_spec_cpu_quota / container_spec_cpu_period`), OR the system-level metric `system_cpu_usage.csv` must be utilized.

#### 3. Latency Units (Seconds to Milliseconds)
* **Problem**: `microservice_latency_p95.csv` records Prometheus histogram quantiles in **seconds** (e.g., $0.250\text{ s}$ for a 250 ms response). AegisOps operates strictly on **milliseconds** (`latency_ms`).
* **Rule**: Telemetry values extracted from `microservice_latency_p95.csv` **must be multiplied by $1,000$** prior to rolling-window ingestion ($\text{latency\_ms} = \text{latency\_seconds} \times 1000.0$).

#### 4. Error-Rate Scaling and Status-Code Definition
* **Status Codes**: The upstream query explicitly filters on `status=~"5.."`. Hence, error rates reflect **server-side HTTP 5xx errors exclusively** (e.g., 500, 502, 503, 504); client-side 4xx errors are excluded.
* **Scale**: The Prometheus query yields a fraction in $[0.0, 1.0]$ over a 5-minute rate. AegisOps models `error_rate_pct` as a percentage in $[0.0, 100.0]\%$.
* **Rule**: Values from `microservice_error_rate.csv` **must be multiplied by $100$** ($\text{error\_rate\_pct} = \text{ratio} \times 100.0$).

#### 5. Sampling Frequency & Temporal Interpolation Implications
* **Upstream Sampling Step**: AnoMod queries Prometheus with `step=15s` (15-second resolution) over 5-minute rolling rate aggregations (`[5m]`).
* **AegisOps Horizon**: AegisOps uses sequence length $W = 24$ at $\Delta t = 5\text{ s}$ ($120\text{ s}$ total window horizon).
* **Implication Analysis**:
  - *Option 1 (Linear Interpolation to 5s)*: Expands each 15s scrape into 3 five-second steps via linear interpolation. This preserves $W = 24$, but introduces synthetic autocorrelation and false intermediate smoothness.
  - *Option 2 (Native 15s Windowing)*: Preserves true raw measurements without interpolation artifacts. With $W = 8$, the time horizon is exactly $8 \times 15\text{s} = 120\text{s}$. However, this requires resizing the model's sequence dimension from 24 to 8. Alternatively, keeping $W = 24$ at 15s steps expands the horizon to $360\text{s}$ (6 minutes).
* **Rule**: Both Option 1 and Option 2 must be formally pre-registered in Protocol Amendment v1.1.0, with Option 1 designated as the zero-shot transfer baseline and Option 2 designated as the native temporal baseline.

---

## 5. Frozen Protocol Amendment v1.1.0

To ensure zero post-hoc data snooping, the following protocol amendments are formally ratified prior to external dataset download:

| Feature Dimension | AegisOps Feature | Upstream AnoMod Metric Source | Transformation / Unit Conversion | Justification |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `cpu_pct` | `system_cpu_usage.csv` (Node Exporter) | Native percentage $[0.0, 100.0]\%$ | Bounded capacity metric matching synthetic host CPU. |
| **2** | `memory_pct` | `system_memory_usage_percent.csv` | Native percentage $[0.0, 100.0]\%$ | Directly reflects memory exhaustion without unbounded byte shifts. |
| **3** | `disk_pct` | `system_disk_usage_percent.csv` | Native percentage $[0.0, 100.0]\%$ | Corrects erroneous substitution of write throughput for capacity utilization. |
| **4** | `latency_ms` | `microservice_latency_p95.csv` | $\text{latency\_seconds} \times 1000.0$ | Converts Prometheus seconds to AegisOps milliseconds. |
| **5** | `error_rate_pct` | `microservice_error_rate.csv` | $\text{error\_ratio} \times 100.0$ | Converts 5xx ratio $[0.0, 1.0]$ to percentage $[0.0, 100.0]\%$. |

### Ground-Truth Fault Independence
* Fault injection labels are generated by ChaosBlade / ChaosMesh execution manifests (e.g., `blade create cpu load --cpu-percent 100 --timeout 300`).
* Fault activation and deactivation timestamps are logged independently in the experiment orchestration runner (`automated_multimodal_collection.sh`).
* Ground truth labels are strictly independent of all detector predictions and operational rules.

---

## 6. Phase 9 Data Ingestion Requirements & Constraints

With evidence integrity verified, data ingestion may proceed subject to the following strict technical constraints:

1. **Official Archive Target**:
   - URL: `https://zenodo.org/records/18342898/files/AnoMod.zip?download=1`
   - Destination: `data/external/anomod/AnoMod.zip`
2. **Network Resilience**:
   - Zenodo endpoints enforce aggressive bot throttling ($\approx 5.38\text{ KB/s}$ on single-stream requests).
   - Ingestion script must implement HTTP `Range` headers to support **resumable multi-chunk downloads**, exponential backoff (1s to 60s), and socket timeout handling.
3. **Integrity Gate**:
   - Prior to archive unpacking, file size must match `201,917,396` bytes ($\pm 0$).
   - MD5 / SHA-256 checksum must be verified and logged in `research/audits/phase8_external_validation/ANOMOD_INGESTION_LOG.md`.
4. **Safe Extraction**:
   - Extraction must use explicit path sanitation to prevent zip-slip / directory traversal vulnerabilities.
   - Archive must be extracted to `data/external/anomod/unpacked/`.

---

## 7. Verification Commands & Execution Log

| Command Executed | Purpose | Outcome | Exit Code |
| :--- | :--- | :--- | :---: |
| `.\.venv\Scripts\pytest.exe -q` | Full test suite regression verification | `42 passed in 32.05s` | 0 |
| `python scratch/audit_predictions.py` | Confusion matrix recomputation on `detection_predictions.csv` | LSTM: TP=120, FP=2, TN=198, FN=0; IsoForest: TP=57, FP=4, TN=196, FN=63 | 0 |
| `python scratch/inspect_queries.py` | Prometheus query extraction from AnoMod upstream `collect_metric.sh` | Verified exact Prometheus queries for CPU, RAM, Disk, Latency, and Error | 0 |
| `python scratch/compute_snapshot_hashes.py` | SHA-256 cryptographic hash computation across all critical artifacts | Hashes computed and cross-referenced with manifest | 0 |

---

## 8. Epistemic Classification of Project Results

* **[Tier 1 — Verified Facts]**:
  - 320 synthetic test windows with exact feature arrays.
  - 42 passing unit and regression tests in `tests/`.
  - Detection metrics: Full Rules ($F_1 = 1.000$), LSTM Autoencoder ($F_1 = 0.9917$, TP=120, FP=2), Isolation Forest ($F_1 = 0.6298$, TP=57, FP=4).
  - Deterministic thresholds: LSTM $\tau = 0.709399$ (99th percentile), Isolation Forest $\tau = -0.018694$ (negated score, 99th percentile).
* **[Tier 2 — Inherited Claims]**:
  - Live LLM RCA evaluation (20/20 incident diagnosis across strict/lenient rubrics) inherited from frozen run records in `research/results/rca_raw_results.json`.
* **[Tier 3 — Methodological Derivations]**:
  - Non-overlapping 24-step sequence structure ($120\text{s}$ exposure per window; 6.67h total normal exposure).
  - Decoupling of window-level false positive rate from operational streaming alarms-per-hour.
* **[Tier 4 — Unresolved / Pending]**:
  - External benchmark performance on AnoMod (Stage 2 through Stage 6 of external validation lifecycle).
