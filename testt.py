import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Union
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QUrl, QUrlQuery
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QFormLayout, QLineEdit, QComboBox, 
                            QPushButton, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout, 
                            QFrame, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, 
                            QAbstractItemView, QMenu, QAction, QFileDialog, QCheckBox)

class DynamicContactDatabase:
    """Gestion dynamique de la base de données contacts avec colonnes personnalisables"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialise la structure de base de la base de données"""
        with self._get_connection() as conn:
            # Table des catégories
            conn.execute('''
                CREATE TABLE IF NOT EXISTS contactcategories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    color TEXT DEFAULT '#3498db',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            
            # Table principale des contacts
            conn.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    given_name TEXT,
                    family_name TEXT,
                    full_name TEXT GENERATED ALWAYS AS (
                        CASE 
                            WHEN given_name IS NOT NULL AND family_name IS NOT NULL THEN given_name || ' ' || family_name
                            WHEN given_name IS NOT NULL THEN given_name
                            ELSE family_name
                        END
                    ) STORED,
                    phone_mobile TEXT,
                    phone_home TEXT,
                    phone_work TEXT,
                    phone_other TEXT,
                    email_personal TEXT,
                    email_work TEXT,
                    email_other TEXT,
                    company TEXT,
                    job_title TEXT,
                    contactcategories_id INTEGER,
                    address_home TEXT,
                    address_work TEXT,
                    address_other TEXT,
                    birthday DATE,
                    notes TEXT,
                    photo BLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (contactcategories_id) REFERENCES contactcategories(id)
                );
            ''')
            
            # Table pour les colonnes personnalisées
            conn.execute('''
                CREATE TABLE IF NOT EXISTS custom_fields (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    field_name TEXT NOT NULL UNIQUE,
                    field_type TEXT DEFAULT 'TEXT',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            
            # Table des valeurs des champs personnalisés
            conn.execute('''
                CREATE TABLE IF NOT EXISTS custom_field_values (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contact_id INTEGER NOT NULL,
                    field_id INTEGER NOT NULL,
                    value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE,
                    FOREIGN KEY (field_id) REFERENCES custom_fields(id) ON DELETE CASCADE,
                    UNIQUE(contact_id, field_id)
                );
            ''')
            
            # Insertion des catégories par défaut
            default_categories = [
                ('Client', '#27ae60'),
                ('Prospect', '#f39c12'),
                ('Partenaire', '#9b59b6'),
                ('Personnel', '#e74c3c')
            ]
            
            for name, color in default_categories:
                try:
                    conn.execute('''
                        INSERT OR IGNORE INTO contactcategories (name, color) 
                        VALUES (?, ?)
                    ''', (name, color))
                except sqlite3.Error as e:
                    print(f"Error inserting default category {name}: {e}")

    def _get_connection(self) -> sqlite3.Connection:
        """Retourne une connexion à la base de données"""
        return sqlite3.connect(self.db_path)
    
    # Gestion des champs personnalisés
    def add_custom_field(self, field_name: str, field_type: str = 'TEXT') -> int:
        """Ajoute un nouveau champ personnalisé"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO custom_fields (field_name, field_type)
                VALUES (?, ?)
            ''', (field_name, field_type))
            return cursor.lastrowid
    
    def get_custom_fields(self) -> List[Dict]:
        """Récupère tous les champs personnalisés"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, field_name, field_type FROM custom_fields')
            return [{'id': row[0], 'name': row[1], 'type': row[2]} for row in cursor.fetchall()]
    
    def set_custom_field_value(self, contact_id: int, field_id: int, value: str) -> None:
        """Définit la valeur d'un champ personnalisé pour un contact"""
        with self._get_connection() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO custom_field_values 
                (contact_id, field_id, value) 
                VALUES (?, ?, ?)
            ''', (contact_id, field_id, value))
    
    def get_custom_field_values(self, contact_id: int) -> Dict[int, str]:
        """Récupère les valeurs des champs personnalisés pour un contact"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT field_id, value FROM custom_field_values 
                WHERE contact_id = ?
            ''', (contact_id,))
            return {row[0]: row[1] for row in cursor.fetchall()}
    
    # Gestion des contacts (méthodes similaires à avant mais adaptées)
    # ... (ajouter les méthodes pour gérer les contacts)

