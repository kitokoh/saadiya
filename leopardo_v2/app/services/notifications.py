from PyQt5.QtWidgets import QMessageBox
from ..ui.notification_badge import NotificationBadge

class NotificationService:
    def __init__(self, parent=None):
        self.parent = parent
        self.badges = {}

    def add_badge(self, name, widget):
        badge = NotificationBadge(widget)
        self.badges[name] = badge
        return badge

    def set_badge_count(self, name, count):
        if name in self.badges:
            self.badges[name].set_count(count)

    def show_notification(self, title, message):
        QMessageBox.information(self.parent, title, message)
