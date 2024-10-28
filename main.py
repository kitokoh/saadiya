import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget,QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo
from ui.header import HeaderSection
from ui.footer import FooterSection
from ui.login import LoginModule
from home import HomePage  # Assurez-vous d'importer le module d'accueil
from translation import TranslatorManager
from imports import *
class Nova360ProApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
             # Charger la langue du système

    def initUI(self):
        # Définir le titre et l'icône
        self.setWindowTitle(self.tr("Nova360Pro - Connexion"))
        self.setGeometry(100, 100, 800, 600)
        # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        self.setWindowIcon(QIcon('resources/icons/robot-512.png'))  # Assurez-vous que le chemin de l'icône est correct

        # Widget central et layout principal
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Initialisation des modules d'en-tête, de pied de page et de connexion
        self.header = HeaderSection(self, title=self.tr("AI Marketing Automation"), app_name="Nova360 AI", slogan=self.tr("AI Marketing & Management Auto"))
        self.footer = FooterSection()  # Pied de page
        self.login_module = LoginModule()  # Module de connexion

 # Créer le menu déroulant pour les langues
        # self.language_selector = QComboBox(self)
        # self.language_selector.addItems(["Français (fr_FR)", "Anglais (en_US)", "Arabe (ar_SA)", "Turc (tr_TR)"])
        # self.language_selector.currentIndexChanged.connect(self.change_language)

        # # Ajouter le sélecteur de langue à la mise en page
        # layout = QVBoxLayout()
        # layout.addWidget(self.language_selector)

        # Connecter le signal de connexion réussie
        self.login_module.connection_successful.connect(self.show_home)

        # Afficher le module de connexion au démarrage
        self.show_login()
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
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
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
        
    def show_login(self):
        """Afficher le module de connexion avec en-tête et pied de page."""
        # Ajouter l'en-tête, le module de connexion et le pied de page au layout principal
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.login_module)
        self.main_layout.addWidget(self.footer)

    def show_home(self):
        """Passer à la page d'accueil après une connexion réussie."""
        # Supprimer tous les widgets actuels du layout
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget in (self.login_module, self.header, self.footer):
                self.main_layout.removeWidget(widget)
                widget.deleteLater()  # Libérer la mémoire des widgets supprimés

        # Ajouter la page d'accueil
        self.home_module = HomePage()  # Module de la page d'accueil
        self.main_layout.addWidget(self.home_module)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Charger la traduction avant de lancer l'application

    # Démarrer l'application Nova360Pro
    window = Nova360ProApp()
    window.show()  # Afficher la fenêtre principale
    sys.exit(app.exec_())
