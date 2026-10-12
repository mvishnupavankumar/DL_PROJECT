# AegisOps — Repository Inventory & Codebase Mapping

**Date**: 2026-10-11  
**Auditor**: Senior Python Engineer / ML Researcher / SRE / Security Reviewer  
**Repository Root**: `c:\DL_PROJECT`  
**Git Branch**: `main`  
**Latest Commit**: `ce1a4cc` ("first commit")  
**Initial Commit**: `a423f37`  

---

## 1. Directory Tree & Structural Mapping

```text
c:\DL_PROJECT\
├── .git/                                 # Git version control metadata (2 commits)
├── .gitignore                            # Ignores .venv, __pycache__, .env, *.pyc, *.pt (except base)
├── .env.example                          # [AUDITOR-CREATED] Configuration template for environment variables
├── .env                                  # [AUDITOR-CREATED] Local active configuration (loopback defaults)
├── app.py                                # Main Streamlit UI entry point
├── live_monitoring.py                    # Complete Live Monitoring UI & orchestration engine (1,289 lines)
├── agents.py                             # Multi-agent incident response system (Groq LLM + offline fallback)
├── approval.py                           # SQLite-backed one-time scoped approval ticket store
├── config.py                             # Environment variable loader (Groq API, model, retry settings)
├── simulator.py                          # Synthetic incident demo executor (table lookup from incidents.json)
├── requirements.txt                      # Declared Python package dependencies
├── run.bat                               # Windows CMD launcher for Streamlit + dependency check
├── run.sh                                # Unix shell launcher for Streamlit + dependency check
├── run_all.bat                           # Windows CMD launcher for demo service + Streamlit
├── run_all.ps1                           # PowerShell launcher for demo service + Streamlit
├── run_worker.bat                        # Windows CMD launcher for independent background collector
├── README.md                             # High-level architecture and usage guide
├── START_HERE.md                         # Detailed operator walkthrough for Windows
├── WINDOWS_DEPLOYMENT.md                 # Hardening checklist and operational guidelines
├── SECURITY.md                           # Threat model and vulnerability scope disclaimer
├── collectors/                           # Telemetry collection subsystem
│   ├── __init__.py                       # Package initializer
│   ├── README.md                         # Subsystem overview
│   ├── system_metrics.py                 # psutil host metrics + timed HTTP probe collector
│   └── worker.py                         # Autonomous background collection daemon
├── demo_service/                         # Local target service for fault simulation
│   ├── __init__.py                       # Package initializer
│   └── main.py                           # FastAPI service (/probe, /health, /logs, /admin/fault)
├── dl/                                   # Deep Learning anomaly detection subsystem
│   ├── __init__.py                       # Package initializer
│   ├── anomaly_detector.py               # LSTM Autoencoder architecture & synthetic generator
│   ├── evaluate_detector.py              # Synthetic smoke-test evaluator (precision, recall, F1)
│   ├── live_training.py                  # Live telemetry dataset slicing, training, calibration
│   ├── train_from_csv.py                 # CLI utility for training from exported CSV telemetry
│   └── train_model.py                    # Training script for synthetic model checkpoint
├── models/                               # Model checkpoints and serialization metadata
│   ├── lstm_autoencoder.pt               # Trained PyTorch checkpoint (synthetic demo model, ~19.8 KB)
│   └── lstm_autoencoder.json             # Calibration metadata & scaling statistics for synthetic model
├── data/                                 # Static incident datasets and runtime database
│   ├── incidents.json                    # 6 predefined synthetic incident definitions
│   └── aegisops_live.sqlite3             # Runtime SQLite database (telemetry, events, approvals)
├── test_*.py                             # Pytest test suite (7 test suites, 34 total test cases)
│   ├── test_agents.py                    # Unit tests for agents in offline deterministic mode
│   ├── test_anomaly_detector.py          # Unit tests for LSTM autoencoder math & shapes
│   ├── test_approval.py                  # Unit tests for approval ticket state machine & race conditions
│   ├── test_live_monitoring.py           # Unit tests for loopback checks, live collector, and training
│   ├── test_simulator.py                 # Unit tests for synthetic incident executor
│   ├── test_target_security.py           # Unit tests for URL security policies and scheme validation
│   └── test_workflow.py                  # Integration tests for 6 synthetic incident workflows
└── audit_output/                         # [AUDITOR-CREATED] Comprehensive technical audit deliverables
```

