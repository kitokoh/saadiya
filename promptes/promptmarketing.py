import sys
import random
import time
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTextEdit, QPushButton, QRadioButton, QButtonGroup, 
                             QFrame, QScrollArea, QSpacerItem, QSizePolicy, QStackedWidget,
                             QProgressBar, QSystemTrayIcon, QMenu, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QSize, QThread, pyqtSignal, QPoint, QEasingCurve
from PyQt5.QtGui import (QFont, QColor, QPalette, QPixmap, QIcon, QLinearGradient, 
                         QPainter, QCursor, QDesktopServices)
from PyQt5.QtMultimedia import QSound
import sqlite3
from sqlite3 import Error
import json
import webbrowser
import markdown2
import platform
import os
from plyer import notification
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGraphicsOpacityEffect

class AnalysisThread(QThread):
    """Thread séparé pour l'analyse du prompt"""
    analysis_complete = pyqtSignal(str, list)
    error_occurred = pyqtSignal(str)

    def __init__(self, prompt_text, db_conn):
        super().__init__()
        self.prompt_text = prompt_text
        self.db_conn = db_conn

    def run(self):
        try:
            # Simulation d'un traitement long
            time.sleep(1)
            
            # Analyse réelle
            cursor = self.db_conn.cursor()
            prompt_lower = self.prompt_text.lower()
            detected = []
            
            cursor.execute('SELECT keyword, platform, response_template FROM detection_rules')
            rules = cursor.fetchall()
            
            for keyword, platform, template in rules:
                if keyword in prompt_lower:
                    detected.append((keyword, platform, template))
            
            # Générer le texte d'analyse
            analysis_text = "## 📊 Analyse de votre demande\n\n"
            
            if not detected:
                analysis_text += ("Je comprends que vous souhaitez promouvoir votre contenu ou produit. "
                                "Voici des recommandations générales basées sur les meilleures pratiques marketing actuelles.")
            else:
                unique_platforms = list(set([p[1] for p in detected]))
                if len(unique_platforms) == 1:
                    analysis_text += f"Votre demande concerne principalement **{unique_platforms[0].capitalize()}**.\n\n"
                else:
                    platforms_str = ', '.join([p.capitalize() for p in unique_platforms])
                    analysis_text += f"Votre demande couvre plusieurs plateformes : **{platforms_str}**.\n\n"
                
                analysis_text += "J'ai identifié les opportunités suivantes :\n"
                for _, platform, template in detected:
                    analysis_text += f"- {template}\n"
            
            # Ajouter des conseils généraux
            analysis_text += "\n## 💡 Conseils supplémentaires\n"
            tips = [
                "Optimisez votre contenu pour chaque plateforme",
                "Utilisez des visuels attrayants et cohérents",
                "Planifiez vos publications à des heures stratégiques",
                "Mesurez les résultats pour ajuster votre stratégie"
            ]
            analysis_text += "\n".join(f"- {tip}" for tip in tips)
            
            self.analysis_complete.emit(analysis_text, detected)
            
        except Exception as e:
            self.error_occurred.emit(f"Erreur d'analyse : {str(e)}")

