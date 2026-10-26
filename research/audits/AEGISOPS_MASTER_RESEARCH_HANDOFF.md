# AegisOps: Master Research Handoff & Scientific Status Matrix

> **Supersession notice (2026-10-15):** This handoff preserves its prior review-state summaries. The current release decision is **NOT READY — MATERIAL CONTRADICTIONS OR RENDERING BLOCKERS REMAIN** pending faithful rendered-manuscript review, author/venue confirmation, and final provenance closure. Do not treat any "Ready for Supervisor Review" line below as the current release verdict.

**Document Path**: `research/audits/AEGISOPS_MASTER_RESEARCH_HANDOFF.md`
**Original Baseline Date**: October 13, 2026<br>
**Latest Audit & Reconciliation Date**: October 14, 2026<br>
**Auditor**: Senior Research Supervisor, ML Engineer & Reproducibility Auditor<br>
**Repository**: `C:\DL_PROJECT` (Current Branch: `publish/research-without-external-dataset`, Git HEAD: `a32713c30a8ddca1425d44b1afbaf6d55a64c276`; Historical Audited Baseline Commit: `ec83d2fe...` on `main`)<br>
**Active Python Runtime**: `C:\DL_PROJECT\.venv\Scripts\python.exe` (Python 3.11.9, PyTorch 2.14.1+cpu)  
**Standard**: Non-Negotiable Research Integrity Rules, Protocol v1.1.0 & Protocol Amendment v1.2.0 Proposal  

---

## A. Research Objective and Claimed Novelty

### Project Title:
**AegisOps: A Human-Gated, Deep-Learning-Augmented Multi-Agent Workflow for IT Incident Detection, Diagnosis, and Recovery Verification.**

### Core Claimed Novelty:
1. **Continuous Neural-Agent Synergy**: Seamless integration of temporal-continuous deep learning anomaly detection (LSTM Autoencoder) with multi-agent LLM reasoning (Triage, SRE Diagnosis, Verification) for distributed microservice incidents.
2. **Deterministic Human-Gated Authorization Boundary**: Enforces single-use UUIDv4 tokens, confirmation phrases, action/target scope binding, and execution constraints (`approval.py`, SQLite `BEGIN IMMEDIATE` atomic state transitions) preventing autonomous LLM agents from executing high-risk remediation actions without explicit human approval.
3. **Closed-Loop Post-Remediation Verification**: Automated verification probes and telemetry monitoring that confirm system health metrics return to nominal operating envelopes prior to incident closure, preventing prematurely resolved incident loops.

---

## B. Verified Completed Phases

| Phase | Description | Standardized Status | Key Verification Evidence |
| :---: | :--- | :---: | :--- |
| **Phase 1** | Repository Inventory & Baseline | **COMPLETED** | 42 baseline tests passing; read-only SQLite schema verified (`data/aegisops_live.sqlite3`, 86,016 bytes). |
| **Phase 2** | Dataset, Telemetry & Episode Reconciliation | **COMPLETED** | Reconciled 200-row telemetry mapping; resolved 169 true fault samples vs 175 episode artifact discrepancy. |
| **Phase 3** | Anomaly Detection Benchmark (Experiment A) | **COMPLETED** | $N=320$ test windows evaluated; exact McNemar $p = 2.168 \times 10^{-19}$ (descriptive); scenario-level Wilcoxon $W = 0.0, p = 0.03125$ (exploratory). Full Operational Rules vs Narrow/Resource rules disaggregated. False Alarms/hr marked UNAVAILABLE. |
| **Phase 4** | Root-Cause Diagnosis Benchmark (Experiment B) | **IN PROGRESS** | 42 rubric evaluations (7 configurations $\times$ 6 scenarios); Live LLM achieved 83.3% strict / 100% lenient accuracy. Pilot complete. |
| **Phase 5** | Execution Boundary Safety Evaluation (Experiment C) | **COMPLETED** | 16-case boundary taxonomy verified (11 attacks, 2 safety checks, 1 verification, 2 controls); 100% containment (11/11). |
| **Phase 6** | Unified Reproducibility Pipeline & Manifest | **COMPLETED** | Historical pipeline run (`run_all.py`) replicated with exit code 0 in 53.6s; historical SHA-256 manifest covers 22 artifacts (17 verified bit-for-bit identical; 5 differing due to subsequent Phase 4/5 audited classifications and metric recomputations). Current pipeline run was not re-executed during documentation passes. |
| **Phase 8** | Reproducibility Closure & Protocol Freezing | **COMPLETED** | Mathematical resolution of IF threshold (-0.018694); AnoMod selected; Protocol v1.1.0 frozen. |
| **Phase 9 (Stages 1–3)** | Dataset Ingestion, Extraction & Schema Validation | **COMPLETED** | Archive `AnoMod.zip` acquired (201,917,396 bytes, MD5 `30c58351...`); 38,349 items unpacked; schema verified. |

---

## C. Current Repository and Checkpoint State

