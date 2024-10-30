import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import QTranslator, QCoreApplication
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

class ScrapingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.tr("Outil de Scraping"))

        layout = QVBoxLayout()

        self.label = QLabel(self.tr("Entrez le mot-clé à extraire :"))
        layout.addWidget(self.label)

        self.keyword_input = QLineEdit(self)
        layout.addWidget(self.keyword_input)

        self.scrape_button = QPushButton(self.tr("Commencer le Scraping"), self)
        self.scrape_button.clicked.connect(self.start_scraping)
        layout.addWidget(self.scrape_button)

        self.setLayout(layout)

    def start_scraping(self):
        keyword = self.keyword_input.text()
        print(f"Scraping pour le mot-clé : {keyword}")
        # Appeler votre fonction de scraping ici

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Gestion de la traduction
    translator = QTranslator(app)
    translator.load("your_translation_file.qm")  # Chargez votre fichier de traduction
    app.installTranslator(translator)

    # Création et affichage de l'application
    ex = ScrapingApp()
    ex.show()

    sys.exit(app.exec_())
