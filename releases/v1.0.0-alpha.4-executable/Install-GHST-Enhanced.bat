@echo off
title GHST Enhanced Installer
echo ================================================================
echo    GHST AI Coding Engine - Enhanced Professional Installer
echo ================================================================
echo.
echo Features:
echo    - Cache cleanup and preference preservation
echo    - Automatic update checking from GitHub
echo    - Advanced installation options
echo    - Professional tabbed interface
echo.
echo Starting installer...
echo.

GHST-Installer-Enhanced.exe

if errorlevel 1 (
    echo.
    echo Installation process completed.
    echo.
)

echo.
echo Thank you for choosing GHST!
echo.
pause
