# AegisOps — Deep Learning Pipeline Audit

**Audit Phase**: Phase 5  
**Auditor**: Senior Python Engineer / ML Researcher / SRE / Security Reviewer  
**Scope**: Model Architecture, Preprocessing, Training, Inference, Calibration, and Methodological Rigor

---

## 1. Model Architecture & Tensor Specification

The anomaly detector is an LSTM Autoencoder implemented in PyTorch (`dl/anomaly_detector.py:19`).

```text
Input Tensor: (B, 24, 5)
   │
   ▼
Encoder: nn.LSTM(input_size=5, hidden_size=16, batch_first=True)
   │  Output: _, (hidden, cell)
   │  hidden[-1] shape: (B, 16)
   ▼
Latent Expansion: hidden[-1].unsqueeze(1).repeat(1, 24, 1)
   │  Latent Tensor shape: (B, 24, 16)
   ▼
Decoder: nn.LSTM(input_size=16, hidden_size=16, batch_first=True)
   │  Decoded Tensor shape: (B, 24, 16)
   ▼
Projection: nn.Linear(in_features=16, out_features=5)
   │
   ▼
Reconstructed Tensor: (B, 24, 5)
```

### Parameter Count Breakdown
- **Encoder LSTM**: $4 \times ((5 + 1) \times 16 + 16^2) = 4 \times (96 + 256) = 1,408$ parameters.
- **Decoder LSTM**: $4 \times ((16 + 1) \times 16 + 16^2) = 4 \times (272 + 256) = 2,112$ parameters.
- **Output Linear Layer**: $(16 \times 5) + 5 = 85$ parameters.
- **Total Trainable Parameters**: **3,605** parameters (lightweight, ~14.4 KB in float32 weights).

---

## 2. Feature Pipeline & Preprocessing

### A. Input Features & Sequence Dimensions
- **Feature Vector**: Exactly 5 dimensions in strict order:
  1. `cpu_pct` (Host CPU utilization, 0–100%)
  2. `memory_pct` (Host RAM utilization, 0–100%)
  3. `latency_ms` (HTTP probe round-trip latency in milliseconds)
  4. `error_rate_pct` (Rolling probe failure percentage over 20 calls, 0–100%)
  5. `disk_pct` (Host filesystem usage, 0–100%)
- **Sequence Length**: `SEQUENCE_LENGTH = 24` consecutive observations.
- **Temporal Assumptions**: Assumes observations arrive at uniform 5.0-second intervals (total temporal receptive field = $24 \times 5\text{s} = 120\text{ seconds}$ / 2 minutes). Does not record or feed inter-sample $\Delta t$, making the model sensitive to jitter or variable sampling frequencies.

### B. Normalization & Standard Deviation Floors
- Normalization formula:
  $$x_{\text{scaled}} = \frac{x - \mu}{\sigma_{\text{adjusted}}}$$
- **Domain-Aware Floors** (`dl/live_training.py:44`):
  $$\sigma_{\text{adjusted}} = \max(\sigma_{\text{empirical}}, [1.0, 0.5, 5.0, 0.5, 0.5])$$
- **Rationale & Verification**: When disk percentage or error rate remains completely stationary during training ($0.0\%$ variation), $\sigma_{\text{empirical}} \to 0$. Without standard deviation floors, floating-point rounding leads to division by near-zero, exploding normalized scores or generating NaNs upon slight perturbation. The implementation of domain floors is a sound, verified engineering safeguard.

---

## 3. Training, Validation & Data Leakage Assessment

### A. Dataset Splitting Protocol
In `dl/live_training.py:36-49`:
1. Chronological order is preserved. The earliest 80% of healthy observations form `train_rows`, and the remaining 20% form `val_rows`.
2. Slicing into 24-step windows is executed **after** the raw chronological split:
   ```python
   train_windows = _windows(train_scaled, SEQUENCE_LENGTH)
   val_windows = _windows(val_scaled, SEQUENCE_LENGTH)
   ```
3. **Leakage Assessment**: Because windowing occurs after the split, no observation from `val_rows` appears in `train_windows`. There is zero test/val leakage into training.
4. **Window Autocorrelation within Training**: The sliding window generator uses a stride of 1:
   `[rows[i:i + sequence_length] for i in range(len(rows) - sequence_length + 1)]`.
   Adjacent windows share 23 out of 24 data points (95.8% overlap). When `DataLoader` runs with `shuffle=True`, these highly correlated slices are shuffled across minibatches. While standard practice for sequence autoencoders, it artificially inflates the effective sample count ($N - 23$) and causes batch-level correlation.

