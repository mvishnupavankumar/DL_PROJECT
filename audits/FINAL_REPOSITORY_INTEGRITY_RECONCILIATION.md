# AegisOps: Final Evidence and Repository Integrity Reconciliation Report

**Document Identifier**: `AEGISOPS-FINAL-REPOSITORY-INTEGRITY-RECONCILIATION`  
**Date**: October 14, 2026  
**Auditor**: Senior ML Research Supervisor, Statistical Auditor & Reproducibility Reviewer  
**Repository Working Tree**: `C:/DL_PROJECT`  
**Current Git Branch**: `publish/research-without-external-dataset`  
**Current Git HEAD**: `a32713c30a8ddca1425d44b1afbaf6d55a64c276`  
**Historical Audited Baseline Commit**: `ec83d2fe501ba50f56839944ba7bd6347544f585` (on `main`)  
**Active Python Runtime**: `C:\DL_PROJECT\.venv\Scripts\python.exe` (Python 3.11.9, PyTorch 2.14.1+cpu)  
**Standard**: Strict Research Integrity, Read-Only Audit & Non-Destructive Reconciliation Policy  
**Final Verdict**: `READY FOR HUMAN COMMIT REVIEW`

---

## 1. Executive Summary

This report delivers the final evidence and repository integrity closure for the AegisOps research project. In strict accordance with audit instructions:
1. No frozen model weights, hyperparameters, detection thresholds, raw detection predictions, or experimental protocols were altered.
2. Production Experiment D was not executed, live LLM APIs were not called, `run_all.py` was not executed, and no test suite was rerun solely for documentation edits.
3. No Git commits, pushes, merges, rebases, file stashes, or branch switches were performed.
4. All 22 artifacts covered by `research/MANIFEST_SHA256.json` were audited in read-only mode, establishing that 17 artifacts match bit-for-bit while the 5 differing artifacts trace to audited classifications and recomputed metrics rather than data corruption.
5. Inaccuracies regarding raw data preservation were corrected: historical observations (`detection_predictions.csv`) are bit-for-bit preserved, while diagnosis and safety CSVs represent audited classifications and recomputed metrics.
6. Terminology across the manuscript, figure index, master handoff, and checklists was harmonized to use "fault-window recall", window-level binomial Wilson intervals with clustering caveats, and exploratory scenario-level paired analysis ($N=6$) for the Wilcoxon signed-rank test.
7. Calibration independence was strictly scoped to supported experiments (Experiment A verified; Experiment D unexecuted with a documented circular calibration leakage defect).
8. Fictitious implementation paths (`src/aegisops/...`) were replaced with verified repository paths (`dl/anomaly_detector.py` and `approval.py`), and machine-specific `file:///c:/...` links were replaced with clean relative repository links.

---

## 2. Git Identity & Working-Tree / Index Status

The Git environment was inspected directly via read-only shell commands:

```bash
git rev-parse --show-toplevel
# Output: C:/DL_PROJECT

git branch --show-current
# Output: publish/research-without-external-dataset

git rev-parse HEAD
# Output: a32713c30a8ddca1425d44b1afbaf6d55a64c276

git diff --check
# Output: Exit code 0 (zero trailing-whitespace or formatting defects)
```

### 2.1 Staged Files (Index State)
**Staged file count**: `0`  
No files have been staged in the index (`git status --short` confirms all changes remain in the unstaged working tree).

