# AegisOps Figure Register

This register covers controlled Phase 4/9 assets. Figure titles, evidence boundaries, and source records were checked against `research/figures/phase4/FIGURE_CAPTIONS.md`, the Phase 4 register, the Phase 8 audit, and Phase 9 remediation records.

| ID | Exact controlled path | Intended section | What it establishes | What it does not establish |
| --- | --- | --- | --- | --- |
| A | `research/figures/phase4/FIG_A_ARCHITECTURE.png` | Methodology/architecture | Implemented components and observed bootstrap-rule path | Remote remediation, authenticated dual control, production authorization |
| B | `research/figures/phase4/FIG_B_FROZEN_LSTM.png` | Model contract | 24-by-5 frozen synthetic-model contract and threshold | Live inference, causal representation, live-model validation |
| C | `research/figures/phase4/FIG_C_TELEMETRY_FLOW.png` | Architecture/live boundary | Collection, persistence, rule fallback, optional inference path | Timestamp continuity or live scoring/performance |
| D | `research/figures/phase4/FIG_D_DIAGNOSIS_APPROVAL.png` | Diagnosis/recovery workflow | Implemented workflow and local-demo restriction | Execution in all B configurations, authenticated approval, production recovery |
| E1 | `research/figures/phase4/FIG_E1_DETECTION_COMPARISON.png` | A results | Synthetic confusion-derived rates | Operational alarms/hour or external performance |
| E2 | `research/figures/phase4/FIG_E2_CONFUSION_MATRICES.png` | A results | TP/FP/TN/FN counts for four methods | Independent live observations |
| E3 | `research/figures/phase4/FIG_E3_SCENARIO_RECALL.png` | Supplement | Descriptive recall for six synthetic scenarios | Confirmatory generalization |
| E4 | `research/figures/phase4/FIG_E4_DIAGNOSIS_PILOT.png` | B results | Strict ITT and completed-case pilot outcomes | LLM superiority, cost, token, or API-reliability claims |
| E5 | `research/figures/phase4/FIG_E5_SAFETY_HARNESS.png` | C results | Local-harness 11/11 attack containment and 16/16 audit completeness | Production-security certification |
| E6 | `research/figures/phase4/FIG_E6_LIVE_EVIDENCE.png` | Limitations | Bootstrap mode, null-score, and stored fault-mode facts | Independent labels or live detection metrics |
| F | `research/figures/phase4/FIG_F_EXPERIMENT_D_READINESS.png` | Limitations/supplement | AnoMod provenance and evaluation blockers | External performance result |

Detailed captions and controlling sources are in `research/figures/phase4/FIGURE_CAPTIONS.md`. Phase 9 changed only PNG title/footer margins for B, D, E2, E4, and E6; see `research/exports/phase9/PHASE9_FIGURE_REMEDIATION_REPORT.md`.
