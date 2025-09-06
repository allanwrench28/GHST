# Release Instructions for GHST

This document explains how to create and publish releases for GHST that show up in GitHub's releases section.

## GitHub Release Process

### 1. Create Git Tags
```bash
# Create an annotated tag for the release
git tag -a v1.0.0-alpha.3 -m "Release v1.0.0-alpha.3 - Python Compatibility Fix"

# Push tags to GitHub
git push origin --tags
```

### 2. GitHub Release Assets
The following files should be uploaded as release assets:

#### Primary Downloads
- `GHST-v1.0.0-alpha.3-windows.zip` - Complete Windows release package
- `ghst_installer.py` - Standalone graphical installer
- `install_ghst.bat` - Windows batch launcher

#### Documentation
- `RELEASE_NOTES.md` - Detailed release notes
- `CHANGELOG.md` - Project changelog

### 3. Release Notes Template
```markdown
# GHST v1.0.0-alpha.3 - Python Compatibility Fix

## 🛠️ Critical Compatibility Fix
This is a critical hotfix release addressing Python version compatibility issues in the installer.

### 🐛 Fixed
- **Python 3.6+ Compatibility**: Resolved `capture_output` parameter error for older Python versions
- **Subprocess Calls**: Replaced `capture_output=True` with `stdout=devnull` for broader compatibility
- **Error Handling**: Enhanced exception handling for installation failures

### ⚡ Installation Impact
- **Backward Compatibility**: Now works with Python 3.6, 3.7, 3.8, 3.9, 3.10+
- **PyQt5 Installation**: Fixed installation failure that prevented GUI from launching
- **Better Error Messages**: More descriptive error reporting for troubleshooting

## 📦 Quick Start

### Windows Installation
1. Download `GHST-v1.0.0-alpha.3-windows.zip`
2. Extract to desired location
3. Run `install_ghst.bat` or `python ghst_installer.py`

### What This Fixes
If you saw this error:
```
❌ Installation failed: Popen.__init__() got an unexpected keyword argument 'capture_output'
```
This release resolves it completely!

## Assets
- **GHST-v1.0.0-alpha.3-windows.zip** - Complete release package
- **ghst_installer.py** - Standalone installer
- **Source code** - Available as zip and tar.gz
```

### 4. Release Creation Steps for GitHub

1. **Go to GitHub Repository**
   - Navigate to `https://github.com/allanwrench28/GHST`
   
2. **Create Release**
   - Click "Releases" on the right sidebar
   - Click "Create a new release"
   - Select tag: `v1.0.0-alpha.3`
   - Release title: `GHST v1.0.0-alpha.3 - Python Compatibility Fix`
   - Description: Use the release notes template above

3. **Upload Assets**
   - Drag and drop the ZIP file
   - Add installer and batch files
   - Add documentation files

4. **Publish**
   - Check "This is a pre-release" for alpha versions
   - Click "Publish release"

### 5. File Structure
```
releases/
├── v1.0.0-alpha.3/
│   ├── ghst_installer.py       # Graphical installer
│   ├── install_ghst.bat        # Windows launcher
│   ├── RELEASE_NOTES.md        # Release documentation
│   ├── launcher.py             # GHST launcher
│   └── core/                   # Complete GHST system
└── GHST-v1.0.0-alpha.3-windows.zip  # Release archive
```

## Automated Release Script

For future releases, use the build script:
```bash
powershell -ExecutionPolicy Bypass -File build_release.ps1 -Version "1.0.0-alpha.4"
```

This will:
- Create new release directory
- Copy all necessary files
- Update version numbers
- Create release archive
- Generate release notes
