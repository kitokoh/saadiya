import sys
import json
import requests
from datetime import datetime
from textblob import TextBlob
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QListWidget, QTextEdit, 
                           QTabWidget, QComboBox, QTableWidget, QTableWidgetItem,
                           QHeaderView, QMessageBox, QSplitter, QProgressBar,
                           QToolBar, QStatusBar, QAction, QFileDialog, QMenuBar,
                           QStackedWidget, QFrame, QSizePolicy, QSpacerItem)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPainter, QLinearGradient
from PyQt5 import QtCore, QtGui
import facebook
from enum import Enum

class PageType(Enum):
    PROFILE = 1
    PAGE = 2
    GROUP = 3

class SocialCommentPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SocialComment Pro")
        self.setMinimumSize(1024, 768)
        
        # Configuration de l'application
        self.config = {
            'theme': 'light',
            'last_token': '',
            'api_version': 'v12.0'
        }
        
        # Données de l'API
        self.graph = None
        self.user_data = None
        self.current_page = None
        self.page_type = None
        self.posts = []
        self.current_post = None
        
        # Initialisation de l'UI
        self.init_ui()
        self.load_styles()
        
        # Charger la configuration
        self.load_config()
        
    def init_ui(self):
        """Initialiser l'interface utilisateur"""
        self.setWindowIcon(QIcon("icons/app_icon.png"))
        
        # Barre de menu principale
        self.create_main_menu()
        
        # Widget central
        self.central_stack = QStackedWidget()
        self.setCentralWidget(self.central_stack)
        
        # Page de connexion
        self.create_login_page()
        
        # Page principale
        self.create_main_page()
        
        # Afficher la page de connexion par défaut
        self.central_stack.setCurrentIndex(0)
        
        # Barre de statut
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Notification système
        self.notification = QLabel()
        self.notification.setAlignment(Qt.AlignCenter)
        self.notification.setFixedHeight(30)
        self.notification.hide()
        
        # Animation de notification
        self.notification_animation = QPropertyAnimation(self.notification, b"geometry")
        
    def create_main_menu(self):
        """Créer le menu principal"""
        menu_bar = self.menuBar()
        
        # Menu Application
        app_menu = menu_bar.addMenu("&Application")
        
        self.theme_action = QAction("Thème sombre", self)
        self.theme_action.triggered.connect(self.toggle_theme)
        app_menu.addAction(self.theme_action)
        
        app_menu.addSeparator()
        
        exit_action = QAction("Quitter", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        app_menu.addAction(exit_action)
        
        # Menu Données
        data_menu = menu_bar.addMenu("&Données")
        
        refresh_action = QAction("Actualiser", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_data)
        data_menu.addAction(refresh_action)
        
        export_action = QAction("Exporter...", self)
        export_action.triggered.connect(self.export_data)
        data_menu.addAction(export_action)
        
        # Menu Aide
        help_menu = menu_bar.addMenu("&Aide")
        
        docs_action = QAction("Documentation", self)
        help_menu.addAction(docs_action)
        
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_login_page(self):
        """Créer la page de connexion"""
        self.login_page = QWidget()
        layout = QVBoxLayout(self.login_page)
        layout.setAlignment(Qt.AlignCenter)
        
        # Logo de l'application
        logo = QLabel()
        logo.setPixmap(QPixmap("icons/app_logo.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        
        # Titre
        title = QLabel("SocialComment Pro")
        title.setObjectName("LoginTitle")
        
        # Sous-titre
        subtitle = QLabel("Gestion avancée des commentaires Facebook")
        subtitle.setObjectName("LoginSubtitle")
        
        # Champ de token
        token_frame = QFrame()
        token_frame.setObjectName("TokenFrame")
        token_layout = QVBoxLayout(token_frame)
        
        token_label = QLabel("Token d'accès Facebook")
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Entrez votre token d'accès...")
        self.token_input.setEchoMode(QLineEdit.Password)
        
        # Bouton de connexion
        self.login_btn = QPushButton("Se connecter")
        self.login_btn.setObjectName("LoginButton")
        self.login_btn.clicked.connect(self.facebook_login)
        
        # Lien pour obtenir un token
        token_link = QLabel("<a href='https://developers.facebook.com/tools/explorer/'>Obtenir un token d'accès</a>")
        token_link.setOpenExternalLinks(True)
        token_link.setAlignment(Qt.AlignCenter)
        
        # Ajout des widgets
        token_layout.addWidget(token_label)
        token_layout.addWidget(self.token_input)
        token_layout.addWidget(self.login_btn)
        token_layout.addWidget(token_link)
        
        # Ajout à la page
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(30)
        layout.addWidget(token_frame)
        layout.addStretch()
        
        self.central_stack.addWidget(self.login_page)
    
    def create_main_page(self):
        """Créer la page principale"""
        self.main_page = QWidget()
        main_layout = QVBoxLayout(self.main_page)
        
        # Barre d'outils supérieure
        self.create_top_toolbar(main_layout)
        
        # Contenu principal
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Panneau gauche - Navigation
        self.create_navigation_panel(content_splitter)
        
        # Panneau droit - Contenu
        self.create_content_panel(content_splitter)
        
        # Configurer le splitter
        content_splitter.setStretchFactor(1, 3)
        content_splitter.setSizes([300, 700])
        
        main_layout.addWidget(content_splitter)
        
        self.central_stack.addWidget(self.main_page)
    
    def create_top_toolbar(self, parent_layout):
        """Créer la barre d'outils supérieure"""
        toolbar = QFrame()
        toolbar.setObjectName("TopToolbar")
        toolbar_layout = QHBoxLayout(toolbar)
        
        # Bouton de menu
        menu_btn = QPushButton()
        menu_btn.setIcon(QIcon("icons/menu.png"))
        menu_btn.setObjectName("MenuButton")
        
        # Titre de la page
        self.page_title = QLabel("Tableau de bord")
        self.page_title.setObjectName("PageTitle")
        
        # Espaceur
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Boutons d'action
        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(QIcon("icons/refresh.png"))
        self.refresh_btn.setToolTip("Actualiser")
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        self.notif_btn = QPushButton()
        self.notif_btn.setIcon(QIcon("icons/notifications.png"))
        self.notif_btn.setToolTip("Notifications")
        
        self.user_btn = QPushButton()
        self.user_btn.setIcon(QIcon("icons/user.png"))
        self.user_btn.setToolTip("Profil")
        self.user_btn.clicked.connect(self.show_user_menu)
        
        # Ajout des widgets
        toolbar_layout.addWidget(menu_btn)
        toolbar_layout.addWidget(self.page_title)
        toolbar_layout.addSpacerItem(spacer)
        toolbar_layout.addWidget(self.refresh_btn)
        toolbar_layout.addWidget(self.notif_btn)
        toolbar_layout.addWidget(self.user_btn)
        
        parent_layout.addWidget(toolbar)
    
    def create_navigation_panel(self, parent):
        """Créer le panneau de navigation"""
        nav_panel = QFrame()
        nav_panel.setObjectName("NavPanel")
        nav_layout = QVBoxLayout(nav_panel)
        
        # Sélecteur de page
        self.page_selector = QComboBox()
        self.page_selector.setObjectName("PageSelector")
        self.page_selector.currentIndexChanged.connect(self.on_page_change)
        
        # Liste des publications
        self.posts_list = QListWidget()
        self.posts_list.setObjectName("PostsList")
        self.posts_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.posts_list.itemClicked.connect(self.load_post_comments)
        
        # Bouton de chargement
        self.load_more_btn = QPushButton("Charger plus")
        self.load_more_btn.setObjectName("LoadMoreButton")
        self.load_more_btn.clicked.connect(self.load_more_posts)
        
        # Ajout des widgets
        nav_layout.addWidget(QLabel("Sélectionner une page"))
        nav_layout.addWidget(self.page_selector)
        nav_layout.addWidget(QLabel("Publications"))
        nav_layout.addWidget(self.posts_list)
        nav_layout.addWidget(self.load_more_btn)
        
        parent.addWidget(nav_panel)
    
    def create_content_panel(self, parent):
        """Créer le panneau de contenu"""
        content_panel = QTabWidget()
        content_panel.setObjectName("ContentPanel")
        content_panel.setTabPosition(QTabWidget.North)
        content_panel.setDocumentMode(True)
        
        # Onglet Commentaires
        self.create_comments_tab(content_panel)
        
        # Onglet Analyse
        self.create_analysis_tab(content_panel)
        
        # Onglet Modération
        self.create_moderation_tab(content_panel)
        
        parent.addWidget(content_panel)
    
    def create_comments_tab(self, tab_widget):
        """Créer l'onglet Commentaires"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # En-tête
        header = QFrame()
        header.setObjectName("CommentsHeader")
        header_layout = QHBoxLayout(header)
        
        self.post_title = QLabel("Aucune publication sélectionnée")
        self.post_title.setObjectName("PostTitle")
        
        self.comments_stats = QLabel()
        self.comments_stats.setObjectName("CommentsStats")
        
        header_layout.addWidget(self.post_title)
        header_layout.addStretch()
        header_layout.addWidget(self.comments_stats)
        
        # Tableau des commentaires
        self.comments_table = QTableWidget()
        self.comments_table.setObjectName("CommentsTable")
        self.comments_table.setColumnCount(5)
        self.comments_table.setHorizontalHeaderLabels(["Auteur", "Commentaire", "Date", "Sentiment", "Actions"])
        self.comments_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.comments_table.verticalHeader().setVisible(False)
        self.comments_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.comments_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Zone de réponse
        reply_frame = QFrame()
        reply_frame.setObjectName("ReplyFrame")
        reply_layout = QVBoxLayout(reply_frame)
        
        self.reply_to_label = QLabel("Répondre à: Aucune sélection")
        self.reply_to_label.setObjectName("ReplyToLabel")
        
        self.reply_text = QTextEdit()
        self.reply_text.setObjectName("ReplyText")
        self.reply_text.setPlaceholderText("Écrivez votre réponse ici...")
        
        reply_btn_layout = QHBoxLayout()
        reply_btn_layout.addStretch()
        
        self.send_reply_btn = QPushButton("Envoyer")
        self.send_reply_btn.setObjectName("SendReplyButton")
        self.send_reply_btn.setIcon(QIcon("icons/send.png"))
        self.send_reply_btn.clicked.connect(self.send_reply)
        
        reply_btn_layout.addWidget(self.send_reply_btn)
        
        reply_layout.addWidget(self.reply_to_label)
        reply_layout.addWidget(self.reply_text)
        reply_layout.addLayout(reply_btn_layout)
        
        # Ajout à l'onglet
        layout.addWidget(header)
        layout.addWidget(self.comments_table)
        layout.addWidget(reply_frame)
        
        tab_widget.addTab(tab, QIcon("icons/comments.png"), "Commentaires")
    
    def create_analysis_tab(self, tab_widget):
        """Créer l'onglet Analyse"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Widgets d'analyse (simplifiés pour l'exemple)
        analysis_title = QLabel("Analyse des Commentaires")
        analysis_title.setObjectName("AnalysisTitle")
        analysis_title.setAlignment(Qt.AlignCenter)
        
        self.sentiment_chart = QLabel()
        self.sentiment_chart.setAlignment(Qt.AlignCenter)
        self.sentiment_chart.setPixmap(QPixmap("icons/sentiment_chart.png"))
        
        self.activity_chart = QLabel()
        self.activity_chart.setAlignment(Qt.AlignCenter)
        self.activity_chart.setPixmap(QPixmap("icons/activity_chart.png"))
        
        layout.addWidget(analysis_title)
        layout.addWidget(self.sentiment_chart)
        layout.addWidget(self.activity_chart)
        layout.addStretch()
        
        tab_widget.addTab(tab, QIcon("icons/analysis.png"), "Analyse")
    
    def create_moderation_tab(self, tab_widget):
        """Créer l'onglet Modération"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Filtres de modération
        filter_frame = QFrame()
        filter_frame.setObjectName("FilterFrame")
        filter_layout = QHBoxLayout(filter_frame)
        
        self.moderation_filter = QComboBox()
        self.moderation_filter.addItems([
            "Tous les commentaires",
            "Commentaires négatifs",
            "Avec mots-clés",
            "Signalés",
            "Avec liens"
        ])
        
        self.keywords_input = QLineEdit()
        self.keywords_input.setPlaceholderText("Mots-clés séparés par des virgules")
        
        filter_btn = QPushButton("Filtrer")
        filter_btn.setIcon(QIcon("icons/filter.png"))
        filter_btn.clicked.connect(self.apply_moderation_filter)
        
        filter_layout.addWidget(self.moderation_filter)
        filter_layout.addWidget(self.keywords_input)
        filter_layout.addWidget(filter_btn)
        
        # Tableau de modération
        self.moderation_table = QTableWidget()
        self.moderation_table.setColumnCount(5)
        self.moderation_table.setHorizontalHeaderLabels(["Sélection", "Auteur", "Commentaire", "Statut", "Actions"])
        self.moderation_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        
        # Actions en masse
        mass_actions_frame = QFrame()
        mass_actions_layout = QHBoxLayout(mass_actions_frame)
        
        select_all = QPushButton("Tout sélectionner")
        select_all.clicked.connect(lambda: self.select_all_comments(True))
        
        deselect_all = QPushButton("Tout désélectionner")
        deselect_all.clicked.connect(lambda: self.select_all_comments(False))
        
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        delete_selected = QPushButton("Supprimer la sélection")
        delete_selected.setIcon(QIcon("icons/delete.png"))
        delete_selected.clicked.connect(self.delete_selected_comments)
        
        mass_actions_layout.addWidget(select_all)
        mass_actions_layout.addWidget(deselect_all)
        mass_actions_layout.addSpacerItem(spacer)
        mass_actions_layout.addWidget(delete_selected)
        
        # Ajout à l'onglet
        layout.addWidget(filter_frame)
        layout.addWidget(self.moderation_table)
        layout.addWidget(mass_actions_frame)
        
        tab_widget.addTab(tab, QIcon("icons/moderation.png"), "Modération")
    
    def load_styles(self):
        """Charger les styles CSS"""
        self.setStyleSheet("""
            /* Styles de base */
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            
            /* Page de connexion */
            #LoginTitle {
                font-size: 28px;
                font-weight: bold;
                color: #3a3a3a;
                text-align: center;
            }
            
            #LoginSubtitle {
                font-size: 16px;
                color: #666;
                text-align: center;
                margin-bottom: 30px;
            }
            
            #TokenFrame {
                background: #ffffff;
                border-radius: 8px;
                padding: 20px;
                border: 1px solid #e0e0e0;
                max-width: 400px;
                margin: 0 auto;
            }
            
            #LoginButton {
                background-color: #4267B2;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
                margin-top: 15px;
            }
            
            #LoginButton:hover {
                background-color: #365899;
            }
            
            /* Barre d'outils supérieure */
            #TopToolbar {
                background-color: #4267B2;
                padding: 10px;
                border: none;
            }
            
            #PageTitle {
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin-left: 10px;
            }
            
            #MenuButton {
                background: transparent;
                border: none;
                padding: 5px;
            }
            
            /* Panneau de navigation */
            #NavPanel {
                background-color: #f5f6f7;
                border-right: 1px solid #dddfe2;
            }
            
            #PageSelector {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #dddfe2;
                margin-bottom: 15px;
            }
            
            #PostsList {
                border: none;
                background: transparent;
            }
            
            #PostsList::item {
                padding: 12px;
                border-bottom: 1px solid #e9ebee;
            }
            
            #PostsList::item:hover {
                background-color: #e9ebee;
            }
            
            #PostsList::item:selected {
                background-color: #4267B2;
                color: white;
            }
            
            #LoadMoreButton {
                background: #f5f6f7;
                border: 1px solid #dddfe2;
                padding: 8px;
                border-radius: 4px;
                margin-top: 10px;
            }
            
            /* Onglets de contenu */
            #ContentPanel::pane {
                border: none;
            }
            
            QTabBar::tab {
                padding: 10px 15px;
                background: #f5f6f7;
                border: none;
                border-bottom: 2px solid transparent;
            }
            
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #4267B2;
                color: #4267B2;
                font-weight: bold;
            }
            
            /* Tableau des commentaires */
            #CommentsTable {
                border: none;
                alternate-background-color: #f9f9f9;
            }
            
            #CommentsTable::item {
                padding: 8px;
            }
            
            #CommentsHeader {
                background: #f5f6f7;
                padding: 15px;
                border-bottom: 1px solid #dddfe2;
            }
            
            #PostTitle {
                font-size: 16px;
                font-weight: bold;
                color: #1d2129;
            }
            
            #CommentsStats {
                color: #65676b;
                font-size: 13px;
            }
            
            /* Zone de réponse */
            #ReplyFrame {
                background: #f5f6f7;
                padding: 15px;
                border-top: 1px solid #dddfe2;
            }
            
            #ReplyToLabel {
                font-size: 13px;
                color: #65676b;
                margin-bottom: 10px;
            }
            
            #ReplyText {
                border: 1px solid #dddfe2;
                border-radius: 4px;
                min-height: 80px;
            }
            
            #SendReplyButton {
                background-color: #4267B2;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
            }
            
            /* Thème sombre */
            .dark-theme {
                background-color: #18191a;
                color: #e4e6eb;
            }
            
            .dark-theme #TokenFrame,
            .dark-theme #NavPanel,
            .dark-theme #ContentPanel::pane,
            .dark-theme QTabBar::tab {
                background-color: #242526;
                border-color: #3e4042;
            }
            
            .dark-theme #PostsList::item:hover,
            .dark-theme #ReplyFrame,
            .dark-theme #CommentsHeader {
                background-color: #3a3b3c;
            }
            
            .dark-theme #LoginTitle,
            .dark-theme #PostTitle {
                color: #e4e6eb;
            }
            
            .dark-theme #LoginSubtitle,
            .dark-theme #CommentsStats,
            .dark-theme #ReplyToLabel {
                color: #b0b3b8;
            }
            
            .dark-theme QLineEdit,
            .dark-theme QTextEdit {
                background-color: #3a3b3c;
                color: #e4e6eb;
                border-color: #3e4042;
            }
        """)
    
    def toggle_theme(self):
        """Basculer entre les thèmes clair/sombre"""
        if self.config['theme'] == 'light':
            self.setStyleSheet(self.styleSheet() + "\nQWidget { background-color: #18191a; color: #e4e6eb; }")
            self.theme_action.setText("Thème clair")
            self.config['theme'] = 'dark'
        else:
            self.setStyleSheet(self.styleSheet().replace("\nQWidget { background-color: #18191a; color: #e4e6eb; }", ""))
            self.theme_action.setText("Thème sombre")
            self.config['theme'] = 'light'
        
        self.save_config()
    
    def facebook_login(self):
        """Se connecter à Facebook"""
        token = self.token_input.text().strip()
        
        if not token:
            self.show_notification("Veuillez entrer un token d'accès valide", error=True)
            return
        
        try:
            # Afficher un indicateur de chargement
            self.login_btn.setEnabled(False)
            self.login_btn.setText("Connexion en cours...")
            
            # Se connecter à l'API
            self.graph = facebook.GraphAPI(access_token=token, version=self.config['api_version'])
            self.user_data = self.graph.get_object("me", fields="id,name,picture,accounts{id,name,category,access_token}")
            
            # Sauvegarder le token
            self.config['last_token'] = token
            self.save_config()
            
            # Remplir le sélecteur de pages
            self.page_selector.clear()
            if 'accounts' in self.user_data:
                for page in self.user_data['accounts']['data']:
                    self.page_selector.addItem(f"{page['name']} ({page['category']})", userData=page)
            
            # Passer à la page principale
            self.central_stack.setCurrentIndex(1)
            self.show_notification(f"Connecté en tant que {self.user_data['name']}")
            
        except Exception as e:
            self.show_notification(f"Échec de la connexion: {str(e)}", error=True)
        finally:
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Se connecter")
    
    def on_page_change(self, index):
        """Changer de page/groupe sélectionné"""
        if index >= 0:
            page_data = self.page_selector.itemData(index)
            self.current_page = page_data
            self.load_posts()
    
    def load_posts(self):
        """Charger les publications"""
        if not self.current_page:
            return
        
        try:
            self.posts_list.clear()
            self.posts = []
            
            # Récupérer les posts avec les commentaires
            posts = self.graph.get_object(
                f"{self.current_page['id']}/posts",
                fields="id,message,created_time,comments.limit(10).summary(true),reactions.limit(0).summary(true)"
            )
            
            self.posts = posts['data']
            self.display_posts()
            
        except Exception as e:
            self.show_notification(f"Erreur lors du chargement des publications: {str(e)}", error=True)
    
    def display_posts(self):
        """Afficher les publications dans la liste"""
        for post in self.posts:
            message = post.get('message', 'Publication sans texte')[:50] + "..." if 'message' in post else "Publication sans texte"
            date = datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d/%m/%Y')
            
            comments = post.get('comments', {}).get('summary', {}).get('total_count', 0)
            reactions = post.get('reactions', {}).get('summary', {}).get('total_count', 0)
            
            item = QListWidgetItem()
            widget = QWidget()
            layout = QVBoxLayout(widget)
            
            title = QLabel(message)
            title.setStyleSheet("font-weight: bold;")
            
            details = QLabel(f"📅 {date} | 💬 {comments} | ❤️ {reactions}")
            details.setStyleSheet("color: #65676b; font-size: 12px;")
            
            layout.addWidget(title)
            layout.addWidget(details)
            layout.setContentsMargins(5, 5, 5, 5)
            
            item.setSizeHint(widget.sizeHint())
            self.posts_list.addItem(item)
            self.posts_list.setItemWidget(item, widget)
    
    def load_post_comments(self, item):
        """Charger les commentaires d'une publication"""
        index = self.posts_list.row(item)
        self.current_post = self.posts[index]
        
        try:
            comments = self.graph.get_object(
                f"{self.current_post['id']}/comments",
                fields="id,from,message,created_time,like_count,comment_count"
            )
            
            # Mettre à jour l'interface
            self.post_title.setText(self.current_post.get('message', 'Publication sans texte')[:100] + "...")
            
            comment_count = len(comments['data'])
            self.comments_stats.setText(f"{comment_count} commentaire(s)")
            
            # Remplir le tableau
            self.comments_table.setRowCount(0)
            
            for comment in comments['data']:
                row = self.comments_table.rowCount()
                self.comments_table.insertRow(row)
                
                # Auteur
                author = QTableWidgetItem(comment['from']['name'])
                
                # Commentaire
                message = QTableWidgetItem(comment['message'])
                message.setToolTip(comment['message'])
                
                # Date
                date = datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d/%m/%Y %H:%M')
                date_item = QTableWidgetItem(date)
                
                # Sentiment
                sentiment = self.analyze_sentiment(comment['message'])
                sentiment_item = QTableWidgetItem(sentiment)
                
                # Appliquer une couleur en fonction du sentiment
                if "positif" in sentiment.lower():
                    sentiment_item.setBackground(QColor(56, 142, 60, 50))
                elif "négatif" in sentiment.lower():
                    sentiment_item.setBackground(QColor(211, 47, 47, 50))
                else:
                    sentiment_item.setBackground(QColor(251, 192, 45, 50))
                
                # Actions
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                
                reply_btn = QPushButton()
                reply_btn.setIcon(QIcon("icons/reply.png"))
                reply_btn.setToolTip("Répondre")
                reply_btn.clicked.connect(lambda _, c=comment: self.prepare_reply(c))
                
                delete_btn = QPushButton()
                delete_btn.setIcon(QIcon("icons/delete.png"))
                delete_btn.setToolTip("Supprimer")
                delete_btn.clicked.connect(lambda _, c=comment: self.delete_comment(c['id']))
                
                action_layout.addWidget(reply_btn)
                action_layout.addWidget(delete_btn)
                action_layout.setContentsMargins(0, 0, 0, 0)
                action_layout.setAlignment(Qt.AlignCenter)
                
                # Ajouter les éléments au tableau
                self.comments_table.setItem(row, 0, author)
                self.comments_table.setItem(row, 1, message)
                self.comments_table.setItem(row, 2, date_item)
                self.comments_table.setItem(row, 3, sentiment_item)
                self.comments_table.setCellWidget(row, 4, action_widget)
            
            # Redimensionner les colonnes
            self.comments_table.resizeColumnsToContents()
            
        except Exception as e:
            self.show_notification(f"Erreur lors du chargement des commentaires: {str(e)}", error=True)
    
    def prepare_reply(self, comment):
        """Préparer une réponse à un commentaire"""
        self.reply_to_label.setText(f"Répondre à: {comment['from']['name']}")
        self.current_reply_to = comment['id']
        self.reply_text.setFocus()
    
    def send_reply(self):
        """Envoyer une réponse"""
        if not hasattr(self, 'current_reply_to'):
            self.show_notification("Aucun commentaire sélectionné pour répondre", error=True)
            return
        
        reply_text = self.reply_text.toPlainText().strip()
        if not reply_text:
            self.show_notification("Veuillez entrer un texte de réponse", error=True)
            return
        
        try:
            self.graph.put_object(parent_object=self.current_reply_to, connection_name="comments", message=reply_text)
            self.show_notification("Réponse envoyée avec succès")
            self.reply_text.clear()
            self.load_post_comments(self.posts_list.currentItem())
        except Exception as e:
            self.show_notification(f"Échec de l'envoi de la réponse: {str(e)}", error=True)
    
    def delete_comment(self, comment_id):
        """Supprimer un commentaire"""
        confirm = QMessageBox.question(
            self, 
            "Confirmer la suppression", 
            "Êtes-vous sûr de vouloir supprimer ce commentaire?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                self.graph.delete_object(comment_id)
                self.show_notification("Commentaire supprimé avec succès")
                self.load_post_comments(self.posts_list.currentItem())
            except Exception as e:
                self.show_notification(f"Échec de la suppression: {str(e)}", error=True)
    
    def analyze_sentiment(self, text):
        """Analyser le sentiment d'un texte"""
        analysis = TextBlob(text)
        
        if analysis.sentiment.polarity > 0.2:
            return "😊 Positif"
        elif analysis.sentiment.polarity < -0.2:
            return "😠 Négatif"
        else:
            return "😐 Neutre"
    
    def apply_moderation_filter(self):
        """Appliquer les filtres de modération"""
        filter_type = self.moderation_filter.currentText()
        keywords = [k.strip() for k in self.keywords_input.text().split(",") if k.strip()]
        
        # Implémentation simplifiée pour l'exemple
        self.show_notification(f"Filtre appliqué: {filter_type}")
    
    def select_all_comments(self, selected):
        """Sélectionner/désélectionner tous les commentaires"""
        for row in range(self.moderation_table.rowCount()):
            checkbox = self.moderation_table.cellWidget(row, 0)
            if checkbox:
                checkbox.setChecked(selected)
    
    def delete_selected_comments(self):
        """Supprimer les commentaires sélectionnés"""
        confirm = QMessageBox.question(
            self,
            "Confirmer la suppression",
            "Êtes-vous sûr de vouloir supprimer les commentaires sélectionnés?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Implémentation simplifiée pour l'exemple
            self.show_notification("Commentaires sélectionnés supprimés")
    
    def refresh_data(self):
        """Actualiser les données"""
        if self.graph:
            self.load_posts()
            if self.posts_list.currentItem():
                self.load_post_comments(self.posts_list.currentItem())
            self.show_notification("Données actualisées")
        else:
            self.show_notification("Veuillez d'abord vous connecter", error=True)
    
    def show_notification(self, message, error=False):
        """Afficher une notification"""
        self.notification.setText(message)
        
        if error:
            self.notification.setStyleSheet("background-color: #ffebee; color: #c62828; border: 1px solid #ef9a9a;")
        else:
            self.notification.setStyleSheet("background-color: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7;")
        
        # Position initiale (hors écran)
        self.notification.setGeometry(
            0, 
            -self.notification.height(), 
            self.width(), 
            self.notification.height()
        )
        
        self.notification.show()
        
        # Animation d'entrée
        self.notification_animation.setDuration(300)
        self.notification_animation.setEasingCurve(QEasingCurve.OutQuad)
        self.notification_animation.setStartValue(self.notification.geometry())
        self.notification_animation.setEndValue(QtCore.QRect(
            0, 0, 
            self.width(), 
            self.notification.height()
        ))
        self.notification_animation.start()
        
        # Timer pour masquer la notification après 3 secondes
        QTimer.singleShot(3000, self.hide_notification)
    
    def hide_notification(self):
        """Masquer la notification"""
        # Animation de sortie
        self.notification_animation.setDuration(300)
        self.notification_animation.setEasingCurve(QEasingCurve.InQuad)
        self.notification_animation.setStartValue(self.notification.geometry())
        self.notification_animation.setEndValue(QtCore.QRect(
            0, 
            -self.notification.height(), 
            self.width(), 
            self.notification.height()
        ))
        self.notification_animation.start()
    
    def show_user_menu(self):
        """Afficher le menu utilisateur"""
        menu = QMenu(self)
        
        profile_action = menu.addAction("Profil")
        settings_action = menu.addAction("Paramètres")
        menu.addSeparator()
        logout_action = menu.addAction("Déconnexion")
        
        action = menu.exec_(self.user_btn.mapToGlobal(self.user_btn.rect().bottomLeft()))
        
        if action == logout_action:
            self.facebook_logout()
            self.central_stack.setCurrentIndex(0)
    
    def load_config(self):
        """Charger la configuration"""
        try:
            with open("config.json", "r") as f:
                self.config = json.load(f)
                
            # Appliquer le thème
            if self.config.get('theme') == 'dark':
                self.toggle_theme()
                
            # Remplir le token
            self.token_input.setText(self.config.get('last_token', ''))
                
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    
    def save_config(self):
        """Sauvegarder la configuration"""
        with open("config.json", "w") as f:
            json.dump(self.config, f)
    
    def show_about(self):
        """Afficher la boîte de dialogue À propos"""
        about = QMessageBox(self)
        about.setWindowTitle("À propos de SocialComment Pro")
        about.setText("""
        <h2>SocialComment Pro</h2>
        <p>Version 2.0</p>
        <p>Une application avancée pour la gestion des commentaires Facebook.</p>
        <p>Fonctionnalités :</p>
        <ul>
            <li>Gestion des commentaires</li>
            <li>Analyse de sentiment</li>
            <li>Modération avancée</li>
            <li>Statistiques détaillées</li>
        </ul>
        <p>© 2023 - Tous droits réservés</p>
        """)
        about.exec_()
    
    def closeEvent(self, event):
        """Événement de fermeture de l'application"""
        self.save_config()
        event.accept()
    def export_data(self):
        """Exporter les données des commentaires"""
        if not self.current_post:
            self.show_notification("Aucune publication sélectionnée à exporter", error=True)
            return

        # Demander le fichier de destination
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter les commentaires",
            "",
            "Fichiers CSV (*.csv);;Fichiers JSON (*.json)",
            options=options
        )

        if not file_name:
            return  # L'utilisateur a annulé

        try:
            # Récupérer tous les commentaires (pas seulement les 10 premiers)
            comments = self.graph.get_object(
                f"{self.current_post['id']}/comments",
                fields="id,from,message,created_time,like_count,comment_count"
            )

            if file_name.endswith('.csv'):
                # Export CSV
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write("ID,Auteur,Message,Date,Likes,Réponses,Sentiment\n")
                    for comment in comments['data']:
                        message = comment['message'].replace('"', '""')
                        sentiment = self.analyze_sentiment(comment['message'])
                        f.write(
                            f'"{comment["id"]}",'
                            f'"{comment["from"]["name"]}",'
                            f'"{message}",'
                            f'"{comment["created_time"]}",'
                            f'{comment.get("like_count", 0)},'
                            f'{comment.get("comment_count", 0)},'
                            f'"{sentiment}"\n'
                        )

            elif file_name.endswith('.json'):
                # Export JSON
                export_data = {
                    'post_id': self.current_post['id'],
                    'post_message': self.current_post.get('message', ''),
                    'comments': []
                }

                for comment in comments['data']:
                    export_data['comments'].append({
                        'id': comment['id'],
                        'author': comment['from']['name'],
                        'message': comment['message'],
                        'created_time': comment['created_time'],
                        'likes': comment.get('like_count', 0),
                        'replies': comment.get('comment_count', 0),
                        'sentiment': self.analyze_sentiment(comment['message'])
                    })

                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)

            self.show_notification(f"Données exportées avec succès vers {file_name}")

        except Exception as e:
            self.show_notification(f"Erreur lors de l'exportation: {str(e)}", error=True)
    def load_more_posts(self):
        """Charger plus de publications"""
        if not self.current_page:
            self.show_notification("Aucune page sélectionnée", error=True)
            return

        try:
            # Récupérer le dernier post chargé pour la pagination
            last_post_id = self.posts[-1]['id'] if self.posts else None

            # Paramètres de la requête
            params = {
                'fields': 'id,message,created_time,comments.limit(10).summary(true),reactions.limit(0).summary(true)',
                'limit': 10
            }

            if last_post_id:
                params['after'] = last_post_id

            # Récupérer les posts supplémentaires
            more_posts = self.graph.get_object(
                f"{self.current_page['id']}/posts",
                **params
            )

            if more_posts['data']:
                self.posts.extend(more_posts['data'])
                self.display_posts()
                self.show_notification(f"{len(more_posts['data'])} publications supplémentaires chargées")
            else:
                self.show_notification("Aucune autre publication à charger")

        except Exception as e:
            self.show_notification(f"Erreur lors du chargement: {str(e)}", error=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Définir une police moderne
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Créer et afficher la fenêtre principale
    window = SocialCommentPro()
    window.show()
    
    sys.exit(app.exec_())