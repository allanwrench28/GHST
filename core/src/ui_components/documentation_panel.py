"""
Documentation Panel with File and Markdown Viewer

Grok-style side panel for displaying documentation, code files, and markdown.
Supports tabbed interface with smooth transitions.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QTabWidget, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

from .styles.modern_theme import COLORS, FONTS
from .code_block_widget import PythonSyntaxHighlighter


class DocumentationPanel(QWidget):
    """
    Side panel for documentation and file viewing.
    
    Features:
    - Tabbed interface (Markdown/Code/Files)
    - Syntax highlighting for code
    - Markdown rendering
    - Collapsible design
    - Close button
    """
    
    closed = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize documentation panel."""
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the panel UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with title and close button
        header = QWidget()
        header.setFixedHeight(48)
        header.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS.BACKGROUND_TERTIARY};
                border-bottom: 1px solid {COLORS.BORDER};
            }}
        """)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(16, 0, 12, 0)
        header.setLayout(header_layout)
        
        # Title
        title = QLabel("📄 Documentation")
        title.setStyleSheet(f"""
            QLabel {{
                color: {COLORS.TEXT_PRIMARY};
                font-weight: {FONTS.WEIGHT_SEMIBOLD};
                font-size: {FONTS.SIZE_MEDIUM};
                background: transparent;
                border: none;
                font-family: {FONTS.SYSTEM};
            }}
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(36, 36)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS.TEXT_SECONDARY};
                border: none;
                border-radius: 18px;
                font-size: 28px;
                font-weight: 300;
                padding: 0;
            }}
            QPushButton:hover {{
                background-color: {COLORS.BACKGROUND_SECONDARY};
                color: {COLORS.TEXT_PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: {COLORS.BORDER};
            }}
        """)
        close_btn.clicked.connect(self.close_panel)
        header_layout.addWidget(close_btn)
        
        layout.addWidget(header)
        
        # Tab widget for different content types
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {COLORS.BACKGROUND};
            }}
            QTabBar::tab {{
                background-color: {COLORS.BACKGROUND_SECONDARY};
                color: {COLORS.TEXT_SECONDARY};
                padding: 10px 20px;
                margin-right: 0;
                border: none;
                font-weight: {FONTS.WEIGHT_MEDIUM};
                font-size: {FONTS.SIZE_BASE};
                font-family: {FONTS.SYSTEM};
            }}
            QTabBar::tab:hover {{
                background-color: {COLORS.BACKGROUND_TERTIARY};
                color: {COLORS.TEXT_PRIMARY};
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS.BACKGROUND};
                color: {COLORS.ACCENT_BLUE};
                border-bottom: 2px solid {COLORS.ACCENT_BLUE};
            }}
        """)
        
        # Markdown/HTML view
        self.markdown_view = QTextEdit()
        self.markdown_view.setReadOnly(True)
        self.markdown_view.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS.BACKGROUND};
                color: {COLORS.TEXT_PRIMARY};
                border: none;
                padding: 16px;
                font-family: {FONTS.SYSTEM};
                font-size: {FONTS.SIZE_MEDIUM};
                line-height: 1.6;
                selection-background-color: {COLORS.ACCENT_BLUE};
            }}
        """)
        self.tab_widget.addTab(self.markdown_view, "📖 Documentation")
        
        # Code view with syntax highlighting
        self.code_view = QTextEdit()
        self.code_view.setReadOnly(True)
        self.code_view.setFont(QFont(FONTS.MONOSPACE.split(',')[0].strip("'"), 13))
        self.code_view.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS.CODE_BG};
                color: {COLORS.TEXT_PRIMARY};
                border: none;
                padding: 16px;
                font-family: {FONTS.MONOSPACE};
                font-size: {FONTS.SIZE_BASE};
                line-height: 1.6;
                selection-background-color: {COLORS.ACCENT_BLUE};
            }}
        """)
        
        # Apply Python syntax highlighting to code view
        self.code_highlighter = PythonSyntaxHighlighter(self.code_view.document())
        
        self.tab_widget.addTab(self.code_view, "💻 Code")
        
        # File browser/info view
        self.file_view = QTextEdit()
        self.file_view.setReadOnly(True)
        self.file_view.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS.BACKGROUND};
                color: {COLORS.TEXT_PRIMARY};
                border: none;
                padding: 16px;
                font-family: {FONTS.MONOSPACE};
                font-size: {FONTS.SIZE_SMALL};
                line-height: 1.4;
                selection-background-color: {COLORS.ACCENT_BLUE};
            }}
        """)
        self.tab_widget.addTab(self.file_view, "📁 Files")
        
        layout.addWidget(self.tab_widget)
        
        self.setLayout(layout)
        self.setMinimumWidth(350)
        self.setMaximumWidth(700)
    
    def set_markdown(self, markdown_text):
        """
        Set markdown/HTML content.
        
        Args:
            markdown_text: HTML or markdown text to display
        """
        self.markdown_view.setHtml(markdown_text)
        self.tab_widget.setCurrentIndex(0)
    
    def set_code(self, code_text, language="Python"):
        """
        Set code content with syntax highlighting.
        
        Args:
            code_text: Code to display
            language: Programming language (default: Python)
        """
        self.code_view.setPlainText(code_text)
        self.tab_widget.setCurrentIndex(1)
    
    def set_file_info(self, file_info):
        """
        Set file information/listing.
        
        Args:
            file_info: File information text
        """
        self.file_view.setPlainText(file_info)
        self.tab_widget.setCurrentIndex(2)
    
    def load_documentation(self, doc_content):
        """
        Load documentation content (auto-detects type).
        
        Args:
            doc_content: Dictionary with 'type' and 'content' keys
        """
        doc_type = doc_content.get('type', 'markdown')
        content = doc_content.get('content', '')
        
        if doc_type == 'markdown' or doc_type == 'html':
            self.set_markdown(content)
        elif doc_type == 'code':
            language = doc_content.get('language', 'Python')
            self.set_code(content, language)
        elif doc_type == 'file':
            self.set_file_info(content)
    
    def close_panel(self):
        """Close/hide the panel."""
        self.closed.emit()
        self.hide()
    
    def show_markdown_tab(self):
        """Switch to markdown tab."""
        self.tab_widget.setCurrentIndex(0)
    
    def show_code_tab(self):
        """Switch to code tab."""
        self.tab_widget.setCurrentIndex(1)
    
    def show_file_tab(self):
        """Switch to file tab."""
        self.tab_widget.setCurrentIndex(2)
    
    def get_current_tab(self):
        """
        Get current tab index.
        
        Returns:
            Current tab index
        """
        return self.tab_widget.currentIndex()
    
    def clear_all(self):
        """Clear all content from all tabs."""
        self.markdown_view.clear()
        self.code_view.clear()
        self.file_view.clear()
