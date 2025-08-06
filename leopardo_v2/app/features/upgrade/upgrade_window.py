from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class SpecialOfferWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Special Offer!")
        self.layout = QVBoxLayout(self)

        title = QLabel("🔥 Limited Time Offer! 🔥")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        offer_text = QLabel("Upgrade to Leopardo Pro and get 50% off for the first year!")
        offer_text.setFont(QFont("Arial", 16))
        offer_text.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(offer_text)

        upgrade_button = QPushButton("Upgrade Now!")
        upgrade_button.setStyleSheet("background-color: #28a745; color: white; padding: 15px; font-size: 18px; border-radius: 10px;")
        self.layout.addWidget(upgrade_button)

        self.setLayout(self.layout)
