# AegisOps Phase 2 Statistical Verification

**Inputs:** The hashes of all inputs listed in `PHASE2_METRIC_RECONCILIATION.md` match the Phase 1 freeze. This document recalculates from current raw records only; it does not rerun an experiment.

## Experiment A calculations

For each detector, `TP`, `FP`, `TN`, and `FN` were counted from `ground_truth` and the detector's recorded binary flag over 320 rows. Precision is `TP/(TP+FP)`, recall is `TP/(TP+FN)`, F1 is `2PR/(P+R)`, specificity is `TN/(TN+FP)`, and FPR is `FP/(FP+TN)`.

| Detector | TP, FP, TN, FN | Precision | Recall | F1 | Specificity | FPR |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Rules | 120, 0, 200, 0 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.000000 |
| Isolation Forest | 57, 4, 196, 63 | 0.934426 | 0.475000 | 0.629834 | 0.980000 | 0.020000 |
| Frozen LSTM | 120, 2, 198, 0 | 0.983607 | 1.000000 | 0.991736 | 0.990000 | 0.010000 |
| Combined | 120, 2, 198, 0 | 0.983607 | 1.000000 | 0.991736 | 0.990000 | 0.010000 |

For the two continuous scores, thresholds were processed in descending order, with an initial PR point `(recall=0, precision=1)`. Trapezoidal PR-AUC integrates adjacent points; average precision uses a step-weighted sum of the recall increases.

| Score | Trapezoidal PR-AUC | Average precision | Interpretation |
| --- | ---: | ---: | --- |
| `iso_score` | 0.9055643731 | 0.9060267404 | Reproducible from current score rows. |
| `lstm_score` | 1.0000000000 | 1.0000000000 | Reproducible from current score rows. |
| `rule_score`, combined flag | N/A | N/A | Binary/non-ranking outputs; not comparable continuous scores. |

For the 120 fault windows, LSTM-only versus Isolation-Forest-only detections are `b=63`, `c=0`. The exact two-sided paired-binomial/McNemar probability is `2 × 0.5^(63) = 2.168404344971009e-19`. This is mathematically reproducible for these rows, but the 120 windows are clustered into six repeated synthetic scenarios and must not be interpreted as independent production incidents.

At the scenario level, the six LSTM recalls are all 1.0 and the six Isolation-Forest recalls are `[0.40, 0.25, 0.85, 0.75, 0.40, 0.20]`. Every nonzero difference is positive; the reported signed-rank result `W-=0` and exact two-sided sign-pattern probability `2 × 0.5^6 = 0.03125` are reproducible. The result is exploratory: six clusters give the smallest attainable two-sided p-value of 0.03125 and insufficient basis for external generalization.

## Experiment B calculations

All seven configurations have six intended scenario rows. Strict intent-to-treat accuracy includes `UNASSESSABLE` rows as zero-score outcomes; completed-case accuracy excludes them. Mean latency uses all completed rows, including an observed zero-duration deterministic row, and excludes omitted API calls.

| Configuration | Strict ITT | Strict completed | Lenient ITT | Lenient completed | Completed-call mean latency (ms) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Rule-based Baseline | 6/6 | 6/6 | 6/6 | 6/6 | 0.008333 |
| Single-Agent Offline | 3/6 | 3/6 | 3/6 | 3/6 | 0.031667 |
| Multi-Agent Full Offline | 3/6 | 3/6 | 3/6 | 3/6 | 0.568333 |
| Multi-Agent No-DL Offline | 6/6 | 6/6 | 6/6 | 6/6 | 0.113333 |
| Single-Agent Groq LLM | 4/6 | 4/5 | 4/6 | 4/5 | 3041.870000 |
| Multi-Agent Full Groq LLM | 5/6 | 5/6 | 6/6 | 6/6 | 23188.720000 |
| Multi-Agent No-DL Groq LLM | 4/6 | 4/5 | 5/6 | 5/5 | 19279.690000 |

No raw field supplies API costs, prompt tokens, completion tokens, or total token use. These measures are not reproducible.

## Experiment C calculations

There are 16 current records: 11 attacks, two precondition checks, two positive controls, and one verification probe. The 11 attack latencies average `124.54 / 11 = 11.3218181818 ms`. Wilson intervals use z=1.959963984540054.

| Measure | Numerator/denominator | Result | 95% Wilson CI |
| --- | --- | ---: | --- |
| Attack containment | 11/11 | 1.000000 | [0.741167, 1.000000] |
| Audit-trail completeness | 16/16 | 1.000000 | [0.806392, 1.000000] |

These calculations describe the tested local harness and categories, not a production-security population.

## Live and Experiment D checks

The 200 telemetry rows have `bootstrap_rules=200`, blank `anomaly_score=200`, and 26 gaps above 60 seconds. This excludes a valid calculation of LSTM live detection performance. Frozen metadata records a 24-step input requirement and threshold 0.7093990445137024. All five expected Experiment D production artifacts are absent; there is no external performance statistic to test.
