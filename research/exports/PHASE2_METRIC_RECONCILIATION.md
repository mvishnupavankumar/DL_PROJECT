# AegisOps Phase 2 Authoritative Metric Reconciliation

**Audit date:** 2026-10-15 (Asia/Kolkata)  
**Scope:** Recalculation from the frozen Phase 1 input snapshot only. This is a metrics audit, not an experiment. No raw input, model, threshold, database, manuscript, historical report, dataset, or result was changed.

## Decision

The current raw files support a bounded, reproducible set of synthetic detection, diagnosis-pilot, and local safety-harness results. They do **not** support a live LSTM performance claim, alarms-per-hour claim, independently adjudicated live-detection claim, or external AnoMod performance result. The evidence is sufficiently reconciled to proceed to Phase 3 **only with those boundaries retained and the stale manifest handled as a versioned integrity issue**.

## 1. Freeze check and reproducibility

Every Phase 2 input hash equals the value recorded in `research/exports/PHASE1_EVIDENCE_FREEZE_AUDIT.md`; no source changed between phases. The deterministic audit script is `research/audits/phase2_metric_reconciliation/reconcile_metrics.py` and uses only Python's standard library.

Run from the repository root:

```powershell
.venv\Scripts\python.exe research\audits\phase2_metric_reconciliation\reconcile_metrics.py
```

| Input | SHA-256 |
| --- | --- |
| `research/raw/detection_predictions.csv` | `246e14f8b84b8b89cbfce180fd7722ae82820f516894aa5dd11462866d10cfbb` |
| `research/raw/detection_metrics.csv` | `ed5775303f74156d844dc0068db4328e2237fc935a2bca260d613571083de57e` |
| `research/raw/detection_by_scenario.csv` | `7bc8400653683465f8f25af7d60398ae892831b4b3038ac5b7933478103bebf9` |
| `research/raw/diagnosis_predictions.csv` | `d43e43370349a1d005cd7de14aa1488486780fc459c2f796559241137b7d1a68` |
| `research/raw/diagnosis_metrics.csv` | `79bf2f53fb0de1c6d24afcb88b475e48c78e8cedd27d45ac051d948d505fc307` |
| `research/raw/safety_test_results.csv` | `19391636c705166981b56120835b2b0a0b12218defaeffc899474acb8f220985` |
| `research/raw/safety_metrics.csv` | `08145f57939c33f8b3db4b017e0833cbfda84a5678f13c54a837ff1335ec0b9a` |
| `research/results/statistical_analysis.md` | `fe401d2a1dd1f28636cb2f1a64198b232f46f72ff215b14e4a29c48cb8108d74` |
| `research/paper/CANONICAL_METRIC_RECONCILIATION.md` | `d3f1509152e56dc0c446275bac1d20f9210e430c4e2564d62dc6ed1ebd791cff` |
| `research/exports/LIVE_DATA_AND_EXTERNAL_VALIDATION_AUDIT.md` | `c5928b43b3de2527a8b0b758d011583ac75542c27873b07a6773a0b44d876832` |
| `research/exports/telemetry.csv` | `0a17468699ad918ffcd98af2d77982e7283206d73de3f5d838b0347db6c493a5` |
| `models/lstm_autoencoder.json` | `24826b053833b08e80fb84e7e694adfad5b4a1124d935ccf3e3cd4f575eb045f` |

The source files for B and C still differ from the older `research/MANIFEST_SHA256.json`; this audit verifies their current bytes against the Phase 1 freeze, not against that stale manifest.

## 2. Experiment A — synthetic anomaly detection

The raw prediction file contains 320 rows: 200 nominal rows and 120 fault rows. Fault rows are 20 each for `INC-1001` through `INC-1006`. They are controlled synthetic windows with repeated scenario structure, not independent production incidents.

| Detector | TP | FP | TN | FN | Precision | Recall | F1 | Specificity | FPR | Trapezoidal PR-AUC | Average precision | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Rules | 120 | 0 | 200 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | N/A | N/A | VERIFIED WITH LIMITATIONS |
| Isolation Forest | 57 | 4 | 196 | 63 | 0.9344 | 0.4750 | 0.6298 | 0.9800 | 0.0200 | 0.905564 | 0.906027 | VERIFIED WITH LIMITATIONS |
| Frozen LSTM | 120 | 2 | 198 | 0 | 0.9836 | 1.0000 | 0.9917 | 0.9900 | 0.0100 | 1.000000 | 1.000000 | VERIFIED WITH LIMITATIONS |
| Combined Rules OR LSTM | 120 | 2 | 198 | 0 | 0.9836 | 1.0000 | 0.9917 | 0.9900 | 0.0100 | N/A | N/A | VERIFIED WITH LIMITATIONS |