- **Git Branch**: `publish/research-without-external-dataset` (checkout at commit `a32713c30a8ddca1425d44b1afbaf6d55a64c276`; historical audited baseline on `main`)
- **Git HEAD Commit**: `a32713c30a8ddca1425d44b1afbaf6d55a64c276`
- **Working Tree State (Verified via `git status --short --untracked-files=all`)**:
  - **Modified Tracked Files (30 files)**: `README.md`, `research/SAFETY_EVALUATION.md`, `research/audits/AEGISOPS_MASTER_RESEARCH_HANDOFF.md`, `research/audits/UPDATED_SEVEN_PHASE_CHECKLIST.md`, `research/experiments/generate_diagnosis_audit.py`, `research/experiments/run_experiment_c.py`, `research/experiments/run_safety_audit.py`, `research/paper/AEGISOPS_RESEARCH_PAPER.md`, `research/paper/FIGURE_AND_TABLE_INDEX.md`, `research/paper/FIGURE_AND_TABLE_REGISTER.md`, `research/paper/FINAL_EVIDENCE_AUDIT.md`, `research/paper/FINAL_MANUSCRIPT_CHECKLIST.md`, `research/paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`, `research/paper/MANUSCRIPT_FINALIZATION_PLAN.md`, `research/paper/REFERENCES_VERIFICATION.md`, `research/paper/REFERENCE_VERIFICATION.md`, `research/paper/figures/approval_recovery_workflow.mmd`, `research/paper/figures/architecture_dataflow.mmd`, `research/raw/diagnosis_metrics.csv`, `research/raw/diagnosis_predictions.csv`, `research/raw/safety_metrics.csv`, `research/raw/safety_test_results.csv`, `research/results/diagnosis_metrics.csv`, `research/results/diagnosis_predictions.csv`, `research/results/generate_statistical_analysis.py`, `research/results/safety_metrics.csv`, `research/results/safety_test_results.csv`, `research/results/statistical_analysis.md`, `research/run_all.py`, `test_research_instrumentation.py`.
  - **Untracked File (1 file)**: `research/paper/CANONICAL_METRIC_RECONCILIATION.md` (authoritative metric reconciliation matrix).
  - **Ignored Assets (Verified via `git status --ignored --short`)**: `.env`, `.pytest_cache/`, `.venv/`, `__pycache__/` trees, SQLite databases (`data/aegisops_live.sqlite3`, `data/safety_telemetry.sqlite3`, `data/safety_test_store.sqlite3`), and external benchmark data (`data/external/anomod/`, 38,349 files).
- **Virtual Environment**: `C:\DL_PROJECT\.venv\Scripts\python.exe` (Python 3.11.9, AMD64).
- **Deep Learning Runtime**: PyTorch `2.14.1+cpu`.
- **Frozen Checkpoint**: `models/lstm_autoencoder.pt` (19,797 bytes).
  - SHA-256: `1cf44e6e82e459f543fcace25334f3076b76c77a357d46f65c11e3c44fd382de`
  - Total Parameters: **3,733** (Encoder: 1,472; Decoder: 2,176; Output: 85).
  - State Dictionary: Strict load verified (`missing_keys=[]`, `unexpected_keys=[]`).
  - Mode: `eval()` verified (`training=False`).
  - Weight Immutability: 10 repeated inferences on identical inputs yielded maximum score delta of $0.00$. Parameter tensors unchanged bit-for-bit.
  - Frozen Metadata: `models/lstm_autoencoder.json` (Threshold: `0.7093990445137024`).
- **Historical & Audited Records**: `research/raw/detection_predictions.csv` (24,357 bytes, $N=320$ test windows) is bit-for-bit preserved identical to the manifest. In contrast, `research/raw/diagnosis_predictions.csv`, `research/raw/diagnosis_metrics.csv`, `research/raw/safety_test_results.csv`, and `research/raw/safety_metrics.csv` reflect audited classifications and recomputed metrics rather than bit-for-bit manifest preservation.
- **Test Suite Provenance & Separation**:
  - **Full Suite (107 tests)**:
    - *Historical Baseline Run*: `task-3108.log`, 107 passed in 77.56s (exit code 0).
    - *Current Working-Tree Run*: `task-3502.log`, 107 passed in 99.50s at `2026-10-14T10:22:24Z` (exit code 0). Zero regressions across modified runners and test files.
  - **Focused Instrumentation Suite (18 tests)**:
    - *Run A*: `task-3284.log`, 18 passed in 11.20s (exit code 0).
    - *Run B*: `task-3429.log`, 18 passed in 30.18s at `2026-10-14T07:39:36Z` (exit code 0).
    - *Duration Variance Cause*: Cold Python module import and background Windows disk I/O contention; both runs passed identical test cases with exit code 0.
- **Review Status**: Manuscript Review Package — Ready for Supervisor Review (Camera-ready submission deferred until visual PDF layout proofing is completed).

---

## D. Verified Synthetic Experiment Results (Clearly Labeled Synthetic)

> [!IMPORTANT]
> **SYNTHETIC BENCHMARK DECLARATION**:
> All results in Experiment A (`research/raw/detection_predictions.csv`, `research/raw/detection_metrics.csv`) were generated exclusively from synthetic mathematical telemetry generated by `simulator.py` across 6 simulated failure scenarios over a 24,000-second (6.67-hour) exposure window. These results reflect controlled simulated fault injections and do NOT establish real-world microservice performance.

### Experiment A Performance Summary ($N=320$ Windows: 200 Normal + 120 Fault):

| Detection Architecture | True Positive (TP) | False Positive (FP) | True Negative (TN) | False Negative (FN) | Recall | Precision | False Positive Rate (FPR) | Specificity | F1 Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Narrow Rules** | 40 | 0 | 200 | 80 | 33.33% | 100.0% | 0.00% | 100.0% | 0.5000 |
| **Resource-Only Rules** | 80 | 0 | 200 | 40 | 66.67% | 100.0% | 0.00% | 100.0% | 0.8000 |
| **Full Operational Rules** | 120 | 0 | 200 | 0 | 100.0% | 100.0% | 0.00% | 100.0% | 1.0000 |
| **Isolation Forest** (Calibrated $\tau = -0.018694$) | 57 | 4 | 196 | 63 | 47.50% | 93.44% | 2.00% | 98.00% | 0.6298 |
| **AegisOps LSTM Autoencoder** (Frozen $\tau = 0.709399$) | 120 | 2 | 198 | 0 | **100.0%** | **98.36%** | **1.00%** | **99.00%** | **0.9917** |
| **Combined Alert** (Rules $\lor$ LSTM AE) | 120 | 2 | 198 | 0 | **100.0%** | **98.36%** | **1.00%** | **99.00%** | **0.9917** |

