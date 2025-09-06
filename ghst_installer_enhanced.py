#!/usr/bin/env python3
"""
GHST Enhanced Installation Wizard
=================================

Professional GUI installer for the GHST AI Coding Engine with:
- Cache cleanup for clean installations
- Version checking and update detection
- Preference preservation during upgrades

Version: 1.0.0-alpha.4
Release Date: September 6, 2025
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

import requests

try:
    from PyQt5.QtCore import Qt, QThread, pyqtSignal
    from PyQt5.QtWidgets import (
        QApplication,
        QCheckBox,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QMainWindow,
        QMessageBox,
        QProgressBar,
        QPushButton,
        QTabWidget,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )
    PYQT5_AVAILABLE = True
except ImportError:
    PYQT5_AVAILABLE = False

# Version and update information
CURRENT_VERSION = "1.0.0-alpha.3"
GITHUB_REPO = "allanwrench28/GHST"
UPDATE_CHECK_URL = "https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

class CacheManager:
    """Manages cache cleanup and preference preservation."""

    def __init__(self, install_path: Path):
        self.install_path = install_path
        self.cache_dirs = [
            "__pycache__", ".pyc_cache", "temp", "tmp",
            ".ghst_cache", "build", "dist", ".pytest_cache"
        ]
        self.preserve_files = [
            "config/user_preferences.yaml",
            "config/api_keys.json",
            "config/custom_settings.yaml",
            "logs/installation.log"
        ]

    def backup_preferences(self) -> Optional[Dict]:
        """Backup user preferences before cleanup."""
        preferences = {}
        backup_path = self.install_path / ".ghst_backup"
        backup_path.mkdir(exist_ok=True)

        for pref_file in self.preserve_files:
            source = self.install_path / pref_file
            if source.exists():
                backup_dest = backup_path / pref_file
                backup_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, backup_dest)
                preferences[pref_file] = str(backup_dest)

        return preferences if preferences else None

    def restore_preferences(self, preferences: Dict):
        """Restore user preferences after installation."""
        self.install_path / ".ghst_backup"

        for pref_file, backup_location in preferences.items():
            backup_source = Path(backup_location)
            restore_dest = self.install_path / pref_file

            if backup_source.exists():
                restore_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup_source, restore_dest)

    def cleanup_caches(self) -> List[str]:
        """Remove all cache directories and files."""
        cleaned = []

        # Remove cache directories
        for root, dirs, files in os.walk(self.install_path):
            for cache_dir in self.cache_dirs:
                if cache_dir in dirs:
                    cache_path = Path(root) / cache_dir
                    try:
                        shutil.rmtree(cache_path)
                        cleaned.append(
                            "Removed cache: {
                                cache_path.relative_to(
                                    self.install_path)}")
                    except Exception as e:
                        cleaned.append(
                            "Warning: Could not remove {cache_path}: {e}")

        # Remove .pyc files
        for root, dirs, files in os.walk(self.install_path):
            for file in files:
                if file.endswith('.pyc') or file.endswith('.pyo'):
                    pyc_path = Path(root) / file
                    try:
                        pyc_path.unlink()
                        cleaned.append(
                            "Removed: {
                                pyc_path.relative_to(
                                    self.install_path)}")
                    except Exception as e:
                        cleaned.append(
                            "Warning: Could not remove {pyc_path}: {e}")

        # Clean backup directory after successful restore
        backup_path = self.install_path / ".ghst_backup"
        if backup_path.exists():
            try:
                shutil.rmtree(backup_path)
                cleaned.append("Cleaned temporary backup directory")
            except Exception:
                pass

        return cleaned

class UpdateChecker:
    """Checks for GHST updates from GitHub releases."""

    @staticmethod
    def check_for_updates() -> Dict:
        """Check GitHub for newer releases."""
        try:
            response = requests.get(UPDATE_CHECK_URL, timeout=10)
            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data.get('tag_name', '').lstrip('v')

                return {
                    'available': latest_version != CURRENT_VERSION,
                    'latest_version': latest_version,
                    'current_version': CURRENT_VERSION,
                    'download_url': release_data.get(
                        'html_url',
                        ''),
                    'release_notes': release_data.get(
                        'body',
                        'No release notes available'),
                    'assets': [
                        asset['browser_download_url'] for asset in release_data.get(
                            'assets',
                            [])]}
        except Exception as e:
            return {
                'available': False,
                'error': str(e),
                'current_version': CURRENT_VERSION
            }

        return {'available': False, 'current_version': CURRENT_VERSION}

class InstallationWorker(QThread):
    """Enhanced background worker for installation tasks."""

    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    log_updated = pyqtSignal(str)
    installation_completed = pyqtSignal(bool)

    def __init__(self, install_options: Dict):
        super().__init__()
        self.install_options = install_options
        self.cancelled = False
        self.cache_manager = None

    def run(self):
        """Execute the enhanced installation process."""
        try:
            self.status_updated.emit("Preparing installation...")
            self.progress_updated.emit(5)

            # Check for existing installation
            install_path = Path.cwd()
            self.cache_manager = CacheManager(install_path)

            # Backup preferences if this is an upgrade
            preferences_backup = None
            if self.install_options.get('clean_install', True):
                self.status_updated.emit("Backing up user preferences...")
                preferences_backup = self.cache_manager.backup_preferences()
                if preferences_backup:
                    self.log_updated.emit(
                        "✅ Backed up {
                            len(preferences_backup)} preference files")

                # Clean caches and temporary files
                self.status_updated.emit(
                    "Cleaning caches and temporary files...")
                cleaned_items = self.cache_manager.cleanup_caches()
                for item in cleaned_items[:10]:  # Show first 10 items
                    self.log_updated.emit("🧹 {item}")
                if len(cleaned_items) > 10:
                    self.log_updated.emit(
                        "🧹 ... and {
                            len(cleaned_items) -
                            10} more items")

            self.progress_updated.emit(15)

            # Install dependencies
            if not self.cancelled:
                self.install_dependencies()

            # Setup environment
            if not self.cancelled:
                self.setup_environment()

            # Restore preferences
            if preferences_backup and not self.cancelled:
                self.status_updated.emit("Restoring user preferences...")
                self.cache_manager.restore_preferences(preferences_backup)
                self.log_updated.emit("✅ User preferences restored")

            # Final cleanup
            if not self.cancelled:
                self.status_updated.emit("Finalizing installation...")
                self.progress_updated.emit(95)
                time.sleep(1)

                self.log_updated.emit("🎉 Installation completed successfully!")
                self.installation_completed.emit(True)

        except Exception as e:
            self.log_updated.emit("❌ Installation failed: {str(e)}")
            self.installation_completed.emit(False)

    def install_dependencies(self):
        """Install required Python packages with enhanced error handling."""
        packages = [
            'PyQt5', 'pyyaml', 'requests', 'pillow',
            'numpy', 'pandas', 'matplotlib'
        ]

        for i, package in enumerate(packages):
            if self.cancelled:
                return

            self.log_updated.emit("📦 Installing {package}...")

            try:
                # Use DEVNULL for older Python compatibility
                with open(os.devnull, 'w') as devnull:
                    subprocess.check_call([
                        sys.executable, '-m', 'pip', 'install', package, '--upgrade'
                    ], stdout=devnull, stderr=subprocess.STDOUT)

                self.log_updated.emit("✅ {package} installed successfully")

            except subprocess.CalledProcessError as e:
                self.log_updated.emit("⚠️ {package} installation failed: {e}")
            except Exception as e:
                self.log_updated.emit("❌ Installation error: {str(e)}")

            progress = 15 + (i + 1) * 15
            self.progress_updated.emit(progress)
            time.sleep(0.5)

    def setup_environment(self):
        """Set up GHST environment and configuration."""
        self.status_updated.emit("Setting up GHST environment...")
        self.progress_updated.emit(70)

        # Create necessary directories
        ghst_dirs = [
            'ghosts', 'training_scripts', 'local_pool',
            'vendor', 'logs', 'exports', 'config', 'temp'
        ]

        for directory in ghst_dirs:
            if self.cancelled:
                return

            dir_path = Path.cwd() / directory
            dir_path.mkdir(exist_ok=True)
            self.log_updated.emit("📁 Created directory: {directory}")

        self.progress_updated.emit(85)

        # Initialize configuration files
        self.log_updated.emit("⚙️ Initializing configuration...")
        self.create_default_config()

        self.progress_updated.emit(90)

    def create_default_config(self):
        """Create default configuration files."""
        config_content = """  # GHST Configuration
