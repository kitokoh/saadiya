import sys
import os
import logging
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QTextEdit, QPushButton, QLabel, QLineEdit, 
                             QSplitter, QComboBox, QMessageBox, QInputDialog, QFrame,
                             QFileDialog, QTabWidget, QCheckBox, QMenu, QAction)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QColor, QTextCharFormat, QTextCursor
import sqlite3
from datetime import datetime
import markdown
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import QStringListModel
from imports import DB_PATH_prompts
class PromptManager1(QMainWindow):
    def __init__(self,main_app=None):
        """Initialisation de l'application principale"""
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("Prompt Genius")
        self.setGeometry(100, 100, 1400, 900)
        self.setWindowIcon(QIcon("prompt_icon.png"))

        # Configuration du style
        self.setup_styles()

        # Initialisation de la base de données
        self.init_db()

        # Variables d'état
        self.current_prompt_id = None
        self.search_delay_timer = QTimer()
        self.search_delay_timer.setSingleShot(True)
        self.search_delay_timer.timeout.connect(self.load_prompts)

        # Création de l'interface
        self.create_ui()

        # Charger les données initiales
        self.load_categories()
        self.load_tags()
        self.load_prompts()

        # Configurer les raccourcis clavier
        self.setup_shortcuts()

        # Configurer l'icône de la barre système
        self.setup_tray_icon()

        # Configurer la sauvegarde automatique
        self.setup_auto_backup()

        # Configurer l'auto-complétion pour la recherche
        self.setup_auto_complete()

        # Créer le menu
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()

        # Menu Fichier
        file_menu = menu_bar.addMenu("Fichier")

        import_action = QAction("Importer un prompt", self)
        import_action.triggered.connect(self.import_prompt)
        file_menu.addAction(import_action)

        export_action = QAction("Exporter le prompt sélectionné", self)
        export_action.triggered.connect(self.export_prompt)
        file_menu.addAction(export_action)

        backup_action = QAction("Sauvegarder la base de données", self)
        backup_action.triggered.connect(self.backup_database)
        file_menu.addAction(backup_action)

        restore_action = QAction("Restaurer la base de données", self)
        restore_action.triggered.connect(self.restore_database)
        file_menu.addAction(restore_action)

        file_menu.addSeparator()

        exit_action = QAction("Quitter", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menu Édition
        edit_menu = menu_bar.addMenu("Édition")

        new_prompt_action = QAction("Nouveau prompt", self)
        new_prompt_action.triggered.connect(self.add_new_prompt)
        edit_menu.addAction(new_prompt_action)

        edit_prompt_action = QAction("Modifier le prompt", self)
        edit_prompt_action.triggered.connect(self.edit_prompt)
        edit_menu.addAction(edit_prompt_action)

        duplicate_action = QAction("Dupliquer le prompt", self)
        duplicate_action.triggered.connect(self.duplicate_prompt)
        edit_menu.addAction(duplicate_action)

        edit_menu.addSeparator()

        new_category_action = QAction("Nouvelle catégorie", self)
        new_category_action.triggered.connect(self.add_new_category)
        edit_menu.addAction(new_category_action)

        manage_tags_action = QAction("Gérer les tags", self)
        manage_tags_action.triggered.connect(self.show_tag_manager)
        edit_menu.addAction(manage_tags_action)

        # Menu Aide
        help_menu = menu_bar.addMenu("Aide")

        markdown_help_action = QAction("Aide Markdown", self)
        markdown_help_action.triggered.connect(self.show_markdown_help)
        help_menu.addAction(markdown_help_action)

        stats_action = QAction("Statistiques", self)
        stats_action.triggered.connect(self.show_stats)
        help_menu.addAction(stats_action)

        sync_action = QAction("Synchroniser", self)
        sync_action.triggered.connect(self.show_sync_dialog)
        help_menu.addAction(sync_action)

        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_markdown_help(self):
        """Afficher l'aide sur le markdown"""
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Aide Markdown")
        help_dialog.setMinimumSize(500, 400)

        layout = QVBoxLayout(help_dialog)

        markdown_help = """
        <style>
            body {{ font-family: Arial, sans-serif; color: white; }}
            h2 {{ color: #10a37f; }}
            table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
            th, td {{ border: 1px solid #565869; padding: 8px; text-align: left; }}
            th {{ background-color: #40414f; }}
            code {{ background-color: #40414f; padding: 2px 4px; border-radius: 3px; }}
        </style>
        <body>
            <h2>Syntaxe Markdown</h2>
            <p>Vous pouvez utiliser la syntaxe Markdown pour formater vos prompts et exemples.</p>

            <table>
                <tr><th>Style</th><th>Syntaxe</th><th>Résultat</th></tr>
                <tr>
                    <td>Gras</td>
                    <td><code>**texte**</code> ou <code>__texte__</code></td>
                    <td><strong>texte</strong></td>
                </tr>
                <tr>
                    <td>Italique</td>
                    <td><code>*texte*</code> ou <code>_texte_</code></td>
                    <td><em>texte</em></td>
                </tr>
                <tr>
                    <td>Titre</td>
                    <td><code># Titre 1</code><br><code>## Titre 2</code></td>
                    <td><h1 style="font-size: 1.5em; margin: 0;">Titre 1</h1><h2 style="font-size: 1.2em; margin: 0;">Titre 2</h2></td>
                </tr>
                <tr>
                    <td>Liste</td>
                    <td><code>- Item 1</code><br><code>- Item 2</code></td>
                    <td><ul><li>Item 1</li><li>Item 2</li></ul></td>
                </tr>
                <tr>
                    <td>Code</td>
                    <td><code>`code inline`</code><br><code>```bloc de code```</code></td>
                    <td><code>code inline</code><br><pre style="background-color: #40414f; padding: 10px;">bloc de code</pre></td>
                </tr>
                <tr>
                    <td>Lien</td>
                    <td><code>[texte](url)</code></td>
                    <td><a href="#">texte</a></td>
                </tr>
            </table>
        </body>
        """

        help_view = QTextEdit()
        help_view.setReadOnly(True)
        help_view.setHtml(markdown_help)
        layout.addWidget(help_view)

        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(help_dialog.accept)
        layout.addWidget(close_btn)

        help_dialog.exec_()

    # ... (autres méthodes inchangées)



    def __inits__(self):
        super().__init__()
        self.setWindowTitle("Prompt Genius")
        self.setGeometry(100, 100, 1400, 900)
        self.setWindowIcon(QIcon("prompt_icon.png"))
        
        # Configuration du style
        self.setup_styles()
        
        # Initialisation de la base de données
        self.init_db()
        
        # Variables d'état
        self.current_prompt_id = None
        self.search_delay_timer = QTimer()
        self.search_delay_timer.setSingleShot(True)
        self.search_delay_timer.timeout.connect(self.load_prompts)
        
        # Création de l'interface
        self.create_ui()
        
        # Charger les données initiales
        self.load_categories()
        self.load_tags()
        self.load_prompts()
        
    def setup_styles(self):
        self.style_sheet = '''
            /* Fenêtre principale */
            QMainWindow {
                background-color: #343541;
            }
            
            /* Boutons principaux */
            QPushButton {
                background-color: #40414f;
                color: white;
                border: 1px solid #565869;
                padding: 8px 15px;
                border-radius: 5px;
                min-width: 80px;
            }
            
            QPushButton:hover {
                background-color: #565869;
            }
            
            QPushButton:pressed {
                background-color: #40414f;
            }
            
            /* Boutons d'action */
            QPushButton.action-primary {
                background-color: #10a37f;
                border: 1px solid #0d8a6a;
            }
            
            QPushButton.action-primary:hover {
                background-color: #1a7f64;
            }
            
            QPushButton.action-danger {
                background-color: #ef4146;
                border: 1px solid #d9393e;
            }
            
            QPushButton.action-danger:hover {
                background-color: #c13539;
            }
            
            QPushButton.action-secondary {
                background-color: #565869;
                border: 1px solid #40414f;
            }
            
            /* Champs de texte */
            QLineEdit, QTextEdit, QComboBox {
                background-color: #40414f;
                color: white;
                border: 1px solid #565869;
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #10a37f;
            }
            
            QTextEdit {
                padding: 12px;
            }
            
            /* Listes */
            QListWidget {
                background-color: #202123;
                color: white;
                border: none;
                outline: 0;
            }
            
            QListWidget::item {
                padding: 12px 15px;
                border-bottom: 1px solid #343541;
            }
            
            QListWidget::item:hover {
                background-color: #343541;
            }
            
            QListWidget::item:selected {
                background-color: #40414f;
            }
            
            /* Séparateurs */
            QFrame[frameShape="4"] { /* HLine */
                background-color: #565869;
                border: none;
                height: 1px;
            }
            
            /* Onglets */
            QTabWidget::pane {
                border: none;
            }
            
            QTabBar::tab {
                background-color: #343541;
                color: #acacbe;
                padding: 8px 15px;
                border: none;
                border-bottom: 2px solid transparent;
            }
            
            QTabBar::tab:selected {
                color: white;
                border-bottom: 2px solid #10a37f;
            }
            
            QTabBar::tab:hover {
                background-color: #40414f;
            }
            
            /* Cases à cocher */
            QCheckBox {
                color: white;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #565869;
                border-radius: 3px;
                background-color: #40414f;
            }
            
            QCheckBox::indicator:checked {
                background-color: #10a37f;
                image: url(:/qtwidgets/images/checkbox_checked.png);
            }
            
            /* Tooltip */
            QToolTip {
                background-color: #202123;
                color: white;
                border: 1px solid #565869;
                padding: 5px;
                border-radius: 3px;
            }
        '''
        self.setStyleSheet(self.style_sheet)
    
    def init_db(self):
        self.conn = sqlite3.connect(DB_PATH_prompts)
        self.cursor = self.conn.cursor()
        
        # Création des tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                example TEXT,
                category_id INTEGER,
                is_favorite BOOLEAN DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompt_tags (
                prompt_id INTEGER,
                tag_id INTEGER,
                PRIMARY KEY (prompt_id, tag_id),
                FOREIGN KEY (prompt_id) REFERENCES prompts (id),
                FOREIGN KEY (tag_id) REFERENCES tags (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompt_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_id INTEGER,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                example TEXT,
                category_id INTEGER,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (prompt_id) REFERENCES prompts (id)
            )
        ''')
        
        self.conn.commit()
    
    def create_ui(self):
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter pour diviser la fenêtre
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel gauche (liste des prompts)
        left_panel = QWidget()
        left_panel.setObjectName("leftPanel")
        left_panel.setStyleSheet("#leftPanel { background-color: #202123; }")
        left_panel_layout = QVBoxLayout(left_panel)
        left_panel_layout.setContentsMargins(10, 10, 10, 10)
        left_panel_layout.setSpacing(10)
        
        # Bouton nouveau prompt
        self.new_prompt_btn = QPushButton("+ Nouveau prompt")
        self.new_prompt_btn.setObjectName("newPromptBtn")
        self.new_prompt_btn.setStyleSheet('''
            #newPromptBtn {
                background-color: #10a37f;
                padding: 12px;
                font-weight: bold;
                text-align: center;
            }
            #newPromptBtn:hover {
                background-color: #1a7f64;
            }
        ''')
        self.new_prompt_btn.clicked.connect(self.add_new_prompt)
        left_panel_layout.addWidget(self.new_prompt_btn)
        
        # Barre de recherche
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher des prompts...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        left_panel_layout.addWidget(self.search_input)
        
        # Filtres
        filter_tabs = QTabWidget()
        filter_tabs.setDocumentMode(True)
        
        # Onglet Catégories
        category_tab = QWidget()
        category_layout = QVBoxLayout(category_tab)
        
        self.category_filter = QComboBox()
        self.category_filter.addItem("Toutes les catégories")
        self.category_filter.currentIndexChanged.connect(self.load_prompts)
        category_layout.addWidget(QLabel("Filtrer par catégorie:"))
        category_layout.addWidget(self.category_filter)
        
        self.favorites_only = QCheckBox("Favoris seulement")
        self.favorites_only.stateChanged.connect(self.load_prompts)
        category_layout.addWidget(self.favorites_only)
        
        category_layout.addStretch()
        filter_tabs.addTab(category_tab, "Catégories")
        
        # Onglet Tags
        tags_tab = QWidget()
        tags_layout = QVBoxLayout(tags_tab)
        
        self.tags_filter = QComboBox()
        self.tags_filter.addItem("Tous les tags")
        self.tags_filter.currentIndexChanged.connect(self.load_prompts)
        tags_layout.addWidget(QLabel("Filtrer par tag:"))
        tags_layout.addWidget(self.tags_filter)
        
        tags_layout.addStretch()
        filter_tabs.addTab(tags_tab, "Tags")
        
        left_panel_layout.addWidget(filter_tabs)
        
        # Liste des prompts
        self.prompts_list = QListWidget()
        self.prompts_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.prompts_list.customContextMenuRequested.connect(self.show_prompt_context_menu)
        self.prompts_list.itemClicked.connect(self.display_prompt)
        left_panel_layout.addWidget(self.prompts_list, 1)
        
        # Panel droit (détails du prompt)
        right_panel = QWidget()
        right_panel.setObjectName("rightPanel")
        right_panel.setStyleSheet("#rightPanel { background-color: #343541; }")
        right_panel_layout = QVBoxLayout(right_panel)
        right_panel_layout.setContentsMargins(20, 20, 20, 20)
        right_panel_layout.setSpacing(15)
        
        # En-tête du prompt
        header_layout = QHBoxLayout()
        
        self.favorite_btn = QPushButton()
        self.favorite_btn.setCheckable(True)
        self.favorite_btn.setFixedSize(30, 30)
        self.favorite_btn.setToolTip("Marquer comme favori")
        self.favorite_btn.clicked.connect(self.toggle_favorite)
        header_layout.addWidget(self.favorite_btn)
        
        self.prompt_title = QLabel("Sélectionnez un prompt")
        self.prompt_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(self.prompt_title, 1)
        
        right_panel_layout.addLayout(header_layout)
        
        # Onglets de contenu
        content_tabs = QTabWidget()
        content_tabs.setDocumentMode(True)
        
        # Onglet Prompt
        prompt_tab = QWidget()
        prompt_layout = QVBoxLayout(prompt_tab)
        
        self.prompt_content = QTextEdit()
        self.prompt_content.setReadOnly(True)
        prompt_layout.addWidget(self.prompt_content, 1)
        
        content_tabs.addTab(prompt_tab, "Prompt")
        
        # Onglet Exemple
        example_tab = QWidget()
        example_layout = QVBoxLayout(example_tab)
        
        self.prompt_example = QTextEdit()
        self.prompt_example.setReadOnly(True)
        example_layout.addWidget(self.prompt_example, 1)
        
        content_tabs.addTab(example_tab, "Exemple")
        
        # Onglet Historique
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.display_history_version)
        history_layout.addWidget(self.history_list)
        
        self.restore_version_btn = QPushButton("Restaurer cette version")
        self.restore_version_btn.setObjectName("action-primary")
        self.restore_version_btn.clicked.connect(self.restore_history_version)
        history_layout.addWidget(self.restore_version_btn)
        
        content_tabs.addTab(history_tab, "Historique")
        
        right_panel_layout.addWidget(content_tabs, 1)
        
        # Tags du prompt
        self.tags_container = QWidget()
        tags_container_layout = QHBoxLayout(self.tags_container)
        tags_container_layout.setContentsMargins(0, 0, 0, 0)
        tags_container_layout.setSpacing(5)
        
        tags_label = QLabel("Tags:")
        tags_container_layout.addWidget(tags_label)
        
        self.tags_layout = QHBoxLayout()
        self.tags_layout.setSpacing(5)
        tags_container_layout.addLayout(self.tags_layout, 1)
        tags_container_layout.addStretch()
        
        self.add_tag_btn = QPushButton("+")
        self.add_tag_btn.setFixedSize(25, 25)
        self.add_tag_btn.clicked.connect(self.show_add_tag_dialog)
        tags_container_layout.addWidget(self.add_tag_btn)
        
        right_panel_layout.addWidget(self.tags_container)
        
        # Boutons d'action
        button_layout = QHBoxLayout()
        
        self.edit_btn = QPushButton("Modifier")
        self.edit_btn.setObjectName("action-primary")
        self.edit_btn.clicked.connect(self.edit_prompt)
        button_layout.addWidget(self.edit_btn)
        
        self.export_btn = QPushButton("Exporter")
        self.export_btn.setObjectName("action-secondary")
        self.export_btn.clicked.connect(self.export_prompt)
        button_layout.addWidget(self.export_btn)
        
        self.delete_btn = QPushButton("Supprimer")
        self.delete_btn.setObjectName("action-danger")
        self.delete_btn.clicked.connect(self.delete_prompt)
        button_layout.addWidget(self.delete_btn)
        
        right_panel_layout.addLayout(button_layout)
        
        # Ajouter les panels au splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter)
        
        # Mettre à jour l'état des boutons
        self.update_buttons_state()
    
    def on_search_text_changed(self):
        self.search_delay_timer.stop()
        self.search_delay_timer.start(500)  # Délai de 500ms avant la recherche
    
    def show_prompt_context_menu(self, position):
        if not self.prompts_list.itemAt(position):
            return
            
        menu = QMenu()
        
        export_action = QAction("Exporter", self)
        export_action.triggered.connect(self.export_prompt)
        menu.addAction(export_action)
        
        duplicate_action = QAction("Dupliquer", self)
        duplicate_action.triggered.connect(self.duplicate_prompt)
        menu.addAction(duplicate_action)
        
        menu.addSeparator()
        
        delete_action = QAction("Supprimer", self)
        delete_action.triggered.connect(self.delete_prompt)
        menu.addAction(delete_action)
        
        menu.exec_(self.prompts_list.mapToGlobal(position))
    
    def update_buttons_state(self):
        has_selection = bool(self.prompts_list.selectedItems())
        
        self.edit_btn.setEnabled(has_selection)
        self.export_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        self.favorite_btn.setEnabled(has_selection)
        self.add_tag_btn.setEnabled(has_selection)
        
        if has_selection:
            prompt_id = self.prompts_list.currentItem().data(Qt.UserRole)
            self.cursor.execute("SELECT is_favorite FROM prompts WHERE id = ?", (prompt_id,))
            is_favorite = self.cursor.fetchone()[0]
            self.favorite_btn.setChecked(is_favorite)
            
            if is_favorite:
                self.favorite_btn.setStyleSheet("background-color: gold; border: none;")
                self.favorite_btn.setToolTip("Retirer des favoris")
            else:
                self.favorite_btn.setStyleSheet("background-color: #40414f; border: 1px solid #565869;")
                self.favorite_btn.setToolTip("Ajouter aux favoris")
    
    def load_categories(self):
        self.category_filter.clear()
        self.category_filter.addItem("Toutes les catégories")
        
        self.cursor.execute("SELECT name FROM categories ORDER BY name")
        categories = self.cursor.fetchall()
        
        for category in categories:
            self.category_filter.addItem(category[0])
    
    def load_tags(self):
        self.tags_filter.clear()
        self.tags_filter.addItem("Tous les tags")
        
        self.cursor.execute("SELECT name FROM tags ORDER BY name")
        tags = self.cursor.fetchall()
        
        for tag in tags:
            self.tags_filter.addItem(tag[0])
    
    def load_prompts(self):
        self.prompts_list.clear()
        
        search_text = self.search_input.text().strip()
        category = self.category_filter.currentText() if self.category_filter.currentText() != "Toutes les catégories" else None
        tag = self.tags_filter.currentText() if self.tags_filter.currentText() != "Tous les tags" else None
        favorites_only = self.favorites_only.isChecked()
        
        query = '''
            SELECT DISTINCT p.id, p.title, c.name, p.is_favorite 
            FROM prompts p
            LEFT JOIN categories c ON p.category_id = c.id
            LEFT JOIN prompt_tags pt ON p.id = pt.prompt_id
            LEFT JOIN tags t ON pt.tag_id = t.id
            WHERE 1=1
        '''
        
        params = []
        
        if search_text:
            query += " AND (p.title LIKE ? OR p.content LIKE ?)"
            params.extend([f"%{search_text}%", f"%{search_text}%"])
        
        if category:
            query += " AND c.name = ?"
            params.append(category)
        
        if tag:
            query += " AND t.name = ?"
            params.append(tag)
        
        if favorites_only:
            query += " AND p.is_favorite = 1"
        
        query += " ORDER BY p.title"
        
        self.cursor.execute(query, params)
        prompts = self.cursor.fetchall()
        
        for prompt in prompts:
            item_text = prompt[1]
            if prompt[2]:
                item_text += f" ({prompt[2]})"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, prompt[0])
            
            if prompt[3]:  # is_favorite
                item.setIcon(QIcon(":/icons/star_filled.png"))
            
            self.prompts_list.addItem(item)
    
    def display_prompt(self):
        selected_items = self.prompts_list.selectedItems()
        if not selected_items:
            return
            
        prompt_id = selected_items[0].data(Qt.UserRole)
        self.current_prompt_id = prompt_id
        
        self.cursor.execute('''
            SELECT p.title, p.content, p.example, c.name, p.is_favorite
            FROM prompts p 
            LEFT JOIN categories c ON p.category_id = c.id 
            WHERE p.id = ?
        ''', (prompt_id,))
        
        prompt = self.cursor.fetchone()
        
        if prompt:
            self.prompt_title.setText(prompt[0])
            
            # Convertir le markdown en HTML si nécessaire
            html_content = self.markdown_to_html(prompt[1])
            self.prompt_content.setHtml(html_content)
            
            html_example = self.markdown_to_html(prompt[2]) if prompt[2] else "<i>Aucun exemple disponible</i>"
            self.prompt_example.setHtml(html_example)
            
            # Charger les tags
            self.load_prompt_tags(prompt_id)
            
            # Charger l'historique
            self.load_prompt_history(prompt_id)
        
        self.update_buttons_state()
    
    def markdown_to_html(self, text):
        if not text:
            return ""
        
        # Convertir le markdown en HTML
        html = markdown.markdown(text)
        
        # Utiliser BeautifulSoup pour nettoyer et formater
        soup = BeautifulSoup(html, 'html.parser')
        
        # Ajouter des styles pour les blocs de code
        for pre in soup.find_all('pre'):
            pre['style'] = 'background-color: #40414f; padding: 10px; border-radius: 5px;'
        
        return str(soup)
    
    def load_prompt_tags(self, prompt_id):
        # Nettoyer les tags précédents
        for i in reversed(range(self.tags_layout.count())): 
            self.tags_layout.itemAt(i).widget().setParent(None)
        
        self.cursor.execute('''
            SELECT t.id, t.name, t.color 
            FROM tags t
            JOIN prompt_tags pt ON t.id = pt.tag_id
            WHERE pt.prompt_id = ?
        ''', (prompt_id,))
        
        tags = self.cursor.fetchall()
        
        for tag in tags:
            tag_id, name, color = tag
            
            tag_btn = QPushButton(name)
            tag_btn.setObjectName("tagButton")
            tag_btn.setCursor(Qt.PointingHandCursor)
            
            if color:
                tag_btn.setStyleSheet(f'''
                    #tagButton {{
                        background-color: {color};
                        color: white;
                        border: none;
                        padding: 3px 8px;
                        border-radius: 10px;
                        font-size: 11px;
                    }}
                ''')
            else:
                tag_btn.setStyleSheet('''
                    #tagButton {
                        background-color: #565869;
                        color: white;
                        border: none;
                        padding: 3px 8px;
                        border-radius: 10px;
                        font-size: 11px;
                    }
                ''')
            
            tag_btn.clicked.connect(lambda _, t=tag_id: self.remove_tag_from_prompt(t))
            self.tags_layout.addWidget(tag_btn)
    
    def load_prompt_history(self, prompt_id):
        self.history_list.clear()
        
        self.cursor.execute('''
            SELECT id, title, updated_at 
            FROM prompt_history 
            WHERE prompt_id = ? 
            ORDER BY updated_at DESC
        ''', (prompt_id,))
        
        history = self.cursor.fetchall()
        
        for version in history:
            version_id, title, updated_at = version
            date_str = datetime.fromisoformat(updated_at).strftime("%d/%m/%Y %H:%M")
            item = QListWidgetItem(f"{date_str} - {title}")
            item.setData(Qt.UserRole, version_id)
            self.history_list.addItem(item)
    
    def show_add_tag_dialog(self):
        if not self.current_prompt_id:
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter un tag")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout(dialog)
        
        # Sélection de tag existant
        existing_tag_combo = QComboBox()
        existing_tag_combo.addItem("-- Sélectionner un tag existant --", None)
        
        self.cursor.execute("SELECT id, name FROM tags ORDER BY name")
        tags = self.cursor.fetchall()
        
        for tag_id, name in tags:
            existing_tag_combo.addItem(name, tag_id)
        
        layout.addWidget(existing_tag_combo)
        
        # Ou création d'un nouveau tag
        new_tag_layout = QHBoxLayout()
        
        new_tag_input = QLineEdit()
        new_tag_input.setPlaceholderText("Nouveau tag")
        new_tag_layout.addWidget(new_tag_input, 1)
        
        color_btn = QPushButton()
        color_btn.setFixedSize(30, 30)
        color_btn.setStyleSheet("background-color: #565869;")
        color_btn.clicked.connect(lambda: self.choose_tag_color(color_btn))
        new_tag_layout.addWidget(color_btn)
        
        layout.addLayout(new_tag_layout)
        
        # Boutons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Ajouter")
        add_btn.setObjectName("action-primary")
        add_btn.clicked.connect(lambda: self.add_tag_to_prompt(
            existing_tag_combo.currentData(),
            new_tag_input.text().strip(),
            color_btn.styleSheet().split(":")[1].split(";")[0].strip(),
            dialog
        ))
        button_layout.addWidget(add_btn)
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("action-danger")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def choose_tag_color(self, button):
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()}; border: none;")
    
    def add_tag_to_prompt(self, existing_tag_id, new_tag_name, color, dialog):
        if not existing_tag_id and not new_tag_name:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un tag existant ou en créer un nouveau!")
            return
            
        tag_id = existing_tag_id
        
        if not existing_tag_id and new_tag_name:
            # Créer un nouveau tag
            try:
                now = datetime.now().isoformat()
                self.cursor.execute(
                    "INSERT INTO tags (name, color, created_at) VALUES (?, ?, ?)",
                    (new_tag_name, color, now)
                )
                tag_id = self.cursor.lastrowid
                self.conn.commit()
                
                # Mettre à jour les listes de tags
                self.load_tags()
                
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Erreur", "Ce tag existe déjà!")
                return
        
        # Associer le tag au prompt
        try:
            self.cursor.execute(
                "INSERT INTO prompt_tags (prompt_id, tag_id) VALUES (?, ?)",
                (self.current_prompt_id, tag_id)
            )
            self.conn.commit()
            
            # Mettre à jour l'affichage
            self.load_prompt_tags(self.current_prompt_id)
            
            dialog.accept()
            
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Erreur", "Ce tag est déjà associé à ce prompt!")
    
    def remove_tag_from_prompt(self, tag_id):
        reply = QMessageBox.question(
            self, 
            'Confirmation', 
            'Voulez-vous vraiment retirer ce tag du prompt?', 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.cursor.execute(
                "DELETE FROM prompt_tags WHERE prompt_id = ? AND tag_id = ?",
                (self.current_prompt_id, tag_id)
            )
            self.conn.commit()
            
            self.load_prompt_tags(self.current_prompt_id)
    
    def toggle_favorite(self):
        if not self.current_prompt_id:
            return
            
        is_favorite = self.favorite_btn.isChecked()
        
        self.cursor.execute(
            "UPDATE prompts SET is_favorite = ? WHERE id = ?",
            (1 if is_favorite else 0, self.current_prompt_id)
        )
        self.conn.commit()
        
        # Mettre à jour l'icône dans la liste
        for i in range(self.prompts_list.count()):
            item = self.prompts_list.item(i)
            if item.data(Qt.UserRole) == self.current_prompt_id:
                if is_favorite:
                    item.setIcon(QIcon(":/icons/star_filled.png"))
                else:
                    item.setIcon(QIcon())
                break
        
        self.update_buttons_state()
    
    def add_new_prompt(self):
        self.open_prompt_editor()
    
    def edit_prompt(self):
        if not self.current_prompt_id:
            return
            
        self.open_prompt_editor(self.current_prompt_id)
    
    def open_prompt_editor(self, prompt_id=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nouveau prompt" if not prompt_id else "Modifier le prompt")
        dialog.setMinimumSize(700, 600)
        
        layout = QVBoxLayout(dialog)
        
        # Titre
        title_label = QLabel("Titre:")
        self.editor_title = QLineEdit()
        layout.addWidget(title_label)
        layout.addWidget(self.editor_title)
        
        # Catégorie
        category_label = QLabel("Catégorie:")
        category_layout = QHBoxLayout()
        
        self.editor_category = QComboBox()
        self.editor_category.addItem("Sans catégorie", None)
        
        self.cursor.execute("SELECT id, name FROM categories ORDER BY name")
        categories = self.cursor.fetchall()
        
        for cat_id, name in categories:
            self.editor_category.addItem(name, cat_id)
        
        category_layout.addWidget(self.editor_category, 1)
        
        add_category_btn = QPushButton("+")
        add_category_btn.setFixedSize(30, 30)
        add_category_btn.clicked.connect(self.add_new_category)
        category_layout.addWidget(add_category_btn)
        
        layout.addWidget(category_label)
        layout.addLayout(category_layout)
        
        # Contenu
        content_label = QLabel("Contenu du prompt (Markdown supporté):")
        self.editor_content = QTextEdit()
        layout.addWidget(content_label)
        layout.addWidget(self.editor_content, 1)
        
        # Exemple
        example_label = QLabel("Exemple de sortie (Markdown supporté):")
        self.editor_example = QTextEdit()
        layout.addWidget(example_label)
        layout.addWidget(self.editor_example, 1)
        
        # Boutons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Enregistrer")
        save_btn.setObjectName("action-primary")
        save_btn.clicked.connect(lambda: self.save_prompt(prompt_id, dialog))
        button_layout.addWidget(save_btn)
        
        preview_btn = QPushButton("Aperçu")
        preview_btn.setObjectName("action-secondary")
        preview_btn.clicked.connect(self.show_preview)
        button_layout.addWidget(preview_btn)
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("action-danger")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Charger les données existantes si modification
        if prompt_id:
            self.cursor.execute('''
                SELECT title, content, example, category_id 
                FROM prompts 
                WHERE id = ?
            ''', (prompt_id,))
            
            prompt = self.cursor.fetchone()
            
            if prompt:
                self.editor_title.setText(prompt[0])
                self.editor_content.setPlainText(prompt[1])
                self.editor_example.setPlainText(prompt[2] if prompt[2] else "")
                
                if prompt[3]:
                    index = self.editor_category.findData(prompt[3])
                    if index >= 0:
                        self.editor_category.setCurrentIndex(index)
        
        dialog.exec_()
    
    def show_preview(self):
        preview_dialog = QDialog(self)
        preview_dialog.setWindowTitle("Aperçu du prompt")
        preview_dialog.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(preview_dialog)
        
        tabs = QTabWidget()
        
        # Onglet Prompt
        prompt_tab = QWidget()
        prompt_layout = QVBoxLayout(prompt_tab)
        
        prompt_preview = QTextEdit()
        prompt_preview.setReadOnly(True)
        prompt_preview.setHtml(self.markdown_to_html(self.editor_content.toPlainText()))
        prompt_layout.addWidget(prompt_preview, 1)
        
        tabs.addTab(prompt_tab, "Prompt")
        
        # Onglet Exemple
        example_tab = QWidget()
        example_layout = QVBoxLayout(example_tab)
        
        example_preview = QTextEdit()
        example_preview.setReadOnly(True)
        example_preview.setHtml(self.markdown_to_html(self.editor_example.toPlainText()))
        example_layout.addWidget(example_preview, 1)
        
        tabs.addTab(example_tab, "Exemple")
        
        layout.addWidget(tabs)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(preview_dialog.accept)
        layout.addWidget(close_btn)
        
        preview_dialog.exec_()
    
    def save_prompt(self, prompt_id, dialog):
        title = self.editor_title.text().strip()
        content = self.editor_content.toPlainText().strip()
        example = self.editor_example.toPlainText().strip()
        category_id = self.editor_category.currentData()
        
        if not title or not content:
            QMessageBox.warning(self, "Erreur", "Le titre et le contenu sont obligatoires!")
            return
            
        now = datetime.now().isoformat()
        
        if prompt_id:
            # Sauvegarder la version actuelle dans l'historique
            self.cursor.execute('''
                INSERT INTO prompt_history (prompt_id, title, content, example, category_id, updated_at)
                SELECT id, title, content, example, category_id, updated_at 
                FROM prompts 
                WHERE id = ?
            ''', (prompt_id,))
            
            # Mettre à jour le prompt
            self.cursor.execute('''
                UPDATE prompts 
                SET title = ?, content = ?, example = ?, category_id = ?, updated_at = ?
                WHERE id = ?
            ''', (title, content, example if example else None, category_id, now, prompt_id))
            
            self.conn.commit()
            
            QMessageBox.information(self, "Succès", "Prompt mis à jour avec succès!")
        else:
            # Créer un nouveau prompt
            self.cursor.execute('''
                INSERT INTO prompts (title, content, example, category_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, content, example if example else None, category_id, now, now))
            
            self.conn.commit()
            
            QMessageBox.information(self, "Succès", "Prompt créé avec succès!")
        
        # Recharger les données
        self.load_categories()
        self.load_prompts()
        
        dialog.accept()
    
    def add_new_category(self):
        name, ok = QInputDialog.getText(
            self, 
            "Nouvelle catégorie", 
            "Nom de la nouvelle catégorie:",
            QLineEdit.Normal
        )
        
        if ok and name:
            try:
                now = datetime.now().isoformat()
                self.cursor.execute(
                    "INSERT INTO categories (name, created_at) VALUES (?, ?)",
                    (name, now)
                )
                self.conn.commit()
                
                # Mettre à jour les combobox
                self.load_categories()
                
                # Sélectionner la nouvelle catégorie dans l'éditeur
                if hasattr(self, 'editor_category'):
                    index = self.editor_category.findText(name)
                    if index >= 0:
                        self.editor_category.setCurrentIndex(index)
                
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Erreur", "Cette catégorie existe déjà!")
    
    def delete_prompt(self):
        selected_items = self.prompts_list.selectedItems()
        if not selected_items:
            return
            
        prompt_id = selected_items[0].data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self, 
            'Confirmation', 
            'Êtes-vous sûr de vouloir supprimer ce prompt?', 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Supprimer les associations de tags d'abord
            self.cursor.execute("DELETE FROM prompt_tags WHERE prompt_id = ?", (prompt_id,))
            
            # Supprimer l'historique
            self.cursor.execute("DELETE FROM prompt_history WHERE prompt_id = ?", (prompt_id,))
            
            # Supprimer le prompt
            self.cursor.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
            self.conn.commit()
            
            # Recharger les données
            self.load_prompts()
            
            # Effacer l'affichage
            self.prompt_title.setText("Sélectionnez un prompt")
            self.prompt_content.clear()
            self.prompt_example.clear()
            self.current_prompt_id = None
            
            self.update_buttons_state()
    
    def export_prompt(self):
        if not self.current_prompt_id:
            return
            
        self.cursor.execute('''
            SELECT p.title, p.content, p.example, c.name, 
                   GROUP_CONCAT(t.name, ', ') as tags
            FROM prompts p
            LEFT JOIN categories c ON p.category_id = c.id
            LEFT JOIN prompt_tags pt ON p.id = pt.prompt_id
            LEFT JOIN tags t ON pt.tag_id = t.id
            WHERE p.id = ?
            GROUP BY p.id
        ''', (self.current_prompt_id,))
        
        prompt = self.cursor.fetchone()
        
        if not prompt:
            return
            
        title, content, example, category, tags = prompt
        
        # Formater les données pour l'export
        prompt_data = {
            "title": title,
            "content": content,
            "example": example,
            "category": category,
            "tags": tags.split(", ") if tags else [],
            "exported_at": datetime.now().isoformat()
        }
        
        # Demander où sauvegarder le fichier
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter le prompt",
            f"{title.replace(' ', '_')}.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(prompt_data, f, ensure_ascii=False, indent=2)
                
                QMessageBox.information(self, "Succès", "Prompt exporté avec succès!")
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de l'export: {str(e)}")
    
    def import_prompt(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Importer un prompt",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    prompt_data = json.load(f)
                
                # Ouvrir l'éditeur avec les données importées
                dialog = QDialog(self)
                dialog.setWindowTitle("Importer un prompt")
                dialog.setMinimumSize(700, 600)
                
                layout = QVBoxLayout(dialog)
                
                # Titre
                title_label = QLabel("Titre:")
                title_input = QLineEdit(prompt_data.get("title", ""))
                layout.addWidget(title_label)
                layout.addWidget(title_input)
                
                # Catégorie
                category_label = QLabel("Catégorie:")
                category_layout = QHBoxLayout()
                
                category_combo = QComboBox()
                category_combo.addItem("Sans catégorie", None)
                
                self.cursor.execute("SELECT id, name FROM categories ORDER BY name")
                categories = self.cursor.fetchall()
                
                for cat_id, name in categories:
                    category_combo.addItem(name, cat_id)
                
                if "category" in prompt_data and prompt_data["category"]:
                    index = category_combo.findText(prompt_data["category"])
                    if index >= 0:
                        category_combo.setCurrentIndex(index)
                
                category_layout.addWidget(category_combo, 1)
                
                add_category_btn = QPushButton("+")
                add_category_btn.setFixedSize(30, 30)
                add_category_btn.clicked.connect(self.add_new_category)
                category_layout.addWidget(add_category_btn)
                
                layout.addWidget(category_label)
                layout.addLayout(category_layout)
                
                # Contenu
                content_label = QLabel("Contenu du prompt:")
                content_input = QTextEdit(prompt_data.get("content", ""))
                layout.addWidget(content_label)
                layout.addWidget(content_input, 1)
                
                # Exemple
                example_label = QLabel("Exemple de sortie:")
                example_input = QTextEdit(prompt_data.get("example", ""))
                layout.addWidget(example_label)
                layout.addWidget(example_input, 1)
                
                # Tags (affichage seulement)
                if "tags" in prompt_data and prompt_data["tags"]:
                    tags_label = QLabel("Tags inclus dans l'import:")
                    layout.addWidget(tags_label)
                    
                    tags_display = QLabel(", ".join(prompt_data["tags"]))
                    tags_display.setStyleSheet("color: #acacbe; font-style: italic;")
                    layout.addWidget(tags_display)
                
                # Boutons
                button_layout = QHBoxLayout()
                
                save_btn = QPushButton("Enregistrer")
                save_btn.setObjectName("action-primary")
                save_btn.clicked.connect(lambda: self.save_imported_prompt(
                    title_input.text(),
                    category_combo.currentData(),
                    content_input.toPlainText(),
                    example_input.toPlainText(),
                    prompt_data.get("tags", []),
                    dialog
                ))
                button_layout.addWidget(save_btn)
                
                cancel_btn = QPushButton("Annuler")
                cancel_btn.setObjectName("action-danger")
                cancel_btn.clicked.connect(dialog.reject)
                button_layout.addWidget(cancel_btn)
                
                layout.addLayout(button_layout)
                
                dialog.exec_()
                
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de l'import: {str(e)}")
    
    def save_imported_prompt(self, title, category_id, content, example, tags, dialog):
        if not title or not content:
            QMessageBox.warning(self, "Erreur", "Le titre et le contenu sont obligatoires!")
            return
            
        now = datetime.now().isoformat()
        
        # Créer le prompt
        self.cursor.execute('''
            INSERT INTO prompts (title, content, example, category_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, content, example if example else None, category_id, now, now))
        
        prompt_id = self.cursor.lastrowid
        
        # Ajouter les tags
        if tags:
            for tag_name in tags:
                # Vérifier si le tag existe
                self.cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
                tag = self.cursor.fetchone()
                
                if not tag:
                    # Créer le tag s'il n'existe pas
                    self.cursor.execute(
                        "INSERT INTO tags (name, created_at) VALUES (?, ?)",
                        (tag_name, now)
                    )
                    tag_id = self.cursor.lastrowid
                else:
                    tag_id = tag[0]
                
                # Associer le tag au prompt
                try:
                    self.cursor.execute(
                        "INSERT INTO prompt_tags (prompt_id, tag_id) VALUES (?, ?)",
                        (prompt_id, tag_id)
                    )
                except sqlite3.IntegrityError:
                    pass  # L'association existe déjà
        
        self.conn.commit()
        
        # Recharger les données
        self.load_tags()
        self.load_prompts()
        
        dialog.accept()
        
        QMessageBox.information(self, "Succès", "Prompt importé avec succès!")
    
    def duplicate_prompt(self):
        if not self.current_prompt_id:
            return
            
        self.cursor.execute('''
            SELECT title, content, example, category_id 
            FROM prompts 
            WHERE id = ?
        ''', (self.current_prompt_id,))
        
        prompt = self.cursor.fetchone()
        
        if not prompt:
            return
            
        title, content, example, category_id = prompt
        
        # Créer une copie avec " (Copie)" ajouté au titre
        now = datetime.now().isoformat()
        new_title = f"{title} (Copie)"
        
        self.cursor.execute('''
            INSERT INTO prompts (title, content, example, category_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (new_title, content, example, category_id, now, now))
        
        new_prompt_id = self.cursor.lastrowid
        
        # Copier les tags
        self.cursor.execute('''
            INSERT INTO prompt_tags (prompt_id, tag_id)
            SELECT ?, tag_id FROM prompt_tags WHERE prompt_id = ?
        ''', (new_prompt_id, self.current_prompt_id))
        
        self.conn.commit()
        
        # Recharger les données
        self.load_prompts()
        
        QMessageBox.information(self, "Succès", "Prompt dupliqué avec succès!")
    
    def display_history_version(self):
        selected_items = self.history_list.selectedItems()
        if not selected_items:
            return
            
        version_id = selected_items[0].data(Qt.UserRole)
        
        self.cursor.execute('''
            SELECT title, content, example 
            FROM prompt_history 
            WHERE id = ?
        ''', (version_id,))
        
        version = self.cursor.fetchone()
        
        if version:
            self.prompt_title.setText(f"{version[0]} (version historique)")
            self.prompt_content.setHtml(self.markdown_to_html(version[1]))
            self.prompt_example.setHtml(self.markdown_to_html(version[2]) if version[2] else "<i>Aucun exemple disponible</i>")
    
    def restore_history_version(self):
        selected_items = self.history_list.selectedItems()
        if not selected_items or not self.current_prompt_id:
            return
            
        version_id = selected_items[0].data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self, 
            'Confirmation', 
            'Voulez-vous vraiment restaurer cette version? La version actuelle sera sauvegardée dans l\'historique.', 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Sauvegarder la version actuelle dans l'historique
            self.cursor.execute('''
                INSERT INTO prompt_history (prompt_id, title, content, example, category_id, updated_at)
                SELECT id, title, content, example, category_id, updated_at 
                FROM prompts 
                WHERE id = ?
            ''', (self.current_prompt_id,))
            
            # Récupérer la version historique
            self.cursor.execute('''
                SELECT title, content, example, category_id 
                FROM prompt_history 
                WHERE id = ?
            ''', (version_id,))
            
            version = self.cursor.fetchone()
            
            if version:
                # Restaurer la version
                now = datetime.now().isoformat()
                self.cursor.execute('''
                    UPDATE prompts 
                    SET title = ?, content = ?, example = ?, category_id = ?, updated_at = ?
                    WHERE id = ?
                ''', (*version, now, self.current_prompt_id))
                
                self.conn.commit()
                
                # Recharger les données
                self.load_prompts()
                self.display_prompt()
                
                QMessageBox.information(self, "Succès", "Version restaurée avec succès!")
    
    def create_menu1(self):
        menu_bar = self.menuBar()
        
        # Menu Fichier
        file_menu = menu_bar.addMenu("Fichier")
        
        import_action = QAction("Importer un prompt", self)
        import_action.triggered.connect(self.import_prompt)
        file_menu.addAction(import_action)
        
        export_action = QAction("Exporter le prompt sélectionné", self)
        export_action.triggered.connect(self.export_prompt)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Quitter", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Édition
        edit_menu = menu_bar.addMenu("Édition")
        
        new_prompt_action = QAction("Nouveau prompt", self)
        new_prompt_action.triggered.connect(self.add_new_prompt)
        edit_menu.addAction(new_prompt_action)
        
        edit_prompt_action = QAction("Modifier le prompt", self)
        edit_prompt_action.triggered.connect(self.edit_prompt)
        edit_menu.addAction(edit_prompt_action)
        
        duplicate_action = QAction("Dupliquer le prompt", self)
        duplicate_action.triggered.connect(self.duplicate_prompt)
        edit_menu.addAction(duplicate_action)
        
        edit_menu.addSeparator()
        
        new_category_action = QAction("Nouvelle catégorie", self)
        new_category_action.triggered.connect(self.add_new_category)
        edit_menu.addAction(new_category_action)
        
        # Menu Aide
        help_menu = menu_bar.addMenu("Aide")
        
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def show_about(self):
        QMessageBox.about(
            self,
            "À propos de Prompt Genius",
            "Prompt Genius\n\n"
            "Une application pour gérer, organiser et réutiliser vos prompts.\n\n"
            "Version 1.0\n"
            "© 2023 - Tous droits réservés"
        )
    
    def closeEvent(self, event):
        self.conn.close()
        event.accept()










































    def setup_shortcuts(self):
        """Configurer les raccourcis clavier"""
        self.new_prompt_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.new_prompt_shortcut.activated.connect(self.add_new_prompt)
        
        self.search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.search_shortcut.activated.connect(lambda: self.search_input.setFocus())
        
        self.export_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        self.export_shortcut.activated.connect(self.export_prompt)
        
        self.delete_shortcut = QShortcut(QKeySequence("Del"), self)
        self.delete_shortcut.activated.connect(self.delete_prompt)

    def show_tag_manager(self):
        """Afficher le gestionnaire de tags"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Gestionnaire de Tags")
        dialog.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Liste des tags
        self.all_tags_list = QListWidget()
        self.load_all_tags()
        layout.addWidget(self.all_tags_list)
        
        # Boutons d'action
        button_layout = QHBoxLayout()
        
        edit_btn = QPushButton("Modifier")
        edit_btn.setObjectName("action-secondary")
        edit_btn.clicked.connect(self.edit_tag)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Supprimer")
        delete_btn.setObjectName("action-danger")
        delete_btn.clicked.connect(self.delete_tag)
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
        
        dialog.exec_()

    def load_all_tags(self):
        """Charger tous les tags dans la liste"""
        self.all_tags_list.clear()
        
        self.cursor.execute("SELECT id, name, color FROM tags ORDER BY name")
        tags = self.cursor.fetchall()
        
        for tag_id, name, color in tags:
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, tag_id)
            
            if color:
                item.setBackground(QColor(color))
                item.setForeground(QColor("white"))
            
            self.all_tags_list.addItem(item)

    def edit_tag(self):
        """Modifier un tag existant"""
        selected_items = self.all_tags_list.selectedItems()
        if not selected_items:
            return
            
        tag_id = selected_items[0].data(Qt.UserRole)
        
        self.cursor.execute("SELECT name, color FROM tags WHERE id = ?", (tag_id,))
        tag_name, color = self.cursor.fetchone()
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier le Tag")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout(dialog)
        
        # Nom du tag
        name_input = QLineEdit(tag_name)
        layout.addWidget(QLabel("Nom du tag:"))
        layout.addWidget(name_input)
        
        # Couleur
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Couleur:"))
        
        color_btn = QPushButton()
        color_btn.setFixedSize(30, 30)
        color_btn.setStyleSheet(f"background-color: {color if color else '#565869'};")
        color_btn.clicked.connect(lambda: self.choose_tag_color(color_btn))
        color_layout.addWidget(color_btn)
        
        layout.addLayout(color_layout)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("Enregistrer")
        save_btn.setObjectName("action-primary")
        save_btn.clicked.connect(lambda: self.save_tag_changes(
            tag_id,
            name_input.text().strip(),
            color_btn.styleSheet().split(":")[1].split(";")[0].strip(),
            dialog
        ))
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("action-danger")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        dialog.exec_()

    def save_tag_changes(self, tag_id, new_name, new_color, dialog):
        """Sauvegarder les modifications d'un tag"""
        if not new_name:
            QMessageBox.warning(self, "Erreur", "Le nom du tag ne peut pas être vide!")
            return
            
        try:
            self.cursor.execute(
                "UPDATE tags SET name = ?, color = ? WHERE id = ?",
                (new_name, new_color, tag_id)
            )
            self.conn.commit()
            
            # Mettre à jour les affichages
            self.load_all_tags()
            self.load_tags()
            
            if self.current_prompt_id:
                self.load_prompt_tags(self.current_prompt_id)
            
            dialog.accept()
            
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Erreur", "Un tag avec ce nom existe déjà!")

    def delete_tag(self):
        """Supprimer un tag"""
        selected_items = self.all_tags_list.selectedItems()
        if not selected_items:
            return
            
        tag_id = selected_items[0].data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self, 
            'Confirmation', 
            'Voulez-vous vraiment supprimer ce tag? Cette action le retirera de tous les prompts.', 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Supprimer les associations d'abord
            self.cursor.execute("DELETE FROM prompt_tags WHERE tag_id = ?", (tag_id,))
            
            # Supprimer le tag
            self.cursor.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
            self.conn.commit()
            
            # Mettre à jour les affichages
            self.load_all_tags()
            self.load_tags()
            
            if self.current_prompt_id:
                self.load_prompt_tags(self.current_prompt_id)

    def show_stats(self):
        """Afficher les statistiques"""
        stats_dialog = QDialog(self)
        stats_dialog.setWindowTitle("Statistiques")
        stats_dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout(stats_dialog)
        
        # Récupérer les stats
        self.cursor.execute("SELECT COUNT(*) FROM prompts")
        total_prompts = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM categories")
        total_categories = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM tags")
        total_tags = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM prompts WHERE is_favorite = 1")
        total_favorites = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM prompt_history")
        total_versions = self.cursor.fetchone()[0]
        
        # Afficher les stats
        stats_html = f"""
        <style>
            body {{ font-family: Arial, sans-serif; color: white; }}
            h2 {{ color: #10a37f; margin-top: 0; }}
            .stat {{ margin-bottom: 10px; }}
            .stat-name {{ font-weight: bold; color: #acacbe; }}
            .stat-value {{ color: white; }}
        </style>
        <body>
            <h2>Statistiques</h2>
            <div class="stat">
                <span class="stat-name">Prompts:</span>
                <span class="stat-value">{total_prompts}</span>
            </div>
            <div class="stat">
                <span class="stat-name">Catégories:</span>
                <span class="stat-value">{total_categories}</span>
            </div>
            <div class="stat">
                <span class="stat-name">Tags:</span>
                <span class="stat-value">{total_tags}</span>
            </div>
            <div class="stat">
                <span class="stat-name">Favoris:</span>
                <span class="stat-value">{total_favorites}</span>
            </div>
            <div class="stat">
                <span class="stat-name">Versions historiques:</span>
                <span class="stat-value">{total_versions}</span>
            </div>
        </body>
        """
        
        stats_view = QTextEdit()
        stats_view.setReadOnly(True)
        stats_view.setHtml(stats_html)
        layout.addWidget(stats_view)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(stats_dialog.accept)
        layout.addWidget(close_btn)
        
        stats_dialog.exec_()

    def backup_database(self):
        """Créer une sauvegarde de la base de données"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder la base de données",
            "prompts_backup.db",
            "Fichiers SQLite (*.db *.sqlite);;Tous les fichiers (*)",
            options=options
        )
        
        if file_path:
            try:
                # Fermer la connexion actuelle
                self.conn.close()
                
                # Copier le fichier
                import shutil
                shutil.copy2(DB_PATH_prompts, file_path)
                
                # Rouvrir la connexion
                self.conn = sqlite3.connect(DB_PATH_prompts)
                self.cursor = self.conn.cursor()
                
                QMessageBox.information(self, "Succès", "Sauvegarde créée avec succès!")
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de la sauvegarde: {str(e)}")
                # Rouvrir la connexion en cas d'erreur
                self.conn = sqlite3.connect(DB_PATH_prompts)
                self.cursor = self.conn.cursor()

    def restore_database(self):
        """Restaurer la base de données depuis une sauvegarde"""
        reply = QMessageBox.warning(
            self,
            "Attention",
            "Cette action écrasera votre base de données actuelle. Voulez-vous continuer?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
            
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Restaurer la base de données",
            "",
            "Fichiers SQLite (*.db *.sqlite);;Tous les fichiers (*)",
            options=options
        )
        
        if file_path:
            try:
                # Fermer la connexion actuelle
                self.conn.close()
                
                # Remplacer le fichier
                import shutil
                shutil.copy2(file_path, DB_PATH_prompts)
                
                # Rouvrir la connexion
                self.conn = sqlite3.connect(DB_PATH_prompts)
                self.cursor = self.conn.cursor()
                
                # Recharger les données
                self.load_categories()
                self.load_tags()
                self.load_prompts()
                
                QMessageBox.information(self, "Succès", "Base de données restaurée avec succès!")
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de la restauration: {str(e)}")
                # Rouvrir la connexion en cas d'erreur
                self.conn = sqlite3.connect(DB_PATH_prompts)
                self.cursor = self.conn.cursor()





    def setup_tray_icon(self):
        """Configurer l'icône de la barre système"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
            
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("prompt_icon.png"))
        
        tray_menu = QMenu()
        
        show_action = QAction("Ouvrir Prompt Genius", self)
        show_action.triggered.connect(self.show_normal)
        tray_menu.addAction(show_action)
        
        new_prompt_action = QAction("Nouveau Prompt", self)
        new_prompt_action.triggered.connect(self.add_new_prompt)
        tray_menu.addAction(new_prompt_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("Quitter", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        """Gérer les clics sur l'icône de la barre système"""
        if reason == QSystemTrayIcon.Trigger:
            self.show_normal()

    def show_normal(self):
        """Afficher la fenêtre normalement"""
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.raise_()

    def closeEvent(self, event):
        """Gérer la fermeture de la fenêtre"""
        if self.tray_icon and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            self.conn.close()
            event.accept()

    def setup_auto_backup(self):
        """Configurer la sauvegarde automatique"""
        self.backup_timer = QTimer()
        self.backup_timer.timeout.connect(self.auto_backup)
        self.backup_timer.start(3600000)  # Toutes les heures

    def auto_backup(self):
        """Effectuer une sauvegarde automatique"""
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        backup_path = os.path.join(
            backup_dir,
            f"prompts_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.db"
        )
        
        try:
            # Fermer la connexion actuelle
            self.conn.close()
            
            # Créer la sauvegarde
            import shutil
            shutil.copy2(DB_PATH_prompts, backup_path)
            
            # Rouvrir la connexion
            self.conn = sqlite3.connect(DB_PATH_prompts)
            self.cursor = self.conn.cursor()
            
            # Garder seulement les 5 dernières sauvegardes
            backups = sorted(
                [f for f in os.listdir(backup_dir) if f.startswith('prompts_backup_')],
                reverse=True
            )
            for old_backup in backups[5:]:
                os.remove(os.path.join(backup_dir, old_backup))
                
        except Exception as e:
            print(f"Erreur lors de la sauvegarde automatique: {str(e)}")
            # Rouvrir la connexion en cas d'erreur
            self.conn = sqlite3.connect(DB_PATH_prompts)
            self.cursor = self.conn.cursor()

    def show_sync_dialog(self):
        """Afficher le dialogue de synchronisation"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Synchronisation")
        dialog.setFixedSize(400, 200)
        
        layout = QVBoxLayout(dialog)
        
        # Options de synchronisation
        self.sync_cloud = QCheckBox("Synchroniser avec le cloud")
        self.sync_cloud.setChecked(False)
        layout.addWidget(self.sync_cloud)
        
        self.sync_local = QCheckBox("Synchroniser avec un dossier local")
        self.sync_local.setChecked(False)
        layout.addWidget(self.sync_local)
        
        # Boutons
        button_layout = QHBoxLayout()
        
        sync_btn = QPushButton("Synchroniser")
        sync_btn.setObjectName("action-primary")
        sync_btn.clicked.connect(lambda: self.start_sync(dialog))
        button_layout.addWidget(sync_btn)
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("action-danger")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        dialog.exec_()

    def start_sync(self, dialog):
        """Démarrer la synchronisation"""
        if self.sync_cloud.isChecked():
            self.sync_with_cloud()
        
        if self.sync_local.isChecked():
            self.sync_with_local()
        
        QMessageBox.information(
            self,
            "Synchronisation",
            "Synchronisation terminée avec succès!"
        )
        dialog.accept()

    def sync_with_cloud(self):
        """Synchroniser avec le cloud (simulé)"""
        # En production, vous implémenteriez ici la logique réelle
        print("Synchronisation avec le cloud effectuée")

    def sync_with_local(self):
        """Synchroniser avec un dossier local"""
        options = QFileDialog.Options()
        folder = QFileDialog.getExistingDirectory(
            self,
            "Sélectionner le dossier de synchronisation",
            options=options
        )
        
        if folder:
            try:
                # Créer un fichier de synchronisation
                sync_file = os.path.join(folder, "prompts_sync.json")
                
                # Exporter tous les prompts
                self.cursor.execute('''
                    SELECT p.id, p.title, p.content, p.example, c.name, 
                           GROUP_CONCAT(t.name, ', ') as tags
                    FROM prompts p
                    LEFT JOIN categories c ON p.category_id = c.id
                    LEFT JOIN prompt_tags pt ON p.id = pt.prompt_id
                    LEFT JOIN tags t ON pt.tag_id = t.id
                    GROUP BY p.id
                ''')
                
                prompts = []
                for row in self.cursor.fetchall():
                    prompt_id, title, content, example, category, tags = row
                    prompts.append({
                        "title": title,
                        "content": content,
                        "example": example,
                        "category": category,
                        "tags": tags.split(", ") if tags else []
                    })
                
                with open(sync_file, 'w', encoding='utf-8') as f:
                    json.dump({"prompts": prompts}, f, ensure_ascii=False, indent=2)
                
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Erreur",
                    f"Erreur lors de la synchronisation: {str(e)}"
                )

    def setup_auto_complete(self):
        """Configurer l'auto-complétion pour la recherche"""
        completer = QCompleter()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        
        self.model = QStringListModel()
        completer.setModel(self.model)
        
        self.search_input.setCompleter(completer)
        
        # Mettre à jour la liste de complétion
        self.update_completer_model()

    def update_completer_model(self):
        """Mettre à jour le modèle de complétion"""
        self.cursor.execute("SELECT title FROM prompts")
        titles = [row[0] for row in self.cursor.fetchall()]
        
        self.cursor.execute("SELECT name FROM categories")
        categories = [row[0] for row in self.cursor.fetchall()]
        
        self.cursor.execute("SELECT name FROM tags")
        tags = [row[0] for row in self.cursor.fetchall()]
        
        all_items = titles + categories + tags
        self.model.setStringList(all_items)




import sys
import os
import logging
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QListWidget, QTextEdit, QPushButton, QLabel, QLineEdit,
                             QSplitter, QComboBox, QMessageBox, QInputDialog, QFrame,
                             QFileDialog, QTabWidget, QCheckBox, QMenu, QAction, QDialog,
                             QListWidgetItem, QColorDialog, QShortcut, QSystemTrayIcon)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QColor, QTextCharFormat, QTextCursor
import sqlite3
from datetime import datetime
import markdown
from bs4 import BeautifulSoup
from imports import DB_PATH_prompts
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import QStringListModel

class PromptManager(QMainWindow):
    def __init__(self, main_app=None):
        """Initialisation de l'application principale"""
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("Prompt Genius")
        self.setGeometry(100, 100, 1400, 900)
        self.setWindowIcon(QIcon("prompt_icon.png"))

        # Configuration du style
        self.setup_styles()

        # Initialisation de la base de données
        self.init_db()

        # Variables d'état
        self.current_prompt_id = None
        self.search_delay_timer = QTimer()
        self.search_delay_timer.setSingleShot(True)
        self.search_delay_timer.timeout.connect(self.load_prompts)

        # Création de l'interface
        self.create_ui()

        # Charger les données initiales
        self.load_categories()
        self.load_tags()
        self.load_prompts()

        # Configurer les raccourcis clavier
        self.setup_shortcuts()

        # Configurer l'icône de la barre système
        self.setup_tray_icon()

        # Configurer la sauvegarde automatique
        self.setup_auto_backup()

        # Configurer l'auto-complétion pour la recherche
        self.setup_auto_complete()

        # Créer le menu
        self.create_menu()
    def show_about(self):
        QMessageBox.about(
            self,
            "À propos de Prompt Genius",
            "Prompt Genius\n\n"
            "Une application pour gérer, organiser et réutiliser vos prompts.\n\n"
            "Version 1.0\n"
            "© 2025 - Tous droits réservés"
        )
    
    def create_menu(self):
        menu_bar = self.menuBar()

        # Menu Fichier
        file_menu = menu_bar.addMenu("Fichier")

        import_action = QAction("Importer un prompt", self)
        import_action.triggered.connect(self.import_prompt)
        file_menu.addAction(import_action)

        export_action = QAction("Exporter le prompt sélectionné", self)
        export_action.triggered.connect(self.export_prompt)
        file_menu.addAction(export_action)

        backup_action = QAction("Sauvegarder la base de données", self)
        backup_action.triggered.connect(self.backup_database)
        file_menu.addAction(backup_action)

        restore_action = QAction("Restaurer la base de données", self)
        restore_action.triggered.connect(self.restore_database)
        file_menu.addAction(restore_action)

        file_menu.addSeparator()

        exit_action = QAction("Quitter", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menu Édition
        edit_menu = menu_bar.addMenu("Édition")

        new_prompt_action = QAction("Nouveau prompt", self)
        new_prompt_action.triggered.connect(self.add_new_prompt)
        edit_menu.addAction(new_prompt_action)

        edit_prompt_action = QAction("Modifier le prompt", self)
        edit_prompt_action.triggered.connect(self.edit_prompt)
        edit_menu.addAction(edit_prompt_action)

        duplicate_action = QAction("Dupliquer le prompt", self)
        duplicate_action.triggered.connect(self.duplicate_prompt)
        edit_menu.addAction(duplicate_action)

        edit_menu.addSeparator()

        new_category_action = QAction("Nouvelle catégorie", self)
        new_category_action.triggered.connect(self.add_new_category)
        edit_menu.addAction(new_category_action)

        manage_tags_action = QAction("Gérer les tags", self)
        manage_tags_action.triggered.connect(self.show_tag_manager)
        edit_menu.addAction(manage_tags_action)

        # Menu Aide
        help_menu = menu_bar.addMenu("Aide")

        markdown_help_action = QAction("Aide Markdown", self)
        markdown_help_action.triggered.connect(self.show_markdown_help)
        help_menu.addAction(markdown_help_action)

        stats_action = QAction("Statistiques", self)
        stats_action.triggered.connect(self.show_stats)
        help_menu.addAction(stats_action)

        sync_action = QAction("Synchroniser", self)
        sync_action.triggered.connect(self.show_sync_dialog)
        help_menu.addAction(sync_action)

        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_markdown_help(self):
        """Afficher l'aide sur le markdown"""
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Aide Markdown")
        help_dialog.setMinimumSize(500, 400)

        layout = QVBoxLayout(help_dialog)

        markdown_help = """
        <style>
            body { font-family: Arial, sans-serif; color: black; }
            h2 { color: #10a37f; }
            table { border-collapse: collapse; width: 100%; margin: 15px 0; }
            th, td { border: 1px solid #565869; padding: 8px; text-align: left; }
            th { background-color: #40414f; }
            code { background-color: #40414f; padding: 2px 4px; border-radius: 3px; }
        </style>
        <body>
            <h2>Syntaxe Markdown</h2>
            <p>Vous pouvez utiliser la syntaxe Markdown pour formater vos prompts et exemples.</p>

            <table>
                <tr><th>Style</th><th>Syntaxe</th><th>Résultat</th></tr>
                <tr>
                    <td>Gras</td>
                    <td><code>**texte**</code> ou <code>__texte__</code></td>
                    <td><strong>texte</strong></td>
                </tr>
                <tr>
                    <td>Italique</td>
                    <td><code>*texte*</code> ou <code>_texte_</code></td>
                    <td><em>texte</em></td>
                </tr>
                <tr>
                    <td>Titre</td>
                    <td><code># Titre 1</code><br><code>## Titre 2</code></td>
                    <td><h1 style="font-size: 1.5em; margin: 0;">Titre 1</h1><h2 style="font-size: 1.2em; margin: 0;">Titre 2</h2></td>
                </tr>
                <tr>
                    <td>Liste</td>
                    <td><code>- Item 1</code><br><code>- Item 2</code></td>
                    <td><ul><li>Item 1</li><li>Item 2</li></ul></td>
                </tr>
                <tr>
                    <td>Code</td>
                    <td><code>`code inline`</code><br><code>```bloc de code```</code></td>
                    <td><code>code inline</code><br><pre style="background-color: #40414f; padding: 10px;">bloc de code</pre></td>
                </tr>
                <tr>
                    <td>Lien</td>
                    <td><code>[texte](url)</code></td>
                    <td><a href="#">texte</a></td>
                </tr>
            </table>
        </body>
        """

        help_view = QTextEdit()
        help_view.setReadOnly(True)
        help_view.setHtml(markdown_help)
        layout.addWidget(help_view)

        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(help_dialog.accept)
        layout.addWidget(close_btn)

        help_dialog.exec_()

    def setup_styles(self):
        self.style_sheet = '''
            /* Fenêtre principale */
            QMainWindow {
                background-color: #ffffff;
            }

            /* Boutons principaux */
            QPushButton {
                background-color: #40414f;
                color: white;
                border: 1px solid #565869;
                padding: 8px 15px;
                border-radius: 5px;
                min-width: 80px;
            }

            QPushButton\:hover {
                background-color: #565869;
            }

            QPushButton\:pressed {
                background-color: #40414f;
            }

            /* Boutons d'action */
            QPushButton.action-primary {
                background-color: #10a37f;
                border: 1px solid #0d8a6a;
            }

            QPushButton.action-primary\:hover {
                background-color: #1a7f64;
            }

            QPushButton.action-danger {
                background-color: #ef4146;
                border: 1px solid #d9393e;
            }

            QPushButton.action-danger\:hover {
                background-color: #c13539;
            }

            QPushButton.action-secondary {
                background-color: #565869;
                border: 1px solid #40414f;
            }

            /* Champs de texte */
            QLineEdit, QTextEdit, QComboBox {
                background-color: #ffffff;
                color: black;
                border: 1px solid #565869;
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #10a37f;
            }

            QTextEdit {
                padding: 12px;
            }

            /* Listes */
            QListWidget {
                background-color: #ffffff;
                color: black;
                border: none;
                outline: 0;
            }

            QListWidget::item {
                padding: 12px 15px;
                border-bottom: 1px solid #e0e0e0;
            }

            QListWidget::item\:hover {
                background-color: #f0f0f0;
            }

            QListWidget::item\:selected {
                background-color: #e0e0e0;
            }

            /* Séparateurs */
            QFrame[frameShape="4"] { /* HLine */
                background-color: #565869;
                border: none;
                height: 1px;
            }

            /* Onglets */
            QTabWidget::pane {
                border: none;
            }

            QTabBar::tab {
                background-color: #ffffff;
                color: #acacbe;
                padding: 8px 15px;
                border: none;
                border-bottom: 2px solid transparent;
            }

            QTabBar::tab\:selected {
                color: black;
                border-bottom: 2px solid #10a37f;
            }

            QTabBar::tab\:hover {
                background-color: #f0f0f0;
            }

            /* Cases à cocher */
            QCheckBox {
                color: black;
                spacing: 8px;
            }

            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #565869;
                border-radius: 3px;
                background-color: #ffffff;
            }

            QCheckBox::indicator\:checked {
                background-color: #10a37f;
                image: url(:/qtwidgets/images/checkbox_checked.png);
            }

            /* Tooltip */
            QToolTip {
                background-color: #ffffff;
                color: black;
                border: 1px solid #565869;
                padding: 5px;
                border-radius: 3px;
            }
        '''
        self.setStyleSheet(self.style_sheet)
    def init_db(self):
        self.conn = sqlite3.connect(DB_PATH_prompts)
        self.cursor = self.conn.cursor()
        
        # Création des tables (inchangé)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                example TEXT,
                category_id INTEGER,
                is_favorite BOOLEAN DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompt_tags (
                prompt_id INTEGER,
                tag_id INTEGER,
                PRIMARY KEY (prompt_id, tag_id),
                FOREIGN KEY (prompt_id) REFERENCES prompts (id),
                FOREIGN KEY (tag_id) REFERENCES tags (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompt_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_id INTEGER,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                example TEXT,
                category_id INTEGER,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (prompt_id) REFERENCES prompts (id)
            )
        ''')
        
        # Vérifier si la base est vide
        self.cursor.execute("SELECT COUNT(*) FROM prompts")
        count = self.cursor.fetchone()[0]
        
        if count == 0:
            self.insert_default_data()
        
        self.conn.commit()

    def insert_default_data(self):
        """Insérer des données par défaut dans la base de données"""
        now = datetime.now().isoformat()
        
        # Catégories par défaut
        default_categories = [
            ("Général", now),
            ("Programmation", now),
            ("Rédaction", now),
            ("Analyse", now)
        ]
        
        self.cursor.executemany(
            "INSERT INTO categories (name, created_at) VALUES (?, ?)",
            default_categories
        )
        
        # Tags par défaut
        default_tags = [
            ("important", "#ef4146", now),
            ("documentation", "#10a37f", now),
            ("code", "#5436DA", now),
            ("creative", "#F4A950", now)
        ]
        
        self.cursor.executemany(
            "INSERT INTO tags (name, color, created_at) VALUES (?, ?, ?)",
            default_tags
        )
        
        # Prompts par défaut
        default_prompts = [
            (
                "Corriger les fautes", 
                "Corrige les fautes d'orthographe et de grammaire dans le texte suivant :\n\n[INSÉRER TEXTE]",
                "Texte avant :\n\"Sa va bien ?\"\n\nTexte après :\n\"Ça va bien ?\"",
                2,  # ID de catégorie Rédaction
                0,  # Non favori
                now,
                now
            ),
            (
                "Expliquer un concept", 
                "Explique le concept suivant de manière simple et concise :\n\n[CONCEPT À EXPLIQUER]",
                "Concept : Machine Learning\n\nExplication : Le machine learning est une branche de l'intelligence artificielle qui permet aux ordinateurs d'apprendre à partir de données sans être explicitement programmés.",
                1,  # ID de catégorie Général
                1,  # Favori
                now,
                now
            ),
            (
                "Générer du code Python", 
                "Écris une fonction Python qui [DESCRIPTION DE LA FONCTION]. Inclus des docstrings et des exemples d'utilisation.",
                "Description : \"une fonction qui calcule la factorielle d'un nombre\"\n\nRéponse :\n```python\ndef factorial(n):\n    \"\"\"Calculate the factorial of a number.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)\n```",
                2,  # ID de catégorie Programmation
                1,  # Favori
                now,
                now
            )
        ]
        
        self.cursor.executemany(
            "INSERT INTO prompts (title, content, example, category_id, is_favorite, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            default_prompts
        )
        
        # Associations tags-prompts
        prompt_tags = [
            (1, 1),  # Prompt 1 (Corriger) -> Tag important
            (2, 2),  # Prompt 2 (Expliquer) -> Tag documentation
            (3, 3),  # Prompt 3 (Python) -> Tag code
            (3, 1)   # Prompt 3 (Python) -> Tag important
        ]
        
        self.cursor.executemany(
            "INSERT INTO prompt_tags (prompt_id, tag_id) VALUES (?, ?)",
            prompt_tags
        )
    def init_db1(self):
        self.conn = sqlite3.connect(DB_PATH_prompts)
        self.cursor = self.conn.cursor()

        # Création des tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT,
                created_at TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                example TEXT,
                category_id INTEGER,
                is_favorite BOOLEAN DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompt_tags (
                prompt_id INTEGER,
                tag_id INTEGER,
                PRIMARY KEY (prompt_id, tag_id),
                FOREIGN KEY (prompt_id) REFERENCES prompts (id),
                FOREIGN KEY (tag_id) REFERENCES tags (id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompt_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_id INTEGER,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                example TEXT,
                category_id INTEGER,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (prompt_id) REFERENCES prompts (id)
            )
        ''')

        self.conn.commit()

    def create_ui(self):
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout principal
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Splitter pour diviser la fenêtre
        splitter = QSplitter(Qt.Horizontal)

        # Panel gauche (liste des prompts)
        left_panel = QWidget()
        left_panel.setObjectName("leftPanel")
        left_panel.setStyleSheet("#leftPanel { background-color: #ffffff; }")
        left_panel_layout = QVBoxLayout(left_panel)
        left_panel_layout.setContentsMargins(10, 10, 10, 10)
        left_panel_layout.setSpacing(10)

        # Bouton nouveau prompt
        self.new_prompt_btn = QPushButton("+ Nouveau prompt")
        self.new_prompt_btn.setObjectName("newPromptBtn")
        self.new_prompt_btn.setStyleSheet('''
            #newPromptBtn {
                background-color: #10a37f;
                padding: 12px;
                font-weight: bold;
                text-align: center;
            }
            #newPromptBtn\:hover {
                background-color: #1a7f64;
            }
        ''')
        self.new_prompt_btn.clicked.connect(self.add_new_prompt)
        left_panel_layout.addWidget(self.new_prompt_btn)

        # Barre de recherche
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher des prompts...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        left_panel_layout.addWidget(self.search_input)

        # Filtres
        filter_tabs = QTabWidget()
        filter_tabs.setDocumentMode(True)

        # Onglet Catégories
        category_tab = QWidget()
        category_layout = QVBoxLayout(category_tab)

        self.category_filter = QComboBox()
        self.category_filter.addItem("Toutes les catégories")
        self.category_filter.currentIndexChanged.connect(self.load_prompts)
        category_layout.addWidget(QLabel("Filtrer par catégorie:"))
        category_layout.addWidget(self.category_filter)

        self.favorites_only = QCheckBox("Favoris seulement")
        self.favorites_only.stateChanged.connect(self.load_prompts)
        category_layout.addWidget(self.favorites_only)

        category_layout.addStretch()
        filter_tabs.addTab(category_tab, "Catégories")

        # Onglet Tags
        tags_tab = QWidget()
        tags_layout = QVBoxLayout(tags_tab)

        self.tags_filter = QComboBox()
        self.tags_filter.addItem("Tous les tags")
        self.tags_filter.currentIndexChanged.connect(self.load_prompts)
        tags_layout.addWidget(QLabel("Filtrer par tag:"))
        tags_layout.addWidget(self.tags_filter)

        tags_layout.addStretch()
        filter_tabs.addTab(tags_tab, "Tags")

        left_panel_layout.addWidget(filter_tabs)

        # Liste des prompts
        self.prompts_list = QListWidget()
        self.prompts_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.prompts_list.customContextMenuRequested.connect(self.show_prompt_context_menu)
        self.prompts_list.itemClicked.connect(self.display_prompt)
        left_panel_layout.addWidget(self.prompts_list, 1)

        # Panel droit (détails du prompt)
        right_panel = QWidget()
        right_panel.setObjectName("rightPanel")
        right_panel.setStyleSheet("#rightPanel { background-color: #ffffff; }")
        right_panel_layout = QVBoxLayout(right_panel)
        right_panel_layout.setContentsMargins(20, 20, 20, 20)
        right_panel_layout.setSpacing(15)

        # En-tête du prompt
        header_layout = QHBoxLayout()

        self.favorite_btn = QPushButton()
        self.favorite_btn.setCheckable(True)
        self.favorite_btn.setFixedSize(30, 30)
        self.favorite_btn.setToolTip("Marquer comme favori")
        self.favorite_btn.clicked.connect(self.toggle_favorite)
        header_layout.addWidget(self.favorite_btn)

        self.prompt_title = QLabel("Sélectionnez un prompt")
        self.prompt_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(self.prompt_title, 1)

        right_panel_layout.addLayout(header_layout)

        # Onglets de contenu
        content_tabs = QTabWidget()
        content_tabs.setDocumentMode(True)

        # Onglet Prompt
        prompt_tab = QWidget()
        prompt_layout = QVBoxLayout(prompt_tab)

        self.prompt_content = QTextEdit()
        self.prompt_content.setReadOnly(True)
        prompt_layout.addWidget(self.prompt_content, 1)

        content_tabs.addTab(prompt_tab, "Prompt")

        # Onglet Exemple
        example_tab = QWidget()
        example_layout = QVBoxLayout(example_tab)

        self.prompt_example = QTextEdit()
        self.prompt_example.setReadOnly(True)
        example_layout.addWidget(self.prompt_example, 1)

        content_tabs.addTab(example_tab, "Exemple")

        # Onglet Historique
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)

        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.display_history_version)
        history_layout.addWidget(self.history_list)

        self.restore_version_btn = QPushButton("Restaurer cette version")
        self.restore_version_btn.setObjectName("action-primary")
        self.restore_version_btn.clicked.connect(self.restore_history_version)
        history_layout.addWidget(self.restore_version_btn)

        content_tabs.addTab(history_tab, "Historique")

        right_panel_layout.addWidget(content_tabs, 1)

        # Tags du prompt
        self.tags_container = QWidget()
        tags_container_layout = QHBoxLayout(self.tags_container)
        tags_container_layout.setContentsMargins(0, 0, 0, 0)
        tags_container_layout.setSpacing(5)

        tags_label = QLabel("Tags:")
        tags_container_layout.addWidget(tags_label)

        self.tags_layout = QHBoxLayout()
        self.tags_layout.setSpacing(5)
        tags_container_layout.addLayout(self.tags_layout, 1)
        tags_container_layout.addStretch()

        self.add_tag_btn = QPushButton("+")
        self.add_tag_btn.setFixedSize(25, 25)
        self.add_tag_btn.clicked.connect(self.show_add_tag_dialog)
        tags_container_layout.addWidget(self.add_tag_btn)

        right_panel_layout.addWidget(self.tags_container)

        # Boutons d'action
        button_layout = QHBoxLayout()

        self.edit_btn = QPushButton("Modifier")
        self.edit_btn.setObjectName("action-primary")
        self.edit_btn.clicked.connect(self.edit_prompt)
        button_layout.addWidget(self.edit_btn)

        self.export_btn = QPushButton("Exporter")
        self.export_btn.setObjectName("action-secondary")
        self.export_btn.clicked.connect(self.export_prompt)
        button_layout.addWidget(self.export_btn)

        self.delete_btn = QPushButton("Supprimer")
        self.delete_btn.setObjectName("action-danger")
        self.delete_btn.clicked.connect(self.delete_prompt)
        button_layout.addWidget(self.delete_btn)

        right_panel_layout.addLayout(button_layout)

        # Ajouter les panels au splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])

        main_layout.addWidget(splitter)

        # Mettre à jour l'état des boutons
        self.update_buttons_state()

    def on_search_text_changed(self):
        self.search_delay_timer.stop()
        self.search_delay_timer.start(500)  # Délai de 500ms avant la recherche

    def show_prompt_context_menu(self, position):
        if not self.prompts_list.itemAt(position):
            return

        menu = QMenu()

        export_action = QAction("Exporter", self)
        export_action.triggered.connect(self.export_prompt)
        menu.addAction(export_action)

        duplicate_action = QAction("Dupliquer", self)
        duplicate_action.triggered.connect(self.duplicate_prompt)
        menu.addAction(duplicate_action)

        menu.addSeparator()

        delete_action = QAction("Supprimer", self)
        delete_action.triggered.connect(self.delete_prompt)
        menu.addAction(delete_action)

        menu.exec_(self.prompts_list.mapToGlobal(position))

    def update_buttons_state(self):
        has_selection = bool(self.prompts_list.selectedItems())

        self.edit_btn.setEnabled(has_selection)
        self.export_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        self.favorite_btn.setEnabled(has_selection)
        self.add_tag_btn.setEnabled(has_selection)

        if has_selection:
            prompt_id = self.prompts_list.currentItem().data(Qt.UserRole)
            self.cursor.execute("SELECT is_favorite FROM prompts WHERE id = ?", (prompt_id,))
            is_favorite = self.cursor.fetchone()[0]
            self.favorite_btn.setChecked(is_favorite)

            if is_favorite:
                self.favorite_btn.setStyleSheet("background-color: gold; border: none;")
                self.favorite_btn.setToolTip("Retirer des favoris")
            else:
                self.favorite_btn.setStyleSheet("background-color: #ffffff; border: 1px solid #565869;")
                self.favorite_btn.setToolTip("Ajouter aux favoris")

    def load_categories(self):
        self.category_filter.clear()
        self.category_filter.addItem("Toutes les catégories")

        self.cursor.execute("SELECT name FROM categories ORDER BY name")
        categories = self.cursor.fetchall()

        for category in categories:
            self.category_filter.addItem(category[0])

    def load_tags(self):
        self.tags_filter.clear()
        self.tags_filter.addItem("Tous les tags")

        self.cursor.execute("SELECT name FROM tags ORDER BY name")
        tags = self.cursor.fetchall()

        for tag in tags:
            self.tags_filter.addItem(tag[0])

    def load_prompts(self):
        self.prompts_list.clear()

        search_text = self.search_input.text().strip()
        category = self.category_filter.currentText() if self.category_filter.currentText() != "Toutes les catégories" else None
        tag = self.tags_filter.currentText() if self.tags_filter.currentText() != "Tous les tags" else None
        favorites_only = self.favorites_only.isChecked()

        query = '''
            SELECT DISTINCT p.id, p.title, c.name, p.is_favorite
            FROM prompts p
            LEFT JOIN categories c ON p.category_id = c.id
            LEFT JOIN prompt_tags pt ON p.id = pt.prompt_id
            LEFT JOIN tags t ON pt.tag_id = t.id
            WHERE 1=1
        '''

        params = []

        if search_text:
            query += " AND (p.title LIKE ? OR p.content LIKE ?)"
            params.extend([f"%{search_text}%", f"%{search_text}%"])

        if category:
            query += " AND c.name = ?"
            params.append(category)

        if tag:
            query += " AND t.name = ?"
            params.append(tag)

        if favorites_only:
            query += " AND p.is_favorite = 1"

        query += " ORDER BY p.title"

        self.cursor.execute(query, params)
        prompts = self.cursor.fetchall()

        for prompt in prompts:
            item_text = prompt[1]
            if prompt[2]:
                item_text += f" ({prompt[2]})"

            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, prompt[0])

            if prompt[3]:  # is_favorite
                item.setIcon(QIcon(":/icons/star_filled.png"))

            self.prompts_list.addItem(item)

    def display_prompt(self):
        selected_items = self.prompts_list.selectedItems()
        if not selected_items:
            return

        prompt_id = selected_items[0].data(Qt.UserRole)
        self.current_prompt_id = prompt_id

        self.cursor.execute('''
            SELECT p.title, p.content, p.example, c.name, p.is_favorite
            FROM prompts p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.id = ?
        ''', (prompt_id,))

        prompt = self.cursor.fetchone()

        if prompt:
            self.prompt_title.setText(prompt[0])

            # Convertir le markdown en HTML si nécessaire
            html_content = self.markdown_to_html(prompt[1])
            self.prompt_content.setHtml(html_content)

            html_example = self.markdown_to_html(prompt[2]) if prompt[2] else "<i>Aucun exemple disponible</i>"
            self.prompt_example.setHtml(html_example)

            # Charger les tags
            self.load_prompt_tags(prompt_id)

            # Charger l'historique
            self.load_prompt_history(prompt_id)

        self.update_buttons_state()

    def markdown_to_html(self, text):
        if not text:
            return ""

        # Convertir le markdown en HTML
        html = markdown.markdown(text)

        # Utiliser BeautifulSoup pour nettoyer et formater
        soup = BeautifulSoup(html, 'html.parser')

        # Ajouter des styles pour les blocs de code
        for pre in soup.find_all('pre'):
            pre['style'] = 'background-color: #40414f; padding: 10px; border-radius: 5px;'

        return str(soup)

    def load_prompt_tags(self, prompt_id):
        # Nettoyer les tags précédents
        for i in reversed(range(self.tags_layout.count())):
            self.tags_layout.itemAt(i).widget().setParent(None)

        self.cursor.execute('''
            SELECT t.id, t.name, t.color
            FROM tags t
            JOIN prompt_tags pt ON t.id = pt.tag_id
            WHERE pt.prompt_id = ?
        ''', (prompt_id,))

        tags = self.cursor.fetchall()

        for tag in tags:
            tag_id, name, color = tag

            tag_btn = QPushButton(name)
            tag_btn.setObjectName("tagButton")
            tag_btn.setCursor(Qt.PointingHandCursor)

            if color:
                tag_btn.setStyleSheet(f'''
                    #tagButton {{
                        background-color: {color};
                        color: white;
                        border: none;
                        padding: 3px 8px;
                        border-radius: 10px;
                        font-size: 11px;
                    }}
                ''')
            else:
                tag_btn.setStyleSheet('''
                    #tagButton {
                        background-color: #565869;
                        color: white;
                        border: none;
                        padding: 3px 8px;
                        border-radius: 10px;
                        font-size: 11px;
                    }
                ''')

            tag_btn.clicked.connect(lambda _, t=tag_id: self.remove_tag_from_prompt(t))
            self.tags_layout.addWidget(tag_btn)

    def load_prompt_history(self, prompt_id):
        self.history_list.clear()

        self.cursor.execute('''
            SELECT id, title, updated_at
            FROM prompt_history
            WHERE prompt_id = ?
            ORDER BY updated_at DESC
        ''', (prompt_id,))

        history = self.cursor.fetchall()

        for version in history:
            version_id, title, updated_at = version
            date_str = datetime.fromisoformat(updated_at).strftime("%d/%m/%Y %H:%M")
            item = QListWidgetItem(f"{date_str} - {title}")
            item.setData(Qt.UserRole, version_id)
            self.history_list.addItem(item)

    def show_add_tag_dialog(self):
        if not self.current_prompt_id:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter un tag")
        dialog.setFixedSize(300, 150)

        layout = QVBoxLayout(dialog)

        # Sélection de tag existant
        existing_tag_combo = QComboBox()
        existing_tag_combo.addItem("-- Sélectionner un tag existant --", None)

        self.cursor.execute("SELECT id, name FROM tags ORDER BY name")
        tags = self.cursor.fetchall()

        for tag_id, name in tags:
            existing_tag_combo.addItem(name, tag_id)

        layout.addWidget(existing_tag_combo)

        # Ou création d'un nouveau tag
        new_tag_layout = QHBoxLayout()

        new_tag_input = QLineEdit()
        new_tag_input.setPlaceholderText("Nouveau tag")
        new_tag_layout.addWidget(new_tag_input, 1)

        color_btn = QPushButton()
        color_btn.setFixedSize(30, 30)
        color_btn.setStyleSheet("background-color: #565869;")
        color_btn.clicked.connect(lambda: self.choose_tag_color(color_btn))
        new_tag_layout.addWidget(color_btn)

        layout.addLayout(new_tag_layout)

        # Boutons
        button_layout = QHBoxLayout()

        add_btn = QPushButton("Ajouter")
        add_btn.setObjectName("action-primary")
        add_btn.clicked.connect(lambda: self.add_tag_to_prompt(
            existing_tag_combo.currentData(),
            new_tag_input.text().strip(),
            color_btn.styleSheet().split(":")[1].split(";")[0].strip(),
            dialog
        ))
        button_layout.addWidget(add_btn)

        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("action-danger")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

        dialog.exec_()

    def choose_tag_color(self, button):
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()}; border: none;")

    def add_tag_to_prompt(self, existing_tag_id, new_tag_name, color, dialog):
        if not existing_tag_id and not new_tag_name:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un tag existant ou en créer un nouveau!")
            return

        tag_id = existing_tag_id

        if not existing_tag_id and new_tag_name:
            # Créer un nouveau tag
            try:
                now = datetime.now().isoformat()
                self.cursor.execute(
                    "INSERT INTO tags (name, color, created_at) VALUES (?, ?, ?)",
                    (new_tag_name, color, now)
                )
                tag_id = self.cursor.lastrowid
                self.conn.commit()

                # Mettre à jour les listes de tags
                self.load_tags()

            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Erreur", "Ce tag existe déjà!")
                return

        # Associer le tag au prompt
        try:
            self.cursor.execute(
                "INSERT INTO prompt_tags (prompt_id, tag_id) VALUES (?, ?)",
                (self.current_prompt_id, tag_id)
            )
            self.conn.commit()

            # Mettre à jour l'affichage
            self.load_prompt_tags(self.current_prompt_id)

            dialog.accept()

        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Erreur", "Ce tag est déjà associé à ce prompt!")

    def remove_tag_from_prompt(self, tag_id):
        reply = QMessageBox.question(
            self,
            'Confirmation',
            'Voulez-vous vraiment retirer ce tag du prompt?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.cursor.execute(
                "DELETE FROM prompt_tags WHERE prompt_id = ? AND tag_id = ?",
                (self.current_prompt_id, tag_id)
            )
            self.conn.commit()

            self.load_prompt_tags(self.current_prompt_id)

    def toggle_favorite(self):
        if not self.current_prompt_id:
            return

        is_favorite = self.favorite_btn.isChecked()

        self.cursor.execute(
            "UPDATE prompts SET is_favorite = ? WHERE id = ?",
            (1 if is_favorite else 0, self.current_prompt_id)
        )
        self.conn.commit()

        # Mettre à jour l'icône dans la liste
        for i in range(self.prompts_list.count()):
            item = self.prompts_list.item(i)
            if item.data(Qt.UserRole) == self.current_prompt_id:
                if is_favorite:
                    item.setIcon(QIcon(":/icons/star_filled.png"))
                else:
                    item.setIcon(QIcon())
                break

        self.update_buttons_state()

    def add_new_prompt(self):
        self.open_prompt_editor()

    def edit_prompt(self):
        if not self.current_prompt_id:
            return

        self.open_prompt_editor(self.current_prompt_id)

    def open_prompt_editor(self, prompt_id=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nouveau prompt" if not prompt_id else "Modifier le prompt")
        dialog.setMinimumSize(700, 600)

        layout = QVBoxLayout(dialog)

        # Titre
        title_label = QLabel("Titre:")
        self.editor_title = QLineEdit()
        layout.addWidget(title_label)
        layout.addWidget(self.editor_title)

        # Catégorie
        category_label = QLabel("Catégorie:")
        category_layout = QHBoxLayout()

        self.editor_category = QComboBox()
        self.editor_category.addItem("Sans catégorie", None)

        self.cursor.execute("SELECT id, name FROM categories ORDER BY name")
        categories = self.cursor.fetchall()

        for cat_id, name in categories:
            self.editor_category.addItem(name, cat_id)

        category_layout.addWidget(self.editor_category, 1)

        add_category_btn = QPushButton("+")
        add_category_btn.setFixedSize(30, 30)
        add_category_btn.clicked.connect(self.add_new_category)
        category_layout.addWidget(add_category_btn)

        layout.addWidget(category_label)
        layout.addLayout(category_layout)

        # Contenu
        content_label = QLabel("Contenu du prompt (Markdown supporté):")
        self.editor_content = QTextEdit()
        layout.addWidget(content_label)
        layout.addWidget(self.editor_content, 1)

        # Exemple
        example_label = QLabel("Exemple de sortie (Markdown supporté):")
        self.editor_example = QTextEdit()
        layout.addWidget(example_label)
        layout.addWidget(self.editor_example, 1)

        # Boutons
        button_layout = QHBoxLayout()

        save_btn = QPushButton("Enregistrer")
        save_btn.setObjectName("action-primary")
        save_btn.clicked.connect(lambda: self.save_prompt(prompt_id, dialog))
        button_layout.addWidget(save_btn)

        preview_btn = QPushButton("Aperçu")
        preview_btn.setObjectName("action-secondary")
        preview_btn.clicked.connect(self.show_preview)
        button_layout.addWidget(preview_btn)

        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("action-danger")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

        # Charger les données existantes si modification
        if prompt_id:
            self.cursor.execute('''
                SELECT title, content, example, category_id
                FROM prompts
                WHERE id = ?
            ''', (prompt_id,))

            prompt = self.cursor.fetchone()

            if prompt:
                self.editor_title.setText(prompt[0])
                self.editor_content.setPlainText(prompt[1])
                self.editor_example.setPlainText(prompt[2] if prompt[2] else "")

                if prompt[3]:
                    index = self.editor_category.findData(prompt[3])
                    if index >= 0:
                        self.editor_category.setCurrentIndex(index)

        dialog.exec_()

    def show_preview(self):
        preview_dialog = QDialog(self)
        preview_dialog.setWindowTitle("Aperçu du prompt")
        preview_dialog.setMinimumSize(600, 500)

        layout = QVBoxLayout(preview_dialog)

        tabs = QTabWidget()

        # Onglet Prompt
        prompt_tab = QWidget()
        prompt_layout = QVBoxLayout(prompt_tab)

        prompt_preview = QTextEdit()
        prompt_preview.setReadOnly(True)
        prompt_preview.setHtml(self.markdown_to_html(self.editor_content.toPlainText()))
        prompt_layout.addWidget(prompt_preview, 1)

        tabs.addTab(prompt_tab, "Prompt")

        # Onglet Exemple
        example_tab = QWidget()
        example_layout = QVBoxLayout(example_tab)

        example_preview = QTextEdit()
        example_preview.setReadOnly(True)
        example_preview.setHtml(self.markdown_to_html(self.editor_example.toPlainText()))
        example_layout.addWidget(example_preview, 1)

        tabs.addTab(example_tab, "Exemple")

        layout.addWidget(tabs)

        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(preview_dialog.accept)
        layout.addWidget(close_btn)

        preview_dialog.exec_()

    def save_prompt(self, prompt_id, dialog):
        title = self.editor_title.text().strip()
        content = self.editor_content.toPlainText().strip()
        example = self.editor_example.toPlainText().strip()
        category_id = self.editor_category.currentData()

        if not title or not content:
            QMessageBox.warning(self, "Erreur", "Le titre et le contenu sont obligatoires!")
            return

        now = datetime.now().isoformat()

        if prompt_id:
            # Sauvegarder la version actuelle dans l'historique
            self.cursor.execute('''
                INSERT INTO prompt_history (prompt_id, title, content, example, category_id, updated_at)
                SELECT id, title, content, example, category_id, updated_at
                FROM prompts
                WHERE id = ?
            ''', (prompt_id,))

            # Mettre à jour le prompt
            self.cursor.execute('''
                UPDATE prompts
                SET title = ?, content = ?, example = ?, category_id = ?, updated_at = ?
                WHERE id = ?
            ''', (title, content, example if example else None, category_id, now, prompt_id))

            self.conn.commit()

            QMessageBox.information(self, "Succès", "Prompt mis à jour avec succès!")
        else:
            # Créer un nouveau prompt
            self.cursor.execute('''
                INSERT INTO prompts (title, content, example, category_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, content, example if example else None, category_id, now, now))

            self.conn.commit()

            QMessageBox.information(self, "Succès", "Prompt créé avec succès!")

        # Recharger les données
        self.load_categories()
        self.load_prompts()

        dialog.accept()

    def add_new_category(self):
        name, ok = QInputDialog.getText(
            self,
            "Nouvelle catégorie",
            "Nom de la nouvelle catégorie:",
            QLineEdit.Normal
        )

        if ok and name:
            try:
                now = datetime.now().isoformat()
                self.cursor.execute(
                    "INSERT INTO categories (name, created_at) VALUES (?, ?)",
                    (name, now)
                )
                self.conn.commit()

                # Mettre à jour les combobox
                self.load_categories()

                # Sélectionner la nouvelle catégorie dans l'éditeur
                if hasattr(self, 'editor_category'):
                    index = self.editor_category.findText(name)
                    if index >= 0:
                        self.editor_category.setCurrentIndex(index)

            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Erreur", "Cette catégorie existe déjà!")

    def delete_prompt(self):
        selected_items = self.prompts_list.selectedItems()
        if not selected_items:
            return

        prompt_id = selected_items[0].data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            'Confirmation',
            'Êtes-vous sûr de vouloir supprimer ce prompt?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Supprimer les associations de tags d'abord
            self.cursor.execute("DELETE FROM prompt_tags WHERE prompt_id = ?", (prompt_id,))

            # Supprimer l'historique
            self.cursor.execute("DELETE FROM prompt_history WHERE prompt_id = ?", (prompt_id,))

            # Supprimer le prompt
            self.cursor.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
            self.conn.commit()

            # Recharger les données
            self.load_prompts()

            # Effacer l'affichage
            self.prompt_title.setText("Sélectionnez un prompt")
            self.prompt_content.clear()
            self.prompt_example.clear()
            self.current_prompt_id = None

            self.update_buttons_state()

    def export_prompt(self):
        if not self.current_prompt_id:
            return

        self.cursor.execute('''
            SELECT p.title, p.content, p.example, c.name,
                   GROUP_CONCAT(t.name, ', ') as tags
            FROM prompts p
            LEFT JOIN categories c ON p.category_id = c.id
            LEFT JOIN prompt_tags pt ON p.id = pt.prompt_id
            LEFT JOIN tags t ON pt.tag_id = t.id
            WHERE p.id = ?
            GROUP BY p.id
        ''', (self.current_prompt_id,))

        prompt = self.cursor.fetchone()

        if not prompt:
            return

        title, content, example, category, tags = prompt

        # Formater les données pour l'export
        prompt_data = {
            "title": title,
            "content": content,
            "example": example,
            "category": category,
            "tags": tags.split(", ") if tags else [],
            "exported_at": datetime.now().isoformat()
        }

        # Demander où sauvegarder le fichier
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter le prompt",
            f"{title.replace(' ', '_')}.json",
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(prompt_data, f, ensure_ascii=False, indent=2)

                QMessageBox.information(self, "Succès", "Prompt exporté avec succès!")
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de l'export: {str(e)}")

    def import_prompt(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Importer un prompt",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    prompt_data = json.load(f)

                # Ouvrir l'éditeur avec les données importées
                dialog = QDialog(self)
                dialog.setWindowTitle("Importer un prompt")
                dialog.setMinimumSize(700, 600)

                layout = QVBoxLayout(dialog)

                # Titre
                title_label = QLabel("Titre:")
                title_input = QLineEdit(prompt_data.get("title", ""))
                layout.addWidget(title_label)
                layout.addWidget(title_input)

                # Catégorie
                category_label = QLabel("Catégorie:")
                category_layout = QHBoxLayout()

                category_combo = QComboBox()
                category_combo.addItem("Sans catégorie", None)

                self.cursor.execute("SELECT id, name FROM categories ORDER BY name")
                categories = self.cursor.fetchall()

                for cat_id, name in categories:
                    category_combo.addItem(name, cat_id)

                if "category" in prompt_data and prompt_data["category"]:
                    index = category_combo.findText(prompt_data["category"])
                    if index >= 0:
                        category_combo.setCurrentIndex(index)

                category_layout.addWidget(category_combo, 1)

                add_category_btn = QPushButton("+")
                add_category_btn.setFixedSize(30, 30)
                add_category_btn.clicked.connect(self.add_new_category)
                category_layout.addWidget(add_category_btn)

                layout.addWidget(category_label)
                layout.addLayout(category_layout)

                # Contenu
                content_label = QLabel("Contenu du prompt:")
                content_input = QTextEdit(prompt_data.get("content", ""))
                layout.addWidget(content_label)
                layout.addWidget(content_input, 1)

                # Exemple
                example_label = QLabel("Exemple de sortie:")
                example_input = QTextEdit(prompt_data.get("example", ""))
                layout.addWidget(example_label)
                layout.addWidget(example_input, 1)

                # Tags (affichage seulement)
                if "tags" in prompt_data and prompt_data["tags"]:
                    tags_label = QLabel("Tags inclus dans l'import:")
                    layout.addWidget(tags_label)

                    tags_display = QLabel(", ".join(prompt_data["tags"]))
                    tags_display.setStyleSheet("color: #acacbe; font-style: italic;")
                    layout.addWidget(tags_display)

                # Boutons
                button_layout = QHBoxLayout()

                save_btn = QPushButton("Enregistrer")
                save_btn.setObjectName("action-primary")
                save_btn.clicked.connect(lambda: self.save_imported_prompt(
                    title_input.text(),
                    category_combo.currentData(),
                    content_input.toPlainText(),
                    example_input.toPlainText(),
                    prompt_data.get("tags", []),
                    dialog
                ))
                button_layout.addWidget(save_btn)

                cancel_btn = QPushButton("Annuler")
                cancel_btn.setObjectName("action-danger")
                cancel_btn.clicked.connect(dialog.reject)
                button_layout.addWidget(cancel_btn)

                layout.addLayout(button_layout)

                dialog.exec_()

            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de l'import: {str(e)}")

    def save_imported_prompt(self, title, category_id, content, example, tags, dialog):
        if not title or not content:
            QMessageBox.warning(self, "Erreur", "Le titre et le contenu sont obligatoires!")
            return

        now = datetime.now().isoformat()

        # Créer le prompt
        self.cursor.execute('''
            INSERT INTO prompts (title, content, example, category_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, content, example if example else None, category_id, now, now))

        prompt_id = self.cursor.lastrowid

        # Ajouter les tags
        if tags:
            for tag_name in tags:
                # Vérifier si le tag existe
                self.cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
                tag = self.cursor.fetchone()

                if not tag:
                    # Créer le tag s'il n'existe pas
                    self.cursor.execute(
                        "INSERT INTO tags (name, created_at) VALUES (?, ?)",
                        (tag_name, now)
                    )
                    tag_id = self.cursor.lastrowid
                else:
                    tag_id = tag[0]

                # Associer le tag au prompt
                try:
                    self.cursor.execute(
                        "INSERT INTO prompt_tags (prompt_id, tag_id) VALUES (?, ?)",
                        (prompt_id, tag_id)
                    )
                except sqlite3.IntegrityError:
                    pass  # L'association existe déjà

        self.conn.commit()

        # Recharger les données
        self.load_tags()
        self.load_prompts()

        dialog.accept()

        QMessageBox.information(self, "Succès", "Prompt importé avec succès!")

    def duplicate_prompt(self):
        if not self.current_prompt_id:
            return

        self.cursor.execute('''
            SELECT title, content, example, category_id
            FROM prompts
            WHERE id = ?
        ''', (self.current_prompt_id,))

        prompt = self.cursor.fetchone()

        if not prompt:
            return

        title, content, example, category_id = prompt

        # Créer une copie avec " (Copie)" ajouté au titre
        now = datetime.now().isoformat()
        new_title = f"{title} (Copie)"

        self.cursor.execute('''
            INSERT INTO prompts (title, content, example, category_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (new_title, content, example, category_id, now, now))

        new_prompt_id = self.cursor.lastrowid

        # Copier les tags
        self.cursor.execute('''
            INSERT INTO prompt_tags (prompt_id, tag_id)
            SELECT ?, tag_id FROM prompt_tags WHERE prompt_id = ?
        ''', (new_prompt_id, self.current_prompt_id))

        self.conn.commit()

        # Recharger les données
        self.load_prompts()

        QMessageBox.information(self, "Succès", "Prompt dupliqué avec succès!")

    def display_history_version(self):
        selected_items = self.history_list.selectedItems()
        if not selected_items:
            return

        version_id = selected_items[0].data(Qt.UserRole)

        self.cursor.execute('''
            SELECT title, content, example
            FROM prompt_history
            WHERE id = ?
        ''', (version_id,))

        version = self.cursor.fetchone()

        if version:
            self.prompt_title.setText(f"{version[0]} (version historique)")
            self.prompt_content.setHtml(self.markdown_to_html(version[1]))
            self.prompt_example.setHtml(self.markdown_to_html(version[2]) if version[2] else "<i>Aucun exemple disponible</i>")

    def restore_history_version(self):
        selected_items = self.history_list.selectedItems()
        if not selected_items or not self.current_prompt_id:
            return

        version_id = selected_items[0].data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            'Confirmation',
            'Voulez-vous vraiment restaurer cette version? La version actuelle sera sauvegardée dans l\'historique.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Sauvegarder la version actuelle dans l'historique
            self.cursor.execute('''
                INSERT INTO prompt_history (prompt_id, title, content, example, category_id, updated_at)
                SELECT id, title, content, example, category_id, updated_at
                FROM prompts
                WHERE id = ?
            ''', (self.current_prompt_id,))

            # Récupérer la version historique
            self.cursor.execute('''
                SELECT title, content, example, category_id
                FROM prompt_history
                WHERE id = ?
            ''', (version_id,))

            version = self.cursor.fetchone()

            if version:
                # Restaurer la version
                now = datetime.now().isoformat()
                self.cursor.execute('''
                    UPDATE prompts
                    SET title = ?, content = ?, example = ?, category_id = ?, updated_at = ?
                    WHERE id = ?
                ''', (*version, now, self.current_prompt_id))

                self.conn.commit()

                # Recharger les données
                self.load_prompts()
                self.display_prompt()

                QMessageBox.information(self, "Succès", "Version restaurée avec succès!")

    def setup_shortcuts(self):
        """Configurer les raccourcis clavier"""
        self.new_prompt_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.new_prompt_shortcut.activated.connect(self.add_new_prompt)

        self.search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.search_shortcut.activated.connect(lambda: self.search_input.setFocus())

        self.export_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        self.export_shortcut.activated.connect(self.export_prompt)

        self.delete_shortcut = QShortcut(QKeySequence("Del"), self)
        self.delete_shortcut.activated.connect(self.delete_prompt)

    def show_tag_manager(self):
        """Afficher le gestionnaire de tags"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Gestionnaire de Tags")
        dialog.setMinimumSize(400, 300)

        layout = QVBoxLayout(dialog)

        # Liste des tags
        self.all_tags_list = QListWidget()
        self.load_all_tags()
        layout.addWidget(self.all_tags_list)

        # Boutons d'action
        button_layout = QHBoxLayout()

        edit_btn = QPushButton("Modifier")
        edit_btn.setObjectName("action-secondary")
        edit_btn.clicked.connect(self.edit_tag)
        button_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Supprimer")
        delete_btn.setObjectName("action-danger")
        delete_btn.clicked.connect(self.delete_tag)
        button_layout.addWidget(delete_btn)

        layout.addLayout(button_layout)

        dialog.exec_()

    def load_all_tags(self):
        """Charger tous les tags dans la liste"""
        self.all_tags_list.clear()

        self.cursor.execute("SELECT id, name, color FROM tags ORDER BY name")
        tags = self.cursor.fetchall()

        for tag_id, name, color in tags:
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, tag_id)

            if color:
                item.setBackground(QColor(color))
                item.setForeground(QColor("white"))

            self.all_tags_list.addItem(item)

    def edit_tag(self):
        """Modifier un tag existant"""
        selected_items = self.all_tags_list.selectedItems()
        if not selected_items:
            return

        tag_id = selected_items[0].data(Qt.UserRole)

        self.cursor.execute("SELECT name, color FROM tags WHERE id = ?", (tag_id,))
        tag_name, color = self.cursor.fetchone()

        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier le Tag")
        dialog.setFixedSize(300, 150)

        layout = QVBoxLayout(dialog)

        # Nom du tag
        name_input = QLineEdit(tag_name)
        layout.addWidget(QLabel("Nom du tag:"))
        layout.addWidget(name_input)

        # Couleur
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Couleur:"))

        color_btn = QPushButton()
        color_btn.setFixedSize(30, 30)
        color_btn.setStyleSheet(f"background-color: {color if color else '#565869'};")
        color_btn.clicked.connect(lambda: self.choose_tag_color(color_btn))
        color_layout.addWidget(color_btn)

        layout.addLayout(color_layout)

        # Boutons
        btn_layout = QHBoxLayout()

        save_btn = QPushButton("Enregistrer")
        save_btn.setObjectName("action-primary")
        save_btn.clicked.connect(lambda: self.save_tag_changes(
            tag_id,
            name_input.text().strip(),
            color_btn.styleSheet().split(":")[1].split(";")[0].strip(),
            dialog
        ))
        btn_layout.addWidget(save_btn)

        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("action-danger")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

        dialog.exec_()

    def save_tag_changes(self, tag_id, new_name, new_color, dialog):
        """Sauvegarder les modifications d'un tag"""
        if not new_name:
            QMessageBox.warning(self, "Erreur", "Le nom du tag ne peut pas être vide!")
            return

        try:
            self.cursor.execute(
                "UPDATE tags SET name = ?, color = ? WHERE id = ?",
                (new_name, new_color, tag_id)
            )
            self.conn.commit()

            # Mettre à jour les affichages
            self.load_all_tags()
            self.load_tags()

            if self.current_prompt_id:
                self.load_prompt_tags(self.current_prompt_id)

            dialog.accept()

        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Erreur", "Un tag avec ce nom existe déjà!")

    def delete_tag(self):
        """Supprimer un tag"""
        selected_items = self.all_tags_list.selectedItems()
        if not selected_items:
            return

        tag_id = selected_items[0].data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            'Confirmation',
            'Voulez-vous vraiment supprimer ce tag? Cette action le retirera de tous les prompts.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Supprimer les associations d'abord
            self.cursor.execute("DELETE FROM prompt_tags WHERE tag_id = ?", (tag_id,))

            # Supprimer le tag
            self.cursor.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
            self.conn.commit()

            # Mettre à jour les affichages
            self.load_all_tags()
            self.load_tags()

            if self.current_prompt_id:
                self.load_prompt_tags(self.current_prompt_id)

    def show_stats(self):
        """Afficher les statistiques"""
        stats_dialog = QDialog(self)
        stats_dialog.setWindowTitle("Statistiques")
        stats_dialog.setFixedSize(400, 300)

        layout = QVBoxLayout(stats_dialog)

        # Récupérer les stats
        self.cursor.execute("SELECT COUNT(*) FROM prompts")
        total_prompts = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM categories")
        total_categories = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM tags")
        total_tags = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM prompts WHERE is_favorite = 1")
        total_favorites = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM prompt_history")
        total_versions = self.cursor.fetchone()[0]

        # Afficher les stats
        stats_html = f"""
        <style>
            body {{ font-family: Arial, sans-serif; color: black; }}
            h2 {{ color: #10a37f; margin-top: 0; }}
            .stat {{ margin-bottom: 10px; }}
            .stat-            name {{ font-weight: bold; color: #acacbe; }}
            .stat-value {{ color: black; }}
        </style>
        <body>
            <h2>Statistiques</h2>
            <div class="stat">
                <span class="stat-name">Prompts:</span>
                <span class="stat-value">{total_prompts}</span>
            </div>
            <div class="stat">
                <span class="stat-name">Catégories:</span>
                <span class="stat-value">{total_categories}</span>
            </div>
            <div class="stat">
                <span class="stat-name">Tags:</span>
                <span class="stat-value">{total_tags}</span>
            </div>
            <div class="stat">
                <span class="stat-name">Favoris:</span>
                <span class="stat-value">{total_favorites}</span>
            </div>
            <div class="stat">
                <span class="stat-name">Versions historiques:</span>
                <span class="stat-value">{total_versions}</span>
            </div>
        </body>
        """

        stats_view = QTextEdit()
        stats_view.setReadOnly(True)
        stats_view.setHtml(stats_html)
        layout.addWidget(stats_view)

        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(stats_dialog.accept)
        layout.addWidget(close_btn)

        stats_dialog.exec_()

    def backup_database(self):
        """Créer une sauvegarde de la base de données"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder la base de données",
            "prompts_backup.db",
            "Fichiers SQLite (*.db *.sqlite);;Tous les fichiers (*)",
            options=options
        )

        if file_path:
            try:
                # Fermer la connexion actuelle
                self.conn.close()

                # Copier le fichier
                import shutil
                shutil.copy2(DB_PATH_prompts, file_path)

                # Rouvrir la connexion
                self.conn = sqlite3.connect(DB_PATH_prompts)
                self.cursor = self.conn.cursor()

                QMessageBox.information(self, "Succès", "Sauvegarde créée avec succès!")
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de la sauvegarde: {str(e)}")
                # Rouvrir la connexion en cas d'erreur
                self.conn = sqlite3.connect(DB_PATH_prompts)
                self.cursor = self.conn.cursor()

    def restore_database(self):
        """Restaurer la base de données depuis une sauvegarde"""
        reply = QMessageBox.warning(
            self,
            "Attention",
            "Cette action écrasera votre base de données actuelle. Voulez-vous continuer?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Restaurer la base de données",
            "",
            "Fichiers SQLite (*.db *.sqlite);;Tous les fichiers (*)",
            options=options
        )

        if file_path:
            try:
                # Fermer la connexion actuelle
                self.conn.close()

                # Remplacer le fichier
                import shutil
                shutil.copy2(file_path, DB_PATH_prompts)

                # Rouvrir la connexion
                self.conn = sqlite3.connect(DB_PATH_prompts)
                self.cursor = self.conn.cursor()

                # Recharger les données
                self.load_categories()
                self.load_tags()
                self.load_prompts()

                QMessageBox.information(self, "Succès", "Base de données restaurée avec succès!")
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de la restauration: {str(e)}")
                # Rouvrir la connexion en cas d'erreur
                self.conn = sqlite3.connect(DB_PATH_prompts)
                self.cursor = self.conn.cursor()

    def setup_tray_icon(self):
        """Configurer l'icône de la barre système"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("prompt_icon.png"))

        tray_menu = QMenu()

        show_action = QAction("Ouvrir Prompt Genius", self)
        show_action.triggered.connect(self.show_normal)
        tray_menu.addAction(show_action)

        new_prompt_action = QAction("Nouveau Prompt", self)
        new_prompt_action.triggered.connect(self.add_new_prompt)
        tray_menu.addAction(new_prompt_action)

        tray_menu.addSeparator()

        quit_action = QAction("Quitter", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        """Gérer les clics sur l'icône de la barre système"""
        if reason == QSystemTrayIcon.Trigger:
            self.show_normal()

    def show_normal(self):
        """Afficher la fenêtre normalement"""
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.raise_()

    def closeEvent(self, event):
        """Gérer la fermeture de la fenêtre"""
        if self.tray_icon and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            self.conn.close()
            event.accept()

    def setup_auto_backup(self):
        """Configurer la sauvegarde automatique"""
        self.backup_timer = QTimer()
        self.backup_timer.timeout.connect(self.auto_backup)
        self.backup_timer.start(3600000)  # Toutes les heures

    def auto_backup(self):
        """Effectuer une sauvegarde automatique"""
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        backup_path = os.path.join(
            backup_dir,
            f"prompts_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.db"
        )

        try:
            # Fermer la connexion actuelle
            self.conn.close()

            # Créer la sauvegarde
            import shutil
            shutil.copy2(DB_PATH_prompts, backup_path)

            # Rouvrir la connexion
            self.conn = sqlite3.connect(DB_PATH_prompts)
            self.cursor = self.conn.cursor()

            # Garder seulement les 5 dernières sauvegardes
            backups = sorted(
                [f for f in os.listdir(backup_dir) if f.startswith('prompts_backup_')],
                reverse=True
            )
            for old_backup in backups[5:]:
                os.remove(os.path.join(backup_dir, old_backup))

        except Exception as e:
            print(f"Erreur lors de la sauvegarde automatique: {str(e)}")
            # Rouvrir la connexion en cas d'erreur
            self.conn = sqlite3.connect(DB_PATH_prompts)
            self.cursor = self.conn.cursor()

    def show_sync_dialog(self):
        """Afficher le dialogue de synchronisation"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Synchronisation")
        dialog.setFixedSize(400, 200)

        layout = QVBoxLayout(dialog)

        # Options de synchronisation
        self.sync_cloud = QCheckBox("Synchroniser avec le cloud")
        self.sync_cloud.setChecked(False)
        layout.addWidget(self.sync_cloud)

        self.sync_local = QCheckBox("Synchroniser avec un dossier local")
        self.sync_local.setChecked(False)
        layout.addWidget(self.sync_local)

        # Boutons
        button_layout = QHBoxLayout()

        sync_btn = QPushButton("Synchroniser")
        sync_btn.setObjectName("action-primary")
        sync_btn.clicked.connect(lambda: self.start_sync(dialog))
        button_layout.addWidget(sync_btn)

        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("action-danger")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

        dialog.exec_()

    def start_sync(self, dialog):
        """Démarrer la synchronisation"""
        if self.sync_cloud.isChecked():
            self.sync_with_cloud()

        if self.sync_local.isChecked():
            self.sync_with_local()

        QMessageBox.information(
            self,
            "Synchronisation",
            "Synchronisation terminée avec succès!"
        )
        dialog.accept()

    def sync_with_cloud(self):
        """Synchroniser avec le cloud (simulé)"""
        # En production, vous implémenteriez ici la logique réelle
        print("Synchronisation avec le cloud effectuée")

    def sync_with_local(self):
        """Synchroniser avec un dossier local"""
        options = QFileDialog.Options()
        folder = QFileDialog.getExistingDirectory(
            self,
            "Sélectionner le dossier de synchronisation",
            options=options
        )

        if folder:
            try:
                # Créer un fichier de synchronisation
                sync_file = os.path.join(folder, "prompts_sync.json")

                # Exporter tous les prompts
                self.cursor.execute('''
                    SELECT p.id, p.title, p.content, p.example, c.name,
                           GROUP_CONCAT(t.name, ', ') as tags
                    FROM prompts p
                    LEFT JOIN categories c ON p.category_id = c.id
                    LEFT JOIN prompt_tags pt ON p.id = pt.prompt_id
                    LEFT JOIN tags t ON pt.tag_id = t.id
                    GROUP BY p.id
                ''')

                prompts = []
                for row in self.cursor.fetchall():
                    prompt_id, title, content, example, category, tags = row
                    prompts.append({
                        "title": title,
                        "content": content,
                        "example": example,
                        "category": category,
                        "tags": tags.split(", ") if tags else []
                    })

                with open(sync_file, 'w', encoding='utf-8') as f:
                    json.dump({"prompts": prompts}, f, ensure_ascii=False, indent=2)

            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Erreur",
                    f"Erreur lors de la synchronisation: {str(e)}"
                )

    def setup_auto_complete(self):
        """Configurer l'auto-complétion pour la recherche"""
        completer = QCompleter()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)

        self.model = QStringListModel()
        completer.setModel(self.model)

        self.search_input.setCompleter(completer)

        # Mettre à jour la liste de complétion
        self.update_completer_model()

    def update_completer_model(self):
        """Mettre à jour le modèle de complétion"""
        self.cursor.execute("SELECT title FROM prompts")
        titles = [row[0] for row in self.cursor.fetchall()]

        self.cursor.execute("SELECT name FROM categories")
        categories = [row[0] for row in self.cursor.fetchall()]

        self.cursor.execute("SELECT name FROM tags")
        tags = [row[0] for row in self.cursor.fetchall()]

        all_items = titles + categories + tags
        self.model.setStringList(all_items)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Style global
    app.setStyleSheet('''
        QMainWindow {
            background-color: #ffffff;
        }
    ''')

    window = PromptManager()
    window.show()
    sys.exit(app.exec_())

