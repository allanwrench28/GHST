# GHST Build Release Script
# Automated build system for creating professional releases
param(
    [string]$Version = "1.0.0-alpha.2",
    [string]$BuildNumber = "5002"
)

Write-Host "🚀 GHST Release Builder v1.0" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Get current directory
$ProjectRoot = Get-Location
$ReleaseDir = Join-Path $ProjectRoot "releases\v$Version"

Write-Host "📦 Creating release v$Version (Build $BuildNumber)" -ForegroundColor Green

# Create release directory
if (Test-Path $ReleaseDir) {
    Write-Host "⚠️  Release directory already exists, updating..." -ForegroundColor Yellow
} else {
    New-Item -ItemType Directory -Path $ReleaseDir -Force | Out-Null
    Write-Host "✅ Created release directory: $ReleaseDir" -ForegroundColor Green
}

# Update version info
Write-Host "🔧 Updating version information..." -ForegroundColor Blue

# Update version_info.txt
$VersionInfoPath = Join-Path $ProjectRoot "version_info.txt"
if (Test-Path $VersionInfoPath) {
    $VersionContent = Get-Content $VersionInfoPath -Raw
    $VersionContent = $VersionContent -replace 'filevers=\(1,0,0,\d+\)', "filevers=(1,0,0,$BuildNumber)"
    $VersionContent = $VersionContent -replace 'prodvers=\(1,0,0,\d+\)', "prodvers=(1,0,0,$BuildNumber)"
    $VersionContent = $VersionContent -replace "u'FileVersion', u'[\d\.]+.*?'", "u'FileVersion', u'$Version'"
    $VersionContent = $VersionContent -replace "u'ProductVersion', u'[\d\.]+.*?'", "u'ProductVersion', u'$Version'"
    Set-Content -Path $VersionInfoPath -Value $VersionContent
    Write-Host "✅ Updated version_info.txt" -ForegroundColor Green
}

# Copy installer to release directory
$InstallerSource = Join-Path $ProjectRoot "releases\v1.0.0-alpha.1\ghst_installer.py"
$InstallerDest = Join-Path $ReleaseDir "ghst_installer.py"
if (Test-Path $InstallerSource) {
    Copy-Item $InstallerSource $InstallerDest -Force
    Write-Host "✅ Copied installer to release directory" -ForegroundColor Green
}

# Copy core files
$CoreFiles = @("launcher.py", "fantom.py", "clockwork.py", "requirements.txt", "pyproject.toml", "setup.py")
foreach ($file in $CoreFiles) {
    $source = Join-Path $ProjectRoot $file
    $dest = Join-Path $ReleaseDir $file
    if (Test-Path $source) {
        Copy-Item $source $dest -Force
        Write-Host "✅ Copied $file" -ForegroundColor Green
    }
}

# Copy src directory
$SrcSource = Join-Path $ProjectRoot "src"
$SrcDest = Join-Path $ReleaseDir "src"
if (Test-Path $SrcSource) {
    Copy-Item $SrcSource $SrcDest -Recurse -Force
    Write-Host "✅ Copied src directory" -ForegroundColor Green
}

# Copy config directory
$ConfigSource = Join-Path $ProjectRoot "config"
$ConfigDest = Join-Path $ReleaseDir "config"
if (Test-Path $ConfigSource) {
    Copy-Item $ConfigSource $ConfigDest -Recurse -Force
    Write-Host "✅ Copied config directory" -ForegroundColor Green
}

# Create release notes
$ReleaseNotesPath = Join-Path $ReleaseDir "RELEASE_NOTES.md"
$ReleaseNotes = @"
# GHST v$Version Release Notes

**Release Date:** $(Get-Date -Format "yyyy-MM-dd")
**Build Number:** $BuildNumber

## 🎯 What's New

### ✨ Features
- Professional graphical installer with step-by-step wizard
- Enhanced AI collaboration system
- Improved plugin architecture
- Advanced ghost management capabilities

### 🔧 Technical Improvements
- PyQt5-based installation interface
- Automated dependency management
- Enhanced error handling and logging
- Streamlined configuration system

### 🛠️ Developer Experience
- Professional release management system
- Automated build scripts
- Comprehensive documentation
- Standardized changelog format

## 📦 Installation

### Quick Install (Recommended)
```bash
python ghst_installer.py
```

### Manual Install
```bash
pip install -r requirements.txt
python launcher.py
```

## 🐛 Known Issues
- Minor UI scaling on high-DPI displays
- Some dependency conflicts on older Python versions

## 🔄 Upgrade Notes
- Clean installation recommended for this alpha release
- Backup existing configurations before upgrading

---
**Full Changelog:** See CHANGELOG.md for detailed technical changes
"@

Set-Content -Path $ReleaseNotesPath -Value $ReleaseNotes
Write-Host "✅ Created release notes" -ForegroundColor Green

# Create simple batch launcher
$BatchLauncherPath = Join-Path $ReleaseDir "install_ghst.bat"
$BatchContent = @"
@echo off
echo GHST v$Version Installer
echo ========================
echo.
echo Starting graphical installer...
python ghst_installer.py
pause
"@

Set-Content -Path $BatchLauncherPath -Value $BatchContent
Write-Host "✅ Created batch launcher" -ForegroundColor Green

# Create ZIP archive
Write-Host "📦 Creating release archive..." -ForegroundColor Blue
$ArchivePath = Join-Path $ProjectRoot "releases\GHST-v$Version.zip"

# Remove existing archive if it exists
if (Test-Path $ArchivePath) {
    Remove-Item $ArchivePath -Force
}

# Create archive
try {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory($ReleaseDir, $ArchivePath)
    Write-Host "✅ Created release archive: GHST-v$Version.zip" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not create ZIP archive: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "" -ForegroundColor White
Write-Host "🎉 Release v$Version build complete!" -ForegroundColor Green
Write-Host "📂 Release directory: $ReleaseDir" -ForegroundColor Cyan
Write-Host "📦 Archive: $ArchivePath" -ForegroundColor Cyan
Write-Host "" -ForegroundColor White
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test the installer: python releases\v$Version\ghst_installer.py" -ForegroundColor White  
Write-Host "2. Update CHANGELOG.md with new version" -ForegroundColor White
Write-Host "3. Commit and tag the release" -ForegroundColor White
Write-Host "" -ForegroundColor White
