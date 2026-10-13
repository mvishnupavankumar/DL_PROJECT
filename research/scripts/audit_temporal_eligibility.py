#!/usr/bin/env python3
"""Audit temporal integrity, trace coverage, and eligible sliding windows for AnoMod."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ANOMOD_ROOT = ROOT / "data" / "external" / "anomod" / "unpacked"


def audit_sn_scenario(scenario_name: str) -> Dict[str, Any]:
    metric_dir = ANOMOD_ROOT / "SN_data" / "metric_data" / scenario_name
    # Trace dir has same prefix but _traces_ instead of _metrics_
    trace_name = scenario_name.replace("_metrics_", "_traces_")
    trace_dir = ANOMOD_ROOT / "SN_data" / "trace_data" / trace_name

    cpu_path = metric_dir / "system_cpu_usage.csv"
    mem_path = metric_dir / "system_memory_usage_percent.csv"
    disk_path = metric_dir / "system_disk_usage_percent.csv"
    trace_path = trace_dir / "all_traces.csv"

    if not cpu_path.exists() or not mem_path.exists() or not disk_path.exists():
        return {"scenario": scenario_name, "error": "Missing system metric CSVs"}

    df_cpu = pd.read_csv(cpu_path)
    df_mem = pd.read_csv(mem_path)
    df_disk = pd.read_csv(disk_path)

    df_cpu["dt"] = pd.to_datetime(df_cpu["timestamp"])
    df_mem["dt"] = pd.to_datetime(df_mem["timestamp"])
    df_disk["dt"] = pd.to_datetime(df_disk["timestamp"])

    df_cpu["grid_dt"] = df_cpu["dt"].dt.round("15s")
    df_mem["grid_dt"] = df_mem["dt"].dt.round("15s")
    df_disk["grid_dt"] = df_disk["dt"].dt.round("15s")

    cpu_s = df_cpu.groupby("grid_dt")["value"].mean().rename("cpu_pct")
    mem_s = df_mem.groupby("grid_dt")["value"].mean().rename("memory_pct")
    disk_s = df_disk.groupby("grid_dt")["value"].mean().rename("disk_pct")

    merged = pd.concat([cpu_s, mem_s, disk_s], axis=1, sort=True).sort_index()
    total_grid_intervals = len(merged)
    t_start = merged.index.min()
    t_end = merged.index.max()
    duration_s = (t_end - t_start).total_seconds() if total_grid_intervals > 0 else 0

    trace_exists = trace_path.exists()
    trace_spans_count = 0
    active_intervals = 0
    empty_intervals = total_grid_intervals
    trace_dur_s = 0

    if trace_exists:
        df_tr = pd.read_csv(trace_path, usecols=["start_time", "duration_us", "http_status_code"])
        trace_spans_count = len(df_tr)
        if trace_spans_count > 0:
            df_tr["dt"] = pd.to_datetime(df_tr["start_time"])
            df_tr["grid_dt"] = df_tr["dt"].dt.round("15s")
            t_tr_min = df_tr["dt"].min()
            t_tr_max = df_tr["dt"].max()
            trace_dur_s = (t_tr_max - t_tr_min).total_seconds()

            req_counts = df_tr.groupby("grid_dt").size().rename("req_count")
            merged = merged.join(req_counts)
            merged["req_count"] = merged["req_count"].fillna(0).astype(int)
            active_intervals = int((merged["req_count"] > 0).sum())
            empty_intervals = int((merged["req_count"] == 0).sum())
        else:
            merged["req_count"] = 0
    else:
        merged["req_count"] = 0

    # Calculate contiguous active runs of length W >= 8
    # An active run is consecutive intervals where req_count > 0 AND delta_t == 15s
    eligible_windows = 0
    contiguous_runs = []
    current_run = []

    for idx, (ts, row) in enumerate(merged.iterrows()):
        is_active = (row["req_count"] > 0)
        if is_active:
            if not current_run:
                current_run.append(ts)
            else:
                last_ts = current_run[-1]
                if (ts - last_ts).total_seconds() == 15.0:
                    current_run.append(ts)
                else:
                    if len(current_run) >= 8:
                        contiguous_runs.append(len(current_run))
                        eligible_windows += (len(current_run) - 8 + 1)
                    current_run = [ts]
        else:
            if len(current_run) >= 8:
                contiguous_runs.append(len(current_run))
                eligible_windows += (len(current_run) - 8 + 1)
            current_run = []

    if len(current_run) >= 8:
        contiguous_runs.append(len(current_run))
        eligible_windows += (len(current_run) - 8 + 1)

    return {
        "scenario": scenario_name,
        "cohort": "SocialNetwork",
        "metric_rows": total_grid_intervals,
        "start_time": str(t_start),
        "end_time": str(t_end),
        "duration_seconds": duration_s,
        "trace_spans": trace_spans_count,
        "trace_duration_seconds": trace_dur_s,
        "active_15s_intervals": active_intervals,
        "empty_15s_intervals": empty_intervals,
        "empty_interval_pct": round(empty_intervals / total_grid_intervals * 100.0, 2) if total_grid_intervals > 0 else 0.0,
        "contiguous_active_runs": contiguous_runs,
        "eligible_w8_windows": eligible_windows,
        "is_normal_baseline": ("Normal_Baseline" in scenario_name),
    }


def audit_tt_scenario(scenario_name: str) -> Dict[str, Any]:
    metric_dir = ANOMOD_ROOT / "TT_data" / "metric_data" / scenario_name
    trace_dir = ANOMOD_ROOT / "TT_data" / "trace_data" / scenario_name

    csv_files = list(metric_dir.glob("*.csv"))
    if not csv_files:
        return {"scenario": scenario_name, "error": "Missing metric CSV"}

    df_raw = pd.read_csv(csv_files[0], low_memory=False)
    df_raw["dt"] = pd.to_datetime(df_raw["timestamp"], unit="s")
    df_raw["grid_dt"] = df_raw["dt"].dt.round("15s")
    unique_grid = df_raw["grid_dt"].drop_duplicates().sort_values()

    total_grid_intervals = len(unique_grid)
    t_start = unique_grid.min()
    t_end = unique_grid.max()
    duration_s = (t_end - t_start).total_seconds() if total_grid_intervals > 0 else 0

    trace_files = list(trace_dir.glob("*skywalking_traces*.json")) if trace_dir.exists() else []
    trace_spans_count = 0
    trace_dur_s = 0
    active_intervals = 0
    empty_intervals = total_grid_intervals
    eligible_windows = 0
    contiguous_runs = []

    if trace_files:
        with open(trace_files[0], "r", encoding="utf-8") as f:
            t_data = json.load(f)
        traces = t_data.get("traces", [])
        trace_spans_count = len(traces)
        if trace_spans_count > 0:
            ts_list = [t.get("summary", {}).get("start_timestamp_ms", 0) for t in traces]
            ts_series = pd.to_datetime(ts_list, unit="ms")
            t_tr_min = ts_series.min()
            t_tr_max = ts_series.max()
            trace_dur_s = (t_tr_max - t_tr_min).total_seconds()

            tr_grid = pd.Series(ts_series.round("15s")).value_counts()
            active_ts = set(tr_grid.index)

            # Map onto metric grid
            current_run = []
            for ts in unique_grid:
                if ts in active_ts:
                    if not current_run:
                        current_run.append(ts)
                    else:
                        last_ts = current_run[-1]
                        if (ts - last_ts).total_seconds() == 15.0:
                            current_run.append(ts)
                        else:
                            if len(current_run) >= 8:
                                contiguous_runs.append(len(current_run))
                                eligible_windows += (len(current_run) - 8 + 1)
                            current_run = [ts]
                else:
                    if len(current_run) >= 8:
                        contiguous_runs.append(len(current_run))
                        eligible_windows += (len(current_run) - 8 + 1)
                    current_run = []
            if len(current_run) >= 8:
                contiguous_runs.append(len(current_run))
                eligible_windows += (len(current_run) - 8 + 1)

            active_intervals = sum(1 for ts in unique_grid if ts in active_ts)
            empty_intervals = total_grid_intervals - active_intervals

    return {
        "scenario": scenario_name,
        "cohort": "TrainTicket",
        "metric_rows": total_grid_intervals,
        "start_time": str(t_start),
        "end_time": str(t_end),
        "duration_seconds": duration_s,
        "trace_spans": trace_spans_count,
        "trace_duration_seconds": trace_dur_s,
        "active_15s_intervals": active_intervals,
        "empty_15s_intervals": empty_intervals,
        "empty_interval_pct": round(empty_intervals / total_grid_intervals * 100.0, 2) if total_grid_intervals > 0 else 0.0,
        "contiguous_active_runs": contiguous_runs,
        "eligible_w8_windows": eligible_windows,
        "is_normal_baseline": ("Normal_case" in scenario_name),
    }


def main():
    sn_root = ANOMOD_ROOT / "SN_data" / "metric_data"
    tt_root = ANOMOD_ROOT / "TT_data" / "metric_data"

    sn_scenarios = sorted(os.listdir(sn_root)) if sn_root.exists() else []
    tt_scenarios = sorted(os.listdir(tt_root)) if tt_root.exists() else []

    audit_records = []
    print(f"Auditing {len(sn_scenarios)} SocialNetwork scenarios...")
    for s in sn_scenarios:
        res = audit_sn_scenario(s)
        audit_records.append(res)
        print(f"  SN: {s[:35]} | metric_int={res['metric_rows']} | act={res['active_15s_intervals']} | empty={res['empty_15s_intervals']} ({res['empty_interval_pct']}%) | W8={res['eligible_w8_windows']}")

    print(f"\nAuditing {len(tt_scenarios)} TrainTicket scenarios...")
    for s in tt_scenarios:
        res = audit_tt_scenario(s)
        audit_records.append(res)
        print(f"  TT: {s[:35]} | metric_int={res['metric_rows']} | trc_dur={res['trace_duration_seconds']}s | act={res['active_15s_intervals']} | W8={res['eligible_w8_windows']}")

    out_path = ROOT / "research" / "audits" / "experiment_d_temporal_eligibility_audit.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "audit_title": "AegisOps Experiment D Temporal Eligibility and Trace Coverage Audit",
            "benchmark": "AnoMod (MSR 2026, Zenodo record 18342898)",
            "total_scenarios_audited": len(audit_records),
            "sn_scenario_count": len(sn_scenarios),
            "tt_scenario_count": len(tt_scenarios),
            "summary_sn": {
                "total_metric_intervals": sum(r.get("metric_rows", 0) for r in audit_records if r.get("cohort") == "SocialNetwork"),
                "total_active_intervals": sum(r.get("active_15s_intervals", 0) for r in audit_records if r.get("cohort") == "SocialNetwork"),
                "total_empty_intervals": sum(r.get("empty_15s_intervals", 0) for r in audit_records if r.get("cohort") == "SocialNetwork"),
                "total_eligible_w8_windows": sum(r.get("eligible_w8_windows", 0) for r in audit_records if r.get("cohort") == "SocialNetwork"),
                "normal_baseline_eligible_w8_windows": next((r["eligible_w8_windows"] for r in audit_records if r.get("cohort") == "SocialNetwork" and r.get("is_normal_baseline")), 0),
            },
            "summary_tt": {
                "total_metric_intervals": sum(r.get("metric_rows", 0) for r in audit_records if r.get("cohort") == "TrainTicket"),
                "total_active_intervals": sum(r.get("active_15s_intervals", 0) for r in audit_records if r.get("cohort") == "TrainTicket"),
                "total_empty_intervals": sum(r.get("empty_15s_intervals", 0) for r in audit_records if r.get("cohort") == "TrainTicket"),
                "total_eligible_w8_windows": sum(r.get("eligible_w8_windows", 0) for r in audit_records if r.get("cohort") == "TrainTicket"),
                "normal_baseline_eligible_w8_windows": next((r["eligible_w8_windows"] for r in audit_records if r.get("cohort") == "TrainTicket" and r.get("is_normal_baseline")), 0),
            },
            "scenarios": audit_records,
        }, f, indent=2)
    print(f"\nAudit completed. Output written to: {out_path}")


if __name__ == "__main__":
    main()