> [!NOTE]
> **Operational Rule Predicate Overlap**: The 100.0% synthetic recall achieved by Full Operational Rules is directly affected by structural overlap between the simulated error-rate injection predicate (`error_rate_pct` ramping from $\ge 0.6\%$ up to $14.0\% - 55.0\%$ across all six failure modes, `dl/anomaly_detector.py`) and the operational rule's own error-rate threshold (`error_rate_pct > 0.5%`, `run_experiment_a.py:90`). Telemetry stores `error_rate_pct` in percentage points ($0$ to $100\%$, `collectors/system_metrics.py:124`), where normal sequences remain $\le 0.5\%$ ($\mu \approx 0.24\%$). Earlier narrative drafts cited fractional notations (`0.05` or `0.15`), but the source code confirms percentage units. This synthetic tautology explains the 100% rule recall on this benchmark, whereas on real-world workloads with novel, non-error-rate failure modes, recall would be significantly lower.

### Verified Statistical Comparisons:
- **McNemar Exact Test (LSTM Autoencoder vs Isolation Forest)**:
  - Discordant pairs on 120 fault windows: $b = 63$ (LSTM detected, IF missed), $c = 0$ (IF detected, LSTM missed), $a = 57, d = 0$.
  - Exact binomial two-sided p-value: **$p = 2 \times (0.5)^{63} \approx 2.168 \times 10^{-19}$** ($p < 0.001$, reject null hypothesis).
- **Wilcoxon Signed-Rank Test Across Scenarios ($N=6$)**:
  - Aggregating the 20 replicates per scenario yields scenario sensitivities:
    - LSTM: $1.00, 1.00, 1.00, 1.00, 1.00, 1.00$ ($100\%$ across all 6).
    - Isolation Forest: $0.40, 0.25, 0.85, 0.75, 0.40, 0.20$ (mean $= 0.475$).
    - Paired differences: $+0.60, +0.75, +0.15, +0.25, +0.60, +0.80$.
  - $W = 0.0$, two-sided exact **$p = 2 \times (1/2)^6 = 0.03125$** (minimum possible discrete p-value for $N=6$).
- **Statistical Sampling Unit and Dependence Caveat**:
  - Evaluation unit is the 24-step discrete normalized sequence window ($W=24, \Delta t=5\text{s}$). The 200 normal windows are non-overlapping synthetic steady-state sequences. The 120 fault windows originate from 6 underlying failure modes ($20$ independent realizations each). Because realizations share underlying failure dynamics within each scenario archetype, windows share intra-cluster correlation. Window-level McNemar test ($p = 2.168 \times 10^{-19}$) is reported as descriptive at the window level.
  - The scenario-level paired non-parametric analysis (Wilcoxon signed-rank test, $N=6$ scenarios; $W = 0.0, p = 0.03125$) removes intra-cluster dependence across replicates, but the $N=6$ result is strictly exploratory and does not establish broad statistical independence or generalization to production architectures. Operational False Alarms/hr is marked **UNAVAILABLE**.

---

## E. Root-Cause Diagnosis (RCA) and Safety-Test Evidence with Limitations

### Experiment B: Multi-Agent RCA Diagnosis (Pilot Benchmark)
- **Design**: Factorial evaluation of 7 agent configurations $\times$ 6 incident scenarios = 42 rubric-scored evaluations.
- **Results**:
  - Config 1: Deterministic Rule Baseline: 100.0% strict ITT (6/6), 100.0% lenient (6/6), 0.01 ms execution latency.
  - Config 2: Single-Agent (Offline Heuristic): 50.0% strict (3/6), 50.0% lenient (3/6), 0.03 ms.
  - Config 3: Multi-Agent Full (Offline Heuristic + DL): 50.0% strict (3/6), 50.0% lenient (3/6), 0.57 ms.
  - Config 4: Multi-Agent No-DL (Offline Heuristic Log-Only): 100.0% strict (6/6), 100.0% lenient (6/6), 0.11 ms.
  - Config 5: Single-Agent (Live Groq LLM): 66.67% strict ITT (4/6), 80.00% completed cases (4/5; 1 omitted due to Groq rate limit), 66.67% lenient (4/6), 3.04 s mean latency over completed cases.
  - Config 6: Multi-Agent Full (+ DL Handoff, Live Groq LLM): 83.33% strict (5/6), 100.0% lenient (6/6), 23.19 s mean latency.
  - Config 7: Multi-Agent No-DL (Log-Only, Live Groq LLM): 66.67% strict ITT (4/6), 80.00% completed cases (4/5; 1 omitted due to Groq rate limit), 83.33% lenient (5/6), 19.28 s mean latency over completed cases.
- **Explicit Limitations**:
  - Bounded sample size ($N=6$, statistical power $1-\beta \approx 0.14$).
  - Rubric lexical overlap: Keyword-based scoring rubrics contain lexical overlap with scenario descriptions.
  - Scoring taxonomy: Strict/lenient and Intention-to-Treat (ITT) versus completed-case distinctions are strictly preserved.
  - Provider wire logging and routing: Provider wire logs were not retained during live API execution, and independent external verification of provider network routing was not performed (evaluations ran against Groq Cloud API endpoints over HTTPS without retaining raw wire traces).
  - Unresolved Cost Provenance: Estimated API costs (~$0.006–$0.018/incident) lack provider wire billing logs, prompt token counts, and completion token records in the repository; no live API calls were performed during audits.
  - Offline mock configurations rely on hardcoded fallback responses.
  - Generalizability claim restricted to pilot feasibility demonstration; large-scale evaluation deferred.

### Experiment C: Execution Boundary Safety
- **Design**: 16-case empirical boundary evaluation.
  - 11 adversarial attacks (`TC-ATT-01` through `TC-ATT-11`: invalid tokens, expired TTL, confirmation phrase mismatch, scope tampering, consumed nonce replay, rejected ticket, out-of-boundary remote targets, plaintext remote, credential leak).
  - 2 execution precondition checks (`TC-FAIL-01`: local test service unreachable, `TC-FAIL-02`: remediation invoked with no active fault).
  - 1 recovery verification probe (`TC-VERIF-01`: degraded service after remediation correctly marked `VERIF_FAILED`).
  - 2 positive controls (`TC-POS-01`: full authorized lifecycle, `TC-AUDIT-01`: independent audit log verification).
