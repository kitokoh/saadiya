import sqlite3
import os
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox, QMenu, QAction, QComboBox, QScrollBar, QFrame, QDialog, QFormLayout
import csv
import json
import os
from PyQt5.QtCore import Qt, QSize, pyqtSignal  # Ajout de pyqtSignal ici
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
                             QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox,
                             QMenu, QAction, QComboBox, QScrollBar, QFrame, QDialog, QFormLayout)

from imports import *
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from ui.footer import FooterSection  # Import du footer
from ui.header import HeaderSection  # Import du header
from ui.secondry_menu import SecondaryMenu  # Assurez-vous d'importer votre nouvelle classe
import sqlite3
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from datetime import datetime



from PyQt5.QtCore import QUrl  # Correction de l'importation
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView, QCheckBox, QHBoxLayout, QLabel,
                             QMenu, QAction, QFileDialog, QWidget, QApplication, QComboBox)  #

import os
import csv
from PyQt5.QtCore import Qt, QUrl, QSize, pyqtSignal
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtWidgets import (
    QFileDialog, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox, QMenu, QAction,
    QComboBox, QScrollBar, QFrame, QDialog, QFormLayout, QMessageBox, QProgressBar
)

# # Chemin vers la base de données SQLite
# DB_PATH = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'groups.db')

# def init_db():
#     """Initialise la base de données SQLite."""
#     os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS groups (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             link TEXT NOT NULL,
#             remarks TEXT,
#             category TEXT,
#             description TEXT,
#             keywords TEXT
#         )
#     ''')
#     # Ajout d'index pour optimiser les recherches
#     cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON groups (name)')
#     cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON groups (category)')
#     conn.commit()
#     conn.close()

# def load_groups():
#     """Charge les groupes depuis la base de données SQLite."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM groups')
#     groups = cursor.fetchall()
#     conn.close()
#     return [dict(zip(['id', 'name', 'link', 'remarks', 'category', 'description', 'keywords'], group)) for group in groups]

# def save_group(group):
#     """Sauvegarde un groupe dans la base de données SQLite."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO groups (name, link, remarks, category, description, keywords)
#         VALUES (?, ?, ?, ?, ?, ?)
#     ''', (group['name'], group['link'], group['remarks'], group['category'], group['description'], group.get('keywords', '')))
#     conn.commit()
#     conn.close()

# def update_group(group):
#     """Met à jour un groupe dans la base de données SQLite."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('''
#         UPDATE groups
#         SET name = ?, link = ?, remarks = ?, category = ?, description = ?, keywords = ?
#         WHERE id = ?
#     ''', (group['name'], group['link'], group['remarks'], group['category'], group['description'], group.get('keywords', ''), group['id']))
#     conn.commit()
#     conn.close()

# def delete_group(group_id):
#     """Supprime un groupe de la base de données SQLite."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('DELETE FROM groups WHERE id = ?', (group_id,))
#     conn.commit()
#     conn.close()

class LoadGroupsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Charger des groupes")
        self.setFixedSize(400, 150)
        
        layout = QFormLayout(self)
        
        self.keywords_input = QLineEdit(self)
        self.keywords_input.setPlaceholderText("Entrez des mots-clés séparés par des virgules")
        layout.addRow("Mots-clés:", self.keywords_input)

        self.load_button = QPushButton("Charger", self)
        self.load_button.clicked.connect(self.load_groups)
        layout.addWidget(self.load_button)

    def load_groups(self):
        keywords = self.keywords_input.text().strip()
        if keywords:
            # Simuler la recherche de groupes sur Facebook (à implémenter)
            QMessageBox.information(self, "Info", f"Recherche de groupes avec les mots-clés : {keywords}")
            self.accept()



class UpdateRobotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Robot")
        self.setFixedSize(500, 400)

        # Style de la boîte de dialogue
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #aaa;
                border-radius: 6px;
                margin-bottom: 10px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #007bff;
                outline: none;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                font-size: 14px;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
        """)

        # Layout principal
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Champs de saisie
        self.name_input = QLineEdit(self)
        self.description_input = QLineEdit(self)
        self.category_input = QLineEdit(self)
        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Active", "Inactive"])  # Statut du robot

        # Ajout des champs au formulaire
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Status:", self.status_combo)

        # Boutons
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Save Robot", self)
        self.submit_button.clicked.connect(self.save_robot)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)

        # Ajout des layouts au layout principal
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        # Variable pour stocker l'ID du robot en cas de mise à jour
        self.robot_id = None

    def save_robot(self):
        """Sauvegarde ou met à jour un robot."""
        # Validation des entrées
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Name cannot be empty!")
            return

        # Création ou mise à jour du robot
        robot_data = {
            'name': self.name_input.text().strip(),
            'description': self.description_input.text().strip(),
            'category': self.category_input.text().strip(),
            'status': self.status_combo.currentText(),
            'creation_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Date de création
        }

        if self.robot_id:
            # Mise à jour d'un robot existant
            robot_data['id'] = self.robot_id
            update_robot(robot_data)
            QMessageBox.information(self, "Success", "Robot updated successfully!")
        else:
            # Création d'un nouveau robot
            save_robot(robot_data)
            QMessageBox.information(self, "Success", "Robot created successfully!")

        self.accept()  # Ferme la boîte de dialogue

    def set_robot_data(self, robot):
        """Remplit les champs avec les données d'un robot existant pour la mise à jour."""
        self.robot_id = robot['id']
        self.name_input.setText(robot.get('name', ''))
        self.description_input.setText(robot.get('description', ''))
        self.category_input.setText(robot.get('category', ''))
        self.status_combo.setCurrentText(robot.get('status', 'Active'))




# Chemin vers la base de données SQLite
DB_PATH = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'groups.db')

def init_db():
    """Initialise la base de données SQLite."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            link TEXT NOT NULL,
            remarks TEXT,
            category TEXT,
            description TEXT,
            keywords TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS robots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            creation_date TEXT,
            category TEXT,
            status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_robot (
            group_id INTEGER,
            robot_id INTEGER,
            FOREIGN KEY(group_id) REFERENCES groups(id),
            FOREIGN KEY(robot_id) REFERENCES robots(id)
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON groups (name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON groups (category)')
    conn.commit()
    conn.close()

def load_groups():
    """Charge les groupes depuis la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM groups')
    groups = cursor.fetchall()
    conn.close()
    return [dict(zip(['id', 'name', 'link', 'remarks', 'category', 'description', 'keywords'], group)) for group in groups]

def load_robots():
    """Charge les robots depuis la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM robots')
    robots = cursor.fetchall()
    conn.close()
    return [dict(zip(['id', 'name', 'description', 'creation_date', 'category', 'status'], robot)) for robot in robots]

def save_group(group):
    """Sauvegarde un groupe dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO groups (name, link, remarks, category, description, keywords)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (group['name'], group['link'], group['remarks'], group['category'], group['description'], group.get('keywords', '')))
    conn.commit()
    conn.close()

def update_group(group):
    """Met à jour un groupe dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE groups
        SET name = ?, link = ?, remarks = ?, category = ?, description = ?, keywords = ?
        WHERE id = ?
    ''', (group['name'], group['link'], group['remarks'], group['category'], group['description'], group.get('keywords', ''), group['id']))
    conn.commit()
    conn.close()

def delete_group(group_id):
    """Supprime un groupe de la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM groups WHERE id = ?', (group_id,))
    conn.commit()
    conn.close()