---

## 2. Python Source Files & Module Responsibilities

| File Path | Lines | Key Classes / Functions | Primary Responsibility | Classification |
| :--- | :---: | :--- | :--- | :--- |
| `app.py` | 26 | `st.set_page_config`, `render_live_monitoring` | Entry point for the Streamlit dashboard; sets page styling and delegates to `live_monitoring`. | Production / UI Entry |
| `live_monitoring.py` | 1,289 | `render_live_monitoring`, `_analyze_latest`, `_bootstrap_analysis`, `_build_live_incident`, `_inject_fault`, `_run_agent_investigation`, `_resolve_local_test_fault` | Primary UI and controller. Orchestrates real-time fragment refreshes (`@st.fragment(run_every="5s")`), telemetry display, anomaly scoring, agent triggers, approval flow, and local remediation. | Core Engine / Hybrid |
| `agents.py` | 267 | `AgentResult`, `GroqAgent`, `IncidentAgents`, `_local_root_cause`, `_preferred_actions` | Implements 5-agent incident response team (Manager, Investigator, Diagnosis, Resolution, Verification). Supports Groq LLM API and deterministic keyword-matching offline mode. | Core Subsystem |
| `approval.py` | 149 | `ApprovalStore`, `ApprovalError`, `request`, `approve`, `consume`, `reject`, `get` | Atomic SQLite-backed approval ticket lifecycle manager. Enforces time-to-live (TTL), exact confirmation phrases, and one-time consumption. | Security / Governance |
| `config.py` | 12 | `GROQ_API_KEY`, `GROQ_MODEL`, `MAX_RETRIES` | Loads environment variables via `python-dotenv`. Filters placeholder keys. | Configuration |
| `simulator.py` | 32 | `get_incidents`, `get_incident`, `execute_action` | Synthetic demo evaluator. Simulates incident actions via boolean lookup table in `data/incidents.json`. | Legacy / Demo-Only |
| `collectors/system_metrics.py` | 140 | `validate_local_service_url`, `validate_monitoring_target_url`, `_disk_usage_percent`, `collect_live_sample` | Collects local host metrics via `psutil` (CPU, RAM, Disk) and times an HTTP GET probe against the target URL. | Core Telemetry |
| `collectors/worker.py` | 59 | `main`, `_stop` | Headless CLI daemon that collects and persists samples every 5s independently of Streamlit. | Core Infrastructure |
| `demo_service/main.py` | 79 | `app`, `root`, `health`, `probe`, `logs`, `set_fault` | Local FastAPI service running on port 8765. Simulates controllable delay (latency mode) or HTTP 500 errors. | Test Fixture / Demo |
| `dl/anomaly_detector.py` | 273 | `LSTMAutoencoder`, `TelemetryAnomalyDetector`, `generate_normal_windows`, `generate_incident_telemetry`, `train_and_save_model`, `load_detector` | PyTorch LSTM autoencoder architecture, Z-score normalization, reconstruction scoring, synthetic signal generator, and synthetic training pipeline. | Core ML & Synthetic |
| `dl/live_training.py` | 111 | `train_live_model`, `load_live_detector`, `_windows` | Trains an LSTM autoencoder checkpoint using healthy real live telemetry from SQLite or CSV. | Core ML Training |
| `dl/train_from_csv.py` | 73 | `load_healthy_samples`, `main` | CLI tool to filter and train a model from exported CSV telemetry. | ML Training Utility |
| `dl/train_model.py` | 20 | `main` | CLI script to generate the synthetic checkpoint `models/lstm_autoencoder.pt`. | Synthetic Utility |
| `dl/evaluate_detector.py` | 49 | `main` | Evaluates synthetic model against 200 normal and 60 synthetic fault windows. | Synthetic Smoke Test |
| `storage/telemetry_store.py` | 130 | `TelemetryStore`, `add_sample`, `recent_samples`, `healthy_training_samples`, `annotate_sample`, `log_event`, `recent_events` | SQLite persistence layer for telemetry samples (`telemetry_samples`) and audit log entries (`incident_events`). | Persistence Layer |

