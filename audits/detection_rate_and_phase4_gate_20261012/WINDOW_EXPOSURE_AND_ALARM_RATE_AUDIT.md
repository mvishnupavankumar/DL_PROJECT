# AegisOps: Window Construction, Exposure, and Alarm Rate Audit

**Audit Gate**: Final Detection Rate Audit and Phase 4 Readiness Gate  
**Audit Date**: 2026-10-12  
**Audit Directory**: `research/audits/detection_rate_and_phase4_gate_20261012/`  
**Inspected Source Files**:
- `dl/anomaly_detector.py` (`generate_normal_windows`, `generate_incident_telemetry`)
- `research/experiments/run_experiment_a.py` (Evaluation loop, lines 80–120)
- `research/results/detection_predictions.csv` ($N = 320$ evaluation rows)
- `research/results/detection_metrics.csv`

---

## 1. Window Construction and Telemetry Generation Audit

### 1.1 Non-Overlapping Independent Window Generation
Inspection of `dl/anomaly_detector.py` lines 35–64 reveals the exact window construction logic:
```python
def generate_normal_windows(
    n_windows: int = 800,
    sequence_length: int = SEQUENCE_LENGTH,  # 24 steps
    seed: int = 42,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    t = np.arange(sequence_length, dtype=np.float32)
    data = np.zeros((n_windows, sequence_length, len(FEATURES)), dtype=np.float32)

    for i in range(n_windows):
        phase = rng.uniform(0, 2 * np.pi)
        cpu_base = rng.normal(42, 4)
        mem_base = rng.normal(54, 3)
        disk_base = rng.normal(47, 4)
        cpu = cpu_base + 5.0 * np.sin(t / 4 + phase) + rng.normal(0, 2.2, sequence_length)
        # ...
        data[i, :, 0] = np.clip(cpu, 15, 75)
        # ...
    return data
```

**Key Architectural Facts**:
1. **Zero Window Overlap**: Each window $i \in \{0, \dots, N-1\}$ is generated with its own freshly sampled random phase (`rng.uniform(0, 2*pi)`), distinct baseline offsets (`cpu_base`, `mem_base`, `disk_base`), and independent Gaussian noise.
2. **No Continuous Streaming Series**: The 200 normal test windows (`seed=2026`) are **not** extracted via a sliding window over a continuous time series. They are 200 independent synthetic draws from the normal telemetry generator.
3. **Temporal Duration per Window**: Each window consists of $L = 24$ discrete time steps. With a documented sampling interval of $\Delta t = 5.0\text{ seconds}$, each window represents:
   $$\text{Duration per window} = 24 \text{ steps} \times 5.0\text{ s/step} = 120.0\text{ seconds (2 minutes)}$$

---

## 2. Telemetry Exposure Quantification

The true observation exposure across the evaluation set is quantified below:

| Telemetry Cohort | Window Count ($N$) | Steps per Window ($L$) | Total Observations | Sampling Interval ($\Delta t$) | Total Exposure (Seconds) | Total Exposure (Hours) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Normal Test Windows** | 200 | 24 | 4,800 steps | 5.0 s | **24,000 s** | **6.6667 hours** |
| **Incident Test Windows** | 120 | 24 | 2,880 steps | 5.0 s | **14,400 s** | **4.0000 hours** |
| **Complete Evaluation Suite** | **320** | **24** | **7,680 steps** | **5.0 s** | **38,400 s** | **10.6667 hours** |

---

## 3. Deconstruction of the "False Alarms per Hour" Metric

### 3.1 The Prior Formula and Its Implicit Assumptions
In `research/experiments/run_experiment_a.py` line 147, the false alarm rate was computed as:
```python
fa_rate = fp / len(test_normal_windows)  # fp / 200
fa_per_hour = fa_rate * (3600.0 / 5.0)   # (fp / 200) * 720
```
This calculation evaluated:
- For LSTM Autoencoder ($\text{FP} = 2$): $\frac{2}{200} \times 720 = 0.010 \times 720 = \mathbf{7.20\text{ false alarms / hour}}$
- For Isolation Forest ($\text{FP} = 4$): $\frac{4}{200} \times 720 = 0.020 \times 720 = \mathbf{14.40\text{ false alarms / hour}}$
- For Full Operational Rules ($\text{FP} = 0$): $\frac{0}{200} \times 720 = \mathbf{0.00\text{ false alarms / hour}}$

### 3.2 Methodological Flaw in Multiplying by 720
Multiplying the per-window False Positive Rate ($\text{FPR} = \text{FP}/200$) by 720 implicitly assumes:
1. **Streaming Sliding Inferences**: A window inference is evaluated once every 5 seconds (i.e., a sliding window with stride = 1 step = 5 s).
2. **Every Flagged Window Emits an Independent Alarm**: There is zero operational alert suppression, zero cooldown period, and zero deduplication across overlapping windows.
3. **Equivalence of Window Errors to Streaming Errors**: It assumes that the error rate measured on 200 independent 2-minute batch windows is identical to the consecutive error rate on 720 overlapping sliding windows.

**Why this assumption is invalid for Experiment A**:
- Experiment A evaluated **batch-level independent 24-step sequences**, not a continuous 1-step sliding stream.
- In actual production operations, consecutive sliding windows covering the same transient disturbance are deduplicated into a single operational incident alarm (e.g. by requiring $k$-of-$m$ consecutive windows or a 5-minute cooldown timer).
- If evaluated strictly as independent batch exposures ($24,000\text{ seconds} = 6.67\text{ hours}$ total observation time), 2 false positive windows over 6.67 hours of normal telemetry corresponds to:
  $$\text{Empirical FP per Exposure Hour} = \frac{2\text{ false positives}}{6.6667\text{ hours}} = \mathbf{0.30\text{ FP / exposure hour}}$$
  and for Isolation Forest ($4\text{ FP}$):
  $$\text{Empirical FP per Exposure Hour} = \frac{4\text{ false positives}}{6.6667\text{ hours}} = \mathbf{0.60\text{ FP / exposure hour}}$$

---

## 4. Operational Alarm Mapping Reality Check

### 4.1 Window-Level Flag vs. Incident Alarm
In this experiment:
- Each sample $j$ produces a binary flag $\hat{y}_j \in \{0, 1\}$.
- A false positive indicates that an entire 24-step normal window had reconstruction error exceeding the threshold ($\text{MSE} > 0.709399$).
- Because the evaluation dataset contains no timestamps connecting window $j$ to window $j+1$ in a continuous timeline, **operational alarm frequency cannot be empirically established**.

### 4.2 Status Determination
In accordance with mandatory audit rules:
- **Operational False Alarms per Hour**: Marked **`UNAVAILABLE`** in formal reporting.
- **Empirical Batch FP Rate per Exposure Hour**: $0.30\text{ FP/hr}$ (LSTM) and $0.60\text{ FP/hr}$ (IsoForest), noted strictly as an empirical exposure rate over 6.67 hours of non-overlapping normal telemetry.
- **Primary Supported Statistical Metric**: **False Positive Window Rate ($\text{FPR}_{\text{window}}$)**:
  - Full Operational Rules: $\text{FPR} = 0.0\%$ ($0/200$, 95% Wilson CI: $[0.0000, 0.0186]$)
  - LSTM Autoencoder: $\text{FPR} = 1.0\%$ ($2/200$, 95% Wilson CI: $[0.0027, 0.0357]$)
  - Isolation Forest: $\text{FPR} = 2.0\%$ ($4/200$, 95% Wilson CI: $[0.0078, 0.0503]$)
