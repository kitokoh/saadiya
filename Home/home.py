import json
import os
import subprocess
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor
# from PyQt5.QtWidgets import QGraphicsDropShadowEffect
# from PyQt5.QtGui import QColor
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import (
    QApplication, QAction, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QLineEdit, QScrollArea, QGraphicsDropShadowEffect, QFrame, QMenu, QMenuBar, QMessageBox
)
from PyQt5.QtWidgets import QPushButton, QMenu, QAction, QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QProgressBar
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtCore import QSize
from ModulesUI.AutoBlog.main_blog_robot import BlogMainWindow  # Importez votre page d'accueil
from ModulesUI.adsPro.main_ads_robot import AdsMainWindow  # Importez votre page d'accueil
from ModulesUI.branding.main_brand_robot import BrandMainWindow  # Importez votre page d'accueil
from ModulesUI.chatBot.main_chatbot_robot import ChatBotMainWindow  # Importez votre page d'accueil
from ModulesUI.emailing.main_mail_robot import MailMainWindow  # Importez votre page d'accueil
from ModulesUI.insta.main_insta_robot import InstaMainWindow  # Importez votre page d'accueil
from ModulesUI.linkeding.main_linkeding_robot import LinkedingMainWindow  # Importez votre page d'accueil
# from Modules.pinterest.main_pin_robot import PinMainWindow  # Importez votre page d'accueil
from ModulesUI.reddit.main_reddit_robot import RedditMainWindow  # Importez votre page d'accueil
from ModulesUI.tiktok.main_tok_robot import TokMainWindow  # Importez votre page d'accueil
from ModulesUI.twitter.main_x_robot import XMainWindow  # Importez votre page d'accueil
from ModulesUI.whasapping.main_wp_robot import WhatsMainWindow  # Importez votre page d'accueil
from ModulesUI.youtube.main_ytb_robot import YtbMainWindow  # Importez votre page d'accueil
from facebook.main_fb_robot import FaceMainWindow  # Importez votre page d'accueil
# from Modules.pinterest.main_pin_robot import PinMainWindow  # Importez votre page d'accueil
from translation import TranslatorManager  # Importer le gestionnaire de traductions

