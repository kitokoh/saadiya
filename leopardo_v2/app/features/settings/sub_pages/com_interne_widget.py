from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class ComInterneWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Com Interne Page (Under Construction)")
        layout.addWidget(label)
        self.setLayout(layout)
