import os
import sys
import sqlite3
from datetime import datetime
from PyQt5.QtCore import Qt, QSize, QDate, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPainter
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QListWidget, QTableWidget, 
                             QTableWidgetItem, QLineEdit, QTextEdit, QComboBox, QDateEdit, 
                             QFileDialog, QMessageBox, QHeaderView, QFormLayout, QTabWidget,
                             QAbstractItemView, QToolBar, QStatusBar, QAction, QDialog,
                             QInputDialog, QSplitter, QDialogButtonBox, QWidgetAction)
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
VERSION = "1.1.0"  # Version mise à jour

# Style modernisé avec animations
MODERN_STYLE = """
/* Police moderne et variables */
* {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 9pt;
    qproperty-iconSize: 20px;
}

/* Fenêtre principale */
QMainWindow {
    background-color: #f8f9fa;
}

/* Barre latérale modernisée */
QListWidget {
    background-color: #ffffff;
    border: none;
    padding: 5px;
    border-radius: 8px;
    margin: 5px;
}

QListWidget::item {
    padding: 12px 15px;
    border-bottom: 1px solid #e9ecef;
    color: #495057;
    border-radius: 5px;
    margin: 2px;
}

QListWidget::item:hover {
    background-color: #e9f5ff;
}

QListWidget::item:selected {
    background-color: #4dabf7;
    color: white;
    border-left: 4px solid #228be6;
}

/* Boutons modernes avec effet de hover */
QPushButton {
    background-color: #4dabf7;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 6px;
    min-width: 80px;
    font-weight: 500;
    transition: background-color 0.2s;
}

QPushButton:hover {
    background-color: #339af0;
}

QPushButton:pressed {
    background-color: #228be6;
}

QPushButton:disabled {
    background-color: #adb5bd;
}

/* Tableaux avec style professionnel */
QTableWidget {
    background-color: white;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    gridline-color: #e9ecef;
    alternate-background-color: #f8f9fa;
    selection-background-color: #d0ebff;
    selection-color: black;
}

QHeaderView::section {
    background-color: #4dabf7;
    color: white;
    padding: 8px;
    border: none;
    font-weight: bold;
    font-size: 9pt;
}

QTableWidget QTableCornerButton::section {
    background-color: #4dabf7;
}

/* Onglets modernes */
QTabWidget::pane {
    border: 1px solid #e9ecef;
    border-radius: 8px;
    margin-top: 5px;
    background: white;
}

QTabBar::tab {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    padding: 8px 15px;
    color: #495057;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background: white;
    border-bottom: 3px solid #4dabf7;
    color: #228be6;
    font-weight: bold;
}

QTabBar::tab:hover {
    background: #e9ecef;
}

/* Champs de formulaire améliorés */
QLineEdit, QTextEdit, QComboBox, QDateEdit {
    border: 1px solid #ced4da;
    border-radius: 6px;
    padding: 6px;
    min-height: 28px;
    background: white;
    selection-background-color: #4dabf7;
    selection-color: white;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 1px solid #4dabf7;
    outline: none;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left-width: 1px;
    border-left-color: #ced4da;
    border-left-style: solid;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}

QComboBox QAbstractItemView {
    border: 1px solid #e9ecef;
    selection-background-color: #4dabf7;
    selection-color: white;
}

/* Barres d'outils modernes */
QToolBar {
    background-color: #f8f9fa;
    border: none;
    padding: 5px;
    spacing: 5px;
    border-bottom: 1px solid #e9ecef;
}

QToolButton {
    padding: 5px;
    border-radius: 4px;
}

QToolButton:hover {
    background-color: #e9ecef;
}

/* Barre de statut améliorée */
QStatusBar {
    background-color: #e9ecef;
    color: #495057;
    padding: 5px;
    border-top: 1px solid #dee2e6;
}

QStatusBar QLabel {
    padding: 0 5px;
}

/* Boîtes de dialogue */
QDialog {
    background-color: white;
}

/* Barres de séparation */
QSplitter::handle {
    background-color: #e9ecef;
    width: 3px;
}

/* Barre de défilement */
QScrollBar:vertical {
    border: none;
    background: #f8f9fa;
    width: 10px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    background: #ced4da;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

/* Tooltips */
QToolTip {
    background-color: #495057;
    color: white;
    border: 1px solid #495057;
    border-radius: 4px;
    padding: 3px;
}
"""

