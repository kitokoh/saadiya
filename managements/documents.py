# -*- coding: utf-8 -*-
import sys
import os
import json
import sqlite3
import pandas as pd
import shutil
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget,
    QFileDialog, QMessageBox, QDialog, QFormLayout, QComboBox,
    QDialogButtonBox, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QHeaderView, QInputDialog, QSplitter,
    QCompleter, QTabWidget, QAction, QMenu, QToolBar
)
from PyQt5.QtGui import QIcon, QDesktopServices, QFont
from PyQt5.QtCore import Qt, QUrl, QStandardPaths, QSettings, QDir

# --- Configuration & Database ---
CONFIG_DIR_NAME = "ClientDocumentManager"
CONFIG_FILE_NAME = "config.json"
DATABASE_NAME = ""
TEMPLATES_SUBDIR = "templates"
CLIENTS_SUBDIR = "clients"
SPEC_TECH_TEMPLATE_NAME = "specification_technique_template.xlsx"
PROFORMA_TEMPLATE_NAME = "proforma_template.xlsx"
CONTRAT_VENTE_TEMPLATE_NAME = "contrat_vente_template.xlsx"
PACKING_LISTE_TEMPLATE_NAME = "packing_liste_template.xlsx"

# Determine application root directory
if getattr(sys, 'frozen', False):
    APP_ROOT_DIR = sys._MEIPASS
else:
    APP_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_TEMPLATES_DIR = os.path.join(APP_ROOT_DIR, TEMPLATES_SUBDIR)
DEFAULT_CLIENTS_DIR = os.path.join(APP_ROOT_DIR, CLIENTS_SUBDIR)

def get_config_dir():
    """Returns path to user-specific configuration directory."""
    config_dir_path = os.path.join(
        QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation), 
        CONFIG_DIR_NAME
    )
    os.makedirs(config_dir_path, exist_ok=True)
    return config_dir_path

def get_config_file_path():
    return os.path.join(get_config_dir(), CONFIG_FILE_NAME)

