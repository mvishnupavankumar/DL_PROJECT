# 04 — Diagnosis Reconciliation

**Audit Date**: 2026-10-12  
**Auditor**: Senior ML Experiment Auditor & NLP Evaluation Specialist  
**Ground-Truth Catalog**: [`data/incidents.json`](file:///c:/DL_PROJECT/data/incidents.json) ($N = 6$ scenarios)  
**Prediction Datasets**: [`research/raw/diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_predictions.csv), [`research/backup_prior_outputs/results/diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/backup_prior_outputs/results/diagnosis_predictions.csv)  
**Evaluator**: [`research/experiments/generate_diagnosis_audit.py`](file:///c:/DL_PROJECT/research/experiments/generate_diagnosis_audit.py)  
**Agent Subsystem**: [`agents.py`](file:///c:/DL_PROJECT/agents.py)

---

## 1. Ground-Truth Incident Catalog ($N = 6$)

All diagnostic benchmarking in AegisOps is evaluated against six ground-truth architectural incident scenarios:

| Incident ID | Subsystem Domain | Description | Canonical Ground-Truth Root Cause |
| :--- | :--- | :--- | :--- |
| **INC-1001** | `API` | Customer payment requests fail with HTTP 500 | Database connection pool exhaustion |
| **INC-1002** | `DATABASE` | Applications cannot connect to customer database | Database service stopped |
| **INC-1003** | `SERVER` | CPU utilization above 95% for $>10$ minutes | Worker service thread exhaustion causing sustained CPU saturation |
| **INC-1004** | `STORAGE` | Server reports low disk capacity, write failures | Runaway application log growth consumed disk capacity |
| **INC-1005** | `AUTHENTICATION` | Valid users receive authentication errors | Incorrect OAuth issuer configuration |
| **INC-1006** | `NETWORK` | Service A times out calling Service B | Broken service route between service-a and service-b |

---

## 2. Reconciled Seven-Configuration Diagnostic Matrix

Every configuration was audited for intended cohort size ($N = 6$), completed API evaluations, omitted/rate-limited cases, and explicit 4-tier rubric scoring (Correct, Partially Correct, Incorrect, Unassessable):

| Configuration | Execution Mechanism | DL Signals? | Intended Cases | Completed Cases | Omitted / Dropped | Incident IDs Evaluated | Strict Correct | Partial Correct | Incorrect | Unassessable | Full-Cohort Strict Acc ($N=6$) | Per-Protocol Strict Acc | Lenient Acc ($N=6$) | Mean Latency (ms) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Rule Baseline** | Deterministic Heuristic | No | 6 | 6 | 0 | INC-1001 to INC-1006 | 6 | 0 | 0 | 0 | **100.0%** ($6/6$) | **100.0%** ($6/6$) | 100.0% | 0.01 |
| **2. Single-Agent Offline** | Deterministic Fallback | Yes | 6 | 6 | 0 | INC-1001 to INC-1006 | 3 | 0 | 3 | 0 | **50.0%** ($3/6$) | **50.0%** ($3/6$) | 50.0% | 0.03 |
| **3. Multi-Agent Full Offline** | Deterministic Fallback | Yes | 6 | 6 | 0 | INC-1001 to INC-1006 | 3 | 0 | 3 | 0 | **50.0%** ($3/6$) | **50.0%** ($3/6$) | 50.0% | 0.57 |
| **4. Multi-Agent No-DL Offline** | Deterministic Fallback | No | 6 | 6 | 0 | INC-1001 to INC-1006 | 6 | 0 | 0 | 0 | **100.0%** ($6/6$) | **100.0%** ($6/6$) | 100.0% | 0.11 |
| **5. Single-Agent Live LLM** | Groq Cloud LLM | Yes | 6 | 5 | 1 | INC-1001, 1003–1006 (dropped 1002) | 4 | 0 | 1 | 1 | **66.7%** ($4/6$) | **80.0%** ($4/5$) | 66.7% | 2,534.89 |
| **6. Multi-Agent Full Live LLM** | Groq Cloud LLM | Yes | 6 | 6 | 0 | INC-1001 to INC-1006 | 5 | 1 | 0 | 0 | **83.3%** ($5/6$) | **83.3%** ($5/6$) | **100.0%** | 23,188.72 |
| **7. Multi-Agent No-DL Live LLM** | Groq Cloud LLM | No | 6 | 5 | 1 | INC-1001–1003, 1005–1006 (dropped 1004) | 4 | 1 | 0 | 1 | **66.7%** ($4/6$) | **80.0%** ($4/5$) | 83.3% | 16,066.41 |

---

## 3. Audit of API Failures and Non-Equivalent Comparisons

### The Flawed Prior Claim
Earlier reporting ([`research/backup_prior_outputs/results/diagnosis_metrics.csv`](file:///c:/DL_PROJECT/research/backup_prior_outputs/results/diagnosis_metrics.csv)) reported:
- Config 7 (Multi-Agent No-DL): $\text{accuracy} = 1.0000$ ($5/5$)
- Config 6 (Multi-Agent Full with DL): $\text{accuracy} = 0.8333$ ($5/6$)
This suggested that omitting DL evidence improved agent accuracy.

### The Empirical Reality
1. **Config 7 dropped INC-1004**: The free-tier Groq API experienced an unhandled HTTP 429 rate limit during INC-1004. By dropping INC-1004, Config 7 was evaluated only on 5 cases.
2. **Config 5 dropped INC-1002**: Suffered an API timeout and JSON parsing abort, excluding INC-1002.
3. **Config 6 evaluated all 6 cases**: Scored 5 correct and 1 partially correct (INC-1002).
4. **Matched-Pair Intent-to-Treat Reality**:
   When evaluating the full intended cohort ($N = 6$), treating dropped cases as unassessable (0 score in strict ITT):
   - Multi-Agent Full (with DL): **83.3%** ($5/6$).
   - Multi-Agent No-DL (without DL): **66.7%** ($4/6$).
   The claim that omitting DL telemetry improved accuracy was an artifact of dropping difficult or rate-limited cases from the denominator.

---

## 4. Unsupported Diagnosis Claims & Hallucinations

Each diagnosis was audited against the ground-truth logs for unsupported or hallucinated claims:
- **INC-1002 in Multi-Agent Full (Live LLM)**:
  - Diagnosis: *"PostgreSQL service crashed due to abnormal disk I/O contention."*
  - Log Reality: The database service crashed, but disk I/O contention was absent from the logs.
  - Rubric Verdict: **PARTIALLY_CORRECT** (correct subsystem, hallucinated secondary cause).
- **INC-1004 in Multi-Agent No-DL (Live LLM)**:
  - Diagnosis: *"Application crashed due to memory exhaustion."*
  - Log Reality: The disk was full (`/var/log/app.log` 42GB); memory was normal.
  - Rubric Verdict: **INCORRECT** (attributed to wrong subsystem due to missing telemetry signals).

---

## 5. Offline vs. Live LLM Separation

- **Offline Mode**: Uses hardcoded regex keyword matching in `_local_root_cause(text)` ([`agents.py:20-37`](file:///c:/DL_PROJECT/agents.py#L20)). The drop from 100% to 50% when adding DL telemetry was caused by string rule ordering: strings like `"elevated response latency"` matched a generic rule before specific rules for CPU, Disk, and Network could execute.
- **Live LLM Mode**: Calls `openai/gpt-oss-20b` via Groq Cloud. Shows genuine reasoning where DL telemetry disambiguates subtle logs (e.g. distinguishing CPU thread exhaustion from disk log growth).

---

## 6. Power Analysis & Statistical Limitations

- Cohort size: $N = 6$.
- Statistical power: $1 - \beta \approx 0.14$.
- **Directive**: No claim of asymptotic statistical significance or generalized agent superiority may be made in the paper. Results must be presented strictly as descriptive point estimates and qualitative case studies.
