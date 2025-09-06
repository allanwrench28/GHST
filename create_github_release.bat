@echo off
REM GitHub Release Creation Script for GHST (Windows)
REM This script helps create proper GitHub releases

set VERSION=v1.0.0-alpha.3
set RELEASE_TITLE=GHST v1.0.0-alpha.3 - Python Compatibility Fix

echo 🚀 GHST GitHub Release Creator
echo ==============================
echo.
echo Release: %VERSION%
echo Title: %RELEASE_TITLE%
echo.

REM Check if gh CLI is installed
gh --version >nul 2>&1
if errorlevel 1 (
    echo ❌ GitHub CLI (gh^) is not installed
    echo 📥 Install it from: https://cli.github.com/
    echo.
    echo Manual Release Steps:
    echo 1. Go to: https://github.com/allanwrench28/GHST/releases/new
    echo 2. Select tag: %VERSION%
    echo 3. Release title: %RELEASE_TITLE%
    echo 4. Upload: releases\GHST-%VERSION%-windows.zip
    echo 5. Upload: releases\%VERSION%\ghst_installer.py
    echo 6. Upload: releases\%VERSION%\install_ghst.bat
    echo 7. Copy release notes from: releases\%VERSION%\RELEASE_NOTES.md
    echo 8. Check 'This is a pre-release'
    echo 9. Click 'Publish release'
    pause
    exit /b 1
)

echo ✅ GitHub CLI found, creating release...

REM Create the release
gh release create "%VERSION%" ^
  --title "%RELEASE_TITLE%" ^
  --notes-file "releases\v1.0.0-alpha.3\RELEASE_NOTES.md" ^
  --prerelease ^
  "releases\GHST-v1.0.0-alpha.3-windows.zip#Windows Release Package" ^
  "releases\v1.0.0-alpha.3\ghst_installer.py#Graphical Installer" ^
  "releases\v1.0.0-alpha.3\install_ghst.bat#Windows Launcher"

echo.
echo 🎉 Release created successfully!
echo 🔗 View at: https://github.com/allanwrench28/GHST/releases/tag/%VERSION%
pause
