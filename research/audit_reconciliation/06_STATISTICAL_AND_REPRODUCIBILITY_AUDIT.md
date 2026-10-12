# 06 — Statistical and Reproducibility Audit

**Audit Date**: 2026-10-12  
**Auditor**: Senior Statistical Reviewer & Reproducibility Specialist  
**Primary Files**:
- [`research/statistical_tests.py`](file:///c:/DL_PROJECT/research/statistical_tests.py)
- [`research/results/generate_statistical_analysis.py`](file:///c:/DL_PROJECT/research/results/generate_statistical_analysis.py)
- [`research/results/statistical_analysis.md`](file:///c:/DL_PROJECT/research/results/statistical_analysis.md)
- [`research/STATISTICAL_AUDIT.md`](file:///c:/DL_PROJECT/research/STATISTICAL_AUDIT.md)
- [`research/run_all.py`](file:///c:/DL_PROJECT/research/run_all.py)
- [`research/MANIFEST_SHA256.json`](file:///c:/DL_PROJECT/research/MANIFEST_SHA256.json)
- Regression Tests: [`test_statistical_audit.py`](file:///c:/DL_PROJECT/test_statistical_audit.py)

---

## 1. Statistical Hypothesis Testing Verification

### A. Paired Exact Binomial Test & McNemar Analysis
Under the null hypothesis $H_0$ that paired classifiers have equal marginal error rates, discordant pair outcomes follow a binomial distribution $X \sim \text{Binomial}(n = b + c, p = 0.5)$.

1. **Benchmark Verification Case ($b = 4, c = 2$)**:
   - Total discordant pairs: $n = 6$, minority count $k = 2$.
   - Probability mass:
     $$P(X = 0) = \frac{1}{64}, \quad P(X = 1) = \frac{6}{64}, \quad P(X = 2) = \frac{15}{64}$$
   - One-sided tail sum: $P(X \le 2) = \frac{22}{64} = 0.34375$.
   - Two-sided exact p-value:
     $$p = 2 \times 0.34375 = \mathbf{0.6875}$$
   - *Regression Status*: Passing in `test_statistical_audit.py::test_mcnemar_exact_b4_c2_equals_0_6875`.  
   - *Finding*: Corrects the historical defect where scripts evaluated $2 \times (0.5)^6 = 0.03125$.
2. **Experiment A Detection Recall ($N = 120$ Incident Episodes)**:
   - LSTM Autoencoder detected, Isolation Forest missed: $b = 63$.
   - Isolation Forest detected, LSTM Autoencoder missed: $c = 0$.
   - Exact Two-Sided Binomial p-value:
     $$p = 2 \times (0.5)^{63} = \mathbf{2.168 \times 10^{-19}} \quad (p < 0.001)$$
   - Edwards Continuity-Corrected $\chi^2$:
     $$\chi^2 = \frac{(|63 - 0| - 1)^2}{63} = \frac{62^2}{63} = \mathbf{61.02} \quad (p = 5.66 \times 10^{-15})$$
   - Paired Difference in Sensitivity:
     $$\Delta = \frac{63 - 0}{120} = \mathbf{+0.5250} \quad \left(95\% \text{ Wald CI}: [+0.4350, +0.6150]\right)$$
   - *Verdict*: Confirmatory rejection of $H_0$ at $\alpha = 0.001$.
3. **Experiment A Steady-State False Alarms ($N = 200$ Normal Windows)**:
   - Isolation Forest alarmed only: $b = 4$.
   - LSTM Autoencoder alarmed only: $c = 2$.
   - Exact Two-Sided Binomial p-value:
     $$p = \mathbf{0.6875} \quad (p > 0.05)$$
   - *Verdict*: Exploratory / Non-significant. The observed difference in false alarm rates (1.0% vs. 2.0%) does not reach statistical significance.

---

## 2. Unit of Analysis & Independence Assumptions

To avoid pseudoreplication, the unit of analysis was explicitly audited for each experiment:

| Experiment | Unit of Analysis | Sample Size ($N$) | Data Generation / Independence Guarantee |
| :--- | :--- | :---: | :--- |
| **Exp A: Fault Detection** | 24-step sequence window | $N = 120$ episodes | Replicate-specific independent seeds ($3001$ to $3120$) across 6 distinct failure classes. |
| **Exp A: False Alarms** | 24-step sequence window | $N = 200$ windows | Disjoint test seed ($2026$) with zero overlap with training/validation seeds ($42$). |
| **Exp B: Diagnosis** | Architectural incident scenario | $N = 6$ scenarios | 6 canonical failure modes in `data/incidents.json`. |
| **Exp C: Safety Boundary** | Adversarial penetration trial | $N = 11$ attacks | Discrete execution trials targeting independent authorization boundaries. |

---

## 3. Power Analysis & Sample Size Constraints

### Experiment B: Root-Cause Diagnosis
- The ground-truth incident catalog contains exactly $N = 6$ scenarios.
- Power Analysis:
  - For an effect size $\Delta = 20\%$ at significance level $\alpha = 0.05$, achieving $80\%$ statistical power requires $N \ge 72$ independent incident scenarios.
  - With $N = 6$, statistical power is approximately **$1 - \beta \approx 0.14$** (severely underpowered).
- **Mandate**: The manuscript must explicitly report Experiment B as an exploratory pilot benchmark. No claims of asymptotic statistical superiority may be asserted.

### Experiment C: Safety Boundary
- Sample size: $N = 11$ adversarial attacks.
- Observed success rate: $100.0\%$ ($11/11$).
- Wilson Score 95% Confidence Interval: $[0.7412, 1.0000]$.
- **Mandate**: The manuscript must report the finite-sample interval $[0.741, 1.000]$ alongside the $100\%$ point estimate to reflect sample size uncertainty.

---

## 4. Controlled Pipeline Replay & Reproducibility Audit

A controlled execution of `research/run_all.py` was conducted under `.venv\Scripts\python.exe`:

### Execution Results
- **Command**: `.\.venv\Scripts\python.exe research/run_all.py`
- **Exit Code**: `0`
- **Total Duration**: `53.6 seconds`
- **Pytest Output**: 42 passed in 17.11s.
- **Side-Effects Verified**:
  - `data/aegisops_live.sqlite3`: Preserved intact (SHA-256: `b8f33f63...`).
  - `models/lstm_autoencoder.pt`: Preserved intact (SHA-256: `df867ce9...`).
  - Temporary disposable test databases unlinked during teardown.
  - Zero network calls to remote endpoints.

### Caveats and Findings for Research Integrity
1. **Virtual Environment Dependency**: Execution with system Python fails on `test_live_monitoring.py` due to missing `streamlit`. Must use `.venv`.
2. **Offline Rubric Audit vs. Live LLM Replay**: `run_all.py` executes `generate_diagnosis_audit.py` (evaluating recorded predictions) rather than calling the live Groq LLM API via `run_experiment_b.py`.
3. **Static Publication Figures**: Figures in `research/figures/` are static assets not generated by `run_all.py`.
4. **Manifest Limitation**: The SHA-256 manifest records existing disk hashes; it does not verify that an experiment was dynamically re-executed.
