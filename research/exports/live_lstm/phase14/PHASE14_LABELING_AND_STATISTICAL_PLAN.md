# Phase 14 Labeling and Statistical Plan

**Status:** Proposed prospective protocol. No labels, performance statistics, or thresholds are generated in this phase.

## 1. Independent ground-truth protocol

### Roles

| Role | Separation requirement |
| --- | --- |
| Operational incident authority | Opens/owns the incident record and supplies source evidence for onset, offset, target, impact, and resolution. |
| Primary adjudicator | Assigns the label from operational evidence without access to detector score, detector mode, rule alert, agent narrative, or model explanation. |
| Second adjudicator | Independently reviews predefined ambiguous or sampled records under the same blinded materials. |
| Resolver | Resolves disagreement using a documented rule and records the final reason; must not use detector outputs as truth. |
| Data custodian/analyst | Links labels to sample IDs only after adjudication is frozen; maintains an audit trail of access and revisions. |

The owner must name these roles and confirm their independence before collection. For injected tests, the injector may document the intervention but must not adjudicate model correctness. Detector alerts and agent outputs are evidence of system behavior, not ground truth.

### Label record

Each adjudicated episode requires: immutable episode ID; target/topology ID; source incident record; onset and offset UTC timestamps with evidence source; cause/condition category; impact/severity definition; label status (`confirmed`, `excluded`, or `unassessable`); adjudicator IDs or pseudonyms; decision time; and a compact rationale. Preserve uncertainty rather than converting it to normal or anomalous.

An event with uncertain boundaries, conflicting evidence, maintenance overlap, topology change, or unavailable source evidence is `unassessable` until resolution. It must not enter primary sensitivity/specificity denominators. Report its count and reason separately.

## 2. Evaluation units and linkage

Use both units, but prespecify distinct estimands:

- **Window-level unit:** an admissible non-overlapping or otherwise explicitly correlated 24-step window, linked to the truth interval it occupies. It measures score/decision behavior at the model's input unit.
- **Episode-level unit:** an independently adjudicated incident episode with a declared onset/offset and a prespecified alert-association rule. It measures whether detection occurred and when, without treating dozens of overlapping windows as independent incidents.

Assign normal exposure only to intervals explicitly reviewed as normal and not within an exclusion buffer around incident onset/offset, deployment changes, maintenance, collection gaps, or ambiguous cases. The owner must approve any boundary buffer and alarm-association window before data review. Do not infer either from observed scores.

## 3. Separation and leakage control

Partition chronologically before fitting:

1. A development/training partition contains only approved healthy telemetry for live-model fitting.
2. A calibration/validation partition is later in time and is used for training controls explicitly allowed by the protocol, including threshold calibration if a new live model is authorized.
3. A final test partition is later, sealed before model/scaler/threshold selection, and may not influence preprocessing, architecture, epochs, thresholds, gap policy, exclusion policy, or label decisions.

Keep a whole episode, its related windows, and any operationally coupled deployment period in one partition. Prevent raw-sample overlap between windows across partitions. Record any embargo/reset interval between partitions, but do not invent its duration in this document. Maintain a partition manifest mapping every sample/window/episode to exactly one role or an excluded/unassessable status.

The frozen synthetic checkpoint is a separate artifact and must not be mixed with a future live-trained checkpoint. A live checkpoint needs its own model version, training-data manifest hash, code revision, feature contract, scaler vectors, thresholds, seed(s), hardware/software versions, and training/calibration records.

## 4. Training and calibration protocol

The existing live-training implementation is evidence of an initial engineering lifecycle, not yet an approved prospective study design. It currently selects HTTP-200, zero-error, `fault_mode=normal`, non-resource-breaching rows; requires at least 180 rows; splits rows chronologically 80/20; fits mean/std only on the training rows with existing floors; and calibrates a 99th-percentile validation threshold. It has no independent test partition and must not be used to make a final prospective performance claim without the separation above.

For an authorized live-training study:

- Freeze the raw training-data export and eligibility decisions before fitting.
- Preserve the exact feature order/units, window construction, finite-value checks, timestamp/gap policy, scaler statistics, threshold method, checkpoint state hash, metadata hash, random seed, code revision, library versions, and device.
- Treat training, scaler fitting, model selection, and threshold calibration as development-stage operations. Do not reuse final-test labels/windows for them.
- Version the output checkpoint and metadata together. Its provenance must identify live-trained data rather than synthetic smoke-test use.
- Retain rejected candidates and failure reasons without replacing or overwriting an earlier checkpoint.

No existing weight, scaler, or threshold changes in Phase 14.

## 5. Prespecified statistical analysis plan

### Primary analyses

1. **Episode-level detection:** proportion of independently adjudicated anomalous episodes with at least one combined alert under the prespecified association rule; report an exact or Wilson confidence interval appropriate to the observed denominator.
2. **Normal-exposure false alerts:** combined alerts per declared normal-exposure time, with the exact exposure denominator, interruptions, exclusions, and confidence method stated. Do not substitute row count for elapsed eligible exposure.
3. **Model/rule decomposition:** report model-only, rule-only, and combined decisions separately at both window and episode level. A guardrail-only alert is not a model detection.

### Secondary analyses

- Model score distribution and missing-score/inference-reason distribution by run, topology, condition class, and checkpoint identity.
- Window-level sensitivity/specificity or precision/negative predictive value only when labels and denominators support them, with uncertainty intervals and explicit correlation limitations.
- Detection delay from adjudicated onset to first alert, with handling of right-censoring and episodes with no alert stated in advance.
- Scenario-stratified reporting by genuine incident, injected event, normal operation, collector failure, and target/probe failure. Injected scenarios must remain separate from genuine operational incidents.
- Calibration analysis only on the prespecified calibration partition, not the final test set.

### Not currently estimable

No live sensitivity, specificity, precision, recall, F1, ROC-AUC, PR-AUC, false-positive rate, alerts per hour, detection delay, calibration, or generalization estimate is currently justified. Each requires sufficient independently labelled anomalous and normal exposure, valid score/decision records, declared denominators, and the frozen partition/label protocol. No sample-size target, effect size, acceptance threshold, or success criterion is supplied here; each needs owner decision informed by pilot variability and intended operational use.

## 6. Reporting safeguards

Report denominator, unit, partition, provenance, missingness, excluded/unassessable cases, and uncertainty beside every metric. Do not pool overlapping windows as independent incident replications. Do not compare a future live-trained model with the frozen synthetic model as though they were one fixed intervention. Do not use live rule-based alerts, agent diagnoses, or injected-fault instructions as labels for primary live performance.
