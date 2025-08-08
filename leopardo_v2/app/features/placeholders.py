from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class PlaceholderWidget(QWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel(f"This is the placeholder for the {name} feature.")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)