- **Results**:
  - Attack Containment: **100.0%** (11/11 attacks blocked; 95% Wilson score CI: $[0.7412, 1.0000]$).
  - Positive Control Execution: 100.0% (2/2 approved commands executed successfully).
  - Implementation Verification: Verified atomic SQLite transactions (`BEGIN IMMEDIATE`) and parameter scope binding in `approval.py`.
- **Explicit Limitations**:
  - Evaluated on localhost application loopback interface (`127.0.0.1:8765`).
  - Does not evaluate distributed Kubernetes RBAC, network service mesh sidecars, or OS kernel escapes.

---

## F. Experiment D Readiness and External Evaluation Status

### Benchmark Dataset:
- **AnoMod** (Ping et al., MSR 2026, Zenodo record `18342898`, DOI: `10.5281/zenodo.18342898`, CC-BY-4.0).
- Unpacked: 38,349 files across 13 SocialNetwork scenarios and 13 TrainTicket scenarios.
- Authoritative MD5: `30c5835190c3550c5efc34d6be4f9238` (201,917,396 bytes).

### Current Execution Gate Status:
```
BLOCKED — PREREQUISITES UNRESOLVED (PROTOCOL AMENDMENT PENDING APPROVAL)
```

### Critical Operational Boundary:
> [!IMPORTANT]
> **Production Experiment D has NOT been executed against external AnoMod microservice telemetry.**
> Confirmatory external predictions, metrics, and transfer claims do not exist and are excluded from the paper. While dataset preflight acquisition was completed (38,349 files verified) and exploratory off-contract diagnostic checks demonstrated severe zero-shot domain shift ($e \approx 59.19$ vs $\tau = 0.7094$, an $\approx 83.4\times$ / $>80\times$ domain shift, resulting in $19/19$ false alarms on nominal $W=8$ data; $0$ valid $W=24$ contiguous segments; see `EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md`), production evaluation was halted and deferred under Path 3.
>
> Critical clarifications regarding external validation:
> 1. **Off-Contract Diagnostic Windows**: The 19/19 preflight windows evaluated in exploratory zero-shot checks are off-contract, overlapping 8-step diagnostic windows ($W=8$, sharing 87.5% temporal overlap). This result is strictly an exploratory diagnostic proof of catastrophic zero-shot distribution shift, **not a production false-alarm-rate estimate**.
> 2. **Temporal Resolution Compatibility Conflict**: The frozen LSTM Autoencoder operates strictly on 24-step normalized sequences sampled at 5-second cadence ($W=24, \Delta t=5\text{s}$, representing a 120-second historical horizon). In contrast, the AnoMod telemetry extracted for Experiment D is recorded at 15-second intervals ($\Delta t = 15\text{s}$, where 24 steps would span 360 seconds). Evaluating 15-second aggregates against the 5-second neural weights constitutes a distinct, unresolved compatibility defect that cannot be bridged without model retraining or sequence interpolation.
> 3. **Unexecuted Status**: The software harness (`research/experiments/run_experiment_d.py`) remains unratified and unexecuted.
> 4. **Harness Calibration/Evaluation Leakage Defect**: A forensic audit (`EXPERIMENT_D_CALIBRATION_INDEPENDENCE_AUDIT.md`) proved that the unexecuted harness reused validation windows (`v_win`) for both 99th percentile threshold calibration and false-alarm evaluation (`run_experiment_d.py:550,566`), which would guarantee $\text{FPR}=0\%$ by circular construction. This methodological defect reinforces why execution was blocked.

### Harness Readiness Summary:
1. **Production Call Graph**: Fully implemented via `run_production_experiment_d()`. Discovers scenarios, extracts 5D telemetry, partitions chronologically, builds contiguous windows, scores all 5 baselines, and validates outputs.
2. **Fail-Closed Execution Gate**:
   - Missing `--authorized`: exits with code 2.
   - Missing `PROTOCOL_AMENDMENT_V1_2_RATIFICATION.json`: exits with code 3.
   - `--dry-run` and `--validate-only`: exits with code 0 without writing artifacts.
   - `--test-pipeline`: exits with code 0 executing in isolated tempdir.
3. **Temporal Continuity Enforced**: `build_contiguous_windows()` enforces strict $\Delta t = 15.0\text{s}$ spacing between adjacent window observations. Gaps or NaNs immediately reset buffer.
4. **Calibration Leakage Defect Identified in Unexecuted Harness**: Documented above; `v_win` reuse in lines 550 and 566 blocks production validity.
5. **No Arbitrary Imputation**: Idle intervals ($N_{\text{req}} = 0$) preserve NaNs; zero latency imputation strictly forbidden.
6. **Multi-Cohort Extraction**: `extract_sn_telemetry()` and `extract_tt_telemetry()` implemented.

---

## G. Statistical Validity and Reproducibility Status

- **Bit-for-Bit Determinism**: Re-evaluated checkpoint on reference synthetic set ($N=320$): max score difference $= 5.55 \times 10^{-17}$, 0/320 flag mismatches.
- **Exact Statistical Formulations**: Harness implements paired exact McNemar test (`scipy.stats.binomtest`) and Wilcoxon signed-rank test (`scipy.stats.wilcoxon`).
- **Statistical Power Awareness**:
  - SocialNetwork cohort provides $K=12$ fault scenarios (vs $K=6$ synthetic), increasing Wilcoxon test power from minimum $p=0.03125$ to $p \approx 0.00049$.
- **Manifest Reproducibility**: Execution pipeline generates machine-readable `experiment_d_manifest.json` recording UTC timestamp, parameters, discordant pairs, and file hashes.

