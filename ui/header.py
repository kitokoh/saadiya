from PyQt5.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QFrame, QPushButton, QWidget
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal,QRect
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtWidgets import (
    QApplication, QAction, QMainWindow, QLabel, QPushButton, QVBoxLayout, 
    QHBoxLayout, QWidget, QLineEdit, QScrollArea, QFrame, QMenu, QMenuBar, QMessageBox
)
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
import os
class ImageLoader:
    """Classe utilitaire pour charger et redimensionner les images."""
    @staticmethod
    def load_pixmap(path, width, height):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            return QPixmap()  # Retourne une pixmap vide en cas d'erreur de chargement
        return pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)


class HeaderSection(QFrame):
    # Signal émis lorsque le bouton de menu est cliqué
    menu_toggled = pyqtSignal()

    def __init__(self, parent=None, title="AI Marketing Automation", app_name="Nova360 AI", slogan="AI Marketing & Management Auto"):
        # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions
        
        super().__init__(parent)
        self.dynamic_title = title  # Titre dynamique
        self.app_name = app_name    # Nom de l'application dynamique
        self.slogan = slogan        # Slogan dynamique
                # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        self.setup_ui()
    def switch_language(self, language):
        """Permet de changer la langue."""
        # if language == "en":
        #     self.translator.load("resources/lang/en_US/ui/header_translated.qm")
        # elif language == "fr":
        #     self.translator.load("resources/lang/fr_FR/ui/header_translated.qm")
        # elif language == "tr":
        #     self.translator.load("resources/lang/tr_TR/ui/header_translated.qm")
        # elif language == "ar":
        #     self.translator.load("resources/lang/ar_AR/ui/header_translated.qm")


        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','ui','header_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','ui','header_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','ui','header_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','ui','header_translated.qm'))

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
                border: 3px solid #4CAF50;
                border-radius: 10px;
                background-color: white;
                box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
            }
        """)
        layout = QHBoxLayout(self)
        main_layout = QVBoxLayout()
        # Titre de l'application (dynamique)
        self.title_label = QLabel(self.dynamic_title)
        self.title_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #2E7D32; padding: 10px;")
        layout.addWidget(self.title_label)

        # Logo du menu
        menu_logo_label = QLabel(self)
        menu_pixmap = ImageLoader.load_pixmap("resources/icons/robot-icons-30497.png", 100, 100)
        if not menu_pixmap.isNull():
            menu_logo_label.setPixmap(menu_pixmap)
        else:
            menu_logo_label.setText(self.tr("Logo non disponible"))
        menu_logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(menu_logo_label)

        # Nom de l'application et slogan (dynamiques)
        app_info_layout = QVBoxLayout()
        app_name_label = QLabel(self.app_name)
        app_name_label.setFont(QFont("Arial", 24, QFont.Bold))
        app_name_label.setAlignment(Qt.AlignCenter)
        app_name_label.setStyleSheet("color: #2E7D32;")
        app_info_layout.addWidget(app_name_label)

        subtitle_label = QLabel(self.slogan)
        subtitle_label.setFont(QFont("Arial", 12))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #555555;")
        app_info_layout.addWidget(subtitle_label)
        layout.addLayout(app_info_layout)

        # Logo GIF
        gif_logo_label = QLabel(self)
        gif_pixmap = ImageLoader.load_pixmap("resources/icons/robot-256.gif", 100, 100)
        if not gif_pixmap.isNull():
            gif_logo_label.setPixmap(gif_pixmap)
        else:
            gif_logo_label.setText(self.tr("GIF non disponible"))
        gif_logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(gif_logo_label)

        # Barre de recherche
        search_bar = QLineEdit()
        search_bar.setPlaceholderText(self.tr("Rechercher..."))
        search_bar.setFont(QFont("Arial", 14))
        search_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #CCCCCC;
                border-radius: 8px;
                padding: 8px;
                background-color: white;
            }
        """)
        search_bar.returnPressed.connect(self.on_search)  # Action lors de la recherche
        layout.addWidget(search_bar)

         # Bouton de menu toggle
        toggle_button = QPushButton(self.tr("≡"))
        toggle_button.setFont(QFont("Arial", 16, QFont.Bold))
        toggle_button.setIcon(QIcon(QPixmap("resources/icons/Delacro-Id-Start-Menu.256.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        toggle_button.clicked.connect(self.toggle_side_menu)
        layout.addWidget(toggle_button)
       # Espacement avant les boutons
        main_layout.addSpacing(20)

        # Menu latéral rétractable
        self.side_menu = QWidget(self)
        self.side_menu.setGeometry(0, 80, 200, 600)  # Positionné un peu plus haut
        self.side_menu.setStyleSheet("""
            QWidget {
                background-color: #4CAF50;
            }
            QPushButton {
                background-color: #66BB6A;
                color: white;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #81C784;
            }
        """)
        self.side_menu.setVisible(False)  # Cache le menu latéral au départ

        self.side_menu_animation = QPropertyAnimation(self.side_menu, b"geometry")
        self.side_menu_animation.setDuration(500)
        self.side_menu_animation.setEasingCurve(QEasingCurve.InOutQuad)

        # Ajouter des boutons au menu latéral
        side_menu_layout = QVBoxLayout()
        side_menu_layout.setContentsMargins(10, 10, 10, 10)
        self.side_menu.setLayout(side_menu_layout)

        # Boutons du menu latéral
        side_buttons = [
            ("Accueil", "resources/icons/home-icon.png"),
            ("Paramètres", "resources/icons/settings-icon.png"),
            ("Aide", "resources/icons/help-icon.png"),
            ("À propos", "resources/icons/info-icon.png"),
            ("Quitter", "resources/icons/exit-icon.png"),
        ]

        for text, icon in side_buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))
            button.setIcon(QIcon(QPixmap(icon).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
            button.setIconSize(QPixmap(icon).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation).size())
            button.clicked.connect(lambda _, btn=text: self.side_menu_action(btn))
            side_menu_layout.addWidget(button)

        # Ajustement de la responsivité des éléments dans le layout
        layout.setStretch(0, 2)  # Ajuste la largeur du titre
        layout.setStretch(1, 1)  # Ajuste la taille de l'icône du menu
        layout.setStretch(2, 2)  # Ajuste la largeur du label app_info_layout
        layout.setStretch(3, 1)  # Ajuste la taille de l'icône GIF
        layout.setStretch(4, 3)  # Ajuste la largeur de la barre de recherche
        layout.setStretch(5, 1)  # Ajuste la taille du bouton de menu
    def side_menu_action(self, action):
        # Actions pour les boutons du menu latéral
        if action == "Accueil":
            QMessageBox.information(self, self.tr("Accueil"),  "Bienvenue à l'accueil!")
        elif action == "Paramètres":
            QMessageBox.information(self, self.tr("Paramètres"),  "Ouvrir les paramètres...")
        elif action == "Aide":
            QMessageBox.information(self, self.tr("Aide"),  "Ouvrir l'aide...")
        elif action == "À propos":
            QMessageBox.information(self, self.tr("À propos"),  "AI FB ROBOT PRO v1.0\n© 2024 Nova360 Pro")
        elif action == "Quitter":
            self.close()

    def create_button(self, text, icon_path, icon_size):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 16, QFont.Bold))
        button.setIcon(QIcon(ImageLoader.load_pixmap(icon_path, icon_size, icon_size)))
        button.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 8px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        return button
    def toggle_side_menu(self):
        # Animation pour afficher ou masquer le menu latéral
        if self.side_menu.isVisible():
            self.side_menu_animation.setStartValue(QRect(0, 80, 200, 600))
            self.side_menu_animation.setEndValue(QRect(0, 80, 0, 600))
            self.side_menu_animation.start()
            self.side_menu.setVisible(False)
        else:
            self.side_menu.setVisible(True)
            self.side_menu_animation.setStartValue(QRect(0, 80, 0, 600))
            self.side_menu_animation.setEndValue(QRect(0, 80, 200, 600))
            self.side_menu_animation.start()

    def on_toggle_clicked(self):
        self.menu_toggled.emit()  # Émettre le signal lorsque le bouton de menu est cliqué

    def on_search(self):
        query = self.findChild(QLineEdit).text()
        print(f"Rechercher : {query}")
        # Logique de recherche à ajouter ici

    def update_title(self, new_title):
        """Méthode pour changer dynamiquement le titre."""
        self.title_label.setText(new_title)
        self.dynamic_title = new_title


# Test de la classe avec changement de titre, nom d'application et slogan dynamiques
class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Passer des valeurs personnalisées pour le titre, le nom de l'application et le slogan
        self.header_section = HeaderSection(self, title="AI Marketing Automation", app_name="Nova360 AI", slogan="AI Marketing & Management Auto")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.header_section)

        # Bouton pour changer dynamiquement le titre
        change_title_button = QPushButton(self.tr("Changer le titre"))
        change_title_button.clicked.connect(self.change_title)
        main_layout.addWidget(change_title_button)

    def change_title(self):
        new_title = "Titre mis à jour dynamiquement!"
        self.header_section.update_title(new_title)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = TestWindow()
    window.setWindowTitle("Test Header Section")
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