def save_robot(robot):
    """Sauvegarde un robot dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO robots (name, description, creation_date, category, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (robot['name'], robot['description'], robot['creation_date'], robot['category'], robot['status']))
    conn.commit()
    conn.close()

def update_robot(robot):
    """Met à jour un robot dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE robots
        SET name = ?, description = ?, creation_date = ?, category = ?, status = ?
        WHERE id = ?
    ''', (robot['name'], robot['description'], robot['creation_date'], robot['category'], robot['status'], robot['id']))
    conn.commit()
    conn.close()

def delete_robot(robot_id):
    """Supprime un robot de la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM robots WHERE id = ?', (robot_id,))
    conn.commit()
    conn.close()

def assign_group_to_robot(group_id, robot_id):
    """Affecte un groupe à un robot."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO group_robot (group_id, robot_id)
        VALUES (?, ?)
    ''', (group_id, robot_id))
    conn.commit()
    conn.close()

def get_robots_for_group(group_id):
    """Récupère les robots associés à un groupe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT robots.* FROM robots
        JOIN group_robot ON robots.id = group_robot.robot_id
        WHERE group_robot.group_id = ?
    ''', (group_id,))
    robots = cursor.fetchall()
    conn.close()
    return [dict(zip(['id', 'name', 'description', 'creation_date', 'category', 'status'], robot)) for robot in robots]

class AddGroupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Add Group"))
        self.setFixedSize(500, 400)

        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #aaa;
                border-radius: 6px;
                margin-bottom: 10px;
            }
            QLineEdit:focus {
                border-color: #007bff;
                outline: none;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                font-size: 14px;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
        """)

        # Layout
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Inputs
        self.name_input = QLineEdit(self)
        self.link_input = QLineEdit(self)
        self.remarks_input = QLineEdit(self)
        self.category_input = QLineEdit(self)
        self.description_input = QLineEdit(self)
        self.keywords_input = QLineEdit(self)

        form_layout.addRow(self.tr("Name:"), self.name_input)
        form_layout.addRow(self.tr("Link:"), self.link_input)
        form_layout.addRow(self.tr("Remarks:"), self.remarks_input)
        form_layout.addRow(self.tr("Category:"), self.category_input)
        form_layout.addRow(self.tr("Description:"), self.description_input)
        form_layout.addRow(self.tr("Keywords:"), self.keywords_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton(self.tr("Submit"), self)
        self.submit_button.clicked.connect(self.add_group)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def add_group(self):
        # Input Validation
        if not self.name_input.text().strip():
            QMessageBox.warning(self, self.tr("Validation Error"), self.tr("Name cannot be empty!"))
            return
        if not self.link_input.text().strip():
            QMessageBox.warning(self, self.tr("Validation Error"), self.tr("Link cannot be empty!"))
            return

        # Save Data
        new_group = {
            'name': self.name_input.text().strip(),
            'link': self.link_input.text().strip(),
            'remarks': self.remarks_input.text().strip(),
            'category': self.category_input.text().strip(),
            'description': self.description_input.text().strip(),
            'keywords': self.keywords_input.text().strip()
        }
        save_group(new_group)
        QMessageBox.information(self, self.tr("Success"), self.tr("Group added successfully!"))
        self.accept()

class AssignGroupToRobotDialog(QDialog):
    def __init__(self, group_id, parent=None):
        super().__init__(parent)
        self.group_id = group_id
        self.setWindowTitle(self.tr("Assign Group to Robot"))
        self.setFixedSize(400, 300)

        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QComboBox {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #aaa;
                border-radius: 6px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                font-size: 14px;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
        """)

        # Layout
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Robots ComboBox
        self.robots_combo = QComboBox(self)
        robots = load_robots()
        for robot in robots:
            self.robots_combo.addItem(robot['name'], robot['id'])
        form_layout.addRow(self.tr("Select Robot:"), self.robots_combo)

        # Buttons
        button_layout = QHBoxLayout()
        self.assign_button = QPushButton(self.tr("Assign"), self)
        self.assign_button.clicked.connect(self.assign_group)
        button_layout.addStretch()
        button_layout.addWidget(self.assign_button)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def assign_group(self):
        robot_id = self.robots_combo.currentData()
        assign_group_to_robot(self.group_id, robot_id)
        QMessageBox.information(self, self.tr("Success"), self.tr("Group assigned to robot successfully!"))
        self.accept()

class GroupTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.all_groups = load_groups()  # All groups loaded initially
        self.filtered_groups = self.all_groups  # Groups after filtering
        self.visible_columns = ['Select', 'Name', 'Link', 'Remarks', 'Category', 'Description', 'Verification', 'Actions']
        self.items_per_page = 25
        self.current_page = 1

        layout = QVBoxLayout(self)

        # Header section
        header = HeaderSection(self, title="FBK GRUP MANAGEMENT", app_name="Nova360 AI", slogan="AI Marketing Automation Solution")
        layout.addWidget(header)

        # Top layout for title, search bar, and buttons
        top_layout = QHBoxLayout()

        group_label = QLabel("List of Groups:", self)
        group_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_layout.addWidget(group_label)

        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Search in groups...")
        self.search_field.textChanged.connect(self.filter_table)
        self.search_field.setStyleSheet("padding: 5px; font-size: 14px;")
        top_layout.addWidget(self.search_field)

        self.import_button = self.create_button('Import Group', '#6c757d', self.import_groups)
        top_layout.addWidget(self.import_button)

        self.export_button = self.create_button('Export', '#007bff', self.export_groups)
        top_layout.addWidget(self.export_button)

        self.add_group_button = self.create_button('+ Add Group', '#28a745', self.open_add_group_dialog)
        top_layout.addWidget(self.add_group_button)

        self.load_groups_button = self.create_button('Load Groups', '#ffc107', self.open_load_groups_dialog)
        top_layout.addWidget(self.load_groups_button)

        self.update_robot_button = self.create_button('Update Robot', '#17a2b8', self.open_update_robot_dialog)
        top_layout.addWidget(self.update_robot_button)

        layout.addLayout(top_layout)

        # Group table
        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.visible_columns))
        self.table.setHorizontalHeaderLabels(self.visible_columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setStyleSheet(self.table_styles())
        layout.addWidget(self.table)

        # Column visibility checkboxes
        self.checkboxes_layout = QHBoxLayout()
        for index, col_name in enumerate(self.visible_columns):
            checkbox = QCheckBox(col_name)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(lambda state, idx=index: self.update_visible_columns(idx, state))
            self.checkboxes_layout.addWidget(checkbox)
        layout.addLayout(self.checkboxes_layout)

        # Pagination
        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_page)
        self.pagination_layout.addWidget(self.prev_button)

        self.pagination_label = QLabel(f"Page {self.current_page}")
        self.pagination_layout.addWidget(self.pagination_label)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.pagination_layout.addWidget(self.next_button)

        layout.addLayout(self.pagination_layout)

        self.update_pagination_buttons()
        self.populate_table()

    def create_button(self, text, color, callback):
        button = QPushButton(text, self)
        button.setStyleSheet(f"background-color: {color}; color: white; padding: 5px 10px;")
        button.clicked.connect(callback)
        return button

    def table_styles(self):
        return """
            QTableWidget {
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #007BFF;
                color: white;
                padding: 10px;
            }
        """

    def populate_table(self):
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        visible_groups = self.filtered_groups[start_index:end_index]

        self.table.setRowCount(len(visible_groups))
        for row, group in enumerate(visible_groups):
            checkbox = QCheckBox()
            self.table.setCellWidget(row, 0, checkbox)

            for col, key in enumerate(['name', 'link', 'remarks', 'category', 'description']):
                self.table.setItem(row, col + 1, QTableWidgetItem(group.get(key, '')))

            verify_button = QPushButton('Verify', self)
            verify_button.clicked.connect(lambda _, link=group.get('link', ''): self.open_link_in_browser(link))
            self.table.setCellWidget(row, 6, verify_button)

            action_button = QPushButton('Actions', self)
            action_menu = QMenu(self)

            edit_action = QAction('Edit', self)
            delete_action = QAction('Delete', self)
            assign_action = QAction('Assign to Robot', self)
            edit_action.triggered.connect(lambda _, r=row: self.edit_group(r))
            delete_action.triggered.connect(lambda _, r=row: self.delete_group(r))
            assign_action.triggered.connect(lambda _, r=row: self.assign_group_to_robot(r))

            action_menu.addAction(edit_action)
            action_menu.addAction(delete_action)
            action_menu.addAction(assign_action)
            action_button.setMenu(action_menu)
            self.table.setCellWidget(row, 7, action_button)

        self.pagination_label.setText(f"Page {self.current_page}")

    def update_visible_columns(self, index, state):
        self.table.setColumnHidden(index, not state)

    def update_pagination_buttons(self):
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page * self.items_per_page < len(self.filtered_groups))

    def filter_table(self):
        search_text = self.search_field.text().lower()
        self.filtered_groups = [group for group in self.all_groups if search_text in group.get('name', '').lower()]
        self.current_page = 1
        self.update_pagination_buttons()
        self.populate_table()

    def next_page(self):
        if (self.current_page * self.items_per_page) < len(self.filtered_groups):
            self.current_page += 1
            self.populate_table()
            self.update_pagination_buttons()

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_table()
            self.update_pagination_buttons()

    def open_link_in_browser(self, link):
        if link:
            QDesktopServices.openUrl(QUrl(link))

    def open_load_groups_dialog(self):
        dialog = LoadGroupsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.all_groups = load_groups()
            self.filtered_groups = self.all_groups
            self.populate_table()

    def import_groups(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Groups", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        save_group(row)
                self.all_groups = load_groups()
                self.filtered_groups = self.all_groups
                self.populate_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error during import: {e}")

    def export_groups(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Groups", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.all_groups[0].keys())
                    writer.writeheader()
                    writer.writerows(self.all_groups)
                QMessageBox.information(self, "Success", "Export successful.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error during export: {e}")

    def open_add_group_dialog(self):
        dialog = AddGroupDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.all_groups = load_groups()
            self.filtered_groups = self.all_groups
            self.populate_table()

    def edit_group(self, row):
        group = self.filtered_groups[row]
        dialog = AddGroupDialog(self)
        dialog.name_input.setText(group.get('name', ''))
        dialog.link_input.setText(group.get('link', ''))
        dialog.remarks_input.setText(group.get('remarks', ''))
        dialog.category_input.setText(group.get('category', ''))
        dialog.description_input.setText(group.get('description', ''))

        if dialog.exec_() == QDialog.Accepted:
            updated_group = {
                'id': group['id'],
                'name': dialog.name_input.text(),
                'link': dialog.link_input.text(),
                'remarks': dialog.remarks_input.text(),
                'category': dialog.category_input.text(),
                'description': dialog.description_input.text()
            }
            update_group(updated_group)
            self.all_groups = load_groups()
            self.filtered_groups = self.all_groups
            self.populate_table()

    def delete_group(self, row):
        group = self.filtered_groups[row]
        delete_group(group['id'])
        self.all_groups = load_groups()
        self.filtered_groups = self.all_groups
        self.populate_table()

    def assign_group_to_robot(self, row):
        group = self.filtered_groups[row]
        dialog = AssignGroupToRobotDialog(group['id'], self)
        dialog.exec_()

    def open_update_robot_dialog(self):
        dialog = UpdateRobotDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.all_groups = load_groups()
            self.filtered_groups = self.all_groups
            self.populate_table()

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    init_db()  # Initialiser la base de données
    app = QApplication(sys.argv)
    window = GroupTable()
    window.show()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     import sys
#     from PyQt5.QtWidgets import QApplication

#     init_db()  # Initialiser la base de données
#     app = QApplication(sys.argv)
#     window = GroupTable()
#     window.show()
#     sys.exit(app.exec_())