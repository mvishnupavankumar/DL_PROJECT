# 02 — Data and Label Reconciliation

**Audit Date**: 2026-10-12  
**Auditor**: Senior ML Data Auditor & Experiment Integrity Specialist  
**Target Database**: [`data/aegisops_live.sqlite3`](file:///c:/DL_PROJECT/data/aegisops_live.sqlite3)  
**Export Files**: [`research/exports/telemetry.csv`](file:///c:/DL_PROJECT/research/exports/telemetry.csv), [`research/exports/incident_episodes.csv`](file:///c:/DL_PROJECT/research/exports/incident_episodes.csv), [`research/exports/incident_events.csv`](file:///c:/DL_PROJECT/research/exports/incident_events.csv)  
**Row-Level Mapping**: [`research/audits/reconciliation_gate_20261012/DATA_ROW_RECONCILIATION.csv`](file:///c:/DL_PROJECT/research/audits/reconciliation_gate_20261012/DATA_ROW_RECONCILIATION.csv)

---

## 1. Verified Schema & Table Inventory

The SQLite database `data/aegisops_live.sqlite3` (86,016 bytes, SHA-256: `b8f33f63116ca4d081b8544f128e4e941ce0ce6fef39ff4f7e2c918ee0e94ff1`) was queried directly via SQLite catalog metadata:

### A. Table `telemetry_samples` (Exactly 200 Rows)
```sql
CREATE TABLE telemetry_samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    cpu_pct REAL NOT NULL,
    memory_pct REAL NOT NULL,
    latency_ms REAL NOT NULL,
    error_rate_pct REAL NOT NULL,
    disk_pct REAL NOT NULL,
    status_code INTEGER NOT NULL,
    service_available INTEGER NOT NULL,
    fault_mode TEXT NOT NULL,
    data_source TEXT NOT NULL,
    anomaly_score REAL,
    is_anomaly INTEGER,
    detection_mode TEXT
);
```

### B. Table `incident_events` (Exactly 11 Rows)
Records lifecycle events: 6 anomaly detections, 2 anomaly recoveries, 2 test fault injections, and 1 agent investigation.

### C. Table `recovery_approvals` (Exactly 0 Rows)
Historical session did not persist approval tickets to this table (approvals were managed in test fixtures).

---

## 2. Row-Level Resolution of the 169 vs. 175 Sample Discrepancy

### The Conflicting Historical Claims
In [`research/DATA_AND_LABEL_AUDIT.md`](file:///c:/DL_PROJECT/research/DATA_AND_LABEL_AUDIT.md) lines 120–125 and [`research/audits/DATABASE_AUDIT.md`](file:///c:/DL_PROJECT/research/audits/DATABASE_AUDIT.md), the database was described as containing:
- 200 total telemetry rows
- 31 healthy rows
- 169 fault-labelled rows
- Four reconstructed episodes: EP-01 (28 samples), EP-02 (7 samples), EP-03 (98 samples), EP-04 (42 samples)
$$\text{Sum of Episode Samples} = 28 + 7 + 98 + 42 = \mathbf{175 \ne 169}$$

### Empirical Resolution via ID and Timestamp Tracing

A full census of `telemetry_samples` in `data/aegisops_live.sqlite3` reveals the exact truth:

1. **True Timestamps**:
   The telemetry samples span **`2026-10-11T07:12:16.034Z` to `2026-10-11T10:15:37.997Z`**.  
   *Finding*: The timestamps `18:24:12` to `18:48:02` reported in prior markdown audits do not exist anywhere in the database; they were fabricated narrative estimates.
2. **True Class Distribution by `fault_mode`**:
   - `fault_mode == 'normal'`: Exactly **31 rows** (IDs 1–31).
   - `fault_mode == 'latency'`: Exactly **1 row** (ID 32).
   - `fault_mode == 'error'`: Exactly **168 rows** (IDs 33–200).
   - **Total Fault-Labelled Rows**: $1 + 168 = \mathbf{169 \text{ rows}}$.
3. **The Origin of the "175 Samples" Discrepancy**:
   The prior author attempted to manually segment the 168 error rows into two hypothetical episodes (98 and 42 samples) and added 7 latency samples and 28 error samples from a fictional template ($28 + 7 + 98 + 42 = 175$). In reality, the error injection was never cleared during the live run; it ran continuously for 168 consecutive sampling intervals without interruption.
4. **The 6-Sample Mathematical Difference ($175 - 169 = 6$)**:
   The 6 extra samples in the prior narrative correspond to grouping healthy boundary transition samples into the episode totals.

---

## 3. Ground-Truth Timeline, Transitions, and Lifecycle Events

Tracing every row ID, timestamp, and incident event from `data/aegisops_live.sqlite3`:

| Row ID Range | Timestamp Range (UTC) | Duration | `fault_mode` | `status_code` | Service Health | Host RAM | `is_anomaly` | Episode ID | Reconciliation Category & Event Description |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1 – 4** | 07:12:16 – 07:12:31 | 15.1 s | `normal` | 200 | Healthy ($<7$ ms) | 93.8%–94.8% | 0 | None | **HEALTHY_NORMAL**: Steady-state normal baseline. |
| **5 – 7** | 07:12:36 – 07:12:46 | 10.9 s | `normal` | 200 | Healthy ($<20$ ms) | 95.0%–95.6% | 1 | **EP-01** | **HOST_RAM_SPIKE_FALSE_ALARM**: Event #1 logged. Service healthy, but host workstation RAM $\ge 95\%$ triggered bootstrap rule alert. |
| **8** | 07:12:51 | — | `normal` | 200 | Healthy ($3.2$ ms) | 94.6% | 0 | **EP-01** | **HOST_RAM_RECOVERY_TRANSITION**: Event #2 logged (`live_anomaly_recovered`). Host RAM dropped below 95%. |
| **9 – 28** | 07:12:56 – 07:14:36 | 99.0 s | `normal` | 200 | Healthy ($<16$ ms) | 95.0%–99.4% | 1 | **EP-02** | **HOST_RAM_SPIKE_FALSE_ALARM**: Events #3 and #4 logged. Workstation RAM peaked at 99.4%, re-triggering bootstrap rule. |
| **29** | 07:14:40 | — | `normal` | 200 | Healthy ($4.9$ ms) | 93.1% | 0 | **EP-02** | **HOST_RAM_RECOVERY_TRANSITION**: Event #5 logged (`live_anomaly_recovered`). Host RAM cleared. |
| **30 – 31** | 07:14:45 – 07:14:46 | 1.0 s | `normal` | 200 | Healthy ($<6$ ms) | 94.1%–94.6% | 0 | None | **HEALTHY_NORMAL**: Steady-state baseline restored. |
| **32** | 07:14:50 | — | `latency` | 200 | Degraded (1185.5 ms) | 94.2% | 1 | **EP-03** | **SERVICE_LATENCY_FAULT**: Event #6 (`test_fault_injected`, latency) and Event #7 logged. Injected latency $\ge 1000$ ms triggered rule. |
| **33 – 200** | 07:14:51 – 10:15:37 | 10,846 s | `error` | 500 | Failed (Err=100%) | 88.2%–96.1% | 1 | **EP-04** | **SERVICE_ERROR_FAULT_UNRECOVERED**: Event #8 (`test_fault_injected`, error), Event #9 (`live_agent_investigation`), and Events #10, #11 logged. Continuous 168-sample error burst running unrecovered in database. |

---

## 4. Deep Dive: Missing Anomaly Scores & Operational Label Provenance

### The Empirical Finding
Across all 200 rows in `data/aegisops_live.sqlite3`:
- `anomaly_score` is **100.0% NULL** (200 / 200 rows).
- `detection_mode` is **100.0% 'bootstrap_rules'** (200 / 200 rows).
- `is_anomaly` is populated for 192 rows as `1` and 8 rows as `0`.

### Technical Root Cause in `live_monitoring.py`
In `_analyze_latest(store, detector)` ([`live_monitoring.py:200-240`](file:///c:/DL_PROJECT/live_monitoring.py)):
```python
if detector is None:
    analysis = _bootstrap_analysis(latest)
    store.annotate_sample(
        latest["id"],
        None,  # <-- Explicitly hardcoded None
        analysis["is_anomaly"],
        "bootstrap_rules",
        model_anomaly=None,
        rule_anomaly=analysis["is_anomaly"],
    )
```
When live monitoring executes without loading `models/lstm_autoencoder.pt` (or before accumulating 24 consecutive sequence steps), it defaults to bootstrap operational rules.  
**Critical Integrity Finding**: Not a single neural inference was performed during the live session that populated `data/aegisops_live.sqlite3`.

---

## 5. Pseudoreplication: Telemetry Rows vs. Independent Fault Episodes

Treating all 168 consecutive error samples as 168 independent statistical trials represents severe **pseudoreplication**:
- The 168 error rows originate from a **single fault injection command** executed at `07:14:50.745Z` via `POST /admin/fault {"mode": "error"}`.
- Telemetry was polled every 5 to 60 seconds while the fault remained active.
- Observations within this window are autocorrelated time-series measurements of a single failure event, not 168 independent outages.
- In [`research/exports/incident_episodes.csv`](file:///c:/DL_PROJECT/research/exports/incident_episodes.csv), these are correctly collapsed into **four independent episodes** (EP-01, EP-02, EP-03, EP-04).

---

## 6. Strict Separation: Historical Telemetry vs. Synthetic Benchmark

| Dimension | Historical Live Telemetry | Controlled Synthetic Benchmark |
| :--- | :--- | :--- |
| **Storage Location** | `data/aegisops_live.sqlite3` | In-memory / `research/raw/detection_predictions.csv` |
| **Sample Size** | 200 rows (31 normal, 169 fault) | $N = 320$ non-overlapping 24-step sequence windows |
| **Data Generation** | Live HTTP probe to `127.0.0.1:8765` + host `psutil` | Sinusoidal baselines + Gaussian noise + mathematical fault ramps |
| **Detection Mechanism** | Static bootstrap threshold rules only | Paired evaluation: Rules vs. Isolation Forest vs. LSTM Autoencoder |
| **Fault Modes Present** | Latency (1 row) and HTTP 500 error (168 rows) | 6 balanced architectural failure classes (20 replicates each) |
| **Scientific Role** | Systems engineering proof of live collector operation | Controlled algorithmic benchmark for statistical hypothesis testing |

---

## 7. What Cannot Be Established from the Available Records

To maintain absolute scientific transparency, the manuscript must explicitly acknowledge what the records **do not** support:

1. **Neural Model Accuracy on Production Data**: Because all 200 historical database rows have `anomaly_score = NULL`, the database provides **zero empirical evidence** of neural LSTM performance in production.
2. **Online Retraining Feasibility**: Retraining an LSTM model directly from `data/aegisops_live.sqlite3` is impossible. `dl/live_training.py` enforces `len(healthy_samples) >= 180`. The database contains only 31 healthy samples, correctly failing pre-flight validation.
3. **Isolated Microservice Resource Utilization**: Host CPU and RAM describe the entire Windows workstation running background developer applications, not the isolated microservice process.
