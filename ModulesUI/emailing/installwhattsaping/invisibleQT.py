import os
import subprocess
import sys
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QProgressBar, QPushButton, QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

# Importe les sections de l'en-tête et du pied de page
from ui.header import HeaderSection
from ui.footer import FooterSection
from imports import *
class InvisibleInstance(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Facebook Robot Pro - Masquer les Dossiers")
        self.setGeometry(600, 300, 800, 400)

        # Initialiser l'interface utilisateur
        self.initUI()

    def initUI(self):
        # Créer un layout vertical principal
        main_layout = QVBoxLayout()

        # Ajouter le header au layout principal
        header = HeaderSection(self, title="Facebook Robot Pro", app_name="Nova360 AI", slogan="Masquage Automatisé")
        main_layout.addWidget(header)

        # Créer un layout horizontal pour le contenu
        content_layout = QHBoxLayout()

        # Zone de sortie pour afficher les messages
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        content_layout.addWidget(self.output_area)

        # Ajouter l'image promotionnelle à droite
        promo_image_label = QLabel()
        pixmap = QPixmap("resources/images/5.jpg")  # Assurez-vous que ce chemin est correct
        promo_image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        promo_image_label.setAlignment(Qt.AlignCenter)

        content_layout.addWidget(promo_image_label)

        # Ajouter le layout de contenu au layout principal
        main_layout.addLayout(content_layout)

        # Bouton pour masquer les dossiers
        self.hide_button = QPushButton("Masquer les Dossiers")
        self.hide_button.clicked.connect(self.hide_folders)
        main_layout.addWidget(self.hide_button)

        # Barre de progression
        self.progress_bar = QProgressBar(self)
        main_layout.addWidget(self.progress_bar)

        # Ajouter le footer
        footer = FooterSection(self)
        main_layout.addWidget(footer)

        # Définir le layout principal de la fenêtre
        self.setLayout(main_layout)

        # Appliquer les styles CSS
        self.setStyleSheet("""
            QWidget {
                font-family: 'Arial';
                font-size: 14px;
                background-color: #f0f0f0;  /* Couleur d'arrière-plan douce */
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                font-weight: bold;
                border-radius: 8px;  /* Coins arrondis */
                padding: 10px;  /* Espace intérieur */
                transition: background-color 0.3s;  /* Transition douce */
            }
            QPushButton:hover {
                background-color: #005a9e;  /* Couleur au survol */
            }
            QTextEdit {
                font-size: 14px;
                background-color: white;  /* Couleur de fond pour la zone de texte */
                border-radius: 8px;  /* Coins arrondis */
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;  /* Couleur de texte sombre */
            }
            QProgressBar {
                background-color: #e0e0e0;  /* Couleur de fond de la barre de progression */
                border-radius: 8px;  /* Coins arrondis */
            }
            QProgressBar::chunk {
                background-color: #0078D7;  /* Couleur de la barre de progression */
                border-radius: 8px;  /* Coins arrondis */
            }
        """)
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/modules/main_fb_robot_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/modules/main_fb_robot_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/modules/main_fb_robot_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/modules/main_fb_robot_translated.qm")

        # Installer le traducteur pour appliquer la nouvelle langue
        QApplication.instance().installTranslator(self.translator)
        
            # Sauvegarder le choix de l'utilisateur
        self.save_language_choice(language)


        # Réappliquer la traduction sur tous les éléments visibles de l'interface
        self.retranslateUi()

    def save_language_choice(self, language):
        """Sauvegarde le choix de langue de l'utilisateur dans un fichier JSON."""
        preferences = {'language': language}
        with open('resources/settings.json', 'w') as f:
            json.dump(preferences, f)
    def retranslateUi(self):
        """Recharge les textes traduits dans l'interface."""
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
        self.instance_action.setText(self.tr('Instance'))
        self.media_action.setText(self.tr('Médias'))
        self.group_action.setText(self.tr('Groupes'))
        self.about_action.setText(self.tr('About'))
        self.certificate_action.setText(self.tr('Certif'))
        self.language_menu.setTitle(self.tr('Langue'))

    def init_language(self):
        """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
        # Vérifiez si le fichier de préférences existe
        if os.path.exists('resources/settings.json'):
            with open('resources/settings.json', 'r') as f:
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
            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)

    def hide_folders(self):
        """Masquer les dossiers dans le répertoire spécifié."""
        base_folder = "C:\\bon"  # Chemin du dossier à masquer
        self.output_area.clear()
        self.output_area.append("Préparation à masquer les dossiers...\n")
        self.progress_bar.setValue(0)

        if os.path.exists(base_folder):
            items = [os.path.join(base_folder, item) for item in os.listdir(base_folder)]
            total_items = len(items)

            # Masquer le dossier principal
            os.system(f'attrib +h +s "{base_folder}"')

            # Masquer les sous-dossiers et fichiers
            for index, item in enumerate(items):
                os.system(f'attrib +h +s "{item}"')
                progress = int((index + 1) / total_items * 100)
                self.progress_bar.setValue(progress)  # Mise à jour de la barre de progression
                self.output_area.append(f"Element positionner ou masqué...\n")  # Afficher les éléments masqués
                QApplication.processEvents()  # Mettre à jour l'interface

            self.log_action(f"Tous les dossiers dans bon sont maintenant masqués.")
            QMessageBox.information(self, "Dossiers Masqués", 
                                    "Tous les dossiers dans bon sont masqués et prêts à l'emploi !")
        else:
            self.log_action(f"Le dossier bon n'existe pas.")
            QMessageBox.critical(self, "Erreur", 
                                 f"Le dossier bon n'existe pas.")

    def log_action(self, message):
        # Chemin du dossier ressources pour le fichier de log
        resources_folder = "resources"
        log_file = os.path.join(user_data_dir , resources_folder, "journalInstallation.txt")

        # Création du fichier de log s'il n'existe pas
        if not os.path.exists(resources_folder):
            os.makedirs(resources_folder)  # Crée le dossier ressources s'il n'existe pas

        if not os.path.exists(log_file):
            with open(log_file, 'w') as f:
                f.write("-- Journal des opérations de masquage démarré --\n")
        
        with open(log_file, 'a') as f:
            f.write(f"{message}\n")

def main():
    app = QApplication(sys.argv)
    fb_app = InvisibleInstance()
    fb_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
