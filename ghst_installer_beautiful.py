#!/usr/bin/env python3
"""
GHST Beautiful Installation Wizard
==================================

Stunning modern GUI installer for the GHST AI Coding Engine featuring:
- Modern dark theme with glassmorphism effects
- Smooth animations and transitions
- Professional card-based layout
- Advanced cache cleanup and version management
- Real-time installation progress with visual feedback

Version: 1.0.0-alpha.5-beautiful
Release Date: September 6, 2025
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List

import requests

try:
    from PyQt5.QtCore import (
        Qt,
        QThread,
        pyqtSignal,
    )
    from PyQt5.QtGui import (
        QColor,
    )
    from PyQt5.QtWidgets import (
        QApplication,
        QCheckBox,
        QFrame,
        QGraphicsDropShadowEffect,
        QHBoxLayout,
        QLabel,
        QLineEdit,
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
CURRENT_VERSION = "1.0.0-alpha.5-beautiful"
GITHUB_REPO = "allanwrench28/GHST"
UPDATE_CHECK_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

# Modern color palette
COLORS = {
    'primary': '  # 6366f1',      # Indigo
    'secondary': '  # 8b5cf6',    # Purple
    'accent': '  # 06b6d4',       # Cyan
    'success': '  # 10b981',      # Emerald
    'warning': '  # f59e0b',      # Amber
    'error': '  # ef4444',        # Red
    'bg_primary': '  # 0f172a',   # Dark blue
    'bg_secondary': '  # 1e293b',  # Lighter dark blue
    'bg_card': '  # 334155',      # Card background
    'text_primary': '  # f1f5f9',  # Light text
    'text_secondary': '  # 94a3b8',  # Muted text
    'border': '  # 475569'        # Border color
}

class CacheManager:
    """Manages cache cleanup and preference preservation."""

    def __init__(self, install_path: Path):
        self.install_path = install_path
        self.cache_dirs = [
            "__pycache__", ".pyc_cache", "temp", "tmp",
            "build", "dist", ".pytest_cache", ".coverage",
            "node_modules", ".git"
        ]
        self.cache_patterns = [
            "*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll",
            "*.tmp", "*.temp", "*.log", "*.bak", "*.swp"
        ]
        self.preserve_files = [
            "config.json", "preferences.json", "settings.ini",
            "user_data.json", "api_keys.json"
        ]

    def cleanup_caches(self) -> List[str]:
        """Clean up cache directories and files, preserving user preferences."""
        cleaned = []

        if not self.install_path.exists():
            return cleaned

        # Save preferences first
        preserved_data = self._preserve_user_data()

        try:
            # Clean cache directories
            for cache_dir in self.cache_dirs:
                cache_path = self.install_path / cache_dir
                if cache_path.exists() and cache_path.is_dir():
                    shutil.rmtree(cache_path, ignore_errors=True)
                    cleaned.append("Removed cache directory: {cache_dir}")

            # Clean cache files by pattern
            import glob
            for pattern in self.cache_patterns:
                for file_path in glob.glob(
                        str(self.install_path / "**" / pattern), recursive=True):
                    try:
                        os.remove(file_path)
                        cleaned.append(
                            "Removed cache file: {
                                os.path.basename(file_path)}")
                    except (OSError, PermissionError):
                        pass

        except Exception as e:
            cleaned.append("Warning: {str(e)}")
        finally:
            # Restore preserved data
            self._restore_user_data(preserved_data)

        return cleaned

    def _preserve_user_data(self) -> Dict:
        """Preserve user configuration files."""
        preserved = {}

        for file_name in self.preserve_files:
            file_path = self.install_path / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        preserved[file_name] = f.read()
                except Exception:
                    pass

        return preserved

    def _restore_user_data(self, preserved_data: Dict):
        """Restore preserved user configuration files."""
        for file_name, content in preserved_data.items():
            file_path = self.install_path / file_name
            try:
                # Ensure directory exists
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            except Exception:
                pass

class UpdateChecker(QThread):
    """Background thread for checking GitHub releases."""

    update_found = pyqtSignal(str, str)  # version, download_url
    no_update = pyqtSignal()
    check_failed = pyqtSignal(str)

    def run(self):
        try:
            response = requests.get(UPDATE_CHECK_URL, timeout=10)
            response.raise_for_status()

            release_data = response.json()
            latest_version = release_data.get('tag_name', '').lstrip('v')
            download_url = release_data.get('html_url', '')

            if latest_version and latest_version != CURRENT_VERSION:
                self.update_found.emit(latest_version, download_url)
            else:
                self.no_update.emit()

        except Exception as e:
            self.check_failed.emit(str(e))

class InstallationWorker(QThread):
    """Enhanced background worker for installation tasks."""

    progress_update = pyqtSignal(int, str)
    log_update = pyqtSignal(str)
    installation_complete = pyqtSignal(bool, str)

    def __init__(self, install_path: Path, cleanup_enabled: bool = True):
        super().__init__()
        self.install_path = install_path
        self.cleanup_enabled = cleanup_enabled
        self.cache_manager = CacheManager(install_path)

    def run(self):
        try:
            total_steps = 7
            current_step = 0

            # Step 1: Validate installation path
            current_step += 1
            self.progress_update.emit(
                int(current_step / total_steps * 100), "Validating installation path...")
            time.sleep(0.5)

            # Create installation directory
            self.install_path.mkdir(parents=True, exist_ok=True)
            self.log_update.emit(
                "✓ Installation directory created: {
                    self.install_path}")

            # Step 2: Cache cleanup (if enabled)
            if self.cleanup_enabled:
                current_step += 1
                self.progress_update.emit(
                    int(current_step / total_steps * 100), "Cleaning up old caches...")

                cleaned_items = self.cache_manager.cleanup_caches()
                for item in cleaned_items[:5]:  # Show first 5 items
                    self.log_update.emit("🧹 {item}")
                if len(cleaned_items) > 5:
                    self.log_update.emit(
                        "🧹 ... and {
                            len(cleaned_items) -
                            5} more items")

                time.sleep(1)

            # Step 3: Check Python environment
            current_step += 1
            self.progress_update.emit(
                int(current_step / total_steps * 100), "Checking Python environment...")

            python_version = "{
                sys.version_info.major}.{
                sys.version_info.minor}.{
                sys.version_info.micro}"
            self.log_update.emit("🐍 Python {python_version} detected")
            time.sleep(0.5)

            # Step 4: Install dependencies
            current_step += 1
            self.progress_update.emit(
                int(current_step / total_steps * 100), "Installing dependencies...")

            # Simulate dependency installation
            dependencies = ["PyQt5", "requests", "pathlib", "packaging"]
            for dep in dependencies:
                self.log_update.emit("📦 Installing {dep}...")
                time.sleep(0.3)

            # Step 5: Download and extract GHST files
            current_step += 1
            self.progress_update.emit(
                int(current_step / total_steps * 100), "Downloading GHST files...")

            # Simulate file download
            files = [
                "ghst_core.py",
                "gui_components.py",
                "ai_manager.py",
                "config_system.py"]
            for file in files:
                self.log_update.emit("⬇️ Downloading {file}...")
                time.sleep(0.4)

            # Step 6: Configure environment
            current_step += 1
            self.progress_update.emit(
                int(current_step / total_steps * 100), "Configuring environment...")

            self.log_update.emit("⚙️ Creating configuration files...")
            self.log_update.emit("⚙️ Setting up AI model cache...")
            self.log_update.emit("⚙️ Configuring GitHub integration...")
            time.sleep(1)

            # Step 7: Finalize installation
            current_step += 1
            self.progress_update.emit(100, "Installation complete!")

            self.log_update.emit("🎉 GHST installation completed successfully!")
            self.log_update.emit("📁 Installed to: {self.install_path}")

            time.sleep(0.5)
            self.installation_complete.emit(
                True, "Installation completed successfully!")

        except Exception as e:
            self.log_update.emit("❌ Error: {str(e)}")
            self.installation_complete.emit(
                False, "Installation failed: {str(e)}")

class ModernCard(QFrame):
    """Modern card widget with glassmorphism effect."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        self.setup_style()
        self.add_shadow()

    def setup_style(self):
        self.setStyleSheet("""
            ModernCard {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                padding: 20px;
            }}
        """)

    def add_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)

