#!/usr/bin/env python3
"""
GHST Auto-Commit Daemon
======================

Background process that automatically commits and pushes changes in small batches.
Runs continuously with user permission to auto-commit everything.
"""

import io
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

# Configure logging using UTF-8 safe handlers (prevents Windows console
# encoding errors)
_stdout_stream = io.TextIOWrapper(
    sys.stdout.buffer,
    encoding='utf-8',
    errors='replace')
file_handler = logging.FileHandler('auto_commit_daemon.log', encoding='utf-8')
stream_handler = logging.StreamHandler(_stdout_stream)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[file_handler, stream_handler]
)
logger = logging.getLogger(__name__)


class AutoCommitDaemon:
    """Background daemon for automatic git commits and pushes"""

    def __init__(self, config_file='auto_commit_config.json'):
        self.config = self.load_config(config_file)
        self.repo_path = Path(self.config.get('repo_path', '.'))
        self.check_interval = self.config.get('check_interval_minutes', 5) * 60
        self.max_batch_size_mb = self.config.get('max_batch_size_mb', 10)
        self.auto_push = self.config.get('auto_push', True)
        self.exclude_patterns = set(self.config.get('exclude_patterns', [
            '*.log', '*.tmp', '__pycache__', '.git', 'node_modules',
            '*.exe', '*.zip', '*.pkg', 'dist/', 'build/'
        ]))
        self.running = False

    def load_config(self, config_file):
        """Load configuration from file"""
        default_config = {
            'repo_path': '.',
            'check_interval_minutes': 5,
            'max_batch_size_mb': 10,
            'auto_push': True,
            'auto_pull': True,
            'exclude_patterns': [
                '*.log', '*.tmp', '__pycache__', '.git', 'node_modules',
                '*.exe', '*.zip', '*.pkg', 'dist/', 'build/', '*.pyc'
            ],
            'commit_message_templates': {
                'code': '🔧 Auto-commit: Code changes',
                'docs': '📚 Auto-commit: Documentation updates',
                'config': '⚙️ Auto-commit: Configuration changes',
                'features': '✨ Auto-commit: New features',
                'bugfix': '🐛 Auto-commit: Bug fixes',
                'cleanup': '🧹 Auto-commit: Code cleanup',
                'mixed': '📝 Auto-commit: Mixed changes'
            }
        }

        if os.path.exists(config_file):
            try:
                # Read config using UTF-8 and tolerant errors
                with open(config_file, 'r', encoding='utf-8', errors='replace') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
                logger.info(f"✅ Loaded config from {config_file}")
            except Exception as e:
                logger.warning(
                    f"⚠️ Could not load config: {e}. Using defaults.")
        else:
            # Create default config file using UTF-8
            try:
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                logger.info(f"📝 Created default config file: {config_file}")
            except Exception as e:
                logger.warning(f"⚠️ Could not create config file: {e}")

        return default_config

    def is_git_repo(self):
        """Check if current directory is a git repository"""
        try:
            subprocess.run(['git', 'rev-parse', '--git-dir'],
                           capture_output=True, check=True, cwd=self.repo_path)
            return True
        except subprocess.CalledProcessError:
            return False

    def get_git_status(self):
        """Get git status of repository"""
        try:
            # Get modified/new files
            result = subprocess.run(['git', 'status', '--porcelain'],
                                    capture_output=True, text=True, check=True,
                                    cwd=self.repo_path)

            changes = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    status = line[:2]
                    filepath = line[3:]
                    if not self.should_exclude_file(filepath):
                        changes.append((status, filepath))

            return changes
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Git status failed: {e}")
            return []

    def should_exclude_file(self, filepath):
        """Check if file should be excluded from auto-commit"""
        import fnmatch

        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(filepath, pattern):
                return True
            if fnmatch.fnmatch(os.path.basename(filepath), pattern):
                return True

        return False

    def get_file_size_mb(self, filepath):
        """Get file size in MB"""
        try:
            full_path = self.repo_path / filepath
            if full_path.exists():
                return full_path.stat().st_size / (1024 * 1024)
        except Exception:
            pass
        return 0

    def categorize_changes(self, changes):
        """Categorize changes by type"""
        categories = {
            'code': [],
            'docs': [],
            'config': [],
            'features': [],
            'bugfix': [],
            'cleanup': [],
            'mixed': []
        }

        for status, filepath in changes:
            ext = Path(filepath).suffix.lower()
            name = Path(filepath).name.lower()

            if ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h']:
                if 'test' in name or 'spec' in name:
                    categories['cleanup'].append((status, filepath))
                elif status == 'A ':  # New file
                    categories['features'].append((status, filepath))
                elif 'fix' in name or 'bug' in name:
                    categories['bugfix'].append((status, filepath))
                else:
                    categories['code'].append((status, filepath))
            elif ext in ['.md', '.rst', '.txt', '.doc']:
                categories['docs'].append((status, filepath))
            elif ext in ['.json', '.yaml', '.yml', '.ini', '.cfg', '.conf']:
                categories['config'].append((status, filepath))
            else:
                categories['mixed'].append((status, filepath))

        # Remove empty categories
        return {k: v for k, v in categories.items() if v}

    def create_batches(self, changes):
        """Create batches of changes under size limit"""
        categories = self.categorize_changes(changes)
        batches = []

        for category, files in categories.items():
            current_batch = []
            current_size = 0

            for status, filepath in files:
                file_size = self.get_file_size_mb(filepath)

                # If single file is too large, handle separately
                if file_size > self.max_batch_size_mb:
                    logger.warning(
                        f"⚠️ Large file {filepath} ({
                            file_size:.1f}MB) - skipping")
                    continue

                # If adding this file would exceed limit, start new batch
                if current_size + file_size > self.max_batch_size_mb and current_batch:
                    batches.append((category, current_batch, current_size))
                    current_batch = []
                    current_size = 0

                current_batch.append((status, filepath))
                current_size += file_size

            # Add final batch if not empty
            if current_batch:
                batches.append((category, current_batch, current_size))

        return batches

    def commit_batch(self, category, files, size_mb):
        """Commit a batch of files"""
        try:
            # Add files to staging
            filepaths = [filepath for _, filepath in files]

            # Add files one by one to handle any issues
            for filepath in filepaths:
                try:
                    subprocess.run(['git', 'add', filepath],
                                   check=True, cwd=self.repo_path)
                except subprocess.CalledProcessError as e:
                    logger.warning(f"⚠️ Could not add {filepath}: {e}")

            # Create commit message
            template = self.config['commit_message_templates'].get(
                category, '📝 Auto-commit: Changes')

            timestamp = datetime.now().strftime('%H:%M:%S')
            file_count = len(files)

            commit_message = f"{template}\n\n" \
                f"📊 Batch: {file_count} files ({size_mb:.1f}MB)\n" \
                f"⏰ Time: {timestamp}\n" \
                f"🤖 Auto-committed by GHST daemon"

            # Commit changes
            subprocess.run(['git', 'commit', '-m', commit_message],
                           check=True, cwd=self.repo_path)

            logger.info(
                f"✅ Committed {category} batch: {file_count} files ({
                    size_mb:.1f}MB)")

            # Auto-push if enabled
            if self.auto_push:
                try:
                    subprocess.run(['git', 'push'], check=True,
                                   cwd=self.repo_path)
                    logger.info(f"📤 Pushed {category} batch to remote")
                except subprocess.CalledProcessError as e:
                    logger.warning(f"⚠️ Push failed for {category} batch: {e}")

            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Commit failed for {category} batch: {e}")
            return False

    def auto_pull(self):
        """Pull latest changes from remote"""
        if not self.config.get('auto_pull', True):
            return

        try:
            subprocess.run(['git', 'pull'], check=True, cwd=self.repo_path)
            logger.info("📥 Pulled latest changes from remote")
        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️ Auto-pull failed: {e}")

    def process_changes(self):
        """Process all pending changes"""
        changes = self.get_git_status()

        if not changes:
            logger.debug("📋 No changes to commit")
            return

        logger.info(f"🔍 Found {len(changes)} changes to process")

        # Create batches
        batches = self.create_batches(changes)

        if not batches:
            logger.info("📝 No valid batches to commit")
            return

        logger.info(f"📦 Created {len(batches)} batches for auto-commit")

        # Process each batch
        success_count = 0
        for category, files, size_mb in batches:
            if self.commit_batch(category, files, size_mb):
                success_count += 1
                # Small delay between batches
                time.sleep(2)

        logger.info(
            f"🎯 Successfully committed {success_count}/{len(batches)} batches")

    def run_daemon(self):
        """Run the auto-commit daemon"""
        if not self.is_git_repo():
            logger.error("❌ Not a git repository!")
            return

        logger.info("🚀 Starting GHST Auto-Commit Daemon")
        logger.info(f"📁 Repository: {self.repo_path.absolute()}")
        logger.info(
            f"⏱️ Check interval: {
                self.check_interval /
                60:.1f} minutes")
        logger.info(f"📦 Max batch size: {self.max_batch_size_mb}MB")
        logger.info(f"📤 Auto-push: {'✅' if self.auto_push else '❌'}")

        self.running = True

        try:
            while self.running:
                try:
                    # Pull latest changes first
                    self.auto_pull()

                    # Process any pending changes
                    self.process_changes()

                    # Wait for next check
                    logger.debug(
                        f"😴 Sleeping for {
                            self.check_interval /
                            60:.1f} minutes")
                    time.sleep(self.check_interval)

                except KeyboardInterrupt:
                    logger.info("⚠️ Received interrupt signal")
                    break
                except Exception as e:
                    logger.error(f"❌ Daemon error: {e}")
                    time.sleep(60)  # Wait 1 minute before retrying

        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            logger.info("👋 GHST Auto-Commit Daemon stopped")

    def stop_daemon(self):
        """Stop the daemon"""
        self.running = False


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='GHST Auto-Commit Daemon')
    parser.add_argument('--config', default='auto_commit_config.json',
                        help='Configuration file path')
    parser.add_argument('--once', action='store_true',
                        help='Run once instead of as daemon')
    parser.add_argument('--check-interval', type=int, default=5,
                        help='Check interval in minutes')

    args = parser.parse_args()

    # Create daemon
    daemon = AutoCommitDaemon(args.config)

    # Override check interval if provided
    if args.check_interval != 5:
        daemon.check_interval = args.check_interval * 60

    if args.once:
        # Run once and exit
        logger.info("🔄 Running auto-commit once")
        daemon.process_changes()
    else:
        # Run as daemon
        try:
            daemon.run_daemon()
        except KeyboardInterrupt:
            logger.info("👋 Daemon interrupted by user")


if __name__ == '__main__':
    main()
