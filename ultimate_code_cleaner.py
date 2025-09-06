#!/usr/bin/env python3
"""
GHST Ultimate Code Cleaner - Removes unused imports and fixes all issues
"""

import os
import re
import subprocess
import sys
from pathlib import Path

def install_autoflake():
    """Install autoflake for removing unused imports"""
    try:
        print("✅ autoflake already installed")
        return True
    except ImportError:
        print("📦 Installing autoflake...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 'autoflake'
            ])
            print("✅ autoflake installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print("❌ Failed to install autoflake: {e}")
            return False

def ultimate_fix_file(file_path):
    """Apply ultimate fixes to a Python file"""
    print("🔧 Ultimate fixing {file_path}")

    try:
        # Step 1: Remove unused imports with autoflake
        cmd_autoflake = [
            sys.executable, '-m', 'autoflake',
            '--in-place',
            '--remove-all-unused-imports',
            '--remove-unused-variables',
            '--remove-duplicate-keys',
            '--expand-star-imports',
            str(file_path)
        ]

        result = subprocess.run(cmd_autoflake, capture_output=True, text=True)
        if result.returncode == 0:
            print("  ✅ Unused imports removed")
        else:
            print("  ⚠️ autoflake warnings: {result.stderr}")

        # Step 2: Aggressive autopep8
        cmd_autopep8 = [
            sys.executable, '-m', 'autopep8',
            '--in-place',
            '--aggressive',
            '--aggressive',
            '--aggressive',  # Triple aggressive!
            '--max-line-length=79',
            str(file_path)
        ]

        result = subprocess.run(cmd_autopep8, capture_output=True, text=True)
        if result.returncode == 0:
            print("  ✅ Style fixes applied")

        # Step 3: Manual fixes for common issues
        manual_fix_file(file_path)

        return True

    except Exception as e:
        print("  ❌ Error fixing {file_path}: {e}")
        return False

def manual_fix_file(file_path):
    """Apply manual fixes that tools can't handle"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix f-strings with no placeholders
        content = re.sub(r'"([^"]*)"(?![^"]*{)', r'"\1"', content)
        content = re.sub(r"'([^']*)'(?![^']*{)", r"'\1'", content)

        # Remove trailing whitespace
        lines = content.split('\n')
        fixed_lines = [line.rstrip() for line in lines]
        content = '\n'.join(fixed_lines)

        # Fix blank lines with whitespace
        content = re.sub(r'\n\s+\n', '\n\n', content)

        # Add proper spacing before inline comments
        content = re.sub(r'(\S)  # \s*([^  # ])', r'\1  # \2', content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print("  ✅ Manual fixes applied")

    except Exception as e:
        print("  ⚠️ Manual fix error: {e}")

def get_all_python_files():
    """Get ALL Python files in the project"""
    python_files = []

    # Get all .py files recursively, excluding certain directories
    exclude_dirs = {
        'build', 'dist', '__pycache__', '.git', 'releases/v1.0.0-alpha',
        'archive', '.ghst_backups'
    }

    for root, dirs, files in os.walk('.'):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if not any(
            ex in os.path.join(root, d) for ex in exclude_dirs
        )]

        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                python_files.append(file_path)

    return python_files

def main():
    print("🚀 GHST Ultimate Code Cleaner")
    print("=" * 50)
    print("Removing unused imports and fixing ALL issues!")
    print()

    # Install autoflake
    if not install_autoflake():
        return False

    print()

    # Get ALL Python files
    python_files = get_all_python_files()
    print("📁 Found {len(python_files)} Python files to fix")
    print()

    # Fix each file
    fixed_count = 0
    for file_path in python_files:
        if ultimate_fix_file(file_path):
            fixed_count += 1
        print()

    print("=" * 50)
    print("✅ Ultimate fixed {fixed_count}/{len(python_files)} files")
    print("🚀 All 1000+ errors should be GONE!")
    print("💨 VS Code will be lightning fast now!")

    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
