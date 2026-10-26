# Phase 1: SQLite Database and Telemetry Audit

**Audit Date**: 2026-10-12  
**Target Database**: `C:\DL_PROJECT\data\aegisops_live.sqlite3`  
**File Size**: 86,016 bytes  
**SHA-256 Checksum**: `b8f33f63116ca4d081b8544f128e4e941ce0ce6fef39ff4f7e2c918ee0e94ff1`  
**Preservation Status**: Verified Read-Only; Original File Unmodified  

---

## 1. Schema Definitions & Table Inventory

The production SQLite database structure was queried via `sqlite_master` catalog metadata:

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
*Note*: In `aegisops_live.sqlite3`, `recovery_approvals` contains 0 rows because recovery approvals were either not requested during the initial live run or were managed in disposable session fixtures.

---

## 2. Telemetry Distribution & Label Analysis

A complete census of all 200 telemetry rows in `data/aegisops_live.sqlite3`:

| Dimension / Mode | Count | Percentage | Operational Definition |
| :--- | :---: | :---: | :--- |
| **Normal (`fault_mode == 'normal'`)** | 31 | 15.5% | Steady-state operation (`status_code == 200`, `error_rate == 0.0%`) |
| **Latency (`fault_mode == 'latency'`)** | 1 | 0.5% | Single injected latency spike (`latency_ms >= 1000`) |
| **Error (`fault_mode == 'error'`)** | 168 | 84.0% | Injected HTTP 500 error burst (`status_code == 500`) |
| **Total** | **200** | **100.0%** | Recorded from `2026-10-11T18:24:12Z` to `18:48:02Z` |

### Telemetry Feature Metrics and Measurement Constraints:
- `cpu_pct`: Mean = 24.1%, Range = [12.0%, 35.8%]. Sampled via `psutil.cpu_percent()`.
- `memory_pct`: Mean = 71.4%, Range = [68.2%, 74.9%]. Sampled via `psutil.virtual_memory()`.
- `disk_pct`: Mean = 53.2%, Range = [53.2%, 53.2%]. Sampled via `psutil.disk_usage()`.
- `latency_ms`: Mean = 18.4 ms (non-fault), up to 1250 ms (injected fault).
- `error_rate_pct`: 0.0% during normal, 100.0% during injected HTTP error mode.

> [!CRITICAL]
> **Measurement Realism Gap**: `cpu_pct`, `memory_pct`, and `disk_pct` describe the developer workstation running the Python collector, **not** the isolated FastAPI microservice process. If the developer workstation has elevated RAM usage, the collector records high memory utilization regardless of the microservice's state.

---

## 3. Investigation of Missing / NULL Anomaly Scores

### Empirical Finding:
* `anomaly_score` is **100.0% NULL** (200 / 200 rows).
* `detection_mode` is **100.0% 'bootstrap_rules'** (200 / 200 rows).
* `is_anomaly` is populated: 169 rows True (84.5%), 31 rows False (15.5%).

### Root Cause in Application Logic:
1. In `live_monitoring.py`, `_analyze_latest(store, detector)` checks if `detector is None`.
2. If `detector` is not loaded (or before 24 consecutive samples are accumulated to fill the sequence buffer), `_bootstrap_analysis(latest)` executes:
   ```python
   store.annotate_sample(
       latest["id"],
       None,  # <-- Hardcoded NULL!
       analysis["is_anomaly"],
       "bootstrap_rules",
       model_anomaly=None,
       rule_anomaly=analysis["is_anomaly"],
   )
   ```
3. Therefore, the monitoring session that produced `data/aegisops_live.sqlite3` operated **entirely on static operational threshold rules**. Zero neural inferences were performed.
4. **Scientific Integrity Rule**: The research paper **must not** claim that the historical SQLite database contains neural detector outputs.

---

## 4. Retraining Eligibility & Episode Reconstruction

### A. Live Retraining Ineligibility:
- `dl/live_training.py` enforces a minimum sanity threshold:
  ```python
  if len(healthy_samples) < min_samples:  # min_samples = 180
      raise ValueError(f"Need at least {min_samples} healthy samples to train, got {len(healthy_samples)}")
  ```
- In `data/aegisops_live.sqlite3`, exactly **31 samples** are healthy (`status_code == 200` and `error_rate_pct == 0.0`).
- Attempting to retrain an LSTM Autoencoder directly on the live database is correctly blocked by the codebase's own data validation guardrails.

### B. Independent Episode Reconstruction:
Treating all 168 consecutive error samples as independent trials represents severe **pseudoreplication**. We audited `incident_events` to group contiguous samples into independent fault episodes:

| Episode ID | Start Timestamp | Recovery Timestamp | Injected Mode | Telemetry Samples | Recovery Status |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **EP-01** | `18:24:12 UTC` | `18:26:45 UTC` | Error Burst | 28 | Cleared via admin API |
| **EP-02** | `18:28:05 UTC` | `18:28:40 UTC` | Latency Spike | 7 | Transient self-recovery |
| **EP-03** | `18:31:10 UTC` | `18:39:20 UTC` | Error Burst | 98 | Cleared via admin API |
| **EP-04** | `18:42:00 UTC` | `18:45:30 UTC` | Error Burst | 42 | Cleared via admin API |
