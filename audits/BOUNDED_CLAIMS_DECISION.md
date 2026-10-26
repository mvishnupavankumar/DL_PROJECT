# AegisOps Research — Supervisory Decision: Bounded-Claims Paper Finalization (Path 3)

**Document Identifier**: `AEGISOPS-SUPERVISORY-DECISION-PATH-3`  
**Date**: October 13, 2026  
**Supervisory Authority**: Senior Research Supervisor, ML Systems Architect & Scientific Auditor  
**Repository**: `C:\DL_PROJECT`  
**Git HEAD**: `d277c1df3c2599ddecdf5f0bb761c99718499667`  
**Decision Gate Status**: **RATIFIED & ACTIVE (PATH 3 ADOPTED)**  
**Production Experiment D Status**: **FORMALLY EXCLUDED FROM IMMEDIATE PAPER CLAIMS (REMAINS BLOCKED)**  

---

## 1. Context and Strategic Decision

Following the comprehensive forensic audits of the frozen model contract ([`EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md`](file:///c:/DL_PROJECT/research/audits/EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md)) and the sequence-length compatibility review ([`EXPERIMENT_D_SEQUENCE_COMPATIBILITY_DECISION.md`](file:///c:/DL_PROJECT/research/audits/EXPERIMENT_D_SEQUENCE_COMPATIBILITY_DECISION.md)), the project faced three potential trajectories:
- **Path 1**: Acquire new external telemetry supporting contiguous 24-step sequences (suspends paper completion).
- **Path 2**: Formally amend the evaluation protocol to ratify an off-contract 8-step diagnostic.
- **Path 3**: Finalize the current manuscript using **bounded, evidence-supported claims**, restricting empirical assertions to verified synthetic, pilot, and security evaluations, and leaving broader external benchmark execution to a subsequent research phase.

### Formal Supervisory Decision:
The research supervisor has formally selected **Path 3: Bounded-Claims Paper Finalization**.

Our immediate priority is to complete a scientifically unassailable, peer-review-ready research paper efficiently. This decision establishes strict claim boundaries, protects scientific integrity, eliminates speculative claims of external cross-domain generalization, and prevents research stagnation.

---

## 2. Mandatory Bounded-Claims Policy

The following 11 policy rules govern all writing, data reporting, tables, and figures in [`research/paper/AEGISOPS_RESEARCH_PAPER.md`](file:///c:/DL_PROJECT/research/paper/AEGISOPS_RESEARCH_PAPER.md):

1. **Synthetic Anomaly Detection Bounding**:
   - The anomaly detection findings for the LSTM Autoencoder ($100.0\%$ recall, $1.0\%$ FPR) and Isolation Forest ($47.5\%$ recall, $2.0\%$ FPR) must be reported **strictly as results from the evaluated synthetic benchmark ($N=320$ windows)** and its documented mathematical configuration.
   - Prohibit claiming that this demonstrates zero misses or operational readiness on production enterprise microservices.
2. **Root-Cause Analysis Bounded as Pilot Evaluation**:
   - Report the Multi-Agent LLM diagnostic evaluation strictly as an **exploratory pilot evaluation on the six canonical incident scenarios ($N=6$)**.
   - Preserve and document the exact scoring rubric, differentiating between Strict Match and Lenient Match criteria.
   - Disclose rubric keyword overlap and low statistical power ($1-\beta \approx 0.14$).
   - Explicitly report that deterministic rules achieved 100% strict accuracy ($6/6$) in $0.01\text{ ms}$, whereas the LLM achieved 83.33% ($5/6$) in $4.78\text{ s}$. Prohibit claiming LLM superiority over rules.
3. **Remediation Safety Bounded to Tested Scope**:
   - Report remediation execution boundary containment ($100\%$ containment, 11/11 attacks blocked) strictly for the **tested 16 cases and localhost / loopback HTTP runtime scope (`127.0.0.1:8765`)**.
   - Do not claim defense against OS kernel exploitation, physical hypervisor compromise, or malicious cloud control planes.
4. **Strict Grounding of Reproducibility Evidence**:
   - Describe reproducibility evidence only to the extent directly substantiated by verifiable logs, manifests, cryptographic SHA-256 hashes, and executed test suites.
5. **Exclusion of External LSTM Validation on AnoMod**:
   - Do **NOT** claim successful external deep learning validation on AnoMod.
   - State transparently that the frozen model contract expects 24-step sequences ($W=24$), whereas the available external Prometheus/trace data contains trace dropouts that yield zero contiguous 24-step windows without unapproved synthetic interpolation.
6. **No Confirmatory Use of the 8-Step Harness**:
   - Do **NOT** treat the $W=8$ direct-model harness, its reconstruction scores, or its nominal false-alarm results as valid confirmatory performance evidence for the frozen $W=24$ detector.
   - The $+41.8\%$ score inflation and off-contract status must be documented as an exploratory domain-transfer diagnostic limitation.
7. **Zero Calibration Leakage Acceptance**:
   - Do **NOT** present threshold calibration or normalization fitting performed on the same data used for evaluation as independent validation.
8. **Strict Accounting for Temporal Dependence**:
   - Do **NOT** treat overlapping sliding windows as independent observations ($87.5\%$ data overlap).
   - Reassess all window-level hypothesis tests (e.g., McNemar's test) as descriptive diagnostics, and report paired scenario-level non-parametric tests ($N=6$ or $N=12$) as primary inferential statistics.
   - Mark operational False Alarms per Hour as **UNAVAILABLE**.
9. **No Unsubstantiated System Superiority Claims**:
   - Prohibit claiming that the integrated AegisOps system is superior to existing state-of-the-art commercial or academic systems unless supported by a direct, head-to-head empirical baseline.
10. **Novelty Defined as Architecture and Workflow Integration**:
    - Characterize the novelty of AegisOps as an **end-to-end integration and closed-loop workflow contribution**—connecting unsupervised deep-learning detection attribution, multi-agent LLM reasoning, atomic Two-Man Rule authorization barriers, and post-remediation loopback probe verification.
11. **Clear Epistemic Categorization**:
    - The manuscript must explicitly distinguish:
      - **Completed & Verified Experiments**: Experiments A, B, and C.
      - **Exploratory Pilot Findings**: LLM diagnostic trade-offs and domain-transfer diagnostics.
      - **Blocked / Deferred Investigations**: Experiment D external benchmark on AnoMod.
      - **Future Work**: Acquiring high-frequency 24-step microservice telemetry, streaming alert deduplication, and on-premise SLMs.

---

## 3. Discrepancy Resolution & Audit Log

### 3.1 Model Parameter Count Discrepancy
- **Documented in Prior Reports**: 3,605 parameters.
- **Actual PyTorch Parameters**: **3,733 parameters** (`sum(p.numel() for p in model.parameters()) = 3733`).
- **Audit Explanation**:
  - In theoretical textbook formulations, LSTM gates share a single bias vector ($4 \times H = 64$ parameters per layer).
    - Encoder: $4 \times 16 \times 5 + 4 \times 16 \times 16 + 64 = 1,408$
    - Decoder: $4 \times 16 \times 16 + 4 \times 16 \times 16 + 64 = 2,112$
    - Linear: $5 \times 16 + 5 = 85$
    - Theoretical Total = $1,408 + 2,112 + 85 = \mathbf{3,605}\text{ parameters}$.
  - PyTorch's `nn.LSTM(bias=True)` allocates separate input-to-hidden (`bias_ih`) and hidden-to-hidden (`bias_hh`) bias vectors ($2 \times 64 = 128$ extra parameters across encoder and decoder).
  - Actual PyTorch Total = $3,605 + 128 = \mathbf{3,733}\text{ parameters}$.
- **Resolution**: All manuscript references must cite the exact PyTorch implementation parameter count: **3,733 parameters** (3.7k parameters).

### 3.2 Nominal Validation-Window Count Discrepancy
- **Documented Historical Range**: ~2 windows, $\le 5$ windows, 8 windows, 19 windows.
- **Audit Explanation**:
  - The raw SocialNetwork `Normal_Baseline` sequence contains 80 grid points ($15\text{s}$ interval, 20 minutes total), with 23 missing trace intervals, leaving 57 complete points clustered into 3 runs (lengths 11, 11, 18).
  - Total eligible $W=8$ sliding windows across the full run = $4 + 4 + 11 = \mathbf{19\text{ windows}}$.
  - The historical "~2 validation windows" arose from analytical estimates assuming partitioning cleaned complete rows ($57 \times 0.25 = 14$ rows, minus 7 purge steps leaves 7 rows $< 8 \implies 0$ to 1 window).
  - The "8 validation windows" reflects actual execution of `partition_normal_series_chronologically(df_normal, train_fraction=0.70, purge_gap_steps=7)` on raw 80 rows, where rows 63..79 contain 15 contiguous valid rows ($15 - 8 + 1 = \mathbf{8\text{ windows}}$).
  - All 8 validation windows share 87.5% overlap across a single 3.5-minute sequence from one run.
  - For $W=24$: exactly **0 eligible windows** exist.
- **Resolution**: This accounting is permanently recorded in [`EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md`](file:///c:/DL_PROJECT/research/audits/EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md). In the paper, Experiment D is excluded from confirmatory claims, eliminating any exposure to this small-sample variance.

---

## 4. Current Project State & Operational Directives

- **Git HEAD**: `d277c1df3c2599ddecdf5f0bb761c99718499667`
- **Experiment D Execution**: Remains **STRICTLY BLOCKED** (unauthorized, no production outputs generated).
- **Protocol v1.1.0**: Remains frozen.
- **Protocol Amendment v1.2.0**: Remains unapproved for production execution.
- **Next Operational Phase**: Audit manuscript claims against evidence ([`MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md`](file:///c:/DL_PROJECT/research/paper/MANUSCRIPT_CLAIM_EVIDENCE_MATRIX.md)) and execute the finalization plan ([`MANUSCRIPT_FINALIZATION_PLAN.md`](file:///c:/DL_PROJECT/research/paper/MANUSCRIPT_FINALIZATION_PLAN.md)).
