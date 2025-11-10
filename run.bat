@echo off
echo ========================================
echo Vendor Management Dashboard Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing/updating dependencies...
pip install -r requirements.txt --quiet

echo.
echo ========================================
echo Starting Vendor Management Dashboard...
echo ========================================
echo.
echo The dashboard will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server.
echo.

streamlit run app.py

