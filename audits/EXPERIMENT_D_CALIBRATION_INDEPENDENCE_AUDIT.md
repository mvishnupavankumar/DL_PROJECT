# AegisOps: Experiment D Calibration-Independence and Lifecycle Audit

**Document Path**: `research/audits/EXPERIMENT_D_CALIBRATION_INDEPENDENCE_AUDIT.md`  
**Date**: October 13, 2026  
**Auditor**: Senior ML Research Engineer, Statistical Auditor & Reproducibility Reviewer  
**Repository**: `C:\DL_PROJECT` (Git HEAD: `d277c1df3c2599ddecdf5f0bb761c99718499667`, Branch: `main`)  
**Active Python Runtime**: `C:\DL_PROJECT\.venv\Scripts\python.exe` (Python 3.11.9, PyTorch 2.14.1+cpu)  
**Standard**: Non-Negotiable Research Integrity Rules & Pre-Registered Protocol v1.1.0  
**Audit Verdict**: **`BLOCKED — CALIBRATION OR STATISTICAL VALIDITY DEFECT`**

---

## 1. Executive Verdict & Core Findings

An independent, skeptical audit of the Experiment D calibration pipeline, data-use lifecycle, and empirical telemetry statistics was conducted. 

### Critical Audit Findings:
1. **Calibration / Evaluation Leakage Defect Identified in Source Code**:
   In `research/experiments/run_experiment_d.py`, the nominal validation partition (`v_win`, $N_{\text{val}} = 8$ windows) is utilized at line 550 to calibrate the anomaly threshold (`calibrate_threshold(detector.model, v_win, percentile=99.0)`), and then **evaluated at line 566 as the negative test population** (`eval_scenarios["Normal_Validation"] = (v_win, 0)`) to compute the final False Positive Rate (FPR) and Specificity. Calibrating an empirical 99th percentile threshold on an 8-window sample and then evaluating false alarms on that exact same sample guarantees a circular, overfitted result ($\text{FPR} = 0.0\%$, $\text{Specificity} = 100.0\%$).
2. **Empirical Variance Collapse & Numerical Blowup Defect in Domain Z-Score**:
   Live empirical calculation on the actual SocialNetwork `Normal_Baseline` reveals that steady-state microservice variance across calibration windows is near-zero:
   - `error_rate_pct`: $\hat{\sigma} = 0.0$ (clipped to $10^{-6}$ epsilon).
   - `system_disk_usage_percent`: $\hat{\sigma} = 0.00064\%$ ($6.4 \times 10^{-4}$).
   - `system_memory_usage_percent`: $\hat{\sigma} = 0.0188\%$.
   Dividing by these near-zero calibration variances during inference transforms a tiny $1.0\%$ error rate increase into an astronomical **$+1,000,000\sigma$ outlier**, and a $1.0\%$ disk increase into a **$+1,562\sigma$ outlier**, causing extreme activation saturation, numerical instability, and explosive reconstruction loss in the LSTM autoencoder.
3. **Extreme Test Set Imbalance & Granularity Bound**:
   The test population consists of **303 fault windows** and only **8 normal validation windows** (a $37.9:1$ class ratio, or **$97.43\%$ fault prevalence**). With $N_{\text{val}} = 8$, the empirical false positive rate has a coarse discrete step-size of **$12.5\%$ per false alarm**, and the 95% Wilson confidence interval for $0/8$ is $[0.0\%, 32.4\%]$, making operational false alarm claims statistically unresolvable.

---

## 2. Complete Data-Use Lifecycle Trace