class ContactManager(QWidget):
    """Interface principale de gestion des contacts"""
    
    def __init__(self, db_manager: DynamicContactDatabase, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
        self.load_contacts()
        self.setup_drag_drop()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        self.setWindowTitle("Gestionnaire de Contacts Avancé")
        self.setMinimumSize(1024, 768)
        
        main_layout = QVBoxLayout(self)
        
        # Barre d'outils
        toolbar = QHBoxLayout()
        
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Rechercher des contacts...")
        self.search_field.textChanged.connect(self.filter_contacts)
        toolbar.addWidget(self.search_field)
        
        # Bouton pour ajouter des champs personnalisés
        self.add_field_btn = QPushButton("Ajouter Champ")
        self.add_field_btn.clicked.connect(self.show_add_field_dialog)
        toolbar.addWidget(self.add_field_btn)
        
        # Bouton d'import/export
        import_export_menu = QMenu()
        import_export_menu.addAction("Importer depuis Google Contacts", self.import_from_google)
        import_export_menu.addAction("Exporter vers Google Contacts", self.export_to_google)
        
        import_export_btn = QPushButton("Import/Export")
        import_export_btn.setMenu(import_export_menu)
        toolbar.addWidget(import_export_btn)
        
        main_layout.addLayout(toolbar)
        
        # Tableau des contacts
        self.contact_table = QTableWidget()
        self.contact_table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.contact_table.cellChanged.connect(self.handle_cell_change)
        main_layout.addWidget(self.contact_table)
    
    def setup_drag_drop(self):
        """Configure le glisser-déposer pour l'import de fichiers"""
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event):
        """Accepte les fichiers glissés"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """Gère le dépôt de fichiers pour l'import"""
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(('.csv', '.vcf')):
                self.import_contacts_from_file(file_path)
    
    def load_contacts(self):
        """Charge les contacts depuis la base de données"""
        # Implémentation à compléter
        pass
    
    def filter_contacts(self):
        """Filtre les contacts selon la recherche"""
        # Implémentation à compléter
        pass
    
    def handle_cell_change(self, row, column):
        """Gère la modification directe dans le tableau"""
        # Implémentation à compléter
        pass
    
    def show_add_field_dialog(self):
        """Affiche le dialogue pour ajouter un champ personnalisé"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter un champ personnalisé")
        
        layout = QFormLayout(dialog)
        
        name_edit = QLineEdit()
        layout.addRow("Nom du champ:", name_edit)
        
        type_combo = QComboBox()
        type_combo.addItems(["Texte", "Nombre", "Date", "Case à cocher"])
        layout.addRow("Type:", type_combo)
        
        buttons = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(dialog.accept)
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(dialog.reject)
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            field_name = name_edit.text().strip()
            if field_name:
                field_type = {
                    "Texte": "TEXT",
                    "Nombre": "INTEGER",
                    "Date": "DATE",
                    "Case à cocher": "BOOLEAN"
                }[type_combo.currentText()]
                
                self.db_manager.add_custom_field(field_name, field_type)
                self.load_contacts()  # Recharger pour afficher le nouveau champ
    
    def import_from_google(self):
        """Importe les contacts depuis Google Contacts"""
        # Implémentation à compléter avec l'API Google
        pass
    
    def export_to_google(self):
        """Exporte les contacts vers Google Contacts"""
        # Implémentation à compléter avec l'API Google
        pass
    
    def import_contacts_from_file(self, file_path: str):
        """Importe les contacts depuis un fichier"""
        # Implémentation à compléter
        pass

# Configuration et lancement de l'application
if __name__ == "__main__":
    import sys
    import os
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.expanduser('~'), 'contacts_advanced.db')
    
    # Initialisation
    app = QApplication(sys.argv)
    
    # Création de la base de données
    db_manager = DynamicContactDatabase(db_path)
    
    # Interface utilisateur
    contact_manager = ContactManager(db_manager)
    contact_manager.show()
    
    sys.exit(app.exec_())