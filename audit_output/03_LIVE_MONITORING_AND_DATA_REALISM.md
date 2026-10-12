# AegisOps — Live Monitoring Reality Check & Fault Realism Audit

**Audit Phase**: Phases 3 & 4  
**Auditor**: Senior Python Engineer / ML Researcher / SRE / Security Reviewer  
**Scope**: Telemetry Ingestion, Metric Fidelity, Fault Mechanics, and Data Realism

---

## 1. Reality Check: What is Real, What is Demo-Specific, and What is Synthetic?

| Measurement / Field | Source Mechanism | True Nature | Limitations & Reality Check |
| :--- | :--- | :---: | :--- |
| `cpu_pct` | `psutil.cpu_percent(interval=0.15)` | **Real Host Measurement** | Measures the **collector machine** (developer laptop / server), **not** the monitored application or target server. If monitoring a remote target, host CPU reflects local IDE/browser load. |
| `memory_pct` | `psutil.virtual_memory().percent` | **Real Host Measurement** | Measures the collector machine's overall RAM utilization, not the target process or remote host. |
| `disk_pct` | `psutil.disk_usage(anchor).percent` | **Real Host Measurement** | Measures local host filesystem disk percentage. Completely disconnected from remote target storage. |
| `latency_ms` | `time.perf_counter()` over `requests.get(/probe)` | **Real Network / Probe Timing** | Real client-side round-trip time. Combines local DNS, connection establishment, server processing, and network jitter. |
| `status_code` | `response.status_code` | **Real HTTP Observation** | Real response code from HTTP server. |
| `error_rate_pct` | Rolling percentage over last 20 probe calls in SQLite | **Derived Real Metric** | Calculated as `100 * sum(status != 200) / len(samples)`. Window size fixed at 20. |
| `fault_mode` | JSON payload field from `/probe` or `/health` | **Demo-Service Synthetic Artifact** | **Only exists on AegisOps `demo_service`**. Real-world microservices do not return a `fault_mode` key in their JSON payloads. Returns `"unknown"` on all external targets. |
| `service_available` | Boolean: `status_code == 200` | **Derived Observation** | Equates any non-200 (including 201, 204, or 302) with service unavailability. |
| `models/lstm_autoencoder.pt` | `generate_normal_windows()` | **100% Synthetic Data** | Pure mathematical synthetic sine waves with gaussian noise. Never touched real system telemetry. |
| `data/incidents.json` | Static JSON file | **100% Synthetic Data** | Hardcoded incident descriptions, fake logs, and boolean action maps. |

---

## 2. Answers to Core Operational Questions

### 1. Which data comes from actual system measurements?
- Collector-host CPU percentage (`psutil.cpu_percent`).
- Collector-host RAM percentage (`psutil.virtual_memory`).
- Collector-host disk percentage (`psutil.disk_usage`).
- HTTP round-trip latency (`requests.get` timed with `time.perf_counter`).
- HTTP response status code.

### 2. Which data is generated synthetically?
- The offline incident catalog in `data/incidents.json`.
- The training data for the legacy model `models/lstm_autoencoder.pt` (`generate_normal_windows`).
- Injected incident windows in `dl/anomaly_detector.py:67` (`generate_incident_telemetry`).
- Simulated resolution results in `simulator.py:18` (`execute_action`).

### 3. Which measurements come only from the project's own demo service?
- The `fault_mode` telemetry attribute (`normal`, `latency`, `error`).
- The application diagnostic log stream (`GET /logs`) queried by `_service_logs()`. Real-world services do not expose an unauthenticated `/logs` endpoint returning in-memory ring-buffer items.

### 4. Can an arbitrary application be monitored without modifying its source code?
**Partially (Black-box HTTP probe only), with significant architectural caveats:**
- **What works**: Any HTTP/HTTPS service exposing a health check, status page, or REST endpoint can have its latency and status code monitored via `AEGISOPS_SERVICE_URL` and `AEGISOPS_PROBE_PATH`.
- **What fails**:
  1. **Host metric decoupling**: The CPU, memory, and disk metrics will reflect the *collector host*, not the target application.
  2. **Model training lockout**: `healthy_training_samples()` (`storage/telemetry_store.py:98`) filters on `WHERE fault_mode = 'normal'`. Arbitrary applications return `fault_mode = 'unknown'`, meaning **the database query returns zero samples**, locking out live model training unless the code is altered or `--assume-healthy` is used via CLI.
  3. **Remediation lockout**: Recovery is strictly blocked for non-loopback targets by `validate_local_service_url()`.

### 5. Can the system monitor a remote service safely and securely?
**Yes, in read-only mode.**
- Enforces HTTPS for all non-loopback targets (`validate_monitoring_target_url`).
- Rejects plaintext HTTP for remote hosts.
- Rejects embedded credentials in target URLs (`https://user:pass@host`).
- Supports bearer token authentication via `AEGISOPS_BEARER_TOKEN`.
- Remediation and fault-injection endpoints are strictly loopback-gated (`127.0.0.1`, `localhost`, `::1`).

### 6. Does monitoring continue if Streamlit closes?
**No, unless `python -m collectors.worker` is executed separately.**
- The web dashboard uses a Streamlit fragment (`@st.fragment(run_every="5s")`). When the browser tab closes or the server shuts down, sampling halts.
- To maintain continuous monitoring, operators must run the worker daemon (`collectors/worker.py`).
- **Warning**: Running both simultaneously causes duplicate sample insertion because no database lock or process coordination exists.

