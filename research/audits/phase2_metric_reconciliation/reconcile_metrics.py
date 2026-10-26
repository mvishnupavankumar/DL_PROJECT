#!/usr/bin/env python3
"""Read-only AegisOps Phase 2 metric reconciliation.

Usage from repository root:
  .venv\Scripts\python.exe research\audits\phase2_metric_reconciliation\reconcile_metrics.py

The program reads only the Phase-2 inputs and emits JSON to stdout. It neither
executes an experiment nor changes a source artifact. Redirect stdout only if a
separate audit record is desired.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[3]
INPUTS = {
    "detection_predictions": "research/raw/detection_predictions.csv",
    "detection_metrics": "research/raw/detection_metrics.csv",
    "detection_by_scenario": "research/raw/detection_by_scenario.csv",
    "diagnosis_predictions": "research/raw/diagnosis_predictions.csv",
    "diagnosis_metrics": "research/raw/diagnosis_metrics.csv",
    "safety_test_results": "research/raw/safety_test_results.csv",
    "safety_metrics": "research/raw/safety_metrics.csv",
    "statistical_analysis": "research/results/statistical_analysis.md",
    "canonical_reconciliation": "research/paper/CANONICAL_METRIC_RECONCILIATION.md",
    "live_data_audit": "research/exports/LIVE_DATA_AND_EXTERNAL_VALIDATION_AUDIT.md",
    "telemetry": "research/exports/telemetry.csv",
    "frozen_model_metadata": "models/lstm_autoencoder.json",
}

# Values captured by Phase 1 for the same frozen inputs.
PHASE1_SHA256 = {
    "detection_predictions": "246e14f8b84b8b89cbfce180fd7722ae82820f516894aa5dd11462866d10cfbb",
    "detection_metrics": "ed5775303f74156d844dc0068db4328e2237fc935a2bca260d613571083de57e",
    "detection_by_scenario": "7bc8400653683465f8f25af7d60398ae892831b4b3038ac5b7933478103bebf9",
    "diagnosis_predictions": "d43e43370349a1d005cd7de14aa1488486780fc459c2f796559241137b7d1a68",
    "diagnosis_metrics": "79bf2f53fb0de1c6d24afcb88b475e48c78e8cedd27d45ac051d948d505fc307",
    "safety_test_results": "19391636c705166981b56120835b2b0a0b12218defaeffc899474acb8f220985",
    "safety_metrics": "08145f57939c33f8b3db4b017e0833cbfda84a5678f13c54a837ff1335ec0b9a",
    "statistical_analysis": "fe401d2a1dd1f28636cb2f1a64198b232f46f72ff215b14e4a29c48cb8108d74",
    "canonical_reconciliation": "d3f1509152e56dc0c446275bac1d20f9210e430c4e2564d62dc6ed1ebd791cff",
    "live_data_audit": "c5928b43b3de2527a8b0b758d011583ac75542c27873b07a6773a0b44d876832",
    "telemetry": "0a17468699ad918ffcd98af2d77982e7283206d73de3f5d838b0347db6c493a5",
    "frozen_model_metadata": "24826b053833b08e80fb84e7e694adfad5b4a1124d935ccf3e3cd4f575eb045f",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def rate_metrics(tp: int, fp: int, tn: int, fn: int) -> dict[str, float | int]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    specificity = tn / (tn + fp) if tn + fp else 0.0
    fpr = fp / (fp + tn) if fp + tn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "precision": precision,
            "recall": recall, "f1": f1, "specificity": specificity, "fpr": fpr}


def pr_metrics(labels: list[int], scores: list[float]) -> dict[str, float]:
    """Trapezoidal PR-AUC and AP, both explicitly defined over score thresholds."""
    points = [(0.0, 1.0)]  # recall, precision convention at threshold above max
    for threshold in sorted(set(scores), reverse=True):
        predicted = [score >= threshold for score in scores]
        tp = sum(flag and label == 1 for flag, label in zip(predicted, labels))
        fp = sum(flag and label == 0 for flag, label in zip(predicted, labels))
        total_positive = sum(labels)
        points.append((tp / total_positive if total_positive else 0.0, tp / (tp + fp) if tp + fp else 1.0))
    auc = 0.0
    ap = 0.0
    last_recall, last_precision = points[0]
    for recall, precision in points[1:]:
        auc += (recall - last_recall) * (precision + last_precision) / 2
        ap += (recall - last_recall) * precision
        last_recall, last_precision = recall, precision
    return {"trapezoidal_pr_auc": auc, "average_precision": ap}


def wilson(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total == 0:
        return (math.nan, math.nan)
    p = successes / total
    denominator = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denominator
    radius = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return (centre - radius, centre + radius)


def reconcile_detection() -> dict:
    data = rows(INPUTS["detection_predictions"])
    labels = [int(row["ground_truth"]) for row in data]
    output = {
        "sample_count": len(data),
        "class_counts": dict(Counter(labels)),
        "scenario_counts": dict(Counter(row["scenario"] for row in data)),
        "detectors": {},
    }
    specs = {
        "rules": ("rule_flag", "rule_score", False),
        "isolation_forest": ("iso_flag", "iso_score", True),
        "lstm": ("lstm_flag", "lstm_score", True),
        "combined": ("combined_flag", None, False),
    }
    for name, (flag_col, score_col, continuous) in specs.items():
        flags = [int(row[flag_col]) for row in data]
        tp = sum(flag == 1 and label == 1 for flag, label in zip(flags, labels))
        fp = sum(flag == 1 and label == 0 for flag, label in zip(flags, labels))
        tn = sum(flag == 0 and label == 0 for flag, label in zip(flags, labels))
        fn = sum(flag == 0 and label == 1 for flag, label in zip(flags, labels))
        metrics = rate_metrics(tp, fp, tn, fn)
        if continuous and score_col:
            metrics.update(pr_metrics(labels, [float(row[score_col]) for row in data]))
        else:
            metrics["trapezoidal_pr_auc"] = None
            metrics["average_precision"] = None
        output["detectors"][name] = metrics

    lstm_flags = [int(row["lstm_flag"]) for row in data]
    iso_flags = [int(row["iso_flag"]) for row in data]
    fault_pairs = [(l, i) for l, i, label in zip(lstm_flags, iso_flags, labels) if label == 1]
    b = sum(l == 1 and i == 0 for l, i in fault_pairs)
    c = sum(l == 0 and i == 1 for l, i in fault_pairs)
    output["mcnemar_fault_windows"] = {
        "n": len(fault_pairs), "lstm_only": b, "isolation_forest_only": c,
        "exact_two_sided_p": 2 * (0.5 ** (b + c)) if b + c else 1.0,
    }
    scenario = defaultdict(list)
    for row in data:
        if int(row["ground_truth"]) == 1:
            scenario[row["scenario"]].append((int(row["lstm_flag"]), int(row["iso_flag"])))
    scenario_rows = []
    for key in sorted(scenario):
        pairs = scenario[key]
        scenario_rows.append({"scenario": key, "n": len(pairs),
                              "lstm_recall": sum(x for x, _ in pairs) / len(pairs),
                              "isolation_forest_recall": sum(y for _, y in pairs) / len(pairs)})
    output["scenario_recall"] = scenario_rows
    output["wilcoxon_reproducibility"] = {
        "n_scenarios": len(scenario_rows), "all_six_differences_positive": all(
            r["lstm_recall"] > r["isolation_forest_recall"] for r in scenario_rows),
        "negative_rank_sum": 0.0,
        "exact_two_sided_p_if_all_positive": 2 * (0.5 ** len(scenario_rows)),
        "note": "With six nonzero same-direction scenario differences, W-=0 and the sign-pattern exact two-sided probability is 0.03125. This is not evidence of production generalization.",
    }
    return output


def reconcile_diagnosis() -> dict:
    data = rows(INPUTS["diagnosis_predictions"])
    by_config: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in data:
        by_config[row["configuration"]].append(row)
    result = []
    for configuration, group in by_config.items():
        completed = [row for row in group if row["rubric_verdict"] != "UNASSESSABLE"]
        # Omitted API calls are excluded through ``completed``. A zero-duration
        # completed deterministic call remains an observed timing, not missing data.
        timings = [float(row["latency_ms"]) for row in completed]
        strict_total = sum(int(row["top1_strict"]) for row in group)
        strict_completed = sum(int(row["top1_strict"]) for row in completed)
        lenient_total = sum(int(row["top1_lenient"]) for row in group)
        lenient_completed = sum(int(row["top1_lenient"]) for row in completed)
        result.append({
            "configuration": configuration, "execution_mode": group[0]["execution_mode"],
            "intended_denominator": len(group), "completed_denominator": len(completed),
            "unassessable": len(group) - len(completed),
            "strict_itt": f"{strict_total}/{len(group)}", "strict_completed_case": f"{strict_completed}/{len(completed)}",
            "lenient_itt": f"{lenient_total}/{len(group)}", "lenient_completed_case": f"{lenient_completed}/{len(completed)}",
            "mean_completed_latency_ms": mean(timings) if timings else None,
        })
    return {"configurations": result, "scenario_count": len(set(row["incident_id"] for row in data)),
            "cost_or_token_measurement": "not present in raw records"}


def reconcile_safety() -> dict:
    data = rows(INPUTS["safety_test_results"])
    by_type = Counter(row["case_type"] for row in data)
    attacks = [row for row in data if row["case_type"] == "ATTACK_CASE"]
    latencies = [float(row["latency_ms"]) for row in attacks]
    passed = sum(row["verdict"] == "PASS" for row in attacks)
    audit_complete = sum(row["audit_trail_verified"] == "1" for row in data)
    return {
        "total": len(data), "categories": dict(by_type), "attack_containment": f"{passed}/{len(attacks)}",
        "attack_wilson_95": wilson(passed, len(attacks)),
        "attack_mean_latency_ms": mean(latencies), "audit_completeness": f"{audit_complete}/{len(data)}",
        "audit_wilson_95": wilson(audit_complete, len(data)),
    }


def reconcile_live() -> dict:
    data = rows(INPUTS["telemetry"])
    timestamps = [datetime.fromisoformat(row["timestamp"]) for row in data]
    gaps = [(later - earlier).total_seconds() for earlier, later in zip(timestamps, timestamps[1:])]
    return {
        "records": len(data), "detector_modes": dict(Counter(row["detector_mode"] for row in data)),
        "null_anomaly_scores": sum(not row["anomaly_score"].strip() for row in data),
        "fault_modes": dict(Counter(row["fault_mode"] for row in data)),
        "timestamp_gap_seconds": {"minimum": min(gaps), "maximum": max(gaps),
                                  "over_60_seconds": sum(gap > 60 for gap in gaps)},
    }


def reconcile_experiment_d() -> dict:
    metadata = json.loads((ROOT / INPUTS["frozen_model_metadata"]).read_text(encoding="utf-8"))
    outputs = [
        "research/raw/external_anomod_predictions.csv", "research/raw/external_anomod_metrics.csv",
        "research/audits/EXPERIMENT_D_RESULTS.md", "research/audits/experiment_d_manifest.json",
        "research/audits/PROTOCOL_AMENDMENT_V1_2_RATIFICATION.json",
    ]
    return {"frozen_sequence_length": metadata["sequence_length"],
            "frozen_threshold": metadata["threshold"],
            "expected_production_artifacts": {str(p): (ROOT / p).exists() for p in outputs}}


def main() -> None:
    hashes = {name: sha256(ROOT / path) for name, path in INPUTS.items()}
    changed = {name: {"phase1": PHASE1_SHA256[name], "current": value}
               for name, value in hashes.items() if value != PHASE1_SHA256[name]}
    output = {"root": str(ROOT), "phase1_hashes_match": not changed, "changed_inputs": changed,
              "input_hashes": hashes, "experiment_a": reconcile_detection(),
              "experiment_b": reconcile_diagnosis(), "experiment_c": reconcile_safety(),
              "live_telemetry": reconcile_live(), "experiment_d": reconcile_experiment_d()}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