class MarketingAIAnalyzer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Marketing AI Assistant Pro")
        self.setMinimumSize(1000, 700)
        
        # Configuration initiale
        self.current_user = "Utilisateur"
        self.history = []
        self.settings = {
            "dark_mode": False,
            "animations": True,
            "notifications": True
        }
        
        # Initialisation des composants
        self.init_db()

        self.init_ui()
        self.init_tray_icon()
        # self.load_settings()
        
        # Style global
        self.update_styles()
        
        # # Tutoriel initial
        # if not self.settings.get("tutorial_shown"):
        #     self.show_tutorial()
        #     self.settings["tutorial_shown"] = True
        #     self.save_settings()

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        # Widget central et layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Création de la sidebar
        # self.create_sidebar()
        
        # Zone de contenu principale
        self.content_area = QWidget()
        self.content_area.setObjectName("contentArea")
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)
        
        # Stacked widget pour les différentes vues
        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)
        
        # Vue principale
        self.main_view = QWidget()
        self.setup_main_view()
        self.stacked_widget.addWidget(self.main_view)
        
        # Vue historique
        self.history_view = QWidget()
        self.setup_history_view()
        self.stacked_widget.addWidget(self.history_view)
        
        # Vue paramètres
        self.settings_view = QWidget()
        # self.setup_settings_view()
        self.stacked_widget.addWidget(self.settings_view)
        
        self.main_layout.addWidget(self.content_area, stretch=1)
        
        # Barre de statut
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Prêt")
        
        # Configuration de la fenêtre
        self.setWindowIcon(QIcon(self.resource_path("assets/ai_icon.png")))
        
    def create_sidebar(self):
        """Crée la sidebar de navigation"""
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setMinimumWidth(250)
        self.sidebar.setMaximumWidth(300)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        sidebar_layout.setSpacing(20)
        
        # Logo et titre
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap(self.resource_path("assets/logo.png")).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(self.logo_pixmap)
        
        self.title_label = QLabel("Marketing AI")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3b82f6;")
        
        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(self.title_label)
        sidebar_layout.addLayout(logo_layout)
        
        # Menu de navigation
        nav_layout = QVBoxLayout()
        nav_layout.setSpacing(10)
        
        self.btn_home = self.create_nav_button("Accueil", "home.png", "Accéder au tableau de bord principal")
        self.btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        self.btn_history = self.create_nav_button("Historique", "history.png", "Voir l'historique des analyses")
        self.btn_history.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        self.btn_settings = self.create_nav_button("Paramètres", "settings.png", "Configurer l'application")
        self.btn_settings.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        
        nav_layout.addWidget(self.btn_home)
        nav_layout.addWidget(self.btn_history)
        nav_layout.addWidget(self.btn_settings)
        
        sidebar_layout.addLayout(nav_layout)
        sidebar_layout.addStretch()
        
        # User info
        user_layout = QHBoxLayout()
        
        self.user_icon = QLabel()
        self.user_pixmap = QPixmap(self.resource_path("assets/user.png")).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.user_icon.setPixmap(self.user_pixmap)
        
        self.user_label = QLabel(self.current_user)
        self.user_label.setStyleSheet("font-size: 14px;")
        
        user_layout.addWidget(self.user_icon)
        user_layout.addWidget(self.user_label)
        user_layout.addStretch()
        
       # sidebar_layout.addLayout(user_layout)
        
        self.main_layout.addWidget(self.sidebar)
    
    def create_nav_button(self, text, icon, tooltip):
        """Crée un bouton de navigation stylisé"""
        btn = QPushButton(text)
        btn.setIcon(QIcon(self.resource_path(f"assets/{icon}")))
        btn.setIconSize(QSize(20, 20))
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 12px 15px;
                border-radius: 8px;
                font-size: 14px;
                color: #4b5563;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
            QPushButton:pressed {
                background-color: #d1d5db;
            }
        """)
        return btn
    
    def setup_main_view(self):
        """Configure la vue principale"""
        layout = QVBoxLayout(self.main_view)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # En-tête
        header = QLabel("Assistant Marketing Intelligent")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #1e40af;")
        layout.addWidget(header)
        
        # Sous-titre
        subheader = QLabel("Obtenez des recommandations personnalisées pour vos campagnes marketing")
        subheader.setStyleSheet("font-size: 16px; color: #6b7280;")
        layout.addWidget(subheader)
        
        # Zone de prompt
        self.setup_prompt_section()
        layout.addWidget(self.prompt_container)
        
        # Section d'analyse
        self.analysis_container = QWidget()
        self.analysis_container.setVisible(False)
        analysis_layout = QVBoxLayout(self.analysis_container)
        analysis_layout.setContentsMargins(0, 0, 0, 0)
        analysis_layout.setSpacing(15)
        
        # Barre de progression pour l'analyse
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        analysis_layout.addWidget(self.progress_bar)
        
        # Résultats d'analyse
        self.analysis_result = QTextEdit()
        self.analysis_result.setReadOnly(True)
        self.analysis_result.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                color: #334155;
            }
        """)
        analysis_layout.addWidget(self.analysis_result)
        
        # Options recommandées
        self.options_group = QButtonGroup()
        self.options_container = QWidget()
        options_layout = QVBoxLayout(self.options_container)
        options_layout.setContentsMargins(0, 10, 0, 0)
        options_layout.setSpacing(10)
        
        options_header = QLabel("Actions recommandées:")
        options_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e40af;")
        options_layout.addWidget(options_header)
        
        # Création des options dynamiques
        self.platform_options = {
            "facebook": ("Publier dans des groupes Facebook", "facebook.png"),
            "whatsapp": ("Envoyer des messages WhatsApp", "whatsapp.png"),
            "email": ("Créer une campagne email", "email.png"),
            "instagram": ("Lancer une publicité Instagram", "instagram.png"),
            "tiktok": ("Créer une vidéo TikTok", "tiktok.png"),
            "linkedin": ("Publier sur LinkedIn", "linkedin.png"),
            "twitter": ("Créer une campagne Twitter", "twitter.png"),
            "youtube": ("Publier une vidéo YouTube", "youtube.png")
        }
        
        for platform, (text, icon) in self.platform_options.items():
            btn = self.create_option_button(text, icon)
            self.options_group.addButton(btn)
            options_layout.addWidget(btn)
        
        # Bouton d'exécution
        self.execute_btn = QPushButton("Exécuter la stratégie")
        self.execute_btn.setIcon(QIcon(self.resource_path("assets/execute.png")))
        self.execute_btn.setIconSize(QSize(20, 20))
        self.execute_btn.setCursor(Qt.PointingHandCursor)
        self.execute_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0d9e6e;
            }
            QPushButton:pressed {
                background-color: #0b845d;
            }
            QPushButton:disabled {
                background-color: #d1fae5;
            }
        """)
        self.execute_btn.clicked.connect(self.execute_strategy)
        self.execute_btn.setEnabled(False)
        options_layout.addWidget(self.execute_btn, alignment=Qt.AlignRight)
        
        analysis_layout.addWidget(self.options_container)
        layout.addWidget(self.analysis_container)
        
        # Boutons d'actions supplémentaires
        action_buttons = QHBoxLayout()
        action_buttons.setSpacing(10)
        
        self.save_btn = QPushButton("Enregistrer l'analyse")
        self.save_btn.setIcon(QIcon(self.resource_path("assets/save.png")))
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_analysis)
        self.save_btn.setEnabled(False)
        
        self.export_btn = QPushButton("Exporter en PDF")
        self.export_btn.setIcon(QIcon(self.resource_path("assets/pdf.png")))
        self.export_btn.setCursor(Qt.PointingHandCursor)
        self.export_btn.clicked.connect(self.export_to_pdf)
        self.export_btn.setEnabled(False)
        
        action_buttons.addWidget(self.save_btn)
        action_buttons.addWidget(self.export_btn)
        action_buttons.addStretch()
        
        layout.addLayout(action_buttons)
    
    def setup_prompt_section(self):
        """Configure la section de saisie du prompt"""
        self.prompt_container = QWidget()
        self.prompt_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                padding: 2px;
            }
        """)

        container_layout = QVBoxLayout(self.prompt_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Champ de texte avec placeholder stylisé
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Décrivez votre besoin marketing...\nEx: Je veux promouvoir mon nouveau produit sur les réseaux sociaux pour toucher les jeunes entrepreneurs.")
        self.prompt_input.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: none;
                font-size: 15px;
                font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
                color: #111827;
                padding: 15px;
            }
            QTextEdit:focus {
                outline: none;
            }
        """)
        self.prompt_input.setMinimumHeight(120)
        self.prompt_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

        # Barre d'outils en bas du champ
        toolbar = QWidget()
        toolbar.setStyleSheet("background-color: #f8fafc; border-top: 1px solid #e2e8f0; border-radius: 0 0 8px 8px;")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        toolbar_layout.setSpacing(10)

        # Bouton d'analyse
        self.analyze_btn = QPushButton("Analyser")
        self.analyze_btn.setIcon(QIcon(self.resource_path("assets/analyze.png")))
        self.analyze_btn.setIconSize(QSize(18, 18))
        self.analyze_btn.setCursor(Qt.PointingHandCursor)
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        self.analyze_btn.clicked.connect(self.analyze_prompt)

        # Indicateur de longueur du texte
        self.text_length = QLabel("0/1000")
        self.text_length.setStyleSheet("color: #94a3b8; font-size: 12px;")
        self.prompt_input.textChanged.connect(self.update_text_length)

        toolbar_layout.addWidget(self.analyze_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.text_length)

        container_layout.addWidget(self.prompt_input)
        container_layout.addWidget(toolbar)
    
    def update_text_length(self):
        """Met à jour l'indicateur de longueur du texte"""
        length = len(self.prompt_input.toPlainText())
        self.text_length.setText(f"{length}/1000")
        
        # Changer la couleur si on approche de la limite
        if length > 900:
            self.text_length.setStyleSheet("color: #ef4444; font-size: 12px;")
        else:
            self.text_length.setStyleSheet("color: #94a3b8; font-size: 12px;")
    
    def create_option_button(self, text, icon):
        """Crée un bouton d'option stylisé"""
        btn = QRadioButton(text)
        btn.setIcon(QIcon(self.resource_path(f"assets/{icon}")))
        btn.setIconSize(QSize(24, 24))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QRadioButton {
                text-align: left;
                padding: 12px 15px;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                font-size: 14px;
                color: #334155;
                background-color: #ffffff;
            }
            QRadioButton:hover {
                background-color: #f1f5f9;
                border-color: #cbd5e1;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #cbd5e1;
            }
            QRadioButton::indicator:checked {
                background-color: #3b82f6;
                border-color: #3b82f6;
            }
        """)
        return btn
    
    def setup_history_view(self):
        """Configure la vue historique"""
        layout = QVBoxLayout(self.history_view)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # En-tête
        header = QLabel("Historique des Analyses")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #1e40af;")
        layout.addWidget(header)
        
        # Barre de recherche et filtres
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        self.search_input = QTextEdit()
        self.search_input.setMaximumHeight(40)
        self.search_input.setPlaceholderText("Rechercher dans l'historique...")
        self.search_input.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }
        """)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Toutes les plateformes", "Facebook", "Instagram", "Email", "WhatsApp", "TikTok"])
        self.filter_combo.setStyleSheet("""
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                min-width: 150px;
            }
        """)
        
        search_btn = QPushButton("Rechercher")
        search_btn.setIcon(QIcon(self.resource_path("assets/search.png")))
        search_btn.setCursor(Qt.PointingHandCursor)
        search_btn.clicked.connect(self.search_history)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.filter_combo)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)
        
        # Zone de défilement pour l'historique
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none; background: transparent;")
        
        self.history_content = QWidget()
        self.history_content_layout = QVBoxLayout(self.history_content)
        self.history_content_layout.setContentsMargins(5, 5, 5, 5)
        self.history_content_layout.setSpacing(15)
        
        # Charger l'historique
        self.load_history_items()
        
        scroll_area.setWidget(self.history_content)
        layout.addWidget(scroll_area)
    
    def load_history_items(self):
        """Charge les éléments de l'historique depuis la base de données"""
        # Nettoyer d'abord le layout
        for i in reversed(range(self.history_content_layout.count())): 
            self.history_content_layout.itemAt(i).widget().setParent(None)
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, prompt_text, analysis_result, created_at FROM prompts ORDER BY created_at DESC")
            history_items = cursor.fetchall()
            
            if not history_items:
                no_history = QLabel("Aucun historique d'analyse pour le moment.")
                no_history.setStyleSheet("font-size: 14px; color: #64748b;")
                no_history.setAlignment(Qt.AlignCenter)
                self.history_content_layout.addWidget(no_history)
                return
            
            for item_id, prompt, analysis, created_at in history_items:
                history_item = self.create_history_item(item_id, prompt, analysis, created_at)
                self.history_content_layout.addWidget(history_item)
            
            self.history_content_layout.addStretch()
            
        except Error as e:
            QMessageBox.warning(self, "Erreur", f"Impossible de charger l'historique : {str(e)}")
    
    def create_history_item(self, item_id, prompt, analysis, created_at):
        """Crée un widget d'élément d'historique"""
        item = QWidget()
        item.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        layout = QVBoxLayout(item)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Première ligne : date + boutons d'action
        top_layout = QHBoxLayout()
        
        date_label = QLabel(datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M"))
        date_label.setStyleSheet("font-size: 13px; color: #64748b;")
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(5)
        
        view_btn = QPushButton()
        view_btn.setIcon(QIcon(self.resource_path("assets/view.png")))
        view_btn.setToolTip("Voir les détails")
        view_btn.setCursor(Qt.PointingHandCursor)
        view_btn.setStyleSheet("QPushButton { border: none; padding: 5px; }")
        view_btn.clicked.connect(lambda: self.view_history_item(item_id))
        
        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon(self.resource_path("assets/delete.png")))
        delete_btn.setToolTip("Supprimer")
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet("QPushButton { border: none; padding: 5px; }")
        delete_btn.clicked.connect(lambda: self.delete_history_item(item_id))
        
        btn_layout.addWidget(view_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addStretch()
        
        top_layout.addWidget(date_label)
        top_layout.addLayout(btn_layout)
        
        # Prompt (texte tronqué)
        prompt_label = QLabel(prompt if len(prompt) < 100 else f"{prompt[:100]}...")
        prompt_label.setStyleSheet("font-size: 14px; color: #1e293b; font-weight: 500;")
        prompt_label.setWordWrap(True)
        
        layout.addLayout(top_layout)
        layout.addWidget(prompt_label)
        
        return item
    
    def setup_settings_view(self):
        """Configure la vue des paramètres"""
        layout = QVBoxLayout(self.settings_view)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # En-tête
        header = QLabel("Paramètres")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #1e40af;")
        layout.addWidget(header)
        
        # Options générales
        general_group = QGroupBox("Préférences générales")
        general_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                margin-top: 10px;
                font-weight: bold;
                color: #334155;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        general_layout = QVBoxLayout(general_group)
        general_layout.setSpacing(15)
        
        # Mode sombre
        self.dark_mode = QCheckBox("Activer le mode sombre")
        self.dark_mode.setChecked(self.settings["dark_mode"])
        self.dark_mode.stateChanged.connect(self.toggle_dark_mode)
        
        # Animations
        self.animations = QCheckBox("Activer les animations")
        self.animations.setChecked(self.settings["animations"])
        self.animations.stateChanged.connect(lambda: self.update_setting("animations", self.animations.isChecked()))
        
        # Notifications
        self.notifications = QCheckBox("Activer les notifications")
        self.notifications.setChecked(self.settings["notifications"])
        self.notifications.stateChanged.connect(lambda: self.update_setting("notifications", self.notifications.isChecked()))
        
        general_layout.addWidget(self.dark_mode)
        general_layout.addWidget(self.animations)
        general_layout.addWidget(self.notifications)
        
        # Paramètres de compte
        account_group = QGroupBox("Compte")
        account_layout = QVBoxLayout(account_group)
        
        # Nom d'utilisateur
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("Nom d'utilisateur:"))
        
        self.username_input = QLineEdit(self.current_user)
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        self.username_input.textChanged.connect(self.update_username)
        username_layout.addWidget(self.username_input)
        account_layout.addLayout(username_layout)
        
        # Bouton de réinitialisation
        reset_btn = QPushButton("Réinitialiser les préférences")
        reset_btn.setCursor(Qt.PointingHandCursor)
        reset_btn.clicked.connect(self.reset_settings)
        account_layout.addWidget(reset_btn, alignment=Qt.AlignRight)
        
        layout.addWidget(general_group)
        layout.addWidget(account_group)
        layout.addStretch()
    
    def init_db(self):
        """Initialise la base de données SQLite"""
        try:
            db_path = self.resource_path("marketing_ai.db")
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            
            # Créer la table pour les prompts et analyses
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_text TEXT NOT NULL,
                    analysis_result TEXT,
                    actions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Créer la table pour les règles de détection
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS detection_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    response_template TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table des paramètres utilisateur
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            
            # Insérer des règles de base si la table est vide
            self.cursor.execute('SELECT COUNT(*) FROM detection_rules')
            if self.cursor.fetchone()[0] == 0:
                base_rules = [
                    ('facebook', 'facebook', 'Publication dans des groupes Facebook ciblés'),
                    ('groupes', 'facebook', 'Publication dans des groupes Facebook ciblés'),
                    ('whatsapp', 'whatsapp', 'Envoi de messages WhatsApp personnalisés'),
                    ('email', 'email', 'Campagne email marketing segmentée'),
                    ('instagram', 'instagram', 'Publicité Instagram ciblée avec hashtags'),
                    ('tiktok', 'tiktok', 'Création de vidéo TikTok promotionnelle'),
                    ('réseaux sociaux', 'multi', 'Campagne multi-plateformes sur les réseaux sociaux'),
                    ('linkedin', 'linkedin', 'Publication professionnelle sur LinkedIn'),
                    ('twitter', 'twitter', 'Campagne Twitter avec mots-clés tendance'),
                    ('youtube', 'youtube', 'Vidéo YouTube avec call-to-action'),
                    ('influenceurs', 'influence', 'Collaboration avec des influenceurs'),
                    ('publicité', 'ads', 'Campagne publicitaire payante'),
                    ('seo', 'seo', 'Optimisation pour les moteurs de recherche'),
                    ('site web', 'website', 'Optimisation du site web'),
                    ('blog', 'blog', 'Stratégie de contenu pour blog'),
                ]
                
                self.cursor.executemany('''
                    INSERT INTO detection_rules (keyword, platform, response_template)
                    VALUES (?, ?, ?)
                ''', base_rules)
                self.conn.commit()
                
        except Error as e:
            QMessageBox.critical(self, "Erreur de base de données", f"Impossible d'initialiser la base de données : {str(e)}")
    
    def init_tray_icon(self):
        """Initialise l'icône de la barre système"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
            
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.resource_path("assets/tray_icon.png")))
        
        tray_menu = QMenu()
        
        show_action = tray_menu.addAction("Ouvrir")
        show_action.triggered.connect(self.show_normal)
        
        exit_action = tray_menu.addAction("Quitter")
        exit_action.triggered.connect(self.close)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # Connecter le double-clic pour afficher l'application
        self.tray_icon.activated.connect(self.tray_icon_activated)
    
    def tray_icon_activated(self, reason):
        """Gère les interactions avec l'icône de la barre système"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_normal()
    
    def show_normal(self):
        """Affiche la fenêtre normalement"""
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()
    
    def load_settings(self):
        """Charge les paramètres utilisateur depuis la base de données"""
        try:
            self.cursor.execute("SELECT key, value FROM user_settings")
            settings = self.cursor.fetchall()
            
            for key, value in settings:
                if key == "dark_mode":
                    self.settings["dark_mode"] = value == "True"
                elif key == "animations":
                    self.settings["animations"] = value == "True"
                elif key == "notifications":
                    self.settings["notifications"] = value == "True"
                elif key == "username":
                    self.current_user = value
                    self.user_label.setText(value)
            
        except Error as e:
            print(f"Erreur lors du chargement des paramètres : {e}")
    
    def save_settings(self):
        """Enregistre les paramètres utilisateur dans la base de données"""
        try:
            # Supprimer les anciens paramètres
            self.cursor.execute("DELETE FROM user_settings")
            
            # Insérer les nouveaux
            settings_to_save = [
                ("dark_mode", str(self.settings["dark_mode"])),
                ("animations", str(self.settings["animations"])),
                ("notifications", str(self.settings["notifications"])),
                ("username", self.current_user),
                ("tutorial_shown", str(self.settings.get("tutorial_shown", False)))
            ]
            
            self.cursor.executemany("""
                INSERT INTO user_settings (key, value)
                VALUES (?, ?)
            """, settings_to_save)
            
            self.conn.commit()
            
        except Error as e:
            print(f"Erreur lors de l'enregistrement des paramètres : {e}")
    
    def update_setting(self, key, value):
        """Met à jour un paramètre et l'enregistre"""
        self.settings[key] = value
        self.save_settings()
    
    def update_username(self):
        """Met à jour le nom d'utilisateur"""
        new_name = self.username_input.text().strip()
        if new_name and new_name != self.current_user:
            self.current_user = new_name
            self.user_label.setText(new_name)
            self.save_settings()
    
    def toggle_dark_mode(self, state):
        """Active/désactive le mode sombre"""
        dark_mode = state == Qt.Checked
        self.settings["dark_mode"] = dark_mode
        self.save_settings()
        self.update_styles()
    
    def update_styles(self):
        """Met à jour les styles CSS de l'application"""
        if self.settings["dark_mode"]:
            self.set_dark_theme()
        else:
            self.set_light_theme()
    
    def set_light_theme(self):
        """Applique le thème clair"""
        # Style général
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #f8fafc;
            }
            #sidebar {
                background-color: #ffffff;
                border-right: 1px solid #e2e8f0;
            }
            #contentArea {
                background-color: #f8fafc;
            }
            QTextEdit, QLineEdit, QComboBox {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                color: #334155;
            }
            QLabel {
                color: #334155;
            }
        """)
        
        # # Mettre à jour les icônes pour le mode clair
        # self.logo_pixmap = QPixmap(self.resource_path("assets/logo.png")).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.logo_label.setPixmap(self.logo_pixmap)
        
        # self.user_pixmap = QPixmap(self.resource_path("assets/user.png")).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.user_icon.setPixmap(self.user_pixmap)
    
    def set_dark_theme(self):
        """Applique le thème sombre"""
        # Style général
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #0f172a;
            }
            #sidebar {
                background-color: #1e293b;
                border-right: 1px solid #334155;
            }
            #contentArea {
                background-color: #0f172a;
            }
            QTextEdit, QLineEdit, QComboBox {
                background-color: #1e293b;
                border: 1px solid #334155;
                color: #e2e8f0;
            }
            QLabel {
                color: #e2e8f0;
            }
            QGroupBox {
                color: #94a3b8;
            }
        """)
        
        # Mettre à jour les icônes pour le mode sombre
        self.logo_pixmap = QPixmap(self.resource_path("assets/logo_light.png")).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(self.logo_pixmap)
        
        self.user_pixmap = QPixmap(self.resource_path("assets/user_light.png")).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.user_icon.setPixmap(self.user_pixmap)
    
    def resource_path(self, relative_path):
        """Gère correctement les chemins des ressources pour le déploiement"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)
    
    def analyze_prompt(self):
        """Analyse le prompt de l'utilisateur"""
        prompt_text = self.prompt_input.toPlainText().strip()
        if not prompt_text:
            self.show_notification("Erreur", "Veuillez saisir une demande à analyser")
            return
        
        # Désactiver le bouton pendant l'analyse
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setText("Analyse en cours...")
        
        # Afficher la section d'analyse avec animation
        self.animate_analysis_start()
        
        # Lancer l'analyse dans un thread séparé
        self.analysis_thread = AnalysisThread(prompt_text, self.conn)
        self.analysis_thread.analysis_complete.connect(self.handle_analysis_result)
        self.analysis_thread.error_occurred.connect(self.handle_analysis_error)
        self.analysis_thread.start()
        
        # Simuler une progression
        self.progress_value = 0
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(50)
    
    def animate_analysis_start(self):
        """Animation au début de l'analyse"""
        self.analysis_container.setVisible(True)
        self.analysis_container.setGraphicsEffect(self.create_fade_effect())
        
        if self.settings["animations"]:
            # Animation de hauteur
            self.analysis_container.setMaximumHeight(0)
            self.animation = QPropertyAnimation(self.analysis_container, b"maximumHeight")
            self.animation.setDuration(500)
            self.animation.setStartValue(0)
            self.animation.setEndValue(500)
            self.animation.setEasingCurve(QEasingCurve.OutCubic)
            self.animation.start()
    
    def create_fade_effect(self):
        """Crée un effet de fondu"""
        effect = QGraphicsOpacityEffect()
        effect.setOpacity(0)
        
        if self.settings["animations"]:
            fade_anim = QPropertyAnimation(effect, b"opacity")
            fade_anim.setDuration(400)
            fade_anim.setStartValue(0)
            fade_anim.setEndValue(1)
            fade_anim.start()
        
        return effect
    
    def update_progress(self):
        """Met à jour la barre de progression"""
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)
        
        if self.progress_value >= 100:
            self.progress_timer.stop()
    
    def handle_analysis_result(self, analysis_text, detected_platforms):
        """Gère les résultats de l'analyse"""
        # Réactiver le bouton
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("Analyser")
        
        # Afficher les résultats
        self.analysis_result.setHtml(markdown2.markdown(analysis_text))
        
        # Afficher les options pertinentes
        self.show_relevant_options(detected_platforms)
        
        # Activer les boutons d'action
        self.execute_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.export_btn.setEnabled(True)
        
        # Enregistrer dans l'historique
        self.save_to_history(analysis_text, detected_platforms)
        
        # Notification
        if self.settings["notifications"]:
            self.show_notification("Analyse terminée", "Vos recommandations marketing sont prêtes!")
    
    def handle_analysis_error(self, error_msg):
        """Gère les erreurs d'analyse"""
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("Analyser")
        self.analysis_result.setText(f"<span style='color: #ef4444;'>Erreur : {error_msg}</span>")
        
        if self.settings["notifications"]:
            self.show_notification("Erreur d'analyse", error_msg)
    
    def show_relevant_options(self, detected_platforms):
        """Affiche les options pertinentes selon l'analyse"""
        # Si aucune détection, montrer toutes les options
        if not detected_platforms:
            for btn in self.options_group.buttons():
                btn.show()
            return
        
        # Cacher toutes les options d'abord
        for btn in self.options_group.buttons():
            btn.hide()
        
        # Montrer les options pertinentes
        platforms_to_show = list(set([p[1] for p in detected_platforms]))
        
        for btn in self.options_group.buttons():
            btn_text_lower = btn.text().lower()
            for platform in platforms_to_show:
                if platform in btn_text_lower:
                    btn.show()
                    break
            else:
                # Pour le cas "multi" ou autres règles spéciales
                if "multi" in platforms_to_show:
                    btn.show()
    
    def save_to_history(self, analysis_text, detected_platforms):
        """Enregistre l'analyse dans l'historique"""
        prompt_text = self.prompt_input.toPlainText().strip()
        platforms = ','.join([p[1] for p in detected_platforms]) if detected_platforms else ""
        
        try:
            self.cursor.execute('''
                INSERT INTO prompts (prompt_text, analysis_result, actions)
                VALUES (?, ?, ?)
            ''', (prompt_text, analysis_text, platforms))
            self.conn.commit()
            
            # Mettre à jour la vue historique si elle est active
            if self.stacked_widget.currentIndex() == 1:
                self.load_history_items()
                
        except Error as e:
            print(f"Erreur lors de l'enregistrement dans l'historique : {e}")
    
    def execute_strategy(self):
        """Exécute la stratégie sélectionnée"""
        selected_button = self.options_group.checkedButton()
        if not selected_button:
            self.show_notification("Action requise", "Veuillez sélectionner une stratégie à exécuter")
            return
        
        action = selected_button.text()
        
        # Simulation d'exécution
        self.execute_btn.setEnabled(False)
        self.execute_btn.setText("Exécution en cours...")
        
        # Enregistrer l'action
        try:
            self.cursor.execute('''
                INSERT INTO prompts (prompt_text, analysis_result, actions)
                VALUES (?, ?, ?)
            ''', (f"Action exécutée: {action}", "Action complétée", action))
            self.conn.commit()
            
            # Mettre à jour l'historique si nécessaire
            if self.stacked_widget.currentIndex() == 1:
                self.load_history_items()
                
        except Error as e:
            print(f"Erreur lors de l'enregistrement de l'action : {e}")
        
        # Animation de succès
        if self.settings["animations"]:
            original_text = self.execute_btn.text()
            self.execute_btn.setText("✓ Succès!")
            QTimer.singleShot(1500, lambda: self.execute_btn.setText(original_text))
        
        # Réactiver le bouton après un délai
        QTimer.singleShot(2000, lambda: self.execute_btn.setEnabled(True))
        
        # Mettre à jour le résultat
        current_html = self.analysis_result.toHtml()
        self.analysis_result.setHtml(current_html + f"<p><strong>✔ Action exécutée :</strong> {action}</p>")
        
        # Notification
        if self.settings["notifications"]:
            self.show_notification("Action exécutée", f"La stratégie '{action}' a été lancée avec succès")
    
    def save_analysis(self):
        """Enregistre l'analyse actuelle"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer l'analyse", "", 
            "Fichiers texte (*.txt);;Fichiers HTML (*.html);;Tous les fichiers (*)", 
            options=options)
        
        if file_name:
            try:
                if file_name.endswith('.html'):
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(self.analysis_result.toHtml())
                else:
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(self.analysis_result.toPlainText())
                
                self.show_notification("Enregistrement réussi", f"L'analyse a été sauvegardée dans {file_name}")
                
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Impossible d'enregistrer le fichier : {str(e)}")
    
    def export_to_pdf(self):
        """Exporte l'analyse en PDF"""
        # Dans une vraie application, vous utiliseriez un moteur de rendu PDF comme ReportLab
        # ou une bibliothèque comme WeasyPrint pour convertir HTML en PDF
        QMessageBox.information(
            self, 
            "Export PDF", 
            "Cette fonctionnalité nécessiterait une bibliothèque PDF supplémentaire.\n"
            "Dans une version complète, l'analyse serait exportée en PDF avec mise en page professionnelle.")
    
    def search_history(self):
        """Recherche dans l'historique"""
        search_text = self.search_input.toPlainText().strip().lower()
        filter_text = self.filter_combo.currentText()
        
        try:
            query = """
                SELECT id, prompt_text, analysis_result, created_at 
                FROM prompts 
                WHERE prompt_text LIKE ? OR analysis_result LIKE ?
            """
            params = (f"%{search_text}%", f"%{search_text}%")
            
            if filter_text != "Toutes les plateformes":
                query += " AND actions LIKE ?"
                params += (f"%{filter_text.lower()}%",)
            
            query += " ORDER BY created_at DESC"
            
            self.cursor.execute(query, params)
            history_items = self.cursor.fetchall()
            
            # Nettoyer le layout
            for i in reversed(range(self.history_content_layout.count())): 
                self.history_content_layout.itemAt(i).widget().setParent(None)
            
            if not history_items:
                no_results = QLabel("Aucun résultat trouvé.")
                no_results.setStyleSheet("font-size: 14px; color: #64748b;")
                no_results.setAlignment(Qt.AlignCenter)
                self.history_content_layout.addWidget(no_results)
                return
            
            for item_id, prompt, analysis, created_at in history_items:
                history_item = self.create_history_item(item_id, prompt, analysis, created_at)
                self.history_content_layout.addWidget(history_item)
            
            self.history_content_layout.addStretch()
            
        except Error as e:
            QMessageBox.warning(self, "Erreur", f"Impossible d'effectuer la recherche : {str(e)}")
    
    def view_history_item(self, item_id):
        """Affiche un élément d'historique en détail"""
        try:
            self.cursor.execute("""
                SELECT prompt_text, analysis_result, created_at 
                FROM prompts 
                WHERE id = ?
            """, (item_id,))
            
            prompt, analysis, created_at = self.cursor.fetchone()
            
            # Créer une fenêtre de détail
            detail_window = QDialog(self)
            detail_window.setWindowTitle(f"Analyse du {created_at}")
            detail_window.setMinimumSize(600, 500)
            
            layout = QVBoxLayout(detail_window)
            
            # Prompt original
            prompt_group = QGroupBox("Prompt original")
            prompt_layout = QVBoxLayout(prompt_group)
            
            prompt_text = QTextEdit()
            prompt_text.setPlainText(prompt)
            prompt_text.setReadOnly(True)
            prompt_layout.addWidget(prompt_text)
            
            # Analyse
            analysis_group = QGroupBox("Analyse et recommandations")
            analysis_layout = QVBoxLayout(analysis_group)
            
            analysis_text = QTextEdit()
            analysis_text.setHtml(analysis)
            analysis_text.setReadOnly(True)
            analysis_layout.addWidget(analysis_text)
            
            layout.addWidget(prompt_group)
            layout.addWidget(analysis_group)
            
            # Boutons
            btn_layout = QHBoxLayout()
            close_btn = QPushButton("Fermer")
            close_btn.clicked.connect(detail_window.close)
            
            export_btn = QPushButton("Exporter")
            export_btn.clicked.connect(lambda: self.export_history_item(prompt, analysis))
            
            btn_layout.addWidget(export_btn)
            btn_layout.addWidget(close_btn)
            layout.addLayout(btn_layout)
            
            detail_window.exec_()
            
        except Error as e:
            QMessageBox.warning(self, "Erreur", f"Impossible de charger les détails : {str(e)}")
    
    def export_history_item(self, prompt, analysis):
        """Exporte un élément d'historique"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Exporter l'analyse", "", 
            "Fichiers texte (*.txt);;Fichiers HTML (*.html);;Tous les fichiers (*)", 
            options=options)
        
        if file_name:
            try:
                if file_name.endswith('.html'):
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(f"<h1>Prompt original</h1><p>{prompt}</p><h1>Analyse</h1>{analysis}")
                else:
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(f"=== Prompt original ===\n{prompt}\n\n=== Analyse ===\n{markdown2.markdown(analysis)}")
                
                self.show_notification("Export réussi", "L'élément a été exporté avec succès")
                
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Impossible d'exporter : {str(e)}")
    
    def delete_history_item(self, item_id):
        """Supprime un élément d'historique"""
        reply = QMessageBox.question(
            self, 'Confirmation',
            'Voulez-vous vraiment supprimer cette analyse?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM prompts WHERE id = ?", (item_id,))
                self.conn.commit()
                
                # Recharger l'historique
                self.load_history_items()
                
                self.show_notification("Suppression réussie", "L'analyse a été supprimée de l'historique")
                
            except Error as e:
                QMessageBox.warning(self, "Erreur", f"Impossible de supprimer : {str(e)}")
    
    def reset_settings(self):
        """Réinitialise les paramètres par défaut"""
        reply = QMessageBox.question(
            self, 'Confirmation',
            'Voulez-vous vraiment réinitialiser tous les paramètres?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Réinitialiser les paramètres
            self.settings = {
                "dark_mode": False,
                "animations": True,
                "notifications": True,
                "tutorial_shown": True
            }
            
            # Mettre à jour l'interface
            self.dark_mode.setChecked(False)
            self.animations.setChecked(True)
            self.notifications.setChecked(True)
            self.username_input.setText("Utilisateur")
            
            # Sauvegarder
            self.save_settings()
            
            # Mettre à jour le style
            self.update_styles()
            
            self.show_notification("Paramètres réinitialisés", "Tous les paramètres ont été restaurés")
    
    def show_tutorial(self):
        """Affiche le tutoriel d'utilisation"""
        tutorial = QDialog(self)
        tutorial.setWindowTitle("Bienvenue dans Marketing AI Assistant")
        tutorial.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(tutorial)
        
        # Contenu du tutoriel
        content = QTextEdit()
        content.setReadOnly(True)
        content.setHtml("""
            <h1>Bienvenue dans Marketing AI Assistant</h1>
            <p>Cet outil vous aide à créer des stratégies marketing efficaces basées sur l'IA.</p>
            
            <h2>Comment ça marche ?</h2>
            <ol>
                <li>Saisissez votre besoin marketing dans la zone de texte</li>
                <li>Cliquez sur "Analyser" pour obtenir des recommandations</li>
                <li>Sélectionnez une stratégie et cliquez sur "Exécuter"</li>
                <li>Consultez l'historique pour revoir vos analyses précédentes</li>
            </ol>
            
            <h2>Fonctionnalités clés</h2>
            <ul>
                <li>Analyse intelligente des besoins marketing</li>
                <li>Recommandations personnalisées par plateforme</li>
                <li>Historique complet de toutes vos analyses</li>
                <li>Export des résultats en différents formats</li>
            </ul>
            
            <p>Commencez dès maintenant en saisissant votre première demande!</p>
        """)
        
        # Bouton de fermeture
        close_btn = QPushButton("Commencer")
        close_btn.clicked.connect(tutorial.close)
        
        layout.addWidget(content)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
        
        tutorial.exec_()
    
    def show_notification(self, title, message):
        """Affiche une notification système"""
        if self.settings["notifications"]:
            try:
                notification.notify(
                    title=title,
                    message=message,
                    app_name="Marketing AI Assistant",
                    timeout=5
                )
            except Exception as e:
                print(f"Erreur de notification : {e}")
    
    def closeEvent(self, event):
        """Gère la fermeture de l'application"""
        # Sauvegarder les paramètres
        self.save_settings()
        
        # Fermer proprement la base de données
        try:
            self.conn.close()
        except:
            pass
        
        # Cacher la fenêtre si l'icône système est active
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Définir une police moderne
    font = QFont()
    font.setFamily("Segoe UI" if platform.system() == "Windows" else "Helvetica Neue")
    font.setPointSize(10)
    app.setFont(font)
    
    # Style de fusion pour des widgets plus modernes
    app.setStyle("Fusion")
    
    # Créer et afficher la fenêtre principale
    window = MarketingAIAnalyzer()
    window.show()
    
    sys.exit(app.exec_())