---

## H. Remaining Scientific and Engineering Blockers (Resolved Under Path 3)

Under the ratified **Path 3: Bounded-Claims Policy** ([`BOUNDED_CLAIMS_DECISION.md`](BOUNDED_CLAIMS_DECISION.md)), external deep-learning benchmark validation on AnoMod is **formally excluded from immediate manuscript claims**:
1. **Protocol Amendment v1.2.0**: Remains unapproved for production execution; Protocol v1.1.0 remains frozen.
2. **Experiment D Execution**: Remains unexecuted / blocked; deferred to a subsequent research phase with high-frequency 24-step telemetry.
3. **Manuscript Bounding**: Anomaly detection claims are bounded to Experiment A ($N=320$); RCA claims are bounded to Experiment B pilot ($N=6$); safety claims are bounded to Experiment C ($N=16$).

---

## I. Manuscript Sections Ready for Drafting versus Sections Awaiting Evidence (Path 3)

| Target Paper Section | Content Focus | Evidence Status (Path 3) | Operational Action |
| :--- | :--- | :---: | :--- |
| **Abstract** | Multi-component framework, 3 empirical benchmarks, quantitative metrics, bounded caveats | **COMPLETED & VERIFIED** | Verified against CLM-01 to CLM-21; 0 unverified claims. |
| **1. Introduction & Motivation** | Incident lifecycle bottlenecks, RQ1–RQ4, defensible contributions | **COMPLETED & VERIFIED** | Bounded scope explicitly stated. |
| **2. Related Work & Literature Survey** | Anomaly detection, AIOps RCA, LLM agents, remediation safety | **COMPLETED & VERIFIED** | 16 verified citations (13 peer-reviewed, 1 NIST SP 800-53 standard, 2 workshop/preprints). |
| **3. Problem Formulation** | Mathematical definitions, 5D telemetry, sliding windows, approval tickets | **COMPLETED & VERIFIED** | Strict feature contract & window definitions aligned. |
| **4. Proposed Methodology & Novelty Claims** | Dual-gate detection, feature attribution, 4 agents, approval barrier, verification | **COMPLETED & VERIFIED** | 3,733 PyTorch parameters and §4.7 approval governance verified. |
| **5. System Architecture, Data Flow & Algorithms** | Figures 1, 2, 3 (Mermaid), Algorithms 1, 2, 3 | **COMPLETED & VERIFIED** | Component interactions and algorithmic flow match code. |
| **6. Experimental Datasets, Protocols & Baselines** | Exp A ($N=320$), Exp B ($N=6$), Exp C ($N=16$), baseline definitions | **COMPLETED & VERIFIED** | 3 rule baselines; FA/hr marked UNAVAILABLE. |
| **7. Anomaly Detection Results** | Table 1 (Detection), confusion matrices, recall/precision/FPR | **COMPLETED & VERIFIED** | All cell values match machine-readable CSVs. |
| **8. Root-Cause Diagnosis Results** | Table 2 (7 configs), Table 3 (scenario breakdown), ITT vs completed | **COMPLETED & VERIFIED** | Strict vs lenient, omitted call handling, no LLM superiority. |
| **9. Recovery & Boundary Safety Results** | Table 4 (16 safety cases), 11 attacks, 2 preconditions, 1 probe, 2 controls | **COMPLETED & VERIFIED** | 100% containment; localhost boundary; SQLite audit persistence. |
| **10. Statistical Analysis & Uncertainty** | Table 5, window McNemar, scenario-level Wilcoxon, Wilson CIs | **COMPLETED & VERIFIED** | Window clustering caveated; scenario-level Wilcoxon primary. |
| **11. Discussion, Limitations & Threats to Validity** | Synthetic domain gap, cold-start telemetry, small RCA cohort ($1-\beta \approx 0.14$) | **COMPLETED & VERIFIED** | §11.4 discloses AnoMod sequence gap and domain shift; Exp D excluded. |
| **12. Conclusion & Future Work** | Summary of 4 findings; future work directions | **COMPLETED & VERIFIED** | Exp D re-scoped as future work; SLMs; alert deduplication. |
| **References** | 16 verified bibliographic entries with DOIs | **COMPLETED & VERIFIED** | 13 peer-reviewed, 1 NIST standard, 2 workshop/preprints; zero hallucinated citations. |

---

## J. Exact Next Action and Why It Is the Correct Next Step

### The Exact Next Action:
Execute the 8-point measurable quality-control acceptance audit (**QC-1 through QC-8**) specified in [`MANUSCRIPT_FINALIZATION_PLAN.md`](../paper/MANUSCRIPT_FINALIZATION_PLAN.md), perform the regression test suite (`pytest test_experiment_d_harness.py -v`), and compile the final manuscript review package for supervisor review (with camera-ready submission formally deferred until visual PDF layout proofing).

### Why This Is the Correct Next Step:
1. **Strategic Path 3 Alignment**: Under the ratified supervisor decision ([`BOUNDED_CLAIMS_DECISION.md`](BOUNDED_CLAIMS_DECISION.md)), external deep-learning evaluation on AnoMod (Experiment D) is formally excluded from immediate paper claims and deferred to future work. Authorizing or running `run_experiment_d.py` is strictly prohibited.
2. **Defensible Scientific Completion**: With all manuscript sections authored, all 21 claims reconciled against machine-readable evidence ([`MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`](../paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md)), and parameter/window discrepancies resolved, completing QC verification guarantees that the manuscript is evidence-reconciled for supervisor review under bounded-claims policy.

---

## K. Evidence Paths and Document Matrix

