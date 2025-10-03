"""
Animated Button Component

A button with smooth hover animations and transitions.
"""

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty, QRect
from PyQt5.QtGui import QColor


class AnimatedButton(QPushButton):
    """A button with smooth animations on hover and click."""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._opacity = 1.0
        self.setup_animations()
        
    def setup_animations(self):
        """Setup button animations."""
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0a84ff, stop:1 #0066cc);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
                min-height: 32px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a9aff, stop:1 #0a84ff);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0066cc, stop:1 #0055aa);
                padding-top: 12px;
                padding-bottom: 8px;
            }
        """)
    
    def get_opacity(self):
        """Get button opacity."""
        return self._opacity
    
    def set_opacity(self, value):
        """Set button opacity."""
        self._opacity = value
        self.update()
    
    opacity = pyqtProperty(float, get_opacity, set_opacity)


class PulseButton(QPushButton):
    """A button with pulse animation effect."""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._scale = 1.0
        self.setup_style()
        
    def setup_style(self):
        """Setup button styling."""
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00d9ff, stop:1 #0a84ff);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                min-height: 40px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3affff, stop:1 #3a9aff);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00aad9, stop:1 #0066cc);
            }
        """)
    
    def pulse(self):
        """Create a pulse animation."""
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.OutBounce)
        
        current_geo = self.geometry()
        center = current_geo.center()
        
        # Expand
        expanded = QRect(
            current_geo.x() - 5,
            current_geo.y() - 5,
            current_geo.width() + 10,
            current_geo.height() + 10
        )
        
        animation.setStartValue(current_geo)
        animation.setEndValue(expanded)
        animation.start()
        
        # Return to normal after delay
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(200, lambda: self._return_to_normal(current_geo))
    
    def _return_to_normal(self, original_geo):
        """Return button to original size."""
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.setStartValue(self.geometry())
        animation.setEndValue(original_geo)
        animation.start()


class GhostButton(QPushButton):
    """A button with ghost/transparent styling and hover effects."""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setup_style()
        
    def setup_style(self):
        """Setup ghost button styling."""
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #0a84ff;
                border: 2px solid #0a84ff;
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
                min-height: 32px;
            }
            QPushButton:hover {
                background: rgba(10, 132, 255, 0.1);
                border-color: #3a9aff;
                color: #3a9aff;
            }
            QPushButton:pressed {
                background: rgba(10, 132, 255, 0.2);
                border-color: #0066cc;
                color: #0066cc;
            }
        """)