### 2.2 Unstaged Tracked Modifications (Working Tree State)
**Tracked modified file count**: `31` files  
Every modified file corresponds to verified audit documentation, metric reconciliation, figure index relative link updates, or CSV reclassifications:
1. `.gitignore` (safeguarding ignored local cache and external datasets)
2. `README.md` (updated project documentation links)
3. `research/SAFETY_EVALUATION.md` (reconciled safety taxonomy and 11-attack cohort)
4. `research/audits/AEGISOPS_MASTER_RESEARCH_HANDOFF.md` (distinguished baseline vs audit dates; verified real implementation paths)
5. `research/audits/UPDATED_SEVEN_PHASE_CHECKLIST.md` (scoped calibration independence; fixed detector path to `dl/anomaly_detector.py`)
6. `research/experiments/generate_diagnosis_audit.py` (reconciliation evaluator)
7. `research/experiments/run_experiment_c.py` (safety runner)
8. `research/experiments/run_safety_audit.py` (safety audit script)
9. `research/paper/AEGISOPS_RESEARCH_PAPER.md` (manuscript: fault-window recall, binomial Wilson CI caveat, exploratory Wilcoxon, simulator onset vs peak rates)
10. `research/paper/FIGURE_AND_TABLE_INDEX.md` (relative links; corrected statistical and window terminology)
11. `research/paper/FIGURE_AND_TABLE_REGISTER.md` (figure and table registry)
12. `research/paper/FINAL_EVIDENCE_AUDIT.md` (evidence audit matrix)
13. `research/paper/FINAL_MANUSCRIPT_CHECKLIST.md` (submission QC checklist)
14. `research/paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md` (traceability matrix)
15. `research/paper/MANUSCRIPT_FINALIZATION_PLAN.md` (Path 3 bounded claims governance plan)
16. `research/paper/REFERENCES_VERIFICATION.md` (verified citations)
17. `research/paper/REFERENCE_VERIFICATION.md` (reference audit log)
18. `research/paper/figures/approval_recovery_workflow.mmd` (Mermaid workflow)
19. `research/paper/figures/architecture_dataflow.mmd` (Mermaid architecture)
20. `research/raw/diagnosis_metrics.csv` (audited completed-case accuracy and latencies)
21. `research/raw/diagnosis_predictions.csv` (reclassified omitted API calls to UNASSESSABLE)
22. `research/raw/safety_metrics.csv` (recomputed attack containment and check latency)
23. `research/raw/safety_test_results.csv` (isolated 11 attacks, 2 preconditions, 1 probe, 2 controls)
24. `research/results/diagnosis_metrics.csv` (synchronized with `research/raw/`)
25. `research/results/diagnosis_predictions.csv` (synchronized with `research/raw/`)
26. `research/results/generate_statistical_analysis.py` (statistical script)
27. `research/results/safety_metrics.csv` (synchronized with `research/raw/`)
28. `research/results/safety_test_results.csv` (synchronized with `research/raw/`)
29. `research/results/statistical_analysis.md` (reconciled statistical analysis outputs)
30. `research/run_all.py` (reproducibility runner updated for Path 3 bounded claims)
31. `test_research_instrumentation.py` (research test suite)

### 2.3 Untracked Files
**Untracked file count**: `3` files
- `research/README.md` (directory overview)
- `research/audits/README.md` (audits index overview)
- `research/paper/CANONICAL_METRIC_RECONCILIATION.md` (authoritative canonical metric reconciliation matrix)

---

## 3. Manifest Hash Verification (Section A)

The SHA-256 manifest `research/MANIFEST_SHA256.json` (generated 2026-10-12T08:44:36Z, prior to the Phase 4/5 diagnostic rubric reconciliation and safety taxonomy disaggregation) covers exactly **22 artifacts**. Each artifact was inspected and rehashed in read-only mode using Python's `hashlib.sha256()`. The manifest was strictly preserved without modification or regeneration.

### 3.1 Verification Census Table

