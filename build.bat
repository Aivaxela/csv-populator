@echo off
echo Building CSV Populator Executable...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python first.
    echo.
    echo You can download Python from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Python found! Building executable...
echo.

REM Run the build script
python build_exe.py

echo.
echo Build process completed!
pause
