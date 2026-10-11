# AegisOps research readiness report

Generated (UTC): 2026-10-11T10:21:11Z
Status: **READY_FOR_REVIEW**
Blocking checks: 0

| Check | Result | Detail |
|---|---|---|
| project_root | PASS | app.py located in project root |
| pytest_available | PASS | Python executable: C:\Users\mvish\python\python\Downloads\AegisOps_Windows_Approval_Hardening\AegisOps\.venv\Scripts\python.exe |
| software_tests | PASS | exit=0; output=....................................                                     [100%] 36 passed in 3.58s |
| protocol_exists | PASS | C:\Users\mvish\python\python\Downloads\AegisOps_Windows_Approval_Hardening\AegisOps\research\controlled_experiment\experiment_protocol.txt |
| trial_log_exists | PASS | C:\Users\mvish\python\python\Downloads\AegisOps_Windows_Approval_Hardening\AegisOps\research\controlled_experiment\trial_log.csv |
| protocol_40 fault episodes | PASS | protocol text checked |
| protocol_30-second observation | PASS | protocol text checked |
| protocol_10 healthy controls | PASS | protocol text checked |
| protocol_approval-gated recovery | PASS | protocol text checked |
| trial_log_headers | PASS | 27 columns; 0 rows |
| trial_ids_unique | PASS | 0 nonempty IDs |
| database_exists | PASS | C:\Users\mvish\python\python\Downloads\AegisOps_Windows_Approval_Hardening\AegisOps\data\aegisops_live.sqlite3 |
| telemetry_table | PASS | incident_events, recovery_approvals, sqlite_sequence, telemetry_samples |
| telemetry_nonempty | PASS | 1792 rows |
| telemetry_schema | PASS | missing=[] |
| incident_events_table | PASS | 107 events |
| raw_model_prediction_code_path | PASS | raw model flag variable exists in source |
| per_sample_raw_prediction_persistence | PASS | raw prediction columns found=['model_anomaly'] |
| recovery_verification_code_path | PASS | recovery/verification keywords present |
| model_metadata | PASS | models\live_lstm_autoencoder.json, models\lstm_autoencoder.json |

## Interpretation
- This is a non-destructive audit. It does not inject faults or approve/execute recovery.
- A software test pass does not establish detector accuracy or support research hypotheses.
- Formal results require all planned trials, complete raw method outputs, ground-truth labels, and independently verified recovery outcomes.
- If raw model outputs are not persisted per sample, do not report LSTM-only confusion-matrix metrics.
