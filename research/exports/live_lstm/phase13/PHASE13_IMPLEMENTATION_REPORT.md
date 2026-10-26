# Phase 13 Live LSTM Integration Repair

Date: 2026-10-16 (Asia/Kolkata)

## Scope and baseline

This phase implemented the minimum live-inference integration repair from the Phase 13 request and the preceding root-cause audit. It did not train a model, change model weights, scalers, thresholds, feature order, decision fusion, research artifacts, manuscripts, historical manifests, or the historical telemetry database.

| Baseline item | Value |
| --- | --- |
| Branch | publish/research-without-external-dataset |
| HEAD before implementation | a32713c30a8ddca1425d44b1afbaf6d55a64c276 |
| Initial working tree | 85 porcelain entries: 40 modified paths and 45 untracked paths |
| Historical live database | data/aegisops_live.sqlite3, SHA-256 B8F33F63FEF6E781FBF7BA45045D8BA5E5EAAB3C041FA85250D71AE276C484D7 |
| Frozen checkpoint | models/lstm_autoencoder.pt, SHA-256 1CF44E6E82E459F543FCACE25334F3076B76C77A357D46F65C11E3C44FD382DE |
| Live-trained checkpoint at start/end | models/live_lstm_autoencoder.pt absent |

The pre-existing dirty working tree was preserved. Immediately before writing these Phase 13 records, it had 90 porcelain entries: 45 modified paths and 45 untracked paths. The five Phase 13 code/configuration changes account for the added modified paths. No reset, clean, stash, commit, model write, or historical database migration was performed.

## Implemented behavior

- dl/live_training.py now selects only the production live path by default: models/live_lstm_autoencoder.pt.
- A configured frozen path is accepted only when AEGISOPS_LSTM_CHECKPOINT_PATH names models/lstm_autoencoder.pt and AEGISOPS_ENABLE_FROZEN_SMOKE_TEST is true. Any other configured path is rejected. There is no automatic fallback to the frozen checkpoint.
- Each selection records bounded provenance: live_trained, frozen_synthetic_smoke_test, or unapproved_checkpoint. The checkpoint identity is filename plus a shortened SHA-256 prefix when readable.
- A positive finite AEGISOPS_LSTM_MAX_INTER_SAMPLE_GAP_S is required before inference. No operational gap value is hard-coded or supplied by default.
- The 24-row candidate window is admitted only when feature values are finite and correctly shaped, timestamps are timezone-aware and strictly increasing, and every inter-sample gap is within the configured limit. It does not reorder, interpolate, resample, impute, or reuse a score.
- Bootstrap rules remain the safe fallback. The UI now displays inference state, provenance, and checkpoint identity, and the telemetry table can show these fields.
- TelemetryStore now migrates, in a database it opens, three nullable fields: inference_reason, checkpoint_provenance, and checkpoint_identity. The Phase 13 tests exercised this only on temporary databases.

## Final reason-code vocabulary

checkpoint_absent, checkpoint_selection_rejected, insufficient_rows, invalid_features, window_not_ready, timestamp_gap_exceeded, checkpoint_load_failure, inference_failure, and inference_success.

The storage layer rejects any other non-null code. Fallback warnings are sanitized fixed text and do not persist exception details.

## Code locations

| File | Main locations | Purpose |
| --- | --- | --- |
| dl/live_training.py | 16-94 | explicit bounded selection, checkpoint identity, and gap setting parser |
| live_monitoring.py | 146-291 | temporal admission, safe fallback persistence, CPU loader invocation, scoring/fusion persistence |
| live_monitoring.py | 738-742, 858-873 | live UI provenance display and export columns |
| storage/telemetry_store.py | 11-82, 134-167 | bounded code vocabulary and additive schema migration/persistence |
| .env.example | 22-29 | documented settings with no default approved gap |
| test_live_monitoring.py | 16-359 | deterministic temporary-store contract and migration coverage |

## Configuration

| Setting | Default/safe effect |
| --- | --- |
| AEGISOPS_LSTM_CHECKPOINT_PATH | Empty selects only models/live_lstm_autoencoder.pt |
| AEGISOPS_ENABLE_FROZEN_SMOKE_TEST | false; required for frozen synthetic checkpoint selection |
| AEGISOPS_LSTM_MAX_INTER_SAMPLE_GAP_S | Empty; scoring is refused until a positive finite owner-approved limit is supplied |

## Limits retained

This is an integration repair, not live-performance validation. The frozen checkpoint remains synthetic-calibrated and is permitted only for explicit smoke testing. The historical 200-row bootstrap-rule dataset was not scored, backfilled, migrated, or treated as model evidence. Prospective labelled evaluation data and an owner-approved operational gap tolerance are still required.
