"""
Modern Chat Interface with Message Bubbles

ChatGPT-style messaging with proper styling and animations.
Supports user/AI messages, code blocks, and HTML formatting.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QScrollArea, QLabel, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

from .styles.modern_theme import COLORS, FONTS
from .code_block_widget import CodeBlockWidget


class MessageBubble(QWidget):
    """
    Individual message bubble for chat interface.
    
    Features:
    - Distinct styling for user vs AI messages
    - Code block integration
    - HTML formatting support
    - Smooth appearance animation
    """
    
    def __init__(self, content, message_type="user", parent=None):
        """
        Initialize message bubble.
        
        Args:
            content: Message content (text or HTML)
            message_type: "user" or "ai"
            parent: Parent widget
        """
        super().__init__(parent)
        self.content = content
        self.message_type = message_type
        self.init_ui()
    
    def init_ui(self):
        """Initialize the message bubble UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 4, 0, 4)
        
        # Message container
        message_widget = QWidget()
        
        if self.message_type == "user":
            # User message styling
            message_widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {COLORS.USER_MESSAGE_BG};
                    border-left: 3px solid {COLORS.USER_MESSAGE_BORDER};
                    border-radius: 8px;
                    padding: 12px;
                }}
            """)
        else:
            # AI message styling
            message_widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {COLORS.AI_MESSAGE_BG};
                    border-left: 3px solid {COLORS.AI_MESSAGE_BORDER};
                    border-radius: 8px;
                    padding: 12px;
                }}
            """)
        
        message_layout = QVBoxLayout()
        message_layout.setContentsMargins(0, 0, 0, 0)
        message_layout.setSpacing(8)
        
        # Header with icon and name
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 4)
        
        icon = "👤" if self.message_type == "user" else "🧠"
        name = "You" if self.message_type == "user" else "AI Expert"
        
        header_label = QLabel(f"{icon} <b>{name}</b>")
        if self.message_type == "user":
            color = COLORS.USER_MESSAGE_BORDER
        else:
            color = COLORS.AI_MESSAGE_BORDER
        
        header_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: {FONTS.SIZE_BASE};
                font-weight: {FONTS.WEIGHT_SEMIBOLD};
                font-family: {FONTS.SYSTEM};
                background: transparent;
                border: none;
            }}
        """)
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        message_layout.addLayout(header_layout)
        
        # Message content
        content_label = QLabel()
        content_label.setWordWrap(True)
        content_label.setText(self.content)
        content_label.setTextFormat(Qt.RichText)
        content_label.setOpenExternalLinks(True)
        content_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS.TEXT_PRIMARY};
                font-size: {FONTS.SIZE_BASE};
                font-family: {FONTS.SYSTEM};
                line-height: 1.6;
                background: transparent;
                border: none;
            }}
        """)
        message_layout.addWidget(content_label)
        
        message_widget.setLayout(message_layout)
        layout.addWidget(message_widget)
        
        self.setLayout(layout)


class ChatInterface(QWidget):
    """
    Modern chat interface component.
    
    Features:
    - User and AI message bubbles
    - Code block integration
    - Auto-scroll to bottom
    - Input field with send button
    - Message history
    """
    
    message_sent = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """Initialize chat interface."""
        super().__init__(parent)
        self.messages = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the chat interface UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Header
        header = QLabel("💬 AI Assistant")
        header.setStyleSheet(f"""
            QLabel {{
                color: {COLORS.ACCENT_BLUE};
                font-size: {FONTS.SIZE_LARGE};
                font-weight: {FONTS.WEIGHT_SEMIBOLD};
                padding: 12px;
                font-family: {FONTS.SYSTEM};
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(header)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"background-color: {COLORS.BORDER}; max-height: 1px;")
        layout.addWidget(separator)
        
        # Message scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {COLORS.BACKGROUND};
                border: none;
            }}
        """)
        
        # Messages container
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout()
        self.messages_layout.setContentsMargins(12, 8, 12, 8)
        self.messages_layout.setSpacing(12)
        self.messages_layout.addStretch()
        self.messages_widget.setLayout(self.messages_layout)
        
        scroll_area.setWidget(self.messages_widget)
        self.scroll_area = scroll_area
        layout.addWidget(scroll_area)
        
        # Input area
        input_container = QWidget()
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(12, 0, 12, 12)
        input_layout.setSpacing(8)
        
        # Text input
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.setMaximumHeight(80)
        self.input_field.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS.BACKGROUND_SECONDARY};
                color: {COLORS.TEXT_PRIMARY};
                border: 1px solid {COLORS.BORDER};
                border-radius: 8px;
                padding: 10px;
                font-size: {FONTS.SIZE_BASE};
                font-family: {FONTS.SYSTEM};
                selection-background-color: {COLORS.ACCENT_BLUE};
            }}
            QTextEdit:focus {{
                border: 1px solid {COLORS.ACCENT_BLUE};
            }}
        """)
        input_layout.addWidget(self.input_field)
        
        # Send button
        self.send_button = QPushButton("✉️ Send Message")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setFixedHeight(40)
        self.send_button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS.BUTTON_BG}, stop:1 {COLORS.BUTTON_ACTIVE});
                color: {COLORS.TEXT_PRIMARY};
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: {FONTS.WEIGHT_SEMIBOLD};
                font-size: {FONTS.SIZE_BASE};
                font-family: {FONTS.SYSTEM};
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS.BUTTON_HOVER}, stop:1 {COLORS.BUTTON_BG});
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS.BUTTON_ACTIVE}, stop:1 #1a6e2e);
            }}
        """)
        input_layout.addWidget(self.send_button)
        
        input_container.setLayout(input_layout)
        layout.addWidget(input_container)
        
        self.setLayout(layout)
        
        # Add welcome message
        self.add_welcome_message()
    
    def add_welcome_message(self):
        """Add initial welcome message."""
        welcome_text = """
        <p>Welcome! I'm your AI coding assistant, powered by the GHST Expert Collective.</p>
        <p>💡 <i>Ask questions, request code reviews, or get debugging help.</i></p>
        """
        self.add_ai_message(welcome_text)
    
    def add_user_message(self, message):
        """
        Add a user message to the chat.
        
        Args:
            message: Message text
        """
        bubble = MessageBubble(message, "user")
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, bubble)
        self.messages.append(("user", message))
        self._scroll_to_bottom()
    
    def add_ai_message(self, message):
        """
        Add an AI message to the chat.
        
        Args:
            message: Message text (can contain HTML)
        """
        bubble = MessageBubble(message, "ai")
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, bubble)
        self.messages.append(("ai", message))
        self._scroll_to_bottom()
    
    def add_code_block(self, code, language="Python"):
        """
        Add a code block to the chat.
        
        Args:
            code: Code content
            language: Programming language
        """
        code_block = CodeBlockWidget(language)
        code_block.set_code(code)
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, code_block)
        self.messages.append(("code", code))
        self._scroll_to_bottom()
    
    def send_message(self):
        """Handle sending a message."""
        message = self.input_field.toPlainText().strip()
        if message:
            self.add_user_message(message)
            self.input_field.clear()
            self.message_sent.emit(message)
            
            # Simulate AI response (replace with actual AI integration)
            QTimer.singleShot(500, lambda: self.add_ai_message(
                "I understand your request. Let me analyze this and provide assistance..."))
    
    def _scroll_to_bottom(self):
        """Scroll to the bottom of the chat."""
        QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()))
    
    def clear_messages(self):
        """Clear all messages from the chat."""
        # Remove all message widgets except the stretch
        while self.messages_layout.count() > 1:
            item = self.messages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.messages.clear()
        self.add_welcome_message()
