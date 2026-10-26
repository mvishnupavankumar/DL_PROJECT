# AegisOps Phase 5 Reference Verification

**Audit date:** 2026-10-15 (Asia/Kolkata)  
**Scope:** Read-only review of `research/paper/AEGISOPS_RESEARCH_PAPER.md`, its active 16-entry bibliography, the canonical reconciliation, Phase 1–3 audit outputs, and Phase 4 figure register/validation. This audit creates only the Phase 5 export files; it does not revise the manuscript or bibliography.

## Method and source hierarchy

The active reference list was inventoried before any assessment. Every entry was checked against a publisher, conference, standards body, or author-maintained scholarly record where accessible. DOI resolver, publisher, or access restrictions are recorded rather than interpreted as verification. Direct URLs and access dates are in `PHASE5_BIBLIOGRAPHY_AUDIT.csv`.

Verification status means bibliographic identity only unless the claim-support column says otherwise. A real citation does not establish that AegisOps reproduced its results, that a feature is operational, or that an architecture is novel.

## Inventory outcome

| Result | Count | Interpretation |
| --- | ---: | --- |
| Active bibliography entries inventoried | 16 | The manuscript has one active reference register. |
| Bibliographic identities verified or verified with an access note | 14 | Identity, authors, title, year, and venue were found in a primary/authoritative record. |
| Partially verified entries requiring a bibliographic correction/check | 2 | AnoMod title differs from its current arXiv primary record; OmniAnomaly uses singular `Network`, not plural `Networks`. |
| Explicitly historical bibliography files | 1 | `research/paper/REFERENCES_VERIFICATION.md` declares itself superseded by `REFERENCE_VERIFICATION.md`; neither replaces this independent audit. |
| Uncited literature/general-claim gaps found | 3 | Shewhart/Holt-Winters history, “automated verification in SRE,” and specific guarded-remediation literature lack active supporting citations. |

## Citation-by-citation findings

The complete machine-readable register is the controlling detailed record. The following summarizes whether each source supports the way it is used.

| Key | Status | Supports | Does not support |
| --- | --- | --- | --- |
| Audibert et al. (2020), USAD | Verified metadata; ACM page inaccessible in this audit environment | USAD as a multivariate unsupervised anomaly-detection comparator | AegisOps performance or a claim that USAD was run here. |
| Edwards (1948) | Verified | Continuity-correction provenance for paired-proportion testing | Statistical validity under dependent synthetic windows by itself. |
| Hong et al. (2024), MetaGPT | Verified as preprint/ICLR-associated record | Role-separated LLM multi-agent workflow precedent | DevOps/incident-performance, approval safety, or AegisOps superiority. |
| Kim et al. (2022) | Verified | Caution about time-series evaluation protocols and point adjustment | That AegisOps’ small synthetic benchmark is externally valid. |
| Lee et al. (2023), Eadro | Verified | Multi-source detection/RCA research context | Recovery execution, approval safety, or equivalence to AegisOps. |
| Liu et al. (2008), Isolation Forest | Verified | Isolation Forest baseline description | Any temporal property for a point-vector implementation without explicit temporal features. |
| McNemar (1947) | Verified | Matched-pair proportion test provenance | Independence of repeated synthetic windows or broad model superiority. |
| Ping et al. (2026), AnoMod | Partially verified | Dataset purpose and modalities from the primary arXiv record | Any AegisOps external result; those outputs are absent/blocked. |
| Su et al. (2019), OmniAnomaly | Verified with title correction | Stochastic recurrent multivariate anomaly-detection related work | AegisOps LSTM architecture novelty. |
| Wilson (1927) | Verified metadata; publisher fetch denied | Wilson interval provenance | Production-security certification from 11 local attack cases. |
| Wu et al. (2020), MicroRCA | Verified | Graph/metric-based microservice RCA precedent | The manuscript’s broad “random walks or PageRank variants” characterization for all cited RCA systems. |
| Wu & Keogh (2021) | Verified | Benchmark-quality caution | A direct validation of AegisOps’ synthetic setup. |
| Zhang et al. (2021), CloudRCA | Verified | Multi-source RCA using KPIs, logs, and topology/KHBN | A PageRank-based description; its published method is KHBN, not a generic PageRank variant. |
| NIST SP 800-53 Rev. 5 | Verified authoritative standard | Governance vocabulary and a control reference | AegisOps compliance, authenticated dual authorization, or production assurance. |
| Malhotra et al. (2016) | Verified | LSTM encoder–decoder reconstruction anomaly-detection precedent | Novelty of the AegisOps LSTM architecture. |
| Wu et al. (2023), AutoGen | Verified preprint | Generic multi-agent LLM application framework | LLM effectiveness for AIOps, causal diagnosis, or safe remediation. |

## Claim-support corrections required before publication review

1. **AnoMod metadata:** the current primary arXiv record reads *Microservice Systems* (plural). The manuscript and active bibliography say *Microservice System* (singular). The ACM DOI page was blocked (403) in the audit tool, so retain the record but correct/check this title against the publisher before release.
2. **OmniAnomaly metadata:** the source title is *Robust Anomaly Detection for Multivariate Time Series through Stochastic Recurrent Neural Network* (singular). Correct the bibliography before release.
3. **RCA wording:** MicroRCA supports graph-based RCA and CloudRCA supports a knowledge-informed hierarchical Bayesian network over multi-source data. Do not describe both collectively as dynamic-topology traversal using PageRank/random walks.
4. **LLM wording:** AutoGen and MetaGPT support generic multi-agent-framework context. Neither provides evidence for AegisOps’ LLM diagnosis accuracy, causal precision, safety, or production suitability.
5. **NIST wording:** SP 800-53 supplies a governance reference only. Phase 3 establishes that the local implementation lacks authenticated dual approvers, so it must not be presented as implementing AC-3(2).

## Evidence-bound reading of the literature

The related literature establishes that LSTM reconstruction, Isolation Forest, unsupervised multivariate anomaly detection, graph/multimodal RCA, and LLM multi-agent orchestration are established prior art. The evidence currently supports only the project’s bounded engineering integration and local/synthetic evaluations:

- Experiment A: 320 synthetic windows (200 nominal, 120 fault), six scenarios.
- Experiment B: 42 records, seven configurations and six cases; the two `UNASSESSABLE` provider omissions remain in strict intent-to-treat denominators.
- Experiment C: 11/11 local-harness attack cases contained and 16/16 audit trails complete.
- Live telemetry: 200 records, all bootstrap-rule mode and all LSTM scores null; no independent performance evaluation.
- Experiment D: archive provenance/input is available, but external AnoMod performance is blocked and absent.

These boundaries are sourced to `PHASE2_METRIC_RECONCILIATION.md`, the Phase 3 architecture audit, and the Phase 4 validation report, not to the literature citations.

## Limitations

This was a document and web-record audit, not a literature review with full-text legal access to every paywalled item. ACM and Taylor & Francis delivery restrictions prevented direct publisher-page inspection for several entries; their restrictions are explicitly noted in the CSV. No citation was silently removed, no metadata was fabricated, and no historical verification assertion was treated as sufficient without independent checking.

**Phase 5 reference-verification disposition: B — bibliography inventory is complete, but metadata corrections, claim-scope corrections, and coverage gaps remain before a publication claim is supportable.**