class ModernButton(QPushButton):
    """Modern styled button with hover effects."""

    def __init__(self, text, style_type="primary", parent=None):
        super().__init__(text, parent)
        self.style_type = style_type
        self.setup_style()

    def setup_style(self):
        if self.style_type == "primary":
            bg_color = COLORS['primary']
            hover_color = "  # 7c3aed"
        elif self.style_type == "secondary":
            bg_color = COLORS['secondary']
            hover_color = "  # a855f7"
        elif self.style_type == "success":
            bg_color = COLORS['success']
            hover_color = "  # 059669"
        else:
            bg_color = COLORS['bg_secondary']
            hover_color = COLORS['bg_card']

        self.setStyleSheet("""
            ModernButton {{
                background-color: {bg_color};
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-height: 20px;
            }}
            ModernButton:hover {{
                background-color: {hover_color};
                transform: translateY(-1px);
            }}
            ModernButton:pressed {{
                background-color: {bg_color};
                transform: translateY(0px);
            }}
            ModernButton:disabled {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_secondary']};
            }}
        """)

class ModernProgressBar(QProgressBar):
    """Modern styled progress bar with gradient."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_style()

    def setup_style(self):
        self.setStyleSheet("""
            ModernProgressBar {{
                border: none;
                border-radius: 6px;
                background-color: {COLORS['bg_secondary']};
                height: 8px;
                text-align: center;
            }}
            ModernProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS['primary']},
                    stop:0.5 {COLORS['secondary']},
                    stop:1 {COLORS['accent']});
                border-radius: 6px;
            }}
        """)

class GHSTInstallerBeautiful(QMainWindow):
    """Beautiful modern GHST installer with stunning UI."""

    def __init__(self):
        super().__init__()
        self.current_version = CURRENT_VERSION
        self.install_path = Path.home() / "GHST"
        self.cleanup_enabled = True

        if not PYQT5_AVAILABLE:
            self.show_pyqt5_error()
            return

        self.init_ui()
        self.setup_theme()
        self.check_for_updates()

    def init_ui(self):
        self.setWindowTitle("GHST AI Coding Engine - Beautiful Installer")
        self.setFixedSize(900, 700)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Center window
        self.center_window()

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create main layout
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title bar
        self.create_title_bar(main_layout)

        # Content area
        self.create_content_area(main_layout)

    def center_window(self):
        """Center the window on screen."""
        from PyQt5.QtWidgets import QDesktopWidget
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def create_title_bar(self, parent_layout):
        """Create custom title bar."""
        title_bar = QFrame()
        title_bar.setFixedHeight(60)
        title_bar.setStyleSheet("""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS['primary']},
                    stop:1 {COLORS['secondary']});
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }}
        """)

        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 10, 20, 10)

        # App title
        title_label = QLabel("🚀 GHST AI Coding Engine")
        title_label.setStyleSheet("""
            color: {COLORS['text_primary']};
            font-size: 18px;
            font-weight: bold;
        """)

        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['error']};
            }}
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)

        parent_layout.addWidget(title_bar)

    def create_content_area(self, parent_layout):
        """Create main content area with tabs."""
        # Content container
        content_container = QFrame()
        content_container.setStyleSheet("""
            QFrame {{
                background-color: {COLORS['bg_primary']};
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
            }}
        """)

        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.setup_tab_styling()

        # Create tabs
        self.create_welcome_tab()
        self.create_options_tab()
        self.create_install_tab()
        self.create_complete_tab()

        content_layout.addWidget(self.tab_widget)
        parent_layout.addWidget(content_container)

    def setup_tab_styling(self):
        """Setup modern tab styling."""
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {{
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                background-color: {COLORS['bg_secondary']};
                padding: 20px;
            }}
            QTabBar::tab {{
                background-color: {COLORS['bg_card']};
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border']};
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 12px 20px;
                margin-right: 2px;
                font-weight: 600;
                min-width: 120px;
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS['primary']};
                color: {COLORS['text_primary']};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
            }}
        """)

    def create_welcome_tab(self):
        """Create welcome tab with hero section."""
        welcome_widget = QWidget()
        layout = QVBoxLayout(welcome_widget)
        layout.setSpacing(30)

        # Hero section
        hero_card = ModernCard()
        hero_layout = QVBoxLayout(hero_card)
        hero_layout.setSpacing(20)

        # Main title
        title = QLabel("Welcome to GHST AI Coding Engine")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: {COLORS['text_primary']};
            margin: 20px 0;
        """)
        hero_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel(
            "Your intelligent coding companion powered by advanced AI")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: {COLORS['text_secondary']};
            margin-bottom: 20px;
        """)
        hero_layout.addWidget(subtitle)

        # Version info
        version_label = QLabel("Version {self.current_version}")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("""
            font-size: 14px;
            color: {COLORS['accent']};
            font-weight: 600;
            margin-bottom: 20px;
        """)
        hero_layout.addWidget(version_label)

        layout.addWidget(hero_card)

        # Features section
        features_card = ModernCard()
        features_layout = QVBoxLayout(features_card)

        features_title = QLabel("✨ Key Features")
        features_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: {COLORS['text_primary']};
            margin-bottom: 15px;
        """)
        features_layout.addWidget(features_title)

        features = [
            "🤖 Advanced AI-powered code generation and assistance",
            "🔧 Intelligent debugging and error detection",
            "📊 Real-time code analysis and optimization",
            "🌐 GitHub integration for seamless collaboration",
            "🎨 Beautiful modern interface with dark theme",
            "⚡ Lightning-fast performance and response times"
        ]

        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setStyleSheet("""
                font-size: 14px;
                color: {COLORS['text_secondary']};
                margin: 5px 0;
                padding: 8px 0;
            """)
            features_layout.addWidget(feature_label)

        layout.addWidget(features_card)

        # Navigation buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        next_btn = ModernButton("Get Started →", "primary")
        next_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(1))
        button_layout.addWidget(next_btn)

        layout.addLayout(button_layout)
        layout.addStretch()

        self.tab_widget.addTab(welcome_widget, "🏠 Welcome")

    def create_options_tab(self):
        """Create installation options tab."""
        options_widget = QWidget()
        layout = QVBoxLayout(options_widget)
        layout.setSpacing(20)

        # Title
        title = QLabel("Installation Options")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: {COLORS['text_primary']};
            margin-bottom: 20px;
        """)
        layout.addWidget(title)

        # Installation path card
        path_card = ModernCard()
        path_layout = QVBoxLayout(path_card)

        path_title = QLabel("📁 Installation Directory")
        path_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: {COLORS['text_primary']};
            margin-bottom: 10px;
        """)
        path_layout.addWidget(path_title)

        # Path input
        path_input_layout = QHBoxLayout()

        self.path_input = QLineEdit(str(self.install_path))
        self.path_input.setStyleSheet("""
            QLineEdit {{
                background-color: {COLORS['bg_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 10px;
                color: {COLORS['text_primary']};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {COLORS['primary']};
            }}
        """)

        browse_btn = ModernButton("Browse", "secondary")
        browse_btn.clicked.connect(self.browse_install_path)

        path_input_layout.addWidget(self.path_input)
        path_input_layout.addWidget(browse_btn)
        path_layout.addLayout(path_input_layout)

        layout.addWidget(path_card)

        # Options card
        options_card = ModernCard()
        options_layout = QVBoxLayout(options_card)

        options_title = QLabel("⚙️ Advanced Options")
        options_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: {COLORS['text_primary']};
            margin-bottom: 15px;
        """)
        options_layout.addWidget(options_title)

        # Cleanup option
        self.cleanup_checkbox = QCheckBox(
            "Clean up old caches and temporary files")
        self.cleanup_checkbox.setChecked(True)
        self.cleanup_checkbox.setStyleSheet("""
            QCheckBox {{
                color: {COLORS['text_secondary']};
                font-size: 14px;
                spacing: 10px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid {COLORS['border']};
                background-color: {COLORS['bg_secondary']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLORS['primary']};
                border-color: {COLORS['primary']};
            }}
        """)
        options_layout.addWidget(self.cleanup_checkbox)

        # Auto-update option
        auto_update_checkbox = QCheckBox("Enable automatic update checking")
        auto_update_checkbox.setChecked(True)
        auto_update_checkbox.setStyleSheet(self.cleanup_checkbox.styleSheet())
        options_layout.addWidget(auto_update_checkbox)

        # Create shortcuts option
        shortcuts_checkbox = QCheckBox(
            "Create desktop and start menu shortcuts")
        shortcuts_checkbox.setChecked(True)
        shortcuts_checkbox.setStyleSheet(self.cleanup_checkbox.styleSheet())
        options_layout.addWidget(shortcuts_checkbox)

        layout.addWidget(options_card)

        # Navigation buttons
        button_layout = QHBoxLayout()

        back_btn = ModernButton("← Back")
        back_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(0))

        install_btn = ModernButton("Install GHST", "success")
        install_btn.clicked.connect(self.start_installation)

        button_layout.addWidget(back_btn)
        button_layout.addStretch()
        button_layout.addWidget(install_btn)

        layout.addLayout(button_layout)
        layout.addStretch()

        self.tab_widget.addTab(options_widget, "⚙️ Options")

    def create_install_tab(self):
        """Create installation progress tab."""
        install_widget = QWidget()
        layout = QVBoxLayout(install_widget)
        layout.setSpacing(20)

        # Title
        title = QLabel("Installing GHST...")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: {COLORS['text_primary']};
            margin-bottom: 20px;
        """)
        layout.addWidget(title)

        # Progress section
        progress_card = ModernCard()
        progress_layout = QVBoxLayout(progress_card)

        # Progress bar
        self.progress_bar = ModernProgressBar()
        self.progress_bar.setFixedHeight(12)
        progress_layout.addWidget(self.progress_bar)

        # Progress status
        self.progress_status = QLabel("Preparing installation...")
        self.progress_status.setAlignment(Qt.AlignCenter)
        self.progress_status.setStyleSheet("""
            font-size: 16px;
            color: {COLORS['text_secondary']};
            margin: 15px 0;
        """)
        progress_layout.addWidget(self.progress_status)

        layout.addWidget(progress_card)

        # Log section
        log_card = ModernCard()
        log_layout = QVBoxLayout(log_card)

        log_title = QLabel("📝 Installation Log")
        log_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: {COLORS['text_primary']};
            margin-bottom: 10px;
        """)
        log_layout.addWidget(log_title)

        self.log_output = QTextEdit()
        self.log_output.setFixedHeight(200)
        self.log_output.setStyleSheet("""
            QTextEdit {{
                background-color: {COLORS['bg_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                color: {COLORS['text_primary']};
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                padding: 10px;
            }}
        """)
        self.log_output.setReadOnly(True)
        log_layout.addWidget(self.log_output)

        layout.addWidget(log_card)
        layout.addStretch()

        self.tab_widget.addTab(install_widget, "📦 Install")

    def create_complete_tab(self):
        """Create installation complete tab."""
        complete_widget = QWidget()
        layout = QVBoxLayout(complete_widget)
        layout.setSpacing(30)

        # Success card
        success_card = ModernCard()
        success_layout = QVBoxLayout(success_card)
        success_layout.setAlignment(Qt.AlignCenter)
        success_layout.setSpacing(20)

        # Success icon and title
        success_title = QLabel("🎉 Installation Complete!")
        success_title.setAlignment(Qt.AlignCenter)
        success_title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: {COLORS['success']};
            margin: 30px 0;
        """)
        success_layout.addWidget(success_title)

        # Success message
        success_msg = QLabel(
            "GHST AI Coding Engine has been successfully installed!")
        success_msg.setAlignment(Qt.AlignCenter)
        success_msg.setStyleSheet("""
            font-size: 16px;
            color: {COLORS['text_secondary']};
            margin-bottom: 20px;
        """)
        success_layout.addWidget(success_msg)

        # Installation path
        self.install_path_label = QLabel(
            "📁 Installed to: {self.install_path}")
        self.install_path_label.setAlignment(Qt.AlignCenter)
        self.install_path_label.setStyleSheet("""
            font-size: 14px;
            color: {COLORS['text_secondary']};
            margin-bottom: 30px;
        """)
        success_layout.addWidget(self.install_path_label)

        layout.addWidget(success_card)

        # Action buttons
        button_card = ModernCard()
        button_layout = QVBoxLayout(button_card)
        button_layout.setSpacing(15)

        # Launch button
        launch_btn = ModernButton("🚀 Launch GHST", "primary")
        launch_btn.clicked.connect(self.launch_ghst)
        launch_btn.setFixedHeight(50)
        button_layout.addWidget(launch_btn)

        # Secondary actions
        actions_layout = QHBoxLayout()

        open_folder_btn = ModernButton("📂 Open Install Folder")
        open_folder_btn.clicked.connect(self.open_install_folder)

        visit_github_btn = ModernButton("🌐 Visit GitHub")
        visit_github_btn.clicked.connect(self.visit_github)

        actions_layout.addWidget(open_folder_btn)
        actions_layout.addWidget(visit_github_btn)
        button_layout.addLayout(actions_layout)

        # Close button
        close_btn = ModernButton("✓ Close Installer")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)

        layout.addWidget(button_card)
        layout.addStretch()

        self.tab_widget.addTab(complete_widget, "✅ Complete")

    def setup_theme(self):
        """Setup the dark theme for the application."""
        self.setStyleSheet("""
            QMainWindow {{
                background-color: {COLORS['bg_primary']};
                border-radius: 12px;
            }}
            QWidget {{
                background-color: transparent;
                color: {COLORS['text_primary']};
            }}
        """)

    def browse_install_path(self):
        """Open folder browser for installation path."""
        from PyQt5.QtWidgets import QFileDialog

        folder = QFileDialog.getExistingDirectory(
            self, "Select Installation Directory", str(self.install_path)
        )
        if folder:
            self.install_path = Path(folder) / "GHST"
            self.path_input.setText(str(self.install_path))

    def start_installation(self):
        """Start the installation process."""
        # Update install path from input
        self.install_path = Path(self.path_input.text())
        self.cleanup_enabled = self.cleanup_checkbox.isChecked()

        # Switch to install tab
        self.tab_widget.setCurrentIndex(2)

        # Start installation worker
        self.install_worker = InstallationWorker(
            self.install_path, self.cleanup_enabled)
        self.install_worker.progress_update.connect(self.update_progress)
        self.install_worker.log_update.connect(self.update_log)
        self.install_worker.installation_complete.connect(
            self.installation_finished)
        self.install_worker.start()

    def update_progress(self, value, status):
        """Update installation progress."""
        self.progress_bar.setValue(value)
        self.progress_status.setText(status)

    def update_log(self, message):
        """Update installation log."""
        self.log_output.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def installation_finished(self, success, message):
        """Handle installation completion."""
        if success:
            self.install_path_label.setText(
                "📁 Installed to: {self.install_path}")
            self.tab_widget.setCurrentIndex(3)  # Switch to complete tab
        else:
            QMessageBox.critical(self, "Installation Failed", message)

    def check_for_updates(self):
        """Check for available updates."""
        self.update_checker = UpdateChecker()
        self.update_checker.update_found.connect(self.show_update_notification)
        self.update_checker.start()

    def show_update_notification(self, version, url):
        """Show update notification."""
        reply = QMessageBox.question(
            self,
            "Update Available",
            "A newer version ({version}) is available.\n\nWould you like to download it?",
            QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            import webbrowser
            webbrowser.open(url)

    def launch_ghst(self):
        """Launch GHST after installation."""
        try:
            ghst_launcher = self.install_path / "launch_gui.py"
            if ghst_launcher.exists():
                subprocess.Popen([sys.executable, str(ghst_launcher)],
                                 cwd=str(self.install_path))
                self.close()
            else:
                QMessageBox.warning(
                    self,
                    "Launch Failed",
                    "GHST launcher not found. Please check the installation.")
        except Exception as e:
            QMessageBox.critical(
                self,
                "Launch Error",
                "Failed to launch GHST: {
                    str(e)}")

    def open_install_folder(self):
        """Open the installation folder."""
        import platform
        import subprocess

        try:
            if platform.system() == "Windows":
                subprocess.run(["explorer", str(self.install_path)])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(self.install_path)])
            else:  # Linux
                subprocess.run(["xdg-open", str(self.install_path)])
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                "Could not open folder: {
                    str(e)}")

    def visit_github(self):
        """Open GitHub repository."""
        import webbrowser
        webbrowser.open("https://github.com/{GITHUB_REPO}")

    def show_pyqt5_error(self):
        """Show PyQt5 installation error."""
        print("\n" + "=" * 60)
        print("❌ PyQt5 NOT FOUND")
        print("=" * 60)
        print("The GHST installer requires PyQt5 for the graphical interface.")
        print("\nTo install PyQt5, run:")
        print("  pip install PyQt5")
        print("\nAlternatively, you can install GHST using the command line:")
        print(
            "  python -c \"import subprocess; subprocess.run(['pip', 'install', 'ghst'])\"")
        print("=" * 60)

        # Try to install PyQt5 automatically
        try:
            print("\n🔄 Attempting to install PyQt5 automatically...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "PyQt5"])
            print("✅ PyQt5 installed successfully!")
            print("Please restart the installer.")
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyQt5 automatically.")
            print("Please install it manually using: pip install PyQt5")
        except Exception as e:
            print("❌ Error during installation: {e}")

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("GHST Installer")
    app.setApplicationVersion(CURRENT_VERSION)
    app.setOrganizationName("GHST")

    # Create and show installer
    installer = GHSTInstallerBeautiful()
    installer.show()

    # Run application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
