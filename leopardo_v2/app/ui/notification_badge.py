from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

class NotificationBadge(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.count = 0
        self.setFixedSize(20, 20)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Arial", 8, QFont.Bold))
        self.setStyleSheet("color: white;")
        self.hide()

    def set_count(self, count):
        self.count = count
        if self.count > 0:
            self.setText(str(self.count))
            self.show()
        else:
            self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("red"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 20, 20)
        super().paintEvent(event)
