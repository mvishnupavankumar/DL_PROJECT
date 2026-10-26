# Phase 14 Blockers and Owner Decisions

**Date:** 2026-10-16 (Asia/Kolkata)  
**Status:** Planning record; no operational settings are changed here.

## Decision register

| ID | Decision needed | Status | Evidence basis | Required owner output |
| --- | --- | --- | --- | --- |
| D1 | Maximum permitted inter-sample gap and window-reset behavior | **Requires owner approval** | Intended cadence is about five seconds, but historical collection was irregular and Phase 13 deliberately supplies no default. | Signed value, pilot rationale, clock policy, and response to a gap/reset. |
| D2 | Prospective topology and target scope | **Requires owner approval** | Existing data combines collector-host metrics and local HTTP-probe measurements. | Named collector, target, environment, endpoint role, target owner, time source, and permitted data scope. |
| D3 | Mode of frozen synthetic checkpoint | **Requires owner approval** | It is technically smoke-testable but not live calibrated. | Confirm it remains test-only or explicitly prohibit all non-test use; do not authorize silent fallback. |
| D4 | Live-training authorization | **Blocked pending data and approval** | No live-trained checkpoint exists; historical record has only eight rows eligible under the current 180-row gate. | Approved training protocol, data eligibility policy, partition plan, and versioning/retention policy. |
| D5 | Ground-truth authority and adjudication process | **Blocked pending assignment** | Historical annotations and injections are not independent of the collection/alert workflow. | Named adjudicators, blinding/separation rule, evidence sources, disagreement process, and unassessable policy. |
| D6 | Evaluation estimands and acceptance criteria | **Requires owner approval** | No prospective labels/exposure or intended operational use threshold exists. | Primary endpoint(s), evaluation unit(s), exposure denominator, uncertainty method, sample-size justification, and decision criteria. |
| D7 | Collection interruption governance | **Requires owner approval** | Existing code rejects bad windows, but operational runbook/retention has not been approved. | Interruption record owner, response/notification procedure, restart rule, and exclusion linkage. |
| D8 | Data retention/privacy and access control | **Requires owner approval** | Future topology may introduce operational identifiers or protected logs. | Data minimization, retention duration, access roles, export controls, and redaction policy. |

## Verified facts that constrain decisions

- `AEGISOPS_LSTM_MAX_INTER_SAMPLE_GAP_S` is the current configuration point. Unset/invalid values fail closed to `window_not_ready` and bootstrap rules.
- Default inference selects only `models/live_lstm_autoencoder.pt`, which is absent. The frozen checkpoint requires both an explicit path and `AEGISOPS_ENABLE_FROZEN_SMOKE_TEST=true`.
- The model contract remains five ordered features and 24 timestamp-valid finite samples. Phase 13 persists bounded inference reason, checkpoint provenance/identity, score, and model/rule/combined decisions.
- The historical 200-row record is bootstrap-only with null scores and is not independently labelled performance evidence.
- Existing safe behavior does not authorize autonomous recovery. Remote recovery remains out of scope; manual, constrained existing safeguards remain in force.

## Gating sequence

1. Approve D1, D2, D5, D7, and D8 before any prospective collection intended for research use.
2. Run a quality-only pilot to measure cadence, gaps, clock behavior, topology stability, and interruption reporting. Freeze the result as protocol evidence, not performance evidence.
3. Approve D4 only after the pilot confirms that the data contract can be satisfied. Train/calibrate only from declared development data under a separately versioned protocol.
4. Seal a final held-out collection partition and complete independent labels before opening score/alert comparisons.
5. Approve D6 before calculating or interpreting performance metrics.

## Blockers that cannot be resolved by this document

- A missing production/live-trained checkpoint cannot be replaced by the frozen synthetic checkpoint without violating provenance boundaries.
- Historical irregular bootstrap telemetry cannot be converted into valid prospective LSTM performance evidence by backfill, imputation, or retrospective self-labelling.
- No metric can be made meaningful without a declared evaluation unit, independent labels, normal-exposure denominator, and partition separation.
- No automatic remediation may be enabled based on proposed evaluation results without separate safety authorization.

## Final classification

**Ready:** fail-closed inference admission, bootstrap fallback, bounded fallback provenance, and technical smoke-test separation.  
**Blocked:** live-trained checkpoint, continuously valid prospective stream, independent labels, sealed partitions, and live performance estimation.  
**Requires owner approval:** cadence gap value, topology, frozen-checkpoint policy, data governance, training authorization, labeling authority, interruption procedure, statistical estimands, and success criteria.
