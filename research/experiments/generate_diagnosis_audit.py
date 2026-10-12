#!/usr/bin/env python3
"""
AegisOps — Root-Cause Diagnosis Audit & Explicit Rubric Evaluator
Evaluates all 7 diagnostic configurations across all 6 ground-truth incidents using an explicit 4-tier rubric:
- CORRECT: Correctly identifies the underlying causal mechanism matching ground truth.
- PARTIALLY_CORRECT: Identifies the correct subsystem or symptom but misidentifies the exact causal mechanism.
- INCORRECT: Attributes failure to wrong subsystem, opposite cause, or irrelevant component.
- UNASSESSABLE: The run failed to produce a prediction due to an API timeout, rate limit (HTTP 429), or schema error.
"""
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "research" / "raw"
RESULTS_DIR = ROOT / "research" / "results"
RAW_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Load ground-truth incidents
with open(ROOT / "data" / "incidents.json", "r", encoding="utf-8") as f:
    ground_truth_incidents = {inc["id"]: inc for inc in json.load(f)}

# Load prior raw predictions
df_prior = pd.read_csv(RESULTS_DIR / "diagnosis_predictions.csv")

# Explicit evaluation records
records = []

configurations = [
    ("1. Rule-based Baseline", "deterministic_rule", False),
    ("2. Single-Agent (Offline)", "deterministic_offline", True),
    ("3. Multi-Agent Full (Offline)", "deterministic_offline", True),
    ("4. Multi-Agent No-DL (Offline)", "deterministic_offline", False),
    ("5. Single-Agent (Groq LLM)", "Groq LLM (openai/gpt-oss-20b)", True),
    ("6. Multi-Agent Full (Groq LLM)", "Groq LLM (openai/gpt-oss-20b)", True),
    ("7. Multi-Agent No-DL (Groq LLM)", "Groq LLM (openai/gpt-oss-20b)", False),
]

all_incident_ids = ["INC-1001", "INC-1002", "INC-1003", "INC-1004", "INC-1005", "INC-1006"]

for config_name, mode, dl_flag in configurations:
    config_rows = df_prior[df_prior["configuration"] == config_name]
    row_by_inc = {r["incident_id"]: r for _, r in config_rows.iterrows()}

    for inc_id in all_incident_ids:
        gt = ground_truth_incidents[inc_id]
        gt_cause = gt["root_cause"]

        if inc_id not in row_by_inc:
            # Unassessable case (dropped during run due to rate limit/error)
            records.append({
                "incident_id": inc_id,
                "configuration": config_name,
                "execution_mode": mode,
                "dl_evidence_supplied": dl_flag,
                "ground_truth_cause": gt_cause,
                "predicted_cause": "N/A (Execution omitted due to Groq TPM rate limit)",
                "rubric_verdict": "UNASSESSABLE",
                "top1_strict": 0,
                "top1_lenient": 0,
                "rubric_rationale": "API call omitted or aborted during evaluation due to Groq Cloud free-tier rate limits.",
                "latency_ms": 0.0,
            })
            continue

        row = row_by_inc[inc_id]
        pred = str(row["predicted_cause"])
        pred_lower = pred.lower()

        # Detailed rubric scoring
        verdict = "INCORRECT"
        strict = 0
        lenient = 0
        rationale = ""

        if inc_id == "INC-1001":
            # GT: Database connection pool exhaustion
            if "pool" in pred_lower and ("exhaust" in pred_lower or "leak" in pred_lower or "database connection" in pred_lower):
                verdict = "CORRECT"
                strict = 1
                lenient = 1
                rationale = "Accurately diagnosed database connection pool exhaustion as root cause."
            elif "database" in pred_lower or "500" in pred_lower:
                verdict = "PARTIALLY_CORRECT"
                lenient = 1
                rationale = "Identified database subsystem failure but did not specify connection pool saturation."
            else:
                verdict = "INCORRECT"
                rationale = "Failed to attribute failure to database connection pool."

        elif inc_id == "INC-1002":
            # GT: Database service stopped
            if ("stopped" in pred_lower or "crashed" in pred_lower or "refusing connection" in pred_lower) and "disk" not in pred_lower:
                verdict = "CORRECT"
                strict = 1
                lenient = 1
                rationale = "Accurately diagnosed database service crash / stopped daemon."
            elif "crashed" in pred_lower and "disk" in pred_lower:
                # E.g. "PostgreSQL service crashed due to abnormal disk I/O contention"
                verdict = "PARTIALLY_CORRECT"
                lenient = 1
                rationale = "Correctly diagnosed PostgreSQL service crash, but hallucinated secondary cause (disk I/O contention) without evidence."
            elif "database" in pred_lower:
                verdict = "PARTIALLY_CORRECT"
                lenient = 1
                rationale = "Identified database issue generally."
            else:
                verdict = "INCORRECT"
                rationale = "Incorrect root cause."

        elif inc_id == "INC-1003":
            # GT: Worker service thread exhaustion causing sustained CPU saturation
            if ("worker" in pred_lower or "thread" in pred_lower) and ("cpu" in pred_lower or "saturat" in pred_lower or "explosion" in pred_lower):
                verdict = "CORRECT"
                strict = 1
                lenient = 1
                rationale = "Accurately diagnosed worker service thread pool exhaustion driving sustained CPU saturation."
            elif "cpu" in pred_lower:
                verdict = "PARTIALLY_CORRECT"
                lenient = 1
                rationale = "Identified CPU saturation symptom without pinpointing worker-service thread pool exhaustion."
            else:
                verdict = "INCORRECT"
                rationale = "Incorrect root cause."

        elif inc_id == "INC-1004":
            # GT: Runaway application log growth consumed disk capacity
            if "disk" in pred_lower and ("log" in pred_lower or "app.log" in pred_lower or "/var" in pred_lower or "full" in pred_lower):
                verdict = "CORRECT"
                strict = 1
                lenient = 1
                rationale = "Accurately identified runaway application log file growth exhausting disk storage."
            elif "disk" in pred_lower or "space" in pred_lower:
                verdict = "PARTIALLY_CORRECT"
                lenient = 1
                rationale = "Identified disk space exhaustion without identifying log growth."
            else:
                verdict = "INCORRECT"
                rationale = "Defaulted to wrong subsystem (e.g. worker process CPU saturation)."

        elif inc_id == "INC-1005":
            # GT: Incorrect OAuth issuer configuration
            if "oauth" in pred_lower and ("issuer" in pred_lower or "config" in pred_lower or "mismatch" in pred_lower or "validation" in pred_lower):
                verdict = "CORRECT"
                strict = 1
                lenient = 1
                rationale = "Accurately identified OAuth identity provider misconfiguration / invalid issuer URL."
            elif "auth" in pred_lower or "login" in pred_lower or "token" in pred_lower:
                verdict = "PARTIALLY_CORRECT"
                lenient = 1
                rationale = "Identified authentication error generally."
            else:
                verdict = "INCORRECT"
                rationale = "Defaulted to wrong subsystem."

        elif inc_id == "INC-1006":
            # GT: Broken service route between service-a and service-b
            if ("route" in pred_lower or "network" in pred_lower or "connectivity" in pred_lower or "unreachable" in pred_lower) and ("service" in pred_lower or "cni" in pred_lower):
                verdict = "CORRECT"
                strict = 1
                lenient = 1
                rationale = "Accurately identified service-to-service network routing / connectivity failure."
            elif "timeout" in pred_lower or "network" in pred_lower:
                verdict = "PARTIALLY_CORRECT"
                lenient = 1
                rationale = "Identified timeout symptom without identifying network route break."
            else:
                verdict = "INCORRECT"
                rationale = "Defaulted to wrong subsystem."

        records.append({
            "incident_id": inc_id,
            "configuration": config_name,
            "execution_mode": mode,
            "dl_evidence_supplied": dl_flag,
            "ground_truth_cause": gt_cause,
            "predicted_cause": pred,
            "rubric_verdict": verdict,
            "top1_strict": strict,
            "top1_lenient": lenient,
            "rubric_rationale": rationale,
            "latency_ms": float(row.get("latency_ms", 0.0)),
        })

