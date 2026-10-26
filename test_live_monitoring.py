from __future__ import annotations

import math
import sqlite3
from datetime import datetime, timedelta, timezone

import numpy as np
import pytest

from collectors.system_metrics import collect_live_sample, validate_local_service_url
from dl.anomaly_detector import FEATURES, SEQUENCE_LENGTH
from dl.live_training import load_live_detector, train_live_model
from storage.telemetry_store import TelemetryStore


def _store_window(store, window, step_seconds=5):
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for index, values in enumerate(window):
        store.add_sample({
            "timestamp": (start + timedelta(seconds=index * step_seconds)).isoformat(),
            **{feature: float(values[position]) for position, feature in enumerate(FEATURES)},
            "service_available": True,
            "status_code": 200,
            "error_message": "",
            "fault_mode": "normal",
            "data_source": "phase13_test_fixture",
        })
    return store.recent_samples()


def _frozen_smoke_environment(monkeypatch, gap="6"):
    monkeypatch.setenv("AEGISOPS_LSTM_CHECKPOINT_PATH", "models/lstm_autoencoder.pt")
    monkeypatch.setenv("AEGISOPS_ENABLE_FROZEN_SMOKE_TEST", "true")
    monkeypatch.setenv("AEGISOPS_LSTM_MAX_INTER_SAMPLE_GAP_S", gap)


def test_local_service_url_is_restricted_to_loopback():
    assert validate_local_service_url("http://127.0.0.1:8765") == "http://127.0.0.1:8765"
    with pytest.raises(ValueError):
        validate_local_service_url("http://example.com:8765")
    with pytest.raises(ValueError):
        validate_local_service_url("https://127.0.0.1:8765")


def test_live_collector_persists_real_style_sample(tmp_path, monkeypatch):
    import collectors.system_metrics as collector

    monkeypatch.setattr(collector.psutil, "cpu_percent", lambda interval=0.1: 23.5)
    monkeypatch.setattr(collector.psutil, "virtual_memory", lambda: type("Mem", (), {"percent": 61.0})())
    monkeypatch.setattr(collector.psutil, "disk_usage", lambda path: type("Disk", (), {"percent": 47.0})())

    class Response:
        status_code = 200
        ok = True

        def json(self):
            return {"fault_mode": "normal", "status": "ok"}

    monkeypatch.setattr(collector.requests, "get", lambda *args, **kwargs: Response())
    store = TelemetryStore(tmp_path / "live.db")
    sample = collect_live_sample(store, "http://127.0.0.1:8765")
    assert sample["cpu_pct"] == 23.5
    assert sample["memory_pct"] == 61.0
    assert sample["status_code"] == 200
    rows = store.recent_samples()
    assert len(rows) == 1
    assert rows[0]["data_source"] == "live_local_host_and_http_probe"
    store.annotate_sample(rows[0]["id"], None, True, "bootstrap_rules")
    annotated = store.recent_samples()[0]
    assert annotated["anomaly_score"] is None
    assert annotated["is_anomaly"] == 1


def test_train_and_load_model_from_healthy_rows(tmp_path):
    count = 190
    rows = []
    for i in range(count):
        cpu = 38 + 5 * math.sin(i / 13)
        memory = 52 + 2 * math.sin(i / 47)
        latency = 35 + 0.5 * cpu + 2 * math.sin(i / 7)
        error = 0.0
        disk = 42 + i * 0.005
        rows.append(dict(zip(FEATURES, [cpu, memory, latency, error, disk])))
    out = tmp_path / "live_model.pt"
    result = train_live_model(rows, output_path=out, epochs=1, min_samples=180)
    assert result["training_samples"] > 0
    assert out.exists()
    from dl.anomaly_detector import TelemetryAnomalyDetector
    detector = TelemetryAnomalyDetector.load(out)
    window = np.asarray([[float(row[f]) for f in FEATURES] for row in rows[-SEQUENCE_LENGTH:]], dtype=np.float32)
    result = detector.detect(window)
    assert result["model"] == "LSTM Autoencoder"
    assert result["data_source"].startswith("Real live telemetry")
    assert set(result["latest_metrics"]) == set(FEATURES)


