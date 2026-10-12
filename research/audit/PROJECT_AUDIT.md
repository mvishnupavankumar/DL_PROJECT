# AegisOps — Repository and Environment Audit

**Date**: 2026-10-12  
**Project Path**: `C:\DL_PROJECT`  
**Git Revision**: `e69cb623ed6902edfbb1d2b946a526cbb23f90ad` (`main` branch)  
**Host Platform**: Windows 11 / Windows NT (`win32`)  
**Python Runtime**: Python 3.11.9 (`C:\DL_PROJECT\.venv\Scripts\python.exe`)  
**Baseline Test Status**: 36 passed / 36 collected (100% passing in 16.85s)

---

## 1. Executive Audit Overview

This audit document establishes the verified ground truth of the AegisOps repository, its runtime dependencies, data stores, neural network artifacts, and execution modes. No assumptions have been made from previous documentation; all statements are backed by direct source inspection, bytecode execution, and database queries.

---

## 2. Environment and Dependency Specifications

| Component | Specification / Version | Verification Status |
| :--- | :--- | :---: |
| Operating System | Windows 11 Pro 64-bit | VERIFIED |
| Python Core | 3.11.9 (tags/v3.11.9:de5405b) | VERIFIED |
| PyTorch (`torch`) | 2.14.1 (CPU mode) | VERIFIED |
| Scikit-Learn (`sklearn`) | 1.9.0 | VERIFIED |
| SciPy (`scipy`) | 1.17.1 | VERIFIED |
| Pandas (`pandas`) | 3.0.6 | VERIFIED |
| NumPy (`numpy`) | 2.4.6 | VERIFIED |
| Streamlit (`streamlit`) | 1.65.0 | VERIFIED |
| FastAPI (`fastapi`) | 0.143.0 | VERIFIED |
| Uvicorn (`uvicorn`) | 0.54.0 | VERIFIED |
| Psutil (`psutil`) | 7.2.2 | VERIFIED |
| Pillow (`PIL`) | 12.3.0 | VERIFIED |
| Pytest (`pytest`) | 9.1.1 | VERIFIED |
| Groq Client (`groq`) | 1.7.0 | VERIFIED |

---

## 3. Component Implementation & Operational Classification

Each major system component is classified strictly according to empirical runtime verification:

| Component | Path / Module | Operational Status | Reality / Execution Nature |
| :--- | :--- | :---: | :--- |
| **Telemetry Ingestion** | `collectors/system_metrics.py` | **Implemented & Directly Verified** | Real host metrics (`psutil`) for collector machine; real client-side HTTP round-trip timing (`time.perf_counter`) against probe target. |
| **Background Collector** | `collectors/worker.py` | **Implemented & Directly Verified** | Standalone Python background daemon polling every 5s into SQLite. |
| **Telemetry Store** | `storage/telemetry_store.py` | **Implemented & Directly Verified** | SQLite (`telemetry_samples`, `incident_events`). Durable, indexed on timestamp. |
| **Approval Guardrail** | `approval.py` | **Implemented & Directly Verified** | State machine (`recovery_approvals`) using `BEGIN IMMEDIATE` transactions, exact confirmation phrase matching, TTL expiration, single-consumption enforcement. |
| **LSTM Autoencoder** | `dl/anomaly_detector.py` | **Implemented & Directly Verified** | PyTorch model (3,605 parameters). Checkpoint `models/lstm_autoencoder.pt` trained on 100% synthetic sine waves (`generate_normal_windows`). |
| **Live Training Module** | `dl/live_training.py` | **Partially Implemented / Blocked by Data** | Correct chronological splitting and std floors, but requires $\ge 180$ healthy samples (`min_samples=180`). Existing database contains only 31 healthy samples; hence no live model checkpoint exists yet. |
| **Operational Guardrails** | `live_monitoring.py` | **Implemented & Directly Verified** | Deterministic static thresholds: Memory $\ge 95\%$, Probe Latency $\ge 1000$ ms, Status $\ne 200$. Logical OR gate with model anomaly. |
| **Multi-Agent Pipeline** | `agents.py` | **Implemented / Deterministic Offline Fallback** | 5 agent roles (Manager, Investigation, Diagnosis, Resolution, Verification). In offline mode, uses hardcoded string heuristics (`_local_root_cause`) rather than neural LLM reasoning. |
| **Action Simulation** | `simulator.py`, `data/incidents.json` | **Simulated / Controlled-Test-Only** | Static JSON catalog of 6 incidents with deterministic dictionary lookups for action outcomes. |
| **Fault Injection Service**| `demo_service/main.py` | **Simulated / Controlled-Test-Only** | Disposable local test service bound strictly to loopback (`127.0.0.1:8765`). Injects synthetic latency (`asyncio.sleep`) and HTTP 500 exceptions. |
| **Execution Safety Boundary**| `live_monitoring.py` | **Implemented & Directly Verified** | Strict URL validation rejecting remote targets for remediation; loopback-only gate for clearing faults. |
| **Streamlit Dashboard** | `live_monitoring.py`, `app.py` | **Implemented & Directly Verified** | Reactive UI utilizing `@st.fragment(run_every="5s")`. |

---

## 4. Investigation of Windows `is_local_target` Error

### Issue History
Previous reports indicated a runtime failure:
```text
NameError: name 'is_local_target' is not defined in live_monitoring.py (previously reported around line 363)
```

