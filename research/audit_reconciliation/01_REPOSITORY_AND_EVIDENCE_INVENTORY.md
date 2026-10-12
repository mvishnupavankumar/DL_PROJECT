# 01 — Repository and Evidence Inventory

**Audit Date**: 2026-10-12  
**Auditor**: Senior ML Experiment Auditor & Software Testing Specialist  
**Target Repository**: `C:\DL_PROJECT`  
**Execution Context**: Pre-Manuscript Evidence Reconciliation and Research Readiness Audit

---

## 1. Version Control & Working Tree State

- **Git Commit SHA**: `8aff34c8249bcef10a3ecc63d7f347f3f0fbb4ef`
- **Active Branch**: `main`
- **Remote Tracking**: `origin/main` (Up to date with `https://github.com/mvishnupavankumar/DL_PROJECT.git`)
- **Working Tree Status**: Clean (Zero uncommitted modifications, zero untracked working files at baseline).
- **Recent Git Log**:
  - `8aff34c` — Phase 2–6 Evidence Reconciliation Gate
  - `11cf0c7` — Updated
  - `e69cb62` — fixed windows integrate issues

---

## 2. Python Environment & Dependency Manifest

- **Python Runtime**: `Python 3.11.9` (`C:\DL_PROJECT\.venv\Scripts\python.exe`)
- **Platform**: `Windows 11 Enterprise` (AMD64)
- **Key Installed Scientific and Application Packages**:

| Package Name | Installed Version | Architectural Role |
| :--- | :--- | :--- |
| `torch` | `2.14.1` | Frozen LSTM Autoencoder inference (`dl/anomaly_detector.py`) |
| `scikit-learn` | `1.9.0` | Baseline Isolation Forest fitting and threshold calibration |
| `scipy` | `1.17.1` | Exact two-sided binomial tests, $\chi^2$ calculations, Wilson CIs |
| `pandas` | `3.0.6` | Telemetry, prediction, and metric dataset processing |
| `numpy` | `2.4.6` | Sliding window tensor transformations and numerical arrays |
| `fastapi` | `0.143.0` | Target microservice harness (`demo_service/main.py`) |
| `uvicorn` | `0.54.0` | ASGI web server for loopback service execution |
| `streamlit` | `1.65.0` | Live monitoring dashboard interface (`app.py`) |
| `groq` | `1.7.0` | Cloud LLM client for agent reasoning (`agents.py`) |
| `psutil` | `7.2.2` | Host workstation CPU, RAM, and disk sampling |
| `pytest` | `9.1.1` | Unit, integration, and security regression test harness |

> [!IMPORTANT]
> **Virtual Environment Prerequisite**: The virtual environment `.venv\Scripts\python.exe` must be used for all script and test execution. Invoking the host global Python interpreter fails on `live_monitoring.py:12` due to an uninstalled `streamlit` dependency in the global environment.

---

## 3. Experiment Scripts & Execution Entry Points

