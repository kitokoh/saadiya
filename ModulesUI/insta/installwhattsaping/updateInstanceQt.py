import sys
import os
import subprocess
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
class UpdateInstance(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI FB ROBOT PRO - Update Assistant")
        self.setGeometry(600, 300, 800, 400)

        # Initialiser l'interface utilisateur
        self.initUI()

    def initUI(self):
        # Créer un layout vertical principal
        main_layout = QVBoxLayout()

        #Ajouter le header au layout principal
        header = HeaderSection(self, title="AI FBK Marketing Instances", app_name="Nova360 AI", slogan="AI Marketing & Management Auto")
        main_layout.addWidget(header)

        # Créer un layout horizontal pour le contenu
        content_layout = QHBoxLayout()

        # Zone de sortie pour afficher les messages
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        content_layout.addWidget(self.output_area)

        # Ajouter l'image promotionnelle à droite
        promo_image_label = QLabel()
        pixmap = QPixmap("resources/images/9.jpg")  # Assurez-vous que ce chemin est correct
        promo_image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        promo_image_label.setAlignment(Qt.AlignCenter)

        content_layout.addWidget(promo_image_label)

        # Ajouter le layout de contenu au layout principal
        main_layout.addLayout(content_layout)

        # Bouton de mise à jour
        self.update_button = QPushButton("Mettre à jour les instances")
        self.update_button.clicked.connect(self.update_instances)
        main_layout.addWidget(self.update_button)

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

    def update_instances(self):
        """Lancer la mise à jour des instances"""
        self.output_area.clear()
        self.output_area.append("Démarrage de la mise à jour des instances...\n")
        self.progress_bar.setValue(0)

        instance_index = 1
        while True:
            foldername = f"C:\\bon\\robot{instance_index}"
            if os.path.exists(foldername):
                self.output_area.append(f"Mise à jour de robot{instance_index}...\n")
                self.update_instance(foldername, instance_index)
                instance_index += 1
            else:
                self.output_area.append("Toutes les instances ont été mises à jour avec succès.")
                self.progress_bar.setValue(100)
                break

    def update_instance(self, foldername, instance_index):
        """Met à jour une instance donnée"""
        os.chdir(foldername)
        try:
            self.run_command("git pull ")
            self.output_area.append(f"robot{instance_index} mis à jour avec succès\n")
            self.progress_bar.setValue((instance_index / 10) * 100)  # Mise à jour de la barre de progression

            env_script = f"C:\\bon\\robot{instance_index}\\env{instance_index}\\Scripts\\activate"
            if os.path.exists(env_script):
                self.run_command(f"{env_script} && pip install --upgrade -r requirements.txt")
                self.output_area.append(f"Dépendances mises à jour pour robot{instance_index}\n")
            else:
                self.output_area.append(f"L'environnement virtuel pour robot{instance_index} n'existe pas.\n")
        except Exception as e:
            self.output_area.append(f"Erreur lors de la mise à jour de robot{instance_index}: {str(e)}\n")

    def run_command(self, command):
        """Exécute une commande dans le shell"""
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        self.output_area.append(output.decode())
        if error:
            self.output_area.append(error.decode())

def main():
    app = QApplication(sys.argv)
    updater = UpdateInstance()
    updater.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
