# AegisOps Phase 4 Publication-Ready Figure Captions

## Figure A — Audited application architecture and trust boundaries

Implemented AegisOps monitoring architecture. The collector records collector-host metrics and a configured-target HTTP probe separately, then persists telemetry and alert-state events in SQLite. Bootstrap rules were the observed path in the audited session; the optional live-LSTM path was unavailable and not observed. Approval is shown as an unauthenticated audit label, and recovery is limited to `clear_demo_service_fault` for the local demo service, followed by independent health/probe verification. This diagram does not establish remote remediation, authenticated dual control, or production authorization. Source: Phase 3 architecture audit and diagram specification.

## Figure B — Frozen synthetic-benchmark LSTM autoencoder contract

The frozen autoencoder accepts a 24-step, five-feature window (`cpu_pct`, `memory_pct`, `latency_ms`, `error_rate_pct`, `disk_pct`), applies frozen mean/std normalization, encodes 5 to 16 dimensions, repeats the final 16-dimensional hidden state over 24 steps, decodes 16 to 16 dimensions, and projects 16 to 5 features. A global reconstruction-MSE score is compared strictly with 0.7093990445137024; per-feature mean-error comparisons are available where applicable. The diagram describes the synthetic-benchmark artifact, not a validated causal representation or live model. Source: `models/lstm_autoencoder.json` and Phase 3 audit.

## Figure C — Telemetry-to-alert flow and audited live-session boundary

The implemented flow collects host metrics and configured-target probe results, constructs a rolling error rate, persists telemetry, selects the last 24 rows in insertion order, optionally attempts model inference, applies rule guards, and persists annotated alert-state events. The audited session contained 200 stored rows, used bootstrap rules only, and had 200 null LSTM scores. Five seconds is an intended sampling cadence, and the live window construction does not validate timestamp continuity. Source: `research/exports/telemetry.csv`, Phase 2 reconciliation, and Phase 3 audit.

## Figure D — Diagnosis, approval, and local-demo recovery workflow

Implemented workflow from manager and investigation through diagnosis, resolution selection, human approval/ticket consumption, restricted local-demo recovery, independent health/probe checks, and verification/event persistence. Diagnosis can use deterministic offline behavior or a Groq-backed API path; the source-visible live application path contains no explicit retry, timeout, or rate-limit handling. The diagram does not imply that every component ran in every Experiment B configuration or in the audited live session. Source: Phase 3 audit and Phase 2 Experiment B reconciliation.

## Figure E1 — Experiment A synthetic detection comparison

Precision, recall, F1, and false-positive rate calculated from the verified confusion matrices for Rules, Isolation Forest, LSTM, and Combined detectors. The benchmark contains 320 synthetic windows (200 nominal and 120 fault windows across six scenarios); windows may be dependent. The figure makes no operational false-alarms-per-hour claim. Source: `research/raw/detection_predictions.csv` and Phase 2 reconciliation.

## Figure E2 — Experiment A confusion matrices

Confusion-matrix counts for the 320-window synthetic benchmark, with fault windows as the positive class. Rules: TP=120, FP=0, TN=200, FN=0; Isolation Forest: TP=57, FP=4, TN=196, FN=63; LSTM: TP=120, FP=2, TN=198, FN=0; Combined: TP=120, FP=2, TN=198, FN=0. Source: `research/raw/detection_predictions.csv` and Phase 2 reconciliation.

## Figure E3 — Experiment A scenario-level recall

Recall by detector across six synthetic fault scenarios, each represented by 20 fault windows. Scenario-level comparisons are descriptive/exploratory because there are only six scenario clusters. Source: `research/raw/detection_predictions.csv` and Phase 2 reconciliation.

## Figure E4 — Experiment B diagnosis pilot

Strict top-1 intent-to-treat and completed-case outcomes for seven six-case configurations. C1–C7 correspond, respectively, to Rule-based Baseline, Single-Agent (Offline), Full Multi-Agent (Offline), Multi-Agent without DL (Offline), Single-Agent (Groq), Full Multi-Agent (Groq), and Multi-Agent without DL (Groq). Strict ITT retains API omissions in a six-case denominator; strict completed-case excludes the two `UNASSESSABLE` omissions in C5 and C7. Colors distinguish offline configurations, Groq-backed configurations, and completed-case values. No superiority, cost-effectiveness, token, or API-reliability claim is made. Source: `research/raw/diagnosis_predictions.csv` and Phase 2 reconciliation.

## Figure E5 — Experiment C bounded local safety harness

Attack containment was 11/11 (Wilson 95% CI 0.741–1.000) and audit-trail completeness was 16/16 (Wilson 95% CI 0.806–1.000). The 16 local-harness cases include 11 attack cases, two precondition checks, two positive controls, and one verification probe. This is a bounded local-harness result, not a production-security certification. Source: `research/raw/safety_test_results.csv` and Phase 2 reconciliation.

## Figure E6 — Live telemetry evidence summary

The audited telemetry export contains 200 stored workflow-associated records, all in `bootstrap_rules` detector mode; all 200 `anomaly_score` values are null, so there are zero stored live-LSTM scored rows. The fault-mode field is displayed only as a stored workflow-associated field, not as independent ground-truth labels. No live ROC, PR curve, accuracy, specificity, false-positive rate, or alarms-per-hour metric is inferred. Source: `research/exports/telemetry.csv` and Phase 2 reconciliation.

## Figure F — Experiment D external-validation readiness

AnoMod archive/provenance and extraction-manifest assets are present, but the audited evidence records unresolved 24-step compatibility and calibration/evaluation-separation blockers. Production predictions, metrics, and ratification evidence are absent. The panel is a readiness/provenance summary only and is not an external-performance chart. Source: Phase 1 evidence freeze, Phase 2 reconciliation, and Phase 3 audit.
