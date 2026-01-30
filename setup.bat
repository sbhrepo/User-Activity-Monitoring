@echo off
REM Setup script for Server Activity Monitor on Windows 11

echo Installing Server Activity Monitor...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    exit /b 1
)

echo Python found. Installing dependencies...

REM Install requirements
pip install -r requirements.txt

if errorlevel 1 (
    echo Error installing dependencies
    exit /b 1
)

echo.
echo Installation complete!
echo.
echo To run the application, execute:
echo   python run.py
echo.
echo Or double-click run.bat
pause
