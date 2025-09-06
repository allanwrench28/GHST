
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class SpeedbuildSlider(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.label = QLabel("Personalization: 50% (Balanced)")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        self.setLayout(layout)
        self.slider.valueChanged.connect(self.update_label)

    def update_label(self, value):
        if value == 0:
            self.label.setText("SPEEDBUILD: Fully Automated (No Prompts)")
        elif value == 100:
            self.label.setText("Personalized: Full User Input Mode")
        else:
            self.label.setText(f"Personalization: {value}% (Mixed Mode)")

    def get_mode(self):
        value = self.slider.value()
        if value == 0:
            return "speedbuild"
        elif value == 100:
            return "personalized"
        else:
            return "mixed"
