import os
import sys
from PyQt5 import QtWidgets, QtCore
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Mise à Jour des Fichiers data.json')
        self.setGeometry(100, 100, 400, 300)

        # Layout principal
        layout = QtWidgets.QVBoxLayout()

        # Champ pour le dossier parent robotx
        self.robotDirEdit = QtWidgets.QLineEdit(self)
        self.robotDirEdit.setPlaceholderText("Entrez le chemin du dossier robot parent (ex: C:/bon)")
        layout.addWidget(self.robotDirEdit)

        # Champ pour le chemin du dossier contenant les sous-dossiers textx
        self.textDirEdit = QtWidgets.QLineEdit(self)
        self.textDirEdit.setPlaceholderText("Entrez le chemin du dossier text (ex: C:/Users/Username/Downloads/AI-FB-Robot/text)")
        layout.addWidget(self.textDirEdit)

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
        robot_dir = self.robotDirEdit.text()
        text_dir = self.textDirEdit.text()
        log_file_path = os.path.join(user_data_dir, "resources", "journalInstallation.txt")

        # Initialiser le fichier log
        with open(log_file_path, 'a') as log_file:
            log_file.write("===========================================\n")
            log_file.write(f"Mise à jour commencée le {QtCore.QDate.currentDate().toString()} à {QtCore.QTime.currentTime().toString()}\n")

        # Vérifier que les chemins existent
        if not os.path.exists(robot_dir):
            self.log("Le dossier robot spécifié n'existe pas.")
            return

        if not os.path.exists(text_dir):
            self.log("Le dossier texte spécifié n'existe pas.")
            return

        # Compter les sous-dossiers textx
        folders = [d for d in os.listdir(text_dir) if d.startswith('text')]
        count = len(folders)

        self.log(f"{count} dossiers textx trouvés.")
        self.log(f"Dossier texte parent : {text_dir}")
        self.log(f"Dossier robot parent : {robot_dir}")

        # Boucle sur tous les dossiers textx et robotx
        for i in range(1, count + 1):
            folder_name = f'text{i}'
            robot_data_file = os.path.join(robot_dir, f'robot{i}', 'data.json')
            text_data_file = os.path.join(text_dir, folder_name, 'data.json')

            self.log(f"Traitement du dossier {folder_name}")
            self.log(f"Chemin data.json dans robot : {robot_data_file}")
            self.log(f"Chemin data.json dans texte : {text_data_file}")

            # Vérification que les fichiers data.json existent dans robotx et textx
            if os.path.exists(robot_data_file):
                if os.path.exists(text_data_file):
                    self.log(f"Copie de {text_data_file} vers {robot_data_file}.")
                    with open(text_data_file, 'r') as src:
                        content = src.read()
                    with open(robot_data_file, 'w') as dest:
                        dest.write(content)
                    self.log(f"Mise à jour réussie du fichier {robot_data_file}.")
                else:
                    self.log(f"[ERREUR] - Le fichier {text_data_file} n'existe pas.")
            else:
                self.log(f"[ERREUR] - Le fichier {robot_data_file} n'existe pas.")

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