def test_csv_training_filter_excludes_non_healthy_rows(tmp_path):
    import pandas as pd
    from dl.train_from_csv import load_healthy_samples

    rows = []
    for i in range(181):
        rows.append({
            **dict(zip(FEATURES, [40 + i * 0.01, 50, 60, 0, 40])),
            "status_code": 200,
            "service_available": 1,
            "error_rate_pct": 0,
            "fault_mode": "normal",
        })
    rows.append({
        **dict(zip(FEATURES, [99, 99, 1500, 100, 99])),
        "status_code": 500,
        "service_available": 0,
        "error_rate_pct": 5,
        "fault_mode": "error",
    })
    csv = tmp_path / "telemetry.csv"
    pd.DataFrame(rows).to_csv(csv, index=False)
    samples = load_healthy_samples(csv)
    assert len(samples) == 181
    assert all(float(item["error_rate_pct"]) == 0 for item in samples)


def test_csv_training_requires_health_metadata_or_explicit_confirmation(tmp_path):
    import pandas as pd
    from dl.train_from_csv import load_healthy_samples

    csv = tmp_path / "telemetry.csv"
    pd.DataFrame([{feature: i + 1 for i, feature in enumerate(FEATURES)}] * 180).to_csv(csv, index=False)
    with pytest.raises(ValueError, match="no health/label columns"):
        load_healthy_samples(csv)
    assert len(load_healthy_samples(csv, assume_healthy=True)) == 180


def test_build_live_incident_scoping_and_name_error_prevention(monkeypatch):
    """
    Regression test for historical 'NameError: name is_local_target is not defined'.
    Verifies that _build_live_incident resolves target locality via _is_loopback_target(service_url)
    and does not rely on an external or uninitialized 'is_local_target' variable.
    """
    from live_monitoring import _build_live_incident

    sample = {
        "id": 42,
        "status_code": 500,
        "latency_ms": 120.0,
        "cpu_pct": 25.0,
        "memory_pct": 50.0,
        "disk_pct": 40.0,
        "error_rate_pct": 10.0,
    }
    analysis = {
        "model": "LSTM Autoencoder",
        "is_anomaly": True,
        "score": 0.85,
        "threshold": 0.709,
    }

    # 1. Local loopback target: should identify as loopback and handle health checks gracefully
    local_incident = _build_live_incident(sample, analysis, "http://127.0.0.1:8765")
    assert local_incident["id"] == "LIVE-000042"
    assert "Live AegisOps monitoring detected" in local_incident["description"]

    # 2. Remote target: should not raise NameError and must restrict valid_actions to read-only
    remote_incident = _build_live_incident(sample, analysis, "https://remote.api.production.internal")
    assert remote_incident["id"] == "LIVE-000042"
    assert remote_incident["valid_actions"] == ["capture_read_only_diagnostics"]


def test_live_lstm_default_missing_checkpoint_preserves_rules_fallback(tmp_path, monkeypatch):
    import dl.live_training as live_training
    from live_monitoring import _analyze_latest

    monkeypatch.setattr(live_training, "LIVE_MODEL_PATH", tmp_path / "missing_live.pt")
    monkeypatch.delenv("AEGISOPS_LSTM_CHECKPOINT_PATH", raising=False)
    monkeypatch.delenv("AEGISOPS_ENABLE_FROZEN_SMOKE_TEST", raising=False)
    monkeypatch.setenv("AEGISOPS_LSTM_MAX_INTER_SAMPLE_GAP_S", "6")
    store = TelemetryStore(tmp_path / "missing.db")
    rows = _store_window(store, np.zeros((SEQUENCE_LENGTH, len(FEATURES)), dtype=np.float32) + 40)

    analysis, mode = _analyze_latest(store, rows)
    persisted = store.recent_samples(1)[0]
    assert mode == "bootstrap_rules"
    assert analysis["inference_reason"] == "checkpoint_absent"
    assert persisted["anomaly_score"] is None
    assert persisted["inference_reason"] == "checkpoint_absent"
    assert persisted["checkpoint_provenance"] == "live_trained"


def test_frozen_checkpoint_requires_explicit_smoke_test_opt_in(tmp_path, monkeypatch):
    from live_monitoring import _analyze_latest

    monkeypatch.setenv("AEGISOPS_LSTM_CHECKPOINT_PATH", "models/lstm_autoencoder.pt")
    monkeypatch.setenv("AEGISOPS_ENABLE_FROZEN_SMOKE_TEST", "false")
    store = TelemetryStore(tmp_path / "rejected.db")
    rows = _store_window(store, np.zeros((SEQUENCE_LENGTH, len(FEATURES)), dtype=np.float32) + 40)

    analysis, mode = _analyze_latest(store, rows)
    persisted = store.recent_samples(1)[0]
    assert mode == "bootstrap_rules"
    assert analysis["inference_reason"] == "checkpoint_selection_rejected"
    assert persisted["checkpoint_provenance"] == "frozen_synthetic_smoke_test"


