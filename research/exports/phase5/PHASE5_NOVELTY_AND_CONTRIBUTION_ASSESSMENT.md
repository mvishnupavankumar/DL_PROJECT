# AegisOps Phase 5 Novelty and Contribution Assessment

**Assessment date:** 2026-10-15  
**Decision rule:** Novelty is assessed against verified literature and the frozen repository evidence, not against intended functionality or historical narrative.

## Bottom line

AegisOps does **not** establish a novel LSTM architecture, causal representation, production-ready security system, autonomous safe recovery system, or external generalization result. Its defensible contribution is a bounded, source-audited engineering integration: a frozen LSTM reconstruction detector evaluated on a synthetic benchmark, diagnosis configurations evaluated on a six-case pilot, and an approval-controlled local recovery harness with explicit test limits.

## Established methods and prior art

| Area | Established prior art | AegisOps position |
| --- | --- | --- |
| LSTM reconstruction anomaly detection | Malhotra et al. establish LSTM encoder–decoder reconstruction scoring; OmniAnomaly and USAD are later unsupervised multivariate methods. | Uses a small LSTM autoencoder; no architecture-level novelty claim is justified. |
| Rule and unsupervised baselines | Threshold rules and Isolation Forest are established baselines. | A synthetic comparison is available; it is not a general benchmark result. |
| AIOps/RCA | MicroRCA, CloudRCA, and Eadro establish graph, multi-source, and end-to-end troubleshooting research. | AegisOps is not the first detection-to-diagnosis pipeline and does not reproduce those systems. |
| LLM multi-agent orchestration | AutoGen and MetaGPT establish generic role-based agent frameworks. | The live-LLM diagnosis pilot is small and subject to provider omissions; no causal/production inference follows. |
| Controlled action governance | NIST supplies a governance/control reference; it is not an implementation certification. | The local one-label approval workflow is not authenticated dual authorization and must not be called NIST compliant. |
| Evaluation discipline | Kim et al. and Wu & Keogh warn that anomaly-benchmark protocol choices can mislead. | The project documents limitations, but synthetic dependence remains a material external-validity constraint. |

## Contributions supported by the current evidence

1. **Audited evidence packaging.** The repository contains raw A/B/C CSVs, a frozen checkpoint/metadata contract, a canonical metric reconciliation, implementation traceability, and a Phase 4 figure register that preserves evidence boundaries. This is an engineering/reproducibility contribution, not proof of scientific external validity.
2. **Bounded synthetic detection comparison.** Experiment A supports within-cohort confusion-derived comparisons across 320 synthetic windows in six scenarios. The frozen LSTM has 120/120 synthetic fault recall and 2/200 false positives in that dataset. Repeated scenario structure prevents treating this as a deployment-rate or independent-incident result.
3. **Intent-to-treat diagnosis pilot accounting.** Experiment B preserves 42 records and retains two provider omissions as `UNASSESSABLE` in strict denominators. This supports transparent pilot reporting, not an LLM causal-effect or superiority claim.
4. **Local authorization-boundary test evidence.** Experiment C supports 11/11 attack-case containment and 16/16 audit-trail completeness in a bounded local harness, including recorded Wilson intervals. It does not support operational authorization assurance or a production security certification.
5. **Observed fallback evidence.** The 200-record live capture demonstrates local collection, persistence, bootstrap-rule mode, and logging. It does not demonstrate LSTM scoring because every score is null.

## Engineering integration that may be described carefully

- A repository implementation joins telemetry collection, fixed-contract synthetic LSTM scoring, diagnosis-agent interfaces, an SQLite approval workflow, local demo recovery, and event logging.
- Source audit confirms an intended live-LSTM path exists in code but the persistent live checkpoint and live inference evidence are absent.
- The approval workflow uses a scoped target, phrase, TTL, and audit events in a local demonstration. It is not authenticated authorization, not dual approval, and not evidence of remediation beyond the allowlisted local demo action.

## Hypotheses requiring future tests

The following are hypotheses, not current contributions:

- Quantitative LSTM context improves LLM diagnosis accuracy or causal precision.
- The integrated workflow reduces incident resolution time or operator workload.
- The approval layer is secure under realistic identities, multi-party authorization, and production threat models.
- The detector/general workflow transfers to external AnoMod data or other microservice estates.
- Live LSTM inference produces useful alert discrimination, stable scores, calibrated thresholds, or acceptable false-alarm rates.
- Model-selection or statistical differences generalize beyond the six synthetic scenarios and six hand-authored diagnosis cases.

## Required novelty boundaries

Do not use these labels without new, independently controlled evidence: “novel LSTM,” “causal representation,” “causal precision improvement,” “production-ready,” “secure autonomous recovery,” “NIST compliant,” “external validation,” “generalizes,” “live LSTM performance,” or “AnoMod result.”

The relevant evidence provenance is recorded in `PHASE5_CLAIM_TO_EVIDENCE_MATRIX.csv`; literature positioning is recorded in `PHASE5_RELATED_WORK_MATRIX.csv`.
