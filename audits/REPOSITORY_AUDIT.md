# Phase 1: Repository and Environment Audit

**Document Date**: 2026-10-12  
**Audit Directory**: `C:\DL_PROJECT\research\audits\`  
**Project Workspace**: `C:\DL_PROJECT`  
**Git Revision**: `11cf0c724e593db8133516ed4244d4fe27fb9787` (`main` branch)  
**Host Environment**: Windows 11 Pro (`win32` / AMD64), PowerShell 5.1 / PowerShell 7  
**Active Python Runtime**: Python `3.11.9 (tags/v3.11.9:de5405b)` (`C:\DL_PROJECT\.venv\Scripts\python.exe`)  

---

## 1. Version Control & Working Tree State

Inspection of Git version control via `git rev-parse HEAD`, `git branch`, and `git status -s`:
- **Current Branch**: `main`
- **Current HEAD Commit**: `11cf0c724e593db8133516ed4244d4fe27fb9787` ("Updated")
- **Parent Commit**: `e69cb623ed6902edfbb1d2b946a526cbb23f90ad` ("fixed windows integrate issues")
- **Working Tree State**:
  - Modified tracked files:
    - `research/FINAL_EXPERIMENT_REPORT.md` (Updated with verified experimental evidence)
    - `research/MANIFEST_SHA256.json` (Updated with complete SHA-256 manifest v2.0.0)
    - `research/run_all.py` (Unified entry point invoking verified runners)
    - `test_live_monitoring.py` (Added regression test for scoping & NameError prevention)
  - Untracked research artifacts:
    - `research/PROJECT_VERSION_AND_ENVIRONMENT.md`
    - `research/DATA_AND_LABEL_AUDIT.md`
    - `research/STATISTICAL_AUDIT.md`
    - `research/SAFETY_EVALUATION.md`
    - `research/statistical_tests.py`
    - `research/raw/` (7 machine-readable per-sample CSVs)
    - `research/figures/FIGURE_CAPTIONS.md`
    - `research/commands_and_logs/` (pytest logs, environment dumps, reproduction scripts)
    - `test_statistical_audit.py` (5 unit tests for statistical formulas)

---

## 2. Python Virtual Environment and Dependency Manifest

The environment uses a managed virtual environment at `C:\DL_PROJECT\.venv\`:
- Configuration (`.venv/pyvenv.cfg`):
  ```ini
  home = C:\Users\chara\AppData\Local\Programs\Python\Python311
  include-system-site-packages = true
  version = 3.11.9
  executable = C:\Users\chara\AppData\Local\Programs\Python\Python311\python.exe
  command = C:\Users\chara\AppData\Local\Programs\Python\Python311\python.exe -m venv C:\DL_PROJECT\.venv
  ```
- **Rationale for Site-Packages Bridge**: `include-system-site-packages = true` allows the virtual environment to access system-installed `scikit-learn 1.9.0` and `scipy 1.17.1` without downloading external binaries, breaking pinned requirements, or modifying locked project packages.

### Pinned Package Inventory:

| Package | Installed Version | Role in Architecture |
| :--- | :---: | :--- |
| **Python** | `3.11.9` | Core Execution Environment |
| **PyTorch (`torch`)** | `2.14.1` | LSTM Autoencoder model definition, training, forward pass |
| **Scikit-Learn (`sklearn`)** | `1.9.0` | Isolation Forest baseline, MinMaxScaler |
| **SciPy (`scipy`)** | `1.17.1` | Exact two-sided binomial test (`binomtest`), $\chi^2$ distribution |
| **Pandas (`pandas`)** | `3.0.6` | Telemetry series framing, rolling windows, CSV exports |
| **NumPy (`numpy`)** | `2.4.6` | Tensor manipulation, continuous array slicing |
| **Streamlit (`streamlit`)** | `1.42.0` | Live Incident Response Console UI (`@st.fragment`) |
| **FastAPI (`fastapi`)** | `0.115.11` | Local disposable demo microservice endpoints |
| **Uvicorn (`uvicorn`)** | `0.34.0` | ASGI web server for local demo service |
| **Pillow (`PIL`)** | `12.3.0` | Programmatic rendering of publication figures |
| **Pytest (`pytest`)** | `9.1.1` | Test suite runner and regression testing |
| **Requests (`requests`)** | `2.32.3` | Probing HTTP health and fault endpoints |
| **psutil (`psutil`)** | `7.0.0` | Host workstation metric collection (CPU, RAM, Disk) |

---

## 3. Configuration & Secrets Inspection

- **Configuration File (`config.py`)**:
  - Loads environment variables from `.env` via `python-dotenv`.
  - Keys defined: `GROQ_API_KEY`, `GROQ_MODEL` (default: `openai/gpt-oss-20b`), `AEGISOPS_SERVICE_URL` (default: `http://127.0.0.1:8765`), `AEGISOPS_STORE_PATH` (default: `data/aegisops_live.sqlite3`).
