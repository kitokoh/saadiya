# import json
# # from imports import *
# import os
# from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
# from PyQt5.QtCore import Qt, QTranslator, QLocale
# from PyQt5.QtCore import Qt, pyqtSignal, QRect
# from PyQt5.QtGui import QFont, QPixmap, QIcon
# from PyQt5.QtWidgets import (
#     QApplication, QAction, QMainWindow, QLabel, QPushButton, QVBoxLayout,
#     QHBoxLayout, QWidget, QLineEdit, QScrollArea, QFrame, QMenu, QMenuBar, QMessageBox
# )
# from PyQt5.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QFrame, QPushButton, QWidget

# from translation import TranslatorManager  # Importer le gestionnaire de traductions
# from translation import TranslatorManager  # Importer le gestionnaire de traductions

# user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

# class ImageLoader:
#     """Classe utilitaire pour charger et redimensionner les images."""
#     @staticmethod
#     def load_pixmap(path, width, height):
#         pixmap = QPixmap(path)
#         if pixmap.isNull():
#             return QPixmap()  # Retourne une pixmap vide en cas d'erreur de chargement
#         return pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)


# class HeaderSection(QFrame):
#     # Signal émis lorsque le bouton de menu est cliqué
#     menu_toggled = pyqtSignal()

#     def __init__(self, parent=None, title="AI Marketing Automation", app_name="Leopardo AI", slogan="AI Marketing & Management Auto"):
#         # Initialiser le traducteur
#         self.translator = QTranslator()
#         self.init_language()  # Initialisation de la langue après la création des actions
        
#         super().__init__(parent)
#         self.dynamic_title = title  # Titre dynamique
#         self.app_name = app_name    # Nom de l'application dynamique
#         self.slogan = slogan        # Slogan dynamique
#                 # Initialiser et charger les traductions
#         self.translator_manager = TranslatorManager()
#         self.translator_manager.load_translations()
#         self.setup_ui()
#     def switch_language(self, language):
#         """Permet de changer la langue."""
#         # if language == "en":
#         #     self.translator.load("resources/lang/en_US/ui/header_translated.qm")
#         # elif language == "fr":
#         #     self.translator.load("resources/lang/fr_FR/ui/header_translated.qm")
#         # elif language == "tr":
#         #     self.translator.load("resources/lang/tr_TR/ui/header_translated.qm")
#         # elif language == "ar":
#         #     self.translator.load("resources/lang/ar_AR/ui/header_translated.qm")


#         if language == "en":
#             self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','ui','header_translated.qm'))
#         elif language == "fr":
#             self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','ui','header_translated.qm'))
#         elif language == "tr":
#             self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','ui','header_translated.qm'))
#         elif language == "ar":
#             self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','ui','header_translated.qm'))
#         elif language == "pt":
#             self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','pt_BR','ui','header_translated.qm'))

#         # Installer le traducteur pour appliquer la nouvelle langue
#         QApplication.instance().installTranslator(self.translator)
        
#             # Sauvegarder le choix de l'utilisateur
#         self.save_language_choice(language)


#         # Réappliquer la traduction sur tous les éléments visibles de l'interface
#         self.retranslateUi()

#     def save_language_choice(self, language):
#         """Sauvegarde le choix de langue de l'utilisateur dans un fichier JSON."""
#         preferences = {'language': language}
#         with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
#             json.dump(preferences, f)
#     def retranslateUi(self):
#         """Recharge les textes traduits dans l'interface."""
#         # self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
#         # # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
#         # # Par exemple, pour les actions du menu :
#         # self.instance_action.setText(self.tr('Instance'))
#         # self.media_action.setText(self.tr('Médias'))
#         # self.group_action.setText(self.tr('Groupes'))
#         # self.about_action.setText(self.tr('About'))
#         # self.certificate_action.setText(self.tr('Certif'))
#         # self.language_menu.setTitle(self.tr('Langue'))
#         pass
#     def init_language(self):
#         """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
#         # Vérifiez si le fichier de préférences existe
#         if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
#             with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
#                 preferences = json.load(f)
#                 selected_language = preferences.get('language', 'en')  # Par défaut à l'anglais si non trouvé
#         else:
#             # Obtenir le code de langue du système
#             system_locale = QLocale.system().name()[:2]  # Par exemple: 'fr', 'en', 'tr', etc.

