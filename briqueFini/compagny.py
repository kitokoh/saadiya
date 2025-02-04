import sys
import csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog, QComboBox, QDialog, QFormLayout,
                             QDialogButtonBox, QHeaderView, QTextEdit, QMenu, QAction, QTabWidget, QDateEdit, QCheckBox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QDate
import sqlite3
from datetime import datetime

class CompanyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Entreprises et Employés")
        self.setGeometry(100, 100, 1200, 800)

        self.init_db()
        self.init_ui()

    def init_db(self):
        self.conn = sqlite3.connect('company.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                role TEXT NOT NULL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_suppression TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS entreprises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                adresse TEXT,
                ville TEXT,
                code_postal TEXT,
                pays TEXT,
                telephone TEXT,
                email TEXT NOT NULL UNIQUE,
                site_web TEXT,
                iban TEXT,
                numero_enregistrement TEXT,
                logo BLOB,
                cachet BLOB,
                signature BLOB,
                devise TEXT DEFAULT 'EUR',
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_suppression TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                entreprise_id INTEGER NOT NULL,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                poste TEXT NOT NULL,
                telephone TEXT,
                email TEXT NOT NULL UNIQUE,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_suppression TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (entreprise_id) REFERENCES entreprises (id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reseaux_sociaux (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entreprise_id INTEGER NOT NULL,
                nom TEXT NOT NULL,
                identifiant TEXT,
                mot_de_passe TEXT,
                description TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_suppression TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (entreprise_id) REFERENCES entreprises (id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS zones_geographiques (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entreprise_id INTEGER NOT NULL,
                nom TEXT NOT NULL,
                description TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_suppression TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (entreprise_id) REFERENCES entreprises (id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                description TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_suppression TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sous_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categorie_id INTEGER NOT NULL,
                nom TEXT NOT NULL,
                description TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_suppression TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (categorie_id) REFERENCES categories (id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS campagnes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entreprise_id INTEGER NOT NULL,
                nom TEXT NOT NULL,
                description TEXT,
                date_debut TIMESTAMP,
                date_fin TIMESTAMP,
                budget REAL,
                devise TEXT DEFAULT 'EUR',
                statut TEXT NOT NULL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_suppression TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (entreprise_id) REFERENCES entreprises (id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS serveurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entreprise_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                hote TEXT NOT NULL,
                port INTEGER,
                identifiant TEXT NOT NULL,
                mot_de_passe TEXT NOT NULL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_suppression TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (entreprise_id) REFERENCES entreprises (id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                table_concernee TEXT NOT NULL,
                id_concerne INTEGER NOT NULL,
                date_action TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS connexions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                adresse_ip TEXT,
                navigateur TEXT,
                date_connexion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS historique_modifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                table_modifiee TEXT NOT NULL,
                id_entite INTEGER NOT NULL,
                ancienne_valeur TEXT,
                nouvelle_valeur TEXT,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS resultats_campagnes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campagne_id INTEGER NOT NULL,
                indicateur TEXT NOT NULL,
                valeur REAL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campagne_id) REFERENCES campagnes (id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cibles_marketing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campagne_id INTEGER NOT NULL,
                age_min INTEGER,
                age_max INTEGER,
                genre TEXT,
                localisation TEXT,
                interets TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campagne_id) REFERENCES campagnes (id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs_detail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                table_concernee TEXT NOT NULL,
                id_concerne INTEGER NOT NULL,
                adresse_ip TEXT,
                navigateur TEXT,
                date_action TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedbacks_utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                feedback TEXT NOT NULL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT NOT NULL UNIQUE,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_expiration TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions_utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type_interaction TEXT NOT NULL,
                description TEXT,
                date_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences_utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                preference TEXT NOT NULL,
                valeur TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Apply styles
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                font-size: 14px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTableWidget {
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background: #4CAF50;
                color: white;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #45a049;
            }
        """)

        # Menu Bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Fichier')

        import_action = QAction('Importer CSV', self)
        import_action.triggered.connect(self.import_csv)
        file_menu.addAction(import_action)

        export_action = QAction('Exporter CSV', self)
        export_action.triggered.connect(self.export_csv)
        file_menu.addAction(export_action)

        # Search Section
        search_layout = QHBoxLayout()
        layout.addLayout(search_layout)

        search_label = QLabel("Rechercher:")
        search_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_data)
        search_layout.addWidget(self.search_input)

        # Tab Widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Company Tab
        company_tab = QWidget()
        company_layout = QVBoxLayout()
        company_tab.setLayout(company_layout)

        company_form_layout = QFormLayout()
        company_layout.addLayout(company_form_layout)

        self.company_name_input = QLineEdit()
        company_form_layout.addRow("Nom de l'entreprise:", self.company_name_input)

        self.company_address_input = QTextEdit()
        company_form_layout.addRow("Adresse:", self.company_address_input)

        self.company_city_input = QLineEdit()
        company_form_layout.addRow("Ville:", self.company_city_input)

        self.company_postal_code_input = QLineEdit()
        company_form_layout.addRow("Code Postal:", self.company_postal_code_input)

        self.company_country_input = QLineEdit()
        company_form_layout.addRow("Pays:", self.company_country_input)

        self.company_phone_input = QLineEdit()
        company_form_layout.addRow("Téléphone:", self.company_phone_input)

        self.company_email_input = QLineEdit()
        company_form_layout.addRow("Email:", self.company_email_input)

        self.company_website_input = QLineEdit()
        company_form_layout.addRow("Site Web:", self.company_website_input)

        self.company_iban_input = QLineEdit()
        company_form_layout.addRow("Numéro IBAN:", self.company_iban_input)

        self.company_registration_input = QLineEdit()
        company_form_layout.addRow("Numéro d'enregistrement:", self.company_registration_input)

        self.logo_path = QLineEdit()
        company_form_layout.addRow("Logo:", self.logo_path)

        browse_button = QPushButton("Parcourir")
        browse_button.clicked.connect(self.browse_logo)
        company_form_layout.addWidget(browse_button)

        add_company_button = QPushButton("Ajouter Entreprise")
        add_company_button.clicked.connect(self.add_company)
        company_layout.addWidget(add_company_button)

        self.tab_widget.addTab(company_tab, "Entreprises")

        # Employee Tab
        employee_tab = QWidget()
        employee_layout = QVBoxLayout()
        employee_tab.setLayout(employee_layout)

        employee_form_layout = QFormLayout()
        employee_layout.addLayout(employee_form_layout)

        self.employee_name_input = QLineEdit()
        employee_form_layout.addRow("Nom de l'employé:", self.employee_name_input)

        self.employee_firstname_input = QLineEdit()
        employee_form_layout.addRow("Prénom de l'employé:", self.employee_firstname_input)

        self.employee_role_input = QLineEdit()
        employee_form_layout.addRow("Rôle:", self.employee_role_input)

        self.employee_phone_input = QLineEdit()
        employee_form_layout.addRow("Téléphone:", self.employee_phone_input)

        self.employee_email_input = QLineEdit()
        employee_form_layout.addRow("Email:", self.employee_email_input)

        company_selection_label = QLabel("Entreprise:")
        employee_form_layout.addWidget(company_selection_label)

        self.company_selection = QComboBox()
        self.load_companies()
        employee_form_layout.addWidget(self.company_selection)

        add_employee_button = QPushButton("Ajouter Employé")
        add_employee_button.clicked.connect(self.add_employee)
        employee_layout.addWidget(add_employee_button)

        self.tab_widget.addTab(employee_tab, "Employés")

        # Campaign Tab
        campaign_tab = QWidget()
        campaign_layout = QVBoxLayout()
        campaign_tab.setLayout(campaign_layout)

        campaign_form_layout = QFormLayout()
        campaign_layout.addLayout(campaign_form_layout)

        self.campaign_name_input = QLineEdit()
        campaign_form_layout.addRow("Nom de la campagne:", self.campaign_name_input)

        self.campaign_description_input = QTextEdit()
        campaign_form_layout.addRow("Description:", self.campaign_description_input)

        self.campaign_start_date_input = QDateEdit()
        self.campaign_start_date_input.setCalendarPopup(True)
        campaign_form_layout.addRow("Date de début:", self.campaign_start_date_input)

        self.campaign_end_date_input = QDateEdit()
        self.campaign_end_date_input.setCalendarPopup(True)
        campaign_form_layout.addRow("Date de fin:", self.campaign_end_date_input)

        self.campaign_budget_input = QLineEdit()
        campaign_form_layout.addRow("Budget:", self.campaign_budget_input)

        self.campaign_status_input = QComboBox()
        self.campaign_status_input.addItems(["Brouillon", "En attente", "En cours", "Terminé"])
        campaign_form_layout.addRow("Statut:", self.campaign_status_input)

        add_campaign_button = QPushButton("Ajouter Campagne")
        add_campaign_button.clicked.connect(self.add_campaign)
        campaign_layout.addWidget(add_campaign_button)

        self.tab_widget.addTab(campaign_tab, "Campagnes")

        # Table Section
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(["Entreprise", "Adresse", "Ville", "Code Postal", "Pays", "Téléphone", "Email", "Site Web", "Logo", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        self.load_data()

    def browse_logo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner le logo", "", "Images (*.png *.xpm *.jpg *.jpeg);;All Files (*)", options=options)
        if file_name:
            self.logo_path.setText(file_name)

    def add_company(self):
        company_name = self.company_name_input.text()
        company_address = self.company_address_input.toPlainText()
        company_city = self.company_city_input.text()
        company_postal_code = self.company_postal_code_input.text()
        company_country = self.company_country_input.text()
        company_phone = self.company_phone_input.text()
        company_email = self.company_email_input.text()
        company_website = self.company_website_input.text()
        company_iban = self.company_iban_input.text()
        company_registration = self.company_registration_input.text()
        logo_path = self.logo_path.text()
        if company_name and company_address and company_city and company_postal_code and company_country and company_phone and company_email and company_website and company_iban and company_registration and logo_path:
            with open(logo_path, 'rb') as file:
                logo_data = file.read()
            self.cursor.execute("INSERT INTO entreprises (nom, adresse, ville, code_postal, pays, telephone, email, site_web, iban, numero_enregistrement, logo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (company_name, company_address, company_city, company_postal_code, company_country, company_phone, company_email, company_website, company_iban, company_registration, logo_data))
            self.conn.commit()
            self.clear_company_inputs()
            self.load_data()
            self.load_companies()
        else:
            QMessageBox.warning(self, "Avertissement", "Veuillez remplir tous les champs.")

    def add_employee(self):
        employee_name = self.employee_name_input.text()
        employee_firstname = self.employee_firstname_input.text()
        employee_role = self.employee_role_input.text()
        employee_phone = self.employee_phone_input.text()
        employee_email = self.employee_email_input.text()
        company_id = self.company_selection.currentData()
        if employee_name and employee_firstname and employee_role and employee_phone and employee_email and company_id:
            self.cursor.execute("INSERT INTO employes (user_id, entreprise_id, nom, prenom, poste, telephone, email) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (1, company_id, employee_name, employee_firstname, employee_role, employee_phone, employee_email))
            self.conn.commit()
            self.clear_employee_inputs()
            self.load_data()
        else:
            QMessageBox.warning(self, "Avertissement", "Veuillez entrer le nom de l'employé, son rôle et sélectionner une entreprise.")

    def add_campaign(self):
        campaign_name = self.campaign_name_input.text()
        campaign_description = self.campaign_description_input.toPlainText()
        campaign_start_date = self.campaign_start_date_input.date().toString(Qt.ISODate)
        campaign_end_date = self.campaign_end_date_input.date().toString(Qt.ISODate)
        campaign_budget = self.campaign_budget_input.text()
        campaign_status = self.campaign_status_input.currentText()
        company_id = self.company_selection.currentData()
        if campaign_name and campaign_description and campaign_start_date and campaign_end_date and campaign_budget and campaign_status and company_id:
            self.cursor.execute("INSERT INTO campagnes (entreprise_id, nom, description, date_debut, date_fin, budget, statut) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (company_id, campaign_name, campaign_description, campaign_start_date, campaign_end_date, campaign_budget, campaign_status))
            self.conn.commit()
            self.clear_campaign_inputs()
            self.load_data()
        else:
            QMessageBox.warning(self, "Avertissement", "Veuillez remplir tous les champs.")

    def load_data(self):
        self.table.setRowCount(0)
        self.cursor.execute('''
            SELECT nom, adresse, ville, code_postal, pays, telephone, email, site_web, logo, id
            FROM entreprises
        ''')
        rows = self.cursor.fetchall()
        for row in rows:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(row[0]))
            self.table.setItem(row_position, 1, QTableWidgetItem(row[1]))
            self.table.setItem(row_position, 2, QTableWidgetItem(row[2]))
            self.table.setItem(row_position, 3, QTableWidgetItem(row[3]))
            self.table.setItem(row_position, 4, QTableWidgetItem(row[4]))
            self.table.setItem(row_position, 5, QTableWidgetItem(row[5]))
            self.table.setItem(row_position, 6, QTableWidgetItem(row[6]))
            self.table.setItem(row_position, 7, QTableWidgetItem(row[7]))
            self.table.setItem(row_position, 8, QTableWidgetItem(row[8]))
            logo_data = row[8]
            if logo_data:
                pixmap = QPixmap()
                pixmap.loadFromData(logo_data)
                logo_label = QLabel()
                logo_label.setPixmap(pixmap.scaled(50, 50))
                self.table.setCellWidget(row_position, 8, logo_label)

            edit_button = QPushButton("Modifier")
            edit_button.clicked.connect(lambda _, r=row: self.edit_company(r))
            delete_button = QPushButton("Supprimer")
            delete_button.clicked.connect(lambda _, r=row: self.delete_company(r))

            actions_layout = QHBoxLayout()
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_widget = QWidget()
            actions_widget.setLayout(actions_layout)
            self.table.setCellWidget(row_position, 9, actions_widget)

    def load_companies(self):
        self.company_selection.clear()
        self.cursor.execute("SELECT id, nom FROM entreprises")
        companies = self.cursor.fetchall()
        for company in companies:
            self.company_selection.addItem(company[1], company[0])

    def edit_company(self, row):
        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier Entreprise")
        dialog_layout = QFormLayout(dialog)

        company_id = row[9]
        company_name_input = QLineEdit(row[0])
        company_address_input = QTextEdit(row[1])
        company_city_input = QLineEdit(row[2])
        company_postal_code_input = QLineEdit(row[3])
        company_country_input = QLineEdit(row[4])
        company_phone_input = QLineEdit(row[5])
        company_email_input = QLineEdit(row[6])
        company_website_input = QLineEdit(row[7])
        company_iban_input = QLineEdit(row[8])

        dialog_layout.addRow("Nom de l'entreprise:", company_name_input)
        dialog_layout.addRow("Adresse:", company_address_input)
        dialog_layout.addRow("Ville:", company_city_input)
        dialog_layout.addRow("Code Postal:", company_postal_code_input)
        dialog_layout.addRow("Pays:", company_country_input)
        dialog_layout.addRow("Téléphone:", company_phone_input)
        dialog_layout.addRow("Email:", company_email_input)
        dialog_layout.addRow("Site Web:", company_website_input)
        dialog_layout.addRow("Numéro IBAN:", company_iban_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)
        dialog_layout.addWidget(buttons)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            new_name = company_name_input.text()
            new_address = company_address_input.toPlainText()
            new_city = company_city_input.text()
            new_postal_code = company_postal_code_input.text()
            new_country = company_country_input.text()
            new_phone = company_phone_input.text()
            new_email = company_email_input.text()
            new_website = company_website_input.text()
            new_iban = company_iban_input.text()
            self.cursor.execute("UPDATE entreprises SET nom=?, adresse=?, ville=?, code_postal=?, pays=?, telephone=?, email=?, site_web=?, iban=? WHERE id=?",
                               (new_name, new_address, new_city, new_postal_code, new_country, new_phone, new_email, new_website, new_iban, company_id))
            self.conn.commit()
            self.load_data()

    def delete_company(self, row):
        company_id = row[9]
        reply = QMessageBox.question(self, 'Confirmation', "Êtes-vous sûr de vouloir supprimer cette entreprise?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM entreprises WHERE id=?", (company_id,))
            self.conn.commit()
            self.load_data()
            self.load_companies()

    def search_data(self):
        search_text = self.search_input.text().lower()
        self.table.setRowCount(0)
        self.cursor.execute('''
            SELECT nom, adresse, ville, code_postal, pays, telephone, email, site_web, logo, id
            FROM entreprises
            WHERE LOWER(nom) LIKE ? OR LOWER(adresse) LIKE ? OR LOWER(ville) LIKE ? OR LOWER(code_postal) LIKE ? OR LOWER(pays) LIKE ? OR LOWER(telephone) LIKE ? OR LOWER(email) LIKE ? OR LOWER(site_web) LIKE ?
        ''', ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))
        rows = self.cursor.fetchall()
        for row in rows:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(row[0]))
            self.table.setItem(row_position, 1, QTableWidgetItem(row[1]))
            self.table.setItem(row_position, 2, QTableWidgetItem(row[2]))
            self.table.setItem(row_position, 3, QTableWidgetItem(row[3]))
            self.table.setItem(row_position, 4, QTableWidgetItem(row[4]))
            self.table.setItem(row_position, 5, QTableWidgetItem(row[5]))
            self.table.setItem(row_position, 6, QTableWidgetItem(row[6]))
            self.table.setItem(row_position, 7, QTableWidgetItem(row[7]))
            self.table.setItem(row_position, 8, QTableWidgetItem(row[8]))
            logo_data = row[8]
            if logo_data:
                pixmap = QPixmap()
                pixmap.loadFromData(logo_data)
                logo_label = QLabel()
                logo_label.setPixmap(pixmap.scaled(50, 50))
                self.table.setCellWidget(row_position, 8, logo_label)

            edit_button = QPushButton("Modifier")
            edit_button.clicked.connect(lambda _, r=row: self.edit_company(r))
            delete_button = QPushButton("Supprimer")
            delete_button.clicked.connect(lambda _, r=row: self.delete_company(r))

            actions_layout = QHBoxLayout()
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_widget = QWidget()
            actions_widget.setLayout(actions_layout)
            self.table.setCellWidget(row_position, 9, actions_widget)

    def clear_company_inputs(self):
        self.company_name_input.clear()
        self.company_address_input.clear()
        self.company_city_input.clear()
        self.company_postal_code_input.clear()
        self.company_country_input.clear()
        self.company_phone_input.clear()
        self.company_email_input.clear()
        self.company_website_input.clear()
        self.company_iban_input.clear()
        self.company_registration_input.clear()
        self.logo_path.clear()

    def clear_employee_inputs(self):
        self.employee_name_input.clear()
        self.employee_firstname_input.clear()
        self.employee_role_input.clear()
        self.employee_phone_input.clear()
        self.employee_email_input.clear()

    def clear_campaign_inputs(self):
        self.campaign_name_input.clear()
        self.campaign_description_input.clear()
        self.campaign_start_date_input.setDate(QDate.currentDate())
        self.campaign_end_date_input.setDate(QDate.currentDate())
        self.campaign_budget_input.clear()
        self.campaign_status_input.setCurrentIndex(0)

    def import_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner le fichier CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            with open(file_name, mode='r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header
                for row in csv_reader:
                    company_name, company_address, company_city, company_postal_code, company_country, company_phone, company_email, company_website, company_iban, company_registration, logo_path = row
                    with open(logo_path, 'rb') as logo_file:
                        logo_data = logo_file.read()
                    self.cursor.execute("INSERT INTO entreprises (nom, adresse, ville, code_postal, pays, telephone, email, site_web, iban, numero_enregistrement, logo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                       (company_name, company_address, company_city, company_postal_code, company_country, company_phone, company_email, company_website, company_iban, company_registration, logo_data))
                self.conn.commit()
                self.load_data()
                self.load_companies()

    def export_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Sélectionner le répertoire de sauvegarde", options=options)
        if directory:
            file_path = f"{directory}/entreprises.csv"
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(["Nom", "Adresse", "Ville", "Code Postal", "Pays", "Téléphone", "Email", "Site Web", "IBAN", "Numéro d'enregistrement", "Logo"])
                self.cursor.execute('''
                    SELECT nom, adresse, ville, code_postal, pays, telephone, email, site_web, iban, numero_enregistrement, logo
                    FROM entreprises
                ''')
                rows = self.cursor.fetchall()
                for row in rows:
                    csv_writer.writerow(row)
            QMessageBox.information(self, "Succès", f"Les données ont été exportées vers {file_path}")

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CompanyApp()
    window.show()
    sys.exit(app.exec_())
