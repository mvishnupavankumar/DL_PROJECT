# Phase 14 Live Readiness Report

**Date:** 2026-10-16 (Asia/Kolkata)  
**Phase type:** Read-only prospective-evaluation planning.  
**Repository at start:** branch `publish/research-without-external-dataset`; HEAD `a32713c30a8ddca1425d44b1afbaf6d55a64c276`; dirty worktree with 90 porcelain entries (45 modified and 45 untracked paths). Existing changes were not reset, staged, stashed, or altered.

## Scope and evidence boundary

This report uses the Phase 13 reports, Phase 1 evidence freeze, Phase 3 architecture audit, Phase 10-12 release/manuscript reviews, the live-data audit, and the Live LSTM root-cause audit. It distinguishes verified current implementation facts from proposed procedures. It does not authorize or perform collection, training, calibration, scoring, database migration, threshold modification, performance analysis, or manuscript changes.

The historical local record remains unsuitable for prospective evaluation: it contains 200 bootstrap-rule rows with null LSTM scores, irregular gaps, a long injected error episode, and labels that are not independent of the generating workflow. The successful Phase 13 frozen-checkpoint test is an integration smoke test, not a live-performance result.

## Configuration readiness

| Prerequisite | Current status | Verified fact or required next step |
| --- | --- | --- |
| Default safe state | **Ready** | With `AEGISOPS_LSTM_MAX_INTER_SAMPLE_GAP_S` unset or invalid, `configured_max_inter_sample_gap_seconds()` returns no value; the analysis path persists `window_not_ready` and uses bootstrap rules. |
| Location of operational gap setting | **Ready** | Set the owner-approved value in the deployment environment as `AEGISOPS_LSTM_MAX_INTER_SAMPLE_GAP_S`; it is documented in `.env.example`. This phase does not write `.env` or select a value. |
| Maximum-gap policy | **Requires owner approval** | Intended cadence is approximately five seconds, but no allowed lateness/jitter, clock source, interruption boundary, or reset policy has been approved. The Phase 13 smoke value of six seconds is test-only and must not become a production default. |
| Live-trained checkpoint | **Blocked** | Default selection is `models/live_lstm_autoencoder.pt`; it is absent. The frozen `models/lstm_autoencoder.pt` is only accepted with explicit smoke-test opt-in and remains synthetic-calibrated. |
| Checkpoint provenance | **Ready** | The selected provenance, compact checkpoint identity, inference reason, score, detector mode, and model/rule/combined decisions have persistence support in the current schema path. |
| Target/collector topology | **Requires owner approval** | Current collection combines collector-host resource measures with a configured HTTP probe. A prospective protocol must name the collector host, target, probe endpoint, ownership, environment, and whether their clocks share a time source. |

### Decision record required for the gap policy

Before scoring a prospective stream, the owner must record: intended cadence; measurement of observed cadence/jitter during a pilot; time source and timezone policy; maximum admissible inter-sample gap; whether any gap starts a new candidate window; and the operational response to collector outage or clock change. The selected value must be derived from that pilot and signed into the protocol/configuration record. A missing, nonnumeric, nonfinite, or nonpositive value remains a safe non-scoring condition.

## Readiness verdict by prerequisite

| Area | Classification | Basis |
| --- | --- | --- |
| Rules fallback, bounded reason codes, and no stale score on invalid window | **Ready** | Implemented and Phase 13-tested. |
| Explicit synthetic smoke-test separation | **Ready** | Implemented and Phase 13-tested; not evidence of live validity. |
| Continuous timestamp-valid telemetry | **Blocked** | No prospective stream exists; the historical stream has long gaps. |
| Approved operational cadence and gap/reset policy | **Requires owner approval** | No approved tolerance exists. |
| Live-trained checkpoint and calibration record | **Blocked** | No checkpoint or metadata exists; historical eligible rows are insufficient for the existing training gate. |
| Independently adjudicated labels | **Blocked** | Historical local annotations/injections are not independent ground truth. |
| Partitioned prospective evaluation cohort | **Blocked** | No prespecified partitions or label-blinded test cohort exists. |
| Statistical analysis plan and release criteria | **Requires owner approval** | This phase supplies a plan but neither sample size nor acceptance criterion may be invented. |
| Automatic operational recovery | **Not authorized** | Retain current rules-only monitoring and local-demo safety limits. No unapproved automatic recovery is proposed. |

## Safe operating behavior for the prospective phase

1. Continue collecting raw telemetry and record the inference reason on every analyzed latest sample.
2. Use bootstrap rules, with a null anomaly score and no model-only decision, for absent/rejected checkpoints, insufficient rows, invalid features, non-monotonic/invalid timestamps, excessive gaps, load failures, and inference failures.
3. Treat `inference_success` as a record of score generation, not proof that an alert is correct. Preserve model-only, rule-only, and combined decisions separately.
4. Treat collection interruption, target unavailability, and clock/timestamp faults as data-quality events. Do not bridge or impute the resulting gaps.
5. Keep recovery actions manually authorized and constrained to existing safety controls. An alert, score, or agent narrative must not create an automatic recovery action.

## Phase 14 conclusion

The integration prerequisites are partly ready, but scientifically defensible prospective performance evaluation is **blocked** until owner-approved cadence policy, documented topology, prospective continuous collection, a separately versioned live-training/calibration lifecycle, and independent ground truth exist. The next legitimate activity is protocol approval and a non-evaluative collection-quality pilot, not a performance claim.
