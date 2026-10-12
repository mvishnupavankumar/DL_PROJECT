# AegisOps — Deep Learning Pipeline & Data Leakage Audit

**Date**: 2026-10-12  
**Auditor**: Senior ML Experiment Engineer / AIOps Researcher  
**Target Modules**: `dl/anomaly_detector.py`, `dl/live_training.py`, `models/lstm_autoencoder.pt`, `models/lstm_autoencoder.json`

---

## 1. Executive Summary

This leakage audit rigorously examines the training, validation, preprocessing, and inference code paths of the AegisOps LSTM Autoencoder. We identify which leakage prevention mechanisms are soundly implemented and uncover three critical methodological threats to scientific validity that must be addressed when reporting experimental results.

---

## 2. Preprocessing & Normalization Audit

### A. Feature Ordering & Unit Consistency
- **Feature Vector**: Strict 5-tuple:
  $$[\text{cpu\_pct}, \text{memory\_pct}, \text{latency\_ms}, \text{error\_rate\_pct}, \text{disk\_pct}]$$
- **Verification**: `dl/anomaly_detector.py:14`, `dl/live_training.py:33`, and `models/lstm_autoencoder.json:24` have identical ordering.
- **Unit Scale Variance**: Features operate across vastly different nominal scales:
  - `cpu_pct`, `memory_pct`, `disk_pct`, `error_rate_pct`: Percentages ($[0, 100]$).
  - `latency_ms`: Continuous positive milliseconds ($[0, 5000+]$).

### B. Normalization Fitting and Re-use
- **Standardization Equation**:
  $$z = \frac{x - \mu_{\text{train}}}{\sigma_{\text{adjusted}}}$$
- **Leakage Status**: **CLEAN (No Leakage)**. Preprocessing parameters $\mu$ and $\sigma$ are computed strictly on the training partition (`train_rows` or synthetic `train`). Validation and test data never inform mean or variance calculations.
- **Standard Deviation Floors** (`dl/live_training.py:44`):
  $$\sigma_{\text{adjusted}} = \max(\sigma_{\text{train}}, [1.0, 0.5, 5.0, 0.5, 0.5])$$
  This domain-aware floor prevents numerical explosion when disk usage or error rate is stationary in training data ($\sigma \to 0$).

---

## 3. Sequence Generation, Window Overlap & Temporal Boundary Audit

### A. Chronological Split vs. Windowing Sequence
In `dl/live_training.py:36-49`:
1. Chronological splitting occurs **first**: `train_rows = rows[:split]`, `val_rows = rows[split:]`.
2. Slicing into 24-step sequences occurs **second**:
   ```python
   train_windows = _windows(train_scaled, SEQUENCE_LENGTH)
   val_windows = _windows(val_scaled, SEQUENCE_LENGTH)
   ```
- **Boundary Leakage Verdict**: **PASS (Zero Boundary Leakage)**. Because the temporal array is partitioned into disjoint time blocks before sequence generation, no single window spans across the boundary from the training period into the validation period.

### B. Intra-Split Sliding Window Autocorrelation
- **Window Stride**: `stride = 1`. Each 24-step sequence shares 23 time steps ($95.83\%$ autocorrelation) with its immediate successor.
- **Batch Shuffling**: `DataLoader(TensorDataset(...), batch_size=32, shuffle=True)` randomly shuffles highly overlapping windows across minibatches.
- **Impact**: While standard in time-series autoencoders to maximize training instances, calculating parametric p-values or standard errors by treating overlapping windows as independent observations is scientifically invalid.

---

## 4. Threshold Calibration Protocol

### A. Threshold Selection Mechanism
In `dl/anomaly_detector.py:236` and `dl/live_training.py:79`:
- The reconstruction error threshold is calibrated as the **99th percentile of reconstruction errors on the held-out validation set**:
  $$\tau = \text{Quantile}_{0.99}(\text{MSE}_{\text{val}})$$
- Per-feature thresholds are calibrated similarly:
  $$\tau_f = \text{Quantile}_{0.99}(\text{MSE}_{\text{val}, f})$$

### B. Methodological Implication (The Baseline 1% False Positive Rate)
- Calibrating at the 99th percentile of normal validation data mathematically guarantees a **1.0% empirical false positive rate on steady-state normal data**.
- At a 5-second sampling cadence:
  $$\text{False Alarms per Hour} = \frac{3600\text{ s/hr}}{5\text{ s/sample}} \times 0.01 = 7.2\text{ false alarms / hour}$$
- In an operational SRE setting, 7 false alarms per hour represents alert fatigue. Thresholds in production AIOps typically target $\ge 99.9\text{th}$ percentile ($\approx 0.72\text{ alarms/hr}$) or require $k$-consecutive anomalous windows.

---

## 5. Checkpoint Compatibility & Live Data Eligibility

| Checkpoint Name | Origin Dataset | Sample Count | Status in Current Environment |
| :--- | :---: | :---: | :--- |
| `models/lstm_autoencoder.pt` | Synthetic normal sine waves (`generate_normal_windows`) | 800 windows | **Present & Operational**. Pre-trained baseline checkpoint. |
| `models/live_lstm_autoencoder.pt` | Real healthy host & probe samples from SQLite | Required $\ge 180$ | **Not Present**. Blocked by database eligibility: SQLite contains only 31 healthy samples (`fault_mode='normal'`). |

---

## 6. Rules for Experiment A & B Protocol Enforcement

To preserve strict scientific integrity:
1. **Never Tune on Test Data**: The existing threshold ($\tau = 0.709399$) of `models/lstm_autoencoder.pt` must be evaluated **frozen** without post-hoc tuning.
2. **Independent Test Split**: Synthetic and baseline evaluations must draw from an independent test partition (`seed=999`) completely unobserved during model training (`seed=42`) or validation.
3. **Isolation Forest Fairness**: The competing Isolation Forest baseline must be fitted strictly on the identical training partition, using the same window representation and features.
4. **Episode-Level Unit of Analysis**: Primary performance metrics must be reported at the independent fault episode level, avoiding inflated N counts from sliding stride-1 windows.
