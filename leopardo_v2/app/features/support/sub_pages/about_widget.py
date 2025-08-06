from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class AboutWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("About Page (Under Construction)")
        layout.addWidget(label)
        self.setLayout(layout)
