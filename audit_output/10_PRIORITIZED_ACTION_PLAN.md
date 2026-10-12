# AegisOps — Prioritized Action Plan & Engineering Backlog

**Audit Phase**: Phase 11  
**Auditor**: Senior Python Engineer / ML Researcher / SRE / Security Reviewer  
**Scope**: Practical, Phased Engineering Roadmap (P0 through P3)

---

## 1. Backlog Overview

| Priority Level | Focus Area | Milestone Target | Task Count |
| :--- | :--- | :--- | :---: |
| **P0 (Critical)** | Correctness, Crash Prevention, Security & Concurrency Safety | Immediate / Before Any Demo | 3 Tasks |
| **P1 (High)** | Reliable Monitoring, Experiment Harness & Telemetry Decoupling | Before Empirical Experiments | 4 Tasks |
| **P2 (Medium)** | Scientific Baselines, Ablations & Empirical Benchmark Runner | Before Paper Submission | 4 Tasks |
| **P3 (Future)** | Production Hardening, Multi-Target Orchestration & Enterprise RBAC | Production Pilot / Long-Term | 4 Tasks |

---

## 2. P0: Critical Safety, Correctness, and Crash Prevention

### Task P0-01: Wrap Groq Client Calls with Exception Handling and Retry Backoff
- **Problem**: `GroqAgent.run` (`agents.py:65`) makes direct calls to `self.client.chat.completions.create` without try/except handling. Network dropouts, socket timeouts, or HTTP 429 rate limits crash the application. `MAX_RETRIES` in `config.py` is dead code.
- **Evidence**: `agents.py:65-74`, `config.py:11`.
- **Proposed Solution**: Wrap API calls with `tenacity` retry loop with exponential backoff. Catch `groq.APIError` and fall back gracefully to `_run_local(payload)` with an audit warning.
- **Acceptance Criteria**: When Groq API is offline or rate-limited, the system does not crash; it logs a warning and falls back to deterministic offline behavior.
- **Verification Test**: Mock `client.chat.completions.create` raising `groq.RateLimitError(429)`; verify fallback output is returned.
- **Milestone**: Immediate (Before Live LLM Testing).

### Task P0-02: Prevent Duplicate Database Sampling between Dashboard and Worker Daemon
- **Problem**: If an operator starts `collectors.worker` while the Streamlit dashboard is open with "Collect live metrics every 5 seconds" checked, both processes insert duplicate samples into `telemetry_samples` at the same timestamps.
- **Evidence**: `live_monitoring.py:665`, `collectors/worker.py:42`, `WINDOWS_DEPLOYMENT.md:10`.
- **Proposed Solution**: Implement an advisory file lock (e.g. `fasteners.InterProcessLock` or a database singleton table `collector_lease` with a 15-second heartbeat) so only one active collector can sample at any given moment.
- **Acceptance Criteria**: When `collectors.worker` is active, the Streamlit dashboard detects the external lease and disables internal sampling automatically.
- **Verification Test**: Launch both processes simultaneously; verify sample count increases by exactly 1 per 5-second interval.
- **Milestone**: Immediate (Before Extended Collection).

### Task P0-03: Enforce Loopback-Only Binding by Default Across All Startup Scripts
- **Problem**: `run.bat` and `run_worker.bat` do not explicitly pass `--server.address 127.0.0.1` to Streamlit, potentially binding to `0.0.0.0` depending on local Streamlit configuration and exposing the unauthenticated UI.
- **Evidence**: `run.bat:20`, `SECURITY.md:20`.
- **Proposed Solution**: Update `run.bat` to execute `streamlit run app.py --server.address 127.0.0.1 --server.port 8501`.
- **Acceptance Criteria**: All batch and shell scripts explicitly enforce loopback binding.
- **Verification Test**: Execute `run.bat`; confirm network socket binds strictly to `127.0.0.1:8501`.
- **Milestone**: Immediate (Before Shared Environment Execution).

