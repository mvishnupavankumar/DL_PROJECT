# AegisOps Phase 19 — Renderer Capability Inventory and Environment-Owner Request

**Discovery date:** 2026-10-19 (Asia/Kolkata)  
**Method:** non-installing command discovery/version probes and virtual-environment import checks. No renderer, package, external service, or system component was installed or used to create a document.

## Installed capability inventory

| Capability | Checked executable/package | Result | Consequence |
| --- | --- | --- |
| Markdown → DOCX/PDF | `pandoc`, `quarto` | Not found | No supported conversion entry point. |
| Office conversion | `soffice`, `libreoffice`, `winword` | Not found | No DOCX-driven PDF production route. |
| TeX/typographic PDF engine | `typst`, `xelatex`, `pdflatex`, `latexmk` | Not found | No installed PDF engine for a Pandoc route. |
| HTML/PDF alternative | `wkhtmltopdf` | Not found | No installed alternative conversion route. |
| PDF metadata/page count | `pdfinfo` | Not found | Cannot record generated PDF page count. |
| PDF → page images | `pdftoppm`, `pdftocairo`, ImageMagick `magick` | Not found | Cannot rasterize every PDF page for required visual inspection. |
| Windows `convert.exe` | Present at `C:\Windows\System32\convert.exe` | NTFS volume-conversion utility, not ImageMagick | Not a PDF/image renderer. |
| Base runtimes | Python 3.11.9; Node.js v25.3.0 | Present | No repository rendering workflow or qualifying packages found. |
| Virtual-environment libraries | `docx`, `markdown`, `pypandoc`, `weasyprint`, `reportlab`, `pypdf`, `PyPDF2`, `fitz`, `pdfplumber` | All unavailable | No documented local substitute chain. |

## Complete-route determination

**No complete approved installed route exists.** In particular, the environment lacks both (a) an auditable Markdown-to-DOCX/PDF conversion path and (b) a PDF page-rasterizer. Therefore no DOCX/PDF may be represented as generated and no page-level visual inspection may be represented as completed.

Phase 10’s proposed procedure remains technically appropriate once provisioned: Pandoc converts the active Markdown source to DOCX and PDF through a documented PDF engine, then Poppler’s `pdfinfo` records page count and `pdftoppm` emits one image per page. The exact commands must be rerun and versioned after the environment owner supplies an approved chain; they were not run here.

## Environment-owner request

Please provide or approve an already-installed, reproducible local toolchain with all of the following capabilities:

1. Markdown (`gfm`) to DOCX conversion that preserves tables, equations, linked local images, references, and UTF-8 text.
2. Markdown to PDF conversion with a documented, local PDF engine and controllable resource path.
3. PDF metadata/page-count inspection.
4. Deterministic PDF-to-PNG page rasterization at a documented resolution.
5. Permission to record exact executable paths, versions, commands, generated-file hashes, page count, and inspection findings in the release record.

An acceptable common route would be approved installed versions of Pandoc, a compatible local PDF engine (for example XeLaTeX), and Poppler (`pdfinfo`, `pdftoppm`). The environment owner must approve the actual versions and any venue template before use. No external rendering service is requested or authorized.

## Stop condition

REL-10 and REL-11 remain **BLOCKED**. Rendering must not start until the requested capabilities and approval are present. Visual inspection must not be marked PASS until the final PDF exists, every page has been rasterized, and every rendered page has been inspected.
