# GHST PowerShell Auto-Continue
# =============================
# Simple automation for Windows PowerShell/VS Code terminals

param(
    [int]$IntervalSeconds = 5,
    [string]$Mode = "manual"
)

Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("="*50) -ForegroundColor Cyan
Write-Host "🤖 GHST POWERSHELL AUTO-CONTINUE" -ForegroundColor Green
Write-Host "=" -ForegroundColor Cyan -NoNewline  
Write-Host ("="*50) -ForegroundColor Cyan

Write-Host ""
Write-Host "📋 Available Modes:" -ForegroundColor Yellow
Write-Host "   manual   - Wait for your input to continue" -ForegroundColor White
Write-Host "   auto     - Automatically send Enter every $IntervalSeconds seconds" -ForegroundColor White
Write-Host "   smart    - Monitor for prompts and respond" -ForegroundColor White
Write-Host ""

# Statistics
$script:ContinuesSent = 0
$script:StartTime = Get-Date

function Send-Continue {
    param([string]$Key = "Enter")
    
    try {
        # Use Windows API to send keys
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait("{$Key}")
        
        $script:ContinuesSent++
        $timestamp = (Get-Date).ToString("HH:mm:ss")
        Write-Host "📤 [$timestamp] Sent: $Key (#$script:ContinuesSent)" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Error sending key: $_" -ForegroundColor Red
        return $false
    }
}

function Start-ManualMode {
    Write-Host "👆 MANUAL MODE ACTIVE" -ForegroundColor Cyan
    Write-Host "🔧 Available commands:" -ForegroundColor Yellow
    Write-Host "   c, continue, enter - Send Enter key" -ForegroundColor White
    Write-Host "   y, yes            - Send Y + Enter" -ForegroundColor White  
    Write-Host "   s, space          - Send Space key" -ForegroundColor White
    Write-Host "   auto              - Switch to auto mode" -ForegroundColor White
    Write-Host "   q, quit, exit     - Exit automation" -ForegroundColor White
    Write-Host ""
    
    while ($true) {
        Write-Host "💬 Command (c/y/s/auto/q): " -ForegroundColor Cyan -NoNewline
        $input = Read-Host
        
        switch ($input.ToLower()) {
            {"c", "continue", "enter", "" -contains $_} {
                Send-Continue
            }
            {"y", "yes" -contains $_} {
                Send-Continue "y"
                Start-Sleep -Milliseconds 100
                Send-Continue "Enter"
            }
            {"s", "space" -contains $_} {
                Send-Continue "Space"
            }
            "auto" {
                Write-Host "🔄 Switching to auto mode..." -ForegroundColor Yellow
                Start-AutoMode
                return
            }
            {"q", "quit", "exit" -contains $_} {
                Stop-Automation
                return
            }
            default {
                Write-Host "❓ Unknown command: $input" -ForegroundColor Red
            }
        }
    }
}

function Start-AutoMode {
    Write-Host "🤖 AUTO MODE ACTIVE" -ForegroundColor Green
    Write-Host "⏱️ Sending Enter every $IntervalSeconds seconds" -ForegroundColor Yellow
    Write-Host "⏹️ Press CTRL+C to stop" -ForegroundColor Red
    Write-Host ""
    
    try {
        while ($true) {
            Start-Sleep -Seconds $IntervalSeconds
            Send-Continue
        }
    }
    catch {
        Write-Host "⏹️ Auto mode stopped" -ForegroundColor Yellow
    }
}

function Start-SmartMode {
    Write-Host "🧠 SMART MODE ACTIVE" -ForegroundColor Magenta
    Write-Host "👁️ Monitoring for prompts..." -ForegroundColor Yellow
    Write-Host "⏹️ Press CTRL+C to stop" -ForegroundColor Red
    Write-Host ""
    
    try {
        while ($true) {
            # Check if there are any prompts waiting
            # This is a simplified implementation
            
            # Look for common prompt patterns in console
            $title = (Get-Host).UI.RawUI.WindowTitle
            
            if ($title -match "continue|press|enter|key") {
                Write-Host "🔍 Detected prompt in window title" -ForegroundColor Cyan
                Send-Continue
            }
            
            Start-Sleep -Seconds 2
        }
    }
    catch {
        Write-Host "⏹️ Smart mode stopped" -ForegroundColor Yellow
    }
}

function Stop-Automation {
    $duration = (Get-Date) - $script:StartTime
    
    Write-Host ""
    Write-Host "⏹️ AUTOMATION STOPPED" -ForegroundColor Red
    Write-Host "⏱️ Duration: $($duration.ToString('hh\:mm\:ss'))" -ForegroundColor White
    Write-Host "📊 Total continues sent: $script:ContinuesSent" -ForegroundColor White
    Write-Host "👋 Goodbye!" -ForegroundColor Green
    
    exit 0
}

function Show-Instructions {
    Write-Host ""
    Write-Host "💡 INSTRUCTIONS:" -ForegroundColor Yellow
    Write-Host "1. Keep your VS Code terminal window active" -ForegroundColor White
    Write-Host "2. This script will send keystrokes to the active window" -ForegroundColor White
    Write-Host "3. Use CTRL+C to stop auto/smart modes" -ForegroundColor White
    Write-Host "4. Switch between modes as needed" -ForegroundColor White
    Write-Host ""
}

# Main execution
try {
    Show-Instructions
    
    switch ($Mode.ToLower()) {
        "auto" {
            Start-AutoMode
        }
        "smart" {
            Start-SmartMode  
        }
        default {
            Start-ManualMode
        }
    }
}
catch {
    Write-Host "❌ Fatal error: $_" -ForegroundColor Red
    Stop-Automation
}

# Usage examples:
# .\ghst_powershell_auto.ps1                    # Manual mode
# .\ghst_powershell_auto.ps1 -Mode auto         # Auto mode  
# .\ghst_powershell_auto.ps1 -Mode auto -IntervalSeconds 3  # Auto mode, 3 sec interval