class IconManager:
    @staticmethod
    def get_icon(name, color="#4dabf7"):
        try:
            return qta.icon(f'fa5.{name}', color=color)
        except:
            try:
                return qta.icon(f'fa.{name}', color=color)
            except:
                try:
                    return QIcon.fromTheme(name)
                except:
                    return QIcon()

class Animations:
    @staticmethod
    def fade_in(widget, duration=300):
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

    @staticmethod
    def fade_out(widget, duration=300):
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.finished.connect(widget.close)
        animation.start()

class DatabaseManager:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Tables avec contraintes améliorées
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT,
                    email TEXT CHECK(email LIKE '%@%.%'),
                    telephone TEXT,
                    societe TEXT,
                    adresse TEXT,
                    ville TEXT,
                    code_postal TEXT,
                    pays TEXT,
                    notes TEXT,
                    date_creation TEXT DEFAULT CURRENT_TIMESTAMP,
                    date_modification TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL CHECK(type IN ('Proforma', 'Contrat', 'Fiche Technique', 'Garantie', 'Autre')),
                    titre TEXT NOT NULL,
                    contenu TEXT,
                    client_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
                    date_creation TEXT DEFAULT CURRENT_TIMESTAMP,
                    date_modification TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historique (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    document_id INTEGER REFERENCES documents(id) ON DELETE SET NULL,
                    client_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
                    details TEXT,
                    date TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS modeles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    nom TEXT NOT NULL UNIQUE,
                    contenu TEXT,
                    date_creation TEXT DEFAULT CURRENT_TIMESTAMP,
                    date_modification TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Index pour améliorer les performances
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_nom ON clients(nom)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_documents_type ON documents(type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_documents_client ON documents(client_id)')
            
            conn.commit()

    def execute_query(self, query, params=None, fetch_one=False):
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.row_factory = sqlite3.Row  # Pour obtenir des résultats sous forme de dictionnaire
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if fetch_one:
                    result = cursor.fetchone()
                    return dict(result) if result else None
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Erreur de base de données", f"Erreur dans la requête : {query}\n{str(e)}")
            return None

    def execute_update(self, query, params=None):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Erreur de base de données", f"Erreur dans la mise à jour : {query}\n{str(e)}")
            return None

class PDFGenerator:
    @staticmethod
    def generate_pdf(document_data, output_path):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # En-tête avec logo
            pdf.image('logo.png', x=10, y=8, w=30) if os.path.exists('logo.png') else None
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, txt=document_data['titre'], ln=1, align='C')
            pdf.set_font("Arial", size=12)
            pdf.ln(10)
            
            # Informations client
            if 'client' in document_data:
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, txt="INFORMATIONS CLIENT", ln=1, border='B')
                pdf.set_font("Arial", size=10)
                
                client_info = [
                    f"Nom: {document_data['client']['nom']} {document_data['client'].get('prenom', '')}",
                    f"Société: {document_data['client'].get('societe', '')}",
                    f"Email: {document_data['client'].get('email', '')}",
                    f"Téléphone: {document_data['client'].get('telephone', '')}",
                    f"Adresse: {document_data['client'].get('adresse', '')}"
                ]
                
                for info in client_info:
                    if info.split(':')[1].strip():
                        pdf.cell(0, 7, txt=info, ln=1)
                
                pdf.ln(10)
            
            # Contenu avec mise en forme
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 7, txt=document_data['contenu'])
            
            # Pied de page professionnel
            pdf.set_y(-20)
            pdf.set_font("Arial", 'I', 8)
            pdf.cell(0, 10, txt=f"Document généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}", border='T', align='C')
            
            pdf.output(output_path)
            return True
        except Exception as e:
            QMessageBox.critical(None, "Erreur PDF", f"Erreur lors de la génération du PDF : {str(e)}")
            return False