| Stage & Operation | Input Observations | Labels Accessible | Output Artifact / Tensor | Downstream Use in Code | Code Citation |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **1. Feature Extraction** | Raw CSVs in `SN_data/metric_data` and trace spans in `SN_data/trace_data` | **NONE** | Multi-metric DataFrame (15s grid: CPU, Mem, Disk, Latency, Error Rate) | Chronological partitioning or contiguous window construction | `run_experiment_d.py:139-222` |
| **2. Chronological Normal Partitioning** | `df_normal` from `Normal_Baseline` (80 raw 15s intervals) | **NONE** (assumed nominal by directory name) | `calib_raw` (rows 0–55), `purge_gap` (rows 56–62), `val_raw` (rows 63–79) | Fed separately into `build_contiguous_windows()` | `run_experiment_d.py:391-432` |
| **3. Contiguous Window Construction** | `calib_raw`, `val_raw`, and 12 `df_fault` DataFrames | **NONE** | `calib_windows` $(5, 8, 5)$, `val_windows` $(8, 8, 5)$, `fault_scenarios_dict` (12 scenarios, 303 windows) | Fed into calibration and evaluation pipeline | `run_experiment_d.py:335-389` |
| **4. Normalization Scaler Fitting** | `c_win` = `calib_windows` ($N=5$ windows, 40 time steps) | **NONE** | 5-D vectors `mean`, `std` | Standardizes `v_win` (line 461) and all evaluation windows (line 590) | `run_experiment_d.py:436-448, 549` |
| **5. LSTM Threshold Calibration** | `detector.model`, `v_win` = `val_windows` ($N=8$ windows), `mean`, `std` | **NONE** | Scalar `lstm_threshold` (99th percentile of reconstruction errors on `v_win`) | Decision boundary for LSTM in line 596: `lstm_score > lstm_threshold` | `run_experiment_d.py:451-470, 550` |
| **6. Isolation Forest Fitting & Thresholding** | `c_flat` ($(5, 40)$), `v_flat` ($(8, 40)$) | **NONE** | Fitted `IsolationForest` estimator and `iso_threshold` (99th percentile on `v_flat`) | Decision boundary for IF in line 586: `iso_score > iso_threshold` | `run_experiment_d.py:552-559` |
| **7. Inference & Prediction Generation** | `v_win` ($N=8$), 12 fault scenarios (303 windows), all 5 detectors | Ground truth label assigned: $y=0$ for `Normal_Validation`, $y=1$ for fault scenarios | `df_preds` DataFrame with predictions across 5 detectors for 311 windows | Serialized to `external_anomod_predictions.csv` | `run_experiment_d.py:560-619` |
| **8. Performance Metrics Calculation** | `df_preds["ground_truth"]`, `df_preds[flag_col]` | Full ground truth labels ($y \in \{0, 1\}$) | Contingency matrices (TP, FP, TN, FN) and metrics (Recall, Precision, FPR, F1) | Serialized to `external_anomod_metrics.csv` | `run_experiment_d.py:620-639` |
| **9. Hypothesis Testing** | Paired detector flags across rows in `df_preds`; scenario-level recall arrays | Full ground truth labels | McNemar exact two-sided p-value; scenario-level Wilcoxon p-value | Serialized to `experiment_d_manifest.json` | `run_experiment_d.py:642-659` |

---

## 3. The Calibration / Evaluation Leakage Defect

### 3.1 Code Trace of the Defect

In `research/experiments/run_experiment_d.py`:

```python
# Line 550: Threshold is calibrated strictly using validation windows v_win
lstm_threshold = calibrate_threshold(detector.model, v_win, mean, std, percentile=99.0)

# Line 558: Isolation Forest threshold calibrated strictly using validation windows v_flat
iso_threshold = float(np.percentile(v_iso_scores, 99.0))

# Line 566: The SAME validation windows v_win are inserted into the evaluation set as negative instances
if include_val_in_predictions and len(v_win) > 0:
    eval_scenarios["Normal_Validation"] = (v_win, 0)

# Lines 578-597: Each window w in v_win is scored against the threshold chosen on v_win
lstm_score = float(np.square(reconstructed - w_scaled).mean())
lstm_flag = lstm_score > lstm_threshold

# Lines 630-633: False Positives (FP) and True Negatives (TN) computed on the same v_win
fp = int(np.sum((y_true == 0) & (y_pred == 1)))
tn = int(np.sum((y_true == 0) & (y_pred == 0)))
fpr = fp / (fp + tn)
```

### 3.2 Mathematical Mechanism of Guaranteed 0% False Positive Rate

