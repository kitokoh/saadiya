from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class FtpServerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("FTP Server Page (Under Construction)")
        layout.addWidget(label)
        self.setLayout(layout)
