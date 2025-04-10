import os
import sys
import sqlite3
from datetime import datetime
from PyQt5.QtCore import Qt, QSize, QDate
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPainter
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QListWidget, QTableWidget, 
                             QTableWidgetItem, QLineEdit, QTextEdit, QComboBox, QDateEdit, 
                             QFileDialog, QMessageBox, QHeaderView, QFormLayout, QTabWidget,
                             QAbstractItemView, QToolBar, QStatusBar, QAction, QDialog,
                             QInputDialog, QSplitter)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from fpdf import FPDF
import qtawesome as qta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import webbrowser
import tempfile

# Configuration initiale
APP_NAME = "DokumanYonetici"
DB_NAME = "dokuman_yonetici.db"
VERSION = "1.0.0"

# Style de l'application
APP_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QListWidget {
    background-color: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 4px;
    padding: 5px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #eeeeee;
}

QListWidget::item:selected {
    background-color: #4CAF50;
    color: white;
}

QTableWidget {
    background-color: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 4px;
    gridline-color: #eeeeee;
}

QHeaderView::section {
    background-color: #4CAF50;
    color: white;
    padding: 5px;
    border: none;
}

QLineEdit, QTextEdit, QComboBox, QDateEdit {
    border: 1px solid #dddddd;
    border-radius: 4px;
    padding: 5px;
    min-height: 25px;
}

QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 4px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b40;
}

QTabWidget::pane {
    border: 1px solid #dddddd;
    border-radius: 4px;
}

QTabBar::tab {
    background: #f1f1f1;
    border: 1px solid #dddddd;
    padding: 8px 15px;
}

QTabBar::tab:selected {
    background: #ffffff;
    border-bottom: 2px solid #4CAF50;
}

QStatusBar {
    background-color: #e9e9e9;
    color: #555555;
}

QToolBar {
    background-color: #f1f1f1;
    border: none;
    padding: 5px;
}

