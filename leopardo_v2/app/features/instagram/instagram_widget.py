from PyQt5.QtWidgets import QWidget, QVBoxLayout
from .instagram_dashboard_widget import InstagramDashboardWidget

class InstagramWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.dashboard = InstagramDashboardWidget()
        layout.addWidget(self.dashboard)
        self.setLayout(layout)
