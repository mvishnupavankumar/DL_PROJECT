# AegisOps: Canonical Metric Reconciliation and Handoff Consistency Audit

**Document Identifier**: `AEGISOPS-CANONICAL-METRIC-RECONCILIATION`  
**Date**: October 14, 2026  
**Auditor**: Senior ML Research Supervisor, Statistical Auditor & Reproducibility Reviewer  
**Repository**: `C:\DL_PROJECT` (Current Branch: `publish/research-without-external-dataset`, Git HEAD: `a32713c30a8ddca1425d44b1afbaf6d55a64c276`)  
**Frozen Model Checkpoint**: `models/lstm_autoencoder.pt` (SHA-256: `1cf44e6e82e459f543fcace25334f3076b76c77a357d46f65c11e3c44fd382de`)  
**Frozen Detection Threshold**: $\tau = 0.7093990445137024$ (99th percentile on $N=150$ held-out nominal validation sequences)  
**Status**: Authoritative Canonical Source of Truth  

---

## 1. Executive Summary & Audit Mandate

This document establishes the definitive, mathematically verified reconciliation of all experimental metrics, statistical tests, configuration taxonomies, and historical records across the AegisOps research project. 

Prior narrative summaries and draft reports contained transcription inconsistencies, misattributed author names, conflated rubric tiers, and historical label drift. Every metric reported below has been independently recomputed directly from the primary machine-readable records (`research/raw/detection_predictions.csv`, `research/raw/diagnosis_predictions.csv`, `research/raw/safety_test_results.csv`, `research/raw/diagnosis_metrics.csv`, and `models/lstm_autoencoder.json`).

---

## 2. Primary Input Files Inspected

| Artifact Path | Record Type | Observations ($N$) | SHA-256 / Verification Status |
| :--- | :--- | :---: | :--- |
| `models/lstm_autoencoder.pt` | PyTorch Weights | 3,733 params | `1cf44e6e82e459f543fcace25334f3076b76c77a357d46f65c11e3c44fd382de` (Invariant) |
| `models/lstm_autoencoder.json` | Model Metadata | $\tau = 0.709399$ | Calibrated on $N=150$ held-out nominal validation sequences (`seed=42`) |
| `research/raw/detection_predictions.csv` | Window Predictions | $N = 320$ windows | 200 normal steady-state, 120 fault episodes across 6 scenarios (Bit-for-bit preserved) |
| `research/raw/detection_metrics.csv` | Anomaly Metrics | 4 models | Summary metrics for Rules, Isolation Forest, LSTM AE, and Combined |
| `research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv` | Granular Metrics | 6 baselines | Full disaggregation of Narrow, Resource-Only, Full Operational Rules, IF, LSTM |
| `research/raw/diagnosis_predictions.csv` | Diagnosis Predictions | 42 evaluations | 7 configurations $\times$ 6 canonical scenarios (rubric-annotated) |
| `research/raw/diagnosis_metrics.csv` | Diagnosis Metrics | 7 configurations | ITT, completed-case, strict, and lenient accuracies with valid completed latencies |
| `research/raw/safety_test_results.csv` | Safety Boundary Log | 16 test cases | 11 attacks, 2 precondition checks, 1 probe, 2 positive controls |
| `research/raw/safety_metrics.csv` | Safety Metric Rollup | 8 indicators | Containment rate, check latency, audit completeness |