# ===================

version: "{}"
install_date: "{}"

# AI Settings
ai:
  expert_mode: true
  safety_checks: true
  human_oversight: true

# GUI Settings
gui:
  theme: "dark"
  startup_checks: true
  auto_save: true

# Plugin Settings
plugins:
  auto_load: true
  builtin_enabled: true

# Update Settings
updates:
  check_on_startup: true
  auto_download: false
""".format(CURRENT_VERSION, time.strftime("%Y-%m-%d %H:%M:%S"))

        config_path = Path.cwd() / 'config' / 'default.yaml'
        with open(config_path, 'w') as f:
            f.write(config_content)

    def cancel(self):
        """Cancel the installation process."""
        self.cancelled = True

class UpdateTab(QWidget):
    """Tab for checking and managing updates."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Header
        header = QLabel("🔄 GHST Update Manager")
        header.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #0078d4; margin: 10px;")
        layout.addWidget(header)

        # Current version info
        version_group = QGroupBox("Current Installation")
        version_layout = QVBoxLayout()

        self.current_version_label = QLabel("Version: {CURRENT_VERSION}")
        self.current_version_label.setStyleSheet("font-weight: bold;")
        version_layout.addWidget(self.current_version_label)

        version_group.setLayout(version_layout)
        layout.addWidget(version_group)

        # Update check section
        update_group = QGroupBox("Check for Updates")
        update_layout = QVBoxLayout()

        self.check_button = QPushButton("🔍 Check for Updates")
        self.check_button.clicked.connect(self.check_for_updates)
        update_layout.addWidget(self.check_button)

        self.update_status = QLabel(
            "Click 'Check for Updates' to see if newer versions are available.")
        self.update_status.setWordWrap(True)
        update_layout.addWidget(self.update_status)

        self.update_details = QTextEdit()
        self.update_details.setMaximumHeight(150)
        self.update_details.setVisible(False)
        update_layout.addWidget(self.update_details)

        self.download_button = QPushButton("📥 Download Latest Release")
        self.download_button.setVisible(False)
        self.download_button.clicked.connect(self.open_download_page)
        update_layout.addWidget(self.download_button)

        update_group.setLayout(update_layout)
        layout.addWidget(update_group)

        layout.addStretch()
        self.setLayout(layout)

    def check_for_updates(self):
        """Check for available updates."""
        self.check_button.setText("🔄 Checking...")
        self.check_button.setEnabled(False)

        # Run update check in background
        self.update_thread = QThread()
        self.update_thread.run = self.perform_update_check
        self.update_thread.finished.connect(self.update_check_finished)
        self.update_thread.start()

    def perform_update_check(self):
        """Perform the actual update check."""
        self.update_info = UpdateChecker.check_for_updates()

    def update_check_finished(self):
        """Handle update check completion."""
        self.check_button.setText("🔍 Check for Updates")
        self.check_button.setEnabled(True)

        if 'error' in self.update_info:
            self.update_status.setText(
                "❌ Update check failed: {
                    self.update_info['error']}")
            return

        if self.update_info['available']:
            latest = self.update_info['latest_version']
            self.update_status.setText("🎉 New version available: v{latest}")
            self.update_status.setStyleSheet(
                "color: #28a745; font-weight: bold;")

            # Show release notes
            self.update_details.setPlainText(
                self.update_info.get(
                    'release_notes',
                    'No release notes available'))
            self.update_details.setVisible(True)

            # Show download button
            self.download_button.setVisible(True)

        else:
            self.update_status.setText("✅ You have the latest version!")
            self.update_status.setStyleSheet("color: #28a745;")
            self.update_details.setVisible(False)
            self.download_button.setVisible(False)

    def open_download_page(self):
        """Open the GitHub releases page."""
        import webbrowser
        download_url = self.update_info.get(
            'download_url', f'https://github.com/{GITHUB_REPO}/releases')
        webbrowser.open(download_url)

