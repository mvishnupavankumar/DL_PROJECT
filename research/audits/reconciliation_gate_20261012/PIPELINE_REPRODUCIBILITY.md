# AegisOps: Pipeline Reproducibility & Execution Audit (Task 5)

**Audit Date**: 2026-10-12  
**Auditor**: Senior ML Systems & Reproducibility Specialist  
**Target Script**: [`research/run_all.py`](file:///c:/DL_PROJECT/research/run_all.py)  
**Execution Environment**: Windows 11, PowerShell, Repository Virtual Environment (`.venv\Scripts\python.exe`, Python 3.11.9)  
**Execution Command**:
```powershell
.\.venv\Scripts\python.exe research/run_all.py
```

---

## 1. Execution Summary & Captured Output

The unified pipeline was executed from a clean state after confirming that all remote services were excluded and the original database (`data/aegisops_live.sqlite3`) was protected.

### Execution Log & Telemetry
```
================================================================================
AEGISOPS UNIFIED EXPERIMENT & REPRODUCIBILITY SUITE
================================================================================

[Step 1/5] Running Pytest Regression Suite (42 tests)...
..........................................                               [100%]
42 passed in 17.11s

[Step 2/5] Running Experiment A (Anomaly Detection)...
======================================================================
EXPERIMENT A: ANOMALY DETECTION EVALUATION
======================================================================
Loaded LSTM Autoencoder (Threshold: 0.709399)
Calibrated Isolation Forest Threshold (99th pct on val): -0.018694
Held-out test set: 200 normal windows, 120 incident windows
Saved raw test predictions: C:\DL_PROJECT\research\results\detection_predictions.csv
Saved detection metrics: C:\DL_PROJECT\research\results\detection_metrics.csv
Saved scenario breakdown: C:\DL_PROJECT\research\results\detection_by_scenario.csv

[Step 3/5] Running Experiment B (Diagnosis Rubric Evaluation)...
[OUTPUT] Saved rubric-annotated diagnosis predictions: C:\DL_PROJECT\research\raw\diagnosis_predictions.csv
[OUTPUT] Saved diagnosis summary metrics: C:\DL_PROJECT\research\raw\diagnosis_metrics.csv

[Step 4/5] Running Experiment C (Safety & Verification Audit)...
===========================================================================
AEGISOPS: RUNNING SAFETY, AUTHORIZATION & RECOVERY AUDIT
Testing ACTUAL application verification & recovery functions
===========================================================================
[INIT] Local disposable FastAPI service running at http://127.0.0.1:8765
[PASS] TC-POS-01 (POSITIVE_CONTROL): Full end-to-end approval, execution, and health restoration -> Success: True, Health: normal
[PASS] TC-ATT-01 (ATTACK_CASE): Consume non-existent ticket ID -> Blocked: Approval ticket does not exist.
[PASS] TC-ATT-02 (ATTACK_CASE): Consume expired ticket -> Blocked: Approval ticket expired; request a new approval.
[PASS] TC-ATT-03 (ATTACK_CASE): Approve with invalid confirmation phrase -> Blocked: Exact confirmation phrase did not match.
[PASS] TC-ATT-04 (ATTACK_CASE): Consume with modified action ID -> Blocked: Approval scope mismatch; no action was authorized.
[PASS] TC-ATT-05 (ATTACK_CASE): Consume with modified target URL -> Blocked: Approval scope mismatch; no action was authorized.
[PASS] TC-ATT-06 (ATTACK_CASE): Consume with modified incident ID -> Blocked: Approval scope mismatch; no action was authorized.
[PASS] TC-ATT-07 (ATTACK_CASE): Replay consumed approval ticket -> Blocked: Ticket is consumed; a fresh approved ticket is required.
[PASS] TC-ATT-08 (ATTACK_CASE): Consume explicitly rejected ticket -> Blocked: Ticket is rejected; a fresh approved ticket is required.
[PASS] TC-ATT-09 (ATTACK_CASE): Execute recovery on remote HTTPS endpoint -> Blocked: Remediation and fault injection are restricted to HTTP on localhost.
[PASS] TC-ATT-10 (ATTACK_CASE): Register remote plaintext HTTP target -> Blocked: Remote monitoring targets must use HTTPS; HTTP is allowed only on localhost.
[PASS] TC-ATT-11 (ATTACK_CASE): Register target with embedded credentials -> Blocked: Do not embed credentials in a URL; configure AEGISOPS_BEARER_TOKEN instead.
[PASS] TC-FAIL-01 (ATTACK_CASE): Execute recovery on unreachable local port -> Aborted safely: The local test service is unreachable. No recovery attempted.
[PASS] TC-FAIL-02 (ATTACK_CASE): Execute recovery when no fault is active -> Aborted safely: No injected demo fault is active. No recovery attempted.
[PASS] TC-VERIF-01 (ATTACK_CASE): Service remains unhealthy after attempted recovery -> action_result['success']=False, msg=Reset was requested, but verification failed.
[PASS] TC-AUDIT-01 (POSITIVE_CONTROL): Independent SQLite audit record verification and schema compliance -> Verified: req=True, grant=True, cons=True, rem=True
[TEARDOWN] Local test service halted successfully.
[OUTPUT] Saved per-case safety test results: C:\DL_PROJECT\research\raw\safety_test_results.csv
[OUTPUT] Saved safety metrics: C:\DL_PROJECT\research\raw\safety_metrics.csv
[OUTPUT] Saved comprehensive safety evaluation report: C:\DL_PROJECT\research\SAFETY_EVALUATION.md

[Step 5/5] Generating Statistical Analysis & Checksum Manifest...
Saved formal statistical analysis: c:\DL_PROJECT\research\results\statistical_analysis.md

Generating SHA-256 Artifact & Model Manifest...
Saved manifest: C:\DL_PROJECT\research\MANIFEST_SHA256.json

================================================================================
ALL EXPERIMENTS AND AUDITS COMPLETED SUCCESSFULLY IN 53.6 SECONDS
================================================================================
```

- **Exit Code**: `0`
- **Total Duration**: `53.6 seconds`
- **Stderr Output**: `None` (zero warnings or runtime errors)

---

## 2. Six-Dimension Verification Matrix

We audited the six explicit operational requirements defined in the reconciliation gate:

| Requirement Dimension | Verified Status | Mechanism / Evidence | Caveat / Gap Identified |
| :--- | :---: | :--- | :--- |
| **1. Runs the tests** | **YES** | Step 1 executes `pytest -q`, running all 42 unit & integration tests (`42 passed in 17.11s`). | Must be run with `.venv\Scripts\python.exe`. Global Python fails on `test_live_monitoring.py` due to missing `streamlit`. |
| **2. Executes intended experiments** | **PARTIAL** | Step 2 runs Experiment A (`run_experiment_a()`). Step 4 runs Experiment C (`run_safety_audit.py`). | Step 3 runs `generate_diagnosis_audit.py` (offline rubric evaluation of prior predictions). It **does not** invoke `run_experiment_b()` (live LLM API benchmark). |
| **3. Produces expected raw outputs** | **PARTIAL** | Generates `results/detection_predictions.csv`, `raw/diagnosis_predictions.csv`, and `raw/safety_test_results.csv`. | `run_experiment_a.py` writes its raw predictions to `research/results/` rather than `research/raw/`. `research/raw/detection_predictions.csv` is not touched. |
| **4. Regenerates metrics, figures, reports** | **PARTIAL** | Metrics CSVs and `results/statistical_analysis.md` are dynamically regenerated from predictions. | **Figures are NOT regenerated**. `detection_confusion_matrices.png` and `detection_comparison.png` are static pre-rendered PNGs with no generator in `run_all.py`. |
| **5. Regenerates SHA-256 manifest** | **YES** | Step 5 creates `research/MANIFEST_SHA256.json` containing fresh hashes for all 22 tracked artifacts. | **Manifest generation does NOT prove fresh experiment execution**; it hashes whatever files are on disk. |
| **6. Returns nonzero exit status on failure** | **YES** | Step 1 returns `res.returncode` if tests fail. Steps 3, 4, 5 use `subprocess.run(..., check=True)`, raising `CalledProcessError` on failure. | Verified in regression tests (`test_statistical_audit.py`). |

---

## 3. Detailed Audit of Pipeline Steps & Discrepancies

### Step 1: Pytest Regression Suite
- Executes `subprocess.run([sys.executable, "-m", "pytest", "-q"])`.
- Passes 42 of 42 tests across 8 test suites (`test_approval.py`, `test_agents.py`, `test_anomaly_detector.py`, `test_live_monitoring.py`, `test_target_security.py`, `test_workflow.py`, `test_statistical_audit.py`, `test_simulator.py`).
- **Environmental Dependency**: If executed in a global Python shell where `streamlit` is not installed, `live_monitoring.py:12` raises `ModuleNotFoundError`. The pipeline runner must enforce virtual environment execution (`.venv`).

### Step 2: Experiment A (Anomaly Detection)
- Evaluates 200 normal windows + 120 fault episodes across 6 scenarios.
- **Path Asymmetry**: `run_experiment_a()` writes to `ROOT / "research" / "results" / "detection_predictions.csv"`. However, `generate_manifest()` in line 37 tracks `ROOT / "research" / "raw" / "detection_predictions.csv"`.  
  Consequently, running `run_all.py` updates the `results/` copy, but the `raw/` copy remains static.

### Step 3: Experiment B (Diagnosis Rubric Audit)
- In `run_all.py` line 14, `from research.experiments.run_experiment_b import run_experiment_b` is imported.
- However, in line 90, `run_all.py` executes `subprocess.run([sys.executable, str(ROOT / "research" / "experiments" / "generate_diagnosis_audit.py")], check=True)`.
- It does **not** call `run_experiment_b()`.
- **Engineering Rationale**: Re-running live Groq LLM API calls would incur network latency ($> 2$ minutes), token rate limits (HTTP 429), and non-deterministic cloud responses. `generate_diagnosis_audit.py` provides deterministic, zero-cost, rubric-based evaluation of recorded model responses.
- **Audit Finding**: In the paper, authors must not claim that `run_all.py` makes live cloud LLM API calls on every invocation.

### Step 4: Experiment C (Safety & Verification Audit)
- Invokes `research/experiments/run_safety_audit.py`.
- Launches a temporary, disposable FastAPI service on `127.0.0.1:8765`.
- Executes all 16 test cases directly against `approval.ApprovalStore`, `live_monitoring._resolve_local_test_fault`, and `storage.telemetry_store.TelemetryStore`.
- Unlinks temporary test databases (`safety_test_store.sqlite3` and `safety_telemetry.sqlite3`) during teardown.
- **Safety Containment**: Strictly bounded to IPv4 loopback. Zero requests dispatched to external IP addresses or domains. The historical database `aegisops_live.sqlite3` is preserved in a read-only state.

### Step 5: Statistical Analysis & Manifest
- Invokes `research/results/generate_statistical_analysis.py`, generating `research/results/statistical_analysis.md`.
- Invokes `generate_manifest()`, producing `research/MANIFEST_SHA256.json` (22 tracked artifacts).

---

## 4. SHA-256 Checksum Manifest of Generated Artifacts

Below are the verified SHA-256 hashes generated by `research/run_all.py`:

| Tracked Artifact File | Relative Path | File Size (Bytes) | SHA-256 Checksum | Regenerated by Pipeline? |
| :--- | :--- | :---: | :--- | :---: |
| `lstm_autoencoder.pt` | `models/lstm_autoencoder.pt` | 19,893 | `df867ce96bf423f03b87441fc9a957270d4944fa734b41a546da9b57564619d0` | No (Frozen Checkpoint) |
| `lstm_autoencoder.json` | `models/lstm_autoencoder.json` | 338 | `e05bbf510b666a2a5ea79c6bb2a9d201083411db1eec780e9a56c4d874558e80` | No (Frozen Hyperparameters) |
| `aegisops_live.sqlite3` | `data/aegisops_live.sqlite3` | 86,016 | `b8f33f63116ca4d081b8544f128e4e941ce0ce6fef39ff4f7e2c918ee0e94ff1` | No (Preserved Database) |
| `incidents.json` | `data/incidents.json` | 5,686 | `b8b54332e6fc9c3a3b0ee461a52fc0d172e9d291916327421e4ae62b608ad2ec` | No (Ground Truth Dataset) |
| `detection_predictions.csv` | `research/results/detection_predictions.csv` | 24,357 | `246e14f8b84b8b89cbfce180fd7722ae82820f516894aa5dd11462866d10cfbb` | **Yes** (Experiment A) |
| `detection_metrics.csv` | `research/results/detection_metrics.csv` | 568 | `ed5775303f74156d844dc0068db4328e2237fc935a2bca260d613571083de57e` | **Yes** (Experiment A) |
| `detection_by_scenario.csv` | `research/results/detection_by_scenario.csv` | 280 | `7bc8400653683465f8f25af7d60398ae892831b4b3038ac5b7933478103bebf9` | **Yes** (Experiment A) |
| `diagnosis_predictions.csv` | `research/raw/diagnosis_predictions.csv` | 11,891 | `7719bdc39f1bf5d3443f486ec66e2319a02a5f9c13ac3dc2eb61c6fad99d8860` | **Yes** (Rubric Audit) |
| `diagnosis_metrics.csv` | `research/raw/diagnosis_metrics.csv` | 868 | `c3633e23d7a2fc9efeb093394a9bbd84b40578eab9a15c48c713fbf4fb38f403` | **Yes** (Rubric Audit) |
| `safety_test_results.csv` | `research/raw/safety_test_results.csv` | 3,008 | `589353e42a422134f11611bea301703bf3afd3c325c74f152e3967d0e2272045` | **Yes** (Experiment C) |
| `safety_metrics.csv` | `research/raw/safety_metrics.csv` | 997 | `65f1a9761d927289dad4d307d50bddc5c178911da38684abc3e43cb3421d3edd` | **Yes** (Experiment C) |
| `statistical_analysis.md` | `research/results/statistical_analysis.md` | 6,792 | `a90da57ef367baea964dfb4c2b9a1ba19b12fe963d722bfcbfe78ae321ef7d5f` | **Yes** (Step 5) |
| `detection_confusion_matrices.png` | `research/figures/detection_confusion_matrices.png` | 27,954 | `8a5bb86f671c6ca6b3da27a69b764c919702206085a6aee4fec401a87754f7a2` | **No** (Static Binary Figure) |
| `detection_comparison.png` | `research/figures/detection_comparison.png` | 16,879 | `96173a11da4f6f890c29ae06fb2ea675cf311e9f168f18073b64c052825bc5fc` | **No** (Static Binary Figure) |

---

## 5. Critical Reproducibility Verdict

The AegisOps reproducibility pipeline (`research/run_all.py`) is **FUNCTIONAL AND SAFE**, successfully orchestrating unit testing, anomaly detection benchmarking, rubric evaluation, live loopback safety verification, statistical analysis, and SHA-256 manifest generation.

However, three specific limitations must be explicitly recorded for manuscript reproducibility:
1. **Virtual Environment Prerequisite**: The pipeline requires execution via `.venv\Scripts\python.exe` to resolve Streamlit and FastAPI dependencies.
2. **Offline vs. Live Diagnosis Execution**: The automated pipeline reproduces rubric evaluation of recorded model responses, not interactive live cloud LLM API calls.
3. **Static Figure Assets**: Figures 1 and 2 in `research/figures/` are static assets rather than dynamically generated script outputs.
