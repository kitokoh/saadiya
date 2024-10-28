import os
import sys
import subprocess
from PyQt5 import QtWidgets, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.tr("Dossier Management"))
        self.setGeometry(100, 100, 400, 300)

        self.folder_path = "C:\\bon"
        
        self.label = QtWidgets.QLabel(self.tr("Tentative de fermeture des processus utilisant le dossier C:\\bon..."), self)
        self.label.setGeometry(20, 20, 360, 20)

        self.close_button = QtWidgets.QPushButton(self.tr("Fermeture des processus"), self)
        self.close_button.setGeometry(150, 60, 120, 40)
        self.close_button.clicked.connect(self.close_processes)

        self.delete_button = QtWidgets.QPushButton(self.tr("Supprimer le dossier"), self)
        self.delete_button.setGeometry(150, 120, 120, 40)
        self.delete_button.clicked.connect(self.delete_folder)

        self.output_area = QtWidgets.QTextEdit(self)
        self.output_area.setGeometry(20, 180, 360, 100)
        self.output_area.setReadOnly(True)

        self.setStyleSheet("font-size: 14px;")

    def close_processes(self):
        self.output_area.clear()
        self.output_area.append(self.tr("Tentative de fermeture des processus..."))
        
        # Utiliser handle.exe pour identifier les processus (remplacez ceci par votre méthode)
        try:
            output = subprocess.check_output(['handle', self.folder_path], stderr=subprocess.STDOUT, text=True)
            for line in output.splitlines():
                if self.folder_path in line:
                    pid = line.split()[1]
                    self.output_area.append(self.tr(f"Fermeture du processus PID {pid} qui utilise {self.folder_path}..."))
                    os.system(f'taskkill /PID {pid} /F')
            self.output_area.append(self.tr("Processus fermés."))
        except Exception as e:
            self.output_area.append(self.tr(f"[ERREUR] Impossible de fermer les processus: {str(e)}"))

    def delete_folder(self):
        self.output_area.clear()
        
        if os.path.exists(self.folder_path):
            self.output_area.append(self.tr(f"Le dossier {self.folder_path} existe, il sera supprimé..."))
            try:
                os.rmdir(self.folder_path)
                self.output_area.append(self.tr(f"[OK] Le dossier {self.folder_path} a été supprimé avec succès."))
            except Exception as e:
                self.output_area.append(self.tr(f"[ERREUR] La suppression du dossier a échoué: {str(e)}"))
        else:
            self.output_area.append(self.tr(f"[ERREUR] Le dossier {self.folder_path} n'existe pas!"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    translator = QtCore.QTranslator()
    
    # Chargez le fichier de traduction ici, par exemple "fr_FR.qm" pour le français
    translator.load("path_to_translations/fr_FR.qm")  # Mettez le chemin correct vers votre fichier de traduction
    app.installTranslator(translator)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
