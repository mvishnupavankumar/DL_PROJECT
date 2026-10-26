# AegisOps Phase 10 Release Provenance Audit

**Audit date:** 2026-10-16 (Asia/Kolkata)  
**Scope:** Current-worktree provenance and source-manuscript review. This audit created only the three Phase 10 deliverables listed in Section 8. It did not change the manuscript, figures, raw evidence, model artifacts, databases, experiment outputs, source code, or either historical manifest.

## Verdict

**B — Source manuscript and controlled figures are internally consistent with the reviewed evidence, but the release package remains incomplete.**

The primary quantitative claims, figure boundaries, and current controlled PNG assets passed this source-level review. A rendered PDF/DOCX could not be generated or page-inspected in the available environment; the worktree is dirty; both historical integrity manifests have recorded mismatches; release metadata remains incomplete; and AnoMod publisher metadata remains unresolved. This is not a publication-ready determination.

## 1. Repository identity and starting state

| Field | Observed value |
| --- | --- |
| Repository root | `C:\DL_PROJECT` |
| Branch | `publish/research-without-external-dataset` |
| HEAD commit | `a32713c30a8ddca1425d44b1afbaf6d55a64c276` |
| HEAD subject | `Publish AegisOps research without external dataset payload` |
| Starting porcelain entries | 77 total: 40 tracked changes and 37 untracked paths |
| Index state | No staged entries observed during this audit. |
| Current manuscript reviewed | `research/paper/AEGISOPS_RESEARCH_PAPER.md` (22,430 bytes; source Markdown) |
| Controlled figure directory | `research/figures/phase4/` |

The dirty worktree means that this review applies to the observed files, not to `HEAD` alone. It must not be represented as a committed release snapshot. No reset, clean, stash, commit, or rewrite of an existing artifact was performed.

## 2. Inputs reviewed

The following current manuscript-control documents were read and cross-checked:

- `research/paper/AEGISOPS_RESEARCH_PAPER.md`
- `research/paper/CLAIM_EVIDENCE_MAP.csv`
- `research/paper/FIGURE_REGISTER.md`
- `research/paper/REFERENCE_VERIFICATION_AUDIT.md`
- `research/paper/MANUSCRIPT_QA_REPORT.md`
- `research/paper/SUPERVISOR_REVIEW_READINESS.md`
- `research/exports/PHASE1_EVIDENCE_FREEZE_AUDIT.md`
- `research/exports/PHASE2_METRIC_RECONCILIATION.md`
- `research/exports/PHASE2_STATISTICAL_VERIFICATION.md`
- `research/exports/PHASE3_IMPLEMENTATION_ARCHITECTURE_AUDIT.md`
- `research/figures/phase4/FIGURE_REGISTER.md`
- `research/figures/phase4/FIGURE_CAPTIONS.md`
- `research/figures/phase4/FIGURE_VALIDATION_REPORT.md`
- `research/exports/phase9/PHASE9_FIGURE_REMEDIATION_REPORT.md`

The current manuscript title is present. Author, affiliation, and venue correctly remain explicit placeholders at lines 3–5. A manuscript date is not present in the Markdown source; that is a release-metadata omission, not an evidence discrepancy.

## 3. Integrity-manifest status

Neither historical manifest was altered or silently refreshed.

| Manifest | Direct verification result | Interpretation |
| --- | --- | --- |
| `research/MANIFEST_SHA256.json` | 15 of 22 entries match; 7 differ | Historical root manifest. Mismatches: `research/STATISTICAL_AUDIT.md`, `research/SAFETY_EVALUATION.md`, `research/FINAL_EXPERIMENT_REPORT.md`, and the current B/C raw metric and prediction files. |
| `research/figures/phase4/PHASE4_SHA256_MANIFEST.json` | 36 of 43 entries match; 7 differ | Historical Phase 4 manifest. The five Phase 9 corrected PNGs, the scoped generator, and the Phase 4 register differ by documented design. |

The Phase 4 differences are `FIG_B_FROZEN_LSTM.png`, `FIG_D_DIAGNOSIS_APPROVAL.png`, `FIG_E2_CONFUSION_MATRICES.png`, `FIG_E4_DIAGNOSIS_PILOT.png`, `FIG_E6_LIVE_EVIDENCE.png`, `FIGURE_REGISTER.md`, and `generate_phase4_figures.py`. Their provenance is documented separately in Phase 9; the older Phase 4 manifest remains a historical record rather than a current release manifest.

## 4. Direct source-to-evidence reconciliation