def init_database():
    DATABASE_NAME = os.path.join(get_config_dir(), "client_manag7er.db")
    
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Client Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Clients (
            client_id TEXT PRIMARY KEY,
            client_name TEXT NOT NULL,
            company_name TEXT,
            need TEXT,
            country TEXT,
            city TEXT,
            project_identifier TEXT NOT NULL,
            base_folder_path TEXT NOT NULL UNIQUE,
            status TEXT DEFAULT 'En cours',
            selected_languages TEXT 
        );
        """)
        
        # Countries Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Countries (
            country_id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_name TEXT NOT NULL UNIQUE
        );
        """)
        
        # Cities Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cities (
            city_id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_id INTEGER NOT NULL REFERENCES Countries(country_id),
            city_name TEXT NOT NULL,
            UNIQUE(country_id, city_name)
        );
        """)
        
        # Insert initial countries if empty
        cursor.execute("SELECT COUNT(*) FROM Countries")
        if cursor.fetchone()[0] == 0:
            initial_countries = [
                "France", "Sénégal", "Turquie", "Maroc", "Algérie", 
                "Allemagne", "Belgique", "Canada", "Suisse", 
                "Royaume-Uni", "États-Unis"
            ]
            for country in initial_countries:
                try:
                    cursor.execute("INSERT INTO Countries (country_name) VALUES (?)", (country,))
                except sqlite3.IntegrityError:
                    pass
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
        QMessageBox.critical(
            None, 
            "Erreur Base de Données", 
            f"Impossible d'initialiser la base de données: {e}\nL'application pourrait ne pas fonctionner correctement."
        )
    finally:
        if conn:
            conn.close()
    return DATABASE_NAME

DATABASE_NAME = init_database()

def load_config():
    config_path = get_config_file_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading config: {e}. Using defaults.")
    
    # Default configuration
    return {
        "templates_dir": DEFAULT_TEMPLATES_DIR,
        "clients_dir": DEFAULT_CLIENTS_DIR,
        "language": "fr"
    }

def save_config(config_data):
    try:
        config_path = get_config_file_path()
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        QMessageBox.warning(None, "Erreur de Configuration", f"Impossible d'enregistrer la configuration: {e}")

CONFIG = load_config()

# Ensure base directories exist
os.makedirs(CONFIG["templates_dir"], exist_ok=True)
os.makedirs(CONFIG["clients_dir"], exist_ok=True)

# --- Excel Editor Dialog ---
class ExcelEditor(QDialog):
    def __init__(self, file_path, client_data=None, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.client_data = client_data or {}
        self.setWindowTitle(f"Édition: {os.path.basename(file_path)}")
        self.setMinimumSize(900, 700)
        
        layout = QVBoxLayout(self)
        
        # Table widget for Excel data
        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_widget)
        
        # Button layout
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Enregistrer")
        self.save_button.setIcon(QIcon.fromTheme("document-save"))
        self.save_button.clicked.connect(self.save_data)
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.setIcon(QIcon.fromTheme("dialog-cancel"))
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.load_data()

    def load_data(self):
        try:
            # Read Excel file
            xls = pd.ExcelFile(self.file_path)
            
            if not xls.sheet_names:
                QMessageBox.warning(self, "Fichier Vide", "Le fichier Excel ne contient aucune feuille.")
                self.create_empty_table()
                return
                
            # Load first sheet by default
            self.loaded_sheet_name = xls.sheet_names[0]
            df = xls.parse(self.loaded_sheet_name)
            
            # Set up table dimensions
            self.table_widget.setRowCount(df.shape[0])
            self.table_widget.setColumnCount(df.shape[1])
            self.table_widget.setHorizontalHeaderLabels(df.columns.astype(str))
            
            # Populate table data
            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    cell_value = str(df.iat[i, j])
                    
                    # Replace placeholders with actual data
                    replacements = {
                        "{NOM_CLIENT}": self.client_data.get("Nom du client", ""),
                        "{BESOIN_CLIENT}": self.client_data.get("Besoin", ""),
                        "{DATE_CREATION}": datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    for placeholder, value in replacements.items():
                        cell_value = cell_value.replace(placeholder, value)
                    
                    item = QTableWidgetItem(cell_value)
                    self.table_widget.setItem(i, j, item)
                    
            self.table_widget.resizeColumnsToContents()
            
            # Show warning if multiple sheets
            if len(xls.sheet_names) > 1:
                QMessageBox.information(
                    self, 
                    "Fichier Multi-Feuilles",
                    f"Attention: Ce fichier contient plusieurs feuilles.\n"
                    f"Seule la première feuille ('{self.loaded_sheet_name}') est chargée pour édition.\n"
                    "Les autres feuilles seront préservées lors de la sauvegarde."
                )
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur de Lecture", f"Impossible de lire le fichier Excel:\n{e}")
            self.create_empty_table()

    def create_empty_table(self):
        self.table_widget.setRowCount(20)
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels([f"Colonne {i+1}" for i in range(6)])

    def save_data(self):
        try:
            # Create DataFrame from table data
            rows = self.table_widget.rowCount()
            cols = self.table_widget.columnCount()
            data = []
            
            # Get headers
            headers = []
            for j in range(cols):
                header_item = self.table_widget.horizontalHeaderItem(j)
                headers.append(header_item.text() if header_item else f"Colonne {j+1}")
            
            # Get cell data
            for i in range(rows):
                row_data = []
                for j in range(cols):
                    item = self.table_widget.item(i, j)
                    row_data.append(item.text() if item else "")
                data.append(row_data)
            
            df = pd.DataFrame(data, columns=headers)
            
            # Save to Excel file
            with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name=self.loaded_sheet_name or 'Sheet1')
            
            QMessageBox.information(self, "Succès", "Fichier sauvegardé avec succès.")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur de Sauvegarde", f"Impossible de sauvegarder le fichier:\n{e}")

# --- Client Widget ---
class ClientWidget(QWidget):
    def __init__(self, client_info, config, parent=None):
        super().__init__(parent)
        self.client_info = client_info
        self.config = config
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Client header
        header = QLabel(f"<h2>{self.client_info['name']}</h2>")
        header.setStyleSheet("color: #2c3e50;")
        layout.addWidget(header)
        
        # Client details
        details_layout = QFormLayout()
        details_layout.setLabelAlignment(Qt.AlignRight)
        
        details = [
            ("ID Projet:", self.client_info.get("project_identifier", "N/A")),
            ("Pays:", self.client_info.get("country", "N/A")),
            ("Ville:", self.client_info.get("city", "N/A")),
            ("Besoin Principal:", self.client_info.get("need", "N/A")),
            ("Chemin Dossier:", f"<a href='file:///{self.client_info['path']}'>{self.client_info['path']}</a>")
        ]
        
        for label, value in details:
            label_widget = QLabel(label)
            value_widget = QLabel(value)
            value_widget.setOpenExternalLinks(True)
            value_widget.setTextInteractionFlags(Qt.TextBrowserInteraction)
            details_layout.addRow(label_widget, value_widget)
        
        layout.addLayout(details_layout)
        
        # Document buttons
        docs_label = QLabel("<b>Actions sur les Documents:</b>")
        layout.addWidget(docs_label)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        docs = [
            ("Spéc. Technique", "document-new", "spec_technique"),
            ("Proforma", "document-new", "proforma"),
            ("Contrat de Vente", "document-new", "contrat_vente"),
            ("Packing Liste", "document-new", "packing_liste")
        ]
        
        for text, icon, doc_type in docs:
            btn = QPushButton(text)
            btn.setIcon(QIcon.fromTheme(icon))
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border-radius: 5px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            btn.clicked.connect(lambda checked, t=doc_type: self.open_document(t))
            buttons_layout.addWidget(btn)
        
        layout.addLayout(buttons_layout)
        
        # File browser
        files_label = QLabel("<b>Fichiers du Client:</b>")
        layout.addWidget(files_label)
        
        self.file_list = QListWidget()
        self.file_list.setAlternatingRowColors(True)
        self.file_list.itemDoubleClicked.connect(self.open_selected_file)
        layout.addWidget(self.file_list)
        
        refresh_btn = QPushButton("Actualiser Fichiers")
        refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        refresh_btn.clicked.connect(self.populate_file_list)
        layout.addWidget(refresh_btn)
        
        self.populate_file_list()

    def populate_file_list(self):
        self.file_list.clear()
        path = self.client_info["path"]
        
        if not os.path.exists(path):
            self.file_list.addItem("Dossier introuvable")
            return
            
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                display = f"{item} {'(Dossier)' if os.path.isdir(item_path) else ''}"
                self.file_list.addItem(display)
        except Exception as e:
            self.file_list.addItem(f"Erreur: {str(e)}")

    def open_selected_file(self, item):
        file_name = item.text().replace(" (Dossier)", "")
        file_path = os.path.join(self.client_info["path"], file_name)
        
        if os.path.exists(file_path):
            try:
                if file_path.lower().endswith('.xlsx'):
                    editor = ExcelEditor(file_path, self.client_info, self)
                    editor.exec_()
                else:
                    QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Impossible d'ouvrir le fichier:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Fichier Introuvable", "Le fichier n'existe plus.")
            self.populate_file_list()

    def open_document(self, doc_type):
        # Map document types to template names
        templates = {
            "spec_technique": SPEC_TECH_TEMPLATE_NAME,
            "proforma": PROFORMA_TEMPLATE_NAME,
            "contrat_vente": CONTRAT_VENTE_TEMPLATE_NAME,
            "packing_liste": PACKING_LISTE_TEMPLATE_NAME
        }
        
        if doc_type not in templates:
            QMessageBox.warning(self, "Type Inconnu", "Type de document non pris en charge")
            return
            
        template_name = templates[doc_type]
        doc_filename = f"{doc_type}.xlsx"
        client_data = {
            "Nom du client": self.client_info.get("name", ""),
            "Besoin": self.client_info.get("need", ""),
            "Pays Client": self.client_info.get("country", ""),
            "Ville Client": self.client_info.get("city", ""),
            "ID Projet": self.client_info.get("project_identifier", "")
        }
        
        # Determine languages
        languages = self.client_info.get("languages", ['fr'])
        created_files = []
        
        for lang in languages:
            lang_dir = os.path.join(self.client_info["path"], lang)
            os.makedirs(lang_dir, exist_ok=True)
            
            target_path = os.path.join(lang_dir, doc_filename)
            
            # Create document if doesn't exist
            if not os.path.exists(target_path):
                template_path = os.path.join(
                    self.config["templates_dir"], 
                    lang, 
                    template_name
                )
                
                if os.path.exists(template_path):
                    shutil.copy(template_path, target_path)
                    created_files.append(lang)
                else:
                    # Create empty Excel file if template not found
                    pd.DataFrame().to_excel(target_path)
                    created_files.append(f"{lang} (vide)")
        
        if created_files:
            QMessageBox.information(
                self, 
                "Documents Créés", 
                f"Document créé pour les langues: {', '.join(created_files)}"
            )
        
        # Open primary language document
        primary_path = os.path.join(
            self.client_info["path"], 
            languages[0], 
            doc_filename
        )
        
        if os.path.exists(primary_path):
            editor = ExcelEditor(primary_path, client_data, self)
            editor.exec_()
            self.populate_file_list()

# --- Main Window ---
class DocumentManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de Documents Client")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon.fromTheme("folder-documents"))
        
        self.config = CONFIG
        self.clients_data = {}
        
        self.setup_ui()
        self.create_actions()
        self.create_menus()
        self.load_clients_from_db()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Client management
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        # Client creation form
        form_group = QWidget()
        form_layout = QVBoxLayout(form_group)
        form_layout.addWidget(QLabel("<b>Nouveau Client</b>"))
        
        creation_form = QFormLayout()
        creation_form.setLabelAlignment(Qt.AlignRight)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom du client")
        creation_form.addRow("Nom Client:", self.name_input)
        
        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("Nom entreprise (optionnel)")
        creation_form.addRow("Nom Entreprise:", self.company_input)
        
        self.need_input = QLineEdit()
        self.need_input.setPlaceholderText("Besoin principal du client")
        creation_form.addRow("Besoin Client:", self.need_input)
        
        # Country selection
        country_layout = QHBoxLayout()
        self.country_combo = QComboBox()
        self.country_combo.setEditable(True)
        self.country_combo.setInsertPolicy(QComboBox.NoInsert)
        self.country_combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.country_combo.completer().setFilterMode(Qt.MatchContains)
        country_layout.addWidget(self.country_combo)
        
        self.add_country_btn = QPushButton("+")
        self.add_country_btn.setFixedSize(30, 30)
        self.add_country_btn.setToolTip("Ajouter un nouveau pays")
        self.add_country_btn.clicked.connect(self.add_new_country)
        country_layout.addWidget(self.add_country_btn)
        creation_form.addRow("Pays Client:", country_layout)
        
        # City selection
        city_layout = QHBoxLayout()
        self.city_combo = QComboBox()
        self.city_combo.setEditable(True)
        self.city_combo.setInsertPolicy(QComboBox.NoInsert)
        self.city_combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.city_combo.completer().setFilterMode(Qt.MatchContains)
        city_layout.addWidget(self.city_combo)
        
        self.add_city_btn = QPushButton("+")
        self.add_city_btn.setFixedSize(30, 30)
        self.add_city_btn.setToolTip("Ajouter une nouvelle ville")
        self.add_city_btn.clicked.connect(self.add_new_city)
        city_layout.addWidget(self.add_city_btn)
        creation_form.addRow("Ville Client:", city_layout)
        
        self.project_id_input = QLineEdit()
        self.project_id_input.setPlaceholderText("Identifiant unique du projet")
        creation_form.addRow("ID Projet:", self.project_id_input)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "Français uniquement (fr)",
            "Arabe uniquement (ar)",
            "Turc uniquement (tr)",
            "Toutes les langues (fr, ar, tr)"
        ])
        creation_form.addRow("Langues:", self.language_combo)
        
        self.create_client_btn = QPushButton("Créer Client")
        self.create_client_btn.setIcon(QIcon.fromTheme("list-add"))
        self.create_client_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.create_client_btn.clicked.connect(self.create_client)
        creation_form.addRow(self.create_client_btn)
        
        form_layout.addLayout(creation_form)
        left_layout.addWidget(form_group)
        
        # Client list
        left_layout.addWidget(QLabel("<b>Clients Existants</b>"))
        self.client_list = QListWidget()
        self.client_list.setAlternatingRowColors(True)
        self.client_list.itemClicked.connect(self.open_client_tab)
        self.client_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.client_list.customContextMenuRequested.connect(self.show_client_context_menu)
        left_layout.addWidget(self.client_list)
        
        splitter.addWidget(left_panel)
        
        # Right panel - Client tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        splitter.addWidget(self.tabs)
        
        splitter.setSizes([350, 650])
        
        # Load countries and cities
        self.load_countries()
        
    def create_actions(self):
        self.settings_action = QAction("Paramètres", self)
        self.settings_action.triggered.connect(self.open_settings)
        
        self.exit_action = QAction("Quitter", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)
        
    def create_menus(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("Fichier")
        file_menu.addAction(self.settings_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        
        help_menu = menu_bar.addMenu("Aide")
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def show_about(self):
        QMessageBox.about(
            self, 
            "À propos", 
            "<b>Gestionnaire de Documents Client</b><br><br>"
            "Version 2.0<br>"
            "Application de gestion de documents clients<br><br>"
            "Développé par Saadiya Management"
        )
        
    def load_countries(self):
        self.country_combo.clear()
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT country_name FROM Countries ORDER BY country_name")
            for country in cursor.fetchall():
                self.country_combo.addItem(country[0])
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Erreur DB", f"Erreur de chargement des pays:\n{str(e)}")
            
    def add_new_country(self):
        country, ok = QInputDialog.getText(
            self, 
            "Nouveau Pays", 
            "Entrez le nom du nouveau pays:"
        )
        
        if ok and country.strip():
            try:
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Countries (country_name) VALUES (?)", 
                    (country.strip(),)
                )
                conn.commit()
                self.load_countries()
                self.country_combo.setCurrentText(country.strip())
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Pays Existant", "Ce pays existe déjà dans la base de données.")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Erreur DB", f"Erreur d'ajout du pays:\n{str(e)}")
                
    def load_cities(self, country):
        self.city_combo.clear()
        if not country:
            return
            
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT city_name FROM Cities "
                "WHERE country_id = (SELECT country_id FROM Countries WHERE country_name = ?) "
                "ORDER BY city_name",
                (country,)
            )
            for city in cursor.fetchall():
                self.city_combo.addItem(city[0])
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Erreur DB", f"Erreur de chargement des villes:\n{str(e)}")
            
    def add_new_city(self):
        country = self.country_combo.currentText()
        if not country:
            QMessageBox.warning(self, "Pays Requis", "Veuillez d'abord sélectionner un pays.")
            return
            
        city, ok = QInputDialog.getText(
            self, 
            "Nouvelle Ville", 
            f"Entrez le nom de la nouvelle ville pour {country}:"
        )
        
        if ok and city.strip():
            try:
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                
                # Get country ID
                cursor.execute("SELECT country_id FROM Countries WHERE country_name = ?", (country,))
                country_id = cursor.fetchone()
                if not country_id:
                    QMessageBox.warning(self, "Pays Inconnu", "Pays sélectionné introuvable dans la base.")
                    return
                    
                # Insert new city
                cursor.execute(
                    "INSERT INTO Cities (country_id, city_name) VALUES (?, ?)", 
                    (country_id[0], city.strip())
                )
                conn.commit()
                self.load_cities(country)
                self.city_combo.setCurrentText(city.strip())
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Ville Existante", "Cette ville existe déjà pour ce pays.")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Erreur DB", f"Erreur d'ajout de la ville:\n{str(e)}")
                
    def generate_client_id(self):
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(client_id) FROM Clients")
            last_id = cursor.fetchone()[0]
            
            if last_id and last_id.startswith("C"):
                try:
                    num = int(last_id[1:]) + 1
                    return f"C{num:04d}"
                except ValueError:
                    pass
            return "C0001"
        except sqlite3.Error:
            return f"C{int(datetime.now().timestamp()) % 10000:04d}"
                
    def create_client(self):
        # Get form data
        name = self.name_input.text().strip()
        company = self.company_input.text().strip()
        need = self.need_input.text().strip()
        country = self.country_combo.currentText().strip()
        city = self.city_combo.currentText().strip()
        project_id = self.project_id_input.text().strip()
        lang_option = self.language_combo.currentText()
        
        # Validation
        if not name:
            QMessageBox.warning(self, "Nom Requis", "Le nom du client est obligatoire.")
            return
            
        if not country:
            QMessageBox.warning(self, "Pays Requis", "Le pays est obligatoire.")
            return
            
        if not project_id:
            QMessageBox.warning(self, "ID Projet Requis", "L'identifiant du projet est obligatoire.")
            return
            
        # Determine languages
        lang_map = {
            "Français uniquement (fr)": ["fr"],
            "Arabe uniquement (ar)": ["ar"],
            "Turc uniquement (tr)": ["tr"],
            "Toutes les langues (fr, ar, tr)": ["fr", "ar", "tr"]
        }
        languages = lang_map.get(lang_option, ["fr"])
        
        # Create folder name
        folder_name = f"{name}_{country}_{project_id}".replace(" ", "_")
        folder_path = os.path.join(self.config["clients_dir"], folder_name)
        
        # Check if folder already exists
        if os.path.exists(folder_path):
            QMessageBox.warning(self, "Dossier Existant", "Un dossier avec ce nom existe déjà.")
            return
            
        # Create client ID
        client_id = self.generate_client_id()
        
        # Save to database
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Clients (client_id, client_name, company_name, need, country, city, "
                "project_identifier, base_folder_path, selected_languages) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    client_id, name, company, need, country, city, 
                    project_id, folder_path, ",".join(languages)
                )
            )
            conn.commit()
            
            # Create folder structure
            os.makedirs(folder_path, exist_ok=True)
            for lang in languages:
                os.makedirs(os.path.join(folder_path, lang), exist_ok=True)
                
            # Update UI
            self.clients_data[name] = {
                "client_id": client_id,
                "name": name,
                "company_name": company,
                "need": need,
                "country": country,
                "city": city,
                "project_identifier": project_id,
                "path": folder_path,
                "languages": languages
            }
            
            self.client_list.addItem(name)
            
            # Clear form
            self.name_input.clear()
            self.company_input.clear()
            self.need_input.clear()
            self.project_id_input.clear()
            
            QMessageBox.information(
                self, 
                "Client Créé", 
                f"Client {name} créé avec succès.\nID: {client_id}\nDossier: {folder_path}"
            )
            
            # Open client tab
            self.open_client_tab_by_name(name)
            
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Client Existant", "Un client avec ce nom existe déjà.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur DB", f"Erreur de sauvegarde du client:\n{str(e)}")
        except OSError as e:
            QMessageBox.critical(self, "Erreur Dossier", f"Erreur de création du dossier:\n{str(e)}")
            
    def load_clients_from_db(self):
        self.clients_data.clear()
        self.client_list.clear()
        
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT client_id, client_name, company_name, need, country, city,
                       project_identifier, base_folder_path, selected_languages
                FROM Clients
                ORDER BY client_name
            """)
            
            for row in cursor.fetchall():
                name = row[1]
                self.clients_data[name] = {
                    "client_id": row[0],
                    "name": name,
                    "company_name": row[2],
                    "need": row[3],
                    "country": row[4],
                    "city": row[5],
                    "project_identifier": row[6],
                    "path": row[7],
                    "languages": row[8].split(',') if row[8] else ['fr']
                }
                self.client_list.addItem(name)
                
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur DB", f"Erreur de chargement des clients:\n{str(e)}")
            
    def open_client_tab(self, item):
        client_name = item.text()
        self.open_client_tab_by_name(client_name)
        
    def open_client_tab_by_name(self, client_name):
        # Check if tab already open
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == client_name:
                self.tabs.setCurrentIndex(i)
                return
                
        # Create new tab
        if client_name in self.clients_data:
            client_widget = ClientWidget(self.clients_data[client_name], self.config, self)
            tab_index = self.tabs.addTab(client_widget, client_name)
            self.tabs.setCurrentIndex(tab_index)
            
    def close_tab(self, index):
        widget = self.tabs.widget(index)
        if widget:
            widget.deleteLater()
        self.tabs.removeTab(index)
        
    def show_client_context_menu(self, pos):
        item = self.client_list.itemAt(pos)
        if not item:
            return
            
        client_name = item.text()
        menu = QMenu()
        
        open_action = menu.addAction("Ouvrir")
        open_action.triggered.connect(lambda: self.open_client_tab_by_name(client_name))
        
        open_folder_action = menu.addAction("Ouvrir le dossier")
        open_folder_action.triggered.connect(lambda: self.open_client_folder(client_name))
        
        menu.addSeparator()
        
        delete_action = menu.addAction("Supprimer")
        delete_action.triggered.connect(lambda: self.delete_client(client_name))
        
        menu.exec_(self.client_list.mapToGlobal(pos))
        
    def open_client_folder(self, client_name):
        if client_name in self.clients_data:
            path = self.clients_data[client_name]["path"]
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
            
    def delete_client(self, client_name):
        if client_name not in self.clients_data:
            return
            
        reply = QMessageBox.question(
            self,
            "Confirmer Suppression",
            f"Êtes-vous sûr de vouloir supprimer le client '{client_name}'?\n"
            "Cette action supprimera également le dossier client.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Remove from database
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM Clients WHERE client_name = ?", 
                    (client_name,)
                )
                conn.commit()
                
                # Remove folder
                path = self.clients_data[client_name]["path"]
                if os.path.exists(path):
                    shutil.rmtree(path)
                
                # Remove from UI
                del self.clients_data[client_name]
                
                # Find and remove from list
                for i in range(self.client_list.count()):
                    if self.client_list.item(i).text() == client_name:
                        self.client_list.takeItem(i)
                        break
                
                # Close tab if open
                for i in range(self.tabs.count()):
                    if self.tabs.tabText(i) == client_name:
                        self.tabs.removeTab(i)
                        break
                        
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Erreur DB", f"Erreur de suppression du client:\n{str(e)}")
            except OSError as e:
                QMessageBox.critical(self, "Erreur Dossier", f"Erreur de suppression du dossier:\n{str(e)}")
                
    def open_settings(self):
        dialog = SettingsDialog(self.config, self)
        if dialog.exec_() == QDialog.Accepted:
            new_config = dialog.get_config()
            self.config.update(new_config)
            save_config(self.config)
            
            # Update template and client directories
            os.makedirs(self.config["templates_dir"], exist_ok=True)
            os.makedirs(self.config["clients_dir"], exist_ok=True)
            
            QMessageBox.information(
                self, 
                "Paramètres Sauvegardés", 
                "Les nouveaux paramètres ont été enregistrés."
            )
            
    def closeEvent(self, event):
        save_config(self.config)
        super().closeEvent(event)

