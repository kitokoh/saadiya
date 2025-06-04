# -*- coding: utf-8 -*-
import sys
import os
import json
import sqlite3
import pandas as pd
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget,
    QFileDialog, QMessageBox, QDialog, QFormLayout, QComboBox,
    QDialogButtonBox, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QHeaderView, QInputDialog, QSplitter,
    QCompleter, QTabWidget, QAction, QMenu, QToolBar, QGroupBox,
    QCheckBox, QDateEdit, QSpinBox, QStackedWidget, QListWidgetItem,
    QStyledItemDelegate, QStyle, QStyleOptionViewItem, QGridLayout
)
from PyQt5.QtGui import QIcon, QDesktopServices, QFont, QColor, QBrush
from PyQt5.QtCore import Qt, QUrl, QStandardPaths, QSettings, QDir, QDate, QTimer
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
import io
from PyQt5.QtWidgets import QDoubleSpinBox

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
    DATABASE_NAME = os.path.join(get_config_dir(), "client_managessr.db")
    
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
            selected_languages TEXT,
            price REAL DEFAULT 0,
            notes TEXT,
            creation_date TEXT,
            last_modified TEXT,
            category TEXT DEFAULT 'Standard',
            primary_contact TEXT
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
        
        # Contacts Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Contacts (
            contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT NOT NULL REFERENCES Clients(client_id),
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            position TEXT,
            is_primary INTEGER DEFAULT 0
        );
        """)
        
        # Templates Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Templates (
            template_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            file_name TEXT NOT NULL,
            language TEXT NOT NULL,
            is_default INTEGER DEFAULT 0,
            category TEXT
        );
        """)
        
        # Status Settings
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS StatusSettings (
            status_id INTEGER PRIMARY KEY AUTOINCREMENT,
            status_name TEXT NOT NULL UNIQUE,
            default_days INTEGER NOT NULL,
            color TEXT
        );
        """)
            # Ajout de la table Produits
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT NOT NULL REFERENCES Clients(client_id),
            name TEXT NOT NULL,
            description TEXT,
            specifications TEXT,
            quantity INTEGER DEFAULT 1,
            unit_price REAL,
            total_price REAL
        );
        """)
        # Insert initial countries if empty
        cursor.execute("SELECT COUNT(*) FROM Countries")
        if cursor.fetchone()[0] == 0:
            initial_countries = [
                "France", "IRAK", "Turquie", "Maroc", "Algérie", 
                "Allemagne", "Belgique", "Canada", "Suisse", 
                "Royaume-Uni", "États-Unis"
            ]
            for country in initial_countries:
                try:
                    cursor.execute("INSERT INTO Countries (country_name) VALUES (?)", (country,))
                except sqlite3.IntegrityError:
                    pass
        
        # Insert default statuses
        cursor.execute("SELECT COUNT(*) FROM StatusSettings")
        if cursor.fetchone()[0] == 0:
            statuses = [
                ("En cours", 30, "#3498db"),
                ("Archivé", 365, "#95a5a6"),
                ("Urgent", 7, "#e74c3c"),
                ("Complété", 0, "#2ecc71"),
                ("En attente", 15, "#f39c12")
            ]
            for status in statuses:
                cursor.execute(
                    "INSERT INTO StatusSettings (status_name, default_days, color) VALUES (?, ?, ?)",
                    status
                )
        
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
        "language": "fr",
        "smtp_server": "",
        "smtp_port": 587,
        "smtp_user": "",
        "smtp_password": "",
        "default_reminder_days": 30
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

# --- Contact Management Dialog ---
class ContactDialog(QDialog):
    def __init__(self, client_id=None, contact_data=None, parent=None):
        super().__init__(parent)
        self.client_id = client_id
        self.contact_data = contact_data or {}
        self.setWindowTitle("Gestion des Contacts" if not contact_data else "Modifier Contact")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QFormLayout(self)
        
        self.name_input = QLineEdit(self.contact_data.get("name", ""))
        layout.addRow("Nom complet:", self.name_input)
        
        self.email_input = QLineEdit(self.contact_data.get("email", ""))
        layout.addRow("Email:", self.email_input)
        
        self.phone_input = QLineEdit(self.contact_data.get("phone", ""))
        layout.addRow("Téléphone:", self.phone_input)
        
        self.position_input = QLineEdit(self.contact_data.get("position", ""))
        layout.addRow("Poste:", self.position_input)
        
        self.primary_check = QCheckBox("Contact principal")
        self.primary_check.setChecked(bool(self.contact_data.get("is_primary", 0)))
        layout.addRow(self.primary_check)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)
        
    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "email": self.email_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "position": self.position_input.text().strip(),
            "is_primary": 1 if self.primary_check.isChecked() else 0
        }

