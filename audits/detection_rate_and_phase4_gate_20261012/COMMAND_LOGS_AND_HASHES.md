# AegisOps: Command Execution Logs and Artifact Checksums

**Audit Gate**: Final Detection Rate Audit and Phase 4 Readiness Gate  
**Audit Date**: 2026-10-12  
**Audit Directory**: `research/audits/detection_rate_and_phase4_gate_20261012/`  
**Environment**: Python 3.11.9 (`.venv`), Windows 10/11, Git branch `main` (`ec83d2f`)

---

## 1. Verified Command Executions & Exit Codes

### 1.1 Complete Regression Suite (`pytest`)
- **Command**: `.\.venv\Scripts\python.exe -m pytest -q`
- **Working Directory**: `c:\DL_PROJECT`
- **Result**: `42 passed in 16.67s` (100% pass rate)
- **Exit Code**: **`0`**

### 1.2 Full Unified Research Runner (`research/run_all.py`)
- **Command**: `.\.venv\Scripts\python.exe research/run_all.py`
- **Working Directory**: `c:\DL_PROJECT`
- **Result**: All 5 pipeline steps executed successfully in 52.7s
- **Exit Code**: **`0`**

### 1.3 Two-Run Deterministic Reproducibility Verification
- **Command**: `.\.venv\Scripts\python.exe scratch/run_two_run_reproducibility.py`
- **Result**: Thresholds (-0.018694), predictions, metrics, and figure images bit-for-bit identical
- **Exit Code**: **`0`**

### 1.4 Rate Denominator & Corrected Metrics Generator
- **Command**: `.\.venv\Scripts\python.exe scratch/generate_corrected_metrics.py`
- **Result**: `research/audits/detection_rate_and_phase4_gate_20261012/CORRECTED_DETECTION_METRICS.csv` generated
- **Exit Code**: **`0`**

---

## 2. Artifact SHA-256 Checksums

### 2.1 Newly Produced Audit Deliverables
| Artifact Path | Size (Bytes) | SHA-256 Checksum |
| :--- | :---: | :--- |
| `CORRECTED_DETECTION_METRICS.csv` | 1,251 | `0dec30a21b954d8e7041b51dc4bb98800685130963a8459523f04c9993255452` |
| `WINDOW_EXPOSURE_AND_ALARM_RATE_AUDIT.md` | 6,587 | `d906b8adc8d5cd5f50816e98fb6d83bb280859e5ae38c1c226774229b31d709c` |
| `STATISTICAL_ASSUMPTION_REVIEW.md` | 5,309 | `6291ddd95302a03b94082f7d013a94e8fe7d3e6eab0da0221324eb291772b718` |
| `PHASE4_READINESS_REVIEW.md` | 7,235 | `d70fe2d1de3356fbec7e1839c942b171fe98212456124c9e3851f0e3b76dd32b` |
| `UPDATED_SEVEN_PHASE_CHECKLIST.md` | 8,224 | `8063943cc6c930184a98b7b8b8d38ef4d563c13120dea7501677fb3639482d4b` |

### 2.2 Primary Underlying Prediction and Model Checksums
| Core Repository Artifact | Size (Bytes) | SHA-256 Checksum |
| :--- | :---: | :--- |
| `research/results/detection_predictions.csv` | 33,656 | `246e14f8b84b8b89e3bb8e3767852db2ae59e21e427210e42353380489aa21ff` |
| `research/results/detection_metrics.csv` | 1,073 | `ed5775303f74156dfaa39eeecddf1fc6766ea9d3b38466185dbeaa0e2bceb8c4` |
| `research/raw/diagnosis_predictions.csv` | 9,933 | `c0faae8805ff0c7c88089ae196f7902bb31ca7a2b9f33bf705da93c66bfcbdf5` |
| `research/raw/diagnosis_metrics.csv` | 1,326 | `d85507106093847b30c9df76fe9bf764121da6a8b139aa2bcba2d8327e5e3153` |
| `research/raw/safety_metrics.csv` | 280 | `18a666576fa1cbeab8d960f9e984534a6ef5370d024aa8657659424c7f0db43d` |
| `models/lstm_autoencoder.pt` | 15,311 | `ef32b7ef5d3b6f9628fe79740e53a3fa2e9aee21183c50974ad0518349dff430` |
| `data/aegisops_live.sqlite3` | 86,016 | `b8f33f63116ca4d081b8544f128e4e941ce0ce6fef39ff4f7e2c918ee0e94ff1` |
