# AegisOps: Project Version, Environment, and Dependency Audit

**Document Date**: 2026-10-12  
**Project Root**: `C:\DL_PROJECT`  
**Git Revision**: `e69cb623ed6902edfbb1d2b946a526cbb23f90ad` (`main` branch)  
**Host Environment**: Windows 11 Pro (`win32` / AMD64), PowerShell 5.1 / PowerShell 7  
**Virtual Environment**: `C:\DL_PROJECT\.venv\Scripts\python.exe` (Python 3.11.9)

---

## 1. Verified Runtime & Dependency Versions

All package versions were queried directly from the active Python virtual environment:

| Package | Version | Primary Purpose | Source / Notes |
| :--- | :--- | :--- | :--- |
| **Python** | `3.11.9` | Core Execution Runtime | CPython 64-bit |
| **PyTorch (`torch`)** | `2.14.1` | Neural Autoencoder Architecture & Tensor Ops | CPU runtime |
| **Scikit-Learn (`sklearn`)** | `1.9.0` | Isolation Forest Baseline & MinMaxScaler | Host site-packages bridge |
| **SciPy (`scipy`)** | `1.17.1` | Exact Statistical Tests & Distributions | Host site-packages bridge |
| **Pandas (`pandas`)** | `3.0.6` | Data Manipulation & Time-Series Framing | Production dependency |
| **NumPy (`numpy`)** | `2.4.6` | Matrix Computations & Sliding Windows | Production dependency |
| **Streamlit (`streamlit`)** | `1.42.0` | Live Incident Response Console UI | Production dependency |
| **FastAPI (`fastapi`)** | `0.115.11` | Local Disposable Test Microservice | Production dependency |
| **Uvicorn (`uvicorn`)** | `0.34.0` | ASGI Server for Demo Microservice | Production dependency |
| **Pillow (`PIL`)** | `12.3.0` | High-Resolution Figure Generation | Production dependency |
| **Pytest (`pytest`)** | `9.1.1` | Test Runner & Regression Suite | Development dependency |
| **Requests (`requests`)** | `2.32.3` | Local HTTP Probing & Rest Client | Production dependency |
| **psutil (`psutil`)** | `7.0.0` | Host Telemetry Metrics Collector | Production dependency |

---

## 2. Inventory of Imported and Executed Application Modules

The application architecture consists of the following active execution paths:

### A. User Interface & Reactive Panel
- **Entrypoint**: `app.py`
  - Imports: `streamlit`, `config.Config`, `live_monitoring.render_live_monitoring`.
- **Live Console Engine**: `live_monitoring.py`
  - Imports: `approval.ApprovalStore`, `approval.ApprovalError`, `collectors.system_metrics.validate_local_service_url`, `dl.anomaly_detector.TelemetryAnomalyDetector`, `dl.live_training.train_live_model`, `storage.telemetry_store.TelemetryStore`, `agents.IncidentAgents`, `config.Config`.
  - Architecture: Uses `@st.fragment(run_every="5s")` to execute `live_panel()`.

### B. Background Telemetry Collector
- **Worker Script**: `collectors/worker.py`
  - Imports: `collectors.system_metrics.collect_live_sample`, `storage.telemetry_store.TelemetryStore`, `config.Config`.
- **System Metrics Collector**: `collectors/system_metrics.py`
  - Imports: `psutil`, `requests`, `storage.telemetry_store.TelemetryStore`.
  - Behavior: Samples host CPU %, memory %, and disk % via `psutil`; queries the target HTTP endpoint (`/probe` or `/health`) via `requests.get`.

### C. Authorization & Safety Engine
- **Module**: `approval.py`
  - Imports: `sqlite3`, `uuid`, `datetime`.
  - Behavior: Implements two-man-rule cryptographic tickets with exact parameter scope matching (`action_id`, `target`, `incident_id`), strict TTL expiration, and atomic single-use state transitions (`BEGIN IMMEDIATE`).

### D. Deep Learning & Anomaly Detection
- **Model Architecture**: `dl/anomaly_detector.py`
  - Imports: `torch`, `torch.nn`, `numpy`, `json`.
  - Architecture: Symmetric LSTM Autoencoder (5 input features $\to$ 16 hidden $\to$ 8 bottleneck $\to$ 16 hidden $\to$ 5 output features; 3,605 total parameters).
