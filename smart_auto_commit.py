#!/usr/bin/env python3
"""
GHST Smart Auto-Commit System
============================

Automatically commits and pushes changes in small, manageable batches
to avoid GitHub's size limits and connection issues.

Features:
- Breaks changes into small batches (under 50MB each)
- Excludes large binary files automatically
- Smart file grouping by type and size
- Automatic commit message generation
- Progress tracking and retry logic
- Configurable batch sizes and exclusions
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CommitBatch:
    """Represents a batch of files to commit together"""
    files: List[str]
    size_mb: float
    description: str
    category: str

class SmartAutoCommit:
    """Smart auto-commit system for GHST repository"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.max_batch_size_mb = 25  # Conservative 25MB limit
        self.max_files_per_batch = 50  # Max files per commit
        
        # File exclusions (large binaries, build artifacts)
        self.exclude_patterns = [
            "*.exe", "*.zip", "*.pkg", "*.dmg", "*.msi",
            "build/", "dist/", "__pycache__/", "*.pyc",
            "node_modules/", ".git/", "*.log", "*.tmp",
            "*.spec", "*.toc", "*.pyz"
        ]
        
        # File categories for smart grouping
        self.file_categories = {
            "core_system": [
                "core/src/ai_collaboration/",
                "core/src/plugins/",
                "core/src/utils/",
                "core/src/ui_components/"
            ],
            "think_tank": [
                "phd_think_tank.py",
                "think_tank_gui.py", 
                "think_tank_integration.py",
                "launch_think_tank.py",
                "README_THINK_TANK.md"
            ],
            "installers": [
                "ghst_installer_",
                "build_",
                "install_",
                "launcher.py"
            ],
            "documentation": [
                "README", "CHANGELOG", "LICENSE", 
                "docs/", "*.md"
            ],
            "scripts": [
                "scripts/", "*.py", "*.bat", "*.sh"
            ],
            "config": [
                "config/", "*.json", "*.yaml", "*.yml", "*.toml"
            ],
            "releases": [
                "releases/"
            ]
        }
    
    def get_file_size_mb(self, file_path: str) -> float:
        """Get file size in MB"""
        try:
            size_bytes = os.path.getsize(self.repo_path / file_path)
            return size_bytes / (1024 * 1024)
        except (OSError, FileNotFoundError):
            return 0.0
    
    def should_exclude_file(self, file_path: str) -> bool:
        """Check if file should be excluded"""
        file_path_str = str(file_path).replace("\\", "/")
        
        for pattern in self.exclude_patterns:
            if pattern.endswith("/"):
                # Directory pattern
                if pattern[:-1] in file_path_str:
                    return True
            elif pattern.startswith("*."):
                # Extension pattern
                if file_path_str.endswith(pattern[1:]):
                    return True
            elif pattern in file_path_str:
                # General pattern
                return True
        
        # Exclude files larger than 10MB
        if self.get_file_size_mb(file_path) > 10:
            return True
        
        return False
    
    def categorize_file(self, file_path: str) -> str:
        """Categorize file based on path and name"""
        file_path_str = str(file_path).replace("\\", "/")
        
        for category, patterns in self.file_categories.items():
            for pattern in patterns:
                if pattern.endswith("/"):
                    if file_path_str.startswith(pattern):
                        return category
                elif pattern in file_path_str:
                    return category
        
        return "misc"
    
    def get_changed_files(self) -> List[str]:
        """Get list of changed files from git"""
        try:
            # Get staged and unstaged changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            changed_files = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    # Parse git status output
                    status = line[:2]
                    file_path = line[3:].strip()
                    
                    # Handle renamed files
                    if ' -> ' in file_path:
                        file_path = file_path.split(' -> ')[1]
                    
                    # Skip deleted files
                    if 'D' not in status and file_path:
                        changed_files.append(file_path)
            
            return changed_files
            
        except subprocess.CalledProcessError:
            print("❌ Error getting changed files")
            return []
    
    def create_batches(self, files: List[str]) -> List[CommitBatch]:
        """Create smart batches of files for committing"""
        # Filter out excluded files
        filtered_files = [f for f in files if not self.should_exclude_file(f)]
        
        if not filtered_files:
            return []
        
        # Group files by category
        categorized = {}
        for file_path in filtered_files:
            category = self.categorize_file(file_path)
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(file_path)
        
        batches = []
        
        # Create batches for each category
        for category, category_files in categorized.items():
            current_batch = []
            current_size = 0.0
            
            for file_path in category_files:
                file_size = self.get_file_size_mb(file_path)
                
                # Check if adding this file would exceed limits
                if (current_size + file_size > self.max_batch_size_mb or 
                    len(current_batch) >= self.max_files_per_batch):
                    
                    # Create batch with current files
                    if current_batch:
                        batches.append(CommitBatch(
                            files=current_batch.copy(),
                            size_mb=current_size,
                            description=self.generate_batch_description(category, current_batch),
                            category=category
                        ))
                    
                    # Start new batch
                    current_batch = [file_path]
                    current_size = file_size
                else:
                    current_batch.append(file_path)
                    current_size += file_size
            
            # Add remaining files as final batch
            if current_batch:
                batches.append(CommitBatch(
                    files=current_batch,
                    size_mb=current_size,
                    description=self.generate_batch_description(category, current_batch),
                    category=category
                ))
        
        return batches
    
    def generate_batch_description(self, category: str, files: List[str]) -> str:
        """Generate descriptive commit message for batch"""
        category_emojis = {
            "think_tank": "🧠",
            "core_system": "🔧",
            "installers": "🎨",
            "documentation": "📚",
            "scripts": "⚙️",
            "config": "⚙️",
            "releases": "📦",
            "misc": "🔄"
        }
        
        category_names = {
            "think_tank": "PhD Think Tank System",
            "core_system": "Core AI Collaboration System", 
            "installers": "Installer and Build Tools",
            "documentation": "Documentation Updates",
            "scripts": "Scripts and Utilities",
            "config": "Configuration Files",
            "releases": "Release Packages",
            "misc": "Miscellaneous Updates"
        }
        
        emoji = category_emojis.get(category, "🔄")
        name = category_names.get(category, "Updates")
        
        # Add file count info
        file_count = len(files)
        if file_count == 1:
            file_info = f"1 file"
        else:
            file_info = f"{file_count} files"
        
        return f"{emoji} {name} ({file_info})"
    
    def commit_batch(self, batch: CommitBatch) -> bool:
        """Commit a single batch of files"""
        try:
            print(f"📝 Committing {batch.description}")
            print(f"   Files: {len(batch.files)}, Size: {batch.size_mb:.1f}MB")
            
            # Add files to staging
            for file_path in batch.files:
                subprocess.run(
                    ["git", "add", file_path],
                    cwd=self.repo_path,
                    check=True,
                    capture_output=True
                )
            
            # Create detailed commit message
            commit_msg = f"{batch.description}\n\n"
            commit_msg += f"📁 Files updated ({len(batch.files)}):\n"
            
            # List first 10 files, then summarize rest
            for i, file_path in enumerate(batch.files[:10]):
                commit_msg += f"- {file_path}\n"
            
            if len(batch.files) > 10:
                commit_msg += f"... and {len(batch.files) - 10} more files\n"
            
            commit_msg += f"\n📊 Batch size: {batch.size_mb:.1f}MB"
            commit_msg += f"\n🏷️  Category: {batch.category}"
            
            # Commit
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            
            print(f"✅ Committed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Commit failed: {e}")
            return False
    
    def push_commits(self, batch_count: int) -> bool:
        """Push all commits to remote"""
        try:
            print(f"🚀 Pushing {batch_count} commits to remote...")
            
            # Configure git for large pushes
            subprocess.run(
                ["git", "config", "http.postBuffer", "52428800"],  # 50MB buffer
                cwd=self.repo_path,
                capture_output=True
            )
            
            subprocess.run(
                ["git", "config", "http.lowSpeedLimit", "1000"],
                cwd=self.repo_path,
                capture_output=True
            )
            
            subprocess.run(
                ["git", "config", "http.lowSpeedTime", "300"],
                cwd=self.repo_path,
                capture_output=True
            )
            
            # Push with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    result = subprocess.run(
                        ["git", "push", "origin", "main"],
                        cwd=self.repo_path,
                        capture_output=True,
                        text=True,
                        timeout=300  # 5 minute timeout
                    )
                    
                    if result.returncode == 0:
                        print("✅ Push successful!")
                        return True
                    else:
                        print(f"⚠️  Push attempt {attempt + 1} failed: {result.stderr}")
                        
                except subprocess.TimeoutExpired:
                    print(f"⚠️  Push attempt {attempt + 1} timed out")
                
                if attempt < max_retries - 1:
                    print(f"🔄 Retrying in {(attempt + 1) * 5} seconds...")
                    time.sleep((attempt + 1) * 5)
            
            print("❌ All push attempts failed")
            return False
            
        except Exception as e:
            print(f"❌ Push error: {e}")
            return False
    
    def run_auto_commit(self) -> bool:
        """Run the complete auto-commit process"""
        print("🤖 GHST Smart Auto-Commit System")
        print("=" * 50)
        
        # Check if we're in a git repository
        if not (self.repo_path / ".git").exists():
            print("❌ Not in a git repository")
            return False
        
        # Get changed files
        print("🔍 Scanning for changed files...")
        changed_files = self.get_changed_files()
        
        if not changed_files:
            print("✅ No changes to commit")
            return True
        
        print(f"📋 Found {len(changed_files)} changed files")
        
        # Create smart batches
        print("🧠 Creating smart commit batches...")
        batches = self.create_batches(changed_files)
        
        if not batches:
            print("⚠️  No files to commit after filtering")
            return True
        
        print(f"📦 Created {len(batches)} commit batches:")
        for i, batch in enumerate(batches, 1):
            print(f"   {i}. {batch.description} - {batch.size_mb:.1f}MB")
        
        # Confirm with user
        response = input(f"\n🚀 Proceed with {len(batches)} commits? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Auto-commit cancelled")
            return False
        
        # Commit each batch
        successful_batches = 0
        for i, batch in enumerate(batches, 1):
            print(f"\n📝 Processing batch {i}/{len(batches)}")
            if self.commit_batch(batch):
                successful_batches += 1
                time.sleep(1)  # Brief pause between commits
            else:
                print(f"❌ Batch {i} failed, stopping...")
                break
        
        if successful_batches == 0:
            print("❌ No commits were successful")
            return False
        
        # Push all commits
        print(f"\n🚀 Pushing {successful_batches} commits...")
        success = self.push_commits(successful_batches)
        
        if success:
            print(f"\n🎉 Auto-commit complete! {successful_batches}/{len(batches)} batches committed and pushed")
        else:
            print(f"\n⚠️  Commits created but push failed. {successful_batches} commits are ready to push manually")
        
        return success

def main():
    """Main entry point"""
    auto_commit = SmartAutoCommit()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(__doc__)
        return
    
    success = auto_commit.run_auto_commit()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
