# AegisOps — Verification Evidence & Audit Trail

**Audit Phase**: Phase 12  
**Auditor**: Senior Python Engineer / ML Researcher / SRE / Security Reviewer  
**Audit Date**: 2026-10-11  
**Environment**: Windows 11 / PowerShell 5.1 / Python 3.11.9 (AMD64) / Git 2.51.0

---

## 1. Exact Commands Executed and Verified Results

### Command 1: Host Tooling Verification
- **Command Line**:
  ```powershell
  python --version; git --version
  ```
- **Exit Code**: `0`
- **Captured Output**:
  ```text
  Python 3.11.9
  git version 2.51.0.windows.1
  ```

### Command 2: Isolated Virtual Environment Creation
- **Command Line**:
  ```powershell
  python -m venv .venv
  ```
- **Exit Code**: `0`
- **Output**: Clean creation of `.venv` directory.

### Command 3: Base Packaging Tooling Upgrade
- **Command Line**:
  ```powershell
  .\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
  ```
- **Exit Code**: `0`
- **Installed**: `pip-26.2.1`, `setuptools-84.0.0`, `wheel-0.48.0`, `packaging-26.3`.

### Command 4: Project Dependency Installation
- **Command Line**:
  ```powershell
  .\.venv\Scripts\python.exe -m pip install -r requirements.txt
  ```
- **Exit Code**: `0`
- **Key Installed Packages**:
  - `torch-2.14.1+cpu`
  - `streamlit-1.65.0`
  - `fastapi-0.143.0`
  - `uvicorn-0.54.0`
  - `pandas-3.0.6`
  - `numpy-2.4.6`
  - `pydantic-2.14.0`
  - `psutil-7.2.2`
  - `pytest-9.1.1`
  - `requests-2.34.2`
  - `groq-1.7.0`
  - `python-dotenv-1.2.4`

### Command 5: Module Import & Version Verification
- **Command Line**:
  ```powershell
  .\.venv\Scripts\python.exe -c "import torch, streamlit, fastapi, uvicorn, pandas, numpy, pydantic, psutil, requests, groq, dotenv; print('All core modules imported successfully!'); print('PyTorch version:', torch.__version__); print('Streamlit version:', streamlit.__version__); print('FastAPI version:', fastapi.__version__)"
  ```
- **Exit Code**: `0`
- **Captured Output**:
  ```text
  All core modules imported successfully!
  PyTorch version: 2.14.1+cpu
  Streamlit version: 1.65.0
  FastAPI version: 0.143.0
  ```

### Command 6: Documented Test Suite Execution
- **Command Line**:
  ```powershell
  .\.venv\Scripts\python.exe -m pytest -q
  ```
- **Exit Code**: `0`
- **Captured Output**:
  ```text
  ..................................                                       [100%]
  34 passed in 20.55s
  ```

### Command 7: Synthetic Model Smoke Evaluation
- **Command Line**:
  ```powershell
  .\.venv\Scripts\python.exe -m dl.evaluate_detector
  ```
- **Exit Code**: `0`
- **Captured Output**:
  ```json
  {
    "warning": "Synthetic smoke evaluation only; do not report as real-world accuracy.",
    "samples": 260,
    "normal_samples": 200,
    "injected_fault_samples": 60,
    "confusion_matrix": {
      "true_positive": 60,
      "true_negative": 198,
      "false_positive": 2,
      "false_negative": 0
    },
    "precision": 0.9677,
    "recall": 1.0,
    "f1": 0.9836,
    "normal_false_positive_rate": 0.01
  }
  ```

### Command 8: Local Demo Service Startup (Daemon)
- **Command Line**:
  ```powershell
  .\.venv\Scripts\python.exe -m uvicorn demo_service.main:app --host 127.0.0.1 --port 8765
  ```
- **Status**: Running in background (`PID 28732`).
- **Startup Log**:
  ```text
  INFO:     Started server process [28732]
  INFO:     Waiting for application startup.
  INFO:     Application startup complete.
  INFO:     Uvicorn running on http://127.0.0.1:8765 (Press CTRL+C to quit)
  ```

### Command 9: Dashboard Application Startup (Daemon)
- **Command Line**:
  ```powershell
  .\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501 --server.headless true
  ```
- **Status**: Running in background.
- **Startup Log**:
  ```text
  Uvicorn server started on 127.0.0.1:8501
  You can now view your Streamlit app in your browser.
  URL: http://127.0.0.1:8501
  ```

