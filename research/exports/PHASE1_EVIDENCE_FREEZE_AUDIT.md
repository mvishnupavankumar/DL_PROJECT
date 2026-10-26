# AegisOps Phase 1 Evidence Freeze Audit

**Audit timestamp:** 2026-10-15 (Asia/Kolkata)  
**Scope:** Read-only inspection of the checked-out repository and locally available artifacts. This report is the only newly created file. No experiment, model, dataset, manuscript, threshold, database, API, or historical report was changed or executed.

## Verdict

**B. Inventory completed but critical artifacts remain unverified.**

The repository and primary evidence are accessible and have been inventoried. Critical limits prevent a fully verified evidence inventory: the named uploaded manuscript `AegisOps_Research_Paper_Professional_v2.docx` is not present in the workspace or supplied attachment folder; the integrity manifest is stale for seven of its 22 entries; the worktree is not clean; and neither live LSTM inference evidence nor production Experiment D outputs exist.

## 1. Repository identity and snapshot boundary

| Field | Observed value |
| --- | --- |
| Repository root | `C:\DL_PROJECT` |
| Branch | `publish/research-without-external-dataset` |
| HEAD | `a32713c30a8ddca1425d44b1afbaf6d55a64c276` |
| HEAD subject | `Publish AegisOps research without external dataset payload` |
| Recent commits | `a32713c`, `d277c1d`, `ec83d2f`, `e7b8d58`, `8aff34c`, `11cf0c7`, `e69cb62`, `ce1a4cc` |
| Index | No staged entries observed. |
| Working tree | 56 porcelain entries: 40 modified and 16 untracked. |
| Current-state rule | Files in the checked-out worktree are the snapshot observed here. A historical narrative or Git-tracked status alone does not make an artifact authoritative. |

The dirty worktree includes manuscript, audit, experiment, raw/derived CSV, and code changes. Therefore this snapshot must not be represented as the committed `HEAD` state. Key untracked release/audit artifacts include `research/exports/LIVE_DATA_AND_EXTERNAL_VALIDATION_AUDIT.md`, `research/paper/CANONICAL_METRIC_RECONCILIATION.md`, and `research/exports/AegisOps_PreSubmission_Evidence_Pack.zip`.

## 2. Inventory method and classification

SHA-256 was calculated directly for the major artifacts below. The full `research/` tree contains 225 files classified as: 105 audits/reports (1,239,079 bytes), 24 experiment protocol/code/report files (459,048 bytes), 18 manuscript/supporting files (330,469 bytes), 13 exports (529,743 bytes), 7 raw-evidence files (42,204 bytes), 18 derived-result files (122,059 bytes), 3 figure/source files (63,041 bytes), 4 historical-backup files (41,569 bytes), and 37 other research files (294,229 bytes). The large unpacked AnoMod source tree is represented by its extraction manifest rather than individually repeated in this report.

Status labels:

- **Verified current:** present and hash checked in this audit; it may still be bounded in scientific use.
- **Current but unmanifested:** present and hash checked, but not covered by the frozen manifest.
- **Historical/superseded:** retained provenance, not a source for current metrics without raw-record confirmation.
- **Absent:** expected by code or requested for comparison, but not available in this snapshot.

## 3. Major artifact inventory

