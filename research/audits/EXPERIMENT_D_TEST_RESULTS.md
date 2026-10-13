# AegisOps: Experiment D Test Results and Verification Audit

**Document Path**: `research/audits/EXPERIMENT_D_TEST_RESULTS.md`  
**Date**: October 13, 2026  
**Auditor**: Senior Research Supervisor, ML Engineer & Reproducibility Auditor  
**Python Runtime**: `C:\DL_PROJECT\.venv\Scripts\python.exe` (Python 3.11.9, pytest 9.1.1, pluggy 1.6.0)  
**Status**: **100% PASSING (40/40 HARNESS TESTS, 105/105 FULL REPOSITORY TESTS)**

---

## 1. Executive Summary

This document records the empirical execution of the automated test suite verifying the **Experiment D** evaluation harness, data extraction functions, baseline detectors, calibration logic, temporal continuity constraints, fail-closed CLI execution guards, and repository regression stability.

All test commands were executed directly inside the active repository virtual environment (`C:\DL_PROJECT\.venv`).

---

## 2. Dedicated Harness Test Suite (`test_experiment_d_harness.py`)

- **Execution Command**: `.venv\Scripts\python.exe -m pytest test_experiment_d_harness.py -v --tb=short`
- **Result**: **40 passed in 13.57 seconds (Exit Code: 0)**
- **Breakdown**:
  - **Passing**: 40
  - **Failing**: 0
  - **Skipped**: 0
  - **Not Executed**: 0
  - **Missing**: 0

### Detailed Test Inventory:

| # | Test Identifier | Module Area | Verified Invariant | Status |
| :-: | :--- | :--- | :--- | :---: |
| 1 | `test_feature_order_strictly_matches_frozen_contract` | Feature Contract | Features match `("cpu_pct", "memory_pct", "latency_ms", "error_rate_pct", "disk_pct")` | **PASSED** |
| 2 | `test_sliding_window_shape_and_feature_order` | Windowing | Array sliding window produces shape `(N, 8, 5)` | **PASSED** |
| 3 | `test_sliding_window_insufficient_samples` | Windowing | Returns empty array `(0, 8, 5)` if samples < 8 | **PASSED** |
| 4 | `test_cpu_counter_rate_calculation` | Telemetry Preprocessing | Idle counter rate converted to $[0, 100]\%$ utilization | **PASSED** |
| 5 | `test_cpu_counter_reset_detection` | Telemetry Preprocessing | Monotonic resets handled safely | **PASSED** |
| 6 | `test_memory_percentage_calculation_no_double_scaling` | Telemetry Preprocessing | Memory fraction converted to percentage without double scaling | **PASSED** |
| 7 | `test_disk_capacity_percentage_not_throughput` | Telemetry Preprocessing | Disk space utilization derived from capacity, not I/O ops | **PASSED** |
| 8 | `test_latency_native_milliseconds_no_spurious_multiplier` | Telemetry Preprocessing | Microseconds to milliseconds correctly divided by 1000.0 | **PASSED** |
| 9 | `test_error_rate_zero_requests_interval` | Telemetry Preprocessing | Error rate strictly 0.0% when request count is zero | **PASSED** |
| 10 | `test_error_rate_calculation_percentage` | Telemetry Preprocessing | HTTP 5xx / total requests * 100.0 | **PASSED** |
| 11 | `test_narrow_rules_baseline` | Baselines | Latency >= 1000ms or Memory >= 95% | **PASSED** |
| 12 | `test_resource_rules_baseline` | Baselines | CPU >= 90% or Mem >= 95% or Disk >= 95% or Lat >= 1000ms | **PASSED** |
| 13 | `test_full_operational_rules_baseline` | Baselines | Resource rules OR Error Rate > 0.5% | **PASSED** |
| 14 | `test_scaler_fitting_restricted_to_calibration_windows` | Calibration | Mean/Std computed exclusively on calibration windows | **PASSED** |
| 15 | `test_threshold_calculation_99th_percentile` | Thresholding | Anomaly threshold at 99th percentile of nominal errors | **PASSED** |
| 16 | `test_threshold_calculation_insufficient_samples_behavior` | Thresholding | Graceful handling when validation samples are empty | **PASSED** |
| 17 | `test_isolation_forest_fitting_restricted_to_normal_data` | Baselines | Isolation Forest trained on normal data strictly | **PASSED** |
| 18 | `test_checkpoint_loads_and_eval_mode` | Checkpoint Rigor | Loads `models/lstm_autoencoder.pt`, strict keys, eval mode | **PASSED** |
| 19 | `test_checkpoint_weights_remain_strictly_frozen` | Checkpoint Rigor | Parameters unchanged bit-for-bit after inference | **PASSED** |
| 20 | `test_model_forward_accepts_8_step_window` | Checkpoint Rigor | Forward pass accepts sequence length $W=8$ cleanly | **PASSED** |
| 21 | `test_contingency_and_metrics_calculation` | Metrics | Correct computation of TP, FP, TN, FN, Recall, FPR, F1 | **PASSED** |
| 22 | `test_degenerate_confusion_matrices_no_divide_by_zero` | Metrics | Zero division handled gracefully | **PASSED** |
| 23 | `test_mcnemar_exact_verified_benchmark` | Statistical Tests | McNemar exact test matches verified benchmark implementation | **PASSED** |
| 24 | `test_mcnemar_exact_zero_discordant` | Statistical Tests | Returns p = 1.0 when discordant pairs $b = 0, c = 0$ | **PASSED** |
| 25 | `test_wilcoxon_signed_rank_exact_benchmark` | Statistical Tests | Wilcoxon signed-rank test matches verified benchmark | **PASSED** |
| 26 | `test_existing_research_artifacts_preserved` | Integrity Protection | SHA-256 of historical CSVs and checkpoint unaltered | **PASSED** |
| 27 | `test_missing_response_time_log_verified` | Dataset Inspection | Asserts `response_time.log` does not exist in AnoMod | **PASSED** |
| 28 | `test_extract_sn_telemetry_synthetic_fixture` | Feature Extraction | Multi-metric join on 15s grid for SocialNetwork | **PASSED** |
| 29 | `test_extract_tt_telemetry_synthetic_fixture` | Feature Extraction | SkyWalking and Prometheus extraction for TrainTicket | **PASSED** |
| 30 | `test_build_contiguous_windows_strictly_consecutive` | Temporal Continuity | Accepts windows with truly $\Delta t = 15.0\text{s}$ spacing | **PASSED** |
| 31 | `test_build_contiguous_windows_rejects_temporal_gap` | Temporal Continuity | Rejects windows spanning missing 15s intervals | **PASSED** |
| 32 | `test_build_contiguous_windows_rejects_missing_latency` | Temporal Continuity | Rejects windows containing NaNs from idle intervals | **PASSED** |
| 33 | `test_partition_normal_series_chronologically_disjoint` | Zero-Leakage | 70/30 chronological split has 0 shared timestamps | **PASSED** |
| 34 | `test_partition_normal_series_leakage_assertion` | Zero-Leakage | Asserts `LeakageViolationError` if timestamps overlap | **PASSED** |
| 35 | `test_run_evaluation_pipeline_sandbox` | Call Graph Integration | End-to-end evaluation pipeline executes in isolated tempdir | **PASSED** |
| 36 | `test_identical_eligible_observations_across_baselines` | Fair Comparison | All detectors scored on identical valid windows | **PASSED** |
| 37 | `test_fail_closed_cli_unauthorized_exit_code_2` | CLI Execution Gate | Unflagged CLI invocation exits with code 2 | **PASSED** |
| 38 | `test_fail_closed_cli_unratified_exit_code_3` | CLI Execution Gate | Flagged CLI invocation without ratification file exits code 3 | **PASSED** |
| 39 | `test_dry_run_cli_exit_code_0` | CLI Execution Gate | `--dry-run` exits code 0 without writing outputs | **PASSED** |
| 40 | `test_test_pipeline_cli_exit_code_0` | CLI Execution Gate | `--test-pipeline` exits code 0 with isolated temp outputs | **PASSED** |

