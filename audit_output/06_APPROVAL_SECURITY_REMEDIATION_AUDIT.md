# AegisOps — Approval, Security, and Remediation Audit

**Audit Phase**: Phase 7  
**Auditor**: Senior Python Engineer / ML Researcher / SRE / Security Reviewer  
**Scope**: Authorization Hardening, Threat Modeling, Replay Resistance, Network Safety, and Remediation Boundaries

---

## 1. Security Architecture & Threat Model Overview

AegisOps is designed as a **local research evaluation prototype**. The codebase incorporates defensive controls around human-in-the-loop remediation to demonstrate structured authorization patterns before automated actions execute.

```text
[Operator Request]
       │
       ▼
ApprovalStore.request(action, target, incident, requester)
       │  Status: 'pending' · TTL: 300s
       ▼
ApprovalStore.approve(ticket_id, action, target, incident, approver, phrase)
       │  Requires: exact match 'APPROVE clear_demo_service_fault'
       │  Requires: non-expired timestamp & matching (action, target, incident)
       ▼  Status: 'approved'
ApprovalStore.consume(ticket_id, action, target, incident)
       │  SQLite BEGIN IMMEDIATE · Atomic UPDATE where status='approved'
       │  Status: 'consumed' (Replay impossible)
       ▼
_resolve_local_test_fault()
       │  Safety Gate 1: validate_local_service_url() [loopback HTTP only]
       │  Safety Gate 2: _is_loopback_target() [blocks remote targets]
       │  Action Execution: POST /admin/fault {'mode': 'normal'}
       │  Post-Action Verification: GET /health + GET /probe
       ▼
store.log_event("recovery_execution_finished")
```

---

## 2. Granular Evaluation of Security Properties

### Property 1: Authorization Enforcement
- **Implementation**: `approval.py:27` (`ApprovalStore`).
- **Verified Strengths**:
  - Requires ticket generation prior to approval.
  - Enforces exact confirmation phrase: `confirmation != f"APPROVE {action_id}"` (`approval.py:82`).
  - Enforces strict three-way scope matching: `(action_id, target, incident_id)` must match across `request()`, `approve()`, and `consume()` (`approval.py:100, 125`).
- **Defects & Vulnerabilities**:
  - **No Operator Identity Authentication (Severity: Medium for evaluation, Critical for production)**:
    - The Streamlit interface provides no user authentication, session tokens, or RBAC.
    - Anyone who can reach port 8501 can input arbitrary text into `approver_label` (e.g. `"lead_sre"`) and approve tickets.
    - As acknowledged in `approval.py:3`: *"This is a workflow guard, not an identity provider... approval actor strings are audit annotations only."*

### Property 2: Replay & Concurrency Prevention
- **Implementation**: `approval.py:109-134` (`ApprovalStore.consume`).
- **Verified Strengths**:
  - Uses `sqlite3.connect(..., isolation_level=None)` and begins explicit transactions with `BEGIN IMMEDIATE` (`approval.py:113`).
  - Executes atomic update:
    ```sql
    UPDATE recovery_approvals SET status='consumed', consumed_at=?
    WHERE ticket_id=? AND status='approved'
    ```
  - Inspects `cur.rowcount != 1` (`approval.py:130`). If a second concurrent thread or replayed request arrives, `rowcount == 0` and an `ApprovalError` is raised.
  - **Verified in Safe Concurrency Test**: `test_approval.py:132` (`test_concurrent_consumers_can_consume_ticket_only_once`) verifies with `Barrier(2)` that one thread succeeds and the second is rejected.

### Property 3: Scope & Target Network Security
- **Implementation**: `collectors/system_metrics.py:21-47` (`validate_local_service_url`, `validate_monitoring_target_url`).
- **Verified Strengths**:
  - **Target Validation**: Rejects plaintext HTTP for remote hosts; mandates HTTPS (`system_metrics.py:41`).
  - **Credential Stripping**: Rejects URLs containing embedded basic auth (`system_metrics.py:43`).
  - **Remediation Boundary**: Enforces loopback address validation:
    ```python
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("Remediation and fault injection are restricted to HTTP on localhost.")
    ```
  - **Unauthenticated Admin Endpoint Guard**: The FastAPI local test service (`demo_service/main.py`) exposes `/admin/fault` with no authentication. Binding strictly to `127.0.0.1` prevents LAN exposure.

