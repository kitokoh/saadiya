import os
import sys
from PyQt5 import QtWidgets, QtCore

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Mise à Jour des Fichiers data.json')
        self.setGeometry(100, 100, 400, 300)

        # Layout principal
        layout = QtWidgets.QVBoxLayout()

        # Champ pour le chemin du dossier contenant les sous-dossiers textx
        self.textDirEdit = QtWidgets.QLineEdit(self)
        self.textDirEdit.setPlaceholderText("Entrez le chemin du dossier (ex: C:/Users/Username/Downloads/AI-FB-Robot/text)")
        layout.addWidget(self.textDirEdit)

        # Champ pour le chemin du fichier data.json source
        self.sourceFileEdit = QtWidgets.QLineEdit(self)
        self.sourceFileEdit.setPlaceholderText("Entrez le chemin du fichier data.json source (ex: C:/path/to/data.json)")
        layout.addWidget(self.sourceFileEdit)

        # Bouton de mise à jour
        self.updateButton = QtWidgets.QPushButton('Mettre à Jour', self)
        self.updateButton.clicked.connect(self.updateJsonFiles)
        layout.addWidget(self.updateButton)

        # Champ de journal
        self.logTextEdit = QtWidgets.QTextEdit(self)
        self.logTextEdit.setReadOnly(True)
        layout.addWidget(self.logTextEdit)

        self.setLayout(layout)

    def updateJsonFiles(self):
        text_dir = self.textDirEdit.text()
        source_file = self.sourceFileEdit.text()
        log_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "journalinstallation.txt")

        if not os.path.exists(source_file):
            self.log("ERREUR : Le fichier source data.json n'existe pas.")
            return

        if not os.path.exists(text_dir):
            self.log("Le dossier spécifié n'existe pas.")
            return

        # Initialiser le fichier log
        with open(log_file_path, 'a') as log_file:
            log_file.write("===========================================\n")
            log_file.write(f"Mise à jour commencée le {QtCore.QDate.currentDate().toString()} à {QtCore.QTime.currentTime().toString()}\n")

        # Compter les sous-dossiers textx
        folders = [d for d in os.listdir(text_dir) if d.startswith('text')]
        count = len(folders)

        self.log(f"{count} dossiers textx trouvés.")
        self.log(f"Dossier texte parent : {text_dir}")
        self.log(f"Fichier source : {source_file}")

        # Boucle sur tous les dossiers textx
        for folder_name in folders:
            folder_path = os.path.join(text_dir, folder_name)
            data_file_path = os.path.join(folder_path, 'data.json')

            self.log(f"Traitement du dossier {folder_name}")
            self.log(f"Chemin du fichier data.json dans {folder_name} : {data_file_path}")

            # Vérification si le fichier data.json existe
            if os.path.exists(data_file_path):
                self.log(f"Mise à jour de {data_file_path} avec le contenu de {source_file}.")
                with open(data_file_path, 'w') as f:
                    with open(source_file, 'r') as source:
                        f.write(source.read())
                self.log(f"Mise à jour réussie du fichier {data_file_path}.")
            else:
                self.log(f"[INFO] - Le fichier data.json n'existe pas dans {folder_name}, création en cours.")
                with open(data_file_path, 'w') as f:
                    with open(source_file, 'r') as source:
                        f.write(source.read())
                self.log(f"Fichier data.json créé dans {folder_name}.")

        self.log("Toutes les mises à jour sont terminées.")

        # Écrire la fin du log
        with open(log_file_path, 'a') as log_file:
            log_file.write("Toutes les mises à jour sont terminées.\n")

    def log(self, message):
        self.logTextEdit.append(message)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
