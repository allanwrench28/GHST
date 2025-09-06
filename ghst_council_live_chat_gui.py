import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor

class GHSTChatGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GHST Council Live Chat")
        self.setGeometry(100, 100, 500, 700)
        self.layout = QVBoxLayout()

        self.chat_box = QTextBrowser()
        self.chat_box.setOpenExternalLinks(True)
        self.chat_box.setStyleSheet("font-size: 16px; background: #181818; color: #e0e0e0; border-radius: 10px;")
        self.layout.addWidget(self.chat_box)

        self.button_layout = QHBoxLayout()
        self.pause_btn = QPushButton("Pause Chat")
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.button_layout.addWidget(self.pause_btn)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.paused = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_ghst_message)
        self.timer.start(2000)
        self.ghst_messages = self.generate_ghst_messages()
        self.msg_index = 0

    def toggle_pause(self):
        if self.paused:
            self.timer.start(2000)
            self.pause_btn.setText("Pause Chat")
        else:
            self.timer.stop()
            self.pause_btn.setText("Resume Chat")
        self.paused = not self.paused

    def add_ghst_message(self):
        if self.msg_index < len(self.ghst_messages):
            msg = self.ghst_messages[self.msg_index]
            self.chat_box.append(msg)
            self.chat_box.moveCursor(QTextCursor.End)
            self.msg_index += 1

    def generate_ghst_messages(self):
        # Example messages with hyperlinks
        return [
            '<b>🧭 Dr. TidyCode:</b> Reviewing <a href="file://ghst_installer_enhanced.py">installer code</a> for errors.',
            '<b>🕯️ Dr. Syntax:</b> Found <a href="https://www.python.org/dev/peps/pep-0008/">PEP8 violation</a> at line 107.',
            '<b>🦴 Dr. ImportOrder:</b> Unused import detected in <a href="file://ghst_auto_continue_gui_ocr.py">OCR script</a>.',
            '<b>🪄 Dr. Formatter:</b> Auto-formatting <a href="file://ghst_installer_beautiful.py">installer_beautiful.py</a>.',
            '<b>🧪 Dr. Archivist:</b> All critical errors resolved. <a href="file://fix_all_errors.py">View log</a>.',
            '<b>🧭 Dr. TidyCode:</b> <a href="file://ghst_council_groupchat.py">Council group chat</a> updated.',
            '<b>🕯️ Dr. Syntax:</b> <a href="file://ghst_tui.py">Terminal UI</a> style fixed.',
            '<b>🦴 Dr. ImportOrder:</b> <a href="file://ghst_orchestrator.py">Orchestrator</a> import order optimized.',
            '<b>🪄 Dr. Formatter:</b> <a href="file://ghst_installer_enhanced.py">installer_enhanced.py</a> ready for deployment.',
            '<b>🧪 Dr. Archivist:</b> <a href="file://fix_all_errors_daemon.py">Daemon</a> running in background.'
        ]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GHSTChatGUI()
    gui.show()
    sys.exit(app.exec_())