| Class and verification status | Exact path | Bytes | Modified (UTC+05:30) | SHA-256 |
| --- | --- | ---: | --- | --- |
| Current manuscript source, unverified against requested DOCX | `research/paper/AEGISOPS_RESEARCH_PAPER.md` | 86,968 | 2026-10-15 05:32:37 | `bbef85b625495b80a3e01e322e75fc8c8d8bdf7644eaa76b40e22867ae9e172f` |
| Current reconciliation narrative, untracked | `research/paper/CANONICAL_METRIC_RECONCILIATION.md` | 27,621 | 2026-10-15 05:20:54 | `d3f1509152e56dc0c446275bac1d20f9210e430c4e2564d62dc6ed1ebd791cff` |
| Historical final-evidence audit, explicitly superseded in-file | `research/paper/FINAL_EVIDENCE_AUDIT.md` | 27,816 | 2026-10-15 05:20:42 | `14501bfc27601bf11f8ffd88c6dc8df0974a873b4c38cc45d296b59e37551f6a` |
| Latest live-data audit, untracked | `research/exports/LIVE_DATA_AND_EXTERNAL_VALIDATION_AUDIT.md` | 18,673 | 2026-10-15 08:18:06 | `c5928b43b3de2527a8b0b758d011583ac75542c27873b07a6773a0b44d876832` |
| Experiment A report, historical projection superseded | `research/experiments/EXPERIMENT_A.md` | 4,151 | 2026-10-15 05:19:28 | `37338f087aeb4a148fee640e84cb4055c1411c43aa54937c6d504b91260fa056` |
| Experiment B report, historical table superseded | `research/experiments/EXPERIMENT_B.md` | 5,168 | 2026-10-14 21:41:51 | `1d48f4ecf9e70c75ba9f1f3f3549a8241a359eab12609b636d4e881b6fa2efc9` |
| Experiment C report, historical table superseded | `research/experiments/EXPERIMENT_C.md` | 7,023 | 2026-10-14 21:41:58 | `5841d6208b60e8019a33f227d16781ddd21799cc56c2cb3e0993df011a65cc82` |
| A raw predictions, verified current | `research/raw/detection_predictions.csv` | 24,357 | 2026-10-12 08:17:39 | `246e14f8b84b8b89cbfce180fd7722ae82820f516894aa5dd11462866d10cfbb` |
| A metrics, verified current | `research/raw/detection_metrics.csv` | 568 | 2026-10-12 08:17:39 | `ed5775303f74156d844dc0068db4328e2237fc935a2bca260d613571083de57e` |
| A scenario metrics, verified current | `research/raw/detection_by_scenario.csv` | 280 | 2026-10-12 08:17:39 | `7bc8400653683465f8f25af7d60398ae892831b4b3038ac5b7933478103bebf9` |
| B raw predictions, current but manifest mismatch | `research/raw/diagnosis_predictions.csv` | 11,982 | 2026-10-13 17:02:41 | `d43e43370349a1d005cd7de14aa1488486780fc459c2f796559241137b7d1a68` |
| B metrics, current but manifest mismatch | `research/raw/diagnosis_metrics.csv` | 862 | 2026-10-13 17:02:41 | `79bf2f53fb0de1c6d24afcb88b475e48c78e8cedd27d45ac051d948d505fc307` |
| C test observations, current but manifest mismatch | `research/raw/safety_test_results.csv` | 3,029 | 2026-10-13 17:06:22 | `19391636c705166981b56120835b2b0a0b12218defaeffc899474acb8f220985` |
| C metrics, current but manifest mismatch | `research/raw/safety_metrics.csv` | 1,126 | 2026-10-13 17:06:48 | `08145f57939c33f8b3db4b017e0833cbfda84a5678f13c54a837ff1335ec0b9a` |
| Derived statistics, not raw evidence | `research/results/statistical_analysis.md` | 9,049 | 2026-10-14 13:08:40 | `fe401d2a1dd1f28636cb2f1a64198b232f46f72ff215b14e4a29c48cb8108d74` |
| Frozen weights, verified current | `models/lstm_autoencoder.pt` | 19,797 | 2026-10-11 12:08:42 | `1cf44e6e82e459f543fcace25334f3076b76c77a357d46f65c11e3c44fd382de` |
| Frozen metadata/scaler/threshold, verified current | `models/lstm_autoencoder.json` | 846 | 2026-10-11 12:08:42 | `24826b053833b08e80fb84e7e694adfad5b4a1124d935ccf3e3cd4f575eb045f` |
| Live collection database, verified current | `data/aegisops_live.sqlite3` | 86,016 | 2026-10-11 15:45:38 | `b8f33f63fef6e781fbf7ba45045d8ba5e5eaab3c041fa85250d71ae276c484d7` |
| Safety fixture database | `data/safety_telemetry.sqlite3` | 20,480 | 2026-10-12 14:14:32 | `08618f9c4cf0e91a16de1240463fe40ddc8deaa7813a24cf6f2f309472d6a889` |
| Safety fixture database | `data/safety_test_store.sqlite3` | 16,384 | 2026-10-12 14:14:26 | `1fe9da1951d3ceb97e43dcf10e965e80ff5e69e62d6f6303b074fcb4ffd939b0` |
| AnoMod archive, hash-verified present | `data/external/anomod/AnoMod.zip` | 201,917,396 | 2026-10-13 16:10:41 | `5086808ff4f2039b88c106cd996f4b9a7148675e20f66ee1718c511b95eb120a` |
| AnoMod acquisition provenance | `data/external/anomod/transfer_provenance.json` | 704 | 2026-10-13 16:10:41 | `e4f4af54a6803911701f824f57fc5fa61a300902b2763c1cfb6488215c20eebd` |
| AnoMod extraction manifest | `data/external/anomod/unpacked/extraction_manifest.json` | 11,504,622 | 2026-10-13 16:12:05 | `213779192db365b5ca7997a24937ed17bf34bd40e26da99dbbe2f010b8d44335` |
| Detection comparison figure | `research/figures/detection_comparison.png` | 21,442 | 2026-10-12 14:14:10 | `ad1935fa98d5a48f5d02cc88a09679cf7d87f4931629c6114310c9ae8a060b7b` |
| Detection confusion figure | `research/figures/detection_confusion_matrices.png` | 35,301 | 2026-10-12 14:14:10 | `0784db0ef9c62667f403f243b52fd99c4689f7404de5e207bf73c5699e1f0337` |
| Live telemetry export, operational demonstration only | `research/exports/telemetry.csv` | 29,062 | 2026-10-12 07:22:56 | `0a17468699ad918ffcd98af2d77982e7283206d73de3f5d838b0347db6c493a5` |
| Live event export | `research/exports/incident_events.csv` | 12,942 | 2026-10-12 07:22:56 | `55e35a50aea157de7d698543c95604ccb47196cd2bdb8d4688f2a1c0e5e16735` |
| Local episode export | `research/exports/incident_episodes.csv` | 1,340 | 2026-10-12 07:22:56 | `de08f88a352f9a51a797c7e2ded4a2dd164ef7d70967c09db7bba4f4ee9826fe` |
| Frozen integrity manifest, stale | `research/MANIFEST_SHA256.json` | 4,847 | 2026-10-12 14:14:36 | `659fd33091b3c45405df166adf2fc5da178e00fed52babf8f095709f4c15948a` |

