import sys
import os
import subprocess

from PyQt5.QtWidgets import (
    QApplication, QAction, QMainWindow, QLabel, QPushButton, QVBoxLayout, 
    QHBoxLayout, QWidget, QLineEdit, QScrollArea, QFrame, QMenu, QMenuBar, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from main_fb_robot import FaceMainWindow  # Importez votre page d'accueil
from ModulesUI.whasapping.main_wp_robot import WhatsMainWindow  # Importez votre page d'accueil

from ModulesUI.emailing.main_mail_robot import MailMainWindow  # Importez votre page d'accueil
from ModulesUI.adsPro.main_ads_robot import AdsMainWindow  # Importez votre page d'accueil
from ModulesUI.AutoBlog.main_blog_robot import BlogMainWindow  # Importez votre page d'accueil
from ModulesUI.branding.main_brand_robot import BrandMainWindow  # Importez votre page d'accueil
from ModulesUI.chatBot.main_chatbot_robot import ChatBotMainWindow  # Importez votre page d'accueil
from ModulesUI.insta.main_insta_robot import InstaMainWindow  # Importez votre page d'accueil
from ModulesUI.linkeding.main_linkeding_robot import LinkedingMainWindow  # Importez votre page d'accueil
#from Modules.pinterest.main_pin_robot import PinMainWindow  # Importez votre page d'accueil
from ModulesUI.reddit.main_reddit_robot import RedditMainWindow  # Importez votre page d'accueil
from ModulesUI.tiktok.main_tok_robot import TokMainWindow  # Importez votre page d'accueil
from ModulesUI.twitter.main_x_robot import XMainWindow  # Importez votre page d'accueil
from ModulesUI.youtube.main_ytb_robot import YtbMainWindow  # Importez votre page d'accueil
#from Modules.pinterest.main_pin_robot import PinMainWindow  # Importez votre page d'accueil
from translation import TranslatorManager  # Importer le gestionnaire de traductions
#pour changer la destinationet developper en local c  ext ici que ca se passe 
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
from ui.clientsBrand import Nosclient
from imports import *
class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()

        # Configuration principale de la fenêtre
        self.setWindowTitle("AI FB ROBOT PRO - Marketing Automation")
        self.setGeometry(100, 100, 1280, 800)  # Taille de la fenêtre
        self.setStyleSheet("background-color: #F5F5F5;")
        # Définir l'icône de la fenêtre
        self.setWindowIcon(QIcon('resources/icons/robot-icons-30497.png'))  # Spécifiez le chemin de l'icône

        # Créer un widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout principal en vertical
        main_layout = QVBoxLayout()

        # Menu en-tête
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Ajouter des menus à la barre de menu
        file_menu = self.menu_bar.addMenu("Fichier")
        edit_menu = self.menu_bar.addMenu("Édition")
        view_menu = self.menu_bar.addMenu("Vue")
        settings_menu = self.menu_bar.addMenu("Paramètres")

        # Créer des actions de menu
        exit_action = QAction("Quitter", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction("Nouvelle")
        file_menu.addAction("Ouvrir")
        file_menu.addAction(exit_action)

        edit_menu.addAction("Copier")
        edit_menu.addAction("Coller")

        view_menu.addAction("Aperçu")
        
        # Action pour changer de thème
        theme_action = QAction("Changer de thème", self)
        theme_action.triggered.connect(self.change_theme)
        settings_menu.addAction(theme_action)

        # Layout pour l'en-tête
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 10, 10, 10)

        # Ajouter un cadre 3D pour l'en-tête
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                border: 3px solid #4CAF50;
                border-radius: 10px;
                background-color: white;
                box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
            }
        """)
        header_frame.setLayout(header_layout)

        # Titre de l'application
        title_label = QLabel("AI Marketing Automation")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2E7D32; padding: 10px;")
        header_layout.addWidget(title_label)

        # Logo du menu
        menu_logo_label = QLabel(self)
        menu_pixmap = QPixmap("resources/icons/robot-icons-30497.png")
        menu_logo_label.setPixmap(menu_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        menu_logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(menu_logo_label)

        # Nom de l'application et slogan
        app_info_layout = QVBoxLayout()
        app_name_label = QLabel("Nova360 AI")
        app_name_label.setFont(QFont("Arial", 24, QFont.Bold))
        app_name_label.setAlignment(Qt.AlignCenter)
        app_name_label.setStyleSheet("color: #2E7D32;")
        app_info_layout.addWidget(app_name_label)

        # Slogan mis à jour
        subtitle_label = QLabel("AI Marketing & Management Auto") 
        subtitle_label.setFont(QFont("Arial", 12))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #555555;")
        app_info_layout.addWidget(subtitle_label)

        header_layout.addLayout(app_info_layout)

        # Logo GIF (plus grand)
        gif_logo_label = QLabel(self)
        gif_pixmap = QPixmap("resources/icons/robot-256.gif")  
        gif_logo_label.setPixmap(gif_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        gif_logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(gif_logo_label)

        # Barre de recherche
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Rechercher...")
        search_bar.setFont(QFont("Arial", 14))
        search_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #CCCCCC;
                border-radius: 8px;
                padding: 8px;  
                background-color: white;
            }
        """)
        header_layout.addWidget(search_bar)

        # Bouton de menu toggle
        toggle_button = QPushButton("≡")
        toggle_button.setFont(QFont("Arial", 16, QFont.Bold))
        toggle_button.setIcon(QIcon(QPixmap("resources/icons/frpr-demoİnstall.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
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
        header_layout.addWidget(toggle_button)

        # Ajouter l'en-tête au layout principal
        main_layout.addWidget(header_frame)

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
            ("Accueil", "resources/icons/robot-256.png"),
            ("Paramètres", "resources/icons/automated_8345946.png"),
            ("Aide", "resources/icons/information-icon-6055-Windows.ico"),
            ("À propos", "resources/icons/information-icon-6055-Windows.ico"),
            ("Quitter", "resources/icons/windows-icon-42333.png"),
        ]

        for text, icon in side_buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))
            button.setIcon(QIcon(QPixmap(icon).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
            button.setIconSize(QPixmap(icon).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation).size())
            button.clicked.connect(lambda _, btn=text: self.side_menu_action(btn))
            side_menu_layout.addWidget(button)

        # Layout pour les icônes et boutons du milieu
        middle_layout = QHBoxLayout()

        # Liste des fonctionnalités avec leurs icônes et couleur
        features = [
            ("FB Robot Pro", "resources/icons/facebook-icon-png-770.png", "#E91E63", self.open_facebook),
            ("WhatsApping", "resources/icons/whatsapp-512.png", "#4CAF50", self.open_whatsapp),
            ("Blogging", "resources/icons/article-marketing-3-512.png", "#4CAF50", self.open_blogging),
            ("Insta Pro", "resources/icons/pink-message-icon-12055.png", "#4CAF50", self.open_instagram),
            ("Ads Pro", "resources/icons/promotion-icon-png-3422.png", "#4CAF50", self.open_adsPro),
            ("Branding", "resources/icons/subscribe-png-574.png", "#4CAF50", self.open_branding),
            ("Emailing", "resources/icons/pink-message-icon-12045.png", "#4CAF50", self.open_Emailing),
        ]


        # Ajouter des boutons avec animation et icônes dynamiques
        for text, icon, color, func in features:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))  # Taille de police réduite
            button.setIcon(QIcon(QPixmap(icon).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)))  # Icônes plus petites
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
                QPushButton:pressed {{
                    background-color: {color};
                }}
            """)
            button.clicked.connect(func)  # Connecter chaque bouton à sa fonction respective

            middle_layout.addWidget(button)

        main_layout.addLayout(middle_layout)

        # Duplication des boutons avec modifications
        duplicate_features = [
            ("Twitter Bot", "resources/icons/aquicon-icon-18708.png", "#1DA1F2",self.open_twitter),
            ("LinkedIn Pro", "resources/icons/aquicon-icon-18717.png", "#0077B5",self.open_linkeding),
            ("Pinterest Bot", "resources/icons/available-updates-512.png", "#BD081C",self.open_pinterest),
            ("Snapchat Bot", "resources/icons/snapchat-icon-1707.png", "#FFFC00",self.open_snapchat),
            ("TikTok Pro", "resources/icons/diving-png-4436.png", "#010101",self.open_tiktok),
            ("Reddit Bot", "resources/icons/robot-icons-30506.png", "#FF4500",self.open_reddit),
            ("YouTube Pro", "resources/icons/youtube-logo-png-3580.png", "#FF0000",self.open_youtube),
        ]

        duplicate_layout = QHBoxLayout()

        for text, icon, color, func in duplicate_features:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))  # Taille de police réduite
            button.setIcon(QIcon(QPixmap(icon).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)))  # Icônes plus petites
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
                QPushButton:pressed {{
                    background-color: {color};
                }}
            """)
            button.clicked.connect(func)  # Connecter chaque bouton à sa fonction respective

            duplicate_layout.addWidget(button)

        main_layout.addLayout(duplicate_layout)

        # Ajouter un titre "Gestion Auto"
        gestion_auto_label = QLabel(self.tr("Autres Solutions"))
        gestion_auto_label.setFont(QFont("Arial", 20, QFont.Bold))
        gestion_auto_label.setAlignment(Qt.AlignCenter)
        gestion_auto_label.setStyleSheet("color: #2E7D32;")
        main_layout.addWidget(gestion_auto_label)

        # Section des boutons du bas
        bottom_layout = QHBoxLayout()

        bottom_buttons = [
            ("Full Marketing", "#4CAF50"),
            ("Auto GES", "#4CAF50"),
            ("Contact 360", "#4CAF50"),
            ("GES Auto", "#4CAF50"),
            ("SAV", "#E91E63"),
            ("ERP", "#4CAF50"),
            ("CRM360", "#E91E63")
        ]

        for text, color in bottom_buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    padding: 20px;
                    border-radius: 15px;
                }}
                QPushButton:hover {{
                    background-color: {self.lighten_color(color)};
                    transform: scale(1.05);
                }}
            """)
            button.clicked.connect(lambda _, btn=text: self.show_message(btn))  
            bottom_layout.addWidget(button)

        main_layout.addLayout(bottom_layout)


        client_layout = QHBoxLayout()
        self.clients=Nosclient()

        client_layout.addWidget(self.clients)
        main_layout.addLayout(client_layout)

        # Créer un pied de page modernisé
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(10, 10, 10, 10)

        footer_frame = QFrame()
        footer_frame.setStyleSheet("""
            QFrame {
                border: none;
                background-color: #2E7D32;
            }
        """)
        footer_frame.setLayout(footer_layout)

        # Texte du footer
        footer_text = QLabel("Politique de confidentialité | © 2024 Nova360 Pro - Tous droits réservés")
        footer_text.setFont(QFont("Arial", 10))
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setStyleSheet("color: white;")

        # Boutons dans le footer
        privacy_button = QPushButton("Politique de confidentialité")
        privacy_button.setFont(QFont("Arial", 10))
        privacy_button.setStyleSheet("""
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
        privacy_button.clicked.connect(lambda: self.open_link("https://www.turknovatech.com/privacy"))

        terms_button = QPushButton("Termes et Conditions")
        terms_button.setFont(QFont("Arial", 10))
        terms_button.setStyleSheet("""
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
        terms_button.clicked.connect(lambda: self.open_link("https://www.turknovatech.com/terms"))

        footer_layout.addWidget(privacy_button)
        footer_layout.addWidget(footer_text)
        footer_layout.addWidget(terms_button)

        main_layout.addWidget(footer_frame)

        # Ajouter le layout principal au widget central
        central_widget.setLayout(main_layout)

        self.show()
# Fonction pour ouvrir Facebook Robot
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','home_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','home_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','modules','home_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','modules','home_translated.qm'))

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

    def open_nova360(self):
        #self.hide()  # Masquer le module de connexion
        self.home_page = HomePage()  # Remplacez ceci par votre classe de page d'accueil
        self.home_page.show()  # Afficher la page d'accueil
    def open_facebook(self):
        #self.hide()  # Masquer le module de connexion
        self.face_main = FaceMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
        # subprocess.Popen([sys.executable, "main_fb_robot.py"])

    # Fonction pour ouvrir WhatsApping
    def open_whatsapp(self):
        #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = WhatsMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
        # subprocess.Popen([sys.executable, "main_fb_robot.py"])

    # Fonction pour ouvrir Blogging
    def open_blogging(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = BlogMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
        
    # Fonction pour ouvrir Insta Pro
    def open_instagram(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = InstaMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
      
    def open_youtube(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = YtbMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
    def open_twitter(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = XMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
      
    def open_tiktok(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = TokMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
      
    def open_snapchat(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = InstaMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
      
    def open_reddit(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = RedditMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
      
    def open_pinterest(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = InstaMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
      
    def open_linkeding(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = LinkedingMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
      
    def open_Emailing(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = MailMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
      
    def open_chatbot(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = ChatBotMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
      
    def open_branding(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = BrandMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
      
  
    def open_adsPro(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])
        self.face_main = AdsMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
      
      

    def lighten_color(self, color):
        # Fonction pour éclaircir une couleur
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'

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

    def show_message(self, button_text):
        # Afficher un message lorsque l'un des boutons est cliqué
        QMessageBox.information(self, "Info", f"Vous avez cliqué sur {button_text}!")

    def open_link(self, url):
        # Ouvrir un lien dans le navigateur par défaut
        import webbrowser
        webbrowser.open(url)

    def side_menu_action(self, action):
        # Actions pour les boutons du menu latéral
        if action == "Accueil":
            QMessageBox.information(self, "Accueil", "Bienvenue à l'accueil!")
        elif action == "Paramètres":
            QMessageBox.information(self, "Paramètres", "Ouvrir les paramètres...")
        elif action == "Aide":
            QMessageBox.information(self, "Aide", "Ouvrir l'aide...")
        elif action == "À propos":
            QMessageBox.information(self, "À propos", "AI FB ROBOT PRO v1.0\n© 2024 Nova360 Pro")
        elif action == "Quitter":
            self.close()

    def change_theme(self):
        # Changer de thème (exemple simple)
        current_color = self.centralWidget().styleSheet()
        new_color = "#2196F3" if "background-color: #F5F5F5;" in current_color else "#F5F5F5"
        self.setStyleSheet(f"background-color: {new_color};")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    sys.exit(app.exec_())