| # | Artifact Path | Expected SHA-256 (Manifest) | Observed SHA-256 (Disk) | Status | Analysis / Explanation |
| :-: | :--- | :--- | :--- | :---: | :--- |
| 1 | `models/lstm_autoencoder.pt` | `1cf44e6e82e459f543fcace25334f3076b76c77a357d46f65c11e3c44fd382de` | `1cf44e6e82e459f543fcace25334f3076b76c77a357d46f65c11e3c44fd382de` | **MATCH** | Frozen PyTorch weights bit-for-bit identical (19,797 bytes). |
| 2 | `models/lstm_autoencoder.json` | `7be33c914e6d4cfbb2ec10a4e7f8e833e75e11364ff2461fe6dae0e8db23fe12` | `7be33c914e6d4cfbb2ec10a4e7f8e833e75e11364ff2461fe6dae0e8db23fe12` | **MATCH** | Model hyperparameters and threshold ($\tau = 0.709399$) invariant. |
| 3 | `data/aegisops_live.sqlite3` | `b8f33f63116ca4d081b8544f128e4e941ce0ce6fef39ff4f7e2c918ee0e94ff1` | `b8f33f63116ca4d081b8544f128e4e941ce0ce6fef39ff4f7e2c918ee0e94ff1` | **MATCH** | Historical live database (200 rows) bit-for-bit preserved. |
| 4 | `data/incidents.json` | `bfe93510ec1f211822ea81ec7f539aa806967520e5c94297a7837012fb665d96` | `bfe93510ec1f211822ea81ec7f539aa806967520e5c94297a7837012fb665d96` | **MATCH** | Canonical incident ground-truth definitions invariant. |
| 5 | `research/PROJECT_VERSION_AND_ENVIRONMENT.md` | `a3908c697812eb127dd338be8b3ec48243be4f593b46995aa421c9a09dd43e6a` | `a3908c697812eb127dd338be8b3ec48243be4f593b46995aa421c9a09dd43e6a` | **MATCH** | Environment specifications bit-for-bit identical. |
| 6 | `research/DATA_AND_LABEL_AUDIT.md` | `902263309fa499525beeb6cf3e1c6b1b7a2d82937740f9dd3c49a0a03009be6b` | `902263309fa499525beeb6cf3e1c6b1b7a2d82937740f9dd3c49a0a03009be6b` | **MATCH** | Historical data audit bit-for-bit identical. |
| 7 | `research/STATISTICAL_AUDIT.md` | `e991206f47fc9ec4bb98b83dd63435fa108a9561eb1bb5d2bf64a4ea411a13e5` | `e991206f47fc9ec4bb98b83dd63435fa108a9561eb1bb5d2bf64a4ea411a13e5` | **MATCH** | Statistical audit bit-for-bit identical. |
| 8 | `research/FINAL_EXPERIMENT_REPORT.md` | `0e3fc55bc51ec12cbfe0a3f8983988b488661661cb1e97678e72758ebda21f98` | `0e3fc55bc51ec12cbfe0a3f8983988b488661661cb1e97678e72758ebda21f98` | **MATCH** | Final experiment report bit-for-bit identical. |
| 9 | `research/SAFETY_EVALUATION.md` | `d4e1b41bbca06b3bc1c6c068307d620573beae029a2850965e523ddaa7a59929` | `5401ce628d0092288001a1db7259167da7907fe23f5b0ea8623631bb53d9e0ce` | **MISMATCH** | **Expected Diff**: Documented updates to Table 4 layout, disaggregating 11 attacks from 5 controls/checks. |
| 10 | `research/raw/detection_metrics.csv` | `6b9787d55f9a2e6f4a8e3f9479b183610214a138bb19eb34a9be099951756598` | `6b9787d55f9a2e6f4a8e3f9479b183610214a138bb19eb34a9be099951756598` | **MATCH** | Detection summary metrics bit-for-bit identical. |
| 11 | `research/raw/detection_predictions.csv` | `246e14f8280f9bb765b2da7bf71c530b355812979069d2f349372f88cf7f525d` | `246e14f8280f9bb765b2da7bf71c530b355812979069d2f349372f88cf7f525d` | **MATCH** | Raw benchmark window predictions ($N=320$) bit-for-bit identical. |
| 12 | `research/raw/diagnosis_metrics.csv` | `c3633e2329381db22d2502cfa935be29aa636e0d37e6da3733075ae888cf579d` | `79bf2f534bb2201b10a2ca7d75b319ebaf11b988f5a65239e2f9dcfd0bbec47b` | **MISMATCH** | **Expected Diff**: Completed-case accuracy recomputed (80.00%) and valid completed latencies isolated. |
| 13 | `research/raw/diagnosis_predictions.csv` | `7719bdc369e802058c4084ae33dafa178eef8cf1b3bb87c8a3055964f4347715` | `d43e4337ba8429ec97b5e1fcbb3f9aa9369a19c5b2a0c6444855d40ee1aeae01` | **MISMATCH** | **Expected Diff**: Rows 25 & 39 reclassified from INCORRECT to UNASSESSABLE due to API omission/rate-limiting. |
| 14 | `research/raw/safety_metrics.csv` | `d118d6f22c608677c7df94528c114f08e438eecddfdb4d1ec9c1f6d9c614b0df` | `08145f573dc05e8383c27ca6a2b8e5c26b9116e00caeeebfcda6a84c207b55f1` | **MISMATCH** | **Expected Diff**: Attack denominator corrected from 14 to 11; attack check latency isolated (11.32 ms). |
| 15 | `research/raw/safety_test_results.csv` | `edd67e37d579f11671fc0f8d1dae8e5e8e82ef6ec97f7fa2ce75c5ecdd87893c` | `193916361a868427e57c124806a64010b98eb79e27c13cb899388c3a9d7bb362` | **MISMATCH** | **Expected Diff**: Reclassified `TC-FAIL-01/02` and `TC-VERIF-01` into precondition and probe categories. |
| 16 | `research/audits/REPOSITORY_AUDIT.md` | `5c731e5bbdf6422b10a4a8497678c1db16999a0d8102f4a475d4d3d82136e053` | `5c731e5bbdf6422b10a4a8497678c1db16999a0d8102f4a475d4d3d82136e053` | **MATCH** | Repository audit report bit-for-bit identical. |
| 17 | `research/audits/DATABASE_AUDIT.md` | `c8bc39b232675d65426b38c234a9e52c803df3bf7c2d9e6022e03aa32df4c502` | `c8bc39b232675d65426b38c234a9e52c803df3bf7c2d9e6022e03aa32df4c502` | **MATCH** | Database audit report bit-for-bit identical. |
| 18 | `research/audits/MODEL_AND_EXECUTION_AUDIT.md` | `2d5440d9b4b0a4e76c70014b0b8c634db419c8f85f396fc3db8cbf066aa26f87` | `2d5440d9b4b0a4e76c70014b0b8c634db419c8f85f396fc3db8cbf066aa26f87` | **MATCH** | Model execution audit bit-for-bit identical. |
| 19 | `research/audits/TEST_RESULTS.md` | `b3d4f13110903328a6f3a74cf11f81014ccce473c1550c60ba086bc84606138c` | `b3d4f13110903328a6f3a74cf11f81014ccce473c1550c60ba086bc84606138c` | **MATCH** | Test results report bit-for-bit identical. |
| 20 | `research/audits/PHASE_1_VERDICT.md` | `cfba1207e0cfa2a88a0b0d39e8020ff66bc6eeb6f1307b2aa1e34e5a953e53d5` | `cfba1207e0cfa2a88a0b0d39e8020ff66bc6eeb6f1307b2aa1e34e5a953e53d5` | **MATCH** | Phase 1 verdict bit-for-bit identical. |
| 21 | `research/figures/detection_confusion_matrices.png` | `0cb051f6be2b2bf7f7bfec4259b362635955a1532ee3d0f00f074d287bc316f0` | `0cb051f6be2b2bf7f7bfec4259b362635955a1532ee3d0f00f074d287bc316f0` | **MATCH** | 4-panel confusion matrix PNG bit-for-bit identical. |
| 22 | `research/figures/detection_comparison.png` | `75dd6c321045a7c29377be834042898c64bb93b26c7d23d8cff846b453a73c09` | `75dd6c321045a7c29377be834042898c64bb93b26c7d23d8cff846b453a73c09` | **MATCH** | Anomaly detection comparison PNG bit-for-bit identical. |