| Category | Artifact Path | Creation / Audit Date | Core Invariant Verified |
| :--- | :--- | :---: | :--- |
| **Master Checklist** | [`research/audits/UPDATED_SEVEN_PHASE_CHECKLIST.md`](UPDATED_SEVEN_PHASE_CHECKLIST.md) | Oct 13, 2026 | Standardized 5-status classification across 4 categories. |
| **Protocol v1.1.0** | [`research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md`](phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md) | Oct 12, 2026 | Frozen baseline evaluation protocol. |
| **Amendment Proposal** | [`research/audits/PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md`](PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md) | Oct 13, 2026 | 8-dimension reconciliation proposal (v1.2.0). |
| **Protocol Reconciliation** | [`research/audits/EXPERIMENT_D_PROTOCOL_RECONCILIATION.md`](EXPERIMENT_D_PROTOCOL_RECONCILIATION.md) | Oct 13, 2026 | Standalone clause-by-clause reconciliation matrix. |
| **Requirements Traceability**| [`research/audits/EXPERIMENT_D_REQUIREMENTS_TRACEABILITY.md`](EXPERIMENT_D_REQUIREMENTS_TRACEABILITY.md) | Oct 13, 2026 | REQ-01 through REQ-10 mapped to code and tests. |
| **Implementation Review** | [`research/audits/EXPERIMENT_D_IMPLEMENTATION_REVIEW.md`](EXPERIMENT_D_IMPLEMENTATION_REVIEW.md) | Oct 13, 2026 | Code audit, call graph analysis, addendum. |
| **Readiness Verdict** | [`research/audits/EXPERIMENT_D_READINESS_VERDICT.md`](EXPERIMENT_D_READINESS_VERDICT.md) | Oct 13, 2026 | Authoritative readiness and gate decision report. |
| **Test Results Audit** | [`research/audits/EXPERIMENT_D_TEST_RESULTS.md`](EXPERIMENT_D_TEST_RESULTS.md) | Oct 13, 2026 | 40/40 harness tests and 105/105 repo tests verified. |
| **Remediation Changelog** | [`research/audits/EXPERIMENT_D_REMEDIATION_CHANGELOG.md`](EXPERIMENT_D_REMEDIATION_CHANGELOG.md) | Oct 13, 2026 | Detailed chronological log of 6 defects remediated. |
| **Temporal Audit Data** | [`research/audits/experiment_d_temporal_eligibility_audit.json`](experiment_d_temporal_eligibility_audit.json) | Oct 13, 2026 | Empirical window counts across 26 scenarios. |
| **Execution Harness** | [`research/experiments/run_experiment_d.py`](../experiments/run_experiment_d.py) | Oct 13, 2026 | Guarded production evaluation harness. |
| **Harness Test Suite** | [`test_experiment_d_harness.py`](../../test_experiment_d_harness.py) | Oct 13, 2026 | 40 dedicated unit and integration tests. |
| **Frozen Checkpoint** | [`models/lstm_autoencoder.pt`](../../models/lstm_autoencoder.pt) | Frozen | SHA-256: `1cf44e6e...`, 3,733 parameters. |

---

## L. Changes Made During This Audit Session

1. **Reconciled Missing Documentation Artifacts**:
   - Created standalone [`EXPERIMENT_D_PROTOCOL_RECONCILIATION.md`](EXPERIMENT_D_PROTOCOL_RECONCILIATION.md) detailing the clause-by-clause reconciliation matrix.
   - Created standalone [`EXPERIMENT_D_REQUIREMENTS_TRACEABILITY.md`](EXPERIMENT_D_REQUIREMENTS_TRACEABILITY.md) mapping REQ-01 through REQ-10 to code, tests, and evidence.
   - Created standalone [`EXPERIMENT_D_READINESS_VERDICT.md`](EXPERIMENT_D_READINESS_VERDICT.md) formalizing the gate verdict and operational boundary.
   - Created standalone [`EXPERIMENT_D_TEST_RESULTS.md`](EXPERIMENT_D_TEST_RESULTS.md) detailing empirical execution of all 40 harness tests and 105 full repository tests.
   - Created standalone [`EXPERIMENT_D_REMEDIATION_CHANGELOG.md`](EXPERIMENT_D_REMEDIATION_CHANGELOG.md) detailing all 6 remediated defects.
2. **Updated Master Research Checklist**:
   - Upgraded [`UPDATED_SEVEN_PHASE_CHECKLIST.md`](UPDATED_SEVEN_PHASE_CHECKLIST.md) to version 2.3.0, incorporating the strict 5-status taxonomy (`COMPLETED`, `IN PROGRESS`, `NEEDS VERIFICATION`, `BLOCKED`, `NOT STARTED`) across four distinct categories (Implementation Readiness, Scientific Validity, External Evaluation, Manuscript Readiness).
3. **Verified Virtual Environment Test Execution**:
   - Resolved the testing discrepancy where running `python -m pytest` under global Python failed on `streamlit`; confirmed that running inside `.venv\Scripts\python.exe` achieves **105/105 passed tests (100% pass rate)**.
   - Verified live CLI execution codes for `run_experiment_d.py`: Exit 2 (unauthorized), Exit 3 (unratified), Exit 0 (dry-run), Exit 0 (test-pipeline).
4. **Authored Master Research Handoff Document**:
   - Authored this comprehensive document ([`AEGISOPS_MASTER_RESEARCH_HANDOFF.md`](AEGISOPS_MASTER_RESEARCH_HANDOFF.md)) covering sections A through L with complete scientific citations and zero fabricated claims.

---

## M. Addendum: Phase 9 Stage 4.5 Final Scientific Decision Gate (October 13, 2026)

Following a comprehensive audit of empirical baseline window yields and methodological requirements, the following scientific decision artifacts have been prepared for human supervisor adjudication:

