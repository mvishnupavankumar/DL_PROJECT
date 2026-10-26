# AegisOps: Experiment D Statistical Acceptance Criteria & Pre-Registered Evaluation Plan

**Document Path**: `research/audits/EXPERIMENT_D_STATISTICAL_ACCEPTANCE_CRITERIA.md`  
**Date**: October 13, 2026  
**Auditor**: Senior ML Research Supervisor, Statistical-Methodology Reviewer & Reproducibility Auditor  
**Predecessor Standard**: [`research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md) (Protocol v1.1.0)  
**Proposed Amendment**: [`research/audits/PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md`](file:///c:/DL_PROJECT/research/audits/PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md) (Protocol v1.2.0 Proposal)  
**Status**: **STATISTICAL ACCEPTANCE CRITERIA FROZEN FOR HUMAN REVIEW**

---

## 1. Confirmatory versus Exploratory Analysis Separation

To prevent post-hoc data dredging and p-hacking, all analyses for Experiment D are partitioned into pre-registered Confirmatory analyses and Secondary Exploratory analyses:

```mermaid
graph TD
    subgraph Confirmatory_Analyses [Confirmatory Analyses (Pre-Registered Hypotheses)]
        A["Primary Cohort: SocialNetwork (K=12 Fault Scenarios)"]
        B["H1: Window-Level Paired McNemar Exact Test (LSTM vs IF)"]
        C["H2: Scenario-Level Wilcoxon Signed-Rank Test (LSTM vs IF)"]
        D["Preprocessing: Option 2 (Domain Z-Score on Normal Baseline)"]
    end

    subgraph Exploratory_Analyses [Exploratory Analyses (Discovery & Sensitivity)]
        E["Secondary Cohort: TrainTicket (Trace-Truncated Scenarios)"]
        F["Zero-Shot Domain Shift Evaluation: Option 3 (Frozen Training Scaler)"]
        G["Threshold Sensitivity: Empirical 99th Percentile vs Parametric Gaussian 3-Sigma"]
        H["Per-Feature Reconstruction Error Breakdown"]
    end
```

---

## 2. Evaluation Units and Population Definitions

### 2.1 Window-Level Unit
- **Definition**: A contiguous sequence of $W = 8$ observations spaced at $\Delta t = 15.0\text{ seconds}$ (duration = 120 seconds).
- **Eligibility Filter**: Every step within the window must have complete host metrics and client trace spans ($N_{\text{req}} \ge 1$). Windows spanning idle intervals ($N_{\text{req}} = 0$) or missing scrapes are excluded.
- **Fairness Constraint**: All five detectors (AegisOps LSTM, Isolation Forest, Narrow Rules, Resource-Only Rules, Full Operational Rules) must be evaluated on **100% identical eligible windows**.

### 2.2 Scenario-Level Unit
- **Definition**: The complete time-series run of a single failure scenario in SocialNetwork ($K = 12$ independent fault scenarios, each lasting 20–25 minutes).
- **Independence Property**: Each scenario represents an independent execution with isolated microservice containers and separate fault injections.

---

## 3. Confusion Matrix Definitions and Performance Metrics

### 3.1 Confusion Matrix Formulations

| Classification | Ground Truth: Fault Window ($y = 1$) | Ground Truth: Normal Window ($y = 0$) |
| :--- | :--- | :--- |
| **Flagged as Anomaly ($\hat{y} = 1$)** | **True Positive (TP)** | **False Positive (FP)** |
| **Not Flagged ($\hat{y} = 0$)** | **False Negative (FN)** | **True Negative (TN)** |

- **Fault Population ($y = 1$)**: Contiguous eligible windows constructed from the 12 fault scenarios in SocialNetwork.
- **Normal Population ($y = 0$)**: Contiguous eligible windows constructed from the held-out validation partition of `Normal_Baseline` ($N_{\text{val}} = 8$ windows).

### 3.2 Formal Performance Metrics

1. **Recall / True Positive Rate (TPR)**:
   $$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$
2. **Precision / Positive Predictive Value (PPV)**:
   $$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$
3. **False Positive Rate (FPR)**:
   $$\text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}$$
4. **Specificity / True Negative Rate (TNR)**:
   $$\text{Specificity} = \frac{\text{TN}}{\text{FP} + \text{TN}} = 1 - \text{FPR}$$
5. **F1 Score**:
   $$\text{F1} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$
6. **Balanced Accuracy**:
   $$\text{Balanced Accuracy} = \frac{\text{Recall} + \text{Specificity}}{2}$$

---

## 4. Paired Comparisons and Hypothesis Testing

### 4.1 Confirmatory Hypothesis H1 (Window-Level McNemar Test)

- **Null Hypothesis ($H_{0, 1}$)**: The marginal detection probability of AegisOps LSTM Autoencoder equals that of Isolation Forest on external microservice telemetry ($P(\text{LSTM}=1) = P(\text{IF}=1)$).
- **Alternative Hypothesis ($H_{1, 1}$)**: The marginal detection probability of AegisOps LSTM Autoencoder exceeds that of Isolation Forest ($P(\text{LSTM}=1) > P(\text{IF}=1)$).
- **Discordant Pair Tally**:
  - $b$: Number of windows where LSTM flags an anomaly ($\hat{y}_{\text{LSTM}} = 1$) and Isolation Forest does not ($\hat{y}_{\text{IF}} = 0$).
  - $c$: Number of windows where Isolation Forest flags an anomaly ($\hat{y}_{\text{IF}} = 1$) and LSTM does not ($\hat{y}_{\text{LSTM}} = 0$).
- **Test Statistic**:
  - If $b + c < 25$: Exact Binomial Test:
    $$p = 2 \cdot \sum_{k=0}^{\min(b, c)} \binom{b + c}{k} 0.5^{b + c}$$
  - If $b + c \ge 25$: Continuity-corrected McNemar $\chi^2$ test:
    $$\chi^2 = \frac{(|b - c| - 1)^2}{b + c}, \quad \text{df} = 1$$
- **Pre-registered Acceptance Criterion**: Reject $H_{0, 1}$ if two-sided $p < 0.05$ and $b > c$.

### 4.2 Confirmatory Hypothesis H2 (Scenario-Level Wilcoxon Signed-Rank Test)

- **Null Hypothesis ($H_{0, 2}$)**: The median difference in scenario-level recall between LSTM Autoencoder and Isolation Forest across the $K = 12$ SocialNetwork fault scenarios is zero ($\tilde{d} = 0$).
- **Alternative Hypothesis ($H_{1, 2}$)**: The median difference in scenario-level recall is strictly positive ($\tilde{d} > 0$).
- **Pairwise Difference**:
  $$d_k = \text{Recall}_{\text{LSTM}, k} - \text{Recall}_{\text{IF}, k}, \quad k \in \{1, \dots, 12\}$$
- **Test Statistic**: Wilcoxon signed-rank statistic $W = \min(W^+, W^-)$ evaluated against exact discrete null distributions.
- **Pre-registered Acceptance Criterion**: Reject $H_{0, 2}$ if two-sided $p < 0.05$ and median difference $\tilde{d} > 0$.

---

## 5. Statistical Dependence and Autocorrelation Accounting

### 5.1 Sliding Window Autocorrelation Disclosure
- **Mandatory Caveat**: Consecutive sliding windows with stride 1 share $W - 1 = 7$ observations ($87.5\%$ sample overlap).
- **Impact on Inference**: While the McNemar test assesses the marginal parity of discordant decisions, sliding window autocorrelation reduces the *effective sample size* below the nominal window count ($N_{\text{eff}} < N$). Consequently, standard uncorrected binomial p-values may exhibit inflated Type I error rates.
- **Reporting Rule**: In all manuscript tables and text, window-level McNemar p-values must be paired with an explicit caveat noting window overlap.
- **Primary Independent Anchor**: The scenario-level Wilcoxon signed-rank test ($K = 12$) evaluates 12 mutually independent microservice runs and serves as the primary independent statistical anchor.

---

## 6. Confidence Intervals and Multiple Comparison Corrections

1. **Proportions (Recall, Precision, FPR, Specificity)**:
   - Must be reported with **95% Wilson Score Intervals**:
     $$\text{CI}_{95\%} = \frac{\hat{p} + \frac{z^2}{2n} \pm z \sqrt{\frac{\hat{p}(1 - \hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}, \quad z = 1.95996$$
2. **Paired Differences in Proportions**:
   - Must be reported with **95% Newcombe Hybrid Score Intervals** for paired binary data.
3. **Multiple Comparison Corrections**:
   - For secondary baseline comparisons (LSTM vs. Narrow Rules, LSTM vs. Resource Rules, LSTM vs. Full Operational Rules), p-values must be adjusted using the **Holm-Bonferroni step-down procedure** to maintain Family-Wise Error Rate (FWER) $\le 0.05$.

---

## 7. Independent Recomputation & Verification Gate

Before any Experiment D results may be incorporated into the manuscript:
1. **Raw Predictions File**: `research/raw/external_anomod_predictions.csv` must be written directly by the evaluation harness.
2. **Independent Recomputation**: An independent audit script must read the CSV, recompute all confusion matrix cells, calculate Wilson CIs, re-run `scipy.stats.binomtest` and `scipy.stats.wilcoxon`, and assert 100% numerical match with `external_anomod_metrics.csv` and `experiment_d_manifest.json`.
3. **Bit-for-Bit Provenance**: The manifest must record Git commit hash, Python version, PyTorch version, checkpoint SHA-256, and UTC timestamp.
