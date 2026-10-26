# AegisOps Phase 19 — Updated Publication Blockers and Next Action

**Release verdict:** **BLOCKED**  
**Control source:** `research/paper/PHASE18_CANONICAL_MANUSCRIPT_RELEASE_CHECKLIST.md` (REL-01 through REL-12). Phase 18 remains historical evidence; this list does not rewrite it.

| Priority | REL control(s) | Current blocker | Evidence from Phase 19 | Exact closure action | Accountable role |
| ---: | --- | --- | --- | --- | --- |
| 1 | REL-08 | Intended release-input set is not owner-approved/frozen; worktree remains dirty. | Exact candidate paths/hashes and dirty Git state are in the proposed manifest. | Approve/revise the named set and authorize a named snapshot; then regenerate/finalize a release manifest for that approved state. | Manuscript/release owner |
| 2 | REL-06 | Author, affiliation, contact, date, venue/template, and declarations are absent. | Metadata sheet records only placeholders/no verified values. | Complete and approve every required metadata/declaration field. | Manuscript owner |
| 3 | REL-07 | AnoMod publisher-page metadata remains unconfirmed; no accepted limitation record exists. | ACM official DOI endpoint was inaccessible (HTTP 403); proposal supplied. | Obtain official publisher metadata or approve the limitation wording for the intended release. | Research supervisor/manuscript owner |
| 4 | REL-10 | No approved installed Markdown-to-DOCX/PDF renderer. | Rechecked executables/packages; complete local route absent. | Environment owner supplies/approves a local versioned toolchain and venue template. | Environment owner |
| 5 | REL-05, REL-11 | No generated final PDF and no PDF page rasterizer; source checks cannot verify layout. | No DOCX/PDF generated; `pdfinfo`/`pdftoppm` absent. | Generate final artifacts from approved frozen inputs, rasterize every PDF page, inspect every page, and log defects/corrections. | Research engineer/reviewer |
| 6 | REL-12 | Independent final release decision unavailable. | Multiple publication controls remain blocked/unverified. | Designated reviewer confirms all controls and issues an independent verdict. | Research supervisor/release manager |

## Controls not changed

REL-01–REL-04 and REL-09 remain **PASS**. REL-05 remains **UNVERIFIED**. REL-06–REL-08 and REL-10–REL-12 remain **BLOCKED**. No status was upgraded because this phase created preparatory records rather than the owner authorization, publisher evidence, renderer output, or page-level inspection required by the controls.

## Continuing evidence boundaries

Live LSTM detection performance is **UNMEASURED**. Experiment A remains synthetic; Experiment B remains a six-case exploratory pilot retaining both `UNASSESSABLE` records in strict ITT; Experiment C remains a bounded local harness with separate denominators; Experiment D remains unexecuted/excluded from performance claims. None of these boundaries is altered by release preparation.

## Next-action recommendation

**First human decision:** the manuscript/release owner must approve or revise `PHASE19_PROPOSED_RELEASE_PROVENANCE_MANIFEST.sha256` and complete `PHASE19_METADATA_OWNER_APPROVAL_SHEET.md`. This is the earliest safe decision because it defines what would be frozen and what a renderer would render. It does not authorize rendering by itself; the environment owner’s toolchain approval remains separately required.
