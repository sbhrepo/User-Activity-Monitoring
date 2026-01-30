@echo off
REM Server Activity Monitor launcher for Windows 11

cd /d "%~dp0"

REM Check if dependencies are installed
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo Dependencies not installed. Running setup...
    call setup.bat
)

REM Run the application
python run.py
pause