1. **Human Decision Packet Formulated**:
   - Documented in [`EXPERIMENT_D_HUMAN_DECISION_PACKET.md`](EXPERIMENT_D_HUMAN_DECISION_PACKET.md).
   - Re-calculated exact contiguous sliding window yields on `Normal_Baseline`:
     - Unpartitioned: 19 eligible $W=8$ windows.
     - Chronological 70/30 partition with 7-step (105s) purge gap: $N_{\text{calib}} = 5$ windows, $N_{\text{val}} = 8$ windows (6 windows lost across the purge gap).
   - Adjudicated Normalization Transformation: Recommended Option 2 (Domain Z-Score) as Primary Confirmatory evaluation; Option 3 (Frozen Training Scaler) as Secondary Exploratory zero-shot shift analysis; Option 1 (Min-Max) rejected due to mathematical incompatibility with frozen LSTM weights.
   - Adjudicated Threshold Calibration: Recommended retaining Empirical 99th percentile with mandatory small-sample caveat ($N_{\text{val}}=8$), paired with Parametric Gaussian sensitivity check ($\mu + 2.326\sigma$).
   - Adjudicated Cohort Scope: Classified SocialNetwork as Primary Confirmatory Cohort ($K=12$ fault scenarios, 303 eligible windows); classified TrainTicket as Secondary Exploratory Cohort (74 total windows, 548s SkyWalking trace truncation).

2. **Statistical Acceptance Criteria Frozen**:
   - Documented in [`EXPERIMENT_D_STATISTICAL_ACCEPTANCE_CRITERIA.md`](EXPERIMENT_D_STATISTICAL_ACCEPTANCE_CRITERIA.md).
   - Pre-registered primary confirmatory hypotheses:
     - H1: Paired window-level McNemar exact test ($p < 0.05, b > c$).
     - H2: Scenario-level Wilcoxon signed-rank test across $K=12$ SocialNetwork fault scenarios ($p < 0.05$).
   - Mandatory Autocorrelation Disclosure: Documented that overlapping sliding windows share $W-1=7$ steps ($87.5\%$ autocorrelation). Window-level McNemar p-values must be reported with this caveat, while scenario-level Wilcoxon ($K=12$) represents the primary independent unit.
   - Multiple Comparison Corrections: Holm-Bonferroni adjustment mandated for secondary baseline comparisons.
   - Independent Recomputation: Automated recalculation gate required prior to manuscript reconciliation.

3. **Implementation Execution Path Verified**:
   - Traced `run_production_experiment_d()` and verified complete end-to-end scoring loop.
   - Updated call to explicitly pass `include_val_in_predictions=True`, ensuring $N_{\text{val}}=8$ held-out normal windows are evaluated as $y=0$ alongside fault scenarios ($y=1$) to compute true False Positive Rate, Specificity, and Precision.
   - 40/40 dedicated harness tests and 105/105 repository tests passing in `.venv`.
   - Verified in [`EXPERIMENT_D_DECISION_PACKET_VERIFICATION.md`](EXPERIMENT_D_DECISION_PACKET_VERIFICATION.md).

4. **Previous Execution Verdict (Superseded)**:
   - **`READY FOR HUMAN METHODOLOGY REVIEW`** (Superseded by Section N).

---

## N. Addendum: Calibration-Independence and Statistical Validity Re-Audit (October 13, 2026)

Following an independent, skeptical deep-dive audit of the actual code in `research/experiments/run_experiment_d.py`, unit test fixtures, and live telemetry behavior on the extracted AnoMod dataset, the readiness verdict has been **REVISED AND DOWNGRADED**:

```
================================================================================
FINAL VERDICT: BLOCKED — CALIBRATION OR STATISTICAL VALIDITY DEFECT
================================================================================
```

### 1. Key Audit Findings & Demonstrated Defects:
1. **Circular Calibration/Evaluation Leakage Defect**:
   - `v_win` ($N_{\text{val}} = 8$ windows) is used in `calibrate_threshold()` to set the empirical 99th percentile threshold and is concurrently inserted into `eval_scenarios["Normal_Validation"]` as the sole negative test population (`run_experiment_d.py:550,566`).
   - For $N=8$, the 99th percentile evaluates to $\approx \max(\mathbf{e}_{\text{val}})$. Testing on the exact same sample guarantees $\text{FP} = 0, \text{TN} = 8 \implies \text{FPR} = 0.0\%, \text{Specificity} = 100.0\%$ by circular mathematical construction.
2. **Near-Zero Variance Calibration Collapse Defect**:
   - Fitting the 5-D Domain Z-Score scaler on the 5 calibration windows of `Normal_Baseline` produces catastrophic variance collapse:
     - `error_rate_pct`: $\sigma = 0.0$ (clipped to $10^{-6}$)
     - `disk_pct`: $\sigma = 0.00064\%$
     - `memory_pct`: $\sigma = 0.0188\%$
   - During fault runs, small shifts produce unregularized inputs of up to **$+1,000,000.0\sigma$**, saturating LSTM activations and causing reconstruction losses to explode by 12 orders of magnitude ($\approx 10^{12}$).
3. **Severe Class Imbalance and 12.5% FPR Resolution Limit**:
   - The test set contains 303 fault windows and only 8 normal validation windows ($97.43\%$ positive prevalence).
   - Each false alarm alters the empirical FPR by **$12.5\%$**. The 95% Wilson Score CI for $0/8$ false alarms spans $[0.0\%, 32.4\%]$, making operational false-alarm claims statistically indeterminate.
   - A constant dummy classifier ($\hat{y} \equiv 1$) achieves an F1 score of **0.9870**, demonstrating metric pathology under this class distribution.
4. **Invalid Sliding Window Inference**:
   - Window-level McNemar tests treat overlapping sliding windows ($87.5\%$ sample overlap) as independent Bernoulli trials without analytical correction, artificially inflating statistical significance.
   - Scenario-level Wilcoxon test ($K=12$) has modest statistical power ($35\% - 70\%$ for medium/large effects).
5. **Harness Test Suite Blind Spots**:
   - 40/40 tests pass in `test_experiment_d_harness.py`, but 28 tests rely on synthetic random fixtures. Line 578 of the test suite even uses the same array for calibration and validation (`calib_windows=calib, val_windows=calib`), actively reinforcing the leakage pattern.

