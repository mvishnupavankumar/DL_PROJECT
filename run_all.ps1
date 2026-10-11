$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Error "Virtual environment not found. Create .venv and install requirements.txt first."
}
Start-Process powershell -ArgumentList @('-NoExit','-Command', "Set-Location '$root'; .\.venv\Scripts\python.exe -m uvicorn demo_service.main:app --host 127.0.0.1 --port 8765")
Start-Sleep -Seconds 2
& .\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1