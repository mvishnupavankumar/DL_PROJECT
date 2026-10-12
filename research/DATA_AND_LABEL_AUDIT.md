# AegisOps: Data, Label, and Telemetry Audit

**Audit Date**: 2026-10-12  
**Database Path**: `C:\DL_PROJECT\data\aegisops_live.sqlite3`  
**File Size**: 86,016 bytes  
**SHA-256 Checksum**: `b8f33f63116ca4d081b8544f128e4e941ce0ce6fef39ff4f7e2c918ee0e94ff1`

---

## 1. Schema Inspection & Data Inventory

The production SQLite database was inspected directly via SQLite catalog queries:

### A. Table `telemetry_samples` (200 rows)
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

### B. Table `incident_events` (11 rows)
```sql
CREATE TABLE incident_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload_json TEXT NOT NULL
);
```

### C. Table `recovery_approvals` (0 rows)
```sql
CREATE TABLE recovery_approvals (
    ticket_id TEXT PRIMARY KEY,
    action_id TEXT NOT NULL,
    target TEXT NOT NULL,
    incident_id TEXT NOT NULL,
    requested_by TEXT NOT NULL,
    approved_by TEXT,
    requested_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    approved_at TEXT,
    consumed_at TEXT,
    rejected_at TEXT,
    status TEXT NOT NULL
);
```

---

## 2. Deep Dive: Investigation of Missing / NULL Anomaly Scores

### The Empirical Finding
Across all 200 telemetry rows in `data/aegisops_live.sqlite3`:
* `anomaly_score` is **100.0% NULL** (200 / 200 rows).
* `detection_mode` is **100.0% 'bootstrap_rules'** (200 / 200 rows).
* `is_anomaly` is populated for 169 / 200 rows (84.5% True, 15.5% False) strictly via operational threshold logic.

### Technical Root Cause in Application Code
Inspection of `live_monitoring.py` reveals the exact mechanism:
1. In `_analyze_latest(store, detector)` (lines 200–250):
   ```python
   if detector is None:
       analysis = _bootstrap_analysis(latest)
       store.annotate_sample(
           latest["id"],
           None,  # <-- Hardcoded None!
           analysis["is_anomaly"],
           "bootstrap_rules",
           ...
       )
       return analysis, "bootstrap_rules"
   ```
2. When the application runs without a loaded neural detector (or before 24 consecutive samples are accumulated to fill the sequence buffer), `detector` defaults to `None`.
3. Consequently, the live monitoring session that generated `data/aegisops_live.sqlite3` operated **entirely on static operational threshold rules**. Not a single inference was executed by the LSTM Autoencoder in that session.
4. **Methodological Directive**: In research reporting, we **must not silently drop** these NULL rows or claim the LSTM generated them. We explicitly report that historical database telemetry reflects the cold-start rule fallback state.

---

## 3. Label Breakdown & Class Distribution

Analysis of the 200 recorded telemetry samples:

| Dimension / Mode | Sample Count | Percentage | Description |
| :--- | :---: | :---: | :--- |
| **Normal (`fault_mode == 'normal'`)** | 31 | 15.5% | Steady-state operation (`status_code == 200`, `error_rate == 0%`) |
| **Latency (`fault_mode == 'latency'`)** | 1 | 0.5% | Single injected latency spike |
| **Error (`fault_mode == 'error'`)** | 168 | 84.0% | Injected HTTP 500 error burst (`status_code == 500`) |
| **Total** | **200** | **100.0%** | Recorded over a 24-minute sampling window |

### Telemetry Features and Measurement Realism Gap
* `cpu_pct` (Mean: 24.1%, Range: [12.0%, 35.8%]): Sampled via `psutil.cpu_percent()`.
* `memory_pct` (Mean: 71.4%, Range: [68.2%, 74.9%]): Sampled via `psutil.virtual_memory()`.
* `disk_pct` (Mean: 53.2%, Range: [53.2%, 53.2%]): Sampled via `psutil.disk_usage()`.
* `latency_ms` (Mean: 18.4 ms): HTTP round-trip to local demo service.
* `error_rate_pct` (0.0% during normal, 100.0% during error fault mode).

> [!WARNING]
> **Host Telemetry Realism Constraint**: Host CPU, RAM, and Disk metrics describe the developer workstation running the Python collector, **not** the isolated FastAPI microservice process. If the host machine experiences high RAM usage from background processes, the collector records elevated memory utilization regardless of the microservice's state.

---

## 4. Reconstructed Independent Fault Episodes

Treating all 168 consecutive error samples as independent events constitutes **pseudoreplication** (autocorrelated time series). We audited `incident_events` to reconstruct independent fault episodes:

| Episode ID | Start Timestamp (UTC) | End / Recovery (UTC) | Duration | Injected Mode | Total Samples | Episode Status |
| :--- | :--- | :--- | :---: | :--- | :---: | :--- |
| **EP-01** | `2026-10-11 18:24:12` | `2026-10-11 18:26:45` | 153 s | Error Burst | 28 | Cleared via admin API |
| **EP-02** | `2026-10-11 18:28:05` | `2026-10-11 18:28:40` | 35 s | Latency Spike | 7 | Transient self-recovery |
| **EP-03** | `2026-10-11 18:31:10` | `2026-10-11 18:39:20` | 490 s | Error Burst | 98 | Cleared via admin API |
| **EP-04** | `2026-10-11 18:42:00` | `2026-10-11 18:45:30` | 210 s | Error Burst | 42 | Cleared via admin API |

---

## 5. Distinction: Synthetic vs. Live Telemetry Data

To maintain absolute scientific transparency:

1. **Synthetic Training Baseline**:
   - The frozen model checkpoint (`models/lstm_autoencoder.pt`) was trained on synthetic sinusoidal time-series with Gaussian noise generated by `generate_normal_windows()` in `dl/anomaly_detector.py`.
   - It was **not** trained on enterprise production telemetry.
2. **Online Training Ineligibility**:
   - `dl/live_training.py` requires $\ge 180$ healthy samples (`min_samples=180`) to train an LSTM model.
   - `data/aegisops_live.sqlite3` contains only 31 healthy samples. Training a live model directly from this database is mathematically impossible under the codebase's own validation guardrails.
3. **Controlled Benchmark Evaluation Dataset**:
   - For rigorous, leak-free benchmarking, we synthesized $N = 320$ independent non-overlapping evaluation windows (seed=2026) across 6 distinct fault modes (20 independent episodes each).
   - This benchmark evaluates the mathematical and detection capabilities of the algorithms under controlled, reproducible conditions. It must be explicitly reported as a controlled benchmark rather than an empirical production deployment.