---

## 3. P1: Reliable Live Monitoring & Experiment Rigor

### Task P1-01: Remove `fault_mode = 'normal'` Hardcoding in Telemetry Training Filter
- **Problem**: `TelemetryStore.healthy_training_samples()` (`storage/telemetry_store.py:98`) filters training data with `AND fault_mode = 'normal'`. Real-world applications do not return a `fault_mode` JSON field, causing the query to return 0 rows and locking out live training.
- **Evidence**: `storage/telemetry_store.py:98`, `collectors/system_metrics.py:100`.
- **Proposed Solution**: Modify query to:
  ```sql
  WHERE service_available = 1 AND status_code = 200 AND error_rate_pct = 0
    AND (fault_mode = 'normal' OR fault_mode = 'unknown')
    AND cpu_pct < 90 AND memory_pct < 95 AND disk_pct < 95 AND latency_ms < 1000
  ```
- **Acceptance Criteria**: Live LSTM training succeeds on telemetry collected from external HTTPS services.
- **Verification Test**: Collect 180 samples against an external HTTPS test target; verify `train_live_model` executes successfully.
- **Milestone**: Required Before Empirical Experiments.

### Task P1-02: Implement Telemetry Staleness and Collector Liveness Detection
- **Problem**: If the collector process halts or crashes, the dashboard continues displaying the last recorded database row without warning, presenting hours-old data as current live metrics.
- **Evidence**: `live_monitoring.py:686`.
- **Proposed Solution**: Check timestamp of latest sample against `datetime.now(timezone.utc)`. If elapsed time exceeds $3 \times \text{INTERVAL}$ (15 seconds), display a prominent warning: `STALE TELEMETRY · Collector appears inactive`.
- **Acceptance Criteria**: Dashboard alerts the operator immediately when new telemetry stops arriving.
- **Verification Test**: Stop collector; verify warning banner appears on next fragment tick.
- **Milestone**: Required Before Live Monitoring Pilot.

### Task P1-03: Decouple Collector Host Metrics from Monitored Target Metrics
- **Problem**: Host CPU, RAM, and Disk metrics are measured on the collector machine (`psutil`), not the target server.
- **Evidence**: `collectors/system_metrics.py:72`.
- **Proposed Solution**: Support reading target host metrics via standard Prometheus Node Exporter endpoints (`/metrics`) or CloudWatch/Datadog APIs when monitoring remote targets.
- **Acceptance Criteria**: Target server CPU and RAM are recorded instead of developer laptop metrics.
- **Verification Test**: Run CPU stress on remote target; verify `cpu_pct` spikes on dashboard while collector laptop CPU remains low.
- **Milestone**: Required Before Multi-Node Experiments.

### Task P1-04: Containerize Test Environment with Docker Compose
- **Problem**: Current tests run directly against host processes on localhost ports 8501 and 8765, risking port conflicts and lacking isolation.
- **Evidence**: `run_all.ps1:7`, `WINDOWS_DEPLOYMENT.md:8`.
- **Proposed Solution**: Provide a standard `docker-compose.yml` defining the target service, Prometheus exporter, collector daemon, and dashboard.
- **Acceptance Criteria**: Environment can be stood up and torn down via `docker compose up -d` and `docker compose down`.
- **Verification Test**: Run clean clone in container; verify full end-to-end workflow passes.
- **Milestone**: Required Before Benchmark Data Collection.

---

## 4. P2: Scientific Baselines & Paper Contributions

### Task P2-01: Implement Standard ML Baselines (Isolation Forest & Static Rules)
- **Problem**: Current repo only contains the LSTM Autoencoder and static bootstrap rules. Peer-reviewed papers require baseline comparisons.
- **Evidence**: `dl/anomaly_detector.py`, `dl/live_training.py`.
- **Proposed Solution**: Implement `IsolationForestDetector` (scikit-learn) and `StatisticalBaselineDetector` (3-sigma rolling z-score) with identical `.detect(window)` interfaces.
- **Acceptance Criteria**: Benchmark script can evaluate LSTM vs Isolation Forest vs Static Rules on identical time-series windows.
- **Verification Test**: Run comparative evaluation script; output joint precision, recall, F1, and latency table.
- **Milestone**: Required Before Paper Submission.