### Property 4: Safe Remediation & Single-Action Allowlisting
- **Implementation**: `live_monitoring.py:511-517`.
- **Verified Strengths**:
  - Even though the multi-agent system produces arbitrary suggested actions, `_resolve_local_test_fault` strictly overwrites the action ID:
    ```python
    resolution = {
        **resolution,
        "action_id": "clear_demo_service_fault",
        "safety_scope": "localhost demo service only",
    }
    ```
  - The prototype does **NOT** execute arbitrary bash commands, restart systemd services, reboot VMs, or invoke cloud APIs. Remediation is strictly limited to clearing the in-memory fault flag on the local demo service.

### Property 5: Independent Recovery Verification
- **Implementation**: `live_monitoring.py:526-559`.
- **Verified Strengths**:
  - Remediation does **not** assume success merely because the POST request succeeded.
  - Executes independent health probe:
    1. Checks `/health` endpoint for `status == "ok"` and `fault_mode == "normal"`.
    2. Measures real HTTP probe to `/probe`: confirms status 200 and latency < 1000ms.
  - Feeds actual probe results into `VerificationAgent`.

### Property 6: Rollback and Escalation Behavior
- **Implementation**: **Not Implemented**.
- **Gap**: If remediation fails (e.g., target does not recover or probe times out), the approval ticket is already consumed (`status: 'consumed'`). The system logs `"recovery_execution_failed"` (`live_monitoring.py:1230`), but has no automated rollback, runbook fallback, or escalation pager trigger. The operator must manually re-investigate and request a new ticket.

---

## 3. Concrete Security Findings & Defect Register

### Finding SEC-01: Unauthenticated Dashboard Control Plane
- **Severity**: **Medium (High if deployed outside local dev machine)**
- **File**: `app.py`, `live_monitoring.py:1108`
- **Problem**: The Streamlit interface has zero authentication or session access controls. Anyone able to connect to port 8501 has full access to inject faults, view telemetry, approve recovery tickets, and clear faults.
- **Impact**: If bound to `0.0.0.0` or a shared network, unauthenticated third parties can approve recovery actions or trigger fault injection.
- **Remediation**: Keep bound strictly to `127.0.0.1`. In production, place behind an authenticated reverse proxy (OIDC/OAuth2/mTLS) and enforce role-based access control (RBAC).

### Finding SEC-02: Missing Atomicity Between Ticket Consumption and Action Execution
- **Severity**: **Low (Operational Reliability)**
- **File**: `live_monitoring.py:1178-1200`
- **Problem**: The approval ticket is consumed in SQLite *before* `_resolve_local_test_fault` executes. If network latency or a temporary process failure interrupts the execution between lines 1178 and 1195, the ticket remains consumed, and the operator must start a completely new approval workflow.
- **Impact**: Frustrates operators during transient network glitches; avoids replay at the cost of requiring full re-approval on network drops.
- **Remediation**: Acceptable design tradeoff for strict non-replay safety in a prototype, but in production, use a two-phase commit or reservation/execution state machine.

### Finding SEC-03: Plaintext Admin Endpoint on Local Test Service
- **Severity**: **Low (Safe by default via loopback)**
- **File**: `demo_service/main.py:71`
- **Problem**: `/admin/fault` accepts arbitrary fault injection without an API key or bearer token.
- **Impact**: Relies entirely on loopback binding (`127.0.0.1`) for security. If started with `--host 0.0.0.0`, any local network user can inject faults.
- **Remediation**: Add a shared secret token header (e.g. `X-AegisOps-Admin-Key`) to `/admin/fault` even on loopback.
