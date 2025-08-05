import sys
from PyQt5.QtWidgets import (QApplication, QStatusBar, QLabel)
from PyQt5.QtCore import Qt

class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = self

        self.status_label = QLabel("Ready")
        self.main_layout.addWidget(self.status_label)