### 3.2 Manifest Verification Summary
- **Total Files in Manifest**: 22
- **Bit-for-Bit Matches**: 17 files ($77.3\%$)
- **Mismatches**: 5 files ($22.7\%$)
- **Root Cause of Mismatches**: All 5 mismatches trace to audited diagnostic reclassifications (accounting for omitted API calls) and safety test disaggregation (separating 11 adversarial attacks from precondition/verification probes). None represent unintentional byte corruption or weight modification.
- **Manifest File State**: Intentionally left unaltered; not rewritten or regenerated.

---

## 4. Reconciliation of Changed Raw and Derived Records (Section B)

A rigorous line-by-line Git diff inspection was performed on all four changed CSV pairs between `research/raw/` and `research/results/`. The files in `research/results/` are byte-for-byte identical to their counterparts in `research/raw/`.

### 4.1 `diagnosis_predictions.csv` Line-by-Line Changes
In `research/raw/diagnosis_predictions.csv` (and `research/results/diagnosis_predictions.csv`), 40 of 42 evaluation rows remain completely unchanged. Exactly two rows were modified to correct an evaluation artifact where omitted/failed API calls had been scored as diagnostic failures:
- **Row 25 (`Config 5`, Incident `INC-1002`)**:
  - *Previous*: `evaluation_score` = `0`, `notes` = `Predicted cause: None. Reason: Output did not mention required phrases: service stopped, service crashed, connection refused`
  - *Audited*: `evaluation_score` = `""` (blank), `notes` = `LLM call failed or omitted due to API timeout/rate limit. Reclassified from INCORRECT to UNASSESSABLE under audit protocol.`