#pour changer la destinationet developper en local c  ext ici que ca se passe
#  
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
from ui.clientsBrand import Nosclient
from imports import *
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QProgressDialog, QLabel, QApplication
class PremiumButtonWidget(QWidget):
    def __init__(self, text, icon, color, func, key, parent=None):
        super().__init__(parent)
        self.button = QPushButton(text)
        self.button.setFont(QFont("Arial", 14))
        self.button.setIcon(QIcon(QPixmap(icon).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        self.button.setStyleSheet(f"""
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
                border: 2px solid #AAAAAA;
                margin: -2px;
            }}
            QPushButton:pressed {{
                background-color: {color};
                border: 2px solid #888888;
                padding: 12px;
            }}
        """)

        # Ajouter l'icône "Premium"
        self.premium_icon = QLabel(self)
        self.premium_icon.setPixmap(QPixmap("resources/icons/premium-icon.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.premium_icon.setAlignment(Qt.AlignTop | Qt.AlignRight)
        self.premium_icon.setStyleSheet("background-color: transparent;")

        # Layout pour le widget personnalisé
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)
        layout.setContentsMargins(0, 0, 0, 0)

        # Connecter le bouton à sa fonction
        if self.is_feature_enabled(key):
            self.button.clicked.connect(func)
        else:
            self.button.clicked.connect(lambda _, k=key: self.prompt_enable_feature(k))

    def lighten_color(self, color):
        # Fonction pour éclaircir la couleur (identique à celle que vous utilisez)
        return QColor(color).lighter(120).name()

    def resizeEvent(self, event):
        # Mettre à jour la position de l'icône "Premium" lorsque le widget est redimensionné
        self.premium_icon.move(self.width() - 30, 5)
        super().resizeEvent(event)
class LoaderThread(QThread):
    finished = pyqtSignal(object)  # Signal pour émettre l'instance de LeopardoProApp

    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

    def run(self):
        # Instancier LeopardoProApp en arrière-plan
        app_instance = FaceMainWindow() 
        self.finished.emit(app_instance)  # Émettre l'instance une fois terminée
class HomePage(QMainWindow):
    def __init__(self,main_app=None):
        super().__init__()
        self.main_app = main_app  # Stocke une référence à MainApp
       
       #charger les settingss 
        self.settings_file = "settings.json"  # Chemin vers le fichier JSON
    
        self.load_settings()
        self.settings = {}

        self.translator = QTranslator()

        self.init_language()
        # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()

        # Configuration principale de la fenêtre
        self.setWindowTitle("AI FB ROBOT PRO - Marketing Automation")
        self.setGeometry(100, 100, 1220, 800)  # Taille de la fenêtre
        self.setStyleSheet("background-color: #F5F5F5;")
        # Définir l'icône de la fenêtre
        self.setWindowIcon(QIcon('resources/icons/robot-icons-30504-Windows.ico'))  # Spécifiez le chemin de l'icône





        # Créer un widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)



        # Layout principal en vertical
        self.main_layout = QVBoxLayout(central_widget)



        # # Menu en-tête
        # self.menu_bar = QMenuBar(self)
        # self.setMenuBar(self.menu_bar)

        # # Ajouter des menus à la barre de menu
        # file_menu = self.menu_bar.addMenu(self.tr("Fichier"))
        # edit_menu = self.menu_bar.addMenu(self.tr("Édition"))
        # view_menu = self.menu_bar.addMenu(self.tr("Vue"))
        # settings_menu = self.menu_bar.addMenu(self.tr("Paramètres"))
        # help_menu = self.menu_bar.addMenu(self.tr("Aide"))

        # # Créer des actions de menu pour le menu Fichier
        # new_project_action = QAction(self.tr("Nouveau Projet"), self)
        # open_project_action = QAction(self.tr("Ouvrir Projet"), self)
        # save_project_action = QAction(self.tr("Enregistrer le Projet"), self)
        # export_action = QAction(self.tr("Exporter..."), self)
        # exit_action = QAction(self.tr("Quitter"), self)
        # exit_action.triggered.connect(self.close)

        # file_menu.addAction(new_project_action)
        # file_menu.addAction(open_project_action)
        # file_menu.addAction(save_project_action)
        # file_menu.addSeparator()
        # file_menu.addAction(export_action)
        # file_menu.addSeparator()
        # file_menu.addAction(exit_action)

        # # Actions de menu pour le menu Édition
        # edit_menu.addAction(self.tr("Copier"))
        # edit_menu.addAction(self.tr("Coller"))
        # edit_menu.addSeparator()
        # edit_menu.addAction(self.tr("Supprimer"))
        # edit_menu.addSeparator()
        # edit_menu.addAction(self.tr("Préférences"))

        # # Actions de menu pour le menu Vue
        # view_menu.addAction(self.tr("Aperçu"))
        # view_menu.addAction(self.tr("Vue Grille"))
        # view_menu.addAction(self.tr("Vue Liste"))

        # # Actions de menu pour le menu Paramètres
        # theme_action = QAction(self.tr("Changer de thème"), self)
        # theme_action.triggered.connect(self.change_theme)
        # language_action = QAction(self.tr("Changer de langue"), self)
        # language_action.triggered.connect(self.show_about)

        # settings_menu.addAction(theme_action)
        # settings_menu.addAction(language_action)

        # # Actions de menu pour le menu Aide
        # help_action = QAction(self.tr("Aide en ligne"), self)
        # help_action.triggered.connect(self.open_help)
        # about_action = QAction(self.tr("À propos de Leopardo.turknovatech.com"), self)
        # about_action.triggered.connect(self.show_about)

        # help_menu.addAction(help_action)
        # help_menu.addAction(about_action)

        # Layout pour l'en-tête
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 10, 10, 10)

        # Ajouter un cadre 3D pour l'en-tête
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-image: url('resources/images/back.webp');
                background-position: center;
                background-size: cover;
                                 
                border: 3px solid #4CAF50;
                border-radius: 10px;
                background-color: white;
               
                                   
            }
        """)
        header_frame.setLayout(header_layout)

        # Ajouter un effet d'ombre
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)  # Rayon de flou
        shadow.setOffset(5, 5)  # Décalage horizontal et vertical
        shadow.setColor(QColor(0, 0, 0, 50))  # Couleur noire avec transparence
        header_frame.setGraphicsEffect(shadow)

        # Titre de l'application
        title_label = QLabel("AI Marketing Automation")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2E7D32; padding: 10px;")
        header_layout.addWidget(title_label)

        # Logo du menu
        menu_logo_label = QLabel(self)
        menu_pixmap = QPixmap("resources/icons/robot-icons-30504-Windows.ico")
        menu_logo_label.setPixmap(menu_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        menu_logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(menu_logo_label)

        # Nom de l'application et slogan
        app_info_layout = QVBoxLayout()
        app_name_label = QLabel("Leopardo AI")
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
        gif_pixmap = QPixmap("resources/icons/robot-256.png")  
        gif_logo_label.setPixmap(gif_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        gif_logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(gif_logo_label)

        # Barre de recherche
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Rechercher...")
        search_bar.setFont(QFont("Arial", 14))
        search_bar.setStyleSheet("""
            QLineEdit {
                background-image: url('resources/images/back.webp');

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
        toggle_button.setIcon(QIcon(QPixmap("resources/icons/robot-icons-30497-Windows.ico").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
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
        self.main_layout.addWidget(header_frame)

        # Espacement avant les boutons
        self.main_layout.addSpacing(20)

        # Menu latéral rétractable
        self.side_menu = QWidget(self)
        self.side_menu.setGeometry(0, 80, 200, 600)  # Positionné un peu plus haut
        self.side_menu.setStyleSheet("""
            QWidget {
                background-color: #4CAF50;
                background-image: url('resources/images/ba.webp');
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
                border-radius: 10px; /* Adoucit les bords */
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2); /* Transparent subtilement */
                color: white;
                border: 1px solid #ffffff50; /* Bordure légère et subtile */
                padding: 12px 20px; /* Ajustement du padding pour un rendu plus équilibré */
                text-align: left;
                font-size: 15px;
                font-weight: bold; /* Ajoute un contraste subtil */
                border-radius: 8px; /* Coins arrondis */
                transition: all 0.3s ease; /* Transition fluide pour le hover */
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.4); /* Accentuation subtile sur hover */
                color: #f5f5f5;
                transform: scale(1.05); /* Légère mise en avant */
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.6); /* Couleur plus marquée au clic */
                transform: scale(1.02); /* Réduction subtile pour effet de clic */
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
            ("Accueil", "resources/icons/robot-icons-30504-Windows.ico"),
            ("Paramètres", "resources/icons/robot-icons-30497-Windows.ico"),
            ("Aide", "resources/icons/information-icon-6055-Windows.ico"),
            ("À propos", "resources/icons/information-icon-6055-Windows.ico"),
            ("Quitter", "resources/icons/robot-icons-30504-Windows.ico"),
        ]

        # for text, icon in side_buttons:
            # button = QPushButton(text)
            # button.setFont(QFont("Arial", 14))
            # button.setIcon(QIcon(QPixmap(icon).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
            # button.setIconSize(QPixmap(icon).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation).size())
            # button.clicked.connect(lambda _, btn=text: self.side_menu_action(btn))
            # side_menu_layout.addWidget(button)

        for text, icon in side_buttons:
            button = QPushButton(text)
            
            # Définir la police et l'icône
            button.setFont(QFont("Arial", 14))
            pixmap = QPixmap(icon).scaled(24, 24, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            button.setIcon(QIcon(pixmap))
            button.setIconSize(pixmap.size())

            # Ajouter des propriétés visuelles
            button.setStyleSheet("""
                QPushButton {
                    background-color: blue; /* Couleur de fond par défaut */
                    border: none; /* Pas de bordure */
                    padding: 10px; /* Espacement intérieur */
                    border-radius: 8px; /* Coins arrondis */
                }
                QPushButton:hover {
                    background-color: #d9d9d9; /* Couleur au survol */
                }
                QPushButton:pressed {
                    background-color: #b3b3b3; /* Couleur au clic */
                }
            """)

            # Connecter l'action
            button.clicked.connect(lambda _, btn=text: self.side_menu_action(btn))
            
            # Ajouter le bouton au layout
            side_menu_layout.addWidget(button)

        # Optionnel : ajouter de l'espacement entre les boutons
            side_menu_layout.setSpacing(10)  # Espacement entre les boutons

                # Layout pour les icônes et boutons du milieu
            middle_layout = QHBoxLayout()
 # Ajouter une image de fond au format .webp
        features = [
            ("FB Robot Pro", "resources/icons/facebook-icon-png-770-Windows.ico", "#E91E63", self.open_facebook, "facebook_bot"),
            ("WhatsApping", "resources/icons/whatsapp-512.png", "#4CAF50", self.open_whatsapp, "whatsapp_bot"),
            ("Blogging", "resources/icons/Hopstarter-Soft-Scraps-Edit-Document.ico", "#4CAF50", self.open_blogging, "blogging_bot"),
            ("Insta Pro", "resources/icons/instagram-icon-956-Windows.ico", "#4CAF50", self.open_instagram, "instagram_bot"),
            ("Telegram Bot", "resources/icons/telgrampng.png", "#4CAF50", self.open_adsPro1, "telegram_bot"),
            ("Branding", "resources/icons/promotion-icon-png-3422-Windows.ico", "#4CAF50", self.open_branding1, "branding_bot"),
            ("Emailing", "resources/icons/pink-message-icon-12045-Windows.ico", "#4CAF50", self.open_Emailing1, "emailing_bot"),
        ]

   # Boutons des fonctionnalités

        feature_layout = QHBoxLayout()


        for text, icon, color, func, key in features:
            # Conteneur principal pour chaque bouton


            # Bouton principal
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
                    border: 2px solid #AAAAAA;
                    padding: 8px;
                }}
                QPushButton:pressed {{
                    background-color: {color};
                    border: 2px solid #888888;
                }}
            """)

            # Badge Premium
            if key in ["blogging_bot", "instagram_bot","telegram_bot","emailing_bot"]:
                # Création du badge premium
                premium_label = QLabel("Premium")
                premium_label.setFont(QFont("Arial", 6, QFont.Bold))  # Police légèrement plus grande
                premium_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        background: qradialgradient(cx:0.5, cy:0.5, radius:1.5, fx:0.5, fy:0.5, 
                                                    stop:0 #ffd700, stop:0.6 #ffb700, stop:1 #d4af37);
                        border-radius: 12px;
                        padding: 6px 12px;
                        border: 2px solid rgba(255, 223, 0, 0.9);
                        transition: all 0.3s ease-in-out;
                    }
                    QLabel:hover {
                        background: qradialgradient(cx:0.5, cy:0.5, radius:1.5, fx:0.5, fy:0.5, 
                                                    stop:0 #ffdf00, stop:0.6 #ffd000, stop:1 #b58f2f);
                        transform: scale(1.05);
                    }
                """)
                premium_label.setAlignment(Qt.AlignCenter)
                premium_label.setFixedSize(80, 30)  # Taille ajustée pour un effet plus distinct

                # Positionnement du badge
                premium_label.move(15, 15)
                premium_label.setParent(button)

                # Ombre dynamique pour le badge
                badge_shadow = QGraphicsDropShadowEffect()
                badge_shadow.setBlurRadius(25)
                badge_shadow.setColor(QColor(255, 223, 0, 150))  # Ombre dorée
                badge_shadow.setOffset(3, 3)
                premium_label.setGraphicsEffect(badge_shadow)
           
            #badge vert Actif
            if key in ["facebook_bot","whatsapp_bot"]:
                # Création du badge premium
                premium_label = QLabel("actif")
                premium_label.setFont(QFont("Arial", 6, QFont.Bold))  # Police légèrement plus grande
                premium_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        background: qradialgradient(cx:0.5, cy:0.5, radius:1.5, fx:0.5, fy:0.5, 
                                                    stop:0 #00ff00, stop:0.6 #00cc00, stop:1 #009900);
                        border-radius: 12px;
                        padding: 6px 12px;
                        border: 2px solid rgba(0, 255, 0, 0.9);
                        transition: all 0.3s ease-in-out;
                    }
                    QLabel:hover {
                        background: qradialgradient(cx:0.5, cy:0.5, radius:1.5, fx:0.5, fy:0.5, 
                                                    stop:0 #00ff00, stop:0.6 #00cc00, stop:1 #009900);
                        transform: scale(1.05);
                    }
                """)
                premium_label.setAlignment(Qt.AlignCenter)
                premium_label.setFixedSize(80, 30)  # Taille ajustée pour un effet plus distinct

                # Positionnement du badge
                premium_label.move(15, 15)
                premium_label.setParent(button)

                # Ombre dynamique pour le badge
                badge_shadow = QGraphicsDropShadowEffect()
                badge_shadow.setBlurRadius(25)
                badge_shadow.setColor(QColor(0, 255, 0, 150))  # Ombre verte
                badge_shadow.setOffset(3, 3)
                premium_label.setGraphicsEffect(badge_shadow)
            # Badge bleu entreprise
            if key in ["branding_bot"]:
                # Création du badge premium
                premium_label = QLabel("Entreprise")
                premium_label.setFont(QFont("Arial", 6, QFont.Bold))  # Police légèrement plus grande
                premium_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        background: qradialgradient(cx:0.5, cy:0.5, radius:1.5, fx:0.5, fy:0.5, 
                                                    stop:0 #00bfff, stop:0.6 #007fff, stop:1 #0055ff);
                        border-radius: 12px;
                        padding: 6px 12px;
                        border: 2px solid rgba(0, 191, 255, 0.9);
                        transition: all 0.3s ease-in-out;
                    }
                    QLabel:hover {
                        background: qradialgradient(cx:0.5, cy:0.5, radius:1.5, fx:0.5, fy:0.5, 
                                                    stop:0 #00bfff, stop:0.6 #007fff, stop:1 #0055ff);
                        transform: scale(1.05);
                    }
                """)
                premium_label.setAlignment(Qt.AlignCenter)
                premium_label.setFixedSize(80, 30)  # Taille ajustée pour un effet plus distinct

                # Positionnement du badge
                premium_label.move(15, 15)
                premium_label.setParent(button)

                # Ombre dynamique pour le badge
                badge_shadow = QGraphicsDropShadowEffect()
                badge_shadow.setBlurRadius(25)
                badge_shadow.setColor(QColor(0, 191, 255, 150))  # Ombre bleue
                badge_shadow.setOffset(3, 3)
                premium_label.setGraphicsEffect(badge_shadow)
            # Effet d'ombre pour le bouton
            if key in ["facebook_bot", "whatsapp_bot", "linkedin_bot"]:
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(50)  # Rayon de flou plus grand
                shadow.setColor(QColor(255, 36, 0, 200))  # Rouge néon avec opacité
                shadow.setOffset(5, 10)  # Décalage plus important
                button.setGraphicsEffect(shadow)
                
            if self.is_feature_enabled(key):
                button.clicked.connect(func)
            else:
                button.clicked.connect(lambda _, f=func, k=key: self.prompt_enable_feature(k))

            button.clicked.connect(func)  # Connecter chaque bouton à sa fonction respective

            # Ajouter le bouton dans le layout
            feature_layout.addWidget(button)
        #     feature_layout.addWidget(button)

            # Connecter les boutons aux fonctions
          # button.clicked.connect(func if self.is_feature_enabled(key) else lambda _, k=key: self.prompt_enable_feature(k))


        self.main_layout.addLayout(feature_layout)


        duplicate_features = [
            ("Twitter Bot", "resources/icons/aquicon-icon-18708-Windows.ico", "#1DA1F2", self.open_twitter1, "twitter_bot"),
            ("LinkedIn Pro", "resources/icons/aquicon-icon-18717-Windows.ico", "#0077B5", self.open_linkedin, "linkedin_bot"),
            ("Pinterest Bot", "resources/icons/subscribe-png-574-Windows.ico", "#BD081C", self.open_pinterest1, "pinterest_bot"),
            ("Snapchat Bot", "resources/icons/snapchat-icon-1707-Windows.ico", "#FFFC00", self.open_snapchat1, "snapchat_bot"),
            ("TikTok Pro", "resources/icons/camera-icon-59-Windows.ico", "#010101", self.open_tiktok1, "tiktok_bot"),
            ("Reddit Bot", "resources/icons/camera-icon-59-Windows.ico", "#FF4500", self.open_reddit1, "reddit_bot"),
            ("YouTube Pro", "resources/icons/youtube-logo-png-3580-Windows.ico", "#FF0000", self.open_youtube1, "youtube_bot"),
        ]
        duplicate_layout = QHBoxLayout()

     
        self.buttons = {}
        for text, icon, color, func, setting_key in duplicate_features:
            # Conteneur principal pour chaque bouton


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
                    border: 2px solid #AAAAAA;
                    margin: -2px;
                }}
                QPushButton:pressed {{
                    background-color: {color};
                    border: 2px solid #888888;
                    padding: 12px;
                }}
            """)
            #badge vert Actif
            if setting_key in ["linkedin_bot"]:
                # Création du badge premium
                premium_label = QLabel("Actif")
                premium_label.setFont(QFont("Arial", 6, QFont.Bold))  # Police légèrement plus grande
                premium_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        background: qradialgradient(cx:0.5, cy:0.5, radius:1.5, fx:0.5, fy:0.5, 
                                                    stop:0 #00ff00, stop:0.6 #00cc00, stop:1 #009900);
                        border-radius: 12px;
                        padding: 6px 12px;
                        border: 2px solid rgba(0, 255, 0, 0.9);
                        transition: all 0.3s ease-in-out;
                    }
                    QLabel:hover {
                        background: qradialgradient(cx:0.5, cy:0.5, radius:1.5, fx:0.5, fy:0.5, 
                                                    stop:0 #00ff00, stop:0.6 #00cc00, stop:1 #009900);
                        transform: scale(1.05);
                    }
                """)
                premium_label.setAlignment(Qt.AlignCenter)
                premium_label.setFixedSize(80, 30)  # Taille ajustée pour un effet plus distinct

                # Positionnement du badge
                premium_label.move(15, 15)
                premium_label.setParent(button)

                # Ombre dynamique pour le badge
                badge_shadow = QGraphicsDropShadowEffect()
                badge_shadow.setBlurRadius(25)
                badge_shadow.setColor(QColor(0, 255, 0, 150))  # Ombre verte
                badge_shadow.setOffset(3, 3)
                premium_label.setGraphicsEffect(badge_shadow)
           
            # Badge Premium
            if setting_key in ["blogging_bot", "instagram_bot","twitter_bot","pinterest_bot","snapchat_bot","tiktok_bot","reddit_bot","youtube_bot"]:
                # Création du badge premium
                premium_label = QLabel("Premium")
                premium_label.setFont(QFont("Arial", 6, QFont.Bold))  # Police légèrement plus grande
                premium_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        background: qradialgradient(cx:0.5, cy:0.5, radius:1.5, fx:0.5, fy:0.5, 
                                                    stop:0 #ffd700, stop:0.6 #ffb700, stop:1 #d4af37);
                        border-radius: 12px;
                        padding: 6px 12px;
                        border: 2px solid rgba(255, 223, 0, 0.9);
                        transition: all 0.3s ease-in-out;
                    }
                    QLabel:hover {
                        background: qradialgradient(cx:0.5, cy:0.5, radius:1.5, fx:0.5, fy:0.5, 
                                                    stop:0 #ffdf00, stop:0.6 #ffd000, stop:1 #b58f2f);
                        transform: scale(1.05);
                    }
                """)
                premium_label.setAlignment(Qt.AlignCenter)
                premium_label.setFixedSize(80, 30)  # Taille ajustée pour un effet plus distinct

                # Positionnement du badge
                premium_label.move(15, 15)
                premium_label.setParent(button)

                # Ombre dynamique pour le badge
                badge_shadow = QGraphicsDropShadowEffect()
                badge_shadow.setBlurRadius(25)
                badge_shadow.setColor(QColor(255, 223, 0, 150))  # Ombre dorée
                badge_shadow.setOffset(3, 3)
                premium_label.setGraphicsEffect(badge_shadow)
           
   # Ajouter un icône "Premium" aux boutons spécifiques
            if setting_key in ["blogging_bot", "instagram_bot", "twitter_bot"]:
                self.add_premium_icon(button)



            if setting_key in ["facebook_bot", "whatsapp_bot", "linkedin_bot"]:
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(30)
                shadow.setColor(QColor(0, 212, 255))  # Neon blue
                shadow.setOffset(0, 5)
                button.setGraphicsEffect(shadow)
            if self.is_feature_enabled(setting_key):
                button.clicked.connect(func)
            else:
                button.clicked.connect(lambda _, f=func, k=setting_key: self.prompt_enable_feature(k))

            button.clicked.connect(func)  # Connecter chaque bouton à sa fonction respective

        #     middle_layout.addWidget(button)

        # self.main_layout.addLayout(middle_layout)



        #     # Vérifie si le module est activé ou non
        #     button.setEnabled(self.settings.get(setting_key, False))
        #     button.clicked.connect(lambda _, f=func, k=setting_key: self.handle_button_click(f, k))
            # Ajouter le bouton dans le layout

        #     self.buttons[setting_key] = button
            duplicate_layout.addWidget(button)

        self.main_layout.addLayout(duplicate_layout)

        # Ajouter un titre "Gestion Auto"
        gestion_auto_label = QLabel(self.tr("Autres Solutions"))
        gestion_auto_label.setFont(QFont("Arial", 20, QFont.Bold))
        gestion_auto_label.setAlignment(Qt.AlignCenter)
        gestion_auto_label.setStyleSheet("color: #2E7D32;")
        self.main_layout.addWidget(gestion_auto_label)
        # self.setup_bottom_buttons()
        # Section des boutons du bas
        bottom_layout = QHBoxLayout()

        # Dictionnaire des icônes pour chaque bouton
        bottom_buttons_icons = {
            "Swipes & Messages": "resources/icons/message-icon.png",
            "Crypto Trade": "resources/icons/crypto-icon.png",
            "Contact 360": "resources/icons/contact-icon.png",
            "List Business Contacts": "resources/icons/business-icon.png",
            "SAV": "resources/icons/sav-icon.png",
            "ERP": "resources/icons/erp-icon.png",
            "CRM360": "resources/icons/crm-icon.png"
        }

        bottom_buttons = [
            ("Swipes & Messages", "#4CAF50"),
            ("Crypto Trade", "#4CAF50"),
            ("Contact 360", "#4CAF50"),
            ("List Business Contacts", "#4CAF50"),
            ("SAV", "#E91E63"),
            ("ERP", "#4CAF50"),
            ("CRM360", "#E91E63")
        ]

        for text, color in bottom_buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14, QFont.Bold))  # Police en gras
            button.setIcon(QIcon(bottom_buttons_icons[text]))  # Ajouter l'icône
            button.setIconSize(QSize(32, 32))  # Taille de l'icône

            # Style avec dégradé, ombre et effets de survol
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                    stop:0 {self.lighten_color(color)}, stop:1 {color});
                    color: white;
                    padding: 20px;
                    border-radius: 15px;
                    border: 2px solid #CCCCCC;
                    font-size: 14px;
                    font-weight: bold;
                    text-align: left;
                    padding-left: 50px;  # Espace pour l'icône
                    transition: all 0.3s ease;
                }}
                QPushButton:hover {{
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                    stop:0 {self.lighten_colr(color, 1.2)}, stop:1 {self.lighten_color(color)});
                    border: 2px solid #AAAAAA;
                    transform: scale(1.05);
                }}
                QPushButton:pressed {{
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                    stop:0 {color}, stop:1 {self.lighten_colr(color, 0.8)});
                    border: 2px solid #888888;
                    transform: scale(0.95);
                }}
            """)

            # Ajouter une ombre
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setColor(QColor(0, 0, 0, 100))  # Ombre noire avec transparence
            shadow.setOffset(3, 3)
            button.setGraphicsEffect(shadow)

            # Connecter le bouton à sa fonction
            button.clicked.connect(lambda _, btn=text: self.show_message1(btn))
            bottom_layout.addWidget(button)

        self.main_layout.addLayout(bottom_layout)



        # Bouton pour ouvrir un nouvel onglet
        open_tab_button = QPushButton("Ouvrir un nouvel onglet")
        open_tab_button.clicked.connect(self.open_new_tab)
       # self.main_layout.addWidget(open_tab_button)
       # client_layout = QHBoxLayout()
       # self.clients=Nosclient()

        #client_layout.addWidget(self.clients)
        #self.main_layout.addLayout(client_layout)

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
        footer_text = QLabel(self.tr("Privacy Policy | © 2025 Leopardo AI"))
        footer_text.setFont(QFont("Arial", 10))
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setStyleSheet("color: white;")


        # Boutons dans le footer
        privacy_button = QPushButton(self.tr("Privacy Policy"))  # Traduction en anglais
        privacy_button.setFont(QFont("Arial", 10))
        privacy_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #81C784;  /* Vert clair au survol */
            }
        """)
        privacy_button.clicked.connect(lambda: self.open_link("https://www.leopard.com/privacy"))  # Lien mis à jour

        terms_button = QPushButton(self.tr("Terms and Conditions"))  # Traduction en anglais
        terms_button.setFont(QFont("Arial", 10))
        terms_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #81C784;  /* Vert clair au survol */
            }
        """)
        terms_button.clicked.connect(lambda: self.open_link("https://www.leopard.com/terms"))  # Lien mis à jour

        footer_layout.addWidget(privacy_button)
        footer_layout.addWidget(footer_text)
        footer_layout.addWidget(terms_button)

        self.main_layout.addWidget(footer_frame)

        # Ajouter le layout principal au widget central
        central_widget.setLayout(self.main_layout)

        self.show()




    def lighten_colr(self, color, factor=1.2):
        """
        Éclaircit une couleur en fonction d'un facteur.
        :param color: La couleur à éclaircir (au format hexadécimal ou QColor).
        :param factor: Le facteur d'éclaircissement (par défaut 1.2).
        :return: La couleur éclaircie au format hexadécimal.
        """
        if isinstance(color, str):
            color = QColor(color)
        elif isinstance(color, QColor):
            pass
        else:
            raise ValueError("La couleur doit être une chaîne hexadécimale ou un objet QColor.")

        # Éclaircir la couleur en fonction du facteur
        lighter_color = color.lighter(int(100 * factor))
        return lighter_color.name()

    def setup_bottom_buttons(self):
        # Section des boutons du bas
        bottom_layout = QHBoxLayout()

        # Dictionnaire des icônes pour chaque bouton
        bottom_buttons_icons = {
            "Swipes & Messages": "resources/icons/message-icon.png",
            "Crypto Trade": "resources/icons/crypto-icon.png",
            "Contact 360": "resources/icons/contact-icon.png",
            "List Business Contacts": "resources/icons/business-icon.png",
            "SAV": "resources/icons/sav-icon.png",
            "ERP": "resources/icons/erp-icon.png",
            "CRM360": "resources/icons/crm-icon.png"
        }

        bottom_buttons = [
            ("Swipes & Messages", "#4CAF50"),
            ("Crypto Trade", "#4CAF50"),
            ("Contact 360", "#4CAF50"),
            ("List Business Contacts", "#4CAF50"),
            ("SAV", "#E91E63"),
            ("ERP", "#4CAF50"),
            ("CRM360", "#E91E63")
        ]

        for text, color in bottom_buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14, QFont.Bold))  # Police en gras
            button.setIcon(QIcon(bottom_buttons_icons[text]))  # Ajouter l'icône
            button.setIconSize(QSize(32, 32))  # Taille de l'icône

            # Style avec dégradé, ombre et effets de survol
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                      stop:0 {self.lighten_colr(color)}, stop:1 {color});
                    color: white;
                    padding: 20px;
                    border-radius: 15px;
                    border: 2px solid #CCCCCC;
                    font-size: 14px;
                    font-weight: bold;
                    text-align: left;
                    padding-left: 50px;  # Espace pour l'icône
                    transition: all 0.3s ease;
                }}
                QPushButton:hover {{
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                      stop:0 {self.lighten_colr(color, 1.5)}, stop:1 {self.lighten_colr(color, 1.2)});
                    border: 2px solid #AAAAAA;
                    transform: scale(1.05);
                }}
                QPushButton:pressed {{
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                      stop:0 {color}, stop:1 {self.lighten_colr(color, 0.8)});
                    border: 2px solid #888888;
                    transform: scale(0.95);
                }}
            """)

            # Ajouter une ombre
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setColor(QColor(0, 0, 0, 100))  # Ombre noire avec transparence
            shadow.setOffset(3, 3)
            button.setGraphicsEffect(shadow)

            # Connecter le bouton à sa fonction
            button.clicked.connect(lambda _, btn=text: self.show_message1(btn))
            bottom_layout.addWidget(button)

        self.main_layout.addLayout(bottom_layout)
    def add_premium_icon(self,button):
        premium_icon = QLabel(button)
        premium_icon.setPixmap(QPixmap("resources/icons/fb_robot.ico").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        premium_icon.setAlignment(Qt.AlignTop | Qt.AlignRight)
        premium_icon.setGeometry(button.width() - 30, 5, 24, 24)  # Position en haut à droite
        premium_icon.setStyleSheet("background-color: transparent;")

    def load_settings1(self):
        try:
            with open(self.settings_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_settings(self):
        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file, indent=4)

    def is_feature_enabled(self, feature_key):
        """
        Vérifie si une fonctionnalité est activée en fonction de la clé fournie.

        Args:
            feature_key (str): La clé correspondant à la fonctionnalité dans les paramètres.

        Returns:
            bool: True si la fonctionnalité est activée, False sinon.
        """
        if not isinstance(feature_key, str):
            raise ValueError("feature_key doit être une chaîne de caractères.")

        if not hasattr(self, 'settings') or not isinstance(self.settings, dict):
            raise AttributeError("L'attribut 'settings' doit être un dictionnaire défini dans l'objet.")

        # Retourne la valeur ou False si la clé n'existe pas
        return bool(self.settings.get(feature_key, False))


    def enable_feature(self, feature_key):
        self.settings[feature_key] = True
        self.save_settings()


    def handle_button_click(self, feature_key, func):
        """Gère le clic sur un bouton."""
        if self.is_feature_enabled(feature_key):
            # La fonctionnalité est activée, exécute la fonction
            func()
        else:
            # La fonctionnalité est désactivée, afficher le popup
            self.prompt_enable_feature(feature_key)

    def prompt_enable_feature(self, feature_key):
        """Affiche un popup pour activer une fonctionnalité."""
        # reply = QMessageBox.question(
        #     None,
        #     "Activation nécessaire",
        #     f"Le module '{feature_key}' n'est pas activé. Souhaitez-vous l'activer ?",
        #     QMessageBox.Yes | QMessageBox.No
        # )
        # if reply == QMessageBox.Yes:
        self.activate_feature()

    def activate_feature(self):
        """Active une fonctionnalité avec une barre de progression."""
        progress = QProgressBar()
        progress.setMaximum(100)
        progress.show()

        def complete_activation():
            progress.setValue(100)
            self.enable_feature("feature_key")
            QMessageBox.information(None, "Activation réussie", f"Le module '' est maintenant activé.")
            progress.close()

        timer = QTimer()
        timer.timeout.connect(complete_activation)
        timer.start(2000)  # Simule une activation en 2 secondes




    # def prompt_enable_feature(self, feature_key):
    #     reply = QMessageBox.question(
    #         None,
    #         "Activation nécessaire",
    #         f"Le module '{feature_key}' n'est pas activé. Souhaitez-vous l'activer ?",
    #         QMessageBox.Yes | QMessageBox.No
    #     )
    #     if reply == QMessageBox.Yes:
    #         self.activate_feature(feature_key)

    # # def activate_feature(self, feature_key):
    # #     progress = QProgressBar()
    # #     progress.setMaximum(100)
    # #     progress.show()

    # #     def complete_activation():
    # #         progress.setValue(100)
    # #         self.enable_feature(feature_key)
    # #         QMessageBox.information(None, "Activation réussie", f"Le module '{feature_key}' est maintenant activé.")
    # #         progress.close()

    # #     timer = QTimer()
    # #     timer.timeout.connect(complete_activation)
    # #     timer.start(2000)  # Simule une activation en 2 secondes




        

    # def open_new_tab(self):
    #         """Ouvre une nouvelle classe dans un nouvel onglet."""
    #         # Vérifiez que main_app existe
    #         if hasattr(self, 'main_app') and self.main_app is not None:
    #             new_widget = QWidget()
    #             new_layout = QVBoxLayout(new_widget)
    #             new_layout.addWidget(QPushButton("Contenu du nouvel onglet"))
    #             self.main_app.add_custom_tab(new_widget, "Nouvel Onglet", "new_icon.ico")
    #         else:
    # def open_new_tab(self, tab_name=None, icon_path=None):
    #     """Ouvre un nouvel onglet avec un widget personnalisé.
        
    #     Args:
    #         tab_name (str): Le titre de l'onglet. Défaut : "Nouvel Onglet".
    #         icon_path (str): Le chemin vers l'icône pour l'onglet. Défaut : None.
    #     """
    #     if not self.main_app:
    #         print("Erreur : main_app n'est pas défini.")
    #         return

    #     # Créer un widget pour le nouvel onglet
    #     new_widget = QLabel(f"Contenu de l'onglet : {tab_name}")
    #     new_widget.setAlignment(Qt.AlignCenter)  # Optionnel : centrer le texte

    #     # Ajouter le nouvel onglet avec le titre et l'icône fournis
    #     self.main_app.add_custom_tab(new_widget, tab_name, icon_path)



    def load_settings(self):
        """Charge les paramètres depuis le fichier JSON."""
        try:
            with open(self.settings_file, "r") as file:
                self.settings = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.settings = {}

    # def save_settings(self):
    #     """Enregistre les paramètres dans le fichier JSON."""
    #     with open(self.settings_file, "w") as file:
    #         json.dump(self.settings, file, indent=4)

    # def handle_button_click(self, func, setting_key):
    #     """Gère le clic sur un bouton."""
    #     if self.settings.get(setting_key, False):
    #         func()
    #     else:
    #         self.show_activation_popup(setting_key)

    def show_activation_popup(self, setting_key):
        """Affiche un popup pour activer un module."""
        reply = QMessageBox.question(
            self, "Activation requise",
            f"Le module '{setting_key}' est désactivé. Voulez-vous l'activer ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.activate_module(setting_key)

    def activate_module(self, setting_key):
        """Active un module avec une barre de progression."""
        progress_dialog = QProgressBar(self)
        progress_dialog.setRange(0, 100)
        progress_dialog.setValue(0)
        progress_dialog.show()

        def update_progress():
            value = progress_dialog.value() + 10
            if value > 100:
                progress_dialog.close()
                self.settings[setting_key] = True
                self.save_settings()
                self.buttons[setting_key].setEnabled(True)
            else:
                progress_dialog.setValue(value)

        timer = QTimer(self)
        timer.timeout.connect(update_progress)
        timer.start(300)

    # def lighten_color(self, color):
    #     """Éclaircit une couleur en hexadécimal."""
    #     r = min(int(color[1:3], 16) + 30, 255)
    #     g = min(int(color[3:5], 16) + 30, 255)
    #     b = min(int(color[5:], 16) + 30, 255)
    #     return f"#{r:02X}{g:02X}{b:02X}"
   
   
   
    def open_new_tab(self, tab_name="Nouvel Onglet", icon_path=None, widget=None):
        """Ouvre un nouvel onglet avec un widget personnalisé.
        
        Args:
            tab_name (str): Le titre de l'onglet. Défaut : "Nouvel Onglet".
            icon_path (str): Le chemin vers l'icône pour l'onglet. Défaut : None.
            widget (QWidget): Le widget personnalisé à afficher dans l'onglet. Défaut : QLabel avec un message.
        """
        if not self.main_app:
            print("Erreur : main_app n'est pas défini.")
            return

        # Utiliser le widget fourni ou créer un widget par défaut
        if widget is None:
            widget = QLabel(f"Contenu de l'onglet : {tab_name}")
            widget.setAlignment(Qt.AlignCenter)  # Optionnel : centrer le texte

        # Ajouter le nouvel onglet avec le titre, l'icône et le widget
        self.main_app.add_custom_tab(widget, tab_name, icon_path)


    # def open_new_tab(self):
    #     if not self.main_app:
    #         print("Erreur : main_app n'est pas défini.")
    #         return

    #     # Créer un nouvel onglet
    #     new_widget = QLabel("Contenu du nouvel ongletttt")
    #     self.main_app.add_custom_tab(new_widget, "Nouvel Onglet", "new_icon.ico")
   
   
    # def open_new_tab(self):
    #     if self.main_app:
    #         new_widget = QLabel("Contenu du nouvel onglet")
    #         self.main_app.add_custom_tab(new_widget, "Nouvel Onglet", "new_icon.ico")
    #     else:
    #         print("Erreur : main_app n'est pas défini.")
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
        elif language == "pt":
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
        self.setWindowTitle(self.tr('AI Marketing ROBOT Pro'))
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
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
                'pt': 'pt',
            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)

    def open_nova360(self):
        #self.hide()  # Masquer le module de connexion
        self.home_page = HomePage()  # Remplacez ceci par votre classe de page d'accueil
        self.home_page.show()  # Afficher la page d'accueil
    def find_tab_by_name(self, name):
        for i in range(self.main_app.tab_widget.count()):
            if self.main_app.tab_widget.tabText(i) == name:
                return i  # Renvoie l'index si trouvé
        return -1  # Aucun onglet trouvé
    def open_facebook(self):
        #self.hide()  # Masquer le module de connexion
        tab_name = "FB Robot"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
            self.face_main = FaceMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)

        # subprocess.Popen([sys.executable, "main_fb_robot.py"])


    def open_facebook1(self):
        tab_name = "fb"

        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Show loading message
        loading_label = QLabel("Chargement en cours...")
        loading_label.setAlignment(Qt.AlignCenter)
        self.main_app.add_custom_tab(loading_label, tab_name, "accueil_icon.ico")

        # Show progress dialog
        progress_dialog = QProgressDialog("Chargement en cours...", "Annuler", 0, 0, self)
        progress_dialog.setCancelButton(None)
        progress_dialog.setWindowTitle("Chargement")
        progress_dialog.setWindowModality(Qt.ApplicationModal)
        progress_dialog.show()

        # Start loading thread
        self.loader_thread = LoaderThread(main_app=self)
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
            # self.nova360pro = FaceMainWindow()  # Créez une seule fois l'instance
            pass

        self.nova360pro = FaceMainWindow()  # Créez une seule fois l'instance

        self.loader_thread.finished.connect(lambda app: self.update_tab_content(tab_name, self.nova360pro, progress_dialog))
        self.loader_thread.start()

    def update_tab_content(self, tab_name, app_instance, dialog):
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            self.main_app.tab_widget.removeTab(existing_tab_index)
            self.main_app.add_custom_tab(app_instance, tab_name, "accueil_icon.ico")
            self.nova360pro = app_instance  # Set the instance here
        dialog.close()

    # Fonction pour ouvrir WhatsApping
    def open_whatsapp(self):
        #subprocess.Popen([sys.executable, "whatsapp.py"])




        #self.hide()  # Masquer le module de connexion
        tab_name = "WA CRM"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
            self.face_main = WhatsMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)
        #self.face_main.show()  # Afficher la page d'accueil
        # subprocess.Popen([sys.executable, "main_fb_robot.py"])

    # Fonction pour ouvrir Blogging
    def open_blogging(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")

    def open_blogging1(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])



        #self.hide()  # Masquer le module de connexion
        tab_name = "bloging"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
           self.face_main = BlogMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)
    # Fonction pour ouvrir Insta Pro
    def open_instagram1(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])



        #self.hide()  # Masquer le module de connexion
        tab_name = "İnsta"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
           self.face_main = InstaMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)
  
    # Fonction pour ouvrir Blogging
    def open_instagram(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")

  
    def open_youtube(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])



        #self.hide()  # Masquer le module de connexion
        tab_name = "Youtube"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
            self.face_main = YtbMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)
    # Fonction pour ouvrir Blogging
    def open_youtube1(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")

    def open_twitter(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])



        #self.hide()  # Masquer le module de connexion
        tab_name = "Twitter"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
            self.face_main = XMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)
    # Fonction pour ouvrir Blogging
    def open_twitter1(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")

    def open_tiktok(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])




        #self.hide()  # Masquer le module de connexion
        tab_name = "Tiktok"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
            self.face_main = TokMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)
    # Fonction pour ouvrir Blogging
    def open_tiktok1(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")

    def open_snapchat(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])




        #self.hide()  # Masquer le module de connexion
        tab_name = "Snapchat"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
            self.face_main = InstaMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)
    # Fonction pour ouvrir Blogging
    def open_snapchat1(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")

    def open_reddit(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])



        #self.hide()  # Masquer le module de connexion
        tab_name = "Reddit"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
            self.face_main = RedditMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)
    # Fonction pour ouvrir Blogging
    def open_reddit1(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")


    def open_pinterest(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])



        #self.hide()  # Masquer le module de connexion
        tab_name = "Pinterest"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
            self.face_main = InstaMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)

    # Fonction pour ouvrir Blogging
    def open_pinterest1(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")

    def open_linkedin(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])




        #self.hide()  # Masquer le module de connexion
        tab_name = "Linkedin"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
            self.face_main = LinkedingMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)

    # Fonction pour ouvrir Blogging
    def open_ssogging(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")


    def open_Emailing(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])



        #self.hide()  # Masquer le module de connexion
        tab_name = "Emailing"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
            self.face_main = MailMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)

    # Fonction pour ouvrir Blogging
    def open_Emailing1(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")

    def open_chatbot(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])




        #self.hide()  # Masquer le module de connexion
        tab_name = "Chatbot"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
           self.face_main = ChatBotMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)

    # Fonction pour ouvrir Blogging
    def open_chatbot1(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")

    def open_branding(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])




        #self.hide()  # Masquer le module de connexion
        tab_name = "Branding"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
            self.face_main = BrandMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)

    # Fonction pour ouvrir Blogging
    def open_branding1(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")

    def open_adsPro(self):
  #subprocess.Popen([sys.executable, "whatsapp.py"])





        #self.hide()  # Masquer le module de connexion
        tab_name = "Ads Pro"  # Nom de l'onglet (correspond au label utilisé dans add_custom_tab)

        # Vérifiez si un onglet avec ce nom existe déjà
        existing_tab_index = self.find_tab_by_name(tab_name)
        if existing_tab_index != -1:
            # Si l'onglet existe déjà, sélectionnez-le
            self.main_app.tab_widget.setCurrentIndex(existing_tab_index)
            return

        # Sinon, créez une instance unique de Nova360ProApp et ajoutez un nouvel onglet
        if not hasattr(self, 'nova360pro') or self.nova360pro is None:
           # self.nova360pro = Nova360ProApp(main_app=self)  # Créez une seule fois l'instance
            self.face_main = AdsMainWindow()  # Remplacez ceci par votre classe de page d'accueil

        self.open_new_tab(tab_name,"cool.ico",self.face_main)

    # Fonction pour ouvrir Blogging
    def open_adsPro1(self):
        """
        Open the 'Upgrade' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")


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
        self.open_new_tab(button_text,"cool.ico")
        QMessageBox.information(self, "Info", f"Vous avez cliqué sur {button_text}!")
    def show_message1(self, button_text):
        """
        Open the 'Ads Pro Bot' window.
        """
        # QMessageBox.information(self, "Upgrade", "Upgrade your plan.")
        self.main_app.add_new_tab(QUrl("https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec"), self.tr("Upgrade"), "resources/icons/tok.ico")

    def open_link(self, url):
        # Ouvrir un lien dans le navigateur par défaut
        import webbrowser
        webbrowser.open(url)
    def open_help(self):
        QMessageBox.information(
        self,
        self.tr("Help"),
        self.tr(
            "📘 **Help Guide for nova360.turknovatech.com**\n\n"
            "Welcome to the nova360.turknovatech.com Help Center! Here, you'll find tips, tutorials, and support to help you make the most of nova360.turknovatech.com.\n\n"
            "🔹 **Getting Started**\n"
            "Learn how to set up your accounts, schedule posts, and automate engagement with our easy-to-follow guides.\n\n"
            "🔹 **FAQs**\n"
            "Find answers to frequently asked questions and common troubleshooting tips.\n\n"
            "🔹 **Technical Support**\n"
            "For further assistance, contact our support team: support@nova360.turknovatech.com\n\n"
            "🌐 **Visit Our Help Center**\n"
            "Check out our online Help Center for additional resources and community forums: [www.nova360.turknovatech.com/help](https://www.nova360.turknovatech.com/help)\n\n"
            "We're here to help you succeed!\n"
        )
                )
    def show_about (self):
        QMessageBox.information(
            self,
            self.tr("About nova360.turknovatech.com"),
            self.tr(
                "🧠 **nova360.turknovatech.com - The Ultimate Social Media Automation Solution**\n\n"
                "Version: 1.0.0\n"
                "Release Date: November 2024\n\n"
                "🌍 **Empower Your Influence**\n"
                "Effortlessly grow your presence across all major social media platforms – Facebook, WhatsApp, YouTube, LinkedIn, Pinterest, and more.\n\n"
                "🚀 **Features**\n"
                "- Automatic post scheduling and sharing\n"
                "- Advanced engagement and comment automation\n"
                "- Analytics and performance tracking\n\n"
                "📞 **Need Help?**\n"
                "Contact our support: support@nova360.turknovatech.com\n"
                "Visit our website: [www.nova360.turknovatech.com](https://www.nova360.turknovatech.com)\n\n"
                "© 2024 Nova360 Pro - nova360.turknovatech.com. All rights reserved.\n"
            )
        )


    def side_menu_action(self, action):
        # Actions pour les boutons du menu latéral
        if action == "Accueil":
            QMessageBox.information(self, "Accueil", "Bienvenue à l'accueil!")
        elif action == "Paramètres":
            QMessageBox.information(self, "Paramètres", "Ouvrir les paramètres...")
        elif action == "Aide":
           # QMessageBox.information(self, "Aide", "Ouvrir l'aide...")
           QMessageBox.information(
                    self,
                    self.tr("Help"),
                    self.tr(
                        "📘 **Help Guide for nova360.turknovatech.com**\n\n"
                        "Welcome to the nova360.turknovatech.com Help Center! Here, you'll find tips, tutorials, and support to help you make the most of nova360.turknovatech.com.\n\n"
                        "🔹 **Getting Started**\n"
                        "Learn how to set up your accounts, schedule posts, and automate engagement with our easy-to-follow guides.\n\n"
                        "🔹 **FAQs**\n"
                        "Find answers to frequently asked questions and common troubleshooting tips.\n\n"
                        "🔹 **Technical Support**\n"
                        "For further assistance, contact our support team: support@nova360.turknovatech.com\n\n"
                        "🌐 **Visit Our Help Center**\n"
                        "Check out our online Help Center for additional resources and community forums: [www.nova360.turknovatech.com/help](https://www.nova360.turknovatech.com/help)\n\n"
                        "We're here to help you succeed!\n"
                    )
                )

        elif action == "À propos":
           # QMessageBox.information(self, "À propos", "AI FB ROBOT PRO v1.0\n© 2024 Nova360 Pro")
           QMessageBox.information(
                        self,
                        self.tr("About nova360.turknovatech.com"),
                        self.tr(
                            "🧠 **nova360.turknovatech.com - The Ultimate Social Media Automation Solution**\n\n"
                            "Version: 1.0.0\n"
                            "Release Date: November 2024\n\n"
                            "🌍 **Empower Your Influence**\n"
                            "Effortlessly grow your presence across all major social media platforms – Facebook, WhatsApp, YouTube, LinkedIn, Pinterest, and more.\n\n"
                            "🚀 **Features**\n"
                            "- Automatic post scheduling and sharing\n"
                            "- Advanced engagement and comment automation\n"
                            "- Analytics and performance tracking\n\n"
                            "📞 **Need Help?**\n"
                            "Contact our support: support@nova360.turknovatech.com\n"
                            "Visit our website: [www.nova360.turknovatech.com](https://www.nova360.turknovatech.com)\n\n"
                            "© 2024 Nova360 Pro - nova360.turknovatech.com. All rights reserved.\n"
                        )
                    )

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