| Evidence area | Current source check | Manuscript location | Result |
| --- | --- | --- | --- |
| Experiment A population and counts | `detection_predictions.csv` directly yielded 320 rows (200 normal, 120 fault). Rules = 120/0/200/0; Isolation Forest = 57/4/196/63; frozen LSTM = 120/2/198/0; Combined = 120/2/198/0 (TP/FP/TN/FN). | Abstract line 10; Table 1 lines 91–98; dataset statement lines 73 and 79. | Matched. |
| A statistics | The controlling Phase 2 verification records `b=63`, `c=0`, exact p approximately `2.1684e-19`, and six-scenario `W=0`, `p=0.03125` as exploratory. | Lines 83–85. | Matched and suitably bounded to clustered synthetic scenarios. |
| A rate limitation | `detection_metrics.csv` retains historical `false_alarms_per_hour` fields, but Phase 2 marks them unsupported without an exposure denominator. | Line 98 excludes operational alarms-per-hour claims. | No discrepancy; exclusion is correct. |
| Experiment B | `diagnosis_predictions.csv` directly yielded 42 rows across 7 configurations. The only `UNASSESSABLE` records are C5/`INC-1002` and C7/`INC-1004`. | Lines 74, 79, and Table 2 lines 110–124. | Matched; strict ITT and completed-case denominators remain distinct. |
| Experiment C | `safety_test_results.csv` directly yielded 16 rows, 11 attack cases all passing, and 16 verified audit trails. Current metrics retain Wilson intervals [0.7412, 1.0000] and [0.8064, 1.0000]. | Lines 75 and 79; Table 3 lines 128–139. | Matched; bounded local-harness wording is retained. |
| Live telemetry | `telemetry.csv` directly yielded 200 rows: 200 `bootstrap_rules` records, 200 null scores, and 0 non-null live-LSTM scores. | Abstract line 10; Table 4 lines 143–148; Figure E6 line 168. | Matched; no live performance metric is claimed. |
| Experiment D | Phase 1/2/3 evidence records AnoMod archive and extraction provenance, but no contract-valid predictions, metrics, ratification, or external result. | Lines 77, 146, 164, and 170–172. | Matched; readiness/provenance only. |

No current scientific contradiction was found between these controlling sources and the reviewed manuscript. The Phase 8 report’s clipping finding concerns a prior manuscript/figure state; its five named PNG defects were remediated and separately validated in Phase 9.

## 5. Figure provenance and review

All eleven registered controlled PNGs were present, hash-recorded, opened, and inspected at full resolution in this audit. Titles, labels, source/boundary notes, and stated values were readable. The Phase 4/9 retained column-scale checks apply to the current controlled assets: the six unchanged files still match the Phase 4 manifest, and the five changed targets match their Phase 9 remediation hashes. No controlled figure was duplicated under another ID, stretched, or treated as a result outside its registered manuscript section.

The machine-readable per-figure review is `PHASE10_FIGURE_VERIFICATION.csv`. Its review found the following boundaries intact:

- A–D are implementation/contract/workflow diagrams, not production-operation evidence.
- E1–E3 remain synthetic Experiment A results; E3 remains supplementary and exploratory.
- E4 retains both strict ITT and completed-case values with C5/C7 omissions visible.
- E5 retains separate 11/11 and 16/16 denominators and local-harness wording.
- E6 expressly reports bootstrap-only, null-score, non-performance live evidence.
- F is a blocked-readiness/provenance panel, not an AnoMod performance chart.

## 6. Reference and AnoMod metadata check

The manuscript correctly retains the Phase 5/active-reference-audit limitation: AnoMod’s authoritative arXiv record is available, while the reported DOI `10.1145/3793302.3793324` requires publisher-page confirmation. On 2026-10-16, a direct request to the ACM DOI landing page returned HTTP 403. Accordingly, the manuscript’s line-200 wording, “publisher confirmation pending,” remains appropriate. No metadata was fabricated or promoted from a search snippet.

## 7. Release blockers and resolution order

1. Freeze or version the current dirty worktree before calling any file set a release candidate.
2. Create a new versioned integrity manifest for the selected release snapshot; preserve, do not overwrite, the two historical manifests.
3. Install or make available a reproducible Markdown-to-PDF/DOCX plus PDF page-rendering route, then generate and inspect the rendered manuscript before external circulation.
4. Confirm author, affiliation, venue, and manuscript date metadata.
5. Obtain AnoMod publisher-page confirmation or retain the current unresolved citation wording.
6. Keep live-LSTM performance and Experiment D external-performance claims blocked unless separately authorized, contract-valid evidence is produced.

## 8. Files changed by this phase

Only these new Phase 10 deliverables were created:

- `research/exports/PHASE10_RELEASE_PROVENANCE_AUDIT.md`
- `research/exports/PHASE10_RENDERED_DOCUMENT_REVIEW.md`
- `research/exports/PHASE10_FIGURE_VERIFICATION.csv`

No PDF or DOCX was generated. No file outside the Phase 10 deliverables was modified by this phase.

