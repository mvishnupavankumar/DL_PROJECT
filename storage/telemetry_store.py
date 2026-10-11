from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = ROOT / "data" / "aegisops_live.sqlite3"


class TelemetryStore:
    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="milliseconds")

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_samples (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    cpu_pct REAL NOT NULL,
                    memory_pct REAL NOT NULL,
                    latency_ms REAL NOT NULL,
                    error_rate_pct REAL NOT NULL,
                    disk_pct REAL NOT NULL,
                    service_available INTEGER NOT NULL,
                    status_code INTEGER NOT NULL,
                    error_message TEXT NOT NULL DEFAULT '',
                    fault_mode TEXT NOT NULL DEFAULT 'unknown',
                    data_source TEXT NOT NULL DEFAULT 'live_local_host_and_http_probe',
                    anomaly_score REAL,
                    is_anomaly INTEGER,
                    detector_mode TEXT NOT NULL DEFAULT 'bootstrap_rules'
                )
            """)
            # Add columns when upgrading a database created by an earlier prototype build.
            columns = {row[1] for row in conn.execute("PRAGMA table_info(telemetry_samples)").fetchall()}
            if "fault_mode" not in columns:
                conn.execute("ALTER TABLE telemetry_samples ADD COLUMN fault_mode TEXT NOT NULL DEFAULT 'unknown'")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_timestamp ON telemetry_samples(timestamp)")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS incident_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
            """)

    def add_sample(self, sample: dict[str, Any]) -> int:
        with self._connect() as conn:
            cur = conn.execute("""
                INSERT INTO telemetry_samples (
                    timestamp, cpu_pct, memory_pct, latency_ms, error_rate_pct, disk_pct,
                    service_available, status_code, error_message, fault_mode, data_source
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sample["timestamp"], sample["cpu_pct"], sample["memory_pct"],
                sample["latency_ms"], sample["error_rate_pct"], sample["disk_pct"],
                int(sample["service_available"]), sample["status_code"], sample.get("error_message", ""),
                sample.get("fault_mode", "unknown"), sample.get("data_source", "live_local_host_and_http_probe"),
            ))
            return int(cur.lastrowid)

    def recent_probe_outcomes(self, limit: int = 19) -> list[int]:
        with self._connect() as conn:
            rows = conn.execute("SELECT status_code FROM telemetry_samples ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [int(row["status_code"]) for row in reversed(rows)]

    def recent_samples(self, limit: int = 1000) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM telemetry_samples ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(row) for row in reversed(rows)]

    def all_samples(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM telemetry_samples ORDER BY id ASC").fetchall()
        return [dict(row) for row in rows]

    def healthy_training_samples(self) -> list[dict[str, Any]]:
        # Keep only successful probe rows and avoid windows polluted by recent failures.
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT * FROM telemetry_samples
                WHERE service_available = 1 AND status_code = 200 AND error_rate_pct = 0 AND fault_mode = 'normal'
                  AND cpu_pct < 90 AND memory_pct < 95 AND disk_pct < 95 AND latency_ms < 1000
                ORDER BY id ASC
            """).fetchall()
        return [dict(row) for row in rows]

    def annotate_sample(self, sample_id: int, score: float | None, is_anomaly: bool, mode: str) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE telemetry_samples SET anomaly_score=?, is_anomaly=?, detector_mode=? WHERE id=?",
                         (None if score is None else float(score), int(is_anomaly), mode, int(sample_id)))

    def sample_count(self) -> int:
        with self._connect() as conn:
            return int(conn.execute("SELECT COUNT(*) FROM telemetry_samples").fetchone()[0])

    def log_event(self, event_type: str, payload: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute("INSERT INTO incident_events(timestamp, event_type, payload_json) VALUES (?, ?, ?)",
                         (self.now_iso(), event_type, json.dumps(payload, default=str)))

    def recent_events(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM incident_events ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        output = []
        for row in rows:
            item = dict(row)
            try:
                item["payload"] = json.loads(item.pop("payload_json"))
            except (TypeError, json.JSONDecodeError):
                item["payload"] = {}
            output.append(item)
        return output