---

## 3. Full Repository Regression Test Suite

- **Execution Command**: `.venv\Scripts\python.exe -m pytest --tb=short`
- **Result**: **105 passed in 36.83 seconds (Exit Code: 0)**
- **Test File Inventory**:
  - `test_agents.py`: 3 passed
  - `test_anomaly_detector.py`: 9 passed
  - `test_approval.py`: 8 passed
  - `test_experiment_d_harness.py`: 40 passed
  - `test_ingest_anomod.py`: 22 passed
  - `test_live_monitoring.py`: 6 passed
  - `test_research_instrumentation.py`: 2 passed
  - `test_simulator.py`: 3 passed
  - `test_statistical_audit.py`: 6 passed
  - `test_target_security.py`: 4 passed
  - `test_workflow.py`: 2 passed
- **Summary**:
  - **Passing**: 105
  - **Failing**: 0
  - **Skipped**: 0
  - **Not Executed**: 0
  - **Missing**: 0

### Virtual Environment Caveat Note:
When executed using the global system Python (`C:\Users\chara\AppData\Local\Programs\Python\Python311\python.exe`), `test_live_monitoring.py` fails due to `ModuleNotFoundError: No module named 'streamlit'`. When executed inside the active project virtual environment (`C:\DL_PROJECT\.venv\Scripts\python.exe`), all 105 tests pass cleanly. All verification commands must strictly target `.venv`.

---

## 4. Live CLI Execution Guard Tests

| Invocations Tested | Command Line | Expected Exit Code | Observed Exit Code | Observed Standard Output / Behavior | Gate Status |
| :--- | :--- | :---: | :---: | :--- | :---: |
| **No Flags** | `.venv\Scripts\python.exe research/experiments/run_experiment_d.py` | 2 | 2 | `EXPERIMENT D EXECUTION: BLOCKED (Unauthorized)` | **VERIFIED** |
| **Authorized Only** | `.venv\Scripts\python.exe research/experiments/run_experiment_d.py --authorized` | 3 | 3 | `EXPERIMENT D EXECUTION: BLOCKED — PROTOCOL AMENDMENT PENDING APPROVAL` | **VERIFIED** |
| **Dry Run** | `.venv\Scripts\python.exe research/experiments/run_experiment_d.py --dry-run` | 0 | 0 | `[DRY RUN / VALIDATION MODE ACTIVE] PASS` | **VERIFIED** |
| **Pipeline Test** | `.venv\Scripts\python.exe research/experiments/run_experiment_d.py --test-pipeline` | 0 | 0 | `Generated 30 predictions and 5 metrics in test sandbox. ExitCode: 0` | **VERIFIED** |
