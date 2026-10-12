# AegisOps: Bibliographic Reference Verification and Novelty Audit

**Document Path**: `research/paper/REFERENCE_VERIFICATION.md`  
**Git Baseline**: `ec83d2fe501ba50f56839944ba7bd6347544f585` (Branch: `main`)  
**Audit Standard**: Authoritative Primary Scholarly Verification & Defensible Novelty Boundaries  
**Date**: October 2026  

---

## 1. Executive Summary & Verification Protocol

Every bibliographic citation in [`research/paper/AEGISOPS_RESEARCH_PAPER.md`](file:///c:/DL_PROJECT/research/paper/AEGISOPS_RESEARCH_PAPER.md) has been cross-checked against authoritative digital registries: IEEE Xplore, ACM Digital Library, arXiv, Springer Nature, Crossref, and the National Institute of Standards and Technology (NIST).

### Critical Corrections from Prior Drafts:
1. **Eadro (Lee et al., ICSE 2023)**: Authors corrected from inaccurate placeholder names to the verified primary author team: *Cheryl Lee, Tianyi Yang, Zhuangbin Chen, Yuxin Su, and Michael R. Lyu* (CUHK & Sun Yat-sen Univ.).
2. **AnoMod (Ping et al., MSR 2026, arXiv:2601.22881)**: Authors corrected from placeholder names to the verified primary author team: *Ke Ping, Hamza Bin Mazhar, Yuqing Wang, Ying Song, and Mika V. Mäntylä* (University of Helsinki).
3. **Time Series Benchmark Flaws (Wu & Keogh, TKDE 2021)**: Authors corrected from three authors to the verified two authors: *Renjie Wu and Eamonn J. Keogh* (UC Riverside).
4. **CloudRCA (Zhang et al., CIKM 2021)**: Publication metadata resolved to *Yingying Zhang, Zhengxiong Guan, Huajie Qian, Leili Xu, Hengbo Liu, Qingsong Wen, Liang Sun, Junwei Jiang, Lunting Fan, and Min Ke* (CIKM '21, DOI: 10.1145/3459637.3481903, arXiv: 2111.03753), eliminating an unverified placeholder citation.
5. **MicroRCA (Wu et al., NOMS 2020)**: Corrected title to *"MicroRCA: Root Cause Localization of Performance Issues in Microservices"*, verified author list (*Li Wu, Johan Tordsson, Erik Elmroth, Odej Kao*), and verified DOI (*10.1109/NOMS47738.2020.9110353*).

---

## 2. Complete Bibliographic Verification Register

### Reference 1: USAD (Audibert et al., 2020)
- **Full Citation**: Audibert, J., Michiardi, P., Guyard, F., Marti, S., & Zuluaga, M. A. (2020). USAD: UnSupervised Anomaly Detection on Multivariate Time Series. *Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (KDD '20)*, pp. 3395–3404.
- **Identifier**: DOI: [10.1145/3394486.3403392](https://doi.org/10.1145/3394486.3403392)
- **Registry Check**: Verified in ACM Digital Library.
- **Paper Context**: Unsupervised multivariate time-series anomaly detection architectures and adversarial autoencoders.

### Reference 2: Edwards Continuity Correction (Edwards, 1948)
- **Full Citation**: Edwards, A. L. (1948). Note on the "correction for continuity" in testing the significance of the difference between correlated proportions. *Psychometrika*, 13(3), pp. 185–187.
- **Identifier**: DOI: [10.1007/BF02289261](https://doi.org/10.1007/BF02289261)
- **Registry Check**: Verified in Springer / Psychometric Society archives.
- **Paper Context**: Continuity correction for McNemar's paired binary proportion test.

### Reference 3: MetaGPT (Hong et al., 2024)
- **Full Citation**: Hong, S., Zhuge, M., Chen, J., Zheng, X., Cheng, Y., Wang, J., Zhang, C., Wang, Z., Yau, S. K. S., Lin, Z., Zhou, L., Ran, C., Xiao, L., & Wu, C. (2024). MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework. *The Twelfth International Conference on Learning Representations (ICLR 2024)*.
- **Identifier**: arXiv: [2308.00352](https://arxiv.org/abs/2308.00352)
- **Registry Check**: Verified in ICLR / OpenReview / arXiv.
- **Paper Context**: Multi-agent collaborative frameworks and standard operating procedures (SOPs).

### Reference 4: Rigorous Evaluation of Time-Series AD (Kim et al., 2022)
- **Full Citation**: Kim, S., Choi, K., Choi, H., Lee, B., & Yoon, S. (2022). Towards a Rigorous Evaluation of Time-Series Anomaly Detection. *Proceedings of the AAAI Conference on Artificial Intelligence*, 36(7), pp. 7194–7201.
- **Identifier**: DOI: [10.1609/aaai.v36i7.20680](https://doi.org/10.1609/aaai.v36i7.20680)
- **Registry Check**: Verified in AAAI Digital Library.
- **Paper Context**: Critique of point-adjustment tricks and inflated F1 scores in time-series anomaly detection evaluation.

### Reference 5: Eadro (Lee et al., 2023)
- **Full Citation**: Lee, C., Yang, T., Chen, Z., Su, Y., & Lyu, M. R. (2023). Eadro: An End-to-End Troubleshooting Framework for Microservices on Multi-source Data. *Proceedings of the 45th IEEE/ACM International Conference on Software Engineering (ICSE '23)*, pp. 1955–1967.
- **Identifier**: DOI: [10.1109/ICSE48619.2023.00165](https://doi.org/10.1109/ICSE48619.2023.00165)
- **Registry Check**: Verified in IEEE Xplore.
- **Paper Context**: Multi-source troubleshooting framework for microservices integrating logs, metrics, and traces via end-to-end multi-task learning.

### Reference 6: Isolation Forest (Liu et al., 2008)
- **Full Citation**: Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation Forest. *Proceedings of the 2008 Eighth IEEE International Conference on Data Mining (ICDM '08)*, pp. 413–422.
- **Identifier**: DOI: [10.1109/ICDM.2008.17](https://doi.org/10.1109/ICDM.2008.17)
- **Registry Check**: Verified in IEEE Xplore.
- **Paper Context**: Classical tree-based anomaly isolation baseline.

### Reference 7: LSTM Autoencoder (Malhotra et al., 2016)
- **Full Citation**: Malhotra, P., Ramakrishnan, A., Anand, G., Vig, L., Agarwal, P., & Shroff, G. (2016). LSTM-based Encoder-Decoder for Multi-sensor Anomaly Detection. *ICML 2016 Workshop on Anomaly Detection (ADW 2016)*.
- **Identifier**: arXiv: [1607.00148](https://arxiv.org/abs/1607.00148)
- **Registry Check**: Verified in arXiv repository.
- **Paper Context**: Recurrent sequence-to-sequence reconstruction autoencoders for multi-sensor anomaly detection.

### Reference 8: McNemar Test (McNemar, 1947)
- **Full Citation**: McNemar, Q. (1947). Note on the sampling error of the difference between correlated proportions or percentages. *Psychometrika*, 12(2), pp. 153–157.
- **Identifier**: DOI: [10.1007/BF02295996](https://doi.org/10.1007/BF02295996)
- **Registry Check**: Verified in Springer / Psychometric Society archives.
- **Paper Context**: Nonparametric paired hypothesis testing on discordant classification outcomes.

### Reference 9: NIST SP 800-53 Rev 5 (NIST, 2020)
- **Full Citation**: National Institute of Standards and Technology (NIST). (2020). *Security and Privacy Controls for Information Systems and Organizations*. NIST Special Publication 800-53, Revision 5.
- **Identifier**: DOI: [10.6028/NIST.SP.800-53r5](https://doi.org/10.6028/NIST.SP.800-53r5)
- **Registry Check**: Verified in NIST Computer Security Resource Center.
- **Paper Context**: Standards for dual authorization (two-man rule), audit accountability, and least-privilege command barriers.

### Reference 10: AnoMod (Ping et al., 2026)
- **Full Citation**: Ping, K., Bin Mazhar, H., Wang, Y., Song, Y., & Mäntylä, M. V. (2026). AnoMod: A Dataset for Anomaly Detection and Root Cause Analysis in Microservice Systems. *Proceedings of the 23rd IEEE/ACM International Conference on Mining Software Repositories (MSR '26)*, pp. 677–681.
- **Identifier**: arXiv: [2601.22881](https://arxiv.org/abs/2601.22881)
- **Registry Check**: Verified in arXiv / MSR 2026 repository.
- **Paper Context**: Standardized microservice benchmark dataset providing logs, metrics, traces, API responses, and code coverage across multi-class injected faults.

### Reference 11: OmniAnomaly (Su et al., 2019)
- **Full Citation**: Su, Y., Zhao, Y., Niu, C., Liu, R., Sun, W., & Pei, D. (2019). Robust Anomaly Detection for Multivariate Time Series through Stochastic Recurrent Neural Networks. *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (KDD '19)*, pp. 2828–2837.
- **Identifier**: DOI: [10.1145/3292500.3330672](https://doi.org/10.1145/3292500.3330672)
- **Registry Check**: Verified in ACM Digital Library.
- **Paper Context**: Stochastic recurrent neural networks and latent planar normalizing flows for multivariate time series anomaly detection.

### Reference 12: CloudRCA (Zhang et al., 2021)
- **Full Citation**: Zhang, Y., Guan, Z., Qian, H., Xu, L., Liu, H., Wen, Q., Sun, L., Jiang, J., Fan, L., & Ke, M. (2021). CloudRCA: A Root Cause Analysis Framework for Cloud Computing Platforms. *Proceedings of the 30th ACM International Conference on Information and Knowledge Management (CIKM '21)*, pp. 3637–3641.
- **Identifier**: DOI: [10.1145/3459637.3481903](https://doi.org/10.1145/3459637.3481903); arXiv: [2111.03753](https://arxiv.org/abs/2111.03753)
- **Registry Check**: Verified in ACM Digital Library / arXiv.
- **Paper Context**: Multimodal root-cause analysis framework for large cloud infrastructure combining metric aggregation and anomaly correlation.

### Reference 13: Wilson Score Interval (Wilson, 1927)
- **Full Citation**: Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. *Journal of the American Statistical Association*, 22(158), pp. 209–212.
- **Identifier**: DOI: [10.1080/01621459.1927.10502953](https://doi.org/10.1080/01621459.1927.10502953)
- **Registry Check**: Verified in Taylor & Francis / JASA.
- **Paper Context**: Asymmetric binomial confidence interval for small-sample, extreme-proportion security evaluation ($11/11$ blocked attacks).

### Reference 14: Time Series Benchmark Flaws (Wu & Keogh, 2021)
- **Full Citation**: Wu, R., & Keogh, E. J. (2021). Current Time Series Anomaly Detection Benchmarks are Flawed and are Creating the Illusion of Progress. *IEEE Transactions on Knowledge and Data Engineering*, 35(3), pp. 2421–2429.
- **Identifier**: DOI: [10.1109/TKDE.2021.3112126](https://doi.org/10.1109/TKDE.2021.3112126)
- **Registry Check**: Verified in IEEE Xplore.
- **Paper Context**: Critical methodological assessment exposing trivial baselines, point-adjustment illusions, and synthetic benchmark vulnerabilities in time-series anomaly detection literature.

### Reference 15: MicroRCA (Wu et al., 2020)
- **Full Citation**: Wu, L., Tordsson, J., Elmroth, E., & Kao, O. (2020). MicroRCA: Root Cause Localization of Performance Issues in Microservices. *Proceedings of the 2020 IEEE/IFIP Network Operations and Management Symposium (NOMS 2020)*, pp. 1–9.
- **Identifier**: DOI: [10.1109/NOMS47738.2020.9110353](https://doi.org/10.1109/NOMS47738.2020.9110353)
- **Registry Check**: Verified in IEEE Xplore.
- **Paper Context**: Attributed graph modeling and personalized PageRank for root cause localization in containerized microservices.

### Reference 16: AutoGen (Wu et al., 2023)
- **Full Citation**: Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang, S., Liu, J., Awadallah, A. H., White, R. W., Burger, D., & Wang, C. (2023). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. *arXiv preprint*.
- **Identifier**: arXiv: [2308.08155](https://arxiv.org/abs/2308.08155)
- **Registry Check**: Verified in arXiv.
- **Paper Context**: Multi-agent conversational patterns and dynamic execution architectures.

---

## 3. Disentangling Prior Art from Proposed Novelty

To prevent unsupported novelty claims, this section delineates what is verified from existing literature versus what AegisOps introduces and substantiates.

```
+--------------------------------------------------------------------------------------------------+
|                                    ESTABLISHED LITERATURE                                        |
+------------------------------------+------------------------------------+------------------------+
| Multivariate Anomaly Detection     | Root Cause Analysis (RCA)          | Agentic Systems        |
| - LSTM Autoencoders                | - Attributed graph walks           | - Multi-agent debate   |
|   (Malhotra et al., 2016)          |   (MicroRCA: Wu et al., 2020)      |   (AutoGen: Wu et al.) |
| - Adversarial training (USAD)      | - Multi-source correlation         | - SOP metaprogramming  |
| - Benchmark pitfalls (Keogh 2021)  |   (Eadro: Lee et al., 2023)        |   (MetaGPT: Hong et al)|
+------------------------------------+------------------------------------+------------------------+
                                                 |
                                                 v
+--------------------------------------------------------------------------------------------------+
|                                     AEGISOPS CONTRIBUTIONS                                       |
+------------------------------------+------------------------------------+------------------------+
| 1. Two-Stage Detection Coupling    | 2. Feature Attribution Handoff     | 3. Bounded Execution   |
| - Rule safety ceiling + deep MSE   | - Per-feature MSE vectors passed   | - Cryptographic nonce  |
| - Defense-in-depth gate            |   directly to LLM agent prompt     | - Atomic 2-man rule    |
| - Rigorous window-level evaluation | - Hybrid quantitative/qualitative  | - Closed-loop /probe   |
+------------------------------------+------------------------------------+------------------------+
                                                 |
                                                 v
+--------------------------------------------------------------------------------------------------+
|                                   DEFENSIBLE BOUNDARIES                                          |
+------------------------------------+------------------------------------+------------------------+
| - Zero additive statistical        | - Multi-agent LLM did NOT beat     | - Security proven on   |
|   sensitivity on synthetic data    |   deterministic rule baseline      |   local loopback only  |
| - Benchmark is synthetically       | - N=6 scenario sample size has     | - Does not guarantee   |
|   generated; external validation   |   low statistical power (1-b~0.14) |   Byzantine cloud-wide |
|   remains future work              | - Rubric test-set leakage disclosed|   consensus            |
+------------------------------------+------------------------------------+------------------------+
```

### Boundary 1: Anomaly Detection Architecture
- **Prior Art**: Malhotra et al. (2016) established LSTM sequence-to-sequence autoencoders; Audibert et al. (2020) and Su et al. (2019) introduced adversarial and variational extensions; Wu & Keogh (2021) and Kim et al. (2022) exposed point-adjustment fallacies and trivial thresholds.
- **AegisOps Implementation**: Employs an LSTM Autoencoder with a calibrated reconstruction threshold ($\tau = 0.709399$) alongside hard operational rules.
- **Defensible Novelty Claim**: AegisOps does *not* claim a novel deep neural architecture. The contribution is the architectural coupling: using the continuous per-feature MSE attribution vector as a structured diagnostic artifact for downstream LLM reasoning, while maintaining hard static bounds for instantaneous threshold excursions.
- **Claim Boundary**: The combined detector provided zero additive statistical sensitivity over standalone LSTM on the synthetic benchmark. Generalization to unstructured production environments is not claimed without real-world telemetry validation.

### Boundary 2: Root-Cause Analysis and Multi-Agent Reasoning
- **Prior Art**: Graph-based RCA (Wu et al., 2020; Zhang et al., 2021) and multi-source trace/log analysis (Lee et al., 2023) require explicit causality graphs or end-to-end training. Multi-agent LLMs (Hong et al., 2024; Wu et al., 2023) demonstrate conversational decomposition.
- **AegisOps Implementation**: A four-agent pipeline (Investigator, Correlator, Hypothesis Tester, Supervisor) that ingests reconstruction error vectors and incident metadata.
- **Defensible Novelty Claim**: Demonstrating that neural metric reconstruction errors can be directly grounded in multi-agent natural language reasoning to produce interpretable, structured incident assessments.
- **Claim Boundary**: Multi-agent LLMs did **not** outperform the deterministic rule baseline (LLM: 83.33% ITT strict; Rule baseline: 100.0% strict in 0.01 ms). The $N=6$ evaluation is bounded as an exploratory feasibility pilot with low power ($1-\beta \approx 0.14$) and disclosed rubric leakage.

### Boundary 3: Autonomous Remediation and Execution Safety
- **Prior Art**: Classical SRE runbooks automate scripts without semantic reasoning; unconstrained LLM agent systems risk executing destructive arbitrary shell commands. NIST SP 800-53 defines two-man authorization principles.
- **AegisOps Implementation**: A closed-loop execution boundary requiring signed cryptographic nonces (UUIDv4), expiration TTL (300s), atomic SQLite state transitions (`BEGIN IMMEDIATE`), allowlisted action templates, and post-execution `/probe` verification.
- **Defensible Novelty Claim**: The end-to-end architectural integration of automated diagnosis with a cryptographically enforced, non-bypassable two-man rule approval gate and active remediation verification.
- **Claim Boundary**: The 100% containment ($11/11$ blocked attacks, 95% Wilson CI: $[0.7412, 1.0000]$) is strictly bounded to the local application loopback boundary (`127.0.0.1:8765`). It does not claim protection against operating system compromise, kernel exploits, or distributed Byzantine multi-tenant attacks.

---

## 4. Verification Sign-Off

All 16 bibliographic references have been verified against authoritative scholarly registries with active DOIs and arXiv identifiers. Novelty boundaries have been rigorously circumscribed to match the empirical evidence in the AegisOps repository.
