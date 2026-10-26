# Phase 16 Pilot Preflight Checklist and Run Sheet

**Status:** **NOT AUTHORIZED — DO NOT START COLLECTION.**
**Purpose:** A reusable, approval-gated quality-only procedure. Blank fields are intentional; this document does not grant access or select production configuration.

## Gate 1 preflight

All items below must be complete and evidenced by a current approval record before a collector or target is contacted.

| Check | Required evidence | Current state |
| --- | --- | --- |
| Accountable collector and target owners identified | Named owners and their authorization roles in the approval record | **NOT COMPLETE** |
| Bounded topology and target access authorized | Collector identity, environment, endpoint role, access method, target identity, and approved scope | **NOT COMPLETE** |
| Data-governance controls approved | Authorized fields, prohibited content, retention/destruction, redaction, access, storage, and export controls | **NOT COMPLETE** |
| Cadence and clock policy approved | Expected cadence, UTC timestamp source, synchronization responsibility, and clock-failure handling | **NOT COMPLETE** |
| Gap/interruption/restart policy approved | Maximum gap, window-reset behavior, interruption recorder, notification path, restart authority, and stop conditions | **NOT COMPLETE** |
| Quality-only permission bounded | Approval identifier, approver, issue/expiry, start/end UTC or duration, and no-inference/no-recovery restriction | **NOT COMPLETE** |
| Runtime is safe for the approved run | Recorded revision/configuration digest excluding secrets; frozen checkpoint disabled; no training/calibration/threshold change | **NOT COMPLETE** |
| Evidence destination approved | Fresh run identifier, storage location, access control, export/hash method, and interruption register | **NOT COMPLETE** |

**Fail-closed decision:** If any row is incomplete, unclear, expired, or outside the recorded scope, stop. Do not contact a target, start a collector, write telemetry, or modify runtime configuration.

## Owner-completed pilot run sheet

| Field | Owner-supplied value before start |
| --- | --- |
| Approval ID; approving authority; issue/expiry UTC |  |
| Quality-only purpose and explicit exclusions |  |
| Authorized start/end UTC or duration; stop/revocation authority |  |
| Collector identity/topology and accountable owner |  |
| Target/environment, endpoint role, target owner, and access authorization |  |
| Statement separating collector-host metrics from HTTP-probe target measurements |  |
| Authorized five fields and units/order; prohibited data |  |
| Retention, redaction, storage, access, and export controls |  |
| Expected cadence and UTC timestamp/clock source |  |
| Approved maximum inter-sample gap and reset rule |  |
| Interruption recorder; classification policy; notification and restart authority |  |
| Code revision, configuration digest excluding secrets, and run ID |  |
| Checkpoint/score policy: detector disabled; no training/calibration/threshold/recovery |  |
| Export/hash custodian and evidence destination |  |

## During-run evidence and measurable quality checks

Record observations only; do not create acceptance thresholds unless an owner approves them beforehand.

| Check | Evidence to capture | Reported quantity or rule |
| --- | --- | --- |
| Sample identity and traceability | Run ID, monotonically assigned sample ID, UTC acquisition timestamp, collector/target topology identifier | Count rows and identify missing/duplicate IDs. |
| Five-field completeness and validity | Field-presence flags, finite/numeric validation outcome, units/order, rejection reason without sensitive payload | Counts and proportions by field and reason. |
| Timestamp integrity | Raw UTC timestamp, parse/clock-source outcome, ordered-record check | Counts of invalid, duplicate, and non-monotonic timestamps. |
| Cadence characterization | Consecutive valid timestamp differences and owner-approved expected cadence | Report count, min, median, selected quantiles, maximum, and deviations from the approved cadence; do not infer a pass/fail limit. |
| Candidate 24-row windows | Window start/end IDs and timestamps; continuity result | Count candidates only at diagnostic maximum-gap values explicitly approved or labeled as diagnostic. Never promote a diagnostic value to production. |
| Interruption handling | Start/end UTC, component, classification, known cause, affected sample range, reporter, disposition | Append one row per interruption to `PHASE15_INTERRUPTION_REGISTER.csv`; never bridge, interpolate, reorder, or backfill the gap. |
| Topology stability | Topology/configuration digest at start and on change | Record every change and partition results by topology; do not pool unlike sources. |
| Detector/provenance boundary | Mode/reason only, checkpoint identifier if any | Confirm no frozen checkpoint is enabled and no scores are interpreted as performance. |

## Stop and preservation rules

- Stop on scope loss, expired/revoked approval, unauthorized topology or target, governance violation, unrecordable interruption, or clock/timestamp condition whose handling is not approved.
- Preserve raw time ordering. Do not fill, interpolate, reorder, bridge, relabel, or backfill data or scores.
- Keep collector-host and probe-target observations distinct. Do not store secrets, personal data, or unnecessary operationally sensitive data.
- Capture the approval record reference, run-sheet version, repository branch/HEAD, permitted configuration digest, and export hashes. Do not modify historical telemetry, model files, thresholds, scalers, databases, manifests, or manuscripts.
- Quality observations do not estimate detector accuracy, false-positive rate, recall, calibration, or operational performance.
