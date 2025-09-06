#!/usr/bin/env python3
"""
GHST Beautiful Installer Builder - Size Optimized
Creates a minimal, beautiful standalone executable installer
"""

import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


def clean_build_dirs():
    """Clean previous build artifacts"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Cleaning {dir_name}/")
            shutil.rmtree(dir_name, ignore_errors=True)

    # Remove spec files
    for spec_file in Path('.').glob('*.spec'):
        print(f"🧹 Removing {spec_file}")
        spec_file.unlink()


def build_optimized_installer():
    """Build optimized beautiful installer"""
    print("🚀 Building GHST Beautiful Installer (Optimized)...")

    # PyInstaller command with maximum optimization
    cmd = [
        'pyinstaller',
        '--onefile',                    # Single executable
        '--windowed',                   # No console window
        '--name=GHST-Installer-Beautiful-Optimized',
        '--clean',                      # Clean cache
        '--noconfirm',                  # Overwrite without asking
        '--optimize=2',                 # Maximum Python optimization
        '--strip',                      # Strip debug symbols
        '--exclude-module=tkinter',     # Don't need tkinter
        '--exclude-module=matplotlib',  # Don't need matplotlib
        '--exclude-module=PIL',         # Don't need PIL
        '--exclude-module=numpy',       # Don't need numpy
        '--exclude-module=pandas',      # Don't need pandas
        '--exclude-module=scipy',       # Don't need scipy
        '--exclude-module=sklearn',     # Don't need sklearn
        '--exclude-module=tensorflow',  # Don't need tensorflow
        '--exclude-module=torch',       # Don't need torch
        '--exclude-module=cv2',         # Don't need opencv
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=requests',
        'ghst_installer_beautiful.py'
    ]

    try:
        print("⚡ Running PyInstaller with optimization...")
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True)
        print("✅ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def create_optimized_release():
    """Create optimized release package"""
    version = "v1.0.0-alpha.5-beautiful-optimized"
    release_dir = Path(f"releases/{version}")

    # Create release directory
    release_dir.mkdir(parents=True, exist_ok=True)

    # Copy executable
    exe_source = Path("dist/GHST-Installer-Beautiful-Optimized.exe")
    exe_dest = release_dir / "GHST-Installer-Beautiful-Optimized.exe"

    if exe_source.exists():
        print(f"📦 Copying executable to {exe_dest}")
        shutil.copy2(exe_source, exe_dest)

        # Get file size
        size_mb = exe_dest.stat().st_size / (1024 * 1024)
        print(f"📏 Executable size: {size_mb:.1f} MB")
    else:
        print("❌ Executable not found!")
        return False

    # Create batch launcher
    batch_content = '''@echo off
echo 🚀 Launching GHST Beautiful Installer (Optimized)...
echo.
echo ✨ Modern UI with dark theme and animations
echo 🎯 No Python installation required
echo 📦 Professional installation experience
echo.
pause
echo Starting installer...
"%~dp0GHST-Installer-Beautiful-Optimized.exe"
'''

    batch_file = release_dir / "Install-GHST-Beautiful-Optimized.bat"
    batch_file.write_text(batch_content, encoding='utf-8')

    # Create README
    readme_content = f'''  # 🎨 GHST Beautiful Installer (Optimized) - {version}

#  # ✨ What's New
- **Beautiful modern UI** with dark theme and animations
- **Size optimized** - minimal footprint executable
- **Zero dependencies** - works on any Windows system
- **Professional installation experience**

#  # 🚀 Quick Install
1. Run `Install-GHST-Beautiful-Optimized.bat`
2. Or double-click `GHST-Installer-Beautiful-Optimized.exe`

#  # 📋 Features
- 🎨 Modern glassmorphism UI design
- 🌙 Beautiful dark theme with gradients
- ⚡ Smooth animations and transitions
- 🧹 Smart cache cleanup system
- 🔄 Integrated update checking
- 📁 Professional installation management

#  # 📏 Technical Details
- **Size**: {size_mb:.1f} MB (optimized)
- **Dependencies**: None - fully standalone
- **Platform**: Windows 10/11
- **Architecture**: x64

---
**GHST AI Coding Engine** - Professional AI-powered development tools
'''

    readme_file = release_dir / "README.md"
    readme_file.write_text(readme_content, encoding='utf-8')

    # Create ZIP archive
    zip_path = Path(f"releases/GHST-{version}.zip")
    print(f"📦 Creating release archive: {zip_path}")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in release_dir.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(release_dir)
                zipf.write(file, arcname)

    archive_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"📏 Archive size: {archive_size_mb:.1f} MB")

    return True


def main():
    print("🎨 GHST Beautiful Installer Builder (Size Optimized)")
    print("=" * 50)

    # Clean previous builds
    clean_build_dirs()

    # Build optimized installer
    if not build_optimized_installer():
        print("❌ Build failed!")
        return False

    # Create release package
    if not create_optimized_release():
        print("❌ Release creation failed!")
        return False

    print("\n✅ Beautiful installer built successfully!")
    print("🎯 Ready for distribution with modern UI and optimized size")

    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
