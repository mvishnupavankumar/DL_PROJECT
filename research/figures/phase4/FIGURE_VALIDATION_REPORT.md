# AegisOps Phase 4 Figure Validation Report

**Audit date:** 2026-10-15 (Asia/Kolkata)  
**Scope:** Phase 4.1 remediated figure assets only. No source data, code, model artifact, database, experiment output, historical report, or manuscript was changed.

## Verdict

**B — Figures are usable, with an explicit SVG-rendering verification limitation.**

All required controlling documents were present; the plotted values were recomputed from the current Phase 2 raw-evidence inputs and agree with the controlling reconciliation. Every final PNG and PDF-page image was reviewed at full size and at a 640px manuscript-column proxy after the Phase 4.1 layout remediation. The evidence boundaries remain unchanged.

## Preflight and source traceability

All nine required preflight files existed and were read before figure creation:

- `research/exports/PHASE1_EVIDENCE_FREEZE_AUDIT.md`
- `research/exports/PHASE2_METRIC_RECONCILIATION.md`
- `research/exports/PHASE2_METRIC_SOURCE_MAP.csv`
- `research/exports/PHASE2_STATISTICAL_VERIFICATION.md`
- `research/exports/PHASE3_IMPLEMENTATION_ARCHITECTURE_AUDIT.md`
- `research/exports/PHASE3_COMPONENT_SOURCE_TRACEABILITY.csv`
- `research/exports/PHASE3_DIAGRAM_SPECIFICATION.md`
- `research/exports/PHASE3_UNSUPPORTED_ARCHITECTURE_CLAIMS.md`
- `research/paper/CANONICAL_METRIC_RECONCILIATION.md`

`generate_phase4_figures.py` reads the four current raw/export CSVs and frozen model metadata directly and aborts if their reconciled row counts are not 320 / 42 / 16 / 200. It does not execute the application, call a model, contact a service, or write outside this directory.

## Numerical checks

| Evidence area | Direct check | Result |
| --- | --- | --- |
| A detection | Raw prediction rows | 320 (200 nominal, 120 fault) — matched |
| A Rules | TP / FP / TN / FN | 120 / 0 / 200 / 0 — matched |
| A Isolation Forest | TP / FP / TN / FN | 57 / 4 / 196 / 63 — matched |
| A LSTM | TP / FP / TN / FN | 120 / 2 / 198 / 0 — matched |
| A Combined | TP / FP / TN / FN | 120 / 2 / 198 / 0 — matched |
| A scenario plot | Fault scenarios and windows | six scenarios, 20 fault windows each — matched |
| B diagnosis | Current raw rows | 42 = 7 configurations × 6 cases — matched |
| B diagnosis | Strict ITT / completed-case denominators | ITT 6 per configuration; C5 and C7 each have one `UNASSESSABLE` omission — matched |
| C safety | Case count and denominators | 16 total, 11 attack cases; containment 11/11; audit trail 16/16 — matched |
| C safety | Wilson intervals | 11/11: [0.741, 1.000]; 16/16: [0.806, 1.000] — reproduced |
| Live export | Stored rows / detector mode / null scores | 200 / 200 `bootstrap_rules` / 200 null — matched |
| Frozen LSTM | Contract | sequence length 24, features 5, hidden size 16, strict threshold 0.7093990445137024 — matched |
| Experiment D | Production result inputs | absent; readiness panel only — matched Phase 1–3 state |

## Render and visual checks

- Regenerated 11 figure IDs (A, B, C, D, E1-E6, F), each with SVG, PDF, and 1800×1125 PNG output at 300 DPI.
- Parsed all 11 SVG files successfully using an XML parser; each rendered PNG is 1800×1125 at approximately 300 DPI. A graphical SVG rasterizer was unavailable, so SVG visual rendering remains a recorded limitation.
- Inspected all 11 full-size PNGs and all 11 corresponding 640×400 manuscript-column proxies.
- Inspected all 11 PDF page payloads. Each is a single-page Pillow PDF containing one DCT raster image at 1800×1125, matching the generated visual layout rather than a separate vector/page layout.
- Checked for clipped text, overflow, collision, and cross-format semantic differences after the remediation.
- `PHASE4_SHA256_MANIFEST.json` records SHA-256 and byte count for every new source and rendering; all listed hashes are independently verified after generation.

## Deliberate exclusions and unresolved limitations

- No live LSTM accuracy, ROC, PR curve, specificity, false-positive rate, or alarms-per-hour figure: all 200 audited live scores are null and detector mode is bootstrap rules.
- No AnoMod performance chart or matrix: production predictions, metrics, ratification record, and contract-valid evaluation remain absent/blocked.
- No claims of remote remediation, production authorization, authenticated dual control, causal model representations, cost-effectiveness, API reliability, or universal workflow execution.
- Experiment A figures are restricted to synthetic windows and mark possible within-window dependence.
- Experiment B shows `UNASSESSABLE` omissions rather than silently excluding them from intent-to-treat values.
- Experiment C is labelled as a bounded local safety harness.
- The historical integrity manifest remains stale for the mismatches documented in Phase 1; this Phase 4 work does not repair or replace it.

## Figures not generated

No required figure was omitted. An Experiment D **performance** figure was deliberately not generated because no valid production outcome evidence exists; Figure F is explicitly a non-performance readiness panel.