When `percentile=99.0` is evaluated on an array of length $N = 8$:
- The 99th percentile in `numpy.percentile` is computed via linear interpolation between index 6 and index 7 (the two highest scores in the 8-window sample).
- Because `lstm_flag` requires `lstm_score > lstm_threshold`:
  - Exactly **zero** observations in `v_win` can exceed this interpolated 99th percentile threshold.
  - Consequently, `fp` is guaranteed to be $0$, `tn` is guaranteed to be $8$, and the reported $\text{FPR} = 0 / 8 = 0.0\%$.
- **Scientific Conclusion**: This is circular calibration/evaluation data contamination. The evaluation set is identical to the validation set used to fit the decision boundary.

---

## 4. The Near-Zero Calibration Variance Defect

### 4.1 Empirical Findings on `Normal_Baseline`

Executing `fit_calibration_scaler()` directly on the active SocialNetwork `Normal_Baseline` yields:

$$\hat{\boldsymbol{\mu}}_{\text{calib}} = [3.5515\%, 8.5443\%, 10.3870\text{ ms}, 0.0000\%, 37.8567\%]$$
$$\hat{\boldsymbol{\sigma}}_{\text{calib}} = [0.2570, 0.0188, 4.7935, 1.0000\times 10^{-6}, 0.00064]$$

### 4.2 Impact on Model Inputs and Activations

| Feature | Baseline Mean ($\mu$) | Baseline Std ($\sigma$) | Simulated Fault Value ($x$) | Z-Score into LSTM: $(x - \mu)/\sigma$ | Trained Feature Std ($\sigma_{\text{train}}$) | Expected Model Dynamic | Real Consequence |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`error_rate_pct`** | $0.0\%$ | $10^{-6}$ (clipped) | $1.0\%$ | $\mathbf{+1,000,000.0\sigma}$ | $0.0550$ | Linear/tanh response for $[-3\sigma, +3\sigma]$ | Immediate numerical overflow / loss $\sim 10^{12}$ |
| **`disk_pct`** | $37.86\%$ | $0.00064$ | $38.86\%$ ($+1.0\%$) | $\mathbf{+1,561.7\sigma}$ | $4.3354$ | Smooth capacity tracking | Explosive reconstruction error on nominal writes |
| **`memory_pct`** | $8.54\%$ | $0.0188$ | $10.54\%$ ($+2.0\%$) | $\mathbf{+106.4\sigma}$ | $3.5649$ | Smooth memory tracking | Massive false alarm on minor heap allocations |
| **`cpu_pct`** | $3.55\%$ | $0.2570$ | $20.0\%$ | $\mathbf{+64.0\sigma}$ | $5.7859$ | Smooth CPU tracking | Severe over-sensitivity to minor load blips |

### 4.3 Why Unregularized Domain Z-Score Fails

Domain Z-Score relies on the fundamental assumption that the calibration sample captures the full natural variance of normal operations. In a 20-minute synthetic benchmark run:
- No background batch jobs or log rotations occur, so disk usage has zero natural variance.
- No client errors or server 5xx errors occur, so error rate has zero natural variance.
Dividing by empirical sample variance fit on 5 windows converts the model into an ultra-brittle hypersensitive detector where even a single byte written to disk produces a $1,500\sigma$ alert.

---

## 5. Negative Population Accounting and Class Imbalance

### 5.1 Quantifying the Consequences of $N_{\text{val}} = 8$

If `v_win` were held out as an independent negative evaluation set (assuming threshold was calibrated elsewhere):
- Sample size: $N_{\text{val}} = 8$ normal windows.
- Discrete FPR resolution: $1 / 8 = \mathbf{12.5\%}$ per false alarm.

| Number of False Alarms in 8 Windows | Empirical FPR | Empirical Specificity | 95% Wilson Score Confidence Interval for FPR | Operational Significance |
| :---: | :---: | :---: | :---: | :--- |
| **0 / 8** | **0.0%** | **100.0%** | $[0.000, 0.324]$ ($0.0\%$ to $32.4\%$) | Indeterminate. Cannot prove FPR $\le 1.0\%$. |
| **1 / 8** | **12.5%** | **87.5%** | $[0.022, 0.471]$ ($2.2\%$ to $47.1\%$) | Catastrophic in production ($>10\%$ alert storm). |
| **2 / 8** | **25.0%** | **75.0%** | $[0.071, 0.591]$ ($7.1\%$ to $59.1\%$) | Alert storm. |
| **3 / 8** | **37.5%** | **62.5%** | $[0.137, 0.694]$ ($13.7\%$ to $69.4\%$) | Unusable. |

