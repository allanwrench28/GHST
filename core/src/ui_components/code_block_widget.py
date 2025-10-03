"""
Code Block Widget - Modern code display with syntax highlighting and copy button

Provides a modern code display widget similar to Grok and ChatGPT interfaces.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTextEdit, QLabel, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor
import re


class PythonHighlighter(QSyntaxHighlighter):
    """Simple Python syntax highlighter."""
    
    def __init__(self, document):
        super().__init__(document)
        
        # Define syntax highlighting rules
        self.highlighting_rules = []
        
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#ff79c6"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
            'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True',
            'try', 'while', 'with', 'yield', 'async', 'await'
        ]
        for word in keywords:
            pattern = r'\b' + word + r'\b'
            self.highlighting_rules.append((re.compile(pattern), keyword_format))
        
        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#f1fa8c"))
        self.highlighting_rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.highlighting_rules.append((re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6272a4"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((re.compile(r'#[^\n]*'), comment_format))
        
        # Functions
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#50fa7b"))
        self.highlighting_rules.append((re.compile(r'\b[A-Za-z_][A-Za-z0-9_]*(?=\()'), function_format))
        
        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#bd93f9"))
        self.highlighting_rules.append((re.compile(r'\b[0-9]+\.?[0-9]*\b'), number_format))
    
    def highlightBlock(self, text):
        """Apply syntax highlighting to the given text block."""
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), format)


class CodeBlockWidget(QWidget):
    """
    Modern code block widget with syntax highlighting and copy button.
    
    Features:
        - Syntax highlighting for Python code
        - Copy button at the top right
        - Modern styling matching GitHub/Grok aesthetic
        - Language label
    """
    
    def __init__(self, code="", language="python", parent=None):
        super().__init__(parent)
        self.code = code
        self.language = language
        self.init_ui()
    
    def init_ui(self):
        """Initialize the code block UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        # Header with language and copy button
        header = QWidget()
        header.setObjectName("codeBlockHeader")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(12, 8, 12, 8)
        header.setLayout(header_layout)
        
        # Language label
        lang_label = QLabel(f"📄 {self.language}")
        lang_label.setStyleSheet("""
            color: #8b949e;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        """)
        header_layout.addWidget(lang_label)
        header_layout.addStretch()
        
        # Copy button
        self.copy_btn = QPushButton("📋 Copy")
        self.copy_btn.setObjectName("codeBlockCopyBtn")
        self.copy_btn.clicked.connect(self.copy_code)
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(self.copy_btn)
        
        layout.addWidget(header)
        
        # Code display
        self.code_display = QTextEdit()
        self.code_display.setReadOnly(True)
        self.code_display.setPlainText(self.code)
        self.code_display.setFont(QFont("Consolas", 10))
        self.code_display.setObjectName("codeBlockDisplay")
        
        # Apply syntax highlighting for Python
        if self.language.lower() == "python":
            self.highlighter = PythonHighlighter(self.code_display.document())
        
        layout.addWidget(self.code_display)
        
        # Apply styling
        self.setStyleSheet("""
            CodeBlockWidget {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
            }
            
            #codeBlockHeader {
                background-color: #1c2128;
                border-bottom: 1px solid #30363d;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            
            #codeBlockCopyBtn {
                background-color: transparent;
                color: #8b949e;
                border: 1px solid #30363d;
                padding: 4px 12px;
                border-radius: 6px;
                font-size: 12px;
            }
            
            #codeBlockCopyBtn:hover {
                background-color: #21262d;
                color: #e6edf3;
                border-color: #484f58;
            }
            
            #codeBlockCopyBtn:pressed {
                background-color: #161b22;
            }
            
            #codeBlockDisplay {
                background-color: #0d1117;
                border: none;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                color: #e6edf3;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                line-height: 1.5;
            }
        """)
    
    def copy_code(self):
        """Copy code to clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code)
        
        # Show feedback
        original_text = self.copy_btn.text()
        self.copy_btn.setText("✅ Copied!")
        self.copy_btn.setEnabled(False)
        
        # Reset after 2 seconds
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self.reset_copy_button(original_text))
    
    def reset_copy_button(self, original_text):
        """Reset copy button to original state."""
        self.copy_btn.setText(original_text)
        self.copy_btn.setEnabled(True)
    
    def set_code(self, code, language="python"):
        """Update the code display."""
        self.code = code
        self.language = language
        self.code_display.setPlainText(code)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = QMainWindow()
    window.setWindowTitle("Code Block Widget Demo")
    window.setGeometry(100, 100, 600, 400)
    
    central = QWidget()
    layout = QVBoxLayout()
    central.setLayout(layout)
    window.setCentralWidget(central)
    
    # Example code block
    example_code = """def hello_world():
    # This is a comment
    message = "Hello, World!"
    print(message)
    return True

if __name__ == "__main__":
    result = hello_world()
    print(f"Result: {result}")
"""
    
    code_block = CodeBlockWidget(example_code, "python")
    layout.addWidget(code_block)
    
    window.show()
    sys.exit(app.exec_())
