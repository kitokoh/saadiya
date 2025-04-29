import os
import csv
import json
import sqlite3
import shutil
from PyQt5.QtCore import Qt, QTimer, QLocale, QTranslator, QDateTime
from PyQt5.QtGui import QPixmap, QIcon, QColor
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView, QMessageBox, QMenu, QDialog, QDialogButtonBox, QFileDialog,
    QCheckBox, QApplication, QStackedWidget, QTableWidgetSelectionRange, QInputDialog, QStyledItemDelegate
)
from PyQt5.QtWidgets import QAction
# Chemin vers le dossier de l'utilisateur (Roaming)
# user_data_dir = os.path.join(os.getenv('APPDATA'), 'saadiya')
# os.makedirs(user_data_dir, exist_ok=True)  # Créer le dossier s'il n'existe pas
from facebooksmodule.group_manager import RobotManagementDialog
from imports import *
from facebooksmodule.group_manager import ReseauSocialManagementDialog
from facebooksmodule.group_manager import MediaTypeManagementDialog
from PyQt5.QtWidgets import QProgressDialog

from ui.header import HeaderSection
from ui.footer import FooterSection
# Chemin de la base de données
# DB_PATH = os.path.join(user_data_dir, 'groups22.db')

# Chemin des médias
media_folder = os.path.join(user_data_dir, 'media')
os.makedirs(media_folder, exist_ok=True)  # Créer le dossier média s'il n'existe pas

