<<<<<<< HEAD
"""
GHST Main Window - AI Coding Engine Interface

Modern interface for AI-assisted coding, debugging, and problem solving.
"""

import sys

from PyQt5.QtCore import Qt
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
)


class GHSTWindow(QMainWindow):
    GHSTWindow(QMainWindow)
    -----------------------
    Main window class for the GHST AI Coding Engine application.
    Features:
        - Modern, customizable UI with professional styling and theming.
        - Left pane: SPEEDBUILD automation control, AI expert agents list, and tools.
        - Center pane: Tabbed workspace including welcome and code editor tabs.
        - Right pane: AI assistant chat interface for expert collaboration.
        - Menu bar: File, AI Experts, Tools, and Help menus.
        - Status bar: Displays application status and live autocommit ticker.
        - Extensible architecture for plugin and expert management.
    Key Methods:
        - init_ui(): Initializes the main UI layout and components.
        - create_left_pane(): Builds the sidebar with expert agents and tools.
        - create_center_pane(): Sets up the main work area with tabs.
        - create_right_pane(): Provides AI chat and assistance features.
        - create_menu_bar(): Configures the application menu bar.
        - create_status_bar(): Sets up the status bar.
        - add_autocommit_ticker(): Adds a live git commit ticker to the status bar.
        - apply_styling(): Applies modern styling to the interface.
        - apply_ghst_theme(): Applies the professional GHST theme.
        - send_chat_message(): Handles sending messages to AI experts.
        - update_ss_status(): Updates Syntax Supervisors status display.
        - add_ss_status_widget(): Adds Syntax Supervisors status to the status bar.
    Attributes:
        - expert_manager: Manages AI expert agents.
        - config_manager: Handles configuration settings.
        - ss_manager: Manages Syntax Supervisors.
        - speedbuild_slider: Controls SPEEDBUILD automation.
        - experts_list: Displays available AI experts.
        - tools_list: Displays available tools.
        - tab_widget: Main tabbed workspace.
        - code_editor: Code editing area.
        - chat_display: AI chat output.
        - chat_input: AI chat input.
        - status_bar: Application status bar.
        - autocommit_label: Displays latest git commit info.
        - ss_status_label: Displays Syntax Supervisors status.
    Usage:
        Instantiate and show GHSTWindow as the main application window.
    def apply_styling(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #222831;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #f8f8f8;
                background-color: #222831;
            }
            QLabel {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 14px;
                color: #00adb5;
                text-shadow: 1px 1px 2px #222;
            }
            QListWidget {
                background: #393e46;
                border-radius: 12px;
                padding: 12px;
                font-size: 16px;
                box-shadow: 0 2px 8px #222;
            }
            QSlider::groove:horizontal {
                border: 1px solid #00adb5;
                height: 10px;
                background: #393e46;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: #00adb5;
                border: 2px solid #f8f8f8;
                width: 22px;
                height: 22px;
                margin: -7px 0;
                border-radius: 11px;
                box-shadow: 0 2px 6px #222;
            }
            QSlider {
                margin: 16px 0 28px 0;
            }
        """)
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
        central_widget.setLayout(main_layout)

        # Create splitter for resizable panes
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left pane - Professional sidebar
        left_pane = QWidget()
        left_layout = QVBoxLayout()
        left_pane.setLayout(left_layout)

        # Sidebar card
        sidebar_card = QWidget()
        sidebar_card.setStyleSheet("background: #393e46; border-radius: 16px; box-shadow: 0 2px 12px #222; padding: 18px;")
        card_layout = QVBoxLayout()
        sidebar_card.setLayout(card_layout)

        # Section header
        card_layout.addWidget(QLabel("⚡ SPEEDBUILD Control Panel"))

        # Prominent slider
        from .speedbuild_slider import SpeedbuildSlider
        self.speedbuild_slider = SpeedbuildSlider()
        card_layout.addWidget(self.speedbuild_slider)

        # Interactive button for SPEEDBUILD mode
        from PyQt5.QtWidgets import QPushButton
        self.speedbuild_btn = QPushButton("Apply SPEEDBUILD Mode")
        self.speedbuild_btn.setStyleSheet("background: #00adb5; color: #fff; font-weight: bold; border-radius: 8px; padding: 8px 16px;")
        card_layout.addWidget(self.speedbuild_btn)

        left_layout.addWidget(sidebar_card)
        left_layout.addStretch()
        splitter.addWidget(left_pane)

        # Center pane - Main work area
        if hasattr(self, 'create_center_pane'):
            center_pane = self.create_center_pane()
            splitter.addWidget(center_pane)

        # Right pane - AI assistance and chat
        if hasattr(self, 'create_right_pane'):
            right_pane = self.create_right_pane()
            splitter.addWidget(right_pane)

        # Set splitter proportions
        splitter.setStretchFactor(0, 1)  # Left pane
        splitter.setStretchFactor(1, 3)  # Center pane (largest)
        splitter.setStretchFactor(2, 1)  # Right pane

        # Create menu bar
        if hasattr(self, 'create_menu_bar'):
            self.create_menu_bar()

        # Create status bar
        if hasattr(self, 'create_status_bar'):
            self.create_status_bar()

        # Apply styling
        if hasattr(self, 'apply_styling'):
            self.apply_styling()

        # Add autocommit ticker to status bar (after status bar is created)
        if hasattr(self, 'add_autocommit_ticker'):
            self.add_autocommit_ticker()
    """Main window for GHST AI Coding Engine."""

    def __init__(self):
        super().__init__()
        self.expert_manager = None
        self.config_manager = None
        self.ss_manager = None  # Syntax Supervisors Manager
        self.init_ui()

    def create_left_pane(self):
        from .speedbuild_slider import SpeedbuildSlider
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # SPEEDBUILD slider for branch control
        layout.addWidget(QLabel("⚙️ SPEEDBUILD Automation Control"))
        self.speedbuild_slider = SpeedbuildSlider()
        layout.addWidget(self.speedbuild_slider)

        # Expert agents section
        layout.addWidget(QLabel("🧠 AI Expert Agents"))

        self.experts_list = QListWidget()
        self.experts_list.addItems([
            "🔍 Code Analysis Expert",
            "🐛 Debugging Expert",
            "🛠️ Problem Solving Expert",
            "📚 Research Expert",
            "⚡ Performance Expert",
            "🔒 Security Expert",
            "📝 Documentation Expert",
            "🧪 Testing Expert",
            "🏗️ Architecture Expert",
            "🎨 UI/UX Expert",
            "🚀 DevOps Expert",
            "📊 Data Expert"
        ])
        layout.addWidget(self.experts_list)

        # Tools section
        layout.addWidget(QLabel("🔧 Tools"))

        self.tools_list = QListWidget()
        self.tools_list.addItems([
            "Plugin Manager",
            "Configuration",
            "Project Templates",
            "Code Snippets"
        ])
        layout.addWidget(self.tools_list)

        return widget
    def create_left_pane(self):
        """Create left pane with expert agents and tools."""
        from .speedbuild_slider import SpeedbuildSlider
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # SPEEDBUILD slider for branch control
        layout.addWidget(QLabel("⚙️ SPEEDBUILD Automation Control"))
        self.speedbuild_slider = SpeedbuildSlider()
        layout.addWidget(self.speedbuild_slider)

        # Expert agents section
        layout.addWidget(QLabel("🧠 AI Expert Agents"))

        self.experts_list = QListWidget()
        self.experts_list.addItems([
            "🔍 Code Analysis Expert",
            "🐛 Debugging Expert",
            "🛠️ Problem Solving Expert",
            "📚 Research Expert",
            "⚡ Performance Expert",
            "🔒 Security Expert",
            "📝 Documentation Expert",
            "🧪 Testing Expert",
            "🏗️ Architecture Expert",
            "🎨 UI/UX Expert",
            "🚀 DevOps Expert",
            "📊 Data Expert"
        ])
        layout.addWidget(self.experts_list)

        # Tools section
        layout.addWidget(QLabel("🔧 Tools"))

        self.tools_list = QListWidget()
        self.tools_list.addItems([
            "Plugin Manager",
            "Configuration",
            "Project Templates",
            "Code Snippets"
        ])
        layout.addWidget(self.tools_list)

        return widget

    def create_center_pane(self):
        """Create center pane with main work area."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Tab widget for multiple work areas
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Welcome tab
        welcome_tab = QWidget()
        welcome_layout = QVBoxLayout()
        welcome_tab.setLayout(welcome_layout)

        welcome_text = QTextEdit()
        welcome_text.setHtml("""
        <h2>🚀 Welcome to GHST - AI Coding Engine</h2>
        <p>Your open-source AI coding assistant with expert agent think tank.</p>

        <h3>✨ Features:</h3>
        <ul>
            <li><strong>AI Collaboration Framework:</strong> Multiple AI experts work together</li>
            <li><strong>Plugin System:</strong> Extensible tools and workflows</li>
            <li><strong>Configuration Management:</strong> YAML-based settings</li>
            <li><strong>Modern UI:</strong> Clean, customizable interface</li>
            <li><strong>Developer Tools:</strong> Built-in automation and utilities</li>
        </ul>

        <h3>🎯 Getting Started:</h3>
        <ol>
            <li>Select an AI expert from the left panel</li>
            <li>Open or create a project</li>
            <li>Get AI assistance with coding, debugging, and problem solving</li>
        </ol>

        <p><em>Remember: You maintain full control. All AI recommendations require your validation.</em></p>
        """)
        welcome_text.setReadOnly(True)
        welcome_layout.addWidget(welcome_text)

        self.tab_widget.addTab(welcome_tab, "Welcome")

        # Code editor tab (placeholder)
        code_tab = QWidget()
        code_layout = QVBoxLayout()
        code_tab.setLayout(code_layout)

        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText(
            "// Your code here...\n// AI experts are ready to assist!")
        code_layout.addWidget(self.code_editor)

        self.tab_widget.addTab(code_tab, "Code Editor")

        return widget

    def create_right_pane(self):
        """Create right pane with AI assistance and chat."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # AI Chat section
        layout.addWidget(QLabel("💬 AI Assistant"))

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.append(
            "🧠 AI Expert Collective: Ready to assist with coding tasks!")
        self.chat_display.append(
            "💡 Ask questions, request code reviews, or get debugging help.")
        layout.addWidget(self.chat_display)

        # Chat input
        self.chat_input = QTextEdit()
        self.chat_input.setMaximumHeight(60)
        self.chat_input.setPlaceholderText("Ask the AI experts anything...")
        layout.addWidget(self.chat_input)

        # Send button
        send_button = QPushButton("Send to Experts")
        send_button.clicked.connect(self.send_chat_message)
        layout.addWidget(send_button)

        return widget

    def create_menu_bar(self):
        """Create application menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')
        file_menu.addAction('New Project', self.new_project)
        file_menu.addAction('Open Project', self.open_project)
        file_menu.addSeparator()
        file_menu.addAction('Exit', self.close)

        # AI menu
        ai_menu = menubar.addMenu('AI Experts')
        ai_menu.addAction('Expert Status', self.show_expert_status)
        ai_menu.addAction('Configure Experts', self.configure_experts)

        # Tools menu
        tools_menu = menubar.addMenu('Tools')
        tools_menu.addAction('Plugin Manager', self.open_plugin_manager)
        tools_menu.addAction('Configuration', self.open_configuration)

        # Help menu
        help_menu = menubar.addMenu('Help')
        help_menu.addAction('About GHST', self.show_about)

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
            self.chat_display.append("👤 You: {message}")
            self.chat_input.clear()

            # Simulate AI response (replace with actual AI integration)
            self.chat_display.append(
                "🧠 AI Expert: I understand your request. Let me analyze this and provide assistance...")

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
        QMessageBox.information(
            self,
            "Configuration",
            "Configuration panel coming soon!")

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
        """Apply professional GHST theme with subtle ghost references."""
        ghost_theme = """
        QMainWindow {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        QTextEdit {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 1px solid #404040;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        QPushButton {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #106ebe;
        }
        QLabel {
            color: #ffffff;
            font-weight: bold;
        }
        QListWidget {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 1px solid #404040;
        }
        QTabWidget::pane {
            border: 1px solid #404040;
        }
        QTabBar::tab {
            background-color: #2d2d2d;
            color: #ffffff;
            padding: 8px 16px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #0078d4;
        }
        """
        self.setStyleSheet(ghost_theme)

    def update_ss_status(self, status_info):
        """Update Syntax Supervisors status display."""
        if hasattr(self, 'ss_status_label'):
            status_text = "🔍 SS: {status_info.get('active', 0)} active"
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
=======
>>>>>>> e5d859f2d87d98897ba379404835c6c543a0ff8a
