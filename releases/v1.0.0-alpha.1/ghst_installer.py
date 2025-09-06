#!/usr/bin/env python3
"""
GHST Graphical Installation Wizard
==================================

Professional GUI installer for the GHST AI Coding Engine.
Handles dependency installation, environment setup, and system validation.

Version: 1.0.0-alpha.1
Release Date: September 6, 2025
"""

import sys
import subprocess
import time
from pathlib import Path
from typing import Dict

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QProgressBar, QTextEdit, QStackedWidget,
        QCheckBox, QComboBox, QGroupBox, QMessageBox, QFrame
    )
    from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
    PYQT5_AVAILABLE = True
except ImportError:
    PYQT5_AVAILABLE = False

class InstallationWorker(QThread):
    """Background worker for installation tasks."""

    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    log_updated = pyqtSignal(str)
    installation_completed = pyqtSignal(bool)

    def __init__(self, install_options: Dict):
        super().__init__()
        self.install_options = install_options
        self.cancelled = False

    def run(self):
        """Execute the installation process."""
        try:
            self.install_dependencies()
            self.setup_environment()
            self.validate_installation()
            self.installation_completed.emit(True)
        except Exception as e:
            self.log_updated.emit("❌ Installation failed: {str(e)}")
            self.installation_completed.emit(False)

    def install_dependencies(self):
        """Install required Python packages."""
        self.status_updated.emit("Installing Python dependencies...")
        self.progress_updated.emit(10)

        packages = [
            'PyQt5', 'pyyaml', 'requests', 'pillow',
            'keyboard', 'pyautogui'
        ]

        for i, package in enumerate(packages):
            if self.cancelled:
                return

            self.log_updated.emit("📦 Installing {package}...")

            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', package
                ], capture_output=True, text=True)

                self.log_updated.emit("✅ {package} installed successfully")

            except subprocess.CalledProcessError as e:
                self.log_updated.emit("⚠️ {package} installation failed: {e}")

            progress = 10 + (i + 1) * 15
            self.progress_updated.emit(progress)
            time.sleep(0.5)

    def setup_environment(self):
        """Set up GHST environment and configuration."""
        self.status_updated.emit("Setting up GHST environment...")
        self.progress_updated.emit(60)

        # Create necessary directories
        ghst_dirs = [
            'ghosts', 'training_scripts', 'local_pool',
            'vendor', 'logs', 'exports'
        ]

        for directory in ghst_dirs:
            if self.cancelled:
                return

            dir_path = Path.cwd() / directory
            dir_path.mkdir(exist_ok=True)
            self.log_updated.emit("📁 Created directory: {directory}")

        self.progress_updated.emit(75)

        # Initialize configuration files
        self.log_updated.emit("⚙️ Initializing configuration...")
        self.create_default_config()

        self.progress_updated.emit(85)

    def create_default_config(self):
        """Create default configuration files."""
        config_content = """  # GHST Configuration
# ===================

app:
  name: "GHST - AI Coding Engine"
  version: "1.0.0-alpha.1"
  theme: "ghost_dark"

syntax_supervisors:
  enabled: true
  scan_interval: 30
  notification_level: "medium"

expert_collective:
  max_agents: 8
  response_timeout: 30

gui:
  window_size: [1400, 900]
  auto_save: true
  dark_theme: true
"""

        config_path = Path.cwd() / 'core' / 'config' / 'installer_default.yaml'
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, 'w') as f:
            f.write(config_content)

        self.log_updated.emit("✅ Default configuration created")

    def validate_installation(self):
        """Validate that GHST components work correctly."""
        self.status_updated.emit("Validating installation...")
        self.progress_updated.emit(90)

        # Test core imports
        validation_tests = [
            ("Syntax Supervisors", "core.src.syntax_supervisors"),
            ("Expert Manager", "core.src.ai_collaboration.expert_manager"),
            ("Config Manager", "core.src.utils.config_manager"),
            ("GUI Components", "core.src.ui_components.main")
        ]

        for test_name, module_path in validation_tests:
            if self.cancelled:
                return

            try:
                __import__(module_path)
                self.log_updated.emit("✅ {test_name}: Working")
            except ImportError as e:
                self.log_updated.emit("⚠️ {test_name}: {str(e)}")

        self.progress_updated.emit(100)
        self.status_updated.emit("Installation complete!")

    def cancel(self):
        """Cancel the installation process."""
        self.cancelled = True