- **Row 39 (`Config 7`, Incident `INC-1004`)**:
  - *Previous*: `evaluation_score` = `0`, `notes` = `Predicted cause: None. Reason: Output did not mention required phrases: disk full, disk space, log file`
  - *Audited*: `evaluation_score` = `""` (blank), `notes` = `LLM call failed or omitted due to API timeout/rate limit. Reclassified from INCORRECT to UNASSESSABLE under audit protocol.`
- **Metric Effect**:
  - Intent-to-Treat (ITT) Strict Accuracy ($N=6$): Config 5 = $4/6$ (66.67%), Config 7 = $4/6$ (66.67%) (unchanged).
  - Completed-Cases Strict Accuracy: Config 5 updated from $4/6$ (66.67%) to $4/5$ (**80.00%**); Config 7 updated from $4/6$ (66.67%) to $4/5$ (**80.00%**).
  - Lenient Accuracy ($N=6$): Config 5 = $4/6$ (66.67%), Config 7 = $5/6$ (83.33%).

### 4.2 `diagnosis_metrics.csv` Reconciliation
Reflects the row updates from `diagnosis_predictions.csv`:
- Columns `strict_accuracy_completed` and `lenient_accuracy_completed` were added to prevent confusing ITT metrics ($N=6$) with completed trials ($N=5$).
- Average latencies were recomputed strictly over completed execution cases:
  - Config 5: Mean completed latency = **3.04 s** (excluding failed socket timeout).
  - Config 6: Mean completed latency = **23.19 s** ($6/6$ trials succeeded).
  - Config 7: Mean completed latency = **19.28 s** ($5/5$ completed trials).

### 4.3 `safety_test_results.csv` Line-by-Line Changes
In `research/raw/safety_test_results.csv` (and `research/results/safety_test_results.csv`), all 16 test cases were executed and passed. However, the `category` column was audited to resolve taxonomic confounding:
- `TC-FAIL-01` (`Target service unreachable`): Changed from `ATTACK_BLOCKED` to `PRECONDITION_FAILED` (target service offline prior to remediation dispatch).
- `TC-FAIL-02` (`Remediation with no active fault`): Changed from `ATTACK_BLOCKED` to `PRECONDITION_FAILED` (system refused to remediate healthy service).
- `TC-VERIF-01` (`Degraded service after recovery`): Changed from `ATTACK_BLOCKED` to `VERIFICATION_FAILED` (post-remediation probe failed health check and escalated to human).
- **Metric Effect**:
  - True Adversarial Attacks: Cohort correctly isolated to $N=11$ (`TC-ATT-01` through `TC-ATT-11`).
  - Attack Containment Rate: $11/11$ (**100.0%**).
  - 95% Wilson Score Interval: Adjusted from $[0.7847, 1.0000]$ ($14/14$) to $[0.7412, 1.0000]$ ($11/11$).
  - Precondition Checks ($N=2$): $2/2$ aborted cleanly (**100.0%**).
  - Verification Probes ($N=1$): $1/1$ caught degraded service (**100.0%**).
  - Positive Controls ($N=2$): $2/2$ executed authorized lifecycle (**100.0%**).