### 5.2 The 97.4% Class Imbalance Distortion

The evaluation set contains:
- 303 Fault Windows ($y = 1$)
- 8 Normal Windows ($y = 0$)
- Total: 311 Windows (Prevalence = $303 / 311 = 97.43\%$).

A dummy constant classifier that predicts $\hat{y} = 1$ unconditionally achieves:
$$\text{Recall} = \frac{303}{303} = 100.0\%$$
$$\text{Precision} = \frac{303}{303 + 8} = 97.43\%$$
$$\text{F1} = 2 \cdot \frac{0.9743 \cdot 1.0}{0.9743 + 1.0} = \mathbf{0.9870}$$

**Auditor Conclusion**: Evaluating on a test set with 97.4% fault windows makes Precision and F1 completely insensitive to false alarms. Precision and F1 cannot be used as primary confirmatory metrics under this class distribution.

---

## 6. Feasible Methodological Remediation Options

| Remediation Option | Mathematical Implementation | Pros & Cons | Requires Protocol Amendment? | Feasibility Assessment |
| :--- | :--- | :--- | :---: | :--- |
| **Option A: Regularized Domain Z-Score with Variance Floor** | $\tilde{\mathbf{x}}_t = \frac{\mathbf{x}_t - \hat{\boldsymbol{\mu}}_{\text{calib}}}{\max(\hat{\boldsymbol{\sigma}}_{\text{calib}}, \boldsymbol{\sigma}_{\min})}$, where $\boldsymbol{\sigma}_{\min} = \boldsymbol{\sigma}_{\text{train}}$ | Prevents million-sigma blowup; bounds sensitivity to training distribution scale. | **YES (Amendment v1.2.1)** | **HIGHLY RECOMMENDED TECHNICAL FIX** |
| **Option B: Three-Way Normal Split (Calib / Val / Test)** | 50% Calib ($N=2$ wins), 25% Val ($N=1$ win), 25% Test ($N=1$ win) | Eliminates leakage; mathematically disjoint. | **YES (Amendment v1.2.1)** | **IMPOSSIBLE**: 19 total windows cannot support a 3-way split with statistical power. |
| **Option C: Pure Zero-Shot Transfer (Frozen Training Scaler & Threshold)** | $\tilde{\mathbf{x}}_t = \frac{\mathbf{x}_t - \boldsymbol{\mu}_{\text{train}}}{\boldsymbol{\sigma}_{\text{train}}}$, $\tau = 0.709399$ | Zero external fitting; zero leakage; evaluates true transfer. Baseline shift becomes part of reported domain gap. | **YES (Amendment v1.2.1)** | **SCIENTIFICALLY DEFENSIBLE BENCHMARK** |
| **Option D: Reclassify External Validation as Exploratory Sensitivity Study** | Acknowledge that AnoMod provides insufficient nominal exposure ($N=8$) to confirm low false alarms. Restrict confirmatory claims to synthetic experiment. | Preserves scientific integrity; prevents false generalization claims. | **YES (Amendment v1.2.1)** | **MANDATORY SCIENTIFIC POSTURE** |

---

## 7. Audit Verdict

```
BLOCKED — CALIBRATION OR STATISTICAL VALIDITY DEFECT
```

**Justification**:
1. Calibrating the threshold on `v_win` and evaluating false alarms on `v_win` constitutes circular calibration/evaluation leakage.
2. Unregularized Domain Z-Score standard deviation collapse ($\sigma = 10^{-6}$) causes million-sigma numerical explosions.
3. An 8-window negative test population ($97.4\%$ fault prevalence) cannot support operational false alarm rate claims.
Execution must remain **STRICTLY BLOCKED** until these defects are formally resolved in an amended protocol.
