# AegisOps Phase 19 — AnoMod Bibliographic Verification and Limitation Proposal

## Scope and result

This is a bibliographic/provenance check only. It does **not** evaluate AnoMod, download it, execute Experiment D, or validate any AegisOps model on external data.

| Item | Result |
| --- | --- |
| Active manuscript entry | Reference 8: Ping et al.; arXiv `2601.22881`; reported DOI `10.1145/3793302.3793324`; publisher confirmation explicitly pending |
| Existing primary evidence | `REFERENCE_VERIFICATION_AUDIT.md` records the arXiv primary record and the plural title “Microservice Systems.” |
| Existing audit limitation | Phase 5 records that the ACM page returned 403 and labels the reported DOI/venue partially verified. |
| Phase 19 official-source attempt | On 2026-10-19, the permitted verifier requested `https://dl.acm.org/doi/10.1145/3793302.3793324`; the official endpoint returned HTTP 403. The DOI resolver was not accessible through that verifier. |
| Publisher metadata confirmation | **Not completed.** No independent publisher-page fields were inferred from the inaccessible page. |
| External AegisOps evaluation | **Not performed and not supported.** Archive/provenance is not model validation. |

## Decision

REL-07 remains **BLOCKED**. The official endpoint’s access limitation is not evidence that the DOI, venue, authors, pages, or title are wrong; it is also not evidence that they are confirmed. The active manuscript must not silently promote the reported DOI/venue to publisher-verified metadata.

## Proposed limitation wording for supervisor approval

> AnoMod is cited from its primary arXiv record (`arXiv:2601.22881`). A reported ACM DOI (`10.1145/3793302.3793324`) is retained as reported metadata, but direct publisher-page confirmation was unavailable at release review. AnoMod archive/provenance evidence is not an AegisOps external evaluation; no contract-valid AnoMod predictions, calibrated threshold, or external performance metric is reported.

Use this wording only after the research supervisor/manuscript owner explicitly approves it, or replace it with exact publisher-verified bibliographic metadata. Neither option changes the manuscript’s existing boundary: Experiment D remains provenance/readiness only.

## Required closure evidence

One of the following must be recorded:

1. An accessible official ACM/publisher record, with exact author list, title, venue, publication year, pages, and DOI transcribed and independently checked; or
2. A supervisor/manuscript-owner approval that the limitation wording above is retained in the release version.

The current arXiv identity and reported DOI support only related-work/dataset context. They never support a claim of external model validation or generalization.
