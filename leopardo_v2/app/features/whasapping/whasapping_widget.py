from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class WhasappingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Whasapping Module")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)
