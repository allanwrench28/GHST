# GHST Simple Continue Helper
# Press 'c' and Enter to send Continue, 'q' and Enter to quit

$count = 0

Write-Host "🤖 GHST Auto-Continue Helper" -ForegroundColor Green
Write-Host "Commands:" -ForegroundColor Yellow  
Write-Host "  c + Enter = Send Continue" -ForegroundColor White
Write-Host "  y + Enter = Send Yes" -ForegroundColor White
Write-Host "  q + Enter = Quit" -ForegroundColor White
Write-Host ""

Add-Type -AssemblyName System.Windows.Forms

while ($true) {
    Write-Host "Command: " -ForegroundColor Cyan -NoNewline
    $input = Read-Host
    
    switch ($input) {
        "c" {
            [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
            $count++
            Write-Host "✅ Sent Enter #$count" -ForegroundColor Green
        }
        "y" {
            [System.Windows.Forms.SendKeys]::SendWait("y{ENTER}")
            $count++
            Write-Host "✅ Sent Y+Enter #$count" -ForegroundColor Green
        }
        "q" {
            Write-Host "👋 Goodbye! Total sent: $count" -ForegroundColor Yellow
            exit
        }
        default {
            Write-Host "❓ Unknown command: $input" -ForegroundColor Red
        }
    }
}
