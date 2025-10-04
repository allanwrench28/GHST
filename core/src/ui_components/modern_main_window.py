"""
Modern Main Window - Complete UI Modernization

Production-quality main window with ChatGPT/Grok-style interface.
Features smooth animations, modern design, and comprehensive component integration.
"""

import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QLabel, QListWidget, QPushButton,
    QTabWidget, QFrame, QStatusBar, QMessageBox,
    QApplication
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from .styles.modern_theme import ModernTheme, COLORS, FONTS
from .styles.animations import AnimationHelper, FadeAnimation
from .chat_interface import ChatInterface
from .code_block_widget import CodeBlockWidget
from .documentation_panel import DocumentationPanel
from .loading_animations import LoadingSpinner, InlineSpinner
from .speedbuild_slider import SpeedbuildSlider


class ModernMainWindow(QMainWindow):
    """
    Modern main window for GHST AI Coding Engine.
    
    Features:
    - Three-pane layout (Controls | Workspace | Chat)
    - GitHub Dark theme with proper contrast
    - Smooth 400ms fade-in animation
    - Modern message bubbles for chat
    - Code blocks with syntax highlighting
    - Collapsible documentation panel
    - Professional button styling
    - Custom scrollbars
    
    Architecture:
    - Left pane: Expert selection, tools, SPEEDBUILD control
    - Center pane: Tabbed workspace (Welcome, Code Editor, Documentation)
    - Right pane: AI chat with modern bubbles
    - Side panel: Documentation viewer (toggleable)
    """
    
    def __init__(self):
        """Initialize the modern main window."""
        super().__init__()
        self.expert_manager = None
        self.config_manager = None
        
        # Apply theme first
        self.setStyleSheet(ModernTheme.get_complete_stylesheet())
        
        # Initialize UI
        self.init_ui()
        
        # Apply fade-in animation (400ms)
        self.fade_animation = FadeAnimation(self, 400)
        self.fade_animation.set_opacity(0.0)
        QTimer.singleShot(50, self.fade_animation.fade_in)
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("GHST - AI Coding Engine")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        
        # Create main splitter for three-pane layout
        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)
        
        # Left pane - Controls and expert selection
        left_pane = self.create_left_pane()
        self.main_splitter.addWidget(left_pane)
        
        # Center pane - Main workspace
        center_pane = self.create_center_pane()
        self.main_splitter.addWidget(center_pane)
        
        # Right pane - AI chat interface
        right_pane = self.create_right_pane()
        self.main_splitter.addWidget(right_pane)
        
        # Documentation side panel (initially hidden)
        self.doc_panel = DocumentationPanel()
        self.doc_panel.hide()
        self.doc_panel.closed.connect(self.on_doc_panel_closed)
        self.main_splitter.addWidget(self.doc_panel)
        
        # Set splitter proportions (1:3:1.2 ratio)
        self.main_splitter.setStretchFactor(0, 1)    # Left: 1
        self.main_splitter.setStretchFactor(1, 3)    # Center: 3 (largest)
        self.main_splitter.setStretchFactor(2, 1)    # Right: 1.2
        self.main_splitter.setStretchFactor(3, 1)    # Doc panel: 1
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.create_status_bar()
    
    def create_left_pane(self):
        """Create left pane with expert selection and controls."""
        widget = QWidget()
        widget.setMaximumWidth(320)
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(20)
        widget.setLayout(layout)
        
        # SPEEDBUILD Control
        speedbuild_label = QLabel("⚡ SPEEDBUILD")
        speedbuild_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS.ACCENT_BLUE};
                font-size: {FONTS.SIZE_LARGE};
                font-weight: {FONTS.WEIGHT_SEMIBOLD};
                padding: 8px 0;
                font-family: {FONTS.SYSTEM};
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(speedbuild_label)
        
        self.speedbuild_slider = SpeedbuildSlider()
        layout.addWidget(self.speedbuild_slider)
        
        # Separator
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setStyleSheet(f"background-color: {COLORS.BORDER}; max-height: 1px;")
        layout.addWidget(separator1)
        
        # AI Experts section
        experts_label = QLabel("🧠 AI Experts")
        experts_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS.ACCENT_BLUE};
                font-size: {FONTS.SIZE_LARGE};
                font-weight: {FONTS.WEIGHT_SEMIBOLD};
                padding: 8px 0;
                font-family: {FONTS.SYSTEM};
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(experts_label)
        
        self.experts_list = QListWidget()
        self.experts_list.addItems([
            "🔍 Code Analysis",
            "🐛 Debugging Expert",
            "🛠️ Problem Solving",
            "📚 Research Specialist",
            "⚡ Performance Optimizer",
            "🔒 Security Auditor",
            "📝 Documentation Writer",
            "🧪 Testing Engineer",
            "🏗️ Architecture Designer",
            "🎨 UI/UX Specialist",
            "🚀 DevOps Engineer",
            "📊 Data Scientist"
        ])
        self.experts_list.setMaximumHeight(320)
        layout.addWidget(self.experts_list)
        
        # Separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setStyleSheet(f"background-color: {COLORS.BORDER}; max-height: 1px;")
        layout.addWidget(separator2)
        
        # Tools section
        tools_label = QLabel("🔧 Tools")
        tools_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS.ACCENT_BLUE};
                font-size: {FONTS.SIZE_LARGE};
                font-weight: {FONTS.WEIGHT_SEMIBOLD};
                padding: 8px 0;
                font-family: {FONTS.SYSTEM};
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(tools_label)
        
        self.tools_list = QListWidget()
        self.tools_list.addItems([
            "📦 Plugin Manager",
            "⚙️ Settings",
            "📋 Templates",
            "✂️ Code Snippets"
        ])
        layout.addWidget(self.tools_list)
        
        layout.addStretch()
        
        # Documentation button
        docs_btn = QPushButton("📄 View Documentation")
        docs_btn.clicked.connect(self.toggle_documentation_panel)
        layout.addWidget(docs_btn)
        
        return widget
    
    def create_center_pane(self):
        """Create center pane with tabbed workspace."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        widget.setLayout(layout)
        
        # Tab widget for workspace
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        layout.addWidget(self.tab_widget)
        
        # Welcome tab
        welcome_tab = self.create_welcome_tab()
        self.tab_widget.addTab(welcome_tab, "🏠 Welcome")
        
        # Code editor tab
        code_tab = self.create_code_editor_tab()
        self.tab_widget.addTab(code_tab, "💻 Code Editor")
        
        # Documentation tab
        docs_tab = self.create_documentation_tab()
        self.tab_widget.addTab(docs_tab, "📚 Documentation")
        
        return widget
    
    def create_welcome_tab(self):
        """Create welcome tab with introduction."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        widget.setLayout(layout)
        
        # Welcome content
        welcome_html = f"""
        <div style="font-family: {FONTS.SYSTEM}; color: {COLORS.TEXT_PRIMARY};">
            <h1 style="color: {COLORS.ACCENT_BLUE}; font-weight: 700; font-size: 36px; margin-bottom: 16px;">
                🚀 Welcome to GHST
            </h1>
            <h2 style="color: {COLORS.TEXT_SECONDARY}; font-weight: 400; font-size: 18px; margin-bottom: 32px;">
                Your AI Coding Engine with Expert Agent Think Tank
            </h2>
            
            <h3 style="color: {COLORS.TEXT_PRIMARY}; font-weight: 600; font-size: 20px; margin-top: 32px; margin-bottom: 16px;">
                ✨ Features
            </h3>
            <ul style="line-height: 2.0; font-size: 15px; margin-left: 20px;">
                <li><strong style="color: {COLORS.ACCENT_BLUE};">AI Collaboration Framework:</strong> Multiple AI experts work together seamlessly</li>
                <li><strong style="color: {COLORS.ACCENT_CYAN};">Modern UI:</strong> ChatGPT/Grok-inspired interface with smooth animations</li>
                <li><strong style="color: {COLORS.ACCENT_GREEN};">Plugin System:</strong> Extensible architecture for any workflow</li>
                <li><strong style="color: {COLORS.ACCENT_PURPLE};">Syntax Highlighting:</strong> Beautiful Python code display with copy buttons</li>
                <li><strong style="color: {COLORS.ACCENT_YELLOW};">Real-time Chat:</strong> Instant communication with AI experts</li>
            </ul>
            
            <h3 style="color: {COLORS.TEXT_PRIMARY}; font-weight: 600; font-size: 20px; margin-top: 32px; margin-bottom: 16px;">
                🎯 Getting Started
            </h3>
            <ol style="line-height: 2.0; font-size: 15px; margin-left: 20px;">
                <li>Select an AI expert from the left panel</li>
                <li>Start a conversation in the chat interface</li>
                <li>Use the code editor for development</li>
                <li>Access documentation anytime</li>
            </ol>
            
            <div style="margin-top: 40px; padding: 20px; background-color: {COLORS.BACKGROUND_TERTIARY}; 
                        border-left: 4px solid {COLORS.ACCENT_BLUE}; border-radius: 8px;">
                <p style="margin: 0; font-size: 14px; line-height: 1.6;">
                    <strong style="color: {COLORS.ACCENT_BLUE};">💡 Pro Tip:</strong>
                    <em style="color: {COLORS.TEXT_SECONDARY};">
                        You maintain full control. All AI recommendations require your validation.
                    </em>
                </p>
            </div>
        </div>
        """
        
        from PyQt5.QtWidgets import QTextBrowser
        welcome_text = QTextBrowser()
        welcome_text.setHtml(welcome_html)
        welcome_text.setReadOnly(True)
        welcome_text.setOpenExternalLinks(True)
        layout.addWidget(welcome_text)
        
        return widget
    
    def create_code_editor_tab(self):
        """Create code editor tab with syntax highlighting."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        widget.setLayout(layout)
        
        # Code block widget
        self.code_editor = CodeBlockWidget("Python")
        self.code_editor.set_code("""# Welcome to GHST Code Editor
