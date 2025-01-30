# donne moi un programme pyqt qui permet dimporter un .json comportant des text dans un base de donne .bd 
# qui conntient des insersion plus precisement en son champ description le code doit inserer les
# text du jos dans la colone esccription du db il dois insere autant il ya des text il doit les inserer dans autant des ligne du media 

import sys
import json
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox


class JsonToDbApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Importer JSON dans la Base de Données')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Bouton pour importer un fichier JSON
        self.import_button = QPushButton('Importer un fichier JSON', self)
        self.import_button.clicked.connect(self.import_json)
        layout.addWidget(self.import_button)

        self.setLayout(layout)

    def import_json(self):
        """Ouvre une boîte de dialogue pour importer un fichier JSON et insérer les données dans la base de données"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier JSON", "", "Fichiers JSON (*.json);;Tous les fichiers (*)", options=options)
        
        if file_name:
            try:
                # Lire le fichier JSON
                with open(file_name, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # Vérifier que le fichier JSON contient bien une liste de textes
                if isinstance(data, list):
                    self.insert_into_db(data)
                else:
                    QMessageBox.warning(self, 'Erreur', 'Le fichier JSON ne contient pas une liste de textes.')
            except Exception as e:
                QMessageBox.critical(self, 'Erreur', f'Erreur lors de la lecture du fichier JSON : {str(e)}')

    def insert_into_db(self, texts):
        """Insère une liste de textes dans la base de données dans la colonne description de la table media"""
        try:
            # Connexion à la base de données SQLite (création si elle n'existe pas)
            conn = sqlite3.connect('media.db')
            cursor = conn.cursor()

            # Création de la table media si elle n'existe pas déjà
            cursor.execute('''CREATE TABLE IF NOT EXISTS media (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                description TEXT
                              )''')

            # Insertion des textes dans la base de données
            for text in texts:
                cursor.execute('INSERT INTO media (description) VALUES (?)', (text,))

            conn.commit()  # Appliquer les changements
            conn.close()  # Fermer la connexion

            # Afficher un message de succès
            QMessageBox.information(self, 'Succès', f'{len(texts)} textes ont été insérés avec succès dans la base de données.')
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'insertion dans la base de données : {str(e)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JsonToDbApp()
    ex.show()
    sys.exit(app.exec_())
