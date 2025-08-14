from PyQt5.QtWidgets import QWidget, QVBoxLayout
from .facebook_dashboard_widget import FacebookDashboardWidget

class FacebookWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.dashboard = FacebookDashboardWidget()
        layout.addWidget(self.dashboard)
        self.setLayout(layout)
