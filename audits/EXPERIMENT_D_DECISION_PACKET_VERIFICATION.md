# AegisOps: Experiment D Decision Packet & Methodology Verification Report

**Document Path**: `research/audits/EXPERIMENT_D_DECISION_PACKET_VERIFICATION.md`  
**Date**: October 13, 2026  
**Auditor**: Senior ML Research Engineer, Statistical Auditor & Reproducibility Reviewer  
**Repository**: `C:\DL_PROJECT` (Git HEAD: `d277c1df3c2599ddecdf5f0bb761c99718499667`, Branch: `main`)  
**Active Python Runtime**: `C:\DL_PROJECT\.venv\Scripts\python.exe` (Python 3.11.9, PyTorch 2.14.1+cpu)  
**Standard**: Non-Negotiable Research Integrity Rules & Pre-Registered Protocol v1.1.0  
**Verification Verdict**: **`READY FOR HUMAN METHODOLOGY REVIEW`**

---

## 1. Executive Summary & Verification Purpose

This report provides an independent, rigorous audit verification of the latest **Experiment D Human Decision Packet** ([`EXPERIMENT_D_HUMAN_DECISION_PACKET.md`](file:///c:/DL_PROJECT/research/audits/EXPERIMENT_D_HUMAN_DECISION_PACKET.md)) and the **Statistical Acceptance Criteria** ([`EXPERIMENT_D_STATISTICAL_ACCEPTANCE_CRITERIA.md`](file:///c:/DL_PROJECT/research/audits/EXPERIMENT_D_STATISTICAL_ACCEPTANCE_CRITERIA.md)).

All material claims, window counts, normalization formulas, call graphs, and test execution results have been verified against active source code and live execution outputs in `C:\DL_PROJECT`.

> [!IMPORTANT]
> **STRICT EXECUTION BOUNDARY**:
> **Experiment D was NOT executed against real AnoMod benchmark data.**
> No external anomaly predictions, metrics, or performance claims have been generated or recorded. The evaluation harness `research/experiments/run_experiment_d.py` remains safely and demonstrably blocked by fail-closed authorization guards (Exit Code 2 without flag, Exit Code 3 without ratification file).

---

## 2. File Inventory and Cryptographic Integrity Verification

All nine expected governance and audit documents were located and verified via SHA-256 checksums:

| Document / Asset | Repository Path | Size (Bytes) | SHA-256 Checksum | Verification Status |
| :--- | :--- | :---: | :--- | :---: |
| **Human Decision Packet** | [`research/audits/EXPERIMENT_D_HUMAN_DECISION_PACKET.md`](file:///c:/DL_PROJECT/research/audits/EXPERIMENT_D_HUMAN_DECISION_PACKET.md) | 15,842 | `42B07EE9C29FD3849EDACBBA819F469D9BDB4655122E3B0EA76DBBFDA53EA914` | **VERIFIED PRESENT** |
| **Statistical Criteria** | [`research/audits/EXPERIMENT_D_STATISTICAL_ACCEPTANCE_CRITERIA.md`](file:///c:/DL_PROJECT/research/audits/EXPERIMENT_D_STATISTICAL_ACCEPTANCE_CRITERIA.md) | 9,845 | `73BD26E831F126ACAF2C2C18256C8A3E96717BD91B39A358380189CA6593AE10` | **VERIFIED PRESENT** |
| **Master Handoff** | [`research/audits/AEGISOPS_MASTER_RESEARCH_HANDOFF.md`](file:///c:/DL_PROJECT/research/audits/AEGISOPS_MASTER_RESEARCH_HANDOFF.md) | 24,050 | `84F2421AF647042958D2075F0D3BF87829E9A60C0CF1A2CF3EA72F4079A38DF4` | **VERIFIED PRESENT** |
| **Master Checklist** | [`research/audits/UPDATED_SEVEN_PHASE_CHECKLIST.md`](file:///c:/DL_PROJECT/research/audits/UPDATED_SEVEN_PHASE_CHECKLIST.md) | 12,203 | `38E30AD9E18E8FE2720ED80312937F284958B87760534A160BB921BA7D7BCA4D` | **VERIFIED PRESENT** |
| **Readiness Verdict** | [`research/audits/EXPERIMENT_D_READINESS_VERDICT.md`](file:///c:/DL_PROJECT/research/audits/EXPERIMENT_D_READINESS_VERDICT.md) | 4,059 | `FDE2EC057561CA8528A503FDF1843BAE390A1A9738C4A364C8D877B9932BF812` | **VERIFIED PRESENT** |
| **Requirements Traceability** | [`research/audits/EXPERIMENT_D_REQUIREMENTS_TRACEABILITY.md`](file:///c:/DL_PROJECT/research/audits/EXPERIMENT_D_REQUIREMENTS_TRACEABILITY.md) | 4,628 | `0914A48F211B933209F59CD6185F2154736DD1CF0A44E68ADB8ACBA1AF25E1B4` | **VERIFIED PRESENT** |
| **Test Results Audit** | [`research/audits/EXPERIMENT_D_TEST_RESULTS.md`](file:///c:/DL_PROJECT/research/audits/EXPERIMENT_D_TEST_RESULTS.md) | 9,125 | `CCBA6276C911EB523E8479D0FF5908757E3B757499A54406439FF6782CEE01E0` | **VERIFIED PRESENT** |
| **Protocol Reconciliation** | [`research/audits/EXPERIMENT_D_PROTOCOL_RECONCILIATION.md`](file:///c:/DL_PROJECT/research/audits/EXPERIMENT_D_PROTOCOL_RECONCILIATION.md) | 6,238 | `5FF19D05E596023992B2F7CB792D98F0EE6ED6C246F0F4784F7504FF25413DF9` | **VERIFIED PRESENT** |
| **Amendment Proposal** | [`research/audits/PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md`](file:///c:/DL_PROJECT/research/audits/PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md) | 12,127 | `ECF610E82089094632EDE7917229F9FED4FDC3494E0472C6354E07A802E05649` | **VERIFIED PRESENT** |
| **Temporal Eligibility JSON** | [`research/audits/experiment_d_temporal_eligibility_audit.json`](file:///c:/DL_PROJECT/research/audits/experiment_d_temporal_eligibility_audit.json) | 15,710 | `3DB978B7FD27D99AFCA0064B95FDD2D5A2252372680E8F666C1EA02ED717A9E9` | **VERIFIED PRESENT** |
| **Execution Harness** | [`research/experiments/run_experiment_d.py`](file:///c:/DL_PROJECT/research/experiments/run_experiment_d.py) | 39,081 | `A09B52EBE0F7A6E557161879308DCE34360F65D654E4B829A09874FE1717EB5D` | **VERIFIED PRESENT** |
| **Frozen Checkpoint** | [`models/lstm_autoencoder.pt`](file:///c:/DL_PROJECT/models/lstm_autoencoder.pt) | 19,797 | `1CF44E6E82E459F543FCACE25334F3076B76C77A357D46F65C11E3C44FD382DE` | **VERIFIED FROZEN** |
| **Model Metadata** | [`models/lstm_autoencoder.json`](file:///c:/DL_PROJECT/models/lstm_autoencoder.json) | 846 | `24826B053833B08E80FB84E7E694ADFAD5B4A1124D935CCF3E3CD4F575EB045F` | **VERIFIED FROZEN** |

---

## 3. Implementation and Execution Path Verification

### 3.1 Authorized Execution Path Trace
Source code inspection of `run_experiment_d.py` confirmed:
1. **Checkpoint & Dataset Verification** (`main()` lines 816–850):
   - Confirms model file existence and SHA-256 (`1cf44e6e...`).
   - Checks feature order `("cpu_pct", "memory_pct", "latency_ms", "error_rate_pct", "disk_pct")`.
   - Discovers unpacked dataset directory structure (13 SN scenarios, 13 TT scenarios).
2. **Fail-Closed Execution Guards** (`main()` lines 896–926):
   - Missing `--authorized`: prints `EXPERIMENT D EXECUTION: BLOCKED` and exits with code 2.
   - Missing `PROTOCOL_AMENDMENT_V1_2_RATIFICATION.json`: prints `EXPERIMENT D EXECUTION: BLOCKED — PROTOCOL AMENDMENT PENDING APPROVAL` and exits with code 3.
   - Ratification JSON validation: verifies `"protocol_version": "v1.2.0"`, `"status": "RATIFIED"`, and `"ratified_by"`.
3. **End-to-End Production Loop** (`run_production_experiment_d()` lines 687–779):
   - Loads `Normal_Baseline` from SocialNetwork metric and trace directories.
   - Calls `partition_normal_series_chronologically()` (70/30 split, 7-step purge gap).
   - Calls `build_contiguous_windows()` on raw calibration and validation partitions.
   - Loops through all 12 SocialNetwork fault scenarios and extracts contiguous $W=8$ windows.
   - Passes partitions and scenarios to `run_evaluation_pipeline()`.
   - **Validation Population Invariant**: Verified that `include_val_in_predictions=True` is explicitly passed (line 746), ensuring held-out normal validation windows ($y = 0$) are evaluated alongside fault windows ($y = 1$) to compute true False Positive Rate, Specificity, and Precision.
   - Evaluates all 5 models (AegisOps LSTM, Isolation Forest, Narrow Rules, Resource Rules, Full Operational Rules) on identical windows.
   - Computes paired McNemar exact test and scenario-level Wilcoxon signed-rank test.
   - Writes `external_anomod_predictions.csv`, `external_anomod_metrics.csv`, `EXPERIMENT_D_RESULTS.md`, and `experiment_d_manifest.json`.
   - Asserts all 4 files exist and `st_size > 0`.
   - **Conclusion**: The authorized execution path is a **genuine, complete execution loop**, NOT a scaffold or stub. It does not return early.

---

## 4. Methodology Audit Findings

### 4.1 Training vs. External Normalization
- **Frozen Training Normalization (Verified Fact)**:
  `models/lstm_autoencoder.json` records that the model was trained on standardized features:
  $\mathbf{z} = (\mathbf{x} - \boldsymbol{\mu}_{\text{train}}) / \boldsymbol{\sigma}_{\text{train}}$ with mean `[42.06, 53.97, 76.89, 0.24, 48.27]` and std `[5.79, 3.56, 6.09, 0.055, 4.34]`.
- **Protocol v1.1.0 Min-Max Conflict (Verified Fact)**:
  Protocol v1.1.0 mandated scaling features into $[0, 1]$. Because the autoencoder's linear output and recurrent activations were optimized for zero-mean targets, mapping features into $[0, 1]$ introduces a $+0.5$ systematic shift that dominates reconstruction error and causes 100% false alarms.
- **Proposed Amendment v1.2.0 Domain Z-Score (Proposed Decision)**:
  Standardizing external telemetry relative to its own steady-state baseline ($\boldsymbol{\mu}_{\text{normal}}^{\text{ext}}, \boldsymbol{\sigma}_{\text{normal}}^{\text{ext}}$) preserves the $\mathcal{N}(0, 1)$ operating regime of the LSTM and scales relative anomaly deviations proportionally.

### 4.2 Calibration Population and Sample Size
- **Empirical Re-Count (Verified Fact)**:
  `Normal_Baseline` in SocialNetwork contains 80 raw 15s observations (1,185s). Request traffic is bursty, with 23 empty intervals (28.75%). Contiguous active runs are `[11, 11, 18]` steps, producing **19 contiguous $W=8$ sliding windows**.
- **Chronological Split & Purge Gap Effect (Verified Fact)**:
  Partitioning the raw time series (rows 0–55 calibration, rows 56–62 purge, rows 63–79 validation) yields:
  - **$N_{\text{calib}} = 5$ contiguous windows**
  - **$N_{\text{val}} = 8$ contiguous windows**
  - 6 windows lost across the 105s purge gap.
- **Small-Sample Tail Uncertainty (Methodological Fact)**:
  Computing an empirical 99th percentile on 8 validation windows evaluates to the empirical maximum ($\max(\mathbf{e}_{\text{val}})$). While statistically valid as a conservative empirical maximum, it has high sampling variance. The decision packet properly pairs this with a parametric Gaussian sensitivity analysis ($\mu + 2.326\sigma$).

### 4.3 Cohort Stratification
- **SocialNetwork Primary Confirmatory Cohort (Verified Fact)**:
  13 scenarios, 303 contiguous windows, complete distributed trace coverage ($1,500$–$2,200$ spans per scenario). $K=12$ fault scenarios provide adequate power for scenario-level Wilcoxon signed-rank tests ($p_{\min} \approx 0.00049$).
- **TrainTicket Secondary Exploratory Cohort (Verified Fact)**:
  SkyWalking traces cover only the final 203 seconds of 765-second runs (548s missing traces). Yields only 74 contiguous windows across all 13 scenarios (only 8 normal windows). Scenarios with 2–4 windows produce degenerate contingency tables. Relegation to secondary exploratory evidence is scientifically mandatory.

### 4.4 Statistical Independence and Autocorrelation
- **Autocorrelation Fact (Verified Fact)**:
  Consecutive sliding windows with stride 1 share 7 of 8 observations ($87.5\%$ overlap). While McNemar's test assesses marginal detection agreement, confidence intervals and p-values assume independent trials. The decision packet properly mandates that:
  - Window-level McNemar p-values must be reported with an explicit autocorrelation caveat.
  - The scenario-level Wilcoxon signed-rank test ($K=12$ mutually independent runs) serves as the primary confirmatory statistical anchor.

---

## 5. Test Evidence and Regression Verification

All tests were executed directly in the repository virtual environment (`C:\DL_PROJECT\.venv`):

| Test Suite | Command Line | Passing | Failing | Skipped | Exit Code | Verified Behavior |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Harness Suite** | `.venv\Scripts\python.exe -m pytest test_experiment_d_harness.py -q` | 40 | 0 | 0 | 0 | 40/40 passed in 8.56s. All windowing, gap rejection, chronological split, baseline rules, and CLI guards verified. |
| **Full Repository Regression** | `.venv\Scripts\python.exe -m pytest --tb=short` | 105 | 0 | 0 | 0 | 105/105 passed in 36.83s across all 11 test modules. |
| **Unauthorized Guard** | `.venv\Scripts\python.exe research/experiments/run_experiment_d.py` | — | — | — | 2 | Refuses unflagged execution; prints BLOCKED. |
| **Unratified Guard** | `.venv\Scripts\python.exe research/experiments/run_experiment_d.py --authorized` | — | — | — | 3 | Refuses execution without ratification file; prints BLOCKED. |
| **Dry Run Mode** | `.venv\Scripts\python.exe research/experiments/run_experiment_d.py --dry-run` | — | — | — | 0 | Completes checks without writing outputs. |
| **Sandbox Pipeline** | `.venv\Scripts\python.exe research/experiments/run_experiment_d.py --test-pipeline` | — | — | — | 0 | Executes full call graph in isolated tempdir; writes and validates test artifacts. |

---

## 6. Categorical Epistemic Classification

To ensure complete scientific integrity, all findings are categorized into five distinct epistemic classes:

1. **Verified Facts (Directly evidenced in code, data, and tests)**:
   - Checkpoint SHA-256 is `1cf44e6e...` with 3,733 frozen parameters.
   - Checkpoint was trained on standardized features with mean `[42.06, 53.97, 76.89, 0.24, 48.27]`.
   - `Normal_Baseline` contains 80 raw intervals yielding 19 contiguous windows ($N_{\text{calib}}=5, N_{\text{val}}=8$ after chronological split and 7-step purge).
   - TrainTicket SkyWalking traces are truncated to the final 203 seconds (548s missing traces).
   - All 40 harness tests and 105 full repository tests pass with exit code 0.
2. **Reported Claims (Documented historical findings)**:
   - Historical Experiment A achieved Recall 100%, FPR 1.50%, McNemar $p = 2.17 \times 10^{-19}$ on synthetic simulator data.
   - Historical Experiment B achieved 83.3% strict accuracy in pilot RCA ($N=6$).
   - Historical Experiment C achieved 100% containment across 11 adversarial injection attacks.
3. **Assumptions (Mathematical and scientific premises)**:
   - Domain Z-score assumes external steady-state microservice telemetry is approximately stationary.
   - Parametric threshold sensitivity assumes reconstruction errors approximate a Gaussian distribution.
4. **Proposed Decisions (Awaiting supervisor sign-off)**:
   - Adopting Domain Z-score (Option 2) as Primary Confirmatory evaluation.
   - Adopting Frozen Training Scaler (Option 3) as Secondary Exploratory zero-shot shift analysis.
   - Designating SocialNetwork as Primary Cohort and TrainTicket as Secondary Exploratory Cohort.
5. **Approvals Still Required (Mandatory external actions)**:
   - Formal supervisor signing and committing of `research/audits/PROTOCOL_AMENDMENT_V1_2_RATIFICATION.json`.

---

## 7. Recommended Next Action

The human supervisor should review [`research/audits/EXPERIMENT_D_HUMAN_DECISION_PACKET.md`](file:///c:/DL_PROJECT/research/audits/EXPERIMENT_D_HUMAN_DECISION_PACKET.md). If approving the proposed methodological resolution, create and commit the ratification record:

**File to Create**: `C:\DL_PROJECT\research\audits\PROTOCOL_AMENDMENT_V1_2_RATIFICATION.json`
```json
{
  "protocol_version": "v1.2.0",
  "status": "RATIFIED",
  "ratified_by": "Research Supervisor",
  "ratification_date_utc": "2026-10-13T07:20:00Z",
  "approved_options": {
    "normalization": "Option 2 (Domain Z-Score) Confirmatory; Option 3 Exploratory",
    "cohort_scope": "SocialNetwork Primary Confirmatory; TrainTicket Secondary Exploratory",
    "threshold_method": "Empirical 99th percentile with Parametric Gaussian sensitivity"
  }
}
```

Once committed, execution can be initiated using:
```powershell
.venv\Scripts\python.exe research/experiments/run_experiment_d.py --authorized
```

---

## 8. Final Audit Verdict

```
READY FOR HUMAN METHODOLOGY REVIEW
```

*(All engineering, code, test, mathematical, and decision-support verification requirements are satisfied. The implementation is complete and verified, the decision packet is sound, and execution remains safely fail-closed awaiting human ratification).*
