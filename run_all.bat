@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Virtual environment missing. Create .venv and install requirements.txt first.
  pause
  exit /b 1
)
echo Starting the localhost-only AegisOps test service on port 8765...
start "AegisOps Test Service" powershell -NoExit -ExecutionPolicy Bypass -Command "Set-Location -LiteralPath '%~dp0'; .\.venv\Scripts\python.exe -m uvicorn demo_service.main:app --host 127.0.0.1 --port 8765"
timeout /t 2 /nobreak > nul
echo Starting the Streamlit dashboard...
.venv\Scripts\python.exe -m streamlit run app.py
