# AegisOps: Statistical Assumption Review and Hypothesis Test Audit

> **Supersession note (2026-10-15):** This dated supporting audit retains the detailed statistical tabulation formerly reproduced as manuscript Table 5. The active four-table manuscript uses its Section 10 narrative and treats the scenario-level Wilcoxon result as post-hoc exploratory, not pre-registered confirmatory inference or proof of broad superiority. Where this historical audit uses stronger language below, the current release interpretation controls.

**Audit Gate**: Final Detection Rate Audit and Phase 4 Readiness Gate  
**Audit Date**: 2026-10-12  
**Audit Directory**: `research/audits/detection_rate_and_phase4_gate_20261012/`  
**Reference Scripts**: `research/results/generate_statistical_analysis.py`, `research/experiments/run_experiment_a.py`  
**Underlying Data**: `research/results/detection_predictions.csv` ($N = 320$ evaluation units)

---

## 1. Audit of Experimental Design & Statistical Units

### 1.1 Independence of Evaluation Units
- **Normal Cohort ($N = 200$)**:
  - Generated via `generate_normal_windows(200, seed=2026)`.
  - Each window represents a completely independent stochastic simulation with freshly sampled phase, baseline offsets, and noise.
  - **Audit Verdict**: Valid independent and identically distributed (i.i.d.) observations under the synthetic data-generating process.
- **Incident Cohort ($N = 120$)**:
  - Generated via `generate_incident_telemetry(inc_id, seed=rep_seed)` across 6 distinct scenario archetypes (INC-1001 through INC-1006).
  - Each scenario contains $R = 20$ replicates with unique stochastic seeds (`rep_seed = 3001` to `3120`).
  - **Audit Verdict**: Clustered replicate structure. While the stochastic noise is independent across replicates, the underlying deterministic fault trajectories (e.g. latency slope, CPU saturation target) are shared within each scenario cluster.

### 1.2 Paired Evaluation Structure
- Every candidate detector (Narrow Rules, Resource-Only Rules, Full Operational Rules, Isolation Forest, LSTM Autoencoder, and Combined Alert) is evaluated on the exact same 320 evaluation windows.
- Predictions across detectors are paired. Paired comparative tests (e.g., McNemar's test, Wilcoxon signed-rank test) are appropriate.

---

## 2. Re-Evaluation of Paired Hypothesis Tests

### 2.1 Standard McNemar Exact Test (Window-Level Analysis)
In `research/results/generate_statistical_analysis.py`, the reported test between LSTM Autoencoder and Isolation Forest on all $N = 120$ incident windows evaluates:

$$\begin{pmatrix} a & b \\ c & d \end{pmatrix} = \begin{pmatrix} 57 & 63 \\ 0 & 0 \end{pmatrix}$$
where:
- $a = 57$: Both LSTM and Isolation Forest detected the anomaly.
- $b = 63$: LSTM detected, Isolation Forest missed.
- $c = 0$: Isolation Forest detected, LSTM missed.
- $d = 0$: Both missed.

**Exact Binomial p-value**:
$$p = 2 \times \sum_{k=63}^{63} \binom{63}{k} (0.5)^{63} = 2.168 \times 10^{-19} < 0.001$$

**Edwards Continuity-Corrected $\chi^2$**:
$$\chi^2 = \frac{(|b - c| - 1)^2}{b + c} = \frac{(|63 - 0| - 1)^2}{63} = \frac{62^2}{63} = \mathbf{61.016} \quad (p = 5.66 \times 10^{-15})$$

### 2.2 Replicate Clustered Correlation Caveat
Because the 120 incident windows consist of 20 replicates across 6 scenarios, treating all 120 windows as independent Bernoulli trials ignores intra-cluster correlation ($\rho_{\text{intra}} > 0$). Intra-cluster correlation reduces the effective sample size ($N_{\text{eff}} < 120$), meaning the standard McNemar $p = 2.17 \times 10^{-19}$ overstates statistical certainty.

### 2.3 Cluster-Adjusted Analysis (Scenario-Level Wilcoxon Signed-Rank Test)
To rigorously adjust for the clustered replicate design, the performance is aggregated across the 6 independent failure archetypes:

| Scenario ID | Architectural Failure Archetype | LSTM Recall ($N=20$) | Isolation Forest Recall ($N=20$) | Paired Recall Difference ($\Delta$) |
| :--- | :--- | :---: | :---: | :---: |
| **INC-1001** | Payment API pool exhaustion | 1.00 (20/20) | 0.05 (1/20) | **+0.95** |
| **INC-1002** | Customer DB unavailable | 1.00 (20/20) | 0.25 (5/20) | **+0.75** |
| **INC-1003** | Production server CPU saturation | 1.00 (20/20) | 0.80 (16/20) | **+0.20** |
| **INC-1004** | Storage disk capacity exhausted | 1.00 (20/20) | 0.70 (14/20) | **+0.30** |
| **INC-1005** | Auth token validation failure | 1.00 (20/20) | 0.45 (9/20) | **+0.55** |
| **INC-1006** | Service-to-service timeouts | 1.00 (20/20) | 0.60 (12/20) | **+0.40** |

**Exact Non-Parametric Test**:
- All $n = 6$ paired differences are strictly positive ($\Delta > 0$).
- Sum of negative signed ranks: $W = 0.0$.
- Two-tailed exact Wilcoxon signed-rank test $p$-value:
  $$p = 2 \times \left(\frac{1}{2}\right)^6 = \mathbf{0.03125} < 0.05$$

**Current release interpretation**:
The six-scenario aggregation yields the stated exploratory Wilcoxon result ($W=0.0$, $p=0.03125$). It is a post-hoc exploratory analysis with a discrete test floor and low power, not a pre-registered confirmatory finding or evidence of broad cross-system superiority.

---

## 3. False Positive Rate Hypothesis Test

Comparing the LSTM Autoencoder ($\text{FP} = 2$) against Full Operational Rules ($\text{FP} = 0$) on the $N = 200$ independent normal evaluation windows:
- Discordant pairs on normal windows: $b = 0$ (Rules flagged, LSTM normal), $c = 2$ (LSTM flagged, Rules normal).
- Exact two-tailed binomial test:
  $$p = 2 \times \binom{2}{0} (0.5)^2 = \mathbf{0.5000}$$
- **Audit Verdict**: The observed difference in false alarm count ($2$ vs. $0$) on $N = 200$ normal evaluation windows is **not statistically significant** ($p = 0.5000 > 0.05$). Claims that the LSTM Autoencoder has a significantly worse false alarm profile than operational rules on this sample are unsupported.
