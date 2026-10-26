# Phase 9 Evidence-Preservation Check

## Scope and method

Phase 9 changed only the raster title/footer margin for the five designated PNGs. The controlled generator continued to read the existing evidence inputs; no dataset, metric, model, database, manuscript, experiment output, or statistical result was edited. `verify_phase9_evidence.py` was executed after staging and promotion and completed with `result: pass`.

## Raw-input checks

| Figure(s) | Controlling input | Check | Result |
| --- | --- | --- | --- |
| E2 | `research/raw/detection_predictions.csv` | 320 rows; confusion matrices reconstructed as Rules 120/0/200/0, Isolation Forest 57/4/196/63, LSTM 120/2/198/0, Combined 120/2/198/0 (TP/FP/TN/FN). | Pass |
| E4 | `research/raw/diagnosis_predictions.csv` | 42 rows; seven configurations with six strict-ITT cases each; strict successes `6,3,3,6,4,5,4`; the fifth and seventh configurations retain one `UNASSESSABLE` omission and use completed-case denominator 5. | Pass |
| E6 | `research/exports/telemetry.csv` | 200 rows; all `bootstrap_rules`; all 200 LSTM scores null; fault-mode counts error 168, latency 1, normal 31. | Pass |
| B, D | Existing Phase 3-audited labels and limitations in the controlled generator | The correction changed only raster header/footer x-coordinate and guide-rule endpoints. | Pass |

## Evidence boundaries retained

- Figure B remains a frozen synthetic-benchmark model contract, not live-inference performance or a causal-representation result.
- Figure D remains an implementation/local-demo workflow diagram and does not establish authenticated dual control, production authorization, or execution of every component in every configuration or live session.
- Figure E2 remains a synthetic 320-window confusion-count display, not independent live evidence.
- Figure E4 retains strict intent-to-treat denominators and the two visible `UNASSESSABLE` API omissions; it makes no superiority, cost, token, or rate-limit-remediation claim.
- Figure E6 retains the no-live-performance boundary: 200 bootstrap-only rows, 200 null LSTM scores, and no ROC, PR, accuracy, specificity, FPR, or alarms-per-hour claim.

## Structural checks

Each staged and promoted PNG is 1800 x 1125. XML parsing passed for the five existing SVGs; the existing PDF embedded pages are each 1800 x 1125. SVG and PDF assets were intentionally not changed because this remediation is limited to the five named PNG assets. Their meaning remains aligned with the corrected PNGs; the only intentional cross-format layout difference is the PNG title/footer margin.

The historic Phase 4 manifest was not rewritten. Its generator entry and the five old PNG hashes no longer represent the controlled current state; `PHASE9_BEFORE_AFTER_HASHES.csv` is the authoritative Phase 9 hash record for these assets.
