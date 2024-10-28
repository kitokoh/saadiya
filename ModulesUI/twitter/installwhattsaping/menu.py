import sys
from PyQt5 import QtWidgets, QtCore

class InstallerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('FB Robot Pro Kurulum Menüsü')
        self.setGeometry(100, 100, 400, 300)

        # Layout principal
        layout = QtWidgets.QVBoxLayout()

        # Titre
        self.titleLabel = QtWidgets.QLabel("FB Robot Pro Kurulum Menüsü", self)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.titleLabel)

        # Boutons du menu
        self.installButton = QtWidgets.QPushButton('FB Robot Pro\'yu Yükle', self)
        self.installButton.clicked.connect(self.install)
        layout.addWidget(self.installButton)

        self.licenseButton = QtWidgets.QPushButton('Lisans İste', self)
        self.licenseButton.clicked.connect(self.request_license)
        layout.addWidget(self.licenseButton)

        self.uninstallButton = QtWidgets.QPushButton('FB Robot Pro\'yu Kaldır', self)
        self.uninstallButton.clicked.connect(self.uninstall)
        layout.addWidget(self.uninstallButton)

        self.exitButton = QtWidgets.QPushButton('Çıkış', self)
        self.exitButton.clicked.connect(self.close)
        layout.addWidget(self.exitButton)

        # Zone de texte pour les logs
        self.logTextEdit = QtWidgets.QTextEdit(self)
        self.logTextEdit.setReadOnly(True)
        layout.addWidget(self.logTextEdit)

        self.setLayout(layout)

    def log(self, message):
        self.logTextEdit.append(message)

    def install(self):
        self.log("FB Robot Pro yükleme başlatılıyor...")
        # Ici, ajoutez vos commandes d'installation
        self.log("Kurulum tamamlandı!")

    def request_license(self):
        self.log("Lisans almak için lütfen şu adrese başvurun: support@fbrobotpro.com")
        # Ici, vous pouvez ajouter des fonctionnalités de demande de licence
        self.log("Lisans talebi gönderildi!")

    def uninstall(self):
        self.log("FB Robot Pro kaldırılıyor...")
        # Ici, ajoutez vos commandes de désinstallation
        self.log("FB Robot Pro başarıyla kaldırıldı!")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = InstallerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
