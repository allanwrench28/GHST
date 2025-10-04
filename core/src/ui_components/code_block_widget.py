"""
Code Block Widget with Python Syntax Highlighting

Production-quality code display with syntax highlighting and copy functionality.
Supports Python syntax with proper keyword, string, and comment highlighting.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QApplication
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QTextCharFormat, QColor, QSyntaxHighlighter, QTextDocument

from .styles.modern_theme import COLORS, FONTS


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """
    Python syntax highlighter.
    
    Highlights Python keywords, strings, comments, and numbers with proper colors.
    """
    
    def __init__(self, document: QTextDocument):
        """Initialize the highlighter."""
        super().__init__(document)
        
        # Define highlighting rules
        self.highlighting_rules = []
        
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(COLORS.SYNTAX_KEYWORD))
        keyword_format.setFontWeight(QFont.Bold)
        
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'None', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
            'True', 'try', 'while', 'with', 'yield', 'async', 'await'
        ]
        
        for keyword in keywords:
            self.highlighting_rules.append((
                f'\\b{keyword}\\b',
                keyword_format
            ))
        
        # Built-in functions
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor(COLORS.SYNTAX_FUNCTION))
        
        builtins = [
            'print', 'len', 'range', 'str', 'int', 'float', 'list',
            'dict', 'set', 'tuple', 'bool', 'open', 'input', 'super',
            'isinstance', 'type', 'hasattr', 'getattr', 'setattr'
        ]
        
        for builtin in builtins:
            self.highlighting_rules.append((
                f'\\b{builtin}\\b',
                builtin_format
            ))
        
        # Strings (double and single quotes)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(COLORS.SYNTAX_STRING))
        self.highlighting_rules.append(('"[^"\\\\]*(\\\\.[^"\\\\]*)*"', string_format))
        self.highlighting_rules.append(("'[^'\\\\]*(\\\\.[^'\\\\]*)*'", string_format))
        
        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(COLORS.SYNTAX_NUMBER))
        self.highlighting_rules.append((r'\b\d+\.?\d*\b', number_format))
        
        # Comments
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(COLORS.SYNTAX_COMMENT))
        self.comment_format.setFontItalic(True)
        
        # Decorators
        decorator_format = QTextCharFormat()
        decorator_format.setForeground(QColor(COLORS.ACCENT_YELLOW))
        self.highlighting_rules.append((r'@\w+', decorator_format))
    
    def highlightBlock(self, text):
        """Highlight a block of text."""
        import re
        
        # Apply highlighting rules
        for pattern, format_type in self.highlighting_rules:
            for match in re.finditer(pattern, text):
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, format_type)
        
        # Handle comments (must be done last to override other highlighting)
        comment_index = text.find('#')
        if comment_index >= 0:
            self.setFormat(comment_index, len(text) - comment_index, self.comment_format)


class CodeBlockWidget(QWidget):
    """
    Modern code block widget with syntax highlighting and copy button.
    
    Features:
    - Python syntax highlighting
    - Copy button with visual feedback
    - Language label
    - Rounded corners and proper styling
    - Monospace typography
    """
    
    def __init__(self, title="Python", parent=None):
        """
        Initialize code block widget.
        
        Args:
            title: Language label (default: "Python")
            parent: Parent widget
        """
        super().__init__(parent)
        self.title = title
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with language label and copy button
        header = QWidget()
        header.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS.BACKGROUND_TERTIARY};
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid {COLORS.BORDER};
                border-bottom: none;
            }}
        """)
        header.setFixedHeight(40)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(12, 0, 12, 0)
        header.setLayout(header_layout)
        
        # Language label
        title_label = QLabel(self.title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS.TEXT_SECONDARY};
                font-weight: {FONTS.WEIGHT_SEMIBOLD};
                font-size: {FONTS.SIZE_SMALL};
                border: none;
                background: transparent;
                font-family: {FONTS.SYSTEM};
            }}
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Copy button
        self.copy_btn = QPushButton("📋 Copy")
        self.copy_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS.BACKGROUND_SECONDARY};
                color: {COLORS.TEXT_PRIMARY};
                border: 1px solid {COLORS.BORDER};
                border-radius: 6px;
                padding: 6px 16px;
                font-size: {FONTS.SIZE_SMALL};
                font-weight: {FONTS.WEIGHT_MEDIUM};
                min-height: 28px;
                font-family: {FONTS.SYSTEM};
            }}
            QPushButton:hover {{
                background-color: {COLORS.BACKGROUND_TERTIARY};
                border-color: {COLORS.BORDER_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {COLORS.BACKGROUND};
            }}
        """)
        self.copy_btn.clicked.connect(self.copy_code)
        header_layout.addWidget(self.copy_btn)
        
        layout.addWidget(header)
        
        # Code display area with syntax highlighting
        self.code_edit = QTextEdit()
        self.code_edit.setReadOnly(True)
        self.code_edit.setFont(QFont(FONTS.MONOSPACE.split(',')[0].strip("'"), 13))
        self.code_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS.CODE_BG};
                color: {COLORS.TEXT_PRIMARY};
                border: 1px solid {COLORS.BORDER};
                border-top: none;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                padding: 16px;
                font-family: {FONTS.MONOSPACE};
                font-size: {FONTS.SIZE_BASE};
                line-height: 1.6;
                selection-background-color: {COLORS.ACCENT_BLUE};
            }}
            QTextEdit:focus {{
                outline: none;
            }}
        """)
        
        # Apply syntax highlighting
        if self.title.lower() == "python":
            self.highlighter = PythonSyntaxHighlighter(self.code_edit.document())
        
        layout.addWidget(self.code_edit)
        self.setLayout(layout)
    
    def set_code(self, code: str):
        """
        Set the code content.
        
        Args:
            code: Code string to display
        """
        self.code_edit.setPlainText(code)
    
    def get_code(self) -> str:
        """
        Get the current code content.
        
        Returns:
            Current code as string
        """
        return self.code_edit.toPlainText()
    
    def copy_code(self):
        """Copy code to clipboard with visual feedback."""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code_edit.toPlainText())
        
        # Visual feedback
        original_text = self.copy_btn.text()
        self.copy_btn.setText("✓ Copied!")
        self.copy_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS.ACCENT_GREEN};
                color: {COLORS.TEXT_PRIMARY};
                border: 1px solid {COLORS.ACCENT_GREEN};
                border-radius: 6px;
                padding: 6px 16px;
                font-size: {FONTS.SIZE_SMALL};
                font-weight: {FONTS.WEIGHT_SEMIBOLD};
                min-height: 28px;
                font-family: {FONTS.SYSTEM};
            }}
        """)
        
        # Reset after 2 seconds
        QTimer.singleShot(2000, lambda: self._reset_copy_button(original_text))
    
    def _reset_copy_button(self, original_text: str):
        """Reset copy button to original state."""
        self.copy_btn.setText(original_text)
        self.copy_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS.BACKGROUND_SECONDARY};
                color: {COLORS.TEXT_PRIMARY};
                border: 1px solid {COLORS.BORDER};
                border-radius: 6px;
                padding: 6px 16px;
                font-size: {FONTS.SIZE_SMALL};
                font-weight: {FONTS.WEIGHT_MEDIUM};
                min-height: 28px;
                font-family: {FONTS.SYSTEM};
            }}
            QPushButton:hover {{
                background-color: {COLORS.BACKGROUND_TERTIARY};
                border-color: {COLORS.BORDER_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {COLORS.BACKGROUND};
            }}
        """)
