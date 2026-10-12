# 05 — Safety Evidence Reconciliation

**Audit Date**: 2026-10-12  
**Auditor**: Senior ML Systems & Security Auditor  
**Primary Source**: [`research/raw/safety_test_results.csv`](file:///c:/DL_PROJECT/research/raw/safety_test_results.csv) ($N = 16$ test cases)  
**Metrics Source**: [`research/raw/safety_metrics.csv`](file:///c:/DL_PROJECT/research/raw/safety_metrics.csv)  
**Evaluation Script**: [`research/experiments/run_safety_audit.py`](file:///c:/DL_PROJECT/research/experiments/run_safety_audit.py)  
**Security Implementations**: [`approval.py`](file:///c:/DL_PROJECT/approval.py), [`live_monitoring.py`](file:///c:/DL_PROJECT/live_monitoring.py), [`collectors/system_metrics.py`](file:///c:/DL_PROJECT/collectors/system_metrics.py)

---

## 1. Resolution of the Conflicting Case Totals (14 vs. 15 vs. 16 Cases)

### The Discrepancy Identified
Across different project documents:
- Some reports cite **15 scenarios** (referencing an earlier draft that omitted `TC-AUDIT-01`).
- The previous summary metric reported **14/14 blocked attacks** (subtracting 2 positive controls from 16 cases).
- The raw results file [`research/raw/safety_test_results.csv`](file:///c:/DL_PROJECT/research/raw/safety_test_results.csv) records exactly **16 test cases**.

### The Reconciled 16-Case Taxonomy
The 16 cases represent four distinct, non-overlapping engineering categories:
1. **Adversarial Security Penetration Attacks ($N = 11$)**: Malicious attempts to bypass authorization, replay tokens, alter operational scope, or exfiltrate credentials.
2. **Execution Precondition Safety Checks ($N = 2$)**: Safeguards preventing destructive execution when target services are unreachable or un-faulted.
3. **Recovery Verification Integrity Checks ($N = 1$)**: Prevention of premature incident closure when probe health checks continue to fail.
4. **Positive Lifecycle Controls ($N = 2$)**: Legitimate execution and SQLite audit trail validation.
$$\mathbf{11 \text{ Attacks}} + \mathbf{2 \text{ Preconditions}} + \mathbf{1 \text{ Verification}} + \mathbf{2 \text{ Controls}} = \mathbf{16 \text{ Total Cases}}$$

---

## 2. Granular Evaluation Census by Security Category

| Security Domain / Category | Test ID | Description | Expected Behavior | Observed Behavior | Numerator / Denominator | Compliance Rate | 95% Wilson Score CI |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **A. Adversarial Attacks** | `TC-ATT-01` | Missing ticket UUID | `ApprovalError: Does not exist` | Blocked at lookup | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| | `TC-ATT-02` | Expired ticket (TTL $>30$s) | `ApprovalError: Ticket expired` | Blocked at timestamp check | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| | `TC-ATT-03` | Malformed confirmation phrase | `ApprovalError: Phrase mismatch` | Blocked; status `requested` | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| | `TC-ATT-04` | Scope tampering: `action_id` | `ApprovalError: Scope mismatch` | Blocked; zero action executed | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| | `TC-ATT-05` | Scope tampering: `target` URL | `ApprovalError: Scope mismatch` | Blocked; zero action executed | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| | `TC-ATT-06` | Scope tampering: `incident_id` | `ApprovalError: Scope mismatch` | Blocked; zero action executed | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| | `TC-ATT-07` | Replay attack on consumed ticket | `ApprovalError: Already consumed` | Blocked at state check | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| | `TC-ATT-08` | Consume rejected ticket | `ApprovalError: Ticket rejected` | Blocked at status check | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| | `TC-ATT-09` | Remote HTTPS remediation | `RuntimeError: Localhost only` | Blocked by `_is_loopback_target` | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| | `TC-ATT-10` | Remote plaintext HTTP target | `ValueError: HTTPS required` | Blocked by URL validator | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| | `TC-ATT-11` | Embedded URL credentials | `ValueError: Credentials forbidden` | Blocked by URL parser | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| *Subtotal: Attacks Blocked* | | | | | **11 / 11** | **100.0%** | **$[0.7412, 1.0000]$** |
| **B. Precondition Safety** | `TC-FAIL-01` | Service offline / port closed | `RuntimeError: Unreachable` | Aborted safely; no reset | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| | `TC-FAIL-02` | Remediation with no active fault | `RuntimeError: No fault active` | Aborted safely; no reset | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| *Subtotal: Preconditions Safe* | | | | | **2 / 2** | **100.0%** | **$[0.3424, 1.0000]$** |
| **C. Verification Integrity** | `TC-VERIF-01` | Probe fails post-reset | `action_result.success == False` | Prevented false recovery | **1 / 1** | **100.0%** | **$[0.2065, 1.0000]$** |
| **D. Positive Controls** | `TC-POS-01` | Valid lifecycle execution | Status `consumed`, HTTP 200 restored | `success=True`, health normal | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| | `TC-AUDIT-01` | Durable SQLite audit logging | All 5 event types in SQLite | Schema & payload verified | $1/1$ | 100.0% | $[0.2065, 1.0000]$ |
| *Subtotal: Controls Passed* | | | | | **2 / 2** | **100.0%** | **$[0.3424, 1.0000]$** |
| **Total Inventory** | | | | | **16 / 16** | **100.0%** | **$[0.8064, 1.0000]$** |

---

## 3. Recomputed Security & Reliability Metrics

| Security Metric | Numerator | Denominator | Recomputed Rate | 95% Wilson Score Interval | Scientific Interpretation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Adversarial Attack Containment** | 11 | 11 | **100.0%** | $[0.7412, 1.0000]$ | 11 of 11 malicious attempts blocked at boundary. |
| **Unauthorized Action Execution Rate** | 0 | 11 | **0.0%** | $[0.0000, 0.2588]$ | Zero unauthorized actions executed. |
| **Replay Attack Rejection Rate** | 1 | 1 | **100.0%** | $[0.2065, 1.0000]$ | Single replay attempt rejected atomically. |
| **Precondition Abort Rate** | 2 | 2 | **100.0%** | $[0.3424, 1.0000]$ | Zero destructive side-effects on dead services. |
| **False Recovery Declaration Rate** | 0 | 1 | **0.0%** | $[0.0000, 0.7935]$ | Failed reset correctly prevented incident closure. |
| **Audit Trail Completeness** | 16 | 16 | **100.0%** | $[0.8064, 1.0000]$ | All trials produced durable SQLite records. |
| **Mean Check Latency** | — | — | **419.93 ms** | N/A | Includes HTTP probe verification roundtrips. |

---

## 4. Architectural Verification: Application Functions & Test Isolation

1. **Target Application Functions Exercised**:
   - `approval.ApprovalStore`: Atomic transactions via `BEGIN IMMEDIATE` (`approval.py:73`).
   - `live_monitoring._resolve_local_test_fault`: Reset endpoint `/admin/fault` and probe health checks.
   - `collectors.system_metrics.validate_local_service_url`: Loopback address validation.
   - `storage.telemetry_store.TelemetryStore`: Append-only event logging.
2. **Strict Test Isolation**:
   - Ran against disposable loopback service on `http://127.0.0.1:8765`.
   - Used disposable SQLite databases (`data/safety_test_store.sqlite3` and `data/safety_telemetry.sqlite3`).
   - The production database `data/aegisops_live.sqlite3` was 100% untouched.
3. **Caveat on Architectural Scope**:
   These safety guarantees apply within the AegisOps application execution harness on the local loopback interface. They do not demonstrate distributed consensus or protection against kernel-level bypasses.
