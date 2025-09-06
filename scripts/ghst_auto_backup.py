#!/usr/bin/env python3
"""
GHST Automated Backup System
============================

Creates comprehensive backups before any automation begins.
Multiple backup strategies for maximum safety.
"""

import json
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

class GHSTBackupManager:
    """Comprehensive backup system for GHST workspace."""

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.backup_root = Path.home() / "GHST_BACKUPS"
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Create backup directory structure
        self.backup_root.mkdir(exist_ok=True)
        self.session_backup = self.backup_root / "session_{self.timestamp}"
        self.session_backup.mkdir(exist_ok=True)

        print("🔒 Backup Manager initialized")
        print("📁 Workspace: {self.workspace_path}")
        print("💾 Backup location: {self.session_backup}")

    def create_full_backup(self):
        """Create multiple types of backups for maximum safety."""

        print("\n🚀 Starting comprehensive backup process...")

        backups_created = []

        # 1. Full directory copy
        try:
            full_backup = self._create_directory_backup()
            backups_created.append(("Full Directory Copy", full_backup))
            print("✅ Full directory backup: {full_backup}")
        except Exception as e:
            print("❌ Full backup failed: {e}")

        # 2. ZIP archive
        try:
            zip_backup = self._create_zip_backup()
            backups_created.append(("ZIP Archive", zip_backup))
            print("✅ ZIP backup: {zip_backup}")
        except Exception as e:
            print("❌ ZIP backup failed: {e}")

        # 3. Git backup (if git repo)
        try:
            git_backup = self._create_git_backup()
            if git_backup:
                backups_created.append(("Git Backup", git_backup))
                print("✅ Git backup: {git_backup}")
        except Exception as e:
            print("❌ Git backup failed: {e}")

        # 4. Critical files backup
        try:
            critical_backup = self._backup_critical_files()
            backups_created.append(("Critical Files", critical_backup))
            print("✅ Critical files backup: {critical_backup}")
        except Exception as e:
            print("❌ Critical files backup failed: {e}")

        # 5. Create backup manifest
        self._create_backup_manifest(backups_created)

        print("\n🎉 Backup process complete!")
        print("📊 {len(backups_created)} backup types created")
        print(
            "📋 Manifest saved to: {
                self.session_backup /
                'backup_manifest.json'}")

        return self.session_backup

    def _create_directory_backup(self):
        """Create a full directory copy backup."""

        backup_dir = self.session_backup / "full_copy"

        # Ignore patterns for backup
        def ignore_patterns(dir, files):
            ignore_list = []
            for file in files:
                if any(pattern in file for pattern in [
                    '__pycache__', '.pyc', '.git', 'node_modules',
                    '.vscode', '.idea', 'GHST_BACKUPS'
                ]):
                    ignore_list.append(file)
            return ignore_list

        shutil.copytree(
            self.workspace_path,
            backup_dir,
            ignore=ignore_patterns
        )

        return str(backup_dir)

    def _create_zip_backup(self):
        """Create a compressed ZIP backup."""

        zip_path = self.session_backup / "ghst_backup_{self.timestamp}.zip"

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.workspace_path):
                # Skip unwanted directories
                dirs[:] = [
                    d for d in dirs if d not in [
                        '__pycache__',
                        '.git',
                        'node_modules',
                        '.vscode',
                        'GHST_BACKUPS']]

                for file in files:
                    if not file.endswith('.pyc'):
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(self.workspace_path)
                        zipf.write(file_path, arcname)

        return str(zip_path)

    def _create_git_backup(self):
        """Create git-based backup if repository exists."""

        git_dir = self.workspace_path / '.git'
        if not git_dir.exists():
            return None

        try:
            # Create git bundle
            bundle_path = self.session_backup / \
                f"ghst_git_{self.timestamp}.bundle"

            subprocess.run([
                'git', 'bundle', 'create', str(bundle_path), '--all'
            ], cwd=self.workspace_path, check=True, capture_output=True)

            # Also export current state
            subprocess.run([
                'git', 'archive', '--format=zip',
                '--output={self.session_backup / "git_snapshot_{self.timestamp}.zip"}',
                'HEAD'
            ], cwd=self.workspace_path, check=True, capture_output=True)

            return str(bundle_path)

        except subprocess.CalledProcessError:
            return None

    def _backup_critical_files(self):
        """Backup critical configuration and code files separately."""

        critical_dir = self.session_backup / "critical_files"
        critical_dir.mkdir(exist_ok=True)

        # Critical file patterns
        critical_patterns = [
            '*.py', '*.md', '*.json', '*.yaml', '*.yml',
            '*.txt', '*.toml', '*.cfg', '*.ini'
        ]

        critical_files = []
        for pattern in critical_patterns:
            critical_files.extend(self.workspace_path.rglob(pattern))

        # Copy critical files maintaining structure
        for file_path in critical_files:
            if any(skip in str(file_path) for skip in [
                '__pycache__', '.git', 'GHST_BACKUPS'
            ]):
                continue

            rel_path = file_path.relative_to(self.workspace_path)
            dest_path = critical_dir / rel_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, dest_path)

        return str(critical_dir)

    def _create_backup_manifest(self, backups_created):
        """Create a manifest of all backups created."""

        manifest = {
            'timestamp': self.timestamp,
            'workspace_path': str(self.workspace_path),
            'backup_session': str(self.session_backup),
            'backups': [
                {
                    'type': backup_type,
                    'path': backup_path,
                    'size_mb': self._get_size_mb(backup_path)
                }
                for backup_type, backup_path in backups_created
            ],
            'system_info': {
                'platform': sys.platform,
                'python_version': sys.version,
                'working_directory': os.getcwd()
            }
        }

        manifest_path = self.session_backup / 'backup_manifest.json'
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        return manifest_path

    def _get_size_mb(self, path):
        """Get size of file or directory in MB."""
        path_obj = Path(path)

        if path_obj.is_file():
            return round(path_obj.stat().st_size / (1024 * 1024), 2)
        elif path_obj.is_dir():
            total_size = sum(
                f.stat().st_size for f in path_obj.rglob('*') if f.is_file()
            )
            return round(total_size / (1024 * 1024), 2)

        return 0

    def verify_backups(self):
        """Verify all backups were created successfully."""

        manifest_path = self.session_backup / 'backup_manifest.json'
        if not manifest_path.exists():
            print("❌ No backup manifest found!")
            return False

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        print("\n🔍 Verifying backups...")
        all_good = True

        for backup in manifest['backups']:
            backup_path = Path(backup['path'])
            if backup_path.exists():
                print("✅ {backup['type']}: {backup['size_mb']} MB")
            else:
                print("❌ {backup['type']}: NOT FOUND")
                all_good = False

        if all_good:
            print("\n🎉 All backups verified successfully!")
            print("📁 Backup location: {self.session_backup}")
        else:
            print("\n⚠️ Some backups are missing!")

        return all_good

def main():
    """Main backup execution."""

    # Get workspace path
    workspace = Path.cwd()

    print("=" * 60)
    print("🔒 GHST AUTOMATED BACKUP SYSTEM")
    print("=" * 60)

    # Create backup manager
    backup_manager = GHSTBackupManager(str(workspace))

    # Create backups
    backup_location = backup_manager.create_full_backup()

    # Verify backups
    if backup_manager.verify_backups():
        print("\n✅ Ready for automation!")
        print("📁 Backups stored at: {backup_location}")
        return True
    else:
        print("\n❌ Backup verification failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
