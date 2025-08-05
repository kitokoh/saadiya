import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import Qt

class ToolsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Title
        self.title = QLabel("Tools")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.main_layout.addWidget(self.title)

        # PDF Editor
        self.pdf_editor_button = QPushButton("PDF Editor")
        self.main_layout.addWidget(self.pdf_editor_button)

        # Watermark
        self.watermark_button = QPushButton("Watermark")
        self.main_layout.addWidget(self.watermark_button)

        # Link Management
        self.link_management_button = QPushButton("Link Management")
        self.main_layout.addWidget(self.link_management_button)

        # Scheduler
        self.scheduler_button = QPushButton("Scheduler")
        self.main_layout.addWidget(self.scheduler_button)
