# AegisOps Live LSTM Integration and Root-Cause Audit

**Date:** 2026-10-16 (Asia/Kolkata)  
**Scope:** Read-only repository, model, configuration, SQLite, telemetry-export, test-source, and audit inspection. No application code, model, threshold, telemetry row, database row, raw evidence, or historical manifest was changed. No model inference or performance experiment was run.

## Executive verdict

| Required determination | Verdict | Basis |
| --- | --- | --- |
| A. Inference integration is currently functional | **No.** | The inference branch exists, but its required live checkpoint is absent and no recorded session entered it. |
| B. Inference integration requires repair | **Yes.** | Checkpoint-selection/provenance handling and temporal-window admission require repair before responsible live inference. |
| C. Live performance can currently be measured | **No.** | There are zero live LSTM scores and no suitable independently labelled evaluation design. |
| D. Additional labelled evaluation data is required | **Yes.** | Current telemetry is irregular, includes a long injected error episode, and has no independent labels or model predictions. |

**Confirmed primary cause:** live_monitoring._analyze_latest only enters inference when models/live_lstm_autoencoder.pt exists at live_monitoring.py:147-150. That file and its metadata are absent. The present models/lstm_autoencoder.pt is not discovered by the live path. Consequently the condition is false, _bootstrap_analysis runs, and the store receives detector_mode bootstrap_rules with anomaly_score NULL at live_monitoring.py:241-252 and storage/telemetry_store.py:114-138.

The existing frozen checkpoint is technically compatible with the generic loader: a read-only strict CPU state-dictionary load found no missing or unexpected keys. It has the required five ordered features, 24-step input, hidden size 16, scaler vectors, and threshold. However, it is a synthetic-calibrated artifact, not a live-trained checkpoint. Its use in a future explicit integration smoke test would not require retraining, but using it silently as the active live model would obscure provenance and would not validate live detection performance.

## Repository state and audit boundary

| State | Value |
| --- | --- |
| Repository | C:\DL_PROJECT |
| Branch before audit outputs | publish/research-without-external-dataset |
| HEAD before audit outputs | a32713c30a8ddca1425d44b1afbaf6d55a64c276 |
| Working tree before audit outputs | Dirty: 84 porcelain entries: 40 modified and 44 untracked paths. |
| Audit actions | No clean, reset, stash, commit, manifest refresh, code edit, model write, database write, telemetry write, training, or performance run. |

The mandatory Phase 1, Phase 3, Phase 10, Phase 11, and Phase 12 records were read. The prior Live LSTM discussion was read from research/exports/LIVE_DATA_AND_EXTERNAL_VALIDATION_AUDIT.md plus supporting live/deep-learning audit notes. The current repository, model, and SQLite state controlled this investigation.

## Confirmed end-to-end trace

The detailed sequence is in LIVE_LSTM_EXECUTION_TRACE.csv.

1. **Collection and persistence.** render_live_monitoring creates TelemetryStore at live_monitoring.py:606-615 and calls collect_live_sample while collection is selected at live_monitoring.py:661-691. The collector reads collector-host CPU, memory, and disk; probes the configured HTTP target; calculates a rolling error rate; timestamps the sample; and inserts it at collectors/system_metrics.py:65-138 and storage/telemetry_store.py:73-86.
2. **Selection.** After rows are read in ascending insertion/id order at storage/telemetry_store.py:93-96, _analyze_latest checks only LIVE_MODEL_PATH. That symbol is fixed to models/live_lstm_autoencoder.pt at dl/live_training.py:14-15 and is loaded by the wrapper at dl/live_training.py:109-110.
3. **Window and scoring.** If that file exists and at least 24 rows exist, the last 24 rows are cast in fixed feature order to float32 and passed to detector.detect at live_monitoring.py:147-160. The detector requires finite exact 24-by-5 input, normalizes with checkpoint mean/std, reconstructs on CPU, uses mean squared reconstruction error, and tests score greater than threshold at dl/anomaly_detector.py:127-187.
4. **Fusion and persistence.** Success is ORed with HTTP/status/resource guardrails and score plus model/rule/combined state are persisted at live_monitoring.py:165-225 and storage/telemetry_store.py:114-138.
5. **Fallback.** A false checkpoint condition or eligible load/inference exception leads to bootstrap rules. The absent-checkpoint branch persists score None and bootstrap_rules at live_monitoring.py:229-252.

## Confirmed findings

### Why the session selected bootstrap_rules

- models/live_lstm_autoencoder.pt and models/live_lstm_autoencoder.json do not exist anywhere in the workspace.
- The only model artifacts are models/lstm_autoencoder.pt and models/lstm_autoencoder.json.
- The live code does not search for or fall back to the frozen file; its wrapper always targets the absent live file.
- The historical SQLite database contains 200 rows, all bootstrap_rules, all anomaly_score NULL, and zero live_lstm_autoencoder rows. Event payloads explicitly say Bootstrap rules (live DL model unavailable).

This is a deterministic branch-selection finding. There is no evidence that a checkpoint-load, tensor, or inference exception occurred in this session because the condition guarding those operations was false.

### Frozen checkpoint architecture and compatibility