### Empirical Audit Findings
1. Inspection of `live_monitoring.py` confirms that `is_local_target` is now explicitly declared at line 642:
   ```python
   @st.fragment(run_every="5s")
   def live_panel() -> None:
       # Define this before any conditional use.
       is_local_target = _is_loopback_target(service_url)
       service_health = _get_service_health(service_url)
   ```
2. Subsequent usages at line 914 (`if not is_local_target:`), line 1031, and line 1036 reside strictly within the scope of `live_panel()` after this assignment.
3. No code path can execute those lines without first defining `is_local_target`.
4. Automated regression test `test_live_monitoring.py::test_local_service_url_is_restricted_to_loopback` executed and passed cleanly.
5. **Verdict**: The defect was resolved in a prior commit; the error is not reproducible in current revision `e69cb62`.

---

## 5. Baseline Test Execution Record

Execution of `pytest -v` across all 8 test modules:
```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- C:\DL_PROJECT\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\DL_PROJECT
plugins: anyio-4.15.1
collected 36 items

test_agents.py::test_local_agents_work_without_api_key PASSED            [  2%]
test_agents.py::test_local_verification_uses_simulator_result PASSED     [  5%]
test_agents.py::test_simulator_contract_still_works PASSED               [  8%]
test_anomaly_detector.py::test_normal_telemetry_shape_and_values PASSED  [ 11%]
test_anomaly_detector.py::test_detector_returns_expected_fields PASSED   [ 13%]
test_anomaly_detector.py::test_all_injected_incident_profiles_trigger_detection[INC-1001] PASSED [ 16%]
test_anomaly_detector.py::test_all_injected_incident_profiles_trigger_detection[INC-1002] PASSED [ 19%]
test_anomaly_detector.py::test_all_injected_incident_profiles_trigger_detection[INC-1003] PASSED [ 22%]
test_anomaly_detector.py::test_all_injected_incident_profiles_trigger_detection[INC-1004] PASSED [ 25%]
test_anomaly_detector.py::test_all_injected_incident_profiles_trigger_detection[INC-1005] PASSED [ 27%]
test_anomaly_detector.py::test_all_injected_incident_profiles_trigger_detection[INC-1006] PASSED [ 30%]
test_anomaly_detector.py::test_detector_rejects_wrong_shape PASSED       [ 33%]
test_approval.py::test_approval_requires_exact_phrase_and_correct_scope PASSED [ 36%]
test_approval.py::test_approved_ticket_is_bound_to_action_target_and_incident PASSED [ 38%]
test_approval.py::test_approval_can_be_consumed_only_once PASSED         [ 41%]
test_approval.py::test_expired_approval_cannot_be_approved_or_consumed PASSED [ 44%]
test_approval.py::test_ticket_must_exist_and_request_fields_are_required PASSED [ 47%]
test_approval.py::test_approved_ticket_cannot_be_consumed_after_expiry PASSED [ 50%]
test_approval.py::test_rejected_ticket_cannot_be_approved_or_consumed PASSED [ 52%]
test_approval.py::test_concurrent_consumers_can_consume_ticket_only_once PASSED [ 55%]
test_live_monitoring.py::test_local_service_url_is_restricted_to_loopback PASSED [ 58%]
test_live_monitoring.py::test_live_collector_persists_real_style_sample PASSED [ 61%]
test_live_monitoring.py::test_train_and_load_model_from_healthy_rows PASSED [ 63%]
test_live_monitoring.py::test_csv_training_filter_excludes_non_healthy_rows PASSED [ 66%]
test_live_monitoring.py::test_csv_training_requires_health_metadata_or_explicit_confirmation PASSED [ 69%]
test_research_instrumentation.py::test_research_prediction_fields_are_migrated_and_persisted PASSED [ 72%]
test_research_instrumentation.py::test_missing_raw_model_prediction_is_null_not_false PASSED [ 75%]
test_simulator.py::test_incidents_loaded PASSED                          [ 77%]
test_simulator.py::test_known_action_resolves PASSED                     [ 80%]
test_simulator.py::test_forced_failure PASSED                            [ 83%]
test_target_security.py::test_remote_https_target_is_allowed_for_monitoring PASSED [ 86%]
test_target_security.py::test_remote_http_target_is_rejected PASSED      [ 88%]
test_target_security.py::test_credentials_in_url_are_rejected PASSED     [ 91%]
test_target_security.py::test_remote_target_never_passes_local_remediation_gate PASSED [ 94%]
test_workflow.py::test_all_six_incidents_resolve_in_offline_demo_mode PASSED [ 97%]
test_workflow.py::test_payment_api_demo_shows_self_correction PASSED     [100%]

============================= 36 passed in 16.85s =============================
```

---

## 6. Audit Summary of Environment Blockers & Research Boundaries

1. **Host Metrics Limitation**: CPU, Memory, and Disk metrics describe the developer's workstation, not any external service.
2. **Deterministic Agent Evaluation**: When Groq API is not called or lacks network access, agent evaluations reflect deterministic string keyword mappings (`_local_root_cause`), which must not be described as LLM reasoning in the manuscript.
3. **Synthetic Model Checkpoint**: The existing checkpoint `models/lstm_autoencoder.pt` is 100% synthetically trained and must be evaluated strictly on synthetic test distributions or held-out validation data, not conflated with real-world server traffic.