- **Online Training**: `dl/live_training.py`
  - Imports: `dl.anomaly_detector.TelemetryAnomalyDetector`, `torch`.
  - Behavior: Sliding-window trainer requiring $\ge 180$ healthy samples before fitting.

### E. Multi-Agent Diagnostic Engine
- **Module**: `agents.py`
  - Imports: `groq.Groq`, `json`, `os`, `re`, `config.Config`.
  - Dual Execution Modes:
    1. **Live LLM Mode**: Calls Groq API using model `openai/gpt-oss-20b`.
    2. **Offline Deterministic Mode**: Uses heuristic regex rules (`_local_root_cause`) as a zero-cost local fallback.

### F. Local Disposable Test Service
- **Module**: `demo_service/main.py`
  - Imports: `fastapi.FastAPI`, `fastapi.Response`, `time`, `logging`.
  - Endpoints: `/probe` (normal 200 latency < 50ms), `/health` (returns JSON status and active fault mode), `/logs`, `/admin/fault` (injects or clears local latency or error faults).

---

## 3. Investigation of Historical Windows `is_local_target` NameError

### A. Context of the Reported Defect
An issue was previously logged as:
```text
NameError: name 'is_local_target' is not defined in live_monitoring.py, previously reported around line 363.
```

### B. Root-Cause Code Analysis & Reproduction Mechanism
Inspection of the code structure in `live_monitoring.py` reveals the exact mechanism that caused this defect historically:

1. **Function Scoping Discrepancy**:
   - In `live_monitoring.py`, the user interface entrypoint is `render_live_monitoring()`, which encapsulates `live_panel()`.
   - In `live_panel()` (lines 640–1290), `is_local_target` is defined as:
     ```python
     is_local_target = _is_loopback_target(service_url)
     ```
   - However, incident payload construction is handled in an independent top-level function:
     ```python
     def _build_live_incident(
         sample: dict[str, Any],
         analysis: dict[str, Any],
         service_url: str,
     ) -> dict[str, Any]:
     ```
2. **The Flawed Implementation (Historical around line 363)**:
   - Inside `_build_live_incident`, health evaluation was attempted:
     ```python
     health = (
         _get_service_health(service_url)
         if is_local_target  # <-- BUG: is_local_target is NOT in _build_live_incident scope!
         else None
     )
     ```
   - Because `is_local_target` was neither a function parameter of `_build_live_incident` nor a module-level global, executing `_build_live_incident` on Windows or Linux raised:
     ```text
     NameError: name 'is_local_target' is not defined
     ```
3. **The Current Verified Fix**:
   - In the active codebase (commit `e69cb62`), line 366 of `_build_live_incident` resolves locality directly via the pure helper function:
     ```python
     health = (
         _get_service_health(service_url)
         if _is_loopback_target(service_url)
         else None
     )
     ```
   - In `live_panel()`, line 642 explicitly declares:
     ```python
     # Define this before any conditional use.
     is_local_target = _is_loopback_target(service_url)
     ```
     before any conditional blocks (e.g. line 914 `if not is_local_target:` and line 1031).

### C. Regression Verification
We added an explicit regression test in `test_live_monitoring.py`:
- `test_build_live_incident_scoping_and_name_error_prevention()`:
  - Invokes `_build_live_incident` with loopback URL `http://127.0.0.1:8765`.
  - Invokes `_build_live_incident` with remote URL `https://remote.api.production.internal`.
  - Asserts zero `NameError` exceptions are raised and asserts read-only action scoping on remote targets.

---

## 4. Preservation of Original Data, Models, and Configurations

Strict preservation guarantees have been enforced:
1. **SQLite Database**: `data/aegisops_live.sqlite3` remains unmodified (86,016 bytes; SHA-256: `b8f33f63116ca4d081b8544f128e4e941ce0ce6fef39ff4f7e2c918ee0e94ff1`).
2. **Trained Checkpoint**: `models/lstm_autoencoder.pt` remains unmodified (19,797 bytes; SHA-256: `1cf44e6efd924ff98ee9d0f4d306b3fa1b5853549646b5a32ba06d96201b17b2`).
3. **Metadata**: `models/lstm_autoencoder.json` remains unmodified.
4. **Disposable Safety Fixtures**: All safety and authorization penetration tests run against dedicated isolated databases (`data/safety_test_store.sqlite3`), completely shielding the live database.
5. **Backups Created**: All prior outputs are backed up in `research/backup_prior_outputs/`.
