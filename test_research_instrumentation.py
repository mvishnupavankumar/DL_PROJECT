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


def test_diagnosis_audit_omitted_case_behavior():
    """Validates that omitted API calls are classified as UNASSESSABLE, not INCORRECT."""
    from pathlib import Path
    import pandas as pd

    root = Path(__file__).resolve().parent
    df_preds = pd.read_csv(root / "research" / "raw" / "diagnosis_predictions.csv")
    df_metrics = pd.read_csv(root / "research" / "raw" / "diagnosis_metrics.csv")

    # Config 5 / INC-1002 omitted
    c5_1002 = df_preds[(df_preds["configuration"] == "5. Single-Agent (Groq LLM)") & (df_preds["incident_id"] == "INC-1002")].iloc[0]
    assert c5_1002["rubric_verdict"] == "UNASSESSABLE"
    assert c5_1002["top1_strict"] == 0
    assert c5_1002["top1_lenient"] == 0

    # Config 7 / INC-1004 omitted
    c7_1004 = df_preds[(df_preds["configuration"] == "7. Multi-Agent No-DL (Groq LLM)") & (df_preds["incident_id"] == "INC-1004")].iloc[0]
    assert c7_1004["rubric_verdict"] == "UNASSESSABLE"
    assert c7_1004["top1_strict"] == 0
    assert c7_1004["top1_lenient"] == 0

    # Summary metrics verification
    c5_metric = df_metrics[df_metrics["configuration"] == "5. Single-Agent (Groq LLM)"].iloc[0]
    assert c5_metric["completed_incidents"] == 5
    assert c5_metric["unassessable"] == 1
    assert c5_metric["per_protocol_accuracy"] == 0.8
    assert c5_metric["full_cohort_accuracy"] == 0.6667
    assert c5_metric["mean_latency_ms"] == 3041.87

    c7_metric = df_metrics[df_metrics["configuration"] == "7. Multi-Agent No-DL (Groq LLM)"].iloc[0]
    assert c7_metric["completed_incidents"] == 5
    assert c7_metric["unassessable"] == 1
    assert c7_metric["per_protocol_accuracy"] == 0.8
    assert c7_metric["full_cohort_accuracy"] == 0.6667
    assert c7_metric["mean_latency_ms"] == 19279.69


def test_safety_runners_import_side_effects_free(tmp_path):
    """Verifies that importing safety runners does not delete existing database files."""
    import importlib
    from pathlib import Path

    root = Path(__file__).resolve().parent
    canary = tmp_path / "canary.sqlite3"
    canary.write_text("canary data", encoding="utf-8")
    assert canary.exists()

    # Create dummy files at the runner module paths if they don't exist
    store_file = root / "data" / "safety_test_store.sqlite3"
    telemetry_file = root / "data" / "safety_telemetry.sqlite3"
    store_file.parent.mkdir(parents=True, exist_ok=True)
    if not store_file.exists():
        store_file.write_text("dummy store", encoding="utf-8")
    if not telemetry_file.exists():
        telemetry_file.write_text("dummy telemetry", encoding="utf-8")

    assert store_file.exists()
    assert telemetry_file.exists()

    # Import and reload safety runners
    import research.experiments.run_safety_audit
    import research.experiments.run_experiment_c
    importlib.reload(research.experiments.run_safety_audit)
    importlib.reload(research.experiments.run_experiment_c)

    # Ensure all files were completely preserved upon import/reload
    assert canary.exists()
    assert canary.read_text(encoding="utf-8") == "canary data"
    assert store_file.exists()
    assert telemetry_file.exists()
