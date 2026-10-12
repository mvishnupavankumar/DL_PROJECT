# AegisOps: Exact Reproduction Commands and Verification Procedures

**Execution Directory**: `C:\DL_PROJECT`  
**Python Virtual Environment**: `C:\DL_PROJECT\.venv\Scripts\python.exe`  
**Platform**: Windows 11 Pro (`win32` / AMD64)

---

## 1. Environment Verification Commands

```powershell
# Verify Python version and virtual environment
.venv\Scripts\python.exe --version

# Verify key scientific computing and deep learning packages
.venv\Scripts\python.exe -c "import torch, sklearn, scipy, pandas, numpy, streamlit; print('PyTorch:', torch.__version__); print('Sklearn:', sklearn.__version__); print('SciPy:', scipy.__version__); print('Pandas:', pandas.__version__); print('NumPy:', numpy.__version__); print('Streamlit:', streamlit.__version__)"

# Check git revision
git rev-parse HEAD
git status
```

---

## 2. Test Suite Execution Commands

```powershell
# Run the complete test suite (42 tests, 100% passing)
.venv\Scripts\pytest.exe -v

# Run targeted statistical audit tests (includes b=4, c=2 -> p=0.6875 benchmark)
.venv\Scripts\pytest.exe -v test_statistical_audit.py

# Run targeted live monitoring scoping regression test
.venv\Scripts\pytest.exe -v test_live_monitoring.py -k test_build_live_incident_scoping_and_name_error_prevention

# Run authorization and boundary security tests
.venv\Scripts\pytest.exe -v test_approval.py test_target_security.py
```

---

## 3. Experiment Execution Commands

```powershell
# Experiment A: Anomaly Detection Comparison (Rule-based, Isolation Forest, LSTM Autoencoder, Combined)
.venv\Scripts\python.exe research\experiments\run_experiment_a.py

# Experiment B: Root-Cause Diagnosis Benchmark (Multi-tier Rubric & Full Cohort vs Completed cases)
.venv\Scripts\python.exe research\experiments\generate_diagnosis_audit.py

# Experiment C: Execution Safety Boundary & Recovery Verification Audit (Live FastAPI test microservice)
.venv\Scripts\python.exe research\experiments\run_safety_audit.py

# Statistical Analysis & Hypothesis Testing (McNemar exact binomial, Wilson score intervals)
.venv\Scripts\python.exe research\results\generate_statistical_analysis.py

# Unified Pipeline (Runs all experiments and audits end-to-end)
.venv\Scripts\python.exe -m research.run_all
```

---

## 4. Cryptographic Manifest Check

```powershell
# Verify SHA-256 hashes of frozen models, databases, and output tables
.venv\Scripts\python.exe -c "import json, hashlib, pathlib; manifest = json.load(open('research/MANIFEST_SHA256.json')); [print(f'{f}: {hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest() == h}') for f, h in manifest.items() if pathlib.Path(f).exists()]"
```
