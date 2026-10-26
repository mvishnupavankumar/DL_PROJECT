# AegisOps Phase 3 Implementation and Architecture Audit

**Audit date:** 2026-10-15 (Asia/Kolkata)  
**Method:** Read-only source, metadata, existing-test-source, Phase 1/2 report, and artifact inspection. No tests, app workflows, model inference, APIs, training, or experiments were executed in this phase.

## Verdict

**B. Architecture verified with explicit limitations and a list of unresolved components.**

The core telemetry, frozen-model, diagnosis, approval, recovery, and audit-event code paths are source-verifiable. They are sufficient to produce source-backed diagram specifications, provided the diagrams clearly distinguish the synthetic frozen model, the intended live-model path, and the observed 200-record bootstrap-rule session. Figure/paper blockers are: no evidence of live-LSTM execution, no authenticated approver identity, no Experiment D production result, and a provenance mismatch between current B/C raw-record schemas and older runner schemas.

## 1. Snapshot and audit boundary

The Phase 1 and Phase 2 audit outputs remain present and unchanged from their recorded Phase 2 hashes. The source tree is the current dirty worktree, not necessarily `HEAD`; no branch or source modifications occurred. Existing test files were inspected as test evidence, but this phase did not run them and makes no current test-pass claim.

## 2. Real telemetry pipeline

| Pipeline component | Source implementation | Behavior established from code | Evidence classification |
| --- | --- | --- | --- |
| Application entry | `app.py:1-22`; `live_monitoring.render_live_monitoring()` | Streamlit app invokes the live monitoring view. | IMPLEMENTED |
| Target validation | `collectors/system_metrics.py:21-47` | HTTP only on loopback; remote monitoring requires HTTPS; URLs with embedded credentials/query/fragment are rejected. | IMPLEMENTED; TESTED by `test_target_security.py` and `test_live_monitoring.py` source |
| Sampling | `live_monitoring.py:636-680`; `collectors/system_metrics.collect_live_sample()` | UI fragment is scheduled every 5 s while selected. CPU uses `psutil.cpu_percent(interval=0.15)`; memory/disk are collector-host values; HTTP probe yields target latency/status. | IMPLEMENTED; observed audit session is irregular, so 5 s is intended cadence rather than demonstrated uniform cadence |
| Timestamp and failures | `TelemetryStore.now_iso()`; `collect_live_sample()` | UTC ISO milliseconds are assigned; request failures set status 0, unavailable state, and error text, then still record latency. | IMPLEMENTED |
| Features and units | `dl/anomaly_detector.py:14-15`; `collect_live_sample()` | Ordered feature vector is `(cpu_pct, memory_pct, latency_ms, error_rate_pct, disk_pct)` with units `%`, `%`, `ms`, `%`, `%`. Error rate is calculated over current plus 19 prior probe outcomes. | IMPLEMENTED; frozen contract VERIFIED |
| Persistence | `storage/telemetry_store.py:27-153` | SQLite `telemetry_samples` persists raw sample fields; `incident_events` persists JSON event payloads. New rows are annotated after analysis. | IMPLEMENTED; collector persistence test source present |
| Sequence construction | `live_monitoring._analyze_latest():141-230` | If a live checkpoint exists and at least 24 rows exist, the last 24 records in insertion order form a float32 24x5 window. The live path does not check timestamp continuity. | PARTIALLY IMPLEMENTED |
| Bootstrap rules | `live_monitoring._bootstrap_analysis():75-139` | Flags CPU >=90, memory >=95, latency >=1000 ms, disk >=95, non-200, or nonzero rolling error rate. | IMPLEMENTED; EVALUATED only as part of the bounded local session/harness |
| Live LSTM and fusion | `_analyze_latest():147-226`; `TelemetryAnomalyDetector.detect()` | Loads `models/live_lstm_autoencoder.pt`; computes model result; ORs it with guard triggers/unavailability; stores model and rule flags. Load/inference exceptions fall back to bootstrap rules. | IMPLEMENTED; UNVERIFIED in audited 200-row live session |
| Alert state/events | `render_live_monitoring():730-762` | Session-state edge transitions write `live_anomaly_detected` and `live_anomaly_recovered` events. | IMPLEMENTED; current database/event export demonstrates local logging, not an independent detection study |
| Evidence packaging/investigation | `_build_live_incident():294-400`; `_run_agent_investigation():431-468` | Incident includes sample-derived summary, service logs, analysis, loopback health scope, and constrained valid actions; manager/investigation/diagnosis trace is persisted as `live_agent_investigation`. | IMPLEMENTED |

