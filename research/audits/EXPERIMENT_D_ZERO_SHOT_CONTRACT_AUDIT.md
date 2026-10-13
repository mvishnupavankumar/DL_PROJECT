# AegisOps Experiment D: Frozen Model Contract and Window Reconciliation Audit

**Document ID**: `AEGISOPS-AUDIT-EXP-D-ZERO-SHOT-CONTRACT-001`  
**Date**: October 13, 2026  
**Auditor**: Independent ML Research Engineer, Statistical Auditor & Reproducibility Reviewer  
**Repository**: `C:\DL_PROJECT`  
**Git HEAD**: `d277c1df3c2599ddecdf5f0bb761c99718499667`  
**Working Tree**: Modified / Uncommitted audit & research documentation (clean execution gate)  
**Status**: Formal Audit Deliverable  

---

## Executive Summary

This audit reconciles the frozen deep learning model contract, resolves conflicting feature-order specifications in existing documentation, traces raw telemetry observations in the external benchmark (AnoMod SocialNetwork cohort), and provides an exact mathematical and physical accounting of nominal window counts.

### Key Audit Findings
1. **Model Contract Verified**:
   - Checkpoint: [`models/lstm_autoencoder.pt`](file:///C:/DL_PROJECT/models/lstm_autoencoder.pt) (SHA-256: `1cf44e6e82e459f543fcace25334f3076b76c77a357d46f65c11e3c44fd382de`, 19,797 bytes).
   - Authoritative Feature Order: `("cpu_pct", "memory_pct", "latency_ms", "error_rate_pct", "disk_pct")` across [`dl/anomaly_detector.py`](file:///C:/DL_PROJECT/dl/anomaly_detector.py#L14), checkpoint keys, and [`models/lstm_autoencoder.json`](file:///C:/DL_PROJECT/models/lstm_autoencoder.json).
   - Fatal Documentation Contradiction: [`EXTERNAL_EVALUATION_PROTOCOL.md`](file:///C:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md#L68-L72) v1.1.0 §4.1 specified `(cpu_pct, memory_pct, disk_pct, latency_ms, error_rate_pct)`. Swapping disk with latency/error would scramble tensor dimensions.
2. **Nominal Window Discrepancy Fully Reconciled**:
   - In SocialNetwork `Normal_Baseline_20251103_220228`, there are **80 raw 15-second grid intervals** (20 minutes total).
   - Due to distributed trace sparsity, 23 intervals contain zero trace spans. Only **57 complete intervals** exist.
   - Contiguous temporal runs with $W \ge 8$ without gaps form exactly **3 runs** of lengths 11, 11, and 18 intervals.
   - Total eligible sliding windows ($W=8$, step=1): $4 + 4 + 11 = \mathbf{19\text{ windows}}$, covering only 40 distinct valid timestamps (10 minutes total).
   - A 70/30 chronological split on raw series with a 7-step purge gap partitions the 80 rows into:
     - Calibration: rows 0..55 (56 rows) $\rightarrow \mathbf{5\text{ calibration windows}}$.
     - Purge gap: rows 56..62 (7 rows purged, preventing overlap).
     - Validation: rows 63..79 (17 rows) $\rightarrow \mathbf{8\text{ validation windows}}$ constructed from 15 contiguous valid rows (22:19:15 to 22:22:45).
   - Historical estimates of "~2 validation windows" arose from analytical estimates on cleaned complete subsets (57 rows) or window-level partitioning, whereas the 8 windows reflect the actual raw row indexing of `partition_normal_series_chronologically()`.
   - All 8 validation windows derive from a single 3.5-minute contiguous sequence and share 87.5% of their data with adjacent windows.
3. **Sequence Length Incompatibility**:
   - The frozen model was trained on $W=24$ ($24 \times 5\text{s} = 120\text{s}$).
   - In SocialNetwork Normal Baseline, the longest contiguous valid run is 18 intervals. Thus, for $W=24$, there are **0 eligible windows**.
   - Evaluating on $W=8$ violates `TelemetryAnomalyDetector.detect()` input assertion (`ValueError: Expected 24 time steps; received 8`).

---

## 1. Frozen Model Contract Audit

### 1.1 Source-of-Truth Artifacts
The frozen model contract was audited directly against the filesystem artifacts:
- Model Checkpoint: [`models/lstm_autoencoder.pt`](file:///C:/DL_PROJECT/models/lstm_autoencoder.pt)
- Model Metadata: [`models/lstm_autoencoder.json`](file:///C:/DL_PROJECT/models/lstm_autoencoder.json)
- Architecture Definition & Loader: [`dl/anomaly_detector.py`](file:///C:/DL_PROJECT/dl/anomaly_detector.py)

### 1.2 Model Architecture and Tensor Shapes
- **Class**: `LSTMAutoencoder` ([`dl/anomaly_detector.py:19-32`](file:///C:/DL_PROJECT/dl/anomaly_detector.py#L19-L32))
- **Total Parameters**: 3,605 learnable weights:
  - `encoder.weight_ih_l0`: `torch.Size([64, 5])` (LSTM input weights: $4 \times 16 \times 5$)
  - `encoder.weight_hh_l0`: `torch.Size([64, 16])` (LSTM hidden weights: $4 \times 16 \times 16$)
  - `encoder.bias_ih_l0`: `torch.Size([64])`
  - `encoder.bias_hh_l0`: `torch.Size([64])`
  - `decoder.weight_ih_l0`: `torch.Size([64, 16])`
  - `decoder.weight_hh_l0`: `torch.Size([64, 16])`
  - `decoder.bias_ih_l0`: `torch.Size([64])`
  - `decoder.bias_hh_l0`: `torch.Size([64])`
  - `output_layer.weight`: `torch.Size([5, 16])`
  - `output_layer.bias`: `torch.Size([5])`
- **Trained Sequence Length**: $W = 24$ ([`dl/anomaly_detector.py:15`](file:///C:/DL_PROJECT/dl/anomaly_detector.py#L15), checkpoint key `sequence_length = 24`).
- **Input Tensor Shape**: $(B, W, D) = (1, 24, 5)$.

### 1.3 Feature Vector Contract and Feature-Order Conflict Resolution

#### Investigation of Conflicting Feature Orders
Two conflicting feature orders appear in the repository documentation:
- **Order A**: `("cpu_pct", "memory_pct", "latency_ms", "error_rate_pct", "disk_pct")`
- **Order B**: `("cpu_pct", "memory_pct", "disk_pct", "latency_ms", "error_rate_pct")`

#### Forensic Source Tracing
| Location | Documented Feature Order | Authority Status |
| :--- | :--- | :--- |
| [`dl/anomaly_detector.py:14`](file:///C:/DL_PROJECT/dl/anomaly_detector.py#L14) | `("cpu_pct", "memory_pct", "latency_ms", "error_rate_pct", "disk_pct")` | **Primary Code Authority** |
| [`models/lstm_autoencoder.pt`](file:///C:/DL_PROJECT/models/lstm_autoencoder.pt) (`ckpt["features"]`) | `['cpu_pct', 'memory_pct', 'latency_ms', 'error_rate_pct', 'disk_pct']` | **Primary Checkpoint Authority** |
| [`models/lstm_autoencoder.json`](file:///C:/DL_PROJECT/models/lstm_autoencoder.json) | `['cpu_pct', 'memory_pct', 'latency_ms', 'error_rate_pct', 'disk_pct']` | **Primary Metadata Authority** |
| [`research/experiments/run_experiment_d.py:66`](file:///C:/DL_PROJECT/research/experiments/run_experiment_d.py#L66) | `("cpu_pct", "memory_pct", "latency_ms", "error_rate_pct", "disk_pct")` | Implementation Code |
| [`EXTERNAL_EVALUATION_PROTOCOL.md:68-72`](file:///C:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md#L68-L72) | `(cpu_pct, memory_pct, disk_pct, latency_ms, error_rate_pct)` | **Erroneous Legacy Documentation** |

**Verdict on Feature Order**:
The true, irrevocable feature contract embedded in the weights of `models/lstm_autoencoder.pt` is **Order A**:
$$\mathbf{x}_t = \begin{bmatrix} x_t^{(0)}: \texttt{cpu\_pct} \\ x_t^{(1)}: \texttt{memory\_pct} \\ x_t^{(2)}: \texttt{latency\_ms} \\ x_t^{(3)}: \texttt{error\_rate\_pct} \\ x_t^{(4)}: \texttt{disk\_pct} \end{bmatrix}$$

`EXTERNAL_EVALUATION_PROTOCOL.md` v1.1.0 §4.1 contains a documentation error that transposed `disk_pct` to position 3. Any implementation relying on the v1.1.0 table without `PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md` would scramble input dimensions and invalidate inference.

### 1.4 Normalization Parameters and Value Semantics
The frozen checkpoint stores precomputed normalization moments derived from synthetic nominal training data ($N=850$ windows):
- **Mean Vector** ($\boldsymbol{\mu} \in \mathbb{R}^5$):
  - `cpu_pct`: $42.059334\%$
  - `memory_pct`: $53.97087\%$
  - `latency_ms`: $76.89183\text{ ms}$
  - `error_rate_pct`: $0.23941098\%$
  - `disk_pct`: $48.268738\%$
- **Standard Deviation Vector** ($\boldsymbol{\sigma} \in \mathbb{R}^5$):
  - `cpu_pct`: $5.785898\%$
  - `memory_pct`: $3.5649338\%$
  - `latency_ms`: $6.089803\text{ ms}$
  - `error_rate_pct`: $0.05497076\%$
  - `disk_pct`: $4.335354\%$
- **Scaling Formula**:
  $$\tilde{\mathbf{x}}_t = \frac{\mathbf{x}_t - \boldsymbol{\mu}}{\max(\boldsymbol{\sigma}, 10^{-6})}$$

### 1.5 Reconstruction Error and Threshold Semantics
- **Reconstruction Error Definition** ([`dl/anomaly_detector.py:164-165`](file:///C:/DL_PROJECT/dl/anomaly_detector.py#L164-L165)):
  $$e(\mathbf{X}) = \frac{1}{W \cdot D} \sum_{t=1}^W \sum_{d=1}^D \left( \hat{x}_{t,d} - \tilde{x}_{t,d} \right)^2$$
- **Frozen Decision Threshold**:
  $$\tau_{\text{frozen}} = 0.7093990445137024$$
  Calibrated as the empirical 99th percentile of reconstruction loss on 150 held-out synthetic validation windows of length $W=24$.
- **Per-Feature Error Thresholds**:
  - `cpu_pct`: $0.804801$
  - `memory_pct`: $0.327871$
  - `latency_ms`: $1.282949$
  - `error_rate_pct`: $1.617288$
  - `disk_pct`: $0.310492$
- **Input Integrity Checks**:
  - Non-finite rejection: `TelemetryAnomalyDetector.detect()` ([`dl/anomaly_detector.py:156-157`](file:///C:/DL_PROJECT/dl/anomaly_detector.py#L156-L157)) raises `ValueError` if any NaN or infinite value is present.
  - Length check: raises `ValueError` if `values.shape[0] != 24` ([`dl/anomaly_detector.py:154-155`](file:///C:/DL_PROJECT/dl/anomaly_detector.py#L154-L155)).

---

## 2. Reconciling Nominal-Window Counts (SocialNetwork Cohort)

### 2.1 Raw Telemetry Audit of `Normal_Baseline`
- **Directory**: `data/external/anomod/unpacked/SN_data/metric_data/Normal_Baseline_20251103_220228_metrics_2025-11-03_22-22-55`
- **Trace Directory**: `data/external/anomod/unpacked/SN_data/trace_data/Normal_Baseline_20251103_220228_traces_2025-11-03_22-22-55`
- **Temporal Grid**: 15.0-second intervals from `2025-11-03 22:03:30` to `2025-11-03 22:23:15` (1,185 seconds total, exactly 80 grid points).

#### Observation Availability Breakdown
| Metric | Available Grid Points | Missing / NaN Points | Notes |
| :--- | :--- | :--- | :--- |
| `cpu_pct` | 79 / 80 | 1 | Single startup interval missing |
| `memory_pct` | 80 / 80 | 0 | Continuous Prometheus scrape |
| `disk_pct` | 80 / 80 | 0 | Continuous Prometheus scrape |
| `latency_ms` | 57 / 80 | 23 | Trace spans absent in 23 intervals |
| `error_rate_pct`| 57 / 80 | 23 | Trace spans absent in 23 intervals |
| **All 5 Finite** | **57 / 80** | **23** | **71.25% complete coverage** |

### 2.2 Contiguous-Window Construction Analysis
In accordance with `build_contiguous_windows()` ([`run_experiment_d.py:335-388`](file:///C:/DL_PROJECT/research/experiments/run_experiment_d.py#L335-L388)), sliding windows require strictly contiguous observations ($\Delta t = 15.0\text{s}$) where all 5 features are finite. Any missing observation resets the window buffer.

Mapping the 80 grid intervals reveals that the 57 valid observations cluster into exactly **3 contiguous runs**:
1. **Run 1** (Rows 36 to 46): 11 contiguous intervals (`22:12:30` to `22:15:00`).
   - Windows constructed ($W=8$, step=1): $11 - 8 + 1 = \mathbf{4\text{ windows}}$.
2. **Run 2** (Rows 48 to 58): 11 contiguous intervals (`22:15:30` to `22:18:00`).
   - Windows constructed ($W=8$, step=1): $11 - 8 + 1 = \mathbf{4\text{ windows}}$.
3. **Run 3** (Rows 60 to 77): 18 contiguous intervals (`22:18:30` to `22:22:45`).
   - Windows constructed ($W=8$, step=1): $18 - 8 + 1 = \mathbf{11\text{ windows}}$.

**Total Eligible Windows ($W=8$)**: $4 + 4 + 11 = \mathbf{19\text{ windows}}$.

#### Critical Sequence Length Impact ($W=24$ vs $W=8$)
- For $W = 24$, the required contiguous span is $24 \times 15\text{s} = 360\text{s}$.
- The longest contiguous run in `Normal_Baseline` is 18 intervals (270 seconds).
- **Result for $W = 24$**: **0 eligible windows**. It is mathematically impossible to construct even a single valid $W=24$ window from the real SocialNetwork baseline without unapproved synthetic interpolation or gap stitching.

### 2.3 Chronological Splitting and Purge Gap Accounting
In `run_experiment_d.py:716-720`, chronological partitioning is performed via:
`partition_normal_series_chronologically(df_normal, train_fraction=0.70, purge_gap_steps=7)`

Tracing this function on the raw 80-row DataFrame:
1. `n_calib = int(80 * 0.70) = 56` raw rows (Index 0 to 55).
2. `purge_gap_steps = 7` raw rows (Index 56 to 62).
3. `val_raw` = Index 63 to 79 (17 raw rows).

#### Resulting Windows
- **Calibration Partition (Rows 0..55)**:
  - Captures all of Run 1 (Rows 36..46): **4 windows**.
  - Captures part of Run 2 (Rows 48..55, exactly 8 rows): **1 window**.
  - Total Calibration Windows = $\mathbf{5\text{ windows}}$.
- **Purge Partition (Rows 56..62)**:
  - Rows 56..58 (tail of Run 2), Row 59 (NaN), Rows 60..62 (head of Run 3).
  - All shared or boundary timestamps purged.
- **Validation Partition (Rows 63..79)**:
  - Rows 63..77 are 15 contiguous valid rows from Run 3.
  - Rows 78..79 are NaNs.
  - Windows constructed from 15 contiguous rows: $15 - 8 + 1 = \mathbf{8\text{ validation windows}}$.

### 2.4 Reconciliation of "~2" vs "8" Validation Windows

| Window Count | Origin / Definition | Why it Exists in Audit Logs |
| :--- | :--- | :--- |
| **~2 Validation Windows** | Analytical estimation on cleaned 57 complete rows with a 75/25 split or window-level partitioning with a 7-window purge. | Documented in early notes ([`AEGISOPS_MASTER_RESEARCH_HANDOFF.md:166`](file:///C:/DL_PROJECT/research/audits/AEGISOPS_MASTER_RESEARCH_HANDOFF.md#L166), [`EXPERIMENT_D_READINESS_REAUDIT.md:189`](file:///C:/DL_PROJECT/research/audits/EXPERIMENT_D_READINESS_REAUDIT.md#L189) "$\le 5$ windows"). If one drops NaNs first, 57 rows with a 75% split leaves 14 rows, and after 7 purge steps, only 7 rows remain ($7 < 8 \implies 0$ windows). |
| **8 Validation Windows** | Actual execution of `run_experiment_d.py:716` where chronological splitting is applied to the **raw 80 rows** (preserving NaNs). | The 70/30 split happens to place the cutoff at raw row 56, and after 7 purge rows (56..62), leaves raw rows 63..79, within which exactly 15 contiguous valid rows remain, producing $15 - 8 + 1 = \mathbf{8\text{ windows}}$. |
| **19 Total Windows** | Full-run windowing across all 3 contiguous runs without any chronological partition or purge gap. | Documented in [`experiment_d_temporal_eligibility_audit.json`](file:///C:/DL_PROJECT/research/audits/experiment_d_temporal_eligibility_audit.json) ($4 + 4 + 11 = 19$). |

### 2.5 Dependence and Real Telemetry Exposure of the 8 Validation Windows
The 8 validation windows do **not** represent 8 independent samples:
- All 8 windows originate from a **single continuous 3.5-minute span** (`22:19:15` to `22:22:45`) in Run 3.
- Every consecutive pair of windows advances by 15 seconds, sharing 7 out of 8 observations (**87.5% shared telemetry**).
- They originate from **a single nominal execution run** (`Normal_Baseline_20251103_220228`).
- The effective sample size ($N_{\text{eff}}$) is close to 1 independent observation.

---

## 3. Audit Verdict

`RECONCILIATION COMPLETE — CONTRACT AND WINDOW COUNTS VERIFIED`

- The frozen model contract is conclusively established as `("cpu_pct", "memory_pct", "latency_ms", "error_rate_pct", "disk_pct")`.
- The nominal window count of 8 validation windows is mathematically verified and traced to raw row indexing in the 80-row sequence.
- The historical discrepancy between ~2 and 8 windows is traceable to raw-series vs cleaned-series partition definitions.
- The fundamental incompatibilities of sequence length ($W=8$ vs $W=24$) and domain shift remain unresolved technical obstacles for zero-shot transfer.
