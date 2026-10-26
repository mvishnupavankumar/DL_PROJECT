# AegisOps Live LSTM Repair and Validation Plan

**Status:** Proposed only. This document authorizes no implementation, model training, threshold change, telemetry modification, or performance experiment.

## Goal

Enable an auditable live-inference integration path while preserving the existing safe default: bootstrap rules remain active unless an approved checkpoint is explicitly selected and passes contract checks. The existing frozen checkpoint can be used for a technical integration smoke test without retraining, but it must remain identified as synthetically trained and must not be described as a calibrated live model or as live-performance evidence.

## Minimal repair set

### 1. Make checkpoint selection explicit and provenance-preserving

**Files:** dl/live_training.py, live_monitoring.py, .env.example, and focused tests.

1. Keep models/live_lstm_autoencoder.pt as the default live-trained checkpoint.
2. Add a narrowly scoped configuration for an inference checkpoint path. Its unset/default state must preserve current live-checkpoint-only behavior.
3. Require a separate explicit opt-in before models/lstm_autoencoder.pt is accepted, because that artifact was trained and calibrated on synthetic windows.
4. Surface selected checkpoint path, checkpoint data source, feature contract, sequence length, threshold, and selection mode in the UI and a durable event payload.
5. Load through the existing TelemetryAnomalyDetector.load(path) routine, which already uses CPU, weights_only loading, checkpoint feature order, checkpoint scaler, and checkpoint threshold.

No architecture, weights, scaler, threshold, or decision-equation change is required. The confirmed defect is path/policy selection, not checkpoint incompatibility.

### 2. Add a temporal-window admission rule

**Files:** live_monitoring.py, optionally a small pure helper, and focused tests.

1. Parse timestamps before constructing a model window and require monotonic, finite values.
2. Require every inter-sample gap in the candidate 24-row window to be at or below a documented configured maximum. The intended cadence is five seconds; the exact tolerance must be approved, documented, and tested rather than inferred from the historical file.
3. When a window fails, defer or reset model scoring and persist a distinct state such as bootstrap_rules_window_not_ready.
4. Do not impute, resample, reorder by timestamp, or bridge gaps without a separately approved protocol.

This is necessary because the current path uses insertion order without checking time continuity, while the historical session has gaps from 0.578 to 6170.223 seconds.

### 3. Preserve fallback observability and prediction provenance

**Files:** live_monitoring.py, storage/telemetry_store.py, and migration-focused tests.

1. Distinguish checkpoint absent, selection rejected, insufficient rows, invalid/nonfinite feature, discontinuous window, checkpoint-load failure, inference failure, and successful score.
2. Write a compact sanitized fallback event that records reason and checkpoint identity; do not store secrets or unbounded exception content.
3. For success, persist score, model-only decision, rule-only decision, combined decision, detector mode, and checkpoint/provenance identifier.
4. Test the existing migration route on a disposable legacy-schema database. Do not rewrite the historical live database.

Keep the existing rule guardrails and OR decision as separate fields. A guardrail-only alert must not be labelled a model detection.

## Focused validation plan

### A. Unit and component tests

1. With no live checkpoint, select bootstrap rules and persist checkpoint_absent.
2. With an explicit frozen-checkpoint opt-in, load the frozen file strictly on CPU and score a valid finite 24-by-5 fixture through TelemetryAnomalyDetector.detect.
3. Reject the frozen path when opt-in is absent.
4. Verify distinct fallback states for wrong feature order, wrong width, fewer than 24 rows, nonfinite feature, malformed checkpoint, missing checkpoint fields, and load exception.
5. Verify a five-second 24-row fixture is eligible and that a timestamp gap above the approved maximum defers or resets model scoring.
6. Verify successful model scoring writes a non-null score and separate model/rule/combined values.
7. Retain current temporary live-training/load coverage in test_live_monitoring.py and extend it with selection and continuity cases.

Use temporary databases and deterministic fixtures. These tests are integration-contract tests, not performance experiments, and must not alter the historical database, frozen checkpoint, or exports.

### B. Limited integration smoke test after implementation

1. Use a new disposable telemetry database and a controlled finite cadence-valid 24-row fixture.
2. Select the frozen checkpoint only through explicit opt-in.
3. Verify a non-null score, provenance-aware detector mode, checkpoint identifier, and separate model/rule/combined decisions.
4. Verify a discontinuous timestamp fixture avoids model scoring and records its reason.
5. Record this only as an integration smoke test. Do not calculate accuracy, precision, recall, false-positive rate, or alarms per hour.

### C. Prospective live evaluation prerequisites

1. Collect a new provenance-recorded stream with continuous cadence, explicit target/collector topology, and model-score provenance.
2. Keep integration testing separate from any calibration/retraining study. A newly trained live model creates a distinct model, scaler, threshold, and study; it is not frozen-checkpoint validation.
3. Prespecify independent adjudication, incident onset/offset, normal/fault partitions, temporal splits, sample/episode units, and exposure denominators.
4. Obtain enough independently labelled, disjoint windows or episodes for the approved evaluation protocol.

The current 200-row file is unsuitable for performance evaluation: it has no LSTM scores, irregular timing, and a long injected error episode rather than independent operational events.

## Owner decisions needed

1. Whether the frozen synthetic checkpoint is permitted only for an integration smoke test or may appear in the live UI with a synthetic-calibration warning.
2. The timestamp-gap tolerance and reset policy for the intended five-second cadence.
3. Checkpoint/fallback event retention and provenance format.
4. The prospective labelled evaluation protocol and ground-truth authority.

## Explicit non-actions

- Do not copy, rename, or overwrite models/lstm_autoencoder.pt as models/live_lstm_autoencoder.pt. That would erase the synthetic-versus-live provenance distinction.
- Do not lower the 180-sample gate, bypass healthy-row selection, retrain on the present mixed session, or alter thresholds merely to score existing rows.
- Do not backfill historical null scores or retroactively call bootstrap alerts LSTM detections.
- Do not calculate live performance from the current telemetry export or local injection annotations.
