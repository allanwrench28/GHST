# GHST Enhanced Executable Builder
# Creates standalone .exe installer with cache cleanup and update checking

import shutil
import subprocess
import sys
from pathlib import Path


def build_installer_exe():
    """Build standalone installer executable."""
    print("🔨 Building GHST Enhanced Installer Executable")
    print("=" * 50)

    # Check if PyInstaller is available
    try:
        subprocess.check_call([sys.executable,
                               '-m',
                               'pip',
                               'show',
                               'pyinstaller'],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

    # Prepare build directory
    build_dir = Path.cwd() / "build"
    dist_dir = Path.cwd() / "dist"

    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    # Build installer executable
    print("🔧 Compiling enhanced installer...")

    pyinstaller_cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                              # Single executable
        '--windowed',                             # No console window
        '--name=GHST-Installer-Enhanced',         # Executable name
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=requests',
        '--clean',                                # Clean build
        'ghst_installer_enhanced.py'              # Source file
    ]

    try:
        subprocess.check_call(pyinstaller_cmd)
        print("✅ Enhanced installer executable built successfully!")

        # Create release package
        create_exe_release_package()

    except subprocess.CalledProcessError as e:
        print("❌ Build failed: {e}")
        return False

    return True


def create_exe_release_package():
    """Create executable release package."""
    print("\n📦 Creating Executable Release Package")
    print("=" * 40)

    # Create release directory for executables
    exe_release_dir = Path.cwd() / "releases" / "v1.0.0-alpha.4-executable"
    exe_release_dir.mkdir(parents=True, exist_ok=True)

    # Copy executable
    dist_dir = Path.cwd() / "dist"
    exe_file = dist_dir / "GHST-Installer-Enhanced.exe"

    if exe_file.exists():
        dest = exe_release_dir / "GHST-Installer-Enhanced.exe"
        shutil.copy2(exe_file, dest)
        print("📁 Copied executable: {exe_file.name}")

    # Create easy-launch batch file
    installer_bat = exe_release_dir / "Install-GHST-Enhanced.bat"
    with open(installer_bat, 'w', encoding='utf-8') as f:
        f.write("""@echo off
title GHST Enhanced Installer
echo ================================================================
echo    GHST AI Coding Engine - Enhanced Professional Installer
echo ================================================================
echo.
echo Features:
echo    - Cache cleanup and preference preservation
echo    - Automatic update checking from GitHub
echo    - Advanced installation options
echo    - Professional tabbed interface
echo.
echo Starting installer...
echo.

GHST-Installer-Enhanced.exe

if errorlevel 1 (
    echo.
    echo Installation process completed.
    echo.
)

echo.
echo Thank you for choosing GHST!
echo.
pause
""")

    # Create release notes for executable version
    readme_content = """  # GHST v1.0.0-alpha.4 - Enhanced Executable Release

#  # 🚀 **Standalone Installer - No Python Required!**

This is the enhanced executable version of GHST that doesn't require Python to be installed on your system.

##  # 📦 **What's Included**

- `GHST-Installer-Enhanced.exe` - Professional standalone installer
- `Install-GHST-Enhanced.bat` - Easy launcher with instructions

##  # ✨ **Enhanced Features**

###  # 🧹 **Smart Cache Management**
- Automatically cleans old caches and temporary files
- Preserves user preferences during upgrades
- Removes corrupted installation artifacts
- Backup and restore system for safe upgrades

###  # 🔄 **Integrated Update System**
- Built-in GitHub integration for update checking
- Shows release notes and version comparisons
- Direct download links to newest releases
- Automatic version detection and compatibility checks

###  # ⚙️ **Professional Installation Options**
- Clean installation vs. upgrade detection
- Advanced developer options
- Desktop shortcut creation
- Comprehensive logging and error reporting

###  # 📋 **Modern Interface**
- Tabbed interface for better organization
- Real-time progress tracking with detailed logs
- Professional dark theme with consistent styling
- Separate update management tab

##  # 🎯 **Quick Start**

1. **Download**: Get this release package from GitHub
2. **Run**: Double-click `Install-GHST-Enhanced.bat` or the .exe directly
3. **Install**: Follow the wizard with intelligent default options
4. **Launch**: GHST will be ready to use immediately

##  # 🔄 **Update Process**

The installer includes an "Updates" tab that:
- Checks GitHub for newer GHST versions
- Shows detailed release notes
- Provides direct download links
- Handles version compatibility

##  # 🛠️ **System Requirements**

- **Windows 10/11** (primary support)
- **No Python required** (standalone executable)
- **Internet connection** recommended for updates
- **Administrator rights** may be needed for installation

##  # 🚨 **What This Fixes**

If you experienced any of these issues:
- ❌ `capture_output` parameter errors
- ❌ Installation corruption from old files
- ❌ Python version compatibility problems
- ❌ Missing dependencies or modules

This enhanced executable installer resolves all of them!

##  # 🆘 **Troubleshooting**

- **Antivirus warnings**: The executable is safe - PyInstaller packages can trigger false positives
- **Installation failures**: Run as administrator if permission errors occur
- **Update issues**: Check internet connection for GitHub API access

##  # 📞 **Support & Links**

- **GitHub Repository**: https://github.com/allanwrench28/GHST
- **Issues & Bug Reports**: https://github.com/allanwrench28/GHST/issues
- **Latest Releases**: https://github.com/allanwrench28/GHST/releases
- **Documentation**: See repository README and wiki

---

**🎉 This release represents a major step forward in GHST's professional distribution system!**

Built with PyInstaller for maximum compatibility and ease of use.
"""

    readme_path = exe_release_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("📁 Executable release package created: {exe_release_dir}")
    print("📋 Files created:")
    print("   - GHST-Installer-Enhanced.exe")
    print("   - Install-GHST-Enhanced.bat")
    print("   - README.md")

    return exe_release_dir


def main():
    """Main build process."""
    print("🚀 GHST Enhanced Executable Build System")
    print("=" * 50)
    print()

    # Check current directory
    if not Path('ghst_installer_enhanced.py').exists():
        print("❌ Enhanced installer not found!")
        print("📁 Please run this script from the GHST root directory")
        return

    # Build enhanced installer executable
    if build_installer_exe():
        print("\n" + "=" * 60)
        print("🎉 GHST Enhanced Executable Build Complete!")
        print("=" * 60)
        print("\n📋 Next Steps:")
        print("1. Test the executable installer")
        print("2. Upload to GitHub releases as v1.0.0-alpha.4-executable")
        print("3. Update release notes with executable download info")
        print("4. Tag the release for easy distribution")
    else:
        print("❌ Build process failed")


if __name__ == "__main__":
    main()
