# AegisOps Phase 3 Diagram Specification

This is a source-backed specification only. It must precede and constrain later figure generation. Every diagram must use a legend distinguishing **implemented**, **observed in audited session**, **evaluated synthetic/local**, **optional**, and **blocked/proposed**. None may imply live-LSTM scoring in the 200-row bootstrap session.

## 1. Overall AegisOps architecture

**Nodes:** Streamlit UI (`app.py`, `live_monitoring.py`); collector-host metrics and configured HTTP target (`collectors/system_metrics.py`); SQLite telemetry/event store (`storage/telemetry_store.py`); bootstrap rules; optional live LSTM; incident builder; Manager/Investigation/Diagnosis agents; human approval UI; `ApprovalStore`; local demo recovery; health/probe verification.

**Directed edges:** collector -> telemetry store -> bootstrap rules or optional live LSTM -> fused alert -> incident builder -> manager -> investigation -> diagnosis -> human approval request -> ticket approval/consume -> local demo recovery -> health and probe verification -> event store. Draw event-store arrows from alert, investigation, and recovery lifecycle.

**Failure/fallback:** missing live checkpoint, fewer than 24 rows, malformed/nonfinite window, or LSTM load/inference error -> bootstrap rules. Remote monitoring -> read-only incident action. Invalid/expired/replayed ticket -> no action. Failed health/probe verification -> failure event and no verified resolution.

**Trust boundary:** configured target sits outside the application; collector-host metrics are not target-host metrics. Human approval label is inside an unauthenticated local UI boundary. Recovery is restricted to the loopback local-demo service.

**Must not show:** live LSTM as active in the audited session; remote remediation; authenticated dual control; external Experiment D validation.

## 2. Detailed LSTM autoencoder architecture

**Frozen-model nodes:** input `X` shape `(24,5)` in exact feature order; frozen mean/std normalization; encoder LSTM `5 -> 16`; final hidden state `h` shape `(16)`; repeat `h` across 24 steps; decoder LSTM `16 -> 16`; linear output `16 -> 5`; normalized reconstruction; elementwise squared error; global MSE score; strict comparison `score > 0.7093990445137024`; per-feature mean errors versus feature thresholds.

**Source:** `dl/anomaly_detector.py:14-31,105-188`; `models/lstm_autoencoder.json`.

**Data-flow direction:** raw 24x5 -> normalized 24x5 -> reconstruction 24x5 -> error -> score/feature errors -> decision.

**Failure paths:** wrong feature dimension, wrong 24-step length, or nonfinite value -> `ValueError`; missing checkpoint -> `FileNotFoundError` on load. In the live UI, runtime failures fall back to rules.

**Distinguish:** frozen synthetic checkpoint has 850/150 synthetic train/validation windows; separate live training would emit a different checkpoint and threshold. Do not call the 16-dimensional hidden state a verified semantic causal representation.

## 3. Telemetry-to-alert data flow

**Nodes:** `psutil` CPU/memory/disk; HTTP `/probe`; optional local `/health`; previous 19 stored status codes; sample builder; `TelemetryStore.add_sample`; last 24 rows; live detector; guard rules; `TelemetryStore.annotate_sample`; alert transition/events.

**Processing:** collect host percentages + timed HTTP response; compute rolling `error_rate_pct`; persist first; select the latest 24 insertion-order records if optional live model exists; otherwise apply rules. In LSTM mode, model decision OR guard/unavailability becomes `is_anomaly`; in fallback, rules decide it.

**Source:** `collectors/system_metrics.py:65-135`; `live_monitoring.py:75-230,636-762`; `storage/telemetry_store.py:70-153`.

**Observed-session overlay:** mark `live_lstm_autoencoder` as **not observed/absent checkpoint**; show `bootstrap_rules` as the only observed detection path for all 200 rows. Mark collection interval as nominal five seconds but observed timestamps as irregular.

**Must not show:** continuous guaranteed sampling, direct target-host resource collection, or a measured live LSTM score.

## 4. Multi-agent diagnosis workflow

**Nodes and edges:** incident/logs/environment + analysis -> Manager plan -> Investigation evidence/signals/candidate causes -> Diagnosis root cause/evidence/confidence -> Resolution action selection from incident catalog -> Verification of supplied action result. `live_monitoring._run_agent_investigation()` executes the first three and persists a trace; `_resolve_local_test_fault()` executes resolution and supplies the result to verification only after approval-controlled recovery.

**Source:** `agents.py:15-268`; `live_monitoring.py:294-468,471-582`.

**Mode labels:** each agent is either deterministic `offline_demo` when client unavailable or Groq-backed when credentials/client are present. Place a service/API boundary around Groq. Note source-visible live path has no explicit retry/timeout/rate-limit handler.

**Must not show:** that all agents ran in all B configurations, that model output proves causality, or that agent diagnosis is independently validated.

## 5. Approval and recovery state machine

**States:** `pending` -> `approved` -> `consumed`; `pending` -> `rejected`; `pending`/`approved` -> `expired`. `consumed`, `rejected`, and `expired` are terminal for that ticket.

**Guards:** request requires action/target/incident/requester; approve requires exact phrase, nonblank label, matching scope, pending state, unexpired ticket; consume requires approved state, matching scope, unexpired ticket, atomic state transition. Before recovery, validate loopback HTTP service, healthy identity response, and active injected `latency`/`error` fault.

**Action/output:** consume -> POST local `/admin/fault` normal -> independent `/health` and `/probe`; success requires health normal, HTTP 200, and latency <1000 ms. Persist lifecycle event records.

**Source:** `approval.py:27-149`; `live_monitoring.py:471-582,1043-1241`; `collectors/system_metrics.py:21-47`.

**Trust/human boundary:** draw a human-labelled approval input, but mark it **unauthenticated audit label**. The only action box must be `clear_demo_service_fault` in local demo scope.

## 6. Experimental design and evidence boundaries

Use separate non-overlapping panels:

- **A — evaluated synthetic detection:** frozen 24-step model; 320 windows; 200 normal and 120 fault; six scenarios x 20. Mark clustered/dependent windows and prohibit live-rate translation.
- **B — exploratory diagnosis pilot:** seven configurations x six scenarios; distinguish offline deterministic from Groq modes; show two `UNASSESSABLE` API omissions; do not use superiority arrows.
- **C — local safety harness:** 16 records: 11 attack, 2 precondition, 2 positive control, 1 verification. Mark local demo boundary.
- **Live record:** 200 local records; bootstrap rules; 200 null LSTM scores; operational demonstration only.
- **D — external AnoMod:** archive/provenance present, but 24-step compatibility and calibration blockers; no production outputs. Draw as blocked, not as a performance-evaluation result.

**Supporting sources:** `PHASE2_METRIC_RECONCILIATION.md`, `PHASE2_STATISTICAL_VERIFICATION.md`, `PHASE3_IMPLEMENTATION_ARCHITECTURE_AUDIT.md`, frozen metadata, and D compatibility audits. Never merge panels, denominators, dates, or snapshot copies.
