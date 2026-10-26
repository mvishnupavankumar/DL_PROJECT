# AegisOps Phase 4.1 Publication Figure Visual Remediation Report

**Date:** 2026-10-15 (Asia/Kolkata)  
**Scope:** Visual remediation of the eleven existing Phase 4 figure assets in this directory only. Raw evidence, model artifacts, application code, databases, historical reports, and the manuscript were not changed.

## Verdict

**B - Figures are usable, with one explicit verification limitation.**

All PNG and PDF-page visual checks passed, and SVG XML integrity passed. A graphical SVG rasterizer was unavailable in this environment, so direct visual raster inspection of the eleven SVG outputs could not be completed. This verdict does **not** assert publication acceptance, broader scientific validation, live LSTM performance, or AnoMod performance availability.

## Starting state and preflight

- The starting Git worktree was already dirty outside this directory; the Phase 4 directory was untracked from the prior phase.
- The existing Phase 4 manifest contained 41 entries and independently hash-verified before remediation with zero mismatches.
- The existing figure register, captions, validation report, manifest, and generator were read before edits.
- Every prior PNG was inspected; the SVG files were structurally parsed and source-reviewed. The PDF companions are single-page Pillow PDFs containing one 1800x1125 DCT image, so their visual content is the corresponding generated raster; no alternate vector page content is present.
- No external API, experiment, training, model inference, or dataset action was performed.

## Figure-by-figure remediation

| Figure | Issues found in prior rendering | Correction | Final validation | Remaining issue |
| --- | --- | --- | --- | --- |
| A | Title/subtitle and long box headers clipped; diagonal paths crossed dense labels. | Shortened display title, widened/split the topology, wrapped box text, and isolated the trust boundary. | Full size and 640px column review. | None. |
| B | Title, long model-stage labels, threshold text, callout, and footer clipped. | Shortened display title, equalized node widths, reduced type scale, and split the boundary callout. | Full size and 640px column review. | None. |
| C | Pipeline labels, session annotation, and optional branch overlapped. | Re-laid out flow into an upper collection path and lower guard/event path; made session statement two lines. | Full size and 640px column review. | None. |
| D | Eight-node single row clipped and overlapped; workflow callout was crowded. | Split into two sequential rows, added whitespace, and retained the API/approval boundary statement. | Full size and 640px column review. | None. |
| E1 | Title/subtitle clipped. | Compact title/subtitle and a consistently spaced legend/chart region. | Counts and all rate labels checked against raw data. | None. |
| E2 | Matrix axis labels and lower panels/footer collided or ran outside the canvas. | Increased panel margins and placed row/column labels inside each panel’s reserved space. | TP/FP/TN/FN values checked for all four methods. | None. |
| E3 | Title clipped and legend/labels crowded. | Compact heading, centered legend, and separated scenario labels. | Scenario values checked against raw data. | None. |
| E4 | Title clipped, labels crowded, omitted cases hard to read; Groq matching was case-sensitive. | Compact title, bottom configuration key, visible omission labels, and case-insensitive Groq classification. | All seven strict ITT and completed-case values checked. | None. |
| E5 | Case-taxonomy labels overlapped each other and the heading. | Replaced crowded inline labels with four clearly separated taxonomy tiles. | 11/11, 16/16, and Wilson intervals checked. | None. |
| E6 | Card labels overlapped counts; one-record latency segment label was unreadable. | Increased card whitespace and added a readable count line below the stacked bar. | 200 rows, bootstrap-only mode, null-score count, and fault-mode counts checked. | None. |
| F | Long readiness labels exceeded boxes. | Shortened display labels while preserving the same availability/blocker states. | Full size and 640px column review. | None. |

## Remaining verification limitation

- A dedicated graphical SVG rasterizer was unavailable. The installed browser did not write a headless local SVG raster, and no Poppler, Inkscape, or compatible Python renderer was installed. All 11 SVG files are well-formed XML and are generated from the same source layout and labels as the inspected PNG/PDF assets, but this is not a substitute for a graphical SVG rendering check in a future release environment.

## Controls retained

- Synthetic Experiment A remains limited to its 320 potentially dependent synthetic windows.
- Experiment B retains strict ITT denominators and explicitly visible `UNASSESSABLE` API omissions.
- Experiment C remains labelled as a bounded local safety harness, not a production-security certification.
- Live telemetry remains bootstrap-rules-only with 200 null LSTM scores; no live performance chart was added.
- Approval remains an unauthenticated audit label/workflow guard; recovery remains local-demo-only.
- Experiment D remains a readiness/provenance panel only; no AnoMod performance result was plotted.

## Modified files

- `generate_phase4_figures.py`
- All eleven figure SVG, PNG, and PDF renderings
- `FIGURE_REGISTER.md`
- `FIGURE_VALIDATION_REPORT.md`
- `PHASE4_SHA256_MANIFEST.json`
- This report

`FIGURE_CAPTIONS.md` required no factual or boundary correction and was not edited.
