from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class RedditDashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("Reddit Dashboard Placeholder")
        layout.addWidget(label)
        self.setLayout(layout)
