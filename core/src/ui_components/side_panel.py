"""
Side Panel Component for Markdown and Code Display

A Grok-inspired side panel for displaying documentation and code.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QPushButton, QLabel, QTabWidget, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class SidePanel(QWidget):
    """A collapsible side panel for markdown and code display."""
    
    closed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_collapsed = False
        self.init_ui()
        
    def init_ui(self):
        """Initialize the side panel UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with close button
        header = QWidget()
        header.setFixedHeight(44)
        header.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border-bottom: 1px solid #3a3a3a;
            }
        """)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(16, 0, 12, 0)
        header.setLayout(header_layout)
        
        # Title
        title = QLabel("📄 Documentation")
        title.setStyleSheet("""
            QLabel {
                color: #e8e8e8;
                font-weight: 600;
                font-size: 14px;
                background: transparent;
                border: none;
            }
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(32, 32)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #999999;
                border: none;
                border-radius: 16px;
                font-size: 24px;
                font-weight: 300;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                color: #e8e8e8;
            }
            QPushButton:pressed {
                background-color: #4a4a4a;
            }
        """)
        close_btn.clicked.connect(self.close_panel)
        header_layout.addWidget(close_btn)
        
        layout.addWidget(header)
        
        # Tab widget for different views
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background-color: #252525;
                color: #999999;
                padding: 10px 16px;
                margin-right: 0;
                border: none;
                font-weight: 500;
                font-size: 12px;
            }
            QTabBar::tab:hover {
                background-color: #2a2a2a;
                color: #e8e8e8;
            }
            QTabBar::tab:selected {
                background-color: #1e1e1e;
                color: #0a84ff;
                border-bottom: 2px solid #0a84ff;
            }
        """)
        
        # Markdown view
        self.markdown_view = QTextEdit()
        self.markdown_view.setReadOnly(True)
        self.markdown_view.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #e8e8e8;
                border: none;
                padding: 16px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        self.tab_widget.addTab(self.markdown_view, "Markdown")
        
        # Code view
        self.code_view = QTextEdit()
        self.code_view.setReadOnly(True)
        self.code_view.setFont(QFont("SF Mono", 12))
        self.code_view.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
                padding: 16px;
                font-family: 'SF Mono', 'Monaco', 'Menlo', 'Consolas', monospace;
                font-size: 13px;
                line-height: 1.5;
            }
        """)
        self.tab_widget.addTab(self.code_view, "Code")
        
        layout.addWidget(self.tab_widget)
        
        self.setLayout(layout)
        self.setMinimumWidth(300)
        self.setMaximumWidth(600)
        
    def set_markdown(self, markdown_text):
        """Set markdown content."""
        self.markdown_view.setHtml(markdown_text)
        
    def set_code(self, code_text):
        """Set code content."""
        self.code_view.setPlainText(code_text)
        
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
