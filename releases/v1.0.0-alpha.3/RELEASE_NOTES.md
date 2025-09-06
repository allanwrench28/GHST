# GHST v1.0.0-alpha.3 Release Notes

**Release Date:** 2025-09-06  
**Build Number:** 5003

## 🛠️ **Critical Compatibility Fix**

This is a critical hotfix release addressing Python version compatibility issues in the installer.

### 🐛 Fixed
- **Python 3.6+ Compatibility**: Resolved `capture_output` parameter error for older Python versions
- **Subprocess Calls**: Replaced `capture_output=True` with `stdout=devnull` for broader compatibility
- **Error Handling**: Enhanced exception handling for installation failures

### ⚡ **Installation Impact**
- **Backward Compatibility**: Now works with Python 3.6, 3.7, 3.8, 3.9, 3.10+
- **PyQt5 Installation**: Fixed installation failure that prevented GUI from launching
- **Better Error Messages**: More descriptive error reporting for troubleshooting

## 📦 Installation

### Quick Install (Recommended)
```bash
python ghst_installer.py
```

### Batch Launcher
```cmd
install_ghst.bat
```

## 🔄 Upgrade Notes
- **Immediate Upgrade Recommended**: This fixes installation failures in previous versions
- **Clean Installation**: Recommended for users who experienced installation issues
- **Python Version Check**: Verify you have Python 3.6+ installed

## 🎯 **What This Fixes**
If you saw this error:
```
❌ Installation failed: Popen.__init__() got an unexpected keyword argument 'capture_output'
```

This release resolves it completely!

---
**Previous Release:** v1.0.0-alpha.2  
**Next Planned:** Enhanced GUI features and plugin system