class EmailSender:
    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, to_email, subject, body, attachment_path=None):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Corps du message en HTML et texte brut
            msg.attach(MIMEText(body, 'plain'))
            msg.attach(MIMEText(f"""
                <html>
                    <body>
                        <p>{body.replace('\n', '<br>')}</p>
                        <p style="color: #666; font-size: 0.9em;">
                            Cet email a été envoyé automatiquement par {APP_NAME}.
                        </p>
                    </body>
                </html>
            """, 'html'))
            
            if attachment_path:
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(attachment_path)}",
                )
                msg.attach(part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            QMessageBox.critical(None, "Erreur d'envoi", f"Erreur lors de l'envoi de l'email : {str(e)}")
            return False

class ClientManagerDialog(QDialog):
    def __init__(self, parent=None, client_id=None):
        super().__init__(parent)
        self.client_id = client_id
        self.db = DatabaseManager()
        self.setWindowTitle("Nouveau Client" if not client_id else "Modifier Client")
        self.setWindowIcon(IconManager.get_icon('user-edit'))
        self.setModal(True)
        self.setMinimumSize(600, 650)
        
        self.init_ui()
        if client_id:
            self.load_client_data()
        
        Animations.fade_in(self)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titre avec icône
        title_layout = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(IconManager.get_icon('user-circle').pixmap(24, 24))
        title_layout.addWidget(title_icon)
        
        title_label = QLabel("Nouveau Client" if not self.client_id else "Modifier Client")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #343a40;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        layout.addSpacing(15)
        
        # Formulaire avec onglets
        tabs = QTabWidget()
        info_tab = QWidget()
        notes_tab = QWidget()
        
        # Onglet Informations
        info_layout = QFormLayout()
        info_layout.setVerticalSpacing(12)
        info_layout.setContentsMargins(10, 10, 10, 10)
        
        self.nom_edit = QLineEdit()
        self.nom_edit.setPlaceholderText("Obligatoire")
        self.prenom_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("exemple@domaine.com")
        self.telephone_edit = QLineEdit()
        self.telephone_edit.setPlaceholderText("+XX XXX XXX XXX")
        self.societe_edit = QLineEdit()
        
        # Adresse groupée
        address_group = QGroupBox("Adresse")
        address_layout = QFormLayout()
        self.adresse_edit = QTextEdit()
        self.adresse_edit.setMaximumHeight(60)
        self.ville_edit = QLineEdit()
        self.code_postal_edit = QLineEdit()
        self.pays_edit = QComboBox()
        self.pays_edit.addItems(["France", "Belgique", "Suisse", "Canada", "Autre"])
        
        address_layout.addRow("Adresse:", self.adresse_edit)
        address_layout.addRow("Ville:", self.ville_edit)
        address_layout.addRow("Code postal:", self.code_postal_edit)
        address_layout.addRow("Pays:", self.pays_edit)
        address_group.setLayout(address_layout)
        
        info_layout.addRow("Nom*:", self.nom_edit)
        info_layout.addRow("Prénom:", self.prenom_edit)
        info_layout.addRow("Email:", self.email_edit)
        info_layout.addRow("Téléphone:", self.telephone_edit)
        info_layout.addRow("Société:", self.societe_edit)
        info_layout.addRow(address_group)
        
        info_tab.setLayout(info_layout)
        
        # Onglet Notes
        notes_layout = QVBoxLayout()
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Notes supplémentaires sur le client...")
        notes_layout.addWidget(self.notes_edit)
        notes_tab.setLayout(notes_layout)
        
        tabs.addTab(info_tab, "Informations")
        tabs.addTab(notes_tab, "Notes")
        
        layout.addWidget(tabs)
        
        # Boutons avec icônes
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton(IconManager.get_icon('times'), " Annuler")
        self.cancel_button.clicked.connect(self.reject)
        
        self.save_button = QPushButton(IconManager.get_icon('save'), " Enregistrer")
        self.save_button.clicked.connect(self.save_client)
        self.save_button.setDefault(True)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def load_client_data(self):
        client_data = self.db.execute_query(
            "SELECT * FROM clients WHERE id = ?", 
            (self.client_id,), 
            fetch_one=True
        )
        
        if client_data:
            self.nom_edit.setText(client_data.get('nom', ''))
            self.prenom_edit.setText(client_data.get('prenom', ''))
            self.email_edit.setText(client_data.get('email', ''))
            self.telephone_edit.setText(client_data.get('telephone', ''))
            self.societe_edit.setText(client_data.get('societe', ''))
            self.adresse_edit.setPlainText(client_data.get('adresse', ''))
            self.ville_edit.setText(client_data.get('ville', ''))
            self.code_postal_edit.setText(client_data.get('code_postal', ''))
            
            index = self.pays_edit.findText(client_data.get('pays', ''))
            if index >= 0:
                self.pays_edit.setCurrentIndex(index)
                
            self.notes_edit.setPlainText(client_data.get('notes', ''))

    def save_client(self):
        nom = self.nom_edit.text().strip()
        if not nom:
            QMessageBox.warning(self, "Champ requis", "Le nom du client est obligatoire.")
            self.nom_edit.setFocus()
            return
        
        client_data = {
            'nom': nom,
            'prenom': self.prenom_edit.text().strip(),
            'email': self.email_edit.text().strip(),
            'telephone': self.telephone_edit.text().strip(),
            'societe': self.societe_edit.text().strip(),
            'adresse': self.adresse_edit.toPlainText().strip(),
            'ville': self.ville_edit.text().strip(),
            'code_postal': self.code_postal_edit.text().strip(),
            'pays': self.pays_edit.currentText(),
            'notes': self.notes_edit.toPlainText().strip(),
            'date_modification': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if self.client_id:
            # Mise à jour
            query = """UPDATE clients SET 
                        nom = :nom, prenom = :prenom, email = :email, 
                        telephone = :telephone, societe = :societe, adresse = :adresse, 
                        ville = :ville, code_postal = :code_postal, pays = :pays, 
                        notes = :notes, date_modification = :date_modification 
                    WHERE id = ?"""
            params = tuple(client_data.values()) + (self.client_id,)
            success = self.db.execute_update(query, params) is not None
        else:
            # Insertion
            client_data['date_creation'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            query = """INSERT INTO clients (
                        nom, prenom, email, telephone, societe, adresse, 
                        ville, code_postal, pays, notes, date_creation, date_modification
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            params = tuple(client_data.values())
            self.client_id = self.db.execute_update(query, params)
            success = self.client_id is not None
        
        if success:
            # Créer le dossier client
            client_folder = os.path.join("clients", f"client_{self.client_id}")
            os.makedirs(client_folder, exist_ok=True)
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de l'enregistrement.")

# [Les autres classes (DocumentManagerDialog, ClientsTab, DocumentsTab, etc.) seraient également modernisées de la même manière...]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{VERSION}")
        self.setWindowIcon(IconManager.get_icon('folder-open'))
        self.setMinimumSize(1200, 800)
        
        # Centrer la fenêtre
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move((screen.width()-size.width())//2, (screen.height()-size.height())//2)
        
        self.db = DatabaseManager()
        self.init_ui()
        
        # Créer les dossiers nécessaires
        os.makedirs("clients", exist_ok=True)
        os.makedirs("exports", exist_ok=True)
        
        Animations.fade_in(self)

    def init_ui(self):
        # Barre de menu modernisée
        self.create_menu_bar()
        
        # Barre d'outils principale
        self.create_main_toolbar()
        
        # Barre de statut avec indicateurs
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.db_status = QLabel("DB: OK")
        self.db_status.setStyleSheet("color: #2b8a3e;")
        self.status_bar.addPermanentWidget(self.db_status)
        self.status_bar.showMessage("Prêt", 3000)
        
        # Widget central avec layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        central_widget.setLayout(main_layout)
        
        # Barre latérale modernisée
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)
        self.sidebar.addItems(["📄 Documents", "👥 Clients", "🕒 Historique", "⚙ Paramètres"])
        self.sidebar.setCurrentRow(0)
        self.sidebar.currentRowChanged.connect(self.change_tab)
        
        # Zone de contenu avec onglets
        self.content_area = QStackedWidget()
        
        # Création des onglets
        self.docs_tab = DocumentsTab()
        self.clients_tab = ClientsTab()
        self.history_tab = HistoryTab()
        self.settings_tab = SettingsTab()
        
        self.content_area.addWidget(self.docs_tab)
        self.content_area.addWidget(self.clients_tab)
        self.content_area.addWidget(self.history_tab)
        self.content_area.addWidget(self.settings_tab)
        
        # Ajout au layout principal
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area, 1)
        
        # Connecter les signaux
        self.docs_tab.export_requested.connect(self.handle_export)
        self.clients_tab.client_selected.connect(self.handle_client_selection)

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # Menu Fichier
        file_menu = menu_bar.addMenu("Fichier")
        
        new_doc_action = QAction(IconManager.get_icon('file-alt'), "Nouveau Document", self)
        new_doc_action.setShortcut("Ctrl+N")
        new_doc_action.triggered.connect(self.docs_tab.add_document)
        
        new_client_action = QAction(IconManager.get_icon('user-plus'), "Nouveau Client", self)
        new_client_action.setShortcut("Ctrl+Shift+N")
        new_client_action.triggered.connect(self.clients_tab.add_client)
        
        exit_action = QAction(IconManager.get_icon('sign-out-alt'), "Quitter", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(new_doc_action)
        file_menu.addAction(new_client_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # Menu Outils
        tools_menu = menu_bar.addMenu("Outils")
        
        backup_action = QAction(IconManager.get_icon('database'), "Sauvegarde", self)
        backup_action.triggered.connect(self.backup_database)
        
        restore_action = QAction(IconManager.get_icon('history'), "Restaurer", self)
        restore_action.triggered.connect(self.restore_database)
        
        tools_menu.addAction(backup_action)
        tools_menu.addAction(restore_action)
        
        # Menu Aide
        help_menu = menu_bar.addMenu("Aide")
        
        about_action = QAction(IconManager.get_icon('info-circle'), "À propos", self)
        about_action.triggered.connect(self.show_about)
        
        help_menu.addAction(about_action)

    def create_main_toolbar(self):
        toolbar = self.addToolBar("Outils principaux")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        toolbar.setMovable(False)
        
        # Actions communes
        self.new_doc_action = QAction(IconManager.get_icon('file-alt'), "Nouveau\nDocument", self)
        self.new_doc_action.triggered.connect(self.docs_tab.add_document)
        
        self.new_client_action = QAction(IconManager.get_icon('user-plus'), "Nouveau\nClient", self)
        self.new_client_action.triggered.connect(self.clients_tab.add_client)
        
        self.export_action = QAction(IconManager.get_icon('file-export'), "Exporter\nPDF", self)
        self.export_action.triggered.connect(self.docs_tab.export_to_pdf)
        
        self.email_action = QAction(IconManager.get_icon('envelope'), "Envoyer\nEmail", self)
        self.email_action.triggered.connect(self.docs_tab.send_by_email)
        
        toolbar.addAction(self.new_doc_action)
        toolbar.addAction(self.new_client_action)
        toolbar.addSeparator()
        toolbar.addAction(self.export_action)
        toolbar.addAction(self.email_action)
        
        # Barre de recherche globale
        toolbar.addSeparator()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Recherche globale...")
        self.search_edit.setClearButtonEnabled(True)
        search_action = QWidgetAction(self)
        search_action.setDefaultWidget(self.search_edit)
        toolbar.addAction(search_action)

    def change_tab(self, index):
        self.content_area.setCurrentIndex(index)
        
        # Mettre à jour la barre d'outils en fonction de l'onglet
        tabs = ["Documents", "Clients", "Historique", "Paramètres"]
        self.status_bar.showMessage(f"Module actif: {tabs[index]}", 2000)

    def backup_database(self):
        default_path = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Sauvegarde de la base de données", 
            default_path, 
            "Fichiers SQLite (*.db *.sqlite)"
        )
        
        if file_path:
            try:
                with open(DB_NAME, 'rb') as f_src, open(file_path, 'wb') as f_dst:
                    f_dst.write(f_src.read())
                QMessageBox.information(self, "Succès", f"Sauvegarde réussie dans :\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de la sauvegarde :\n{str(e)}")

    def restore_database(self):
        reply = QMessageBox.warning(
            self, 
            "Confirmation", 
            "Cette action écrasera la base actuelle. Continuer ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            file_path, _ = QFileDialog.getOpenFileName(
                self, 
                "Restaurer une sauvegarde", 
                "", 
                "Fichiers SQLite (*.db *.sqlite)"
            )
            
            if file_path:
                try:
                    # Fermer les connexions
                    self.db = None
                    
                    # Remplacer la base
                    with open(file_path, 'rb') as f_src, open(DB_NAME, 'wb') as f_dst:
                        f_dst.write(f_src.read())
                    
                    # Réinitialiser
                    self.db = DatabaseManager()
                    self.docs_tab.load_documents()
                    self.clients_tab.load_clients()
                    self.history_tab.load_history()
                    
                    QMessageBox.information(self, "Succès", "Base de données restaurée avec succès")
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Échec de la restauration :\n{str(e)}")
                    self.db = DatabaseManager()

    def show_about(self):
        about_text = f"""
        <html>
            <body>
                <h1 style="color: #4dabf7;">{APP_NAME} v{VERSION}</h1>
                <p>Gestionnaire de documents professionnels</p>
                <p>Développé avec Python et PyQt</p>
                <p>© {datetime.now().year} - Tous droits réservés</p>
                <hr>
                <p style="font-size: 0.9em; color: #6c757d;">
                    Un outil complet pour gérer vos documents, clients et historiques.
                </p>
            </body>
        </html>
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
    app.setStyle('Fusion')  # Style Fusion moderne
    app.setStyleSheet(MODERN_STYLE)
    
    # Vérifier les dépendances
    try:
        import qtawesome as qta
    except ImportError:
        QMessageBox.critical(None, "Erreur", "Le module qtawesome est requis. Installez-le avec :\npip install qtawesome")
        sys.exit(1)
    
    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())