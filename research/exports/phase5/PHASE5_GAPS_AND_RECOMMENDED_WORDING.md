# AegisOps Phase 5 Gaps and Recommended Wording

This is an audit aid, not a manuscript edit. It gives bounded alternatives for a later, separately authorized correction pass.

| Priority | Gap or risk | Evidence | Avoid | Bounded replacement for later review |
| ---: | --- | --- | --- | --- |
| 1 | External validation absent | Phase 1/2: AnoMod production artifacts and ratification are absent; Phase 4 omits external plots | “validated on AnoMod” or “external generalization” | “AnoMod archive provenance is present; contract-valid external evaluation is blocked and no external performance result is reported.” |
| 2 | Live LSTM performance absent | 200 telemetry records; 200 `bootstrap_rules`; 200 null scores | “live LSTM detected…”, live ROC/FPR/alarms/hour, deployment performance | “The audited session demonstrates collection and rule-fallback logging; it does not demonstrate live-LSTM inference or independently labeled performance.” |
| 3 | Synthetic detection scope | A has 320 structured synthetic windows across six scenarios | “production detection accuracy” or a rate estimate beyond the dataset | “On the defined synthetic-window benchmark, the frozen LSTM produced 120/120 fault detections and 2/200 nominal false positives.” |
| 4 | Diagnosis pilot scope | B has 42 records, six cases, two ITT `UNASSESSABLE` omissions | “LLM improvement,” “causal precision,” or “superiority” | “The six-case pilot reports configuration-specific strict intent-to-treat results, preserving provider omissions as `UNASSESSABLE`; it is not a causal or generalization study.” |
| 5 | Approval/security scope | C: 11/11 local attack cases; Phase 3: no authenticated dual approvers | “NIST compliant,” “secure recovery,” or “autonomous safe recovery” | “The local harness tested scoped approval and audit controls against 11 specified attack cases; authenticated dual authorization and production security assurance were not evaluated.” |
| 6 | RCA literature accuracy | MicroRCA graph RCA; CloudRCA uses multi-source/KHBN | “MicroRCA and CloudRCA both traverse dynamic topologies using PageRank/random walks” | “Prior RCA systems use graph or multi-source probabilistic approaches; their specific mechanisms differ.” |
| 7 | LLM literature scope | AutoGen/MetaGPT are generic frameworks, not AIOps trials | “literature demonstrates LLMs improve operations diagnosis” | “Generic LLM multi-agent frameworks motivate the workflow design; AegisOps’ operational effectiveness remains a pilot question.” |
| 8 | Bibliographic metadata | AnoMod singular/plural discrepancy; OmniAnomaly singular `Network` discrepancy | Releasing current titles unchanged | “Verify publisher metadata and correct title spelling before release; retain identifiers and uncertain venue details until confirmed.” |
| 9 | Literature coverage | No active source for Shewhart/Holt-Winters history, SRE verification, or guarded-remediation systems | Broad historical/industry claims without citation | “Either add authoritative primary sources in a later reference-only update or narrow the uncited narrative to an implementation description.” |
| 10 | Statistical scope | Correlated/repeated synthetic windows; six scenario aggregates | A tiny p-value as deployment proof | “Window-level tests are descriptive within the synthetic cohort; scenario-level inference is exploratory and does not establish operational superiority.” |

## Minimum correction order

1. Correct or publisher-check the two bibliographic metadata discrepancies without deleting uncertain references.
2. Repair claim-to-source scope, beginning with external validation, live LSTM, approval/security, and LLM effectiveness statements.
3. Add primary references or trim the three uncited literature assertions.
4. Keep intent-to-treat omissions and all A/B/C/D/live evidence boundaries unchanged.
5. Re-run a text-only claim/citation audit after a separately authorized manuscript revision; do not treat this report as an edit.