The stated confusion-matrix claims are all verified. PR-AUC and average precision were recomputed separately from continuous `iso_score` and `lstm_score`, by descending unique score thresholds: trapezoidal integration across recall/precision points for PR-AUC and a right-step recall-weighted sum for average precision. The Rules and Combined outputs lack a comparable continuous ranking score, so their PR-AUC/AP are intentionally `N/A` rather than mechanically calculated from binary flags.

Fault-window paired comparison of LSTM versus Isolation Forest has LSTM-only detections `b=63`, Isolation-Forest-only detections `c=0`, and exact two-sided McNemar/binomial probability `2 × 0.5^63 = 2.1684e-19`. The scenario recalls are LSTM `[1.00, 1.00, 1.00, 1.00, 1.00, 1.00]` and Isolation Forest `[0.40, 0.25, 0.85, 0.75, 0.40, 0.20]`. The documented six-scenario Wilcoxon/sign-pattern result is reproducible as `W-=0`, exact two-sided `p=0.03125`; it is **EXPLORATORY ONLY** because there are only six clustered scenarios and the p-value is the smallest possible two-sided value with six same-direction nonzero differences.

`false_alarms_per_hour` values in `research/raw/detection_metrics.csv` (0.0, 14.4, and 7.2) are **UNSUPPORTED** as operational-rate claims: this finite synthetic batch has no defensible wall-clock exposure denominator. The window-level FPR values above remain valid for this dataset.

## 3. Experiment B — diagnosis pilot

Current raw records contain seven configurations and six scenarios each (42 rows). `UNASSESSABLE` records remain in intent-to-treat denominators and are excluded only from completed-case accuracy and mean-latency calculations. API costs and token usage are not present in the raw data and are **NOT REPRODUCIBLE**.

| Configuration | Intended / completed | Unassessable | Strict ITT | Strict completed case | Lenient ITT | Lenient completed case | Mean completed latency (ms) | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 Rule-based Baseline | 6 / 6 | 0 | 6/6 | 6/6 | 6/6 | 6/6 | 0.0083 | VERIFIED WITH LIMITATIONS |
| 2 Single-Agent Offline | 6 / 6 | 0 | 3/6 | 3/6 | 3/6 | 3/6 | 0.0317 | VERIFIED WITH LIMITATIONS |
| 3 Multi-Agent Full Offline | 6 / 6 | 0 | 3/6 | 3/6 | 3/6 | 3/6 | 0.5683 | VERIFIED WITH LIMITATIONS |
| 4 Multi-Agent No-DL Offline | 6 / 6 | 0 | 6/6 | 6/6 | 6/6 | 6/6 | 0.1133 | VERIFIED WITH LIMITATIONS |
| 5 Single-Agent Groq LLM | 6 / 5 | 1 | 4/6 | 4/5 | 4/6 | 4/5 | 3,041.87 | EXPLORATORY ONLY |
| 6 Multi-Agent Full Groq LLM | 6 / 6 | 0 | 5/6 | 5/6 | 6/6 | 6/6 | 23,188.72 | EXPLORATORY ONLY |
| 7 Multi-Agent No-DL Groq LLM | 6 / 5 | 1 | 4/6 | 4/5 | 5/6 | 5/5 | 19,279.69 | EXPLORATORY ONLY |

The two rate-limit omissions are Config 5 / `INC-1002` and Config 7 / `INC-1004`, both with `latency_ms=0` and verdict `UNASSESSABLE`; they are not failures nor completed calls. The current `diagnosis_metrics.csv` agrees with the completed-call latency convention. No comparison here justifies a statistical-superiority claim: the corpus is six hand-authored scenarios, configurations differ in deterministic versus live-API mode, and two API calls were omitted.

## 4. Experiment C — local safety harness

The raw safety file contains 16 records: 11 `ATTACK_CASE`, 2 `POSITIVE_CONTROL`, 2 `PRECONDITION_CHECK`, and 1 `VERIFICATION_PROBE`. All 16 records have `audit_trail_verified=1` and verdict `PASS`.

