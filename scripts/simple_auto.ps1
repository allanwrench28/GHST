# GHST Simple Auto-Continue
# Simple PowerShell automation for VS Code terminals

param(
    [int]$Interval = 5,
    [string]$Mode = "manual"
)

$ContinuesSent = 0
$StartTime = Get-Date

Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 40) -ForegroundColor Cyan
Write-Host "🤖 GHST AUTO-CONTINUE" -ForegroundColor Green  
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 40) -ForegroundColor Cyan
Write-Host ""

function Send-Key {
    param([string]$Key = "Enter")
    
    try {
        Add-Type -AssemblyName System.Windows.Forms
        
        if ($Key -eq "Enter") {
            [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
        }
        elseif ($Key -eq "Space") {
            [System.Windows.Forms.SendKeys]::SendWait(" ")
        }
        else {
            [System.Windows.Forms.SendKeys]::SendWait($Key)
        }
        
        $script:ContinuesSent++
        $timestamp = (Get-Date).ToString("HH:mm:ss")
        Write-Host "📤 [$timestamp] Sent: $Key (#$script:ContinuesSent)" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Error sending key: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

if ($Mode -eq "auto") {
    Write-Host "🤖 AUTO MODE - Sending Enter every $Interval seconds" -ForegroundColor Yellow
    Write-Host "⏹️ Press CTRL+C to stop" -ForegroundColor Red
    Write-Host ""
    
    try {
        while ($true) {
            Start-Sleep -Seconds $Interval
            Send-Key "Enter"
        }
    }
    catch {
        Write-Host "⏹️ Stopped" -ForegroundColor Yellow
    }
}
else {
    Write-Host "👆 MANUAL MODE" -ForegroundColor Cyan
    Write-Host "Commands: c=Continue, y=Yes, s=Space, q=Quit" -ForegroundColor Yellow
    Write-Host ""
    
    while ($true) {
        Write-Host "Command: " -ForegroundColor Cyan -NoNewline
        $userInput = Read-Host
        
        switch ($userInput.ToLower()) {
            "c" { Send-Key "Enter" }
            "y" { 
                Send-Key "y"
                Start-Sleep -Milliseconds 100
                Send-Key "Enter"
            }
            "s" { Send-Key "Space" }
            "q" { 
                $duration = (Get-Date) - $StartTime
                Write-Host "Duration: $($duration.ToString('hh\:mm\:ss'))" -ForegroundColor White
                Write-Host "Total: $ContinuesSent" -ForegroundColor White
                Write-Host "Bye!" -ForegroundColor Green
                exit 
            }
            default { Write-Host "Unknown: $userInput" -ForegroundColor Red }
        }
    }
}