## 4. Authoritative evidence map

| Topic | Raw observations | Derived metrics/figures | Narrative or historical records | Current evidence determination |
| --- | --- | --- | --- | --- |
| Experiment A: synthetic anomaly detection | `research/raw/detection_predictions.csv`, with companion metric/scenario CSVs | `research/results/statistical_analysis.md`, detection figures | `EXPERIMENT_A.md`, `FINAL_EXPERIMENT_REPORT.md`, older audits | Raw prediction CSV and frozen model metadata are authoritative for the synthetic benchmark only. `raw/` and `results/` A CSVs are bit-identical, as is the backup copy. |
| Experiment B: diagnosis pilot | `research/raw/diagnosis_predictions.csv`, `diagnosis_metrics.csv` | same-named mirrors in `research/results/` | `EXPERIMENT_B.md`, reconciliation narratives | Current `raw/` and `results/` are bit-identical and prevail over `backup_prior_outputs/`, whose B CSVs differ. The manifest must be refreshed before calling this integrity-verified. |
| Experiment C: safety boundary | `research/raw/safety_test_results.csv`, `safety_metrics.csv` | matching `results/` mirrors | `EXPERIMENT_C.md`, `SAFETY_EVALUATION.md` | Current raw/result pairs are bit-identical. The Experiment C report explicitly says its historical table is superseded; use raw CSVs with the reconciliation document, subject to manifest refresh. |
| Experiment D: AnoMod | AnoMod archive, provenance, extraction manifest; no predictions or metrics | No production metrics or figures | protocol, readiness, compatibility, calibration, and supervisor-decision audits | The archive is a verified input asset, not evaluation evidence. Production result artifacts are absent and the decision package blocks execution. |
| Live telemetry | `data/aegisops_live.sqlite3`; CSV exports | local event/episode summaries | live-data audit | Supports collector, rule fallback, alert transition, and logging demonstration only; it is not independent labeled performance evidence. |
| Frozen model | `models/lstm_autoencoder.pt` and `.json` | N/A | model/execution audits | Checkpoint and metadata match the old manifest. Metadata records the synthetic 24-step feature contract and threshold `0.7093990445137024`. |

