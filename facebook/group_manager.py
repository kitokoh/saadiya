import sqlite3
import os
import csv
from datetime import datetime
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QUrl
from PyQt5.QtWidgets import (
    QFileDialog, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox, QMenu, QAction,
    QComboBox, QScrollBar, QFrame, QDialog, QFormLayout, QMessageBox, QProgressBar
)
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QComboBox
import sqlite3
from PyQt5.QtGui import QPalette, QColor  # Pour PyQt5
# OU
#from test import ManageArchivesDialog
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QComboBox, QLineEdit, QDateTimeEdit, QMessageBox
from PyQt5.QtCore import QDateTime
from imports import *

from ui.header import HeaderSection
from ui.footer import FooterSection
# def load_categories():
#     """Charge toutes les catégories depuis la base de données."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM category')
#     categories = cursor.fetchall()
#     conn.close()
#     return [dict(zip(['id', 'name', 'label', 'description', 'date_creation', 'date_modification', 'date_suppression'], cat)) for cat in categories]

# def load_reseaux_sociaux():
#     """Charge tous les réseaux sociaux depuis la base de données."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM reseaux_sociaux')
#     reseaux_sociaux = cursor.fetchall()
#     conn.close()
#     return [dict(zip(['id', 'name', 'description', 'date_creation', 'date_modification', 'date_suppression'], rs)) for rs in reseaux_sociaux]

# def save_robot(robot):
#     """Sauvegarde un nouveau robot dans la base de données."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO robots (name, label, description, category_id, reseau_social_id)
#         VALUES (?, ?, ?, ?, ?)
#     ''', (robot['name'], robot.get('label', ''), robot.get('description', ''), robot['category_id'], robot['reseau_social_id']))
#     conn.commit()
#     conn.close()


def save_reseau_social(reseau_social):
    """Sauvegarde un nouveau réseau social dans la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reseaux_sociaux (name, description)
        VALUES (?, ?)
    ''', (reseau_social['name'], reseau_social.get('description', '')))
    conn.commit()
    conn.close()
def update_category(category):
    """
    Met à jour une catégorie dans la base de données.
    
    Args:
        category (dict): Un dictionnaire contenant les informations de la catégorie.
                         Doit contenir les clés 'id', 'name', 'label', et 'description'.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Mettre à jour la catégorie dans la table
    cursor.execute('''
        UPDATE category
        SET name = ?, label = ?, description = ?, date_modification = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (category['name'], category.get('label', ''), category.get('description', ''), category['id']))
    
    conn.commit()
    conn.close()

def delete_category(category_id):
    """
    Supprime une catégorie de la base de données.
    
    Args:
        category_id (int): L'ID de la catégorie à supprimer.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Supprimer la catégorie de la table
    cursor.execute('DELETE FROM category WHERE id = ?', (category_id,))
    
    conn.commit()
    conn.close()
def update_reseau_social(reseau_social):
    """Met à jour un réseau social dans la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE reseaux_sociaux
        SET name = ?, description = ?, date_modification = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (reseau_social['name'], reseau_social.get('description', ''), reseau_social['id']))
    conn.commit()
    conn.close()

def delete_reseau_social(reseau_social_id):
    """Supprime un réseau social de la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reseaux_sociaux WHERE id = ?', (reseau_social_id,))
    conn.commit()
    conn.close()
def save_category(category):
    """
    Sauvegarde une nouvelle catégorie dans la base de données.
    
    Args:
        category (dict): Un dictionnaire contenant les informations de la catégorie.
                         Doit contenir les clés 'name', 'label', et 'description'.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insérer la nouvelle catégorie dans la table
    cursor.execute('''
        INSERT INTO category (name, label, description)
        VALUES (?, ?, ?)
    ''', (category['name'], category.get('label', ''), category.get('description', '')))
    
    conn.commit()
    conn.close()

def load_reseaux_sociaux():
    """Charge tous les réseaux sociaux depuis la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reseaux_sociaux')
    reseaux_sociaux = cursor.fetchall()
    conn.close()
    return [dict(zip(['id', 'name', 'description', 'date_creation', 'date_modification', 'date_suppression'], rs)) for rs in reseaux_sociaux]


def load_media_types():
    """Charge tous les types de médias depuis la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM media_type')
    media_types = cursor.fetchall()
    conn.close()
    return [dict(zip(['id', 'type', 'label', 'description', 'date_creation', 'date_modification', 'date_suppression'], mt)) for mt in media_types]

def save_media_type(media_type):
    """Sauvegarde un nouveau type de média dans la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO media_type (type, label, description)
        VALUES (?, ?, ?)
    ''', (media_type['type'], media_type.get('label', ''), media_type.get('description', '')))
    conn.commit()
    conn.close()

def update_media_type(media_type):
    """Met à jour un type de média dans la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE media_type
        SET type = ?, label = ?, description = ?, date_modification = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (media_type['type'], media_type.get('label', ''), media_type.get('description', ''), media_type['id']))
    conn.commit()
    conn.close()

def delete_media_type(media_type_id):
    """Supprime un type de média de la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM media_type WHERE id = ?', (media_type_id,))
    conn.commit()
    conn.close()

def load_robots():
    """Charge tous les robots depuis la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM robots')
    robots = cursor.fetchall()
    conn.close()
    return [dict(zip(['id', 'name', 'label', 'description', 'category', 'reseau_social', 'date_creation', 'date_modification', 'date_suppression'], r)) for r in robots]

# def save_robot(robot):
#     """Sauvegarde un nouveau robot dans la base de données."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO robots (name, label, description, category, reseau_social)
#         VALUES (?, ?, ?, ?, ?)
#     ''', (robot['name'], robot.get('label', ''), robot.get('description', ''), robot.get('category', ''), robot.get('reseau_social', '')))
#     conn.commit()
#     conn.close()

# def update_robot(robot):
#     """Met à jour un robot dans la base de données."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('''
#         UPDATE robots
#         SET name = ?, label = ?, description = ?, category = ?, reseau_social = ?, date_modification = CURRENT_TIMESTAMP
#         WHERE id = ?
#     ''', (robot['name'], robot.get('label', ''), robot.get('description', ''), robot.get('category', ''), robot.get('reseau_social', ''), robot['id']))
#     conn.commit()
#     conn.close()

def delete_robot(robot_id):
    """Supprime un robot de la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM robots WHERE id = ?', (robot_id,))
    conn.commit()
    conn.close()


import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QDialog, QLineEdit, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt



# Boîte de dialogue pour éditer un réseau social
class EditReseauSocialDialog(QDialog):
    def __init__(self, reseau_social_id, parent=None):
        super().__init__(parent)
        self.reseau_social_id = reseau_social_id
        self.setWindowTitle("Edit Reseau Social")
        self.setFixedSize(400, 200)

        # Layout
        layout = QVBoxLayout(self)

        # Charger les données du réseau social
        self.reseau_social = self.load_reseau_social_data()

        # Champs de saisie
        self.name_input = QLineEdit(self.reseau_social['name'], self)
        self.name_input.setPlaceholderText("Enter name...")
        layout.addWidget(self.name_input)

        self.description_input = QLineEdit(self.reseau_social.get('description', ''), self)
        self.description_input.setPlaceholderText("Enter description...")
        layout.addWidget(self.description_input)

        # Boutons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_reseau_social)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def load_reseau_social_data(self):
        """Charge les données du réseau social à modifier."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reseaux_sociaux WHERE id = ?', (self.reseau_social_id,))
        reseau_social = cursor.fetchone()
        conn.close()
        return dict(zip(['id', 'name', 'description', 'date_creation', 'date_modification', 'date_suppression'], reseau_social))

    def save_reseau_social(self):
        """Sauvegarde les modifications du réseau social."""
        name = self.name_input.text().strip()
        description = self.description_input.text().strip()

        if name:
            reseau_social = {
                'id': self.reseau_social_id,
                'name': name,
                'description': description
            }
            update_reseau_social(reseau_social)
            self.accept()
        else:
            QMessageBox.warning(self, "Validation Error", "Name cannot be empty!")

