@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\\Scripts\\python.exe" (
  echo Missing virtual environment. Run run.bat once to install dependencies.
  exit /b 1
)
if not exist ".env" copy ".env.example" ".env" >nul
".venv\\Scripts\\python.exe" -m collectors.worker
