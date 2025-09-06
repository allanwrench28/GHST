@echo off
REM FANTOM Nightly Build Script for Windows
REM ⚠️ WARNING: Use at your own risk - No liability assumed!

echo.
echo ============================================================
echo 🚀 FANTOM NIGHTLY BUILD - WINDOWS
echo ============================================================
echo ⚠️ DISCLAIMER: This script assumes NO LIABILITY
echo ⚠️ Use at your own risk - Verify all outputs
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Run the nightly build script
echo 🔄 Starting FANTOM nightly build process...
python scripts\nightly_build.py

REM Check build result
if errorlevel 1 (
    echo.
    echo ❌ Build failed! Check the output above for errors.
    echo 📋 Check build_report.md for detailed information.
) else (
    echo.
    echo ✅ Build completed successfully!
    echo 📦 Check the dist\ folder for compiled executable
    echo 📋 See build_report.md for full details
)

echo.
echo 👻 Ghost collective monitoring complete
echo ⚠️ Remember: Always review AI-generated code before use!
echo.
pause