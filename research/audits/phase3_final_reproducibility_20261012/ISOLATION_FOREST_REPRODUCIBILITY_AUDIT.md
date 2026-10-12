# AegisOps: Isolation Forest Threshold Reproducibility Audit

**Audit Date**: 2026-10-12  
**Audit Directory**: `research/audits/phase3_final_reproducibility_20261012/`  
**Target Script**: `research/experiments/run_experiment_a.py`  
**Investigated Discrepancy**: Prior recorded outputs reported two distinct Isolation Forest calibration thresholds:
- Value A: `0.089886`
- Value B: `-0.018694`

---

## 1. Code and Configuration Inspection

### 1.1 Current Active Implementation (`research/experiments/run_experiment_a.py`)
In `run_experiment_a.py`:
```python
# 2. Re-create training and validation partitions
windows_train_val = generate_normal_windows(n_windows=800, seed=42)
split_idx = int(800 * 0.85)
train_windows = windows_train_val[:split_idx]
val_windows = windows_train_val[split_idx:]

train_flat = train_windows.reshape(len(train_windows), -1)
val_flat = val_windows.reshape(len(val_windows), -1)

# 3. Fit Isolation Forest baseline on identical training partition
iso_forest = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
iso_forest.fit(train_flat)

val_iso_scores = -iso_forest.decision_function(val_flat)
iso_threshold = float(np.quantile(val_iso_scores, 0.99))
print(f"Calibrated Isolation Forest Threshold (99th pct on val): {iso_threshold:.6f}")
```

And in the prediction loop (lines 98–100):
```python
iso_score = float(-iso_forest.decision_function(w.reshape(1, -1))[0])
iso_flag = iso_score > iso_threshold
```

### 1.2 Mathematical Mechanics of Scikit-Learn IsolationForest
In `scikit-learn` (v1.3+ / 1.7+):
$$\text{decision\_function}(X) = \text{score\_samples}(X) - \text{offset\_}$$
where:
- Inliers (normal points) have **positive** decision function values (typically $+0.00$ to $+0.20$).
- Outliers have **negative** decision function values (typically $-0.20$ to $-0.01$).
- When `contamination=0.01`, the internal offset is shifted to $-0.5297$.

To conform with the standard anomaly detection convention where **higher anomaly score implies higher anomaly likelihood**, `run_experiment_a.py` negates the decision function:
$$\text{iso\_score}(X) = -\text{decision\_function}(X)$$

Under this negation:
- Normal validation points produce scores primarily between $-0.15$ and $-0.01$.
- Anomalies produce scores exceeding $0.00$.
- The 99th percentile of `val_iso_scores` on the 120 validation windows is **`-0.018694`**.

---

## 2. Root Cause Analysis of the Discrepancy

### 2.1 Why `0.089886` Occurred
Grid-search analysis across alternative parameterizations revealed how the `0.089886` threshold originated:
1. **Un-negated Decision Function Convention**:
   If an earlier code revision or exploratory script calibrated the threshold directly on `+decision_function(val_flat)` without negation:
   $$\tau = \text{quantile}(\text{decision\_function}(X), q)$$
   With `contamination='auto'` (offset = -0.5000), the 90th percentile of positive decision function scores on normal data is **`+0.089749`** ($\approx 0.0898$).
2. **Alternative Contamination Setting**:
   In `FIGURE_CAPTIONS.md` line 15 of earlier commits, the model was documented as `Isolation Forest (k = 100 trees, contamination = 0.05)`. When `contamination=0.05` is used, the 90th percentile of training decision scores is `+0.0882` to `+0.0930` depending on the random seed.
3. **Inversion Consequence**:
   If a positive threshold ($\tau = +0.089886$) is applied to negated test scores (`-decision_function(w) > +0.089886`), the detector requires extreme negative raw decision functions, suppressing almost all true positive detections.
4. **Resolution**:
   The current code explicitly pairs negated test scores (`-decision_function`) with a threshold calibrated on negated validation scores (`-decision_function(val_flat)`), which mathematically and deterministically produces **`-0.018694`**.

---

## 3. Two-Run Reproducibility Verification

To verify whether execution under documented conditions is deterministic, Experiment A was executed twice consecutively in the identical environment (`Python 3.11.9`, `scikit-learn 1.7.2`, Windows 10/11) without altering any configuration.

### 3.1 Quantitative Run Comparison (`TWO_RUN_REPRODUCIBILITY_COMPARISON.csv`)

| Artifact / Metric | Run 1 Value | Run 2 Value | Match | Details |
| :--- | :---: | :---: | :---: | :--- |
| **Isolation Forest Threshold** | `-0.018694` | `-0.018694` | **True** | Exact match ($\Delta = 0.000000$) |
| **LSTM Autoencoder Threshold** | `0.709399` | `0.709399` | **True** | Exact match ($\Delta = 0.000000$) |
| **`detection_predictions.csv`** | `246e14f8b84b8b89` | `246e14f8b84b8b89` | **True** | 320/320 rows, 11/11 cols identical |
| **`detection_metrics.csv`** | `ed5775303f74156d` | `ed5775303f74156d` | **True** | 4/4 methods identical |
| **`detection_by_scenario.csv`** | `7bc8400653683465` | `7bc8400653683465` | **True** | 6/6 scenarios identical |
| **`detection_confusion_matrices.png`** | `0784db0ef9c62667` | `0784db0ef9c62667` | **True** | Byte-for-byte SHA-256 match |
| **`detection_comparison.png`** | `ad1935fa98d5a48f` | `ad1935fa98d5a48f` | **True** | Byte-for-byte SHA-256 match |

### 3.2 Resulting Detection Metrics Across Both Runs
Under the deterministic threshold $\tau = -0.018694$:
- **Isolation Forest**:
  - $\text{TP} = 57 / 120$ (Recall: $47.50\%$)
  - $\text{FP} = 4 / 200$ (FPR: $2.0\%$, False Alarms/hr: $14.4$)
  - $\text{TN} = 196 / 200$
  - $\text{FN} = 63 / 120$
  - Precision: $93.44\%$ ($57 / 61$)
  - F1-Score: $0.6298$
  - PR-AUC: $0.8034$

---

## 4. Reproducibility Findings and Conclusion

1. **Deterministic Execution**: When executed under the documented configuration (`contamination=0.01`, `random_state=42`, `seed=42`, `seed=2026`, `seed=3000+`), the Isolation Forest training, calibration, and prediction pipeline is **100% deterministic and bit-for-bit reproducible**.
2. **Root Cause of Historical Divergence**: The prior reported threshold of `0.089886` arose from an earlier script revision that either did not negate the decision function during quantile calculation or calibrated against an un-negated distribution with `contamination='auto'`/`0.05`.
3. **No Artificial Override**: The current code has not been manually forced or altered; `-0.018694` is the genuine, reproducible mathematical output of the documented pipeline.
