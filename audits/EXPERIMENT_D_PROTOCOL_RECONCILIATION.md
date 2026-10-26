# AegisOps: Experiment D Protocol Reconciliation Report

**Document Path**: `research/audits/EXPERIMENT_D_PROTOCOL_RECONCILIATION.md`  
**Date**: October 13, 2026  
**Auditor**: Senior Research Supervisor, ML Engineer & Reproducibility Auditor  
**Baseline Protocol**: [`research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md) (Protocol v1.1.0 Frozen)  
**Proposed Amendment**: [`research/audits/PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md`](file:///c:/DL_PROJECT/research/audits/PROTOCOL_AMENDMENT_V1_2_PROPOSAL.md) (Protocol v1.2.0 Proposal)  
**Target Benchmark**: AnoMod (MSR 2026, Zenodo record `18342898`)  
**Status**: **RECONCILED — AMENDMENT PROPOSED — FORMAL RATIFICATION PENDING**

---

## 1. Executive Summary

This document provides the formal audit reconciliation between the frozen **External Evaluation Protocol v1.1.0** and the empirical characteristics of the acquired **AnoMod** benchmark. 

The empirical inspection of AnoMod revealed multiple discrepancies between assumptions in Protocol v1.1.0 and the real telemetry files:
1. **Missing Authoritative Latency File**: Table 4.1 in Protocol v1.1.0 specified `api_responses/response_time.log`. This file does not exist in the unpackaged archive. Tracing spans (`all_traces.csv` in SocialNetwork, SkyWalking JSON in TrainTicket) represent the ground-truth latency source.
2. **Feature Distribution Mismatch**: Protocol v1.1.0 mandated Min-Max normalization $[0, 1]$ computed on nominal warmup. The frozen LSTM autoencoder checkpoint (`models/lstm_autoencoder.pt`) was trained strictly on standardized data ($\mu=0, \sigma=1$). Min-Max inputs into the LSTM cause extreme gate saturation and severe false anomaly scores.
3. **Telemetry Burstiness**: SocialNetwork client requests occur in bursts, resulting in 14 to 46 empty 15-second windows ($N_{\text{req}} = 0$) per scenario. Zero cannot be imputed for latency.
4. **TrainTicket Trace Truncation**: SkyWalking traces exist only for the final 203 seconds of the 765-second run (first 548 seconds missing traces).

---

## 2. Protocol Clause-by-Clause Reconciliation Matrix

| Protocol Dimension | Frozen Protocol v1.1.0 Clause | Empirical Finding in AnoMod | Reconciled Specification (Proposed v1.2.0) | Implementation Status in `run_experiment_d.py` | Scientific Gate Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Normalization** | Min-Max scaling $\tilde{\mathbf{x}}_t \in [0, 1]$ on nominal warmup. | Frozen model trained on standardized $\mathcal{N}(0, 1)$ inputs. Min-Max causes severe gate saturation. | Domain-specific Z-score standardization on nominal baseline: $\tilde{\mathbf{x}}_t = (\mathbf{x}_t - \boldsymbol{\mu}_{\text{normal}}^{\text{ext}}) / \boldsymbol{\sigma}_{\text{normal}}^{\text{ext}}$. | Implemented via `fit_calibration_scaler()` and scaled inference in `run_evaluation_pipeline()`. | **PENDING SUPERVISOR RATIFICATION** |
| **2. Client Latency Source** | P95 latency from `api_responses/response_time.log`. | `response_time.log` does not exist in extracted AnoMod archive. | P95 latency computed from distributed trace spans: `all_traces.csv` (`duration_us` / 1000.0) in SN; SkyWalking `duration_ms` in TT. | Implemented via `extract_sn_telemetry()` and `extract_tt_telemetry()`. | **VERIFIED IN CODE & TESTS** |
| **3. Zero-Request Windows** | Assumed continuous synchronous traffic. | Workload is bursty; 14 to 46 empty 15s intervals per scenario ($N_{\text{req}} = 0$). | Intervals with $N_{\text{req}} = 0$ marked `NaN` (undefined). Contiguous windowing rejects gaps; zero latency imputation strictly forbidden. | Implemented via `build_contiguous_windows()` resetting buffer on missing values. | **VERIFIED IN CODE & TESTS** |
| **4. TrainTicket Cohort Scope** | Primary co-evaluation of SocialNetwork and TrainTicket. | SkyWalking traces exist only for final 203s (8 normal windows, 0-6 fault windows). | Designate SocialNetwork as Primary Cohort ($K=12$ faults); relegate TrainTicket to secondary exploratory analysis. | Implemented: `run_production_experiment_d()` targets SN primary cohort; TT extraction implemented. | **PENDING SUPERVISOR RATIFICATION** |
| **5. Timestamp Scraping Offsets** | Assumed synchronized scrape intervals. | Host Prometheus scrapes exhibit fixed 9–14s offsets (CPU :40, Mem :26, Disk :31). | Metric series aligned onto common 15-second epoch grid using nearest-interval rounding (`round("15s")`). | Implemented in `extract_sn_telemetry()` and `extract_tt_telemetry()`. | **VERIFIED IN CODE & TESTS** |
| **6. Error Rate Denominator** | Non-2xx fraction in `api_responses/`. | Client 4xx errors generated continuously by synthetic load generators ($100\%$ nominal rate). | Ratio of HTTP 5xx server errors to total requests recorded in trace spans per 15s window $\times 100.0$. | Implemented in `extract_sn_telemetry()` and `extract_tt_telemetry()`. | **VERIFIED IN CODE & TESTS** |
| **7. CPU Utilization Metric** | Raw CPU counter rate. | TT raw `node_cpu_seconds_total` includes all modes. | SN: Host `system_cpu_usage.csv` direct percentage.<br>TT: `(1 - rate(node_cpu_seconds_total{mode="idle"}[5m]) / n_cores) * 100`. | Implemented in `extract_sn_telemetry()` and `extract_tt_telemetry()`. | **VERIFIED IN CODE & TESTS** |
| **8. Calibration Isolation** | 15-minute warmup inside each fault run ($t < t_{\text{fault}}$). | Fault injection begins within 45–60s in fault runs, precluding intra-run warmup. | Calibration partition sourced strictly from dedicated `Normal_Baseline` run (79 unperturbed steps). | Implemented via `partition_normal_series_chronologically()` with 7-step purge gap. | **VERIFIED IN CODE & TESTS** |

---

## 3. Reconciliation Verdict

The technical and algorithmic reconciliation between Protocol v1.1.0 and the AnoMod dataset is **COMPLETE** in the harness implementation `research/experiments/run_experiment_d.py`. 

However, because the normalization policy changes the formal evaluation contract from Min-Max to Domain Z-Score, **production execution remains BLOCKED** pending formal human supervisor approval and signing of `research/audits/PROTOCOL_AMENDMENT_V1_2_RATIFICATION.json`.
