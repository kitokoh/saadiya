import sys
import os
import json
import sqlite3
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

class VirtualEnvThread(QThread):
    """Thread to handle the virtual environment execution"""
    process_finished = pyqtSignal()

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword

    def run(self):
        """Run the virtual environment process"""
        try:
            # Path to the virtual environment's batch file or script
            env_script = f"C:\\path_to_your_virtualenv\\Scripts\\activate.bat"
            
            # Start the virtual environment process (change this to match your environment)
            process = subprocess.Popen([env_script, self.keyword], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Wait for the process to finish
            if process.returncode == 0:
                self.process_finished.emit()  # Signal that the process is complete
            else:
                raise Exception(f"Erreur dans l'exécution de l'environnement virtuel: {stderr.decode('utf-8')}")
        except Exception as e:
            self.process_finished.emit()
            QMessageBox.critical(None, "Erreur", f"Erreur lors de l'exécution : {str(e)}")

class DbJsonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Exécution Environnement Virtuel et Gestion de Données')
        self.setGeometry(100, 100, 500, 250)

        layout = QVBoxLayout()

        # Ajout d'un champ pour saisir le mot-clé
        self.label = QLabel("Entrez un mot-clé pour démarrer l'environnement virtuel :", self)
        layout.addWidget(self.label)

        self.keyword_input = QLineEdit(self)
        layout.addWidget(self.keyword_input)

        # Bouton pour démarrer l'environnement virtuel
        self.start_button = QPushButton('Démarrer l\'environnement virtuel', self)
        self.start_button.clicked.connect(self.start_virtual_env)
        layout.addWidget(self.start_button)

        # Bouton pour importer un fichier JSON
        self.import_button = QPushButton('Importer les données JSON dans la base de données', self)
        self.import_button.clicked.connect(self.import_json_to_db)
        layout.addWidget(self.import_button)

        self.setLayout(layout)

    def start_virtual_env(self):
        """Démarre l'environnement virtuel en fonction du mot-clé"""
        keyword = self.keyword_input.text()
        if not keyword:
            QMessageBox.warning(self, "Erreur", "Le mot-clé ne peut pas être vide.")
            return

        self.virtual_env_thread = VirtualEnvThread(keyword)
        self.virtual_env_thread.process_finished.connect(self.on_process_finished)
        self.virtual_env_thread.start()

    def on_process_finished(self):
        """Callback lorsque le processus de l'environnement virtuel est terminé"""
        QMessageBox.information(self, "Succès", "L'environnement virtuel a terminé son travail.")

        # Récupérer et insérer les données du fichier JSON dans la base de données
        self.import_json_to_db()

    def import_json_to_db(self):
        """Exporte les données de la table 'media' vers un fichier JSON"""
        json_file_path = "C:\\bon\\data.json"

        # Vérifier si le fichier JSON existe
        if not os.path.exists(json_file_path):
            QMessageBox.warning(self, "Erreur", "Le fichier JSON n'existe pas dans le dossier C:\\bon\\.")
            return

        try:
            # Lire le fichier JSON
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
            
            # Connexion à la base de données SQLite
            conn = sqlite3.connect('media.db')
            cursor = conn.cursor()

            # Créer la table media si elle n'existe pas déjà
            cursor.execute('''CREATE TABLE IF NOT EXISTS media (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                description TEXT
                              )''')

            # Insérer chaque texte du fichier JSON dans la base de données
            for text in data:
                cursor.execute('INSERT INTO media (description) VALUES (?)', (text,))

            conn.commit()  # Appliquer les changements
            conn.close()  # Fermer la connexion

            # Vider le fichier JSON après l'insertion
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump([], json_file)

            QMessageBox.information(self, "Succès", f"{len(data)} textes ont été insérés dans la base de données et le fichier JSON a été vidé.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'importation des données : {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DbJsonApp()
    ex.show()
    sys.exit(app.exec_())


# donne moi un programme complet tres bien disigner permettant de recevoir un keyword puis de 
# demarrer un environnement virtuelle windows  puis une fois l environnement virtuelle a fin son travail le programme part recupere les 
# donnee pressent dans un .json et les inserer dans le .db et enfin il laisse le .json la a vide note que le json est dans un dossier nome bon present dans c 