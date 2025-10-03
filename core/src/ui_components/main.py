"""
GHST Main Window - AI Coding Engine Interface

Modern interface for AI-assisted coding, debugging, and problem solving.
"""

import sys

from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QFrame,
)


class GHSTWindow(QMainWindow):
    """
    Main window class for the GHST AI Coding Engine application.
    
    Features:
        - Modern, customizable UI with professional styling and theming.
        - Left pane: SPEEDBUILD automation control, AI expert agents list, and tools.
        - Center pane: Tabbed workspace including welcome and code editor tabs.
        - Right pane: AI assistant chat interface for expert collaboration.
        - Menu bar: File, AI Experts, Tools, and Help menus.
        - Status bar: Displays application status and live autocommit ticker.
        - Extensible architecture for plugin and expert management.
    """
    
    def __init__(self):
        super().__init__()
        self.expert_manager = None
        self.config_manager = None
        self.ss_manager = None  # Syntax Supervisors Manager
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("GHST - AI Coding Engine")
        self.setGeometry(100, 100, 1400, 900)

        # Apply GHST theme
        if hasattr(self, 'apply_ghst_theme'):
            self.apply_ghst_theme()

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # Create main splitter for resizable panes
        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)

        # Left pane - Professional sidebar
        left_pane = self.create_left_pane()
        self.main_splitter.addWidget(left_pane)

        # Center pane - Main work area
        center_pane = self.create_center_pane()
        self.main_splitter.addWidget(center_pane)

        # Right pane - AI assistance and chat
        right_pane = self.create_right_pane()
        self.main_splitter.addWidget(right_pane)

        # Side panel for documentation (initially hidden)
        from .side_panel import SidePanel
        self.side_panel = SidePanel()
        self.side_panel.hide()
        self.side_panel.closed.connect(self.on_side_panel_closed)
        self.main_splitter.addWidget(self.side_panel)

        # Set splitter proportions
        self.main_splitter.setStretchFactor(0, 1)  # Left pane
        self.main_splitter.setStretchFactor(1, 3)  # Center pane (largest)
        self.main_splitter.setStretchFactor(2, 1)  # Right pane
        self.main_splitter.setStretchFactor(3, 1)  # Side panel

        # Create menu bar
        self.create_menu_bar()

        # Create status bar
        self.create_status_bar()

        # Add autocommit ticker to status bar
        self.add_autocommit_ticker()
    
    def on_side_panel_closed(self):
        """Handle side panel close event."""
        pass  # Side panel will hide itself
    
    def toggle_side_panel(self):
        """Toggle the documentation side panel."""
        if self.side_panel.isVisible():
            self.side_panel.hide()
        else:
            self.side_panel.show()
            # Set some example content
            self.side_panel.set_markdown("""
                <h2>GHST Documentation</h2>
                <p>Welcome to the GHST documentation panel!</p>
                <h3>Quick Start</h3>
                <ul>
                    <li>Select an AI expert to get started</li>
                    <li>Open a project or create a new one</li>
                    <li>Get AI-powered assistance</li>
                </ul>
            """)
            self.side_panel.set_code("""# Example code
def hello_ghst():
    print("Hello from GHST!")
    
hello_ghst()
""")
    """Main window for GHST AI Coding Engine."""

    def __init__(self):
        super().__init__()
        self.expert_manager = None
        self.config_manager = None
        self.ss_manager = None  # Syntax Supervisors Manager
        self.init_ui()

    def create_left_pane(self):
        """Create left pane with expert agents and tools."""
        from .speedbuild_slider import SpeedbuildSlider
        widget = QWidget()
        widget.setMaximumWidth(280)
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(16)
        widget.setLayout(layout)

        # SPEEDBUILD Control Panel
        speedbuild_label = QLabel("⚡ SPEEDBUILD")
        speedbuild_label.setStyleSheet("""
            QLabel {
                color: #0a84ff;
                font-size: 16px;
                font-weight: 600;
                padding: 8px 0;
            }
        """)
        layout.addWidget(speedbuild_label)
        
        self.speedbuild_slider = SpeedbuildSlider()
        layout.addWidget(self.speedbuild_slider)

        # Separator
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setStyleSheet("background-color: #3a3a3a; max-height: 1px;")
        layout.addWidget(separator1)

        # Expert agents section
        experts_label = QLabel("🧠 AI Experts")
        experts_label.setStyleSheet("""
            QLabel {
                color: #0a84ff;
                font-size: 16px;
                font-weight: 600;
                padding: 8px 0;
            }
        """)
        layout.addWidget(experts_label)

        self.experts_list = QListWidget()
        self.experts_list.addItems([
            "🔍 Code Analysis",
            "🐛 Debugging",
            "🛠️ Problem Solving",
            "📚 Research",
            "⚡ Performance",
            "🔒 Security",
            "📝 Documentation",
            "🧪 Testing",
            "🏗️ Architecture",
            "🎨 UI/UX",
            "🚀 DevOps",
            "📊 Data Science"
        ])
        self.experts_list.setMaximumHeight(280)
        layout.addWidget(self.experts_list)

        # Separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setStyleSheet("background-color: #3a3a3a; max-height: 1px;")
        layout.addWidget(separator2)

        # Tools section
        tools_label = QLabel("🔧 Tools")
        tools_label.setStyleSheet("""
            QLabel {
                color: #0a84ff;
                font-size: 16px;
                font-weight: 600;
                padding: 8px 0;
            }
        """)
        layout.addWidget(tools_label)

        self.tools_list = QListWidget()
        self.tools_list.addItems([
            "📦 Plugins",
            "⚙️ Settings",
            "📋 Templates",
            "✂️ Snippets"
        ])
        layout.addWidget(self.tools_list)

        layout.addStretch()
        
        # View Docs button
        docs_btn = QPushButton("📄 View Documentation")
        docs_btn.clicked.connect(self.toggle_side_panel)
        layout.addWidget(docs_btn)

        return widget

    def create_center_pane(self):
        """Create center pane with main work area."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        widget.setLayout(layout)

        # Tab widget for multiple work areas
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        layout.addWidget(self.tab_widget)

        # Welcome tab
        welcome_tab = QWidget()
        welcome_layout = QVBoxLayout()
        welcome_layout.setContentsMargins(24, 24, 24, 24)
        welcome_tab.setLayout(welcome_layout)

        welcome_text = QTextEdit()
        welcome_text.setHtml("""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; color: #e8e8e8;">
            <h1 style="color: #0a84ff; font-weight: 600; font-size: 32px; margin-bottom: 16px;">
                🚀 Welcome to GHST
            </h1>
            <h2 style="color: #999999; font-weight: 400; font-size: 18px; margin-bottom: 32px;">
                Your AI Coding Engine with Expert Agent Think Tank
            </h2>

            <h3 style="color: #e8e8e8; font-weight: 600; font-size: 20px; margin-top: 24px; margin-bottom: 12px;">
                ✨ Features
            </h3>
            <ul style="line-height: 1.8; font-size: 14px;">
                <li><strong style="color: #0a84ff;">AI Collaboration Framework:</strong> Multiple AI experts work together seamlessly</li>
                <li><strong style="color: #0a84ff;">Plugin System:</strong> Extensible tools and workflows for any task</li>
                <li><strong style="color: #0a84ff;">Configuration Management:</strong> YAML-based settings you control</li>
                <li><strong style="color: #0a84ff;">Modern UI:</strong> Clean, intuitive, iOS-inspired interface</li>
                <li><strong style="color: #0a84ff;">Developer Tools:</strong> Built-in automation and utilities</li>
            </ul>

            <h3 style="color: #e8e8e8; font-weight: 600; font-size: 20px; margin-top: 24px; margin-bottom: 12px;">
                🎯 Getting Started
            </h3>
            <ol style="line-height: 1.8; font-size: 14px;">
                <li>Select an AI expert from the left panel to activate specialized assistance</li>
                <li>Open or create a project to begin coding</li>
                <li>Get AI assistance with coding, debugging, and problem solving</li>
                <li>Use the side panel for quick documentation reference</li>
            </ol>

            <p style="margin-top: 32px; padding: 16px; background-color: rgba(10, 132, 255, 0.1); border-left: 3px solid #0a84ff; border-radius: 4px; font-size: 14px;">
                <em>💡 Remember: You maintain full control. All AI recommendations require your validation.</em>
            </p>
        </div>
        """)
        welcome_text.setReadOnly(True)
        welcome_layout.addWidget(welcome_text)

        self.tab_widget.addTab(welcome_tab, "Welcome")

        # Code editor tab with enhanced display
        code_tab = QWidget()
        code_layout = QVBoxLayout()
        code_layout.setContentsMargins(12, 12, 12, 12)
        code_tab.setLayout(code_layout)

        # Add code display box
        from .code_display import CodeDisplayBox
        self.code_display = CodeDisplayBox("Python Code")
        self.code_display.set_code("""# Your AI-assisted code here
