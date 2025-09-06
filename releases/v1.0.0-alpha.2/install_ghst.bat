@echo off
echo GHST v1.0.0-alpha.2 Installer
echo ============================
echo.
echo Starting professional graphical installer...
echo.
python ghst_installer.py
if errorlevel 1 (
    echo.
    echo Error: Python installation failed
    echo Please ensure Python is installed and in your PATH
    echo.
)
pause
