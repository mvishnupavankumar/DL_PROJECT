"""Smoke-evaluate the detector on generated normals and injected fault profiles.

This is a reproducibility check for the synthetic demo, not a real-world benchmark.
"""
import json

import numpy as np

from dl.anomaly_detector import generate_incident_telemetry, generate_normal_windows, load_detector


def main() -> None:
    detector = load_detector()
    normal = generate_normal_windows(n_windows=200, seed=2026)
    y_true = [0] * len(normal)
    windows = [x for x in normal]
    for scenario_index, incident_id in enumerate(
        ["INC-1001", "INC-1002", "INC-1003", "INC-1004", "INC-1005", "INC-1006"]
    ):
        for repeat in range(10):
            window, _ = generate_incident_telemetry(incident_id, seed=300 + scenario_index * 20 + repeat)
            windows.append(window)
            y_true.append(1)

    y_pred = [int(detector.detect(window)["is_anomaly"]) for window in windows]
    tp = sum(t == 1 and p == 1 for t, p in zip(y_true, y_pred))
    tn = sum(t == 0 and p == 0 for t, p in zip(y_true, y_pred))
    fp = sum(t == 0 and p == 1 for t, p in zip(y_true, y_pred))
    fn = sum(t == 1 and p == 0 for t, p in zip(y_true, y_pred))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
    output = {
        "warning": "Synthetic smoke evaluation only; do not report as real-world accuracy.",
        "samples": len(windows),
        "normal_samples": len(normal),
        "injected_fault_samples": len(windows) - len(normal),
        "confusion_matrix": {"true_positive": tp, "true_negative": tn, "false_positive": fp, "false_negative": fn},
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "normal_false_positive_rate": round(fp / len(normal), 4) if len(normal) else 0.0,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
