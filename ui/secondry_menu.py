from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
class SecondaryMenu(QWidget):
    # Signal pour notifier un changement de contenu
    menu_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
                # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        # Layout pour le menu secondaire (horizontal)
        menu_layout = QHBoxLayout(self)

        # Bouton Instances
        instances_button = QPushButton(self.tr("Youtube Pro"), self)
        instances_button.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: black;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        instances_button.clicked.connect(lambda: self.menu_selected.emit("instances"))
        menu_layout.addWidget(instances_button)

        # Bouton Media
        media_button = QPushButton(self.tr("Marketing AI"), self)
        media_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        media_button.clicked.connect(lambda: self.menu_selected.emit("media"))
        menu_layout.addWidget(media_button)

        # Bouton Groupes
        groups_button = QPushButton(self.tr("Decouvre Facebook Pro"), self)
        groups_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        groups_button.clicked.connect(lambda: self.menu_selected.emit("groups"))
        menu_layout.addWidget(groups_button)

        self.setLayout(menu_layout)
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/ui/secondry_menu_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/ui/secondry_menu_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/ui/secondry_menu_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/ui/secondry_menu_translated.qm")

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
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))

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
