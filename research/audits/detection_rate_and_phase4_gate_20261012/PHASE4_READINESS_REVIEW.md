# AegisOps: Phase 4 Diagnosis Readiness and Rubric Evaluation Review

**Audit Gate**: Final Detection Rate Audit and Phase 4 Readiness Gate  
**Audit Date**: 2026-10-12  
**Audit Directory**: `research/audits/detection_rate_and_phase4_gate_20261012/`  
**Reference Files**:
- `data/incidents.json` (Ground-truth incident specifications)
- `research/raw/diagnosis_predictions.csv` ($N = 42$ evaluations)
- `research/raw/diagnosis_metrics.csv`
- `research/experiments/generate_diagnosis_audit.py`

---

## 1. Ground-Truth Incident Catalog and Reference Causes

The diagnosis benchmark evaluates $N = 6$ architectural failure scenarios defined in `data/incidents.json`:

| Incident ID | Incident Title | Category | Ground-Truth Root Cause | Reference Remediation |
| :--- | :--- | :---: | :--- | :--- |
| **INC-1001** | Payment API returning HTTP 500 | API | Database connection pool exhaustion | `restart_connection_pool` / `increase_connection_pool` |
| **INC-1002** | Customer database unavailable | DATABASE | Database service stopped | `restart_database_service` |
| **INC-1003** | Production server CPU at 98% | SERVER | Worker service thread exhaustion causing sustained CPU saturation | `restart_worker_service` / `scale_worker_instances` |
| **INC-1004** | Server disk space almost full | STORAGE | Runaway application log growth consumed disk capacity | `rotate_application_logs` |
| **INC-1005** | Users cannot log in | AUTHENTICATION | Incorrect OAuth issuer configuration | `restore_oauth_configuration` |
| **INC-1006** | Internal API timeout | NETWORK | Broken service route between service-a and service-b | `refresh_service_route` |

---

## 2. Configuration Execution Modes and Evidence Paths

Experiment B evaluates a $7 \times 6 = 42$ factorial matrix across seven configurations:

| Configuration | Execution Mode | Engine / Model | Deep Learning Evidence Supplied |
| :--- | :---: | :---: | :---: |
| **1. Rule-based Baseline** | Deterministic Offline | Regex / keyword pattern matching | False |
| **2. Single-Agent (Offline)** | Deterministic Offline | Local rule mock (`_local_root_cause`) | True |
| **3. Multi-Agent Full (Offline)** | Deterministic Offline | Mock multi-agent pipeline | True |
| **4. Multi-Agent No-DL (Offline)** | Deterministic Offline | Mock multi-agent pipeline (logs only) | False |
| **5. Single-Agent (Groq LLM)** | Live API Calls | Groq Cloud (`openai/gpt-oss-20b`) | True |
| **6. Multi-Agent Full (Groq LLM)** | Live API Calls | Groq Cloud (`openai/gpt-oss-20b`) | True |
| **7. Multi-Agent No-DL (Groq LLM)** | Live API Calls | Groq Cloud (`openai/gpt-oss-20b`) | False |

### Key Distinction: Offline Mocks vs. Live LLM Calls
- **Configurations 1, 2, 3, 4** execute entirely locally via deterministic Python functions in $< 1\text{ ms}$.
- **Configurations 5, 6, 7** execute against remote LLM endpoints via the Groq Cloud API, exhibiting mean inference latencies of $2.5\text{ s}$ to $23.2\text{ s}$.
- All 42 prediction records are fully preserved in `research/raw/diagnosis_predictions.csv` and `research/results/diagnosis_predictions.csv`.

---

## 3. Rubric Definitions and Scoring Breakdown

### 3.1 Rubric Grading Tiers
In `research/experiments/generate_diagnosis_audit.py`:
1. **CORRECT (Strict = 1, Lenient = 1)**: Correctly identifies the exact underlying causal mechanism matching ground truth.
2. **PARTIALLY_CORRECT (Strict = 0, Lenient = 1)**: Identifies the correct failing subsystem or symptom, but misidentifies the exact causal mechanism (e.g. diagnosing a database crash on INC-1002 but hallucinating disk contention as the secondary cause).
3. **INCORRECT (Strict = 0, Lenient = 0)**: Attributes the failure to the wrong subsystem, opposite cause, or irrelevant component.
4. **UNASSESSABLE (Strict = 0, Lenient = 0)**: Run aborted due to network timeout or HTTP 429 rate limit. (There are currently **0** unassessable cases in the recorded dataset).

