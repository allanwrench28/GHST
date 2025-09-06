@echo off
echo 🤖 GHST Smart Auto-Commit System
echo ===================================
echo.
echo This script will automatically:
echo - Scan for changed files
echo - Create smart commit batches (under 25MB each)
echo - Exclude large binary files automatically
echo - Commit and push in manageable chunks
echo.
echo Press any key to start auto-commit...
pause >nul

python smart_auto_commit.py

echo.
echo ✅ Auto-commit process complete!
echo.
pause