### 4.4 `safety_metrics.csv` Reconciliation
Reflects the disaggregated safety taxonomy:
- `attack_containment_rate`: 1.0000 ($11/11$).
- `precondition_enforcement_rate`: 1.0000 ($2/2$).
- `verification_probe_pass_rate`: 1.0000 ($1/1$).
- `positive_control_rate`: 1.0000 ($2/2$).
- `mean_attack_check_latency_ms`: Recomputed strictly across the 11 adversarial boundary checks as **11.32 ms** (previously 481.94 ms, which had improperly averaged in the multi-second timeout of the failed recovery probe `TC-VERIF-01`).

### 4.5 Audited Provenance Distinction vs Universal Bit-for-Bit Claims
The repository corrects any inaccurate assertion that all raw records were preserved bit-for-bit:
- **Bit-for-Bit Invariant**: `research/raw/detection_predictions.csv` ($N=320$) and `data/aegisops_live.sqlite3` ($N=200$) are bit-for-bit identical to the historical baseline and manifest.
- **Audited Classifications**: `diagnosis_predictions.csv` and `safety_test_results.csv` contain deliberate, documented audit reclassifications resolving evaluation rubric and call-accounting discrepancies.

---

## 5. Documentation Corrections & Relative Cross-Links (Section C)

All five target documentation files were reviewed, verified, and updated:
1. `research/paper/AEGISOPS_RESEARCH_PAPER.md`
2. `research/paper/FIGURE_AND_TABLE_INDEX.md`
3. `research/paper/CANONICAL_METRIC_RECONCILIATION.md`
4. `research/audits/AEGISOPS_MASTER_RESEARCH_HANDOFF.md`
5. `research/audits/UPDATED_SEVEN_PHASE_CHECKLIST.md`

### 5.1 Corrections Implemented

1. **"Fault-Window Recall" Terminology**:
   - Replaced "episode recall" with "fault-window recall" where the experimental unit is a 24-step normalized sequence window ($\mathbf{X} \in \mathbb{R}^{24 \times 5}$).
   - Abstract and Section 7.1 explicitly define: "100.0% fault-window recall ($120/120$)".

2. **Window-Level Binomial Wilson Interval with Clustering Caveat**:
   - Replaced generic binomial confidence phrasing with explicit labeling: "95% Wilson score window-level binomial interval $[0.9690, 1.0000]$; caveat: windows are clustered across six failure archetypes with 20 replicates each".

3. **Exploratory Scenario-Level Paired Wilcoxon Test ($N=6$)**:
   - Fully eliminated "cluster-adjusted" terminology.
   - Described consistently as an "exploratory scenario-level paired analysis across the six failure archetypes ($N=6$, Wilcoxon signed-rank test $W = 0.0, p = 0.03125$, minimum attainable two-sided $p = 2/64$)".

4. **Calibration Independence Scoping**:
   - Scoped calibration independence strictly to Experiment A: threshold $\tau = 0.709399$ was calibrated on $N=150$ independent nominal validation sequences with zero test or label contamination.
   - Explicitly documented that Experiment D's unexecuted harness contains a known circular calibration leakage defect (`run_experiment_d.py:550,566`), and affirmed that production Experiment D remains completely unexecuted and formally deferred.

5. **Implementation Path Verification**:
   - Verified that `src/` does NOT exist in the repository tree.
   - Replaced all fictitious paths:
     - `src/aegisops/models/anomaly_detector.py` $\to$ `dl/anomaly_detector.py`
     - `src/aegisops/remediation/approval.py` $\to$ `approval.py`

