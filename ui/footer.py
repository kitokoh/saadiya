import sys
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QFrame, QPushButton, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal, QTranslator, QLocale, QLibraryInfo
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
import os
class FooterSection(QFrame):
    # Signal émis lors du clic sur les boutons
    privacy_clicked = pyqtSignal()
    terms_clicked = pyqtSignal()

    def __init__(self, parent=None):
                # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        super().__init__(parent)
                # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        self.setup_ui()
    def switch_language(self, language):
        """Permet de changer la langue."""
        # if language == "en":
        #     self.translator.load("resources/lang/en_US/ui/footer_translated.qm")
        # elif language == "fr":
        #     self.translator.load("resources/lang/fr_FR/ui/footer_translated.qm")
        # elif language == "tr":
        #     self.translator.load("resources/lang/tr_TR/ui/footer_translated.qm")
        # elif language == "ar":
        #     self.translator.load("resources/lang/ar_AR/ui/footer_translated.qm")


        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','ui','footer_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','ui','footer_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','ui','footer_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','ui','footer_translated.qm'))

        # Installer le traducteur pour appliquer la nouvelle langue
        QApplication.instance().installTranslator(self.translator)
        
            # Sauvegarder le choix de l'utilisateur
        self.save_language_choice(language)


        # Réappliquer la traduction sur tous les éléments visibles de l'interface
        self.retranslateUi()

    def save_language_choice(self, language):
        """Sauvegarde le choix de langue de l'utilisateur dans un fichier JSON."""
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
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
            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)

    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                border: none;
                background-color: #2E7D32;
            }
        """)

        layout = QHBoxLayout(self)

        # Création et configuration des boutons
        privacy_button = self.create_button(self.tr("Politique de confidentialité"))
        privacy_button.clicked.connect(self.on_privacy_clicked)

        terms_button = self.create_button(self.tr("Termes et Conditions"))
        terms_button.clicked.connect(self.on_terms_clicked)

        footer_text = QLabel(self.tr("visit www.turknovatech.com | © 2024 by Türk Novatech - Tous droits réservés."))
        footer_text.setFont(QFont("Arial", 10))
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setStyleSheet("color: white;")

        # Ajouter les widgets au layout
        layout.addWidget(privacy_button)
        layout.addWidget(terms_button)
        layout.addWidget(footer_text)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 10))
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #81C784;
            }
        """)
        return button

    def on_privacy_clicked(self):
        self.privacy_clicked.emit()  # Émettre le signal pour indiquer que le bouton a été cliqué

    def on_terms_clicked(self):
        self.terms_clicked.emit()  # Émettre le signal pour indiquer que le bouton a été cliqué


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Charger la traduction selon la langue du système
    translator = QTranslator()
    system_locale = QLocale.system().name()  # ex : 'fr_FR', 'en_US', etc.
    qm_path = f"lang/{system_locale}/ui/footer.qm"  # Chemin de ton fichier .qm

    if translator.load(qm_path):
        app.installTranslator(translator)

    # Créer et afficher la fenêtre principale
    window = FooterSection()
    window.show()

    sys.exit(app.exec_())
