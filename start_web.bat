@echo off
REM Chronos Outreach System - Web Interface Launcher for Windows

echo Starting Chronos Outreach Web Interface...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Check if config exists
if not exist "config.json" (
    echo Configuration not found. Running setup...
    python setup.py
)

REM Launch the web interface
echo.
echo Launching web interface...
echo The app will open at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py --server.headless=true
