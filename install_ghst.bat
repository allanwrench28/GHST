@echo off
title GHST Installer Launcher
color 0A

echo ==========================================
echo    GHST AI Coding Engine Installer
echo    Version 1.0.0-alpha.1
echo ==========================================
echo.

echo 🚀 Starting GHST Graphical Installer...
echo.

python releases\v1.0.0-alpha.1\ghst_installer.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Installer failed to start
    echo 💡 Make sure Python and PyQt5 are installed
    echo.
    echo Press any key to exit...
    pause >nul
) else (
    echo.
    echo ✅ Installer completed
)

exit /b %ERRORLEVEL%