### 3.2 Quantitative Performance Summary across Configurations

| Configuration | Completed Cases | Strict Correct | Partially Correct | Incorrect | Strict Accuracy | Lenient Accuracy | Mean Latency (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Rule-based Baseline** | 6 / 6 | 6 | 0 | 0 | **100.0%** (6/6) | 100.0% (6/6) | 0.01 ms |
| **2. Single-Agent (Offline)** | 6 / 6 | 3 | 0 | 3 | **50.0%** (3/6) | 50.0% (3/6) | 0.03 ms |
| **3. Multi-Agent Full (Offline)** | 6 / 6 | 3 | 0 | 3 | **50.0%** (3/6) | 50.0% (3/6) | 0.57 ms |
| **4. Multi-Agent No-DL (Offline)** | 6 / 6 | 6 | 0 | 0 | **100.0%** (6/6) | 100.0% (6/6) | 0.11 ms |
| **5. Single-Agent (Groq LLM)** | 6 / 6 | 4 | 0 | 2 | **66.67%** (4/6) | 66.67% (4/6) | 2,534.89 ms |
| **6. Multi-Agent Full (Groq LLM)** | 6 / 6 | 5 | 1 | 0 | **83.33%** (5/6) | **100.0%** (6/6) | 23,188.72 ms |
| **7. Multi-Agent No-DL (Groq LLM)** | 6 / 6 | 4 | 1 | 1 | **66.67%** (4/6) | 83.33% (5/6) | 16,066.41 ms |

---

## 4. Methodological Audit & Test-Set Leakage Findings

### 4.1 Test-Set Leakage in Rubric Evaluation
1. **Hardcoded Rubric Keywords**: Inspection of `generate_diagnosis_audit.py` lines 79–173 reveals that the rubric parser contains explicit `if inc_id == "INC-1001": ... elif inc_id == "INC-1002": ...` branches with keywords written specifically for these 6 scenarios.
2. **Zero Held-Out Evaluation Incidents**: The exact same 6 incidents used during prompt design and prototype testing were used to evaluate diagnostic accuracy. There is no independent held-out incident evaluation set.
3. **Statistical Power**: With $N = 6$ cases, a difference between 5/6 (83.3%) and 4/6 (66.7%) corresponds to a single incident flip and has statistical power of only $1 - \beta \approx 0.14$.

### 4.2 Offline Mock With-DL Anomaly
In offline evaluations, Multi-Agent Full (Offline) achieved only 50.0% accuracy, while Multi-Agent No-DL (Offline) achieved 100.0%. This occurred because the mock function `_local_root_cause` in `multi_agent.py` gave precedence to high reconstruction error / CPU rules over log parsing, causing INC-1004 (disk), INC-1005 (auth), and INC-1006 (route) to be misdiagnosed as worker thread saturation. This was an artifact of the local mock rule ordering, **not** a deficiency of the deep learning architecture.

---

## 5. Phase 4 Readiness Determination & Recommendation

### Readiness Assessment
- **Data Integrity**: All 42 evaluation records are preserved, verified, and accounted for without missing cases.
- **Reproducibility**: The evaluation script `generate_diagnosis_audit.py` executes in Step 3 of `research/run_all.py` without requiring live API credits or triggering rate limits.
- **Rerun Policy**: Live LLM calls do **not** need to be re-executed, as doing so introduces non-deterministic LLM variance and risks HTTP 429 quota exhaustion without adding scientific clarity.

### Final Recommendation: PROCEED TO PHASE 4 WITH EXPLICIT BOUNDS
**Recommendation**: **Proceed to close Phase 4 as a pilot feasibility study.**  
Do not claim broad diagnostic superiority in production. In the research manuscript and reports, Experiment B must be explicitly described as a 6-scenario pilot feasibility benchmark with acknowledged small-sample power limitations and rubric design leakage.
