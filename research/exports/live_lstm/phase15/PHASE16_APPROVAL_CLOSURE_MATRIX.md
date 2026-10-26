# Phase 16 Approval-Closure Matrix

**Date:** 2026-10-17 (Asia/Kolkata)
**Scope:** Administrative closure and reproducible preflight only. This is not an authorization record and no pilot was run.

## Evidence reviewed

- Phase 15 readiness, collection-quality, interruption-register, and evidence-preservation artifacts.
- Phase 13 implementation/evidence-preservation records and Phase 14 readiness, collection, labeling/statistics, and owner-decision records.
- `research/audits/AEGISOPS_MASTER_RESEARCH_HANDOFF.md` and the repository working tree.

The Phase 14 decision register and the Phase 15 proposed run sheet are planning records. Neither is a signed authorization, a target-access grant, or a data-governance approval.

## Approval-closure matrix

| Requirement | Classification | Verified evidence or missing record | Closure required before Gate 1 can pass |
| --- | --- | --- | --- |
| Collector topology, target identity/environment, endpoint role, and responsible owner | **REQUIRES HUMAN APPROVAL** | Phase 15 records no signed topology/run record; Phase 14 D2 requires owner approval. | A named accountable owner must approve a bounded collector-to-target topology, endpoint role, access method, start/end scope, and a responsible operator. |
| Actual authorization record for the proposed run | **MISSING EVIDENCE** | No approval identifier, approver, date, expiry, or signed scope record was found in the reviewed materials. | Store a durable approval record that identifies the approving authority and the exact pilot scope; an absent or ambiguous record is not authorization. |
| Permitted telemetry schema | **DOCUMENTED AND VERIFIED** | The fixed five-feature contract is documented: `cpu_pct`, `memory_pct`, `latency_ms`, `error_rate_pct`, `disk_pct`; Phase 15 confirms it remains unchanged. | Governance approval must separately permit collection of these fields in the approved environment; schema documentation alone grants no collection right. |
| Data governance: authorized fields, retention, redaction, access, and export | **REQUIRES HUMAN APPROVAL** | Phase 15 found no data-governance authorization; Phase 14 D8 remains an owner decision. | The data/governance authority must approve field minimization, prohibited data, retention/destruction, redaction, access roles, storage location, and export controls. |
| Collection cadence, UTC timestamp source, interruption recording, restart behavior, and gap handling | **REQUIRES HUMAN APPROVAL** | No approved cadence, clock source, maximum inter-sample gap, reset policy, interruption owner, or restart policy was found; Phase 14 D1/D7 remain open. | The operational owner must approve those values and policies for the named topology. Diagnostic values may not substitute for a production-approved setting. |
| Safe behavior with no approved gap configuration | **DOCUMENTED AND VERIFIED** | Phase 13/15 evidence states an absent or invalid `AEGISOPS_LSTM_MAX_INTER_SAMPLE_GAP_S` prevents LSTM scoring and retains `window_not_ready` rules fallback. | No closure action for the safeguard itself. It neither starts collection nor authorizes access. |
| Quality-only purpose, authorized target access, run scope, and duration | **REQUIRES HUMAN APPROVAL** | No documented permission, permitted target, duration, scope, or target-access confirmation was found. | The target/environment owner and approving authority must authorize a quality-only, non-evaluative run with explicit start/end UTC or duration and revocation/stop authority. |
| Frozen synthetic checkpoint use for this pilot | **NOT APPLICABLE, WITH JUSTIFICATION** | A quality-only telemetry pilot does not require neural inference. The frozen checkpoint is disabled for non-test use and must remain disabled. | Do not enable it as a condition of this pilot. Record that no detector was enabled if a later approved run occurs. |
| Detection performance, training, calibration, thresholds, and recovery actions | **NOT APPLICABLE, WITH JUSTIFICATION** | The pilot is quality-only. Phase 15 did not collect data or calculate performance; live performance remains **UNMEASURED**. | Exclude these actions and metrics from the authorization and run. A separate approved prospective protocol is needed for evaluation. |

## Scope-verification rule for a future approval

Before Gate 1 is reconsidered, the designated reviewer must verify that an approval record is explicit, current, and matches the run sheet on all of: approving authority; collector and target identity; endpoint role and access method; permitted five-field schema; privacy/retention/access/export controls; cadence and UTC-clock policy; gap/reset/interruption/restart policy; quality-only purpose; duration; storage/export destination; and prohibitions on inference, training, calibration, threshold changes, recovery, and performance claims. Any mismatch, omission, expired authorization, or ambiguous wording leaves Gate 1 closed.

## Conclusion

The documented safeguards and schema make the proposed pilot reproducible once authorized, but they do not supply the missing human decisions. **Gate 1 remains closed.**
