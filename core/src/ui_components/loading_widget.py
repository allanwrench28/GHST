"""
Loading Widget - Modern loading spinner for GHST UI

Provides a smooth animated loading indicator for async operations.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, pyqtProperty
from PyQt5.QtGui import QPainter, QColor, QPen


class LoadingSpinner(QWidget):
    """
    A modern circular loading spinner widget.
    
    Features:
        - Smooth rotation animation
        - Customizable colors and size
        - Lightweight and performant
    """
    
    def __init__(self, parent=None, size=40, color="#1f6feb"):
        super().__init__(parent)
        self._angle = 0
        self._size = size
        self._color = QColor(color)
        self._is_spinning = False
        
        # Set widget properties
        self.setFixedSize(size, size)
        
        # Animation timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._rotate)
        self._timer.setInterval(30)  # ~33 FPS
    
    def start(self):
        """Start the spinning animation."""
        self._is_spinning = True
        self._timer.start()
        self.show()
    
    def stop(self):
        """Stop the spinning animation."""
        self._is_spinning = False
        self._timer.stop()
        self.hide()
    
    def _rotate(self):
        """Rotate the spinner."""
        self._angle = (self._angle + 10) % 360
        self.update()
    
    def paintEvent(self, event):
        """Paint the spinner."""
        if not self._is_spinning:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate center
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = min(self.width(), self.height()) // 2 - 4
        
        # Draw spinner arcs
        for i in range(8):
            angle = (self._angle + i * 45) % 360
            alpha = int(255 * (i + 1) / 8)
            
            color = QColor(self._color)
            color.setAlpha(alpha)
            
            pen = QPen(color)
            pen.setWidth(3)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            
            # Calculate start and end points
            start_angle = angle * 16
            span_angle = 30 * 16
            
            rect = QRect(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2
            )
            
            painter.drawArc(rect, start_angle, span_angle)


class LoadingMessage(QWidget):
    """
    A loading message widget with spinner and text.
    
    Combines a spinner with a text message for user feedback.
    """
    
    def __init__(self, message="Loading...", parent=None):
        super().__init__(parent)
        self._message = message
        self.init_ui()
    
    def init_ui(self):
        """Initialize the loading message UI."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        self.setLayout(layout)
        
        # Spinner
        self.spinner = LoadingSpinner(self, size=48, color="#1f6feb")
        spinner_container = QWidget()
        spinner_layout = QVBoxLayout()
        spinner_layout.setAlignment(Qt.AlignCenter)
        spinner_layout.addWidget(self.spinner)
        spinner_container.setLayout(spinner_layout)
        layout.addWidget(spinner_container)
        
        # Message label
        self.message_label = QLabel(self._message)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("""
            QLabel {
                color: #e6edf3;
                font-size: 14px;
                font-weight: 500;
                padding: 8px;
            }
        """)
        layout.addWidget(self.message_label)
        
        # Style the container
        self.setStyleSheet("""
            LoadingMessage {
                background-color: rgba(13, 17, 23, 0.95);
                border-radius: 12px;
                padding: 24px;
            }
        """)
    
    def start(self, message=None):
        """Start showing the loading indicator."""
        if message:
            self._message = message
            self.message_label.setText(message)
        self.spinner.start()
        self.show()
    
    def stop(self):
        """Stop and hide the loading indicator."""
        self.spinner.stop()
        self.hide()
    
    def set_message(self, message):
        """Update the loading message."""
        self._message = message
        self.message_label.setText(message)


class PulseLoader(QWidget):
    """
    A simple pulse animation loader (three dots).
    
    Lighter weight alternative to spinner for inline loading.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._dot_count = 0
        self.init_ui()
    
    def init_ui(self):
        """Initialize the pulse loader UI."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        
        self.label = QLabel("●●●")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: #1f6feb;
                font-size: 24px;
                letter-spacing: 8px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.label)
        
        # Animation timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._pulse)
        self._timer.setInterval(400)
    
    def start(self):
        """Start the pulse animation."""
        self._timer.start()
        self.show()
    
    def stop(self):
        """Stop the pulse animation."""
        self._timer.stop()
        self.hide()
    
    def _pulse(self):
        """Animate the dots."""
        self._dot_count = (self._dot_count + 1) % 4
        
        dots = "●" * max(1, self._dot_count)
        empty = "○" * (3 - len(dots))
        self.label.setText(dots + empty)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = QMainWindow()
    window.setWindowTitle("Loading Widget Demo")
    window.setGeometry(100, 100, 600, 400)
    
    # Set dark background
    window.setStyleSheet("""
        QMainWindow {
            background-color: #0d1117;
        }
        QPushButton {
            background-color: #1f6feb;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: #388bfd;
        }
    """)
    
    central = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)
    layout.setSpacing(20)
    central.setLayout(layout)
    window.setCentralWidget(central)
    
    # Spinner demo
    spinner_label = QLabel("Spinner:")
    spinner_label.setStyleSheet("color: #e6edf3; font-size: 14px;")
    layout.addWidget(spinner_label)
    
    spinner = LoadingSpinner(size=50)
    layout.addWidget(spinner)
    
    # Loading message demo
    loading_msg = LoadingMessage("Processing your request...")
    layout.addWidget(loading_msg)
    
    # Pulse loader demo
    pulse_label = QLabel("Pulse Loader:")
    pulse_label.setStyleSheet("color: #e6edf3; font-size: 14px;")
    layout.addWidget(pulse_label)
    
    pulse = PulseLoader()
    layout.addWidget(pulse)
    
    # Control buttons
    start_btn = QPushButton("Start All")
    start_btn.clicked.connect(lambda: (spinner.start(), loading_msg.start(), pulse.start()))
    layout.addWidget(start_btn)
    
    stop_btn = QPushButton("Stop All")
    stop_btn.clicked.connect(lambda: (spinner.stop(), loading_msg.stop(), pulse.stop()))
    layout.addWidget(stop_btn)
    
    window.show()
    sys.exit(app.exec_())