# --- Template Management Dialog ---
class TemplateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestion des Modèles")
        self.setMinimumSize(600, 400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Template list
        self.template_list = QListWidget()
        self.template_list.itemDoubleClicked.connect(self.edit_template)
        layout.addWidget(self.template_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Ajouter Modèle")
        self.add_btn.setIcon(QIcon.fromTheme("list-add"))
        self.add_btn.clicked.connect(self.add_template)
        btn_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("Modifier")
        self.edit_btn.setIcon(QIcon.fromTheme("document-edit"))
        self.edit_btn.clicked.connect(self.edit_template)
        btn_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("Supprimer")
        self.delete_btn.setIcon(QIcon.fromTheme("edit-delete"))
        self.delete_btn.clicked.connect(self.delete_template)
        btn_layout.addWidget(self.delete_btn)
        
        self.default_btn = QPushButton("Définir par Défaut")
        self.default_btn.setIcon(QIcon.fromTheme("emblem-default"))
        self.default_btn.clicked.connect(self.set_default_template)
        btn_layout.addWidget(self.default_btn)
        
        layout.addLayout(btn_layout)
        
        self.load_templates()
        
    def load_templates(self):
        self.template_list.clear()
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT template_id, name, language, is_default 
                FROM Templates
                ORDER BY name, language
            """)
            
            for row in cursor.fetchall():
                item = QListWidgetItem(f"{row[1]} ({row[2]}) {'[Défaut]' if row[3] else ''}")
                item.setData(Qt.UserRole, row[0])
                self.template_list.addItem(item)
                
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Erreur DB", f"Erreur de chargement des modèles:\n{str(e)}")
            
    def add_template(self):
        # Get file path
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Sélectionner un modèle", 
            CONFIG["templates_dir"], 
            "Fichiers Excel (*.xlsx);;Tous les fichiers (*)"
        )
        
        if not file_path:
            return
            
        # Get template details
        name, ok = QInputDialog.getText(self, "Nom du Modèle", "Entrez un nom pour ce modèle:")
        if not ok or not name.strip():
            return
            
        # Get language
        languages = ["fr", "ar", "tr"]
        lang, ok = QInputDialog.getItem(
            self, 
            "Langue du Modèle", 
            "Sélectionnez la langue:", 
            languages, 
            0, 
            False
        )
        
        if not ok:
            return
            
        # Copy file to templates directory
        target_dir = os.path.join(CONFIG["templates_dir"], lang)
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, os.path.basename(file_path))
        
        try:
            shutil.copy(file_path, target_path)
            
            # Save to database
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Templates (name, file_name, language, is_default) "
                "VALUES (?, ?, ?, 0)",
                (name.strip(), os.path.basename(file_path), lang)
            )
            conn.commit()
            
            self.load_templates()
            QMessageBox.information(self, "Succès", "Modèle ajouté avec succès.")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout du modèle:\n{str(e)}")
            
    def edit_template(self):
        item = self.template_list.currentItem()
        if not item:
            return
            
        template_id = item.data(Qt.UserRole)
        
        # Open template in default application
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT file_name, language FROM Templates WHERE template_id = ?",
                (template_id,)
            )
            result = cursor.fetchone()
            if result:
                file_path = os.path.join(CONFIG["templates_dir"], result[1], result[0])
                QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Erreur DB", f"Erreur d'accès au modèle:\n{str(e)}")
            
    def delete_template(self):
        item = self.template_list.currentItem()
        if not item:
            return
            
        template_id = item.data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self,
            "Confirmer Suppression",
            "Êtes-vous sûr de vouloir supprimer ce modèle?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                
                # Get file info
                cursor.execute(
                    "SELECT file_name, language FROM Templates WHERE template_id = ?",
                    (template_id,)
                )
                result = cursor.fetchone()
                
                # Delete from DB
                cursor.execute("DELETE FROM Templates WHERE template_id = ?", (template_id,))
                conn.commit()
                
                # Delete file
                if result:
                    file_path = os.path.join(CONFIG["templates_dir"], result[1], result[0])
                    if os.path.exists(file_path):
                        os.remove(file_path)
                
                self.load_templates()
                QMessageBox.information(self, "Succès", "Modèle supprimé avec succès.")
                
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Erreur DB", f"Erreur de suppression du modèle:\n{str(e)}")
            except OSError as e:
                QMessageBox.critical(self, "Erreur Fichier", f"Erreur de suppression du fichier:\n{str(e)}")
                
    def set_default_template(self):
        item = self.template_list.currentItem()
        if not item:
            return
            
        template_id = item.data(Qt.UserRole)
        
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            # Get template category
            cursor.execute(
                "SELECT name FROM Templates WHERE template_id = ?",
                (template_id,)
            )
            name = cursor.fetchone()[0]
            
            # Reset all defaults for this category
            cursor.execute(
                "UPDATE Templates SET is_default = 0 WHERE name LIKE ?",
                (f"{name}%",)
            )
            
            # Set this template as default
            cursor.execute(
                "UPDATE Templates SET is_default = 1 WHERE template_id = ?",
                (template_id,)
            )
            conn.commit()
            
            self.load_templates()
            QMessageBox.information(self, "Succès", "Modèle défini comme modèle par défaut.")
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur DB", f"Erreur de mise à jour du modèle:\n{str(e)}")

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
        
        self.export_pdf_button = QPushButton("Exporter PDF")
        self.export_pdf_button.setIcon(QIcon.fromTheme("application-pdf"))
        self.export_pdf_button.clicked.connect(self.export_to_pdf)
        button_layout.addWidget(self.export_pdf_button)
        
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
                        "{DATE_CREATION}": datetime.now().strftime("%Y-%m-%d"),
                        "{PRIX_FINAL}": str(self.client_data.get("price", "")),
                        "{PROJECT_ID}": self.client_data.get("project_identifier", "")
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
            
    def export_to_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter en PDF",
            os.path.expanduser("~"),
            "Fichiers PDF (*.pdf)"
        )
        
        if not file_path:
            return
            
        try:
            # Create a PDF document
            packet = io.BytesIO()
            can = canvas.Canvas(packet)
            
            # Set up document
            can.setFont("Helvetica", 10)
            width, height = 800, 600
            can.setPageSize((width, height))
            
            # Add title
            title = f"{os.path.basename(self.file_path)} - {datetime.now().strftime('%Y-%m-%d')}"
            can.setFont("Helvetica-Bold", 14)
            can.drawString(50, height - 50, title)
            can.line(50, height - 60, width - 50, height - 60)
            
            # Add client information
            can.setFont("Helvetica", 10)
            y_pos = height - 100
            can.drawString(50, y_pos, f"Client: {self.client_data.get('name', '')}")
            can.drawString(50, y_pos - 20, f"Projet: {self.client_data.get('project_identifier', '')}")
            can.drawString(50, y_pos - 40, f"Prix: {self.client_data.get('price', 0)} €")
            
            # Add table header
            y_pos -= 80
            can.setFont("Helvetica-Bold", 10)
            headers = []
            for j in range(self.table_widget.columnCount()):
                header_item = self.table_widget.horizontalHeaderItem(j)
                headers.append(header_item.text() if header_item else f"Colonne {j+1}")
            
            col_width = (width - 100) / len(headers)
            for i, header in enumerate(headers):
                can.drawString(50 + i * col_width, y_pos, header)
            
            # Add table content
            can.setFont("Helvetica", 9)
            y_pos -= 20
            for row in range(self.table_widget.rowCount()):
                if y_pos < 100:  # New page if needed
                    can.showPage()
                    y_pos = height - 50
                    can.setFont("Helvetica", 9)
                
                for col in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, col)
                    text = item.text() if item else ""
                    can.drawString(50 + col * col_width, y_pos, text)
                
                y_pos -= 15
            
            # Save PDF
            can.save()
            packet.seek(0)
            with open(file_path, "wb") as f:
                f.write(packet.getvalue())
            
            QMessageBox.information(self, "Export Réussi", f"Le document a été exporté en PDF:\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur d'Export", f"Erreur lors de l'export en PDF:\n{str(e)}")

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
        
        # Status indicator
        status_layout = QHBoxLayout()
        status_label = QLabel("Statut:")
        status_layout.addWidget(status_label)
        
        self.status_combo = QComboBox()
        self.load_statuses()
        self.status_combo.setCurrentText(self.client_info.get("status", "En cours"))
        self.status_combo.currentTextChanged.connect(self.update_client_status)
        status_layout.addWidget(self.status_combo)
        
        layout.addLayout(status_layout)
        
        # Client details
        details_layout = QFormLayout()
        details_layout.setLabelAlignment(Qt.AlignRight)
        
        details = [
            ("ID Projet:", self.client_info.get("project_identifier", "N/A")),
            ("Pays:", self.client_info.get("country", "N/A")),
            ("Ville:", self.client_info.get("city", "N/A")),
            ("Besoin Principal:", self.client_info.get("need", "N/A")),
            ("Prix Final:", f"{self.client_info.get('price', 0)} €"),
            ("Date Création:", self.client_info.get("creation_date", "N/A")),
            ("Chemin Dossier:", f"<a href='file:///{self.client_info['path']}'>{self.client_info['path']}</a>")
        ]
        
        for label, value in details:
            label_widget = QLabel(label)
            value_widget = QLabel(value)
            value_widget.setOpenExternalLinks(True)
            value_widget.setTextInteractionFlags(Qt.TextBrowserInteraction)
            details_layout.addRow(label_widget, value_widget)
        
        layout.addLayout(details_layout)
        
        # Notes section
        notes_group = QGroupBox("Notes")
        notes_layout = QVBoxLayout(notes_group)
        
        self.notes_edit = QTextEdit(self.client_info.get("notes", ""))
        self.notes_edit.setPlaceholderText("Ajoutez des notes sur ce client...")
        self.notes_edit.textChanged.connect(self.save_client_notes)
        notes_layout.addWidget(self.notes_edit)
        
        layout.addWidget(notes_group)
        
        # Tab widget for documents and contacts
        self.tab_widget = QTabWidget()
        
        # Documents tab
        docs_tab = QWidget()
        docs_layout = QVBoxLayout(docs_tab)
        
        # Document buttons
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
        
        docs_layout.addLayout(buttons_layout)
        
        # Export section
        export_group = QGroupBox("Exporter Documents")
        export_layout = QVBoxLayout(export_group)
        
        self.export_docs_list = QListWidget()
        self.export_docs_list.setSelectionMode(QListWidget.MultiSelection)
        self.populate_export_list()
        export_layout.addWidget(self.export_docs_list)
        
        export_btn_layout = QHBoxLayout()
        self.export_pdf_btn = QPushButton("Exporter PDF")
        self.export_pdf_btn.setIcon(QIcon.fromTheme("application-pdf"))
        self.export_pdf_btn.clicked.connect(self.export_selected_docs)
        export_btn_layout.addWidget(self.export_pdf_btn)
        
        self.send_email_btn = QPushButton("Envoyer par Email")
        self.send_email_btn.setIcon(QIcon.fromTheme("mail-send"))
        self.send_email_btn.clicked.connect(self.send_docs_email)
        export_btn_layout.addWidget(self.send_email_btn)
        
        export_layout.addLayout(export_btn_layout)
        docs_layout.addWidget(export_group)
        
        # File browser
        files_group = QGroupBox("Fichiers du Client")
        files_layout = QVBoxLayout(files_group)
        
        self.file_list = QListWidget()
        self.file_list.setAlternatingRowColors(True)
        self.file_list.itemDoubleClicked.connect(self.open_selected_file)
        files_layout.addWidget(self.file_list)
        
        refresh_btn = QPushButton("Actualiser Fichiers")
        refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        refresh_btn.clicked.connect(self.populate_file_list)
        files_layout.addWidget(refresh_btn)
        
        docs_layout.addWidget(files_group)
        self.tab_widget.addTab(docs_tab, "Documents")
        
        # Contacts tab
        contacts_tab = QWidget()
        contacts_layout = QVBoxLayout(contacts_tab)
        
        # Contacts list
        self.contacts_list = QListWidget()
        self.contacts_list.setAlternatingRowColors(True)
        self.contacts_list.itemDoubleClicked.connect(self.edit_contact)
        contacts_layout.addWidget(self.contacts_list)
        
        # Contacts buttons
        contacts_btn_layout = QHBoxLayout()
        self.add_contact_btn = QPushButton("Ajouter Contact")
        self.add_contact_btn.setIcon(QIcon.fromTheme("contact-new"))
        self.add_contact_btn.clicked.connect(self.add_contact)
        contacts_btn_layout.addWidget(self.add_contact_btn)
        
        self.edit_contact_btn = QPushButton("Modifier")
        self.edit_contact_btn.setIcon(QIcon.fromTheme("document-edit"))
        self.edit_contact_btn.clicked.connect(self.edit_contact)
        contacts_btn_layout.addWidget(self.edit_contact_btn)
        
        self.remove_contact_btn = QPushButton("Supprimer")
        self.remove_contact_btn.setIcon(QIcon.fromTheme("edit-delete"))
        self.remove_contact_btn.clicked.connect(self.remove_contact)
        contacts_btn_layout.addWidget(self.remove_contact_btn)
        
        contacts_layout.addLayout(contacts_btn_layout)
        self.tab_widget.addTab(contacts_tab, "Contacts")
        
        layout.addWidget(self.tab_widget)
        
        # Populate data
        self.populate_file_list()
        self.load_contacts()
        
    def load_statuses(self):
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT status_name FROM StatusSettings")
            for status in cursor.fetchall():
                self.status_combo.addItem(status[0])
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Erreur DB", f"Erreur de chargement des statuts:\n{str(e)}")
            
    def update_client_status(self, status):
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Clients SET status = ? WHERE client_id = ?",
                (status, self.client_info["client_id"])
            )
            conn.commit()
            
            # Update client info
            self.client_info["status"] = status
            
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Erreur DB", f"Erreur de mise à jour du statut:\n{str(e)}")
            
    def save_client_notes(self):
        notes = self.notes_edit.toPlainText()
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Clients SET notes = ? WHERE client_id = ?",
                (notes, self.client_info["client_id"])
            )
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Erreur DB", f"Erreur de sauvegarde des notes:\n{str(e)}")
            
    def populate_file_list(self):
        self.file_list.clear()
        path = self.client_info["path"]
        
        if not os.path.exists(path):
            self.file_list.addItem("Dossier introuvable")
            return
            
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    # Add language folders and their contents
                    for lang_file in os.listdir(item_path):
                        lang_file_path = os.path.join(item_path, lang_file)
                        display = f"{item}/{lang_file} {'(Dossier)' if os.path.isdir(lang_file_path) else ''}"
                        self.file_list.addItem(display)
                else:
                    display = f"{item} {'(Dossier)' if os.path.isdir(item_path) else ''}"
                    self.file_list.addItem(display)
        except Exception as e:
            self.file_list.addItem(f"Erreur: {str(e)}")
            
    def populate_export_list(self):
        self.export_docs_list.clear()
        path = self.client_info["path"]
        
        if not os.path.exists(path):
            return
            
        try:
            for lang in self.client_info.get("languages", ["fr"]):
                lang_path = os.path.join(path, lang)
                if os.path.exists(lang_path):
                    for doc in os.listdir(lang_path):
                        if doc.endswith(".xlsx"):
                            item = QListWidgetItem(f"{lang}/{doc}")
                            item.setData(Qt.UserRole, os.path.join(lang_path, doc))
                            self.export_docs_list.addItem(item)
        except Exception as e:
            print(f"Erreur population export: {str(e)}")

    def open_selected_file(self, item):
        file_name = item.text().replace(" (Dossier)", "")
        file_path = os.path.join(self.client_info["path"], file_name)
        
        if os.path.exists(file_path):
            try:
                if file_path.lower().endswith('.xlsx'):
                    editor = ExcelEditor(file_path, self.client_info, self)
                    editor.exec_()
                    self.populate_file_list()
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
            "ID Projet": self.client_info.get("project_identifier", ""),
            "price": self.client_info.get("price", 0)
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
            self.populate_export_list()
            
    def load_contacts(self):
        self.contacts_list.clear()
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT contact_id, name, email, phone, is_primary "
                "FROM Contacts WHERE client_id = ?",
                (self.client_info["client_id"],)
            )
            
            for row in cursor.fetchall():
                contact_text = f"{row[1]}"
                if row[4]:  # is_primary
                    contact_text += " [Principal]"
                item = QListWidgetItem(contact_text)
                item.setData(Qt.UserRole, row[0])
                self.contacts_list.addItem(item)
                
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Erreur DB", f"Erreur de chargement des contacts:\n{str(e)}")
            
    def add_contact(self):
        dialog = ContactDialog(self.client_info["client_id"])
        if dialog.exec_() == QDialog.Accepted:
            contact_data = dialog.get_data()
            try:
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                
                # If setting as primary, clear existing primary
                if contact_data["is_primary"]:
                    cursor.execute(
                        "UPDATE Contacts SET is_primary = 0 WHERE client_id = ?",
                        (self.client_info["client_id"],)
                    )
                
                cursor.execute(
                    "INSERT INTO Contacts (client_id, name, email, phone, is_primary) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (
                        self.client_info["client_id"],
                        contact_data["name"],
                        contact_data["email"],
                        contact_data["phone"],
                        contact_data["is_primary"]
                    )
                )
                conn.commit()
                
                self.load_contacts()
                
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Erreur DB", f"Erreur d'ajout du contact:\n{str(e)}")
                
    def edit_contact(self):
        item = self.contacts_list.currentItem()
        if not item:
            return
            
        contact_id = item.data(Qt.UserRole)
        
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, email, phone, is_primary FROM Contacts WHERE contact_id = ?",
                (contact_id,)
            )
            contact_data = cursor.fetchone()
            
            if contact_data:
                dialog = ContactDialog(self.client_info["client_id"], {
                    "name": contact_data[0],
                    "email": contact_data[1],
                    "phone": contact_data[2],
                    "is_primary": contact_data[3]
                })
                
                if dialog.exec_() == QDialog.Accepted:
                    new_data = dialog.get_data()
                    
                    # If setting as primary, clear existing primary
                    if new_data["is_primary"]:
                        cursor.execute(
                            "UPDATE Contacts SET is_primary = 0 WHERE client_id = ?",
                            (self.client_info["client_id"],)
                        )
                    
                    cursor.execute(
                        "UPDATE Contacts SET name = ?, email = ?, phone = ?, is_primary = ? "
                        "WHERE contact_id = ?",
                        (
                            new_data["name"],
                            new_data["email"],
                            new_data["phone"],
                            new_data["is_primary"],
                            contact_id
                        )
                    )
                    conn.commit()
                    self.load_contacts()
                    
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur DB", f"Erreur de modification du contact:\n{str(e)}")
            
    def remove_contact(self):
        item = self.contacts_list.currentItem()
        if not item:
            return
            
        contact_id = item.data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self,
            "Confirmer Suppression",
            "Êtes-vous sûr de vouloir supprimer ce contact?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM Contacts WHERE contact_id = ?",
                    (contact_id,)
                )
                conn.commit()
                self.load_contacts()
                
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Erreur DB", f"Erreur de suppression du contact:\n{str(e)}")
                
    def export_selected_docs(self):
        items = self.export_docs_list.selectedItems()
        if not items:
            QMessageBox.warning(self, "Aucun document sélectionné", "Veuillez sélectionner au moins un document à exporter.")
            return
            
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Sélectionnez un dossier pour l'export",
            os.path.expanduser("~")
        )
        
        if not dir_path:
            return
            
        exported_files = []
        
        for item in items:
            file_path = item.data(Qt.UserRole)
            if os.path.exists(file_path):
                try:
                    # Create PDF from Excel
                    output_path = os.path.join(dir_path, os.path.basename(file_path).replace(".xlsx", ".pdf"))
                    
                    # Simple conversion - in real app, use proper conversion
                    with open(output_path, "w") as f:
                        f.write(f"Export PDF de: {os.path.basename(file_path)}\n")
                        f.write(f"Client: {self.client_info['name']}\n")
                        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                    
                    exported_files.append(output_path)
                    
                except Exception as e:
                    QMessageBox.warning(self, "Erreur d'export", f"Erreur lors de l'export de {os.path.basename(file_path)}:\n{str(e)}")
        
        if exported_files:
            QMessageBox.information(
                self,
                "Export Réussi",
                f"{len(exported_files)} documents exportés avec succès dans:\n{dir_path}"
            )
            QDesktopServices.openUrl(QUrl.fromLocalFile(dir_path))
            
    def send_docs_email(self):
        items = self.export_docs_list.selectedItems()
        if not items:
            QMessageBox.warning(self, "Aucun document sélectionné", "Veuillez sélectionner au moins un document à envoyer.")
            return
            
        # Get primary contact
        primary_contact = None
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT email FROM Contacts WHERE client_id = ? AND is_primary = 1",
                (self.client_info["client_id"],)
            )
            primary_contact = cursor.fetchone()
        except sqlite3.Error:
            pass
            
        email, ok = QInputDialog.getText(
            self,
            "Adresse Email",
            "Entrez l'adresse email du destinataire:",
            text=primary_contact[0] if primary_contact else ""
        )
        
        if not ok or not email.strip():
            return
            
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = CONFIG.get("smtp_user", "noreply@example.com")
        msg['To'] = email
        msg['Subject'] = f"Documents pour {self.client_info['name']}"
        
        body = f"Bonjour,\n\nVeuillez trouver ci-joint les documents demandés pour le projet {self.client_info['project_identifier']}.\n\nCordialement,\nÉquipe ClientDocManager"
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach files
        for item in items:
            file_path = item.data(Qt.UserRole)
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                msg.attach(part)
        
        # Send email
        try:
            server = smtplib.SMTP(CONFIG["smtp_server"], CONFIG["smtp_port"])
            server.starttls()
            server.login(CONFIG["smtp_user"], CONFIG["smtp_password"])
            server.send_message(msg)
            server.quit()
            
            QMessageBox.information(self, "Email Envoyé", "Les documents ont été envoyés avec succès.")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur d'envoi", f"Erreur lors de l'envoi de l'email:\n{str(e)}")

# --- Statistics Widget ---
class StatisticsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.update_stats()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Total clients
        total_group = QGroupBox("Clients Totaux")
        total_layout = QVBoxLayout(total_group)
        self.total_label = QLabel("0")
        self.total_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.total_label.setAlignment(Qt.AlignCenter)
        total_layout.addWidget(self.total_label)
        layout.addWidget(total_group)
        
        # Total value
        value_group = QGroupBox("Valeur Totale")
        value_layout = QVBoxLayout(value_group)
        self.value_label = QLabel("0 €")
        self.value_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.value_label.setAlignment(Qt.AlignCenter)
        value_layout.addWidget(self.value_label)
        layout.addWidget(value_group)
        
        # Ongoing projects
        ongoing_group = QGroupBox("Projets en Cours")
        ongoing_layout = QVBoxLayout(ongoing_group)
        self.ongoing_label = QLabel("0")
        self.ongoing_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.ongoing_label.setAlignment(Qt.AlignCenter)
        ongoing_layout.addWidget(self.ongoing_label)
        layout.addWidget(ongoing_group)
        
        # Urgent projects
        urgent_group = QGroupBox("Projets Urgents")
        urgent_layout = QVBoxLayout(urgent_group)
        self.urgent_label = QLabel("0")
        self.urgent_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.urgent_label.setStyleSheet("color: #e74c3c;")
        self.urgent_label.setAlignment(Qt.AlignCenter)
        urgent_layout.addWidget(self.urgent_label)
        layout.addWidget(urgent_group)
        
    def update_stats(self):
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            # Total clients
            cursor.execute("SELECT COUNT(*) FROM Clients")
            total = cursor.fetchone()[0]
            self.total_label.setText(str(total))
            
            # Total value
            cursor.execute("SELECT SUM(price) FROM Clients")
            total_value = cursor.fetchone()[0] or 0
            self.value_label.setText(f"{total_value:,.2f} €")
            
            # Ongoing projects
            cursor.execute("SELECT COUNT(*) FROM Clients WHERE status = 'En cours'")
            ongoing = cursor.fetchone()[0]
            self.ongoing_label.setText(str(ongoing))
            
            # Urgent projects
            cursor.execute("SELECT COUNT(*) FROM Clients WHERE status = 'Urgent'")
            urgent = cursor.fetchone()[0]
            self.urgent_label.setText(str(urgent))
            
        except sqlite3.Error as e:
            print(f"Erreur de statistiques: {str(e)}")

# --- Status Delegate for List Widget ---
class StatusDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Get status data
        status = index.data(Qt.UserRole)
        
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT color FROM StatusSettings WHERE status_name = ?", (status,))
            color = cursor.fetchone()[0]
        except:
            color = "#95a5a6"  # Default color
        
        # Draw background
        painter.save()
        painter.fillRect(option.rect, QColor(color))
        
        # Draw text
        text_rect = option.rect.adjusted(5, 0, -5, 0)
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, index.data())
        painter.restore()

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
        self.check_old_clients()
        
        # Setup timer for periodic checks
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_old_clients)
        self.check_timer.start(3600000)  # Check every hour
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Statistics bar
        self.stats_widget = StatisticsWidget()
        main_layout.addWidget(self.stats_widget)
        
        # Main content
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # Left panel - Client management
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        # Filter and search
        filter_layout = QHBoxLayout()
        
        self.status_filter = QComboBox()
        self.status_filter.addItem("Tous les statuts")
        self.load_statuses_into_filter()
        self.status_filter.currentIndexChanged.connect(self.filter_clients)
        filter_layout.addWidget(QLabel("Filtrer par statut:"))
        filter_layout.addWidget(self.status_filter)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher client...")
        self.search_input.textChanged.connect(self.filter_clients)
        filter_layout.addWidget(self.search_input)
        
        left_layout.addLayout(filter_layout)
        
        # Client list with status colors
        self.client_list = QListWidget()
        self.client_list.setAlternatingRowColors(True)
        self.client_list.setItemDelegate(StatusDelegate(self.client_list))
        self.client_list.itemClicked.connect(self.open_client_tab)
        self.client_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.client_list.customContextMenuRequested.connect(self.show_client_context_menu)
        left_layout.addWidget(self.client_list)
        
        # Client creation form
        form_group = QGroupBox("Ajouter un Nouveau Client")
        form_layout = QVBoxLayout(form_group)
        
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
        self.country_combo.currentTextChanged.connect(self.load_cities)
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
        
        self.price_input = QDoubleSpinBox()
        self.price_input.setPrefix("€ ")
        self.price_input.setRange(0, 10000000)
        self.price_input.setValue(0)
        creation_form.addRow("Prix Final:", self.price_input)
        
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
        
        content_layout.addWidget(left_panel, 1)
        
        # Right panel - Client tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        content_layout.addWidget(self.tabs, 2)
        
        # Load countries and cities
        self.load_countries()
        
    def create_actions(self):
        self.settings_action = QAction("Paramètres", self)
        self.settings_action.triggered.connect(self.open_settings)
        
        self.template_action = QAction("Gérer les Modèles", self)
        self.template_action.triggered.connect(self.manage_templates)
        
        self.status_action = QAction("Gérer les Statuts", self)
        self.status_action.triggered.connect(self.manage_statuses)
        
        self.exit_action = QAction("Quitter", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)
        
    def create_menus(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("Fichier")
        file_menu.addAction(self.settings_action)
        file_menu.addAction(self.template_action)
        file_menu.addAction(self.status_action)
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
            "Version 3.0<br>"
            "Application complète de gestion de documents clients<br><br>"
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
        price = self.price_input.value()
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
                "project_identifier, base_folder_path, selected_languages, price, creation_date) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    client_id, name, company, need, country, city, 
                    project_id, folder_path, ",".join(languages), price,
                    datetime.now().strftime("%Y-%m-%d")
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
                "languages": languages,
                "price": price,
                "creation_date": datetime.now().strftime("%Y-%m-%d"),
                "status": "En cours"
            }
            
            self.add_client_to_list(name, "En cours")
            
            # Clear form
            self.name_input.clear()
            self.company_input.clear()
            self.need_input.clear()
            self.project_id_input.clear()
            self.price_input.setValue(0)
            
            QMessageBox.information(
                self, 
                "Client Créé", 
                f"Client {name} créé avec succès.\nID: {client_id}\nDossier: {folder_path}"
            )
            
            # Open client tab
            self.open_client_tab_by_name(name)
            self.stats_widget.update_stats()
            
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
                       project_identifier, base_folder_path, selected_languages, 
                       price, notes, status, creation_date
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
                    "languages": row[8].split(',') if row[8] else ['fr'],
                    "price": row[9],
                    "notes": row[10],
                    "status": row[11],
                    "creation_date": row[12]
                }
                self.add_client_to_list(name, row[11])
                
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur DB", f"Erreur de chargement des clients:\n{str(e)}")
            
    def add_client_to_list(self, name, status):
        item = QListWidgetItem(name)
        item.setData(Qt.UserRole, status)  # Store status for delegate
        self.client_list.addItem(item)
            
    def filter_clients(self):
        search_text = self.search_input.text().lower()
        status_filter = self.status_filter.currentText()
        
        self.client_list.clear()
        
        for name, client in self.clients_data.items():
            # Apply status filter
            if status_filter != "Tous les statuts" and client["status"] != status_filter:
                continue
                
            # Apply search filter
            if search_text and search_text not in name.lower():
                continue
                
            self.add_client_to_list(name, client["status"])
            
    def load_statuses_into_filter(self):
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT status_name FROM StatusSettings")
            for status in cursor.fetchall():
                self.status_filter.addItem(status[0])
        except sqlite3.Error as e:
            print(f"Erreur de chargement des statuts: {str(e)}")
            
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
        
        archive_action = menu.addAction("Archiver")
        archive_action.triggered.connect(lambda: self.archive_client(client_name))
        
        delete_action = menu.addAction("Supprimer")
        delete_action.triggered.connect(lambda: self.delete_client(client_name))
        
        menu.exec_(self.client_list.mapToGlobal(pos))
        
    def open_client_folder(self, client_name):
        if client_name in self.clients_data:
            path = self.clients_data[client_name]["path"]
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
            
    def archive_client(self, client_name):
        if client_name not in self.clients_data:
            return
            
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Clients SET status = 'Archivé' WHERE client_name = ?",
                (client_name,)
            )
            conn.commit()
            
            # Update local data
            self.clients_data[client_name]["status"] = "Archivé"
            
            # Update list
            for i in range(self.client_list.count()):
                item = self.client_list.item(i)
                if item.text() == client_name:
                    item.setData(Qt.UserRole, "Archivé")
                    self.client_list.update()
                    break
                    
            QMessageBox.information(self, "Client Archivé", f"Le client {client_name} a été archivé.")
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur DB", f"Erreur d'archivage du client:\n{str(e)}")
            
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
                cursor.execute(
                    "DELETE FROM Contacts WHERE client_id = ?",
                    (self.clients_data[client_name]["client_id"],)
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
                
                self.stats_widget.update_stats()
                        
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Erreur DB", f"Erreur de suppression du client:\n{str(e)}")
            except OSError as e:
                QMessageBox.critical(self, "Erreur Dossier", f"Erreur de suppression du dossier:\n{str(e)}")
                
    def check_old_clients(self):
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            # Get default reminder days
            reminder_days = self.config.get("default_reminder_days", 30)
            
            # Find clients older than reminder_days that are still active
            cursor.execute("""
                SELECT client_name, creation_date 
                FROM Clients 
                WHERE status NOT IN ('Archivé', 'Complété')
                AND date(creation_date) <= date('now', ?)
            """, (f"-{reminder_days} days",))
            
            old_clients = cursor.fetchall()
            
            if old_clients:
                client_list = "\n".join([f"- {client[0]} ({client[1]})" for client in old_clients])
                reply = QMessageBox.question(
                    self,
                    "Clients Anciens",
                    f"Les clients suivants sont actifs depuis plus de {reminder_days} jours:\n{client_list}\n\n"
                    "Voulez-vous les archiver?",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    for client in old_clients:
                        self.archive_client(client[0])
                        
        except sqlite3.Error as e:
            print(f"Erreur vérification clients anciens: {str(e)}")
            
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
            
    def manage_templates(self):
        dialog = TemplateDialog(self)
        dialog.exec_()
        
    def manage_statuses(self):
        QMessageBox.information(self, "Gestion des Statuts", "Cette fonctionnalité sera implémentée dans la prochaine version.")
            
    def closeEvent(self, event):
        save_config(self.config)
        super().closeEvent(event)

# --- Settings Dialog ---
class SettingsDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Paramètres de l'Application")
        self.setMinimumSize(500, 400)
        
        self.config = config
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # General settings tab
        general_tab = QWidget()
        general_layout = QFormLayout(general_tab)
        
        # Templates directory
        self.templates_input = QLineEdit(self.config["templates_dir"])
        templates_btn = QPushButton("Parcourir...")
        templates_btn.clicked.connect(lambda: self.browse_directory(self.templates_input))
        
        templates_layout = QHBoxLayout()
        templates_layout.addWidget(self.templates_input)
        templates_layout.addWidget(templates_btn)
        general_layout.addRow("Dossier des Modèles:", templates_layout)
        
        # Clients directory
        self.clients_input = QLineEdit(self.config["clients_dir"])
        clients_btn = QPushButton("Parcourir...")
        clients_btn.clicked.connect(lambda: self.browse_directory(self.clients_input))
        
        clients_layout = QHBoxLayout()
        clients_layout.addWidget(self.clients_input)
        clients_layout.addWidget(clients_btn)
        general_layout.addRow("Dossier des Clients:", clients_layout)
        
        # Language selection
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Français (fr)", "Arabe (ar)", "Turc (tr)"])
        
        lang_map = {"fr": "Français (fr)", "ar": "Arabe (ar)", "tr": "Turc (tr)"}
        self.lang_combo.setCurrentText(lang_map.get(self.config.get("language", "fr"), "fr"))
        general_layout.addRow("Langue Interface:", self.lang_combo)
        
        # Reminder days
        self.reminder_spin = QSpinBox()
        self.reminder_spin.setRange(1, 365)
        self.reminder_spin.setValue(self.config.get("default_reminder_days", 30))
        general_layout.addRow("Jours avant rappel:", self.reminder_spin)
        
        tabs.addTab(general_tab, "Général")
        
        # Email settings tab
        email_tab = QWidget()
        email_layout = QFormLayout(email_tab)
        
        self.smtp_server_input = QLineEdit(self.config.get("smtp_server", ""))
        email_layout.addRow("Serveur SMTP:", self.smtp_server_input)
        
        self.smtp_port_input = QSpinBox()
        self.smtp_port_input.setRange(1, 65535)
        self.smtp_port_input.setValue(self.config.get("smtp_port", 587))
        email_layout.addRow("Port SMTP:", self.smtp_port_input)
        
        self.smtp_user_input = QLineEdit(self.config.get("smtp_user", ""))
        email_layout.addRow("Utilisateur SMTP:", self.smtp_user_input)
        
        self.smtp_pass_input = QLineEdit(self.config.get("smtp_password", ""))
        self.smtp_pass_input.setEchoMode(QLineEdit.Password)
        email_layout.addRow("Mot de passe SMTP:", self.smtp_pass_input)
        
        tabs.addTab(email_tab, "Email")
        
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
            "language": lang_map.get(self.lang_combo.currentText(), "fr"),
            "default_reminder_days": self.reminder_spin.value(),
            "smtp_server": self.smtp_server_input.text(),
            "smtp_port": self.smtp_port_input.value(),
            "smtp_user": self.smtp_user_input.text(),
            "smtp_password": self.smtp_pass_input.text()
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
                    "{PRIX_FINAL} €"
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