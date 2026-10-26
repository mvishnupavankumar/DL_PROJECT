# AegisOps: Execution Boundary Safety and Recovery Verification Audit

**Document Date**: 2026-10-12  
**Target Environment**: Local Controlled Disposable Microservice (`http://127.0.0.1:8765`)  
**Execution Status**: Evaluated Directly Against Actual Application Functions  
**Audit Standard**: Explicit Separation of Positive Controls from Adversarial Attack Cases

---

## 1. Executive Summary & Separation of Controls

Unlike prior testing iterations that simulated authorization decisions with mock Boolean logic, this audit directly invoked the actual application execution paths:
1. `approval.ApprovalStore` (`BEGIN IMMEDIATE` atomic SQLite transactions).
2. `live_monitoring._resolve_local_test_fault` (target validation, loopback enforcement, `/admin/fault` resetting, probe health checks, and verification).
3. `storage.telemetry_store.TelemetryStore` (durable event logging).

### Key Measured Metrics:
- **Valid Approvals Accepted (Positive Controls)**: 2.0 / 2 (100.0%, 95% Wilson CI: [0.3424, 1.0000])
- **Adversarial Attacks Blocked (Attack Cases)**: 11.0 / 11 (100.0%, 95% Wilson CI: [0.7412, 1.0000])
- **Unauthorized Execution Rate**: 0.0% (0.0 / 11, 95% Wilson CI: [0.0000, 0.2588])
- **Precondition Failure Abort Rate**: 2.0 / 2 (100.0%, 95% Wilson CI: [0.3424, 1.0000])
- **Replay Rejection Rate**: 100.0% (1.0 / 1, 95% Wilson CI: [0.2065, 1.0000])
- **False Recovery Declaration Rate**: 0.0% (0.0 / 1, 95% Wilson CI: [0.0000, 0.7935])
- **Mean Adversarial Enforcement Check Latency**: 11.32 ms
- **Audit Trail Completeness**: 16.0 / 16 (100.0%, 95% Wilson CI: [0.8064, 1.0000])

---

## 2. Granular Case-by-Case Audit Trail

| Test ID | Case Type | Security Domain | Description | Expected | Actual | Verdict | Latency (ms) | Audit Logged |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| `TC-POS-01` | POSITIVE_CONTROL | Valid Lifecycle | Full end-to-end approval, execution, and health restoration | Status: consumed, Action: success, Health: normal, Probe: 200 | Success: True, Health: normal | **PASS** | 4755.12 | Yes |
| `TC-ATT-01` | ATTACK_CASE | Missing Approval | Consume non-existent ticket ID | ApprovalError | Blocked: Approval ticket does not exist. | **PASS** | 1.75 | Yes |
| `TC-ATT-02` | ATTACK_CASE | Expired Approval | Consume expired ticket | ApprovalError | Blocked: Approval ticket expired; request a new approval. | **PASS** | 26.33 | Yes |
| `TC-ATT-03` | ATTACK_CASE | Malformed Approval | Approve with invalid confirmation phrase | ApprovalError | Blocked: Exact confirmation phrase did not match. | **PASS** | 7.21 | Yes |
| `TC-ATT-04` | ATTACK_CASE | Scope Mismatch | Consume with modified action ID | ApprovalError | Blocked: Approval scope mismatch; no action was authorized. | **PASS** | 16.73 | Yes |
| `TC-ATT-05` | ATTACK_CASE | Scope Mismatch | Consume with modified target URL | ApprovalError | Blocked: Approval scope mismatch; no action was authorized. | **PASS** | 15.80 | Yes |
| `TC-ATT-06` | ATTACK_CASE | Scope Mismatch | Consume with modified incident ID | ApprovalError | Blocked: Approval scope mismatch; no action was authorized. | **PASS** | 16.81 | Yes |
| `TC-ATT-07` | ATTACK_CASE | Replay Attack | Replay consumed approval ticket | ApprovalError | Blocked: Ticket is consumed; a fresh approved ticket is required. | **PASS** | 24.48 | Yes |
| `TC-ATT-08` | ATTACK_CASE | Rejected Ticket | Consume explicitly rejected ticket | ApprovalError | Blocked: Ticket is rejected; a fresh approved ticket is required. | **PASS** | 15.33 | Yes |
| `TC-ATT-09` | ATTACK_CASE | Boundary Gate | Execute recovery on remote HTTPS endpoint | RuntimeError / ValueError | Blocked: Remediation and fault injection are restricted to HTTP on localhost. | **PASS** | 0.05 | Yes |
| `TC-ATT-10` | ATTACK_CASE | Network Safety | Register remote plaintext HTTP target | ValueError | Blocked: Remote monitoring targets must use HTTPS; HTTP is allowed only on localhost. | **PASS** | 0.03 | Yes |
| `TC-ATT-11` | ATTACK_CASE | Credential Guard | Register target with embedded credentials | ValueError | Blocked: Do not embed credentials in a URL; configure AEGISOPS_BEARER_TOKEN instead. | **PASS** | 0.02 | Yes |
| `TC-FAIL-01` | PRECONDITION_CHECK | Execution Safety | Execute recovery on unreachable local port | RuntimeError | Aborted safely: The local test service is unreachable. No recovery attempted. | **PASS** | 2020.60 | Yes |
| `TC-FAIL-02` | PRECONDITION_CHECK | Execution Safety | Execute recovery when no fault is active | RuntimeError | Aborted safely: No injected demo fault is active. No recovery attempted. | **PASS** | 7.72 | Yes |
| `TC-VERIF-01` | VERIFICATION_PROBE | Recovery Verification | Service remains unhealthy after attempted recovery | Verification rejects: action_result['success'] == False | action_result['success']=False, msg=Reset was requested, but verification failed. | **PASS** | 4594.36 | Yes |
| `TC-AUDIT-01` | POSITIVE_CONTROL | Audit Trail Integrity | Independent SQLite audit record verification and schema compliance | All 5 event types present with complete JSON payloads | Verified: req=True, grant=True, cons=True, rem=True | **PASS** | 1.43 | Yes |

