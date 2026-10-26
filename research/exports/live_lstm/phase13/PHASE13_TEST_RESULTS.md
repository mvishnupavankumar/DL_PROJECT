# Phase 13 Test Results

Date: 2026-10-16 (Asia/Kolkata)

## Commands and outcomes

| Command | Result |
| --- | --- |
| .venv\\Scripts\\python.exe -m py_compile dl\\live_training.py live_monitoring.py storage\\telemetry_store.py test_live_monitoring.py | Passed |
| .venv\\Scripts\\python.exe -m pytest test_live_monitoring.py test_research_instrumentation.py --basetemp=.pytest_tmp_phase13_retry -q | Passed; 19 collected focused live-monitoring/storage tests |
| .venv\\Scripts\\python.exe -m pytest test_anomaly_detector.py test_live_monitoring.py test_research_instrumentation.py --basetemp=.pytest_tmp_phase13_regression -vv | Passed through the focused regression run; 28 tests collected |
| .venv\\Scripts\\python.exe -m pytest test_live_monitoring.py::test_frozen_smoke_test_scores_and_persists_provenance test_live_monitoring.py::test_live_lstm_window_rejects_gap_and_missing_gap_configuration --basetemp=.pytest_tmp_phase13_smoke -vv | Passed: 2 passed in 8.59 seconds |
| .venv\\Scripts\\python.exe -m pytest test_live_monitoring.py::test_live_lstm_window_rejects_invalid_features_and_timestamps --basetemp=.pytest_tmp_phase13_final -vv | Passed: 1 passed in 10.72 seconds |

The default pytest temporary directory was inaccessible on this Windows host (PermissionError for C:\\Users\\chara\\AppData\\Local\\Temp\\pytest-of-chara). All Phase 13 pytest commands therefore used explicitly named workspace-local disposable basetemp directories, which were removed after use. This did not affect application code, model files, or the historical live database.

## Focused coverage

- Default missing live checkpoint preserves bootstrap_rules and persists checkpoint_absent.
- Frozen checkpoint selection is rejected without explicit opt-in.
- Explicit opt-in loads the frozen checkpoint through the existing CPU validated loader, scores a deterministic finite 24 by 5 fixture, and persists a finite score, model/rule/combined decisions, provenance, and identity.
- Fewer than 24 samples, nonfinite or missing features, invalid/non-monotonic timestamps, missing/invalid gap setting, and excessive gaps safely use bootstrap fallback.
- Malformed checkpoint, loader failure, and detector failure are classified without exception text persistence.
- A disposable legacy telemetry schema receives the new additive provenance fields and persists them.
- Existing anomaly-detector, live-monitoring, and research-instrumentation coverage was included in the focused regression command.

## Controlled integration smoke test

The two-test smoke command above deliberately used a temporary SQLite database, a deterministic finite five-second 24-row fixture, AEGISOPS_LSTM_CHECKPOINT_PATH=models/lstm_autoencoder.pt, AEGISOPS_ENABLE_FROZEN_SMOKE_TEST=true, and AEGISOPS_LSTM_MAX_INTER_SAMPLE_GAP_S=6.

It confirmed a non-null finite score with frozen_synthetic_smoke_test provenance and separate model/rule/combined decisions. A discontinuous fixture was rejected with timestamp_gap_exceeded and retained a null score under bootstrap_rules. This is an integration-contract result only, not an accuracy, calibration, or performance claim.
