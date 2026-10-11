# Security model and deployment boundary

AegisOps is a research prototype with production-oriented hardening, **not a certified production-ready product**. Deploy it first in staging with read-only access.

## Monitoring targets
- Remote targets must use HTTPS. TLS verification is enabled by default.
- Do not put credentials in URLs. `AEGISOPS_BEARER_TOKEN` adds a bearer token to monitoring GET requests.
- Monitoring access does not grant remediation access.
- The collector's CPU/memory/disk readings describe the collector host. Remote host metrics require a separate authenticated agent/exporter.
- Restrict egress to approved target hosts at the network layer. URL validation alone is not a complete SSRF defense.

## Remediation
- Fault injection and the only executable remediation remain limited to the local AegisOps test service.
- Never expose the local test service's `/admin/fault` endpoint to a LAN or the internet.
- Do not add arbitrary shell commands or unrestricted LLM-selected actions.
- Production remediation must use a separate policy-enforced executor, fixed runbooks, least-privilege identities, explicit approval, idempotency, rate limits, and rollback plans. This repository does not implement a production remediation executor.

## Secrets and data
- Keep `.env` out of version control and shared archives.
- Rotate any credential that was ever committed or shared.
- Restrict access to SQLite files and exported CSVs; telemetry can reveal operational details.
- Define retention, backup, encryption-at-rest, and incident-response procedures before production use.

## Before a production pilot
Complete the controls in `OPERATIONS.md`, run security review and dependency scanning, and validate recovery in a non-production environment.


## Recovery approval workflow added in the hardening pass

Recovery approval tickets are stored in SQLite and are time-limited, bound to one action/target/incident, and consumed atomically before execution. The UI requires a typed confirmation phrase. Expired, mismatched, replayed, or missing tickets are rejected. Approval actor labels are not authenticated identities; no user login or RBAC is currently implemented. Consequently, this is defense-in-depth for a local evaluation, not sufficient authorization for a production operations console.
