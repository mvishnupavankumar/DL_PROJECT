# Windows local deployment hardening (evaluation stage)

## Run the dashboard and collector

1. Open PowerShell in this project directory.
2. Run `run.bat` once to create `.venv` and install dependencies, or use an approved Python installation and install `requirements.txt`.
3. Configure `.env`; do not commit secrets.
4. Start the local test service only when needed: `.\.venv\Scripts\python.exe -m uvicorn demo_service.main:app --host 127.0.0.1 --port 8765`.
5. Start the dashboard with `run.bat`.
6. For continuous collection independent of Streamlit, close dashboard auto-collection first, then start `run_worker.bat`. Do not run both collectors simultaneously against the same database/target.

## Windows-specific safeguards before a pilot

- Run under a dedicated, non-administrator Windows account.
- Keep the dashboard and test service bound to loopback; do not expose the Streamlit port to a LAN or the internet.
- Use Windows Defender Firewall rules to block inbound access unless a reviewed access path is required.
- Store `.env` with NTFS ACLs limited to the service account and administrators. Never put tokens in command-line arguments or logs.
- Use a supported, patched Python version and pin dependencies to a reviewed lock file before deployment.
- Use Task Scheduler or a reviewed Windows service wrapper only after defining restart policy, log rotation, health checks, and shutdown behavior.
- Back up the SQLite database and test restoration. Avoid placing it on a network share.
- Approval records are persisted, expiring, action/target/incident-bound, and one-time. The approver label is an audit annotation, not authenticated identity: the current local UI does not provide login, MFA, or role-based authorization. Do not expose this UI as a production control plane.

## Human approval semantics

Every recovery execution must have a new approval ticket, a matching exact confirmation phrase, and a still-valid ticket for the same action, target URL, and incident ID. The ticket is consumed atomically before the recovery request is sent. If execution fails after consumption, the operator must investigate and request a new ticket for any retry. This avoids replay but means an interrupted operation may require a fresh approval.

## Validation status

These are implementation safeguards and testable behaviors, not evidence of production readiness. A real Windows validation still needs to exercise process crashes, reboot recovery, ACLs, firewall behavior, TLS/auth configuration, stale telemetry, SQLite contention/corruption recovery, backup restoration, and approval audit integrity on the actual target machine.
