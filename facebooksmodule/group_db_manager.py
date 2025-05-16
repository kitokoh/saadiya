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
import math

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
            
            edit_button = QPushButton("Edit", self)
            edit_button.setIcon(QIcon("icons/edit.png"))
            edit_button.setStyleSheet("""
                QPushButton {
                    padding: 5px;
                    font-size: 12px;
                    background-color: #FFC107;
                    color: black;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #e0a800;
                }
            """)
            edit_button.clicked.connect(lambda _, r=row: self.edit_category(r))
            action_button_layout.addWidget(edit_button)

            delete_button = QPushButton("Delete", self)
            delete_button.setIcon(QIcon("icons/delete.png"))
            delete_button.setStyleSheet("""
                QPushButton {
                    padding: 5px;
                    font-size: 12px;
                    background-color: #f44336;
                    color: white;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
            """)
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS category_group (
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
            link TEXT NOT NULL UNIQUE,
            remarks TEXT,
            category_group_id INTEGER,
            description TEXT,
            keywords TEXT,
            FOREIGN KEY(category_group_id) REFERENCES category_group(id)
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
        ('Group1', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
        ('Group2', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
        ('Group3', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
        ('Group4', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
        ('Group5', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
        ('Group6', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
        ('Group7', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
        ('Group8', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
        ('Group9', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
        ('Group10', 'https://www.facebook.com/groups/1533868653533875/', '', 1, '', ''),
        ('Group11', 'https://www.facebook.com/groups/2309210009291237/', '', 1, '', ''),
        ('Group12', 'https://www.facebook.com/groups/119929018423623/', '', 1, '', ''),
        ('Group13', 'https://www.facebook.com/groups/1914166852277174/', '', 1, '', ''),
        ('Group14', 'https://www.facebook.com/groups/249218873426277/', '', 1, '', ''),
        ('Group15', 'https://www.facebook.com/groups/382896815533960/', '', 1, '', ''),
        ('Group16', 'https://www.facebook.com/groups/501089116661238/', '', 1, '', ''),
        ('Group17', 'https://www.facebook.com/groups/313539295727010/', '', 1, '', ''),
        ('Group18', 'https://www.facebook.com/groups/2939025449709547/', '', 1, '', ''),
        ('Group19', 'https://www.facebook.com/groups/753693605432949/', '', 1, '', ''),
        ('Group20', 'https://www.facebook.com/groups/785886162129417/', '', 1, '', ''),
        ('Group21', 'https://www.facebook.com/groups/887867051269561/', '', 1, '', ''),
        ('Group22', 'https://www.facebook.com/groups/pressegypt/', '', 1, '', ''),
        ('Group23', 'https://www.facebook.com/groups/208073056046127/', '', 1, '', ''),
        ('Group24', 'https://www.facebook.com/groups/1335838006878557/', '', 1, '', ''),
        ('Group25', 'https://www.facebook.com/groups/1980706472159891/', '', 1, '', ''),
        ('Group26', 'https://www.facebook.com/groups/2245742298849513/', '', 1, '', ''),
        ('Group27', 'https://www.facebook.com/groups/266563507144846/', '', 1, '', ''),
        ('Group28', 'https://www.facebook.com/groups/1713003238853136/', '', 1, '', ''),
        ('Group29', 'https://www.facebook.com/groups/668946039826955', '', 1, '', ''),
        ('Group30', 'https://www.facebook.com/groups/1090039738545144/', '', 1, '', ''),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO groups (name, link, remarks, category_group_id, description, keywords)
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
    return [dict(zip(['id', 'name', 'link', 'remarks', 'category_group_id', 'description', 'keywords'], group)) for group in groups]

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
        INSERT INTO groups (name, link, remarks, category_group_id, description, keywords)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (group['name'], group['link'], group['remarks'], group['category_group_id'], group['description'], group.get('keywords', '')))
    conn.commit()
    conn.close()

def update_group(group):
    """Met à jour un groupe dans la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE groups
        SET name = ?, link = ?, remarks = ?, category_group_id = ?, description = ?, keywords = ?
        WHERE id = ?
    ''', (group['name'], group['link'], group['remarks'], group['category_group_id'], group['description'], group.get('keywords', ''), group['id']))
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
            INSERT INTO groups (name, link, remarks, category_group_id, description, keywords)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            group['name'],
            group['link'],
            group['remarks'],
            group['category_group_id'],
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













import sqlite3
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
                            QPushButton, QCheckBox, QLineEdit, QLabel, QMenu, QAction, 
                            QMessageBox, QFileDialog, QHeaderView, QComboBox, QScrollBar,
                            QStyledItemDelegate, QStyleOptionViewItem)
from PyQt5.QtCore import Qt, QUrl, QRegExp
from PyQt5.QtGui import QDesktopServices, QRegExpValidator, QFont
from PyQt5.Qt import QApplication

class URLDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.font.setUnderline(True)
        option.palette.setColor(QPalette.Text, QColor(0, 0, 255))

from PyQt5.QtWidgets import QTextEdit


































class GroupTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nova360 AI - Group Management")
        self.setMinimumSize(1200, 800)
        
        # Configuration initiale
        self.current_page = 1
        self.items_per_page = 25
        self.visible_columns = ['Select', 'Name', 'Link', 'Remarks', 'Category', 'Actions']
        # Initialisation de l'interface
        self.init_ui()
        self.load_data()
        
        # Appliquer les styles
        self.apply_styles()
        
    def init_ui(self):
        """Initialisation complète de l'interface utilisateur"""
        self.setup_main_layout()
        # self.setup_header()
        self.setup_controls()
        self.setup_table()
        self.setup_column_toggles()
        self.setup_pagination()
        self.setup_footer()
        
    def setup_main_layout(self):
        """Configuration du layout principal"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)
        
    def setup_header(self):
        """Configuration de l'en-tête"""
        self.header = QLabel("FB Group Management")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 5px;
            }
        """)
        self.main_layout.addWidget(self.header)
        
    def setup_controls(self):
        """Configuration des contrôles supérieurs"""
        control_layout = QHBoxLayout()
        control_layout.setSpacing(15)

        self.title_label = QLabel("FBK GROUP")
        self.title_label.setAlignment(Qt.AlignCenter)  # Centre le texte horizontalement
        self.title_label.setStyleSheet("""
            color: #3b82f6;
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            background-color: transparent;  /* Optionnel selon votre fond */
        """)
        control_layout.addWidget(self.title_label)       
        # Bouton Action
        self.action_btn = self.create_tool_button("⚡ Actions", "#3498db")
        self.setup_action_menu()
        control_layout.addWidget(self.action_btn)
        
        # Bouton Settings
        self.settings_btn = self.create_tool_button("⚙️ Settings", "#7f8c8d")
        self.setup_settings_menu()
        control_layout.addWidget(self.settings_btn)
        
        # Bouton Robot
        self.robot_btn = self.create_tool_button("🤖 Robot", "#e74c3c")
        self.robot_btn.clicked.connect(self.open_robot_dialog)
        control_layout.addWidget(self.robot_btn)
        
        # Barre de recherche
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("🔍 Search groups...")
        self.search_field.setClearButtonEnabled(True)
        self.search_field.textChanged.connect(self.filter_table)
        control_layout.addWidget(self.search_field, 1)
        
        # Bouton Filter
        self.filter_btn = self.create_tool_button("🔍 Filter", "#2ecc71")
        self.filter_btn.clicked.connect(self.open_filter_dialog)
        control_layout.addWidget(self.filter_btn)
        
        self.main_layout.addLayout(control_layout)




    def add_blank_rows(self, count=10):
        """Ajoute des lignes vides à la table pour nouvelle saisie"""
        # Désactiver temporairement les signaux pour éviter les déclenchements intempestifs
        self.table.blockSignals(True)
        
        current_row_count = self.table.rowCount()
        self.table.setRowCount(current_row_count + count)
        
        for row in range(current_row_count, current_row_count + count):
            # Colonne "Select" - Checkbox
            cb = QCheckBox()
            cb_widget = QWidget()
            cb_layout = QHBoxLayout(cb_widget)
            cb_layout.addWidget(cb)
            cb_layout.setAlignment(Qt.AlignCenter)
            cb_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row, 0, cb_widget)
            
            # Colonne "Name" - Champ texte
            name_item = QTableWidgetItem("")
            self.table.setItem(row, 1, name_item)
            
            # Colonne "Link" - Champ texte avec validation URL
            link_item = QTableWidgetItem("")
            self.table.setItem(row, 2, link_item)
            
            # Colonne "Remarks" - Champ texte
            remarks_item = QTableWidgetItem("")
            self.table.setItem(row, 3, remarks_item)
            
            # Colonne "Category" - Combobox des catégories
            category_combo = QComboBox()
            category_combo.addItem("", None)  # Option vide
            
            # Charger les catégories disponibles
            for category in self.group_categories:
                category_combo.addItem(category['name'], category['id'])
            
            self.table.setCellWidget(row, 4, category_combo)
            
            # Colonne "Actions" - Bouton Ajouter
            add_btn = QPushButton("➕ Add")
            add_btn.setStyleSheet("""
                QPushButton {
                    padding: 5px 10px;
                    background-color: #2ecc71;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #27ae60;
                }
            """)
            add_btn.clicked.connect(lambda _, r=row: self.save_new_row(r))
            self.table.setCellWidget(row, 5, add_btn)
        
        # Faire défiler jusqu'aux nouvelles lignes
        self.table.scrollToBottom()
        
        # Réactiver les signaux
        self.table.blockSignals(False)
        
        # Message d'information (optionnel)
        QMessageBox.information(self, "Lignes ajoutées", f"{count} nouvelles lignes vides ont été ajoutées.")



        
    def create_tool_button(self, text, color):
        """Crée un bouton stylisé"""
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        """)
        return btn
        
    def setup_action_menu(self):
        """Configure le menu Action"""
        menu = QMenu()
        
        actions = [
            ("📥 Import CSV", self.import_groups),
            ("📤 Export CSV", self.export_groups),
            ("🔄 Refresh Data", self.refresh_data),
            ("➕ Add 10 Rows", self.add_blank_rows),
            ("❌ Delete Selected", self.delete_selected),
            ("🗑️ Empty Table", self.empty_table)
        ]
        
        for text, callback in actions:
            action = QAction(text, self)
            action.triggered.connect(callback)
            menu.addAction(action)
            
        self.action_btn.setMenu(menu)
        
    def setup_settings_menu(self):
        """Configure le menu Settings"""
        menu = QMenu()
        
        settings = [
            ("📂 Group Categories", self.open_group_categories),
            ("🌐 Social Networks", self.open_social_networks),
            ("🎥 Media Types", self.open_media_types),
            ("⚙️ System Settings", self.open_system_settings)
        ]
        
        for text, callback in settings:
            action = QAction(text, self)
            action.triggered.connect(callback)
            menu.addAction(action)
            
        self.settings_btn.setMenu(menu)
        
    def setup_table(self):
        """Configuration de la table principale"""
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.visible_columns))
        self.table.setHorizontalHeaderLabels(self.visible_columns)
        
        # Configuration de la table
        self.table.setEditTriggers(QTableWidget.AllEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.horizontalHeader().setStretchLastSection(True)
        
        # Définir les largeurs de colonnes
        self.table.setColumnWidth(0, 50)   # Select
        self.table.setColumnWidth(1, 250)  # Name
        self.table.setColumnWidth(2, 350)  # Link
        self.table.setColumnWidth(3, 200)  # Remarks
        self.table.setColumnWidth(4, 200)  # Category
        
        # Définir le délégué pour la colonne Link
        self.table.setItemDelegateForColumn(2, URLDelegate())
        
        # Connecter les signaux
        self.table.cellChanged.connect(self.handle_cell_change)
        
        # Ajouter des lignes vides initiales
        self.add_blank_rows(10)
        
        self.main_layout.addWidget(self.table, 1)
        
    def setup_column_toggles(self):
        """Configuration des cases à cocher pour les colonnes"""
        toggle_layout = QHBoxLayout()
        toggle_layout.setSpacing(15)
        
        for idx, col in enumerate(self.visible_columns):
            cb = QCheckBox(col)
            cb.setChecked(True)
            cb.stateChanged.connect(lambda state, i=idx: self.toggle_column(i, state))
            toggle_layout.addWidget(cb)
            
        self.main_layout.addLayout(toggle_layout)
        
    def setup_pagination(self):
        """Configuration de la pagination"""
        pagination_layout = QHBoxLayout()
        pagination_layout.setAlignment(Qt.AlignCenter)
        
        self.prev_btn = self.create_pagination_button("◀ Previous")
        self.prev_btn.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_btn)
        
        self.page_label = QLabel("Page 1 of 1")
        pagination_layout.addWidget(self.page_label)
        
        self.next_btn = self.create_pagination_button("Next ▶")
        self.next_btn.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_btn)
        
        self.main_layout.addLayout(pagination_layout)
        
    def create_pagination_button(self, text):
        """Crée un bouton de pagination stylisé"""
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                padding: 5px 15px;
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        return btn
        
    def setup_footer(self):
        """Configuration du pied de page"""
        footer = QLabel("© 2023 Nova360 AI - Marketing Automation Solution")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                padding: 10px;
                font-size: 12px;
            }
        """)
        self.main_layout.addWidget(footer)
        
    def apply_styles(self):
        """Applique les styles globaux"""
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #ecf0f1;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                font-size: 14px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
            QCheckBox {
                spacing: 5px;
            }
        """)
        
    def load_data(self):
        """Charge les données depuis la base de données"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Charger les groupes avec leurs catégories (category_group)
            cursor.execute("""
                SELECT g.id, g.name, g.link, g.remarks, cg.name as category
                FROM groups g
                LEFT JOIN category_group cg ON g.category_group_id = cg.id
                ORDER BY g.name
            """)
            
            self.all_groups = []
            columns = [desc[0] for desc in cursor.description]
            for row in cursor.fetchall():
                self.all_groups.append(dict(zip(columns, row)))
                
            self.filtered_groups = self.all_groups.copy()
            
            # Charger les catégories de groupes
            cursor.execute("SELECT id, name FROM category_group ORDER BY name")
            self.group_categories = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
            
            conn.close()
            
            self.populate_table()
            
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load data: {str(e)}")
            
    def populate_table(self):
        """Remplit la table avec les données"""
        # Désactiver les signaux pendant la mise à jour
        self.table.blockSignals(True)
        self.table.setSortingEnabled(False)
        
        try:
            # Calculer la plage de données à afficher
            start_idx = (self.current_page - 1) * self.items_per_page
            end_idx = start_idx + self.items_per_page
            page_data = self.filtered_groups[start_idx:end_idx]
            
            # Effacer le contenu existant mais garder les lignes vides
            self.table.setRowCount(len(page_data) + 10)
            
            # Remplir avec les données
            for row, group in enumerate(page_data):
                # Checkbox de sélection
                cb = QCheckBox()
                cb.setProperty('group_id', group['id'])
                self.table.setCellWidget(row, 0, cb)
                
                # Nom
                name_item = QTableWidgetItem(group['name'])
                name_item.setData(Qt.UserRole, group['id'])
                self.table.setItem(row, 1, name_item)
                
                # Lien (avec validation)
                link_item = QTableWidgetItem(group['link'])
                link_item.setToolTip(group['link'])
                self.table.setItem(row, 2, link_item)
                
                # Remarques
                remarks_item = QTableWidgetItem(group.get('remarks', ''))
                self.table.setItem(row, 3, remarks_item)
                
                # Catégorie (combobox)
                category_combo = QComboBox()
                for cat in self.group_categories:
                    category_combo.addItem(cat['name'], cat['id'])
                
                # Sélectionner la catégorie actuelle
                if group['category']:
                    index = category_combo.findText(group['category'])
                    if index >= 0:
                        category_combo.setCurrentIndex(index)
                
                category_combo.currentIndexChanged.connect(
                    lambda idx, r=row: self.update_category(r, category_combo.itemData(idx)))
                self.table.setCellWidget(row, 4, category_combo)
                
                # Actions
                actions_btn = QPushButton("Actions ▼")
                actions_btn.setStyleSheet("""
                    QPushButton {
                        padding: 5px 10px;
                        background-color: #95a5a6;
                        color: white;
                        border: none;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #7f8c8d;
                    }
                """)
                
                menu = QMenu()
                
                verify_action = QAction("🔍 Verify Link", self)
                verify_action.triggered.connect(lambda _, r=row: self.verify_link(r))
                menu.addAction(verify_action)
                
                delete_action = QAction("❌ Delete", self)
                delete_action.triggered.connect(lambda _, r=row: self.delete_group(r))
                menu.addAction(delete_action)
                
                assign_action = QAction("🤖 Assign to Robot", self)
                assign_action.triggered.connect(lambda _, r=row: self.assign_to_robot(r))
                menu.addAction(assign_action)
                
                actions_btn.setMenu(menu)
                self.table.setCellWidget(row, 5, actions_btn)
            
            # Configurer les lignes vides pour nouvelle saisie
            for row in range(len(page_data), self.table.rowCount()):
                # Checkbox
                cb = QCheckBox()
                self.table.setCellWidget(row, 0, cb)
                
                # Nom
                self.table.setItem(row, 1, QTableWidgetItem(""))
                
                # Lien
                link_item = QTableWidgetItem("")
                self.table.setItem(row, 2, link_item)
                
                # Remarques
                self.table.setItem(row, 3, QTableWidgetItem(""))
                
                # Catégorie
                category_combo = QComboBox()
                for cat in self.group_categories:
                    category_combo.addItem(cat['name'], cat['id'])
                self.table.setCellWidget(row, 4, category_combo)
                
                # Bouton Ajouter
                add_btn = QPushButton("➕ Add")
                add_btn.setStyleSheet("""
                    QPushButton {
                        padding: 5px 10px;
                        background-color: #2ecc71;
                        color: white;
                        border: none;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #27ae60;
                    }
                """)
                add_btn.clicked.connect(lambda _, r=row: self.save_new_row(r))
                self.table.setCellWidget(row, 5, add_btn)
            
            # Mettre à jour la pagination
            total_pages = max(1, (len(self.filtered_groups) + self.items_per_page - 1) // self.items_per_page)
            self.page_label.setText(f"Page {self.current_page} of {total_pages}")
            self.prev_btn.setEnabled(self.current_page > 1)
            self.next_btn.setEnabled(self.current_page < total_pages)
            
        finally:
            self.table.setSortingEnabled(True)
            self.table.blockSignals(False)
            
    def add_blank_rows(self, count=10):
        """Ajoute des lignes vides à la table"""
        current_rows = self.table.rowCount()
        self.table.setRowCount(current_rows + count)
        
        for row in range(current_rows, current_rows + count):
            # Checkbox
            cb = QCheckBox()
            self.table.setCellWidget(row, 0, cb)
            
            # Nom
            self.table.setItem(row, 1, QTableWidgetItem(""))
            
            # Lien
            self.table.setItem(row, 2, QTableWidgetItem(""))
            
            # Remarques
            self.table.setItem(row, 3, QTableWidgetItem(""))
            
            # Catégorie
            category_combo = QComboBox()
            for cat in self.group_categories:
                category_combo.addItem(cat['name'], cat['id'])
            self.table.setCellWidget(row, 4, category_combo)
            
            # Bouton Ajouter
            add_btn = QPushButton("➕ Add")
            add_btn.setStyleSheet("""
                QPushButton {
                    padding: 5px 10px;
                    background-color: #2ecc71;
                    color: white;
                    border: none;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #27ae60;
                }
            """)
            add_btn.clicked.connect(lambda _, r=row: self.save_new_row(r))
            self.table.setCellWidget(row, 5, add_btn)
        
        # Faire défiler jusqu'aux nouvelles lignes
        self.table.scrollToBottom()
        
    def handle_cell_change(self, row, column):
        """Gère les modifications des cellules"""
        # Ignorer les lignes vides ou les colonnes non éditables
        if row >= len(self.filtered_groups) or column not in [1, 2, 3]:
            return
            
        item = self.table.item(row, column)
        if not item:
            return
            
        group_id = self.table.item(row, 1).data(Qt.UserRole)
        new_value = item.text()
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            if column == 1:  # Name
                cursor.execute("UPDATE groups SET name = ? WHERE id = ?", (new_value, group_id))
            elif column == 2:  # Link
                # Validation du lien
                if not self.validate_url(new_value):
                    QMessageBox.warning(self, "Invalid URL", "Please enter a valid URL starting with http:// or https://")
                    return
                cursor.execute("UPDATE groups SET link = ? WHERE id = ?", (new_value, group_id))
            elif column == 3:  # Remarks
                cursor.execute("UPDATE groups SET remarks = ? WHERE id = ?", (new_value, group_id))
                
            conn.commit()
            conn.close()
            
            # Mettre à jour les données locales
            for group in self.all_groups:
                if group['id'] == group_id:
                    if column == 1:
                        group['name'] = new_value
                    elif column == 2:
                        group['link'] = new_value
                    elif column == 3:
                        group['remarks'] = new_value
                    break
                    
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to update group: {str(e)}")
            
    def validate_url(self, url):
        """Valide qu'une URL est correctement formatée"""
        if not url:
            return True
        return url.startswith(('http://', 'https://'))
        
    def update_category(self, row, category_id):
        """Met à jour la catégorie d'un groupe"""
        if row >= len(self.filtered_groups):
            return
            
        group_id = self.table.item(row, 1).data(Qt.UserRole)
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("UPDATE groups SET category_group_id = ? WHERE id = ?", (category_id, group_id))
            conn.commit()
            conn.close()
            
            # Mettre à jour les données locales
            for group in self.all_groups:
                if group['id'] == group_id:
                    category_name = ""
                    for cat in self.group_categories:
                        if cat['id'] == category_id:
                            category_name = cat['name']
                            break
                    group['category'] = category_name
                    break
                    
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to update category: {str(e)}")
            
    def save_new_row(self, row):
        """Sauvegarde une nouvelle ligne dans la base de données"""
        name = self.table.item(row, 1).text().strip()
        link = self.table.item(row, 2).text().strip()
        remarks = self.table.item(row, 3).text().strip()
        category_combo = self.table.cellWidget(row, 4)
        category_id = category_combo.currentData() if category_combo else None
        
        # Validation
        if not name:
            QMessageBox.warning(self, "Missing Information", "Group name is required!")
            return
            
        if not link:
            QMessageBox.warning(self, "Missing Information", "Group link is required!")
            return
            
        if not self.validate_url(link):
            QMessageBox.warning(self, "Invalid URL", "Please enter a valid URL starting with http:// or https://")
            return
            
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO groups (name, link, remarks, category_group_id)
                VALUES (?, ?, ?, ?)
            """, (name, link, remarks, category_id))
            
            group_id = cursor.lastrowid
            
            # Récupérer le nom de la catégorie
            category_name = ""
            for cat in self.group_categories:
                if cat['id'] == category_id:
                    category_name = cat['name']
                    break
            
            # Ajouter aux données locales
            new_group = {
                'id': group_id,
                'name': name,
                'link': link,
                'remarks': remarks,
                'category': category_name
            }
            
            self.all_groups.append(new_group)
            self.filtered_groups.append(new_group)
            
            conn.commit()
            conn.close()
            
            # Recharger les données
            self.load_data()
            
            QMessageBox.information(self, "Success", "Group added successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to add new group: {str(e)}")
            
    # def verify_link(self, row):
    #     """Ouvre le lien dans le navigateur par défaut"""
    #     if row >= len(self.filtered_groups):
    #         return
            
    #     link = self.table.item(row, 2).text()
    #     if link:
    #         QDesktopServices.openUrl(QUrl(link))

    def verify_link(self, row):
        """Ouvre le lien uniquement dans Google Chrome"""
        if row >= len(self.filtered_groups):
            return

        link = self.table.item(row, 2).text()
        if link:
            try:
                # Détection de l'OS
                if sys.platform.startswith('win'):
                    # Windows
                    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                    if not os.path.exists(chrome_path):
                        chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
                    subprocess.Popen([chrome_path, link])
                elif sys.platform.startswith('linux'):
                    # Linux
                    subprocess.Popen(['google-chrome', link])
                elif sys.platform.startswith('darwin'):
                    # macOS
                    subprocess.Popen(['open', '-a', 'Google Chrome', link])
            except Exception as e:
                print(f"Erreur lors de l'ouverture du lien avec Chrome : {e}")
            
    def delete_group(self, row):
        """Supprime un groupe de la base de données"""
        if row >= len(self.filtered_groups):
            return
            
        group_id = self.table.item(row, 1).data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this group?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM groups WHERE id = ?", (group_id,))
                conn.commit()
                conn.close()
                
                # Mettre à jour les données locales
                self.all_groups = [g for g in self.all_groups if g['id'] != group_id]
                self.filtered_groups = [g for g in self.filtered_groups if g['id'] != group_id]
                
                # Recharger les données
                self.load_data()
                
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Failed to delete group: {str(e)}")
                
    def delete_selected(self):
        """Supprime les groupes sélectionnés"""
        selected_ids = []
        
        for row in range(self.table.rowCount()):
            cb = self.table.cellWidget(row, 0)
            if isinstance(cb, QCheckBox) and cb.isChecked():
                item = self.table.item(row, 1)
                if item and item.data(Qt.UserRole):
                    selected_ids.append(item.data(Qt.UserRole))
        
        if not selected_ids:
            QMessageBox.warning(self, "No Selection", "No groups selected for deletion!")
            return
            
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete {len(selected_ids)} selected groups?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                
                # Supprimer en une seule requête
                placeholders = ','.join(['?'] * len(selected_ids))
                cursor.execute(f"DELETE FROM groups WHERE id IN ({placeholders})", selected_ids)
                
                conn.commit()
                conn.close()
                
                # Mettre à jour les données locales
                self.all_groups = [g for g in self.all_groups if g['id'] not in selected_ids]
                self.filtered_groups = [g for g in self.filtered_groups if g['id'] not in selected_ids]
                
                # Recharger les données
                self.load_data()
                
                QMessageBox.information(self, "Success", f"Deleted {len(selected_ids)} groups successfully!")
                
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Failed to delete groups: {str(e)}")
                
    def empty_table(self):
        """Vide complètement la table"""
        reply = QMessageBox.question(
            self, "Confirm Empty Table",
            "Are you sure you want to delete ALL groups? This cannot be undone!",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM groups")
                conn.commit()
                conn.close()
                
                # Réinitialiser les données locales
                self.all_groups = []
                self.filtered_groups = []
                
                # Recharger les données
                self.load_data()
                
                QMessageBox.information(self, "Success", "All groups have been deleted!")
                
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Failed to empty table: {str(e)}")
                
    def assign_to_robot(self, row):
        """Assigne un groupe à un robot"""
        if row >= len(self.filtered_groups):
            return
            
        group_id = self.table.item(row, 1).data(Qt.UserRole)
        # dialog = AssignRobotDialog(group_id, self)
        # dialog.exec_()
        pass
        
    def filter_table(self):
        """Filtre la table selon le texte de recherche"""
        search_text = self.search_field.text().lower()
        
        if not search_text:
            self.filtered_groups = self.all_groups.copy()
        else:
            self.filtered_groups = [
                g for g in self.all_groups
                if (search_text in g['name'].lower() or 
                    search_text in g.get('link', '').lower() or 
                    search_text in g.get('remarks', '').lower() or 
                    search_text in g.get('category', '').lower())
            ]
            
        self.current_page = 1
        self.populate_table()
        
    def prev_page(self):
        """Va à la page précédente"""
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_table()
            
    def next_page(self):
        """Va à la page suivante"""
        if self.current_page * self.items_per_page < len(self.filtered_groups):
            self.current_page += 1
            self.populate_table()
            
    def refresh_data(self):
        """Rafraîchit les données depuis la base"""
        self.load_data()
        QMessageBox.information(self, "Refresh", "Data has been refreshed from database.")
        
    def import_groups(self):
        """Importe des groupes depuis un fichier CSV"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Import Groups", "", 
            "CSV Files (*.csv);;All Files (*)", options=options
        )
        
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    groups_to_import = [row for row in reader]
                
                if not groups_to_import:
                    QMessageBox.warning(self, "Empty File", "The selected file contains no data!")
                    return
                    
                # Valider les données
                required_fields = ['name', 'link']
                for group in groups_to_import:
                    for field in required_fields:
                        if field not in group or not group[field].strip():
                            raise ValueError(f"Missing required field: {field}")
                    
                    if not self.validate_url(group['link']):
                        raise ValueError(f"Invalid URL: {group['link']}")
                
                # Importer dans la base de données
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                
                for group in groups_to_import:
                    # Trouver l'ID de la catégorie si spécifiée
                    category_id = None
                    if 'category' in group and group['category']:
                        for cat in self.group_categories:
                            if cat['name'] == group['category']:
                                category_id = cat['id']
                                break
                    
                    cursor.execute("""
                        INSERT INTO groups (name, link, remarks, category_group_id)
                        VALUES (?, ?, ?, ?)
                    """, (
                        group['name'],
                        group['link'],
                        group.get('remarks', ''),
                        category_id
                    ))
                
                conn.commit()
                conn.close()
                
                # Recharger les données
                self.load_data()
                
                QMessageBox.information(
                    self, "Import Successful", 
                    f"Successfully imported {len(groups_to_import)} groups!"
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self, "Import Error", 
                    f"Failed to import groups: {str(e)}"
                )



    def import_groups(self):
        """Importe des groupes depuis un fichier CSV"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Import Groups", "", 
            "CSV Files (*.csv);;All Files (*)", options=options
        )
        
        if not file_name:  # L'utilisateur a annulé la sélection
            return
            
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                # Détecter le délimiteur automatiquement
                try:
                    dialect = csv.Sniffer().sniff(f.read(1024))
                    f.seek(0)
                    reader = csv.DictReader(f, dialect=dialect)
                except:
                    f.seek(0)
                    reader = csv.DictReader(f)  # Fallback si la détection échoue
                
                groups_to_import = [row for row in reader]
            
            if not groups_to_import:
                QMessageBox.warning(self, "Empty File", "The selected file contains no data!")
                return
                
            # Valider les données
            required_fields = ['name', 'link']
            for idx, group in enumerate(groups_to_import, 1):
                # Vérifier les champs obligatoires
                for field in required_fields:
                    if field not in group or not str(group[field]).strip():
                        raise ValueError(f"Ligne {idx}: Champ requis '{field}' manquant ou vide")
                    
                # Valider l'URL
                if not self.validate_url(group['link']):
                    raise ValueError(f"Ligne {idx}: URL invalide '{group['link']}'")
                
                # Nettoyer les données
                group['name'] = str(group['name']).strip()
                group['link'] = str(group['link']).strip()
                group['remarks'] = str(group.get('remarks', '')).strip()
                group['category'] = str(group.get('category', '')).strip()
            
            # Importer dans la base de données
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Compter les groupes importés et les doublons
            imported_count = 0
            duplicate_count = 0
            
            for group in groups_to_import:
                try:
                    # Vérifier si le groupe existe déjà
                    cursor.execute("SELECT id FROM groups WHERE name = ? OR link = ?", 
                                (group['name'], group['link']))
                    if cursor.fetchone():
                        duplicate_count += 1
                        continue
                    
                    # Trouver l'ID de la catégorie si spécifiée
                    category_id = None
                    if group['category']:
                        cursor.execute("SELECT id FROM category_group WHERE name = ?", 
                                    (group['category'],))
                        result = cursor.fetchone()
                        if result:
                            category_id = result[0]
                        else:
                            # Option: créer automatiquement la catégorie si elle n'existe pas
                            # cursor.execute("INSERT INTO category_group (name) VALUES (?)", 
                            #              (group['category'],))
                            # category_id = cursor.lastrowid
                            pass
                    
                    # Insérer le groupe
                    cursor.execute("""
                        INSERT INTO groups (name, link, remarks, category_group_id)
                        VALUES (?, ?, ?, ?)
                    """, (
                        group['name'],
                        group['link'],
                        group['remarks'] if group['remarks'] else None,
                        category_id
                    ))
                    imported_count += 1
                    
                except sqlite3.Error as e:
                    conn.rollback()
                    raise ValueError(f"Erreur base de données pour le groupe '{group['name']}': {str(e)}")
            
            conn.commit()
            conn.close()
            
            # Recharger les données
            self.load_data()
            
            # Message de résultat
            msg = f"Import terminé avec succès!\n\n" \
                f"Groupes importés: {imported_count}\n" \
                f"Doublons ignorés: {duplicate_count}"
            
            if duplicate_count > 0:
                msg += "\n\nNote: Certains groupes n'ont pas été importés car ils existent déjà."
            
            QMessageBox.information(self, "Import Successful", msg)
            
        except Exception as e:
            QMessageBox.critical(
                self, "Import Error", 
                f"Échec de l'importation:\n\n{str(e)}"
            )

            
    def export_groups(self):
        """Exporte les groupes vers un fichier CSV"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Export Groups", "", 
            "CSV Files (*.csv);;All Files (*)", options=options
        )
        
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['name', 'link', 'remarks', 'category'])
                    writer.writeheader()
                    
                    for group in self.all_groups:
                        writer.writerow({
                            'name': group['name'],
                            'link': group['link'],
                            'remarks': group.get('remarks', ''),
                            'category': group.get('category', '')
                        })
                
                QMessageBox.information(
                    self, "Export Successful", 
                    f"Successfully exported {len(self.all_groups)} groups!"
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self, "Export Error", 
                    f"Failed to export groups: {str(e)}"
                )
    
    # Méthodes pour les dialogues (à implémenter)
    def open_group_categories(self):
        # dialog = GroupCategoriesDialog(self)
        # dialog.exec_()
        
    # def open_category_management_dialog(self):
        """Ouvre une boîte de dialogue pour gérer les catégories."""
        dialog = GroupCategoriesDialog(self)
        dialog.exec_()
        
    def open_social_networks(self):
        # dialog = SocialNetworksDialog(self)
        # dialog.exec_()
        pass
        
    def open_media_types(self):
        # dialog = MediaTypesDialog(self)
        # dialog.exec_()
        pass
        
    def open_system_settings(self):
        # dialog = SystemSettingsDialog(self)
        # dialog.exec_()
        pass
    def open_robot_dialog(self):
        dialog = RobotManagementDialog(self)
        dialog.exec_()
        
    def open_filter_dialog(self):
        # dialog = FilterDialog(self)
        # dialog.exec_()
        pass
        
    def darken_color(self, hex_color, percent=10):
        """Assombrit une couleur hexadécimale"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * (100 - percent) / 100)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
        
    def toggle_column(self, index, visible):
        """Affiche ou masque une colonne"""
        self.table.setColumnHidden(index, not visible)




# class GroupTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nova360 AI - Group Management")
        self.setMinimumSize(1200, 800)
        
        # Configuration initiale
        self.current_page = 1
        self.items_per_page = 25
        self.visible_columns = ['Select', 'Name', 'Link', 'Remarks', 'Category', 'Actions']
        self.all_groups = []
        self.filtered_groups = []
        self.group_categories = []  # Initialisation ajoutée ici
        
        # Initialisation de l'interface
        self.init_ui()
        self.load_data()
        
        # Appliquer les styles
        self.apply_styles()
        
    def init_ui(self):
        """Initialisation complète de l'interface utilisateur"""
        self.setup_main_layout()
        # self.setup_header()
        self.setup_controls()
        self.setup_table()
        self.setup_column_toggles()
        self.setup_pagination()
        self.setup_footer()
        
    def load_data(self):
        """Charge les données depuis la base de données"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # D'abord charger les catégories de groupes
            cursor.execute("SELECT id, name FROM category_group ORDER BY name")
            self.group_categories = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
            
            # Ensuite charger les groupes avec leurs catégories
            cursor.execute("""
                SELECT g.id, g.name, g.link, g.remarks, cg.name as category, cg.id as category_id
                FROM groups g
                LEFT JOIN category_group cg ON g.category_group_id = cg.id
                ORDER BY g.name
            """)
            
            self.all_groups = []
            columns = [desc[0] for desc in cursor.description]
            for row in cursor.fetchall():
                group_data = dict(zip(columns, row))
                # Assurer que category_id est inclus même si NULL
                group_data['category_group_id'] = group_data.get('category_id')
                self.all_groups.append(group_data)
                
            self.filtered_groups = self.all_groups.copy()
            
            conn.close()
            
            self.populate_table()
            
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load data: {str(e)}")
            
    def populate_table(self):
        """Remplit la table avec les données"""
        # Désactiver les signaux pendant la mise à jour
        self.table.blockSignals(True)
        self.table.setSortingEnabled(False)
        
        try:
            # Calculer la plage de données à afficher
            start_idx = (self.current_page - 1) * self.items_per_page
            end_idx = start_idx + self.items_per_page
            page_data = self.filtered_groups[start_idx:end_idx]
            
            # Effacer le contenu existant mais garder les lignes vides
            self.table.setRowCount(len(page_data) + 10)  # 10 lignes vides supplémentaires
            
            # Remplir avec les données
            for row, group in enumerate(page_data):
                # Checkbox de sélection
                cb = QCheckBox()
                cb.setProperty('group_id', group['id'])
                self.table.setCellWidget(row, 0, cb)
                
                # Nom
                name_item = QTableWidgetItem(group['name'])
                name_item.setData(Qt.UserRole, group['id'])
                self.table.setItem(row, 1, name_item)
                
                # Lien (avec validation)
                link_item = QTableWidgetItem(group['link'])
                link_item.setToolTip(group['link'])
                self.table.setItem(row, 2, link_item)
                
                # Remarques
                remarks_item = QTableWidgetItem(group.get('remarks', ''))
                self.table.setItem(row, 3, remarks_item)
                
                # Catégorie (combobox)
                category_combo = QComboBox()
                # Ajouter une option vide
                category_combo.addItem("", None)
                for cat in self.group_categories:
                    category_combo.addItem(cat['name'], cat['id'])
                
                # Sélectionner la catégorie actuelle
                current_category_id = group.get('category_group_id')
                if current_category_id:
                    index = category_combo.findData(current_category_id)
                    if index >= 0:
                        category_combo.setCurrentIndex(index)
                
                category_combo.currentIndexChanged.connect(
                    lambda idx, r=row: self.update_category(r, category_combo.itemData(idx)))
                self.table.setCellWidget(row, 4, category_combo)
                
                # Actions
                actions_btn = QPushButton("Actions ▼")
                actions_btn.setStyleSheet("""
                    QPushButton {
                        padding: 5px 10px;
                        background-color: #95a5a6;
                        color: white;
                        border: none;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #7f8c8d;
                    }
                """)
                
                menu = QMenu()
                
                verify_action = QAction("🔍 Verify Link", self)
                verify_action.triggered.connect(lambda _, r=row: self.verify_link(r))
                menu.addAction(verify_action)
                
                delete_action = QAction("❌ Delete", self)
                delete_action.triggered.connect(lambda _, r=row: self.delete_group(r))
                menu.addAction(delete_action)
                
                assign_action = QAction("🤖 Assign to Robot", self)
                assign_action.triggered.connect(lambda _, r=row: self.assign_to_robot(r))
                menu.addAction(assign_action)
                
                actions_btn.setMenu(menu)
                self.table.setCellWidget(row, 5, actions_btn)
            
            # Configurer les lignes vides pour nouvelle saisie
            for row in range(len(page_data), self.table.rowCount()):
                # Checkbox
                cb = QCheckBox()
                self.table.setCellWidget(row, 0, cb)
                
                # Nom
                self.table.setItem(row, 1, QTableWidgetItem(""))
                
                # Lien
                link_item = QTableWidgetItem("")
                self.table.setItem(row, 2, link_item)
                
                # Remarques
                self.table.setItem(row, 3, QTableWidgetItem(""))
                
                # Catégorie
                category_combo = QComboBox()
                category_combo.addItem("", None)
                for cat in self.group_categories:
                    category_combo.addItem(cat['name'], cat['id'])
                self.table.setCellWidget(row, 4, category_combo)
                
                # Bouton Ajouter
                add_btn = QPushButton("➕ Add")
                add_btn.setStyleSheet("""
                    QPushButton {
                        padding: 5px 10px;
                        background-color: #2ecc71;
                        color: white;
                        border: none;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #27ae60;
                    }
                """)
                add_btn.clicked.connect(lambda _, r=row: self.save_new_row(r))
                self.table.setCellWidget(row, 5, add_btn)
            
            # Mettre à jour la pagination
            total_pages = max(1, (len(self.filtered_groups) + self.items_per_page - 1) // self.items_per_page)
            self.page_label.setText(f"Page {self.current_page} of {total_pages}")
            self.prev_btn.setEnabled(self.current_page > 1)
            self.next_btn.setEnabled(self.current_page < total_pages)
            
        finally:
            self.table.setSortingEnabled(True)
            self.table.blockSignals(False)

    # ... (le reste de vos méthodes reste inchangé)

    def save_new_row(self, row):
        """Sauvegarde une nouvelle ligne dans la base de données"""
        name = self.table.item(row, 1).text().strip()
        link = self.table.item(row, 2).text().strip()
        remarks = self.table.item(row, 3).text().strip()
        category_combo = self.table.cellWidget(row, 4)
        category_id = category_combo.currentData() if category_combo else None
        
        # Validation
        if not name:
            QMessageBox.warning(self, "Missing Information", "Group name is required!")
            return
            
        if not link:
            QMessageBox.warning(self, "Missing Information", "Group link is required!")
            return
            
        if not self.validate_url(link):
            QMessageBox.warning(self, "Invalid URL", "Please enter a valid URL starting with http:// or https://")
            return
            
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO groups (name, link, remarks, category_group_id)
                VALUES (?, ?, ?, ?)
            """, (name, link, remarks, category_id))
            
            group_id = cursor.lastrowid
            
            # Récupérer le nom de la catégorie
            category_name = ""
            if category_id:
                for cat in self.group_categories:
                    if cat['id'] == category_id:
                        category_name = cat['name']
                        break
            
            # Ajouter aux données locales
            new_group = {
                'id': group_id,
                'name': name,
                'link': link,
                'remarks': remarks,
                'category': category_name,
                'category_group_id': category_id
            }
            
            self.all_groups.append(new_group)
            self.filtered_groups.append(new_group)
            
            conn.commit()
            conn.close()
            
            # Recharger les données
            self.load_data()
            
            QMessageBox.information(self, "Success", "Group added successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to add new group: {str(e)}")
            
    def update_category(self, row, category_id):
        """Met à jour la catégorie d'un groupe"""
        if row >= len(self.filtered_groups):
            return
            
        group_id = self.table.item(row, 1).data(Qt.UserRole)
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("UPDATE groups SET category_group_id = ? WHERE id = ?", (category_id, group_id))
            conn.commit()
            conn.close()
            
            # Mettre à jour les données locales
            for group in self.all_groups:
                if group['id'] == group_id:
                    category_name = ""
                    if category_id:
                        for cat in self.group_categories:
                            if cat['id'] == category_id:
                                category_name = cat['name']
                                break
                    group['category'] = category_name
                    group['category_group_id'] = category_id
                    break
                    
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to update category: {str(e)}")



    def add_blank_row2s(self, count=10):
        """Ajoute des lignes vides à la table pour nouvelle saisie"""
        # Désactiver temporairement les signaux pour éviter les déclenchements intempestifs
        self.table.blockSignals(True)
        
        current_row_count = self.table.rowCount()
        self.table.setRowCount(current_row_count + count)
        
        for row in range(current_row_count, current_row_count + count):
            # Colonne "Select" - Checkbox
            cb = QCheckBox()
            cb_widget = QWidget()
            cb_layout = QHBoxLayout(cb_widget)
            cb_layout.addWidget(cb)
            cb_layout.setAlignment(Qt.AlignCenter)
            cb_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row, 0, cb_widget)
            
            # Colonne "Name" - Champ texte
            name_item = QTableWidgetItem("")
            self.table.setItem(row, 1, name_item)
            
            # Colonne "Link" - Champ texte avec validation URL
            link_item = QTableWidgetItem("")
            self.table.setItem(row, 2, link_item)
            
            # Colonne "Remarks" - Champ texte
            remarks_item = QTableWidgetItem("")
            self.table.setItem(row, 3, remarks_item)
            
            # Colonne "Category" - Combobox des catégories
            category_combo = QComboBox()
            category_combo.addItem("", None)  # Option vide
            
            # Charger les catégories disponibles
            for category in self.group_categories:
                category_combo.addItem(category['name'], category['id'])
            
            self.table.setCellWidget(row, 4, category_combo)
            
            # Colonne "Actions" - Bouton Ajouter
            add_btn = QPushButton("➕ Add")
            add_btn.setStyleSheet("""
                QPushButton {
                    padding: 5px 10px;
                    background-color: #2ecc71;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #27ae60;
                }
            """)
            add_btn.clicked.connect(lambda _, r=row: self.save_new_row(r))
            self.table.setCellWidget(row, 5, add_btn)
        
        # Faire défiler jusqu'aux nouvelles lignes
        self.table.scrollToBottom()
        
        # Réactiver les signaux
        self.table.blockSignals(False)
        
        # Message d'information (optionnel)
        QMessageBox.information(self, "Lignes ajoutées", f"{count} nouvelles lignes vides ont été ajoutées.")

class GroupCategoriesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Group Categories Management")
        self.setMinimumSize(800, 600)
        
        # Variables
        self.categories = []
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Configuration de la table
        self.setup_table()
        layout.addWidget(self.table)
        
        # Boutons d'action
        self.setup_buttons()
        layout.addLayout(self.button_layout)
        
        # Charger les données
        self.load_categories()
        
        # Appliquer les styles
        self.apply_styles()
    
    def setup_table(self):
        """Configure la table des catégories"""
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Label", "Description", "Created", "Actions"])
        
        # Configuration de la table
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setSortingEnabled(True)
        
        # Ajuster les largeurs de colonnes
        self.table.setColumnWidth(0, 60)   # ID
        self.table.setColumnWidth(1, 200)  # Name
        self.table.setColumnWidth(2, 150)  # Label
        self.table.setColumnWidth(3, 250)  # Description
        self.table.setColumnWidth(4, 150)  # Created
        self.table.horizontalHeader().setStretchLastSection(True)
    
    def setup_buttons(self):
        """Configure les boutons d'action"""
        self.button_layout = QHBoxLayout()
        
        # Bouton Ajouter
        self.add_btn = QPushButton("➕ Add Category")
        self.add_btn.clicked.connect(self.add_category)
        self.button_layout.addWidget(self.add_btn)
        
        # Bouton Rafraîchir
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_categories)
        self.button_layout.addWidget(self.refresh_btn)
        
        # Bouton Fermer
        self.close_btn = QPushButton("❌ Close")
        self.close_btn.clicked.connect(self.close)
        self.button_layout.addWidget(self.close_btn)
        
        # Espacement
        self.button_layout.addStretch()
    
    def load_categories(self):
        """Charge les catégories depuis la base de données"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, label, description, 
                       strftime('%Y-%m-%d %H:%M', date_creation) as created
                FROM category_group
                WHERE date_suppression IS NULL
                ORDER BY name
            """)
            
            self.categories = []
            columns = [desc[0] for desc in cursor.description]
            for row in cursor.fetchall():
                self.categories.append(dict(zip(columns, row)))
            
            conn.close()
            
            self.populate_table()
            
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load categories: {str(e)}")
    
    def populate_table(self):
        """Remplit la table avec les catégories"""
        self.table.setRowCount(len(self.categories))
        
        for row, category in enumerate(self.categories):
            # ID
            id_item = QTableWidgetItem(str(category['id']))
            id_item.setData(Qt.UserRole, category['id'])
            self.table.setItem(row, 0, id_item)
            
            # Name
            self.table.setItem(row, 1, QTableWidgetItem(category['name']))
            
            # Label
            self.table.setItem(row, 2, QTableWidgetItem(category.get('label', '')))
            
            # Description
            desc_item = QTableWidgetItem(category.get('description', ''))
            desc_item.setToolTip(category.get('description', ''))
            self.table.setItem(row, 3, desc_item)
            
            # Created
            self.table.setItem(row, 4, QTableWidgetItem(category.get('created', '')))
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            # Bouton Edit
            edit_btn = QPushButton("✏️")
            edit_btn.setToolTip("Edit category")
            edit_btn.setStyleSheet("""
                QPushButton {
                    padding: 3px;
                    border-radius: 3px;
                    background-color: #3498db;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            edit_btn.clicked.connect(lambda _, r=row: self.edit_category(r))
            actions_layout.addWidget(edit_btn)
            
            # Bouton Delete
            delete_btn = QPushButton("🗑️")
            delete_btn.setToolTip("Delete category")
            delete_btn.setStyleSheet("""
                QPushButton {
                    padding: 3px;
                    border-radius: 3px;
                    background-color: #e74c3c;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            delete_btn.clicked.connect(lambda _, r=row: self.delete_category(r))
            actions_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(row, 5, actions_widget)
    
    def add_category(self):
        """Ouvre le dialogue pour ajouter une nouvelle catégorie"""
        dialog = CategoryEditDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_categories()
            # Rafraîchir les catégories dans la table parente si nécessaire
            if self.parent() and hasattr(self.parent(), 'load_data'):
                self.parent().load_data()
    
    def edit_category(self, row):
        """Ouvre le dialogue pour modifier une catégorie existante"""
        category_id = self.table.item(row, 0).data(Qt.UserRole)
        dialog = CategoryEditDialog(self, category_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_categories()
            # Rafraîchir les catégories dans la table parente si nécessaire
            if self.parent() and hasattr(self.parent(), 'load_data'):
                self.parent().load_data()
    
    def delete_category(self, row):
        """Supprime une catégorie"""
        category_id = self.table.item(row, 0).data(Qt.UserRole)
        category_name = self.table.item(row, 1).text()
        
        # Vérifier si la catégorie est utilisée par des groupes
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM groups WHERE category_group_id = ?", (category_id,))
            group_count = cursor.fetchone()[0]
            conn.close()
            
            if group_count > 0:
                QMessageBox.warning(
                    self, "Cannot Delete", 
                    f"Cannot delete category '{category_name}' because it's used by {group_count} group(s).\n"
                    "Please reassign or delete these groups first."
                )
                return
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to check category usage: {str(e)}")
            return
        
        # Confirmation
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete category '{category_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                
                # Soft delete (marquer comme supprimé plutôt que de supprimer réellement)
                cursor.execute("""
                    UPDATE category_group 
                    SET date_suppression = CURRENT_TIMESTAMP 
                    WHERE id = ?
                """, (category_id,))
                
                conn.commit()
                conn.close()
                
                self.load_categories()
                # Rafraîchir les catégories dans la table parente si nécessaire
                if self.parent() and hasattr(self.parent(), 'load_data'):
                    self.parent().load_data()
                
                QMessageBox.information(self, "Success", "Category deleted successfully!")
                
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Failed to delete category: {str(e)}")
    
    def apply_styles(self):
        """Applique les styles à la boîte de dialogue"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                font-size: 14px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }
            QPushButton {
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
        """)


class CategoryEditDialog(QDialog):
    def __init__(self, parent=None, category_id=None):
        super().__init__(parent)
        self.category_id = category_id
        self.setWindowTitle("Add Category" if category_id is None else "Edit Category")
        self.setMinimumSize(400, 300)
        
        # Layout
        layout = QVBoxLayout(self)
        
        # Formulaire
        self.setup_form()
        layout.addLayout(self.form_layout)
        
        # Boutons
        self.setup_buttons()
        layout.addLayout(self.button_layout)
        
        # Charger les données si édition
        if category_id is not None:
            self.load_category_data()
        
        # Appliquer les styles
        self.apply_styles()
    
    def setup_form(self):
        """Configure le formulaire de saisie"""
        self.form_layout = QFormLayout()
        
        # Nom
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Required")
        self.form_layout.addRow("Name:", self.name_edit)
        
        # Label
        self.label_edit = QLineEdit()
        self.label_edit.setPlaceholderText("Optional")
        self.form_layout.addRow("Label:", self.label_edit)
        
        # Description
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("Optional description")
        self.desc_edit.setMaximumHeight(100)
        self.form_layout.addRow("Description:", self.desc_edit)
    
    def setup_buttons(self):
        """Configure les boutons"""
        self.button_layout = QHBoxLayout()
        
        # Bouton Sauvegarder
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.clicked.connect(self.save_category)
        self.button_layout.addWidget(self.save_btn)
        
        # Bouton Annuler
        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_btn)
    
    def load_category_data(self):
        """Charge les données de la catégorie à éditer"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, label, description 
                FROM category_group 
                WHERE id = ? AND date_suppression IS NULL
            """, (self.category_id,))
            
            category = cursor.fetchone()
            conn.close()
            
            if category:
                self.name_edit.setText(category[0])
                self.label_edit.setText(category[1] if category[1] else "")
                self.desc_edit.setPlainText(category[2] if category[2] else "")
            else:
                QMessageBox.warning(self, "Not Found", "Category not found or has been deleted.")
                self.reject()
                
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load category: {str(e)}")
            self.reject()
    
    def save_category(self):
        """Sauvegarde la catégorie dans la base de données"""
        name = self.name_edit.text().strip()
        label = self.label_edit.text().strip()
        description = self.desc_edit.toPlainText().strip()
        
        # Validation
        if not name:
            QMessageBox.warning(self, "Validation Error", "Category name is required!")
            return
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            if self.category_id is None:
                # Ajout d'une nouvelle catégorie
                cursor.execute("""
                    INSERT INTO category_group (name, label, description)
                    VALUES (?, ?, ?)
                """, (name, label or None, description or None))
            else:
                # Mise à jour d'une catégorie existante
                cursor.execute("""
                    UPDATE category_group 
                    SET name = ?, label = ?, description = ?, date_modification = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (name, label or None, description or None, self.category_id))
            
            conn.commit()
            conn.close()
            
            self.accept()
            
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Duplicate Name", "A category with this name already exists!")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save category: {str(e)}")
    
    def apply_styles(self):
        """Applique les styles à la boîte de dialogue"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #3498db;
            }
            QPushButton {
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
        """)



if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    init_db()  # Initialiser la base de données
    app = QApplication(sys.argv)
    window = GroupTable()
    window.show()
    sys.exit(app.exec_())  
    