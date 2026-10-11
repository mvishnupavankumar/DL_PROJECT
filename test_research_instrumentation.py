from storage.telemetry_store import TelemetryStore


def sample():
    return {
        "timestamp": TelemetryStore.now_iso(), "cpu_pct": 10.0, "memory_pct": 50.0,
        "latency_ms": 10.0, "error_rate_pct": 0.0, "disk_pct": 20.0,
        "service_available": True, "status_code": 200, "error_message": "",
        "fault_mode": "normal", "data_source": "research_test",
    }


def test_research_prediction_fields_are_migrated_and_persisted(tmp_path):
    store = TelemetryStore(tmp_path / "research.sqlite3")
    sample_id = store.add_sample(sample())
    store.annotate_sample(sample_id, 0.2, False, "live_lstm_autoencoder", model_anomaly=False, rule_anomaly=False)
    row = store.recent_samples(1)[0]
    assert row["model_anomaly"] == 0
    assert row["rule_anomaly"] == 0
    assert row["combined_anomaly"] == 0
    assert row["anomaly_score"] == 0.2


def test_missing_raw_model_prediction_is_null_not_false(tmp_path):
    store = TelemetryStore(tmp_path / "research.sqlite3")
    sample_id = store.add_sample(sample())
    store.annotate_sample(sample_id, None, True, "bootstrap_rules", model_anomaly=None, rule_anomaly=True)
    row = store.recent_samples(1)[0]
    assert row["model_anomaly"] is None
    assert row["rule_anomaly"] == 1
    assert row["combined_anomaly"] == 1
