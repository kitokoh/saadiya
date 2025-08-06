from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class LicencesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Licences Page (Under Construction)")
        layout.addWidget(label)
        self.setLayout(layout)