#             # Dictionnaire pour mapper les codes de langue aux traductions
#             language_map = {
#                 'en': 'en',
#                 'fr': 'fr',
#                 'tr': 'tr',
#                 'ar': 'ar',
#                 'pt': 'pt',

#             }

#             # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
#             selected_language = language_map.get(system_locale, 'en')

#         self.switch_language(selected_language)

#     def setup_ui(self):
#         self.setStyleSheet("""
#             QFrame {
#                 background-image: url('resources/images/back.webp');
#                 background-position: center;
#                 background-size: cover;
#                 border: 3px solid #4CAF50;
#                 border-radius: 10px;
#                 background-color: white;
#                 box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
#             }
#         """)
#         layout = QHBoxLayout(self)
#         main_layout = QVBoxLayout()
#         # Titre de l'application (dynamique)
#         self.title_label = QLabel(self.dynamic_title)
#         self.title_label.setFont(QFont("Arial", 28, QFont.Bold))
#         self.title_label.setAlignment(Qt.AlignCenter)
#         self.title_label.setStyleSheet("color: #2E7D32; padding: 10px;")
#         layout.addWidget(self.title_label)

#         # Logo du menu robot-icons-30504.png
#         menu_logo_label = QLabel(self)
#         #menu_pixmap = ImageLoader.load_pixmap("resources/icons/robot-icons-30504.png", 100, 100)
#         menu_pixmap = ImageLoader.load_pixmap("resources/icons/robot-icons-30497-Windows.ico", 100, 100)

#         if not menu_pixmap.isNull():
#             menu_logo_label.setPixmap(menu_pixmap)
#         else:
#             menu_logo_label.setText(self.tr("Logo non disponible"))
#         menu_logo_label.setAlignment(Qt.AlignCenter)
#         layout.addWidget(menu_logo_label)

#         # Nom de l'application et slogan (dynamiques)
#         app_info_layout = QVBoxLayout()
#         app_name_label = QLabel(self.app_name)
#         app_name_label.setFont(QFont("Arial", 24, QFont.Bold))
#         app_name_label.setAlignment(Qt.AlignCenter)
#         app_name_label.setStyleSheet("color: #2E7D32;")
#         app_info_layout.addWidget(app_name_label)

#         subtitle_label = QLabel(self.slogan)
#         subtitle_label.setFont(QFont("Arial", 12))
#         subtitle_label.setAlignment(Qt.AlignCenter)
#         subtitle_label.setStyleSheet("color: #555555;")
#         app_info_layout.addWidget(subtitle_label)
#         layout.addLayout(app_info_layout)

#         # Logo GIF
#         gif_logo_label = QLabel(self)
#         gif_pixmap = ImageLoader.load_pixmap("resources/icons/robot-256.png", 100, 100)
#         if not gif_pixmap.isNull():
#             gif_logo_label.setPixmap(gif_pixmap)
#         else:
#             gif_logo_label.setText(self.tr("GIF non disponible"))
#         gif_logo_label.setAlignment(Qt.AlignCenter)
#         layout.addWidget(gif_logo_label)

#         # Barre de recherche
#         search_bar = QLineEdit()
#         search_bar.setPlaceholderText(self.tr("Rechercher..."))
#         search_bar.setFont(QFont("Arial", 14))
#         search_bar.setStyleSheet("""
#             QLineEdit {
#                 border: 2px solid #CCCCCC;
#                 border-radius: 8px;
#                 padding: 8px;
#                 background-color: white;
#             }
#         """)
#         search_bar.returnPressed.connect(self.on_search)  # Action lors de la recherche
#         layout.addWidget(search_bar)

#          # Bouton de menu toggle
#         toggle_button = QPushButton(self.tr("≡"))
#         toggle_button.setFont(QFont("Arial", 16, QFont.Bold))
#         toggle_button.setIcon(QIcon(QPixmap("resources/icons/robot-icons-30497-Windows.ico").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
#         toggle_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #2E7D32;
#                 color: white;
#                 padding: 10px;
#                 border: none;
#                 border-radius: 8px;
#             }
#             QPushButton:hover {
#                 background-color: #388E3C;
#             }
#         """)
#         toggle_button.clicked.connect(self.toggle_side_menu)
#         layout.addWidget(toggle_button)
#        # Espacement avant les boutons
#         main_layout.addSpacing(20)