No counts were combined across raw/results copies, historical backups, dates, database snapshots, Git commits, or live/export records.

## 5. Evidence status by required area

### Experiment A — Synthetic

**Verified current, bounded.** The raw prediction set has 320 rows (200 nominal and 120 fault windows per the current reconciliation) and is hash-consistent with all three A copies. It supports only the defined synthetic benchmark. It does not validate continuous/live false-alarm rates: `EXPERIMENT_A.md` expressly supersedes its historical alarms-per-hour projections.

### Experiment B — Diagnosis

**Current raw evidence present; integrity manifest stale.** Current raw and result CSV pairs contain 42 data rows (43 lines including header) for 7 configurations x 6 scenarios. The report marks two API-rate-limit omissions as `UNASSESSABLE`; older summaries are not authoritative for the current count/accuracy. The historical backup has differing B content and must not be merged.

### Experiment C — Safety

**Current raw evidence present; integrity manifest stale.** Current raw and result pairs contain 16 test rows (17 lines including header). The report itself supersedes its old table and identifies the raw safety files plus current reconciliation as the proper source. Safety databases are fixtures and not live detection evidence.

### Experiment D — AnoMod

**Input archive verified; production evaluation absent and blocked.** `run_experiment_d.py` declares expected production outputs `research/raw/external_anomod_predictions.csv`, `research/raw/external_anomod_metrics.csv`, `research/audits/EXPERIMENT_D_RESULTS.md`, and `research/audits/experiment_d_manifest.json`; none exists. `research/audits/PROTOCOL_AMENDMENT_V1_2_RATIFICATION.json` is also absent. Existing audits report zero valid finite contiguous 24-step nominal windows, an off-contract 8-step path, and circular target-calibration/evaluation leakage. Preflight diagnostics are not production Experiment D results.

### Live telemetry collection

**Verified as local operational demonstration only.** The current live audit records 200 telemetry rows, local/injected subsets, irregular collection gaps, self-authored operational episode annotations, and bootstrap-rule detection. This is not an independently adjudicated live detection study.

### Live LSTM inference

**Absent.** `models/live_lstm_autoencoder.pt` and associated metadata are absent. The live audit records `detector_mode=bootstrap_rules` for all 200 rows and null `anomaly_score` for all 200 rows. Do not infer live LSTM accuracy, scoring, or generalization.

## 6. Duplicates, stale records, contradictions, and missing artifacts

### Duplicate or parallel artifacts

- Experiment A raw, result, and `backup_prior_outputs/results/` CSV triplets are byte-identical. They are duplicates, not independent replications.
- B and C `raw/` and `results/` pairs are byte-identical; their corresponding `backup_prior_outputs/results/` files have different hashes and fewer rows. Backups are historical, not additional observations.
- Detection figures appear both under `research/figures/` and `research/paper/figures/` with identical hashes; they are duplicate renderings/placements.
- Root `audits/` and `research/audits/` are parallel audit trees. They require a future identity/provenance decision before either can be designated as a unique master archive.

### Verified contradictions or staleness

