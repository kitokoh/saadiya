import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel)
from PyQt5.QtCore import Qt
class HomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Title
        self.title = QLabel("Home")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.main_layout.addWidget(self.title)

        # Data Label
        self.data_label = QLabel("No data")
        self.data_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.data_label)

    def update_data(self, data):
        self.data_label.setText(data)
