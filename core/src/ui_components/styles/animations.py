"""
Animation Utilities for GHST UI

Smooth animation helpers for window fade-ins, loading spinners, and transitions.
All animations run at 30-60 FPS for smooth performance.
"""

from PyQt5.QtCore import (
    QPropertyAnimation, QEasingCurve, QTimer,
    pyqtProperty, QObject, Qt, QVariantAnimation
)
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtGui import QTransform


class AnimationHelper:
    """Helper class for creating common animations."""
    
    @staticmethod
    def create_fade_in(widget, duration=400, start_opacity=0.0, end_opacity=1.0):
        """
        Create a fade-in animation for a widget.
        
        Args:
            widget: QWidget to animate
            duration: Animation duration in milliseconds (default: 400ms)
            start_opacity: Starting opacity (default: 0.0)
            end_opacity: Ending opacity (default: 1.0)
            
        Returns:
            QPropertyAnimation object
        """
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)
        
        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        
        return animation
    
    @staticmethod
    def create_fade_out(widget, duration=400, start_opacity=1.0, end_opacity=0.0):
        """
        Create a fade-out animation for a widget.
        
        Args:
            widget: QWidget to animate
            duration: Animation duration in milliseconds (default: 400ms)
            start_opacity: Starting opacity (default: 1.0)
            end_opacity: Ending opacity (default: 0.0)
            
        Returns:
            QPropertyAnimation object
        """
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)
        
        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setEasingCurve(QEasingCurve.InCubic)
        
        return animation
    
    @staticmethod
    def create_slide_in(widget, duration=300, direction='left'):
        """
        Create a slide-in animation for a widget.
        
        Args:
            widget: QWidget to animate
            duration: Animation duration in milliseconds (default: 300ms)
            direction: Direction to slide from ('left', 'right', 'top', 'bottom')
            
        Returns:
            QPropertyAnimation object
        """
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        
        current_pos = widget.pos()
        
        if direction == 'left':
            start_pos = current_pos.x() - widget.width()
            animation.setStartValue(widget.pos())
            animation.setEndValue(current_pos)
        elif direction == 'right':
            start_pos = current_pos.x() + widget.width()
            animation.setStartValue(widget.pos())
            animation.setEndValue(current_pos)
        
        return animation


class FadeAnimation(QObject):
    """
    Reusable fade animation class.
    
    Provides smooth fade-in/out animations with proper opacity management.
    """
    
    def __init__(self, widget, duration=400):
        """
        Initialize fade animation.
        
        Args:
            widget: Target widget to animate
            duration: Animation duration in milliseconds
        """
        super().__init__()
        self.widget = widget
        self.duration = duration
        self.opacity_effect = QGraphicsOpacityEffect()
        self.widget.setGraphicsEffect(self.opacity_effect)
        
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(self.duration)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
    
    def fade_in(self):
        """Fade in the widget."""
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()
    
    def fade_out(self):
        """Fade out the widget."""
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start()
    
    def set_opacity(self, opacity):
        """Set opacity directly without animation."""
        self.opacity_effect.setOpacity(opacity)


class RotateAnimation(QObject):
    """
    Smooth rotation animation for loading spinners.
    
    Provides continuous rotation at 30 FPS for smooth performance.
    """
    
    def __init__(self, widget, rotation_speed=30):
        """
        Initialize rotation animation.
        
        Args:
            widget: Widget to rotate
            rotation_speed: Degrees per step (default: 30 for 30 FPS)
        """
        super().__init__()
        self.widget = widget
        self.rotation_speed = rotation_speed
        self.current_angle = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._rotate)
        self.timer.setInterval(33)  # ~30 FPS
    
    def start(self):
        """Start the rotation animation."""
        self.timer.start()
    
    def stop(self):
        """Stop the rotation animation."""
        self.timer.stop()
        self.current_angle = 0
    
    def _rotate(self):
        """Internal rotation step."""
        self.current_angle = (self.current_angle + self.rotation_speed) % 360
        transform = QTransform()
        transform.rotate(self.current_angle)
        # Note: This would need to be implemented with custom painting
        # For now, we'll use a simpler approach in the actual spinner widget


class TransitionHelper:
    """Helper for creating smooth transitions between states."""
    
    @staticmethod
    def create_value_animation(target_object, property_name, start_value, 
                               end_value, duration=300, easing=QEasingCurve.InOutCubic):
        """
        Create a property animation for smooth value transitions.
        
        Args:
            target_object: Object to animate
            property_name: Property to animate (as bytes)
            start_value: Starting value
            end_value: Ending value
            duration: Animation duration in milliseconds
            easing: Easing curve type
            
        Returns:
            QPropertyAnimation object
        """
        animation = QPropertyAnimation(target_object, property_name)
        animation.setDuration(duration)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        animation.setEasingCurve(easing)
        
        return animation
    
    @staticmethod
    def delay_call(callback, delay_ms):
        """
        Call a function after a delay.
        
        Args:
            callback: Function to call
            delay_ms: Delay in milliseconds
        """
        QTimer.singleShot(delay_ms, callback)


class LoadingAnimationHelper:
    """Helper for loading animation states."""
    
    @staticmethod
    def create_pulse_animation(widget, duration=1000):
        """
        Create a pulse animation effect.
        
        Args:
            widget: Widget to pulse
            duration: Full pulse cycle duration
            
        Returns:
            QPropertyAnimation object
        """
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)
        
        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.5)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        animation.setLoopCount(-1)  # Infinite loop
        
        return animation
