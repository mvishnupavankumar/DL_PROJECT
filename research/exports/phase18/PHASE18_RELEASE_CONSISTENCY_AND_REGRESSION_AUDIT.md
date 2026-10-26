# Phase 18 Release Consistency and Regression Audit

**Date:** 2026-10-18 (Asia/Kolkata)
**Scope:** Release-control reconciliation, non-destructive source review, renderer readiness discovery, and full repository regression. No new experiment, rendering, collection, target contact, configuration change, or model/database modification was performed.

## Baseline and preservation

| Item | Before audit |
| --- | --- |
| Repository root | `C:\DL_PROJECT` |
| Branch | `publish/research-without-external-dataset` |
| HEAD | `a32713c30a8ddca1425d44b1afbaf6d55a64c276` |
| Short Git status | 91 entries: 45 tracked modifications and 46 untracked top-level/path-collapsed entries |
| Full untracked Git status | 327 entries: 45 tracked modifications and 282 untracked leaf artifacts |

All pre-existing changes were preserved. No reset, clean, stash, commit, or overwrite of unrelated files occurred.

## Authoritative current control set and stale-status reconciliation

| Topic | Current control | Historical/stale ambiguity | Phase 18 resolution |
| --- | --- | --- | --- |
| Release checklist identifiers | `PHASE18_CANONICAL_MANUSCRIPT_RELEASE_CHECKLIST.md` | The finalization plan uses seven release criteria named QC-1–QC-7; the final evidence audit uses a different eight-item QC-1–QC-8 audit. | Retain both historical schemes and govern release with unique `REL-01` through `REL-12` checks. |
| Current release status | Phase 12/17 reports and canonical checklist | Older documents retain “Ready for Supervisor Review” language. | That is historical source-review status only. Camera-ready/publication release is **BLOCKED**. |
| Regression evidence | `PHASE18_FULL_SUITE_TEST_LOG.md` | Earlier 107-test records were historical and Phase 17 ran only a focused 40-test harness. | Current root-suite result is 116/116 passed, exit 0. |
| Rendering evidence | Phase 12 report plus Phase 18 tool discovery | Source-level reviews could be mistaken for page-level review. | No DOCX/PDF was generated and no page was inspected; visual verification is **BLOCKED**. |

## Current evidence-boundary review

- Experiment A remains a 320-window constructed synthetic benchmark; its counts and metric terminology remain bounded to that cohort.
- Experiment B remains a seven-configuration, six-case pilot. Strict ITT keeps the C5/INC-1002 and C7/INC-1004 `UNASSESSABLE` omissions; completed-case results remain separate.
- Experiment C retains separate 11/11 attack-containment and 16/16 audit-completeness denominators with their Wilson intervals.
- Historical live telemetry remains 200 `bootstrap_rules` records with 200 null LSTM scores. Live LSTM detection performance remains **UNMEASURED**.
- Experiment D remains unexecuted for production external evaluation and excluded from confirmatory manuscript claims.

## Full regression result

The root suite was inspected for external/production side effects and then executed in the Windows virtual environment with a dedicated workspace-local temporary root. The command, complete output, environment, and exit code are preserved in `PHASE18_FULL_SUITE_TEST_LOG.md`.

**Result: 116 passed, 0 failed, 0 errors, exit code 0, 65.70 seconds.** This verifies test-suite behavior only; it does not validate rendered layout, authorize Experiment D, or establish live performance.

## Renderer and inspection readiness

| Capability | Current discovery | Status |
| --- | --- | --- |
| Markdown-to-DOCX/PDF conversion | `pandoc` and `quarto` unavailable | **BLOCKED** |
| Office/PDF renderer | `soffice` and `libreoffice` unavailable | **BLOCKED** |
| PDF page inspection | `pdfinfo` and `pdftoppm` unavailable | **BLOCKED** |
| Generated supervisor-review DOCX/PDF | No artifact found; Phase 12 correctly created neither | **BLOCKED** |
| Page-by-page visual inspection | No generated PDF and no page rasterizer | **BLOCKED** |

No renderer, package, external service, or system setting was installed or changed. A future rendering procedure must use an approved installed conversion chain, create the selected output artifacts, rasterize every PDF page, and record inspection of every page before visual verification may pass.

## Final verdict

**Substantive research readiness: READY WITH DOCUMENTED LIMITATIONS.** Bounded claims and current controlling evidence are aligned at the source level, and the current full repository test suite passes.

**Camera-ready/publication release readiness: BLOCKED.** The ranked blockers are recorded in `PHASE18_PUBLICATION_BLOCKERS.md`; all publication-blocking `REL-` checks in the canonical checklist must be closed and independently reviewed before release.

## Actions not taken

No live pilot was started; no telemetry was collected; no target was contacted; no external dataset was accessed for a new experiment; Experiment D production evaluation was not executed; no runtime/model/threshold/database change occurred; and no unsupported scientific claim was introduced.
