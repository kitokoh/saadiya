import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import Qt

class ToolsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Title
        title = QLabel("Tools")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.main_layout.addWidget(title)

        # PDF Editor
        self.pdf_editor_button = QPushButton("PDF Editor")
        self.pdf_editor_button.clicked.connect(self.launch_pdf_editor)
        self.main_layout.addWidget(self.pdf_editor_button)

        # Watermark
        self.watermark_button = QPushButton("Watermark")
        self.watermark_button.clicked.connect(self.launch_watermark)
        self.main_layout.addWidget(self.watermark_button)

        # Link Management
        self.link_management_button = QPushButton("Link Management")
        self.link_management_button.clicked.connect(self.launch_link_management)
        self.main_layout.addWidget(self.link_management_button)

        # Scheduler
        self.scheduler_button = QPushButton("Scheduler")
        self.scheduler_button.clicked.connect(self.launch_scheduler)
        self.main_layout.addWidget(self.scheduler_button)

    def launch_pdf_editor(self):
        try:
            subprocess.Popen(["python", "tools/editpdf.py"])
        except FileNotFoundError:
            print("Error: Could not find 'tools/editpdf.py'")

    def launch_watermark(self):
        try:
            subprocess.Popen(["python", "tools/watermarks/watermark_window.py"])
        except FileNotFoundError:
            print("Error: Could not find 'tools/watermarks/watermark_window.py'")

    def launch_link_management(self):
        try:
            subprocess.Popen(["python", "liens/gestionliens.py"])
        except FileNotFoundError:
            print("Error: Could not find 'liens/gestionliens.py'")

    def launch_scheduler(self):
        try:
            subprocess.Popen(["python", "statistique/activiteprogramme.py"])
        except FileNotFoundError:
            print("Error: Could not find 'statistique/activiteprogramme.py'")
