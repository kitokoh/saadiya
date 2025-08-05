from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class ExternalDiskWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("External Disk Page (Under Construction)")
        layout.addWidget(label)
        self.setLayout(layout)
