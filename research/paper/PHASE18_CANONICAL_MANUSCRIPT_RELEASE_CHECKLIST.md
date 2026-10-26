# AegisOps Canonical Manuscript Release Checklist

**Established:** 2026-10-18 (Asia/Kolkata)
**Authority for current release control:** This checklist supersedes only the *release-gate interpretation* of conflicting QC numbering in prior planning/audit documents. It does not replace historical evidence, results, manifests, or prior reports.

## Reconciliation of prior QC schemes

`MANUSCRIPT_FINALIZATION_PLAN.md` retains a seven-item, release-oriented QC list (`QC-1` through `QC-7`). `FINAL_EVIDENCE_AUDIT.md` retains an eight-item supervisory audit using the same identifiers for different topics. Both remain valuable historical records, but neither identifier set is safe as a single current release gate. The stable `REL-` identifiers below are the authoritative Phase 18 release checks. Each references the prior material rather than renumbering or rewriting it.

| Status | Meaning |
| --- | --- |
| **PASS** | Current evidence meets the stated acceptance criterion. |
| **FAIL** | Current evidence contradicts the criterion. |
| **BLOCKED** | A required action, authority, tool, or evidence source is absent. |
| **UNVERIFIED** | Evidence has not been inspected at the required level. |

## Canonical release checks

| ID | Check and acceptance criterion | Evidence / reproducible verification | Status | Remaining action and accountable role | Publication blocker |
| --- | --- | --- | --- | --- | --- |
| REL-01 | **Claim-to-evidence consistency.** Manuscript claims must remain bounded to synthetic Experiment A, pilot Experiment B, and local Experiment C; live LSTM performance and Experiment D performance must not be claimed. | `AEGISOPS_RESEARCH_PAPER.md`; `MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`; `PHASE17_MANUSCRIPT_QC_REPORT.md`. Source inspection confirms 200 bootstrap-rule rows/200 null scores and no live-performance claim. | **PASS** | Maintain this boundary in any later edit. Research supervisor. | No |
| REL-02 | **Canonical metric reconciliation.** Experiment A counts, Experiment B denominators including both `UNASSESSABLE` records, and Experiment C separate denominators/Wilson intervals must match controlling evidence. | `CANONICAL_METRIC_RECONCILIATION.md`; `PHASE11_FINAL_QA_REPORT.md`; manuscript Tables 1–4. | **PASS** | Re-run source cross-check after any results-table edit. Research engineer. | No |
| REL-03 | **Dataset and experiment scope.** Synthetic A, six-case pilot B, local-harness C, live bootstrap telemetry, and excluded/unexecuted D must be clearly distinguished. | `FINAL_EVIDENCE_AUDIT.md`; `FINAL_EXPERIMENT_REPORT.md`; manuscript §§8–11. | **PASS** | Preserve labels and evidence boundaries. Research supervisor. | No |
| REL-04 | **Statistical validity and limitations.** Window dependence, exploratory scenario analysis, strict ITT/completed-case distinction, Wilson intervals, and unavailable operational rates must be disclosed. | `STATISTICAL_AUDIT.md`; `MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`; manuscript §§9–10. | **PASS** | Retain caveats; do not promote exploratory or source-level checks to deployment evidence. Research supervisor. | No |
| REL-05 | **Figures, tables, algorithms, and references.** Source paths, captions, definitions, and release-candidate Figure A.2 must align; original stale Figure A.2 must remain excluded. Rendering must be visually checked before release. | `FIGURE_AND_TABLE_INDEX.md`; `FIGURE_AND_TABLE_REGISTER.md`; `REFERENCE_VERIFICATION.md`; `PHASE11_FINAL_QA_REPORT.md`. | **UNVERIFIED** | Perform rendered-document review of all figures, tables, equations, references, algorithms, and cross-references after a reproducible renderer is available. Research engineer/reviewer. | Yes |
| REL-06 | **Author and venue metadata.** Author, affiliation, corresponding author, manuscript date, venue, and venue template must be confirmed. | Visible placeholders in `AEGISOPS_RESEARCH_PAPER.md`; Phase 11/12 release reports. | **BLOCKED** | Supply and approve all metadata and venue/template requirements. Manuscript owner. | Yes |
| REL-07 | **AnoMod bibliographic state.** Either confirm publisher-page metadata or preserve an explicit limitation; do not treat archive provenance as external model validation. | `PHASE11_FINAL_QA_REPORT.md`; `PHASE12_RENDER_AND_RELEASE_REPORT.md`; `REFERENCE_VERIFICATION.md`. | **BLOCKED** | Manuscript owner/supervisor must confirm publisher metadata or explicitly accept and retain the limitation for the release. | Yes |
| REL-08 | **Release provenance.** A release-specific manifest must identify the selected immutable input state without overwriting historical manifests. The dirty worktree must not be represented as a clean release. | `PHASE12_ARTIFACT_MANIFEST.sha256`; `PHASE12_RENDER_AND_RELEASE_REPORT.md`; current Git status. | **BLOCKED** | Freeze/version the intended release inputs and create a scoped release manifest after owner approval. Release manager. | Yes |
| REL-09 | **Full repository regression.** Root test suite must pass in the documented virtual environment using isolated temporary paths; test output and exit code must be retained. | `PHASE18_FULL_SUITE_TEST_LOG.md`: `116 passed in 65.70s`, exit 0, `.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_tmp_phase18_full_verified`. | **PASS** | Re-run after code or dependency changes. Research engineer. | No |
| REL-10 | **Reproducible DOCX/PDF generation.** A documented, approved installed toolchain must generate the review artifacts from selected inputs. | Phase 12 tool discovery; Phase 18 tool recheck. `pandoc`, `quarto`, `soffice`, and `libreoffice` are unavailable. | **BLOCKED** | Provide an approved installed Markdown-to-DOCX/PDF toolchain; then document exact versioned commands. Environment owner. | Yes |
| REL-11 | **Page-by-page visual inspection.** Every generated PDF page must be rasterized and inspected for layout, figures, equations, tables, references, metadata, and clipping. | Phase 12 report; Phase 18 tool recheck. No generated review PDF and no `pdfinfo`/`pdftoppm`. | **BLOCKED** | Provide page-inspection capability, render the final PDF, and inspect every page. Research engineer/reviewer. | Yes |
| REL-12 | **Independent final release verdict.** All publication-blocking checks above must be PASS and a designated reviewer must issue a release decision. | This checklist and `PHASE18_RELEASE_CONSISTENCY_AND_REGRESSION_AUDIT.md`. | **BLOCKED** | Resolve REL-05 through REL-11 as applicable and obtain reviewer sign-off. Research supervisor/release manager. | Yes |

## Current verdict

**Substantive research readiness: READY WITH DOCUMENTED LIMITATIONS.** The manuscript source preserves the bounded-claims strategy and current controlling results.

**Camera-ready/publication release readiness: BLOCKED.** Passing source and regression checks do not substitute for provenance closure, approved metadata, bibliographic confirmation/limitation, reproducible document generation, or page-by-page inspection.
