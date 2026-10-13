# AegisOps: Experiment D Requirements Traceability Matrix

**Document Path**: `research/audits/EXPERIMENT_D_REQUIREMENTS_TRACEABILITY.md`  
**Date**: October 13, 2026  
**Auditor**: Senior Research Supervisor, ML Engineer & Reproducibility Auditor  
**Scope**: Traceability from Protocol Requirements & Integrity Rules to Code, Tests, and Verification Evidence  
**Status**: **TRACEABILITY COMPLETE & VERIFIED**

---

## 1. Traceability Matrix

| Requirement ID | Requirement Description | Source Standard | Implementation Location | Verification Test(s) | Empirical Evidence / Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | **Frozen Model Preservation**: Checkpoint weights and architecture must remain unmodified. | Integrity Rule 1 | `dl/anomaly_detector.py`<br>`run_experiment_d.py:816-830` | `test_experiment_d_harness.py::test_checkpoint_loads_and_eval_mode`<br>`test_checkpoint_weights_remain_strictly_frozen` | SHA-256: `1cf44e6e...` bit-for-bit verified. 3,733 params, eval mode, weight delta = 0. |
| **REQ-02** | **5-D Feature Contract**: Telemetry must strictly extract `(cpu_pct, memory_pct, latency_ms, error_rate_pct, disk_pct)`. | Protocol §4.1 | `run_experiment_d.py:66` | `test_feature_order_strictly_matches_frozen_contract` | 5 features ordered and validated in tensor inputs. |
| **REQ-03** | **Zero-Leakage Calibration**: Scaler parameters and threshold fit exclusively on normal warmup data. | Integrity Rule 2, Protocol §5.1 | `run_experiment_d.py:391-432, 436-470` | `test_scaler_fitting_restricted_to_calibration_windows`<br>`test_partition_normal_series_chronologically_disjoint`<br>`test_partition_normal_series_leakage_assertion` | Chronological pre-windowing partition with 7-step purge gap. Disjoint timestamps verified. |
| **REQ-04** | **Temporal Continuity**: Windows must consist of consecutive 15-second intervals ($\Delta t = 15.0\text{s}$) with no gaps. | Time-Series Evaluation Rigor | `run_experiment_d.py:335-389` | `test_build_contiguous_windows_strictly_consecutive`<br>`test_build_contiguous_windows_rejects_temporal_gap`<br>`test_build_contiguous_windows_rejects_missing_latency` | Windows spanning missing intervals or NaNs are rejected; buffer reset enforced. |
| **REQ-05** | **No Arbitrary Imputation**: No zero values may be imputed for latency during idle intervals. | Integrity Rule 6 | `run_experiment_d.py:209-221, 361-367` | `test_latency_native_milliseconds_no_spurious_multiplier`<br>`test_build_contiguous_windows_rejects_missing_latency` | NaN preserved when $N_{\text{req}} = 0$; rejected from contiguous windowing. |
| **REQ-06** | **Baseline Rule Evaluation**: Implement Narrow, Resource-Only, and Full Operational rule baselines. | Protocol §4.3 | `run_experiment_d.py:102-135` | `test_narrow_rules_baseline`<br>`test_resource_rules_baseline`<br>`test_full_operational_rules_baseline` | Exact rule logic verified against protocol definitions. |
| **REQ-07** | **Isolation Forest Baseline**: Calibrate IF threshold on identical nominal calibration partition. | Protocol §4.3 | `run_experiment_d.py:552-559` | `test_isolation_forest_fitting_restricted_to_normal_data` | Contamination 0.01, 100 estimators, 99th percentile threshold fit on normal windows. |
| **REQ-08** | **Paired Statistical Comparisons**: Evaluate all detectors on identical eligible windows with exact paired tests. | Protocol §6.2 | `run_experiment_d.py:642-658` | `test_identical_eligible_observations_across_baselines`<br>`test_mcnemar_exact_verified_benchmark`<br>`test_wilcoxon_signed_rank_exact_benchmark` | Discordant pair tally and exact binomial p-value calculated. Scenario-level Wilcoxon executed. |
| **REQ-09** | **Fail-Closed Execution Gate**: Execution without explicit flags or unratified protocol must fail closed. | Integrity Rule 5 | `run_experiment_d.py:896-926` | `test_fail_closed_cli_unauthorized_exit_code_2`<br>`test_fail_closed_cli_unratified_exit_code_3` | Exit 2 for unauthorized; Exit 3 for unratified; Exit 0 for dry-run/pipeline test. |
| **REQ-10** | **Reproducible Provenance Manifest**: Serialize SHA-256 hashes, timestamps, sample counts, and parameters. | Protocol §7.3 | `run_experiment_d.py:661-681` | `test_run_evaluation_pipeline_sandbox` | JSON manifest serializes calibration metadata, discordant pairs, and file paths. |

---

## 2. Traceability Verification Verdict

All 10 fundamental requirements (REQ-01 through REQ-10) have been mapped to specific functions in `research/experiments/run_experiment_d.py` and are covered by 40 unit and integration tests in `test_experiment_d_harness.py`. All tests pass deterministically.
