from PyQt5.QtWidgets import QWidget, QVBoxLayout
from .linkedin_dashboard_widget import LinkedInDashboardWidget

class LinkedinWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.dashboard = LinkedInDashboardWidget()
        layout.addWidget(self.dashboard)
        self.setLayout(layout)
