from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
class FeatureButtons(QHBoxLayout):
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
        if language == "en":
            self.translator.load("resources/lang/en_US/ui/feature_buttons_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/ui/feature_buttons_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/ui/feature_buttons_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/ui/feature_buttons_translated.qm")

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

    def setup_ui(self):
        features = [
            ("FB Robot Pro", "resources/icons/facebook-icon-png-770.png", "#E91E63"),
            ("WhatsApping", "resources/icons/whatsapp-512.png", "#4CAF50"),
            ("Blogging", "resources/icons/article-marketing-3-512.gif", "#4CAF50"),
            # Add other buttons here...
        ]

        for text, icon, color in features:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))
            button.setIcon(QIcon(QPixmap(icon).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: 2px solid #CCCCCC;
                    border-radius: 15px;
                    padding: 10px;
                    min-width: 150px;
                    min-height: 150px;
                }}
                QPushButton:hover {{
                    background-color: {self.lighten_color(color)};
                    transform: scale(1.05);
                }}
            """)
            self.addWidget(button)

    def lighten_color(self, color):
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'
