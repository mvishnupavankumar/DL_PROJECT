from __future__ import annotations

import math

import numpy as np
import pytest

from collectors.system_metrics import collect_live_sample, validate_local_service_url
from dl.anomaly_detector import FEATURES, SEQUENCE_LENGTH
from dl.live_training import load_live_detector, train_live_model
from storage.telemetry_store import TelemetryStore


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

