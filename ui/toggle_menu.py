from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QRect, QPropertyAnimation, QEasingCurve
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
class ToggleMenu(QWidget):
    def __init__(self, parent=None):
                # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

                # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        super(ToggleMenu, self).__init__(parent)

        self.setGeometry(0, 80, 200, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #4CAF50; /* Couleur de fond principale */
                border: 1px solid #388E3C; /* Bordure pour un meilleur contraste */
                border-radius: 10px; /* Coins arrondis */
            }
            QPushButton {
                background-color: #66BB6A; /* Couleur des boutons */
                color: white;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 16px;
                border-radius: 5px; /* Coins arrondis pour les boutons */
            }
            QPushButton:hover {
                background-color: #81C784; /* Couleur au survol */
            }
        """)

        # Layout du menu toggle
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Exemple de boutons avec traduction
        buttons = [
            (self.tr("Accueil"), "home"),
            (self.tr("Paramètres"), "settings"),
            (self.tr("Aide"), "help"),
            (self.tr("À propos"), "info"),
            (self.tr("Quitter"), "exit")
        ]

        for text, icon in buttons:
            button = QPushButton(text)
            layout.addWidget(button)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/ui/toggle_menu_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/ui/toggle_menu_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/ui/toggle_menu_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/ui/toggle_menu_translated.qm")

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

    def toggle(self):
        if self.isVisible():
            self.animation.setStartValue(QRect(0, 80, 200, 600))
            self.animation.setEndValue(QRect(0, 80, 0, 600))
            self.animation.start()
            self.setVisible(False)
        else:
            self.setVisible(True)
            self.animation.setStartValue(QRect(0, 80, 0, 600))
            self.animation.setEndValue(QRect(0, 80, 200, 600))
            self.animation.start()