class WelcomePage(QWidget):
    """Enhanced welcome page with update check."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Header
        title = QLabel("🧠 GHST AI Coding Engine Installer")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #0078d4; margin: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Version info
        version_label = QLabel("Version {CURRENT_VERSION}")
        version_label.setStyleSheet(
            "font-size: 14px; color: #666; margin-bottom: 20px;")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)

        # Welcome text
        welcome_text = QLabel("""
        Welcome to the GHST AI Coding Engine installation wizard!

        This installer will:
        • Clean any existing caches and temporary files
        • Preserve your user preferences and settings
        • Install the latest dependencies
        • Set up the complete GHST environment
        • Check for updates automatically

        🔄 Enhanced Installation Features:
        ✅ Cache cleanup for clean installations
        ✅ Preference preservation during upgrades
        ✅ Update checking and version management
        ✅ Professional error handling and logging
        """)
        welcome_text.setWordWrap(True)
        welcome_text.setStyleSheet(
            "font-size: 12px; line-height: 1.4; margin: 20px;")
        layout.addWidget(welcome_text)

        layout.addStretch()
        self.setLayout(layout)

class OptionsPage(QWidget):
    """Enhanced options page with cache cleanup options."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Header
        title = QLabel("⚙️ Installation Options")
        title.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #0078d4; margin: 10px;")
        layout.addWidget(title)

        # Installation type
        install_group = QGroupBox("Installation Type")
        install_layout = QVBoxLayout()

        self.clean_install = QCheckBox(
            "🧹 Perform clean installation (recommended)")
        self.clean_install.setChecked(True)
        self.clean_install.setToolTip(
            "Remove caches and temporary files, but preserve user preferences")
        install_layout.addWidget(self.clean_install)

        self.preserve_logs = QCheckBox("📋 Preserve installation logs")
        self.preserve_logs.setChecked(True)
        install_layout.addWidget(self.preserve_logs)

        self.auto_updates = QCheckBox("🔄 Enable automatic update checking")
        self.auto_updates.setChecked(True)
        install_layout.addWidget(self.auto_updates)

        install_group.setLayout(install_layout)
        layout.addWidget(install_group)

        # Advanced options
        advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QVBoxLayout()

        self.dev_mode = QCheckBox("🔧 Install development dependencies")
        self.dev_mode.setToolTip(
            "Install additional packages for GHST development")
        advanced_layout.addWidget(self.dev_mode)

        self.create_shortcuts = QCheckBox("🔗 Create desktop shortcuts")
        self.create_shortcuts.setChecked(True)
        advanced_layout.addWidget(self.create_shortcuts)

        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)

        layout.addStretch()
        self.setLayout(layout)

    def get_options(self) -> Dict:
        """Get selected installation options."""
        return {
            'clean_install': self.clean_install.isChecked(),
            'preserve_logs': self.preserve_logs.isChecked(),
            'auto_updates': self.auto_updates.isChecked(),
            'dev_mode': self.dev_mode.isChecked(),
            'create_shortcuts': self.create_shortcuts.isChecked()
        }

