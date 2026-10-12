# AegisOps: Detection Metric Reconciliation Report

**Audit Gate**: Phase 3 Detection Evidence Closure and Master Checklist Update  
**Audit Date**: 2026-10-12  
**Audit Directory**: `research/audits/detection_closure_gate_20261012/`  
**Reference CSV**: `research/audits/detection_closure_gate_20261012/RECOMPUTED_DETECTION_METRICS.csv`  
**Underlying Predictions**: `research/results/detection_predictions.csv` ($N = 320$)

---

## 1. Baseline Definitions and Code Implementation Mapping

To resolve previous ambiguities where audit texts referenced 40/120 (33.33%), 80/120 (66.67%), and 120/120 (100.0%) recall figures, the rule configurations are formally cataloged below:

| Baseline Name | Implementation Logic / Code Condition | Target Telemetry Dimensions |
| :--- | :--- | :--- |
| **Narrow Rules** | `lat >= 1000.0 or mem >= 95.0` | Latency (ms), Memory (%) |
| **Resource-Only Rules** | `lat >= 1000.0 or mem >= 95.0 or cpu >= 90.0 or disk >= 95.0` | Latency, Memory, CPU (%), Disk (%) |
| **Full Operational Rules** | Resource rules $+$ `err > 0.5` | Latency, Memory, CPU, Disk, HTTP Error Rate (%) |
| **Isolation Forest** | `-iso_forest.decision_function(w) > -0.018694` | Flattened 120-dim feature vector ($24 \times 5$) |
| **LSTM Autoencoder** | `reconstruction_mse(w) > 0.709399` | 24-step $\times$ 5-channel temporal trajectory |
| **Combined Alert** | `rule_flag or lstm_flag` | Logical OR union of Full Rules and LSTM |

---

## 2. Comprehensive Recomputed Metrics Table

Every metric below was independently calculated directly from the 320 evaluation rows using exact formulas and 95% Wilson score confidence intervals:

| Method | TP | FP | TN | FN | Accuracy | FPR | Precision (95% CI) | Recall (95% CI) | F1-Score | PR-AUC | False Alarms / Hr |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Narrow Rules** | 40 | 0 | 200 | 80 | 0.7500 | 0.0000 | 1.0000 [0.9124, 1.0000] | 0.3333 [0.2553, 0.4217] | 0.5000 | N/A | 0.00 |
| **Resource-Only Rules** | 80 | 0 | 200 | 40 | 0.8750 | 0.0000 | 1.0000 [0.9542, 1.0000] | 0.6667 [0.5783, 0.7447] | 0.8000 | N/A | 0.00 |
| **Full Operational Rules** | 120 | 0 | 200 | 0 | 1.0000 | 0.0000 | 1.0000 [0.9690, 1.0000] | 1.0000 [0.9690, 1.0000] | 1.0000 | 1.0000 | 0.00 |
| **Isolation Forest** | 57 | 4 | 196 | 63 | 0.7906 | 0.0200 | 0.9344 [0.8432, 0.9742] | 0.4750 [0.3878, 0.5637] | 0.6298 | 0.8034 | 14.40 |
| **LSTM Autoencoder** | 120 | 2 | 198 | 0 | 0.9938 | 0.0100 | 0.9836 [0.9422, 0.9955] | 1.0000 [0.9690, 1.0000] | 0.9917 | 0.9998 | 7.20 |
| **Combined Alert** | 120 | 2 | 198 | 0 | 0.9938 | 0.0100 | 0.9836 [0.9422, 0.9955] | 1.0000 [0.9690, 1.0000] | 0.9917 | N/A | 7.20 |

---

## 3. Scenario-by-Scenario Sensitivity Audit

Breakdown across the six synthetic failure archetypes ($N = 20$ replicates each):

