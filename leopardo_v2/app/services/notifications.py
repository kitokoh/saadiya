from PyQt5.QtWidgets import QMessageBox

class NotificationService:
    def __init__(self, parent=None):
        self.parent = parent

    def show_notification(self, title, message):
        QMessageBox.information(self.parent, title, message)
