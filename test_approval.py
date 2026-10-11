from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import sqlite3
from datetime import datetime, timedelta, timezone

import pytest

from approval import ApprovalError, ApprovalStore


def setup_ticket(tmp_path):
    store = ApprovalStore(tmp_path / "approvals.sqlite3", ttl_seconds=60)
    ticket = store.request(
        action_id="clear_demo_service_fault",
        target="http://127.0.0.1:8765",
        incident_id="LIVE-000123",
        requested_by="local_operator",
    )
    return store, ticket


def test_approval_requires_exact_phrase_and_correct_scope(tmp_path):
    store, ticket = setup_ticket(tmp_path)
    with pytest.raises(ApprovalError, match="Exact confirmation"):
        store.approve(ticket["ticket_id"], "clear_demo_service_fault",
                      "http://127.0.0.1:8765", "LIVE-000123",
                      "operator", "yes")
    with pytest.raises(ApprovalError, match="scope"):
        store.approve(ticket["ticket_id"], "clear_demo_service_fault",
                      "http://127.0.0.1:9999", "LIVE-000123",
                      "operator", "APPROVE clear_demo_service_fault")
    assert store.get(ticket["ticket_id"])["status"] == "pending"


def test_approved_ticket_is_bound_to_action_target_and_incident(tmp_path):
    store, ticket = setup_ticket(tmp_path)
    tid = ticket["ticket_id"]
    store.approve(tid, "clear_demo_service_fault", "http://127.0.0.1:8765",
                  "LIVE-000123", "operator", "APPROVE clear_demo_service_fault")
    with pytest.raises(ApprovalError, match="scope mismatch"):
        store.consume(tid, "clear_demo_service_fault", "http://127.0.0.1:9999", "LIVE-000123")
    assert store.get(tid)["status"] == "approved"


def test_approval_can_be_consumed_only_once(tmp_path):
    store, ticket = setup_ticket(tmp_path)
    tid = ticket["ticket_id"]
    scope = ("clear_demo_service_fault", "http://127.0.0.1:8765", "LIVE-000123")
    store.approve(tid, *scope, approved_by="operator", confirmation="APPROVE clear_demo_service_fault")
    assert store.consume(tid, *scope)["status"] == "consumed"
    with pytest.raises(ApprovalError, match="consumed"):
        store.consume(tid, *scope)


def test_expired_approval_cannot_be_approved_or_consumed(tmp_path):
    store, ticket = setup_ticket(tmp_path)
    tid = ticket["ticket_id"]
    with sqlite3.connect(store.db_path) as conn:
        conn.execute("UPDATE recovery_approvals SET expires_at=? WHERE ticket_id=?",
                     ((datetime.now(timezone.utc) - timedelta(seconds=2)).isoformat(timespec="seconds"), tid))
    with pytest.raises(ApprovalError, match="expired"):
        store.approve(tid, "clear_demo_service_fault", "http://127.0.0.1:8765",
                      "LIVE-000123", "operator", "APPROVE clear_demo_service_fault")
    assert store.get(tid)["status"] == "expired"


def test_ticket_must_exist_and_request_fields_are_required(tmp_path):
    store = ApprovalStore(tmp_path / "approvals.sqlite3")
    with pytest.raises(ValueError):
        store.request("clear_demo_service_fault", "", "LIVE-1", "operator")
    with pytest.raises(ApprovalError, match="does not exist"):
        store.get("missing")

def test_approved_ticket_cannot_be_consumed_after_expiry(tmp_path):
    store, ticket = setup_ticket(tmp_path)
    tid = ticket["ticket_id"]
    scope = (
        "clear_demo_service_fault",
        "http://127.0.0.1:8765",
        "LIVE-000123",
    )

    store.approve(
        tid,
        *scope,
        approved_by="operator",
        confirmation="APPROVE clear_demo_service_fault",
    )

    with sqlite3.connect(store.db_path) as conn:
        conn.execute(
            "UPDATE recovery_approvals SET expires_at=? WHERE ticket_id=?",
            (
                (
                    datetime.now(timezone.utc) - timedelta(seconds=2)
                ).isoformat(timespec="seconds"),
                tid,
            ),
        )

    with pytest.raises(ApprovalError, match="expired"):
        store.consume(tid, *scope)

    assert store.get(tid)["status"] == "expired"


def test_rejected_ticket_cannot_be_approved_or_consumed(tmp_path):
    store, ticket = setup_ticket(tmp_path)
    tid = ticket["ticket_id"]
    scope = (
        "clear_demo_service_fault",
        "http://127.0.0.1:8765",
        "LIVE-000123",
    )

    store.reject(tid, rejected_by="operator")

    with pytest.raises(ApprovalError):
        store.approve(
            tid,
            *scope,
            approved_by="operator",
            confirmation="APPROVE clear_demo_service_fault",
        )

    with pytest.raises(ApprovalError):
        store.consume(tid, *scope)

    assert store.get(tid)["status"] == "rejected"

def test_concurrent_consumers_can_consume_ticket_only_once(tmp_path):
    store, ticket = setup_ticket(tmp_path)
    tid = ticket["ticket_id"]
    scope = (
        "clear_demo_service_fault",
        "http://127.0.0.1:8765",
        "LIVE-000123",
    )

    store.approve(
        tid,
        *scope,
        approved_by="operator",
        confirmation="APPROVE clear_demo_service_fault",
    )

    barrier = Barrier(2)

    def attempt_consume():
        barrier.wait()

        try:
            result = store.consume(tid, *scope)
            return result["status"]
        except ApprovalError:
            return "rejected"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(
            lambda _: attempt_consume(),
            range(2),
        ))

    assert results.count("consumed") == 1
    assert results.count("rejected") == 1
    assert store.get(tid)["status"] == "consumed"


