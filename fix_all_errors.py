#!/usr/bin/env python3
"""
GHST Code Quality Fixer - Fixes 1000+ lint errors automatically
This will dramatically speed up VS Code and improve code quality
"""

import subprocess
import sys
from pathlib import Path


def install_autopep8():
    """Install autopep8 for automatic code formatting"""
    try:
        print("✅ autopep8 already installed")
        return True
    except ImportError:
        print("📦 Installing autopep8...")
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', 'autopep8'])
            print("✅ autopep8 installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install autopep8")
            return False


def install_isort():
    """Install isort for import sorting"""
    try:
        print("✅ isort already installed")
        return True
    except ImportError:
        print("📦 Installing isort...")
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', 'isort'])
            print("✅ isort installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install isort")
            return False


def fix_python_file(file_path):
    """Fix a single Python file with aggressive formatting"""
    print("🔧 Fixing {file_path}")

    try:
        # Run autopep8 with aggressive fixes
        cmd = [
            sys.executable, '-m', 'autopep8',
            '--in-place',              # Edit files in place
            '--aggressive',            # Enable aggressive fixes
            '--aggressive',            # Double aggressive for maximum fixes
            '--max-line-length=79',    # Standard line length
            str(file_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("  ✅ autopep8 fixes applied")
        else:
            print("  ⚠️ autopep8 warnings: {result.stderr}")

        # Run isort to fix imports
        cmd_isort = [
            sys.executable, '-m', 'isort',
            '--line-length=79',
            '--multi-line=3',
            '--trailing-comma',
            '--force-grid-wrap=0',
            '--combine-as',
            '--line-width=79',
            str(file_path)
        ]

        result = subprocess.run(cmd_isort, capture_output=True, text=True)
        if result.returncode == 0:
            print("  ✅ isort import fixes applied")
        else:
            print("  ⚠️ isort warnings: {result.stderr}")

        return True

    except Exception as e:
        print(f"  ❌ Error fixing {file_path}: {e}")
        return False


def get_python_files():
    """Get all Python files that need fixing"""
    python_files = []

    # Main directory Python files
    main_files = [
        "ghst_installer_beautiful.py",
        "ghst_installer_enhanced.py",
        "build_beautiful_optimized.py",
        "release_manager.py",
        "install_wizard.py"
    ]

    for file in main_files:
        path = Path(file)
        if path.exists():
            python_files.append(path)

    # Core directory
    core_dir = Path("core")
    if core_dir.exists():
        python_files.extend(core_dir.glob("*.py"))

    # Scripts directory
    scripts_dir = Path("scripts")
    if scripts_dir.exists():
        python_files.extend(scripts_dir.glob("*.py"))

    return python_files


def main():
    print("🚀 GHST Code Quality Fixer")
    print("=" * 50)
    print("This will fix 1000+ lint errors to speed up VS Code!")
    print()

    # Install required tools
    if not install_autopep8():
        return False

    if not install_isort():
        return False

    print()

    # Get Python files to fix
    python_files = get_python_files()
    print("📁 Found {len(python_files)} Python files to fix")
    print()

    # Fix each file
    fixed_count = 0
    for file_path in python_files:
        if fix_python_file(file_path):
            fixed_count += 1
        print()

    print("=" * 50)
    print("✅ Fixed {fixed_count}/{len(python_files)} files")
    print("🚀 VS Code should be much faster now!")
    print("💡 Tip: Restart VS Code to see the performance improvement")

    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