def test_frozen_smoke_test_scores_and_persists_provenance(tmp_path, monkeypatch):
    from dl.anomaly_detector import generate_normal_windows
    from live_monitoring import _analyze_latest

    _frozen_smoke_environment(monkeypatch)
    store = TelemetryStore(tmp_path / "success.db")
    rows = _store_window(store, generate_normal_windows(1, seed=123)[0])

    analysis, mode = _analyze_latest(store, rows)
    persisted = store.recent_samples(1)[0]
    assert mode == "live_lstm_autoencoder"
    assert analysis["inference_reason"] == "inference_success"
    assert np.isfinite(analysis["score"])
    assert persisted["anomaly_score"] is not None
    assert persisted["model_anomaly"] in {0, 1}
    assert persisted["rule_anomaly"] in {0, 1}
    assert persisted["combined_anomaly"] in {0, 1}
    assert persisted["checkpoint_provenance"] == "frozen_synthetic_smoke_test"
    assert persisted["checkpoint_identity"].startswith("lstm_autoencoder.pt:sha256:")


def test_live_lstm_window_rejects_invalid_features_and_timestamps(tmp_path, monkeypatch):
    from dl.anomaly_detector import generate_normal_windows
    from live_monitoring import _analyze_latest

    _frozen_smoke_environment(monkeypatch)
    store = TelemetryStore(tmp_path / "invalid.db")
    rows = _store_window(store, generate_normal_windows(1, seed=124)[0])
    rows[3]["cpu_pct"] = float("nan")
    analysis, mode = _analyze_latest(store, rows)
    assert mode == "bootstrap_rules"
    assert analysis["inference_reason"] == "invalid_features"
    assert store.recent_samples(1)[0]["anomaly_score"] is None

    rows = _store_window(TelemetryStore(tmp_path / "timestamps.db"), generate_normal_windows(1, seed=125)[0])
    rows[10]["timestamp"] = "not-a-timestamp"
    analysis, mode = _analyze_latest(TelemetryStore(tmp_path / "timestamps.db"), rows)
    assert mode == "bootstrap_rules"
    assert analysis["inference_reason"] == "window_not_ready"

    timestamp_store = TelemetryStore(tmp_path / "nonmonotonic.db")
    rows = _store_window(timestamp_store, generate_normal_windows(1, seed=132)[0])
    rows[12]["timestamp"] = rows[11]["timestamp"]
    analysis, mode = _analyze_latest(timestamp_store, rows)
    assert mode == "bootstrap_rules"
    assert analysis["inference_reason"] == "window_not_ready"

    shape_store = TelemetryStore(tmp_path / "wrong_features.db")
    rows = _store_window(shape_store, generate_normal_windows(1, seed=133)[0])
    del rows[4]["disk_pct"]
    analysis, mode = _analyze_latest(shape_store, rows)
    assert mode == "bootstrap_rules"
    assert analysis["inference_reason"] == "invalid_features"


def test_live_lstm_window_requires_twenty_four_rows(tmp_path, monkeypatch):
    from dl.anomaly_detector import generate_normal_windows
    from live_monitoring import _analyze_latest

    _frozen_smoke_environment(monkeypatch)
    store = TelemetryStore(tmp_path / "short_window.db")
    rows = _store_window(store, generate_normal_windows(1, seed=130)[0][:-1])
    analysis, mode = _analyze_latest(store, rows)
    assert mode == "bootstrap_rules"
    assert analysis["inference_reason"] == "insufficient_rows"


def test_live_lstm_window_rejects_gap_and_missing_gap_configuration(tmp_path, monkeypatch):
    from dl.anomaly_detector import generate_normal_windows
    from live_monitoring import _analyze_latest

    _frozen_smoke_environment(monkeypatch, gap="6")
    store = TelemetryStore(tmp_path / "gap.db")
    rows = _store_window(store, generate_normal_windows(1, seed=126)[0], step_seconds=5)
    rows[12]["timestamp"] = (datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=90)).isoformat()
    analysis, mode = _analyze_latest(store, rows)
    assert mode == "bootstrap_rules"
    assert analysis["inference_reason"] == "timestamp_gap_exceeded"
    assert store.recent_samples(1)[0]["inference_reason"] == "timestamp_gap_exceeded"

    monkeypatch.delenv("AEGISOPS_LSTM_MAX_INTER_SAMPLE_GAP_S", raising=False)
    store = TelemetryStore(tmp_path / "no_gap_config.db")
    rows = _store_window(store, generate_normal_windows(1, seed=127)[0])
    analysis, mode = _analyze_latest(store, rows)
    assert mode == "bootstrap_rules"
    assert analysis["inference_reason"] == "window_not_ready"