# The AI experts are ready to help!

def main():
    print("Welcome to GHST - AI Coding Engine")
    # Start coding with AI assistance

if __name__ == "__main__":
    main()
""")
        code_layout.addWidget(self.code_display)

        self.tab_widget.addTab(code_tab, "Code Editor")

        return widget

    def create_right_pane(self):
        """Create right pane with AI assistance and chat."""
        widget = QWidget()
        widget.setMaximumWidth(350)
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        widget.setLayout(layout)

        # AI Chat section header
        chat_header = QLabel("💬 AI Assistant")
        chat_header.setStyleSheet("""
            QLabel {
                color: #0a84ff;
                font-size: 16px;
                font-weight: 600;
                padding: 8px 0;
            }
        """)
        layout.addWidget(chat_header)

        # Chat display with welcome message
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setHtml("""
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
                <div style="background-color: rgba(10, 132, 255, 0.15); padding: 12px; border-radius: 8px; margin: 8px 0;">
                    <strong style="color: #0a84ff;">🧠 AI Expert Collective</strong><br>
                    <span style="color: #999999; font-size: 13px;">Ready to assist with coding tasks!</span>
                </div>
                <div style="background-color: rgba(255, 255, 255, 0.05); padding: 12px; border-radius: 8px; margin: 8px 0;">
                    <span style="color: #e8e8e8; font-size: 13px;">💡 Ask questions, request code reviews, or get debugging help.</span>
                </div>
            </div>
        """)
        layout.addWidget(self.chat_display)

        # Chat input area
        input_container = QWidget()
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)
        input_container.setLayout(input_layout)

        self.chat_input = QTextEdit()
        self.chat_input.setPlaceholderText("Type your message here...")
        self.chat_input.setMaximumHeight(80)
        self.chat_input.setStyleSheet("""
            QTextEdit {
                background-color: #252525;
                color: #e8e8e8;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 1px solid #0a84ff;
            }
        """)
        input_layout.addWidget(self.chat_input)

        # Send button with icon
        send_button = QPushButton("✉️ Send Message")
        send_button.clicked.connect(self.send_chat_message)
        send_button.setFixedHeight(40)
        input_layout.addWidget(send_button)

        layout.addWidget(input_container)

        return widget

    def create_menu_bar(self):
        """Create application menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('📁 File')
        file_menu.addAction('🆕 New Project', self.new_project)
        file_menu.addAction('📂 Open Project', self.open_project)
        file_menu.addSeparator()
        file_menu.addAction('❌ Exit', self.close)

        # View menu
        view_menu = menubar.addMenu('👁️ View')
        view_menu.addAction('📄 Toggle Documentation Panel', self.toggle_side_panel)

        # AI menu
        ai_menu = menubar.addMenu('🧠 AI Experts')
        ai_menu.addAction('📊 Expert Status', self.show_expert_status)
        ai_menu.addAction('⚙️ Configure Experts', self.configure_experts)

        # Tools menu
        tools_menu = menubar.addMenu('🔧 Tools')
        tools_menu.addAction('📦 Plugin Manager', self.open_plugin_manager)
        tools_menu.addAction('⚙️ Configuration', self.open_configuration)

        # Help menu
        help_menu = menubar.addMenu('❓ Help')
        help_menu.addAction('ℹ️ About GHST', self.show_about)

    def create_status_bar(self):
        """Create application status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("GHST AI Coding Engine - Ready")

    def add_autocommit_ticker(self):
        """Add live autocommit ticker to the status bar."""
        from PyQt5.QtCore import QTimer
        self.autocommit_label = QLabel("🔄 Last autocommit: loading...")
        self.status_bar.addPermanentWidget(self.autocommit_label)
        self.autocommit_timer = QTimer(self)
        self.autocommit_timer.timeout.connect(self.update_autocommit_ticker)
        self.autocommit_timer.start(10000)  # Refresh every 10 seconds
        self.update_autocommit_ticker()

    def update_autocommit_ticker(self):
        """Update the autocommit ticker with latest commit info."""
        import subprocess
        try:
            result = subprocess.run([
                "git", "log", "-1", "--pretty=format:%h %s (%ci)"
            ], capture_output=True, text=True, cwd=None)
            if result.returncode == 0:
                commit_info = result.stdout.strip()
                if commit_info:
                    self.autocommit_label.setText(f"🔄 Last autocommit: {commit_info}")
                else:
                    self.autocommit_label.setText("🔄 Last autocommit: No commits found.")
            else:
                self.autocommit_label.setText("❌ Autocommit ticker error: git log failed.")
        except Exception as e:
            self.autocommit_label.setText(f"❌ Autocommit ticker error: {e}")

    def apply_styling(self):
        """Apply modern styling to the interface."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                font-weight: bold;
                color: #ffffff;
                padding: 5px;
            }
            QListWidget {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
            }
            QTextEdit {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #3c3c3c;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #0d7377;
            }
        """)

    def send_chat_message(self):
        """Handle sending chat message to AI experts."""
        message = self.chat_input.toPlainText().strip()
        if message:
            # Add user message with styling
            current_html = self.chat_display.toHtml()
            user_msg = f"""
                <div style="background-color: rgba(10, 132, 255, 0.2); padding: 10px; border-radius: 8px; margin: 8px 0;">
                    <strong style="color: #0a84ff;">👤 You:</strong><br>
                    <span style="color: #e8e8e8; font-size: 13px;">{message}</span>
                </div>
            """
            self.chat_display.setHtml(current_html + user_msg)
            self.chat_input.clear()

            # Simulate AI response (replace with actual AI integration)
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(500, lambda: self.add_ai_response(
                "I understand your request. Let me analyze this and provide assistance..."))

    def new_project(self):
        """Create a new project."""
        QMessageBox.information(
            self,
            "New Project",
            "New project functionality coming soon!")

    def open_project(self):
        """Open an existing project."""
        QMessageBox.information(
            self,
            "Open Project",
            "Open project functionality coming soon!")

    def show_expert_status(self):
        """Show AI expert status."""
        if self.expert_manager:
            status = self.expert_manager.get_experts_status()
            msg = f"Active Experts: {status['active_experts']}/{status['total_experts']}"
            QMessageBox.information(self, "Expert Status", msg)
        else:
            QMessageBox.information(self, "Expert Status", "Expert manager not initialized.")

    def configure_experts(self):
        """Configure AI experts."""
        QMessageBox.information(
            self,
            "Configure Experts",
            "Expert configuration coming soon!")

    def open_plugin_manager(self):
        """Open plugin manager."""
        QMessageBox.information(
            self,
            "Plugin Manager",
            "Plugin manager coming soon!")

    def open_configuration(self):
        """Open configuration."""
        from .settings_dialog import SettingsDialog
        dialog = SettingsDialog(self)
        dialog.exec_()

    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About GHST",
            "GHST - Open Source AI Coding Engine\n\n" +
            "An AI-driven coding assistant with expert agent think tank.\n" +
            "Designed for coding, debugging, and creative problem solving.\n\n" +
            "Version: 0.1.0-alpha\n" +
            "License: MIT")

    def apply_ghst_theme(self):
        """Apply professional GHST theme with iOS/Mac-inspired design."""
        ghost_theme = """
        QMainWindow {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        
        QWidget {
            background-color: #1a1a1a;
            color: #e8e8e8;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
        }
        
        QTextEdit {
            background-color: #252525;
            color: #e8e8e8;
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            padding: 12px;
            font-family: 'SF Mono', 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 13px;
            selection-background-color: #0a84ff;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0a84ff, stop:1 #0066cc);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 13px;
            min-height: 32px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3a9aff, stop:1 #0a84ff);
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0066cc, stop:1 #0055aa);
        }
        
        QLabel {
            color: #e8e8e8;
            font-weight: 600;
            font-size: 14px;
            padding: 4px;
        }
        
        QListWidget {
            background-color: #252525;
            color: #e8e8e8;
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            padding: 8px;
            outline: none;
        }
        
        QListWidget::item {
            padding: 8px 12px;
            border-radius: 6px;
            margin: 2px 0;
        }
        
        QListWidget::item:hover {
            background-color: #2f2f2f;
        }
        
        QListWidget::item:selected {
            background-color: #0a84ff;
            color: white;
        }
        
        QTabWidget::pane {
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            background-color: #252525;
            top: -1px;
        }
        
        QTabBar::tab {
            background-color: #252525;
            color: #999999;
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-weight: 500;
            font-size: 13px;
        }
        
        QTabBar::tab:hover {
            background-color: #2f2f2f;
            color: #e8e8e8;
        }
        
        QTabBar::tab:selected {
            background-color: #0a84ff;
            color: white;
        }
        
        QSplitter::handle {
            background-color: #3a3a3a;
            width: 1px;
        }
        
        QSplitter::handle:hover {
            background-color: #4a4a4a;
        }
        
        QStatusBar {
            background-color: #1f1f1f;
            color: #999999;
            border-top: 1px solid #3a3a3a;
            font-size: 12px;
        }
        
        QMenuBar {
            background-color: #1f1f1f;
            color: #e8e8e8;
            border-bottom: 1px solid #3a3a3a;
            padding: 4px;
        }
        
        QMenuBar::item {
            padding: 6px 12px;
            border-radius: 4px;
        }
        
        QMenuBar::item:selected {
            background-color: #2f2f2f;
        }
        
        QMenu {
            background-color: #252525;
            color: #e8e8e8;
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            padding: 4px;
        }
        
        QMenu::item {
            padding: 8px 24px;
            border-radius: 4px;
        }
        
        QMenu::item:selected {
            background-color: #0a84ff;
            color: white;
        }
        
        QScrollBar:vertical {
            background-color: #1a1a1a;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #3a3a3a;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #4a4a4a;
        }
        
        QScrollBar:horizontal {
            background-color: #1a1a1a;
            height: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #3a3a3a;
            border-radius: 6px;
            min-width: 20px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #4a4a4a;
        }
        
        QScrollBar::add-line, QScrollBar::sub-line {
            border: none;
            background: none;
        }
        """
        self.setStyleSheet(ghost_theme)

    def add_ai_response(self, response):
        """Add AI response to chat display."""
        current_html = self.chat_display.toHtml()
        ai_msg = f"""
            <div style="background-color: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; margin: 8px 0;">
                <strong style="color: #00d9ff;">🧠 AI Expert:</strong><br>
                <span style="color: #e8e8e8; font-size: 13px;">{response}</span>
            </div>
        """
        self.chat_display.setHtml(current_html + ai_msg)
        
        # Scroll to bottom
        scrollbar = self.chat_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def update_ss_status(self, status_info):
        """Update Syntax Supervisors status display."""
        if hasattr(self, 'ss_status_label'):
            status_text = f"🔍 SS: {status_info.get('active', 0)} active"
            self.ss_status_label.setText(status_text)

    def add_ss_status_widget(self):
        """Add Syntax Supervisors status to the status bar."""
        if hasattr(self, 'statusBar'):
            self.ss_status_label = QLabel("🔍 SS: Initializing...")
            self.statusBar().addPermanentWidget(self.ss_status_label)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = GHSTWindow()
    window.show()
    sys.exit(app.exec_())