# AI-powered coding assistance

def greet():
    \"\"\"Greet the GHST user.\"\"\"
    print("Hello from GHST!")
    print("Let's build something amazing together! 🚀")

class AIAssistant:
    \"\"\"AI coding assistant.\"\"\"
    
    def __init__(self, name):
        self.name = name
        self.expertise = ["debugging", "optimization", "architecture"]
    
    def help(self, task):
        \"\"\"Provide AI assistance.\"\"\"
        return f"{self.name} is ready to help with {task}!"

# Get started with AI assistance
if __name__ == "__main__":
    greet()
    assistant = AIAssistant("GHST Expert")
    print(assistant.help("your project"))
""")
        layout.addWidget(self.code_editor)
        
        return widget
    
    def create_documentation_tab(self):
        """Create documentation tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        widget.setLayout(layout)
        
        # Documentation content
        from PyQt5.QtWidgets import QTextBrowser
        docs_browser = QTextBrowser()
        docs_browser.setHtml(f"""
        <div style="font-family: {FONTS.SYSTEM}; color: {COLORS.TEXT_PRIMARY};">
            <h1 style="color: {COLORS.ACCENT_BLUE};">📚 GHST Documentation</h1>
            <p style="font-size: 15px; line-height: 1.8;">
                Welcome to the GHST documentation. Here you'll find comprehensive guides
                for using the AI coding engine effectively.
            </p>
            
            <h2 style="color: {COLORS.ACCENT_CYAN}; margin-top: 24px;">Quick Links</h2>
            <ul style="line-height: 2.0;">
                <li><a href="#" style="color: {COLORS.ACCENT_BLUE};">Getting Started Guide</a></li>
                <li><a href="#" style="color: {COLORS.ACCENT_BLUE};">AI Experts Overview</a></li>
                <li><a href="#" style="color: {COLORS.ACCENT_BLUE};">Plugin Development</a></li>
                <li><a href="#" style="color: {COLORS.ACCENT_BLUE};">Configuration Guide</a></li>
            </ul>
        </div>
        """)
        docs_browser.setOpenExternalLinks(False)
        layout.addWidget(docs_browser)
        
        return widget
    
    def create_right_pane(self):
        """Create right pane with chat interface."""
        widget = QWidget()
        widget.setMaximumWidth(400)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 16, 16, 16)
        widget.setLayout(layout)
        
        # Modern chat interface
        self.chat_interface = ChatInterface()
        self.chat_interface.message_sent.connect(self.handle_chat_message)
        layout.addWidget(self.chat_interface)
        
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
        view_menu.addAction('📄 Toggle Documentation', self.toggle_documentation_panel)
        view_menu.addAction('🎨 Theme Settings', self.show_theme_settings)
        
        # AI menu
        ai_menu = menubar.addMenu('🧠 AI Experts')
        ai_menu.addAction('📊 Expert Status', self.show_expert_status)
        ai_menu.addAction('⚙️ Configure Experts', self.configure_experts)
        
        # Tools menu
        tools_menu = menubar.addMenu('🔧 Tools')
        tools_menu.addAction('📦 Plugin Manager', self.open_plugin_manager)
        tools_menu.addAction('⚙️ Settings', self.open_settings)
        
        # Help menu
        help_menu = menubar.addMenu('❓ Help')
        help_menu.addAction('ℹ️ About GHST', self.show_about)
        help_menu.addAction('📖 Documentation', self.show_documentation)
    
    def create_status_bar(self):
        """Create application status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("✅ GHST AI Coding Engine - Ready")
        
        # Add status widgets
        self.status_label = QLabel("🟢 Connected")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS.TEXT_SECONDARY};
                font-size: {FONTS.SIZE_SMALL};
                padding: 0 12px;
                font-family: {FONTS.SYSTEM};
            }}
        """)
        self.status_bar.addPermanentWidget(self.status_label)
    
    # Event handlers and utility methods
    
    def handle_chat_message(self, message):
        """Handle chat message from user."""
        # This would connect to actual AI processing
        # For now, it's handled by the chat interface itself
        pass
    
    def toggle_documentation_panel(self):
        """Toggle the documentation side panel."""
        if self.doc_panel.isVisible():
            self.doc_panel.hide()
        else:
            self.doc_panel.show()
            # Set example documentation
            self.doc_panel.set_markdown(f"""
                <div style="font-family: {FONTS.SYSTEM}; color: {COLORS.TEXT_PRIMARY};">
                <h2 style="color: {COLORS.ACCENT_BLUE};">GHST Documentation</h2>
                <p>Welcome to the GHST documentation panel!</p>
                <h3 style="color: {COLORS.ACCENT_CYAN};">Features</h3>
                <ul>
                    <li>Modern UI with GitHub Dark theme</li>
                    <li>AI-powered coding assistance</li>
                    <li>Real-time collaboration</li>
                    <li>Extensible plugin system</li>
                </ul>
                </div>
            """)
    
    def on_doc_panel_closed(self):
        """Handle documentation panel close event."""
        pass  # Panel hides itself
    
    def new_project(self):
        """Create new project."""
        QMessageBox.information(self, "New Project", 
                                "New project functionality coming soon!")
    
    def open_project(self):
        """Open existing project."""
        QMessageBox.information(self, "Open Project",
                                "Open project functionality coming soon!")
    
    def show_theme_settings(self):
        """Show theme settings dialog."""
        QMessageBox.information(self, "Theme Settings",
                                "Theme customization coming soon!")
    
    def show_expert_status(self):
        """Show AI expert status."""
        QMessageBox.information(self, "Expert Status",
                                "12 AI experts active and ready to assist!")
    
    def configure_experts(self):
        """Configure AI experts."""
        QMessageBox.information(self, "Configure Experts",
                                "Expert configuration coming soon!")
    
    def open_plugin_manager(self):
        """Open plugin manager."""
        QMessageBox.information(self, "Plugin Manager",
                                "Plugin management coming soon!")
    
    def open_settings(self):
        """Open settings dialog."""
        from .settings_dialog import SettingsDialog
        dialog = SettingsDialog(self)
        dialog.exec_()
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About GHST",
            "<h2>GHST - AI Coding Engine</h2>"
            "<p><b>Version:</b> 2.0.0-modern</p>"
            "<p><b>License:</b> MIT</p>"
            "<p>Open-source AI-powered coding assistant with modern interface.</p>"
            "<p>Features ChatGPT/Grok-style design with smooth animations.</p>"
            "<p><i>Built with PyQt5 and love for clean code.</i></p>"
        )
    
    def show_documentation(self):
        """Show documentation."""
        self.tab_widget.setCurrentIndex(2)  # Switch to documentation tab


def main():
    """Main entry point for testing."""
    app = QApplication(sys.argv)
    window = ModernMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