---

## 3. Test Files & Coverage Mapping

| Test File | Lines | Test Functions Count | Scope & Components Covered |
| :--- | :---: | :---: | :--- |
| `test_agents.py` | 39 | 3 | Offline mode execution, deterministic root-cause matching, simulator action resolution. |
| `test_anomaly_detector.py` | 46 | 4 | Synthetic normal window shapes, return dictionary schema, 6 incident profiles crossing threshold, shape error rejection. |
| `test_approval.py` | 170 | 8 | Exact phrase requirement, scope binding, one-time consumption, expiration enforcement, invalid ticket rejection, rejection state, concurrent double-spend race prevention (via `Barrier` and `ThreadPoolExecutor`). |
| `test_live_monitoring.py` | 110 | 5 | Loopback restriction validation, mocked live sample collection/persistence, live model training/inference, CSV health filter rules. |
| `test_simulator.py` | 22 | 3 | Loading `data/incidents.json`, known action success, forced failure flag. |
| `test_target_security.py` | 22 | 4 | HTTPS remote target requirement, plaintext remote HTTP rejection, embedded credential rejection, remote remediation blocking. |
| `test_workflow.py` | 63 | 2 | End-to-end resolution of all 6 synthetic incidents in offline mode; self-correction multi-step retry loop. |
| **Total** | **472** | **29 test defs (34 cases)** | **All 34 test cases passing via `pytest -q`.** |

---

## 4. Database Schemas & Persistence

All database operations reside in `data/aegisops_live.sqlite3` across three tables:

### A. Table: `telemetry_samples` (managed by `TelemetryStore`)
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `timestamp` TEXT NOT NULL (ISO 8601 with milliseconds)
- `cpu_pct` REAL NOT NULL (Local host CPU %)
- `memory_pct` REAL NOT NULL (Local host RAM %)
- `latency_ms` REAL NOT NULL (Client round-trip probe latency in ms)
- `error_rate_pct` REAL NOT NULL (Rolling error % over last 20 probe calls)
- `disk_pct` REAL NOT NULL (Local host root disk %)
- `service_available` INTEGER NOT NULL (1 if HTTP 200, else 0)
- `status_code` INTEGER NOT NULL (HTTP response code or 0 on connection error)
- `error_message` TEXT NOT NULL DEFAULT ''
- `fault_mode` TEXT NOT NULL DEFAULT 'unknown' (`normal`, `latency`, `error`, `unknown`)
- `data_source` TEXT NOT NULL
- `anomaly_score` REAL NULL (Reconstruction MSE from LSTM or NULL if rules)
- `is_anomaly` INTEGER NULL (1 if anomaly flagged, 0 if normal)
- `detector_mode` TEXT NOT NULL DEFAULT 'bootstrap_rules' (`bootstrap_rules` or `live_lstm_autoencoder`)
- *Index*: `idx_telemetry_timestamp` on `timestamp`

### B. Table: `incident_events` (managed by `TelemetryStore`)
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `timestamp` TEXT NOT NULL (ISO 8601)
- `event_type` TEXT NOT NULL (e.g., `live_agent_investigation`, `recovery_approval_requested`, `recovery_approval_granted`, `recovery_approval_consumed`, `recovery_execution_finished`)
- `payload_json` TEXT NOT NULL (Serialized JSON containing context, agent outputs, tickets, or error stacks)

