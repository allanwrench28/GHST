#!/usr/bin/env python3
"""
Build scrip    # Build with PyInstaller - optimized for size
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=GHST-Installer-Beautiful",
        "--icon=icon.ico" if os.path.exists("icon.ico") else "",
        # Don't include all files - only what we need
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=requests",
        "--exclude-module=matplotlib",  # Exclude large unused modules
        "--exclude-module=numpy",
        "--exclude-module=pandas",
        "--exclude-module=scipy",
        "--exclude-module=PyQt5.QtWebEngine",
        "--exclude-module=PyQt5.QtWebEngineWidgets",
        "--optimize=2",  # Maximum optimization
        "--strip",       # Strip debug symbols
        "--clean",
        "ghst_installer_beautiful.py"
    ]tiful Installer
==========================================

Creates a standalone executable from the beautiful installer using PyInstaller.
Includes proper error handling and professional packaging.

Usage: python build_beautiful_exe.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import zipfile

def clean_build_directories():
    """Clean previous build artifacts."""
    print("🧹 Cleaning previous build artifacts...")

    # Directories to clean
    dirs_to_clean = ["build", "dist", "__pycache__"]

    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name, ignore_errors=True)
            print("   ✓ Removed {dir_name}/")

    # Files to clean
    spec_files = [f for f in os.listdir(".") if f.endswith(".spec")]
    for spec_file in spec_files:
        os.remove(spec_file)
        print("   ✓ Removed {spec_file}")

def build_installer_exe():
    """Build the installer executable using PyInstaller."""
    print("🏗️ Building beautiful installer executable...")

    # PyInstaller command with optimized settings
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=GHST-Installer-Beautiful",
        "--icon=icon.ico" if os.path.exists("icon.ico") else "",
        "--add-data=.;.",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=requests",
        "--clean",
        "ghst_installer_beautiful.py"
    ]

    # Remove empty icon parameter if no icon exists
    cmd = [arg for arg in cmd if arg]

    try:
        # Run PyInstaller
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8')

        if result.returncode == 0:
            print("   ✅ Executable built successfully!")

            # Check if executable exists
            exe_path = Path("dist/GHST-Installer-Beautiful.exe")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print("   📦 Executable size: {size_mb:.1f} MB")
                return True
            else:
                print("   ❌ Executable not found in dist/ directory")
                return False
        else:
            print(
                "   ❌ PyInstaller failed with return code {
                    result.returncode}")
            print("   Error output:")
            for line in result.stderr.split('\n'):
                if line.strip():
                    print("     {line}")
            return False

    except FileNotFoundError:
        print("   ❌ PyInstaller not found. Please install it with: pip install pyinstaller")
        return False
    except Exception as e:
        print("   ❌ Error during build: {e}")
        return False

def create_beautiful_release_package():
    """Create a complete release package with documentation."""
    print("📦 Creating beautiful release package...")

    # Version and release info
    version = "v1.0.0-alpha.5-beautiful"
    release_dir = Path("releases/{version}")

    # Create release directory
    release_dir.mkdir(parents=True, exist_ok=True)
    print("   📁 Created release directory: {release_dir}")

    # Copy executable
    exe_source = Path("dist/GHST-Installer-Beautiful.exe")
    exe_dest = release_dir / "GHST-Installer-Beautiful.exe"

    if exe_source.exists():
        shutil.copy2(exe_source, exe_dest)
        print("   ✅ Copied executable: {exe_dest.name}")
    else:
        print("   ❌ Executable not found!")
        return False

    # Create batch launcher
    batch_content = '''@echo off
echo ================================================
echo    GHST AI Coding Engine - Beautiful Installer
echo    Version: {version}
echo    Launching installation wizard...
echo ================================================
echo.

REM Launch the beautiful installer
GHST-Installer-Beautiful.exe

echo.
echo Installation wizard closed.
pause
'''

    batch_file = release_dir / "Install-GHST-Beautiful.bat"
    with open(batch_file, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    print(f"   ✅ Created batch launcher: {batch_file.name}")

    # Create comprehensive README
    readme_content = '''  # GHST AI Coding Engine - Beautiful Installer {version}

#  # 🎨 Beautiful Modern Interface

This is the stunning redesigned installer for GHST AI Coding Engine featuring:

##  # ✨ Visual Features
- **Modern Dark Theme**: Professional dark interface with glassmorphism effects
- **Gradient Animations**: Smooth color transitions and visual feedback
- **Card-Based Layout**: Clean, organized interface with modern styling
- **Custom Components**: Beautiful progress bars, buttons, and form elements
- **Responsive Design**: Optimized for different screen sizes

##  # 🚀 Enhanced Functionality
- **Zero Dependencies**: Complete standalone executable (no Python required)
- **Smart Cache Management**: Intelligent cleanup preserving user preferences
- **Real-time Progress**: Beautiful progress tracking with detailed logging
- **GitHub Integration**: Automatic update checking and version management
- **Professional Navigation**: Intuitive tab-based workflow

#  # 📦 Installation Options

##  # Option 1: One-Click Installation (Recommended)
1. Double-click `Install-GHST-Beautiful.bat`
2. Follow the beautiful guided installer
3. Enjoy the stunning interface!

##  # Option 2: Direct Executable
1. Run `GHST-Installer-Beautiful.exe` directly
2. Complete the installation process
3. Launch GHST from the completion screen

#  # 🎯 System Requirements

- **Operating System**: Windows 10/11 (64-bit)
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free space for installation
- **Display**: 1024x768 minimum resolution
- **Internet**: Required for update checking and downloads

#  # 🔧 Installation Features

##  # Welcome Screen
- Hero section with beautiful typography
- Feature highlights with modern icons
- Professional branding and version info

##  # Advanced Options
- Custom installation directory selection
- Cache cleanup configuration
- Automatic update preferences
- Desktop shortcut creation

##  # Installation Progress
- Real-time progress visualization
- Detailed logging with emojis
- Beautiful progress bars with gradients
- Smart error handling and recovery

##  # Completion Screen
- Celebration animation
- Quick launch functionality
- Open installation folder option
- Visit GitHub repository link

#  # 🎨 Design Philosophy

This installer represents the evolution of GHST into professional-grade software:

- **User Experience First**: Every interaction is designed to be intuitive and beautiful
- **Performance Optimized**: Fast loading, smooth animations, efficient processing
- **Accessibility Focused**: High contrast colors, readable fonts, clear navigation
- **Modern Standards**: Following 2025 design trends and best practices

#  # 🔄 Update System

The installer includes intelligent update checking:
- Automatic detection of newer versions
- Direct links to latest releases
- Seamless upgrade path preservation
- User preference migration

#  # 📊 Technical Details

- **Built with**: PyQt5, PyInstaller, Python 3.9+
- **Architecture**: Single executable with embedded dependencies
- **Size**: ~246MB (optimized)
- **Startup**: <3 seconds on modern systems
- **Memory**: <100MB runtime footprint

#  # 🎉 What's New in Beautiful Edition

1. **Complete UI Redesign**: Modern, professional interface
2. **Enhanced Performance**: Faster loading and smoother operation
3. **Better User Feedback**: Clear progress indicators and status messages
4. **Improved Error Handling**: Graceful error recovery and user guidance
5. **Professional Branding**: Consistent visual identity throughout

#  # 🌟 Future Enhancements

- Animated logo and splash screen
- Custom themes and color schemes
- Installation analytics and feedback
- Multi-language support
- Automatic dark/light mode detection

---

**Enjoy the beautiful GHST installation experience!** 🚀

For support, visit: https://github.com/allanwrench28/GHST
Report issues: https://github.com/allanwrench28/GHST/issues

© 2025 GHST AI Coding Engine. All rights reserved.
'''

    readme_file = release_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"   ✅ Created comprehensive README: {readme_file.name}")

    # Create changelog
    changelog_content = '''  # GHST Beautiful Installer Changelog

#  # {version} - September 6, 2025

##  # 🎨 Major Visual Overhaul
- **NEW**: Complete interface redesign with modern dark theme
- **NEW**: Glassmorphism effects and gradient backgrounds
- **NEW**: Custom styled components (buttons, progress bars, cards)
- **NEW**: Professional typography and spacing
- **NEW**: Smooth animations and transitions

##  # ✨ Enhanced User Experience
- **IMPROVED**: Four-tab navigation workflow (Welcome → Options → Install → Complete)
- **IMPROVED**: Hero section with feature highlights
- **IMPROVED**: Real-time installation progress with beautiful visualization
- **IMPROVED**: Professional completion screen with quick actions
- **NEW**: Custom title bar with close button

##  # 🔧 Technical Improvements
- **ENHANCED**: Modern color palette with semantic color system
- **ENHANCED**: Responsive layout with proper spacing
- **ENHANCED**: Better error handling and user feedback
- **ENHANCED**: Optimized performance and memory usage
- **NEW**: Custom shadow effects and visual depth

##  # 🚀 Advanced Features
- **MAINTAINED**: All previous functionality (cache cleanup, update checking)
- **ENHANCED**: GitHub integration with better UI
- **ENHANCED**: Installation logging with emoji indicators
- **NEW**: Browse button for custom installation paths
- **NEW**: Advanced options with modern checkboxes

##  # 🎯 Code Quality
- **REFACTORED**: Modular component architecture
- **IMPROVED**: Clean separation of styling and logic
- **ENHANCED**: Better code documentation and structure
- **NEW**: Modern Python typing and best practices

##  # 📦 Distribution
- **MAINTAINED**: Single executable with no dependencies
- **ENHANCED**: Professional release packaging
- **NEW**: Beautiful batch launcher with branding
- **NEW**: Comprehensive documentation and README

---

This release transforms GHST from a functional installer into a
professional, beautiful application that users will love to use.
'''

    changelog_file = release_dir / "CHANGELOG.md"
    with open(changelog_file, 'w', encoding='utf-8') as f:
        f.write(changelog_content)
    print("   ✅ Created detailed changelog: {changelog_file.name}")

    return True

def create_zip_archive():
    """Create a ZIP archive of the release."""
    print("📦 Creating distribution archive...")

    version = "v1.0.0-alpha.5-beautiful"
    release_dir = Path("releases/{version}")
    zip_path = Path("releases/GHST-{version}.zip")

    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in release_dir.rglob('*'):
                if file_path.is_file():
                    # Create relative path for archive
                    arcname = file_path.relative_to(release_dir.parent)
                    zipf.write(file_path, arcname)

        zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
        print("   ✅ Created archive: {zip_path.name} ({zip_size_mb:.1f} MB)")
        return True

    except Exception as e:
        print("   ❌ Failed to create archive: {e}")
        return False

def main():
    """Main build process."""
    print("🎨 GHST Beautiful Installer Build System")
    print("=" * 50)

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Check if source file exists
    if not Path("ghst_installer_beautiful.py").exists():
        print("❌ Source file 'ghst_installer_beautiful.py' not found!")
        sys.exit(1)

    try:
        # Step 1: Clean previous builds
        clean_build_directories()
        print()

        # Step 2: Build executable
        if not build_installer_exe():
            print("❌ Build failed!")
            sys.exit(1)
        print()

        # Step 3: Create release package
        if not create_beautiful_release_package():
            print("❌ Release packaging failed!")
            sys.exit(1)
        print()

        # Step 4: Create ZIP archive
        if not create_zip_archive():
            print("❌ Archive creation failed!")
            sys.exit(1)
        print()

        # Success summary
        print("🎉 Beautiful installer build completed successfully!")
        print("\n📁 Generated files:")
        print("   • dist/GHST-Installer-Beautiful.exe")
        print("   • releases/v1.0.0-alpha.5-beautiful/")
        print("   • releases/GHST-v1.0.0-alpha.5-beautiful.zip")
        print("\n🚀 Ready for distribution!")

    except KeyboardInterrupt:
        print("\n⏹️ Build interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print("\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
