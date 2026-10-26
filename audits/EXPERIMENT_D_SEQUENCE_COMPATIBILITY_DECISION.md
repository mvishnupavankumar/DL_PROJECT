# AegisOps Experiment D: Sequence-Length Compatibility and Contract Audit

**Document ID**: `AEGISOPS-AUDIT-EXP-D-SEQ-COMPAT-001`  
**Date**: October 13, 2026  
**Auditor**: Independent ML Research Engineer, Statistical Auditor & Reproducibility Reviewer  
**Repository**: `C:\DL_PROJECT`  
**Git HEAD**: `d277c1df3c2599ddecdf5f0bb761c99718499667`  
**Working Tree Status**: Audit documentation updates (Pre-execution gate locked)  
**Audit Verdict**: `BLOCKED — MODEL CONTRACT INCOMPATIBILITY`  
**Production Status**: **STRICTLY BLOCKED — NO AUTHORIZED PRODUCTION EXECUTION**  

---

## 1. Sequence-Length Contract Forensic Analysis

### 1.1 The Frozen Model Contract ($W=24$)
The frozen PyTorch model checkpoint [`models/lstm_autoencoder.pt`](file:///C:/DL_PROJECT/models/lstm_autoencoder.pt) and its metadata [`models/lstm_autoencoder.json`](file:///C:/DL_PROJECT/models/lstm_autoencoder.json) define an irrevocable temporal contract:
- **Trained Sequence Length**: $W = 24$ (`checkpoint["sequence_length"] = 24`, [`models/lstm_autoencoder.json:31`](file:///C:/DL_PROJECT/models/lstm_autoencoder.json#L31)).
- **Input Tensor Dimensions**: $(B, W, D) = (1, 24, 5)$.
- **Synthetic Training Temporal Horizon**: In training, telemetry was synthesized at $\Delta t = 5.0\text{ seconds}$ per step:
  $$\text{Temporal Horizon} = 24 \times 5.0\text{s} = 120.0\text{ seconds}$$
- **Official Model Inference Interface**:
  In [`dl/anomaly_detector.py:150-158`](file:///C:/DL_PROJECT/dl/anomaly_detector.py#L150-L158), `TelemetryAnomalyDetector.detect(telemetry)` enforces strict contract assertions:
  ```python
  if values.ndim != 2 or values.shape[1] != len(self.features):
      raise ValueError(f"Telemetry must have shape (time_steps, {len(self.features)} features).")
  if values.shape[0] != self.sequence_length:
      raise ValueError(f"Expected {self.sequence_length} time steps; received {values.shape[0]}.")
  if not np.isfinite(values).all():
      raise ValueError("Telemetry contains NaN or infinite values.")
  ```
  Calling `detect()` on any input where $W \ne 24$ fails closed with `ValueError: Expected 24 time steps; received 8`.
- **Threshold Calibration Semantics**:
  The frozen decision threshold $\tau_{\text{frozen}} = 0.7093990445137024$ was computed as the empirical 99th percentile of mean squared reconstruction error on 150 held-out synthetic validation sequences of length $W = 24$ ([`dl/anomaly_detector.py:236`](file:///C:/DL_PROJECT/dl/anomaly_detector.py#L236)).

---

## 2. Forensic Investigation: Why the External Harness Uses $W=8$

In [`research/experiments/run_experiment_d.py:48,322,337`](file:///C:/DL_PROJECT/research/experiments/run_experiment_d.py#L48), the external validation harness hardcodes $W = 8$:
```python
WINDOW_SIZE: int = 8
WINDOW_STEP: int = 1
LSTM_WINDOW_SIZE: int = 8
```

### 2.1 The Rationale Behind $W=8$
The origin of $W = 8$ is documented in [`EXTERNAL_EVALUATION_PROTOCOL.md:75`](file:///C:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md#L75) (v1.1.0 §4.2):
> *"Sampling Rate Conversion: AnoMod Prometheus scrapes are collected at $\Delta t = 15\text{ seconds}$. Telemetry will be resampled to $\Delta t = 5\text{ seconds}$ via linear interpolation, or sliding window length will be set to $W = 8$ steps (preserving the $120\text{-second}$ temporal horizon: $8 \times 15\text{s} = 120\text{s}$)."*

The harness authors recognized that AnoMod scraped Prometheus metrics every 15 seconds. To match the $120\text{-second}$ physical duration of the training sequences ($24 \times 5\text{s} = 120\text{s}$), they set $W = 120 / 15 = 8$ discrete steps.

### 2.2 Why $W=8$ is an Off-Contract Diagnostic (Not Supported Inference)
Although $8 \times 15\text{s} = 120\text{s}$ matches physical duration, recurrent neural networks operate on **discrete sequential steps**, not physical continuous time.

1. **Architectural Internal Mechanics**:
   - Encoder: `nn.LSTM(5, 16)`.
   - Hidden representation: `latent = hidden[-1].unsqueeze(1).repeat(1, x.size(1), 1)` ([`dl/anomaly_detector.py:30`](file:///C:/DL_PROJECT/dl/anomaly_detector.py#L30)).
   - In training, the hidden vector $h_{24} \in \mathbb{R}^{16}$ absorbed 24 sequential state transitions.
   - On $W=8$, the encoder only executes 8 transitions. The latent vector $h_8$ has never been learned or calibrated.
   - The decoder unfolds for 8 steps instead of 24 steps, repeating $h_8$ only 8 times.
2. **Reconstruction Score Measurement Shift**:
   In our isolated empirical benchmark (`scratch_score_semantics.py`), feeding the exact same normalized telemetry into the autoencoder yielded:
   - Reconstruction score on $W=8$: **$0.339067$**
   - Reconstruction score on $W=24$: **$0.239059$**
   - **Score Shift**: $+41.8\%$ inflation on $W=8$ simply due to sequence truncation.
   The reconstruction error measurement is mathematically dependent on sequence length.
3. **Bypassing the Inference Contract**:
   To execute $W=8$, `run_experiment_d.py:590-596` directly accesses private member `detector.model(w_tensor)`, bypassing `detector.detect()`.
   **Finding**: The 8-step scoring procedure is **not a supported model inference path** under the frozen contract. It is an **off-contract diagnostic bypass**.

---

## 3. Data Availability Audit: Why Contiguous $W=24$ Windows Do Not Exist

Could the harness simply use $W = 24$ on AnoMod at 15-second intervals ($24 \times 15\text{s} = 360\text{s}$)?

The empirical audit in [`EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md`](file:///C:/DL_PROJECT/research/audits/EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md) examined all 80 raw intervals of SocialNetwork `Normal_Baseline`:
- Distributed traces contain 23 intervals with zero trace spans. Only 57 complete intervals exist.
- Complete intervals cluster into 3 contiguous runs without gaps:
  - Run 1 (Rows 36..46): 11 intervals (165 seconds)
  - Run 2 (Rows 48..58): 11 intervals (165 seconds)
  - Run 3 (Rows 60..77): 18 intervals (270 seconds)
- **Result for $W = 24$**: The longest contiguous run is 18 intervals.
  $$\text{Eligible } W=24 \text{ Windows in SocialNetwork Normal Baseline} = \mathbf{0}$$
- In TrainTicket `Normal_case`, there is only a single active run of 15 intervals ($15 < 24$).
  $$\text{Eligible } W=24 \text{ Windows in TrainTicket Normal Baseline} = \mathbf{0}$$

**Conclusion**: Under strict zero-imputation rules (Research Integrity Rule 4), **it is mathematically impossible to construct even a single valid $W=24$ window from the real AnoMod nominal baseline**.

---

## 4. Evaluation of the Three Proposed Reporting Modalities

| Evaluation Dimension | Modality 3A: Pure Zero-Shot Transfer | Modality 3B: Threshold-Free Ranking (ROC-AUC) | Modality 3C: Target-Calibrated Exploratory |
| :--- | :--- | :--- | :--- |
| **Model Contract Compatibility** | **FATAL INCOMPATIBILITY**: Requires $W=24$ (0 windows exist) or $W=8$ (off-contract diagnostic). $\tau=0.7094$ calibrated on $W=24$. | **OFF-CONTRACT DIAGNOSTIC**: Does not use $\tau=0.7094$, but still relies on off-contract 8-step model scoring. | **FATAL INCOMPATIBILITY**: Abandons frozen scaler and threshold; off-contract 8-step scoring. |
| **Data Availability ($W=24$)** | **0 Normal Windows**; 0 Fault Windows. Unexecutable. | **0 Normal Windows**; 0 Fault Windows. Unexecutable. | **0 Normal Windows**; 0 Fault Windows. Unexecutable. |
| **Data Availability ($W=8$)** | 19 Normal Windows; 303 Fault Windows. | 19 Normal Windows; 303 Fault Windows. | 5 Calib Windows; 8 Val Windows; 303 Fault Windows. |
| **Calibration Leakage Status** | **Avoided** (zero target fitting). | **Avoided** (zero target fitting). | **FATAL RISK**: 5-window variance collapse ($\sigma \to 10^{-6}$), or circular leakage ($0\%$ FPR). |
| **Nominal False Alarm Rate** | **100.0% (19/19 flagged)** due to severe domain shift ($\mu_{\text{lat}}=10\text{ms}$ vs $76.9\text{ms}$). | N/A (continuous score evaluated across all thresholds). | $\text{FPR} = 0.0\%$ by circular leakage, or $100\%$ by variance collapse. |
| **Scientifically Defensible Claims** | Can only claim: *"Model fails to transfer zero-shot due to extreme domain shift and sequence length incompatibility."* | Can claim: *"Off-contract 8-step reconstruction scores rank fault windows relative to nominal traffic with exploratory AUC."* | **None**. Mathematically degenerate and scientifically indefensible. |
| **Execution Recommendation** | **REJECT AS PRODUCTION TEST** (trivial constant-positive detector). | **VIABLE ONLY AS FORMALLY DISCLOSED EXPLORATORY DIAGNOSTIC**. | **REJECT ENTIRELY** (unscientific and mathematically broken). |

---

## 5. Statistical Validity of the 19 Nominal Windows

Can the 19 nominal windows ($W=8$) support inferential statistical claims regarding operational false alarms?

1. **Extreme Temporal Autocorrelation**:
   - The 19 windows derive from only 3 contiguous runs ($4 + 4 + 11$ windows).
   - Adjacent windows advance by $\Delta t = 15\text{s}$, sharing 7 out of 8 observations (**87.5% shared telemetry**).
   - In the validation partition, all 8 windows derive from a single 3.5-minute sequence (15 timestamps).
2. **Single Execution Run**:
   - Telemetry originates from a single cluster execution (`Normal_Baseline_20251103_220228`).
   - The effective independent sample size ($N_{\text{eff}}$) is approximately 1.
3. **Statistical Uncertainty**:
   - The Wilson 95% Score Confidence Interval for $0/8$ false alarms is $[0.0\%, 32.4\%]$ (a $12.5\%$ discrete step per false alarm).
   - The Wilson 95% Score Confidence Interval for $0/19$ false alarms is $[0.0\%, 16.8\%]$ (a $5.3\%$ discrete step per false alarm).
4. **Mandatory Reporting Boundary**:
   - No operational certification of False Alarm Rate (e.g. false alarms per day/week) is statistically defensible from 10 minutes of active telemetry.
   - Any inferential confirmatory hypothesis regarding false positive rates must be strictly withheld.

---

## 6. Audit Verdict and Recommendation

### Audit Verdict: `BLOCKED — MODEL CONTRACT INCOMPATIBILITY`

**Reasoning**:
1. The frozen model contract strictly mandates $W = 24$.
2. The external benchmark dataset contains **0 contiguous 24-step nominal windows**.
3. Bypassing the contract to evaluate on $W = 8$ is an **off-contract diagnostic**, not supported inference.
4. Pure zero-shot transfer (Modality 3A) produces a 100% false alarm rate due to severe domain shift.
5. Target calibration (Modality 3C) produces fatal variance collapse or circular leakage.
6. The only scientifically defensible use of the external benchmark is **Modality 3B (Threshold-Free Ranking)** treated strictly as an **exploratory off-contract diagnostic**, requiring formal protocol amendment and withdrawal of confirmatory claims.

Production execution of Experiment D remains **STRICTLY BLOCKED**.
