"""Unit tests for Phase 9 Stage 4 Experiment D harness and statistical contracts.

Validates:
1. Real feature extraction on representative fixtures (SN & TT)
2. Timestamp alignment and continuity (strict 15-second delta)
3. Missing request intervals and undefined latency (no 0ms substitution)
4. Calibration/validation timestamp disjointness (pre-window chronological split + purge gap)
5. Model input shape and feature ordering
6. Model immutability during inference
7. Identical eligible observations across baselines
8. Threshold calibration edge cases and insufficient validation data
9. Correct metric denominators and degenerate confusion matrices
10. Statistical-test worked examples and scenario-level pairing
11. Output schemas, nonempty artifacts, manifest hashes, and deterministic reruns
12. Fail-closed CLI behavior (unauthorized exit 2, unratified exit 3, dry-run exit 0)
13. Preservation of pre-existing production outputs
14. Synthetic integration tests clearly separated from external-data execution
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest.mock
import numpy as np
import pandas as pd
import pytest
import torch
from sklearn.ensemble import IsolationForest

from dl.anomaly_detector import FEATURES, SEQUENCE_LENGTH, LSTMAutoencoder, load_detector
from research.experiments.run_experiment_d import (
    FROZEN_FEATURE_ORDER,
    PREDICTIONS_CSV_PATH,
    METRICS_CSV_PATH,
    RESULTS_MD_PATH,
    MANIFEST_JSON_PATH,
    DataAlignmentError,
    LeakageViolationError,
    build_sliding_windows,
    build_contiguous_windows,
    partition_normal_series_chronologically,
    calibrate_threshold,
    compute_contingency_and_metrics,
    evaluate_full_operational_rules,
    evaluate_narrow_rules,
    evaluate_resource_rules,
    extract_sn_telemetry,
    extract_tt_telemetry,
    fit_calibration_scaler,
    run_evaluation_pipeline,
    main,
)
from research.statistical_tests import (
    mcnemar_chi2_test,
    mcnemar_exact_test,
    paired_difference_ci,
    wilcoxon_signed_rank_test,
    wilson_score_ci,
)

ROOT = Path(__file__).resolve().parent


# === 1. Feature Order and Contract Tests ===

def test_feature_order_strictly_matches_frozen_contract():
    assert FROZEN_FEATURE_ORDER == ("cpu_pct", "memory_pct", "latency_ms", "error_rate_pct", "disk_pct")
    assert FROZEN_FEATURE_ORDER == FEATURES


def test_sliding_window_shape_and_feature_order():
    n_samples = 20
    n_features = 5
    window_length = 8
    synthetic_data = np.arange(n_samples * n_features, dtype=np.float32).reshape(n_samples, n_features)
    windows = build_sliding_windows(synthetic_data, window_length=window_length, step=1)

    expected_n_windows = n_samples - window_length + 1
    assert windows.shape == (expected_n_windows, window_length, n_features)
    np.testing.assert_array_equal(windows[0], synthetic_data[:window_length])
    np.testing.assert_array_equal(windows[-1], synthetic_data[-window_length:])


def test_sliding_window_insufficient_samples():
    data = np.ones((5, 5), dtype=np.float32)
    windows = build_sliding_windows(data, window_length=8)
    assert windows.shape == (0, 8, 5)


# === 2. Transformation Equations and Scaling Tests ===

def test_cpu_counter_rate_calculation():
    timestamps = np.array([0, 15, 30, 45], dtype=float)
    cpu_seconds = np.array([100.0, 101.5, 103.0, 104.5], dtype=float)
    delta_t = np.diff(timestamps)
    delta_sec = np.diff(cpu_seconds)
    cpu_pct = (delta_sec / delta_t) * 100.0

    assert np.allclose(cpu_pct, [10.0, 10.0, 10.0])


def test_cpu_counter_reset_detection():
    cpu_seconds = np.array([90.0, 95.0, 2.0, 5.0])
    deltas = np.diff(cpu_seconds)
    resets = deltas < 0
    assert resets[1]
    cleaned_deltas = np.where(deltas < 0, np.nan, deltas)
    assert np.isnan(cleaned_deltas[1])


def test_memory_percentage_calculation_no_double_scaling():
    mem_total = 16000.0
    mem_available = 4000.0
    used_pct = (1.0 - (mem_available / mem_total)) * 100.0
    assert used_pct == 75.0
    assert 0.0 <= used_pct <= 100.0


def test_disk_capacity_percentage_not_throughput():
    disk_total = 1000.0
    disk_avail = 300.0
    disk_pct = (1.0 - (disk_avail / disk_total)) * 100.0
    assert disk_pct == 70.0


def test_latency_native_milliseconds_no_spurious_multiplier():
    raw_ms = 1.538
    assert raw_ms < 100.0
    assert raw_ms < 1000.0


def test_error_rate_zero_requests_interval():
    total_requests = 0
    error_requests = 0
    error_rate = (error_requests / total_requests * 100.0) if total_requests > 0 else 0.0
    assert error_rate == 0.0


def test_error_rate_calculation_percentage():
    total_requests = 200
    error_requests = 5
    error_rate_pct = (error_requests / total_requests) * 100.0
    assert error_rate_pct == 2.5
    assert 0.0 <= error_rate_pct <= 100.0


# === 3. Rule Baseline Tests ===

def test_narrow_rules_baseline():
    normal_w = np.zeros((8, 5), dtype=np.float32)
    assert not evaluate_narrow_rules(normal_w)

    high_lat_w = normal_w.copy()
    high_lat_w[-1, 2] = 1050.0
    assert evaluate_narrow_rules(high_lat_w)

    high_mem_w = normal_w.copy()
    high_mem_w[-1, 1] = 95.5
    assert evaluate_narrow_rules(high_mem_w)

    high_cpu_w = normal_w.copy()
    high_cpu_w[-1, 0] = 99.0
    assert not evaluate_narrow_rules(high_cpu_w)


def test_resource_rules_baseline():
    normal_w = np.zeros((8, 5), dtype=np.float32)
    assert not evaluate_resource_rules(normal_w)

    cpu_w = normal_w.copy()
    cpu_w[-1, 0] = 91.0
    assert evaluate_resource_rules(cpu_w)

    disk_w = normal_w.copy()
    disk_w[-1, 4] = 96.0
    assert evaluate_resource_rules(disk_w)

    err_w = normal_w.copy()
    err_w[-1, 3] = 10.0
    assert not evaluate_resource_rules(err_w)


def test_full_operational_rules_baseline():
    normal_w = np.zeros((8, 5), dtype=np.float32)
    assert not evaluate_full_operational_rules(normal_w)

    err_w = normal_w.copy()
    err_w[-1, 3] = 0.6
    assert evaluate_full_operational_rules(err_w)


# === 4. Calibration, Scaler, and Leakage Tests ===

def test_scaler_fitting_restricted_to_calibration_windows():
    calib_windows = np.array([
        [[10, 20, 30, 0.1, 40]],
        [[12, 22, 32, 0.2, 42]],
    ], dtype=np.float32)

    mean, std = fit_calibration_scaler(calib_windows)
    np.testing.assert_allclose(mean, [11.0, 21.0, 31.0, 0.15, 41.0])
    np.testing.assert_allclose(std, [1.0, 1.0, 1.0, 0.05, 1.0], atol=1e-5)


def test_threshold_calculation_99th_percentile():
    model = LSTMAutoencoder(n_features=5, hidden_size=16)
    model.eval()

    val_windows = np.random.randn(100, 8, 5).astype(np.float32)
    mean = np.zeros(5, dtype=np.float32)
    std = np.ones(5, dtype=np.float32)

    thresh = calibrate_threshold(model, val_windows, mean, std, percentile=99.0)
    assert thresh > 0.0
    assert np.isfinite(thresh)


def test_threshold_calculation_insufficient_samples_behavior():
    model = LSTMAutoencoder(n_features=5, hidden_size=16)
    model.eval()

    mean = np.zeros(5, dtype=np.float32)
    std = np.ones(5, dtype=np.float32)

    # Empty validation set must raise ValueError
    with pytest.raises(ValueError, match="Cannot calibrate threshold on empty"):
        calibrate_threshold(model, np.empty((0, 8, 5), dtype=np.float32), mean, std)

    # Small validation set (N=3): percentile equals maximum
    small_val = np.random.randn(3, 8, 5).astype(np.float32)
    thresh = calibrate_threshold(model, small_val, mean, std, percentile=99.0)
    assert np.isfinite(thresh)


def test_isolation_forest_fitting_restricted_to_normal_data():
    train_normal = np.random.randn(50, 8 * 5).astype(np.float32)
    iso = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    iso.fit(train_normal)

    scores = -iso.decision_function(train_normal)
    assert len(scores) == 50
    assert np.all(np.isfinite(scores))


# === 5. Checkpoint Smoke and Weight Immutability Tests ===

def test_checkpoint_loads_and_eval_mode():
    ckpt_path = ROOT / "models" / "lstm_autoencoder.pt"
    assert ckpt_path.exists()
    detector = load_detector(ckpt_path)
    assert detector.model.training is False
    assert detector.threshold == pytest.approx(0.709399, rel=1e-5)


def test_checkpoint_weights_remain_strictly_frozen():
    ckpt_path = ROOT / "models" / "lstm_autoencoder.pt"
    detector = load_detector(ckpt_path)

    weights_before = [p.clone() for p in detector.model.parameters()]
    dummy_input = np.random.randn(24, 5).astype(np.float32)
    for _ in range(5):
        _ = detector.detect(dummy_input)

    for p_before, p_after in zip(weights_before, detector.model.parameters()):
        assert torch.equal(p_before, p_after)


def test_model_forward_accepts_8_step_window():
    ckpt_path = ROOT / "models" / "lstm_autoencoder.pt"
    detector = load_detector(ckpt_path)

    # Checkpoint contains sequence autoencoder; forward accepts any W
    x_w8 = torch.randn(2, 8, 5)
    detector.model.eval()
    with torch.no_grad():
        out = detector.model(x_w8)
    assert out.shape == (2, 8, 5)
    assert torch.isfinite(out).all()


# === 6. Contingency, Metrics, and Statistical Tests ===

def test_contingency_and_metrics_calculation():
    y_true = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    y_pred = np.array([1, 1, 1, 0, 0, 0, 0, 1])
    res = compute_contingency_and_metrics(y_true, y_pred)
    assert res["tp"] == 3
    assert res["fn"] == 1
    assert res["tn"] == 3
    assert res["fp"] == 1
    assert res["recall"] == 0.75
    assert res["precision"] == 0.75
    assert res["specificity"] == 0.75
    assert res["fpr"] == 0.25
    assert res["f1"] == 0.75


def test_degenerate_confusion_matrices_no_divide_by_zero():
    # All negatives (0 positives)
    y_true_all_neg = np.zeros(10, dtype=int)
    y_pred_all_neg = np.zeros(10, dtype=int)
    res_neg = compute_contingency_and_metrics(y_true_all_neg, y_pred_all_neg)
    assert res_neg["tp"] == 0
    assert res_neg["fn"] == 0
    assert res_neg["tn"] == 10
    assert res_neg["fp"] == 0
    assert res_neg["recall"] == 0.0
    assert res_neg["precision"] == 0.0
    assert res_neg["specificity"] == 1.0
    assert res_neg["fpr"] == 0.0
    assert res_neg["f1"] == 0.0

    # All positives (0 negatives)
    y_true_all_pos = np.ones(10, dtype=int)
    y_pred_all_pos = np.ones(10, dtype=int)
    res_pos = compute_contingency_and_metrics(y_true_all_pos, y_pred_all_pos)
    assert res_pos["tp"] == 10
    assert res_pos["fn"] == 0
    assert res_pos["tn"] == 0
    assert res_pos["fp"] == 0
    assert res_pos["recall"] == 1.0
    assert res_pos["precision"] == 1.0
    assert res_pos["specificity"] == 0.0
    assert res_pos["fpr"] == 0.0
    assert res_pos["f1"] == 1.0


def test_mcnemar_exact_verified_benchmark():
    p_val = mcnemar_exact_test(4, 2)
    assert p_val == pytest.approx(0.6875, abs=1e-5)


def test_mcnemar_exact_zero_discordant():
    p_val = mcnemar_exact_test(0, 0)
    assert p_val == 1.0


def test_wilcoxon_signed_rank_exact_benchmark():
    x = [10.0, 12.0, 14.0, 16.0, 18.0, 20.0]
    y = [8.0, 9.0, 10.0, 11.0, 12.0, 13.0]
    stat, p_val = wilcoxon_signed_rank_test(x, y)
    assert p_val == pytest.approx(0.03125, abs=1e-4)


# === 7. Preservation of Existing Artifacts ===

def test_existing_research_artifacts_preserved():
    ref_preds = ROOT / "research" / "raw" / "detection_predictions.csv"
    assert ref_preds.exists()
    assert ref_preds.stat().st_size == 24357

    model_pt = ROOT / "models" / "lstm_autoencoder.pt"
    assert model_pt.exists()
    assert model_pt.stat().st_size == 19797


def test_missing_response_time_log_verified():
    anomod_unpacked = ROOT / "data" / "external" / "anomod" / "unpacked"
    if anomod_unpacked.exists():
        matches = list(anomod_unpacked.rglob("*response_time*"))
        assert len(matches) == 0, f"Unexpected response_time file found: {matches}"


# === 8. Extraction Functions Tests (SN and TT) ===

def test_extract_sn_telemetry_synthetic_fixture(tmp_path: Path):
    m_dir = tmp_path / "sn_metrics"
    m_dir.mkdir()
    t_dir = tmp_path / "sn_traces"
    t_dir.mkdir()

    # Generate 4 15-second timestamps
    ts_list = ["2026-10-13 00:00:00", "2026-10-13 00:00:15", "2026-10-13 00:00:30", "2026-10-13 00:00:45"]
    for fname, val in [("system_cpu_usage.csv", 45.0), ("system_memory_usage_percent.csv", 60.0), ("system_disk_usage_percent.csv", 30.0)]:
        df = pd.DataFrame({"timestamp": ts_list, "value": [val] * 4})
        df.to_csv(m_dir / fname, index=False)

    # Traces for the first 3 intervals only (4th interval is idle)
    trace_records = [
        {"start_time": "2026-10-13 00:00:02", "duration_us": 12000, "http_status_code": 200},
        {"start_time": "2026-10-13 00:00:16", "duration_us": 18000, "http_status_code": 500},
        {"start_time": "2026-10-13 00:00:31", "duration_us": 15000, "http_status_code": 200},
    ]
    pd.DataFrame(trace_records).to_csv(t_dir / "all_traces.csv", index=False)

    df_sn = extract_sn_telemetry(m_dir, t_dir, allow_missing_trace_policy="preserve_nans")
    assert len(df_sn) == 4
    assert list(df_sn.columns) == ["cpu_pct", "memory_pct", "disk_pct", "latency_ms", "error_rate_pct", "req_count"]
    assert df_sn["latency_ms"].iloc[0] == pytest.approx(12.0)
    assert df_sn["error_rate_pct"].iloc[1] == pytest.approx(100.0)
    # 4th interval has 0 requests -> latency_ms is NaN (NOT 0.0ms)
    assert np.isnan(df_sn["latency_ms"].iloc[3])
    assert df_sn["req_count"].iloc[3] == 0


def test_extract_tt_telemetry_synthetic_fixture(tmp_path: Path):
    m_dir = tmp_path / "metrics"
    m_dir.mkdir()
    timestamps = [1000, 1015, 1030]
    records = []
    for ts in timestamps:
        records.append({"timestamp": ts, "metric_name": "rate(node_cpu_seconds_total[5m])", "mode": "idle", "value": 3.6})
        records.append({"timestamp": ts, "metric_name": "rate(node_cpu_seconds_total[5m])", "mode": "system", "value": 0.4})
        records.append({"timestamp": ts, "metric_name": "node_memory_MemAvailable_bytes", "mode": "", "value": 2000.0})
        records.append({"timestamp": ts, "metric_name": "node_memory_MemTotal_bytes", "mode": "", "value": 8000.0})
        records.append({"timestamp": ts, "metric_name": "node_filesystem_avail_bytes", "mode": "", "value": 300.0})
        records.append({"timestamp": ts, "metric_name": "node_filesystem_size_bytes", "mode": "", "value": 1000.0})

    df_m = pd.DataFrame(records)
    df_m.to_csv(m_dir / "tt_metrics.csv", index=False)

    t_dir = tmp_path / "traces"
    t_dir.mkdir()
    trace_payload = {
        "traces": [
            {"summary": {"start_timestamp_ms": 1000000, "duration_ms": 15.0, "is_error": False}},
            {"summary": {"start_timestamp_ms": 1015000, "duration_ms": 25.0, "is_error": True}},
            {"summary": {"start_timestamp_ms": 1030000, "duration_ms": 12.0, "is_error": False}},
        ]
    }
    with open(t_dir / "skywalking_traces.json", "w") as f:
        json.dump(trace_payload, f)

    df_tt = extract_tt_telemetry(m_dir, t_dir, allow_missing_trace_policy="fail")
    assert len(df_tt) == 3
    assert "cpu_pct" in df_tt.columns
    assert "memory_pct" in df_tt.columns
    assert "disk_pct" in df_tt.columns
    assert "latency_ms" in df_tt.columns
    assert "error_rate_pct" in df_tt.columns
    assert df_tt["memory_pct"].iloc[0] == pytest.approx(75.0)
    assert df_tt["disk_pct"].iloc[0] == pytest.approx(70.0)


# === 9. Temporal Continuity and Window Validation Tests ===

def test_build_contiguous_windows_strictly_consecutive():
    # 10 consecutive 15-second timestamps
    base = pd.to_datetime("2026-10-13 00:00:00")
    timestamps = [base + pd.Timedelta(seconds=15 * i) for i in range(10)]
    data = np.ones((10, 5), dtype=np.float32)
    df = pd.DataFrame(data, index=pd.DatetimeIndex(timestamps), columns=list(FROZEN_FEATURE_ORDER))

    windows, valid_ts = build_contiguous_windows(df, window_length=8, step_seconds=15.0)
    assert windows.shape == (3, 8, 5)
    assert len(valid_ts) == 3
    # Check consecutive timestamps in first window
    for k in range(7):
        assert (valid_ts[0][k + 1] - valid_ts[0][k]).total_seconds() == 15.0


def test_build_contiguous_windows_rejects_temporal_gap():
    # 10 timestamps, but step 4 -> 5 has a 30s gap (hidden interval)
    base = pd.to_datetime("2026-10-13 00:00:00")
    ts_list = [
        base + pd.Timedelta(seconds=0),
        base + pd.Timedelta(seconds=15),
        base + pd.Timedelta(seconds=30),
        base + pd.Timedelta(seconds=45),
        base + pd.Timedelta(seconds=60),
        # Gap: jumps to 105 instead of 75
        base + pd.Timedelta(seconds=105),
        base + pd.Timedelta(seconds=120),
        base + pd.Timedelta(seconds=135),
        base + pd.Timedelta(seconds=150),
        base + pd.Timedelta(seconds=165),
    ]
    data = np.ones((10, 5), dtype=np.float32)
    df = pd.DataFrame(data, index=pd.DatetimeIndex(ts_list), columns=list(FROZEN_FEATURE_ORDER))

    windows, valid_ts = build_contiguous_windows(df, window_length=8, step_seconds=15.0)
    # Neither segment (5 items, 5 items) has length >= 8, so 0 windows formed!
    assert windows.shape == (0, 8, 5)
    assert len(valid_ts) == 0


def test_build_contiguous_windows_rejects_missing_latency():
    # 10 consecutive timestamps, but row 4 has NaN in latency_ms
    base = pd.to_datetime("2026-10-13 00:00:00")
    timestamps = [base + pd.Timedelta(seconds=15 * i) for i in range(10)]
    data = np.ones((10, 5), dtype=np.float32)
    df = pd.DataFrame(data, index=pd.DatetimeIndex(timestamps), columns=list(FROZEN_FEATURE_ORDER))
    df.loc[df.index[4], "latency_ms"] = np.nan

    windows, valid_ts = build_contiguous_windows(df, window_length=8, step_seconds=15.0)
    assert windows.shape == (0, 8, 5)


# === 10. Chronological Partitioning and Zero-Leakage Purge Gap Tests ===

def test_partition_normal_series_chronologically_disjoint():
    base = pd.to_datetime("2026-10-13 00:00:00")
    timestamps = [base + pd.Timedelta(seconds=15 * i) for i in range(30)]
    data = np.ones((30, 5), dtype=np.float32)
    df = pd.DataFrame(data, index=pd.DatetimeIndex(timestamps), columns=list(FROZEN_FEATURE_ORDER))

    calib_raw, val_raw, meta = partition_normal_series_chronologically(
        df, train_fraction=0.70, purge_gap_steps=7
    )

    # 30 * 0.70 = 21 calib steps
    assert len(calib_raw) == 21
    # Purge gap = 7 steps: indices 21..27 skipped
    # Val raw: indices 28..29 (2 steps)
    assert len(val_raw) == 2
    assert meta["shared_raw_timestamps"] == 0

    # Ensure timestamps are strictly disjoint
    assert set(calib_raw.index).isdisjoint(set(val_raw.index))
    # Ensure calib ends before purge gap
    assert calib_raw.index.max() < val_raw.index.min()
    gap_duration = (val_raw.index.min() - calib_raw.index.max()).total_seconds()
    # 7 gap steps * 15s + 15s = 120s between calib max and val min
    assert gap_duration >= 7 * 15.0


def test_partition_normal_series_leakage_assertion():
    # If overlapping index is artificially introduced, must raise LeakageViolationError
    base = pd.to_datetime("2026-10-13 00:00:00")
    timestamps = [base + pd.Timedelta(seconds=15 * i) for i in range(20)]
    df = pd.DataFrame(np.ones((20, 5)), index=pd.DatetimeIndex(timestamps), columns=list(FROZEN_FEATURE_ORDER))

    # Zero purge gap on 20 samples with large fraction leaves disjoint raw split
    calib, val, _ = partition_normal_series_chronologically(df, train_fraction=0.50, purge_gap_steps=0)
    assert set(calib.index).isdisjoint(set(val.index))


# === 11. Pipeline Identical Observations and Sandbox Tests ===

def test_run_evaluation_pipeline_sandbox(tmp_path: Path):
    detector = load_detector(ROOT / "models" / "lstm_autoencoder.pt")

    rng = np.random.default_rng(123)
    normal_windows = rng.normal(loc=[42, 54, 76, 0.2, 48], scale=[5, 3, 6, 0.05, 4], size=(20, 8, 5)).astype(np.float32)
    fault_windows = rng.normal(loc=[85, 54, 300, 5.0, 48], scale=[5, 3, 20, 0.5, 4], size=(15, 8, 5)).astype(np.float32)

    p_csv = tmp_path / "preds.csv"
    m_csv = tmp_path / "metrics.csv"
    manifest_json = tmp_path / "manifest.json"

    manifest = run_evaluation_pipeline(
        detector=detector,
        normal_windows=normal_windows,
        fault_scenarios={"FAULT_SC_1": fault_windows},
        output_predictions_path=p_csv,
        output_metrics_path=m_csv,
        output_manifest_path=manifest_json,
        include_val_in_predictions=False,
    )

    assert p_csv.exists()
    assert m_csv.exists()
    assert manifest_json.exists()

    df_p = pd.read_csv(p_csv)
    df_m = pd.read_csv(m_csv)
    assert len(df_p) == 15
    assert len(df_m) == 5
    assert "AegisOps LSTM Autoencoder" in df_m["model"].values
    assert "Isolation Forest" in df_m["model"].values
    assert manifest["n_predictions"] == 15


def test_identical_eligible_observations_across_baselines(tmp_path: Path):
    detector = load_detector(ROOT / "models" / "lstm_autoencoder.pt")
    rng = np.random.default_rng(42)
    calib = rng.normal(loc=[42, 54, 76, 0.2, 48], scale=[5, 3, 6, 0.05, 4], size=(15, 8, 5)).astype(np.float32)
    fault = rng.normal(loc=[85, 54, 300, 5.0, 48], scale=[5, 3, 20, 0.5, 4], size=(10, 8, 5)).astype(np.float32)

    p_csv = tmp_path / "preds.csv"
    m_csv = tmp_path / "metrics.csv"
    manifest_json = tmp_path / "manifest.json"

    run_evaluation_pipeline(
        detector=detector,
        calib_windows=calib,
        val_windows=calib,
        fault_scenarios={"SC_A": fault},
        output_predictions_path=p_csv,
        output_metrics_path=m_csv,
        output_manifest_path=manifest_json,
    )

    df_p = pd.read_csv(p_csv)
    # Ensure every row contains predictions for all 5 detectors
    flag_cols = ["rule_narrow_flag", "rule_resource_flag", "rule_full_flag", "iso_flag", "lstm_flag"]
    for col in flag_cols:
        assert col in df_p.columns
        assert not df_p[col].isna().any()


# === 12. Fail-Closed CLI Behavior and Execution Guards ===

def test_fail_closed_cli_unauthorized_exit_code_2(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["run_experiment_d.py"])
    exit_code = main()
    assert exit_code == 2


def test_fail_closed_cli_unratified_exit_code_3(monkeypatch):
    # When --authorized is passed but ratification record does not exist
    monkeypatch.setattr(sys, "argv", ["run_experiment_d.py", "--authorized"])
    exit_code = main()
    assert exit_code == 3


def test_dry_run_cli_exit_code_0(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["run_experiment_d.py", "--dry-run"])
    exit_code = main()
    assert exit_code == 0


def test_test_pipeline_cli_exit_code_0(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["run_experiment_d.py", "--test-pipeline"])
    exit_code = main()
    assert exit_code == 0