#         # Menu latéral rétractable
#         self.side_menu = QWidget(self)
#         self.side_menu.setGeometry(0, 80, 200, 600)  # Positionné un peu plus haut
#         self.side_menu.setStyleSheet("""
#             QWidget {
#                 background-color: #4CAF50;
#             }
#             QPushButton {
#                 background-color: #66BB6A;
#                 color: white;
#                 border: none;
#                 padding: 15px;
#                 text-align: left;
#                 font-size: 16px;
#             }
#             QPushButton:hover {
#                 background-color: #81C784;
#             }
#         """)
#         self.side_menu.setVisible(False)  # Cache le menu latéral au départ

#         self.side_menu_animation = QPropertyAnimation(self.side_menu, b"geometry")
#         self.side_menu_animation.setDuration(500)
#         self.side_menu_animation.setEasingCurve(QEasingCurve.InOutQuad)

#         # Ajouter des boutons au menu latéral
#         side_menu_layout = QVBoxLayout()
#         side_menu_layout.setContentsMargins(10, 10, 10, 10)
#         self.side_menu.setLayout(side_menu_layout)

#         # Boutons du menu latéral
#         side_buttons = [
#             ("Accueil", "resources/icons/robot-icons-30504-Windows.ico"),
#             ("Paramètres", "resources/icons/camera-icon-59-Windows.ico"),
#             ("Aide", "resources/icons/information-icon-6055-Windows.ico"),
#             ("À propos", "resources/icons/Hopstarter-Soft-Scraps-Edit-Document.ico"),
#             ("Quitter", "resources/icons/robot-256.ico"),
#         ]

#         for text, icon in side_buttons:
#             button = QPushButton(text)
#             button.setFont(QFont("Arial", 14))
#             button.setIcon(QIcon(QPixmap(icon).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
#             button.setIconSize(QPixmap(icon).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation).size())
#             button.clicked.connect(lambda _, btn=text: self.side_menu_action(btn))
#             side_menu_layout.addWidget(button)

#         # Ajustement de la responsivité des éléments dans le layout
#         layout.setStretch(0, 2)  # Ajuste la largeur du titre
#         layout.setStretch(1, 1)  # Ajuste la taille de l'icône du menu
#         layout.setStretch(2, 2)  # Ajuste la largeur du label app_info_layout
#         layout.setStretch(3, 1)  # Ajuste la taille de l'icône GIF
#         layout.setStretch(4, 3)  # Ajuste la largeur de la barre de recherche
#         layout.setStretch(5, 1)  # Ajuste la taille du bouton de menu
#     def side_menu_action(self, action):
#         # Actions pour les boutons du menu latéral
#         if action == "Accueil":
#             QMessageBox.information(self, self.tr("Accueil"),  "Bienvenue à l'accueil!")
#         elif action == "Paramètres":
#             QMessageBox.information(self, self.tr("Paramètres"),  "Ouvrir les paramètres...")
#         elif action == "Aide":
#             QMessageBox.information(self, self.tr("Aide"),  "Ouvrir l'aide...")
#         elif action == "À propos":
#             QMessageBox.information(self, self.tr("À propos"),  "AI FB ROBOT PRO v1.0\n© 2024 Leopardo Pro")
#         elif action == "Quitter":
#             self.close()

#     def create_button(self, text, icon_path, icon_size):
#         button = QPushButton(text)
#         button.setFont(QFont("Arial", 16, QFont.Bold))
#         button.setIcon(QIcon(ImageLoader.load_pixmap(icon_path, icon_size, icon_size)))
#         button.setStyleSheet("""
#             QPushButton {
#                 background-color: #2E7D32;
#                 color: white;
#                 padding: 10px;
#                 border: none;
#                 border-radius: 8px;
#                 box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
#                 transition: background-color 0.3s ease;
#             }
#             QPushButton:hover {
#                 background-color: #388E3C;
#             }
#         """)
#         return button
#     def toggle_side_menu(self):
#         # Animation pour afficher ou masquer le menu latéral
#         if self.side_menu.isVisible():
#             self._extracted_from_toggle_side_menu_4(200, 0)
#             self.side_menu.setVisible(False)
#         else:
#             self.side_menu.setVisible(True)
#             self._extracted_from_toggle_side_menu_4(0, 200)

#     # TODO Rename this here and in `toggle_side_menu`
#     def _extracted_from_toggle_side_menu_4(self, arg0, arg1):
#         self.side_menu_animation.setStartValue(QRect(0, 80, arg0, 600))
#         self.side_menu_animation.setEndValue(QRect(0, 80, arg1, 600))
#         self.side_menu_animation.start()

