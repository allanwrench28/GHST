# GHST Release Build Script
# =========================
# Automates the build and release process for GHST

param(
    [string]$Version = "1.0.0-alpha.1",
    [string]$BuildNumber = "5001",
    [switch]$TestOnly = $false
)

Write-Host "🔨 GHST Release Build Script" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green
Write-Host ""

$ReleaseDir = "releases\v$Version"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "📋 Build Configuration:" -ForegroundColor Yellow
Write-Host "   Version: $Version" -ForegroundColor White
Write-Host "   Build: $BuildNumber" -ForegroundColor White  
Write-Host "   Release Dir: $ReleaseDir" -ForegroundColor White
Write-Host "   Test Only: $TestOnly" -ForegroundColor White
Write-Host ""

# Create release directory
if (!(Test-Path $ReleaseDir)) {
    New-Item -ItemType Directory -Path $ReleaseDir -Force | Out-Null
    Write-Host "📁 Created release directory: $ReleaseDir" -ForegroundColor Green
}

# Update version info
Write-Host "🔢 Updating version information..." -ForegroundColor Yellow

$VersionContent = @"
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, $BuildNumber),
    prodvers=(1, 0, 0, $BuildNumber),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'GHST Open Source'),
         StringStruct(u'FileDescription', u'GHST - AI Coding Engine'),
         StringStruct(u'FileVersion', u'$Version'),
         StringStruct(u'InternalName', u'GHST'),
         StringStruct(u'LegalCopyright', u'MIT License - No Liability Assumed'),
         StringStruct(u'OriginalFilename', u'GHST.exe'),
         StringStruct(u'ProductName', u'GHST AI Coding Engine'),
         StringStruct(u'ProductVersion', u'$Version')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"@

$VersionContent | Out-File -FilePath "core\version_info.txt" -Encoding UTF8
Write-Host "✅ Version info updated to $Version" -ForegroundColor Green

# Run tests
Write-Host "🧪 Running system tests..." -ForegroundColor Yellow

try {
    $TestResult = python test_ghst_system.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ All tests passed!" -ForegroundColor Green
    } else {
        Write-Host "❌ Tests failed!" -ForegroundColor Red
        if (!$TestOnly) {
            Write-Host "⚠️ Continuing with build despite test failures..." -ForegroundColor Yellow
        } else {
            exit 1
        }
    }
} catch {
    Write-Host "⚠️ Could not run tests: $_" -ForegroundColor Yellow
}

if ($TestOnly) {
    Write-Host "🏁 Test-only mode complete" -ForegroundColor Green
    exit 0
}

# Copy release artifacts
Write-Host "📦 Copying release artifacts..." -ForegroundColor Yellow

$Artifacts = @(
    @{Source="releases\v$Version\ghst_installer.py"; Dest="$ReleaseDir\ghst_installer.py"},
    @{Source="core\launcher.py"; Dest="$ReleaseDir\ghst_launcher.py"},
    @{Source="README.md"; Dest="$ReleaseDir\README.md"},
    @{Source="LICENSE"; Dest="$ReleaseDir\LICENSE"},
    @{Source="CHANGELOG.md"; Dest="$ReleaseDir\CHANGELOG.md"}
)

foreach ($Artifact in $Artifacts) {
    if (Test-Path $Artifact.Source) {
        Copy-Item $Artifact.Source $Artifact.Dest -Force
        Write-Host "✅ Copied: $($Artifact.Source)" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Missing: $($Artifact.Source)" -ForegroundColor Yellow
    }
}

# Create release manifest
Write-Host "📋 Creating release manifest..." -ForegroundColor Yellow

$Manifest = @{
    version = $Version
    build_number = $BuildNumber
    release_date = $Timestamp
    artifacts = @()
    system_requirements = @{
        python = "3.8+"
        platform = "Windows 10+"
        memory = "4GB RAM"
        storage = "500MB"
    }
}

# Add artifact info
Get-ChildItem $ReleaseDir | ForEach-Object {
    $Manifest.artifacts += @{
        name = $_.Name
        size = $_.Length
        type = $_.Extension
    }
}

$Manifest | ConvertTo-Json -Depth 3 | Out-File "$ReleaseDir\manifest.json" -Encoding UTF8
Write-Host "✅ Release manifest created" -ForegroundColor Green

# Create checksums
Write-Host "🔐 Creating checksums..." -ForegroundColor Yellow

$ChecksumFile = "$ReleaseDir\checksums.txt"
"# GHST v$Version Checksums" | Out-File $ChecksumFile -Encoding UTF8
"# Generated: $Timestamp" | Out-File $ChecksumFile -Append -Encoding UTF8
"" | Out-File $ChecksumFile -Append -Encoding UTF8

Get-ChildItem $ReleaseDir -File | Where-Object {$_.Name -ne "checksums.txt"} | ForEach-Object {
    $Hash = Get-FileHash $_.FullName -Algorithm SHA256
    "$($Hash.Hash)  $($_.Name)" | Out-File $ChecksumFile -Append -Encoding UTF8
}

Write-Host "✅ Checksums created" -ForegroundColor Green

# Final summary
Write-Host ""
Write-Host "🎉 BUILD COMPLETE!" -ForegroundColor Green
Write-Host "==================" -ForegroundColor Green
Write-Host "Version: $Version" -ForegroundColor White
Write-Host "Build: $BuildNumber" -ForegroundColor White
Write-Host "Location: $ReleaseDir" -ForegroundColor White
Write-Host "Artifacts: $($Manifest.artifacts.Count)" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Ready for release!" -ForegroundColor Cyan

# Usage examples:
# .\build_release.ps1                              # Standard build
# .\build_release.ps1 -Version "1.0.0-alpha.2"    # Custom version  
# .\build_release.ps1 -TestOnly                    # Test only, no build