### Observed execution versus design

The 200 audited telemetry records had `detector_mode=bootstrap_rules` and all 200 `anomaly_score` values null. Thus the session demonstrates collection, SQLite persistence, rule fallback, alert/event logging, and local fault-associated observations. It does **not** demonstrate live-LSTM checkpoint loading, 24-step LSTM scoring, LSTM/rule fusion, or live-model performance.

## 3. Frozen LSTM model and the intended live-model path

### A. Frozen synthetic benchmark model

`dl/anomaly_detector.py:19-31` defines `LSTMAutoencoder`: encoder LSTM `5 -> 16`, decoder LSTM `16 -> 16`, and linear projection `16 -> 5`. The encoder's final hidden state is repeated across the input time dimension before decoding; the established latent representation is the final encoder hidden vector of dimension 16. `TelemetryAnomalyDetector.detect():151-188` requires finite, exactly `24 x 5` input; it z-normalizes with frozen mean/std (std floored at `1e-6`), reconstructs normalized telemetry, and uses mean squared reconstruction error over time and features. It flags when `score > threshold`.

`models/lstm_autoencoder.json` establishes five named ordered features, `sequence_length=24`, hidden size 16, 850 synthetic training windows, 150 held-out synthetic validation windows, and threshold `0.7093990445137024`, selected as the 99th percentile of held-out normal reconstruction scores. `TelemetryAnomalyDetector.load():127-149` loads checkpoint state on CPU and raises `FileNotFoundError` if absent. Invalid dimensions/nonfinite inputs raise `ValueError` before inference.

This frozen model is the source-backed model used for the Phase 2 synthetic Experiment A. The code test source `test_anomaly_detector.py` covers shape rejection, output fields, and six injected synthetic profiles; Phase 2 supplies the evaluated 320-window metrics. It is not evidence of production or external generalization.

### B. Intended live LSTM path

`dl/live_training.train_live_model():24-107` would train a separate checkpoint at `models/live_lstm_autoencoder.pt`. It requires at least 180 eligible samples, chronological 80/20 row splitting, at least 72 training rows and 29 validation rows, at least 20 train windows and five validation windows. It fits mean/std on training rows only, with domain std floors `[1.0, 0.5, 5.0, 0.5, 0.5]`, trains the same LSTM architecture, and calibrates a separate 99th-percentile validation threshold. Overlapping windows exist within each split; there is no temporal purge gap or independent test partition.

`TelemetryStore.healthy_training_samples():105-115` selects successful HTTP-200, zero-error, `fault_mode='normal'`, non-threshold-breaching rows. This selection uses local health/fault attributes and supports only a local bootstrap baseline; it is not independently adjudicated data. Tests source in `test_live_monitoring.py` exercises a temporary checkpoint training/load path, but no persistent live checkpoint exists in this snapshot.

### C. Actual audited live session

`models/live_lstm_autoencoder.pt` and the matching live metadata file are absent. The audit export shows only bootstrap mode and null score rows. The immediate blocker was insufficient healthy eligible rows: the live-data audit identifies eight qualifying rows, versus the 180 minimum. Therefore the intended live checkpoint lifecycle is **IMPLEMENTED but not operationally demonstrated** in this snapshot.

## 4. Diagnosis and multi-agent responsibilities

`agents.IncidentAgents` wires five `GroqAgent` instances. With an API key and available package, `GroqAgent.run()` invokes the configured Groq chat completion with temperature 0.1, max 1200 tokens, and JSON parsing. It has no source-visible timeout, retry, or rate-limit handling in the live application path. Without a client it uses deterministic `_run_local()` handlers.

| Component | Input to step | Output/persistence | Mode and limitation |
| --- | --- | --- | --- |
| Manager | Incident description/category/environment via `manager_step()` | category, priority, tasks, objective | Offline deterministic or Groq-generated; no independent verification |
| Investigation | incident logs/environment, manager plan, DL analysis via `investigation_step()` | evidence, signals, candidate causes, confidence, copied DL analysis | Model output is an input; in bootstrap mode it carries no LSTM score |
| Diagnosis | incident/logs, investigation, DL analysis via `diagnosis_step()` | root cause, evidence_used, confidence, short rationale | Candidate cause is not independently adjudicated by the live workflow |
| Resolution | incident, diagnosis, action catalog, failed actions via `resolution_step()` | one action ID/rationale/expected result | Local recovery path overrides output to `clear_demo_service_fault` |
| Verification | incident, diagnosis, selected action, action result via `verification_step()` | verified/PASS or FAIL/next step | Agent reads action result; external health/probe checks are produced before this call |