class InstallationPage(QWidget):
    """Installation page with enhanced progress tracking."""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker = None

    def init_ui(self):
        layout = QVBoxLayout()

        # Header
        title = QLabel("📦 Installing GHST")
        title.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #0078d4; margin: 10px;")
        layout.addWidget(title)

        # Progress section
        self.status_label = QLabel("Preparing installation...")
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        # Log section
        log_label = QLabel("Installation Log:")
        log_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(300)
        self.log_text.setStyleSheet(
            "background-color: #1e1e1e; color: #ffffff; font-family: 'Consolas', monospace;")
        layout.addWidget(self.log_text)

        # Control buttons
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("❌ Cancel")
        self.cancel_button.clicked.connect(self.cancel_installation)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def start_installation(self, options: Dict):
        """Start the installation process with given options."""
        self.worker = InstallationWorker(options)
        self.worker.progress_updated.connect(self.progress_bar.setValue)
        self.worker.status_updated.connect(self.status_label.setText)
        self.worker.log_updated.connect(self.append_log)
        self.worker.installation_completed.connect(self.installation_finished)
        self.worker.start()

    def append_log(self, message: str):
        """Append message to installation log."""
        self.log_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def cancel_installation(self):
        """Cancel the installation process."""
        if self.worker:
            self.worker.cancel()
            self.status_label.setText("Cancelling installation...")

    def installation_finished(self, success: bool):
        """Handle installation completion."""
        self.cancel_button.setText("Close")
        if success:
            self.status_label.setText("✅ Installation completed successfully!")
        else:
            self.status_label.setText("❌ Installation failed!")

