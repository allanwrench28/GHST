"""
Loading Animations for GHST UI

Smooth loading spinners and progress indicators at 30 FPS.
Provides visual feedback for async operations.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QFont

from .styles.modern_theme import COLORS, FONTS


class LoadingSpinner(QWidget):
    """
    Smooth rotating loading spinner.
    
    Features:
    - 30 FPS smooth rotation
    - Customizable size and color
    - Minimal CPU usage
    - Clean circular design
    """
    
    def __init__(self, size=32, color=None, parent=None):
        """
        Initialize loading spinner.
        
        Args:
            size: Spinner diameter in pixels (default: 32)
            color: Spinner color (default: ACCENT_BLUE)
            parent: Parent widget
        """
        super().__init__(parent)
        self.size = size
        self.color = color or COLORS.ACCENT_BLUE
        self.angle = 0
        
        self.setFixedSize(size, size)
        
        # Timer for animation (30 FPS)
        self.timer = QTimer()
        self.timer.timeout.connect(self._rotate)
        self.timer.setInterval(33)  # ~30 FPS
    
    def start(self):
        """Start the spinner animation."""
        self.timer.start()
        self.show()
    
    def stop(self):
        """Stop the spinner animation."""
        self.timer.stop()
        self.hide()
    
    def _rotate(self):
        """Rotate the spinner by one step."""
        self.angle = (self.angle + 30) % 360
        self.update()
    
    def paintEvent(self, event):
        """Paint the spinner."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw spinner arc
        pen = QPen(QColor(self.color))
        pen.setWidth(3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        
        # Draw arc
        rect = self.rect().adjusted(4, 4, -4, -4)
        painter.drawArc(rect, self.angle * 16, 120 * 16)


class LoadingDots(QWidget):
    """
    Animated loading dots indicator.
    
    Features:
    - Three dots with pulsing animation
    - Smooth fade in/out effect
    - Minimal design
    """
    
    def __init__(self, parent=None):
        """Initialize loading dots."""
        super().__init__(parent)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        self.dots = []
        for i in range(3):
            dot = QLabel("●")
            dot.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS.ACCENT_BLUE};
                    font-size: {FONTS.SIZE_LARGE};
                    font-family: {FONTS.SYSTEM};
                }}
            """)
            dot.setAlignment(Qt.AlignCenter)
            layout.addWidget(dot)
            self.dots.append(dot)
        
        self.setLayout(layout)
        
        # Animation state
        self.current_dot = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate)
        self.timer.setInterval(400)  # Change dot every 400ms
    
    def start(self):
        """Start the dots animation."""
        self.timer.start()
        self.show()
    
    def stop(self):
        """Stop the dots animation."""
        self.timer.stop()
        self.hide()
    
    def _animate(self):
        """Animate the dots."""
        # Reset all dots
        for dot in self.dots:
            dot.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS.TEXT_TERTIARY};
                    font-size: {FONTS.SIZE_LARGE};
                    font-family: {FONTS.SYSTEM};
                }}
            """)
        
        # Highlight current dot
        self.dots[self.current_dot].setStyleSheet(f"""
            QLabel {{
                color: {COLORS.ACCENT_BLUE};
                font-size: {FONTS.SIZE_LARGE};
                font-family: {FONTS.SYSTEM};
            }}
        """)
        
        self.current_dot = (self.current_dot + 1) % 3


class LoadingOverlay(QWidget):
    """
    Full-screen loading overlay with spinner and message.
    
    Features:
    - Semi-transparent background
    - Centered spinner and message
    - Blocks interaction while loading
    """
    
    def __init__(self, message="Loading...", parent=None):
        """
        Initialize loading overlay.
        
        Args:
            message: Loading message to display
            parent: Parent widget
        """
        super().__init__(parent)
        self.message = message
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(13, 17, 23, 0.85);
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Spinner
        self.spinner = LoadingSpinner(48, COLORS.ACCENT_BLUE)
        spinner_container = QWidget()
        spinner_layout = QHBoxLayout()
        spinner_layout.setAlignment(Qt.AlignCenter)
        spinner_layout.addWidget(self.spinner)
        spinner_container.setLayout(spinner_layout)
        layout.addWidget(spinner_container)
        
        # Message label
        self.message_label = QLabel(self.message)
        self.message_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS.TEXT_PRIMARY};
                font-size: {FONTS.SIZE_MEDIUM};
                font-weight: {FONTS.WEIGHT_MEDIUM};
                font-family: {FONTS.SYSTEM};
                margin-top: 16px;
            }}
        """)
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)
        
        self.setLayout(layout)
        self.hide()
    
    def show_loading(self, message=None):
        """
        Show the loading overlay.
        
        Args:
            message: Optional message to display (uses default if not provided)
        """
        if message:
            self.message_label.setText(message)
        self.spinner.start()
        self.show()
        self.raise_()
    
    def hide_loading(self):
        """Hide the loading overlay."""
        self.spinner.stop()
        self.hide()
    
    def update_message(self, message):
        """
        Update the loading message.
        
        Args:
            message: New message to display
        """
        self.message_label.setText(message)


class ProgressIndicator(QWidget):
    """
    Indeterminate progress indicator.
    
    Features:
    - Smooth sliding animation
    - Customizable color
    - Compact design
    """
    
    progress_updated = pyqtSignal(int)
    
    def __init__(self, parent=None):
        """Initialize progress indicator."""
        super().__init__(parent)
        self.progress = 0
        self.setFixedHeight(4)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate)
        self.timer.setInterval(50)  # 20 FPS
    
    def start(self):
        """Start the progress animation."""
        self.progress = 0
        self.timer.start()
        self.show()
    
    def stop(self):
        """Stop the progress animation."""
        self.timer.stop()
        self.progress = 0
        self.hide()
    
    def _animate(self):
        """Animate the progress."""
        self.progress = (self.progress + 2) % 100
        self.progress_updated.emit(self.progress)
        self.update()
    
    def paintEvent(self, event):
        """Paint the progress indicator."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor(COLORS.BACKGROUND_TERTIARY))
        
        # Progress bar
        width = int(self.width() * 0.3)  # 30% width
        x = int((self.width() - width) * (self.progress / 100.0))
        
        painter.fillRect(x, 0, width, self.height(), QColor(COLORS.ACCENT_BLUE))


class InlineSpinner(QWidget):
    """
    Small inline spinner for buttons and compact spaces.
    
    Features:
    - Compact size (16px)
    - Smooth rotation
    - Minimal design
    """
    
    def __init__(self, parent=None):
        """Initialize inline spinner."""
        super().__init__(parent)
        self.setFixedSize(16, 16)
        self.angle = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._rotate)
        self.timer.setInterval(50)  # 20 FPS (more efficient for small spinner)
    
    def start(self):
        """Start the spinner."""
        self.timer.start()
    
    def stop(self):
        """Stop the spinner."""
        self.timer.stop()
        self.angle = 0
        self.update()
    
    def _rotate(self):
        """Rotate the spinner."""
        self.angle = (self.angle + 30) % 360
        self.update()
    
    def paintEvent(self, event):
        """Paint the spinner."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor(COLORS.ACCENT_BLUE))
        pen.setWidth(2)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        
        rect = self.rect().adjusted(2, 2, -2, -2)
        painter.drawArc(rect, self.angle * 16, 90 * 16)