# Styles CSS modernes
STYLESHEET = """
    QMainWindow {
        background-color: #f5f5f5;
    }
    QLabel {
        font-size: 16px;
        color: #333;
    }
    QPushButton {
        background-color: #0078d7;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #005bb5;
    }
    QTableWidget {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    QHeaderView::section {
        background-color: #0078d7;
        color: white;
        padding: 10px;
        font-size: 14px;
    }
    QComboBox {
        padding: 5px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    QLineEdit {
        padding: 5px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    QDialog {
        background-color: white;
    }
"""
class MediaManager:
    def __init__(self, DB_PATH):
        self.DB_PATH = DB_PATH


        self.update_queue = []
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.process_updates)
        self.update_timer.start(2000)  # Traite les updates toutes les 2 secondes
        self.create_database()


    def load_media_from_db_paginated(self, user_choice, limit=50, offset=0):
        """Version paginée de la requête"""
        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT m.id, m.nom, m.description, m.preview_path, c.name AS categorie
            FROM media m
            LEFT JOIN category c ON m.category_id = c.id
            WHERE m.type_id = (SELECT id FROM media_type WHERE type = ?)
            AND m.est_supprime = 0
            ORDER BY m.date_ajout DESC
            LIMIT ? OFFSET ?
        ''', (user_choice, limit, offset))

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results

    def get_media_count(self, user_choice):
        """Compte le nombre total de médias"""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT COUNT(*) 
            FROM media 
            WHERE type_id = (SELECT id FROM media_type WHERE type = ?)
            AND est_supprime = 0
        ''', (user_choice,))

        count = cursor.fetchone()[0]
        conn.close()
        return count



    def queue_update(self, media_id, field, value):
        """Ajoute une mise à jour à la file d'attente"""
        self.update_queue.append((media_id, field, value))
        
    def process_updates(self):
        """Exécute les mises à jour en batch"""
        if not self.update_queue:
            return
            
        updates = {}
        for media_id, field, value in self.update_queue:
            if media_id not in updates:
                updates[media_id] = {}
            updates[media_id][field] = value
            
        self.update_queue = []
        
        with sqlite3.connect(self.DB_PATH) as conn:
            cursor = conn.cursor()
            for media_id, fields in updates.items():
                set_clause = ", ".join(f"{k} = ?" for k in fields.keys())
                values = list(fields.values()) + [media_id]
                
                cursor.execute(f"""
                    UPDATE media 
                    SET {set_clause}, date_modification = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, values)
            conn.commit()
# Classe pour gérer les médias
# class MediaManager:

    def create_database(self):
        """Crée la base de données SQLite avec les tables media, media_type, et category."""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

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

        # Insérer les types de médias par défaut (media1 à media10)
        for i in range(1, 11):
            cursor.execute('''
                INSERT OR IGNORE INTO media_type (type, label, description) VALUES (?, ?, ?)
            ''', (f'media{i}', f'Media {i}', f'Description for Media {i}'))

        # Insérer une catégorie par défaut
        cursor.execute('''
            INSERT OR IGNORE INTO category (name, label, description) VALUES (?, ?, ?)
        ''', ('Default', 'Default Category', 'Default category description'))

        conn.commit()
        conn.close()

    # def load_media_from_db(self, user_choice):
    #     """Charge les médias depuis la base de données."""
    #     conn = sqlite3.connect(self.DB_PATH)
    #     cursor = conn.cursor()

    #     cursor.execute('''
    #         SELECT media.id, media.nom, media.description, media.preview_path, category.name 
    #         FROM media 
    #         LEFT JOIN category ON media.category_id = category.id
    #         WHERE media.type_id = (SELECT id FROM media_type WHERE type = ?) AND media.est_supprime = 0
    #     ''', (user_choice,))

    #     media_list = [
    #         {
    #             'id': row[0],
    #             'nom': row[1],
    #             'description': row[2],
    #             'preview_path': row[3],
    #             'categorie': row[4]
    #         }
    #         for row in cursor.fetchall()
    #     ]

    #     conn.close()
    #     return media_list
    def load_media_from_db(self, user_choice, limit=100, offset=0):
        """Charge les médias avec pagination et jointures optimisées"""
        with sqlite3.connect(self.DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Requête optimisée avec LEFT JOIN et pagination
            cursor.execute('''
                SELECT 
                    m.id, 
                    m.nom, 
                    m.description, 
                    m.preview_path, 
                    c.name AS categorie,
                    mt.type AS media_type
                FROM media m
                LEFT JOIN category c ON m.category_id = c.id
                LEFT JOIN media_type mt ON m.type_id = mt.id
                WHERE mt.type = ? 
                AND m.est_supprime = 0
                ORDER BY m.date_ajout DESC
                LIMIT ? OFFSET ?
            ''', (user_choice, limit, offset))
            
            return [dict(row) for row in cursor.fetchall()]
        

    import logging

    logging.basicConfig(level=logging.DEBUG)

    def add_media_to_db(self, media, user_choice):
        """Ajoute un média à la base de données."""
        logging.debug(f"Tentative d'ajout d'un média avec user_choice = {user_choice}")
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        # Récupérer l'id du type de média sélectionné
        cursor.execute('SELECT id FROM media_type WHERE type = ?', (user_choice,))
        type_result = cursor.fetchone()
        logging.debug(f"Résultat de la requête media_type : {type_result}")
        if type_result is None:
            raise ValueError(f"Le type de média '{user_choice}' n'existe pas dans la table media_type.")
        type_id = type_result[0]

        # Récupérer l'id de la catégorie par défaut
        cursor.execute('SELECT id FROM category WHERE name = ?', ('Default',))
        category_result = cursor.fetchone()
        logging.debug(f"Résultat de la requête category : {category_result}")
        if category_result is None:
            raise ValueError("La catégorie 'Default' n'existe pas dans la table category.")
        category_id = category_result[0]

        # Ajouter le média avec le type_id et category_id correspondants
        cursor.execute('''
            INSERT INTO media (nom, description, preview_path, type_id, category_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (media['nom'], media['description'], media['preview_path'], type_id, category_id))

        conn.commit()
        conn.close()
        
    def update_media_in_db(self, media, user_choice):
        """Met à jour un média dans la base de données."""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE media
            SET description = ?, category_id = ?, date_modification = CURRENT_TIMESTAMP
            WHERE nom = ? AND type_id = (SELECT id FROM media_type WHERE type = ?)
        ''', (media['description'], media.get('category_id'), media['nom'], user_choice))

        conn.commit()
        conn.close()

    def delete_media_in_db(self, media, user_choice):
        """Marque un média comme supprimé dans la base de données."""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE media
            SET est_supprime = 1, date_suppression = CURRENT_TIMESTAMP
            WHERE nom = ? AND type_id = (SELECT id FROM media_type WHERE type = ?)
        ''', (media['nom'], user_choice))

        conn.commit()
        conn.close()

    def load_categories(self):
        """Charge la liste des catégories depuis la base de données."""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, name, label, description, date_creation, date_modification, date_suppression FROM category
        ''')

        categories = [{'id': row[0], 'name': row[1], 'label': row[2], 'description': row[3], 'date_creation': row[4], 'date_modification': row[5], 'date_suppression': row[6]} for row in cursor.fetchall()]
        conn.close()
        return categories

    def add_category(self, name, label, description):
        """Ajoute une nouvelle catégorie à la base de données."""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO category (name, label, description) VALUES (?, ?, ?)
        ''', (name, label, description))

        conn.commit()
        conn.close()

    def delete_category(self, category_id):
        """Supprime une catégorie de la base de données."""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM category WHERE id = ?
        ''', (category_id,))

        conn.commit()
        conn.close()

    def load_archives(self, user_choice):
        """Charge les médias archivés depuis la base de données."""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT media.id, media.nom, media.description, media.preview_path, category.name 
            FROM media 
            LEFT JOIN category ON media.category_id = category.id
            WHERE media.type_id = (SELECT id FROM media_type WHERE type = ?) AND media.est_supprime = 1
        ''', (user_choice,))

        archives = [
            {
                'id': row[0],
                'nom': row[1],
                'description': row[2],
                'preview_path': row[3],
                'categorie': row[4]
            }
            for row in cursor.fetchall()
        ]

        conn.close()
        return archives

    def restore_media(self, media_id, user_choice):
        """Restaure un média archivé."""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE media
            SET est_supprime = 0, date_suppression = NULL
            WHERE id = ? AND type_id = (SELECT id FROM media_type WHERE type = ?)
        ''', (media_id, user_choice))

        conn.commit()
        conn.close()

    def has_media_in_category(self, category_id):
        """Vérifie si une catégorie contient des médias."""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT COUNT(*) FROM media WHERE category_id = ?
        ''', (category_id,))

        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def has_media_in_type(self, type_id):
        """Vérifie si un type contient des médias."""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT COUNT(*) FROM media WHERE type_id = ?
        ''', (type_id,))

        count = cursor.fetchone()[0]
        conn.close()
        return count > 0



from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QHeaderView, QAbstractItemView, QMessageBox, QFileDialog, QMenu, QAction
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
import json
import sqlite3
import shutil
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QComboBox, 
                            QDialogButtonBox, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QComboBox, 
                            QDialogButtonBox, QLabel, QFrame, QHBoxLayout,
                            QPushButton, QFileDialog, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon

class AddMediaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un média")
        self.setFixedSize(600, 500)
        self.media_path = ""
        
        # Style CSS moderne
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #333;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            QLineEdit, QComboBox {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                margin-bottom: 15px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #4d90fe;
            }
            QPushButton {
                background-color: #4d90fe;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #357ae8;
            }
            QPushButton#cancelButton, QPushButton#browseButton {
                background-color: #f1f1f1;
                color: #333;
            }
            QPushButton#cancelButton:hover, QPushButton#browseButton:hover {
                background-color: #e5e5e5;
            }
            .header {
                font-size: 18px;
                color: #444;
                margin-bottom: 20px;
            }
            #previewLabel {
                border: 2px dashed #ccc;
                border-radius: 4px;
                background-color: white;
                qproperty-alignment: AlignCenter;
                min-height: 150px;
            }
            #previewLabel:hover {
                border-color: #4d90fe;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # En-tête
        header = QLabel("Ajouter un nouveau média")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(header)

        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #ddd;")
        layout.addWidget(separator)

        # Nom du média
        name_label = QLabel("Nom du média:")
        layout.addWidget(name_label)
        
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Entrez le nom du média")
        self.name_input.setToolTip("Le nom doit contenir entre 3 et 50 caractères")
        layout.addWidget(self.name_input)

        # Description
        description_label = QLabel("Description:")
        layout.addWidget(description_label)
        
        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Entrez une description (optionnel)")
        layout.addWidget(self.description_input)

        # Catégorie
        category_label = QLabel("Catégorie:")
        layout.addWidget(category_label)
        
        self.category_combo = QComboBox(self)
        self.category_combo.addItems(["Film", "Série", "Documentaire", "Animation", "Autre"])
        self.category_combo.setCurrentIndex(-1)  # Aucune sélection par défaut
        layout.addWidget(self.category_combo)

        # Sélection du fichier média
        file_label = QLabel("Fichier média:")
        layout.addWidget(file_label)
        
        file_layout = QHBoxLayout()
        
        self.file_path_input = QLineEdit(self)
        self.file_path_input.setReadOnly(True)
        self.file_path_input.setPlaceholderText("Aucun fichier sélectionné")
        file_layout.addWidget(self.file_path_input)
        
        browse_button = QPushButton("Parcourir...", self)
        browse_button.setObjectName("browseButton")
        browse_button.clicked.connect(self.browse_media_file)
        file_layout.addWidget(browse_button)
        
        layout.addLayout(file_layout)

        # Aperçu du média
        preview_label = QLabel("Aperçu:", self)
        layout.addWidget(preview_label)
        
        self.preview_label = QLabel(self)
        self.preview_label.setObjectName("previewLabel")
        self.preview_label.setFixedHeight(200)
        self.preview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.preview_label.setText("Aperçu du média apparaîtra ici")
        self.preview_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.preview_label)

        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        
        # Personnalisation des boutons
        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setText("Confirmer")
        ok_button.setObjectName("confirmButton")
        
        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText("Annuler")
        cancel_button.setObjectName("cancelButton")
        
        button_box.accepted.connect(self.validate_inputs)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)

    def browse_media_file(self):
        """Ouvre un dialogue pour sélectionner un fichier média."""
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Fichiers média (*.mp4 *.mov *.avi *.jpg *.png *.jpeg)")
        file_dialog.setViewMode(QFileDialog.Detail)
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.media_path = selected_files[0]
                self.file_path_input.setText(os.path.basename(self.media_path))
                self.update_preview()

    def update_preview(self):
        """Met à jour l'aperçu en fonction du type de fichier."""
        if not self.media_path:
            return
            
        # Vérifie si c'est une image
        if self.media_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            pixmap = QPixmap(self.media_path)
            if not pixmap.isNull():
                # Redimensionne l'image pour qu'elle tienne dans le label
                pixmap = pixmap.scaled(
                    self.preview_label.width(), 
                    self.preview_label.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.preview_label.setPixmap(pixmap)
        else:
            # Pour les vidéos, affiche une icône générique
            self.preview_label.setPixmap(QIcon.fromTheme("video-x-generic").pixmap(64, 64))
            self.preview_label.setText(f"Fichier vidéo: {os.path.basename(self.media_path)}")

    def validate_inputs(self):
        """Valide les entrées avant d'accepter le dialogue."""
        # Réinitialise les styles
        self.name_input.setStyleSheet("")
        self.category_combo.setStyleSheet("")
        
        name = self.name_input.text().strip()
        errors = []
        
        if not name:
            errors.append("Le nom du média est requis")
            self.name_input.setStyleSheet("border: 1px solid red;")
            
        if len(name) < 3 or len(name) > 50:
            errors.append("Le nom doit contenir entre 3 et 50 caractères")
            self.name_input.setStyleSheet("border: 1px solid red;")
            
        if self.category_combo.currentIndex() == -1:
            errors.append("Veuillez sélectionner une catégorie")
            self.category_combo.setStyleSheet("border: 1px solid red;")
            
        if not self.media_path:
            errors.append("Veuillez sélectionner un fichier média")
            self.file_path_input.setStyleSheet("border: 1px solid red;")
        else:
            self.file_path_input.setStyleSheet("")
            
        if errors:
            # Ici vous pourriez afficher les erreurs dans un QMessageBox
            return
            
        # Si tout est valide
        self.accept()

    def get_media_data(self):
        """Return the media data entered by the user."""
        return {
            'nom': self.name_input.text().strip(),
            'description': self.description_input.text().strip(),
            'categorie': self.category_combo.currentText(),
            'media_path': self.media_path,
            'file_name': os.path.basename(self.media_path) if self.media_path else "",
            'file_type': os.path.splitext(self.media_path)[1].lower() if self.media_path else "",
            'preview_path': self.generate_preview() if self.media_path else ""
        }

    def generate_preview(self):
        """Génère un aperçu à enregistrer dans la base de données."""
        # Ici vous pourriez:
        # 1. Pour les images: enregistrer une miniature
        # 2. Pour les vidéos: extraire une frame ou garder le chemin
        # Pour l'exemple, nous retournons simplement le chemin
        return self.media_path
    
import time
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QDateTime, QTime
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QCalendarWidget

from PyQt5.QtWidgets import QSpinBox, QDateTimeEdit, QDialogButtonBox, QCalendarWidget, QTextEdit
from PyQt5.QtCore import QDate, QTime, QDateTime
from PyQt5.QtCore import QEvent

    # ... (les autres méthodes restent les mêmes)
class RichTextDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = None
    def eventFilter(self, editor, event):
        """Gère les événements clavier pour une meilleure expérience d'édition"""
        if event.type() == QEvent.KeyPress:
            # Valider avec Ctrl+Entrée
            if event.key() == Qt.Key_Return and (event.modifiers() & Qt.ControlModifier):
                self.commitData.emit(editor)
                self.closeEditor.emit(editor, QAbstractItemDelegate.SubmitModelCache)
                return True
            
            # Tabulation pour navigation
            elif event.key() == Qt.Key_Tab:
                self.commitData.emit(editor)
                self.closeEditor.emit(editor, QAbstractItemDelegate.SubmitModelCache)
                return False  # Laissez le tableau gérer la navigation
                
            # Échap pour annuler
            elif event.key() == Qt.Key_Escape:
                self.closeEditor.emit(editor, QAbstractItemDelegate.RevertModelCache)
                return True
                
        return super().eventFilter(editor, event)

    def createEditor(self, parent, option, index):
        """Crée un éditeur riche lorsqu'on double-clique"""
        self.editor = QTextEdit(parent)
        self.editor.setStyleSheet("""
            QTextEdit {
                border: 2px solid #3498db;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Segoe UI';
                font-size: 14px;
                min-height: 100px;
                background-color: white;
            }
        """)
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.editor.setAcceptRichText(False)
        return self.editor

    def setEditorData(self, editor, index):
        """Charge les données dans l'éditeur"""
        editor.setPlainText(index.data(Qt.DisplayRole))

    def setModelData(self, editor, model, index):
        """Sauvegarde les données après édition"""
        model.setData(index, editor.toPlainText(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        """Ajuste la géométrie de l'éditeur"""
        editor.setGeometry(option.rect.adjusted(0, 0, 0, 100))  # Étendre vers le bas

    def sizeHint(self, option, index):
        """Définit la taille initiale de l'item"""
        size = super().sizeHint(option, index)
        size.setHeight(size.height() * 2)  # Double hauteur pour les descriptions
        return size


class MediaTable(QWidget):
    def handle_item_changed(self, item):
        """Gère les modifications des cellules"""
        if item.column() == 2:  # Si c'est la colonne description
            media_id = self.table.item(item.row(), 0).data(Qt.UserRole)
            new_description = item.text()
            
            # Sauvegarde différée
            QTimer.singleShot(1000, lambda: 
                self.save_description(media_id, new_description)
            )

    def save_description(self, media_id, description):
        """Sauvegarde asynchrone"""
        threading.Thread(
            target=self.media_manager.update_media_description,
            args=(media_id, description, self.user_choice),
            daemon=True
    ).start()
 # class MediaTable(QWidget):
    def __inipt__(self, parent=None):
        super().__init__(parent)
        self.user_choice = self.load_user_choice()
        self.media_manager = MediaManager(DB_PATH)
        self.media_list = self.media_manager.load_media_from_db(self.user_choice)
        self.page_size = 20
        self.current_page = 0
        
        # Couleurs modernes
        self.primary_color = "#3498db"
        self.secondary_color = "#2ecc71"
        self.dark_color = "#2c3e50"
        self.light_color = "#ecf0f1"
        self.accent_color = "#e74c3c"
        self.setup_pagination()

        self.init_ui()

        # ... (header et toolbar existants)

        self.db_manager = DatabaseManager(DB_PATH)  # Nouveau manager optimisé
        self.init_ui()
        self.load_page()
        # ... (pagination et footer existants)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_page = 0
        self.page_size = 50
        self.total_items = 0
        
        # Initialisez d'abord le layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Ensuite initialisez la table
        self.table = QTableWidget()
        self.init_table()
        
        # Initialisez la pagination
        self.setup_pagination()
        
        # Chargez les données
        self.load_page()

    def load_page(self):
        """Charge une page spécifique"""
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            offset = self.current_page * self.page_size
            self.media_list = self.media_manager.load_media_from_db_paginated(
                self.user_choice, 
                limit=self.page_size, 
                offset=offset
            )
            self.total_items = self.media_manager.get_media_count(self.user_choice)
            self.populate_table()
            self.update_pagination_controls()
        finally:
            QApplication.restoreOverrideCursor()

    def update_pagination_controls(self):
        """Met à jour l'état des boutons"""
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(
            (self.current_page + 1) * self.page_size < self.total_items
        )
        self.page_label.setText(
            f"Page {self.current_page + 1}/{(self.total_items // self.page_size) + 1}"
        )

    def next_page(self):
        """Page suivante"""
        if (self.current_page + 1) * self.page_size < self.total_items:
            self.current_page += 1
            self.load_page()

    def prev_page(self):
        """Page précédente"""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_page()





    def load_page1(self):
        """Charge une page de données de manière optimisée"""
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.media_list = self.db_manager.get_paginated_media(
                self.user_choice,
                limit=self.page_size,
                offset=self.current_page * self.page_size
            )
            self.populate_table()
            self.update_pagination()
        finally:
            QApplication.restoreOverrideCursor()

    def update_pagination(self):
        """Met à jour les contrôles de pagination"""
        total_items = self.db_manager.get_media_count(self.user_choice)
        total_pages = (total_items + self.page_size - 1) // self.page_size
        
        self.page_label.setText(
            f"Page {self.current_page + 1}/{max(1, total_pages)} | "
            f"Total: {total_items} médias"
        )
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(
            (self.current_page + 1) * self.page_size < total_items
        )  
# class MediaTable(QWidget):



    def init_ui(self):
        """Initialise l'interface utilisateur avec un design moderne"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.light_color};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QLabel {{
                color: {self.dark_color};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header avec dégradé et ombre (hauteur réduite)
        self.header = QWidget()
        self.header.setFixedHeight(80)  # Hauteur réduite
        self.header.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.primary_color}, stop:1 {self.secondary_color});
                border-radius: 0;
                padding: 10px;
            }}
        """)
        
        header_layout = QVBoxLayout(self.header)
        header_layout.setContentsMargins(20, 5, 20, 5)  # Marges réduites
        
        # Titre avec icône
        title_layout = QHBoxLayout()
        
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("icons/logo.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        self.title_label = QLabel("FBK GROUP MANAGEMENT")
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: 20px;  # Taille réduite
                font-weight: bold;
                margin-left: 10px;
            }}
        """)
        
        title_layout.addWidget(self.logo_label)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        layout.addWidget(self.header)

        # Barre d'outils avec effet de carte
        toolbar = QWidget()
        toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-radius: 8px;
                margin: 15px;
                padding: 10px;
                border: 1px solid #ddd;
            }}
        """)
        
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        
        # Bouton d'action avec menu déroulant (avec emoji)
        self.action_button = self.create_tool_button("📋 Actions", self.primary_color)
        self.action_button.setMenu(self.create_action_menu())
        
        # Bouton de paramètres (avec emoji)
        self.settings_button = self.create_tool_button("⚙️ Paramètres", "#7f8c8d")
        self.settings_button.setMenu(self.create_settings_menu())
        
        # Bouton d'ajout de média (avec emoji)
        self.add_media_button = self.create_tool_button("➕ Ajouter média", self.secondary_color)
        self.add_media_button.clicked.connect(self.import_media)
        
        # Bouton d'envoi au robot
        self.update_robot_button = self.create_tool_button("🤖 Envoyer au robot", self.accent_color)
        self.update_robot_button.clicked.connect(self.show_update_modal)
        
        # Barre de recherche
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("🔍 Rechercher...")
        self.search_field.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px 15px;
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 20px;
                background-color: white;
                min-width: 250px;
            }}
            QLineEdit:focus {{
                border: 1px solid {self.primary_color};
                box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
            }}
        """)
        self.search_field.textChanged.connect(self.filter_table)
        
        # Sélecteur d'instance
        self.instance_combo = QComboBox()
        self.instance_combo.addItems([f"media{i}" for i in range(1, 11)])
        self.instance_combo.setCurrentText(self.user_choice)
        self.instance_combo.currentIndexChanged.connect(self.on_instance_changed)
        self.instance_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 8px 15px;
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 20px;
                background-color: white;
            }}
            QComboBox:hover {{
                border: 1px solid {self.primary_color};
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left-width: 1px;
                border-left-color: #ddd;
                border-left-style: solid;
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }}
        """)
        
        toolbar_layout.addWidget(self.search_field)
        toolbar_layout.addWidget(self.instance_combo)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_media_button)
        toolbar_layout.addWidget(self.action_button)
        toolbar_layout.addWidget(self.settings_button)
        toolbar_layout.addWidget(self.update_robot_button)
        
        layout.addWidget(toolbar)

        # Configuration du tableau avec style amélioré pour l'édition
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Nom', 'Description', 'Catégorie', 'Aperçu', 'Actions'])

        # Configuration pour la sélection multiple
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)  # Permet la sélection multiple
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # Augmenter la hauteur des lignes
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setDefaultSectionSize(40)
        
        # Activer le word-wrap pour les descriptions
        self.table.setWordWrap(True)
        
        # Style amélioré pour le tableau
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 8px;
                margin: 15px;
                border: 1px solid #ddd;
                gridline-color: #eee;
                font-size: 14px;
                selection-background-color: #e3f2fd;
                selection-color: black;
                alternate-background-color: #f9f9f9;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: black;
            }
            QTextEdit {
                selection-background-color: #3498db;
                selection-color: white;
            }
        """)

        # Configuration des colonnes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        # Activer l'édition
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        
        layout.addWidget(self.table)
        
        # Pagination avec style moderne
        pagination = QWidget()
        pagination.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                margin: 15px;
                padding: 10px;
                border: 1px solid #ddd;
            }
        """)
        
        pagination_layout = QHBoxLayout(pagination)
        
        self.prev_button = QPushButton("◀ Précédent")
        self.prev_button.setStyleSheet(f"""
            QPushButton {{
                padding: 8px 15px;
                background-color: {self.light_color};
                color: {self.dark_color};
                border: none;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #d5dbdb;
            }}
        """)
        self.prev_button.clicked.connect(self.prev_page)
        
        self.page_label = QLabel("Page 1")
        self.page_label.setStyleSheet(f"color: {self.dark_color};")
        
        self.next_button = QPushButton("Suivant ▶")
        self.next_button.setStyleSheet(f"""
            QPushButton {{
                padding: 8px 15px;
                background-color: {self.primary_color};
                color: white;
                border: none;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
        """)
        self.next_button.clicked.connect(self.next_page)
        
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.next_button)
        
        layout.addWidget(pagination)
        
        # Activer la navigation au clavier
        self.table.setTabKeyNavigation(True)
        
        self.populate_table()
        
    
    def __ini4t__(self, parent=None):
        super().__init__(parent)
        # ... (initialisation existante)
        self.init_ui()
           



    def populate_table(self):
        """Remplit le tableau avec pagination"""
        self.table.setRowCount(len(self.media_list))
        
        for row, media in enumerate(self.media_list):
            # Colonne 0 cachée - ID
            id_item = QTableWidgetItem(str(media['id']))
            id_item.setData(Qt.UserRole, media['id'])
            id_item.setFlags(Qt.NoItemFlags)
            self.table.setItem(row, 0, id_item)

            # Colonne 1 - Nom
            name_item = QTableWidgetItem(media['nom'])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, name_item)

            # Colonne 2 - Description
            desc_item = QTableWidgetItem(media['description'])
            desc_item.setFont(QFont("Segoe UI", 10))
            desc_item.setFlags(desc_item.flags() | Qt.ItemIsEditable)
            self.table.setItem(row, 2, desc_item)
            
            # ... le reste de votre méthode existante ...


    # def populate_table(self):
    #     """Remplit le tableau avec un style amélioré et les nouvelles fonctionnalités"""
    #     self.table.setRowCount(len(self.media_list))
        
    #     for row, media in enumerate(self.media_list):
    #         # Colonne Nom
    #         name_item = QTableWidgetItem(media['nom'])
    #         name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
    #         self.table.setItem(row, 0, name_item)

    #         # # Colonne Description avec éditeur enrichi
    #         # desc_item = QTableWidgetItem(media['description'])
    #         # desc_item.setFont(QFont("Segoe UI", 10))
    #         # self.table.setItem(row, 1, desc_item)
   
    #         # Colonne Description avec éditeur enrichi
    #         desc_item = QTableWidgetItem(media['description'])
    #         desc_item.setFont(QFont("Segoe UI", 10))
    #         desc_item.setFlags(desc_item.flags() | Qt.ItemIsEditable)
    #         self.table.setItem(row, 1, desc_item)
            
            # Configurer le delegate pour la colonne Description
            self.table.setItemDelegateForColumn(1, RichTextDelegate(self.table))

 
            # Colonne Catégorie
            category_combo = QComboBox()
            categories = self.media_manager.load_categories()
            for category in categories:
                category_combo.addItem(category['name'])
            category_combo.setCurrentText(media.get('categorie', 'Default'))
            category_combo.currentTextChanged.connect(lambda text, row=row: self.update_category(row, text))
            self.table.setCellWidget(row, 2, category_combo)

            # Colonne Aperçu
            preview_label = QLabel()
            preview_label.setAlignment(Qt.AlignCenter)
            if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
                pixmap = QPixmap(media['preview_path']).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                preview_label.setPixmap(pixmap)
            elif media['nom'].endswith(('.mp4', '.mov')):
                preview_label.setText("🎥 Voir")
            preview_label.mousePressEvent = lambda event, path=media['preview_path']: self.show_preview(path)
            self.table.setCellWidget(row, 3, preview_label)
            from PyQt5.QtWidgets import QToolButton

            def create_action_button(emoji, tooltip, color, hover_color, callback):
                btn = QToolButton()
                btn.setText(emoji)
                btn.setToolTip(tooltip)
                btn.setCursor(Qt.PointingHandCursor)
                btn.setStyleSheet(f"""
                    QToolButton {{
                        background-color: {color};
                        color: white;
                        border: none;
                        border-radius: 6px;
                        padding: 6px;
                        font-size: 18px;
                    }}
                    QToolButton:hover {{
                        background-color: {hover_color};
                        box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
                    }}
                """)
                btn.clicked.connect(callback)
                return btn

            # Colonne Actions avec style amélioré
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(8, 2, 8, 2)
            action_layout.setSpacing(10)

            # Boutons avec emojis
            schedule_btn = create_action_button("📅", "Planifier la publication", "#9b59b6", "#8e44ad", lambda _, m=media: self.schedule_publication(m))
            send_btn = create_action_button("🤖", "Envoyer au robot", "#3498db", "#2980b9", lambda _, m=media: self.send_to_robot(m))
            delete_btn = create_action_button("🗑️", "Supprimer", "#e74c3c", "#c0392b", lambda _, m=media: self.delete_media(m))

            # Ajout à l’interface
            for btn in [schedule_btn, send_btn, delete_btn]:
                action_layout.addWidget(btn)


            self.table.setCellWidget(row, 4, action_widget)
   
        # Ajuster automatiquement la hauteur des lignes
        self.table.resizeRowsToContents()
        self.table.setColumnHidden(0, True)
        
        # Connecter le signal pour redimensionner après édition
        self.table.model().dataChanged.connect(lambda: self.table.resizeRowsToContents())
           # Cache la colonne ID
   
    def delete_media(self, media):
        """Version corrigée de la suppression de média"""
        try:
            # Vérifier si le fichier existe avant de le déplacer
            if not os.path.exists(media['preview_path']):
                QMessageBox.warning(self, "Erreur", "Le fichier média n'existe plus.")
                return

            # Créer le dossier archive s'il n'existe pas
            archive_folder = os.path.join(media_folder, f"{self.user_choice}Archive")
            os.makedirs(archive_folder, exist_ok=True)

            # Générer un nom de fichier d'archive unique
            base_name = os.path.basename(media['preview_path'])
            archive_name = f"archived_{int(time.time())}_{base_name}"
            archive_path = os.path.join(archive_folder, archive_name)

            # Déplacer le fichier
            shutil.move(media['preview_path'], archive_path)

            # Supprimer de la base de données
            self.media_manager.delete_media_in_db(media, self.user_choice)
            
            # Rafraîchir l'affichage
            self.media_list = self.media_manager.load_media_from_db(self.user_choice)
            self.populate_table()

            QMessageBox.information(self, "Succès", "Média supprimé et archivé avec succès.")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")

    def schedule_publication(self, media):
        """Ouvre un modal de planification avec calendrier"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Planifier la publication")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Calendrier
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            QCalendarWidget QToolButton {
                height: 30px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.calendar)
        
        # Sélecteur d'heure
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Heure:"))
        
        self.hour_spin = QSpinBox()
        self.hour_spin.setRange(0, 23)
        self.hour_spin.setValue(12)
        time_layout.addWidget(self.hour_spin)
        
        time_layout.addWidget(QLabel("Minute:"))
        
        self.minute_spin = QSpinBox()
        self.minute_spin.setRange(0, 59)
        self.minute_spin.setValue(0)
        time_layout.addWidget(self.minute_spin)
        
        layout.addLayout(time_layout)
        
        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        if dialog.exec_() == QDialog.Accepted:
            selected_date = self.calendar.selectedDate()
            selected_time = QTime(self.hour_spin.value(), self.minute_spin.value())
            datetime = QDateTime(selected_date, selected_time)
            
            # Ici vous pourriez enregistrer la date planifiée dans la base de données
            QMessageBox.information(self, "Planifié", 
                                  f"Publication planifiée pour le {datetime.toString('dd/MM/yyyy HH:mm')}")

    def send_to_robot(self, media):
        """Envoie un seul média au robot"""
        try:
            # Préparer les données pour l'envoi
            data = {
                "posts": [{
                    "id": media['id'],
                    "name": media['nom'],
                    "description": media['description'],
                    "path": media['preview_path'],
                    "type": "image" if media['nom'].endswith(('.png', '.jpg', '.jpeg')) else "video"
                }],
                "groups": []
            }

            # Afficher une progression
            progress = QProgressDialog("Envoi au robot en cours...", "Annuler", 0, 100, self)
            progress.setWindowModality(Qt.WindowModal)
            
            # Simuler l'envoi progressif
            for i in range(5):
                progress.setValue(i * 20)
                QApplication.processEvents()
                time.sleep(0.5)
                if progress.wasCanceled():
                    break

            progress.close()
            
            QMessageBox.information(self, "Succès", "Média envoyé au robot avec succès!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de l'envoi au robot : {str(e)}")

    # Pour avoir un éditeur qui s'étend en hauteur
    def eventFilter(self, editor, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            editor.textCursor().insertText("\n")
            return True
        return super().eventFilter(editor, event)

    def on_cell_changed(self, row, column):
        """Amélioration de l'édition directe dans le tableau"""
        if column == 1:  # Colonne Description
            try:
                new_description = self.table.item(row, column).text()
                media = self.media_list[row]
                
                # Créer un champ de texte riche temporaire pour améliorer l'expérience
                text_edit = QTextEdit()
                text_edit.setPlainText(new_description)
                text_edit.setStyleSheet("""
                    QTextEdit {
                        border: 1px solid #3498db;
                        border-radius: 4px;
                        padding: 5px;
                        font-family: 'Segoe UI';
                        font-size: 14px;
                    }
                """)
                
                # Afficher l'éditeur en plein tableau
                self.table.setCellWidget(row, column, text_edit)
                text_edit.setFocus()
                
                # Quand l'édition est terminée (quand le widget perd le focus)
                def finish_edit():
                    final_text = text_edit.toPlainText()
                    self.table.removeCellWidget(row, column)
                    item = QTableWidgetItem(final_text)
                    self.table.setItem(row, column, item)
                    
                    # Mettre à jour la base de données
                    media['description'] = final_text
                    self.media_manager.update_media_in_db(media, self.user_choice)
                
                text_edit.focusOutEvent = lambda event: finish_edit()
                
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de la modification : {str(e)}")

    def create_tool_button(self, text, color):
        """Crée un bouton d'outil stylisé"""
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                padding: 8px 15px;
                background-color: {color};
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 14px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color, 15)};
            }}
        """)
        return button

    def darken_color(self, hex_color, percent):
        """Assombrit une couleur hexadécimale"""
        color = QColor(hex_color)
        return color.darker(100 + percent).name()

    def populate_table1(self):
        """Remplit le tableau avec un style amélioré"""
        self.table.setRowCount(len(self.media_list))
        
        for row, media in enumerate(self.media_list):
            # Nom avec icône selon le type
            name_item = QTableWidgetItem()
            if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
                name_item.setIcon(QIcon("icons/image.png"))
            elif media['nom'].endswith(('.mp4', '.mov')):
                name_item.setIcon(QIcon("icons/video.png"))
            name_item.setText(media['nom'])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, name_item)
            
            # Description avec style riche
            desc_item = QTableWidgetItem(media['description'])
            desc_item.setFont(QFont("Segoe UI", 10))
            self.table.setItem(row, 1, desc_item)
            
            # Catégorie avec badge coloré
            category_combo = QComboBox()
            categories = self.media_manager.load_categories()
            for category in categories:
                category_combo.addItem(category['name'])
            category_combo.setCurrentText(media.get('categorie', 'Default'))
            category_combo.currentTextChanged.connect(lambda text, row=row: self.update_category(row, text))
            category_combo.setStyleSheet("""
                QComboBox {
                    padding: 5px;
                    border: 1px solid #ddd;
                    border-radius: 12px;
                }
            """)
            self.table.setCellWidget(row, 2, category_combo)
            
            # Aperçu avec effet de survol
            preview_label = QLabel()
            preview_label.setAlignment(Qt.AlignCenter)
            if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
                pixmap = QPixmap(media['preview_path']).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                preview_label.setPixmap(pixmap)
            elif media['nom'].endswith(('.mp4', '.mov')):
                preview_label.setText("🎥 Cliquer pour prévisualiser")
                preview_label.setStyleSheet("color: #3498db; font-style: italic;")
            preview_label.mousePressEvent = lambda event, path=media['preview_path']: self.show_preview(path)
            self.table.setCellWidget(row, 3, preview_label)
            
            # Boutons d'action avec style moderne
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(5)
            
            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon("icons/edit.png"))
            edit_btn.setToolTip("Modifier")
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f39c12;
                    border-radius: 5px;
                    padding: 5px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #e67e22;
                }
            """)
            edit_btn.clicked.connect(lambda _, m=media: self.edit_media(m))
            
            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon("icons/delete.png"))
            delete_btn.setToolTip("Supprimer")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    border-radius: 5px;
                    padding: 5px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            delete_btn.clicked.connect(lambda _, m=media: self.delete_media(m))
            
            view_btn = QPushButton()
            view_btn.setIcon(QIcon("icons/view.png"))
            view_btn.setToolTip("Voir")
            view_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    border-radius: 5px;
                    padding: 5px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            view_btn.clicked.connect(lambda _, m=media: self.show_media(m))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(view_btn)
            action_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(row, 4, action_widget)
        
        # Mise à jour de la pagination
        self.page_label.setText(f"Page {self.current_page + 1}")
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled((self.current_page + 1) * self.page_size < len(self.media_list))

    def show_preview(self, path):
        """Affiche un aperçu agrandi avec animation"""
        preview = QDialog(self)
        preview.setWindowTitle("Aperçu")
        preview.setWindowModality(Qt.ApplicationModal)
        
        layout = QVBoxLayout(preview)
        
        if path.endswith(('.png', '.jpg', '.jpeg')):
            label = QLabel()
            pixmap = QPixmap(path)
            label.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(label)
        elif path.endswith(('.mp4', '.mov')):
            # Ici vous pourriez intégrer un lecteur vidéo
            label = QLabel("Prévisualisation vidéo non implémentée")
            layout.addWidget(label)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(preview.close)
        layout.addWidget(close_btn)
        
        preview.exec_()

    # ... (le reste des méthodes reste inchangé)