| Measure | Recalculated value | Method | Status |
| --- | --- | --- | --- |
| Attack containment | 11/11 = 100% | `ATTACK_CASE` records with `PASS` | VERIFIED WITH LIMITATIONS |
| Attack containment 95% Wilson CI | [0.7412, 1.0000] | Wilson interval, z=1.9599639845 | VERIFIED |
| Mean attack enforcement latency | 11.3218 ms | Arithmetic mean of 11 attack-case latency values | VERIFIED |
| Audit trail completeness | 16/16 = 100% | `audit_trail_verified` across all records | VERIFIED WITH LIMITATIONS |
| Audit completeness 95% Wilson CI | [0.8064, 1.0000] | Wilson interval | VERIFIED |

The taxonomic counts and latency agree with the current metric file after rounding. This is a local approval/execution-boundary harness with a defined taxonomy; it is not a general production-security guarantee.

## 5. Live telemetry

`research/exports/telemetry.csv` has 200 stored rows: `bootstrap_rules=200`, null `anomaly_score=200`, fault modes `normal=31`, `latency=1`, and `error=168`. Consecutive timestamp gaps range from 0.578 to 6170.223 seconds; 26 exceed 60 seconds. These are record-level facts, not an accuracy dataset. Valid descriptive visualizations include record counts, fault-mode composition, detector-mode composition, score missingness, and gap distributions. Invalid confirmatory visualizations include live sensitivity, specificity, FPR, ROC/PR performance, or alarms/hour.

The recorded session therefore demonstrates collection, persistence, rule-fallback alerts, and operational logging only. The labels/episode annotations were produced in the same local workflow and are not independent adjudicated ground truth. Live LSTM inference remains absent: all stored rows are bootstrap-rule mode with null scores.

## 6. Experiment D — AnoMod

The frozen metadata verifies five ordered features, `sequence_length=24`, and frozen threshold `0.7093990445137024`. Existing compatibility and calibration audits report zero valid finite contiguous 24-step nominal windows in the audited AnoMod normal material. The alternate eight-step path bypasses the frozen input contract, and the target-calibrated branch reuses validation windows for calibration and false-alarm evaluation while also risking near-zero-variance scaling collapse.

No `external_anomod_predictions.csv`, `external_anomod_metrics.csv`, `EXPERIMENT_D_RESULTS.md`, `experiment_d_manifest.json`, or `PROTOCOL_AMENDMENT_V1_2_RATIFICATION.json` is present. External performance metrics are therefore **UNSUPPORTED**. Archive ingestion/compatibility failure is not evidence of model generalization or lack of generalization.

## 7. Disposition

The complete claim-level disposition is in `research/exports/PHASE2_METRIC_SOURCE_MAP.csv`; statistical detail is in `research/exports/PHASE2_STATISTICAL_VERIFICATION.md`.

### Confirmed for a bounded paper

- Experiment A synthetic-window confusion matrices and window-level metrics.
- Experiment B's seven-configuration, six-scenario raw-pilot accounting, including omissions.
- Experiment C's 11/11 local attack containment, Wilson interval, and 11.3218 ms mean enforcement latency.
- Live record counts, bootstrap-rule mode, null-score count, and timestamp-gap facts.
- AnoMod archive presence and the absence of production evaluation artifacts.

### Must be qualified

- All A inference is synthetic and clustered; McNemar and Wilcoxon are descriptive/exploratory, not production performance evidence.
- B is a six-scenario pilot, with rate-limit omissions and no cost/token records.
- C is a local test-harness result with a bounded attack taxonomy.
- Live data is an operational demonstration, not a labeled performance study.

### Unsupported claims to remove or retain only as historical text

- Operational false alarms per hour from Experiment A.
- Any live LSTM score, accuracy, or generalization claim.
- Any independent live-detection performance claim.
- Any executed AnoMod/external performance metric, confusion matrix, or transfer conclusion.
- Any API token/cost claim for Experiment B.

### Remaining numerical contradictions

The Phase 1 manifest is stale for seven entries; it must not be used as a current-integrity certificate. Historical A/B/C tables contain superseded values. No unresolved discrepancy remains in the four requested A confusion matrices, B's current raw accounting, or C's current raw accounting. The external and live-LSTM result gaps are missing evidence, not numerical contradictions.

**Phase 3 readiness: yes, conditionally.** Proceed only to a non-experimental correction/planning phase that uses this report's dispositions, retains frozen-snapshot provenance, and does not claim unsupported live/external results.
