from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class ManuelleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Manuelle Page (Under Construction)")
        layout.addWidget(label)
        self.setLayout(layout)