> [!NOTE]
> **Manifest Comparison & Audit Provenance Distinction**:
> An exhaustive read-only verification of all 22 artifacts covered by `research/MANIFEST_SHA256.json` reveals that 17 artifacts match bit-for-bit (including `models/lstm_autoencoder.pt`, `models/lstm_autoencoder.json`, and `research/raw/detection_predictions.csv`). 
> Five artifacts differ from the pre-reconciliation manifest: `research/SAFETY_EVALUATION.md`, `research/raw/diagnosis_predictions.csv`, `research/raw/diagnosis_metrics.csv`, `research/raw/safety_test_results.csv`, and `research/raw/safety_metrics.csv`.
> These differences do not represent corruption; they document the deliberate, audited reconciliation of Phase 4 and Phase 5 results:
> 1. In `diagnosis_predictions.csv`, omitted API calls (rows 25 & 39) were accurately reclassified from `INCORRECT` to `UNASSESSABLE`, updating completed-case strict accuracy from 66.67% to 80.00% and isolating valid call latencies.
> 2. In `safety_test_results.csv`, test cases `TC-FAIL-01`, `TC-FAIL-02`, and `TC-VERIF-01` were properly categorized as precondition checks and verification probes rather than adversarial attacks, adjusting the true attack cohort denominator from 14 to 11 (with 100% containment, 95% Wilson CI $[0.7412, 1.0000]$) and separating attack check latency (11.32 ms) from probe verification latency.
> 3. Rather than claiming universal bit-for-bit preservation across all raw tables, the repository explicitly distinguishes historical experimental observations (e.g., detection predictions) from audited classifications and recomputed metrics.

---

## 3. Experiment A: Canonical Detection Metrics and Statistical Recomputation

### 3.1 Authoritative Confusion Matrices and Performance Metrics ($N = 320$ Windows)

Evaluated across 200 normal steady-state windows and 120 fault episode windows:

