@echo off
setlocal
if not exist .venv (
    python -m venv .venv
    if errorlevel 1 goto :error
)
call .venv\Scripts\activate
python -m pip install --upgrade pip
if errorlevel 1 goto :error
pip install -r requirements.txt
if errorlevel 1 goto :error
if not exist .env copy .env.example .env
if not exist models\lstm_autoencoder.pt (
    python -m dl.train_model
    if errorlevel 1 goto :error
)
echo.
echo Starting AegisOps Live Monitoring. Groq API key is optional; offline agent behavior works without it.
echo.
streamlit run app.py
goto :eof
:error
echo Setup failed. Check the error above and confirm your Python/pip installation.
pause
exit /b 1