`_run_agent_investigation()` persists the manager/investigation/diagnosis trace to `incident_events`, but does not execute Resolution or Verification until the approval-controlled recovery path. The Phase 2 diagnosis evidence is a six-scenario, seven-configuration pilot. A concrete provenance difference exists: older `run_experiment_b.py` emits earlier field names such as `agent_execution_mode` and `top1_correct`; `generate_diagnosis_audit.py` emits the current reconciled `execution_mode`, `rubric_verdict`, strict/lenient fields, and raw CSVs. Do not show a diagram that claims one unchanged runner produced all current B raw fields.

## 5. Approval-controlled recovery

`approval.ApprovalStore` stores expiring tickets in SQLite. It validates nonblank request fields; sets TTL 30–1800 seconds; requires exact `APPROVE <action_id>` confirmation; binds ticket to action, exact target, and incident; uses `BEGIN IMMEDIATE` transactions; rejects expired, rejected, scope-mismatched, and repeated consumption; and marks the approval `consumed` before the action. Test source in `test_approval.py` covers exact phrase, scope binding, expiry, rejection, one-time consumption, and concurrent consumers.

`live_monitoring._resolve_local_test_fault():471-582` permits only loopback HTTP service remediation. It requires service health `status='ok'` and injected fault mode `latency` or `error`; resets the demo service only to normal through `/admin/fault`; then independently obtains fresh `/health` and `/probe` responses. Success requires normal health fault mode, HTTP 200, and probe latency under 1000 ms. It writes `live_local_remediation`; UI orchestration writes requested/granted/consumed/finished/failed events.

Enforced boundaries: remote recovery is rejected; HTTP remote monitoring is rejected; embedded URL credentials are rejected; the resolution action is forcibly narrowed to `clear_demo_service_fault`; ticket replay is blocked. Material limitations: the approver label is explicitly unauthenticated, the Streamlit UI is not an identity provider, the exact confirmation phrase is not authentication, and no production action allowlist beyond the local demo action is implemented. No diagram or paper may claim authenticated dual authorization, remote remediation, or production-grade authorization.

## 6. Experiment-to-code reconciliation

| Evidence area | Current raw evidence | Closest code path | Classification |
| --- | --- | --- | --- |
| A synthetic detection | 320 prediction rows and reconciled metrics | `run_experiment_a.py`; frozen `TelemetryAnomalyDetector`; synthetic generators | IMPLEMENTED; TESTED by source tests; EVALUATED on bounded synthetic data |
| B diagnosis pilot | Current 42-row reconciled raw diagnosis records | `agents.py`; earlier `run_experiment_b.py`; current-audit producer `generate_diagnosis_audit.py` | IMPLEMENTED; EVALUATED as bounded pilot; provenance transition must be disclosed |
| C safety harness | 16 current raw safety records | `ApprovalStore`; URL validation; `_resolve_local_test_fault`; `run_safety_audit.py` | IMPLEMENTED; TESTED by source tests; EVALUATED as a local harness |
| 200 live records | telemetry export/database | collector, SQLite store, bootstrap analysis, session-event logic | IMPLEMENTED; observed collection/fallback/logging only; not LSTM evaluated |
| D AnoMod | archive/provenance and blocking audits; no outputs | `run_experiment_d.py` guarded pipeline | PARTIALLY IMPLEMENTED; tests source exists; production evaluation UNVERIFIED/blocked |

## 7. Figure-sensitive unresolved items

- Current tests were not run in this phase; test files evidence intended coverage, not current pass status.
- The actual live session has no LSTM inference artifact; diagrams must depict it as an optional/absent branch for that session.
- Live windows are last-24 insertion-order samples with no timestamp-continuity test; do not describe them as guaranteed contiguous 5-second sequences.
- Current B/C raw evidence was generated/reconciled through later audit scripts, while older experiment runners expose differing schemas; do not overstate end-to-end direct rerun provenance.
- `run_experiment_d.py` contains an 8-step harness pathway that directly calls `detector.model`, while the frozen contract requires 24 steps. It remains blocked and cannot be represented as valid frozen-model external inference.
- Approval identity is a label only; authorization is a local workflow guard, not authenticated human dual control.
