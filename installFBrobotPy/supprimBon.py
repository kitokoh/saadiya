import os
import sys
import json
import subprocess
import shutil
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QVBoxLayout, QWidget

# Importe les sections de l'en-tête et du pied de page
from ui.header import HeaderSection  # Assurez-vous que ce fichier existe
from ui.footer import FooterSection  # Assurez-vous que ce fichier existe
_current_folder = os.getcwd()
#user_data_dir1 = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

user_data_dir1 = os.path.dirname(_current_folder)
user_data_dir = os.path.join(user_data_dir1, 'lang', 'resources')
key_data_dir = os.path.join(user_data_dir1, 'lang', 'resources')

class DeleteBon(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.tr("Dossier Management"))
        self.setGeometry(100, 100, 800, 400)
        self.translator = QTranslator()

        self.init_language()
        # Chemin du dossier et du fichier à supprimer
        self.folder_path = "C:\\bon"
        self.file_path = os.path.join(os.path.expanduser("~"), "Desktop", "FB-Robot.exe")
        
        # Initialisation de l'interface utilisateur
        self.initUI()

    def initUI(self):
        # Créer un layout vertical principal
        main_layout = QtWidgets.QVBoxLayout()
        self.translator = QTranslator()

        self.init_language()
        # Ajouter le header au layout principal
        header = HeaderSection(self, title="Facebook Robot Pro", app_name="Nova360 AI", slogan="Gestion des Dossiers")
        main_layout.addWidget(header)

        # Label d'information
        self.label = QtWidgets.QLabel(self.tr("Tentative de fermer les processus utilisant le dossier bon..."), self)
        main_layout.addWidget(self.label)

        # Créer un layout horizontal pour le contenu
        content_layout = QtWidgets.QHBoxLayout()

        # Zone de sortie pour afficher les messages
        self.output_area = QtWidgets.QTextEdit(self)
        self.output_area.setReadOnly(True)
        content_layout.addWidget(self.output_area)

        # Ajouter l'image promotionnelle à droite
        promo_image_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("resources/images/6.jpg")  # Assurez-vous que ce chemin est correct
        promo_image_label.setPixmap(pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        promo_image_label.setAlignment(QtCore.Qt.AlignCenter)
        content_layout.addWidget(promo_image_label)

        # Ajouter le layout de contenu au layout principal
        main_layout.addLayout(content_layout)

        # Bouton pour fermer les processus
        self.close_button = QtWidgets.QPushButton(self.tr("Fermeture des processus"), self)
        self.close_button.clicked.connect(self.close_processes)
        main_layout.addWidget(self.close_button)

        # Bouton pour supprimer le dossier et le fichier
        self.delete_button = QtWidgets.QPushButton(self.tr("Supprimer le dossier et le fichier"), self)
        self.delete_button.clicked.connect(self.confirm_delete)
        main_layout.addWidget(self.delete_button)

        # Barre de progression
        self.progress_bar = QtWidgets.QProgressBar(self)
        main_layout.addWidget(self.progress_bar)

        # Ajouter le footer
        footer = FooterSection(self)
        main_layout.addWidget(footer)

        # Set the main layout
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
            QProgressBar {
                background-color: #e0e0e0;
                border-radius: 8px;
            }
            QProgressBar::chunk {
                background-color: #0078D7;
                border-radius: 8px;
            }
        """)
    def switch_language(self, language):
        """Permet de changer la langue."""
        # if language == "en":
        #     self.translator.load("resources/lang/en_US/ui/login_translated.qm")
        # elif language == "fr":
        #     self.translator.load("resources/lang/fr_FR/ui/login_translated.qm")
        # elif language == "tr":
        #     self.translator.load("resources/lang/tr_TR/ui/login_translated.qm")
        # elif language == "ar":
        #     self.translator.load("resources/lang/ar_AR/ui/login_translated.qm")


        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','ui','login_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','ui','login_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','ui','login_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','ui','login_translated.qm'))
        elif language == "pt":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','pt_BR','ui','login_translated.qm'))

        # Installer le traducteur pour appliquer la nouvelle langue
        QApplication.instance().installTranslator(self.translator)
        
            # Sauvegarder le choix de l'utilisateur
        self.save_language_choice(language)


        # Réappliquer la traduction sur tous les éléments visibles de l'interface
        self.retranslateUi()

    def save_language_choice(self, language):
        """Sauvegarde le choix de langue de l'utilisateur dans un fichier JSON."""
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'settings.json'), 'w') as f:
            json.dump(preferences, f)
    def retranslateUi(self):
        """Recharge les textes traduits dans l'interface."""
        # self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # # Par exemple, pour les actions du menu :
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))
        pass

    def init_language(self):
        """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
        # Vérifiez si le fichier de préférences existe
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')  # Par défaut à l'anglais si non trouvé
        else:
            # Obtenir le code de langue du système
            system_locale = QLocale.system().name()[:2]  # Par exemple: 'fr', 'en', 'tr', etc.

            # Dictionnaire pour mapper les codes de langue aux traductions
            language_map = {
                'en': 'en',
                'fr': 'fr',
                'tr': 'tr',
                'ar': 'ar',
                 'pt': 'pt',

            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)

    def close_processes(self):
        self.output_area.clear()
        self.output_area.append(self.tr("Tentative de fermeture des processus..."))
        
        # Utiliser handle.exe pour identifier les processus
        try:
            output = subprocess.check_output(['handle', self.folder_path], stderr=subprocess.STDOUT, text=True)
            for line in output.splitlines():
                if self.folder_path in line:
                    pid = line.split()[1]
                    self.output_area.append(self.tr(f"Fermeture du processus PID {pid} qui utilise jsoon..."))
                    os.system(f'taskkill /PID {pid} /F')
            self.output_area.append(self.tr("Processus fermés."))
        except Exception as e:
            self.output_area.append(self.tr(f"[ERREUR] Impossible de fermer les processus: {str(e)}"))

    def confirm_delete(self):
        # Modal de confirmation avant la suppression
        reply = QtWidgets.QMessageBox.question(self, 
            self.tr("Confirmation de suppression"), 
            self.tr("Êtes-vous sûr de vouloir supprimer ce dossier ?\nCela supprimera également toutes les instances de Facebook Robot."), 
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
            QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            # Si l'utilisateur confirme, procéder à la suppression
            self.delete_folder_and_file()

    def delete_folder_and_file(self):
        self.output_area.clear()
        self.progress_bar.setValue(0)  # Réinitialiser la barre de progression

        # Forcer la suppression du dossier et de son contenu
        if os.path.exists(self.folder_path):
            self.output_area.append(self.tr(f"Le dossier bon existe, suppression forcée..."))
            try:
                # Supprimer les attributs cachés, système, ou en lecture seule
                for root, dirs, files in os.walk(self.folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        os.chmod(file_path, 0o777)  # Supprimer les restrictions sur les fichiers
                shutil.rmtree(self.folder_path, ignore_errors=True)
                self.output_area.append(self.tr(f"[OK] Le dossier bn a été supprimé avec succès."))
                self.progress_bar.setValue(50)  # Mettre à jour la barre de progression
            except Exception as e:
                self.output_area.append(self.tr(f"[ERREUR] La suppression du dossier a échoué: {str(e)}"))
        else:
            self.output_area.append(self.tr(f"[ERREUR] Le dossier bon n'existe pas!"))

        # Supprimer le fichier FB-Robot.exe
        if os.path.exists(self.file_path):
            self.output_area.append(self.tr(f"Le fichier json existe, il sera supprimé..."))
            try:
                os.remove(self.file_path)
                self.output_area.append(self.tr(f"[OK] Le fichier json a été supprimé avec succès."))
                self.progress_bar.setValue(100)  # Mettre à jour la barre de progression
            except Exception as e:
                self.output_area.append(self.tr(f"[ERREUR] La suppression du fichier a échoué: {str(e)}"))
        else:
            self.output_area.append(self.tr(f"[ERREUR] Le fichier  n'existe pas!"))

def main():
    app = QtWidgets.QApplication(sys.argv)
    # translator = QtCore.QTranslator()

    # # Chargez le fichier de traduction ici, par exemple "fr_FR.qm" pour le français
    # translator.load("path_to_translations/fr_FR.qm")  # Mettez le chemin correct vers votre fichier de traduction
    # app.installTranslator(translator)

    window = DeleteBon()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
