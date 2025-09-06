@echo off
title GHST Auto-Continue Helper
color 0A

echo ==========================================
echo    GHST AUTO-CONTINUE HELPER
echo ==========================================
echo.
echo Commands:
echo   c = Send Continue (Enter key)
echo   y = Send Yes (y + Enter)  
echo   s = Send Space
echo   q = Quit
echo.

set /a count=0

:loop
set /p "cmd=Command: "

if /i "%cmd%"=="c" (
    echo Sending Enter...
    powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')"
    set /a count+=1
    echo [✓] Sent Enter #!count!
    goto loop
)

if /i "%cmd%"=="y" (
    echo Sending Y + Enter...
    powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('y{ENTER}')"
    set /a count+=1
    echo [✓] Sent Y+Enter #!count!
    goto loop
)

if /i "%cmd%"=="s" (
    echo Sending Space...
    powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait(' ')"
    set /a count+=1
    echo [✓] Sent Space #!count!
    goto loop
)

if /i "%cmd%"=="q" (
    echo.
    echo Goodbye! Total commands sent: !count!
    pause
    exit /b 0
)

echo Unknown command: %cmd%
goto loop
