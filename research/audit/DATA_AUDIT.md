# AegisOps — Telemetry, Incident, and Label Data Audit

**Date**: 2026-10-12  
**Source Database**: `data/aegisops_live.sqlite3` (86,016 bytes)  
**Export Files**:
- `research/exports/telemetry.csv` (200 records)
- `research/exports/incident_events.csv` (11 records)
- `research/exports/incident_episodes.csv` (4 reconstructed episodes)

---

## 1. Database Schema and Record Counts

The SQLite database contains 3 operational tables and 1 internal sequence table:

| Table Name | Verified Row Count | Column Count | Primary Key | Description |
| :--- | :---: | :---: | :--- | :--- |
| `telemetry_samples` | **200** | 15 | `id` (INTEGER AUTOINCREMENT) | Streaming host and probe telemetry records. |
| `incident_events` | **11** | 4 | `id` (INTEGER AUTOINCREMENT) | Asynchronous audit events (anomalies, recoveries, injections, investigations). |
| `recovery_approvals` | **0** | 11 | `ticket_id` (TEXT) | Gated approval state machine tickets. (Empty in this database). |
| `sqlite_sequence` | 2 | 2 | N/A | SQLite internal autoincrement tracking (`telemetry_samples` seq=200, `incident_events` seq=11). |

---

## 2. Telemetry Feature Audit & Statistical Distribution

### Feature Specifications and Units

| Field | Data Type | Units / Range | Measured Entity | Null Count |
| :--- | :---: | :---: | :--- | :---: |
| `timestamp` | TEXT (ISO-8601 UTC) | Microsecond UTC string | Clock time of probe observation | 0 (0.0%) |
| `cpu_pct` | REAL | 0.0% – 100.0% | Collector machine CPU utilization (`psutil`) | 0 (0.0%) |
| `memory_pct` | REAL | 0.0% – 100.0% | Collector machine RAM utilization (`psutil`) | 0 (0.0%) |
| `disk_pct` | REAL | 0.0% – 100.0% | Collector machine filesystem utilization (`psutil`) | 0 (0.0%) |
| `latency_ms` | REAL | Milliseconds | HTTP client-side round-trip time (`time.perf_counter`) | 0 (0.0%) |
| `error_rate_pct` | REAL | 0.0% – 100.0% | Rolling failure rate over trailing 20 probe calls | 0 (0.0%) |
| `service_available` | INTEGER | 0 or 1 | Derived: $1 \iff \text{status\_code} == 200$ | 0 (0.0%) |
| `status_code` | INTEGER | HTTP code (200, 500) | Response code from target `/probe` endpoint | 0 (0.0%) |
| `error_message` | TEXT | String | Exception message or probe error text | 0 (0.0%) |
| `fault_mode` | TEXT | `normal`, `latency`, `error` | Ground-truth mode reported by `demo_service` | 0 (0.0%) |
| `data_source` | TEXT | String | Telemetry ingestion channel descriptor | 0 (0.0%) |
| `anomaly_score` | REAL | None | LSTM reconstruction error (MSE) | **200 (100.0%)** |
| `is_anomaly` | INTEGER | 0 or 1 | Final binary alert decision | 0 (0.0%) |
| `detector_mode` | TEXT | `bootstrap_rules` | Mode of the active detector during capture | 0 (0.0%) |

### Telemetry Value Distributions (N = 200)

- **Timestamp Extents**: `2026-10-11T07:12:16.034Z` to `2026-10-11T10:15:37.997Z` (Total duration: 3 hours, 3 minutes, 21.96 seconds).
- **Duplicate Timestamps**: Exactly 0 duplicate records.
- **Fault Mode Frequencies**:
  - `error`: 168 rows (84.0%)
  - `normal`: 31 rows (15.5%)
  - `latency`: 1 row (0.5%)
- **HTTP Status Codes**:
  - `500 Internal Server Error`: 168 rows (84.0%)
  - `200 OK`: 32 rows (16.0%)
