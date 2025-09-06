@echo off
echo GHST v1.0.0-alpha.3 Installer - Compatibility Fix
echo ================================================
echo.
echo This version fixes Python compatibility issues!
echo.
echo Starting professional graphical installer...
echo.
python ghst_installer.py
if errorlevel 1 (
    echo.
    echo Error: Installation failed
    echo Please check that Python 3.6+ is installed
    echo.
    echo If you see capture_output errors, this version should fix them!
    echo.
)
pause