| Contract item | Confirmed value | Source |
| --- | --- | --- |
| Features/order | cpu_pct, memory_pct, latency_ms, error_rate_pct, disk_pct | dl/anomaly_detector.py:13-16; metadata |
| Sequence length | 24 | metadata/checkpoint |
| Architecture | encoder LSTM 5-to-16; decoder LSTM 16-to-16; linear 16-to-5 | dl/anomaly_detector.py:19-32 |
| Hidden size | 16 | metadata/checkpoint |
| Parameters | 3,733 | read-only architecture inspection; research/scripts/smoke_test_checkpoint.py:51-65 |
| Normalization | checkpoint mean/std; load floor 1e-6 | dl/anomaly_detector.py:117-120,159-166 |
| Global threshold | 0.7093990445137024 | metadata/checkpoint |
| Device | CPU map_location | dl/anomaly_detector.py:133 |
| Strict load | zero missing and zero unexpected keys | direct read-only checkpoint inspection |

Checkpoint and metadata agree on feature order, sequence length, hidden size, mean, standard deviation, global/per-feature thresholds, epochs, training/validation windows, and threshold method. TelemetryAnomalyDetector.load(path) can therefore load the frozen artifact without retraining. The live wrapper cannot because it hardcodes a different path.

### Model provenance boundary

The frozen artifact is trained by generate_normal_windows at dl/anomaly_detector.py:35-64 and 190-259. Metadata records 850 synthetic training windows, 150 synthetic validation windows, and a 99th-percentile synthetic-normal threshold. This agrees with Phase 1, Phase 3, Phase 11, and the prior live-data audit. Path selection can enable technical scoring but cannot establish calibration validity or performance on collector-host and HTTP-probe telemetry.

### Data/window findings

All five required model features are finite in all 200 rows. There are 177 mechanically constructible 24-row ID-order windows. Thus neither insufficient row count nor nonfinite values selected bootstrap mode.

However, live_monitoring.py:147-160 performs no timestamp continuity check. Inter-sample gaps range from 0.578 to 6170.223 seconds; 26 exceed 60 seconds. At a hypothetical maximum gap of 10 seconds, 41 of 177 mechanical windows are continuous; at 60 seconds, 54 are continuous. The current implementation would admit discontinuous windows if a checkpoint existed. The appropriate maximum gap and reset behavior are unresolved policy questions.

### Intended live-training lifecycle

The separate UI path trains only from healthy_training_samples at live_monitoring.py:861-905. The SQL filter requires service availability, HTTP 200, zero error rate, fault_mode normal, and non-breaching resource/latency values at storage/telemetry_store.py:103-112. The current database has only 8 fully eligible rows; the trainer requires 180 at live_monitoring.py:32 and dl/live_training.py:24-51. The stored session could not have produced the live checkpoint through its intended lifecycle.

## Likely causes and repair-relevant weaknesses

### Checkpoint policy lacks explicit provenance-aware selection

Separating synthetic and live-trained checkpoints is scientifically correct. The repair need is an explicit selection policy: a default live-trained path, a separately approved opt-in frozen path for integration smoke testing, and durable selection/fallback reason records. The current branch treats absent live checkpoint as expected fallback but gives no supported route to intentionally test the frozen artifact without renaming/copying it.

### Fallback errors are not durably classified

ValueError, KeyError, RuntimeError, OSError, and TypeError are warned in Streamlit before rules are used at live_monitoring.py:229-239. No durable fallback event or distinct detector mode is written. Future malformed-checkpoint or inference failure would be difficult to distinguish from checkpoint absence in export data.

### Historical schema lacks decision decomposition

Current initialization can add model_anomaly, rule_anomaly, and combined_anomaly at storage/telemetry_store.py:52-63, but the historical on-disk database lacks them. This does not cause the observed fallback, but it precludes historical model-versus-rule analysis. A future migration must be tested on a disposable copy, never on historical evidence.

## Unresolved questions

1. Does the owner authorize frozen synthetic-checkpoint use only for a labelled integration smoke test, or exposure in the UI with a synthetic-calibration warning?
2. What maximum timestamp gap and window-reset policy represents intended five-second collection?
3. Did a dashboard fragment, worker process, or both produce the irregular historical cadence? The available evidence does not establish this.
4. What target metrics, independently adjudicated labels, and evaluation unit will govern prospective live performance evaluation?
5. How will non-demo targets provide healthy-training eligibility when fault_mode normal is local-demo-specific?

## Existing tests and coverage gap

test_live_monitoring.py:51-71 tests temporary live-checkpoint training/loading. test_anomaly_detector.py:26-45 tests frozen detector fields, synthetic injected cases, and wrong shape. test_research_instrumentation.py:12-31 tests prediction persistence in a temporary database. They do not test actual _analyze_latest checkpoint selection, explicit frozen provenance, timestamp-gap rejection/reset, or durable fallback-cause classification.

## Required non-implementation repair plan

See LIVE_LSTM_REPAIR_AND_VALIDATION_PLAN.md. The key preservation rule is not to copy, rename, or overwrite the frozen checkpoint as the live checkpoint. Doing so would erase the synthetic-versus-live provenance distinction.

## Evidence limits

- This audit explains why scores are null; it does not demonstrate live LSTM scoring.
- Strict frozen-checkpoint loading confirms technical compatibility only, not live calibration.
- No live accuracy, recall, precision, false-positive rate, alarms-per-hour rate, causal diagnosis, or external-generalization result is available.
- The historical 31 normal, 1 latency, and 168 error rows include local injections and a long error episode; they are not independently labelled disjoint operational evaluation units.

## Repository state after audit outputs

This audit adds only its three files under research/exports/live_lstm. Branch and HEAD remain publish/research-without-external-dataset and a32713c30a8ddca1425d44b1afbaf6d55a64c276. The final working tree has 85 porcelain entries: 40 modified and 45 untracked paths. Relative to the recorded pre-output state, only the new live_lstm output directory was added; no existing tracked or historical artifact was modified by this audit.