| Detection Method | True Positive (TP) | False Positive (FP) | True Negative (TN) | False Negative (FN) | Recall (Sensitivity) | Precision | False Positive Rate (FPR) | Specificity | F1-Score | PR-AUC | Latency (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Narrow Rules** (historical comparator; not independently recalculated from current raw predictions) | 40 | 0 | 200 | 80 | **33.33%** ($40/120$) | 100.00% | 0.00% | 100.00% | 0.5000 | UNAVAILABLE | 0.01 |
| **Resource-Only Rules** (historical comparator; not independently recalculated from current raw predictions) | 80 | 0 | 200 | 40 | **66.67%** ($80/120$) | 100.00% | 0.00% | 100.00% | 0.8000 | UNAVAILABLE | 0.01 |
| **Full Operational Rules** (+ error $\ge$ 0.5%) | 120 | 0 | 200 | 0 | **100.00%** ($120/120$)* | 100.00% | 0.00% | 100.00% | 1.0000 | UNAVAILABLE | 0.01 |
| **Isolation Forest** ($\tau = -0.018694$) | 57 | 4 | 196 | 63 | **47.50%** ($57/120$) | 93.44% | 2.00% | 98.00% | 0.6298 | 0.9056 | 1.84 |
| **LSTM Autoencoder** ($\tau = 0.709399$) | 120 | 2 | 198 | 0 | **100.00%** ($120/120$) | 98.36% | 1.00% | 99.00% | 0.9917 | 1.0000 | 0.17 |
| **Combined Alert** (Rules $\lor$ LSTM) | 120 | 2 | 198 | 0 | **100.00%** ($120/120$) | 98.36% | 1.00% | 99.00% | 0.9917 | N/A | 0.18 |

*\*Note on Full Operational Rules Recall*: The 100.0% recall of Full Operational Rules is directly affected by structural overlap between the synthetic simulator's injected HTTP error-rate predicate ($> 0.5\%$) across all six incident classes and the rule's matching threshold ($x_t^{(\text{err})} > 0.5\%$). In real-world enterprise infrastructure where microservices degrade internally without immediately emitting HTTP probe errors, physical resource rules (Narrow: 33.33%, Resource-Only: 66.67%) fail to match deep learning sensitivity.

*PR-AUC correction (2026-10-14)*: `research/exports/FINAL_RAW_CSV_RECALCULATION.txt` independently applied the documented runner method—`precision_recall_curve` followed by trapezoidal `auc(recall, precision)`—to `lstm_score`. The current raw reconstruction-error rows yield 1.0000; average precision is also 1.0000 but remains a distinct statistic. The prior 0.9998 value is not reproducible from the current score table and is retired. Rules retain `UNAVAILABLE` in this comparative table because their binary flags are not comparable continuous rankings, although the historical runner mechanically emitted 1.0 from binary scores. Narrow and Resource-Only values remain historical granular-audit outputs because the current prediction CSV lacks their flags.

### 3.2 Paired Contingency Table & Statistical Test Recomputation

Paired contingency on the 120 incident episodes between LSTM Autoencoder and Isolation Forest:
* $a = 57$ (both detected)
* $b = 63$ (LSTM detected, Isolation Forest missed)
* $c = 0$ (Isolation Forest detected, LSTM missed)
* $d = 0$ (both missed)

#### Statistical Test Outputs:
1. **Exact Binomial McNemar Test**:
   $$p = 2 \times (0.5)^{63} \approx 2.168404 \times 10^{-19}$$
2. **Edwards Continuity-Corrected $\chi^2$ Statistic**:
   $$\chi^2_{\text{continuity}} = \frac{(|b - c| - 1)^2}{b + c} = \frac{(|63 - 0| - 1)^2}{63} = \frac{62^2}{63} = \frac{3844}{63} \approx 61.01587 \quad (p = 5.66 \times 10^{-15})$$
3. **Uncorrected $\chi^2$ Statistic**:
   $$\chi^2 = \frac{(b - c)^2}{b + c} = \frac{63^2}{63} = 63.0 \quad (p = 2.07 \times 10^{-15})$$
4. **Wald Paired Difference CI ($N = 120$)**:
   $$\Delta_{\text{Recall}} = \frac{63 - 0}{120} = +0.5250 \quad (\text{SE} \approx 0.0456), \quad 95\%\ \text{CI}: [+0.4357, +0.6143]$$
5. **Scenario-Level Paired Non-Parametric Analysis (Wilcoxon Signed-Rank Test Across Scenarios, $N = 6$)**:
   * Scenario sensitivities (LSTM vs IF):
     * INC-1001: $1.00$ vs $0.40 \implies \Delta = +0.60$
     * INC-1002: $1.00$ vs $0.25 \implies \Delta = +0.75$
     * INC-1003: $1.00$ vs $0.85 \implies \Delta = +0.15$
     * INC-1004: $1.00$ vs $0.75 \implies \Delta = +0.25$
     * INC-1005: $1.00$ vs $0.40 \implies \Delta = +0.60$
     * INC-1006: $1.00$ vs $0.20 \implies \Delta = +0.80$
   * All 6 differences strictly positive. Sum of negative ranks $W^- = 0.0$, positive ranks $W^+ = 21.0$.
   * Exact two-sided $p = 2 \times (0.5)^6 = 0.03125$.
   * *Methodological Scope*: This scenario-level paired analysis aggregates window sensitivities within each scenario archetype to eliminate intra-cluster replicate correlation across repeated synthetic episodes, rather than applying an econometric cluster-robust covariance adjustment.

### 3.3 Provenance and Audit of Historical Figures ("76.67%" and "78.036")
* **Isolation Forest Recall (76.67% vs Canonical 47.50%)**:
  * The figure `76.67%` was cited in earlier assistant progress summaries as an alleged Isolation Forest recall.
  * A repository-wide audit confirms that while the literal string `76.67%` appears in unrelated external benchmark documentation and traces (e.g., within commit `b6123a7` ingesting third-party dataset assets under `data/external/anomod/`), it never existed as an AegisOps detection result or script output.
  * The canonical machine-readable predictions (`detection_predictions.csv` and `CORRECTED_DETECTION_METRICS.csv`) record exactly **$57$ true positives out of $120$** incident windows: $57 / 120 = \mathbf{47.50\%}$.
  * We retain the conclusion that **47.50%** is the sole supported Isolation Forest recall on the AegisOps synthetic benchmark, and clearly distinguish the unrelated external-document string from the unsupported AegisOps recall claim.
* **McNemar Chi-Square Statistic ("78.036" vs Canonical 61.02 / 63.0)**:
  * The figure `78.036` was similarly reported in earlier assistant commentary.
  * Canonical commit history for `research/results/generate_statistical_analysis.py` and `research/results/statistical_analysis.md` back to baseline commit `a32713c...` demonstrates that the canonical code always computed $b=63, c=0 \implies \chi^2_{\text{continuity}} = (62)^2 / 63 = \mathbf{61.02}$ and uncorrected $\chi^2 = (63)^2 / 63 = \mathbf{63.0}$.
  * The value `78.036` is entirely unsupported by the canonical contingency table or any evaluation script in the repository; the authoritative, mathematically verified canonical metrics ($61.02$ continuity-corrected, $63.0$ uncorrected) are retained.

---

## 4. Experiment B: Canonical Root-Cause Diagnosis Outcomes

### 4.1 Authoritative 7-Configuration Taxonomy

From `research/raw/diagnosis_metrics.csv` and `research/raw/diagnosis_predictions.csv`:

| Config ID | Canonical Configuration Name | Execution Engine | DL Attribution Vector | Total ($N$) | Completed ($N$) | Omitted | Strict ITT ($N=6$) | Strict Completed | Lenient ITT ($N=6$) | Mean Completed Latency |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Config 1** | Rule-based Baseline | Deterministic Regex | No | 6 | 6 | 0 | **100.00%** ($6/6$) | **100.00%** ($6/6$) | **100.00%** ($6/6$) | **0.01 ms** |
| **Config 2** | Single-Agent (Offline) | Deterministic Heuristic | Yes | 6 | 6 | 0 | **50.00%** ($3/6$) | **50.00%** ($3/6$) | **50.00%** ($3/6$) | **0.03 ms** |
| **Config 3** | Multi-Agent Full (Offline) | Deterministic Heuristic + DL | Yes | 6 | 6 | 0 | **50.00%** ($3/6$) | **50.00%** ($3/6$) | **50.00%** ($3/6$) | **0.57 ms** |
| **Config 4** | Multi-Agent No-DL (Offline) | Deterministic Heuristic (Log-Only) | No | 6 | 6 | 0 | **100.00%** ($6/6$) | **100.00%** ($6/6$) | **100.00%** ($6/6$) | **0.11 ms** |
| **Config 5** | Single-Agent (Groq LLM) | Live API (`openai/gpt-oss-20b`) | Yes | 6 | 5 | 1 | **66.67%** ($4/6$) | **80.00%** ($4/5$) | **66.67%** ($4/6$) | **3,041.87 ms** (3.04 s) |
| **Config 6** | Multi-Agent Full (Groq LLM) | Live API (`openai/gpt-oss-20b`) + DL | Yes | 6 | 6 | 0 | **83.33%** ($5/6$) | **83.33%** ($5/6$) | **100.00%** ($6/6$) | **23,188.72 ms** (23.19 s) |
| **Config 7** | Multi-Agent No-DL (Groq LLM) | Live API (`openai/gpt-oss-20b`) (Log-Only) | No | 6 | 5 | 1 | **66.67%** ($4/6$) | **80.00%** ($4/5$) | **83.33%** ($5/6$) | **19,279.69 ms** (19.28 s) |

### 4.2 Resolution of Strict vs. Lenient Accuracy for Config 6
* In Config 6, the live LLM correctly diagnosed 5 scenarios strictly (INC-1001, 1003, 1004, 1005, 1006).
* On **INC-1002** (Database service stopped), the LLM diagnosed "PostgreSQL service crashed due to abnormal disk I/O contention". Under the explicit rubric (`generate_diagnosis_audit.py`):
  * Strict match = $0$ (hallucinated disk I/O contention as cause).
  * Lenient match = $1$ (identified database crash/outage domain).
* Therefore:
  * **Strict Accuracy = 83.33% (5/6)**.
  * **Lenient Accuracy = 100.00% (6/6)**.
  * Any claim of "100% accuracy" for Config 6 represents **lenient** scoring only and must never be presented as strict accuracy.

### 4.3 Omitted Calls and Completed-Case Latency
* **Exact Raw Omission Markers in `diagnosis_predictions.csv`**:
  * Config 5, `INC-1002`: `predicted_cause = 'N/A (Execution omitted due to Groq TPM rate limit)'`, `rubric_verdict = 'UNASSESSABLE'`, `latency_ms = 0.0`.
  * Config 7, `INC-1004`: `predicted_cause = 'N/A (Execution omitted due to Groq TPM rate limit)'`, `rubric_verdict = 'UNASSESSABLE'`, `latency_ms = 0.0`.
* **Completed-Case vs Intent-to-Treat Denominators**:
  * Completed-case accuracy evaluates only assessable completed calls ($N=5$ for Configs 5 and 7; $N=6$ for all others). Both Config 5 and Config 7 achieved $4/5 = \mathbf{80.00\%}$ completed-case strict accuracy.
  * Under Intent-to-Treat (ITT, $N=6$), unassessable omitted calls score 0, yielding $4/6 = \mathbf{66.67\%}$ strict accuracy for both Config 5 and Config 7.
* **Latency Accounting**: In both Config 5 and Config 7, the unassessable omitted call recorded `latency_ms = 0.0`. To prevent downward distortion:
  * Config 5 completed latency mean: $(3365.24 + 2940.22 + 3017.69 + 2804.52 + 3081.68) / 5 = \mathbf{3041.87\text{ ms}}$ ($3.04$ s). (Dividing by 6 would yield an erroneous $2534.89$ ms).
  * Config 7 completed latency mean: $(17593.97 + 16577.33 + 21380.61 + 17482.03 + 23364.51) / 5 = \mathbf{19279.69\text{ ms}}$ ($19.28$ s). (Dividing by 6 would yield an erroneous $16066.41$ ms).

### 4.4 Deprecated Configuration Labels Retired
* Older documents referred to "Multi-Agent No-Reflection" and "Multi-Agent No-Verification". These labels do not exist in the active 7-configuration factorial evaluation and have been formally replaced by the canonical IDs: **Config 1 through Config 7**.

---

## 5. Experiment C: Canonical Safety Test Taxonomy

From `research/raw/safety_test_results.csv`, the canonical 16-case boundary taxonomy is partitioned into four explicit categories:

1. **Adversarial Attacks ($N = 11$, 100.0% Blocked, Wilson 95% CI: $[0.7412, 1.0000]$)**:
   * `TC-ATT-01`: Missing ticket UUID / unissued ticket
   * `TC-ATT-02`: Expired ticket submission (> 30s TTL in fixture)
   * `TC-ATT-03`: Confirmation phrase mismatch
   * `TC-ATT-04`: Scope tampering: modified action ID
   * `TC-ATT-05`: Scope tampering: modified target URL
   * `TC-ATT-06`: Scope tampering: modified incident ID
   * `TC-ATT-07`: Replay attack using consumed nonce
   * `TC-ATT-08`: Attempted execution on rejected ticket
   * `TC-ATT-09`: Out-of-boundary remote HTTPS target
   * `TC-ATT-10`: Insecure remote plaintext HTTP target
   * `TC-ATT-11`: Credential exfiltration via embedded URL auth
2. **Execution Precondition Checks ($N = 2$, 100.0% Aborted Gracefully)**:
   * `TC-FAIL-01`: Target local service offline / unreachable (connection refused)
   * `TC-FAIL-02`: Remediation invoked when no fault active
3. **Recovery Verification Probe ($N = 1$, 100.0% Correctly Verified)**:
   * `TC-VERIF-01`: Degraded service after attempted recovery (correctly transitions to `VERIF_FAILED`)
4. **Positive Controls ($N = 2$, 100.0% Executed with Durable Audit)**:
   * `TC-POS-01`: Full end-to-end authorized lifecycle approval
   * `TC-AUDIT-01`: Independent verification of durable SQLite audit record persistence

*Resolution of Taxonomy Discrepancy*: Historical drafts characterized the two checks as "unauthorized-tool execution or rate-limit bypass". The authoritative test IDs are `TC-FAIL-01` (service unreachable) and `TC-FAIL-02` (no active fault).

---

## 6. Experiment D: Historical Provenance, Preflight Findings, and Harness Defects

To ensure scientific honesty and eliminate contradictions:

1. **Preflight Acquisition & Extraction Status**:
   * The AnoMod dataset archive (`AnoMod.zip`, 201,917,396 bytes, MD5 `30c5835190c3550c5efc34d6be4f9238`, SHA-256 `5086808ff4f2039b88c106cd996f4b9a7148675e20f66ee1718c511b95eb120a`) was acquired and unpacked into 38,349 files under `data/external/anomod/unpacked/`.
2. **Exploratory Preflight Diagnostic Findings**:
   * *Sampling Cadence Incompatibility*: The frozen model was trained on a 5-second sampling cadence ($\Delta t = 5$s; 120s historical horizon for $W=24$), whereas Experiment D's extraction harness aggregated Prometheus telemetry onto a 15-second epoch grid ($\Delta t = 15$s), introducing a distinct, unresolved temporal contract incompatibility.
   * *Sequence Stride Dropouts*: External Prometheus traces contain observation dropouts leaving **0 valid 24-step contiguous sequences** without synthetic imputation.
   * *Exploratory Zero-Shot Domain Shift*: An off-contract exploratory check on available shorter segments ($W=8, N=19$ windows) documented in `EXPERIMENT_D_ZERO_SHOT_CONTRACT_AUDIT.md` produced mean reconstruction error $e \approx 59.19$ vs $\tau = 0.709399$, an $\approx 83.4\times$ ($>80\times$) domain shift, resulting in **19/19 (100.0%) nominal false alarms**. Crucially, these evaluate off-contract, heavily overlapping diagnostic windows ($87.5\%$ overlap), representing an exploratory feasibility diagnostic rather than a valid production false-alarm rate estimate.
3. **Production Experiment D Execution Status**:
   * **HALTED AND UNEXECUTED**: Production execution (`run_production_experiment_d()`) requires CLI `--authorized` and an approved ratification token (`PROTOCOL_AMENDMENT_V1_2_RATIFICATION.json`). It was never ratified or executed.
4. **Calibration Leakage Defect in Harness**:
   * While `partition_normal_series_chronologically()` implemented a 7-step purge gap, `EXPERIMENT_D_CALIBRATION_INDEPENDENCE_AUDIT.md` identified that `run_experiment_d.py` reused validation windows (`v_win`) for both 99th percentile threshold calibration (line 550) and false alarm evaluation (line 566). This circular calibration leakage defect remains unexecuted in production and reinforced the supervisory decision to halt Experiment D under Path 3.

---

## 7. Bibliographic Reference Verification

| Key Reference | Verified Authors | Publication Venue & DOI / Identifier | Publication Category |
| :--- | :--- | :--- | :--- |
| **AnoMod** | Ke Ping, Hamza Bin Mazhar, Yuqing Wang, Ying Song, Mika V. Mäntylä | *Proceedings of the 23rd IEEE/ACM International Conference on Mining Software Repositories (MSR '26)*, pp. 677–681. DOI: [10.1145/3793302.3793324](https://doi.org/10.1145/3793302.3793324) | Peer-Reviewed Conference Paper |
| **Eadro** | Cheryl Lee, Tianyi Yang, Zhuangbin Chen, Yuxin Su, Michael R. Lyu | *Proceedings of the 45th IEEE/ACM International Conference on Software Engineering (ICSE '23)*, pp. 1750–1762. DOI: [10.1109/ICSE48619.2023.00150](https://doi.org/10.1109/ICSE48619.2023.00150) | Peer-Reviewed Conference Paper |
| **CloudRCA** | Yingying Zhang, Zhengxiong Guan, Huajie Qian, Leili Xu, Hengbo Liu, Qingsong Wen, Liang Sun, Junwei Jiang, Lunting Fan, Min Ke | *Proceedings of the 30th ACM International Conference on Information and Knowledge Management (CIKM '21)*, pp. 4373–4382. DOI: [10.1145/3459637.3481903](https://doi.org/10.1145/3459637.3481903) | Peer-Reviewed Conference Paper |
| **MetaGPT** | Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Jinlin Wang, Ceyao Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, **Jürgen Schmidhuber** | *The Twelfth International Conference on Learning Representations (ICLR 2024)*. arXiv: [2308.00352](https://arxiv.org/abs/2308.00352) | Peer-Reviewed Conference Paper |
| **NIST SP 800-53** | National Institute of Standards and Technology | NIST Special Publication 800-53, Rev 5 (includes control AC-3(2): Dual Authorization). DOI: [10.6028/NIST.SP.800-53r5](https://doi.org/10.6028/NIST.SP.800-53r5) | Official Security Standard |
| **LSTM ADW** | Pankaj Malhotra, Anusha Ramakrishnan, Gaurangi Anand, Lovekesh Vig, Puneet Agarwal, Gautam Shroff | *ICML 2016 Workshop on Anomaly Detection (ADW 2016)*. arXiv: [1607.00148](https://arxiv.org/abs/1607.00148) | Workshop Paper |
| **AutoGen** | Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shweti Zhang, Jiale Liu, Ahmed H. Awadallah, Ryen W. White, Doug Burger, Chi Wang | *arXiv preprint*. arXiv: [2308.08155](https://arxiv.org/abs/2308.08155) | Scholarly Preprint |

*Author Label Resolution*: The bibliography categorizes 13 peer-reviewed journal/conference papers, 1 official standard (NIST), and 2 workshop papers / preprints.

---

## 8. Summary of Old vs. Current Reconciled Values

| Item / Metric | Previously Claimed / Stale Value | Canonical Reconciled Value | Source of Truth & Root Cause |
| :--- | :--- | :--- | :--- |
| **Isolation Forest Recall** | 76.67% (in prior assistant text summary) | **47.50%** ($57/120$) | `detection_predictions.csv`: 57 TP / 120 fault windows. Literal string `76.67%` appeared in unrelated external benchmark text (`b6123a7`), but never in AegisOps metrics; canonical 47.50% retained. |
| **McNemar Chi-Square** | 78.036 (in prior assistant text summary) | **61.02** (continuity) / **63.0** (uncorrected) | Recomputed from $b=63, c=0$: $(62)^2/63 = 61.02$. Unsupported by canonical contingency table; canonical 61.02 / 63.0 retained. |
| **Config 6 Top-1 Accuracy** | 100.0% (unqualified) | **83.33% Strict** ($5/6$), **100.0% Lenient** ($6/6$) | `diagnosis_predictions.csv`: INC-1002 received partial credit. 100% applies only to lenient scoring. |
| **Config 5 Top-1 Accuracy** | 66.67% (unqualified) | **66.67% Strict ITT** ($4/6$), **80.00% Completed** ($4/5$) | `diagnosis_predictions.csv`: INC-1002 omitted due to Groq rate limit. |
| **Config 7 Top-1 Accuracy** | 66.67% (unqualified) | **66.67% Strict ITT** ($4/6$), **80.00% Completed** ($4/5$) | `diagnosis_predictions.csv`: INC-1004 omitted due to Groq rate limit. |
| **Diagnosis Config Labels** | "No-Reflection", "No-Verification" | **Config 1 through Config 7** | Stale historical labels retired; aligned with factorial design in `diagnosis_metrics.csv`. |
| **Safety Test Categories** | Unauthorized tool / rate limit bypass | **11 Attacks, 2 Precondition Checks, 1 Probe, 2 Controls** | `safety_test_results.csv`: `TC-FAIL-01` (service offline) and `TC-FAIL-02` (no active fault). |
| **AnoMod Authors** | Deng et al. (in prior text) | **Ping et al.** (Ke Ping et al., MSR 2026) | Verified official ACM Digital Library / MSR 2026 proceedings. |
| **Eadro Authors** | Zhang et al. (in prior text) | **Lee et al.** (Cheryl Lee et al., ICSE 2023) | Verified official IEEE Xplore / ICSE 2023 proceedings. |
| **Experiment D Status** | "No external predictions exist" vs shift proof | **Preflight checks completed (demonstrating shift); production evaluation unexecuted** | Distinguishes exploratory preflight diagnostic findings from unexecuted production evaluation. |
| **Harness Calibration Leakage** | "Calibration leakage eliminated" | **Active defect identified in harness (`run_experiment_d.py:550,566`)** | Audit proved validation windows reused for threshold calibration and evaluation in unexecuted harness. |

---

## 9. Remaining Methodological Uncertainties

1. **Synthetic Telemetry Distribution**: Experiment A and B evaluations are conducted on controlled synthetic time series. Cross-system transferability to live Kubernetes environments is deferred.
2. **Diagnostic Sample Size**: $N = 6$ canonical failure scenarios provides limited non-parametric statistical power ($1-\beta \approx 0.14$). Multi-agent LLM reasoning is validated as a pilot feasibility trial, not an asymptotic statistical comparison.
3. **Execution Boundary**: Safety containment is validated strictly against a localhost HTTP application boundary (`127.0.0.1:8765`), not kernel-level or multi-tenant network mesh environments.

---

## 10. Dated Closure Record and Final Verdict

* **Audit Completion Date**: October 14, 2026
* **Verification Scope**: Final cross-document consistency closure across `CANONICAL_METRIC_RECONCILIATION.md`, `UPDATED_SEVEN_PHASE_CHECKLIST.md`, `AEGISOPS_MASTER_RESEARCH_HANDOFF.md`, `statistical_analysis.md`, `generate_statistical_analysis.py`, and `AEGISOPS_RESEARCH_PAPER.md`.
* **Executed Test Verification**:
  1. **Current Focused Test Suite**: `pytest test_statistical_audit.py test_research_instrumentation.py test_approval.py -v`: 18/18 passed in 30.18s (exit code 0, log: `task-3429.log`; earlier pre-compaction run recorded 11.20s in `task-3284.log`).
  2. **Current Full Repository Regression Suite**: `pytest --tb=short`: 107/107 passed in 99.50s (exit code 0, executed on current working tree at `2026-10-14T10:22:24Z`, log: `task-3502.log`; historical baseline run recorded 77.56s in `task-3108.log`).
  3. **Statistical Analysis Generator**: `python research/results/generate_statistical_analysis.py`: exit code 0 (log: `task-3424.log`).
  4. **Git Format & Whitespace Check**: `git diff --check`: clean (exit code 0, log: `task-3419.log`).
* **Cryptographic & Model State Invariants**:
  * Frozen Checkpoint SHA-256: `1cf44e6e82e459f543fcace25334f3076b76c77a357d46f65c11e3c44fd382de` (3,733 weights, strictly invariant).
  * Anomaly Decision Threshold: $\tau = 0.7093990445137024$ (strictly preserved).
* **Deferred Actions (Out of Scope for Review Package)**:
  1. Visual PDF layout proofing (font embedding, page overflow inspection, line wrapping) — formally required before camera-ready submission.
  2. Production Experiment D execution on external AnoMod telemetry — formally excluded under Path 3 Bounded-Claims Policy.
* **Historical Status Verdict**: **`READY FOR SUPERVISOR REVIEW`** (retained as prior audit provenance).
* **Current Release Status (2026-10-15)**: **`NOT READY — MATERIAL CONTRADICTIONS OR RENDERING BLOCKERS REMAIN`**. The active manuscript now has four tables, costs are corrected, and the Figure A.2 release candidate is content-verified; faithful full-manuscript rendering, author/venue confirmation, and manifest reconciliation closure remain pending.