#     def on_toggle_clicked(self):
#         self.menu_toggled.emit()  # Émettre le signal lorsque le bouton de menu est cliqué

#     def on_search(self):
#         query = self.findChild(QLineEdit).text()
#         print(f"Rechercher : {query}")
#         # Logique de recherche à ajouter ici

#     def update_title(self, new_title):
#         """Méthode pour changer dynamiquement le titre."""
#         self.title_label.setText(new_title)
#         self.dynamic_title = new_title


# # Test de la classe avec changement de titre, nom d'application et slogan dynamiques
# class TestWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         # Passer des valeurs personnalisées pour le titre, le nom de l'application et le slogan
#         self.header_section = HeaderSection(self, title="AI Marketing Automation", app_name="Leopardo AI", slogan="AI Marketing & Management Auto")
#         self.setup_ui()

#     def setup_ui(self):
#         main_layout = QVBoxLayout(self)
#         main_layout.addWidget(self.header_section)

#         # Bouton pour changer dynamiquement le titre
#         change_title_button = QPushButton(self.tr("Changer le titre"))
#         change_title_button.clicked.connect(self.change_title)
#         main_layout.addWidget(change_title_button)

#     def change_title(self):
#         new_title = "Titre mis à jour dynamiquement!"
#         self.header_section.update_title(new_title)


# if __name__ == "__main__":
#     from PyQt5.QtWidgets import QApplication
#     import sys

#     app = QApplication(sys.argv)
#     window = TestWindow()
#     window.setWindowTitle("Test Header Section")
#     window.resize(800, 600)
#     window.show()
#     sys.exit(app.exec_())
import json
import os
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSize, QPoint
from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor, QPainter, QBrush, QLinearGradient
from PyQt5.QtWidgets import (
    QApplication, QLabel, QToolButton, QHBoxLayout,
    QVBoxLayout, QWidget, QFrame, QMenu, QSizeGrip
)
from PyQt5.QtWidgets import QSizePolicy, QSpacerItem
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
from translation import TranslatorManager  # Importer le gestionnaire de traductions

