# Phase 13 Evidence Preservation

## Preserved items

- The frozen synthetic checkpoint and metadata were read only. Their end-of-phase SHA-256 values are respectively 1CF44E6E82E459F543FCACE25334F3076B76C77A357D46F65C11E3C44FD382DE and 24826B053833B08E80FB84E7E694ADFAD5B4A1124D935CCF3E3CD4F575EB045F.
- models/live_lstm_autoencoder.pt remained absent. The repair does not copy, rename, or synthesize it.
- data/aegisops_live.sqlite3 was not opened by TelemetryStore during this phase, migrated, or backfilled. Its end-of-phase SHA-256 is B8F33F63FEF6E781FBF7BA45045D8BA5E5EAAB3C041FA85250D71AE276C484D7.
- Phase 1 through Phase 12 evidence reports, the root-cause audit, manuscripts, and historical manifests were not edited.
- All inference and migration validation used test-owned SQLite files below workspace-local pytest temporary directories; those directories were removed after validation.

## Explicit non-actions

No training, retraining, threshold adjustment, scaler update, feature reordering, synthetic-data change, telemetry edit, historical-score backfill, performance experiment, performance metric calculation, commit, reset, clean, stash, or release-manifest rewrite was performed.

## Remaining evidence boundary

The successful smoke test proves that the repaired integration path can invoke the existing frozen checkpoint on an intentionally selected valid fixture. It does not establish live calibration, operational performance, or clinical or production readiness. Any future performance study needs a separately specified prospective stream, independent labels, exposure definition, and approved evaluation design.
