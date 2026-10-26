# AegisOps Phase 3 Unsupported Architecture Claims

The following claims must not appear in the paper, final figures, algorithms, captions, or system description unless new independently verifiable evidence is added.

1. **Live LSTM inference occurred during the audited 200-row session.** It did not: all rows are `bootstrap_rules` and all anomaly scores are null.
2. **The live system used the frozen synthetic checkpoint.** The live path looks only for `models/live_lstm_autoencoder.pt`, which is absent. The frozen `models/lstm_autoencoder.pt` supports synthetic Experiment A only.
3. **All live windows are contiguous 24 samples at five-second intervals.** The intended UI cadence is five seconds, but collection has observed large gaps and live window construction uses insertion order without timestamp-continuity validation.
4. **Live telemetry provides independently labeled detection accuracy, specificity, FPR, PR-AUC, alarms/hour, or generalization.** The local labels/episodes are workflow-derived; records are irregular and LSTM scores are absent.
5. **AegisOps executes autonomous or remote production remediation.** Recovery is forcibly limited to clearing an injected local-demo fault over loopback HTTP.
6. **Approvals use authenticated human identity, authenticated dual control, or an enterprise authorization service.** `approved_by` is a user-supplied audit label; `ApprovalStore` explicitly says it is not an identity provider.
7. **The confirmation phrase is authentication.** It is only a workflow condition.
8. **Agent diagnosis is independently verified.** The investigation and diagnosis steps may be deterministic fallback or API-generated; the verification agent consumes the action-result payload. No independent diagnostic ground-truth verifier is implemented for live cases.
9. **The manager, investigation, diagnosis, resolution, and verification components all ran in each Experiment B configuration or in the audited live session.** Their invocation varies by configuration; the live session proves bootstrap monitoring, not a full recorded agent/recovery lifecycle.
10. **The current Experiment B raw CSV was produced unchanged by the older `run_experiment_b.py`.** Its older output fields differ; current reconciled B records trace through `generate_diagnosis_audit.py`.
11. **Experiment C is a production-security certification.** It is a 16-record local harness with 11 attack cases and a defined taxonomy.
12. **Experiment D provides external performance, zero-shot validation, or an AnoMod confusion matrix.** Production outputs and protocol ratification are absent; the frozen 24-step contract is incompatible with audited valid-window availability.
13. **The 8-step AnoMod pathway validates the frozen LSTM.** It bypasses `detect()` and its 24-step contract.
14. **The model can infer causal root causes from anomaly scores.** Model output is passed as supporting evidence; source prompts explicitly say it is not ground truth.
15. **The system collects target-host CPU, memory, and disk for remote targets.** Those three values come from the collector host; only HTTP probe data concerns the configured target.

Figures may show implemented optional branches, but must label their execution state. For the audited session, render the live LSTM branch as absent/unavailable and route records through bootstrap rules only.
