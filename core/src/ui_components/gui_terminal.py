"""Minimal terminal-centered GUI widget for MoE REPL integration.

This module creates a simple PyQt5 window with a QTextEdit for output and a
QLineEdit for input. Typing a prompt and pressing Enter sends it to the
MultiExpertOrchestrator and displays the combined output.

The GUI is optional and guarded: importing this module won't crash if PyQt5
is unavailable; the module provides `run_terminal_gui(orchestrator)` to start.
"""
from typing import Optional
import logging

logger = logging.getLogger(__name__)

try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget
    from PyQt5.QtCore import Qt
except Exception:
    QApplication = None


def run_terminal_gui(orchestrator, title: str = "GHST Terminal", port: Optional[int] = None):
    if QApplication is None:
        raise RuntimeError("PyQt5 is not installed")

    app = QApplication([])
    win = QMainWindow()
    win.setWindowTitle(title)
    central = QWidget()
    layout = QVBoxLayout()
    out = QTextEdit()
    out.setReadOnly(True)
    inp = QLineEdit()

    def on_enter():
        text = inp.text().strip()
        if not text:
            return
        out.append(f">>> {text}")
        res = orchestrator.run(text)
        out.append(res.get('combined', '[no output]'))
        out.append('\n')
        inp.clear()

    inp.returnPressed.connect(on_enter)
    layout.addWidget(out)
    layout.addWidget(inp)
    central.setLayout(layout)
    win.setCentralWidget(central)

    # center and show
    win.resize(800, 600)
    win.show()
    app.exec_()