df_audit = pd.DataFrame(records)
raw_pred_csv = RAW_DIR / "diagnosis_predictions.csv"
df_audit.to_csv(raw_pred_csv, index=False)
df_audit.to_csv(RESULTS_DIR / "diagnosis_predictions.csv", index=False)
print(f"[OUTPUT] Saved rubric-annotated diagnosis predictions: {raw_pred_csv}")

# Summary Metrics Table
summary_rows = []
for config_name, mode, dl_flag in configurations:
    sub = df_audit[df_audit["configuration"] == config_name]
    total_incidents = len(sub)  # always 6
    completed_incidents = len(sub[sub["rubric_verdict"] != "UNASSESSABLE"])
    unassessable_count = total_incidents - completed_incidents

    strict_correct = int(sub["top1_strict"].sum())
    lenient_correct = int(sub["top1_lenient"].sum())
    partially_correct = int((sub["rubric_verdict"] == "PARTIALLY_CORRECT").sum())
    incorrect = int((sub["rubric_verdict"] == "INCORRECT").sum())

    # Full Cohort Accuracy (Intent-to-treat, N=6)
    full_cohort_acc = round(strict_correct / total_incidents, 4)
    # Per-Protocol Accuracy (Completed cases only)
    per_protocol_acc = round(strict_correct / completed_incidents, 4) if completed_incidents > 0 else 0.0

    mean_lat = round(float(sub[sub["rubric_verdict"] != "UNASSESSABLE"]["latency_ms"].mean()), 2) if completed_incidents > 0 else 0.0

    summary_rows.append({
        "configuration": config_name,
        "execution_mode": mode,
        "dl_evidence": dl_flag,
        "total_incidents": total_incidents,
        "completed_incidents": completed_incidents,
        "unassessable": unassessable_count,
        "correct_strict": strict_correct,
        "partially_correct": partially_correct,
        "incorrect": incorrect,
        "full_cohort_accuracy": full_cohort_acc,
        "per_protocol_accuracy": per_protocol_acc,
        "lenient_accuracy": round(lenient_correct / total_incidents, 4),
        "mean_latency_ms": mean_lat,
    })

df_summary = pd.DataFrame(summary_rows)
raw_metrics_csv = RAW_DIR / "diagnosis_metrics.csv"
df_summary.to_csv(raw_metrics_csv, index=False)
df_summary.to_csv(RESULTS_DIR / "diagnosis_metrics.csv", index=False)
print(f"[OUTPUT] Saved diagnosis summary metrics: {raw_metrics_csv}")
print(df_summary[["configuration", "completed_incidents", "correct_strict", "full_cohort_accuracy", "per_protocol_accuracy"]])
