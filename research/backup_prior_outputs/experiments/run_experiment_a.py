#!/usr/bin/env python3
"""Experiment A: Anomaly detection benchmark comparing Rules, Isolation Forest, LSTM, and Combined."""
import json
import math
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import torch
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_recall_curve, auc
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

MODELS = ROOT / "models"
RESULTS = ROOT / "research" / "results"
FIGURES = ROOT / "research" / "figures"
EXPERIMENTS = ROOT / "research" / "experiments"

RESULTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)
EXPERIMENTS.mkdir(parents=True, exist_ok=True)

from dl.anomaly_detector import (
    FEATURES, SEQUENCE_LENGTH, HIDDEN_SIZE,
    generate_normal_windows, generate_incident_telemetry,
    TelemetryAnomalyDetector, load_detector
)

def run_experiment_a():
    print("=" * 70)
    print("EXPERIMENT A: ANOMALY DETECTION EVALUATION")
    print("=" * 70)

    # 1. Load frozen LSTM checkpoint
    lstm_detector = load_detector(MODELS / "lstm_autoencoder.pt")
    print(f"Loaded LSTM Autoencoder (Threshold: {lstm_detector.threshold:.6f})")

    # 2. Re-create training and validation partitions
    windows_train_val = generate_normal_windows(n_windows=800, seed=42)
    split_idx = int(800 * 0.85)
    train_windows = windows_train_val[:split_idx]
    val_windows = windows_train_val[split_idx:]

    train_flat = train_windows.reshape(len(train_windows), -1)
    val_flat = val_windows.reshape(len(val_windows), -1)

    # 3. Fit Isolation Forest baseline on identical training partition
    iso_forest = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    iso_forest.fit(train_flat)

    val_iso_scores = -iso_forest.decision_function(val_flat)
    iso_threshold = float(np.quantile(val_iso_scores, 0.99))
    print(f"Calibrated Isolation Forest Threshold (99th pct on val): {iso_threshold:.6f}")

    # 4. Generate Held-Out Test Set (seed=2026)
    n_normal_test = 200
    test_normal_windows = generate_normal_windows(n_windows=n_normal_test, seed=2026)

    incident_ids = [f"INC-{1001 + i}" for i in range(6)]
    replicates_per_scenario = 20
    test_incident_windows = []
    incident_metadata = []

    rep_seed = 3000
    for inc_id in incident_ids:
        for rep in range(replicates_per_scenario):
            rep_seed += 1
            w, label = generate_incident_telemetry(inc_id, seed=rep_seed)
            test_incident_windows.append(w)
            incident_metadata.append({
                "scenario": inc_id,
                "replicate": rep,
                "label": label,
                "fault_onset_step": 16
            })

    test_incident_windows = np.array(test_incident_windows)
    print(f"Held-out test set: {len(test_normal_windows)} normal windows, {len(test_incident_windows)} incident windows")

    # 5. Operational rules baseline
    def evaluate_operational_rules(window: np.ndarray) -> tuple[bool, str]:
        latest = window[-1]
        cpu, mem, lat, err, disk = latest[0], latest[1], latest[2], latest[3], latest[4]
        reasons = []
        if mem >= 95.0: reasons.append("memory_pct >= 95")
        if lat >= 1000.0: reasons.append("latency_ms >= 1000")
        if err > 0.5: reasons.append("error_rate_pct > 0.5")
        if cpu >= 90.0: reasons.append("cpu_pct >= 90")
        if disk >= 95.0: reasons.append("disk_pct >= 95")
        return (len(reasons) > 0, "; ".join(reasons))

    predictions_list = []
    for idx, w in enumerate(test_normal_windows):
        rule_flag, _ = evaluate_operational_rules(w)
        iso_score = float(-iso_forest.decision_function(w.reshape(1, -1))[0])
        iso_flag = iso_score > iso_threshold
        lstm_res = lstm_detector.detect(w)
        lstm_score = float(lstm_res["score"])
        lstm_flag = bool(lstm_res["is_anomaly"])
        combined_flag = rule_flag or lstm_flag
        predictions_list.append({
            "sample_id": f"NORM-{idx+1:03d}",
            "ground_truth": 0,
            "scenario": "NORMAL",
            "rule_flag": int(rule_flag),
            "rule_score": float(rule_flag),
            "iso_flag": int(iso_flag),
            "iso_score": iso_score,
            "lstm_flag": int(lstm_flag),
            "lstm_score": lstm_score,
            "combined_flag": int(combined_flag),
            "delay_steps": np.nan
        })

    for idx, (w, meta) in enumerate(zip(test_incident_windows, incident_metadata)):
        rule_flag, _ = evaluate_operational_rules(w)
        iso_score = float(-iso_forest.decision_function(w.reshape(1, -1))[0])
        iso_flag = iso_score > iso_threshold
        lstm_res = lstm_detector.detect(w)
        lstm_score = float(lstm_res["score"])
        lstm_flag = bool(lstm_res["is_anomaly"])
        combined_flag = rule_flag or lstm_flag
        predictions_list.append({
            "sample_id": f"{meta['scenario']}-REP-{meta['replicate']+1:02d}",
            "ground_truth": 1,
            "scenario": meta["scenario"],
            "rule_flag": int(rule_flag),
            "rule_score": float(rule_flag),
            "iso_flag": int(iso_flag),
            "iso_score": iso_score,
            "lstm_flag": int(lstm_flag),
            "lstm_score": lstm_score,
            "combined_flag": int(combined_flag),
            "delay_steps": 0 if lstm_flag else np.nan
        })

    df_preds = pd.DataFrame(predictions_list)
    preds_path = RESULTS / "detection_predictions.csv"
    df_preds.to_csv(preds_path, index=False)
    print(f"Saved raw test predictions: {preds_path}")

    y_true = df_preds["ground_truth"].values
    methods = [
        ("Operational Rules", "rule_flag", "rule_score"),
        ("Isolation Forest", "iso_flag", "iso_score"),
        ("LSTM Autoencoder (Frozen)", "lstm_flag", "lstm_score"),
        ("Combined Alert (Rules OR LSTM)", "combined_flag", None)
    ]

    metrics_records = []
    for name, flag_col, score_col in methods:
        y_pred = df_preds[flag_col].values
        tp = int(np.sum((y_true == 1) & (y_pred == 1)))
        fp = int(np.sum((y_true == 0) & (y_pred == 1)))
        tn = int(np.sum((y_true == 0) & (y_pred == 0)))
        fn = int(np.sum((y_true == 1) & (y_pred == 0)))
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0

        def wilson_ci(k, n, z=1.96):
            if n == 0: return (0.0, 0.0)
            p = k / n
            denom = 1 + z**2 / n
            center = (p + z**2 / (2 * n)) / denom
            delta = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
            return (max(0.0, center - delta), min(1.0, center + delta))

        prec_ci = wilson_ci(tp, tp + fp)
        rec_ci = wilson_ci(tp, tp + fn)

        pr_auc = np.nan
        if score_col is not None and score_col in df_preds.columns:
            p_curve, r_curve, _ = precision_recall_curve(y_true, df_preds[score_col].values)
            pr_auc = float(auc(r_curve, p_curve))

        fa_rate = fp / len(test_normal_windows)
        fa_per_hour = fa_rate * (3600.0 / 5.0)
        ep_detect_rate = tp / 120.0

        metrics_records.append({
            "method": name,
            "TP": tp, "FP": fp, "TN": tn, "FN": fn,
            "precision": round(prec, 4),
            "precision_ci95_low": round(prec_ci[0], 4),
            "precision_ci95_high": round(prec_ci[1], 4),
            "recall": round(rec, 4),
            "recall_ci95_low": round(rec_ci[0], 4),
            "recall_ci95_high": round(rec_ci[1], 4),
            "f1_score": round(f1, 4),
            "pr_auc": round(pr_auc, 4) if not np.isnan(pr_auc) else "N/A",
            "false_alarm_rate": round(fa_rate, 4),
            "false_alarms_per_hour": round(fa_per_hour, 2),
            "episode_detection_rate": round(ep_detect_rate, 4)
        })

    df_metrics = pd.DataFrame(metrics_records)
    metrics_path = RESULTS / "detection_metrics.csv"
    df_metrics.to_csv(metrics_path, index=False)
    print(f"Saved detection metrics: {metrics_path}")

    # Scenario breakdown
    scenario_records = []
    for sc in incident_ids:
        df_sc = df_preds[df_preds["scenario"] == sc]
        n_sc = len(df_sc)
        scenario_records.append({
            "scenario": sc,
            "n_episodes": n_sc,
            "rule_recall": round(int(df_sc["rule_flag"].sum()) / n_sc, 4),
            "isolation_forest_recall": round(int(df_sc["iso_flag"].sum()) / n_sc, 4),
            "lstm_autoencoder_recall": round(int(df_sc["lstm_flag"].sum()) / n_sc, 4),
            "combined_alert_recall": round(int(df_sc["combined_flag"].sum()) / n_sc, 4)
        })

    df_sc = pd.DataFrame(scenario_records)
    sc_path = RESULTS / "detection_by_scenario.csv"
    df_sc.to_csv(sc_path, index=False)
    print(f"Saved scenario breakdown: {sc_path}")

if __name__ == "__main__":
    run_experiment_a()
