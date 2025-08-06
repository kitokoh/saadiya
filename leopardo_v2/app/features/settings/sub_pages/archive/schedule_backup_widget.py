from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class ScheduleBackupWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Schedule Backup Page (Under Construction)")
        layout.addWidget(label)
        self.setLayout(layout)