### B. Data Filtering and Quality Gates
- **Minimum Data Requirement**: Enforces `min_samples = 180` healthy rows (15 minutes of uninterrupted collection) before training can execute.
- **Health Filter SQL** (`storage/telemetry_store.py:96`):
  ```sql
  WHERE service_available = 1 AND status_code = 200 AND error_rate_pct = 0 AND fault_mode = 'normal'
    AND cpu_pct < 90 AND memory_pct < 95 AND disk_pct < 95 AND latency_ms < 1000
  ```
- **Finding on Target Generalization**: As documented in Phase 3, `fault_mode = 'normal'` restricts automatic training to the project's own `demo_service`. Any external production service returns `fault_mode = 'unknown'` and will be filtered out unless CLI `--assume-healthy` is used.

---

## 4. Threshold Calibration & Anomaly Scoring

### A. Scoring Metric
At inference time (`dl/anomaly_detector.py:164`):
$$\text{Reconstruction Error Matrix } E = (X_{\text{reconstructed}} - X_{\text{normalized}})^2$$
$$\text{Overall Anomaly Score } S = \frac{1}{T \times D} \sum_{t=1}^{24} \sum_{d=1}^{5} E_{t, d}$$
$$\text{Feature Dimension Error } F_d = \frac{1}{T} \sum_{t=1}^{24} E_{t, d}$$

### B. Threshold Calculation
- Overall Threshold: $T_{\text{global}} = \text{Quantile}_{0.99}(S_{\text{val}})$.
- Feature-Specific Thresholds: $T_{d} = \text{Quantile}_{0.99}(F_{d, \text{val}})$.
- **Theoretical Implication**: Calibrating at the 99th percentile of healthy validation data guarantees an expected **1.0% False Positive Rate (FPR)** on normal steady-state operations. On a system collecting every 5 seconds (720 samples/hour), a 1.0% FPR equates to approximately **7 false alerts per hour** in the absence of any true incident!

---

## 5. Checkpoint Management & Runtime Loading Realities

| Checkpoint File | Metadata File | Source Data | Loaded By | Role in Live Dashboard |
| :--- | :--- | :--- | :--- | :--- |
| `models/lstm_autoencoder.pt` | `models/lstm_autoencoder.json` | Synthetic sine waves (`generate_normal_windows`) | `dl/evaluate_detector.py`, `test_anomaly_detector.py`, `test_workflow.py` | **Completely ignored.** Not loaded anywhere in `live_monitoring.py`. |
| `models/live_lstm_autoencoder.pt` | `models/live_lstm_autoencoder.json` | Live collected SQLite telemetry | `live_monitoring.py:149` (`load_live_detector()`) | **Active Live Model.** Loaded only if present on disk; falls back to rules if absent. |

### Handling of Missing or Incompatible Checkpoints
- If `models/live_lstm_autoencoder.pt` is missing, `live_monitoring.py:147` smoothly falls back to `_bootstrap_analysis(latest)` (rule-based detection).
- If the checkpoint file is corrupted, malformed, or has an incompatible shape, lines 227–237 catch `(ValueError, KeyError, RuntimeError, OSError, TypeError)`, issue a Streamlit warning, and fallback to `_bootstrap_analysis`.

---

## 6. Scientific Risks and Research Limitations

1. **Synthetic Evaluation Metrics are Unrepresentative**:
   - `dl/evaluate_detector.py` reports Precision = 0.9677, Recall = 1.000, F1 = 0.9836.
   - **Critical Reality**: This benchmark evaluates synthetic gaussian noise against synthetic step-function ramp-ups (`INC-1001` through `INC-1006`). In this synthetic world, latency jumps abruptly from 42ms to 760ms or 1250ms. Any basic threshold rule achieves 100% recall on this dataset.
2. **Absence of Real-World Evaluation Benchmark**:
   - The repository contains **zero labeled real-world anomaly datasets** (e.g. NAB, SMD, or Yahoo benchmark data).
   - The live model has never been evaluated against real distributed production incidents.
3. **Severe Distribution Shift Vulnerability**:
   - Training on 180 samples (15 minutes) of idle developer machine telemetry produces a hyper-fragile baseline. If the user subsequently opens an IDE, browses a heavy webpage, or compiles code, CPU and RAM jump outside the 15-minute distribution, causing continuous false positive alerts.
4. **OR-Gate Masking of Model Weaknesses**:
   - Because `live_monitoring.py:199-204` overrides the anomaly decision with hardcoded static rules (`latency >= 1000ms`, `status != 200`, `cpu >= 90%`), a reviewer or operator cannot tell whether an incident was detected by the PyTorch LSTM or by the static `if` statement.
