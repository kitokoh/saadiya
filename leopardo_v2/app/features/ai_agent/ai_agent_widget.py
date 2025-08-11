from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QStackedWidget)
from PyQt5.QtCore import Qt

class AiAgentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Title
        self.title = QLabel("AI Agent")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.main_layout.addWidget(self.title)

        # Content stack to hold the different AI agent tools
        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack)
