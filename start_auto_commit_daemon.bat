@echo off
echo 🤖 Starting GHST Auto-Commit Daemon...
echo.
echo ✅ User permission granted for automatic commits
echo 📁 Repository: %CD%
echo ⏱️ Check interval: 5 minutes (configurable)
echo 📦 Max batch size: 10MB (configurable)  
echo 📤 Auto-push: Enabled
echo.
echo 💡 The daemon will:
echo    - Monitor for file changes every 5 minutes
echo    - Automatically commit changes in small batches
echo    - Push commits to GitHub automatically
echo    - Log all activity to auto_commit_daemon.log
echo.
echo 🛑 To stop: Press Ctrl+C
echo.
pause

python auto_commit_daemon.py

echo.
echo 👋 Auto-commit daemon stopped
pause