- **Secrets Audit**:
  - The project `.env` file was inspected. No API tokens or passwords are hardcoded in git tracking.
  - Dual Execution Mode: When `GROQ_API_KEY` is empty, `agents.IncidentAgents()` automatically falls back to deterministic local heuristic handlers (`_local_root_cause()`), enabling 100% offline testing.

---

## 4. Application Entry Points and Execution Flow

The active application contains 4 distinct entry points:

1. **User Interface Console (`app.py` & `live_monitoring.py`)**:
   - Run via: `streamlit run app.py`
   - Uses `@st.fragment(run_every="5s")` to execute `live_panel()`.
   - Displays real-time metrics, anomaly status, live investigation trace, approval request controls, and recovery action triggers.
2. **Background Telemetry Collector (`collectors/worker.py`)**:
   - Run via: `python collectors/worker.py`
   - Samples host CPU/RAM/Disk via `psutil` and sends HTTP GET probe to configured target URL at 5-second intervals.
   - Inserts records into SQLite table `telemetry_samples`.
3. **Local Disposable Test Microservice (`demo_service/main.py`)**:
   - Run via: `uvicorn demo_service.main:app --host 127.0.0.1 --port 8765`
   - Exposes `/probe`, `/health`, `/logs`, and `/admin/fault`.
   - Provides safe, loopback-only fault injection (`error` HTTP 500 burst, `latency` 1200ms delay) and fault clearing.
4. **Unified Research Pipeline (`research/run_all.py`)**:
   - Run via: `python -m research.run_all`
   - Executes Pytest suite, runs Anomaly Detection evaluation, runs Root-Cause Diagnosis rubric audit, executes live Safety & Verification audit, and generates cryptographic SHA-256 manifest.

---

## 5. Investigation of Windows Runtime Defect (`is_local_target`)

### A. The Defect Report
A historical issue was reported as:
```text
NameError: name 'is_local_target' is not defined in live_monitoring.py, previously reported around line 363.
```

### B. Code Structure & Scope Analysis
We performed static code analysis of `live_monitoring.py`:
1. `_is_loopback_target(url)` (lines 80–87) is a pure helper function:
   ```python
   def _is_loopback_target(url: str) -> bool:
       try:
           parsed = urllib.parse.urlsplit(url)
           return parsed.hostname in {"127.0.0.1", "localhost", "::1"}
       except ValueError:
           return False
   ```
2. In `live_monitoring.py`, incident dictionary construction occurs in top-level function `_build_live_incident(sample, analysis, service_url)` (lines 290–402).
3. In earlier versions of `_build_live_incident` (around line 363), health evaluation was attempted using:
   ```python
   health = _get_service_health(service_url) if is_local_target else None
   ```
   Because `is_local_target` was **neither a parameter of `_build_live_incident` nor a module-level variable**, calling `_build_live_incident` raised `NameError: name 'is_local_target' is not defined`.
4. In the current codebase (`e69cb62` and `11cf0c7`), line 366 resolves locality directly:
   ```python
   health = (
       _get_service_health(service_url)
       if _is_loopback_target(service_url)
       else None
   )
   ```
5. In `live_panel()` (the Streamlit fragment), line 642 explicitly declares:
   ```python
   # Define this before any conditional use.
   is_local_target = _is_loopback_target(service_url)
   ```
   before any subsequent conditional checks (e.g. line 914 `if not is_local_target:` and line 1031).

### C. Regression Verification
We added an explicit regression test to [`test_live_monitoring.py`](file:///c:/DL_PROJECT/test_live_monitoring.py):
- `test_build_live_incident_scoping_and_name_error_prevention`:
  - Calls `_build_live_incident` with local loopback `http://127.0.0.1:8765`.
  - Calls `_build_live_incident` with remote `https://remote.api.production.internal`.
  - Asserts that no `NameError` is raised and verifies that remote targets are strictly restricted to read-only diagnostics (`valid_actions = ["capture_read_only_diagnostics"]`).
  - Passed cleanly in pytest.
