from PyQt5.QtWidgets import QSplashScreen, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap("resources/images/splashScreer.png"))
        self.setStyleSheet("background-color: #2E7D32;")
        self.setFont(QFont("Arial", 12))
        self.showMessage("Loading, please wait...", Qt.AlignBottom | Qt.AlignCenter, Qt.white)