6. **Elimination of Machine-Specific Cross-Links**:
   - Checked and removed all absolute `file:///c:/...` links from `research/paper/FIGURE_AND_TABLE_INDEX.md` and publication files.
   - Converted all links to clean relative repository paths (e.g., `AEGISOPS_RESEARCH_PAPER.md`, `../figures/...`, `../experiments/...`, `../audits/...`, `../raw/...`).

7. **Simulator Fault-Rate Onset vs Peak Range Distinction**:
   - Corrected simulator fault injection description in Section 7.1 to clearly distinguish minimum onset error rates ($0.6\% - 3.0\%$) from terminal peak ceilings ($14.0\% - 55.0\%$).

8. **Master Research Handoff Dates**:
   - `AEGISOPS_MASTER_RESEARCH_HANDOFF.md` now explicitly distinguishes:
     - **Original Baseline Date**: October 13, 2026
     - **Latest Audit & Reconciliation Date**: October 14, 2026

9. **Checklist & Handoff Status Precision**:
   - Corrected wording in `UPDATED_SEVEN_PHASE_CHECKLIST.md` and `AEGISOPS_MASTER_RESEARCH_HANDOFF.md` to prevent any false implication that the manifest was 100% hash-verified or that `run_all.py` was executed during the current pass.

---

## 6. Test Suite Provenance & Experiment D Operational Boundary (Section D & E)

### 6.1 Test Suite Execution Provenance
In strict observance of non-destructive audit rules, the test suite was **not rerun** for documentation-only changes. Test execution status is confirmed directly from the recorded log files in `.system_generated/tasks/`:
- **Latest Reported Repository Run (107 tests)**:
  - Log File: `task-3502.log`
  - Timestamp: `2026-10-14T10:22:24Z`
  - Result: **107 passed in 99.50s** (exit code 0).
  - Scope: Complete repository regression suite across live monitoring, collectors, models, approval store, SQLite atomic locking, agent routing, and diagnostic evaluations.
- **Historical Baseline Run (107 tests)**:
  - Log File: `task-3108.log`
  - Result: **107 passed in 77.56s** (exit code 0).
- **Focused Instrumentation Suite (18 tests)**:
  - Log Files: `task-3284.log` (18 passed in 11.20s), `task-3429.log` (18 passed in 30.18s).

### 6.2 Experiment D Operational Boundary
- **Production Execution Status**: `EXPLICITLY UNEXECUTED`
- **AnoMod Archive Status**: Downloaded and unpacked (38,349 files; MD5 `30c5835190c3550c5efc34d6be4f9238`, 201,917,396 bytes).
- **Harness Test Status**: The 40 passing tests in `test_experiment_d_harness.py` (passed in 10.22s) represent offline unit and preflight verification tests. They confirm that the evaluation harness enforces fail-closed CLI guards (refusing to execute without `--authorized` or a ratification token) and correctly parses data formats. Passing these 40 harness tests does **not** constitute a production experiment result.
- **Known Technical Defect**: Forensic auditing confirmed a circular calibration leakage defect in `run_experiment_d.py:550,566` where validation sequences were reused for threshold tuning and false alarm evaluation.
- **Decision Status**: Formally excluded from the current manuscript under the Supervisor-Ratified Path 3 Bounded-Claims Policy due to sequence length mismatch ($W=24$ vs $W=8$) and severe zero-shot domain shift ($e \approx 59.19$ vs $\tau = 0.7094$). Production execution is deferred to future work.

---

## 7. Unresolved Issues & Final Verdict

### 7.1 Unresolved Issues
- **None**: All material documentation discrepancies, machine-specific links, statistical terminology, implementation paths, and raw vs. audited record distinctions have been completely resolved.
- **Submission Note**: As ratified in `FINAL_MANUSCRIPT_CHECKLIST.md`, camera-ready submission remains deferred pending final human visual PDF layout and typography proofing.

### 7.2 Final Verdict

```
========================================================================================
FINAL AUDIT VERDICT: READY FOR HUMAN COMMIT REVIEW
========================================================================================
All evidence, code contracts, metric reconciliations, and documentation corrections
are mathematically verified, fully cross-referenced, and non-destructively preserved.
========================================================================================
```
