import os
import sys
from PyQt5 import QtWidgets, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.tr("Gestion des Dossiers"))
        self.setGeometry(100, 100, 400, 300)

        self.label = QtWidgets.QLabel(self.tr("Appuyez sur le bouton pour supprimer le dossier courant."), self)
        self.label.setGeometry(20, 20, 360, 20)

        self.delete_button = QtWidgets.QPushButton(self.tr("Supprimer le dossier courant"), self)
        self.delete_button.setGeometry(130, 60, 150, 40)
        self.delete_button.clicked.connect(self.delete_current_folder)

        self.output_area = QtWidgets.QTextEdit(self)
        self.output_area.setGeometry(20, 120, 360, 150)
        self.output_area.setReadOnly(True)

    def delete_current_folder(self):
        self.output_area.clear()
        
        current_dir = os.getcwd()  # Obtenir le chemin du dossier courant
        self.output_area.append(self.tr(f"Suppression de tous les fichiers et sous-dossiers dans : {current_dir}..."))
        
        try:
            # Remonter d'un niveau et supprimer le dossier courant
            parent_dir = os.path.dirname(current_dir)
            os.rmdir(current_dir)  # Supprimer le dossier courant
            self.output_area.append(self.tr(f"[OK] Le dossier {current_dir} a été supprimé avec succès."))
        except Exception as e:
            self.output_area.append(self.tr(f"[ERREUR] La suppression du dossier a échoué : {str(e)}"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    translator = QtCore.QTranslator()
    
    # Chargez le fichier de traduction ici, par exemple "fr_FR.qm" pour le français
    translator.load("path_to_translations/fr_FR.qm")  # Mettez le chemin correct vers votre fichier de traduction
    app.installTranslator(translator)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
