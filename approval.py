"""Durable, expiring, one-time approvals for explicitly scoped recovery actions.

This is a workflow guard, not an identity provider. The local Streamlit UI has no
authenticated user identity; approval actor strings are audit annotations only.
"""
from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(value: datetime) -> str:
    return value.isoformat(timespec="seconds")


class ApprovalError(RuntimeError):
    pass


class ApprovalStore:
    def __init__(self, db_path: str | Path, ttl_seconds: int = 300):
        if not 30 <= int(ttl_seconds) <= 1800:
            raise ValueError("Approval TTL must be between 30 and 1800 seconds.")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = int(ttl_seconds)
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS recovery_approvals (
                    ticket_id TEXT PRIMARY KEY,
                    action_id TEXT NOT NULL,
                    target TEXT NOT NULL,
                    incident_id TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('pending','approved','rejected','consumed','expired')),
                    requested_by TEXT NOT NULL,
                    approved_by TEXT,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    approved_at TEXT,
                    consumed_at TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_approval_status ON recovery_approvals(status, expires_at)")

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10, isolation_level=None)
        conn.row_factory = sqlite3.Row
        return conn

    def request(self, action_id: str, target: str, incident_id: str, requested_by: str) -> dict[str, Any]:
        values = [action_id, target, incident_id, requested_by]
        if any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError("Action, target, incident, and requester are required.")
        now = _now()
        ticket = str(uuid.uuid4())
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute("""INSERT INTO recovery_approvals
                (ticket_id, action_id, target, incident_id, status, requested_by, created_at, expires_at)
                VALUES (?, ?, ?, ?, 'pending', ?, ?, ?)""",
                (ticket, action_id, target, incident_id, requested_by.strip(), _iso(now),
                 _iso(now + timedelta(seconds=self.ttl_seconds))))
            conn.execute("COMMIT")
        return self.get(ticket)

    def get(self, ticket_id: str) -> dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM recovery_approvals WHERE ticket_id=?", (ticket_id,)).fetchone()
        if row is None:
            raise ApprovalError("Approval ticket does not exist.")
        return dict(row)

    def approve(self, ticket_id: str, action_id: str, target: str, incident_id: str,
                approved_by: str, confirmation: str) -> dict[str, Any]:
        if confirmation != f"APPROVE {action_id}":
            raise ApprovalError("Exact confirmation phrase did not match.")
        if not approved_by.strip():
            raise ApprovalError("Approver label is required.")
        now = _now()
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT * FROM recovery_approvals WHERE ticket_id=?", (ticket_id,)).fetchone()
            if row is None:
                conn.execute("ROLLBACK")
                raise ApprovalError("Approval ticket does not exist.")
            if row["status"] != "pending":
                conn.execute("ROLLBACK")
                raise ApprovalError(f"Ticket is {row['status']}; only pending tickets can be approved.")
            if row["expires_at"] <= _iso(now):
                conn.execute("UPDATE recovery_approvals SET status='expired' WHERE ticket_id=?", (ticket_id,))
                conn.execute("COMMIT")
                raise ApprovalError("Approval ticket expired; request a new approval.")
            if (row["action_id"], row["target"], row["incident_id"]) != (action_id, target, incident_id):
                conn.execute("ROLLBACK")
                raise ApprovalError("Approval scope does not match the requested action, target, and incident.")
            conn.execute("""UPDATE recovery_approvals SET status='approved', approved_by=?, approved_at=?
                            WHERE ticket_id=? AND status='pending'""",
                         (approved_by.strip(), _iso(now), ticket_id))
            conn.execute("COMMIT")
        return self.get(ticket_id)

    def consume(self, ticket_id: str, action_id: str, target: str, incident_id: str) -> dict[str, Any]:
        """Atomically consume a valid approval immediately before the action executes."""
        now = _now()
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT * FROM recovery_approvals WHERE ticket_id=?", (ticket_id,)).fetchone()
            if row is None:
                conn.execute("ROLLBACK")
                raise ApprovalError("Approval ticket does not exist.")
            if row["status"] != "approved":
                conn.execute("ROLLBACK")
                raise ApprovalError(f"Ticket is {row['status']}; a fresh approved ticket is required.")
            if row["expires_at"] <= _iso(now):
                conn.execute("UPDATE recovery_approvals SET status='expired' WHERE ticket_id=?", (ticket_id,))
                conn.execute("COMMIT")
                raise ApprovalError("Approval ticket expired; request a new approval.")
            if (row["action_id"], row["target"], row["incident_id"]) != (action_id, target, incident_id):
                conn.execute("ROLLBACK")
                raise ApprovalError("Approval scope mismatch; no action was authorized.")
            cur = conn.execute("""UPDATE recovery_approvals SET status='consumed', consumed_at=?
                                  WHERE ticket_id=? AND status='approved'""", (_iso(now), ticket_id))
            if cur.rowcount != 1:
                conn.execute("ROLLBACK")
                raise ApprovalError("Approval was already consumed; request a new approval.")
            conn.execute("COMMIT")
        return self.get(ticket_id)

    def reject(self, ticket_id: str, rejected_by: str) -> dict[str, Any]:
        if not rejected_by.strip():
            raise ValueError("Rejector label is required.")
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            cur = conn.execute("""UPDATE recovery_approvals SET status='rejected', approved_by=?
                                  WHERE ticket_id=? AND status='pending'""",
                               (f"REJECTED:{rejected_by.strip()}", ticket_id))
            if cur.rowcount != 1:
                conn.execute("ROLLBACK")
                raise ApprovalError("Only a pending ticket can be rejected.")
            conn.execute("COMMIT")
        return self.get(ticket_id)
