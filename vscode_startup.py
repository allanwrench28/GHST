#!/usr/bin/env python3
"""
GHST Auto-Startup Script
========================

Automatically starts the auto-commit daemon when VS Code opens the repository.
This script checks if the daemon is already running and starts it if needed.
"""

import os
import sys
import time
import subprocess
import psutil
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - STARTUP - %(message)s',
    handlers=[
        logging.FileHandler('auto_commit_startup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def is_daemon_running():
    """Check if auto-commit daemon is already running"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                cmdline = proc.info['cmdline']
                if cmdline and any('auto_commit_daemon.py' in arg for arg in cmdline):
                    return True, proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False, None

def start_daemon_background():
    """Start the auto-commit daemon in background"""
    try:
        # Start daemon in background
        process = subprocess.Popen(
            [sys.executable, 'auto_commit_daemon.py'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=Path.cwd()
        )
        
        # Give it a moment to start
        time.sleep(2)
        
        # Check if it started successfully
        if process.poll() is None:
            logger.info(f"✅ Auto-commit daemon started successfully (PID: {process.pid})")
            return True
        else:
            logger.error("❌ Auto-commit daemon failed to start")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to start daemon: {e}")
        return False

def load_config():
    """Load auto-commit configuration"""
    config_file = 'auto_commit_config.json'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"⚠️ Could not load config: {e}")
    return {}

def main():
    """Main startup routine"""
    logger.info("🚀 GHST Repository opened in VS Code")
    
    # Load configuration
    config = load_config()
    
    # Check if auto-commit is enabled
    if not config.get('auto_start_on_vscode_open', True):
        logger.info("⏸️ Auto-start disabled in configuration")
        return
    
    # Check if daemon is already running
    is_running, pid = is_daemon_running()
    
    if is_running:
        logger.info(f"✅ Auto-commit daemon already running (PID: {pid})")
        return
    
    logger.info("🤖 Starting auto-commit daemon...")
    
    # Start the daemon
    if start_daemon_background():
        logger.info("🎯 GHST auto-commit system is now active!")
        logger.info("📝 Changes will be automatically committed and pushed")
        logger.info("📊 Check auto_commit_daemon.log for activity")
    else:
        logger.error("❌ Failed to start auto-commit daemon")
        logger.info("💡 You can start it manually: python auto_commit_daemon.py")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f"❌ Startup script error: {e}")
    except KeyboardInterrupt:
        logger.info("⚠️ Startup interrupted")