class HeaderSection(QFrame):
    """
    Header moderne inspiré des interfaces Office (Word/Excel) avec :
    - Menu ruban stylisé
    - Animations fluides
    - Thème personnalisable
    - Boutons d'actions contextuels
    """
    
    menu_toggled = pyqtSignal()
    quick_action_triggered = pyqtSignal(str)
    language_changed = pyqtSignal(str)
    theme_changed = pyqtSignal(str)

    def __init__(self, parent=None, title="AI Marketing Automation", 
                 app_name="Leopardo AI", slogan="AI Marketing & Management Auto"):
        super().__init__(parent)
        self.setObjectName("HeaderSection")
        
        # Configuration initiale
        self.translator = QTranslator()
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        
        self.dynamic_title = title
        self.app_name = app_name
        self.slogan = slogan
        self.current_theme = "light"  # Par défaut
        
        # Initialisation UI
        self.setup_ui()
        self.setup_animations()
        self.init_language()
        self.apply_theme(self.current_theme)

    def init_language(self):
        """Initialise la langue à partir des préférences utilisateur"""
        lang_file = os.path.join(user_data_dir, 'resources', 'settings.json')
        try:
            if os.path.exists(lang_file):
                with open(lang_file, 'r') as f:
                    preferences = json.load(f)
                    lang = preferences.get('language', 'en')
            else:
                system_locale = QLocale.system().name()[:2]
                lang = 'en' if system_locale not in ['fr', 'tr', 'ar', 'pt'] else system_locale
            
            self.change_language(lang)
        except Exception as e:
            print(f"Error loading language: {e}")
            self.change_language('en')

    def change_language(self, language):
        """Change la langue de l'interface"""
        try:
            lang_path = os.path.join(user_data_dir, 'resources', 'lang',
                                   f'{language}_{language.upper()}', 'ui', 'header_translated.qm')
            if os.path.exists(lang_path):
                if self.translator.load(lang_path):
                    QApplication.instance().installTranslator(self.translator)
                    self.save_language_preference(language)
                    self.retranslate_ui()
        except Exception as e:
            print(f"Error changing language: {e}")

    def save_language_preference(self, language):
        """Sauvegarde la préférence de langue"""
        try:
            os.makedirs(os.path.dirname(user_data_dir), exist_ok=True)
            pref_path = os.path.join(user_data_dir, 'resources', 'settings.json')
            with open(pref_path, 'w') as f:
                json.dump({'language': language, 'theme': self.current_theme}, f)
        except Exception as e:
            print(f"Error saving preferences: {e}")

    def retranslate_ui(self):
        """Recharge les textes traduits"""
        self.title_label.setText(self.tr(self.dynamic_title))
        self.slogan_label.setText(self.tr(self.slogan))
        
        # Mettre à jour les tooltips
        for btn, (_, _, tooltip) in zip(self.action_buttons, self.get_action_items()):
            btn.setToolTip(self.tr(tooltip))

    def setup_ui(self):
        """Configuration de l'interface utilisateur moderne"""
        self.setMinimumHeight(80)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Layout principal avec marges réduites
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 4, 8, 4)
        main_layout.setSpacing(6)

        # Bouton menu avec animation
        self.menu_button = self.create_icon_button(
            "resources/icons/menu_icon.png", 
            self.tr("Menu principal"),
            size=QSize(32, 32),
            toggle=True
        )
        self.menu_button.clicked.connect(self.toggle_side_menu)
        main_layout.addWidget(self.menu_button)

        # Séparateur visuel
        main_layout.addWidget(self.create_separator())

        # Logo application
        self.logo_label = QLabel()
        logo_pix = self.load_scaled_pixmap("resources/icons/robot-256.png", QSize(36, 36))
        self.logo_label.setPixmap(logo_pix)
        self.logo_label.setCursor(Qt.PointingHandCursor)
        main_layout.addWidget(self.logo_label)

        # Séparateur visuel
        main_layout.addWidget(self.create_separator())

        # Titre et slogan dans un layout vertical
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        
        self.title_label = QLabel(self.dynamic_title)
        self.title_label.setObjectName("HeaderTitle")
        self.title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        
        self.slogan_label = QLabel(self.slogan)
        self.slogan_label.setObjectName("HeaderSlogan")
        self.slogan_label.setFont(QFont("Segoe UI", 8))
        
        title_layout.addWidget(self.title_label)
        # title_layout.addWidget(self.slogan_label)
        main_layout.addLayout(title_layout, stretch=1)

        # Barre d'outils rapide (style ruban)
        self.setup_quick_access_toolbar(main_layout)

        # Espace flexible
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Boutons de contrôle de fenêtre (minimiser, maximiser, fermer)
        # self.setup_window_controls(main_layout)

        # Menu latéral
        self.side_menu = QWidget(self)
        self.side_menu.setObjectName("SideMenu")
        self.setup_side_menu()

    def setup_quick_access_toolbar(self, main_layout):
        """Configure la barre d'outils rapide comme dans Office"""
        self.action_buttons = []
        
        # Création des boutons d'action
        for emoji, action, tooltip in self.get_action_items():
            btn = self.create_tool_button(emoji, self.tr(tooltip))
            btn.clicked.connect(lambda _, a=action: self.quick_action_triggered.emit(a))
            self.action_buttons.append(btn)
            main_layout.addWidget(btn)

    def get_action_items(self):
        """Retourne les éléments de la barre d'outils"""
        return [
            ("📄", "new", "Nouveau fichier (Ctrl+N)"),
            ("📂", "open", "Ouvrir (Ctrl+O)"),
            ("💾", "save", "Enregistrer (Ctrl+S)"),
            ("🔍", "search", "Rechercher (Ctrl+F)"),
            ("🖨️", "print", "Imprimer (Ctrl+P)")
            # ("↻", "refresh", "Actualiser (F5)")
        ]

    def setup_window_controls(self, layout):
        """Configure les boutons de contrôle de fenêtre"""
        controls = [
            ("_", "minimize", self.tr("Minimiser")),
            ("🗖", "maximize", self.tr("Maximiser")),
            ("✕", "close", self.tr("Fermer"))
        ]

        control_buttons = []
        for text, action, tooltip in controls:
            btn = self.create_control_button(text, tooltip)
            btn.clicked.connect(lambda _, a=action: self.window_control_action(a))
            control_buttons.append(btn)
            layout.addWidget(btn)

    def create_control_button(self, text, tooltip):
        """Crée un bouton de contrôle de fenêtre stylisé"""
        btn = QToolButton()
        btn.setText(text)
        btn.setToolTip(tooltip)
        btn.setFixedSize(32, 24)
        btn.setFont(QFont("Segoe UI Symbol", 10))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setObjectName("WindowControlButton")
        return btn

    def create_tool_button(self, icon_or_text, tooltip, size=QSize(28, 28)):
        """Crée un bouton d'outil moderne"""
        btn = QToolButton()
        
        if isinstance(icon_or_text, str) and len(icon_or_text) == 1:  # Emoji
            btn.setText(icon_or_text)
            btn.setFont(QFont("Segoe UI Emoji", 12))
        else:  # Chemin d'icône
            btn.setIcon(QIcon(icon_or_text))
            btn.setIconSize(size)
        
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedSize(size)
        btn.setObjectName("ToolButton")
        return btn

    def create_icon_button(self, icon_path, tooltip, size=QSize(24, 24), toggle=False):
        """Crée un bouton avec icône"""
        btn = QToolButton()
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(size)
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setCheckable(toggle)
        btn.setFixedSize(size.width() + 8, size.height() + 8)
        btn.setObjectName("IconButton")
        return btn

    def create_separator(self):
        """Crée un séparateur vertical"""
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setLineWidth(1)
        separator.setFixedHeight(24)
        separator.setObjectName("Separator")
        return separator

    def load_scaled_pixmap(self, path, size):
        """Charge une image et la redimensionne"""
        if os.path.exists(path):
            return QPixmap(path).scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return QPixmap(size)

    def setup_side_menu(self):
        """Configure le menu latéral moderne"""
        self.side_menu.setFixedWidth(280)
        self.side_menu.move(-280, 0)
        self.side_menu.setObjectName("SideMenu")
        
        layout = QVBoxLayout(self.side_menu)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(5)

        # En-tête du menu
        menu_header = QLabel(self.app_name)
        menu_header.setAlignment(Qt.AlignCenter)
        menu_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        menu_header.setObjectName("MenuHeader")
        layout.addWidget(menu_header)

        layout.addWidget(self.create_separator())

        # Items du menu
        for text, icon, action in self.get_menu_items():
            btn = self.create_menu_button(text, icon, action)
            layout.addWidget(btn)

        layout.addStretch()

        # Pied de page du menu
        footer = QFrame()
        footer.setObjectName("MenuFooter")
        footer_layout = QHBoxLayout(footer)
        
        theme_btn = self.create_icon_button(
            "resources/icons/theme.png", 
            self.tr("Changer de thème"),
            QSize(20, 20)
        )
        theme_btn.clicked.connect(self.toggle_theme)
        
        footer_layout.addWidget(theme_btn)
        footer_layout.addStretch()
        
        settings_btn = self.create_icon_button(
            "resources/icons/settings.png", 
            self.tr("Paramètres"),
            QSize(20, 20)
        )
        settings_btn.clicked.connect(lambda: self.handle_menu_action("settings"))
        
        footer_layout.addWidget(settings_btn)
        layout.addWidget(footer)

    def get_menu_items(self):
        """Retourne les éléments du menu"""
        return [
            (self.tr("Accueil"), "home.png", "home"),
            (self.tr("Projets"), "projects.png", "projects"),
            (self.tr("Analytique"), "analytics.png", "analytics"),
            (self.tr("Historique"), "history.png", "history"),
            (self.tr("Favoris"), "favorites.png", "favorites"),
            (self.tr("Partage"), "share.png", "share")
        ]

    def create_menu_button(self, text, icon, action):
        """Crée un bouton de menu moderne"""
        btn = QToolButton()
        btn.setText(text)
        btn.setToolTip(text)
        
        if icon:
            btn.setIcon(QIcon(f"resources/icons/{icon}"))
            btn.setIconSize(QSize(20, 20))
        
        btn.setCursor(Qt.PointingHandCursor)
        btn.setObjectName("MenuButton")
        btn.clicked.connect(lambda _, a=action: self.handle_menu_action(a))
        return btn

    def setup_animations(self):
        """Configure les animations modernes"""
        # Animation du menu latéral
        self.menu_animation = QPropertyAnimation(self.side_menu, b"pos")
        self.menu_animation.setDuration(300)
        self.menu_animation.setEasingCurve(QEasingCurve.OutQuint)
        
        # Animation de fondu pour les boutons
        self.button_animations = {}

    def toggle_side_menu(self):
        """Bascule le menu latéral avec animation"""
        if self.side_menu.isVisible():
            self.menu_animation.setStartValue(QPoint(0, 0))
            self.menu_animation.setEndValue(QPoint(-self.side_menu.width(), 0))
            self.menu_animation.finished.connect(self.side_menu.hide)
        else:
            self.side_menu.show()
            self.side_menu.raise_()
            self.menu_animation.setStartValue(QPoint(-self.side_menu.width(), 0))
            self.menu_animation.setEndValue(QPoint(0, 0))
            self.menu_animation.finished.disconnect()
        
        self.menu_animation.start()
        self.menu_toggled.emit()

    def toggle_theme(self):
        """Bascule entre les thèmes clair et sombre"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(self.current_theme)
        self.theme_changed.emit(self.current_theme)
        self.save_language_preference(QLocale().name()[:2])  # Sauvegarde aussi le thème

    def apply_theme(self, theme):
        """Applique un thème à l'interface"""
        if theme == "dark":
            self.setStyleSheet("""
                #HeaderSection {
                    background-color: #2d2d2d;
                    border-bottom: 1px solid #1e1e1e;
                }
                QLabel#HeaderTitle {
                    color: #ffffff;
                }
                QLabel#HeaderSlogan {
                    color: #aaaaaa;
                }
                #ToolButton, #IconButton {
                    background: transparent;
                    color: #ffffff;
                }
                #ToolButton:hover, #IconButton:hover {
                    background: #3d3d3d;
                    border-radius: 4px;
                }
                #WindowControlButton {
                    background: transparent;
                    color: #ffffff;
                }
                #WindowControlButton:hover {
                    background: #3d3d3d;
                }
                #WindowControlButton:hover:last-child {
                    background: #e81123;
                }
                #SideMenu {
                    background-color: #252526;
                    border-right: 1px solid #1e1e1e;
                }
                #MenuButton {
                    text-align: left;
                    padding: 8px 16px;
                    color: #ffffff;
                    background: transparent;
                }
                #MenuButton:hover {
                    background: #2a2d2e;
                }
                #Separator {
                    background: #1e1e1e;
                }
            """)
        else:  # Light theme
            self.setStyleSheet("""
                #HeaderSection {
                    background-color: #ffffff;
                    border-bottom: 1px solid #e0e0e0;
                }
                QLabel#HeaderTitle {
                    color: #000000;
                }
                QLabel#HeaderSlogan {
                    color: #666666;
                }
                #ToolButton, #IconButton {
                    background: transparent;
                    color: #333333;
                }
                #ToolButton:hover, #IconButton:hover {
                    background: #f0f0f0;
                    border-radius: 4px;
                }
                #WindowControlButton {
                    background: transparent;
                    color: #333333;
                }
                #WindowControlButton:hover {
                    background: #e5e5e5;
                }
                #WindowControlButton:hover:last-child {
                    background: #e81123;
                    color: white;
                }
                #SideMenu {
                    background-color: #f6f6f6;
                    border-right: 1px solid #e0e0e0;
                }
                #MenuButton {
                    text-align: left;
                    padding: 8px 16px;
                    color: #333333;
                    background: transparent;
                }
                #MenuButton:hover {
                    background: #e5e5e5;
                }
                #Separator {
                    background: #e0e0e0;
                }
            """)

    def window_control_action(self, action):
        """Gère les actions des boutons de contrôle de fenêtre"""
        window = self.window()
        if action == "minimize":
            window.showMinimized()
        elif action == "maximize":
            if window.isMaximized():
                window.showNormal()
            else:
                window.showMaximized()
        elif action == "close":
            window.close()

    def handle_menu_action(self, action):
        """Gère les actions du menu"""
        print(f"Action sélectionnée: {action}")
        if action == "home":
            self.update_title(self.tr("Accueil"))
        elif action == "settings":
            self.quick_action_triggered.emit("open_settings")

    def update_title(self, new_title):
        """Met à jour le titre dynamiquement"""
        self.title_label.setText(new_title)
        self.dynamic_title = new_title

    def paintEvent(self, event):
        """Dessine un dégradé de fond si nécessaire"""
        painter = QPainter(self)
        if self.current_theme == "dark":
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor("#2d2d2d"))
            gradient.setColorAt(1, QColor("#1e1e1e"))
            painter.fillRect(self.rect(), gradient)
        else:
            super().paintEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    
    header = HeaderSection()
    header.show()
    
    app.exec_()