### Command 10: Live Health Verification
- **Command Line**:
  ```powershell
  .\.venv\Scripts\python.exe -c "import requests; print('Demo /:', requests.get('http://127.0.0.1:8765/').json()); print('Demo /health:', requests.get('http://127.0.0.1:8765/health').json()); print('Demo /probe:', requests.get('http://127.0.0.1:8765/probe').json()); print('Streamlit health:', requests.get('http://127.0.0.1:8501/_stcore/health').text)"
  ```
- **Exit Code**: `0`
- **Captured Output**:
  ```text
  Demo /: {'service': 'AegisOps local test service', 'status': 'running'}
  Demo /health: {'status': 'ok', 'service': 'aegisops-demo-service', 'fault_mode': 'normal'}
  Demo /probe: {'status': 'ok', 'fault_mode': 'normal', 'server_processing_ms': 0.006}
  Streamlit health: ok
  ```

### Command 11: End-to-End Workflow Validation
- **Command Line**:
  ```powershell
  .\.venv\Scripts\python.exe validate_workflow.py
  ```
- **Exit Code**: `0`
- **Output Summary**:
  - Step 1 (Collection & Persistence): CPU=22.5%, RAM=88.9%, Disk=75.2%, Latency=12.8ms, Status=200 stored in SQLite.
  - Step 2 (Model Loading & Inference): Loaded `models/lstm_autoencoder.pt`, detected anomaly with Score=6973.08 > Threshold=0.7094.
  - Step 3 (Agent Investigation & Diagnosis): Manager plan generated; Investigation extracted log signals; Diagnosis generated root cause.
  - Step 4 (Approval Enforcement): Created ticket `b4d92bf8-...`; unapproved consumption blocked; mismatched phrase blocked; exact phrase approved.
  - Step 5 (Audit Logging): Persisted and verified event in `incident_events`.
  - Step 6 (Fault Injection, Remediation & Post-Verification): Injected latency fault; atomically consumed ticket; executed `/admin/fault` reset; verified return to `fault_mode: normal` and probe latency 4.21ms; verified ticket cannot be replayed.

---

## 2. Inventory of Inspected Source Files

1. `app.py` (complete line-by-line inspection)
2. `live_monitoring.py` (complete line-by-line inspection, 1,289 lines)
3. `agents.py` (complete line-by-line inspection, 267 lines)
4. `approval.py` (complete line-by-line inspection, 149 lines)
5. `config.py` (complete line-by-line inspection, 12 lines)
6. `simulator.py` (complete line-by-line inspection, 32 lines)
7. `collectors/system_metrics.py` (complete line-by-line inspection, 140 lines)
8. `collectors/worker.py` (complete line-by-line inspection, 59 lines)
9. `demo_service/main.py` (complete line-by-line inspection, 79 lines)
10. `dl/anomaly_detector.py` (complete line-by-line inspection, 273 lines)
11. `dl/live_training.py` (complete line-by-line inspection, 111 lines)
12. `dl/train_from_csv.py` (complete line-by-line inspection, 73 lines)
13. `dl/train_model.py` (complete line-by-line inspection, 20 lines)
14. `dl/evaluate_detector.py` (complete line-by-line inspection, 49 lines)
15. `storage/telemetry_store.py` (complete line-by-line inspection, 130 lines)
16. `models/lstm_autoencoder.json` (metadata and threshold values verified)
17. `data/incidents.json` (all 6 incident structures inspected)
18. `data/aegisops_live.sqlite3` (database tables and row inserts verified)
19. `test_agents.py`, `test_anomaly_detector.py`, `test_approval.py`, `test_live_monitoring.py`, `test_simulator.py`, `test_target_security.py`, `test_workflow.py` (all 7 test files inspected)
20. `run.bat`, `run.sh`, `run_all.bat`, `run_all.ps1`, `run_worker.bat` (all startup scripts inspected)
21. `README.md`, `START_HERE.md`, `WINDOWS_DEPLOYMENT.md`, `SECURITY.md` (all documentation files inspected)

---

## 3. Uninspected Areas & Audit Limitations

1. **Live External Groq API Calls**:
   - The audit was executed without configuring an external `GROQ_API_KEY`. The offline deterministic execution path was verified, and the live API call path was statically analyzed. Real latency, token consumption, and Groq rate-limiting behavior could not be dynamically benchmarked against the live cloud endpoint.
2. **Multi-Day Continuous Telemetry Collection**:
   - The database write volume and memory consumption over a 7-day continuous run were not observed during this single-day audit.
3. **Distributed Remote Target Environment**:
   - All tests were executed against the loopback target (`http://127.0.0.1:8765`). Remote HTTPS targets behind cloud load balancers were not live-tested.