# --- Settings Dialog ---
class SettingsDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Paramètres de l'Application")
        self.setMinimumSize(500, 300)
        
        self.config = config
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        
        # Templates directory
        self.templates_input = QLineEdit(self.config["templates_dir"])
        templates_btn = QPushButton("Parcourir...")
        templates_btn.clicked.connect(lambda: self.browse_directory(self.templates_input))
        
        templates_layout = QHBoxLayout()
        templates_layout.addWidget(self.templates_input)
        templates_layout.addWidget(templates_btn)
        form.addRow("Dossier des Modèles:", templates_layout)
        
        # Clients directory
        self.clients_input = QLineEdit(self.config["clients_dir"])
        clients_btn = QPushButton("Parcourir...")
        clients_btn.clicked.connect(lambda: self.browse_directory(self.clients_input))
        
        clients_layout = QHBoxLayout()
        clients_layout.addWidget(self.clients_input)
        clients_layout.addWidget(clients_btn)
        form.addRow("Dossier des Clients:", clients_layout)
        
        # Language selection
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Français (fr)", "Arabe (ar)", "Turc (tr)"])
        
        lang_map = {"fr": "Français (fr)", "ar": "Arabe (ar)", "tr": "Turc (tr)"}
        self.lang_combo.setCurrentText(lang_map.get(self.config.get("language", "fr"), "fr"))
        form.addRow("Langue Interface:", self.lang_combo)
        
        layout.addLayout(form)
        
        # Button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def browse_directory(self, line_edit):
        path = QFileDialog.getExistingDirectory(
            self, 
            "Sélectionner un dossier", 
            line_edit.text()
        )
        if path:
            line_edit.setText(path)
            
    def get_config(self):
        lang_map = {
            "Français (fr)": "fr",
            "Arabe (ar)": "ar",
            "Turc (tr)": "tr"
        }
        
        return {
            "templates_dir": self.templates_input.text(),
            "clients_dir": self.clients_input.text(),
            "language": lang_map.get(self.lang_combo.currentText(), "fr")
        }

