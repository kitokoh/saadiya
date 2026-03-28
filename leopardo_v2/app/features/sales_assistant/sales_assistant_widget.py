from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel)
from PyQt5.QtCore import Qt

class SalesAssistantWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Title
        self.title = QLabel("Sales Assistant")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.main_layout.addWidget(self.title)

        # Placeholder for content
        self.content_label = QLabel("Sales Assistant content will be here.")
        self.content_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.content_label)
