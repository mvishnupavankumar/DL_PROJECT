# AegisOps: Formal Statistical Audit & Hypothesis Testing Protocol

> **Supersession notice (2026-10-15):** This historical audit retains nominal FA/hr projections. Current release documents supersede those values: operational false alarms per hour are `UNAVAILABLE` for the non-streaming synthetic batch benchmark. The active manuscript treats the window-level McNemar result as descriptive and the six-scenario Wilcoxon result as post-hoc exploratory.

**Audit Date**: 2026-10-12  
**Lead Auditor**: Senior ML Researcher & Software Testing Specialist  
**Verification Status**: All calculations verified from raw observations; unit tests passing (`test_statistical_audit.py`).

---

## 1. Inspection and Correction of the Paired Binomial Test

### A. The Defect in Prior Implementation
In previous analysis scripts, the p-value for paired discordant counts was calculated as:
```python
# DEFECTIVE IMPLEMENTATION
mcnemar_exact_p = stats.binom.pmf(0, b + c, 0.5) * 2
```
This formula computes $2 \times (0.5)^{b+c}$. It is valid **only** in the degenerate edge-case where one of the discordant cells is zero ($\min(b, c) = 0$). When both discordant cells are non-zero (such as false alarm counts $b = 4$ and $c = 2$), this formula evaluated to $2 \times (0.5)^6 = 0.03125$, erroneously reporting statistical significance ($p < 0.05$) where none existed!

### B. The Correct Exact Two-Sided Binomial Test
Under the null hypothesis $H_0$ that both paired classifiers have equal marginal probabilities, the number of discordant pairs $k = \min(b, c)$ out of $n = b + c$ total discordant pairs follows a binomial distribution:
$$X \sim \text{Binomial}\left(n = b + c, p = 0.5\right)$$

The exact two-sided p-value is the sum of probabilities of all outcomes that are as likely or less likely than the observed count $k$:
$$p = 2 \times \sum_{i=0}^{\min(b, c)} \binom{n}{i} (0.5)^n \quad \text{for symmetric } p = 0.5$$

This is implemented directly via `scipy.stats.binomtest`:
```python
import scipy.stats as stats

def mcnemar_exact_test(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    res = stats.binomtest(k, n, p=0.5, alternative="two-sided")
    return float(res.pvalue)
```

### C. Benchmark Verification Test Case ($b = 4, c = 2$)
For discordant counts $b = 4$ and $c = 2$ ($n = 6, k = 2$):
* $P(X = 0) = \binom{6}{0} (0.5)^6 = \frac{1}{64} = 0.015625$
* $P(X = 1) = \binom{6}{1} (0.5)^6 = \frac{6}{64} = 0.093750$
* $P(X = 2) = \binom{6}{2} (0.5)^6 = \frac{15}{64} = 0.234375$
* One-sided tail probability: $P(X \le 2) = \frac{1 + 6 + 15}{64} = \frac{22}{64} = 0.34375$
* **Two-sided exact p-value**:
  $$p = 2 \times 0.34375 = \mathbf{0.6875}$$

This benchmark is formally tested and passing in `test_statistical_audit.py::test_mcnemar_exact_b4_c2_equals_0_6875`.

---

## 2. Complete Recalculation of Experimental Findings

### Experiment A: Detection Recall (Confirmatory Analysis)
* **Design**: Paired evaluation on $N = 120$ independent fault episodes across 6 failure classes.
* **Contingency Table**:
  * Both Detected ($a$): 57
  * LSTM Only Detected ($b$): 63
  * Isolation Forest Only Detected ($c$): 0
  * Both Missed ($d$): 0
* **Hypothesis**: $H_0: P(\text{LSTM misses} \cap \text{IsoForest detects}) = P(\text{LSTM detects} \cap \text{IsoForest misses})$.
* **Test Statistics**:
  * Discordant Pairs: $b = 63, c = 0, n = 63$.
  * Exact Two-Sided Binomial p-value:
    $$p = 2 \times (0.5)^{63} = \mathbf{2.168 \times 10^{-19}} \quad (p < 0.001)$$
  * Edwards Continuity-Corrected $\chi^2$:
    $$\chi^2 = \frac{(|63 - 0| - 1)^2}{63} = \frac{62^2}{63} = \mathbf{61.02} \quad (p = 5.66 \times 10^{-15})$$
  * Paired Difference in Recall:
    $$\Delta = \frac{b - c}{N} = \frac{63 - 0}{120} = \mathbf{+0.5250} \quad \left(95\% \text{ Wald CI}: [+0.4350, +0.6150]\right)$$
* **Scientific Verdict**: **Confirmatory**. We reject $H_0$ at $\alpha = 0.001$. The LSTM Autoencoder achieves significantly superior sensitivity over Isolation Forest on multivariate temporal fault profiles.

---

### Experiment A: Normal False Alarms (Exploratory Analysis)
* **Design**: Paired evaluation on $N = 200$ independent steady-state normal windows.
* **Observations**:
  * LSTM Autoencoder False Alarms: 2 / 200 (1.0%, 7.2 FA/hr; Wilson 95% CI: $[0.003, 0.036]$).
  * Isolation Forest False Alarms: 4 / 200 (2.0%, 14.4 FA/hr; Wilson 95% CI: $[0.008, 0.050]$).
* **Discordant Analysis**:
  * Isolation Forest alarmed only ($b$): 4
  * LSTM alarmed only ($c$): 2
* **Hypothesis Test**:
  * Exact Two-Sided Binomial p-value ($b = 4, c = 2$):
    $$p = \mathbf{0.6875}$$
* **Scientific Verdict**: **Exploratory / Non-Significant**. The difference in false alarm rates (1.0% vs. 2.0%) is **not statistically significant** ($p = 0.6875 > 0.05$). Larger long-term telemetry traces are required before claiming false alarm divergence.

---

### Experiment B: Root-Cause Diagnosis (Power & Sample Size Audit)
* **Design**: $N = 6$ ground-truth architectural failure scenarios.
* **Power Analysis**:
  * To detect an effect size $\Delta = 20\%$ at $\alpha = 0.05$ with $80\%$ power ($1 - \beta = 0.80$), a paired study requires $N \ge 72$ independent incident cases.
  * With $N = 6$, statistical power is $1 - \beta \approx 0.14$ (severely underpowered).
* **Scientific Verdict**: **Descriptive Pilot Benchmark Only**.
  * No claims of asymptotic statistical significance or generalized agent superiority may be made in the paper.
  * Results must be reported strictly as point estimates with explicit qualitative case discussions.

---

### Experiment C: Execution Safety Boundary (Confirmatory Local Audit)
* **Design**: $N = 11$ adversarial boundary penetration cases against the two-man-rule ticket engine.
* **Observations**:
  * Attacks Attempted: 11
  * Attacks Blocked: 11 (100.0%)
  * Wilson 95% Confidence Interval: $[0.7412, 1.0000]$
* **Independent Recovery Verification**:
  * Verification Trials: 4
  * Correct Verifications: 4 (100.0%)
  * Wilson 95% Confidence Interval: $[0.5101, 1.0000]$
* **Scientific Verdict**: Confirms strict software boundary enforcement within the local architecture. Wilson confidence intervals must be reported alongside point estimates to reflect finite sample uncertainty.