# Tableau principal avec modification directe et boutons d'action
class ReseauSocialTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reseau Social Management")
        self.setFixedSize(800, 600)

        # Layout
        layout = QVBoxLayout(self)

        # Tableau
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Description", "Date Creation", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.setEditTriggers(QTableWidget.AllEditTriggers)  # Permettre la modification directe
        layout.addWidget(self.table)

        # Charger les données
        self.load_data()

    def load_data(self):
        """Charge les données des réseaux sociaux dans le tableau."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reseaux_sociaux')
        reseaux_sociaux = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(reseaux_sociaux))
        for row, reseau in enumerate(reseaux_sociaux):
            for col, data in enumerate(reseau):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

            # Bouton "Edit"
            edit_button = QPushButton("Edit", self)
            edit_button.clicked.connect(lambda _, r=row: self.edit_reseau_social(r))
            self.table.setCellWidget(row, 4, edit_button)

    def edit_reseau_social(self, row):
        """Ouvre la boîte de dialogue pour éditer un réseau social."""
        reseau_social_id = int(self.table.item(row, 0).text())
        dialog = EditReseauSocialDialog(reseau_social_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()  # Recharger les données après modification


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon

class FilterByRobotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Filter by Robot")
        self.setWindowIcon(QIcon("icons/filter.png"))  # Ajouter une icône
        self.setFixedSize(300, 150)

        # Layout
        layout = QVBoxLayout(self)

        # Robots ComboBox
        self.robots_combo = QComboBox(self)
        self.robots_combo.setStyleSheet("padding: 8px; font-size: 14px;")
        robots = load_robots()
        self.robots_combo.addItem("All Robots", None)  # Option pour afficher tous les groupes
        for robot in robots:
            self.robots_combo.addItem(robot['name'], robot['id'])
        layout.addWidget(self.robots_combo)

        # Buttons
        button_layout = QHBoxLayout()
        self.filter_button = QPushButton("Filter", self)
        self.filter_button.setIcon(QIcon("icons/filter.png"))  # Ajouter une icône
        self.filter_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #2196F3; color: white;")
        self.filter_button.clicked.connect(self.accept)
        button_layout.addWidget(self.filter_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))  # Ajouter une icône
        self.cancel_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #f44336; color: white;")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.selected_robot_id = None

    def accept(self):
        self.selected_robot_id = self.robots_combo.currentData()
        super().accept()

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class CategoryManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Category Management")
        self.setWindowIcon(QIcon("icons/category.png"))  # Ajouter une icône
        self.setFixedSize(600, 400)

        # Layout
        layout = QVBoxLayout(self)

        # Table to display categories
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)  # Ajouter une colonne "Actions"
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Label", "Description", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)  # Redimensionnement manuel
        self.table.setEditTriggers(QTableWidget.AllEditTriggers)  # Permettre la modification directe
        layout.addWidget(self.table)

        # Buttons for Add
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Category", self)
        self.add_button.setIcon(QIcon("icons/add.png"))  # Ajouter une icône
        self.add_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #4CAF50; color: white;")
        self.add_button.clicked.connect(self.add_category)
        button_layout.addWidget(self.add_button)

        layout.addLayout(button_layout)

        # Charger les catégories
        self.load_categories()

    def load_categories(self):
        """Charge les catégories dans la table."""
        categories = load_categories()
        self.table.setRowCount(len(categories))
        for row, category in enumerate(categories):
            # Colonne ID
            self.table.setItem(row, 0, QTableWidgetItem(str(category['id'])))
            self.table.item(row, 0).setFlags(self.table.item(row, 0).flags() & ~Qt.ItemIsEditable)  # ID non modifiable

            # Colonne Name
            self.table.setItem(row, 1, QTableWidgetItem(category['name']))

            # Colonne Label
            self.table.setItem(row, 2, QTableWidgetItem(category.get('label', '')))

            # Colonne Description
            self.table.setItem(row, 3, QTableWidgetItem(category.get('description', '')))

            # Colonne Actions
            action_button_layout = QHBoxLayout()
            action_button_layout.setStyleSheet("""
            QPushButton {
                padding: 10px 18px;
                font-size: 14px;
                font-weight: bold;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003d80;
            }
        """)
        
            edit_button = QPushButton("Edit", self)
            edit_button.setIcon(QIcon("icons/edit.png"))  # Ajouter une icône
            edit_button.setStyleSheet("padding: 5px; font-size: 12px; background-color: #FFC107; color: black;")
            edit_button.clicked.connect(lambda _, r=row: self.edit_category(r))
            action_button_layout.addWidget(edit_button)

            delete_button = QPushButton("Delete", self)
            delete_button.setIcon(QIcon("icons/delete.png"))  # Ajouter une icône
            delete_button.setStyleSheet("padding: 5px; font-size: 12px; background-color: #f44336; color: white;")
            delete_button.clicked.connect(lambda _, r=row: self.delete_category(r))
            action_button_layout.addWidget(delete_button)

            action_widget = QWidget()
            action_widget.setLayout(action_button_layout)
            self.table.setCellWidget(row, 4, action_widget)

    def add_category(self):
        """Ouvre une boîte de dialogue pour ajouter une catégorie."""
        dialog = AddCategoryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_categories()

    def edit_category(self, row):
        """Ouvre une boîte de dialogue pour modifier une catégorie."""
        category_id = int(self.table.item(row, 0).text())
        dialog = EditCategoryDialog(category_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_categories()

    def delete_category(self, row):
        """Supprime la catégorie sélectionnée."""
        category_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(
            self, "Confirm Delete", "Are you sure you want to delete this category?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_category(category_id)
            self.load_categories()

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon

class AddReseauSocialDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Reseau Social")
        self.setWindowIcon(QIcon("icons/add.png"))  # Ajouter une icône
        self.setFixedSize(400, 200)

        # Layout
        layout = QVBoxLayout(self)

        # Input fields
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")
        self.name_input.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.name_input)

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Description")
        self.description_input.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.description_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.save_button.setIcon(QIcon("icons/save.png"))  # Ajouter une icône
        self.save_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #4CAF50; color: white;")
        self.save_button.clicked.connect(self.save_reseau_social)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))  # Ajouter une icône
        self.cancel_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #f44336; color: white;")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def save_reseau_social(self):
        """Sauvegarde le nouveau réseau social."""
        name = self.name_input.text().strip()
        description = self.description_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Name cannot be empty!")
            return

        reseau_social = {
            'name': name,
            'description': description
        }
        save_reseau_social(reseau_social)
        self.accept()

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon

class AddCategoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Category")
        self.setWindowIcon(QIcon("icons/add.png"))  # Ajouter une icône
        self.setFixedSize(400, 250)

        # Layout
        layout = QVBoxLayout(self)

        # Input fields
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")
        self.name_input.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.name_input)

        self.label_input = QLineEdit(self)
        self.label_input.setPlaceholderText("Label")
        self.label_input.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.label_input)

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Description")
        self.description_input.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.description_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.save_button.setIcon(QIcon("icons/save.png"))  # Ajouter une icône
        self.save_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #4CAF50; color: white;")
        self.save_button.clicked.connect(self.save_category)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))  # Ajouter une icône
        self.cancel_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #f44336; color: white;")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def save_category(self):
        """Sauvegarde la nouvelle catégorie."""
        name = self.name_input.text().strip()
        label = self.label_input.text().strip()
        description = self.description_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Name cannot be empty!")
            return

        category = {
            'name': name,
            'label': label,
            'description': description
        }
        save_category(category)
        self.accept()
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon

class EditCategoryDialog(QDialog):
    def __init__(self, category_id, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.setWindowTitle("Edit Category")
        self.setWindowIcon(QIcon("icons/edit.png"))  # Ajouter une icône
        self.setFixedSize(400, 250)

        # Layout
        layout = QVBoxLayout(self)

        # Charger les données de la catégorie
        self.category = self.load_category_data()

        # Input fields
        self.name_input = QLineEdit(self.category['name'], self)
        self.name_input.setPlaceholderText("Name")
        self.name_input.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.name_input)

        self.label_input = QLineEdit(self.category.get('label', ''), self)
        self.label_input.setPlaceholderText("Label")
        self.label_input.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.label_input)

        self.description_input = QLineEdit(self.category.get('description', ''), self)
        self.description_input.setPlaceholderText("Description")
        self.description_input.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.description_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.save_button.setIcon(QIcon("icons/save.png"))  # Ajouter une icône
        self.save_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #4CAF50; color: white;")
        self.save_button.clicked.connect(self.save_category)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))  # Ajouter une icône
        self.cancel_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #f44336; color: white;")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def load_category_data(self):
        """Charge les données de la catégorie à modifier."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM category WHERE id = ?', (self.category_id,))
        category = cursor.fetchone()
        conn.close()
        return dict(zip(['id', 'name', 'label', 'description', 'date_creation', 'date_modification', 'date_suppression'], category))

    def save_category(self):
        """Sauvegarde les modifications de la catégorie."""
        name = self.name_input.text().strip()
        label = self.label_input.text().strip()
        description = self.description_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Name cannot be empty!")
            return

        category = {
            'id': self.category_id,
            'name': name,
            'label': label,
            'description': description
        }
        update_category(category)
        self.accept()

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt

class ReseauSocialManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reseau Social Management")
        self.setFixedSize(800, 600)

        # Layout
        layout = QVBoxLayout(self)

        # Table to display reseaux sociaux
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)  # Ajouter une colonne "Actions"
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Description", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)  # Redimensionnement manuel
        self.table.setEditTriggers(QTableWidget.AllEditTriggers)  # Permettre la modification directe
        layout.addWidget(self.table)

        # Buttons for Add
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Reseau Social", self)
        self.add_button.clicked.connect(self.add_reseau_social)
        button_layout.addWidget(self.add_button)

        layout.addLayout(button_layout)

        # Charger les réseaux sociaux
        self.load_reseaux_sociaux()

    def load_reseaux_sociaux(self):
        """Charge les réseaux sociaux dans la table."""
        reseaux_sociaux = load_reseaux_sociaux()
        self.table.setRowCount(len(reseaux_sociaux))
        for row, reseau in enumerate(reseaux_sociaux):
            # Colonne ID
            self.table.setItem(row, 0, QTableWidgetItem(str(reseau['id'])))
            self.table.item(row, 0).setFlags(self.table.item(row, 0).flags() & ~Qt.ItemIsEditable)  # ID non modifiable

            # Colonne Name
            self.table.setItem(row, 1, QTableWidgetItem(reseau['name']))

            # Colonne Description
            self.table.setItem(row, 2, QTableWidgetItem(reseau.get('description', '')))

            # Colonne Actions
            action_button_layout = QHBoxLayout()
            edit_button = QPushButton("Edit", self)
            edit_button.clicked.connect(lambda _, r=row: self.edit_reseau_social(r))
            action_button_layout.addWidget(edit_button)

            delete_button = QPushButton("Delete", self)
            delete_button.clicked.connect(lambda _, r=row: self.delete_reseau_social(r))
            action_button_layout.addWidget(delete_button)

            action_widget = QWidget()
            action_widget.setLayout(action_button_layout)
            self.table.setCellWidget(row, 3, action_widget)

    def add_reseau_social(self):
        """Ouvre une boîte de dialogue pour ajouter un réseau social."""
        dialog = AddReseauSocialDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_reseaux_sociaux()

    def edit_reseau_social(self, row):
        """Ouvre une boîte de dialogue pour modifier un réseau social."""
        reseau_id = int(self.table.item(row, 0).text())
        dialog = EditReseauSocialDialog(reseau_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_reseaux_sociaux()

    def delete_reseau_social(self, row):
        """Supprime le réseau social sélectionné."""
        reseau_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(
            self, "Confirm Delete", "Are you sure you want to delete this reseau social?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_reseau_social(reseau_id)
            self.load_reseaux_sociaux()


# class AddReseauSocialDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Add Reseau Social")
#         self.setFixedSize(400, 300)

#         # Layout
#         layout = QVBoxLayout(self)

#         # Input fields
#         self.name_input = QLineEdit(self)
#         self.name_input.setPlaceholderText("Name")
#         layout.addWidget(self.name_input)

#         self.description en me donnant tout les modal sous setting pour rappel voic mon db # Initialisation de la base de données




















# Chemin vers la base de données SQLite




def init_db():
    """Initialise la base de données SQLite avec des tables et des données par défaut."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table pour les catégories
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            label TEXT,
            description TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP,
            date_suppression TIMESTAMP
        )
    ''')

    # Table pour les réseaux sociaux
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reseaux_sociaux (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP,
            date_suppression TIMESTAMP
        )
    ''')

    # Table pour les types de médias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media_type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL UNIQUE,
            label TEXT,
            description TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP,
            date_suppression TIMESTAMP
        )
    ''')

    # Table pour les médias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            description TEXT,
            preview_path TEXT NOT NULL,
            type_id INTEGER NOT NULL,
            category_id INTEGER,
            date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP,
            date_suppression TIMESTAMP,
            est_supprime BOOLEAN DEFAULT 0,
            FOREIGN KEY (type_id) REFERENCES media_type(id),
            FOREIGN KEY (category_id) REFERENCES category(id)
        )
    ''')

    # Table pour les robots
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS robots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            label TEXT,
            description TEXT,
            creation_date TEXT,
            category TEXT,
            status TEXT,
            reseau_social_id INTEGER,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP,
            date_suppression TIMESTAMP,
            FOREIGN KEY(reseau_social_id) REFERENCES reseaux_sociaux(id)
        )
    ''')

    # Table de liaison entre robots et types de médias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS robot_media_type (
            robot_id INTEGER,
            media_type_id INTEGER,
            FOREIGN KEY(robot_id) REFERENCES robots(id),
            FOREIGN KEY(media_type_id) REFERENCES media_type(id)
        )
    ''')

    # Table pour les groupes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            link TEXT NOT NULL,
            remarks TEXT,
            category_id INTEGER,
            description TEXT,
            keywords TEXT,
            FOREIGN KEY(category_id) REFERENCES category(id)
        )
    ''')

    # Table de liaison entre groupes et robots
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_robot (
            group_id INTEGER,
            robot_id INTEGER,
            FOREIGN KEY(group_id) REFERENCES groups(id),
            FOREIGN KEY(robot_id) REFERENCES robots(id)
        )
    ''')

    # Table pour les identifiants
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS identifiant (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            reseau_social_id INTEGER,
            robot_id INTEGER,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP,
            date_suppression TIMESTAMP,
            FOREIGN KEY(reseau_social_id) REFERENCES reseaux_sociaux(id),
            FOREIGN KEY(robot_id) REFERENCES robots(id)
        )
    ''')


    # Table pour les archives
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS archive (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            robot_id INTEGER,
            reseau_social_id INTEGER,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP,
            date_suppression TIMESTAMP,
            version INTEGER DEFAULT 1,
            FOREIGN KEY(robot_id) REFERENCES robots(id),
            FOREIGN KEY(reseau_social_id) REFERENCES reseaux_sociaux(id)
        )
    ''')

    # Insertion des données par défaut

    # Catégories par défaut
    cursor.execute('''
        INSERT OR IGNORE INTO category (name, label, description)
        VALUES (?, ?, ?)
    ''', ('Default', 'Default Category', 'Default category description'))

    # Réseaux sociaux par défaut
    reseaux_sociaux = [
        ('Facebook', 'Réseau social Facebook'),
        ('WhatsApp', 'Application de messagerie WhatsApp'),
        ('Twitter', 'Réseau social Twitter')
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO reseaux_sociaux (name, description)
        VALUES (?, ?)
    ''', reseaux_sociaux)

    # Types de médias par défaut
    media_types = [
        ('Image', 'Image', 'Type de média pour les images'),
        ('Video', 'Vidéo', 'Type de média pour les vidéos')
    ] + [(f'media{i}', f'Media {i}', f'Description for Media {i}') for i in range(1, 11)]
    cursor.executemany('''
        INSERT OR IGNORE INTO media_type (type, label, description)
        VALUES (?, ?, ?)
    ''', media_types)

    # Robots par défaut
    robots = [
        ('Robot1', 'Robot 1', 'Description Robot 1', '2023-01-01', 'Category1', 'Active', 1),
        ('Robot2', 'Robot 2', 'Description Robot 2', '2023-01-01', 'Category2', 'Inactive', 2)
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO robots (name, label, description, creation_date, category, status, reseau_social_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', robots)

    # Groupes par défaut
    groups = [
        ('Group1', 'http://example.com/group1', 'Remarks 1', 1, 'Description 1', 'Keywords1'),
        ('Group2', 'http://example.com/group2', 'Remarks 2', 1, 'Description 2', 'Keywords2')
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO groups (name, link, remarks, category_id, description, keywords)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', groups)

    conn.commit()
    conn.close()

# Exécuter l'initialisation
init_db()

# Chargement des données
def load_groups(robot_id=None):
    """Charge les groupes depuis la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if robot_id:
        cursor.execute('''
            SELECT groups.* FROM groups
            JOIN group_robot ON groups.id = group_robot.group_id
            WHERE group_robot.robot_id = ?
        ''', (robot_id,))
    else:
        cursor.execute('SELECT * FROM groups')
    groups = cursor.fetchall()
    conn.close()
    return [dict(zip(['id', 'name', 'link', 'remarks', 'category_id', 'description', 'keywords'], group)) for group in groups]

def load_robots():
    """Charge les robots depuis la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM robots')
    robots = cursor.fetchall()
    conn.close()
    return [dict(zip(['id', 'name', 'label', 'description', 'creation_date', 'category', 'status', 'reseau_social_id', 'date_creation', 'date_modification', 'date_suppression'], robot)) for robot in robots]

def load_categories():
    """Charge les catégories depuis la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM category')
    categories = cursor.fetchall()
    conn.close()
    return [dict(zip(['id', 'name', 'label', 'description', 'date_creation', 'date_modification', 'date_suppression'], category)) for category in categories]

def save_group(group):
    """Sauvegarde un groupe dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO groups (name, link, remarks, category_id, description, keywords)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (group['name'], group['link'], group['remarks'], group['category_id'], group['description'], group.get('keywords', '')))
    conn.commit()
    conn.close()

def update_group(group):
    """Met à jour un groupe dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE groups
        SET name = ?, link = ?, remarks = ?, category_id = ?, description = ?, keywords = ?
        WHERE id = ?
    ''', (group['name'], group['link'], group['remarks'], group['category_id'], group['description'], group.get('keywords', ''), group['id']))
    conn.commit()
    conn.close()

def delete_group(group_id):
    """Supprime un groupe de la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM groups WHERE id = ?', (group_id,))
    conn.commit()
    conn.close()
# def delete_group1(self, row):
#     group = self.filtered_groups[row]
#     dialog = ConfirmationDialog(self, title="Delete Group", message="Are you sure you want to delete this group?")
#     if dialog.exec_() == QDialog.Accepted:
#         delete_group(group['id'])
#         self.all_groups = load_groups()
#         self.filtered_groups = self.all_groups
#         self.populate_table()
# def save_robot(robot):
#     """Sauvegarde un robot dans la base de données SQLite."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO robots (name, label, description, creation_date, category, status, reseau_social_id)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#     ''', (robot['name'], robot.get('label', ''), robot['description'], robot['creation_date'], robot['category'], robot['status'], robot.get('reseau_social_id', None)))
#     conn.commit()
#     conn.close()

def save_robot(robot):
    """Sauvegarde un robot dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO robots (name, label, description, creation_date, category, status, reseau_social_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (robot['name'], robot.get('label', ''), robot['description'], robot['creation_date'], robot['category'], robot['status'], robot.get('reseau_social_id', None)))
    conn.commit()
    conn.close()

def update_robot(robot):
    """Met à jour un robot dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE robots
        SET name = ?, label = ?, description = ?, creation_date = ?, category = ?, status = ?, reseau_social_id = ?
        WHERE id = ?
    ''', (robot['name'], robot.get('label', ''), robot['description'], robot['creation_date'], robot['category'], robot['status'], robot.get('reseau_social_id', None), robot['id']))
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
    return [dict(zip(['id', 'name', 'label', 'description', 'creation_date', 'category', 'status', 'reseau_social_id', 'date_creation', 'date_modification', 'date_suppression'], robot)) for robot in robots]

def save_media_type(media_type):
    """Sauvegarde un type de média dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO media_type (type, label, description)
        VALUES (?, ?, ?)
    ''', (media_type['type'], media_type.get('label', ''), media_type.get('description', '')))
    conn.commit()
    conn.close()

