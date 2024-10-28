import sys
import subprocess
from PyQt5 import QtWidgets, QtCore

class InstallerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('AI FB Robot Pro - Kurulum Bilgilendirmesi')
        self.setGeometry(100, 100, 400, 300)

        # Layout principal
        layout = QtWidgets.QVBoxLayout()

        # Titre
        self.titleLabel = QtWidgets.QLabel("AI FB Robot Pro - Kurulum Bilgilendirmesi", self)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.titleLabel)

        # Message d'accueil
        self.welcomeMessage = QtWidgets.QLabel(
            "AI FB Robot Pro Kurulumu Tamamlandi\n\n"
            "Lutfen tarayicinizi acarak Chrome uzerinde baglanti kurun ve\n"
            "AI FB Robot Pro'yu baslatmak icin Chrome'dan devam edin.",
            self
        )
        self.welcomeMessage.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.welcomeMessage)

        # Bouton pour ouvrir Chrome
        self.openChromeButton = QtWidgets.QPushButton('Google Chrome Aç', self)
        self.openChromeButton.clicked.connect(self.open_chrome)
        layout.addWidget(self.openChromeButton)

        # Bouton de sortie
        self.exitButton = QtWidgets.QPushButton('Çıkış', self)
        self.exitButton.clicked.connect(self.close)
        layout.addWidget(self.exitButton)

        self.setLayout(layout)

    def open_chrome(self):
        try:
            # Vérifie si Chrome est installé et l'ouvre
            subprocess.Popen(['C:/Program Files/Google/Chrome/Application/chrome.exe'])
            # Remplacez le chemin ci-dessus si Chrome est installé ailleurs
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Hata", "Chrome açılamadı. Lütfen Chrome'un yüklü olduğundan emin olun.")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = InstallerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
