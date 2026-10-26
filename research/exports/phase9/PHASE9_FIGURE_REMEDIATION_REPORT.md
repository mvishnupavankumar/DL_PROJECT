# Phase 9 Targeted Figure Clipping Remediation

**Date:** 2026-10-16 (Asia/Kolkata)  
**Scope:** `FIG_B_FROZEN_LSTM.png`, `FIG_D_DIAGNOSIS_APPROVAL.png`, `FIG_E2_CONFUSION_MATRICES.png`, `FIG_E4_DIAGNOSIS_PILOT.png`, and `FIG_E6_LIVE_EVIDENCE.png` only.

## Result

The five named PNGs were regenerated from the controlled Phase 4 generator after a raster-only layout adjustment. No scientific data, labels, values, captions, limitations, evidence boundaries, or dimensions changed. The corrected assets passed full-resolution and 600-px manuscript-column-scale inspection, raw-input crosschecks where applicable, and post-promotion hash verification.

## Preflight and root cause

The Phase 8 audit, checklist, and blockers were read with the controlled Phase 4 register, remediation report, generator, validator, and historical manifest. The starting working tree was already dirty; `research/figures/phase4/` was an existing untracked controlled figure directory. No existing unrelated change was reset, cleaned, stashed, or altered.

The five starting files were all 1800 x 1125; their baseline byte sizes and SHA-256 values are preserved in `PHASE9_BEFORE_AFTER_HASHES.csv`. A target-only staging generation using the prior 70-px raster title/footer guard reproduced the starting PNGs byte-for-byte. Direct cropped inspection showed the starting pixels were not physically absent, but the narrow left guard could present as lost leading title/footer text in the Phase 8/column-scale viewing path. The corrective action therefore widened only the five targeted raster title/footer margins from 70 px to 120 px.

The generator has an earlier and a later set of figure function definitions. Target-only generation initially exposed that the active `detection` override lacked the new `emit` argument. It was made signature-compatible; default complete-set generation behavior remains unchanged. The generator now also supports scoped staging (`--output-dir`, `--targets`, `--formats`, `--no-manifest`) so a future repair does not regenerate unaffected controlled assets.

## Per-figure remediation

| Figure | Issue addressed | Correction | Validation result |
| --- | --- | --- | --- |
| B | Vulnerable narrow left title/footer guard. | Regenerated PNG with 120-px raster title/footer guard. | Full and reduced-size inspection passed; model-contract wording and threshold label retained. |
| D | Phase 8 reported title/footer clipping. | Same 120-px raster guard; workflow boxes and arrows untouched. | Full and reduced-size inspection passed; implementation/local-demo limitation retained. |
| E2 | Phase 8 reported title/footer clipping. | Same 120-px raster guard; confusion-matrix panel positions/counts untouched. | Raw reconstruction and visual checks passed. |
| E4 | Phase 8 reported title/footer clipping. | Same 120-px raster guard; bars, labels, and `UNASSESSABLE` annotations untouched. | Raw reconstruction and visual checks passed. |
| E6 | Phase 8 reported title/footer clipping. | Same 120-px raster guard; cards, stacked fault-mode field, and values untouched. | Raw reconstruction and visual checks passed. |

## Staging, backup, and promotion

The five assets were first generated in `research/exports/phase9/staging/`. Full-size visual inspection was performed on every staged PNG, then on 600 x 375 column-scale renderings in `research/exports/phase9/column_scale/`. Representative direct header/footer crops are retained in `research/exports/phase9/inspection_crops/` as inspection evidence. Each staged PNG was 1800 x 1125 with header non-white pixels beginning at x=123 and footer non-white pixels beginning at x=120.

The original controlled files were copied without modification to `research/exports/phase9/backups/pre-remediation/` before promotion. Promoted controlled PNG hashes exactly match their staged hashes. See `PHASE9_BEFORE_AFTER_HASHES.csv`.

## Validator and format checks

`validate_phase41_assets.py` was run before promotion but correctly stopped with `Manifest mismatch: generate_phase4_figures.py`, because the generator was updated for the scoped raster correction while the historical Phase 4 manifest intentionally remains frozen. It was therefore not used as an after-promotion pass signal.

An equivalent Phase 9 check, `verify_phase9_evidence.py`, passed after promotion. It verifies raw values for E2/E4/E6, staged PNG dimensions and title/footer pixel bounds, SVG XML parsing, and existing PDF embedded-page dimensions. The SVG and PDF counterparts remain unchanged by design: their semantic content remains aligned, while only the five PNG title/footer margins differ. No historical manifest was overwritten; `PHASE9_BEFORE_AFTER_HASHES.csv` is the separate remediation manifest.

## Changed paths

- `research/figures/phase4/generate_phase4_figures.py` — scoped staging support, active override compatibility, and target-only raster title/footer margin capability.
- `research/figures/phase4/FIG_B_FROZEN_LSTM.png`
- `research/figures/phase4/FIG_D_DIAGNOSIS_APPROVAL.png`
- `research/figures/phase4/FIG_E2_CONFUSION_MATRICES.png`
- `research/figures/phase4/FIG_E4_DIAGNOSIS_PILOT.png`
- `research/figures/phase4/FIG_E6_LIVE_EVIDENCE.png`
- `research/figures/phase4/FIGURE_REGISTER.md` — appended Phase 9 provenance note.
- `research/exports/phase9/` — reports, checks, staged PNGs, backup copies, column-scale previews, direct inspection crops, and read-only verification helper.

No path outside the authorized five figure assets, their generator/register, their Phase 9 backups, and `research/exports/phase9/` was modified by this phase.
