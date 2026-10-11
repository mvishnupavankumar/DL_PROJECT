# AegisOps — Start Here

AegisOps now opens directly into **Live Monitoring**. The synthetic Incident Demo workspace has been removed from the dashboard navigation.

Live Monitoring collects actual CPU, memory, and disk readings from the collector host, plus HTTP probe latency/status/error-rate measurements from a configured service endpoint. Remote endpoints must use HTTPS; an optional bearer token is supported. It stores observations in SQLite and can train a separate LSTM checkpoint from eligible healthy observations. Remediation is restricted to resetting the fault mode of this project's local test service after explicit approval.

## One-time setup on Windows

Open PowerShell inside the extracted `AegisOps` folder:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

## Start live monitoring

**Recommended:** run this from the project folder after installing requirements:

```powershell
.\\run_all.ps1
```

This opens the local test service in a second PowerShell window and runs Streamlit in the current one. You can also double-click `run_all.bat`.

**Manual option — use two terminals:**

Terminal 1 — local test service:

```powershell
.\\.venv\\Scripts\\Activate.ps1
python -m uvicorn demo_service.main:app --host 127.0.0.1 --port 8765
```

Terminal 2 — dashboard:

```powershell
.\\.venv\\Scripts\\Activate.ps1
python -m streamlit run app.py
```

Open the local URL printed by Streamlit. The dashboard opens directly into Live Monitoring; there is no workspace selector.

Keep the test service bound to `127.0.0.1`. Do not use `--host 0.0.0.0` or expose its admin fault-injection endpoint to the internet/LAN.

## Live-data walkthrough

1. For local testing, confirm the local test service is reachable and set to `normal`. For an authorized remote target, configure `AEGISOPS_SERVICE_URL` and `AEGISOPS_PROBE_PATH` in `.env`; remote targets must use HTTPS.
2. Leave **Collect live metrics every 5 seconds** enabled. A sample records host CPU, memory, disk, HTTP probe latency, response status, rolling probe error rate, and timestamp.
3. Let the service stay healthy while samples are collected. Samples are stored in `data/aegisops_live.sqlite3`; the dashboard can export observations as CSV.
4. Bootstrap rules can alert before the Deep Learning model is trained. The UI labels this mode explicitly; it is not an LSTM prediction.
5. Collect at least **180 eligible healthy samples** before training; **240 or more** is a better first baseline (about 20 minutes at a five-second interval). Do not inject faults during baseline collection.
6. Train using **Train / retrain LSTM from healthy live telemetry**.
7. After training, use **Inject 1.2 s latency** or **Inject HTTP 500** to create a controlled fault in the local test service. Wait for samples, then inspect the alert and LSTM score/guardrail evidence.
8. Click **Run agents on latest live evidence** and review the investigation and diagnosis.
9. To test remediation, tick the explicit approval checkbox and click **Resolve local test-service fault and verify**. The action only resets this project's local fault mode; success depends on actual health/probe checks.
10. Observe the recovery and audit trail.

## Model and data notes

- `models/lstm_autoencoder.pt` is a legacy synthetic-evaluation checkpoint and is not used by the live-only dashboard.
- Live Monitoring writes its separate model to `models/live_lstm_autoencoder.pt`, with metadata in the matching `.json` file.
- `data/aegisops_live.sqlite3` stores local observations and audit events. Keep it private if telemetry contains sensitive details.
- A model trained on one laptop/service is not automatically suitable for another. Collect multiple normal workload periods and evaluate with known faults before drawing conclusions.
- This is a local research prototype. It does not restart arbitrary OS services, run arbitrary commands, modify cloud resources, or change external production systems.

## Tests

Run the software tests:

```powershell
python -m pytest -q
```

`python -m dl.evaluate_detector` remains a synthetic-only legacy smoke test; do not present its metrics as live-monitoring accuracy. Synthetic fixtures and test utilities remain in the repository for regression testing, but they are not available as a dashboard mode.

## Optional LLM agents

The agent workflow runs in deterministic offline mode without an API key. For Groq-backed investigation, put your own key in `.env` as `GROQ_API_KEY=...`, set `GROQ_MODEL` to a model available to your account, and restart Streamlit. Never commit or share `.env`.


## Independent collector process

For monitoring that continues when Streamlit is closed, start a separate process in the same environment:

```powershell
python -m collectors.worker
```

Run only one collector per target/database unless duplicate sampling is intentional. Use an OS service supervisor for unattended execution. Read `OPERATIONS.md` and `SECURITY.md` before a pilot. Remote targets are read-only; fault injection and remediation remain localhost-only.
