from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class RemoveBgWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Remove Background Page (Under Construction)")
        layout.addWidget(label)
        self.setLayout(layout)