# class MediaTable(QWidget):
    def __initt__(self, parent=None):
        super().__init__(parent)
        self.user_choice = self.load_user_choice()  # Load user choice
        self.media_manager = MediaManager(DB_PATH)
        self.media_list = self.media_manager.load_media_from_db(self.user_choice)
        self.page_size = 10
        self.current_page = 0

        # Initialize UI
        self.init_ui()

    def load_user_choice(self):
        """Load the last user choice from a JSON file."""
        config_path = os.path.join(user_data_dir, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get('user_choice', 'media1')  # Default to 'media1'
        return 'media1'  # Default to 'media1'

    def save_user_choice(self, choice):
        """Save the user choice to a JSON file."""
        config_path = os.path.join(user_data_dir, 'config.json')
        config = {'user_choice': choice}
        with open(config_path, 'w') as f:
            json.dump(config, f)
    def setup_pagination1(self):
        """Initialise les contrôles de pagination"""
        self.pagination_widget = QWidget()
        pagination_layout = QHBoxLayout(self.pagination_widget)
        
        self.prev_button = QPushButton("◀ Précédent")
        self.prev_button.clicked.connect(self.prev_page)
        
        self.page_label = QLabel()
        
        self.next_button = QPushButton("Suivant ▶")
        self.next_button.clicked.connect(self.next_page)
        
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.next_button)
        
        # Ajoutez ce widget à votre layout principal
        self.layout().addWidget(self.pagination_widget)
    def setup_pagination(self):
        """Initialise les contrôles de pagination"""
        self.pagination_widget = QWidget()
        pagination_layout = QHBoxLayout(self.pagination_widget)
        pagination_layout.setContentsMargins(10, 5, 10, 5)
        
        self.prev_button = QPushButton("◀ Précédent")
        self.prev_button.clicked.connect(self.prev_page)
        
        self.page_label = QLabel("Chargement...")
        self.page_label.setAlignment(Qt.AlignCenter)
        
        self.next_button = QPushButton("Suivant ▶")
        self.next_button.clicked.connect(self.next_page)
        
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.next_button)
        
        # Ajout au layout principal
        self.main_layout.addWidget(self.table)
        self.main_layout.addWidget(self.pagination_widget)


    def init_table(self):
        """Initialise la configuration de base du tableau"""
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Nom', 'Description', 'Catégorie', 'Actions'])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        
        # Configuration des colonnes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        def init_uii(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)

        # # Header
        # header = QLabel("📁 AI Media Management", self)
        # header.setStyleSheet("font-size: 24px; font-weight: bold; color: #003366; padding: 10px;")
        # layout.addWidget(header)
        header = HeaderSection(self, title="FBK GRUP MANAGEMENT", app_name="Nova360 AI", slogan="AI Marketing Automation Solution")
        layout.addWidget(header)

        # Top layout for buttons and search bar
        top_layout = QHBoxLayout()

        # Action button with dropdown menu
        self.action_button = QPushButton("⚡ Action", self)
        self.action_button.setMenu(self.create_action_menu())
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
        
        

        # Settings button with dropdown menu
        self.settings_button = QPushButton("⚙️ Settings", self)
        self.settings_button.setMenu(self.create_settings_menu())
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

        # # Update Robot button
        # self.update_robot_button = QPushButton("🤖 Update Robot", self)
        # self.update_robot_button.clicked.connect(self.show_update_modal)
        # self.update_robot_button.setStyleSheet("""
        #     QPushButton {
        #         padding: 10px 18px;
        #         font-size: 14px;
        #         font-weight: bold;
        #         background-color: #17a2b8;
        #         color: white;
        #         border: none;
        #         border-radius: 8px;
        #     }
        #     QPushButton:hover {
        #         background-color: #117a8b;
        #     }
        #     QPushButton:pressed {
        #         background-color: #0d5c73;
        #     }
        # """)

        self.add_media_button = QPushButton("🖼️ Add Media")
        self.add_media_button.clicked.connect(self.import_media)

        # Stylisation du bouton
        self.add_media_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)
            
        # Bouton "Update Robot" avec menu déroulant
        self.update_robot_button = QPushButton(self.tr("🤖 Send to Robot"), self)
        self.update_robot_button.setStyleSheet("""
            QPushButton {
                background-color: #1F1B24; /* Dark background */
                color: #00D4FF; /* Neon text color */
                border: 2px solid #00D4FF; /* Bright border */
                border-radius: 20px; /* Rounded corners */
                font-size: 16px;
                padding: 10px 20px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #00D4FF; /* Hover color */
                color: #1F1B24; /* Inverted text */
                border: 2px solid #1F1B24; /* Dark border */
            }
            QPushButton:pressed {
                background-color: #008DBE; /* Click color */
                border: 2px solid #006B93;
            }
        """)
        self.update_robot_button.clicked.connect(self.show_update_modal)

        # Search bar
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText(self.tr("🔍 Search..."))
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

        # Media selection combo box
        self.instance_combo = QComboBox(self)
        self.instance_combo.addItems([f"media{i}" for i in range(1, 11)])  # Media 1 to Media 10
        self.instance_combo.setCurrentText(self.user_choice)
        self.instance_combo.currentIndexChanged.connect(self.on_instance_changed)
        self.instance_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: white;
            }
            QComboBox:hover {
                border: 1px solid #007BFF;
            }
        """)



        top_layout.addWidget(self.search_field)
        top_layout.addWidget(self.instance_combo)

        # Spacer to push the search bar and media selection to the right
        top_layout.addStretch()

        top_layout.addWidget(self.add_media_button)
        
        top_layout.addWidget(self.action_button)
        top_layout.addWidget(self.settings_button)
        
        top_layout.addWidget(self.update_robot_button)
        


        # Add the top layout to the main layout
        layout.addLayout(top_layout)


        # # Media table
        # self.table = QTableWidget(self)
        # self.table.setColumnCount(5)
        # self.table.setHorizontalHeaderLabels(['Name', 'Description', 'Category', 'Preview', 'Action'])
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        # self.table.cellChanged.connect(self.on_cell_changed)
        # layout.addWidget(self.table)

        # Media table
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Name', 'Description', 'Category', 'Preview', 'Action'])

        # Configuration des résizes des colonnes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Nom - s'ajuste au contenu
        header.setSectionResizeMode(1, QHeaderView.Stretch)          # Description - prend l'espace disponible
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Catégorie - s'ajuste au contenu
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Preview - s'ajuste au contenu
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Action - s'ajuste au contenu

        # Ou si vous préférez des largeurs fixes :
        # self.table.setColumnWidth(0, 100)   # Nom (largeur fixe)
        # self.table.setColumnWidth(1, 400)   # Description (plus large)
        # self.table.setColumnWidth(2, 100)   # Catégorie
        # self.table.setColumnWidth(3, 150)   # Preview
        # self.table.setColumnWidth(4, 100)   # Action

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.table.cellChanged.connect(self.on_cell_changed)
        layout.addWidget(self.table)


        # Pagination buttons
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("⬅️ Previous", self)
        self.prev_button.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("➡️ Next", self)
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)

        layout.addLayout(pagination_layout)

        # # Footer
        # footer = QLabel("© 2023 AI Media Management", self)
        # footer.setStyleSheet("font-size: 12px; color: #666; padding: 10px;")
        # layout.addWidget(footer)
        footer = FooterSection(self)
        layout.addWidget(footer)
        # Populate the table
        self.populate_table()
  
  
    def export_media(self):
        """Export media to a file."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Media", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['nom', 'description', 'categorie', 'preview_path'])
                    writer.writeheader()
                    writer.writerows(self.media_list)
                QMessageBox.information(self, "Success", "Media exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error during export: {e}")

    def export_description(self):
        """Export descriptions to a file."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Descriptions", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            try:
                descriptions = {media['id']: media['description'] for media in self.media_list}
                with open(file_name, 'w') as f:
                    json.dump(descriptions, f, indent=4)
                QMessageBox.information(self, "Success", "Descriptions exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error during export: {e}")

    def reload_list(self):
        """Reload the media list from the database."""
        self.media_list = self.media_manager.load_media_from_db(self.user_choice)
        self.populate_table()
        QMessageBox.information(self, "Success", "Media list reloaded successfully!")

    def manage_social_networks(self):
        """Open a dialog to manage social networks."""
        dialog = ReseauSocialManagementDialog(self)  # Utilisez la classe ReseauSocialManagementDialog
        dialog.exec_()
    def manage_media_types(self):
        """Open a dialog to manage social networks."""
        dialog = MediaTypeManagementDialog(self)  # Utilisez la classe ReseauSocialManagementDialog
        dialog.exec_()

    def open_robot_management_dialog(self):
        """Ouvre une boîte de dialogue pour gérer les robots."""
        dialog = RobotManagementDialog(self)
        dialog.exec_()
                
    def manage_archives(self):
        # """Open a dialog to manage archives."""
        # dialog = ManageArchivesDialog(self.media_manager, self.user_choice, self)
        # dialog.exec_()
        pass
    def create_action_menu(self):
        """Create a context menu for the Action button."""
        menu = QMenu()
        # Import Media action
        import_media_action = QAction("📥 Import Media", self)
        import_media_action.triggered.connect(self.import_media)
        menu.addAction(import_media_action)
        # Add Media action
        add_media_action = QAction("➕ Add Media", self)
        add_media_action.triggered.connect(self.open_add_media_dialog)
        # menu.addAction(add_media_action)

        # Export Media action
        export_media_action = QAction("📤 Export Media", self)
        export_media_action.triggered.connect(self.export_media)
        menu.addAction(export_media_action)

        # Import Description action
        import_description_action = QAction("📄 Import Description", self)
        import_description_action.triggered.connect(self.import_description)
        menu.addAction(import_description_action)

        # Export Description action
        export_description_action = QAction("📝 Export Description", self)
        export_description_action.triggered.connect(self.export_description)
        menu.addAction(export_description_action)

        # Delete Selected action
        delete_selected_action = QAction("🗑️ Delete Selected", self)
        delete_selected_action.triggered.connect(self.delete_selected_media)
        menu.addAction(delete_selected_action)

        # Delete All action
        delete_all_action = QAction("🔥 Delete All", self)
        delete_all_action.triggered.connect(self.delete_all_media)
        menu.addAction(delete_all_action)

        # Reload List action
        reload_list_action = QAction("🔄 Reload List", self)
        reload_list_action.triggered.connect(self.reload_list)
        menu.addAction(reload_list_action)

        return menu

    def create_settings_menu(self):
        """Create a context menu for the Settings button."""
        menu = QMenu()

        # Category Management action
        category_management_action = QAction("📂 Category Management", self)
        category_management_action.triggered.connect(self.manage_categories)
        menu.addAction(category_management_action)

        # Social Network Management action
        social_network_management_action = QAction("🌐 Social Network Management", self)
        social_network_management_action.triggered.connect(self.manage_social_networks)
        menu.addAction(social_network_management_action)

        # Media Type Management action
        media_type_management_action = QAction("🎥 Media Type Management", self)
        media_type_management_action.triggered.connect(self.manage_media_types)
        menu.addAction(media_type_management_action)

        # Archive Management action
        archive_management_action = QAction("📦 Archive Management", self)
        archive_management_action.triggered.connect(self.manage_archives)
        menu.addAction(archive_management_action)

        robot_management_action = QAction("🤖 " + self.tr("Robot Management"), self)
        robot_management_action.triggered.connect(self.open_robot_management_dialog)
        menu.addAction(robot_management_action)
        return menu


    def open_add_media_dialog(self):
        """Open a dialog to add a new media."""
        dialog = AddMediaDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            media_data = dialog.get_media_data()  # Assurez-vous que cette méthode existe dans AddMediaDialog
            self.media_manager.add_media_to_db(media_data, self.user_choice)
            self.populate_table()


    def populate_table1(self):
        """Populate the table with media."""
        self.table.setRowCount(len(self.media_list))

        for row, media in enumerate(self.media_list):
            # Name column
            name_item = QTableWidgetItem(media['nom'])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)  # Prevent editing the name
            self.table.setItem(row, 0, name_item)

            # Description column
            description_item = QTableWidgetItem(media['description'])
            self.table.setItem(row, 1, description_item)

            # Category column
            category_combo = QComboBox()
            categories = self.media_manager.load_categories()
            for category in categories:
                category_combo.addItem(category['name'])
            category_combo.setCurrentText(media.get('categorie', 'Default'))
            category_combo.currentTextChanged.connect(lambda text, row=row: self.update_category(row, text))
            self.table.setCellWidget(row, 2, category_combo)

            # Preview column
            preview_label = QLabel()
            if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
                pixmap = QPixmap(media['preview_path']).scaled(150, 150, Qt.KeepAspectRatio)
                preview_label.setPixmap(pixmap)
            elif media['nom'].endswith(('.mp4', '.mov')):
                preview_label.setText("🎥 Video (click to preview)")
            preview_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 3, preview_label)

            # Action column
            action_button = QPushButton("⚡ Action", self)
            action_button.setMenu(self.create_action_menu_for_media(media))
            self.table.setCellWidget(row, 4, action_button)

    def create_action_menu_for_media(self, media):
        """Create a context menu for media actions."""
        menu = QMenu()

        # Edit action
        edit_action = QAction("✏️ Edit", self)
        edit_action.triggered.connect(lambda: self.edit_media(media))
        menu.addAction(edit_action)

        # Delete action
        delete_action = QAction("🗑️ Delete", self)
        delete_action.triggered.connect(lambda: self.delete_media(media))
        menu.addAction(delete_action)

        # Show action
        show_action = QAction("👁️ Show", self)
        show_action.triggered.connect(lambda: self.show_media(media))
        menu.addAction(show_action)

        return menu
    








    def create_add_media_menu(self):
        """Create a context menu for adding media."""
        menu = QMenu()

        # Import Media action
        import_media_action = QAction("📥 Import Media", self)
        import_media_action.triggered.connect(self.import_media)
        menu.addAction(import_media_action)

        # Import Description action
        import_description_action = QAction("📄 Import Description", self)
        import_description_action.triggered.connect(self.import_description)
        menu.addAction(import_description_action)

        return menu

    def create_delete_menu(self):
        """Create a context menu for delete actions."""
        menu = QMenu()

        # Delete Selected action
        delete_selected_action = QAction("🗑️ Delete Selected", self)
        delete_selected_action.triggered.connect(self.delete_selected_media)
        menu.addAction(delete_selected_action)

        # Delete All action
        delete_all_action = QAction("🔥 Delete All", self)
        delete_all_action.triggered.connect(self.delete_all_media)
        menu.addAction(delete_all_action)

        return menu






    def import_media(self):
        """Ouvre une boîte de dialogue pour importer des médias."""
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Sélectionner des médias")
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg);;Vidéos (*.mp4 *.mov)")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)

        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_files = file_dialog.selectedFiles()
            for selected_file in selected_files:
                self.add_single_media(selected_file)
        self.media_list = self.media_manager.load_media_from_db(self.user_choice)
        self.populate_table()
    def import_description(self):
        """Ouvre une boîte de dialogue pour importer des descriptions."""
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Sélectionner un fichier JSON")
        file_dialog.setNameFilter("JSON files (*.json)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            with open(selected_file, 'r') as f:
                descriptions = json.load(f)
                for media_id, description in descriptions.items():
                    self.update_media_description(int(media_id), description)

    def add_single_media(self, file_path):
        """Ajoute un seul média à la base de données."""
        file_name = os.path.basename(file_path)

        # Créer le dossier média correspondant au type sélectionné
        media_type_folder = os.path.join(media_folder, self.user_choice)
        os.makedirs(media_type_folder, exist_ok=True)

        # Trouver le prochain numéro disponible
        existing_files = [f for f in os.listdir(media_type_folder) if f.split('.')[0].isdigit()]
        existing_numbers = sorted([int(f.split('.')[0]) for f in existing_files])
        next_number = 1
        for i, num in enumerate(existing_numbers):
            if num != i + 1:
                next_number = i + 1
                break
        else:
            next_number = len(existing_numbers) + 1

        # Renommer le fichier
        new_name = f"{next_number}{os.path.splitext(file_name)[1]}"
        destination_path = os.path.join(media_type_folder, new_name)

        # Copier le fichier dans le dossier média
        shutil.copy(file_path, destination_path)

        # Créer un nouvel objet média
        new_media = {
            'nom': new_name,
            'description': 'Nouveau média',
            'preview_path': destination_path,
            'categorie': 'Default'
        }

        # Ajouter le média à la base de données
        self.media_manager.add_media_to_db(new_media, self.user_choice)
        self.populate_table()

    def update_media_description1(self, media_id, description):
        """Met à jour la description d'un média dans la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE media
            SET description = ?, date_modification = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (description, media_id))

        conn.commit()
        conn.close()
        self.populate_table()
    def update_media_description(self, media_id, new_description, user_choice):
        """Met à jour la description dans la base"""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE media 
            SET description = ?, date_modification = CURRENT_TIMESTAMP
            WHERE id = ? AND type_id = (
                SELECT id FROM media_type WHERE type = ?
            )
        ''', (new_description, media_id, user_choice))
        
        conn.commit()
        conn.close()
    def on_instance_changed(self):
        """Met à jour l'interface lorsque l'utilisateur change de dossier média."""
        self.user_choice = self.instance_combo.currentText()
        self.save_user_choice(self.user_choice)
        self.media_list = self.media_manager.load_media_from_db(self.user_choice)
        self.populate_table()

    # def populate_table(self):
    #     """Remplit le tableau avec les médias."""
    #     self.table.setRowCount(len(self.media_list))

    #     for row, media in enumerate(self.media_list):
    #         # Colonne "Nom"
    #         nom_item = QTableWidgetItem(media['nom'])
    #         nom_item.setFlags(nom_item.flags() & ~Qt.ItemIsEditable)  # Empêcher l'édition du nom
    #         self.table.setItem(row, 0, nom_item)

    #         # Colonne "Description"
    #         description_item = QTableWidgetItem(media['description'])
    #         self.table.setItem(row, 1, description_item)

    #         # Colonne "Catégorie"
    #         categorie_combo = QComboBox()
    #         categories = self.media_manager.load_categories()
    #         for category in categories:
    #             categorie_combo.addItem(category['name'])
    #         categorie_combo.setCurrentText(media.get('categorie', 'Default'))
    #         categorie_combo.currentTextChanged.connect(lambda text, row=row: self.update_category(row, text))
    #         self.table.setCellWidget(row, 2, categorie_combo)

    #         # Colonne "Preview"
    #         preview_label = QLabel()
    #         if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
    #             pixmap = QPixmap(media['preview_path']).scaled(150, 150, Qt.KeepAspectRatio)
    #             preview_label.setPixmap(pixmap)
    #         elif media['nom'].endswith(('.mp4', '.mov')):
    #             preview_label.setText("Vidéo (cliquer pour prévisualiser)")
    #         preview_label.setAlignment(Qt.AlignCenter)
    #         self.table.setCellWidget(row, 3, preview_label)

    #         # Colonne "Action"
    #         action_button = QPushButton('Action', self)
    #         action_button.setMenu(self.create_action_menu(media))
    #         self.table.setCellWidget(row, 4, action_button)

    def update_category(self, row, category_name):
        """Met à jour la catégorie d'un média."""
        media = self.media_list[row]
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id FROM category WHERE name = ?
        ''', (category_name,))
        category_id = cursor.fetchone()[0]

        cursor.execute('''
            UPDATE media
            SET category_id = ?, date_modification = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (category_id, media['id']))

        conn.commit()
        conn.close()



    def edit_media(self, media):
        """Ouvre une boîte de dialogue pour éditer un média."""
        dialog = UpdateMediaDialog(media, self)
        if dialog.exec_() == QDialog.Accepted:
            updated_media = dialog.get_updated_media()
            self.media_manager.update_media_in_db(updated_media, self.user_choice)
            self.populate_table()


    def delete_media1(self, media):
        progress = QProgressDialog("Suppression en cours...", None, 0, 0, self)
        progress.setWindowTitle("Veuillez patienter")
        progress.setCancelButton(None)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        QApplication.processEvents()

        try:
            archive_folder = os.path.join(media_folder, f"{self.user_choice}Archive")
            os.makedirs(archive_folder, exist_ok=True)

            archive_files = [f for f in os.listdir(archive_folder) if f.startswith('archive')]
            archive_number = len(archive_files) + 1
            archive_name = f"archive{archive_number}{os.path.splitext(media['nom'])[1]}"
            archive_path = os.path.join(archive_folder, archive_name)

            shutil.move(media['preview_path'], archive_path)

            self.media_manager.delete_media_in_db(media, self.user_choice)
            # self.media_list = self.media_manager.load_media_from_db(self.user_choice)
            # self.populate_table()
        finally:
            progress.close()


    def show_media(self, media):
        """Affiche un aperçu du média."""
        dialog = PreviewDialog(media['preview_path'], media['description'], self)
        dialog.exec_()


    def delete_selected_media(self):
        """Supprime les médias sélectionnés avec une indication visuelle professionnelle."""
        selected_rows = sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True)
        if not selected_rows:
            return

        progress = QProgressDialog("Suppression des éléments sélectionnés...", None, 0, len(selected_rows), self)
        progress.setWindowTitle("Veuillez patienter")
        progress.setWindowModality(Qt.ApplicationModal)
        progress.setCancelButton(None)
        progress.setMinimumDuration(0)
        progress.show()

        for i, row in enumerate(selected_rows):
            media = self.media_list[row]
            self.delete_media(media)
            progress.setValue(i + 1)
            QApplication.processEvents()

        progress.close()
        self.media_list = self.media_manager.load_media_from_db(self.user_choice)
        self.populate_table()

    def delete_all_media(self):
        """Supprime tous les médias avec confirmation et progression professionnelle."""
        confirm = QMessageBox.question(self, 'Confirmation', "Êtes-vous sûr de vouloir supprimer tous les médias ?", QMessageBox.Yes | QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return

        total = len(self.media_list)
        if total == 0:
            return

        progress = QProgressDialog("Suppression de tous les médias...", None, 0, total, self)
        progress.setWindowTitle("Veuillez patienter")
        progress.setWindowModality(Qt.ApplicationModal)
        progress.setCancelButton(None)
        progress.setMinimumDuration(0)
        progress.show()

        for i, media in enumerate(self.media_list):
            self.delete_media(media)
            progress.setValue(i + 1)
            QApplication.processEvents()

        progress.close()
        self.media_list = self.media_manager.load_media_from_db(self.user_choice)
        self.populate_table()


    def manage_categories(self):
        """Ouvre une boîte de dialogue pour gérer les catégories."""
        dialog = ManageCategoriesDialog(self.media_manager, self)
        dialog.exec_()

    def manage_types(self):
        """Ouvre une boîte de dialogue pour gérer les types de médias."""
        dialog = ManageTypesDialog(self.media_manager, self)
        dialog.exec_()

    def manage_archives(self):
        """Ouvre une boîte de dialogue pour gérer les archives."""
        dialog = ManageArchivesDialog(self.media_manager, self.user_choice, self)
        dialog.exec_()

    def show_update_modal(self):
        """Affiche une boîte de dialogue pour mettre à jour le robot."""
        dialog = UpdateRobotDialog(self)
        dialog.exec_() 
            # choice, remember = dialog.get_choice()
            # if choice == "text":
            #     print("Mise à jour du texte uniquement")
            # elif choice == "robot":
            #     print("Mise à jour complète du robot")

    def filter_table(self):
        """Filtre les médias affichés dans le tableau en fonction du texte de recherche."""
        search_text = self.search_field.text().lower()
        filtered_media = [media for media in self.media_list if search_text in media['nom'].lower() or search_text in media['description'].lower()]
        self.populate_table()

    def prev_page1(self):
        """Navigue vers la page précédente."""
        if self.current_page > 0:
            self.current_page -= 1
            self.populate_table()

    def next_page1(self):
        """Navigue vers la page suivante."""
        if (self.current_page + 1) * self.page_size < len(self.media_list):
            self.current_page += 1
            self.populate_table()

    def on_cell_changed1(self, row, column):
        """Met à jour la base de données lorsque l'utilisateur modifie une cellule."""
        if column == 1:  # Colonne "Description"
            media = self.media_list[row]
            new_description = self.table.item(row, column).text()
            media['description'] = new_description
            self.media_manager.update_media_in_db(media, self.user_choice)
        elif column == 2:  # Colonne "Catégorie"
            media = self.media_list[row]
            new_category = self.table.item(row, column).text()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id FROM category WHERE name = ?
            ''', (new_category,))
            category_id = cursor.fetchone()[0]

            cursor.execute('''
                UPDATE media
                SET category_id = ?, date_modification = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (category_id, media['id']))

            conn.commit()
            conn.close()

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QLabel, QMessageBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class UpdateMediaDialog(QDialog):
    def __init__(self, media, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Éditer le média")
        self.setWindowIcon(QIcon("icons/edit.png"))  # Ajouter une icône
        self.setFixedSize(400, 200)  # Taille fixe pour une meilleure apparence
        self.media = media

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-bottom: 20px;
            }
            QLineEdit:focus {
                border: 2px solid #007BFF;
            }
            QDialogButtonBox {
                margin-top: 20px;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 6px;
                background-color: #007BFF;
                color: white;
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

        # Layout principal
        layout = QVBoxLayout(self)

        # Titre
        self.title_label = QLabel("Modifier la description du média", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Champ de saisie pour la description
        self.description_input = QLineEdit(self.media['description'], self)
        self.description_input.setPlaceholderText("Entrez la nouvelle description...")
        self.description_input.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.description_input)

        # Boutons Ok et Annuler
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.button(QDialogButtonBox.Ok).setIcon(QIcon("icons/check.png"))  # Icône pour Ok
        button_box.button(QDialogButtonBox.Cancel).setIcon(QIcon("icons/cancel.png"))  # Icône pour Annuler
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def validate_and_accept(self):
        """Valide la saisie avant d'accepter."""
        description = self.description_input.text().strip()
        if not description:
            QMessageBox.warning(self, "Erreur", "La description ne peut pas être vide !")
            return
        self.accept()

    def get_updated_media(self):
        """Retourne le média avec la description mise à jour."""
        self.media['description'] = self.description_input.text().strip()
        return self.media
    
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QCheckBox, QMessageBox
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QComboBox, QListWidget, QListWidgetItem, QHBoxLayout, QLabel, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sqlite3
import os
import sqlite3
from PyQt5.QtWidgets import QProgressDialog, QMessageBox
from PyQt5.QtCore import Qt
from datetime import datetime
import ctypes

class FileTransferApp:
    def __init__(self):
        # Connexion à la base de données
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        # Dossier cible pour les données
        self.target_dir = "C:\\Bon"

    # def start_process(self):
    #     """Démarre le processus de transfert des données depuis la base de données."""
    #     if not self.confirm_submission():
    #         self.show_error("Processus annulé par l'utilisateur.")
    #         return

    #     if not os.path.exists(self.target_dir):
    #         os.makedirs(self.target_dir)

    #     # Créer une boîte de dialogue de progression
    #     progress_dialog = QProgressDialog("Transfert des données en cours...", "Annuler", 0, 100)
    #     progress_dialog.setWindowTitle("Processus de transfert")
    #     progress_dialog.setWindowModality(Qt.WindowModal)
    #     progress_dialog.setMinimumDuration(0)
    #     progress_dialog.setValue(0)

    #     # Récupérer les données des médias et des groupes depuis la base de données
    #     media_data = self.get_media_data()
    #     group_data = self.get_group_data()

    #     if not media_data and not group_data:
    #         self.show_error("Aucune donnée trouvée dans la base de données.")
    #         return

    #     # Créer un dossier pour chaque robot
    #     for idx, (media, groups) in enumerate(zip(media_data, group_data)):
    #         robot_folder = os.path.join(self.target_dir, f"robot{idx + 1}")
    #         if not os.path.exists(robot_folder):
    #             os.makedirs(robot_folder)

    #         # Enregistrer les données dans un fichier JSON
    #         combined_content = {
    #             "posts": [{"text": media_item[1], "image": media_item[2]} for media_item in media],
    #             "groups": [{"link": group_item[1]} for group_item in groups],
    #         }

    #         target_json_path = os.path.join(robot_folder, "data.json")
    #         with open(target_json_path, 'w', encoding='utf-8') as json_file:
    #             import json
    #             json.dump(combined_content, json_file, ensure_ascii=False, indent=4)

    #         # Cacher le dossier
    #         self.hide_file(robot_folder)

    #         # Mettre à jour la progression
    #         progress_dialog.setValue(int((idx + 1) / len(media_data) * 100))
    #         if progress_dialog.wasCanceled():
    #             self.show_error("Processus annulé.")
    #             return

    #     progress_dialog.setValue(100)
    #     self.show_success("Le processus est terminé avec succès.")


    def start_process(self, combined_content):
        """
        Démarre le processus de transfert des données vers le robot.
        
        Args:
            combined_content (dict): Données combinées (médias et groupes).
        """
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        # Créer un dossier pour chaque robot
        robot_folder = os.path.join(self.target_dir, "robot1")
        if not os.path.exists(robot_folder):
            os.makedirs(robot_folder)

        # Enregistrer les données dans un fichier JSON
        target_json_path = os.path.join(robot_folder, "data.json")
        with open(target_json_path, 'w', encoding='utf-8') as json_file:
            import json
            json.dump(combined_content, json_file, ensure_ascii=False, indent=4)

        # Cacher le dossier
        self.hide_file(robot_folder)

    def hide_file(self, file_path):
        """Cache un fichier ou un dossier avec les attributs 'hidden' et 'system'."""
        if os.path.exists(file_path):
            ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04)
    def get_media_data(self):
        """Récupère les données des médias depuis la base de données."""
        self.cursor.execute("""
            SELECT m.id, m.nom, m.description, m.preview_path, mt.type
            FROM media m
            JOIN media_type mt ON m.type_id = mt.id
            WHERE m.est_supprime = 0
        """)
        return self.cursor.fetchall()

    def get_group_data(self):
        """Récupère les données des groupes depuis la base de données."""
        self.cursor.execute("""
            SELECT g.id, g.link, g.remarks, g.description, g.keywords
            FROM groups g
            WHERE g.category_id IN (SELECT id FROM category)
        """)
        return self.cursor.fetchall()

    def confirm_submission(self):
        """Demande à l'utilisateur de confirmer la soumission."""
        reply = QMessageBox.question(
            None,
            "Confirmation",
            "Avez-vous vérifié que tous les médias et leurs descriptions sont corrects avant de les soumettre au robot ?",
            QMessageBox.Yes | QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def hide_file(self, file_path):
        """Cache un fichier ou un dossier avec les attributs 'hidden' et 'system'."""
        if os.path.exists(file_path):
            ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04)

    def show_error(self, message):
        """Affiche une boîte de dialogue d'erreur."""
        QMessageBox.critical(None, "Erreur", message)

    def show_success(self, message):
        """Affiche une boîte de dialogue de succès."""
        QMessageBox.information(None, "Succès", message)

    def close_connection(self):
        """Ferme la connexion à la base de données."""
        self.conn.close()

class FileTransferApp2:
    def __init__(self):
        # Connexion à la base de données
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        # Dossier cible pour les données
        self.target_dir = "C:\\Bon"

    # def start_process(self):
    #     """Démarre le processus de transfert des données depuis la base de données."""
    #     if not self.confirm_submission():
    #         self.show_error("Processus annulé par l'utilisateur.")
    #         return

    #     if not os.path.exists(self.target_dir):
    #         os.makedirs(self.target_dir)

    #     # Créer une boîte de dialogue de progression
    #     progress_dialog = QProgressDialog("Transfert des données en cours...", "Annuler", 0, 100)
    #     progress_dialog.setWindowTitle("Processus de transfert")
    #     progress_dialog.setWindowModality(Qt.WindowModal)
    #     progress_dialog.setMinimumDuration(0)
    #     progress_dialog.setValue(0)

    #     # Récupérer les données des médias et des groupes depuis la base de données
    #     media_data = self.get_media_data()
    #     group_data = self.get_group_data()

    #     if not media_data and not group_data:
    #         self.show_error("Aucune donnée trouvée dans la base de données.")
    #         return

    #     # Créer un dossier pour chaque robot
    #     for idx, (media, groups) in enumerate(zip(media_data, group_data)):
    #         robot_folder = os.path.join(self.target_dir, f"robot{idx + 1}")
    #         if not os.path.exists(robot_folder):
    #             os.makedirs(robot_folder)

    #         # Enregistrer les données dans un fichier JSON
    #         combined_content = {
    #             "posts": [{"text": media_item[1], "image": media_item[2]} for media_item in media],
    #             "groups": [{"link": group_item[1]} for group_item in groups],
    #         }

    #         target_json_path = os.path.join(robot_folder, "data.json")
    #         with open(target_json_path, 'w', encoding='utf-8') as json_file:
    #             import json
    #             json.dump(combined_content, json_file, ensure_ascii=False, indent=4)

    #         # Cacher le dossier
    #         self.hide_file(robot_folder)

    #         # Mettre à jour la progression
    #         progress_dialog.setValue(int((idx + 1) / len(media_data) * 100))
    #         if progress_dialog.wasCanceled():
    #             self.show_error("Processus annulé.")
    #             return

    #     progress_dialog.setValue(100)
    #     self.show_success("Le processus est terminé avec succès.")


    def start_process(self, combined_content):
        """
        Démarre le processus de transfert des images vers le robot.
        
        Args:
            combined_content (dict): Données combinées (médias et groupes).
        """
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        # Créer un dossier pour chaque robot
        robot_folder = os.path.join(self.target_dir, "robot1")
        if not os.path.exists(robot_folder):
            os.makedirs(robot_folder)

        # Enregistrer les images dans le dossier
        for idx, post in enumerate(combined_content["posts"]):
            if post["image"]:  # Vérifier si une image est associée
                image_path = post["image"]
                target_image_path = os.path.join(robot_folder, f"image_{idx + 1}.jpg")
                if os.path.exists(image_path):
                    import shutil
                    shutil.copy(image_path, target_image_path)

        # Cacher le dossier
        self.hide_file(robot_folder)

    def hide_file(self, file_path):
        """Cache un fichier ou un dossier avec les attributs 'hidden' et 'system'."""
        if os.path.exists(file_path):
            ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04)
    def get_media_data(self):
        """Récupère les données des médias depuis la base de données."""
        self.cursor.execute("""
            SELECT m.id, m.nom, m.description, m.preview_path, mt.type
            FROM media m
            JOIN media_type mt ON m.type_id = mt.id
            WHERE m.est_supprime = 0
        """)
        return self.cursor.fetchall()

    def get_group_data(self):
        """Récupère les données des groupes depuis la base de données."""
        self.cursor.execute("""
            SELECT g.id, g.link, g.remarks, g.description, g.keywords
            FROM groups g
            WHERE g.category_id IN (SELECT id FROM category)
        """)
        return self.cursor.fetchall()

    def confirm_submission(self):
        """Demande à l'utilisateur de confirmer la soumission."""
        reply = QMessageBox.question(
            None,
            "Confirmation",
            "Avez-vous vérifié que tous les médias et leurs descriptions sont corrects avant de les soumettre au robot ?",
            QMessageBox.Yes | QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def hide_file(self, file_path):
        """Cache un fichier ou un dossier avec les attributs 'hidden' et 'system'."""
        if os.path.exists(file_path):
            ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04)

    def show_error(self, message):
        """Affiche une boîte de dialogue d'erreur."""
        QMessageBox.critical(None, "Erreur", message)

    def show_success(self, message):
        """Affiche une boîte de dialogue de succès."""
        QMessageBox.information(None, "Succès", message)

    def close_connection(self):
        """Ferme la connexion à la base de données."""
        self.conn.close()

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLabel, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sqlite3

import os
import sqlite3
import json
import ctypes
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLabel, QMessageBox, QProgressDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sqlite3
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QListWidget, QListWidgetItem, 
                            QPushButton, QLabel, QMessageBox, QTabWidget, QWidget,
                            QProgressDialog, QHBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal

DB_PATH = "database.db"
class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._optimize_database()

    def _optimize_database(self):
        """Applique les optimisations SQLite au démarrage"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA cache_size=-10000")  # 10MB cache
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA temp_store=MEMORY")
            
            # Création des index critiques
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_media_type 
                ON media(type_id)
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_media_category 
                ON media(category_id)
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_media_deleted 
                ON media(est_supprime)
            ''')

    def get_paginated_media(self, media_type, limit=100, offset=0):
        """Version optimisée pour la pagination"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT m.*, c.name AS category_name
                FROM media m
                LEFT JOIN category c ON m.category_id = c.id
                WHERE m.type_id = (
                    SELECT id FROM media_type WHERE type = ?
                )
                AND m.est_supprime = 0
                LIMIT ? OFFSET ?
            ''', (media_type, limit, offset))
            
            return [dict(row) for row in cursor.fetchall()]

    def get_media_count(self, media_type):
        """Compte rapide pour la pagination"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) 
                FROM media 
                WHERE type_id = (
                    SELECT id FROM media_type WHERE type = ?
                )
                AND est_supprime = 0
            ''', (media_type,))
            return cursor.fetchone()[0]
# class DatabaseManager:
#     def __init__(self, db_path):
#         self.db_path = db_path
        
#     def __enter__(self):
#         self.conn = sqlite3.connect(self.db_path)
#         self.cursor = self.conn.cursor()
#         return self
        
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.conn.close()
        
#     def get_media_categories(self):
#         self.cursor.execute("SELECT id, name, description FROM category")
#         return self.cursor.fetchall()
        
#     def get_group_categories(self):
#         self.cursor.execute("SELECT id, name, description FROM category")
#         return self.cursor.fetchall()
        
#     def get_media_by_category(self, category_ids):
#         query = f"""
#             SELECT m.id, m.nom, m.description, m.preview_path, mt.type
#             FROM media m
#             JOIN media_type mt ON m.type_id = mt.id
#             WHERE m.category_id IN ({','.join('?'*len(category_ids))})
#         """
#         self.cursor.execute(query, category_ids)
#         return self.cursor.fetchall()
        
#     def get_groups_by_category(self, category_ids):
#         query = f"""
#             SELECT g.id, g.link, g.remarks, g.description, g.keywords
#             FROM groups g
#             WHERE g.category_id IN ({','.join('?'*len(category_ids))})
#         """
#         self.cursor.execute(query, category_ids)
#         return self.cursor.fetchall()
        
#     def get_single_media(self, media_id):
#         self.cursor.execute("""
#             SELECT m.id, m.nom, m.description, m.preview_path, mt.type
#             FROM media m
#             JOIN media_type mt ON m.type_id = mt.id
#             WHERE m.id = ?
#         """, (media_id,))
#         return self.cursor.fetchone()
        
#     def get_single_group(self, group_id):
#         self.cursor.execute("""
#             SELECT id, link, remarks, description, keywords
#             FROM groups
#             WHERE id = ?
#         """, (group_id,))
#         return self.cursor.fetchone()

class SendWorker(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, data, is_bulk=True):
        super().__init__()
        self.data = data
        self.is_bulk = is_bulk
        
    def run(self):
        try:
            if self.is_bulk:
                # Logique d'envoi en masse
                total_items = len(self.data.get("posts", [])) + len(self.data.get("groups", []))
                for i in range(total_items):
                    self.progress_updated.emit(int((i+1)/total_items*100))
                    QThread.msleep(100)  # Simulation
            else:
                # Logique d'envoi unitaire
                for i in range(5):  # Simulation de sous-étapes
                    self.progress_updated.emit((i+1)*20)
                    QThread.msleep(150)
                    
            self.finished.emit(True, "Envoi réussi")
        except Exception as e:
            self.finished.emit(False, str(e))

class UpdateRobotDialognew(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()
        self.load_data_async()
        self.current_selection = None
        
    def setup_ui(self):
        self.setWindowTitle("Envoyer au Robot")
        self.setWindowIcon(QIcon("icons/robot.png"))
        self.setFixedSize(700, 550)
        
        # Style moderne
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial;
            }
            QTabWidget::pane {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 4px;
                background: white;
            }
            QTabBar::tab {
                padding: 8px 16px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #3b82f6;
                color: white;
            }
            QListWidget {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                background: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e5e7eb;
            }
            QListWidget::item:selected {
                background: #bfdbfe;
                color: #1e40af;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
            }
            #send_button {
                background-color: #3b82f6;
                color: white;
            }
            #send_button:hover {
                background-color: #2563eb;
            }
            #send_one_button {
                background-color: #10b981;
                color: white;
            }
            #send_one_button:hover {
                background-color: #059669;
            }
        """)
        
        # Onglets principaux
        self.tabs = QTabWidget()
        self.setup_media_tab()
        self.setup_groups_tab()
        
        # Barre de boutons
        button_layout = QHBoxLayout()
        self.send_button = QPushButton("Envoyer la sélection", objectName="send_button")
        self.send_one_button = QPushButton("Envoyer l'élément sélectionné", objectName="send_one_button")
        self.cancel_button = QPushButton("Annuler")
        button_layout.addWidget(self.send_one_button)
        button_layout.addStretch()
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.cancel_button)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        
    def setup_media_tab(self):
        """Configure l'onglet des médias"""
        self.media_tab = QWidget()
        layout = QVBoxLayout()
        
        # Filtres
        filter_layout = QHBoxLayout()
        self.media_filter = QLineEdit(placeholderText="Filtrer les médias...")
        self.media_filter.setClearButtonEnabled(True)
        filter_layout.addWidget(QLabel("Filtre:"))
        filter_layout.addWidget(self.media_filter)
        
        # Liste des catégories
        self.media_category_list = QListWidget()
        self.media_category_list.setSelectionMode(QListWidget.MultiSelection)
        
        # Liste des médias
        self.media_list = QListWidget()
        self.media_list.setSelectionMode(QListWidget.SingleSelection)
        
        # Layout
        layout.addLayout(filter_layout)
        layout.addWidget(QLabel("Catégories:"))
        layout.addWidget(self.media_category_list)
        layout.addWidget(QLabel("Médias disponibles:"))
        layout.addWidget(self.media_list)
        
        self.media_tab.setLayout(layout)
        self.tabs.addTab(self.media_tab, "Médias")
        
    def setup_groups_tab(self):
        """Configure l'onglet des groupes"""
        self.groups_tab = QWidget()
        layout = QVBoxLayout()
        
        # Filtres
        filter_layout = QHBoxLayout()
        self.group_filter = QLineEdit(placeholderText="Filtrer les groupes...")
        self.group_filter.setClearButtonEnabled(True)
        filter_layout.addWidget(QLabel("Filtre:"))
        filter_layout.addWidget(self.group_filter)
        
        # Liste des catégories
        self.group_category_list = QListWidget()
        self.group_category_list.setSelectionMode(QListWidget.MultiSelection)
        
        # Liste des groupes
        self.group_list = QListWidget()
        self.group_list.setSelectionMode(QListWidget.SingleSelection)
        
        # Layout
        layout.addLayout(filter_layout)
        layout.addWidget(QLabel("Catégories:"))
        layout.addWidget(self.group_category_list)
        layout.addWidget(QLabel("Groupes disponibles:"))
        layout.addWidget(self.group_list)
        
        self.groups_tab.setLayout(layout)
        self.tabs.addTab(self.groups_tab, "Groupes")
        
    def setup_connections(self):
        """Connecte les signaux et slots"""
        # Boutons
        self.send_button.clicked.connect(self.send_to_robot)
        self.send_one_button.clicked.connect(self.send_one_to_robot)
        self.cancel_button.clicked.connect(self.reject)
        
        # Filtres
        self.media_filter.textChanged.connect(self.filter_media)
        self.group_filter.textChanged.connect(self.filter_groups)
        
        # Sélections
        self.media_category_list.itemSelectionChanged.connect(self.load_media_for_categories)
        self.group_category_list.itemSelectionChanged.connect(self.load_groups_for_categories)
        self.media_list.itemSelectionChanged.connect(self.update_current_selection)
        self.group_list.itemSelectionChanged.connect(self.update_current_selection)
        
    def update_current_selection(self):
        """Met à jour la sélection courante"""
        sender = self.sender()
        if sender == self.media_list and sender.currentItem():
            self.current_selection = ("media", sender.currentItem().data(Qt.UserRole))
        elif sender == self.group_list and sender.currentItem():
            self.current_selection = ("group", sender.currentItem().data(Qt.UserRole))
        else:
            self.current_selection = None
            
        # Active/désactive le bouton d'envoi unitaire
        self.send_one_button.setEnabled(self.current_selection is not None)
        
    def load_data_async(self):
        """Charge les données de manière asynchrone"""
        # Afficher un indicateur de chargement
        self.loading_indicator = QLabel("Chargement en cours...")
        self.loading_indicator.setAlignment(Qt.AlignCenter)
        self.tabs.addTab(self.loading_indicator, "Chargement")
        self.tabs.setCurrentIndex(2)
        
        # Simuler un chargement asynchrone
        QTimer.singleShot(500, self.populate_initial_data)
        
    def populate_initial_data(self):
        """Remplit les données initiales"""
        try:
            with DatabaseManager(DB_PATH) as db:
                # Catégories de médias
                media_categories = db.get_media_categories()
                for cat_id, name, desc in media_categories:
                    item = QListWidgetItem(f"{name} - {desc}")
                    item.setData(Qt.UserRole, cat_id)
                    self.media_category_list.addItem(item)
                
                # Catégories de groupes
                group_categories = db.get_group_categories()
                for cat_id, name, desc in group_categories:
                    item = QListWidgetItem(f"{name} - {desc}")
                    item.setData(Qt.UserRole, cat_id)
                    self.group_category_list.addItem(item)
                
            # Retirer l'onglet de chargement
            self.tabs.removeTab(2)
            
        except Exception as e:
            self.show_error("Erreur de chargement", f"Impossible de charger les données: {str(e)}")
            self.reject()
            
    def load_media_for_categories(self):
        """Charge les médias pour les catégories sélectionnées"""
        selected_ids = [item.data(Qt.UserRole) for item in self.media_category_list.selectedItems()]
        if not selected_ids:
            self.media_list.clear()
            return
            
        try:
            with DatabaseManager(DB_PATH) as db:
                medias = db.get_media_by_category(selected_ids)
                self.media_list.clear()
                for media_id, name, desc, path, mtype in medias:
                    item = QListWidgetItem(f"{mtype}: {name}")
                    item.setData(Qt.UserRole, media_id)
                    item.setToolTip(desc)
                    self.media_list.addItem(item)
                    
        except Exception as e:
            self.show_error("Erreur", f"Impossible de charger les médias: {str(e)}")
            
    def load_groups_for_categories(self):
        """Charge les groupes pour les catégories sélectionnées"""
        selected_ids = [item.data(Qt.UserRole) for item in self.group_category_list.selectedItems()]
        if not selected_ids:
            self.group_list.clear()
            return
            
        try:
            with DatabaseManager(DB_PATH) as db:
                groups = db.get_groups_by_category(selected_ids)
                self.group_list.clear()
                for group_id, link, remarks, desc, keywords in groups:
                    item = QListWidgetItem(f"{link} - {remarks}")
                    item.setData(Qt.UserRole, group_id)
                    item.setToolTip(f"{desc}\nMots-clés: {keywords}")
                    self.group_list.addItem(item)
                    
        except Exception as e:
            self.show_error("Erreur", f"Impossible de charger les groupes: {str(e)}")
            
    def filter_media(self, text):
        """Filtre la liste des médias"""
        for i in range(self.media_list.count()):
            item = self.media_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())
            
    def filter_groups(self, text):
        """Filtre la liste des groupes"""
        for i in range(self.group_list.count()):
            item = self.group_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())
            
    def validate_selection(self):
        """Valide qu'il y a une sélection"""
        if not any([self.media_category_list.selectedItems(), self.group_category_list.selectedItems()]):
            self.show_warning("Sélection requise", 
                             "Veuillez sélectionner au moins une catégorie de médias ou de groupes.")
            return False
        return True
        
    def send_to_robot(self):
        """Envoie les sélections au robot"""
        if not self.validate_selection():
            return
            
        # Préparer les données
        media_ids = [item.data(Qt.UserRole) for item in self.media_category_list.selectedItems()]
        group_ids = [item.data(Qt.UserRole) for item in self.group_category_list.selectedItems()]
        
        try:
            with DatabaseManager(DB_PATH) as db:
                media_data = db.get_media_by_category(media_ids) if media_ids else []
                group_data = db.get_groups_by_category(group_ids) if group_ids else []
                
                data = {
                    "posts": [{
                        "id": m[0],
                        "name": m[1],
                        "description": m[2],
                        "path": m[3],
                        "type": m[4]
                    } for m in media_data],
                    "groups": [{
                        "id": g[0],
                        "link": g[1],
                        "remarks": g[2],
                        "description": g[3],
                        "keywords": g[4]
                    } for g in group_data]
                }
                
                # Démarrer l'envoi en arrière-plan
                self.start_send_process(data, is_bulk=True)
                
        except Exception as e:
            self.show_error("Erreur d'envoi", f"Échec de la préparation des données: {str(e)}")
            
    def send_one_to_robot(self):
        """Envoie un seul élément sélectionné au robot"""
        if not self.current_selection:
            return
            
        item_type, item_id = self.current_selection
        
        try:
            with DatabaseManager(DB_PATH) as db:
                if item_type == "media":
                    media = db.get_single_media(item_id)
                    if not media:
                        self.show_warning("Introuvable", "Le média sélectionné n'existe plus.")
                        return
                        
                    data = {
                        "posts": [{
                            "id": media[0],
                            "name": media[1],
                            "description": media[2],
                            "path": media[3],
                            "type": media[4]
                        }],
                        "groups": []
                    }
                else:
                    group = db.get_single_group(item_id)
                    if not group:
                        self.show_warning("Introuvable", "Le groupe sélectionné n'existe plus.")
                        return
                        
                    data = {
                        "posts": [],
                        "groups": [{
                            "id": group[0],
                            "link": group[1],
                            "remarks": group[2],
                            "description": group[3],
                            "keywords": group[4]
                        }]
                    }
                
                # Démarrer l'envoi en arrière-plan
                self.start_send_process(data, is_bulk=False)
                
        except Exception as e:
            self.show_error("Erreur d'envoi", f"Échec de la préparation des données: {str(e)}")
            
    def start_send_process(self, data, is_bulk=True):
        """Démarre le processus d'envoi avec une progress bar"""
        self.progress = QProgressDialog(
            "Envoi en cours...", 
            "Annuler", 
            0, 
            100, 
            self
        )
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setAutoClose(True)
        
        # Créer et démarrer le worker
        self.worker = SendWorker(data, is_bulk)
        self.worker.progress_updated.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_send_finished)
        self.progress.canceled.connect(self.worker.terminate)
        self.worker.start()
        
    def on_send_finished(self, success, message):
        """Gère la fin de l'envoi"""
        self.progress.close()
        
        if success:
            self.show_success("Succès", message)
            self.accept()
        else:
            self.show_error("Échec", message)
            
    def show_success(self, title, message):
        """Affiche un message de succès"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    def show_warning(self, title, message):
        """Affiche un avertissement"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    def show_error(self, title, message):
        """Affiche une erreur"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

# # Exemple d'utilisation
# if __name__ == "__main__":
#     import sys
#     from PyQt5.QtWidgets import QApplication
    
#     app = QApplication(sys.argv)
#     dialog = UpdateRobotDialog()
#     dialog.show()
#     sys.exit(app.exec_())
class UpdateRobotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Envoyer au Robot")
        self.setWindowIcon(QIcon("icons/update.png"))  # Ajouter une icône
        self.setFixedSize(500, 400)  # Taille fixe pour une meilleure apparence

        # Connexion à la base de données
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        # Vérifier si les tables existent
        self.check_tables()

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 12px;
                border: 1px solid #ddd;
            }
            QPushButton {
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #007BFF, stop:1 #0056b3);
                color: white;
                margin: 8px;
                border: none;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0056b3, stop:1 #003f8a);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #003f8a, stop:1 #002b60);
                box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
            }
            QPushButton:focus {
                outline: none;
            }
            QListWidget {
                font-size: 14px;
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 6px;
                background-color: white;
            }
            QLabel {
                font-size: 14px;
                color: #444;
                margin-bottom: 8px;
            }
        """)

        # Layout
        layout = QVBoxLayout()

        # Sélection des catégories de médias
        self.media_category_label = QLabel("Sélectionnez une ou plusieurs catégories de médias:")
        layout.addWidget(self.media_category_label)

        self.media_category_list = QListWidget()
        self.media_category_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_media_categories()
        layout.addWidget(self.media_category_list)

        # Sélection des catégories de groupes
        self.group_category_label = QLabel("Sélectionnez une ou plusieurs catégories de groupes:")
        layout.addWidget(self.group_category_label)

        self.group_category_list = QListWidget()
        self.group_category_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_group_categories()
        layout.addWidget(self.group_category_list)

        # Bouton pour envoyer au robot
        self.send_button = QPushButton("Envoyer au Robot", self)
        self.send_button.setIcon(QIcon("icons/robot.png"))  # Ajouter une icône
        self.send_button.clicked.connect(self.send_to_robot)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def check_tables(self):
        """Vérifie si les tables nécessaires existent dans la base de données."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                label TEXT,
                description TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP,
                date_suppression TIMESTAMP
            )
        """)
        self.conn.commit()

    def load_media_categories(self):
        """Charge les catégories de médias depuis la base de données."""
        self.cursor.execute("SELECT id, name FROM category")
        media_categories = self.cursor.fetchall()
        for category in media_categories:
            item = QListWidgetItem(category[1])
            item.setData(Qt.UserRole, category[0])  # Stocker l'ID de la catégorie
            self.media_category_list.addItem(item)

    def load_group_categories(self):
        """Charge les catégories de groupes depuis la base de données."""
        self.cursor.execute("SELECT id, name FROM category")
        group_categories = self.cursor.fetchall()
        for category in group_categories:
            item = QListWidgetItem(category[1])
            item.setData(Qt.UserRole, category[0])  # Stocker l'ID de la catégorie
            self.group_category_list.addItem(item)

    def send_to_robot(self):
        """Envoie les données sélectionnées au robot."""
        selected_media_categories = [
            item.data(Qt.UserRole) for item in self.media_category_list.selectedItems()
        ]
        selected_group_categories = [
            item.data(Qt.UserRole) for item in self.group_category_list.selectedItems()
        ]

        if not selected_media_categories and not selected_group_categories:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner au moins une catégorie de médias ou de groupes.")
            return

        # Récupérer les données de la base de données
        media_data = self.get_media_data(selected_media_categories)
        group_data = self.get_group_data(selected_group_categories)

        # Envoyer les données au robot
        self.send_data_to_robot(media_data, group_data)

        QMessageBox.information(self, "Succès", "Les données ont été envoyées au robot avec succès.")
        self.accept()

    def get_media_data(self, category_ids):
        """Récupère les données des médias pour les catégories sélectionnées."""
        query = """
            SELECT m.id, m.nom, m.description, m.preview_path, mt.type
            FROM media m
            JOIN media_type mt ON m.type_id = mt.id
            WHERE m.category_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        self.cursor.execute(query, category_ids)
        return self.cursor.fetchall()

    def get_group_data(self, category_ids):
        """Récupère les données des groupes pour les catégories sélectionnées."""
        query = """
            SELECT g.id, g.link, g.remarks, g.description, g.keywords
            FROM groups g
            WHERE g.category_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        self.cursor.execute(query, category_ids)
        return self.cursor.fetchall()

    def send_data_to_robot(self, media_data, group_data):
        """
        Envoie les données sélectionnées au robot en utilisant FileTransferApp et FileTransferApp2.
        
        Args:
            media_data (list): Liste des données de médias sélectionnées.
            group_data (list): Liste des données de groupes sélectionnées.
        """
        # Organiser les données dans un format structuré
        combined_content = {
            "posts": [],
            "groups": []
        }

        # Ajouter les données de médias
        for media in media_data:
            combined_content["posts"].append({
                "text": media[1],  # Nom du média
                "image": media[3]  # Chemin de l'image
            })

        # Ajouter les données de groupes
        for group in group_data:
            combined_content["groups"].append({
                "link": group[1],  # Lien du groupe
                "remarks": group[2],  # Remarques
                "description": group[3],  # Description
                "keywords": group[4]  # Mots-clés
            })

        # Créer une instance de FileTransferApp pour envoyer les données
        transfer_app = FileTransferApp()
        transfer_app.start_process(combined_content)  # Envoyer les données combinées

        # Créer une instance de FileTransferApp2 pour envoyer les images
        transfer_app2 = FileTransferApp2()
        transfer_app2.start_process(combined_content)  # Envoyer les images

    def closeEvent(self, event):
        """Ferme la connexion à la base de données lors de la fermeture de la fenêtre."""
        self.conn.close()
        event.accept()


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QAbstractItemView, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QIcon

class ManageCategoriesDialog(QDialog):
    def __init__(self, media_manager, parent=None):
        super().__init__(parent)
        self.media_manager = media_manager
        self.setWindowTitle("Gérer les catégories")
        self.setWindowIcon(QIcon("icons/category.png"))  # Ajouter une icône
        self.setFixedSize(600, 400)  # Taille fixe pour une meilleure apparence

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #007BFF;
                color: white;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 6px;
                background-color: #007BFF;
                color: white;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
        """)

        # Layout
        layout = QVBoxLayout()

        # Tableau des catégories
        self.category_list = QTableWidget(self)
        self.category_list.setColumnCount(4)
        self.category_list.setHorizontalHeaderLabels(['ID', 'Nom', 'Libellé', 'Description'])
        self.category_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.category_list)

        # Boutons pour ajouter/supprimer
        button_layout = QHBoxLayout()
        self.add_button = QPushButton('Ajouter', self)
        self.add_button.setIcon(QIcon("icons/add.png"))  # Ajouter une icône
        self.add_button.clicked.connect(self.add_category)
        button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton('Supprimer', self)
        self.delete_button.setIcon(QIcon("icons/delete.png"))  # Ajouter une icône
        self.delete_button.clicked.connect(self.delete_category)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.populate_categories()

    def populate_categories(self):
        """Remplit la liste des catégories."""
        categories = self.media_manager.load_categories()
        self.category_list.setRowCount(len(categories))

        for row, category in enumerate(categories):
            id_item = QTableWidgetItem(str(category['id']))
            self.category_list.setItem(row, 0, id_item)

            name_item = QTableWidgetItem(category['name'])
            self.category_list.setItem(row, 1, name_item)

            label_item = QTableWidgetItem(category.get('label', ''))
            self.category_list.setItem(row, 2, label_item)

            description_item = QTableWidgetItem(category.get('description', ''))
            self.category_list.setItem(row, 3, description_item)

    def add_category(self):
        """Ajoute une nouvelle catégorie."""
        dialog = AddCategoryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name, label, description = dialog.get_category_data()
            if name:  # Validation du nom
                self.media_manager.add_category(name, label, description)
                self.populate_categories()
            else:
                QMessageBox.warning(self, 'Erreur', 'Le nom de la catégorie ne peut pas être vide.')

    def delete_category(self):
        """Supprime la catégorie sélectionnée."""
        selected_row = self.category_list.currentRow()
        if selected_row >= 0:
            category_id = int(self.category_list.item(selected_row, 0).text())
            if self.media_manager.has_media_in_category(category_id):
                QMessageBox.warning(self, 'Erreur', 'Cette catégorie contient des médias. Veuillez d\'abord supprimer les médias associés.')
            else:
                confirm = QMessageBox.question(
                    self, 'Confirmer', 'Êtes-vous sûr de vouloir supprimer cette catégorie ?',
                    QMessageBox.Yes | QMessageBox.No
                )
                if confirm == QMessageBox.Yes:
                    self.media_manager.delete_category(category_id)
                    self.populate_categories()

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QMessageBox
from PyQt5.QtGui import QIcon

class AddCategoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter une catégorie")
        self.setWindowIcon(QIcon("icons/add.png"))  # Ajouter une icône
        self.setFixedSize(400, 200)  # Taille fixe pour une meilleure apparence

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-bottom: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #007BFF;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 6px;
                background-color: #007BFF;
                color: white;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
        """)

        # Layout
        layout = QVBoxLayout()

        # Champ de saisie pour le nom
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nom de la catégorie")
        layout.addWidget(self.name_input)

        # Champ de saisie pour le libellé
        self.label_input = QLineEdit(self)
        self.label_input.setPlaceholderText("Libellé de la catégorie")
        layout.addWidget(self.label_input)

        # Champ de saisie pour la description
        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Description de la catégorie")
        layout.addWidget(self.description_input)

        # Boutons Ok et Annuler
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.button(QDialogButtonBox.Ok).setIcon(QIcon("icons/check.png"))  # Icône pour Ok
        button_box.button(QDialogButtonBox.Cancel).setIcon(QIcon("icons/cancel.png"))  # Icône pour Annuler
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def validate_and_accept(self):
        """Valide la saisie avant d'accepter."""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, 'Erreur', 'Le nom de la catégorie ne peut pas être vide.')
            return
        self.accept()

    def get_category_data(self):
        """Retourne les données de la catégorie."""
        return (
            self.name_input.text().strip(),
            self.label_input.text().strip(),
            self.description_input.text().strip()
        )
    
    



from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QAbstractItemView, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QIcon

class ManageTypesDialog(QDialog):
    def __init__(self, media_manager, parent=None):
        super().__init__(parent)
        self.media_manager = media_manager
        self.setWindowTitle("Gérer les types de médias")
        self.setWindowIcon(QIcon("icons/types.png"))  # Ajouter une icône
        self.setFixedSize(800, 500)  # Taille fixe pour une meilleure apparence

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #007BFF;
                color: white;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 6px;
                background-color: #007BFF;
                color: white;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
        """)

        # Layout
        layout = QVBoxLayout()

        # Tableau des types de médias
        self.type_list = QTableWidget(self)
        self.type_list.setColumnCount(4)
        self.type_list.setHorizontalHeaderLabels(['ID', 'Type', 'Libellé', 'Description'])
        self.type_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.type_list)

        # Boutons pour ajouter/supprimer
        button_layout = QHBoxLayout()
        self.add_button = QPushButton('Ajouter', self)
        self.add_button.setIcon(QIcon("icons/add.png"))  # Ajouter une icône
        self.add_button.clicked.connect(self.add_type)
        button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton('Supprimer', self)
        self.delete_button.setIcon(QIcon("icons/delete.png"))  # Ajouter une icône
        self.delete_button.clicked.connect(self.delete_type)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.populate_types()

    def populate_types(self):
        """Remplit la liste des types de médias."""
        types = self.media_manager.load_types()
        self.type_list.setRowCount(len(types))

        for row, type_ in enumerate(types):
            id_item = QTableWidgetItem(str(type_['id']))
            self.type_list.setItem(row, 0, id_item)

            type_item = QTableWidgetItem(type_['type'])
            self.type_list.setItem(row, 1, type_item)

            label_item = QTableWidgetItem(type_.get('label', ''))
            self.type_list.setItem(row, 2, label_item)

            description_item = QTableWidgetItem(type_.get('description', ''))
            self.type_list.setItem(row, 3, description_item)

    def add_type(self):
        """Ajoute un nouveau type de média."""
        dialog = AddTypeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            type_, label, description = dialog.get_type_data()
            if type_:  # Validation du type
                self.media_manager.add_type(type_, label, description)
                self.populate_types()
            else:
                QMessageBox.warning(self, 'Erreur', 'Le type de média ne peut pas être vide.')

    def delete_type(self):
        """Supprime le type de média sélectionné."""
        selected_row = self.type_list.currentRow()
        if selected_row >= 0:
            type_id = int(self.type_list.item(selected_row, 0).text())
            if self.media_manager.has_media_in_type(type_id):
                QMessageBox.warning(self, 'Erreur', 'Ce type contient des médias. Veuillez d\'abord supprimer les médias associés.')
            else:
                confirm = QMessageBox.question(
                    self, 'Confirmer', 'Êtes-vous sûr de vouloir supprimer ce type ?',
                    QMessageBox.Yes | QMessageBox.No
                )
                if confirm == QMessageBox.Yes:
                    self.media_manager.delete_type(type_id)
                    self.populate_types()

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QMessageBox
from PyQt5.QtGui import QIcon

class AddTypeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un type de média")
        self.setWindowIcon(QIcon("icons/add.png"))  # Ajouter une icône
        self.setFixedSize(400, 200)  # Taille fixe pour une meilleure apparence

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-bottom: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #007BFF;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 6px;
                background-color: #007BFF;
                color: white;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
        """)

        # Layout
        layout = QVBoxLayout()

        # Champ de saisie pour le type
        self.type_input = QLineEdit(self)
        self.type_input.setPlaceholderText("Type de média")
        layout.addWidget(self.type_input)

        # Champ de saisie pour le libellé
        self.label_input = QLineEdit(self)
        self.label_input.setPlaceholderText("Libellé du type")
        layout.addWidget(self.label_input)

        # Champ de saisie pour la description
        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Description du type")
        layout.addWidget(self.description_input)

        # Boutons Ok et Annuler
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.button(QDialogButtonBox.Ok).setIcon(QIcon("icons/check.png"))  # Icône pour Ok
        button_box.button(QDialogButtonBox.Cancel).setIcon(QIcon("icons/cancel.png"))  # Icône pour Annuler
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def validate_and_accept(self):
        """Valide la saisie avant d'accepter."""
        type_ = self.type_input.text().strip()
        if not type_:
            QMessageBox.warning(self, 'Erreur', 'Le type de média ne peut pas être vide.')
            return
        self.accept()

    def get_type_data(self):
        """Retourne les données saisies par l'utilisateur."""
        return (
            self.type_input.text().strip(),
            self.label_input.text().strip(),
            self.description_input.text().strip()
        )


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QAbstractItemView, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QIcon

class ManageArchivesDialog(QDialog):
    def __init__(self, media_manager, user_choice, parent=None):
        super().__init__(parent)
        self.media_manager = media_manager
        self.user_choice = user_choice
        self.setWindowTitle("Gérer les archives")
        self.setWindowIcon(QIcon("icons/archive.png"))  # Ajouter une icône
        self.setFixedSize(800, 500)  # Taille fixe pour une meilleure apparence

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #007BFF;
                color: white;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 6px;
                background-color: #007BFF;
                color: white;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
        """)

        # Layout
        layout = QVBoxLayout()

        # Tableau des archives
        self.archive_list = QTableWidget(self)
        self.archive_list.setColumnCount(4)
        self.archive_list.setHorizontalHeaderLabels(['ID', 'Nom', 'Description', 'Catégorie'])
        self.archive_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.archive_list)

        # Boutons pour restaurer/supprimer
        button_layout = QHBoxLayout()
        self.restore_button = QPushButton('Restaurer', self)
        self.restore_button.setIcon(QIcon("icons/restore.png"))  # Ajouter une icône
        self.restore_button.clicked.connect(self.restore_media)
        button_layout.addWidget(self.restore_button)

        self.delete_button = QPushButton('Supprimer définitivement', self)
        self.delete_button.setIcon(QIcon("icons/delete.png"))  # Ajouter une icône
        self.delete_button.clicked.connect(self.delete_media)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.populate_archives()

    def populate_archives(self):
        """Remplit la liste des archives."""
        archives = self.media_manager.load_archives(self.user_choice)
        self.archive_list.setRowCount(len(archives))

        for row, archive in enumerate(archives):
            id_item = QTableWidgetItem(str(archive['id']))
            self.archive_list.setItem(row, 0, id_item)

            nom_item = QTableWidgetItem(archive['nom'])
            self.archive_list.setItem(row, 1, nom_item)

            description_item = QTableWidgetItem(archive['description'])
            self.archive_list.setItem(row, 2, description_item)

            categorie_item = QTableWidgetItem(archive.get('categorie', ''))
            self.archive_list.setItem(row, 3, categorie_item)

    def restore_media(self):
        """Restaure le média sélectionné."""
        selected_row = self.archive_list.currentRow()
        if selected_row >= 0:
            media_id = int(self.archive_list.item(selected_row, 0).text())
            self.media_manager.restore_media(media_id, self.user_choice)
            self.populate_archives()

    def delete_media(self):
        """Supprime définitivement le média sélectionné."""
        selected_row = self.archive_list.currentRow()
        if selected_row >= 0:
            media_id = int(self.archive_list.item(selected_row, 0).text())
            # confirm = QMessageBox.question(
            #     self, 'Confirmation', "Êtes-vous sûr de vouloir supprimer définitivement ce média ?",
            #     QMessageBox.Yes | QMessageBox.No
            # )
            # if confirm == QMessageBox.Yes:
            self.media_manager.delete_media(media_id)
            self.populate_archives()


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

class PreviewDialog(QDialog):
    def __init__(self, media_path, description, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aperçu du média")
        self.setWindowIcon(QIcon("icons/preview.png"))  # Ajouter une icône
        self.setFixedSize(500, 500)  # Taille fixe pour une meilleure apparence

        # Styles CSS modernes
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
                color: #333;
                margin-bottom: 10px;
            }
        """)

        # Layout
        layout = QVBoxLayout()

        # Description du média
        self.description_label = QLabel(description, self)
        self.description_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.description_label)

        # Aperçu du média
        if media_path.endswith(('.png', '.jpg', '.jpeg')):
            self.preview_label = QLabel(self)
            pixmap = QPixmap(media_path).scaled(400, 400, Qt.KeepAspectRatio)
            self.preview_label.setPixmap(pixmap)
            self.preview_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.preview_label)
        else:
            self.preview_label = QLabel("Aperçu vidéo non disponible.", self)
            self.preview_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.preview_label)

        self.setLayout(layout)


# Application principale
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de médias")
        self.setGeometry(100, 100, 800, 600)
        self.setCentralWidget(MediaTable(self))

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()