- The manifest dated 2026-10-12 matches **15/22** entries, not all entries. These seven entries mismatch its recorded bytes and SHA-256: `research/STATISTICAL_AUDIT.md`, `research/SAFETY_EVALUATION.md`, `research/FINAL_EXPERIMENT_REPORT.md`, `research/raw/diagnosis_metrics.csv`, `research/raw/diagnosis_predictions.csv`, `research/raw/safety_metrics.csv`, and `research/raw/safety_test_results.csv`.
- The current canonical reconciliation's assertion of 17 matching manifest entries is itself stale relative to this snapshot; direct hash verification returned 15 matching entries.
- Historical Experiment A, B, and C report tables each contain explicit supersession language. They cannot override current raw data.
- `FINAL_EVIDENCE_AUDIT.md` retains a historical readiness verdict but explicitly states that its original readiness language is superseded by a current not-ready release state.
- `README.md` appears in Git's diff as a binary change, an unusual condition that should be checked before any release process; it was not altered here.

### Missing or inaccessible

- `AegisOps_Research_Paper_Professional_v2.docx` was not found in the workspace or `C:\Users\chara\.codex\attachments\dd395b34-0508-480a-ad2f-75f14844eed2`. That folder contains only `pasted-text.txt`. No DOCX-to-repository comparison was possible.
- Experiment D production predictions, metrics, result report, manifest, and ratification record are absent as listed above.
- No live LSTM checkpoint/metadata or non-null live LSTM score record is available.
- This audit did not run test suites, render documents, run database-mutating tools, execute model inference, or invoke network/external APIs. Those were intentionally unavailable to this read-only phase, not silently treated as successful verification.

## 7. Traceability from manuscript sections to evidence

| Manuscript topic/section class | Evidence that may support it | Constraint |
| --- | --- | --- |
| System architecture and frozen model contract | `models/lstm_autoencoder.json`, `.pt`, `dl/anomaly_detector.py`, manuscript figure sources | Architecture claims are checkable; live deployment claims are not supported by the current live record. |
| Synthetic detection results | A raw prediction/metric/scenario CSVs; matching detection figures | State 24-step synthetic-window scope. Do not state live rate metrics. |
| Diagnosis pilot and ablations | B current raw CSVs and canonical reconciliation | Preserve six-scenario, seven-configuration scope and `UNASSESSABLE` omissions. |
| Safety boundary tests | C current raw CSVs and canonical reconciliation | Bound claims to the local application/runtime test suite; distinguish test fixtures from production telemetry. |
| Statistical analysis | Raw A/B/C inputs plus `research/results/statistical_analysis.md` | Derived calculations require re-check after integrity-manifest repair; do not rely on historical totals. |
| Live operational demonstration | live SQLite database plus three CSV exports | Supports collection/logging/rule-fallback behavior only. |
| External validation or transfer | AnoMod archive/provenance and D-blocking audits | No valid Experiment D outcome exists. Describe only data availability and protocol incompatibility. |
| Figures/tables | hash-listed figure files and Markdown/mermaid sources | Figure placement/caption/release suitability is not established by file presence alone. |

## 8. Recommended resolution order

1. Freeze or explicitly version the current dirty worktree; do not blend it with `HEAD` or historical backup snapshots.
2. Reconcile the 22-entry integrity manifest against the chosen current evidence set, preserving old manifest provenance rather than overwriting it without a versioned replacement.
3. Select one raw/result canonical location for A/B/C and label all duplicates and `backup_prior_outputs` as mirrors or historical copies.
4. Obtain the exact requested `AegisOps_Research_Paper_Professional_v2.docx`, then perform a page/text/table comparison against the frozen Markdown manuscript and live-data audit.
5. Resolve manuscript/report supersession references and release-gate contradictions before any correction work.
6. Keep Experiment D and live LSTM claims blocked unless separately authorized, contract-valid artifacts are produced under an amended protocol; this report neither authorizes nor performs that work.

## 9. Verification limitations

This is a file-system and repository-state freeze, not a rerun of experiments. Hash equality establishes byte identity, not scientific correctness. Database, CSV, source, and historical-audit contents were inspected without changing them. The inability to compare the absent DOCX and the deliberate prohibition on running experiments are material limitations. No external API, dataset download, model training, inference run, regeneration, deletion, rename, or overwrite occurred.

**Final verdict: B. Inventory completed but critical artifacts remain unverified.**
