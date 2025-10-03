"""
Code Display Component with Copy Button

A polished code display widget with syntax highlighting and copy functionality.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QPushButton, QLabel, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class CodeDisplayBox(QWidget):
    """A code display box with copy button and title."""
    
    def __init__(self, title="Code", parent=None):
        super().__init__(parent)
        self.title = title
        self.init_ui()
        
    def init_ui(self):
        """Initialize the code display UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with title and copy button
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid #3a3a3a;
                border-bottom: none;
            }
        """)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(12, 8, 12, 8)
        header.setLayout(header_layout)
        
        # Title label
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            QLabel {
                color: #999999;
                font-weight: 600;
                font-size: 12px;
                border: none;
                background: transparent;
            }
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Copy button
        self.copy_btn = QPushButton("📋 Copy")
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #e8e8e8;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 500;
                min-height: 24px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                border-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
        """)
        self.copy_btn.clicked.connect(self.copy_code)
        header_layout.addWidget(self.copy_btn)
        
        layout.addWidget(header)
        
        # Code display area
        self.code_edit = QTextEdit()
        self.code_edit.setReadOnly(True)
        self.code_edit.setFont(QFont("SF Mono", 12))
        self.code_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3a3a3a;
                border-top: none;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                padding: 12px;
                font-family: 'SF Mono', 'Monaco', 'Menlo', 'Consolas', monospace;
                font-size: 13px;
                line-height: 1.5;
            }
        """)
        
        layout.addWidget(self.code_edit)
        self.setLayout(layout)
        
    def set_code(self, code):
        """Set the code content."""
        self.code_edit.setPlainText(code)
        
    def copy_code(self):
        """Copy code to clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code_edit.toPlainText())
        
        # Visual feedback
        original_text = self.copy_btn.text()
        self.copy_btn.setText("✓ Copied!")
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #0a84ff;
                color: white;
                border: 1px solid #0a84ff;
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 500;
                min-height: 24px;
            }
        """)
        
        # Reset after 2 seconds
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self.reset_copy_button(original_text))
        
    def reset_copy_button(self, original_text):
        """Reset copy button to original state."""
        self.copy_btn.setText(original_text)
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #e8e8e8;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 500;
                min-height: 24px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                border-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
        """)
