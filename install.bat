@echo off
title GHST Install Wizard
color 0A

echo.
echo ==========================================
echo    GHST AI CODING ENGINE
echo    Installation and Testing Wizard
echo ==========================================
echo.
echo This wizard will:
echo   - Test all GHST components
echo   - Validate dependencies
echo   - Launch the GUI for testing
echo   - Identify and help fix bugs
echo.
echo Starting GHST Install Wizard...
echo.

python install_wizard.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Install wizard failed to start
    echo Make sure Python is installed and in your PATH
    echo.
    pause
)

echo.
echo Install wizard completed.
pause