### Task P2-02: Build Automated Chaos Injection and Labeling Harness
- **Problem**: Injected faults in `demo_service` are simple sleep delays; there is no automated dataset recorder for empirical trials.
- **Evidence**: `demo_service/main.py:56`.
- **Proposed Solution**: Build an automated runner that injects 5 fault types across 50 trials, recording microsecond-accurate ground-truth timestamps for onset, alert, diagnosis, and recovery.
- **Acceptance Criteria**: Generates an independently labeled CSV containing 50 labeled incident trials.
- **Verification Test**: Execute automated harness; confirm 50 labeled trials are persisted with ground-truth metadata.
- **Milestone**: Required Before Paper Submission.

### Task P2-03: Implement Grounding Precision and Hallucination Metrics
- **Problem**: No automated evaluation metrics exist for evaluating agent diagnosis quality.
- **Evidence**: `agents.py:124`.
- **Proposed Solution**: Implement an automated scoring script that parses diagnosis outputs and evaluates Top-1 diagnostic accuracy and evidence grounding precision against injected fault ground truth.
- **Acceptance Criteria**: Produces quantitative accuracy and hallucination tables for the research paper.
- **Verification Test**: Evaluate agent outputs across 50 trials; verify scores match manual annotations.
- **Milestone**: Required Before Paper Submission.

### Task P2-04: Execute Ablation Study: Multi-Agent vs Single-Agent Prompting
- **Problem**: No experimental evidence proves that 5 sequential agents outperform a single unified prompt.
- **Evidence**: `agents.py:208`.
- **Proposed Solution**: Implement `SinglePromptAgent` baseline that performs triage, investigation, diagnosis, and action selection in a single LLM call. Compare against `IncidentAgents`.
- **Acceptance Criteria**: Quantifies trade-offs between accuracy, latency, and token cost across architectures.
- **Verification Test**: Run both architectures on 50 incident trials; output comparative performance metrics.
- **Milestone**: Required Before Paper Submission.

---

## 5. P3: Enterprise Production Hardening

### Task P3-01: Multi-Tenant Authentication & Role-Based Access Control (RBAC)
- **Problem**: Dashboard has zero authentication; approval ticket requester and approver can be identical unauthenticated users.
- **Proposed Solution**: Integrate OIDC/OAuth2 (Keycloak / Okta). Enforce separation of duties: `requester_id != approver_id`.
- **Milestone**: Production Pilot.

### Task P3-02: Migrate from SQLite to PostgreSQL with Connection Pooling
- **Problem**: SQLite cannot sustain concurrent writes from distributed collectors and dashboard instances without lock contention.
- **Proposed Solution**: Introduce SQLAlchemy / asyncpg persistence layer targeting PostgreSQL with PgBouncer.
- **Milestone**: Production Pilot.

### Task P3-03: Externalize Audit Trail to Immutable Append-Only Storage
- **Problem**: Audit events in local SQLite can be tampered with or deleted by local users.
- **Proposed Solution**: Forward all `recovery_approval_*` and `recovery_execution_*` events to an external SIEM or WORM log storage (e.g. AWS CloudWatch / Splunk).
- **Milestone**: Production Pilot.

### Task P3-04: Asynchronous Agent Worker Queues (Temporal / Celery)
- **Problem**: Agent calls run synchronously inside the Streamlit UI thread, blocking user interaction during multi-second LLM calls.
- **Proposed Solution**: Move agent orchestration to background worker tasks managed via Temporal or Celery with WebSocket status updates.
- **Milestone**: Production Pilot.
