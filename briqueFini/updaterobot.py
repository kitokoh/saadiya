import sys
import json
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox


class DbToJsonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Exporter Base de Données vers JSON')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Bouton pour exporter les données de la base de données vers un fichier JSON
        self.export_button = QPushButton('Exporter vers un fichier JSON', self)
        self.export_button.clicked.connect(self.export_to_json)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

    def export_to_json(self):
        """Exporte les données de la table 'media' vers un fichier JSON"""
        # Connexion à la base de données SQLite
        try:
            conn = sqlite3.connect('media.db')
            cursor = conn.cursor()

            # Sélectionner toutes les descriptions depuis la table 'media'
            cursor.execute('SELECT description FROM media')
            rows = cursor.fetchall()

            # Extraire les descriptions dans une liste
            descriptions = [row[0] for row in rows]

            conn.close()

            # Ouvrir une boîte de dialogue pour enregistrer le fichier JSON
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer fichier JSON", "", "Fichiers JSON (*.json);;Tous les fichiers (*)", options=options)
            
            if file_name:
                # Sauvegarder les descriptions dans le fichier JSON
                with open(file_name, 'w', encoding='utf-8') as json_file:
                    json.dump(descriptions, json_file, ensure_ascii=False, indent=4)

                # Afficher un message de succès
                QMessageBox.information(self, 'Succès', f'Les données ont été exportées avec succès dans "{file_name}".')
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur lors de la lecture de la base de données : {str(e)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DbToJsonApp()
    ex.show()
    sys.exit(app.exec_())


# maintenant donne moi un programme qui permet d insere des donnee pressent dans un .db a un ficier .json 