def update_media_type(media_type):
    """Met à jour un type de média dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE media_type
        SET type = ?, label = ?, description = ?
        WHERE id = ?
    ''', (media_type['type'], media_type.get('label', ''), media_type.get('description', ''), media_type['id']))
    conn.commit()
    conn.close()

def delete_media_type(media_type_id):
    """Supprime un type de média de la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM media_type WHERE id = ?', (media_type_id,))
    conn.commit()
    conn.close()

def save_reseau_social(reseau_social):
    """Sauvegarde un réseau social dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reseaux_sociaux (name, description)
        VALUES (?, ?)
    ''', (reseau_social['name'], reseau_social.get('description', '')))
    conn.commit()
    conn.close()

def update_reseau_social(reseau_social):
    """Met à jour un réseau social dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE reseaux_sociaux
        SET name = ?, description = ?
        WHERE id = ?
    ''', (reseau_social['name'], reseau_social.get('description', ''), reseau_social['id']))
    conn.commit()
    conn.close()

def delete_reseau_social(reseau_social_id):
    """Supprime un réseau social de la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reseaux_sociaux WHERE id = ?', (reseau_social_id,))
    conn.commit()
    conn.close()

def save_identifiant(identifiant):
    """Sauvegarde un identifiant dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO identifiant (username, password, reseau_social_id, robot_id)
        VALUES (?, ?, ?, ?)
    ''', (identifiant['username'], identifiant['password'], identifiant['reseau_social_id'], identifiant['robot_id']))
    conn.commit()
    conn.close()

def update_identifiant(identifiant):
    """Met à jour un identifiant dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE identifiant
        SET username = ?, password = ?, reseau_social_id = ?, robot_id = ?
        WHERE id = ?
    ''', (identifiant['username'], identifiant['password'], identifiant['reseau_social_id'], identifiant['robot_id'], identifiant['id']))
    conn.commit()
    conn.close()

def delete_identifiant(identifiant_id):
    """Supprime un identifiant de la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM identifiant WHERE id = ?', (identifiant_id,))
    conn.commit()
    conn.close()

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


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QFormLayout, QMessageBox
from PyQt5.QtGui import QIcon

class AddGroupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Add Group"))
        self.setWindowIcon(QIcon("icons/add.png"))  # Ajouter une icône
        self.setFixedSize(500, 450)

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
            }
            QComboBox, QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-bottom: 10px;
                background-color: #fff;
            }
            QComboBox:focus, QLineEdit:focus {
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
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
        """)

        # Layout
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Inputs
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText(self.tr("Enter group name..."))

        self.link_input = QLineEdit(self)
        self.link_input.setPlaceholderText(self.tr("Enter group link..."))

        self.remarks_input = QLineEdit(self)
        self.remarks_input.setPlaceholderText(self.tr("Enter remarks..."))

        self.category_combo = QComboBox(self)  # ComboBox pour sélectionner la catégorie
        self.category_combo.setPlaceholderText(self.tr("Select a category..."))

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText(self.tr("Enter description..."))

        self.keywords_input = QLineEdit(self)
        self.keywords_input.setPlaceholderText(self.tr("Enter keywords..."))

        # Charger les catégories depuis la base de données
        self.load_categories()

        # Ajouter les champs au formulaire
        form_layout.addRow(self.tr("Name:"), self.name_input)
        form_layout.addRow(self.tr("Link:"), self.link_input)
        form_layout.addRow(self.tr("Remarks:"), self.remarks_input)
        form_layout.addRow(self.tr("Category:"), self.category_combo)
        form_layout.addRow(self.tr("Description:"), self.description_input)
        form_layout.addRow(self.tr("Keywords:"), self.keywords_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton(self.tr("Submit"), self)
        self.submit_button.setIcon(QIcon("icons/save.png"))  # Ajouter une icône
        self.submit_button.clicked.connect(self.add_group)

        self.cancel_button = QPushButton(self.tr("Cancel"), self)
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))  # Ajouter une icône
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def load_categories(self):
        """Charge les catégories depuis la base de données et les ajoute au ComboBox."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM category')
        categories = cursor.fetchall()
        self.category_combo.clear()
        for category in categories:
            self.category_combo.addItem(category[1], category[0])  # Ajouter le nom de la catégorie et son ID
        conn.close()

    def add_group(self):
        """Valide et enregistre les données du groupe."""
        # Validation des champs obligatoires
        if not self.name_input.text().strip():
            QMessageBox.warning(self, self.tr("Validation Error"), self.tr("Name cannot be empty!"))
            return
        if not self.link_input.text().strip():
            QMessageBox.warning(self, self.tr("Validation Error"), self.tr("Link cannot be empty!"))
            return
        if self.category_combo.currentIndex() == -1:
            QMessageBox.warning(self, self.tr("Validation Error"), self.tr("Please select a category!"))
            return

        # Récupérer l'ID de la catégorie sélectionnée
        category_id = self.category_combo.currentData()

        # Enregistrer les données dans la base de données
        new_group = {
            'name': self.name_input.text().strip(),
            'link': self.link_input.text().strip(),
            'remarks': self.remarks_input.text().strip(),
            'category_id': category_id,
            'description': self.description_input.text().strip(),
            'keywords': self.keywords_input.text().strip()
        }
        self.save_group(new_group)
        QMessageBox.information(self, self.tr("Success"), self.tr("Group added successfully!"))
        self.accept()

    def save_group(self, group):
        """Enregistre le groupe dans la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO groups (name, link, remarks, category_id, description, keywords)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            group['name'],
            group['link'],
            group['remarks'],
            group['category_id'],
            group['description'],
            group['keywords']
        ))
        conn.commit()
        conn.close()




from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QFormLayout, QMessageBox
from PyQt5.QtGui import QIcon

class AssignGroupToRobotDialog(QDialog):
    def __init__(self, group_id, parent=None):
        super().__init__(parent)
        self.group_id = group_id
        self.setWindowTitle(self.tr("Assign Group to Robot"))
        self.setWindowIcon(QIcon("icons/assign.png"))  # Ajouter une icône
        self.setFixedSize(400, 200)

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
            }
            QComboBox {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-bottom: 10px;
                background-color: #fff;
            }
            QComboBox:focus {
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
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
        """)

        # Layout
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Robots ComboBox
        self.robots_combo = QComboBox(self)
        self.robots_combo.setPlaceholderText(self.tr("Select a robot..."))
        robots = load_robots()
        for robot in robots:
            self.robots_combo.addItem(robot['name'], robot['id'])
        form_layout.addRow(self.tr("Select Robot:"), self.robots_combo)

        # Buttons
        button_layout = QHBoxLayout()
        self.assign_button = QPushButton(self.tr("Assign"), self)
        self.assign_button.setIcon(QIcon("icons/save.png"))  # Ajouter une icône
        self.assign_button.clicked.connect(self.assign_group)

        self.cancel_button = QPushButton(self.tr("Cancel"), self)
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))  # Ajouter une icône
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.assign_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def assign_group(self):
        """Assigne le groupe au robot sélectionné."""
        robot_id = self.robots_combo.currentData()
        if not robot_id:
            QMessageBox.warning(self, self.tr("Validation Error"), self.tr("Please select a robot!"))
            return

        assign_group_to_robot(self.group_id, robot_id)
        QMessageBox.information(self, self.tr("Success"), self.tr("Group assigned to robot successfully!"))
        self.accept()


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MediaTypeManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Media Type Management")
        self.setWindowIcon(QIcon("icons/media.png"))  # Ajouter une icône
        self.setFixedSize(600, 400)

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            QTableWidget {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #007bff;
                color: white;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                font-size: 14px;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
        """)

        # Layout
        layout = QVBoxLayout(self)

        # Table to display media types
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)  # Ajouter une colonne "Actions"
        self.table.setHorizontalHeaderLabels(["ID", "Type", "Label", "Description", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)  # Redimensionnement manuel
        self.table.setEditTriggers(QTableWidget.AllEditTriggers)  # Permettre la modification directe
        layout.addWidget(self.table)

        # Buttons for Add
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Media Type", self)
        self.add_button.setIcon(QIcon("icons/add.png"))  # Ajouter une icône
        self.add_button.clicked.connect(self.add_media_type)
        button_layout.addWidget(self.add_button)

        layout.addLayout(button_layout)

        # Charger les types de médias
        self.load_media_types()

    def load_media_types(self):
        """Charge les types de médias dans la table."""
        media_types = load_media_types()
        self.table.setRowCount(len(media_types))
        for row, media_type in enumerate(media_types):
            # Colonne ID
            self.table.setItem(row, 0, QTableWidgetItem(str(media_type['id'])))
            self.table.item(row, 0).setFlags(self.table.item(row, 0).flags() & ~Qt.ItemIsEditable)  # ID non modifiable

            # Colonne Type
            self.table.setItem(row, 1, QTableWidgetItem(media_type['type']))

            # Colonne Label
            self.table.setItem(row, 2, QTableWidgetItem(media_type.get('label', '')))

            # Colonne Description
            self.table.setItem(row, 3, QTableWidgetItem(media_type.get('description', '')))

            # Colonne Actions
            action_button_layout = QHBoxLayout()
            edit_button = QPushButton("Edit", self)
            edit_button.setIcon(QIcon("icons/edit.png"))  # Ajouter une icône
            edit_button.setStyleSheet("padding: 5px; font-size: 12px; background-color: #FFC107; color: black;")
            edit_button.clicked.connect(lambda _, r=row: self.edit_media_type(r))
            action_button_layout.addWidget(edit_button)

            delete_button = QPushButton("Delete", self)
            delete_button.setIcon(QIcon("icons/delete.png"))  # Ajouter une icône
            delete_button.setStyleSheet("padding: 5px; font-size: 12px; background-color: #f44336; color: white;")
            delete_button.clicked.connect(lambda _, r=row: self.delete_media_type(r))
            action_button_layout.addWidget(delete_button)

            action_widget = QWidget()
            action_widget.setLayout(action_button_layout)
            self.table.setCellWidget(row, 4, action_widget)

    def add_media_type(self):
        """Ouvre une boîte de dialogue pour ajouter un type de média."""
        dialog = AddMediaTypeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_media_types()

    def edit_media_type(self, row):
        """Ouvre une boîte de dialogue pour modifier un type de média."""
        media_type_id = int(self.table.item(row, 0).text())
        dialog = EditMediaTypeDialog(media_type_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_media_types()

    def delete_media_type(self, row):
        """Supprime le type de média sélectionné."""
        media_type_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(
            self, "Confirm Delete", "Are you sure you want to delete this media type?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_media_type(media_type_id)
            self.load_media_types()


class GroupTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.all_groups = load_groups()  # All groups loaded initially
        self.filtered_groups = self.all_groups  # Groups after filtering
        self.visible_columns = ['Select', 'Name', 'Link', 'Remarks', 'Category', 'Description', 'Verification', 'Actions']
        self.items_per_page = 25
        self.current_page = 1

        # Main layout
        layout = QVBoxLayout(self)

        header = HeaderSection(self, title="FBK GRUP MANAGEMENT", app_name="Nova360 AI", slogan="AI Marketing Automation Solution")
        layout.addWidget(header)

        # Top layout for buttons, search bar, and dropdowns
        top_layout = QHBoxLayout()

        # Action button with dropdown menu
        self.action_button = QPushButton("⚡ Action", self)
        self.action_menu = QMenu(self)

        # Actions for the Action menu
        self.import_action = QAction("📥 " + self.tr("Import Groups"), self)
        self.export_action = QAction("📤 " + self.tr("Export Groups"), self)
        self.reload_action = QAction("🔄 " + self.tr("Reload Groups"), self)
        self.delete_selected_action = QAction("❌ " + self.tr("Delete Selected"), self)
        self.delete_all_action = QAction("🗑️ " + self.tr("Delete All"), self)
        self.add_group_action = QAction("➕ " + self.tr("Add Group"), self)

        # Connect actions
        self.import_action.triggered.connect(self.import_groups)
        self.export_action.triggered.connect(self.export_groups)
        self.reload_action.triggered.connect(self.open_load_groups_dialog)
        self.delete_selected_action.triggered.connect(self.delete_selected_groups)
        self.delete_all_action.triggered.connect(self.delete_all_groups)
        self.add_group_action.triggered.connect(self.open_add_group_dialog)

        # Add actions to the Action menu
        self.action_menu.addAction(self.import_action)
        self.action_menu.addAction(self.export_action)
        self.action_menu.addAction(self.reload_action)
        self.action_menu.addSeparator()
        self.action_menu.addAction(self.delete_selected_action)
        self.action_menu.addAction(self.delete_all_action)
        self.action_menu.addSeparator()
        self.action_menu.addAction(self.add_group_action)

        self.action_button.setMenu(self.action_menu)
        self.action_button.setStyleSheet("""
            QPushButton {
                padding: 10px 18px;
                font-size: 14px;
                font-weight: bold;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003d80;
            }
        """)
        
        top_layout.addWidget(self.action_button)

        # Settings button with dropdown menu
        self.settings_button = QPushButton("⚙️ Settings", self)
        self.settings_button.setStyleSheet("""
            QPushButton {
                padding: 10px 18px;
                font-size: 14px;
                font-weight: bold;
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #343a40;
            }
        """)
        self.settings_menu = QMenu(self)

        # Actions for the Settings menu
        self.category_management_action = QAction("📂 " + self.tr("Category Management"), self)
        self.social_network_management_action = QAction("🌐 " + self.tr("Social Network Management"), self)
        
        
        self.media_type_management_action = QAction("🎥 " + self.tr("Media Type Management"), self)


# Replace this line:
# top_layout.addWidget(self.archive_management_action)

        # # With the following:
        # self.archive_management_button = QPushButton("📂 Archive Management", self)
        # self.archive_management_button.setStyleSheet("""
        #     padding: 8px 16px;
        #     font-size: 14px;
        #     background-color: #6c757d;
        #     color: white;
        #     border-radius: 6px;
        # """)
        # self.archive_management_button.clicked.connect(self.archive_management_action.trigger)  # Connect the action
        # #top_layout.addWidget(archive_management_button)

      
        self.robot_management_action = QAction("🔄 " + self.tr("Robot Management"), self)
        self.update_active_robot = QAction("🤖 " + self.tr("Activate Robot "), self)

        # Connect actions
        self.category_management_action.triggered.connect(self.open_category_management_dialog)
        self.social_network_management_action.triggered.connect(self.open_social_network_management_dialog)
        self.media_type_management_action.triggered.connect(self.open_media_type_management_dialog)
        self.robot_management_action.triggered.connect(self.open_robot_management_dialog)
        self.update_active_robot.triggered.connect(self.open_update_robot_dialog)

        # Add actions to the Settings menu
        self.settings_menu.addAction(self.category_management_action)
        self.settings_menu.addAction(self.social_network_management_action)
        self.settings_menu.addAction(self.media_type_management_action)
        self.settings_menu.addAction(self.robot_management_action)
        self.settings_menu.addAction(self.update_active_robot)

        self.settings_button.setMenu(self.settings_menu)
        top_layout.addWidget(self.settings_button)

        # Update Robot button
        self.update_robot_button = QPushButton("🤖 " + self.tr("Update Robot"), self)
        self.update_robot_button.clicked.connect(self.open_update_robot_dialog)
        self.update_robot_button.setStyleSheet("""
            QPushButton {
                padding: 10px 18px;
                font-size: 14px;
                font-weight: bold;
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #117a8b;
            }
            QPushButton:pressed {
                background-color: #0d5c73;
            }
        """)
        top_layout.addWidget(self.update_robot_button)

        # Spacer to push the search bar to the center
        top_layout.addStretch()

        # Search bar
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText(self.tr("🔍 Search groups..."))
        self.search_field.textChanged.connect(self.filter_table)
        self.search_field.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #007BFF;
                box-shadow: 0 0 8px rgba(0, 123, 255, 0.5);
            }
        """)
        top_layout.addWidget(self.search_field)

        # Filter by Robot button
        self.filter_robot_button = QPushButton("🤖 " + self.tr("Filter by Robot"), self)
        self.filter_robot_button.setStyleSheet("""
            QPushButton {
                padding: 10px 18px;
                font-size: 14px;
                font-weight: bold;
                background-color: #6c757d;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #343a40;
            }
        """)
        self.filter_robot_button.clicked.connect(self.open_filter_robot_dialog)
        top_layout.addWidget(self.filter_robot_button)

        # Add the top layout to the main layout
        layout.addLayout(top_layout)

        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.visible_columns))
        self.table.setHorizontalHeaderLabels(self.visible_columns)

        # Activer le redimensionnement manuel des colonnes
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        # Définir des largeurs par défaut pour les colonnes
        self.table.setColumnWidth(0, 50)   # Colonne "Select"
        self.table.setColumnWidth(1, 150)  # Colonne "Name"
        self.table.setColumnWidth(2, 250)  # Colonne "Link"
        self.table.setColumnWidth(3, 100)  # Colonne "Remarks"
        self.table.setColumnWidth(4, 120)  # Colonne "Category"
        self.table.setColumnWidth(5, 200)  # Colonne "Description"
        self.table.setColumnWidth(6, 100)  # Colonne "Verification"
        self.table.setColumnWidth(7, 100)  # Colonne "Actions"

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QTableWidget.AllEditTriggers)
        self.table.cellChanged.connect(self.on_cell_changed)
      # Activer le redimensionnement manuel des lignes
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)


        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setStyleSheet(self.table_styles())

        layout.addWidget(self.table)

        # Column visibility checkboxes
        self.checkboxes_layout = QHBoxLayout()
        for index, col_name in enumerate(self.visible_columns):
            checkbox = QCheckBox(self.tr(col_name))
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(lambda state, idx=index: self.update_visible_columns(idx, state))
            self.checkboxes_layout.addWidget(checkbox)
        layout.addLayout(self.checkboxes_layout)

        # Pagination
        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("⬅️ " + self.tr("Previous"), self)
        self.prev_button.clicked.connect(self.previous_page)
        self.pagination_layout.addWidget(self.prev_button)

        self.pagination_label = QLabel(self.tr(f"Page {self.current_page}"), self)
        self.pagination_layout.addWidget(self.pagination_label)

        self.next_button = QPushButton("➡️ " + self.tr("Next"), self)
        self.next_button.clicked.connect(self.next_page)
        self.pagination_layout.addWidget(self.next_button)

        layout.addLayout(self.pagination_layout)

        # Initialization
        self.update_pagination_buttons()
        self.populate_table()
        # Ajouter le footer
        footer = FooterSection(self)
        layout.addWidget(footer)
    def manage_archives(self):
        """Open a dialog to manage archives."""
        # dialog = ManageArchivesDialog(self.media_manager, self.user_choice, self)
        # dialog.exec_()
        pass
    def delete_selected_groups(self):
        pass
    def delete_all_groups(self):
     pass
    def open_social_network_management_dialog(self):
        pass
    def table_styles2(self):
        """Returns CSS styles for the table."""
        return """
            QTableWidget {
                font-size: 14px;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #007BFF;
                color: white;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #007BFF;
                color: white;
            }
        """

    def update_visible_columns(self, index, state):
        self.table.setColumnHidden(index, not state)


    def open_filter_robot_dialog(self):
        """Ouvre une boîte de dialogue pour filtrer les groupes par robot."""
        dialog = FilterByRobotDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            robot_id = dialog.selected_robot_id
            if robot_id:
                self.filtered_groups = load_groups(robot_id)
            else:
                self.filtered_groups = self.all_groups
            self.current_page = 1
            self.update_pagination_buttons()
            self.populate_table()

    def open_category_management_dialog(self):
        """Ouvre une boîte de dialogue pour gérer les catégories."""
        dialog = CategoryManagementDialog(self)
        dialog.exec_()

    def open_reseau_social_management_dialog(self):
        """Ouvre une boîte de dialogue pour gérer les réseaux sociaux."""
        dialog = ReseauSocialManagementDialog(self)
        dialog.exec_()

    def open_media_type_management_dialog(self):
        """Ouvre une boîte de dialogue pour gérer les types de médias."""
        dialog = MediaTypeManagementDialog(self)
        dialog.exec_()

    def open_robot_management_dialog(self):
        """Ouvre une boîte de dialogue pour gérer les robots."""
        dialog = RobotManagementDialog(self)
        dialog.exec_()

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
            # Checkbox pour la sélection
            checkbox = QCheckBox()
            self.table.setCellWidget(row, 0, checkbox)

            # Colonnes modifiables
            for col, key in enumerate(['name', 'link', 'remarks', 'description']):
                item = QTableWidgetItem(group.get(key, ''))
                self.table.setItem(row, col + 1, item)

            # Colonne "Category" avec QComboBox
            category_combo = QComboBox()
            categories = load_categories()  # Charger les catégories depuis la base de données
            for category in categories:
                category_combo.addItem(category['name'], category['id'])
            index = category_combo.findData(group.get('category_id'))
            if index >= 0:
                category_combo.setCurrentIndex(index)
            category_combo.currentIndexChanged.connect(lambda idx, r=row: self.update_group_category(r, category_combo.itemData(idx)))
            self.table.setCellWidget(row, 4, category_combo)  # "Category" est à l'index 4

            # Bouton "Verify"
            verify_button = QPushButton('Verify', self)
            verify_button.clicked.connect(lambda _, link=group.get('link', ''): self.open_link_in_browser(link))
            self.table.setCellWidget(row, 6, verify_button)  # "Verification" est à l'index 6

            # Bouton "Actions" avec menu déroulant
            action_button = QPushButton('Actions', self)
            action_menu = QMenu(self)
            action_button.setStyleSheet("""
                QPushButton {
                    padding: 10px 18px;
                    font-size: 14px;
                    font-weight: bold;
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QPushButton:pressed {
                    background-color: #003d80;
                }
            """)
            
            show_action = QAction('Show', self)
            edit_action = QAction('Edit', self)
            delete_action = QAction('Delete', self)
            assign_action = QAction('Assign to Robot', self)

            show_action.triggered.connect(lambda _, r=row: self.show_group(r))
            edit_action.triggered.connect(lambda _, r=row: self.edit_group(r))
            delete_action.triggered.connect(lambda _, r=row: self.delete_group(r))
            assign_action.triggered.connect(lambda _, r=row: self.assign_group_to_robot(r))

            action_menu.addAction(show_action)
            action_menu.addAction(edit_action)
            action_menu.addAction(delete_action)
            action_menu.addAction(assign_action)
            action_button.setMenu(action_menu)
            self.table.setCellWidget(row, 7, action_button)  # "Actions" est à l'index 7

        # Connecter le signal cellChanged pour mettre à jour la base de données
        self.table.cellChanged.connect(self.on_cell_changed)

    def on_cell_changed(self, row, column):
        """Slot appelé lorsqu'une cellule est modifiée."""
        group_id = self.filtered_groups[row]['id']
        new_value = self.table.item(row, column).text()

        if column == 1:  # Colonne "Name"
            self.update_group_name(group_id, new_value)
        elif column == 2:  # Colonne "Link"
            self.update_group_link(group_id, new_value)
        elif column == 3:  # Colonne "Remarks"
            self.update_group_remarks(group_id, new_value)
        elif column == 5:  # Colonne "Description"
            self.update_group_description(group_id, new_value)

    def update_group_name(self, group_id, new_name):
        """Met à jour le nom du groupe dans la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE groups SET name = ? WHERE id = ?', (new_name, group_id))
        conn.commit()
        conn.close()

    def update_group_link(self, group_id, new_link):
        """Met à jour le lien du groupe dans la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE groups SET link = ? WHERE id = ?', (new_link, group_id))
        conn.commit()
        conn.close()

    def update_group_remarks(self, group_id, new_remarks):
        """Met à jour les remarques du groupe dans la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE groups SET remarks = ? WHERE id = ?', (new_remarks, group_id))
        conn.commit()
        conn.close()

    def update_group_description(self, group_id, new_description):
        """Met à jour la description du groupe dans la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE groups SET description = ? WHERE id = ?', (new_description, group_id))
        conn.commit()
        conn.close()

    def update_group_category(self, row, category_id):
        """Met à jour la catégorie du groupe dans la base de données."""
        group_id = self.filtered_groups[row]['id']
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE groups SET category_id = ? WHERE id = ?', (category_id, group_id))
        conn.commit()
        conn.close()


    def load_categories1(self):
        """Charge les catégories depuis la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM categories')
        categories = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
        conn.close()
        return categories

    def update_group_category(self, row, category_id):
        """Met à jour la catégorie du groupe dans la base de données."""
        group_id = self.filtered_groups[row]['id']
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE groups SET category_id = ? WHERE id = ?', (category_id, group_id))
        conn.commit()
        conn.close()


    def show_group(self, row):
        """Affiche les détails du groupe."""
        group = self.filtered_groups[row]
        print(group)  # Pour déboguer

        # Récupérer l'ID de la catégorie
        category_id = group.get('category_id', 'N/A')

        # Afficher les détails du groupe
        QMessageBox.information(
            self,
            "Group Details",
            f"Name: {group['name']}\nLink: {group['link']}\nCategory ID: {category_id}"
        )

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
        # Récupérer le groupe à éditer
        group = self.filtered_groups[row]

        # Ouvrir la boîte de dialogue d'édition
        dialog = AddGroupDialog(self)
        dialog.name_input.setText(group.get('name', ''))
        dialog.link_input.setText(group.get('link', ''))
        dialog.remarks_input.setText(group.get('remarks', ''))
        dialog.description_input.setText(group.get('description', ''))
        dialog.keywords_input.setText(group.get('keywords', ''))

        # Définir la catégorie sélectionnée dans le QComboBox
        category_name = group.get('category', '')
        if category_name:
            index = dialog.category_combo.findText(category_name)
            if index >= 0:
                dialog.category_combo.setCurrentIndex(index)

        # Si la boîte de dialogue est validée
        if dialog.exec_() == QDialog.Accepted:
            # Récupérer les nouvelles valeurs
            updated_group = {
                'id': group['id'],  # Conserver l'ID du groupe
                'name': dialog.name_input.text().strip(),
                'link': dialog.link_input.text().strip(),
                'remarks': dialog.remarks_input.text().strip(),
                'category_id': dialog.category_combo.currentData(),  # Récupérer l'ID de la catégorie sélectionnée
                'description': dialog.description_input.text().strip(),
                'keywords': dialog.keywords_input.text().strip()
            }

            # Mettre à jour le groupe dans la base de données
            self.update_group(updated_group)

            # Recharger les groupes et mettre à jour l'affichage
            self.all_groups = load_groups()
            self.filtered_groups = self.all_groups
            self.populate_table()
    def delete_group(self, row):
        group = self.filtered_groups[row]
        delete_group(group['id'])
        self.all_groups = load_groups()
        self.filtered_groups = self.all_groups
        self.populate_table()
    def update_group(self, group):
        """Met à jour un groupe dans la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE groups
            SET name = ?, link = ?, remarks = ?, category_id = ?, description = ?, keywords = ?
            WHERE id = ?
        ''', (
            group['name'],
            group['link'],
            group['remarks'],
            group['category_id'],
            group['description'],
            group['keywords'],
            group['id']
        ))
        conn.commit()
        conn.close()
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

    def open_settings_dialog(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtGui import QIcon
import sqlite3

class EditMediaTypeDialog(QDialog):
    def __init__(self, media_type_id, parent=None):
        super().__init__(parent)
        self.media_type_id = media_type_id
        self.setWindowTitle("Edit Media Type")
        self.setWindowIcon(QIcon("icons/edit.png"))  # Ajouter une icône
        self.setFixedSize(400, 250)

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-bottom: 10px;
                background-color: #fff;
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
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
        """)

        # Layout
        layout = QVBoxLayout(self)

        # Charger les données du type de média
        self.media_type = self.load_media_type_data()

        # Input fields
        self.type_input = QLineEdit(self.media_type['type'], self)
        self.type_input.setPlaceholderText("Enter media type...")
        layout.addWidget(self.type_input)

        self.label_input = QLineEdit(self.media_type.get('label', ''), self)
        self.label_input.setPlaceholderText("Enter label...")
        layout.addWidget(self.label_input)

        self.description_input = QLineEdit(self.media_type.get('description', ''), self)
        self.description_input.setPlaceholderText("Enter description...")
        layout.addWidget(self.description_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.save_button.setIcon(QIcon("icons/save.png"))  # Ajouter une icône
        self.save_button.clicked.connect(self.save_media_type)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))  # Ajouter une icône
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def load_media_type_data(self):
        """Charge les données du type de média à modifier."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM media_type WHERE id = ?', (self.media_type_id,))
        media_type = cursor.fetchone()
        conn.close()
        return dict(zip(['id', 'type', 'label', 'description', 'date_creation', 'date_modification', 'date_suppression'], media_type))

    def save_media_type(self):
        """Sauvegarde les modifications du type de média."""
        type_ = self.type_input.text().strip()
        label = self.label_input.text().strip()
        description = self.description_input.text().strip()

        if not type_:
            QMessageBox.warning(self, "Validation Error", "Type cannot be empty!")
            return

        media_type = {
            'id': self.media_type_id,
            'type': type_,
            'label': label,
            'description': description
        }
        update_media_type(media_type)
        QMessageBox.information(self, "Success", "Media type updated successfully!")
        self.accept()

class AddMediaTypeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Media Type")
        self.setMinimumSize(400, 300)

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
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
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
        """)

        # Layout
        layout = QVBoxLayout(self)

        # Input fields
        self.type_input = QLineEdit(self)
        self.type_input.setPlaceholderText("Type (e.g., Video, Audio)")
        layout.addWidget(self.type_input)

        self.label_input = QLineEdit(self)
        self.label_input.setPlaceholderText("Label (e.g., Video Content)")
        layout.addWidget(self.label_input)

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Description (e.g., Media for video content)")
        layout.addWidget(self.description_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.save_button.setIcon(QIcon("icons/save.png"))  # Ajouter une icône
        self.save_button.clicked.connect(self.save_media_type)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))  # Ajouter une icône
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def save_media_type(self):
        """Sauvegarde le nouveau type de média."""
        type_ = self.type_input.text().strip()
        label = self.label_input.text().strip()
        description = self.description_input.text().strip()

        if not type_:
            QMessageBox.warning(self, "Validation Error", "Type cannot be empty!")
            return

        if not label:
            QMessageBox.warning(self, "Validation Error", "Label cannot be empty!")
            return

        media_type = {
            'type': type_,
            'label': label,
            'description': description
        }
        save_media_type(media_type)
        QMessageBox.information(self, "Success", "Media type saved successfully!")
        self.accept()

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QDateTimeEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime

class AddRobotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Robot")
        self.setWindowIcon(QIcon("icons/add.png"))  # Ajouter une icône
        self.setFixedSize(450, 400)

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
            }
            QLineEdit, QComboBox, QDateTimeEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-bottom: 10px;
                background-color: #fff;
            }
            QLineEdit:focus, QComboBox:focus, QDateTimeEdit:focus {
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
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
        """)

        # Layout
        layout = QVBoxLayout(self)

        # Input fields
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter robot name...")
        layout.addWidget(self.name_input)

        self.label_input = QLineEdit(self)
        self.label_input.setPlaceholderText("Enter label (optional)...")
        layout.addWidget(self.label_input)

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Enter description...")
        layout.addWidget(self.description_input)

        # Champ pour la date de création
        self.creation_date_input = QDateTimeEdit(self)
        self.creation_date_input.setDateTime(QDateTime.currentDateTime())  # Définit la date et l'heure actuelles
        self.creation_date_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        layout.addWidget(self.creation_date_input)

        # Combobox pour sélectionner une catégorie
        self.category_combo = QComboBox(self)
        self.category_combo.setPlaceholderText("Select a category...")
        self.populate_category_combo()  # Remplir la combobox avec les catégories
        layout.addWidget(self.category_combo)

        # Combobox pour sélectionner un statut
        self.status_combo = QComboBox(self)
        self.status_combo.setPlaceholderText("Select a status...")
        self.status_combo.addItems(["Active", "Inactive", "Pending"])  # Exemple de statuts
        layout.addWidget(self.status_combo)

        # Combobox pour sélectionner un réseau social
        self.reseau_social_combo = QComboBox(self)
        self.reseau_social_combo.setPlaceholderText("Select a social network...")
        self.populate_reseau_social_combo()  # Remplir la combobox avec les réseaux sociaux
        layout.addWidget(self.reseau_social_combo)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.save_button.setIcon(QIcon("icons/save.png"))  # Ajouter une icône
        self.save_button.clicked.connect(self.save_robot)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))  # Ajouter une icône
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def populate_category_combo(self):
        """Remplit la combobox des catégories avec les données de la base de données."""
        categories = load_categories()  # Charge les catégories depuis la base de données
        for category in categories:
            self.category_combo.addItem(category['name'], category['id'])  # Ajoute le nom et l'ID de la catégorie

    def populate_reseau_social_combo(self):
        """Remplit la combobox des réseaux sociaux avec les données de la base de données."""
        reseaux_sociaux = load_reseaux_sociaux()  # Charge les réseaux sociaux depuis la base de données
        for reseau in reseaux_sociaux:
            self.reseau_social_combo.addItem(reseau['name'], reseau['id'])  # Ajoute le nom et l'ID du réseau social

    def save_robot(self):
        """Sauvegarde le nouveau robot."""
        name = self.name_input.text().strip()
        label = self.label_input.text().strip()
        description = self.description_input.text().strip()
        creation_date = self.creation_date_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")  # Format SQL
        category_id = self.category_combo.currentData()  # Récupère l'ID de la catégorie sélectionnée
        status = self.status_combo.currentText()  # Récupère le statut sélectionné
        reseau_social_id = self.reseau_social_combo.currentData()  # Récupère l'ID du réseau social sélectionné

        if not name:
            QMessageBox.warning(self, "Validation Error", "Name cannot be empty!")
            return
        if not description:
            QMessageBox.warning(self, "Validation Error", "Description cannot be empty!")
            return
        if not category_id:
            QMessageBox.warning(self, "Validation Error", "Please select a category!")
            return
        if not status:
            QMessageBox.warning(self, "Validation Error", "Please select a status!")
            return

        robot = {
            'name': name,
            'label': label,
            'description': description,
            'creation_date': creation_date,
            'category_id': category_id,
            'status': status,
            'reseau_social_id': reseau_social_id
        }
        save_robot(robot)  # Sauvegarde le robot dans la base de données
        QMessageBox.information(self, "Success", "Robot added successfully!")
        self.accept()


from PyQt5.QtWidgets import QComboBox, QDateTimeEdit, QMessageBox
from PyQt5.QtCore import QDateTime

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QDateTimeEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime

class EditRobotDialog(QDialog):
    def __init__(self, robot_id, parent=None):
        super().__init__(parent)
        self.robot_id = robot_id
        self.setWindowTitle("Edit Robot")
        self.setWindowIcon(QIcon("icons/edit.png"))  # Ajouter une icône
        self.setFixedSize(450, 400)

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
            }
            QLineEdit, QComboBox, QDateTimeEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-bottom: 10px;
                background-color: #fff;
            }
            QLineEdit:focus, QComboBox:focus, QDateTimeEdit:focus {
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
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
        """)

        # Layout
        layout = QVBoxLayout(self)

        # Charger les données du robot
        self.robot = self.load_robot_data()

        # Input fields
        self.name_input = QLineEdit(self.robot['name'], self)
        self.name_input.setPlaceholderText("Enter robot name...")
        layout.addWidget(self.name_input)

        self.label_input = QLineEdit(self.robot.get('label', ''), self)
        self.label_input.setPlaceholderText("Enter label (optional)...")
        layout.addWidget(self.label_input)

        self.description_input = QLineEdit(self.robot.get('description', ''), self)
        self.description_input.setPlaceholderText("Enter description...")
        layout.addWidget(self.description_input)

        # Champ pour la date de création
        self.creation_date_input = QDateTimeEdit(self)
        creation_date = QDateTime.fromString(self.robot['creation_date'], "yyyy-MM-dd HH:mm:ss")
        self.creation_date_input.setDateTime(creation_date)
        self.creation_date_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        layout.addWidget(self.creation_date_input)

        # Combobox pour sélectionner une catégorie
        self.category_combo = QComboBox(self)
        self.category_combo.setPlaceholderText("Select a category...")
        self.populate_category_combo()  # Remplir la combobox avec les catégories
        self.category_combo.setCurrentText(self.robot.get('category', ''))  # Sélectionne la catégorie actuelle
        layout.addWidget(self.category_combo)

        # Combobox pour sélectionner un statut
        self.status_combo = QComboBox(self)
        self.status_combo.setPlaceholderText("Select a status...")
        self.status_combo.addItems(["Active", "Inactive", "Pending"])  # Exemple de statuts
        self.status_combo.setCurrentText(self.robot.get('status', ''))  # Sélectionne le statut actuel
        layout.addWidget(self.status_combo)

        # Combobox pour sélectionner un réseau social
        self.reseau_social_combo = QComboBox(self)
        self.reseau_social_combo.setPlaceholderText("Select a social network...")
        self.populate_reseau_social_combo()  # Remplir la combobox avec les réseaux sociaux
        self.reseau_social_combo.setCurrentText(self.robot.get('reseau_social', ''))  # Sélectionne le réseau social actuel
        layout.addWidget(self.reseau_social_combo)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.save_button.setIcon(QIcon("icons/save.png"))  # Ajouter une icône
        self.save_button.clicked.connect(self.save_robot)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))  # Ajouter une icône
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def load_robot_data(self):
        """Charge les données du robot à modifier."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM robots WHERE id = ?', (self.robot_id,))
        robot = cursor.fetchone()
        conn.close()
        return dict(zip(['id', 'name', 'label', 'description', 'creation_date', 'category', 'status', 'reseau_social_id'], robot))

    def populate_category_combo(self):
        """Remplit la combobox des catégories avec les données de la base de données."""
        categories = load_categories()  # Charge les catégories depuis la base de données
        for category in categories:
            self.category_combo.addItem(category['name'], category['id'])  # Ajoute le nom et l'ID de la catégorie

    def populate_reseau_social_combo(self):
        """Remplit la combobox des réseaux sociaux avec les données de la base de données."""
        reseaux_sociaux = load_reseaux_sociaux()  # Charge les réseaux sociaux depuis la base de données
        for reseau in reseaux_sociaux:
            self.reseau_social_combo.addItem(reseau['name'], reseau['id'])  # Ajoute le nom et l'ID du réseau social

    def save_robot(self):
        """Sauvegarde les modifications du robot."""
        name = self.name_input.text().strip()
        label = self.label_input.text().strip()
        description = self.description_input.text().strip()
        creation_date = self.creation_date_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")  # Format SQL
        category_id = self.category_combo.currentData()  # Récupère l'ID de la catégorie sélectionnée
        status = self.status_combo.currentText()  # Récupère le statut sélectionné
        reseau_social_id = self.reseau_social_combo.currentData()  # Récupère l'ID du réseau social sélectionné

        if not name:
            QMessageBox.warning(self, "Validation Error", "Name cannot be empty!")
            return
        if not description:
            QMessageBox.warning(self, "Validation Error", "Description cannot be empty!")
            return
        if not category_id:
            QMessageBox.warning(self, "Validation Error", "Please select a category!")
            return
        if not status:
            QMessageBox.warning(self, "Validation Error", "Please select a status!")
            return

        robot = {
            'id': self.robot_id,
            'name': name,
            'label': label,
            'description': description,
            'creation_date': creation_date,
            'category_id': category_id,
            'status': status,
            'reseau_social_id': reseau_social_id
        }
        update_robot(robot)  # Met à jour le robot dans la base de données
        QMessageBox.information(self, "Success", "Robot updated successfully!")
        self.accept()

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class RobotManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Robot Management")
        self.setWindowIcon(QIcon("icons/robot.png"))  # Ajouter une icône
        self.setFixedSize(800, 500)

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            QTableWidget {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #007bff;
                color: white;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                font-size: 14px;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
        """)

        # Layout
        layout = QVBoxLayout(self)

        # Table to display robots
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)  # Ajouter une colonne "Actions"
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Label", "Description", "Category", "Reseau Social", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)  # Redimensionnement manuel
        self.table.setEditTriggers(QTableWidget.AllEditTriggers)  # Permettre la modification directe
        layout.addWidget(self.table)

        # Buttons for Add
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Robot", self)
        self.add_button.setIcon(QIcon("icons/add.png"))  # Ajouter une icône
        self.add_button.clicked.connect(self.add_robot)
        button_layout.addWidget(self.add_button)

        layout.addLayout(button_layout)

        # Charger les robots
        self.load_robots()

    def load_robots(self):
        """Charge les robots dans la table."""
        robots = load_robots()
        self.table.setRowCount(len(robots))
        for row, robot in enumerate(robots):
            # Colonne ID
            self.table.setItem(row, 0, QTableWidgetItem(str(robot['id'])))
            self.table.item(row, 0).setFlags(self.table.item(row, 0).flags() & ~Qt.ItemIsEditable)  # ID non modifiable

            # Colonne Name
            self.table.setItem(row, 1, QTableWidgetItem(robot['name']))

            # Colonne Label
            self.table.setItem(row, 2, QTableWidgetItem(robot.get('label', '')))

            # Colonne Description
            self.table.setItem(row, 3, QTableWidgetItem(robot.get('description', '')))

            # Colonne Category
            self.table.setItem(row, 4, QTableWidgetItem(robot.get('category', '')))

            # Colonne Reseau Social
            self.table.setItem(row, 5, QTableWidgetItem(robot.get('reseau_social', '')))

            # Colonne Actions
            action_button_layout = QHBoxLayout()
            edit_button = QPushButton("Edit", self)
            edit_button.setIcon(QIcon("icons/edit.png"))  # Ajouter une icône
            edit_button.setStyleSheet("padding: 5px; font-size: 12px; background-color: #FFC107; color: black;")
            edit_button.clicked.connect(lambda _, r=row: self.edit_robot(r))
            action_button_layout.addWidget(edit_button)

            delete_button = QPushButton("Delete", self)
            delete_button.setIcon(QIcon("icons/delete.png"))  # Ajouter une icône
            delete_button.setStyleSheet("padding: 5px; font-size: 12px; background-color: #f44336; color: white;")
            delete_button.clicked.connect(lambda _, r=row: self.delete_robot(r))
            action_button_layout.addWidget(delete_button)

            action_widget = QWidget()
            action_widget.setLayout(action_button_layout)
            self.table.setCellWidget(row, 6, action_widget)

    def add_robot(self):
        """Ouvre une boîte de dialogue pour ajouter un robot."""
        dialog = AddRobotDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_robots()

    def edit_robot(self, row):
        """Ouvre une boîte de dialogue pour modifier un robot."""
        robot_id = int(self.table.item(row, 0).text())
        dialog = EditRobotDialog(robot_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_robots()

    def delete_robot(self, row):
        """Supprime le robot sélectionné."""
        robot_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(
            self, "Confirm Delete", "Are you sure you want to delete this robot?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_robot(robot_id)
            self.load_robots()



class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(400, 300)

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            QLabel {
                font-size: 14px;
                margin-bottom: 10px;
            }
            QComboBox {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-bottom: 20px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                font-size: 14px;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
        """)

        # Layout
        layout = QVBoxLayout(self)

        # Theme selection
        self.theme_label = QLabel("Select Theme:", self)
        layout.addWidget(self.theme_label)

        self.theme_combo = QComboBox(self)
        self.theme_combo.addItems(["Light", "Dark", "System Default"])
        layout.addWidget(self.theme_combo)

        # Save button
        self.save_button = QPushButton("Save Settings", self)
        self.save_button.setIcon(QIcon("icons/save.png"))  # Ajouter une icône
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

    def save_settings(self):
        selected_theme = self.theme_combo.currentText()
        # Appliquer le thème sélectionné
        apply_theme(selected_theme)  # Fonction à implémenter pour appliquer le thème
        QMessageBox.information(self, "Settings Saved", f"Theme '{selected_theme}' has been applied.")
        self.accept()
def apply_theme(theme_name):
    """Applique un thème à l'application."""
    if theme_name == "Light":
        QApplication.setStyle("Fusion")
        QApplication.setPalette(QApplication.style().standardPalette())
    elif theme_name == "Dark":
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(dark_palette)
    elif theme_name == "System Default":
        QApplication.setPalette(QApplication.style().standardPalette())

class HeaderSection1(QWidget):
    def __init__(self, parent=None, title="", app_name="", slogan=""):
        super().__init__(parent)
        self.title = title
        self.app_name = app_name
        self.slogan = slogan

        # Styles CSS
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #007BFF, stop:1 #00BFFF);
                padding: 20px;
                border-radius: 10px;
            }
            QLabel {
                color: white;
                text-align: center;
            }
        """)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Titre de l'application
        self.title_label = QLabel(self.title, self)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(self.title_label)

        # Nom de l'application
        self.app_name_label = QLabel(self.app_name, self)
        self.app_name_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.app_name_label)

        # Slogan
        self.slogan_label = QLabel(self.slogan, self)
        self.slogan_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.slogan_label)

        # Séparateur
        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        layout.addWidget(separator)

class ProgressDialog(QDialog):
    def __init__(self, parent=None, title="Processing", message="Please wait..."):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 150)

        # Styles CSS
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QProgressBar {
                background-color: #e0e0e0;
                border-radius: 5px;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #007BFF;
                border-radius: 5px;
            }
        """)

        # Layout
        layout = QVBoxLayout(self)

        # Message
        self.message_label = QLabel(message, self)
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

        # Barre de progression
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

    def set_progress(self, value):
        """Met à jour la valeur de la barre de progression."""
        self.progress_bar.setValue(value)
        if value >= 100:
            self.close()


class ConfirmationDialog(QDialog):
    def __init__(self, parent=None, title="Confirmation", message="Are you sure?"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(350, 150)

        # Styles CSS
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton#yes_button {
                background-color: #28a745;
                color: white;
            }
            QPushButton#no_button {
                background-color: #dc3545;
                color: white;
            }
        """)

        # Layout
        layout = QVBoxLayout(self)

        # Message
        self.message_label = QLabel(message, self)
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

        # Boutons
        button_layout = QHBoxLayout()
        self.yes_button = QPushButton("Yes", self)
        self.yes_button.setObjectName("yes_button")
        self.yes_button.setIcon(QIcon("icons/check.png"))
        self.yes_button.clicked.connect(self.accept)
        button_layout.addWidget(self.yes_button)

        self.no_button = QPushButton("No", self)
        self.no_button.setObjectName("no_button")
        self.no_button.setIcon(QIcon("icons/cancel.png"))
        self.no_button.clicked.connect(self.reject)
        button_layout.addWidget(self.no_button)

        layout.addLayout(button_layout)

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedSize(400, 250)

        # Styles CSS
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
                background-color: #007BFF;
                color: white;
            }
        """)

        # Layout
        layout = QVBoxLayout(self)

        # Icône de l'application
        self.app_icon = QLabel(self)
        self.app_icon.setPixmap(QPixmap("icons/app_icon.png").scaled(64, 64))
        self.app_icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.app_icon)

        # Informations sur l'application
        self.app_name_label = QLabel("Nova360 AI", self)
        self.app_name_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.app_name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.app_name_label)

        self.version_label = QLabel("Version 1.0.0", self)
        self.version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.version_label)

        self.description_label = QLabel("AI Marketing Automation Solution", self)
        self.description_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.description_label)

        # Bouton de fermeture
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)





if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    init_db()  # Initialiser la base de données
    app = QApplication(sys.argv)
    window = GroupTable()
    window.show()
    sys.exit(app.exec_())