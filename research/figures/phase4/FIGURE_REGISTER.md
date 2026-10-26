# AegisOps Phase 4 Figure Register

**Status:** Evidence-bounded figure assets only. These assets have not been inserted into the manuscript.

**Phase 4.1 layout revision (2026-10-15):** Filenames, figure IDs, sources, denominators, interpretations, and evidence boundaries are unchanged. The rendering layouts were redesigned for non-clipped titles, readable column-scale labels, and non-overlapping workflow and taxonomy elements. See `FIGURE_VISUAL_REMEDIATION_REPORT.md`.

**Phase 9 targeted PNG remediation (2026-10-16):** The PNG renderings for B, D, E2, E4, and E6 were regenerated from the controlled generator with widened 120-px raster title/footer margins. Their data, labels, sources, limitations, IDs, filenames, and dimensions are unchanged. The accompanying SVG and PDF files remain the Phase 4.1 renderings; this targeted PNG-only correction did not retroactively rewrite the historical Phase 4 manifest. See `research/exports/phase9/PHASE9_FIGURE_REMEDIATION_REPORT.md` and `PHASE9_BEFORE_AFTER_HASHES.csv`.

| ID | Purpose and proposed placement | Primary evidence and denominator | Interpretation permitted | Deliberate limitation | Formats |
| --- | --- | --- | --- | --- | --- |
| A | System architecture / Methods | Phase 3 architecture audit and diagram specification | Implemented monitoring, persistence, workflow, fallback, and local-demo boundaries | Not a deployment or authorization diagram | SVG, PDF, PNG, Mermaid source |
| B | Frozen model contract / Methods | `models/lstm_autoencoder.json`; Phase 3 audit | Synthetic-benchmark architecture and strict threshold contract | No live checkpoint or causal-representation claim | SVG, PDF, PNG, Mermaid source |
| C | Telemetry-to-alert flow / Operations | `research/exports/telemetry.csv` (200 rows); Phase 3 audit | Audited bootstrap-rule path and persistence flow | Intended five-second cadence; no timestamp-continuity validation or live scoring claim | SVG, PDF, PNG, Mermaid source |
| D | Diagnosis and approval workflow / Methods | Phase 3 audit; Phase 2 B reconciliation | Component and local-demo workflow boundaries | Not evidence that every component ran in every B configuration or live session | SVG, PDF, PNG, Mermaid source |
| E1 | Experiment A detection comparison / Results | `research/raw/detection_predictions.csv` (320 synthetic windows) | Confusion-derived precision, recall, F1, and FPR | Windows may be dependent; no alarms/hour estimate | SVG, PDF, PNG |
| E2 | Experiment A confusion matrices / Results | `research/raw/detection_predictions.csv` (200 nominal, 120 fault) | TP/FP/TN/FN counts for four methods | Synthetic benchmark only | SVG, PDF, PNG |
| E3 | Experiment A scenario recall / Results | `research/raw/detection_predictions.csv` (six scenarios × 20 fault windows) | Descriptive scenario recall | Six clusters makes scenario analysis exploratory | SVG, PDF, PNG |
| E4 | Experiment B diagnosis pilot / Results | `research/raw/diagnosis_predictions.csv` (7 configurations × 6 cases) | Strict ITT and strict completed-case proportions; visible omissions | No superiority, cost, token, or reliability claim | SVG, PDF, PNG |
| E5 | Experiment C safety harness / Results | `research/raw/safety_test_results.csv` (16 local-harness cases) | Attack containment 11/11 and audit completeness 16/16 with Wilson intervals | Local harness, not production-security certification | SVG, PDF, PNG |
| E6 | Live telemetry evidence summary / Operations | `research/exports/telemetry.csv` (200 stored records) | Detector mode, null-score status, and stored fault-mode field | Not independent labels; no live discrimination metric | SVG, PDF, PNG |
| F | Experiment D readiness panel / Limitations | Phase 1, Phase 2, and Phase 3 controlling audits | Archive/provenance availability and blockers | Explicitly not a performance result | SVG, PDF, PNG |

## Visual convention

- Blue: implemented code path or evaluated synthetic/local evidence.
- Green: observed in the audited session or confirmed present.
- Orange: human/workflow or local-demo restriction.
- Purple: optional external/API execution boundary.
- Gray: optional, unavailable, absent, or blocked component.
- Red: material boundary or unresolved blocker.

The editable Mermaid sources are `FIG_A_ARCHITECTURE.mmd`, `FIG_B_FROZEN_LSTM.mmd`, `FIG_C_TELEMETRY_FLOW.mmd`, and `FIG_D_DIAGNOSIS_APPROVAL.mmd`. The rendered diagrams preserve the audited labels and restrictions rather than presenting the Mermaid files as authoritative evidence.
