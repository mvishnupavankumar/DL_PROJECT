# AegisOps: Experiment D Remediation Changelog

**Document Path**: `research/audits/EXPERIMENT_D_REMEDIATION_CHANGELOG.md`  
**Date**: October 13, 2026  
**Auditor**: Senior Research Supervisor, ML Engineer & Reproducibility Auditor  
**Target Codebase**: `research/experiments/run_experiment_d.py`, `test_experiment_d_harness.py`, `research/audits/`  
**Status**: **ALL DEFECTS REMEDIATED AND INDEPENDENTLY VERIFIED**

---

## 1. Executive Summary

This changelog records all defects, architectural omissions, and mathematical leakage risks identified during the Phase 9 Stage 4 audit of the **Experiment D** harness, along with their precise code remediations and regression test verifications.

---

## 2. Chronological Log of Defects and Remediations

### Defect 1: Authorized Execution Path was a Non-Executing Scaffold
- **Discovered In**: Initial code audit of `run_experiment_d.py:370-373`.
- **Finding**: Passing `--authorized` printed `Executing authorized Experiment D...` and immediately returned exit code 0 without discovering scenarios, running detectors, or writing CSV files.
- **Remediation**: Implemented `run_production_experiment_d()` in `run_experiment_d.py`. It executes real SocialNetwork scenario discovery, 5D telemetry extraction, chronological partitioning, contiguous windowing, baseline scoring, and artifact validation.
- **Verification**: Verified via `--test-pipeline` end-to-end sandbox execution and `--dry-run` validation.

---

### Defect 2: Missing Fail-Closed Protocol Ratification Gate
- **Discovered In**: Preflight audit of protocol governance.
- **Finding**: Merely passing `--authorized` on the command line would execute against unapproved protocol alterations without an auditable ratification record.
- **Remediation**: Implemented a mandatory ratification check in `run_experiment_d.py`. Execution requires the presence of `research/audits/PROTOCOL_AMENDMENT_V1_2_RATIFICATION.json` containing `"protocol_version": "v1.2.0"`, `"status": "RATIFIED"`, and `"ratified_by"`. Missing or invalid ratification exits with code 3.
- **Verification**: Tested in `test_experiment_d_harness.py::test_fail_closed_cli_unratified_exit_code_3` and verified live via CLI.

---

### Defect 3: Permissive Metric Concatenation Bridging Over Multi-Minute Gaps
- **Discovered In**: Time-series continuity inspection of `extract_sn_telemetry`.
- **Finding**: Prior code utilized `dropna(subset=['latency_ms'])`, which concatenated non-consecutive 15s intervals separated by minutes of idle traffic into an artificially continuous array.
- **Remediation**: Implemented `build_contiguous_windows(df, window_length=8, step_seconds=15.0)`. Every accepted 8-step window strictly verifies that adjacent timestamps advance by $15.0\text{s} \pm 10^{-3}\text{s}$ and contain finite values across all 5 features. Any temporal gap or NaN immediately resets the buffer.
- **Verification**: Added `test_build_contiguous_windows_strictly_consecutive`, `test_build_contiguous_windows_rejects_temporal_gap`, and `test_build_contiguous_windows_rejects_missing_latency`.

---

### Defect 4: Calibration Partition Leakage via Shared Sliding Window Observations
- **Discovered In**: Calibration audit of `fit_calibration_scaler` and `calibrate_threshold`.
- **Finding**: A 70/30 post-windowing train/test split on overlapping sliding windows allowed the final calibration window and first validation window to share up to 7 raw time points ($W-1=7$ steps of overlap).
- **Remediation**: Implemented `partition_normal_series_chronologically(df_normal, train_fraction=0.70, purge_gap_steps=7)`. The raw nominal time series is partitioned chronologically *before* windowing, enforcing a strict purge gap of 7 steps (105 seconds). Calibration and validation windows have 100% disjoint unique raw timestamps.
- **Verification**: Added `test_partition_normal_series_chronologically_disjoint` and `test_partition_normal_series_leakage_assertion`.

---

### Defect 5: Missing TrainTicket Ingestion and Extraction Function
- **Discovered In**: Benchmark coverage audit.
- **Finding**: `run_experiment_d.py` contained extraction for SocialNetwork but had no function for parsing TrainTicket multi-container Prometheus CSVs or SkyWalking trace JSON.
- **Remediation**: Implemented `extract_tt_telemetry(scenario_metric_dir, scenario_trace_dir)` to parse non-idle CPU counter deltas, memory usage from `MemAvailable`/`MemTotal`, disk usage, SkyWalking P95 duration, and `is_error` rates.
- **Verification**: Tested on synthetic TrainTicket fixture in `test_extract_tt_telemetry_synthetic_fixture`.

---

### Defect 6: Missing End-to-End Test Sandbox
- **Discovered In**: Continuous integration and reproducibility audit.
- **Finding**: No mechanism existed to verify the complete call graph (including statistical tests and CSV writing) without modifying repository production paths.
- **Remediation**: Implemented `--test-pipeline` flag in `run_experiment_d.py` and `run_evaluation_pipeline()`. It instantiates synthetic calibration, validation, and fault scenarios, runs all 5 detectors, computes McNemar and Wilcoxon tests, and writes artifacts to an isolated temporary directory.
- **Verification**: Tested in `test_run_evaluation_pipeline_sandbox` and `test_test_pipeline_cli_exit_code_0`.

---

## 3. Summary of Code & Test Additions

| File | Changes Made | Lines Changed / Added | Test Count Impact |
| :--- | :--- | :---: | :---: |
| `research/experiments/run_experiment_d.py` | Added `extract_tt_telemetry`, `build_contiguous_windows`, `partition_normal_series_chronologically`, `run_production_experiment_d`, `--test-pipeline`, ratification gate | +450 lines | Enabled 15 new test cases |
| `test_experiment_d_harness.py` | Added test cases for TT extraction, contiguous windowing, gap rejection, chronological partitioning, sandbox execution, CLI exit codes | +260 lines | Expanded from 25 to 40 tests |
