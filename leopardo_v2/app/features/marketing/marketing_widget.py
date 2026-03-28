import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget)
from PyQt5.QtCore import Qt

class MarketingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Title
        self.title = QLabel("Marketing")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.main_layout.addWidget(self.title)

        # Content Stack
        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack)