### C. Table: `recovery_approvals` (managed by `ApprovalStore`)
- `ticket_id` TEXT PRIMARY KEY (UUID v4 string)
- `action_id` TEXT NOT NULL (`clear_demo_service_fault`)
- `target` TEXT NOT NULL (`http://127.0.0.1:8765`)
- `incident_id` TEXT NOT NULL (`LIVE-000xxx`)
- `status` TEXT NOT NULL CHECK (`status IN ('pending','approved','rejected','consumed','expired')`)
- `requested_by` TEXT NOT NULL (Audit string, e.g. `local_operator`)
- `approved_by` TEXT NULL (Audit string)
- `created_at` TEXT NOT NULL
- `expires_at` TEXT NOT NULL
- `approved_at` TEXT NULL
- `consumed_at` TEXT NULL
- *Index*: `idx_approval_status` on `status, expires_at`

---

## 5. Model Architecture & Artifact Inventory

1. **`models/lstm_autoencoder.pt` & `models/lstm_autoencoder.json`**
   - **Origin**: Trained on synthetic sine waves and injected gaussian noise (`generate_normal_windows`).
   - **Parameters**: 4,741 trainable parameters (Encoder LSTM 5->16, Decoder LSTM 16->16, Linear 16->5).
   - **Target**: Used only by synthetic test fixtures (`test_anomaly_detector.py`, `test_workflow.py`, `evaluate_detector.py`).
   - **Runtime role in Live Dashboard**: **Unused**. Explicitly bypassed by `live_monitoring.py`.
2. **`models/live_lstm_autoencoder.pt` & `models/live_lstm_autoencoder.json`**
   - **Origin**: Generated dynamically on user request via the Streamlit dashboard or `dl.train_from_csv`.
   - **Training Data**: Real host metrics and local service HTTP probe readings stored in SQLite.
   - **Threshold**: 99th percentile of held-out healthy validation windows.

---

## 6. Documentation Discrepancies & Missing Files

During the inventory scan, several documentation references were cross-checked against actual filesystem paths:

| Referenced In Document | Referenced File Name | Actual File Status | Impact / Finding |
| :--- | :--- | :--- | :--- |
| `README.md:46`, `START_HERE.md:104` | `LIVE_DATA_GUIDE.md` | **MISSING** (File does not exist in repo) | Operators looking for advanced live dataset guidelines will encounter dead links. |
| `README.md:47`, `START_HERE.md:104` | `RESEARCH_PLAN.md` | **MISSING** (File does not exist in repo) | Research objectives and methodology plan claimed in README tree are not present. |
| `START_HERE.md:93`, `SECURITY.md:25` | `OPERATIONS.md` | **MISSING** (File does not exist in repo) | Operational and pilot security procedures are referenced but missing. |
| `START_HERE.md:16`, `README.md:64`, `run.bat:12` | `.env.example` | **ORIGINALLY MISSING** (Created by Auditor during setup) | Initial setup instruction `Copy-Item .env.example .env` failed out-of-the-box until auditor wrote template. |
| `README.md:7` | "Incident Demo workspace" | **REMOVED** from UI, retained in code | `simulator.py` and `data/incidents.json` remain in repo for unit tests, but dashboard only exposes Live Monitoring. |

---

## 7. Duplicate, Obsolete, and Unused Modules

1. **`simulator.py` & `data/incidents.json`**:
   - Status: Obsolete for live operations; retained solely for `test_workflow.py` and `test_simulator.py`.
   - The live monitoring engine has its own incident constructor (`_build_live_incident`) and local remediation handler (`_resolve_local_test_fault`), rendering `simulator.execute_action` completely bypassed in runtime.
2. **`dl/train_model.py` & `dl/evaluate_detector.py`**:
   - Status: Demo/synthetic artifacts. They operate exclusively on synthetic numpy arrays and have no connection to live telemetry or SQLite database.
3. **`config.MAX_RETRIES`**:
   - Status: Dead configuration. Defined in `config.py` line 11, but never imported or referenced in `agents.py` or any other module.
