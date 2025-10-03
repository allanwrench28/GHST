"""
GHST Main Window - AI Coding Engine Interface

Modern interface for AI-assisted coding, debugging, and problem solving.
"""

import sys
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QFont, QColor, QPalette
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
    QScrollArea,
    QFrame,
    QGraphicsOpacityEffect,
)

try:
    from .code_block_widget import CodeBlockWidget
except ImportError:
    # Fallback if code_block_widget is not available
    CodeBlockWidget = None


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
        
        # Add fade-in animation
        self.fade_in_animation()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("GHST - AI Coding Engine")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1000, 600)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create splitter for resizable panes
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Create panes
        left_pane = self.create_left_pane()
        center_pane = self.create_center_pane()
        right_pane = self.create_right_pane()

        splitter.addWidget(left_pane)
        splitter.addWidget(center_pane)
        splitter.addWidget(right_pane)

        # Set splitter proportions
        splitter.setStretchFactor(0, 1)  # Left pane
        splitter.setStretchFactor(1, 3)  # Center pane (largest)
        splitter.setStretchFactor(2, 1)  # Right pane

        # Create menu bar
        self.create_menu_bar()

        # Create status bar
        self.create_status_bar()

        # Apply modern styling
        self.apply_modern_styling()

        # Add autocommit ticker to status bar
        self.add_autocommit_ticker()

    def create_left_pane(self):
        """Create left pane with expert agents and tools."""
        from .speedbuild_slider import SpeedbuildSlider
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # SPEEDBUILD section header
        speedbuild_label = QLabel("⚡ SPEEDBUILD Control")
        speedbuild_label.setObjectName("sectionHeader")
        layout.addWidget(speedbuild_label)
        
        self.speedbuild_slider = SpeedbuildSlider()
        layout.addWidget(self.speedbuild_slider)

        # Expert agents section
        experts_label = QLabel("🧠 AI Expert Agents")
        experts_label.setObjectName("sectionHeader")
        layout.addWidget(experts_label)

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
        tools_label = QLabel("🔧 Tools")
        tools_label.setObjectName("sectionHeader")
        layout.addWidget(tools_label)

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
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Tab widget for multiple work areas
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        layout.addWidget(self.tab_widget)

        # Welcome tab
        welcome_tab = self.create_welcome_tab()
        self.tab_widget.addTab(welcome_tab, "🏠 Welcome")

        # Code editor tab
        code_tab = self.create_code_editor_tab()
        self.tab_widget.addTab(code_tab, "📝 Code Editor")

        # Documentation panel tab
        docs_tab = self.create_docs_panel_tab()
        self.tab_widget.addTab(docs_tab, "📚 Documentation")

        return widget

    def create_welcome_tab(self):
        """Create the welcome tab with modern styling."""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content = QWidget()
        content_layout = QVBoxLayout()
        content.setLayout(content_layout)
        content_layout.setSpacing(20)

        welcome_text = QTextEdit()
        welcome_text.setHtml("""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
            <h1 style="color: #00d4ff; margin-bottom: 16px;">🚀 Welcome to GHST</h1>
            <p style="font-size: 16px; color: #b4b4b4; margin-bottom: 24px;">
                Your open-source AI coding assistant with expert agent think tank.
            </p>

            <h2 style="color: #00adb5; margin-top: 24px; margin-bottom: 12px;">✨ Features</h2>
            <ul style="font-size: 15px; line-height: 1.8; color: #d4d4d4;">
                <li><strong style="color: #00d4ff;">AI Collaboration Framework:</strong> Multiple AI experts work together</li>
                <li><strong style="color: #00d4ff;">Plugin System:</strong> Extensible tools and workflows</li>
                <li><strong style="color: #00d4ff;">Configuration Management:</strong> YAML-based settings</li>
                <li><strong style="color: #00d4ff;">Modern UI:</strong> Clean, customizable interface</li>
                <li><strong style="color: #00d4ff;">Developer Tools:</strong> Built-in automation and utilities</li>
            </ul>

            <h2 style="color: #00adb5; margin-top: 24px; margin-bottom: 12px;">🎯 Getting Started</h2>
            <ol style="font-size: 15px; line-height: 1.8; color: #d4d4d4;">
                <li>Select an AI expert from the left panel</li>
                <li>Open or create a project using File menu</li>
                <li>Get AI assistance with coding, debugging, and problem solving</li>
            </ol>

            <p style="font-size: 14px; color: #888; margin-top: 24px; font-style: italic;">
                Remember: You maintain full control. All AI recommendations require your validation.
            </p>
        </div>
        """)
        welcome_text.setReadOnly(True)
        content_layout.addWidget(welcome_text)
        content_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

        return tab

    def create_code_editor_tab(self):
        """Create the code editor tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        layout.setContentsMargins(8, 8, 8, 8)

        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText(
            "// Your code here...\n// AI experts are ready to assist!")
        self.code_editor.setFont(QFont("Consolas", 11))
        layout.addWidget(self.code_editor)

        return tab

    def create_docs_panel_tab(self):
        """Create documentation panel tab for markdown/code display."""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        layout.setContentsMargins(8, 8, 8, 8)

        # Toolbar for docs panel
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout()
        toolbar.setLayout(toolbar_layout)
        toolbar_layout.setContentsMargins(0, 0, 0, 8)
        
        toolbar_label = QLabel("📄 Documentation Viewer")
        toolbar_label.setObjectName("sectionHeader")
        toolbar_layout.addWidget(toolbar_label)
        toolbar_layout.addStretch()
        
        # Copy button
        self.docs_copy_btn = QPushButton("📋 Copy")
        self.docs_copy_btn.setObjectName("modernButton")
        self.docs_copy_btn.clicked.connect(self.copy_docs_content)
        toolbar_layout.addWidget(self.docs_copy_btn)
        
        layout.addWidget(toolbar)

        # Documentation display
        self.docs_display = QTextEdit()
        self.docs_display.setReadOnly(True)
        self.docs_display.setFont(QFont("Consolas", 10))
        self.docs_display.setPlaceholderText(
            "Documentation and code snippets will appear here...\n\n" +
            "You can view markdown files, code examples, and API documentation.")
        layout.addWidget(self.docs_display)

        return tab

    def copy_docs_content(self):
        """Copy documentation content to clipboard."""
        from PyQt5.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self.docs_display.toPlainText())
        self.status_bar.showMessage("📋 Content copied to clipboard!", 3000)

    def create_right_pane(self):
        """Create right pane with AI assistance and chat."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # AI Chat header
        chat_header = QLabel("💬 AI Assistant Chat")
        chat_header.setObjectName("sectionHeader")
        layout.addWidget(chat_header)

        # Chat display area with scroll
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setHtml("""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 12px;">
            <div style="background: #1e3a4c; padding: 12px; border-radius: 8px; margin-bottom: 8px;">
                <p style="margin: 0; color: #00d4ff;"><strong>🧠 AI Expert Collective</strong></p>
                <p style="margin: 4px 0 0 0; color: #d4d4d4;">Ready to assist with coding tasks!</p>
            </div>
            <div style="background: #1e3a4c; padding: 12px; border-radius: 8px;">
                <p style="margin: 0; color: #00d4ff;"><strong>💡 Tips</strong></p>
                <p style="margin: 4px 0 0 0; color: #d4d4d4;">Ask questions, request code reviews, or get debugging help.</p>
            </div>
        </div>
        """)
        layout.addWidget(self.chat_display)

        # Chat input with label
        input_label = QLabel("Your Message:")
        input_label.setStyleSheet("color: #b4b4b4; font-size: 12px;")
        layout.addWidget(input_label)

        self.chat_input = QTextEdit()
        self.chat_input.setMaximumHeight(80)
        self.chat_input.setPlaceholderText("Ask the AI experts anything...")
        self.chat_input.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.chat_input)

        # Send button with modern styling
        send_button = QPushButton("📤 Send to Experts")
        send_button.setObjectName("primaryButton")
        send_button.clicked.connect(self.send_chat_message)
        send_button.setMinimumHeight(40)
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

    def apply_modern_styling(self):
        """Apply modern iOS-inspired styling to the interface."""
        self.setStyleSheet("""
            /* Main Window - Dark theme with modern palette */
            QMainWindow {
                background-color: #0d1117;
                color: #e6edf3;
            }
            
            /* Modern Widget styling */
            QWidget {
                background-color: #0d1117;
                color: #e6edf3;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
                font-size: 13px;
            }
            
            /* Section Headers */
            QLabel#sectionHeader {
                color: #00d4ff;
                font-size: 14px;
                font-weight: 600;
                padding: 8px 0 4px 0;
                border: none;
            }
            
            /* Standard Labels */
            QLabel {
                color: #e6edf3;
                padding: 2px;
            }
            
            /* List Widgets - Modern cards */
            QListWidget {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 8px;
                outline: none;
                font-size: 13px;
            }
            
            QListWidget::item {
                padding: 10px;
                border-radius: 6px;
                margin: 2px 0;
            }
            
            QListWidget::item:hover {
                background-color: #1c2128;
            }
            
            QListWidget::item:selected {
                background-color: #1f6feb;
                color: #ffffff;
            }
            
            /* Text Edit - Code editor style */
            QTextEdit {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 12px;
                color: #e6edf3;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 13px;
                selection-background-color: #1f6feb;
                selection-color: #ffffff;
            }
            
            QTextEdit:focus {
                border: 1px solid #1f6feb;
            }
            
            /* Scroll Areas */
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            
            /* Scroll Bars - Modern thin style */
            QScrollBar:vertical {
                background-color: #0d1117;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #30363d;
                border-radius: 6px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #484f58;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar:horizontal {
                background-color: #0d1117;
                height: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:horizontal {
                background-color: #30363d;
                border-radius: 6px;
                min-width: 30px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background-color: #484f58;
            }
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            
            /* Primary Buttons - Vibrant style */
            QPushButton#primaryButton {
                background-color: #1f6feb;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
            }
            
            QPushButton#primaryButton:hover {
                background-color: #388bfd;
            }
            
            QPushButton#primaryButton:pressed {
                background-color: #1a5fdc;
            }
            
            /* Modern Buttons */
            QPushButton#modernButton {
                background-color: #21262d;
                color: #e6edf3;
                border: 1px solid #30363d;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 12px;
            }
            
            QPushButton#modernButton:hover {
                background-color: #30363d;
                border-color: #484f58;
            }
            
            QPushButton#modernButton:pressed {
                background-color: #161b22;
            }
            
            /* Standard Buttons */
            QPushButton {
                background-color: #21262d;
                color: #e6edf3;
                border: 1px solid #30363d;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #30363d;
                border-color: #484f58;
            }
            
            QPushButton:pressed {
                background-color: #161b22;
            }
            
            /* Tab Widget - Clean modern tabs */
            QTabWidget::pane {
                border: 1px solid #30363d;
                border-radius: 8px;
                background-color: #0d1117;
                top: -1px;
            }
            
            QTabBar::tab {
                background-color: #161b22;
                color: #8b949e;
                padding: 10px 20px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid #30363d;
                border-bottom: none;
                min-width: 100px;
            }
            
            QTabBar::tab:hover {
                background-color: #1c2128;
                color: #e6edf3;
            }
            
            QTabBar::tab:selected {
                background-color: #0d1117;
                color: #00d4ff;
                border-bottom: 2px solid #1f6feb;
                font-weight: 600;
            }
            
            /* Splitter Handle - Subtle dividers */
            QSplitter::handle {
                background-color: #21262d;
                width: 1px;
                height: 1px;
            }
            
            QSplitter::handle:hover {
                background-color: #30363d;
            }
            
            /* Menu Bar - Clean modern style */
            QMenuBar {
                background-color: #161b22;
                color: #e6edf3;
                padding: 4px;
                border-bottom: 1px solid #30363d;
            }
            
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                border-radius: 4px;
            }
            
            QMenuBar::item:selected {
                background-color: #1c2128;
            }
            
            QMenuBar::item:pressed {
                background-color: #30363d;
            }
            
            /* Menu - Modern dropdown */
            QMenu {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 4px;
            }
            
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
            }
            
            QMenu::item:selected {
                background-color: #1c2128;
            }
            
            /* Status Bar */
            QStatusBar {
                background-color: #161b22;
                color: #8b949e;
                border-top: 1px solid #30363d;
            }
            
            QStatusBar::item {
                border: none;
            }
        """)

    def send_chat_message(self):
        """Handle sending chat message to AI experts with modern formatting."""
        message = self.chat_input.toPlainText().strip()
        if message:
            # Add user message with modern styling
            self.chat_display.append(f"""
            <div style="background: #1c2128; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 3px solid #1f6feb;">
                <p style="margin: 0; color: #00d4ff; font-weight: 600;">👤 You</p>
                <p style="margin: 4px 0 0 0; color: #e6edf3;">{message}</p>
            </div>
            """)
            self.chat_input.clear()

            # Simulate AI response with code block example
            self.chat_display.append(f"""
            <div style="background: #1e3a4c; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 3px solid #00d4ff;">
                <p style="margin: 0; color: #00d4ff; font-weight: 600;">🧠 AI Expert Collective</p>
                <p style="margin: 4px 0 0 0; color: #e6edf3;">I understand your request. Let me analyze this and provide assistance...</p>
            </div>
            """)
            
            # Show example code response
            self.show_code_example()
            
            # Show status message
            self.status_bar.showMessage("💬 Message sent to AI experts", 3000)
    
    def show_code_example(self):
        """Show an example code block in the chat (demo functionality)."""
        example_code = """def process_code(input_text):
    \"\"\"Process and analyze code input.\"\"\"
    # AI expert analysis
    lines = input_text.split('\\n')
    analysis = {
        'lines': len(lines),
        'complexity': calculate_complexity(lines)
    }
    return analysis"""
        
        self.chat_display.append(f"""
        <div style="background: #161b22; padding: 12px; border-radius: 8px; margin: 8px 0; border: 1px solid #30363d;">
            <div style="background: #1c2128; padding: 8px 12px; border-radius: 6px 6px 0 0; border-bottom: 1px solid #30363d; margin: -12px -12px 8px -12px;">
                <span style="color: #8b949e; font-size: 11px; font-weight: 600; text-transform: uppercase;">📄 PYTHON</span>
                <span style="float: right; color: #8b949e; font-size: 11px; cursor: pointer;">📋 Copy</span>
            </div>
            <pre style="margin: 0; color: #e6edf3; font-family: 'Consolas', 'Monaco', monospace; font-size: 12px; line-height: 1.5; white-space: pre-wrap;">{example_code}</pre>
        </div>
        """)

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
    
    def fade_in_animation(self):
        """Add a smooth fade-in animation when the window appears."""
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(400)  # 400ms
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_animation.start()
    
    def add_button_hover_animation(self, button):
        """Add hover animation to a button."""
        # This would typically be done with CSS animations in the stylesheet
        # The hover effects are already defined in apply_modern_styling()
        pass


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for consistent cross-platform look
    window = GHSTWindow()
    window.show()
    sys.exit(app.exec_())
