# AegisOps — Test Suite & Reproducibility Audit

**Audit Phase**: Phase 8  
**Auditor**: Senior Python Engineer / ML Researcher / SRE / Security Reviewer  
**Scope**: Test Suite Architecture, Mocking Boundaries, Determinism, and Environmental Reproducibility

---

## 1. Test Execution & Verified Results

The complete test suite was executed in the active Python 3.11.9 virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

### Verified Test Outcome
- **Total Test Cases**: **34**
- **Passed**: **34**
- **Failed**: **0**
- **Skipped**: **0**
- **Errored**: **0**
- **Total Wall-Clock Time**: **20.55 seconds** (including PyTorch CPU inference on test windows)

---

## 2. Test Suite Architecture & Coverage Breakdown

| Test Module | Test Functions Count | Test Type | Mocked Dependencies | Actual Runtime Behavior Exercised |
| :--- | :---: | :---: | :--- | :--- |
| `test_agents.py` | 3 | Unit | `monkeypatch.setattr("agents.GROQ_API_KEY", "")` | Exercises `IncidentAgents` offline deterministic keyword matching, candidate action selection, and verification steps. |
| `test_anomaly_detector.py` | 4 | Unit / Integration | None | Generates synthetic windows, loads PyTorch checkpoint (`models/lstm_autoencoder.pt`), checks forward-pass tensor shapes, and verifies all 6 synthetic incident profiles cross threshold. |
| `test_approval.py` | 8 | Unit / Concurrency | None (uses `tmp_path` SQLite DB) | Exercises approval ticket state transitions (`pending`, `approved`, `consumed`, `rejected`, `expired`), TTL boundary conditions, scope mismatches, and multi-threaded race conditions via `ThreadPoolExecutor(max_workers=2)` and `Barrier(2)`. |
| `test_live_monitoring.py` | 5 | Unit / Integration | `monkeypatch` on `psutil.cpu_percent`, `virtual_memory`, `disk_usage`, and `requests.get` | Exercises loopback URL validation, mock sample persistence in SQLite, live LSTM model training on mathematical series, and CSV data-quality filters. |
| `test_simulator.py` | 3 | Unit | None | Exercises `simulator.py` lookup table in `data/incidents.json` and checks boolean `force_fail` flag. |
| `test_target_security.py` | 4 | Unit | None | Exercises URL validation rules: verifies HTTPS requirement for remote targets, rejection of plaintext HTTP, credential stripping, and loopback gating. |
| `test_workflow.py` | 2 | Integration / End-to-End (Synthetic) | `monkeypatch.setattr("agents.GROQ_API_KEY", "")` | Exercises full 5-agent resolution loop against all 6 synthetic incidents in `data/incidents.json`, including self-correcting retry on initial failure (`force_first_failure=True`). |

---

## 3. Mocked vs Real Runtime Behavior

| Subsystem | In Test Suite | In Real Runtime (`app.py` / `live_monitoring.py`) | Fidelity Gap |
| :--- | :--- | :--- | :--- |
| **Agent Execution** | Mocked via `GROQ_API_KEY = ""` to run deterministic offline rules. | In real runtime, if `GROQ_API_KEY` is provided, calls live Groq Cloud API. | **Significant Gap**: Live Groq API calls, prompt parsing, network timeouts, and rate-limits are completely unexercised by automated tests. |
| **Incident Environment** | Synthetic lookup via `simulator.py` and `data/incidents.json`. | Live observations collected from `demo_service/main.py` via HTTP probes. | **Significant Gap**: Real HTTP service interactions are not part of `test_workflow.py`. |
| **Remediation Execution** | Simulates action success by reading boolean dictionary in `incidents.json`. | Sends HTTP POST to `/admin/fault` and queries live `/probe`. | **Medium Gap**: Real HTTP fault reset is tested only in `test_live_monitoring.py` or manual validation. |
| **Telemetry Ingestion** | Mocked in `test_live_monitoring.py:25` using static lambdas. | Live calls to OS `psutil` and real HTTP round-trips. | **Low Gap**: Real telemetry collector is simple and was verified in Phase 5 manual validation. |

---

## 4. Uncovered & Missing Test Areas

1. **Groq LLM Integration**:
   - Zero tests exercise real or mock responses from `GroqAgent.client.chat.completions.create`.
   - Zero tests verify behavior when Groq returns malformed JSON, rate limits (HTTP 429), or network dropouts.
2. **Headless Collector Worker (`collectors/worker.py`)**:
   - Zero unit or integration tests for the continuous loop in `collectors/worker.py`.
   - Signal handling (`SIGINT`/`SIGTERM`) and interval pacing are completely untested.
3. **Streamlit UI Components (`live_monitoring.py`)**:
   - No UI integration tests (e.g. via `streamlit.testing.v1.AppTest`).
   - Fragment re-execution, button states, session state persistence, and chart rendering are unverified in automated tests.
4. **Target Service Failures & Timeouts**:
   - No tests verifying collector behavior when target socket hangs indefinitely (verifying `REQUEST_TIMEOUT_S` enforcement).
5. **Real-World Anomaly Datasets**:
   - No test measures precision/recall against benchmark time-series datasets (e.g. NAB, SMD).

---

## 5. Environmental Reproducibility & Determinism

### A. Environment Replication
- **Platform Tested**: Windows 11 / PowerShell 5.1 / Python 3.11.9 (AMD64).
- **Dependency Clean-Install**: Verified. A fresh `.venv` installs dependencies from `requirements.txt` with zero compile errors (pre-built wheels available for PyTorch, NumPy, Pandas, Pydantic, etc.).
- **Missing File Fixed**: Initial clean-install required `.env.example`, which was created by the auditor during Phase 1.

### B. Seed Determinism
- **Synthetic Training (`dl/anomaly_detector.py:197`)**: Fixed seeds: `torch.manual_seed(seed)`, `np.random.seed(seed)`, `torch.set_num_threads(1)` with default `seed=42`. Generates bit-identical model weights on identical PyTorch versions.
- **Live Training (`dl/live_training.py:53`)**: Sets `seed=37` for torch and numpy.
- **Evaluation (`dl/evaluate_detector.py:14`)**: Evaluates against fixed seed `seed=2026`.

---

## 6. Critical Evaluator Warning

> [!WARNING]
> **Passing 34 out of 34 software tests does NOT demonstrate research validity or production readiness.**
> The test suite validates code contracts, state machines, math dimensions, and offline fallback consistency. It proves that the software does not crash under predefined scenarios.
> It does **not** prove that the LSTM Autoencoder outperforms standard statistical process control (SPC) or rules on real systems, nor does it prove that the LLM agents can diagnose real production incidents without human intervention.
