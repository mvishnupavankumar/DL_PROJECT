# Phase 17 Bounded Claims Manuscript Quality Control Report

**Date:** 2026-10-17 (Asia/Kolkata)
**Scope:** Source-level, non-destructive Path 3 quality control plus the prescribed isolated Experiment D harness regression. This report is not a rendered-document inspection and does not certify publication or camera-ready release.

## Baseline and controls

| Item | Recorded state before Phase 17 edits |
| --- | --- |
| Branch | `publish/research-without-external-dataset` |
| HEAD | `a32713c30a8ddca1425d44b1afbaf6d55a64c276` |
| Working tree | Dirty; preserved without reset, clean, stash, commit, or overwrite of unrelated work. |
| Experiment D | Production evaluation remained blocked and unexecuted. |
| Live pilot | Gate 1 remained closed; no target or collector action occurred. |

## QC framework clarification

`MANUSCRIPT_FINALIZATION_PLAN.md` presents seven release criteria labelled QC-1 through QC-7, while `FINAL_EVIDENCE_AUDIT.md` presents an eight-item supervisory audit labelled QC-1 through QC-8. This report uses the current eight-item supervisory-audit labels below and cross-checks the plan's seven acceptance criteria within the relevant rows. The numbering difference is a documentation ambiguity that must be reconciled before a final release checklist can be treated as a single unambiguous control.

## QC-1 through QC-8 results

| QC | Status | Evidence and Phase 17 result |
| --- | --- | --- |
| QC-1 Detection metric reconciliation | **PASS — source-level** | Manuscript Table 1 matches the canonical counts: Full Rules 120/0/200/0, Isolation Forest 57/4/196/63, frozen LSTM 120/2/198/0, Combined OR 120/2/198/0 (TP/FP/TN/FN). The source confines these results to 320 constructed windows and excludes operational alarms-per-hour. |
| QC-2 Windowing and statistical independence | **PASS — source-level** | The manuscript identifies 24-step synthetic windows, six scenario clusters, window-level McNemar as descriptive, and the six-scenario Wilcoxon result as exploratory (`W=0`, `p=0.03125`). |
| QC-3 Frozen model contract | **PASS — source-level and focused regression** | Feature order, Z-score contract, 3,733 parameters, threshold `0.709399`, and the frozen checkpoint are consistent with the controlling audit. The isolated harness test verified feature order and checkpoint/eval-mode behavior without running production evaluation. |
| QC-4 Diagnosis consistency | **PASS — source-level** | The manuscript retains seven configurations times six cases, strict ITT/completed-case separation, both `UNASSESSABLE` omissions (C5/INC-1002 and C7/INC-1004), and the bounded C6 result (5/6 strict, 6/6 lenient). No LLM-superiority claim appears. |
| QC-5 Safety and governance boundary | **PASS — source-level** | It retains separate 11/11 attack-containment and 16/16 audit-completeness denominators/Wilson intervals, confines evidence to the local loopback boundary, and does not claim authenticated dual authorization or production security certification. |
| QC-6 Abstract, conclusions, and contribution bounds | **PASS — source-level** | Abstract and conclusion label Experiment A synthetic, Experiment B exploratory, Experiment C local, live-LSTM performance unavailable, and Experiment D external performance unavailable. The combined detector is not credited with added sensitivity. |
| QC-7 References, figures/tables, algorithms, and technical definitions | **BLOCKED FOR RELEASE** | Source checks found the fixed five-feature definition, figures/tables, figure captions, and reference register aligned with bounded claims. However, Phase 11/12 retain final AnoMod publisher-page confirmation as a release prerequisite, and no rendered PDF/DOCX page-level review has validated reference wrapping, figures, equations, tables, or Mermaid rendering. |
| QC-8 Reproducibility and regression verification | **PARTIALLY VERIFIED; BLOCKED FOR FINAL SIGN-OFF** | The prescribed test passed 40/40 in 16.01s with a workspace-local pytest base directory. A first standard invocation reached 36 passes but four `tmp_path` setup errors because the global pytest temp directory was inaccessible; this was environmental, not a harness assertion failure. The reported historical/current full-suite 107/107 evidence was reviewed but not re-run in Phase 17, so the full-regression portion of final sign-off was not newly exercised. |

## Bounded-claims and source consistency findings

- The manuscript correctly distinguishes synthetic Experiment A results from operational rates; `UNAVAILABLE` remains the only defensible status for operational false alarms per hour.
- Experiment B retains strict ITT and completed-case denominators, the two API omissions, and its low-power/rubric-overlap caveats. Its 83.33% strict versus 100% lenient C6 result is not generalized.
- Experiment C retains separate 11/11 and 16/16 denominators and Wilson intervals rather than collapsing them.
- The live record remains 200 `bootstrap_rules` rows with 200 null scores and zero live-LSTM-scored rows. Live performance remains **UNMEASURED**.
- Experiment D remains archive/provenance/readiness only. The production harness was not invoked; the test suite exercised fail-closed guards and temporary fixtures only.
- The manuscript does not claim external AnoMod performance, real-world detector performance, live accuracy, operational FPR, or production-security certification.

## Commands and results

| Command | Exit code | Result |
| --- | ---: | --- |
| `git branch --show-current`; `git rev-parse HEAD`; `git status --short --untracked-files=all` | 0 | Baseline captured before editing. |
| Required-artifact/path, source, figure/table, reference, and claim-boundary inspections | 0 | Required records resolved; no missing named input artifact. |
| `./.venv/Scripts/python.exe -m pytest test_experiment_d_harness.py -v` | 1 | 36 passed; 4 setup errors caused by denied access to `C:\Users\chara\AppData\Local\Temp\pytest-of-chara`. No production harness command ran. |
| `./.venv/Scripts/python.exe -m pytest test_experiment_d_harness.py -v --basetemp .pytest_tmp_phase17` | 0 | **40 passed in 16.01s**. Temporary directory was removed after the run. |
| Tool availability recheck for `pandoc`, `quarto`, `soffice`, `libreoffice`, `pdfinfo`, `pdftoppm` | 0 | All absent; no renderer was installed or substituted. |

## Release verdict and remaining blockers

**Supervisor-review source verdict: B — source evidence is bounded and internally consistent for substantive review.**

**Publication/camera-ready release verdict: BLOCKED.** The blockers are: (1) no reproducible DOCX/PDF generation and page-by-page visual inspection; (2) visible metadata placeholders still require owner confirmation; (3) release-specific provenance for the dirty worktree remains unresolved; (4) final AnoMod publisher-page confirmation remains a stated prerequisite or must remain explicitly limited; (5) the QC-1–QC-7 versus QC-1–QC-8 naming ambiguity must be reconciled; and (6) a full current-suite regression run was not repeated in this phase.

No manuscript claim was strengthened or rewritten in Phase 17. No live collection, target access, production evaluation, unauthorized configuration change, database mutation, model change, or unsupported performance claim occurred.