# --- Main Function ---
def main():
    # Enable High DPI scaling
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("ClientDocManager")
    app.setStyle("Fusion")
    
    # Create default templates if needed
    templates_dir = CONFIG["templates_dir"]
    for lang in ["fr", "ar", "tr"]:
        lang_dir = os.path.join(templates_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)
        
        # Create sample templates
        templates = {
            SPEC_TECH_TEMPLATE_NAME: pd.DataFrame({
                'Section': ["Informations Client", "", "Détails Techniques"],
                'Champ': ["Nom:", "Besoin:", "Exigence:"],
                'Valeur': ["{NOM_CLIENT}", "{BESOIN_CLIENT}", ""]
            }),
            PROFORMA_TEMPLATE_NAME: pd.DataFrame({
                'Article': ["Produit 1", "Produit 2"],
                'Quantité': [1, 2],
                'Prix Unitaire': [100.00, 50.00],
                'Total': [100.00, 100.00]
            }),
            CONTRAT_VENTE_TEMPLATE_NAME: pd.DataFrame({
                'Clause': ["Parties", "Objet", "Prix"],
                'Description': [
                    "Vendeur: ...\nAcheteur: {NOM_CLIENT}",
                    "Vente de ...",
                    "{PRIX_TOTAL} €"
                ]
            }),
            PACKING_LISTE_TEMPLATE_NAME: pd.DataFrame({
                'Colis': [1, 2],
                'Description': ["Ordinateurs", "Accessoires"],
                'Quantité': [5, 10],
                'Poids (kg)': [25.5, 5.2]
            })
        }
        
        for template_name, df in templates.items():
            template_path = os.path.join(lang_dir, template_name)
            if not os.path.exists(template_path):
                try:
                    df.to_excel(template_path, index=False)
                except Exception as e:
                    print(f"Erreur création template {template_name}: {str(e)}")
    
    window = DocumentManager()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

