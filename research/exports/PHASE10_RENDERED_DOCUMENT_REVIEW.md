# AegisOps Phase 10 Rendered-Document Review

**Audit date:** 2026-10-16 (Asia/Kolkata)  
**Reviewed source:** `research/paper/AEGISOPS_RESEARCH_PAPER.md`  
**Outcome:** **Rendered review blocked by unavailable local tooling; no PDF/DOCX was generated or opened.**

## 1. Renderer discovery

The repository contains no established Markdown-to-PDF/DOCX workflow or current rendered manuscript artifact. The available environment was checked for the usual reproducible command-line components:

| Component | Result |
| --- | --- |
| Pandoc | Not installed/available. |
| Quarto | Not installed/available. |
| LibreOffice / `soffice` | Not installed/available. |
| `wkhtmltopdf` | Not installed/available. |
| Poppler `pdfinfo` / `pdftoppm` | Not installed/available. |
| `.venv` rendering libraries (`weasyprint`, `markdown`, `reportlab`) | Not available. |
| Node.js | Available, but no repository Markdown rendering workflow or renderer dependency was found. |

This audit did not install a renderer, download dependencies, or create a substitute rendering system. No current PDF or DOCX was found under `research/`.

## 2. Source-level review completed

The source Markdown was read and its figure paths checked. It has a title, explicit author/affiliation/venue placeholders, a clear supervisor-review status, 10 embedded main-paper figures, and Figure E3 identified as supplementary. Section/table placement is coherent at source level:

| Item | Source-level result | Rendered-page result |
| --- | --- | --- |
| Title and status | Present at lines 1 and 6. | Not inspected: no rendered page. |
| Author, affiliation, venue | Deliberate placeholders at lines 3–5. | Not inspected: no rendered page. |
| Date | Not present. | Release-metadata issue; no rendered page. |
| Tables 1–4 | Markdown tables and evidence boundaries checked against raw/Phase 2 sources. | Not inspected for wrapping, overflow, or page breaks. |
| Main-paper figures | Paths exist and controlled PNGs were individually opened; see Phase 10 figure verification CSV. | Not inspected in document pagination. |
| References | Source numbering 1–16 maps to active reference audit; AnoMod publisher confirmation remains pending. | Not inspected for page-break or typography issues. |

No claim is made that the manuscript’s page layout, font embedding, equation rendering, table pagination, image scaling, references, or line wrapping has passed a rendered review.

## 3. Reproducible manual rendering and inspection procedure

Run the following only in an environment with Pandoc, a TeX PDF engine such as XeLaTeX, and Poppler installed. The commands are intentionally not executed in this audit.

```powershell
Set-Location C:\DL_PROJECT\research\paper
New-Item -ItemType Directory -Force ..\exports\phase10_render | Out-Null

pandoc AEGISOPS_RESEARCH_PAPER.md `
  --from gfm `
  --resource-path=".;..\figures\phase4" `
  --pdf-engine=xelatex `
  --output ..\exports\phase10_render\AEGISOPS_SUPERVISOR_REVIEW.pdf

pandoc AEGISOPS_RESEARCH_PAPER.md `
  --from gfm `
  --resource-path=".;..\figures\phase4" `
  --output ..\exports\phase10_render\AEGISOPS_SUPERVISOR_REVIEW.docx

pdfinfo ..\exports\phase10_render\AEGISOPS_SUPERVISOR_REVIEW.pdf
pdftoppm -png -r 200 `
  ..\exports\phase10_render\AEGISOPS_SUPERVISOR_REVIEW.pdf `
  ..\exports\phase10_render\page
```

For the required rendered review, open every generated `page-*.png` at full size and review every page at a realistic manuscript-column display. Confirm all titles, placeholders, tables, formulas, references, captions, source/boundary notes, and all embedded figures are complete and legible; check that no figure is cropped, distorted, duplicated, stale, or moved away from its intended discussion. Record the PDF and DOCX SHA-256 values, page count, page dimensions, render tool/version, and any corrections in a new versioned release report.

## 4. Release consequence

The Markdown source and separately opened figure assets passed the source-level checks described in the release-provenance audit. However, absence of a page-level render prevents verification of layout-dependent defects. This blocker, together with unresolved release provenance and metadata, requires a **B** verdict for Phase 10 rather than an A verdict.