class WelcomePage(QWidget):
    """Welcome page of the installer."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("Welcome to GHST Installation")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #0078d4;")
        layout.addWidget(title)

        # Logo placeholder
        logo_frame = QFrame()
        logo_frame.setFixedHeight(120)
        logo_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 2px solid #0078d4;
                border-radius: 8px;
                margin: 20px;
            }
        """)
        layout.addWidget(logo_frame)

        # Description
        description = QLabel("""
        <h3>🚀 GHST - AI Coding Engine</h3>
        <p>Professional AI-powered coding assistant with expert agent collective.</p>

        <h4>✨ Features:</h4>
        <ul>
            <li>🧠 AI Expert Collective for coding assistance</li>
            <li>🔍 Background Syntax Supervisors monitoring</li>
            <li>🎨 Professional themed interface</li>
            <li>🔌 Extensible plugin system</li>
            <li>⚙️ Human-centered design principles</li>
        </ul>

        <p><strong>Version:</strong> 1.0.0-alpha.1<br>
        <strong>Release Date:</strong> September 6, 2025</p>
        """)
        description.setWordWrap(True)
        layout.addWidget(description)

        layout.addStretch()

class OptionsPage(QWidget):
    """Installation options page."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("Installation Options")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Installation type
        install_group = QGroupBox("Installation Type")
        install_layout = QVBoxLayout()
        install_group.setLayout(install_layout)

        self.full_install = QCheckBox("Full Installation (Recommended)")
        self.full_install.setChecked(True)
        self.full_install.setToolTip("Install all components and dependencies")
        install_layout.addWidget(self.full_install)

        self.minimal_install = QCheckBox("Minimal Installation")
        self.minimal_install.setToolTip("Core components only")
        install_layout.addWidget(self.minimal_install)

        self.developer_install = QCheckBox("Developer Mode")
        self.developer_install.setToolTip(
            "Include development tools and debug features")
        install_layout.addWidget(self.developer_install)

        layout.addWidget(install_group)

        # Components
        components_group = QGroupBox("Components")
        components_layout = QVBoxLayout()
        components_group.setLayout(components_layout)

        self.syntax_supervisors = QCheckBox("Syntax Supervisors")
        self.syntax_supervisors.setChecked(True)
        components_layout.addWidget(self.syntax_supervisors)

        self.expert_collective = QCheckBox("AI Expert Collective")
        self.expert_collective.setChecked(True)
        components_layout.addWidget(self.expert_collective)

        self.plugin_system = QCheckBox("Plugin System")
        self.plugin_system.setChecked(True)
        components_layout.addWidget(self.plugin_system)

        self.automation_tools = QCheckBox("Automation Tools")
        self.automation_tools.setChecked(True)
        components_layout.addWidget(self.automation_tools)

        layout.addWidget(components_group)

        # Configuration
        config_group = QGroupBox("Configuration")
        config_layout = QVBoxLayout()
        config_group.setLayout(config_layout)

        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(
            ["Ghost Dark", "Ghost Light", "Professional"])
        theme_layout.addWidget(self.theme_combo)
        config_layout.addLayout(theme_layout)

        layout.addWidget(config_group)

        layout.addStretch()

    def get_install_options(self) -> Dict:
        """Get the selected installation options."""
        return {
            'full_install': self.full_install.isChecked(),
            'minimal_install': self.minimal_install.isChecked(),
            'developer_mode': self.developer_install.isChecked(),
            'syntax_supervisors': self.syntax_supervisors.isChecked(),
            'expert_collective': self.expert_collective.isChecked(),
            'plugin_system': self.plugin_system.isChecked(),
            'automation_tools': self.automation_tools.isChecked(),
            'theme': self.theme_combo.currentText()
        }

class InstallationPage(QWidget):
    """Installation progress page."""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker = None

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("Installing GHST...")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Preparing installation...")
        layout.addWidget(self.status_label)

        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(200)
        layout.addWidget(self.log_output)

        # Control buttons
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        layout.addStretch()

    def start_installation(self, options: Dict):
        """Start the installation process."""
        self.worker = InstallationWorker(options)

        # Connect signals
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.status_updated.connect(self.update_status)
        self.worker.log_updated.connect(self.update_log)
        self.worker.installation_completed.connect(self.installation_finished)

        self.cancel_button.clicked.connect(self.worker.cancel)

        # Start installation
        self.worker.start()

    def update_progress(self, value: int):
        """Update progress bar."""
        self.progress_bar.setValue(value)

    def update_status(self, status: str):
        """Update status label."""
        self.status_label.setText(status)

    def update_log(self, message: str):
        """Update log output."""
        self.log_output.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def installation_finished(self, success: bool):
        """Handle installation completion."""
        if success:
            self.status_label.setText("✅ Installation completed successfully!")
            self.cancel_button.setText("Finish")
        else:
            self.status_label.setText("❌ Installation failed")
            self.cancel_button.setText("Close")

class CompletionPage(QWidget):
    """Installation completion page."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Success message
        title = QLabel("🎉 GHST Installation Complete!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #00a86b;")
        layout.addWidget(title)

        # Completion info
        info = QLabel("""
        <h3>✅ Installation Successful</h3>
        <p>GHST AI Coding Engine has been installed and is ready to use.</p>

        <h4>🚀 What's Next:</h4>
        <ul>
            <li>Launch GHST from the desktop shortcut</li>
            <li>Explore the AI Expert Collective</li>
            <li>Try the Syntax Supervisors</li>
            <li>Configure plugins and themes</li>
        </ul>

        <h4>📚 Resources:</h4>
        <ul>
            <li>Documentation: README.md</li>
            <li>Configuration: core/config/</li>
            <li>Plugins: core/src/plugins/</li>
        </ul>
        """)
        info.setWordWrap(True)
        layout.addWidget(info)

        # Action buttons
        button_layout = QHBoxLayout()

        self.launch_button = QPushButton("🚀 Launch GHST")
        self.launch_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        button_layout.addWidget(self.launch_button)

        self.close_button = QPushButton("Close Installer")
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)
        layout.addStretch()