### 7. Are collection failures, missing values, and stale telemetry detected?
**Incomplete Handling:**
- **Connection timeouts / connection errors**: Caught in `collectors/system_metrics.py:103` (`requests.RequestException`). Records `status_code = 0`, `service_available = False`, and sets latency to elapsed timeout time.
- **Missing / Stale Telemetry**: **Not detected**. The dashboard merely selects `SELECT * FROM telemetry_samples ORDER BY id DESC LIMIT 1`. If the collector process died 6 hours ago, the UI displays the 6-hour-old row as the current metric without an "outdated telemetry" alert.

### 8. Is the collected data sufficient for meaningful root-cause analysis?
**No. Telemetry is too coarse for production RCA:**
- Only 5 coarse time-series metrics: Host CPU, Host RAM, Host Disk, HTTP Latency, HTTP Status.
- Lacks application-level APM metrics: database connection pool utilization, thread saturation, JVM/garbage collection pauses, queue depths, inbound request concurrency, network packet drop, or distributed tracing.
- The diagnosis agent can identify *symptoms* (e.g. elevated latency), but cannot pinpoint application root causes (e.g., specific SQL query lock, deadlocked thread) without target-level telemetry.

---

## 3. Fault Mechanism & Simulation Fidelity Audit

### A. Supported Fault Types in `demo_service/main.py`
1. **Latency Fault (`mode: "latency"`)**:
   - Implementation (`demo_service/main.py:56`): `await asyncio.sleep(delay / 1000)`.
   - Delay configurable between 100ms and 5000ms (default 1200ms).
   - Fidelity: **Synthetic sleep delay**. Does not generate true thread pool exhaustion, CPU thrashing, or connection backlog queues.
2. **Error Fault (`mode: "error"`)**:
   - Implementation (`demo_service/main.py:60`): `raise HTTPException(status_code=500, detail="Injected local test fault: HTTP 500")`.
   - Fidelity: **Direct synthetic exception**. Does not originate from database failure, out-of-memory crash, or corrupted payload.

### B. Fault State Management & Cleanup
- **State Storage**: In-memory global variables `_fault_mode` and `_delay_ms` guarded by a threading lock `_state_lock` (`demo_service/main.py:14`).
- **Persistence**: Not persisted across process restarts. Restarting the test service automatically resets the fault mode to `"normal"`.
- **Fault Cleanup Guarantee**: **None**. There is no automatic TTL on injected faults. If a fault is injected and the test suite or operator crashes, the service remains faulty indefinitely until `/admin/fault` is called with `mode: "normal"` or the process is restarted.
- **Ground Truth Recording**: `demo_service` logs timestamped events in an in-memory deque `_request_log` (limit 500) (`demo_service/main.py:17`), recording `timestamp, path, status_code, latency_ms, fault_mode`.

---

## 4. Component Classification Register

| Component / Subsystem | Code Location | Classification | Evidence & Operational Role |
| :--- | :--- | :---: | :--- |
| Host Telemetry Collection | `collectors/system_metrics.py:78-80` | **A. Real System Measurement** | Reads actual OS metrics via `psutil`. |
| HTTP Probe Timer | `collectors/system_metrics.py:81-105` | **A. Real System Measurement** | Executes live HTTP GET and times socket response via `time.perf_counter`. |
| SQLite Telemetry Store | `storage/telemetry_store.py` | **A. Real System Measurement** | Stores real runtime records in durable SQLite tables. |
| Approval Store | `approval.py` | **A. Real System Measurement** | Real database transactions, TTL calculations, and atomic locks. |
| Local Demo Service | `demo_service/main.py` | **D. Controlled Fault Mechanism** | Local FastAPI process simulating 500 errors and sleep delays. |
| Live Anomaly Guardrails | `live_monitoring.py:165-204` | **A. Real System Measurement** | Live rule evaluation over collected metrics. |
| Live LSTM Autoencoder | `dl/live_training.py` | **A. Real System Measurement** | Real PyTorch training on real collected telemetry. |
| Synthetic Incident Catalog | `data/incidents.json` | **B. Synthetic / Simulated Behavior** | Hardcoded incident templates for evaluation. |
| Synthetic Model Checkpoint | `models/lstm_autoencoder.pt` | **B. Synthetic / Simulated Behavior** | Trained on artificial mathematical curves. |
| Action Executor Simulator | `simulator.py` | **B. Synthetic / Simulated Behavior** | Boolean dictionary lookup table simulating remediation. |
| Synthetic Evaluator | `dl/evaluate_detector.py` | **C. Mock or Test Fixture** | Benchmark utility running solely against generated numpy arrays. |
| Groq LLM Agent Calls | `agents.py:65` | **A. Real System Measurement** | Live external API calls to Groq endpoint when key provided. |
| Offline Agent Logic | `agents.py:84` | **B. Synthetic / Simulated Behavior** | Hardcoded string heuristics imitating agent decisions. |

---

## 5. Requirements for Scientifically Defensible, Isolated Experimentation

To transform AegisOps from a single-machine research prototype into an academically rigorous benchmarking platform:

1. **Dockerized Target Environment**:
   - Move the target service into an isolated container (e.g. standard microservices like Google's Online Boutique or TrainTicket).
2. **True Fault Injection (Chaos Engineering)**:
   - Replace `asyncio.sleep` with kernel-level or network-level disruptions:
     - Network delay and packet loss using Linux `tc` (traffic control) / NetEm or Chaos Mesh.
     - Process CPU starvation using `stress-ng` or cgroups CPU quotas.
     - Database connection pool exhaustion using simulated traffic spikes.
3. **Decoupled Telemetry Agents**:
   - Deploy lightweight metric exporters (e.g. Prometheus Node Exporter + cAdvisor) inside the target container to collect target-specific CPU/RAM rather than collector-host metrics.
4. **Automated Experiment Harness**:
   - Record exact microsecond timestamps for fault onset, fault duration, agent alert latency, approval delay, remediation duration, and recovery confirmation.