| Script Path | Entry Point Function | Purpose & Operational Execution Scope | Execution Mode |
| :--- | :--- | :--- | :--- |
| [`research/run_all.py`](file:///c:/DL_PROJECT/research/run_all.py) | `main()` | Master reproducible research pipeline runner. Orchestrates tests, Exp A, diagnosis audit, Exp C, statistics, and SHA-256 manifest. | End-to-End Orchestrator |
| [`research/experiments/run_experiment_a.py`](file:///c:/DL_PROJECT/research/experiments/run_experiment_a.py) | `run_experiment_a()` | Experiment A: Benchmarks Operational Rules, Isolation Forest, LSTM Autoencoder, and Combined Alert on $N=320$ synthetic windows. | Offline Deterministic |
| [`research/experiments/run_experiment_b.py`](file:///c:/DL_PROJECT/research/experiments/run_experiment_b.py) | `run_experiment_b()` | Experiment B: Evaluates 7 diagnostic configurations across 6 incident scenarios. Makes live Groq LLM API calls when `GROQ_API_KEY` is set. | Cloud API / Local Fallback |
| [`research/experiments/generate_diagnosis_audit.py`](file:///c:/DL_PROJECT/research/experiments/generate_diagnosis_audit.py) | Top-level script | Standardized 4-tier rubric evaluator for Experiment B predictions. Used by `run_all.py` for deterministic pipeline replay. | Offline Deterministic |
| [`research/experiments/run_safety_audit.py`](file:///c:/DL_PROJECT/research/experiments/run_safety_audit.py) | `run_safety_audit()` | Experiment C: Evaluates 16 safety, authorization, and recovery verification cases against disposable loopback FastAPI service (`:8765`). | Local Loopback / SQLite |
| [`research/results/generate_statistical_analysis.py`](file:///c:/DL_PROJECT/research/results/generate_statistical_analysis.py) | Top-level script | Generates `research/results/statistical_analysis.md` computing exact McNemar tests, continuity-corrected $\chi^2$, and Wilson CIs. | Offline Deterministic |
| [`research_automation.py`](file:///c:/DL_PROJECT/research_automation.py) | `main()` | CLI harness for running automated research trials (`run`, `analyze`). | CLI Subsystem |
| [`research_pipeline.py`](file:///c:/DL_PROJECT/research_pipeline.py) | `main()` | Controlled readiness gate and pre-flight validation harness. | CLI Readiness Gate |

---

## 4. Primary Data, Model, and Checksum Artifacts

| Artifact Category | File Path | File Size | Verified SHA-256 Checksum | Preservation Status |
| :--- | :--- | :---: | :--- | :---: |
| **Model Checkpoint** | [`models/lstm_autoencoder.pt`](file:///c:/DL_PROJECT/models/lstm_autoencoder.pt) | 19,893 B | `df867ce96bf423f03b87441fc9a957270d4944fa734b41a546da9b57564619d0` | Read-only preserved |
| **Model Metadata** | [`models/lstm_autoencoder.json`](file:///c:/DL_PROJECT/models/lstm_autoencoder.json) | 338 B | `e05bbf510b666a2a5ea79c6bb2a9d201083411db1eec780e9a56c4d874558e80` | Read-only preserved |
| **Historical Database** | [`data/aegisops_live.sqlite3`](file:///c:/DL_PROJECT/data/aegisops_live.sqlite3) | 86,016 B | `b8f33f63116ca4d081b8544f128e4e941ce0ce6fef39ff4f7e2c918ee0e94ff1` | Read-only preserved |
| **Incident Catalog** | [`data/incidents.json`](file:///c:/DL_PROJECT/data/incidents.json) | 5,686 B | `b8b54332e6fc9c3a3b0ee461a52fc0d172e9d291916327421e4ae62b608ad2ec` | Read-only preserved |
| **Exp A Predictions** | [`research/raw/detection_predictions.csv`](file:///c:/DL_PROJECT/research/raw/detection_predictions.csv) | 24,357 B | `246e14f8b84b8b89cbfce180fd7722ae82820f516894aa5dd11462866d10cfbb` | Machine-readable record |
| **Exp A Metrics** | [`research/raw/detection_metrics.csv`](file:///c:/DL_PROJECT/research/raw/detection_metrics.csv) | 568 B | `ed5775303f74156d844dc0068db4328e2237fc935a2bca260d613571083de57e` | Machine-readable record |
| **Exp B Predictions** | [`research/raw/diagnosis_predictions.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_predictions.csv) | 11,891 B | `7719bdc39f1bf5d3443f486ec66e2319a02a5f9c13ac3dc2eb61c6fad99d8860` | Machine-readable record |
| **Exp B Metrics** | [`research/raw/diagnosis_metrics.csv`](file:///c:/DL_PROJECT/research/raw/diagnosis_metrics.csv) | 868 B | `c3633e23d7a2fc9efeb093394a9bbd84b40578eab9a15c48c713fbf4fb38f403` | Machine-readable record |
| **Exp C Test Results** | [`research/raw/safety_test_results.csv`](file:///c:/DL_PROJECT/research/raw/safety_test_results.csv) | 3,008 B | `589353e42a422134f11611bea301703bf3afd3c325c74f152e3967d0e2272045` | Machine-readable record |
| **Exp C Metrics** | [`research/raw/safety_metrics.csv`](file:///c:/DL_PROJECT/research/raw/safety_metrics.csv) | 997 B | `65f1a9761d927289dad4d307d50bddc5c178911da38684abc3e43cb3421d3edd` | Machine-readable record |
| **Figure 1** | [`research/figures/detection_confusion_matrices.png`](file:///c:/DL_PROJECT/research/figures/detection_confusion_matrices.png) | 27,954 B | `8a5bb86f671c6ca6b3da27a69b764c919702206085a6aee4fec401a87754f7a2` | Static publication asset |
| **Figure 2** | [`research/figures/detection_comparison.png`](file:///c:/DL_PROJECT/research/figures/detection_comparison.png) | 16,879 B | `96173a11da4f6f890c29ae06fb2ea675cf311e9f168f18073b64c052825bc5fc` | Static publication asset |
| **Manifest** | [`research/MANIFEST_SHA256.json`](file:///c:/DL_PROJECT/research/MANIFEST_SHA256.json) | 4,847 B | Freshly regenerated by `run_all.py` | Tracks 22 repository artifacts |

---

## 5. Verification Status: Primary Evidence vs. Unverified Narrative Claims

A core directive of this audit is to strictly separate empirical machine-readable records from historical narrative claims:

| Research Dimension | Previous Narrative Claim | Raw Underlying Evidence | Audit Verdict |
| :--- | :--- | :--- | :--- |
| **Historical Telemetry** | 175 fault samples across 4 episodes (28, 7, 98, 42). | Exactly 169 fault samples (1 latency + 168 error) and 31 normal samples in `data/aegisops_live.sqlite3`. | **CLAIM DISPROVEN**: Prior claim contained fictional timestamps and 6-sample inflation. Reconciled. |
| **Model Inferences in DB** | Implied that historical database telemetry includes neural LSTM inference scores. | `anomaly_score` is 100% NULL; `detection_mode` is 100% `'bootstrap_rules'`. | **CLAIM DISPROVEN**: Database records cold-start fallback only. Neural inferences were not executed. |
| **Exp A Sensitivity** | LSTM Autoencoder recall is 100.0%, Isolation Forest is 47.5%. | $N = 320$ test windows in `detection_predictions.csv`: LSTM TP=120, IsoForest TP=57. | **VERIFIED FACT**: Statistically significant superiority confirmed ($p = 2.168 \times 10^{-19}$). |
| **Exp A Rules Baseline** | Conflicting reports of 33.3% recall (40 TP) vs. 100.0% recall (120 TP). | Resource-only rules flag 40 TP; script rule including `err > 0.5%` flags 120 TP. | **RECONCILED**: Both valid under distinct operational definitions; distinction must be explicit in paper. |
| **Exp B Evaluation Cohort** | Narrative described 42 evaluated incident cases. | Exactly 6 ground-truth incidents evaluated across 7 configurations ($7 \times 6 = 42$). | **CLAIM CLARIFIED**: Factorial evaluation across 6 scenarios, NOT 42 independent outages. |
| **Exp B Live LLM Drops** | Multi-Agent No-DL reported as 100.0% accuracy ($5/5$) vs. Multi-Agent Full at 83.3% ($5/6$). | Config 7 dropped INC-1004 due to rate limit; Config 5 dropped INC-1002 due to timeout. | **CLAIM CLARIFIED**: Invalid non-equivalent comparison. Full-cohort ITT is 83.3% (Full) vs. 66.7% (No-DL). |
| **Exp C Attack Containment** | "14 of 14 adversarial attacks blocked." | 16-case inventory: 11 attacks, 2 failure checks, 1 verification probe, 2 controls. | **CLAIM RECLASSIFIED**: Conflated failure handling with attacks. Actual attack containment is 11/11 (100.0%). |
| **Automated Reproducibility** | Pipeline regenerates all experiments and publication figures. | `run_all.py` runs tests, Exp A, rubric audit, Exp C, and manifest. Does not call live LLM or generate PNGs. | **VERIFIED WITH CAVEATS**: Fully functional for local reproducibility; figure generation and live LLM excluded. |