| Scenario ID | Architectural Failure Description | Narrow Rules Recall | Resource-Only Rules Recall | Full Operational Rules Recall | Isolation Forest Recall | LSTM Autoencoder Recall |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **INC-1001** | Payment API connection pool exhaustion | 0.0% (0/20) | 0.0% (0/20) | 100.0% (20/20) | 5.0% (1/20) | 100.0% (20/20) |
| **INC-1002** | Customer DB service unavailable | 100.0% (20/20) | 100.0% (20/20) | 100.0% (20/20) | 25.0% (5/20) | 100.0% (20/20) |
| **INC-1003** | Production server CPU saturation | 0.0% (0/20) | 100.0% (20/20) | 100.0% (20/20) | 80.0% (16/20) | 100.0% (20/20) |
| **INC-1004** | Storage disk capacity exhausted | 0.0% (0/20) | 100.0% (20/20) | 100.0% (20/20) | 70.0% (14/20) | 100.0% (20/20) |
| **INC-1005** | Auth token validation failure | 0.0% (0/20) | 0.0% (0/20) | 100.0% (20/20) | 45.0% (9/20) | 100.0% (20/20) |
| **INC-1006** | Service-to-service timeouts | 100.0% (20/20) | 100.0% (20/20) | 100.0% (20/20) | 60.0% (12/20) | 100.0% (20/20) |

### Key Findings from Scenario Breakdown
1. **Physical Resource Blindspots**: Narrow Rules miss 4 out of 6 failure modes (INC-1001, INC-1003, INC-1004, INC-1005) because latency remains below 1000 ms and memory remains below 95%. Resource-Only Rules recover INC-1003 (CPU) and INC-1004 (Disk), but remain completely blind to INC-1001 (connection pooling) and INC-1005 (auth degradation).
2. **Error-Rate Dominance**: In the synthetic simulator, all 6 failure modes inject probe errors exceeding 0.5%, causing Full Operational Rules to achieve 100% recall.
3. **Temporal Sensitivity**: The LSTM Autoencoder detects 100% of all scenarios based on multivariate temporal trajectory disruption, without needing explicit error-rate thresholding.

---

## 4. Evaluation of Temporal Latency and Detection Delay

### 4.1 False Alarm Rate Derivation
- Telemetry sampling frequency: $\Delta t = 5\text{ seconds}$ per observation.
- Step conversion factor: $3600\text{ s} / 5\text{ s} = 720\text{ observations per hour}$.
- False alarms per hour is computed as: $\text{FPR} \times 720$.
- Full Rules: $0 / 200 \times 720 = 0.0\text{ alarms/hr}$.
- Isolation Forest: $4 / 200 \times 720 = 14.4\text{ alarms/hr}$.
- LSTM Autoencoder: $2 / 200 \times 720 = 7.2\text{ alarms/hr}$.

### 4.2 Detection Delay Reality Check
- `detection_predictions.csv` records `delay_steps = 0.0` for all 120 incident rows.
- **Audit Clarification**: In Experiment A, evaluation is performed offline on static 24-step windows where fault injection occurs at step 16 (the final 8 steps contain fault dynamics). Detection is evaluated on the full window at step 23.
- Because the evaluation classifies whole windows rather than evaluating a streaming step-by-step sequential sequential-probability-ratio test, `delay_steps = 0.0` reflects immediate window-level detection, **not** continuous real-time detection latency. Claims of sub-step temporal latency must not be made.

---

## 5. Paired Statistical Hypothesis Tests

1. **LSTM Autoencoder vs. Isolation Forest**:
   - Contingency Table: $a = 57$ (both detect), $b = 63$ (LSTM detects, Iso misses), $c = 0$ (Iso detects, LSTM misses), $d = 0$ (both miss).
   - Discordant pairs: $b = 63, c = 0$.
   - Exact McNemar Test:
     $$p = \left(\frac{1}{2}\right)^{63} \sum_{k=63}^{63} \binom{63}{k} = 2.168 \times 10^{-19} < 0.001$$
   - Edwards Continuity-Corrected $\chi^2$:
     $$\chi^2 = \frac{(|63 - 0| - 1)^2}{63 + 0} = \frac{62^2}{63} = 61.016 \quad (p = 5.66 \times 10^{-15})$$
   - Conclusion: The recall advantage of the LSTM Autoencoder is statistically significant ($p < 10^{-18}$).

2. **LSTM Autoencoder vs. Full Operational Rules**:
   - Incident Recall: Both achieve 120/120 detections ($b = 0, c = 0 \implies p = 1.000$).
   - False Positives on Normal Windows: LSTM has 2 FP, Rules has 0 FP ($b = 0, c = 2$).
   - Exact McNemar Test on FPR:
     $$p = 2 \times \binom{2}{0} (0.5)^2 = 0.5000$$
   - Conclusion: The 2 false alarms observed in the LSTM Autoencoder do not represent a statistically significant FPR difference on $N = 200$ normal evaluation windows.