- **Active Detector Mode**: `bootstrap_rules` across all 200 samples (100.0%).
- **Detector Decisions**:
  - `is_anomaly = 1`: 192 samples (96.0%)
  - `is_anomaly = 0`: 8 samples (4.0%)
- **Reconstruction Scores**: `anomaly_score` is `NULL` for all 200 records because the live monitoring dashboard was operating in bootstrap rule fallback mode without an active neural model forward pass during logging.

---

## 3. Sampling Cadence, Irregularities, and Temporal Gaps

Analysis of consecutive timestamp deltas ($\Delta t$):
- **Mean $\Delta t$**: 55.29 seconds
- **Median $\Delta t$**: 5.013 seconds
- **Min $\Delta t$**: 0.578 seconds
- **25th Percentile**: 4.995 seconds
- **75th Percentile**: 59.986 seconds
- **Max $\Delta t$**: 6,170.22 seconds (102.84 minutes)

### Sampling Regimes Observed
1. **Nominal 5-Second Stream (Samples 1 to 49)**: Uniform polling at $\approx 5.0$ seconds (developer interacting with UI).
2. **Transition & Gap (Samples 49 to 59)**:
   - Sample 50 occurred at +32.0s.
   - Samples 51 to 58 polled at 60.0-second intervals.
   - **Severe Gap**: Between Sample 58 (`2026-10-11T07:24:37.995Z`) and Sample 59 (`2026-10-11T09:07:28.234Z`), an outage of 6,170.2 seconds occurred with zero telemetry collection.
3. **Low-Frequency Polling (Samples 59 to 200)**: Steady polling at 60.0-second intervals while the local service remained in HTTP 500 error mode.

---

## 4. Reconstructed Independent Incident Episodes

An **independent incident episode** is defined as an isolated temporal window beginning with an explicit fault onset (either an injected service failure or a distinct operational threshold excursion) and ending when the system either recovers to normal operation or is superseded by a distinct fault mode.

Treating 200 consecutive sliding samples as independent incidents constitutes severe pseudoreplication. From the historical database, exactly **4 distinct episodes** are reconstructed:

| Episode ID | Classification | Cause / Trigger | Time Range (UTC) | Duration | Samples | Outcome |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| **EP-01** | Host Memory Excursion | Workstation RAM $\ge 95\%$ | 07:12:36 to 07:12:51 | 15.86s | 4 (IDs 5–8) | Recovered |
| **EP-02** | Host Memory Excursion | Workstation RAM $\ge 95\%$ | 07:12:56 to 07:14:40 | 103.79s | 21 (IDs 9–29) | Recovered |
| **EP-03** | Controlled Fault Injection | Injected 1.2s latency via demo service | 07:14:46 to 07:14:50 | 4.20s | 1 (ID 32) | Superseded |
| **EP-04** | Controlled Fault Injection | Injected HTTP 500 error via demo service | 07:14:50 to 10:15:37 | 10,847.25s | 168 (IDs 33–200) | Unrecovered in DB |

### Critical Findings Regarding Existing Database Labels
1. **No True Generalization Labels**: All alerts in `telemetry_samples` were produced by static rules (Memory $\ge 95\%$, Latency $\ge 1000$ ms, Status $\ne 200$). None originated from the LSTM Autoencoder.
2. **Operational Rules False Positive Rate on Normal Service**: During EP-01 and EP-02, the target demo service was completely healthy (`status=200`, `latency < 5ms`, `fault_mode='normal'`), yet the system issued persistent anomaly alerts because the developer's laptop RAM was at 95.1%. This empirically demonstrates that **coupling host hardware metrics with target service monitoring causes severe false alarm leakage**.
3. **Absence of Completed Recovery Cycles**: In EP-04, the fault was injected, but no recovery approval ticket was created or consumed in `recovery_approvals`, and the database terminates with the service still in HTTP 500 state.