def test_live_lstm_load_and_inference_failures_are_sanitized(tmp_path, monkeypatch):
    import live_monitoring
    from dl.anomaly_detector import generate_normal_windows

    _frozen_smoke_environment(monkeypatch)
    store = TelemetryStore(tmp_path / "load_failure.db")
    rows = _store_window(store, generate_normal_windows(1, seed=128)[0])
    monkeypatch.setattr(live_monitoring, "load_live_detector", lambda path: (_ for _ in ()).throw(RuntimeError("sensitive detail")))
    analysis, mode = live_monitoring._analyze_latest(store, rows)
    assert mode == "bootstrap_rules"
    assert analysis["inference_reason"] == "checkpoint_load_failure"

    class FailingDetector:
        def detect(self, window):
            raise RuntimeError("sensitive detail")

    store = TelemetryStore(tmp_path / "inference_failure.db")
    rows = _store_window(store, generate_normal_windows(1, seed=129)[0])
    monkeypatch.setattr(live_monitoring, "load_live_detector", lambda path: FailingDetector())
    analysis, mode = live_monitoring._analyze_latest(store, rows)
    assert mode == "bootstrap_rules"
    assert analysis["inference_reason"] == "inference_failure"
    assert store.recent_samples(1)[0]["anomaly_score"] is None


def test_live_lstm_malformed_selected_checkpoint_falls_back(tmp_path, monkeypatch):
    import dl.live_training as live_training
    from dl.anomaly_detector import generate_normal_windows
    from live_monitoring import _analyze_latest

    malformed = tmp_path / "malformed_live.pt"
    malformed.write_bytes(b"not a checkpoint")
    monkeypatch.setattr(live_training, "LIVE_MODEL_PATH", malformed)
    monkeypatch.delenv("AEGISOPS_LSTM_CHECKPOINT_PATH", raising=False)
    monkeypatch.delenv("AEGISOPS_ENABLE_FROZEN_SMOKE_TEST", raising=False)
    monkeypatch.setenv("AEGISOPS_LSTM_MAX_INTER_SAMPLE_GAP_S", "6")
    store = TelemetryStore(tmp_path / "malformed.db")
    rows = _store_window(store, generate_normal_windows(1, seed=131)[0])
    analysis, mode = _analyze_latest(store, rows)
    assert mode == "bootstrap_rules"
    assert analysis["inference_reason"] == "checkpoint_load_failure"


def test_legacy_schema_migrates_inference_provenance_columns(tmp_path):
    db_path = tmp_path / "legacy.sqlite3"
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE telemetry_samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL,
                cpu_pct REAL NOT NULL, memory_pct REAL NOT NULL, latency_ms REAL NOT NULL,
                error_rate_pct REAL NOT NULL, disk_pct REAL NOT NULL,
                service_available INTEGER NOT NULL, status_code INTEGER NOT NULL,
                error_message TEXT NOT NULL DEFAULT '', fault_mode TEXT NOT NULL DEFAULT 'unknown',
                data_source TEXT NOT NULL DEFAULT 'legacy', anomaly_score REAL, is_anomaly INTEGER,
                detector_mode TEXT NOT NULL DEFAULT 'bootstrap_rules', model_anomaly INTEGER,
                rule_anomaly INTEGER, combined_anomaly INTEGER
            )
        """)

    store = TelemetryStore(db_path)
    sample_id = store.add_sample({
        "timestamp": TelemetryStore.now_iso(), "cpu_pct": 10, "memory_pct": 20,
        "latency_ms": 30, "error_rate_pct": 0, "disk_pct": 40,
        "service_available": True, "status_code": 200,
    })
    store.annotate_sample(
        sample_id, 0.2, False, "live_lstm_autoencoder", False, False,
        "inference_success", "test", "fixture:sha256:1234",
    )
    row = store.recent_samples(1)[0]
    assert row["inference_reason"] == "inference_success"
    assert row["checkpoint_provenance"] == "test"
    assert row["checkpoint_identity"] == "fixture:sha256:1234"

