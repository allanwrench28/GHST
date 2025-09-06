#!/usr/bin/env python3
"""
GHST Release Manager
Intelligent release management system that maintains clean release structure
while preserving important versions for rollback and compatibility.
"""

import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

class ReleaseManager:
    def __init__(self, releases_dir="releases"):
        self.releases_dir = Path(releases_dir)
        self.archive_dir = self.releases_dir / "archive"
        self.config_file = self.releases_dir / "release_config.json"

        # Ensure directories exist
        self.archive_dir.mkdir(exist_ok=True)

        # Load or create config
        self.config = self.load_config()

    def load_config(self):
        """Load release management configuration"""
        default_config = {
            "keep_recent_versions": 3,
            "archive_older_than_days": 90,
            # Always keep major releases
            "preserve_milestones": ["v1.0.0", "v2.0.0"],
            "last_cleanup": None
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except BaseException:
                return default_config
        return default_config

    def save_config(self):
        """Save release management configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def parse_version(self, version_string):
        """Parse version string into comparable tuple"""
        # Extract version numbers (handles alpha, beta, rc suffixes)
        match = re.match(r'v?(\d+)\.(\d+)\.(\d+)(?:-([^.]+))?', version_string)
        if match:
            major, minor, patch, suffix = match.groups()
            # Convert to tuple for comparison
            return (int(major), int(minor), int(patch), suffix or "")
        return (0, 0, 0, "")

    def get_release_versions(self):
        """Get all release versions sorted by version number"""
        versions = []
        for item in self.releases_dir.iterdir():
            if item.is_dir() and item.name.startswith('v') and item.name != "archive":
                versions.append(item.name)

        # Sort by version number (newest first)
        versions.sort(key=self.parse_version, reverse=True)
        return versions

    def is_milestone_version(self, version):
        """Check if version is a milestone that should be preserved"""
        return any(
            milestone in version for milestone in self.config["preserve_milestones"])

    def clean_old_releases(self, dry_run=False):
        """Clean old releases according to policy"""
        print("🧹 GHST Release Manager - Cleaning old releases...")

        versions = self.get_release_versions()
        keep_recent = self.config["keep_recent_versions"]

        if len(versions) <= keep_recent:
            print("✅ Only {len(versions)} versions found, keeping all")
            return

        # Versions to keep (recent + milestones)
        keep_versions = set(versions[:keep_recent])
        for version in versions:
            if self.is_milestone_version(version):
                keep_versions.add(version)
                print("🎯 Preserving milestone: {version}")

        # Versions to archive
        archive_versions = [v for v in versions if v not in keep_versions]

        if not archive_versions:
            print("✅ No versions need archiving")
            return

        print("\n📦 Archiving {len(archive_versions)} old versions:")
        for version in archive_versions:
            print("   • {version}")

        if dry_run:
            print("\n🔍 DRY RUN - No files were moved")
            return

        # Move to archive
        for version in archive_versions:
            source = self.releases_dir / version
            target = self.archive_dir / version

            if target.exists():
                shutil.rmtree(target)

            shutil.move(str(source), str(target))
            print("📁 Moved {version} → archive/")

        # Update config
        self.config["last_cleanup"] = datetime.now().isoformat()
        self.save_config()

        print(
            "\n✨ Cleanup complete! Keeping {
                len(keep_versions)} active versions")

    def create_new_release(self, version, source_files):
        """Create a new release and manage old ones"""
        print("🚀 Creating new release: {version}")

        # Create release directory
        release_dir = self.releases_dir / version
        release_dir.mkdir(exist_ok=True)

        # Copy files to release
        for source_path, target_name in source_files.items():
            if os.path.exists(source_path):
                target_path = release_dir / target_name
                if os.path.isfile(source_path):
                    shutil.copy2(source_path, target_path)
                else:
                    if target_path.exists():
                        shutil.rmtree(target_path)
                    shutil.copytree(source_path, target_path)
                print("📄 Added: {target_name}")

        print("✅ Release {version} created successfully")

        # Auto-cleanup old releases
        self.clean_old_releases()

    def list_releases(self):
        """List all releases with details"""
        print("📋 GHST Release History:")
        print("=" * 50)

        # Active releases
        active_versions = self.get_release_versions()
        if active_versions:
            print("\n🟢 Active Releases:")
            for version in active_versions:
                version_dir = self.releases_dir / version
                size = self.get_dir_size(version_dir)
                milestone = "🎯" if self.is_milestone_version(version) else "  "
                print("  {milestone} {version:<25} ({size})")

        # Archived releases
        archived_versions = []
        if self.archive_dir.exists():
            for item in self.archive_dir.iterdir():
                if item.is_dir():
                    archived_versions.append(item.name)

        if archived_versions:
            archived_versions.sort(key=self.parse_version, reverse=True)
            print("\n📦 Archived Releases:")
            for version in archived_versions:
                version_dir = self.archive_dir / version
                size = self.get_dir_size(version_dir)
                print("     {version:<25} ({size})")

        print(
            "\n📊 Total: {
                len(active_versions)} active, {
                len(archived_versions)} archived")

    def get_dir_size(self, path):
        """Get human-readable directory size"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)

        # Convert to human readable
        for unit in ['B', 'KB', 'MB', 'GB']:
            if total_size < 1024.0:
                return "{total_size:.1f} {unit}"
            total_size /= 1024.0
        return "{total_size:.1f} TB"

    def restore_from_archive(self, version):
        """Restore a version from archive to active releases"""
        archive_path = self.archive_dir / version
        if not archive_path.exists():
            print("❌ Version {version} not found in archive")
            return False

        target_path = self.releases_dir / version
        if target_path.exists():
            print("⚠️  Version {version} already exists in active releases")
            return False

        shutil.move(str(archive_path), str(target_path))
        print("✅ Restored {version} from archive to active releases")
        return True

def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="GHST Release Manager")
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all releases')
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Clean old releases')
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be cleaned without doing it')
    parser.add_argument('--restore', help='Restore version from archive')

    args = parser.parse_args()

    manager = ReleaseManager()

    if args.list:
        manager.list_releases()
    elif args.clean or args.dry_run:
        manager.clean_old_releases(dry_run=args.dry_run)
    elif args.restore:
        manager.restore_from_archive(args.restore)
    else:
        print("🎯 GHST Release Manager")
        print("Usage:")
        print("  python release_manager.py --list      # List all releases")
        print("  python release_manager.py --clean     # Clean old releases")
        print("  python release_manager.py --dry-run   # Preview cleanup")
        print(
            "  python release_manager.py --restore v1.0.0-alpha.3  # Restore from archive")

if __name__ == "__main__":
    main()
