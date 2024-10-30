import os
import sys
import shutil
import ctypes
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

# Classes HeaderSection et FooterSection à ajouter à votre application pour la cohérence avec le design fourni.
class HeaderSection(QtWidgets.QWidget):
    def __init__(self, parent=None, title="App", app_name="AppName", slogan="Slogan"):
        super().__init__(parent)
        layout = QVBoxLayout()
        header_label = QLabel(f"<h1>{title}</h1>")
        app_label = QLabel(f"<h3>{app_name}</h3>")
        slogan_label = QLabel(f"<h4>{slogan}</h4>")
        layout.addWidget(header_label)
        layout.addWidget(app_label)
        layout.addWidget(slogan_label)
        self.setLayout(layout)

class FooterSection(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        footer_label = QLabel("© 2024 - Tous droits réservés")
        footer_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(footer_label)
        self.setLayout(layout)

class JsonToRobot(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.tr("Gestion de Fichier - Facebook Robot"))
        self.setGeometry(100, 100, 800, 400)

        # Chemin du fichier source et destination
        self.source_file = os.path.expanduser(r'~\Desktop\Fb-robot-ai\tex\textx\data.json')
        self.dest_dir = r'C:\bon'

        # Initialisation de l'interface utilisateur
        self.initUI()

    def initUI(self):
        # Créer un layout vertical principal
        main_layout = QVBoxLayout()

        # Ajouter le header
        header = HeaderSection(self, title="Gestion des Fichiers", app_name="Nova360 AI", slogan="Automatisation Avancée")
        main_layout.addWidget(header)

        # Label d'information
        self.label = QLabel(self.tr("Copie du fichier data.json..."), self)
        main_layout.addWidget(self.label)

        # Créer un layout horizontal pour le contenu
        content_layout = QHBoxLayout()

        # Zone de sortie pour afficher les messages
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        content_layout.addWidget(self.output_area)

        # Ajouter l'image promotionnelle à droite
        promo_image_label = QLabel()
        pixmap = QtGui.QPixmap("resources/images/5.jpg")  # Assurez-vous que ce chemin est correct
        promo_image_label.setPixmap(pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        promo_image_label.setAlignment(QtCore.Qt.AlignCenter)
        content_layout.addWidget(promo_image_label)

        # Ajouter le layout de contenu au layout principal
        main_layout.addLayout(content_layout)

        # Bouton pour copier le fichier
        self.copy_button = QPushButton(self.tr("Copier Fichier data.json"), self)
        self.copy_button.clicked.connect(self.copy_file)
        main_layout.addWidget(self.copy_button)

        # Ajouter le footer
        footer = FooterSection(self)
        main_layout.addWidget(footer)

        # Définir le widget central
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Appliquer les styles CSS
        self.setStyleSheet("""
            QWidget {
                font-family: 'Arial';
                font-size: 14px;
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QTextEdit {
                font-size: 14px;
                background-color: white;
                border-radius: 8px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }
        """)

    def copy_file(self):
        # Demander confirmation avant de copier le fichier
        reply = QMessageBox.question(self, 
            self.tr("Confirmation de Copie"), 
            self.tr("Êtes-vous sûr de vouloir copier le fichier 'data.json' ?"), 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Commencer la copie
            self.output_area.append("Début de la copie du fichier...")

            if os.path.exists(self.source_file):
                try:
                    # Trouver le prochain dossier robtx dans le répertoire cible
                    counter = 1
                    while os.path.exists(os.path.join(self.dest_dir, f'robtx{counter}')):
                        counter += 1

                    # Créer le dossier de destination
                    dest_folder = os.path.join(self.dest_dir, f'robtx{counter}')
                    os.makedirs(dest_folder, exist_ok=True)

                    # S'assurer que les dossiers cachés et protégés sont accessibles
                    self.ensure_directory_access(dest_folder)

                    # Copier le fichier
                    shutil.copy2(self.source_file, os.path.join(dest_folder, 'data.json'))

                    self.output_area.append(f"Fichier copié dans {dest_folder}")
                    QMessageBox.information(self, self.tr("Succès"), self.tr("Fichier copié avec succès."))

                except Exception as e:
                    QMessageBox.critical(self, self.tr("Erreur"), self.tr(f"Erreur lors de la copie : {str(e)}"))
            else:
                QMessageBox.critical(self, self.tr("Erreur"), self.tr("Le fichier source est introuvable."))

        else:
            QMessageBox.information(self, self.tr("Annulé"), self.tr("La copie a été annulée."))

    def ensure_directory_access(self, path):
        """
        S'assurer que tous les droits de lecture et d'écriture sont accordés, même pour les fichiers cachés.
        """
        if os.path.exists(path):
            try:
                os.chmod(path, 0o777)
                FILE_ATTRIBUTE_NORMAL = 0x80
                ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_NORMAL)
            except Exception as e:
                self.output_area.append(f"Erreur lors de l'attribution des droits : {str(e)}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = JsonToRobot()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