class CompletionPage(QWidget):
    """Enhanced completion page with next steps."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Success header
        title = QLabel("🎉 GHST Installation Complete!")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #28a745; margin: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Next steps
        next_steps = QLabel("""
        ✅ GHST AI Coding Engine has been successfully installed!

        🚀 Next Steps:

        1. 🎮 Launch GHST: Run 'python launcher.py' to start the AI coding engine

        2. 🔧 Configure: Customize settings in the config/ directory

        3. 🔌 Explore Plugins: Check out the built-in tools and extensions

        4. 📚 Documentation: Visit the GitHub repository for guides and tutorials

        5. 🔄 Updates: Use the installer's Update tab to check for new versions

        🤝 Thank you for choosing GHST!
        Your AI-powered coding companion is ready to assist you.
        """)
        next_steps.setWordWrap(True)
        next_steps.setStyleSheet(
            "font-size: 12px; line-height: 1.5; margin: 20px;")
        layout.addWidget(next_steps)

        # Action buttons
        button_layout = QHBoxLayout()

        self.launch_button = QPushButton("🚀 Launch GHST Now")
        self.launch_button.setStyleSheet(
            "background-color: #0078d4; color: white; font-weight: bold; padding: 10px;")
        self.launch_button.clicked.connect(self.launch_ghst)
        button_layout.addWidget(self.launch_button)

        self.open_folder_button = QPushButton("📁 Open Installation Folder")
        self.open_folder_button.clicked.connect(self.open_install_folder)
        button_layout.addWidget(self.open_folder_button)

        layout.addLayout(button_layout)
        layout.addStretch()
        self.setLayout(layout)

    def launch_ghst(self):
        """Launch GHST after installation."""
        try:
            subprocess.Popen([sys.executable, 'launcher.py'],
                             cwd=Path.cwd())
            QApplication.quit()
        except Exception as e:
            QMessageBox.warning(self, "Launch Error",
                                "Could not launch GHST: {str(e)}")

    def open_install_folder(self):
        """Open the installation folder."""
        try:
            os.startfile(str(Path.cwd()))
        except Exception:
            # Fallback for non-Windows systems
            subprocess.run(['explorer', str(Path.cwd())], shell=True)

class GHSTInstaller(QMainWindow):
    """Enhanced GHST Installation Wizard with tabbed interface."""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_page = 0
        self.installation_options = {}

    def init_ui(self):
        self.setWindowTitle(
            "GHST AI Coding Engine - Enhanced Installer v1.0.0-alpha.4")
        self.setGeometry(200, 200, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #0078d4;
            }
        """)

        # Create central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # Create tab widget
        self.tab_widget = QTabWidget()

        # Installation wizard pages
        self.welcome_page = WelcomePage()
        self.options_page = OptionsPage()
        self.installation_page = InstallationPage()
        self.completion_page = CompletionPage()

        # Update management tab
        self.update_tab = UpdateTab()

        # Add tabs
        self.tab_widget.addTab(self.welcome_page, "🏠 Welcome")
        self.tab_widget.addTab(self.options_page, "⚙️ Options")
        self.tab_widget.addTab(self.installation_page, "📦 Install")
        self.tab_widget.addTab(self.completion_page, "✅ Complete")
        self.tab_widget.addTab(self.update_tab, "🔄 Updates")

        main_layout.addWidget(self.tab_widget)

        # Navigation buttons
        nav_layout = QHBoxLayout()

        self.back_button = QPushButton("⬅️ Back")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)
        nav_layout.addWidget(self.back_button)

        nav_layout.addStretch()

        self.next_button = QPushButton("Next ➡️")
        self.next_button.clicked.connect(self.go_next)
        nav_layout.addWidget(self.next_button)

        main_layout.addLayout(nav_layout)
        central_widget.setLayout(main_layout)

        # Connect tab changes
        self.tab_widget.currentChanged.connect(self.tab_changed)

    def tab_changed(self, index):
        """Handle tab changes."""
        self.current_page = index
        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        """Update navigation button states."""
        # Don't show navigation for update tab
        if self.current_page == 4:  # Update tab
            self.back_button.setVisible(False)
            self.next_button.setVisible(False)
            return

        self.back_button.setVisible(True)
        self.next_button.setVisible(True)

        self.back_button.setEnabled(self.current_page > 0)

        if self.current_page == 3:  # Completion page
            self.next_button.setText("Finish")
        else:
            self.next_button.setText("Next ➡️")

    def go_back(self):
        """Go to previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.tab_widget.setCurrentIndex(self.current_page)

    def go_next(self):
        """Go to next page or start installation."""
        if self.current_page == 1:  # Options page
            # Get installation options
            self.installation_options = self.options_page.get_options()
            self.current_page += 1
            self.tab_widget.setCurrentIndex(self.current_page)
            # Start installation
            self.installation_page.start_installation(
                self.installation_options)

        elif self.current_page == 3:  # Completion page
            self.close()

        else:
            self.current_page += 1
            self.tab_widget.setCurrentIndex(self.current_page)

def main():
    """Main application entry point."""
    if not PYQT5_AVAILABLE:
        print("❌ PyQt5 is required for the graphical installer")
        print("📦 Installing PyQt5...")
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', 'PyQt5'])
            print("✅ PyQt5 installed. Please restart the installer.")
        except Exception as e:
            print("❌ Failed to install PyQt5: {e}")
            print("🔧 Please install PyQt5 manually: pip install PyQt5")
        return

    app = QApplication(sys.argv)
    app.setApplicationName("GHST Enhanced Installer")

    installer = GHSTInstaller()
    installer.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
