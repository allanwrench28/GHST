"""
Settings Dialog Component

A polished settings dialog with tabbed interface for GHST configuration.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
    QWidget, QLabel, QPushButton, QCheckBox, QComboBox,
    QSpinBox, QLineEdit, QGroupBox, QSlider
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class SettingsDialog(QDialog):
    """A polished settings dialog for GHST configuration."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GHST Settings")
        self.setMinimumSize(700, 500)
        self.init_ui()
        self.apply_theme()
        
    def init_ui(self):
        """Initialize the settings UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: #2a2a2a; border-bottom: 1px solid #3a3a3a;")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(24, 0, 24, 0)
        header.setLayout(header_layout)
        
        title = QLabel("⚙️ Settings")
        title.setStyleSheet("""
            QLabel {
                color: #0a84ff;
                font-size: 20px;
                font-weight: 600;
            }
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        layout.addWidget(header)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        
        # General tab
        general_tab = self.create_general_tab()
        self.tab_widget.addTab(general_tab, "General")
        
        # AI Experts tab
        ai_tab = self.create_ai_tab()
        self.tab_widget.addTab(ai_tab, "AI Experts")
        
        # Appearance tab
        appearance_tab = self.create_appearance_tab()
        self.tab_widget.addTab(appearance_tab, "Appearance")
        
        # Advanced tab
        advanced_tab = self.create_advanced_tab()
        self.tab_widget.addTab(advanced_tab, "Advanced")
        
        layout.addWidget(self.tab_widget)
        
        # Footer with buttons
        footer = QWidget()
        footer.setFixedHeight(70)
        footer.setStyleSheet("background-color: #2a2a2a; border-top: 1px solid #3a3a3a;")
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(24, 16, 24, 16)
        footer.setLayout(footer_layout)
        
        footer_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setFixedWidth(100)
        footer_layout.addWidget(cancel_btn)
        
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_settings)
        apply_btn.setFixedWidth(100)
        footer_layout.addWidget(apply_btn)
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        save_btn.setFixedWidth(100)
        footer_layout.addWidget(save_btn)
        
        layout.addWidget(footer)
        
        self.setLayout(layout)
    
    def create_general_tab(self):
        """Create general settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        widget.setLayout(layout)
        
        # Auto-save group
        autosave_group = QGroupBox("Auto-Save")
        autosave_layout = QVBoxLayout()
        autosave_group.setLayout(autosave_layout)
        
        self.autosave_check = QCheckBox("Enable auto-save")
        self.autosave_check.setChecked(True)
        autosave_layout.addWidget(self.autosave_check)
        
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Save interval (seconds):"))
        self.save_interval = QSpinBox()
        self.save_interval.setRange(10, 300)
        self.save_interval.setValue(60)
        interval_layout.addWidget(self.save_interval)
        interval_layout.addStretch()
        autosave_layout.addLayout(interval_layout)
        
        layout.addWidget(autosave_group)
        
        # Project settings
        project_group = QGroupBox("Project")
        project_layout = QVBoxLayout()
        project_group.setLayout(project_layout)
        
        self.recent_projects_check = QCheckBox("Remember recent projects")
        self.recent_projects_check.setChecked(True)
        project_layout.addWidget(self.recent_projects_check)
        
        layout.addWidget(project_group)
        
        layout.addStretch()
        
        return widget
    
    def create_ai_tab(self):
        """Create AI experts settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        widget.setLayout(layout)
        
        # AI Model selection
        model_group = QGroupBox("AI Model")
        model_layout = QVBoxLayout()
        model_group.setLayout(model_layout)
        
        model_select_layout = QHBoxLayout()
        model_select_layout.addWidget(QLabel("Default model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "GPT-4",
            "Claude 3",
            "Local LLaMA",
            "Mixtral"
        ])
        model_select_layout.addWidget(self.model_combo)
        model_select_layout.addStretch()
        model_layout.addLayout(model_select_layout)
        
        layout.addWidget(model_group)
        
        # Expert behavior
        behavior_group = QGroupBox("Expert Behavior")
        behavior_layout = QVBoxLayout()
        behavior_group.setLayout(behavior_layout)
        
        self.auto_suggestions = QCheckBox("Enable automatic suggestions")
        self.auto_suggestions.setChecked(True)
        behavior_layout.addWidget(self.auto_suggestions)
        
        self.context_aware = QCheckBox("Context-aware assistance")
        self.context_aware.setChecked(True)
        behavior_layout.addWidget(self.context_aware)
        
        layout.addWidget(behavior_group)
        
        layout.addStretch()
        
        return widget
    
    def create_appearance_tab(self):
        """Create appearance settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        widget.setLayout(layout)
        
        # Theme
        theme_group = QGroupBox("Theme")
        theme_layout = QVBoxLayout()
        theme_group.setLayout(theme_layout)
        
        theme_select_layout = QHBoxLayout()
        theme_select_layout.addWidget(QLabel("Color theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "GHST Dark (Default)",
            "GHST Light",
            "High Contrast",
            "Solarized Dark"
        ])
        theme_select_layout.addWidget(self.theme_combo)
        theme_select_layout.addStretch()
        theme_layout.addLayout(theme_select_layout)
        
        layout.addWidget(theme_group)
        
        # Font settings
        font_group = QGroupBox("Font")
        font_layout = QVBoxLayout()
        font_group.setLayout(font_layout)
        
        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(QLabel("Editor font size:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(13)
        font_size_layout.addWidget(self.font_size_spin)
        font_size_layout.addStretch()
        font_layout.addLayout(font_size_layout)
        
        layout.addWidget(font_group)
        
        layout.addStretch()
        
        return widget
    
    def create_advanced_tab(self):
        """Create advanced settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        widget.setLayout(layout)
        
        # Performance
        perf_group = QGroupBox("Performance")
        perf_layout = QVBoxLayout()
        perf_group.setLayout(perf_layout)
        
        self.hardware_accel = QCheckBox("Enable hardware acceleration")
        self.hardware_accel.setChecked(True)
        perf_layout.addWidget(self.hardware_accel)
        
        thread_layout = QHBoxLayout()
        thread_layout.addWidget(QLabel("Worker threads:"))
        self.thread_spin = QSpinBox()
        self.thread_spin.setRange(1, 16)
        self.thread_spin.setValue(4)
        thread_layout.addWidget(self.thread_spin)
        thread_layout.addStretch()
        perf_layout.addLayout(thread_layout)
        
        layout.addWidget(perf_group)
        
        # Developer options
        dev_group = QGroupBox("Developer Options")
        dev_layout = QVBoxLayout()
        dev_group.setLayout(dev_layout)
        
        self.debug_mode = QCheckBox("Enable debug mode")
        dev_layout.addWidget(self.debug_mode)
        
        self.verbose_logging = QCheckBox("Verbose logging")
        dev_layout.addWidget(self.verbose_logging)
        
        layout.addWidget(dev_group)
        
        layout.addStretch()
        
        return widget
    
    def apply_theme(self):
        """Apply GHST theme to the dialog."""
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                color: #e8e8e8;
            }
            QTabWidget::pane {
                border: none;
                background-color: #1a1a1a;
            }
            QTabBar::tab {
                background-color: #252525;
                color: #999999;
                padding: 12px 24px;
                margin-right: 0;
                border: none;
                font-weight: 500;
                font-size: 13px;
            }
            QTabBar::tab:hover {
                background-color: #2a2a2a;
                color: #e8e8e8;
            }
            QTabBar::tab:selected {
                background-color: #1a1a1a;
                color: #0a84ff;
                border-bottom: 2px solid #0a84ff;
            }
            QGroupBox {
                background-color: #252525;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
                font-weight: 600;
                font-size: 14px;
                color: #e8e8e8;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }
            QCheckBox {
                color: #e8e8e8;
                spacing: 8px;
                font-size: 13px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #3a3a3a;
                background-color: #252525;
            }
            QCheckBox::indicator:hover {
                border-color: #0a84ff;
            }
            QCheckBox::indicator:checked {
                background-color: #0a84ff;
                border-color: #0a84ff;
            }
            QLabel {
                color: #e8e8e8;
                font-size: 13px;
            }
            QComboBox, QSpinBox, QLineEdit {
                background-color: #252525;
                color: #e8e8e8;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                min-height: 28px;
            }
            QComboBox:hover, QSpinBox:hover, QLineEdit:hover {
                border-color: #0a84ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0a84ff, stop:1 #0066cc);
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
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
            }
        """)
    
    def apply_settings(self):
        """Apply settings without closing dialog."""
        # Implement settings application logic here
        pass
