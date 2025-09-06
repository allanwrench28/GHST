# GHST Build Release Script
param(
    [string]$Version = "1.0.0-alpha.2",
    [string]$BuildNumber = "5002"
)

Write-Host "GHST Release Builder v1.0" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

$ProjectRoot = Get-Location
$ReleaseDir = Join-Path $ProjectRoot "releases\v$Version"

Write-Host "Creating release v$Version (Build $BuildNumber)" -ForegroundColor Green

# Create release directory
if (Test-Path $ReleaseDir) {
    Write-Host "Release directory already exists, updating..." -ForegroundColor Yellow
} else {
    New-Item -ItemType Directory -Path $ReleaseDir -Force | Out-Null
    Write-Host "Created release directory: $ReleaseDir" -ForegroundColor Green
}

# Copy installer to release directory
$InstallerSource = Join-Path $ProjectRoot "releases\v1.0.0-alpha.1\ghst_installer.py"
$InstallerDest = Join-Path $ReleaseDir "ghst_installer.py"
if (Test-Path $InstallerSource) {
    Copy-Item $InstallerSource $InstallerDest -Force
    Write-Host "Copied installer to release directory" -ForegroundColor Green
}

# Copy core files
$CoreFiles = @("launcher.py", "fantom.py", "clockwork.py", "requirements.txt")
foreach ($file in $CoreFiles) {
    $source = Join-Path $ProjectRoot $file
    $dest = Join-Path $ReleaseDir $file
    if (Test-Path $source) {
        Copy-Item $source $dest -Force
        Write-Host "Copied $file" -ForegroundColor Green
    }
}

# Create release notes
$ReleaseNotesPath = Join-Path $ReleaseDir "RELEASE_NOTES.md"
$ReleaseNotes = "# GHST v$Version Release Notes`n`n**Release Date:** $(Get-Date -Format 'yyyy-MM-dd')`n**Build Number:** $BuildNumber`n`n## Features`n- Professional graphical installer`n- Enhanced AI collaboration system`n- Improved plugin architecture`n`n## Installation`n```bash`npython ghst_installer.py`n```"

Set-Content -Path $ReleaseNotesPath -Value $ReleaseNotes
Write-Host "Created release notes" -ForegroundColor Green

# Create batch launcher
$BatchLauncherPath = Join-Path $ReleaseDir "install_ghst.bat"
$BatchContent = "@echo off`necho GHST v$Version Installer`necho ========================`necho.`necho Starting graphical installer...`npython ghst_installer.py`npause"

Set-Content -Path $BatchLauncherPath -Value $BatchContent
Write-Host "Created batch launcher" -ForegroundColor Green

Write-Host ""
Write-Host "Release v$Version build complete!" -ForegroundColor Green
Write-Host "Release directory: $ReleaseDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "Test the installer with: python releases\v$Version\ghst_installer.py" -ForegroundColor Yellow