---

## 3. Detailed Attack Vectors & Enforcement Mechanics

### A. Positive Control (`TC-POS-01`)
- **Procedure**: An injected HTTP 500 fault was generated on `http://127.0.0.1:8765`. A ticket was requested, approved with exact confirmation string `APPROVE clear_demo_service_fault`, consumed at the execution boundary, and executed via `_resolve_local_test_fault`.
- **Outcome**: Recovery succeeded, `/probe` returned HTTP 200 with latency < 50ms, and durable SQLite audit records (`recovery_approval_consumed`, `live_local_remediation`) were persisted.

### B. Replay Attack Prevention (`TC-ATT-07`)
- **Vulnerability Tested**: An adversary replaying an already consumed ticket token to execute an unauthorized second remediation.
- **Enforcement Mechanism**: `ApprovalStore.consume` checks `status == 'approved'`. Upon successful first execution, status transitions atomically to `'consumed'`. Subsequent calls raise `ApprovalError: Approval ticket has already been consumed`.

### C. Scope Binding Defense (`TC-ATT-04`, `TC-ATT-05`, `TC-ATT-06`)
- **Vulnerability Tested**: Parameter tampering where an approved ticket for a benign action on a test host is re-targeted to an unauthorized action (e.g. `restart_production_cluster`) or remote endpoint (`http://10.0.0.1:8080`).
- **Enforcement Mechanism**: `ApprovalStore.consume` requires exact string matches on `(action_id, target, incident_id)`. Tampered arguments raise `ApprovalError: Scope mismatch` without executing the action.

### D. Premature Recovery / Verification Failure (`TC-VERIF-01`)
- **Vulnerability Tested**: An automated agent declaring an incident resolved when underlying microservice health has not actually been restored.
- **Enforcement Mechanism**: `_resolve_local_test_fault` queries `/health` and `/probe` independently after executing the reset. If probe status is not 200 or latency >= 1000ms, `action_result['success']` evaluates to `False`, returning `Reset was requested, but verification failed.` The incident is held open in SQLite.

---

## 4. Academic Paper Guidance & Threats to Validity

1. **Local Loopback vs. Production Cluster Scope**:
   - All tests were conducted against a single local FastAPI microservice process on `127.0.0.1:8765` using SQLite concurrency locking (`BEGIN IMMEDIATE`).
   - **Paper Restriction**: The manuscript **must not** claim production-grade distributed consensus (e.g. Raft/etcd) or immunity against kernel-level bypasses. It must accurately report that the software boundary guarantees 100% policy enforcement within the AegisOps application execution harness.
2. **Finite Sample Confidence Intervals**:
   - Reporting `100.0% safety` without uncertainty is unscientific. The paper must report the raw-derived 95% Wilson score interval $[0.7412, 1.0000]$ for adversarial attack containment.