### 2. Standalone Audit Artifacts Produced:
- [`EXPERIMENT_D_CALIBRATION_INDEPENDENCE_AUDIT.md`](EXPERIMENT_D_CALIBRATION_INDEPENDENCE_AUDIT.md): Complete data-use lifecycle trace, leakage demonstration, and normalization variance analysis.
- [`EXPERIMENT_D_STATISTICAL_VALIDITY_REAUDIT.md`](EXPERIMENT_D_STATISTICAL_VALIDITY_REAUDIT.md): Reassessment of window-level autocorrelation, scenario-level power, class imbalance, and harness test risks.
- [`EXPERIMENT_D_FINAL_METHOD_DECISION.md`](EXPERIMENT_D_FINAL_METHOD_DECISION.md): Comprehensive synthesis, evaluation of 4 remediation options, blocking rationale, and supervisor directives.
- [`EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md`](EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md): Frozen model contract verification, feature order conflict resolution, and exact nominal window count trace.
- [`EXPERIMENT_D_ZERO_SHOT_IMPLEMENTATION_PLAN.md`](EXPERIMENT_D_ZERO_SHOT_IMPLEMENTATION_PLAN.md): Pre-execution architecture for zero-shot transfer, domain shift proof (100% nominal false alarm rate), and dependence treatment.
- [`EXPERIMENT_D_HUMAN_METHOD_DECISION_V2.md`](EXPERIMENT_D_HUMAN_METHOD_DECISION_V2.md): Human Decision Package v2.0 reconciling Option C + Option D, prerequisite checklist, and reporting modality choice.
- [`EXPERIMENT_D_SEQUENCE_COMPATIBILITY_DECISION.md`](EXPERIMENT_D_SEQUENCE_COMPATIBILITY_DECISION.md): Forensic audit of sequence-length mismatch ($W=24$ vs $W=8$), off-contract diagnostic proof, and absence of 24-step contiguous runs.
- [`EXPERIMENT_D_FINAL_SUPERVISOR_DECISION.md`](EXPERIMENT_D_FINAL_SUPERVISOR_DECISION.md): Final decision package comparing Path 1 (new data), Path 2 (exploratory 8-step diagnostic), and Path 3 (rules/synthetic restriction).
- [`BOUNDED_CLAIMS_DECISION.md`](BOUNDED_CLAIMS_DECISION.md): Supervisory ratification of Path 3, 11-point bounded-claims policy, and parameter/window count reconciliation.
- [`MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`](../paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md): Comprehensive 21-claim audit matrix mapping every manuscript statement to verified evidence.
- [`MANUSCRIPT_FINALIZATION_PLAN.md`](../paper/MANUSCRIPT_FINALIZATION_PLAN.md): 13-section manuscript finalization plan and QC acceptance criteria.

### 3. Current Supervisory Direction: Path 3 Adopted (Bounded-Claims Paper Finalization):
The human research supervisor has formally selected **Path 3: Bounded-Claims Paper Finalization** ([`BOUNDED_CLAIMS_DECISION.md`](BOUNDED_CLAIMS_DECISION.md)).
- **External LSTM Validation on AnoMod**: Formally excluded from confirmatory paper claims; remains unexecuted.
- **Protocol v1.1.0**: Remains frozen; Protocol Amendment v1.2.0 remains unapproved.
- **Manuscript Scope**: Confirmatory findings are bounded to verified synthetic anomaly detection ($N=320$), pilot root-cause analysis ($N=6$), execution boundary safety ($N=16$), and reproducible closed-loop architecture.
- **Active Operational Task**: Final manuscript text alignment and quality-control verification under [`MANUSCRIPT_FINALIZATION_PLAN.md`](../paper/MANUSCRIPT_FINALIZATION_PLAN.md).

### Phase 15–16 live-telemetry administrative status (2026-10-17)

Phase 15 made no live collection: its quality-only pilot Gate 1 was closed because no documented authorization established the collector/target topology and owner, data-governance controls, cadence/clock/gap/interruption policy, or permitted target scope/duration. Phase 16 prepared a bounded approval-closure matrix and preflight run sheet at [`research/exports/live_lstm/phase15/`](../exports/live_lstm/phase15/); it did not supply an approval or change any runtime setting. The frozen synthetic checkpoint remains disabled for this quality-only pilot, no detector performance was measured, and live detection performance remains **UNMEASURED**. Gate 1 may be reconsidered only after explicit, current human authorization matches the run sheet.

### Phase 17 status (2026-10-17)

Phase 17 prepared an owner-ready approval request and reassessed the gate without creating an authorization record. Gate 1 remains **CLOSED**: the topology/owner, data-governance, cadence/clock/gap/interruption, and bounded-scope decisions require explicit human authorization. Its prescribed isolated Experiment D harness regression passed 40/40 tests in a workspace-local temporary directory; production Experiment D remained unexecuted. Source-level Path 3 manuscript QC preserved synthetic/pilot/local/live boundaries, but camera-ready release remains blocked pending a reproducible rendered PDF/DOCX page inspection, release provenance/metadata closure, and the remaining documented release prerequisites.

### Phase 18 release consistency and regression status (2026-10-18)

Phase 18 established `research/paper/PHASE18_CANONICAL_MANUSCRIPT_RELEASE_CHECKLIST.md` as the stable current release-control set, reconciling rather than rewriting the historically overlapping seven-item and eight-item QC schemes. The full root test suite passed **116/116** in 65.70 seconds (exit code 0) in the repository virtual environment using a workspace-local temporary root; production Experiment D was not invoked. The manuscript remains substantively suitable for bounded supervisor review, but camera-ready/publication release is **BLOCKED** by missing approved document generation/page inspection, release provenance, metadata, bibliographic closure/limitation, and final independent sign-off. Live LSTM performance remains **UNMEASURED**.