class GHSTInstaller(QMainWindow):
    """Main installer window."""

    def __init__(self):
        super().__init__()
        self.current_page = 0
        self.init_ui()

    def init_ui(self):
        """Initialize the installer UI."""
        self.setWindowTitle("GHST Installer - v1.0.0-alpha.1")
        self.setGeometry(200, 200, 800, 600)
        self.setMinimumSize(700, 500)

        # Apply installer theme
        self.apply_installer_theme()

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Header
        header = QLabel("GHST AI Coding Engine Installer")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                background-color: #0078d4;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
        """)
        main_layout.addWidget(header)

        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Add pages
        self.welcome_page = WelcomePage()
        self.options_page = OptionsPage()
        self.installation_page = InstallationPage()
        self.completion_page = CompletionPage()

        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.options_page)
        self.stacked_widget.addWidget(self.installation_page)
        self.stacked_widget.addWidget(self.completion_page)

        # Navigation buttons
        nav_layout = QHBoxLayout()

        self.back_button = QPushButton("← Back")
        self.back_button.setEnabled(False)
        self.back_button.clicked.connect(self.go_back)
        nav_layout.addWidget(self.back_button)

        nav_layout.addStretch()

        self.next_button = QPushButton("Next →")
        self.next_button.clicked.connect(self.go_next)
        nav_layout.addWidget(self.next_button)

        main_layout.addLayout(nav_layout)

        # Connect completion page signals
        self.completion_page.launch_button.clicked.connect(self.launch_ghst)
        self.completion_page.close_button.clicked.connect(self.close)

    def apply_installer_theme(self):
        """Apply professional installer theme."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QWidget {
                background-color: #ffffff;
                color: #333333;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                background-color: #e1e1e1;
                border: 1px solid #cccccc;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                color: #999999;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QCheckBox {
                spacing: 8px;
            }
            QProgressBar {
                border: 2px solid #cccccc;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 3px;
            }
        """)

    def go_next(self):
        """Navigate to next page."""
        if self.current_page == 0:  # Welcome -> Options
            self.current_page = 1
            self.stacked_widget.setCurrentIndex(1)
            self.back_button.setEnabled(True)
            self.next_button.setText("Install")

        elif self.current_page == 1:  # Options -> Installation
            self.current_page = 2
            self.stacked_widget.setCurrentIndex(2)
            self.next_button.setEnabled(False)
            self.back_button.setEnabled(False)

            # Start installation
            options = self.options_page.get_install_options()
            self.installation_page.start_installation(options)

            # Connect installation completion
            self.installation_page.worker.installation_completed.connect(
                self.installation_finished
            )

        elif self.current_page == 2:  # Installation -> Completion
            self.current_page = 3
            self.stacked_widget.setCurrentIndex(3)
            self.next_button.setVisible(False)
            self.back_button.setVisible(False)

    def go_back(self):
        """Navigate to previous page."""
        if self.current_page == 1:  # Options -> Welcome
            self.current_page = 0
            self.stacked_widget.setCurrentIndex(0)
            self.back_button.setEnabled(False)
            self.next_button.setText("Next →")

    def installation_finished(self, success: bool):
        """Handle installation completion."""
        if success:
            # Auto-advance after 2 seconds
            QTimer.singleShot(2000, self.go_next)

    def launch_ghst(self):
        """Launch GHST application."""
        try:
            ghst_path = Path.cwd() / "core" / "launcher.py"
            subprocess.Popen([sys.executable, str(ghst_path)])
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Launch Error",
                                 "Failed to launch GHST: {str(e)}")

def main():
    """Main entry point for the installer."""
    if not PYQT5_AVAILABLE:
        print("❌ PyQt5 not found. Installing...")
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', 'PyQt5'])
            print("✅ PyQt5 installed. Please restart the installer.")
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyQt5. Please install manually:")
            print("   pip install PyQt5")
        return 1

    app = QApplication(sys.argv)
    app.setApplicationName("GHST Installer")
    app.setApplicationVersion("1.0.0-alpha.1")

    installer = GHSTInstaller()
    installer.show()

    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
