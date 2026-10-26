# AegisOps Phase 6 — Results and Statistics Crosscheck

**Scope:** a non-recalculation crosscheck against the Phase 2 canonical reconciliation and its stated controlling raw inputs. No experiment was rerun and no metric was recomputed.

## Controlling results record

| Experiment / record | Controlling source | Crosschecked state for later manuscript correction |
|---|---|---|
| A: synthetic detection | `research/raw/detection_predictions.csv`, `detection_metrics.csv`, `detection_by_scenario.csv`; Phase 2 reconciliation | 320 synthetic windows: 200 nominal, 120 fault; six scenarios with 20 fault windows each. |
| B: diagnosis pilot | `research/raw/diagnosis_predictions.csv`, `diagnosis_metrics.csv`; Phase 2 reconciliation | 42 records: seven configurations x six cases. Preserve two rate-limit `UNASSESSABLE` omissions in strict ITT. |
| C: safety boundary | `research/raw/safety_test_results.csv`, `safety_metrics.csv`; Phase 2 reconciliation | 16 local-harness evaluations: 11 attack cases contained and all 16 audit trails complete. |
| Live telemetry | `data/aegisops_live.sqlite3` and audited exports | 200 records, all `bootstrap_rules`; all anomaly scores null. Demonstration/logging evidence only. |
| D: AnoMod | archive/provenance and blocking audits | No valid production predictions, metrics, manifest, ratification, or performance result. |

## A. Synthetic detection — allowed result statements

| Method in current raw evidence | TP | FP | TN | FN | Recall | Precision | F1 | Boundary |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Full operational rules | 120 | 0 | 200 | 0 | 1.0000 | 1.0000 | 1.0000 | Synthetic, structurally related to the simulated error-rate predicate. |
| Isolation Forest | 57 | 4 | 196 | 63 | 0.4750 | 0.9344 | 0.6298 | Flattened 24 x 5-window benchmark baseline. |
| Frozen LSTM autoencoder | 120 | 2 | 198 | 0 | 1.0000 | 0.9836 | 0.9917 | Frozen synthetic-window benchmark only. |
| Combined OR alert | 120 | 2 | 198 | 0 | 1.0000 | 0.9836 | 0.9917 | Same recorded counts as the LSTM on this cohort. |

Permitted short result: “On the defined 320-window synthetic benchmark, the frozen LSTM detected 120/120 fault windows and produced 2/200 nominal false positives.” It must not become a live accuracy, an alert-per-hour claim, a production reliability claim, or a generalization claim.

### Required statistical wording

The manuscript should explicitly declare, before reporting p-values:

- **Window-level comparison:** H0: the paired LSTM and Isolation Forest outcomes have equal probability of discordant detection in this synthetic cohort; H1: those probabilities differ. The exact McNemar result (`b=63`, `c=0`, two-sided `p=2.168 × 10^-19`) is descriptive because windows are clustered within six constructed scenarios.
- **Scenario-level comparison:** H0: the median paired scenario-level recall difference is zero; H1: it is non-zero. The Wilcoxon signed-rank result (`W=0.0`, `p=0.03125`, six scenarios) is post-hoc exploratory and not confirmatory evidence of operational superiority.
- **Intervals:** Wilson intervals describe the finite synthetic/local samples. They do not establish population, continuous-operation, or deployment confidence.

Do not include a false-alarm-per-hour number. The evidence supports only the batch-window FPRs shown above; operational alarms/hour is unavailable.

### Table 1 correction rule

Narrow Rules (33.33%) and Resource-Only Rules (66.67%) are historical comparator outputs pending independent reconstruction. They must not appear as equal-status rows in the primary current-results table or abstract. If retained for provenance, put them in a labeled historical appendix separated from current raw results.

## B. Diagnosis pilot — denominator and claim controls

| Item | Crosschecked record | Required presentation |
|---|---|---|
| Scope | 42 records, 7 configurations x 6 cases | Show both configuration and six-case denominator; do not aggregate as independent replications. |
| Omissions | C5 / `INC-1002` and C7 / `INC-1004` rate-limit omissions | Keep `UNASSESSABLE` in strict ITT, with zero recorded latency; do not silently remove them. |
| Full LLM + DL configuration | 5/6 strict ITT (83.33%); 6/6 lenient; raw provider payloads absent | Call it a pilot configuration result, not LLM benefit or causal validation. |
| Deterministic heuristic | 6/6 strict in 0.01 ms | Include it when making any comparative statement; it precludes an LLM-superiority claim on this suite. |
| Pilot limitations | Six cases, rubric/keyword overlap, low stated power | Keep the limitation next to results, not only in discussion. |

The manuscript may report B’s values as configuration-specific observations. It may not claim that deep-learning context, LLM agents, or agent orchestration caused improved root-cause accuracy; that all agents executed in every run; or that results transfer to live incidents.

## C. Approval/safety harness — permitted result statements

| Quantity | Current evidence | Required boundary |
|---|---:|---|
| Specified attack cases contained | 11 / 11 | Local application/runtime harness only. |
| Audit trails complete | 16 / 16 | Local SQLite audit behavior, not regulated/nonrepudiable logging. |
| Wilson interval, attacks | [0.7412, 1.0000] | Interval for finite local harness cases only. |
| Wilson interval, audit trails | [0.8064, 1.0000] | Interval for finite local harness cases only. |

“100% threat mitigation,” authenticated two-person approval, NIST compliance, replay protection, production security, or autonomous safe recovery are not supported. The approver is a label, not a verified identity; the recovery action is a bounded local demonstration.

## Live telemetry and external validation exclusions

| Topic | Exact state | Mandatory manuscript treatment |
|---|---|---|
| Live collection | 200 rows; bootstrap-rule mode on all 200; anomaly score null on all 200 | State only collection, logging, fallback-rule, and alert-transition demonstration. |
| Live LSTM | No live checkpoint/metadata and no non-null score record | State absent; do not infer accuracy, scoring, FPR, or generalization. |
| AnoMod / D | Archive/provenance exists; production result artifacts absent; protocol blocked | State that no external performance result is reported. Do not plot or tabulate D performance. |

## Crosscheck result

All listed values can be carried forward only with the boundaries above. The supervisor-review revision needs a text-only reconciliation pass after edits to ensure that its abstract, tables, captions, discussion, and conclusion apply identical denominators and exclusions.
