@echo off
REM Build executable using PyInstaller

echo Building Server Activity Monitor executable...

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Build the executable
pyinstaller --onefile --windowed --name "ServerActivityMonitor" ^
    --distpath "./dist" ^
    --buildpath "./build" ^
    --specpath "./build" ^
    --hidden-import=PyQt5 ^
    src/main.py

if errorlevel 1 (
    echo Error building executable
    exit /b 1
)

echo.
echo Build complete!
echo Executable created at: dist\ServerActivityMonitor.exe
echo.
pause