QSplitter::handle {
    background-color: #dddddd;
    width: 3px;
}
"""

class DatabaseManager:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Création de la table clients
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT,
                    email TEXT,
                    telephone TEXT,
                    societe TEXT,
                    adresse TEXT,
                    ville TEXT,
                    code_postal TEXT,
                    pays TEXT,
                    notes TEXT,
                    date_creation TEXT,
                    date_modification TEXT
                )
            ''')
            
            # Création de la table documents
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    titre TEXT NOT NULL,
                    contenu TEXT,
                    client_id INTEGER,
                    date_creation TEXT,
                    date_modification TEXT,
                    FOREIGN KEY (client_id) REFERENCES clients(id)
                )
            ''')
            
            # Création de la table historique
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historique (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    document_id INTEGER,
                    client_id INTEGER,
                    details TEXT,
                    date TEXT,
                    FOREIGN KEY (document_id) REFERENCES documents(id),
                    FOREIGN KEY (client_id) REFERENCES clients(id)
                )
            ''')
            
            # Création de la table modeles
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS modeles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    nom TEXT NOT NULL,
                    contenu TEXT,
                    date_creation TEXT,
                    date_modification TEXT
                )
            ''')
            
            conn.commit()

    def execute_query(self, query, params=None, fetch_one=False):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()

    def execute_update(self, query, params=None):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.lastrowid

class PDFGenerator:
    @staticmethod
    def generate_pdf(document_data, output_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Titre du document
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt=document_data['titre'], ln=1, align='C')
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        
        # Informations sur le client si disponible
        if 'client' in document_data:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt="Client:", ln=1)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"{document_data['client']['nom']} {document_data['client'].get('prenom', '')}", ln=1)
            if document_data['client'].get('societe'):
                pdf.cell(200, 10, txt=f"Société: {document_data['client']['societe']}", ln=1)
            pdf.ln(5)
        
        # Contenu du document
        pdf.multi_cell(0, 10, txt=document_data['contenu'])
        
        # Pied de page
        pdf.set_y(-15)
        pdf.set_font("Arial", 'I', 8)
        #pdf.cell(0, 10, txt=f"Document généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 0, 'C')
        
        pdf.output(output_path)

class EmailSender:
    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, to_email, subject, body, attachment_path=None):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        if attachment_path:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(attachment_path)}",
            )
            msg.attach(part)
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email: {e}")
            return False

class ClientManagerDialog(QDialog):
    def __init__(self, parent=None, client_id=None):
        super().__init__(parent)
        self.client_id = client_id
        self.db = DatabaseManager()
        self.setWindowTitle("Gestion Client" if client_id else "Nouveau Client")
        self.setWindowIcon(qta.icon('fa.user'))
        self.setModal(True)
        self.setMinimumSize(500, 600)
        
        self.init_ui()
        self.load_client_data() if client_id else None

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Formulaire client
        form_layout = QFormLayout()
        
        self.nom_edit = QLineEdit()
        self.prenom_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.telephone_edit = QLineEdit()
        self.societe_edit = QLineEdit()
        self.adresse_edit = QTextEdit()
        self.adresse_edit.setMaximumHeight(80)
        self.ville_edit = QLineEdit()
        self.code_postal_edit = QLineEdit()
        self.pays_edit = QLineEdit()
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        
        form_layout.addRow("Nom*:", self.nom_edit)
        form_layout.addRow("Prénom:", self.prenom_edit)
        form_layout.addRow("Email:", self.email_edit)
        form_layout.addRow("Téléphone:", self.telephone_edit)
        form_layout.addRow("Société:", self.societe_edit)
        form_layout.addRow("Adresse:", self.adresse_edit)
        form_layout.addRow("Ville:", self.ville_edit)
        form_layout.addRow("Code postal:", self.code_postal_edit)
        form_layout.addRow("Pays:", self.pays_edit)
        form_layout.addRow("Notes:", self.notes_edit)
        
        layout.addLayout(form_layout)
        
        # Boutons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton(qta.icon('fa.save'), "Enregistrer")
        self.save_button.clicked.connect(self.save_client)
        self.cancel_button = QPushButton(qta.icon('fa.times'), "Annuler")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def load_client_data(self):
        client_data = self.db.execute_query(
            "SELECT * FROM clients WHERE id = ?", 
            (self.client_id,), 
            fetch_one=True
        )
        
        if client_data:
            columns = [desc[0] for desc in self.db.execute_query("PRAGMA table_info(clients)")]
            client_dict = dict(zip(columns, client_data))
            
            self.nom_edit.setText(client_dict.get('nom', ''))
            self.prenom_edit.setText(client_dict.get('prenom', ''))
            self.email_edit.setText(client_dict.get('email', ''))
            self.telephone_edit.setText(client_dict.get('telephone', ''))
            self.societe_edit.setText(client_dict.get('societe', ''))
            self.adresse_edit.setPlainText(client_dict.get('adresse', ''))
            self.ville_edit.setText(client_dict.get('ville', ''))
            self.code_postal_edit.setText(client_dict.get('code_postal', ''))
            self.pays_edit.setText(client_dict.get('pays', ''))
            self.notes_edit.setPlainText(client_dict.get('notes', ''))

    def save_client(self):
        nom = self.nom_edit.text().strip()
        if not nom:
            QMessageBox.warning(self, "Champ requis", "Le nom du client est obligatoire.")
            return
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        client_data = {
            'nom': nom,
            'prenom': self.prenom_edit.text().strip(),
            'email': self.email_edit.text().strip(),
            'telephone': self.telephone_edit.text().strip(),
            'societe': self.societe_edit.text().strip(),
            'adresse': self.adresse_edit.toPlainText().strip(),
            'ville': self.ville_edit.text().strip(),
            'code_postal': self.code_postal_edit.text().strip(),
            'pays': self.pays_edit.text().strip(),
            'notes': self.notes_edit.toPlainText().strip(),
            'date_modification': now
        }
        
        if self.client_id:
            # Mise à jour du client existant
            query = """UPDATE clients SET 
                        nom = :nom, prenom = :prenom, email = :email, 
                        telephone = :telephone, societe = :societe, adresse = :adresse, 
                        ville = :ville, code_postal = :code_postal, pays = :pays, 
                        notes = :notes, date_modification = :date_modification 
                    WHERE id = ?"""
            params = tuple(client_data.values()) + (self.client_id,)
            self.db.execute_update(query, params)
            
            # Créer le dossier client s'il n'existe pas
            client_folder = os.path.join("clients", f"client_{self.client_id}")
            os.makedirs(client_folder, exist_ok=True)
        else:
            # Création d'un nouveau client
            client_data['date_creation'] = now
            query = """INSERT INTO clients (
                        nom, prenom, email, telephone, societe, adresse, 
                        ville, code_postal, pays, notes, date_creation, date_modification
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            params = tuple(client_data.values()) + (now,)
            client_id = self.db.execute_update(query, params)
            
            # Créer le dossier client
            client_folder = os.path.join("clients", f"client_{client_id}")
            os.makedirs(client_folder, exist_ok=True)
            
            self.client_id = client_id
        
        self.accept()

class DocumentManagerDialog(QDialog):
    def __init__(self, parent=None, document_id=None, client_id=None):
        super().__init__(parent)
        self.document_id = document_id
        self.client_id = client_id
        self.db = DatabaseManager()
        self.setWindowTitle("Modifier Document" if document_id else "Nouveau Document")
        self.setWindowIcon(qta.icon('fa.file-text'))
        self.setModal(True)
        self.setMinimumSize(700, 600)
        
        self.init_ui()
        self.load_document_data() if document_id else None
        self.load_modeles()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Formulaire document
        form_layout = QFormLayout()
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Proforma", "Contrat", "Fiche Technique", "Garantie", "Autre"])
        
        self.titre_edit = QLineEdit()
        self.client_combo = QComboBox()
        self.populate_clients_combo()
        
        self.contenu_edit = QTextEdit()
        
        form_layout.addRow("Type*:", self.type_combo)
        form_layout.addRow("Titre*:", self.titre_edit)
        form_layout.addRow("Client:", self.client_combo)
        form_layout.addRow("Contenu:", self.contenu_edit)
        
        layout.addLayout(form_layout)
        
        # Boutons d'action
        action_layout = QHBoxLayout()
        
        self.template_button = QPushButton(qta.icon('fa.magic'), "Appliquer Modèle")
        self.template_button.clicked.connect(self.apply_template)
        action_layout.addWidget(self.template_button)
        
        self.variables_button = QPushButton(qta.icon('fa.code'), "Insérer Variable")
        self.variables_button.clicked.connect(self.insert_variable)
        action_layout.addWidget(self.variables_button)
        
        layout.addLayout(action_layout)
        
        # Boutons de contrôle
        button_layout = QHBoxLayout()
        self.save_button = QPushButton(qta.icon('fa.save'), "Enregistrer")
        self.save_button.clicked.connect(self.save_document)
        self.cancel_button = QPushButton(qta.icon('fa.times'), "Annuler")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Pré-sélectionner le client si spécifié
        if self.client_id:
            index = self.client_combo.findData(self.client_id)
            if index >= 0:
                self.client_combo.setCurrentIndex(index)

    def populate_clients_combo(self):
        clients = self.db.execute_query("SELECT id, nom, prenom, societe FROM clients ORDER BY nom")
        self.client_combo.addItem("Aucun client", None)
        
        for client in clients:
            client_id, nom, prenom, societe = client
            display_text = f"{nom} {prenom}" + (f" ({societe})" if societe else "")
            self.client_combo.addItem(display_text, client_id)

    def load_modeles(self):
        self.modeles = self.db.execute_query("SELECT id, type, nom FROM modeles")

    def load_document_data(self):
        document_data = self.db.execute_query(
            "SELECT * FROM documents WHERE id = ?", 
            (self.document_id,), 
            fetch_one=True
        )
        
        if document_data:
            columns = [desc[0] for desc in self.db.execute_query("PRAGMA table_info(documents)")]
            document_dict = dict(zip(columns, document_data))
            
            index = self.type_combo.findText(document_dict.get('type', ''))
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
            
            self.titre_edit.setText(document_dict.get('titre', ''))
            
            client_id = document_dict.get('client_id')
            if client_id:
                index = self.client_combo.findData(client_id)
                if index >= 0:
                    self.client_combo.setCurrentIndex(index)
            
            self.contenu_edit.setPlainText(document_dict.get('contenu', ''))

    def apply_template(self):
        if not self.modeles:
            QMessageBox.information(self, "Aucun modèle", "Aucun modèle n'est disponible.")
            return
        
        modele_dialog = QDialog(self)
        modele_dialog.setWindowTitle("Sélectionner un modèle")
        modele_dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        list_widget = QListWidget()
        for modele in self.modeles:
            item = QListWidgetItem(f"{modele[1]} - {modele[2]}")
            item.setData(Qt.UserRole, modele[0])
            list_widget.addItem(item)
        
        layout.addWidget(list_widget)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(modele_dialog.accept)
        button_box.rejected.connect(modele_dialog.reject)
        layout.addWidget(button_box)
        
        modele_dialog.setLayout(layout)
        
        if modele_dialog.exec_() == QDialog.Accepted:
            selected_item = list_widget.currentItem()
            if selected_item:
                modele_id = selected_item.data(Qt.UserRole)
                modele_contenu = self.db.execute_query(
                    "SELECT contenu FROM modeles WHERE id = ?", 
                    (modele_id,), 
                    fetch_one=True
                )[0]
                
                self.contenu_edit.setPlainText(modele_contenu)

    def insert_variable(self):
        variables = [
            ("{{date}}", "Date actuelle"),
            ("{{client.nom}}", "Nom du client"),
            ("{{client.prenom}}", "Prénom du client"),
            ("{{client.societe}}", "Société du client"),
            ("{{client.email}}", "Email du client"),
            ("{{client.telephone}}", "Téléphone du client"),
            ("{{client.adresse}}", "Adresse complète du client"),
        ]
        
        var_dialog = QDialog(self)
        var_dialog.setWindowTitle("Insérer une variable")
        var_dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        list_widget = QListWidget()
        for var, desc in variables:
            item = QListWidgetItem(f"{var} - {desc}")
            item.setData(Qt.UserRole, var)
            list_widget.addItem(item)
        
        layout.addWidget(list_widget)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(var_dialog.accept)
        button_box.rejected.connect(var_dialog.reject)
        layout.addWidget(button_box)
        
        var_dialog.setLayout(layout)
        
        if var_dialog.exec_() == QDialog.Accepted:
            selected_item = list_widget.currentItem()
            if selected_item:
                variable = selected_item.data(Qt.UserRole)
                self.contenu_edit.insertPlainText(variable)

    def save_document(self):
        type_doc = self.type_combo.currentText()
        titre = self.titre_edit.text().strip()
        
        if not type_doc or not titre:
            QMessageBox.warning(self, "Champs requis", "Le type et le titre du document sont obligatoires.")
            return
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_id = self.client_combo.currentData() or None
        
        document_data = {
            'type': type_doc,
            'titre': titre,
            'contenu': self.contenu_edit.toPlainText(),
            'client_id': client_id,
            'date_modification': now
        }
        
        if self.document_id:
            # Mise à jour du document existant
            query = """UPDATE documents SET 
                        type = :type, titre = :titre, contenu = :contenu, 
                        client_id = :client_id, date_modification = :date_modification 
                    WHERE id = ?"""
            params = tuple(document_data.values()) + (self.document_id,)
            self.db.execute_update(query, params)
        else:
            # Création d'un nouveau document
            document_data['date_creation'] = now
            query = """INSERT INTO documents (
                        type, titre, contenu, client_id, date_creation, date_modification
                    ) VALUES (?, ?, ?, ?, ?, ?)"""
            params = tuple(document_data.values()) + (now,)
            self.document_id = self.db.execute_update(query, params)
            
            # Enregistrer dans l'historique
            self.db.execute_update(
                "INSERT INTO historique (action, document_id, client_id, details, date) VALUES (?, ?, ?, ?, ?)",
                ("creation", self.document_id, client_id, f"Création du document {titre}", now)
            )
        
        self.accept()

class ClientsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.init_ui()
        self.load_clients()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Barre d'outils
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        
        self.add_client_action = QAction(qta.icon('fa.user-plus'), "Ajouter Client", self)
        self.add_client_action.triggered.connect(self.add_client)
        toolbar.addAction(self.add_client_action)
        
        self.edit_client_action = QAction(qta.icon('fa.edit'), "Modifier Client", self)
        self.edit_client_action.triggered.connect(self.edit_client)
        toolbar.addAction(self.edit_client_action)
        
        self.delete_client_action = QAction(qta.icon('fa.trash'), "Supprimer Client", self)
        self.delete_client_action.triggered.connect(self.delete_client)
        toolbar.addAction(self.delete_client_action)
        
        toolbar.addSeparator()
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Rechercher client...")
        self.search_edit.textChanged.connect(self.load_clients)
        search_action = QWidgetAction(self)
        search_action.setDefaultWidget(self.search_edit)
        toolbar.addAction(search_action)
        
        layout.addWidget(toolbar)
        
        # Tableau des clients
        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(6)
        self.clients_table.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Société", "Email", "Téléphone"])
        self.clients_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.clients_table.verticalHeader().setVisible(False)
        self.clients_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.clients_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.clients_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        layout.addWidget(self.clients_table)
        
        self.setLayout(layout)

    def load_clients(self, search_term=None):
        query = "SELECT id, nom, prenom, societe, email, telephone FROM clients"
        params = None
        
        if search_term and search_term.strip():
            query += " WHERE nom LIKE ? OR prenom LIKE ? OR societe LIKE ? OR email LIKE ?"
            search_param = f"%{search_term.strip()}%"
            params = (search_param, search_param, search_param, search_param)
        
        query += " ORDER BY nom, prenom"
        
        clients = self.db.execute_query(query, params)
        
        self.clients_table.setRowCount(len(clients))
        
        for row_idx, client in enumerate(clients):
            for col_idx, value in enumerate(client):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.clients_table.setItem(row_idx, col_idx, item)

    def add_client(self):
        dialog = ClientManagerDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_clients(self.search_edit.text())

    def edit_client(self):
        selected_row = self.clients_table.currentRow()
        if selected_row >= 0:
            client_id = int(self.clients_table.item(selected_row, 0).text())
            dialog = ClientManagerDialog(self, client_id)
            if dialog.exec_() == QDialog.Accepted:
                self.load_clients(self.search_edit.text())

    def delete_client(self):
        selected_row = self.clients_table.currentRow()
        if selected_row >= 0:
            client_id = int(self.clients_table.item(selected_row, 0).text())
            client_name = self.clients_table.item(selected_row, 1).text()
            
            reply = QMessageBox.question(
                self, 
                "Confirmation", 
                f"Êtes-vous sûr de vouloir supprimer le client {client_name} ?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Vérifier si le client a des documents associés
                has_documents = self.db.execute_query(
                    "SELECT COUNT(*) FROM documents WHERE client_id = ?", 
                    (client_id,), 
                    fetch_one=True
                )[0]
                
                if has_documents > 0:
                    QMessageBox.warning(
                        self, 
                        "Impossible de supprimer", 
                        "Ce client a des documents associés. Veuillez d'abord supprimer ou réaffecter ces documents."
                    )
                    return
                
                self.db.execute_update("DELETE FROM clients WHERE id = ?", (client_id,))
                self.load_clients(self.search_edit.text())

class DocumentsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.init_ui()
        self.load_documents()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Barre d'outils
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        
        self.add_doc_action = QAction(qta.icon('fa.file-text-o'), "Nouveau Document", self)
        self.add_doc_action.triggered.connect(self.add_document)
        toolbar.addAction(self.add_doc_action)
        
        self.edit_doc_action = QAction(qta.icon('fa.edit'), "Modifier Document", self)
        self.edit_doc_action.triggered.connect(self.edit_document)
        toolbar.addAction(self.edit_doc_action)
        
        self.delete_doc_action = QAction(qta.icon('fa.trash'), "Supprimer Document", self)
        self.delete_doc_action.triggered.connect(self.delete_document)
        toolbar.addAction(self.delete_doc_action)
        
        toolbar.addSeparator()
        
        self.export_pdf_action = QAction(qta.icon('fa.file-pdf-o'), "Exporter PDF", self)
        self.export_pdf_action.triggered.connect(self.export_to_pdf)
        toolbar.addAction(self.export_pdf_action)
        
        self.send_email_action = QAction(qta.icon('fa.send'), "Envoyer par Email", self)
        self.send_email_action.triggered.connect(self.send_by_email)
        toolbar.addAction(self.send_email_action)
        
        self.send_whatsapp_action = QAction(qta.icon('fa.whatsapp'), "Envoyer par WhatsApp", self)
        self.send_whatsapp_action.triggered.connect(self.send_by_whatsapp)
        toolbar.addAction(self.send_whatsapp_action)
        
        toolbar.addSeparator()
        
        # Filtres
        filter_layout = QHBoxLayout()
        
        self.type_filter = QComboBox()
        self.type_filter.addItem("Tous les types", None)
        self.type_filter.addItem("Proforma", "Proforma")
        self.type_filter.addItem("Contrat", "Contrat")
        self.type_filter.addItem("Fiche Technique", "Fiche Technique")
        self.type_filter.addItem("Garantie", "Garantie")
        self.type_filter.currentIndexChanged.connect(self.load_documents)
        
        self.client_filter = QComboBox()
        self.client_filter.addItem("Tous les clients", None)
        self.populate_client_filter()
        self.client_filter.currentIndexChanged.connect(self.load_documents)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Rechercher document...")
        self.search_edit.textChanged.connect(self.load_documents)
        
        filter_layout.addWidget(QLabel("Type:"))
        filter_layout.addWidget(self.type_filter)
        filter_layout.addWidget(QLabel("Client:"))
        filter_layout.addWidget(self.client_filter)
        filter_layout.addWidget(self.search_edit)
        filter_layout.addStretch()
        
        filter_widget = QWidget()
        filter_widget.setLayout(filter_layout)
        toolbar.addWidget(filter_widget)
        
        layout.addWidget(toolbar)
        
        # Tableau des documents
        self.documents_table = QTableWidget()
        self.documents_table.setColumnCount(6)
        self.documents_table.setHorizontalHeaderLabels(["ID", "Type", "Titre", "Client", "Créé le", "Modifié le"])
        self.documents_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.documents_table.verticalHeader().setVisible(False)
        self.documents_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.documents_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.documents_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        layout.addWidget(self.documents_table)
        
        self.setLayout(layout)

    def populate_client_filter(self):
        clients = self.db.execute_query("SELECT id, nom, prenom, societe FROM clients ORDER BY nom")
        for client in clients:
            client_id, nom, prenom, societe = client
            display_text = f"{nom} {prenom}" + (f" ({societe})" if societe else "")
            self.client_filter.addItem(display_text, client_id)

    def load_documents(self):
        type_filter = self.type_filter.currentData()
        client_filter = self.client_filter.currentData()
        search_term = self.search_edit.text().strip()
        
        query = """SELECT d.id, d.type, d.titre, 
                          CASE WHEN c.id IS NULL THEN 'Aucun' 
                               ELSE c.nom || COALESCE(' ' || c.prenom, '') || COALESCE(' (' || c.societe || ')', '') 
                          END as client_name,
                          d.date_creation, d.date_modification
                   FROM documents d
                   LEFT JOIN clients c ON d.client_id = c.id
                   WHERE 1=1"""
        
        params = []
        
        if type_filter:
            query += " AND d.type = ?"
            params.append(type_filter)
        
        if client_filter:
            query += " AND d.client_id = ?"
            params.append(client_filter)
        
        if search_term:
            query += " AND (d.titre LIKE ? OR d.type LIKE ? OR d.contenu LIKE ?)"
            search_param = f"%{search_term}%"
            params.extend([search_param, search_param, search_param])
        
        query += " ORDER BY d.date_modification DESC"
        
        documents = self.db.execute_query(query, params)
        
        self.documents_table.setRowCount(len(documents))
        
        for row_idx, doc in enumerate(documents):
            for col_idx, value in enumerate(doc):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.documents_table.setItem(row_idx, col_idx, item)

    def add_document(self):
        dialog = DocumentManagerDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_documents()

    def edit_document(self):
        selected_row = self.documents_table.currentRow()
        if selected_row >= 0:
            doc_id = int(self.documents_table.item(selected_row, 0).text())
            dialog = DocumentManagerDialog(self, doc_id)
            if dialog.exec_() == QDialog.Accepted:
                self.load_documents()

    def delete_document(self):
        selected_row = self.documents_table.currentRow()
        if selected_row >= 0:
            doc_id = int(self.documents_table.item(selected_row, 0).text())
            doc_title = self.documents_table.item(selected_row, 2).text()
            
            reply = QMessageBox.question(
                self, 
                "Confirmation", 
                f"Êtes-vous sûr de vouloir supprimer le document '{doc_title}' ?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.db.execute_update("DELETE FROM documents WHERE id = ?", (doc_id,))
                self.load_documents()

    def export_to_pdf(self):
        selected_row = self.documents_table.currentRow()
        if selected_row >= 0:
            doc_id = int(self.documents_table.item(selected_row, 0).text())
            
            # Récupérer les données du document
            doc_data = self.db.execute_query(
                """SELECT d.id, d.type, d.titre, d.contenu, 
                          c.id as client_id, c.nom, c.prenom, c.societe, c.email, c.telephone, 
                          c.adresse, c.ville, c.code_postal, c.pays
                   FROM documents d
                   LEFT JOIN clients c ON d.client_id = c.id
                   WHERE d.id = ?""", 
                (doc_id,), 
                fetch_one=True
            )
            
            if doc_data:
                columns = [desc[0] for desc in self.db.execute_query("PRAGMA table_info(documents)")] + \
                         [desc[0] for desc in self.db.execute_query("PRAGMA table_info(clients)")][4:]
                
                doc_dict = dict(zip(columns, doc_data))
                
                # Préparer les données pour le PDF
                pdf_data = {
                    'titre': doc_dict['titre'],
                    'contenu': doc_dict['contenu']
                }
                
                if doc_dict.get('client_id'):
                    pdf_data['client'] = {
                        'nom': doc_dict['nom'],
                        'prenom': doc_dict['prenom'],
                        'societe': doc_dict['societe'],
                        'email': doc_dict['email'],
                        'telephone': doc_dict['telephone'],
                        'adresse': f"{doc_dict['adresse']}, {doc_dict['code_postal']} {doc_dict['ville']}, {doc_dict['pays']}"
                    }
                
                # Demander où sauvegarder le PDF
                file_path, _ = QFileDialog.getSaveFileName(
                    self, 
                    "Exporter en PDF", 
                    f"{doc_dict['titre']}.pdf", 
                    "Fichiers PDF (*.pdf)"
                )
                
                if file_path:
                    PDFGenerator.generate_pdf(pdf_data, file_path)
                    QMessageBox.information(self, "Export réussi", f"Le document a été exporté en PDF avec succès:\n{file_path}")

    def send_by_email(self):
        selected_row = self.documents_table.currentRow()
        if selected_row >= 0:
            doc_id = int(self.documents_table.item(selected_row, 0).text())
            
            # Récupérer les données du document
            doc_data = self.db.execute_query(
                """SELECT d.id, d.type, d.titre, d.contenu, 
                          c.id as client_id, c.nom, c.prenom, c.societe, c.email
                   FROM documents d
                   LEFT JOIN clients c ON d.client_id = c.id
                   WHERE d.id = ?""", 
                (doc_id,), 
                fetch_one=True
            )
            
            if doc_data:
                columns = [desc[0] for desc in self.db.execute_query("PRAGMA table_info(documents)")] + \
                         [desc[0] for desc in self.db.execute_query("PRAGMA table_info(clients)")][4:]
                
                doc_dict = dict(zip(columns, doc_data))
                
                # Vérifier si on a un email de client
                client_email = doc_dict.get('email')
                
                # Demander les paramètres d'email
                dialog = EmailDialog(self, client_email, doc_dict['titre'])
                if dialog.exec_() == QDialog.Accepted:
                    email, subject, body = dialog.get_email_data()
                    
                    # Générer un PDF temporaire
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
                        pdf_data = {
                            'titre': doc_dict['titre'],
                            'contenu': doc_dict['contenu']
                        }
                        
                        if doc_dict.get('client_id'):
                            pdf_data['client'] = {
                                'nom': doc_dict['nom'],
                                'prenom': doc_dict['prenom'],
                                'societe': doc_dict['societe']
                            }
                        
                        PDFGenerator.generate_pdf(pdf_data, temp_pdf.name)
                        
                        # Envoyer l'email
                        email_sender = EmailSender(
                            smtp_server="smtp.example.com",
                            smtp_port=587,
                            username="votre@email.com",
                            password="votre_mot_de_passe"
                        )
                        
                        if email_sender.send_email(email, subject, body, temp_pdf.name):
                            QMessageBox.information(self, "Email envoyé", "Le document a été envoyé par email avec succès.")
                            
                            # Enregistrer dans l'historique
                            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            self.db.execute_update(
                                "INSERT INTO historique (action, document_id, client_id, details, date) VALUES (?, ?, ?, ?, ?)",
                                ("email", doc_id, doc_dict.get('client_id'), f"Document envoyé par email à {email}", now)
                            )
                        else:
                            QMessageBox.warning(self, "Erreur", "Une erreur est survenue lors de l'envoi de l'email.")
                    
                    # Supprimer le fichier temporaire
                    try:
                        os.unlink(temp_pdf.name)
                    except:
                        pass

    def send_by_whatsapp(self):
        selected_row = self.documents_table.currentRow()
        if selected_row >= 0:
            doc_id = int(self.documents_table.item(selected_row, 0).text())
            
            # Récupérer les données du document
            doc_data = self.db.execute_query(
                """SELECT d.id, d.type, d.titre, d.contenu, 
                          c.id as client_id, c.nom, c.prenom, c.telephone
                   FROM documents d
                   LEFT JOIN clients c ON d.client_id = c.id
                   WHERE d.id = ?""", 
                (doc_id,), 
                fetch_one=True
            )
            
            if doc_data:
                columns = [desc[0] for desc in self.db.execute_query("PRAGMA table_info(documents)")] + \
                         [desc[0] for desc in self.db.execute_query("PRAGMA table_info(clients)")][4:]
                
                doc_dict = dict(zip(columns, doc_data))
                
                # Vérifier si on a un téléphone de client
                client_phone = doc_dict.get('telephone')
                
                if client_phone:
                    # Nettoyer le numéro de téléphone
                    clean_phone = ''.join(filter(str.isdigit, client_phone))
                    
                    # Générer un PDF temporaire
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
                        pdf_data = {
                            'titre': doc_dict['titre'],
                            'contenu': doc_dict['contenu']
                        }
                        
                        if doc_dict.get('client_id'):
                            pdf_data['client'] = {
                                'nom': doc_dict['nom'],
                                'prenom': doc_dict['prenom']
                            }
                        
                        PDFGenerator.generate_pdf(pdf_data, temp_pdf.name)
                        
                        # Essayer d'ouvrir WhatsApp avec le PDF
                        try:
                            # Note: Cette partie est théorique, l'envoi réel de fichiers via WhatsApp Web n'est pas direct
                            # Dans une application réelle, vous utiliseriez une API WhatsApp Business
                            whatsapp_url = f"https://wa.me/{clean_phone}?text=Voici%20votre%20document%20{doc_dict['titre']}"
                            webbrowser.open(whatsapp_url)
                            
                            # Enregistrer dans l'historique
                            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            self.db.execute_update(
                                "INSERT INTO historique (action, document_id, client_id, details, date) VALUES (?, ?, ?, ?, ?)",
                                ("whatsapp", doc_id, doc_dict.get('client_id'), f"Document envoyé par WhatsApp au {client_phone}", now)
                            )
                        except Exception as e:
                            QMessageBox.warning(self, "Erreur", f"Impossible d'ouvrir WhatsApp: {e}")
                else:
                    QMessageBox.warning(self, "Information manquante", "Aucun numéro de téléphone n'est associé à ce document ou client.")

class EmailDialog(QDialog):
    def __init__(self, parent=None, default_email=None, doc_title=None):
        super().__init__(parent)
        self.setWindowTitle("Envoyer par Email")
        self.setWindowIcon(qta.icon('fa.send'))
        self.setModal(True)
        self.setMinimumSize(400, 300)
        
        self.init_ui(default_email, doc_title)

    def init_ui(self, default_email, doc_title):
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.email_edit = QLineEdit(default_email if default_email else "")
        self.subject_edit = QLineEdit(f"Document: {doc_title}" if doc_title else "")
        self.body_edit = QTextEdit()
        self.body_edit.setPlainText("Bonjour,\n\nVeuillez trouver ci-joint le document demandé.\n\nCordialement,")
        
        form_layout.addRow("Email du destinataire*:", self.email_edit)
        form_layout.addRow("Sujet*:", self.subject_edit)
        form_layout.addRow("Message:", self.body_edit)
        
        layout.addLayout(form_layout)
        
        # Boutons
        button_layout = QHBoxLayout()
        self.send_button = QPushButton(qta.icon('fa.send'), "Envoyer")
        self.send_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton(qta.icon('fa.times'), "Annuler")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def get_email_data(self):
        return (
            self.email_edit.text().strip(),
            self.subject_edit.text().strip(),
            self.body_edit.toPlainText().strip()
        )

class HistoryTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.init_ui()
        self.load_history()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Barre d'outils
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        
        self.refresh_action = QAction(qta.icon('fa.refresh'), "Actualiser", self)
        self.refresh_action.triggered.connect(self.load_history)
        toolbar.addAction(self.refresh_action)
        
        self.clear_action = QAction(qta.icon('fa.trash'), "Effacer l'historique", self)
        self.clear_action.triggered.connect(self.clear_history)
        toolbar.addAction(self.clear_action)
        
        toolbar.addSeparator()
        
        self.date_filter = QDateEdit()
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.setCalendarPopup(True)
        self.date_filter.dateChanged.connect(self.load_history)
        
        self.show_all_check = QAction(qta.icon('fa.list'), "Tout afficher", self)
        self.show_all_check.setCheckable(True)
        self.show_all_check.setChecked(True)
        self.show_all_check.triggered.connect(self.toggle_date_filter)
        
        toolbar.addWidget(QLabel("Filtrer par date:"))
        toolbar.addWidget(self.date_filter)
        toolbar.addAction(self.show_all_check)
        
        layout.addWidget(toolbar)
        
        # Tableau de l'historique
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Date", "Action", "Document", "Client", "Détails"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.history_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        layout.addWidget(self.history_table)
        
        self.setLayout(layout)

    def toggle_date_filter(self):
        self.date_filter.setEnabled(not self.show_all_check.isChecked())
        self.load_history()

    def load_history(self):
        if self.show_all_check.isChecked():
            query = """SELECT h.date, h.action, 
                               COALESCE(d.titre, 'N/A') as document_titre,
                               COALESCE(c.nom || COALESCE(' ' || c.prenom, ''), 'N/A') as client_name,
                               h.details
                        FROM historique h
                        LEFT JOIN documents d ON h.document_id = d.id
                        LEFT JOIN clients c ON h.client_id = c.id
                        ORDER BY h.date DESC"""
            params = None
        else:
            selected_date = self.date_filter.date().toString("yyyy-MM-dd")
            query = """SELECT h.date, h.action, 
                               COALESCE(d.titre, 'N/A') as document_titre,
                               COALESCE(c.nom || COALESCE(' ' || c.prenom, ''), 'N/A') as client_name,
                               h.details
                        FROM historique h
                        LEFT JOIN documents d ON h.document_id = d.id
                        LEFT JOIN clients c ON h.client_id = c.id
                        WHERE DATE(h.date) = ?
                        ORDER BY h.date DESC"""
            params = (selected_date,)
        
        history = self.db.execute_query(query, params)
        
        self.history_table.setRowCount(len(history))
        
        for row_idx, record in enumerate(history):
            for col_idx, value in enumerate(record):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.history_table.setItem(row_idx, col_idx, item)

    def clear_history(self):
        reply = QMessageBox.question(
            self, 
            "Confirmation", 
            "Êtes-vous sûr de vouloir effacer tout l'historique ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.execute_update("DELETE FROM historique")
            self.load_history()

class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Onglets
        tabs = QTabWidget()
        
        # Onglet Paramètres généraux
        general_tab = QWidget()
        general_layout = QFormLayout()
        
        self.company_name = QLineEdit()
        self.company_address = QTextEdit()
        self.company_address.setMaximumHeight(80)
        self.company_phone = QLineEdit()
        self.company_email = QLineEdit()
        self.company_logo = QLabel()
        self.company_logo.setAlignment(Qt.AlignCenter)
        self.company_logo.setFixedSize(150, 150)
        self.company_logo.setStyleSheet("border: 1px solid #ddd; background-color: white;")
        
        self.browse_logo_btn = QPushButton("Parcourir...")
        self.browse_logo_btn.clicked.connect(self.browse_logo)
        
        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.company_logo)
        logo_layout.addWidget(self.browse_logo_btn)
        logo_layout.addStretch()
        
        general_layout.addRow("Nom de l'entreprise:", self.company_name)
        general_layout.addRow("Adresse:", self.company_address)
        general_layout.addRow("Téléphone:", self.company_phone)
        general_layout.addRow("Email:", self.company_email)
        general_layout.addRow("Logo:", logo_layout)
        
        general_tab.setLayout(general_layout)
        tabs.addTab(general_tab, "Général")
        
        # Onglet Paramètres email
        email_tab = QWidget()
        email_layout = QFormLayout()
        
        self.smtp_server = QLineEdit()
        self.smtp_port = QLineEdit()
        self.smtp_username = QLineEdit()
        self.smtp_password = QLineEdit()
        self.smtp_password.setEchoMode(QLineEdit.Password)
        
        email_layout.addRow("Serveur SMTP:", self.smtp_server)
        email_layout.addRow("Port SMTP:", self.smtp_port)
        email_layout.addRow("Nom d'utilisateur:", self.smtp_username)
        email_layout.addRow("Mot de passe:", self.smtp_password)
        
        email_tab.setLayout(email_layout)
        tabs.addTab(email_tab, "Email")
        
        # Onglet Modèles de documents
        templates_tab = QWidget()
        templates_layout = QVBoxLayout()
        
        self.templates_table = QTableWidget()
        self.templates_table.setColumnCount(3)
        self.templates_table.setHorizontalHeaderLabels(["Type", "Nom", "Dernière modification"])
        self.templates_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.templates_table.verticalHeader().setVisible(False)
        self.templates_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.templates_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.templates_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        templates_toolbar = QToolBar()
        templates_toolbar.setIconSize(QSize(24, 24))
        
        self.add_template_action = QAction(qta.icon('fa.plus'), "Ajouter Modèle", self)
        self.add_template_action.triggered.connect(self.add_template)
        templates_toolbar.addAction(self.add_template_action)
        
        self.edit_template_action = QAction(qta.icon('fa.edit'), "Modifier Modèle", self)
        self.edit_template_action.triggered.connect(self.edit_template)
        templates_toolbar.addAction(self.edit_template_action)
        
        self.delete_template_action = QAction(qta.icon('fa.trash'), "Supprimer Modèle", self)
        self.delete_template_action.triggered.connect(self.delete_template)
        templates_toolbar.addAction(self.delete_template_action)
        
        templates_layout.addWidget(templates_toolbar)
        templates_layout.addWidget(self.templates_table)
        
        templates_tab.setLayout(templates_layout)
        tabs.addTab(templates_tab, "Modèles")
        
        layout.addWidget(tabs)
        
        # Boutons de sauvegarde
        button_layout = QHBoxLayout()
        self.save_button = QPushButton(qta.icon('fa.save'), "Enregistrer les paramètres")
        self.save_button.clicked.connect(self.save_settings)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Charger les modèles
        self.load_templates()

    def browse_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Sélectionner un logo", 
            "", 
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # Redimensionner tout en conservant le ratio
                pixmap = pixmap.scaled(
                    self.company_logo.size(), 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                self.company_logo.setPixmap(pixmap)
                self.logo_path = file_path

    def load_settings(self):
        # Ici, vous chargeriez normalement les paramètres depuis une table de configuration
        # Pour cet exemple, nous utilisons des valeurs par défaut
        self.company_name.setText("Ma Société")
        self.company_address.setPlainText("123 Rue Principale\n75000 Paris")
        self.company_phone.setText("+33 1 23 45 67 89")
        self.company_email.setText("contact@masociete.com")
        
        # Paramètres SMTP par défaut
        self.smtp_server.setText("smtp.example.com")
        self.smtp_port.setText("587")
        self.smtp_username.setText("votre@email.com")
        self.smtp_password.setText("votre_mot_de_passe")

    def load_templates(self):
        templates = self.db.execute_query("SELECT id, type, nom, date_modification FROM modeles ORDER BY type, nom")
        self.templates_table.setRowCount(len(templates))
        
        for row_idx, template in enumerate(templates):
            for col_idx, value in enumerate(template[1:]):  # On saute l'ID
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.templates_table.setItem(row_idx, col_idx, item)
                
                # Stocker l'ID dans la dernière colonne (cachée)
                if col_idx == 2:  # Quand on arrive à la dernière colonne visible
                    item.setData(Qt.UserRole, template[0])

    def add_template(self):
        dialog = TemplateDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            type_doc, name, content = dialog.get_template_data()
            
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.execute_update(
                "INSERT INTO modeles (type, nom, contenu, date_creation, date_modification) VALUES (?, ?, ?, ?, ?)",
                (type_doc, name, content, now, now)
            )
            
            self.load_templates()

    def edit_template(self):
        selected_row = self.templates_table.currentRow()
        if selected_row >= 0:
            template_id = self.templates_table.item(selected_row, 2).data(Qt.UserRole)
            
            template_data = self.db.execute_query(
                "SELECT type, nom, contenu FROM modeles WHERE id = ?", 
                (template_id,), 
                fetch_one=True
            )
            
            if template_data:
                dialog = TemplateDialog(self, template_data)
                if dialog.exec_() == QDialog.Accepted:
                    type_doc, name, content = dialog.get_template_data()
                    
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.db.execute_update(
                        "UPDATE modeles SET type = ?, nom = ?, contenu = ?, date_modification = ? WHERE id = ?",
                        (type_doc, name, content, now, template_id)
                    )
                    
                    self.load_templates()

    def delete_template(self):
        selected_row = self.templates_table.currentRow()
        if selected_row >= 0:
            template_id = self.templates_table.item(selected_row, 2).data(Qt.UserRole)
            template_name = self.templates_table.item(selected_row, 1).text()
            
            reply = QMessageBox.question(
                self, 
                "Confirmation", 
                f"Êtes-vous sûr de vouloir supprimer le modèle '{template_name}' ?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.db.execute_update("DELETE FROM modeles WHERE id = ?", (template_id,))
                self.load_templates()

    def save_settings(self):
        # Ici, vous enregistreriez normalement les paramètres dans une table de configuration
        QMessageBox.information(self, "Paramètres enregistrés", "Les paramètres ont été enregistrés avec succès.")

class TemplateDialog(QDialog):
    def __init__(self, parent=None, template_data=None):
        super().__init__(parent)
        self.setWindowTitle("Modifier Modèle" if template_data else "Nouveau Modèle")
        self.setWindowIcon(qta.icon('fa.file-text-o'))
        self.setModal(True)
        self.setMinimumSize(600, 500)
        
        self.init_ui()
        if template_data:
            self.load_template_data(template_data)

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Formulaire modèle
        form_layout = QFormLayout()
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Proforma", "Contrat", "Fiche Technique", "Garantie", "Autre"])
        
        self.name_edit = QLineEdit()
        self.content_edit = QTextEdit()
        
        form_layout.addRow("Type*:", self.type_combo)
        form_layout.addRow("Nom*:", self.name_edit)
        form_layout.addRow("Contenu:", self.content_edit)
        
        layout.addLayout(form_layout)
        
        # Boutons variables
        var_layout = QHBoxLayout()
        
        variables = [
            ("{{date}}", "Date actuelle"),
            ("{{client.nom}}", "Nom du client"),
            ("{{client.prenom}}", "Prénom du client"),
            ("{{client.societe}}", "Société du client"),
            ("{{client.email}}", "Email du client"),
            ("{{client.telephone}}", "Téléphone du client"),
            ("{{client.adresse}}", "Adresse complète du client"),
            ("{{entreprise.nom}}", "Nom de votre entreprise"),
            ("{{entreprise.adresse}}", "Adresse de votre entreprise"),
            ("{{entreprise.telephone}}", "Téléphone de votre entreprise"),
        ]
        
        self.var_combo = QComboBox()
        for var, desc in variables:
            self.var_combo.addItem(f"{var} - {desc}", var)
        
        insert_var_btn = QPushButton("Insérer Variable")
        insert_var_btn.clicked.connect(self.insert_variable)
        
        var_layout.addWidget(self.var_combo)
        var_layout.addWidget(insert_var_btn)
        var_layout.addStretch()
        
        layout.addLayout(var_layout)
        
        # Boutons de contrôle
        button_layout = QHBoxLayout()
        self.save_button = QPushButton(qta.icon('fa.save'), "Enregistrer")
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton(qta.icon('fa.times'), "Annuler")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def load_template_data(self, template_data):
        type_doc, name, content = template_data
        index = self.type_combo.findText(type_doc)
        if index >= 0:
            self.type_combo.setCurrentIndex(index)
        
        self.name_edit.setText(name)
        self.content_edit.setPlainText(content)

    def insert_variable(self):
        variable = self.var_combo.currentData()
        if variable:
            self.content_edit.insertPlainText(variable)

    def get_template_data(self):
        return (
            self.type_combo.currentText(),
            self.name_edit.text().strip(),
            self.content_edit.toPlainText()
        )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{VERSION}")
        self.setWindowIcon(qta.icon('fa.folder-open'))
        self.setMinimumSize(1000, 700)
        
        self.db = DatabaseManager()
        self.init_ui()
        
        # Créer le dossier clients s'il n'existe pas
        os.makedirs("clients", exist_ok=True)

    def init_ui(self):
        # Barre de menu
        self.create_menu_bar()
        
        # Barre d'outils
        self.create_tool_bar()
        
        # Barre de statut
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Barre latérale
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.addItems(["Documents", "Clients", "Historique", "Paramètres"])
        self.sidebar.setCurrentRow(0)
        self.sidebar.currentRowChanged.connect(self.change_tab)
        
        # Icônes pour la barre latérale
        for i, icon in enumerate([qta.icon('fa.files-o'), qta.icon('fa.users'), qta.icon('fa.history'), qta.icon('fa.cog')]):
            self.sidebar.item(i).setIcon(icon)
        
        main_layout.addWidget(self.sidebar)
        
        # Zone de contenu
        self.content_area = QStackedWidget()
        
        # Onglets
        self.docs_tab = DocumentsTab()
        self.clients_tab = ClientsTab()
        self.history_tab = HistoryTab()
        self.settings_tab = SettingsTab()
        
        self.content_area.addWidget(self.docs_tab)
        self.content_area.addWidget(self.clients_tab)
        self.content_area.addWidget(self.history_tab)
        self.content_area.addWidget(self.settings_tab)
        
        main_layout.addWidget(self.content_area, 1)

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # Menu Fichier
        file_menu = menu_bar.addMenu("Fichier")
        
        new_doc_action = QAction(qta.icon('fa.file-o'), "Nouveau Document", self)
        new_doc_action.triggered.connect(self.docs_tab.add_document)
        file_menu.addAction(new_doc_action)
        
        new_client_action = QAction(qta.icon('fa.user-plus'), "Nouveau Client", self)
        new_client_action.triggered.connect(self.clients_tab.add_client)
        file_menu.addAction(new_client_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(qta.icon('fa.power-off'), "Quitter", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Outils
        tools_menu = menu_bar.addMenu("Outils")
        
        backup_action = QAction(qta.icon('fa.database'), "Sauvegarde de la base", self)
        backup_action.triggered.connect(self.backup_database)
        tools_menu.addAction(backup_action)
        
        restore_action = QAction(qta.icon('fa.undo'), "Restaurer base", self)
        restore_action.triggered.connect(self.restore_database)
        tools_menu.addAction(restore_action)
        
        # Menu Aide
        help_menu = menu_bar.addMenu("Aide")
        
        about_action = QAction(qta.icon('fa.info-circle'), "À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_tool_bar(self):
        tool_bar = self.addToolBar("Outils")
        tool_bar.setIconSize(QSize(24, 24))
        
        # Boutons en fonction de l'onglet actif
        self.active_toolbar_actions = []
        
        # Documents
        docs_actions = [
            (qta.icon('fa.file-text-o'), "Nouveau Document", self.docs_tab.add_document),
            (qta.icon('fa.edit'), "Modifier Document", self.docs_tab.edit_document),
            (qta.icon('fa.trash'), "Supprimer Document", self.docs_tab.delete_document),
            (qta.icon('fa.file-pdf-o'), "Exporter PDF", self.docs_tab.export_to_pdf),
            (qta.icon('fa.send'), "Envoyer par Email", self.docs_tab.send_by_email),
            (qta.icon('fa.whatsapp'), "Envoyer par WhatsApp", self.docs_tab.send_by_whatsapp)
        ]
        
        # Clients
        clients_actions = [
            (qta.icon('fa.user-plus'), "Ajouter Client", self.clients_tab.add_client),
            (qta.icon('fa.edit'), "Modifier Client", self.clients_tab.edit_client),
            (qta.icon('fa.trash'), "Supprimer Client", self.clients_tab.delete_client)
        ]
        
        # Historique
        history_actions = [
            (qta.icon('fa.refresh'), "Actualiser", self.history_tab.load_history),
            (qta.icon('fa.trash'), "Effacer Historique", self.history_tab.clear_history)
        ]
        
        # Paramètres
        settings_actions = [
            (qta.icon('fa.save'), "Enregistrer", self.settings_tab.save_settings)
        ]
        
        self.all_toolbar_actions = {
            0: docs_actions,
            1: clients_actions,
            2: history_actions,
            3: settings_actions
        }
        
        # Initialiser avec les actions du premier onglet
        self.update_toolbar(0)

    def update_toolbar(self, tab_index):
        # Supprimer les anciennes actions
        for action in self.active_toolbar_actions:
            self.removeAction(action)
        self.active_toolbar_actions.clear()
        
        # Ajouter les nouvelles actions
        for icon, text, callback in self.all_toolbar_actions.get(tab_index, []):
            action = QAction(icon, text, self)
            action.triggered.connect(callback)
            self.addAction(action)
            self.active_toolbar_actions.append(action)
            
            # Ajouter à la barre d'outils si elle existe
            for toolbar in self.findChildren(QToolBar):
                toolbar.addAction(action)

    def change_tab(self, index):
        self.content_area.setCurrentIndex(index)
        self.update_toolbar(index)
        
        # Mettre à jour le statut
        tabs = ["Documents", "Clients", "Historique", "Paramètres"]
        self.status_bar.showMessage(f"Module {tabs[index]} actif")

    def backup_database(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Sauvegarde de la base de données", 
            f"backup_{datetime.now().strftime('%Y%m%d')}.db", 
            "Fichiers SQLite (*.db *.sqlite)"
        )
        
        if file_path:
            try:
                with open(DB_NAME, 'rb') as f_src, open(file_path, 'wb') as f_dst:
                    f_dst.write(f_src.read())
                QMessageBox.information(self, "Sauvegarde réussie", f"La base de données a été sauvegardée avec succès dans:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de la sauvegarde:\n{str(e)}")

    def restore_database(self):
        reply = QMessageBox.warning(
            self, 
            "Confirmation", 
            "Êtes-vous sûr de vouloir restaurer une sauvegarde ?\nCette action écrasera la base de données actuelle.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            file_path, _ = QFileDialog.getOpenFileName(
                self, 
                "Restaurer la base de données", 
                "", 
                "Fichiers SQLite (*.db *.sqlite)"
            )
            
            if file_path:
                try:
                    # Fermer la connexion actuelle
                    self.db = None
                    
                    # Remplacer la base de données
                    with open(file_path, 'rb') as f_src, open(DB_NAME, 'wb') as f_dst:
                        f_dst.write(f_src.read())
                    
                    # Rétablir la connexion
                    self.db = DatabaseManager()
                    
                    # Recharger les données
                    self.docs_tab.load_documents()
                    self.clients_tab.load_clients()
                    self.history_tab.load_history()
                    
                    QMessageBox.information(self, "Restauration réussie", "La base de données a été restaurée avec succès.")
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de la restauration:\n{str(e)}")
                    self.db = DatabaseManager()

    def show_about(self):
        about_text = f"""
        <h2>{APP_NAME} v{VERSION}</h2>
        <p>Gestionnaire de documents professionnels</p>
        <p>Développé avec Python et PyQt</p>
        <p>© {datetime.now().year} - Tous droits réservés</p>
        <p><small>Version: {VERSION}</small></p>
        """
        QMessageBox.about(self, "À propos", about_text)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 
            "Confirmation", 
            "Êtes-vous sûr de vouloir quitter l'application ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    
    # Vérifier et créer le dossier clients s'il n'existe pas
    if not os.path.exists("clients"):
        os.makedirs("clients")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())