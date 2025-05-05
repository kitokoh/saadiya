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
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QPropertyAnimation
import time
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtCore import QTime

from ui.header import HeaderSection
from ui.footer import FooterSection
# Chemin de la base de données
# DB_PATH = os.path.join(user_data_dir, 'groups22.db')
from PyQt5.QtWidgets import QTextEdit

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

# Classe pour gérer les médias
class MediaManager:
    def __init__(self, DB_PATH):
        self.DB_PATH = DB_PATH
        self.create_database()

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

    def load_media_from_db(self, user_choice):
        """Charge les médias depuis la base de données."""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT media.id, media.nom, media.description, media.preview_path, category.name 
            FROM media 
            LEFT JOIN category ON media.category_id = category.id
            WHERE media.type_id = (SELECT id FROM media_type WHERE type = ?) AND media.est_supprime = 0
        ''', (user_choice,))

        media_list = [
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
        return media_list

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
from PyQt5.QtWidgets import QToolButton
from facebooksmodule.notemedia import MediaEditorModal


class MediaTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_choice = self.load_user_choice()  # Load user choice
        self.media_manager = MediaManager(DB_PATH)
        self.media_list = self.media_manager.load_media_from_db(self.user_choice)
        self.page_size = 10
        self.current_page = 0
        self.total_pages = 0
        # Couleurs modernes
        self.primary_color = "#3498db"
        self.secondary_color = "#2ecc71"
        self.dark_color = "#2c3e50"
        self.light_color = "#ecf0f1"
        self.accent_color = "#e74c3c"
        # Initialize UI
        self.init_ui()
        self.media_editor = MediaEditorModal(self)

    def toggle_modal(self):
        """Fonction à connecter au bouton pour ouvrir/fermer le modal avec animation"""
        if not hasattr(self, '_modal'):
            # Création du modal seulement au premier appel
            self._modal = ElegantModal(self)
            # Positionnement initial caché
            self._modal.hide()
        
        if self._modal.isVisible():
            # Fermer avec animation
            self._modal.hide_modal()
            # Changer l'icône/text du bouton si nécessaire
            self.robot_note_action.setText("Ouvrir le Modal")
        else:
            # Ouvrir avec animation
            self._modal.show_modal(self.robot_note_action)
            # Changer l'icône/text du bouton si nécessaire
            self.robot_note_action.setText("Fermer le Modal")
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
    def open_premium_modal(self):
        """Fonction appelée quand on clique sur le bouton"""
        
        # Création et configuration du modal
        self.modal = WorkingPremiumModal(parent=self)
        self.modal.set_title("Éditeur Premium")
        
        # Personnalisation du contenu (exemple)
        content = QLabel("Contenu personnalisé du modal...")
        self.modal.set_content(content)
        
        # Optionnel: personnaliser le bouton d'action
        self.modal.set_action_text("Fermer")
        self.modal.set_action_callback(self.on_modal_close)
        
        # Afficher le modal
        self.modal.show()
    
    def on_modal_close(self):
        """Callback quand on ferme le modal"""
        print("Modal fermé")  
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

    def init_uii(self):
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
        # Activer l'édition


        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.table.cellChanged.connect(self.on_cell_changed)
        
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
        
    def iinit_ui(self):
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


        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.table.cellChanged.connect(self.on_cell_changed)



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
        # menu.addAction(import_media_action)
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






        self.robot_note_action = QAction("📋 " + self.tr("Notes"), self)
        self.robot_note_action.triggered.connect(self.show_media_editor)
        menu.addAction(self.robot_note_action)
      
        return menu

    def show_media_editor(self):
        """Affiche l'éditeur de médias"""
        self.media_editor.show_modal()
    
    # Exemple d'accès aux données
    def get_current_prompt(self):
        return self.media_editor.get_prompt()
    
    def get_current_descriptions(self):
        return self.media_editor.get_media_descriptions()
    def default_desc(self):
        return self.media_editor.get_default_description()
    def open_add_media_dialog(self):
        """Open a dialog to add a new media."""
        dialog = AddMediaDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            media_data = dialog.get_media_data()  # Assurez-vous que cette méthode existe dans AddMediaDialog
            self.media_manager.add_media_to_db(media_data, self.user_choice)
            self.populate_table()


    def populate_table2(self):
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
        # file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg);;Vidéos (*.mp4 *.mov)")
        file_dialog.setNameFilter("Médias (*.png *.jpg *.jpeg *.mp4 *.mov)")

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
    def import_description(self):
        """Importe des descriptions et les applique dans l'ordre aux médias existants."""
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Sélectionner un fichier JSON")
        file_dialog.setNameFilter("JSON files (*.json)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            with open(selected_file, 'r', encoding='utf-8') as f:
                descriptions = json.load(f)

                # Connexion à la base pour obtenir les IDs des médias existants (triés)
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM media ORDER BY id ASC")
                media_ids = [row[0] for row in cursor.fetchall()]
                conn.close()

                # Appliquer les descriptions dans l'ordre
                for media_id, description in zip(media_ids, descriptions):
                    self.update_media_description(media_id, description)

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
        desc = self.default_desc()  # Récupère et stocke la description

        # Copier le fichier dans le dossier média
        shutil.copy(file_path, destination_path)

        # Créer un nouvel objet média
        new_media = {
            'nom': new_name,
            'description': desc,
            'preview_path': destination_path,
            'categorie': 'Default'
        }

        # Ajouter le média à la base de données
        self.media_manager.add_media_to_db(new_media, self.user_choice)
        self.populate_table()

    def update_media_description(self, media_id, description):
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


    def delete_media(self, media):
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
    def delete_all_media(self):
        """Supprime tous les médias sans confirmation, avec une barre de progression."""
        total = len(self.media_list)
        if total == 0:
            return  # Rien à supprimer

        progress = QProgressDialog("Suppression de tous les médias...", None, 0, total, self)
        progress.setWindowTitle("Veuillez patienter")
        progress.setWindowModality(Qt.ApplicationModal)
        progress.setCancelButton(None)
        progress.setMinimumDuration(0)
        progress.show()

        for i, media in enumerate(self.media_list):
            self.delete_mediamuet(media)
            progress.setValue(i + 1)
            QApplication.processEvents()

        progress.close()
        self.media_list = self.media_manager.load_media_from_db(self.user_choice)
        self.populate_table()


    def delete_mediamuet(self, media):
        """Supprime un média sans confirmation, avec une indication visuelle de progression."""
        progress = QProgressDialog("Suppression en cours...", None, 0, 0, self)
        progress.setWindowTitle("Veuillez patienter")
        progress.setCancelButton(None)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        QApplication.processEvents()

        try:
            # Déplacement vers le dossier d'archive
            archive_folder = os.path.join(media_folder, f"{self.user_choice}Archive")
            os.makedirs(archive_folder, exist_ok=True)

            # Génération du nom d'archive
            archive_files = [f for f in os.listdir(archive_folder) if f.startswith('archive')]
            archive_number = len(archive_files) + 1
            archive_name = f"archive{archive_number}{os.path.splitext(media['nom'])[1]}"
            archive_path = os.path.join(archive_folder, archive_name)

            # Déplacement du fichier et suppression de la base de données
            shutil.move(media['preview_path'], archive_path)
            self.media_manager.delete_media_in_db(media, self.user_choice)

        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")  # Optionnel : logging ou message d'erreur
        finally:
            progress.close()
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

    def prev_page(self):
        """Navigue vers la page précédente."""
        if self.current_page > 0:
            self.current_page -= 1
            self.populate_table()

    def next_page(self):
        """Navigue vers la page suivante."""
        if (self.current_page + 1) * self.page_size < len(self.media_list):
            self.current_page += 1
            self.populate_table()

    def on_cell_changed(self, row, column):
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



    def populate_table(self):
        """Remplit le tableau avec un style amélioré et les nouvelles fonctionnalités"""
        self.table.setRowCount(len(self.media_list))
        
        for row, media in enumerate(self.media_list):
            # Colonne Nom
            name_item = QTableWidgetItem(media['nom'])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, name_item)


            # Colonne Description avec éditeur enrichi
            desc_item = QTableWidgetItem(media['description'])
            desc_item.setFont(QFont("Segoe UI", 10))
            desc_item.setFlags(desc_item.flags() | Qt.ItemIsEditable)
            
            self.table.setItem(row, 1, desc_item)

            # Colonne Catégorie
            category_combo = QComboBox()
            categories = self.media_manager.load_categories()
            for category in categories:
                category_combo.addItem(category['name'])
            category_combo.setCurrentText(media.get('categorie', 'Default'))
            category_combo.currentTextChanged.connect(lambda text, row=row: self.update_category(row, text))
            self.table.setCellWidget(row, 2, category_combo)

            # # Colonne Aperçu (chargement paresseux)
            # preview_label = QLabel()
            # preview_label.setAlignment(Qt.AlignCenter)
            
            # if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
            #     # On crée un QLabel vide et on stocke le chemin pour chargement ultérieur
            #     preview_label.setProperty("image_path", media['preview_path'])
            #     preview_label.setText("(Chargement...)")
            # elif media['nom'].endswith(('.mp4', '.mov')):
            #     preview_label.setText("🎥 Voir")
                
            # preview_label.mousePressEvent = lambda event, path=media['preview_path']: self.show_preview(path)
            # self.table.setCellWidget(row, 3, preview_label)
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



            # # Colonne Aperçu (avec chargement paresseux + style amélioré)
            # preview_label = QLabel()
            # preview_label.setAlignment(Qt.AlignCenter)

            # if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
            #     image_path = media['preview_path']

            #     # Vérifie si l'image est déjà chargée ou existe en cache
            #     if os.path.exists(image_path):  # tu peux aussi utiliser un cache ici
            #         pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            #         preview_label.setPixmap(pixmap)
            #     else:
            #         preview_label.setText("(Chargement...)")
            #         preview_label.setProperty("image_path", image_path)

            # elif media['nom'].endswith(('.mp4', '.mov')):
            #     preview_label.setText("🎥 Voir")

            # # Dans tous les cas, ajout d'un événement pour afficher l'aperçu au clic
            # preview_label.mousePressEvent = lambda event, path=media['preview_path']: self.show_preview(path)
            # self.table.setCellWidget(row, 3, preview_label)

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
   

        # Configurer le chargement paresseux
        self.table.verticalScrollBar().valueChanged.connect(self.lazy_load_images)
        # Charger les images visibles initialement
        QTimer.singleShot(100, self.lazy_load_images)
        
        # Ajustement automatique des hauteurs de ligne
        self.table.resizeRowsToContents()
        self.table.model().dataChanged.connect(lambda: self.table.resizeRowsToContents())


            # Configurer le delegate pour la colonne Description
        # Ajuster automatiquement la hauteur des lignes
        # self.table.resizeRowsToContents()
        
        # # Connecter le signal pour redimensionner après édition
        # self.table.model().dataChanged.connect(lambda: self.table.resizeRowsToContents())
        # #self.table.setItemDelegateForColumn(1, RichTextDelegate(self.table))

   
        # Ajuster automatiquement la hauteur des lignes


    def populate_tablex(self):
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
            # preview_label = QLabel()
            # preview_label.setAlignment(Qt.AlignCenter)
            # if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
            #     pixmap = QPixmap(media['preview_path']).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            #     preview_label.setPixmap(pixmap)
            # elif media['nom'].endswith(('.mp4', '.mov')):
            #     preview_label.setText("🎥 Voir")
            #     preview_label.mousePressEvent = lambda event, path=media['preview_path']: self.show_preview(path)
            #     self.table.setCellWidget(row, 3, preview_label)
            import subprocess
            from PyQt5.QtCore import Qt
            from PyQt5.QtGui import QPixmap, QImage
            from PyQt5.QtWidgets import QLabel
            from io import BytesIO

            def extract_thumbnail_from_video(video_path):
                # Utiliser ffmpeg pour extraire une image en mémoire
                process = subprocess.Popen(
                    ['ffmpeg', '-i', video_path, '-ss', '00:00:01', '-vframes', '1', '-f', 'image2pipe', '-'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                # Lire l'image extraite depuis la sortie standard de ffmpeg
                image_data, _ = process.communicate()
                
                # Charger l'image directement depuis les données binaires
                image = QImage.fromData(image_data)
                
                # Convertir l'image en pixmap pour l'affichage dans la QLabel
                pixmap = QPixmap(image)
                
                return pixmap

            # Colonne Aperçu
            preview_label = QLabel()
            preview_label.setAlignment(Qt.AlignCenter)

            if media['nom'].endswith(('.png', '.jpg', '.jpeg')):  # Si c'est une image
                pixmap = QPixmap(media['preview_path']).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                preview_label.setPixmap(pixmap)
            elif media['nom'].endswith(('.mp4', '.mov')):  # Si c'est une vidéo
                # Extraire la miniature de la vidéo en live (sans fichier temporaire)
                pixmap = extract_thumbnail_from_video(media['preview_path'])
                pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                preview_label.setPixmap(pixmap)

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
    def populate_tablex(self):
        """Remplit le tableau avec un style amélioré et fonctionnalités complètes"""
        self.table.setRowCount(len(self.media_list))
        categories = self.media_manager.load_categories()

        for row, media in enumerate(self.media_list):
            # ID caché
            id_item = QTableWidgetItem(str(media.get('id', '')))
            id_item.setData(Qt.UserRole, media.get('id', ''))
            id_item.setFlags(Qt.NoItemFlags)
            self.table.setItem(row, 0, id_item)

            # Nom
            name_item = QTableWidgetItem(media['nom'])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, name_item)

            # Description enrichie
            desc_item = QTableWidgetItem(media['description'])
            desc_item.setFont(QFont("Segoe UI", 10))
            desc_item.setFlags(desc_item.flags() | Qt.ItemIsEditable)
            self.table.setItem(row, 2, desc_item)

            # Catégorie
            category_combo = QComboBox()
            for category in categories:
                category_combo.addItem(category['name'])
            category_combo.setCurrentText(media.get('categorie', 'Default'))
            category_combo.currentTextChanged.connect(lambda text, row=row: self.update_category(row, text))
            self.table.setCellWidget(row, 3, category_combo)

            # Aperçu
            preview_label = QLabel()
            preview_label.setAlignment(Qt.AlignCenter)
            file_name = media['nom']
            preview_path = media.get('preview_path', '')

            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                pixmap = QPixmap(preview_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                preview_label.setPixmap(pixmap)
            elif file_name.lower().endswith(('.mp4', '.mov')):
                preview_label.setText("🎥 Voir")

            preview_label.mousePressEvent = lambda event, path=preview_path: self.show_preview(path)
            self.table.setCellWidget(row, 4, preview_label)

            # Actions
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 0, 5, 0)
            action_layout.setSpacing(5)

            def create_button(icon_path, tooltip, bg_color, hover_color, callback):
                btn = QPushButton()
                btn.setIcon(QIcon(icon_path))
                btn.setToolTip(tooltip)
                btn.setCursor(Qt.PointingHandCursor)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {bg_color};
                        border: none;
                        border-radius: 4px;
                        padding: 5px;
                    }}
                    QPushButton:hover {{
                        background-color: {hover_color};
                    }}
                """)
                btn.clicked.connect(callback)
                return btn

            schedule_btn = create_button("icons/calendar.png", "Planifier la publication", "#9b59b6", "#8e44ad", lambda _, m=media: self.schedule_publication(m))
            robot_btn = create_button("icons/robot.png", "Envoyer au robot", "#3498db", "#2980b9", lambda _, m=media: self.send_to_robot(m))
            delete_btn = create_button("icons/delete.png", "Supprimer", "#e74c3c", "#c0392b", lambda _, m=media: self.delete_media(m))

            action_layout.addWidget(schedule_btn)
            action_layout.addWidget(robot_btn)
            action_layout.addWidget(delete_btn)

            self.table.setCellWidget(row, 5, action_widget)

        # Déléguer la description à un éditeur enrichi
        self.table.setItemDelegateForColumn(2, RichTextDelegate(self.table))  # ou un autre delegate si tu préfères

        # Ajuster automatiquement la hauteur
        self.table.resizeRowsToContents()
        self.table.model().dataChanged.connect(lambda: self.table.resizeRowsToContents())


    def schedule_publication(self, media):
        """Ouvre un modal de planification avec calendrier et sélecteur de temps"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Planifier la publication")
        dialog.setFixedSize(450, 350)
        
        layout = QVBoxLayout(dialog)
        
        # Calendrier
        calendar = QCalendarWidget()
        calendar.setMinimumDate(QDate.currentDate())
        calendar.setStyleSheet("""
            QCalendarWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            QCalendarWidget QToolButton {
                height: 30px;
                font-size: 14px;
            }
        """)
        layout.addWidget(calendar)
        
        # Sélecteur de temps
        time_group = QGroupBox("Heure de publication")
        time_layout = QHBoxLayout(time_group)
        
        time_edit = QDateTimeEdit()
        time_edit.setDisplayFormat("HH:mm")
        time_edit.setTime(QTime(12, 0))  # Défaut: 12:00
        time_edit.setStyleSheet("""
            QDateTimeEdit {
                padding: 8px;
                font-size: 14px;
                border-radius: 4px;
                border: 1px solid #ccc;
            }
        """)
        
        time_layout.addWidget(QLabel("Heure:"))
        time_layout.addWidget(time_edit)
        time_layout.addStretch()
        
        layout.addWidget(time_group)
        
        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        if dialog.exec_() == QDialog.Accepted:
            selected_date = calendar.selectedDate()
            selected_time = time_edit.time()
            publish_datetime = QDateTime(selected_date, selected_time)
            
            # Formatage pour l'affichage
            formatted_date = publish_datetime.toString("dddd d MMMM yyyy à HH'h'mm")
            
            # Ici vous devriez enregistrer la date dans votre base de données
            QMessageBox.information(
                self, 
                "Publication planifiée",
                f"Le média sera publié le {formatted_date}"
            )
            
            # Exemple d'enregistrement (à adapter):
            # self.media_manager.schedule_media(media['id'], publish_datetime)    
    
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

    def on_cell_changed2(self, row, column):
        """Gestion de la modification de cellule avec mise à jour UX et base de données."""
        try:
            media = self.media_list[row]

            if column == 1:  # Colonne "Description"
                new_description = self.table.item(row, column).text()

                # Créer un champ de texte riche temporaire
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
                self.table.setCellWidget(row, column, text_edit)
                text_edit.setFocus()

                def finish_edit():
                    final_text = text_edit.toPlainText()
                    self.table.removeCellWidget(row, column)
                    item = QTableWidgetItem(final_text)
                    self.table.setItem(row, column, item)
                    media['description'] = final_text
                    self.media_manager.update_media_in_db(media, self.user_choice)

                text_edit.focusOutEvent = lambda event: finish_edit()

            elif column == 2:  # Colonne "Catégorie"
                new_category = self.table.item(row, column).text()
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()

                cursor.execute("SELECT id FROM category WHERE name = ?", (new_category,))
                result = cursor.fetchone()
                if result:
                    category_id = result[0]
                    cursor.execute("""
                        UPDATE media
                        SET category_id = ?, date_modification = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (category_id, media['id']))
                    conn.commit()
                    media['category_id'] = category_id  # mise à jour locale
                else:
                    QMessageBox.warning(self, "Catégorie introuvable", f"La catégorie '{new_category}' n'existe pas.")
                conn.close()

        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur s'est produite : {str(e)}")

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









        # Header avec dégradé et ombre
        self.header = QWidget()
        self.header.setFixedHeight(120)
        self.header.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.primary_color}, stop:1 {self.secondary_color});
                border-radius: 0;
                padding: 15px;
            }}
        """)
        
        header_layout = QVBoxLayout(self.header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        # Titre avec icône
        title_layout = QHBoxLayout()
        
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("icons/logo.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        self.title_label = QLabel("FBK GROUP MANAGEMENT")
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: 24px;
                font-weight: bold;
                margin-left: 10px;
            }}
        """)
        
        title_layout.addWidget(self.logo_label)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        
        # Sous-titre
        self.subtitle_label = QLabel("Nova360 AI - Marketing Automation Solution")
        self.subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                margin-top: 5px;
                margin-left: 50px;
            }
        """)
        
        header_layout.addLayout(title_layout)
        header_layout.addWidget(self.subtitle_label)
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
        
        # Bouton d'action avec menu déroulant
        self.action_button = self.create_tool_button("⚡ Actions", self.primary_color)
        self.action_button.setMenu(self.create_action_menu())
        
        # Bouton de paramètres
        self.settings_button = self.create_tool_button("⚙️ Paramètres", "#7f8c8d")
        self.settings_button.setMenu(self.create_settings_menu())
        
        # Bouton d'ajout de média
        self.add_media_button = self.create_tool_button("🖼️ Ajouter média", self.secondary_color)
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
    # Activer le word-wrap pour les descriptions
        self.table.setWordWrap(True)
        
        # Adapter la hauteur des lignes au contenu
        self.table.resizeRowsToContents()
        
        # Configurer le header vertical pour plus d'espace
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.verticalHeader().setMinimumSectionSize(40)
            
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
        """)

        # Configuration des colonnes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Description prend plus de place
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)


        
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.table.cellChanged.connect(self.on_cell_changed)
        
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
        
        # Footer minimaliste
        footer = QLabel("© 2023 FBK Group - Tous droits réservés")
        footer.setStyleSheet(f"""
            QLabel {{
                color: {self.dark_color};
                font-size: 12px;
                padding: 15px;
                text-align: center;
            }}
        """)
        layout.addWidget(footer)
        
        self.populate_table()


        # Activer la navigation au clavier
        self.table.setTabKeyNavigation(True)
        
        # Permettre la sélection complète du texte lors de l'édition
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)


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


    def show_preview(self, path):
        """Affiche un aperçu agrandi pour image ou ouvre la vidéo avec le lecteur par défaut"""
        if path.endswith(('.png', '.jpg', '.jpeg')):
            preview = QDialog(self)
            preview.setWindowTitle("Aperçu")
            preview.setWindowModality(Qt.ApplicationModal)

            layout = QVBoxLayout(preview)
            label = QLabel()
            pixmap = QPixmap(path)
            label.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(label)

            close_btn = QPushButton("Fermer")
            close_btn.clicked.connect(preview.close)
            layout.addWidget(close_btn)

            preview.exec_()

        elif path.endswith(('.mp4', '.mov')):
            # Ouvre la vidéo avec le lecteur système par défaut
            if sys.platform.startswith('win'):
                os.startfile(path)
            elif sys.platform.startswith('darwin'):
                subprocess.call(['open', path])
            else:
                subprocess.call(['xdg-open', path])

    def init_ui(self):
        """Initialise l'interface utilisateur avec un design moderne et des améliorations UX"""
        # Appliquer le style global
        self.setStyleSheet(f"""
            /* Styles de base */
            QWidget {{
                background-color: {self.light_color};
                font-family: 'Segoe UI', Arial, sans-serif;
                color: {self.dark_color};
            }}
            
            /* Styles pour les éléments désactivés */
            QWidget:disabled {{
                color: #95a5a6;
            }}
            
            /* Effets de transition pour les interactions */
            QPushButton, QComboBox, QLineEdit {{
                transition: all 0.3s ease;
            }}
        """)

        # Layout principal avec espacement optimisé
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)  # Espacement réduit mais présent pour une meilleure hiérarchie
        
        top_bar = QWidget()
        top_bar.setFixedHeight(70)
        top_bar.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1F2937, stop:1 #4B5563);
                border-bottom: 2px solid #3B82F6;
                border-radius: 12px;
            }}
        """)

        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 10, 20, 10)
        top_layout.setSpacing(15)

        # ---- Logo + Titre (gauche) ----
        logo_title = QWidget()
        logo_layout = QHBoxLayout(logo_title)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(10)

        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("icons/logo.png").scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.title_label = QLabel("📁 FBK GROUP MANAGEMENT")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #E5E7EB;
                font-size: 20px;
                font-weight: 600;
                font-family: "Segoe UI", sans-serif;
            }
        """)

        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(self.title_label)

        # ---- Recherche + Combo (centre) ----
        search_group = QWidget()
        search_layout = QHBoxLayout(search_group)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(0)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("🔍 Rechercher...")
        self.search_field.setStyleSheet("""
            QLineEdit {
                padding: 8px 20px;
                font-size: 14px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-right: none;
                border-radius: 18px 0 0 18px;
                background: rgba(255, 255, 255, 0.05);
                color: #E5E7EB;
            }
            QLineEdit::placeholder {
                color: #9CA3AF;
            }
        """)

        self.instance_combo = QComboBox()
        self.instance_combo.addItems([f"media{i}" for i in range(1, 11)])
        self.instance_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 15px;
                font-size: 14px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-left: none;
                border-radius: 0 18px 18px 0;
                background: rgba(255, 255, 255, 0.05);
                color: #E5E7EB;
            }
            QComboBox QAbstractItemView {
                background: #1F2937;
                color: white;
                selection-background-color: #374151;
            }
        """)

        search_layout.addWidget(self.search_field)
        search_layout.addWidget(self.instance_combo)

        # ---- Boutons (droite) ----
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)

        button_style = """
            QPushButton {
                padding: 8px 18px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 20px;
                border: none;
                color: white;
                font-family: "Segoe UI", sans-serif;
            }
            QPushButton:hover {
                opacity: 0.92;
            }
        """

        self.add_media_button = QPushButton("➕ Ajouter média")
        self.add_media_button.setStyleSheet(button_style + "background: #10B981;")
        self.add_media_button.clicked.connect(self.import_media)

        self.action_button = QPushButton("📋 Actions")
        self.action_button.setStyleSheet(button_style + "background: #3B82F6;")
        self.action_button.setMenu(self.create_action_menu())

        self.settings_button = QPushButton("⚙️ Paramètres")
        self.settings_button.setStyleSheet(button_style + "background: #6B7280;")
        self.settings_button.setMenu(self.create_settings_menu())

        self.update_robot_button = QPushButton("🤖 Envoyer au robot")
        self.update_robot_button.setStyleSheet(button_style + "background: #F59E0B;")
        self.update_robot_button.clicked.connect(self.show_update_modal)

        buttons_layout.addWidget(self.add_media_button)
        buttons_layout.addWidget(self.action_button)
        buttons_layout.addWidget(self.settings_button)
        buttons_layout.addWidget(self.update_robot_button)

        # ---- Intégration finale ----
        top_layout.addWidget(logo_title)
        top_layout.addStretch()
        top_layout.addWidget(search_group)
        top_layout.addStretch()
        top_layout.addWidget(buttons_container)

        layout.addWidget(top_bar)

        # Tableau amélioré
        # ----------------------------
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Nom', 'Description', 'Catégorie', 'Aperçu', 'Actions'])
        
        # Configuration avancée du tableau
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        
        # Hauteur des lignes et polices
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.setFont(QFont('Segoe UI', 10))
        
        # Configuration des colonnes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Nom
        header.setSectionResizeMode(1, QHeaderView.Stretch)          # Description
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) # Catégorie
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # Aperçu
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents) # Actions
        header.setSectionsClickable(True)
        
        # Style amélioré pour le tableau
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border-radius: 0;
                margin: 0;
                border: none;
                alternate-background-color: #f9f9f9;
                selection-background-color: {self.primary_color}20;  /* 20% d'opacité */
                selection-color: {self.dark_color};
            }}
            QHeaderView::section {{
                background-color: {self.primary_color};
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #eee;
            }}
            QTableWidget::item:selected {{
                background-color: {self.primary_color}40;  /* 40% d'opacité */
            }}
            QScrollBar:vertical {{
                width: 12px;
                margin: 0;
                background: transparent;
            }}
            QScrollBar::handle:vertical {{
                background: {self.primary_color};
                min-height: 20px;
                border-radius: 6px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
                background: none;
            }}

                /* Lignes verticales seulement */
    QTableWidget::item {{
        border-right: 1px solid #e0e0e0;  /* Couleur des lignes verticales */
        border-bottom: none;  /* Désactive les lignes horizontales */
    }}
        """)

        # Activer l'édition avec feedback visuel
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.table.cellChanged.connect(self.on_cell_changed)
        
        layout.addWidget(self.table, 1)  # Facteur d'extension 1 pour prendre tout l'espace disponible
        
        # ----------------------------
        # Pagination améliorée
        # ----------------------------
        pagination = QWidget()
        pagination.setStyleSheet("""
            QWidget {
                background-color: white;
                border-top: 1px solid #ddd;
                padding: 10px 15px;
            }
        """)
        
        pagination_layout = QHBoxLayout(pagination)
        pagination_layout.setContentsMargins(0, 0, 0, 0)
        
        # Boutons de pagination avec indicateurs d'état
        self.prev_button = QPushButton("◀ Précédent")
        self.prev_button.setCursor(Qt.PointingHandCursor)
        self.prev_button.setStyleSheet(f"""
            QPushButton {{
                padding: 8px 15px;
                background-color: {self.light_color};
                color: {self.dark_color};
                border: 1px solid #ddd;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #e0e0e0;
            }}
            QPushButton:disabled {{
                background-color: #f5f5f5;
                color: #bdbdbd;
            }}
        """)
        self.prev_button.clicked.connect(self.prev_page)
        
        self.page_label = QLabel("Page 1")
        self.page_label.setStyleSheet(f"""
            QLabel {{
                color: {self.dark_color};
                font-weight: bold;
            }}
        """)
        self.page_label.setAlignment(Qt.AlignCenter)
        
        self.next_button = QPushButton("Suivant ▶")
        self.next_button.setCursor(Qt.PointingHandCursor)
        self.next_button.setStyleSheet(f"""
            QPushButton {{
                padding: 8px 15px;
                background-color: {self.primary_color};
                color: white;
                border: none;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {QColor(self.primary_color).darker(110).name()};
            }}
            QPushButton:disabled {{
                background-color: #b0bec5;
            }}
        """)
        self.next_button.clicked.connect(self.next_page)
        
        # Indicateur d'éléments par page
        self.items_per_page = QComboBox()
        self.items_per_page.addItems(["10", "25", "50", "100"])
        self.items_per_page.setCurrentText("25")
        self.items_per_page.currentTextChanged.connect(self.update_pagination)
        self.items_per_page.setStyleSheet(f"""
            QComboBox {{
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 60px;
            }}
        """)
        
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addStretch()
        pagination_layout.addWidget(QLabel("Éléments par page:"))
        pagination_layout.addWidget(self.items_per_page)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.next_button)
        
        layout.addWidget(pagination)
        
        # Configuration finale
        self.setMinimumSize(1000, 700)  # Taille minimale pour une bonne expérience
        self.populate_table()


    def update_pagination(self):
        """Met à jour la pagination lorsque le nombre d'éléments par page change"""
        self.current_page = 1  # Retour à la première page
        self.page_label.setText(f"Page {self.current_page}")
        self.populate_table()  # Ou self.populate_model() si vous utilisez QTableView

    def init_uiplus(self):
        """Initialise l'interface utilisateur avec un design moderne et des améliorations UX"""
        # Appliquer le style global avec effets de matériel design
        self.setStyleSheet(f"""
            /* Styles de base avec animation fluide */
            QWidget {{
                background-color: {self.light_color};
                font-family: 'Segoe UI', Arial, sans-serif;
                color: {self.dark_color};
            }}
            
            /* Effets de hover et de focus modernes */
            QPushButton, QComboBox, QLineEdit, QTableView {{
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            /* Effets d'ombre pour les éléments flottants */
            .shadow-effect {{
                border-radius: 8px;
                background: white;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }}
            
            /* Style pour les tooltips */
            QToolTip {{
                background-color: {self.dark_color};
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                opacity: 240;
            }}
        """)

        # Layout principal avec espacement optimisé
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)  # Nous gérons les marges individuellement
        
        # ----------------------------
        # Header premium avec effet de verre
        # ----------------------------
        self.header = QWidget()
        self.header.setFixedHeight(80)
        self.header.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.primary_color}, stop:1 {self.secondary_color});
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            }}
        """)
        
        # Effet de flou pour le header (simulé avec un dégradé)
        header_effect = QGraphicsOpacityEffect(self.header)
        header_effect.setOpacity(0.98)
        self.header.setGraphicsEffect(header_effect)
        
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_layout.setSpacing(15)
        
        # Logo et titre avec animation au hover
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(15)
        
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("icons/logo.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignVCenter)
        self.logo_label.setCursor(Qt.PointingHandCursor)
        self.logo_label.setStyleSheet("""
            QLabel:hover {
                transform: rotate(10deg);
            }
        """)
        
        self.title_label = QLabel("FBK GROUP MANAGEMENT")
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: 22px;
                font-weight: 600;
                letter-spacing: 1px;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }}
        """)
        self.title_label.setAlignment(Qt.AlignVCenter)
        
        title_layout.addWidget(self.logo_label)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        
        # Bouton de menu utilisateur avec icône circulaire
        self.user_button = QPushButton()
        self.user_button.setFixedSize(40, 40)
        self.user_button.setStyleSheet(f"""
            QPushButton {{
                border-radius: 20px;
                background-color: white;
                border: 2px solid rgba(255, 255, 255, 0.4);
                padding: 0;
            }}
            QPushButton:hover {{
                border: 2px solid white;
                background-color: {self.accent_color};
            }}
        """)
        user_icon = QLabel(self.user_button)
        user_icon.setPixmap(QPixmap("icons/user.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        user_icon.setAlignment(Qt.AlignCenter)
        user_icon.setGeometry(8, 8, 24, 24)
        
        header_layout.addWidget(title_container)
        header_layout.addStretch()
        header_layout.addWidget(self.user_button)
        
        layout.addWidget(self.header)

        # ----------------------------
        # Barre d'outils premium avec onglets
        # ----------------------------
        toolbar_container = QWidget()
        toolbar_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        
        toolbar_layout = QVBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(0)
        
        # Onglets modernes
        self.tab_bar = QTabWidget()
        self.tab_bar.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                margin: 0;
                padding: 0;
            }}
            QTabBar::tab {{
                background: transparent;
                color: {self.dark_color};
                padding: 12px 20px;
                border: none;
                font-weight: 500;
                font-size: 14px;
            }}
            QTabBar::tab:selected {{
                color: {self.primary_color};
                border-bottom: 3px solid {self.primary_color};
            }}
            QTabBar::tab:hover {{
                background-color: #f5f5f5;
            }}
        """)
        
        # Onglet principal
        main_tab = QWidget()
        self.tab_bar.addTab(main_tab, "📁 Gestion des médias")
        self.tab_bar.addTab(QWidget(), "📊 Statistiques")
        self.tab_bar.addTab(QWidget(), "⚙️ Paramètres avancés")
        
        # Contenu de l'onglet principal
        tab_layout = QHBoxLayout(main_tab)
        tab_layout.setContentsMargins(15, 15, 15, 15)
        tab_layout.setSpacing(15)
        
        # Barre de recherche avec icône intégrée
        search_container = QWidget()
        search_container.setStyleSheet(".shadow-effect;")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(5, 5, 5, 5)
        
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Rechercher des médias...")
        self.search_field.setClearButtonEnabled(True)
        self.search_field.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px 15px;
                font-size: 14px;
                border: none;
                background: transparent;
                min-width: 300px;
            }}
            QLineEdit:focus {{
                border: none;
                outline: none;
            }}
        """)
        self.search_field.textChanged.connect(self.filter_table)
        
        search_button = QPushButton()
        search_button.setIcon(QIcon("icons/search.png"))
        search_button.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                padding: 8px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {self.light_color};
            }}
        """)
        
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(search_button)
        
        # Sélecteur d'instance avec style moderne
        self.instance_combo = QComboBox()
        self.instance_combo.addItems([f"media{i}" for i in range(1, 11)])
        self.instance_combo.setCurrentText(self.user_choice)
        self.instance_combo.setCurrentIndex(0)
        self.instance_combo.currentIndexChanged.connect(self.on_instance_changed)
        self.instance_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 10px 15px;
                font-size: 14px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                min-width: 150px;
            }}
            QComboBox:hover {{
                border: 1px solid {self.primary_color};
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: none;
            }}
            QComboBox::down-arrow {{
                image: url(icons/arrow-down.png);
                width: 14px;
                height: 14px;
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid #e0e0e0;
                selection-background-color: {self.primary_color};
                selection-color: white;
                padding: 8px;
            }}
        """)
        
        # Boutons d'action avec effets matériels
        button_style = """
            QPushButton {{
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 8px;
                border: none;
                color: white;
                background-color: {0};
                min-width: 140px;
                transition: all 0.2s;
            }}
            QPushButton:hover {{
                background-color: {1};
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                transform: translateY(0);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            QPushButton::menu-indicator {{
                image: none;
            }}
        """
        
        self.add_media_button = QPushButton("Ajouter média")
        self.add_media_button.setIcon(QIcon("icons/add.png"))
        self.add_media_button.setStyleSheet(button_style.format(
            self.secondary_color, 
            QColor(self.secondary_color).darker(110).name()
        ))
        self.add_media_button.clicked.connect(self.import_media)
        
        self.action_button = QPushButton("Actions")
        self.action_button.setIcon(QIcon("icons/actions.png"))
        self.action_button.setStyleSheet(button_style.format(
            self.primary_color,
            QColor(self.primary_color).darker(110).name()
        ))
        self.action_button.setMenu(self.create_action_menu())
        
        self.settings_button = QPushButton("Paramètres")
        self.settings_button.setIcon(QIcon("icons/settings.png"))
        self.settings_button.setStyleSheet(button_style.format(
            "#7f8c8d",
            QColor("#7f8c8d").darker(110).name()
        ))
        self.settings_button.setMenu(self.create_settings_menu())
        
        self.update_robot_button = QPushButton("Envoyer au robot")
        self.update_robot_button.setIcon(QIcon("icons/robot.png"))
        self.update_robot_button.setStyleSheet(button_style.format(
            self.accent_color,
            QColor(self.accent_color).darker(110).name()
        ))
        self.update_robot_button.clicked.connect(self.show_update_modal)
        
        # Ajout des éléments avec espacement
        tab_layout.addWidget(search_container)
        tab_layout.addWidget(self.instance_combo)
        tab_layout.addStretch()
        tab_layout.addWidget(self.add_media_button)
        tab_layout.addWidget(self.action_button)
        tab_layout.addWidget(self.settings_button)
        tab_layout.addWidget(self.update_robot_button)
        
        toolbar_layout.addWidget(self.tab_bar)
        layout.addWidget(toolbar_container)

        # ----------------------------
        # Tableau ultra moderne
        # ----------------------------
        self.table_container = QWidget()
        self.table_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: none;
            }
        """)
        
        table_layout = QVBoxLayout(self.table_container)
        table_layout.setContentsMargins(20, 20, 20, 20)
        table_layout.setSpacing(15)
        
        # En-tête du tableau
        table_header = QWidget()
        table_header.setStyleSheet(".shadow-effect;")
        header_layout = QHBoxLayout(table_header)
        header_layout.setContentsMargins(15, 10, 15, 10)
        
        self.table_title = QLabel("Liste des médias")
        self.table_title.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: 600;
                color: {self.dark_color};
            }}
        """)
        
        self.selected_count = QLabel("0 éléments sélectionnés")
        self.selected_count.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #7f8c8d;
            }
        """)
        
        header_layout.addWidget(self.table_title)
        header_layout.addStretch()
        header_layout.addWidget(self.selected_count)
        
        table_layout.addWidget(table_header)
        
        # Tableau lui-même
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Nom', 'Description', 'Catégorie', 'Aperçu', 'Actions'])
        
        # Configuration avancée du tableau
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.table.cellChanged.connect(self.on_cell_changed)
        
        # Hauteur des lignes et polices
        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.setFont(QFont('Segoe UI', 11))
        
        # Configuration des colonnes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Nom
        header.setSectionResizeMode(1, QHeaderView.Stretch)          # Description
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) # Catégorie
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # Aperçu
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents) # Actions
        header.setDefaultAlignment(Qt.AlignLeft)
        
        # Style premium pour le tableau
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border-radius: 8px;
                border: none;
                alternate-background-color: #fafafa;
                selection-background-color: {self.primary_color}15;
                selection-color: {self.dark_color};
                gridline-color: transparent;
            }}
            QHeaderView {{
                background-color: white;
                border-radius: 8px 8px 0 0;
                border: none;
            }}
            QHeaderView::section {{
                background-color: white;
                color: {self.dark_color};
                padding: 15px;
                border: none;
                font-weight: 500;
                font-size: 13px;
                text-transform: uppercase;
                letter-spacing: 1px;
                border-bottom: 2px solid {self.primary_color};
            }}
            QTableWidget::item {{
                padding: 12px 15px;
                border-bottom: 1px solid #f0f0f0;
            }}
            QTableWidget::item:selected {{
                background-color: {self.primary_color}20;
            }}
            QScrollBar:vertical {{
                width: 10px;
                background: transparent;
                margin: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.primary_color}40;
                min-height: 30px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {self.primary_color}60;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
                background: none;
            }}
        """)
        
        # Ajouter des boutons d'action dans chaque ligne
        self.table.setRowCount(0)  # Reset avant le remplissage
        
        table_layout.addWidget(self.table, 1)
        layout.addWidget(self.table_container, 1)

        # ----------------------------
        # Pagination et statut bar
        # ----------------------------
        footer = QWidget()
        footer.setStyleSheet("""
            QWidget {
                background-color: white;
                border-top: 1px solid #e0e0e0;
            }
        """)
        
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 15, 20, 15)
        
        # Statistiques
        self.stats_label = QLabel("Total: 0 médias")
        self.stats_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 13px;
            }
        """)
        
        # Pagination avancée
        pagination_container = QWidget()
        pagination_layout = QHBoxLayout(pagination_container)
        pagination_layout.setContentsMargins(0, 0, 0, 0)
        pagination_layout.setSpacing(5)
        
        # Boutons de pagination avec icônes
        self.first_page_button = QPushButton()
        self.first_page_button.setIcon(QIcon("icons/first-page.png"))
        self.first_page_button.setToolTip("Première page")
        self.first_page_button.setFixedSize(32, 32)
        
        self.prev_button = QPushButton()
        self.prev_button.setIcon(QIcon("icons/chevron-left.png"))
        self.prev_button.setToolTip("Page précédente")
        self.prev_button.setFixedSize(32, 32)
        
        self.page_edit = QLineEdit("1")
        self.page_edit.setAlignment(Qt.AlignCenter)
        self.page_edit.setFixedWidth(50)
        self.page_edit.setValidator(QIntValidator(1, 999))
        
        self.page_label = QLabel("/ 1")
        self.page_label.setFixedWidth(40)
        
        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon("icons/chevron-right.png"))
        self.next_button.setToolTip("Page suivante")
        self.next_button.setFixedSize(32, 32)
        
        self.last_page_button = QPushButton()
        self.last_page_button.setIcon(QIcon("icons/last-page.png"))
        self.last_page_button.setToolTip("Dernière page")
        self.last_page_button.setFixedSize(32, 32)
        
        # Style des boutons de pagination
        pagination_style = f"""
            QPushButton {{
                border-radius: 16px;
                background-color: white;
                border: 1px solid #e0e0e0;
            }}
            QPushButton:hover {{
                background-color: #f5f5f5;
            }}
            QPushButton:pressed {{
                background-color: #eeeeee;
            }}
            QPushButton:disabled {{
                background-color: #fafafa;
                border-color: #eeeeee;
            }}
            QLineEdit {{
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 5px;
            }}
        """
        
        for btn in [self.first_page_button, self.prev_button, self.next_button, self.last_page_button]:
            btn.setStyleSheet(pagination_style)
            btn.setCursor(Qt.PointingHandCursor)
        
        # Sélecteur d'éléments par page
        self.items_per_page = QComboBox()
        self.items_per_page.addItems(["10", "25", "50", "100", "Tous"])
        self.items_per_page.setCurrentText("25")
        self.items_per_page.currentTextChanged.connect(self.update_pagination)
        self.items_per_page.setStyleSheet(f"""
            QComboBox {{
                padding: 5px 10px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                min-width: 80px;
            }}
        """)
        
        # Connecter les signaux
        # self.first_page_button.clicked.connect(lambda: self.go_to_page(1))
        # self.prev_button.clicked.connect(self.prev_page)
        # self.next_button.clicked.connect(self.next_page)
        # self.last_page_button.clicked.connect(self.go_to_last_page)
        # self.page_edit.returnPressed.connect(self.on_page_edit_changed)

        # Remplacer les connexions des signaux de pagination par ceci :
        self.first_page_button.clicked.connect(lambda: self.go_to_page(1))
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.last_page_button.clicked.connect(lambda: self.go_to_page(self.total_pages))
        self.page_edit.returnPressed.connect(self.on_page_edit_changed)

            
        # Assembler la pagination
        pagination_layout.addWidget(QLabel("Éléments par page:"))
        pagination_layout.addWidget(self.items_per_page)
        pagination_layout.addSpacing(20)
        pagination_layout.addWidget(self.first_page_button)
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.page_edit)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_button)
        pagination_layout.addWidget(self.last_page_button)
        
        # Ajouter au footer
        footer_layout.addWidget(self.stats_label)
        footer_layout.addStretch()
        footer_layout.addWidget(pagination_container)
        
        layout.addWidget(footer)
        
        # Configuration finale
        self.setMinimumSize(1200, 800)
        self.setWindowTitle("FBK Group Management")
        self.setWindowIcon(QIcon("icons/logo.png"))
        
        # Animation d'apparition
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(300)
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        self.opacity_animation.start()
        
        # Remplir le tableau
        self.populate_table()




    def go_to_page(self, page_num):
        """Aller à une page spécifique"""
        if 1 <= page_num <= self.total_pages:
            self.current_page = page_num
            self.update_pagination()
            self.populate_table()

    def on_page_edit_changed(self):
        """Gère le changement de page via l'édition directe"""
        try:
            page_num = int(self.page_edit.text())
            self.go_to_page(page_num)
        except ValueError:
            pass

    def update_pagination(self):
        """Met à jour l'état des boutons de pagination et les labels"""
        # Calculer le nombre total de pages
        items_per_page = int(self.items_per_page.currentText()) if self.items_per_page.currentText() != "Tous" else float('inf')
        self.total_pages = max(1, math.ceil(len(self.media_data) / items_per_page)) if items_per_page != float('inf') else 1
        
        # Mettre à jour les boutons
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < self.total_pages)
        self.first_page_button.setEnabled(self.current_page > 1)
        self.last_page_button.setEnabled(self.current_page < self.total_pages)
        
        # Mettre à jour les labels
        self.page_edit.setText(str(self.current_page))
        self.page_label.setText(f"/ {self.total_pages}")
        self.stats_label.setText(f"Total: {len(self.media_data)} médias | Page {self.current_page}/{self.total_pages}")

    def prev_page(self):
        """Aller à la page précédente"""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()
            self.populate_table()

    def next_page(self):
        """Aller à la page suivante"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_pagination()
            self.populate_table()


    def populate_tabl1e(self):
        """Remplit le tableau avec un style amélioré et chargement paresseux des images"""
        self.table.setRowCount(len(self.media_list))
        
        # Configurer le delegate pour la colonne Description
        # self.table.setItemDelegateForColumn(1, RichTextDelegate(self.table))
        
        for row, media in enumerate(self.media_list):
            # Colonne Nom
            name_item = QTableWidgetItem(media['nom'])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, name_item)

            # Colonne Description
            desc_item = QTableWidgetItem(media['description'])
            desc_item.setFont(QFont("Segoe UI", 10))
            desc_item.setFlags(desc_item.flags() | Qt.ItemIsEditable)
            self.table.setItem(row, 1, desc_item)

            # Colonne Catégorie
            category_combo = QComboBox()
            categories = self.media_manager.load_categories()
            category_combo.addItems([c['name'] for c in categories])
            category_combo.setCurrentText(media.get('categorie', 'Default'))
            category_combo.currentTextChanged.connect(lambda text, row=row: self.update_category(row, text))
            self.table.setCellWidget(row, 2, category_combo)

            # Colonne Aperçu (chargement paresseux)
            preview_label = QLabel()
            preview_label.setAlignment(Qt.AlignCenter)
            
            if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
                # On crée un QLabel vide et on stocke le chemin pour chargement ultérieur
                preview_label.setProperty("image_path", media['preview_path'])
                preview_label.setText("(Chargement...)")
            elif media['nom'].endswith(('.mp4', '.mov')):
                preview_label.setText("🎥 Voir")
                
            preview_label.mousePressEvent = lambda event, path=media['preview_path']: self.show_preview(path)
            self.table.setCellWidget(row, 3, preview_label)

            # Colonne Actions
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(8, 2, 8, 2)
            action_layout.setSpacing(10)

            # Fonction pour créer les boutons
            def create_button(emoji, tooltip, color, hover_color, callback):
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
                btn.clicked.connect(lambda _, m=media: callback(m))
                return btn

            # Création des boutons
            buttons = [
                ("📅", "Planifier la publication", "#9b59b6", "#8e44ad", self.schedule_publication),
                ("🤖", "Envoyer au robot", "#3498db", "#2980b9", self.send_to_robot),
                ("🗑️", "Supprimer", "#e74c3c", "#c0392b", self.delete_media)
            ]
            
            for params in buttons:
                action_layout.addWidget(create_button(*params))

            self.table.setCellWidget(row, 4, action_widget)
        
        # Configurer le chargement paresseux
        self.table.verticalScrollBar().valueChanged.connect(self.lazy_load_images)
        # Charger les images visibles initialement
        QTimer.singleShot(100, self.lazy_load_images)
        
        # Ajustement automatique des hauteurs de ligne
        self.table.resizeRowsToContents()
        self.table.model().dataChanged.connect(lambda: self.table.resizeRowsToContents())

    def lazy_load_images(self):
        """Charge les images uniquement pour les lignes visibles"""
        visible_rect = self.table.viewport().rect()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 3) or self.table.cellWidget(row, 3)
            if isinstance(item, QLabel) and item.property("image_path"):
                # Vérifier si la ligne est visible
                row_rect = self.table.visualItemRect(self.table.item(row, 0) or self.table.item(row, 1))
                if visible_rect.intersects(row_rect):
                    path = item.property("image_path")
                    pixmap = QPixmap(path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    item.setPixmap(pixmap)
                    item.setProperty("image_path", None)  # Pour ne pas recharger
                    
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



class UpdateRobotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Envoyer au Robot")
        self.setWindowIcon(QIcon("icons/update.png"))
        self.setFixedSize(500, 400)

        # Connexion à la base de données
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

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

        # Sélection des catégories de groupes (MODIFIÉ pour utiliser category_group)
        self.group_category_label = QLabel("Sélectionnez une ou plusieurs catégories de groupes:")
        layout.addWidget(self.group_category_label)

        self.group_category_list = QListWidget()
        self.group_category_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_group_categories()  # Cette méthode va maintenant utiliser category_group
        layout.addWidget(self.group_category_list)

        # Bouton pour envoyer au robot
        self.send_button = QPushButton("Envoyer au Robot", self)
        self.send_button.setIcon(QIcon("icons/robot.png"))
        self.send_button.clicked.connect(self.send_to_robot)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def load_media_categories(self):
        """Charge les catégories de médias depuis la table 'category'"""
        self.cursor.execute("SELECT id, name FROM category")
        media_categories = self.cursor.fetchall()
        for category in media_categories:
            item = QListWidgetItem(category[1])
            item.setData(Qt.UserRole, category[0])
            self.media_category_list.addItem(item)

    def load_group_categories(self):
        """Charge les catégories de groupes depuis la table 'category_group' (MODIFIÉ)"""
        self.cursor.execute("SELECT id, name FROM category_group")
        group_categories = self.cursor.fetchall()
        for category in group_categories:
            item = QListWidgetItem(category[1])
            item.setData(Qt.UserRole, category[0])
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
        if not category_ids:
            return []
            
        query = """
            SELECT m.id, m.nom, m.description, m.preview_path, mt.type
            FROM media m
            JOIN media_type mt ON m.type_id = mt.id
            WHERE m.category_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        self.cursor.execute(query, category_ids)
        return self.cursor.fetchall()

    def get_group_data(self, category_ids):
        """Récupère les données des groupes pour les catégories sélectionnées (MODIFIÉ)."""
        if not category_ids:
            return []
            
        query = """
            SELECT g.id, g.name, g.link, g.remarks, g.description, g.keywords
            FROM groups g
            WHERE g.category_group_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        self.cursor.execute(query, category_ids)
        return self.cursor.fetchall()

    def send_data_to_robot(self, media_data, group_data):
        """
        Envoie les données sélectionnées au robot en utilisant FileTransferApp et FileTransferApp2.
        """
        combined_content = {
            "posts": [],
            "groups": []
        }

        # Ajouter les données de médias
        for media in media_data:
            combined_content["posts"].append({
                "id": media[0],
                "name": media[1],
                "description": media[2],
                "preview_path": media[3],
                "type": media[4]
            })

        # Ajouter les données de groupes (MODIFIÉ selon la structure de votre table groups)
        for group in group_data:
            combined_content["groups"].append({
                "id": group[0],
                "name": group[1],
                "link": group[2],
                "remarks": group[3],
                "description": group[4],
                "keywords": group[5]
            })

        # Envoyer les données
        transfer_app = FileTransferApp()
        transfer_app.start_process(combined_content)

        transfer_app2 = FileTransferApp2()
        transfer_app2.start_process(combined_content)

    def closeEvent(self, event):
        """Ferme la connexion à la base de données."""
        self.conn.close()
        event.accept()






import os
import sqlite3
import ctypes
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, 
                            QPushButton, QMessageBox, QComboBox, QHBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QCoreApplication

class UpdateRobotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Envoyer au Robot"))
        self.setWindowIcon(QIcon("icons/update.png"))
        self.setFixedSize(600, 500)
        
        # Connexion à la base de données
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        
        # Détection des réseaux sociaux et robots disponibles
        self.social_networks = self.detect_social_networks()
        
        # Styles CSS modernes
        self.setup_styles()
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Ajout des contrôles pour la sélection du réseau social et du robot
        self.setup_network_robot_selection(layout)
        
        # Sélection des catégories
        self.setup_category_selection(layout)
        
        # Bouton d'envoi
        self.setup_send_button(layout)
        
        self.setLayout(layout)
    
    def setup_styles(self):
        """Configure les styles CSS"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 12px;
                border: 1px solid #ddd;
            }
            QPushButton {
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #007BFF, stop:1 #0056b3);
                color: white;
                margin: 4px;
                border: none;
                box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0056b3, stop:1 #003f8a);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #003f8a, stop:1 #002b60);
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
                margin-bottom: 4px;
            }
            QComboBox {
                padding: 6px;
                font-size: 14px;
                border: 1px solid #ced4da;
                border-radius: 4px;
            }
        """)
    
    def detect_social_networks(self):
        """Détecte les réseaux sociaux disponibles et leurs robots"""
        social_networks = {}
        base_path = "C:\\"
        
        # Dictionnaire des dossiers à vérifier et leurs noms affichés
        network_folders = {
            "bon": "Facebook",
            "wabon": "WhatsApp",
            "instabon": "Instagram",
            "inbon": "LinkedIn",
            "ytbon": "YouTube"
        }
        
        for folder, display_name in network_folders.items():
            network_path = os.path.join(base_path, folder)
            if os.path.exists(network_path):
                robots = []
                # Recherche des sous-dossiers robot1, robot2, etc.
                for item in os.listdir(network_path):
                    if os.path.isdir(os.path.join(network_path, item)) and item.startswith("robot"):
                        robots.append(item)
                
                if robots:
                    social_networks[network_path] = {
                        'display_name': display_name,
                        'robots': sorted(robots)
                    }
        
        return social_networks
    
    def setup_network_robot_selection(self, layout):
        """Configure la sélection du réseau social et du robot"""
        if not self.social_networks:
            # Aucun réseau social détecté
            no_robot_label = QLabel(self.tr("Aucun robot détecté. Veuillez installer un robot."))
            layout.addWidget(no_robot_label)
            self.has_robots = False
            return
        
        self.has_robots = True
        
        # Layout horizontal pour les combobox
        h_layout = QHBoxLayout()
        
        # Combobox pour le réseau social
        self.network_combo = QComboBox()
        self.network_combo.addItem(self.tr("Sélectionnez un réseau social"))
        
        # Combobox pour le robot
        self.robot_combo = QComboBox()
        self.robot_combo.addItem(self.tr("Sélectionnez un robot"))
        
        # Remplir les combobox
        self.network_paths = []  # Pour garder la correspondance entre l'index et le chemin
        for i, (path, data) in enumerate(self.social_networks.items()):
            self.network_combo.addItem(data['display_name'])
            self.network_paths.append(path)
        
        # Connecter le signal de changement de réseau social
        self.network_combo.currentIndexChanged.connect(self.update_robot_combo)
        
        # Sélectionner Facebook par défaut s'il existe
        for i, (path, data) in enumerate(self.social_networks.items()):
            if data['display_name'] == "Facebook":
                self.network_combo.setCurrentIndex(i + 1)
                break
        
        h_layout.addWidget(QLabel(self.tr("Réseau social:")))
        h_layout.addWidget(self.network_combo)
        h_layout.addWidget(QLabel(self.tr("Robot:")))
        h_layout.addWidget(self.robot_combo)
        
        layout.addLayout(h_layout)
    
    def update_robot_combo(self, index):
        """Met à jour la liste des robots lorsqu'un réseau social est sélectionné"""
        if index == 0:  # "Sélectionnez un réseau social"
            self.robot_combo.clear()
            self.robot_combo.addItem(self.tr("Sélectionnez un robot"))
            return
        
        self.robot_combo.clear()
        network_path = self.network_paths[index - 1]
        robots = self.social_networks[network_path]['robots']
        
        for robot in robots:
            self.robot_combo.addItem(robot)
    
    def setup_category_selection(self, layout):
        """Configure la sélection des catégories avec des boutons"""
        if not self.has_robots:
            return
        
        # Catégories de médias
        media_category_label = QLabel(self.tr("Sélectionnez une ou plusieurs catégories de médias:"))
        layout.addWidget(media_category_label)
        
        self.media_category_list = QListWidget()
        self.media_category_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_media_categories()
        layout.addWidget(self.media_category_list)
        
        # Catégories de groupes
        group_category_label = QLabel(self.tr("Sélectionnez une ou plusieurs catégories de groupes:"))
        layout.addWidget(group_category_label)
        
        self.group_category_list = QListWidget()
        self.group_category_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_group_categories()
        layout.addWidget(self.group_category_list)
    
    def setup_send_button(self, layout):
        """Configure le bouton d'envoi"""
        if self.has_robots:
            self.send_button = QPushButton(self.tr("Envoyer au Robot"), self)
            self.send_button.setIcon(QIcon("icons/robot.png"))
            self.send_button.clicked.connect(self.send_to_robot)
            layout.addWidget(self.send_button)
        else:
            self.install_button = QPushButton(self.tr("Installer un Robot"), self)
            self.install_button.setIcon(QIcon("icons/install.png"))
            self.install_button.clicked.connect(self.install_robot)
            layout.addWidget(self.install_button)
    
    def load_media_categories(self):
        """Charge les catégories de médias depuis la table 'category'"""
        self.cursor.execute("SELECT id, name FROM category")
        media_categories = self.cursor.fetchall()
        for category in media_categories:
            item = QListWidgetItem(self.tr(category[1]))
            item.setData(Qt.UserRole, category[0])
            self.media_category_list.addItem(item)
    
    def load_group_categories(self):
        """Charge les catégories de groupes depuis la table 'category_group'"""
        self.cursor.execute("SELECT id, name FROM category_group")
        group_categories = self.cursor.fetchall()
        for category in group_categories:
            item = QListWidgetItem(self.tr(category[1]))
            item.setData(Qt.UserRole, category[0])
            self.group_category_list.addItem(item)
    
    def send_to_robot(self):
        """Envoie les données sélectionnées au robot."""
        # Vérifier qu'un réseau social et un robot sont sélectionnés
        if self.network_combo.currentIndex() == 0 or self.robot_combo.currentIndex() == -1:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Veuillez sélectionner un réseau social et un robot."))
            return
        
        selected_media_categories = [
            item.data(Qt.UserRole) for item in self.media_category_list.selectedItems()
        ]
        selected_group_categories = [
            item.data(Qt.UserRole) for item in self.group_category_list.selectedItems()
        ]

        if not selected_media_categories and not selected_group_categories:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Veuillez sélectionner au moins une catégorie de médias ou de groupes."))
            return

        # Récupérer les données de la base de données
        media_data = self.get_media_data(selected_media_categories)
        group_data = self.get_group_data(selected_group_categories)

        # Préparer les données combinées
        combined_content = {
            "posts": [],
            "groups": []
        }

        # Ajouter les données de médias
        for media in media_data:
            combined_content["posts"].append({
                "id": media[0],
                "name": media[1],
                "description": media[2],
                "preview_path": media[3],
                "type": media[4]
            })

        # Ajouter les données de groupes
        for group in group_data:
            combined_content["groups"].append({
                "id": group[0],
                "name": group[1],
                "link": group[2],
                "remarks": group[3],
                "description": group[4],
                "keywords": group[5]
            })

        # Envoyer les données au robot sélectionné
        network_path = self.network_paths[self.network_combo.currentIndex() - 1]
        robot_name = self.robot_combo.currentText()
        
        # Créer une instance de FileTransferApp avec le bon chemin
        transfer_app = FileTransferApp(network_path, robot_name)
        transfer_app.start_process(combined_content)

        QMessageBox.information(self, self.tr("Succès"), self.tr("Les données ont été envoyées au robot avec succès."))
        self.accept()
    
    def get_media_data(self, category_ids):
        """Récupère les données des médias pour les catégories sélectionnées."""
        if not category_ids:
            return []
            
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
        if not category_ids:
            return []
            
        query = """
            SELECT g.id, g.name, g.link, g.remarks, g.description, g.keywords
            FROM groups g
            WHERE g.category_group_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        self.cursor.execute(query, category_ids)
        return self.cursor.fetchall()
    
    def install_robot(self):
        """Ouvre la fenêtre d'installation du robot (à implémenter plus tard)"""
        QMessageBox.information(self, self.tr("Installation"), self.tr("Cette fonctionnalité sera implémentée ultérieurement."))
    
    def closeEvent(self, event):
        """Ferme la connexion à la base de données."""
        self.conn.close()
        event.accept()


class FileTransferApp:
    def __init__(self, network_path, robot_name):
        self.network_path = network_path
        self.robot_name = robot_name
        self.target_dir = os.path.join(network_path, robot_name)
    
    def start_process(self, combined_content):
        """
        Envoie les données au robot spécifié.
        
        Args:
            combined_content (dict): Données combinées (médias et groupes).
        """
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        # Enregistrer les données dans un fichier JSON
        target_json_path = os.path.join(self.target_dir, "data.json")
        with open(target_json_path, 'w', encoding='utf-8') as json_file:
            import json
            json.dump(combined_content, json_file, ensure_ascii=False, indent=4)

        # Cacher le dossier
        self.hide_file(self.target_dir)
    
    def hide_file(self, file_path):
        """Cache un fichier ou un dossier avec les attributs 'hidden' et 'system'."""
        if os.path.exists(file_path):
            ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04)

import os
import sqlite3
import ctypes
import json
from datetime import datetime
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, 
                            QPushButton, QMessageBox, QComboBox, QHBoxLayout, QTabWidget,
                            QTextEdit, QWidget, QFormLayout, QGroupBox, QScrollArea)
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import Qt, QCoreApplication

class UpdateRobotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Robot Data Manager"))
        self.setWindowIcon(QIcon("icons/robot.png"))
        self.setFixedSize(900, 700)
        
        # Connexion à la base de données
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        
        # Détection des réseaux sociaux et robots disponibles
        self.social_networks = self.detect_social_networks()
        self.current_network = None
        self.current_robot = None
        self.json_structure = {}
        
        # Styles CSS modernes
        self.setup_styles()
        
        # Layout principal
        main_layout = QVBoxLayout()
        
        # Section de sélection du réseau et robot
        self.setup_network_robot_selection(main_layout)
        
        # Section des catégories (en ligne)
        categories_layout = QHBoxLayout()
        self.setup_category_selection(categories_layout)
        main_layout.addLayout(categories_layout)
        
        # Section de visualisation des données
        self.setup_data_viewer(main_layout)
        
        # Boutons d'action
        self.setup_action_buttons(main_layout)
        
        self.setLayout(main_layout)
    
    def setup_styles(self):
        """Configure les styles CSS"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
                border: none;
                margin: 4px;
                min-width: 120px;
            }
            QPushButton#send_button {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#send_button:hover {
                background-color: #45a049;
            }
            QPushButton#send_button1 {
                background-color: #2196F3;
                color: white;
            }
            QPushButton#send_button1:hover {
                background-color: #0b7dda;
            }
            QPushButton#send_button2 {
                background-color: #ff9800;
                color: white;
            }
            QPushButton#send_button2:hover {
                background-color: #e68a00;
            }
            QPushButton#test_button {
                background-color: #9c27b0;
                color: white;
            }
            QPushButton#test_button:hover {
                background-color: #7b1fa2;
            }
            QListWidget {
                font-size: 14px;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
                min-width: 280px;
                min-height: 200px;
            }
            QLabel {
                font-size: 14px;
                color: #333;
                margin-bottom: 4px;
                font-weight: bold;
            }
            QComboBox {
                padding: 6px;
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 200px;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 6px;
                background: white;
            }
            QTabBar::tab {
                padding: 8px 12px;
                background: #f1f1f1;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #2196F3;
                font-weight: bold;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
    
    def detect_social_networks(self):
        """Détecte les réseaux sociaux disponibles et leurs robots"""
        social_networks = {}
        base_path = "C:\\"
        
        # Dictionnaire des dossiers à vérifier et leurs configurations
        network_config = {
            "bon": {
                "display_name": "Facebook",
                "json_files": ["data.json", "data1.json"],
                "button_names": ["Publier Posts", "Publier Stories", "Publier Groups"],
                "tab_names": ["Posts", "Stories", "Groups"]
            },
            "wabon": {
                "display_name": "WhatsApp",
                "json_files": ["contacts.json", "groups.json", "broadcast.json"],
                "button_names": ["Envoyer Contacts", "Envoyer Groups", "Envoyer Broadcast"],
                "tab_names": ["Contacts", "Groups", "Broadcast"]
            },
            "instabon": {
                "display_name": "Instagram",
                "json_files": ["posts.json", "stories.json", "reels.json"],
                "button_names": ["Publier Posts", "Publier Stories", "Publier Reels"],
                "tab_names": ["Posts", "Stories", "Reels"]
            },
            "inbon": {
                "display_name": "LinkedIn",
                "json_files": ["posts.json", "articles.json", "connections.json"],
                "button_names": ["Publier Posts", "Publier Articles", "Envoyer Connections"],
                "tab_names": ["Posts", "Articles", "Connections"]
            },
            "ytbon": {
                "display_name": "YouTube",
                "json_files": ["videos.json", "shorts.json", "comments.json"],
                "button_names": ["Publier Videos", "Publier Shorts", "Commenter"],
                "tab_names": ["Videos", "Shorts", "Comments"]
            }
        }
        
        for folder, config in network_config.items():
            network_path = os.path.join(base_path, folder)
            if os.path.exists(network_path):
                robots = []
                # Recherche des sous-dossiers robot1, robot2, etc.
                for item in os.listdir(network_path):
                    if os.path.isdir(os.path.join(network_path, item)) and item.startswith("robot"):
                        robots.append(item)
                
                if robots:
                    social_networks[network_path] = {
                        'display_name': config['display_name'],
                        'robots': sorted(robots),
                        'json_files': config['json_files'],
                        'button_names': config['button_names'],
                        'tab_names': config['tab_names']
                    }
        
        return social_networks
    
    def setup_network_robot_selection(self, layout):
        """Configure la sélection du réseau social et du robot"""
        group_box = QGroupBox(self.tr("Sélection du Robot"))
        form_layout = QFormLayout()
        
        # Combobox pour le réseau social
        self.network_combo = QComboBox()
        self.network_combo.addItem(self.tr("Sélectionnez un réseau social"))
        
        # Combobox pour le robot
        self.robot_combo = QComboBox()
        self.robot_combo.addItem(self.tr("Sélectionnez un robot"))
        
        # Combobox pour le fichier JSON
        self.json_combo = QComboBox()
        self.json_combo.addItem(self.tr("Sélectionnez un fichier"))
        
        # Remplir les combobox
        self.network_paths = []  # Pour garder la correspondance entre l'index et le chemin
        for i, (path, data) in enumerate(self.social_networks.items()):
            self.network_combo.addItem(data['display_name'])
            self.network_paths.append(path)
        
        # Connecter les signaux
        self.network_combo.currentIndexChanged.connect(self.update_robot_combo)
        self.robot_combo.currentIndexChanged.connect(self.update_json_combo)
        self.json_combo.currentIndexChanged.connect(self.load_json_data)
        
        form_layout.addRow(QLabel(self.tr("Réseau social:")), self.network_combo)
        form_layout.addRow(QLabel(self.tr("Robot:")), self.robot_combo)
        form_layout.addRow(QLabel(self.tr("Fichier:")), self.json_combo)
        
        group_box.setLayout(form_layout)
        layout.addWidget(group_box)
    
    def update_robot_combo(self, index):
        """Met à jour la liste des robots lorsqu'un réseau social est sélectionné"""
        if index == 0:  # "Sélectionnez un réseau social"
            self.robot_combo.clear()
            self.robot_combo.addItem(self.tr("Sélectionnez un robot"))
            self.json_combo.clear()
            self.json_combo.addItem(self.tr("Sélectionnez un fichier"))
            return
        
        self.current_network = self.network_paths[index - 1]
        network_data = self.social_networks[self.current_network]
        
        self.robot_combo.clear()
        for robot in network_data['robots']:
            self.robot_combo.addItem(robot)
    
    def update_json_combo(self, index):
        """Met à jour la liste des fichiers JSON lorsqu'un robot est sélectionné"""
        if index == 0:  # "Sélectionnez un robot"
            self.json_combo.clear()
            self.json_combo.addItem(self.tr("Sélectionnez un fichier"))
            return
        
        self.current_robot = self.robot_combo.currentText()
        network_data = self.social_networks[self.current_network]
        
        self.json_combo.clear()
        for json_file in network_data['json_files']:
            self.json_combo.addItem(json_file)
    
    def setup_category_selection(self, layout):
        """Configure la sélection des catégories avec des listes"""
        # Catégories de médias
        media_group = QGroupBox(self.tr("Catégories de Médias"))
        media_layout = QVBoxLayout()
        
        self.media_category_list = QListWidget()
        self.media_category_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_media_categories()
        
        media_layout.addWidget(self.media_category_list)
        media_group.setLayout(media_layout)
        layout.addWidget(media_group)
        
        # Catégories de groupes
        group_group = QGroupBox(self.tr("Catégories de Groupes"))
        group_layout = QVBoxLayout()
        
        self.group_category_list = QListWidget()
        self.group_category_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_group_categories()
        
        group_layout.addWidget(self.group_category_list)
        group_group.setLayout(group_layout)
        layout.addWidget(group_group)
    
    def setup_data_viewer(self, layout):
        """Configure la visualisation des données JSON"""
        group_box = QGroupBox(self.tr("Visualisation des Données"))
        vbox = QVBoxLayout()
        
        # Onglets pour afficher les données
        self.tab_widget = QTabWidget()
        self.tabs = []
        
        # Créer les onglets dynamiquement (sera mis à jour lors de la sélection du JSON)
        self.update_tabs()
        
        # Zone de texte pour afficher le contenu
        self.content_viewer = QTextEdit()
        self.content_viewer.setReadOnly(True)
        
        vbox.addWidget(self.tab_widget)
        vbox.addWidget(self.content_viewer)
        group_box.setLayout(vbox)
        layout.addWidget(group_box)
    
    def update_tabs(self):
        """Met à jour les onglets en fonction du réseau social sélectionné"""
        self.tab_widget.clear()
        self.tabs = []
        
        if not self.current_network:
            return
        
        network_data = self.social_networks[self.current_network]
        
        for tab_name in network_data['tab_names']:
            tab = QWidget()
            self.tabs.append(tab)
            self.tab_widget.addTab(tab, tab_name)
        
        # Connecter le changement d'onglet
        self.tab_widget.currentChanged.connect(self.update_content_viewer)
    
    def load_json_data(self, index):
        """Charge les données JSON lorsqu'un fichier est sélectionné"""
        if index == 0 or not self.current_network or not self.current_robot:
            self.json_structure = {}
            self.update_tabs()
            return
        
        json_file = self.json_combo.currentText()
        robot_path = os.path.join(self.current_network, self.current_robot, json_file)
        
        try:
            if os.path.exists(robot_path):
                with open(robot_path, 'r', encoding='utf-8') as f:
                    self.json_structure = json.load(f)
            else:
                self.json_structure = {}
            
            self.update_tabs()
            self.update_content_viewer()
        except Exception as e:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr(f"Impossible de charger le fichier: {str(e)}"))
            self.json_structure = {}
    
    def update_content_viewer(self):
        """Met à jour le contenu affiché en fonction de l'onglet sélectionné"""
        if not self.json_structure or not self.tabs:
            self.content_viewer.clear()
            return
        
        current_tab_index = self.tab_widget.currentIndex()
        tab_name = self.tab_widget.tabText(current_tab_index).lower()
        
        if tab_name in self.json_structure:
            content = self.json_structure[tab_name]
            
            if isinstance(content, list):
                if content and isinstance(content[0], dict):
                    # Formatage des dictionnaires en JSON lisible
                    formatted_content = json.dumps(content, ensure_ascii=False, indent=4)
                else:
                    formatted_content = "\n".join(str(item) for item in content)
            else:
                formatted_content = str(content)
            
            self.content_viewer.setPlainText(formatted_content)
            self.content_viewer.moveCursor(QTextCursor.Start)
        else:
            self.content_viewer.setPlainText(self.tr("Aucune donnée disponible pour cet onglet."))
    
    def setup_action_buttons(self, layout):
        """Configure les boutons d'action"""
        group_box = QGroupBox(self.tr("Actions"))
        hbox = QHBoxLayout()
        
        # Boutons dynamiques en fonction du réseau social
        self.send_button = QPushButton()
        self.send_button.setObjectName("send_button")
        self.send_button1 = QPushButton()
        self.send_button1.setObjectName("send_button1")
        self.send_button2 = QPushButton()
        self.send_button2.setObjectName("send_button2")
        
        # Bouton de test
        self.test_button = QPushButton(self.tr("Tester le Robot"))
        self.test_button.setObjectName("test_button")
        self.test_button.setIcon(QIcon("icons/test.png"))
        
        # Connecter les signaux
        self.send_button.clicked.connect(lambda: self.send_to_robot(0))
        self.send_button1.clicked.connect(lambda: self.send_to_robot(1))
        self.send_button2.clicked.connect(lambda: self.send_to_robot(2))
        self.test_button.clicked.connect(self.test_robot)
        
        hbox.addWidget(self.send_button)
        hbox.addWidget(self.send_button1)
        hbox.addWidget(self.send_button2)
        hbox.addWidget(self.test_button)
        
        group_box.setLayout(hbox)
        layout.addWidget(group_box)
        
        # Mettre à jour les libellés des boutons
        self.update_button_labels()
        
        # Connecter le changement de réseau social pour mettre à jour les boutons
        self.network_combo.currentIndexChanged.connect(self.update_button_labels)
    
    def update_button_labels(self):
        """Met à jour les libellés des boutons en fonction du réseau social sélectionné"""
        if not self.current_network:
            self.send_button.setText(self.tr("Envoyer"))
            self.send_button1.setText(self.tr("Envoyer"))
            self.send_button2.setText(self.tr("Envoyer"))
            return
        
        network_data = self.social_networks[self.current_network]
        
        self.send_button.setText(network_data['button_names'][0])
        self.send_button1.setText(network_data['button_names'][1])
        self.send_button2.setText(network_data['button_names'][2])
    
    def load_media_categories(self):
        """Charge les catégories de médias depuis la table 'category'"""
        self.cursor.execute("SELECT id, name FROM category")
        media_categories = self.cursor.fetchall()
        for category in media_categories:
            item = QListWidgetItem(self.tr(category[1]))
            item.setData(Qt.UserRole, category[0])
            self.media_category_list.addItem(item)
    
    def load_group_categories(self):
        """Charge les catégories de groupes depuis la table 'category_group'"""
        self.cursor.execute("SELECT id, name FROM category_group")
        group_categories = self.cursor.fetchall()
        for category in group_categories:
            item = QListWidgetItem(self.tr(category[1]))
            item.setData(Qt.UserRole, category[0])
            self.group_category_list.addItem(item)
    
    def send_to_robot(self, button_index):
        """Envoie les données sélectionnées au robot."""
        # Vérifier qu'un réseau social, un robot et un fichier sont sélectionnés
        if (self.network_combo.currentIndex() == 0 or 
            self.robot_combo.currentIndex() == 0 or 
            self.json_combo.currentIndex() == 0):
            QMessageBox.warning(self, self.tr("Erreur"), 
                              self.tr("Veuillez sélectionner un réseau social, un robot et un fichier."))
            return
        
        selected_media_categories = [
            item.data(Qt.UserRole) for item in self.media_category_list.selectedItems()
        ]
        selected_group_categories = [
            item.data(Qt.UserRole) for item in self.group_category_list.selectedItems()
        ]

        if not selected_media_categories and not selected_group_categories:
            QMessageBox.warning(self, self.tr("Erreur"), 
                              self.tr("Veuillez sélectionner au moins une catégorie de médias ou de groupes."))
            return

        # Récupérer les données de la base de données
        media_data = self.get_media_data(selected_media_categories)
        group_data = self.get_group_data(selected_group_categories)

        # Préparer les données combinées selon le type de fichier
        json_file = self.json_combo.currentText()
        combined_content = self.prepare_content(media_data, group_data, json_file, button_index)

        # Chemin complet du fichier JSON
        robot_path = os.path.join(self.current_network, self.current_robot)
        json_path = os.path.join(robot_path, json_file)
        
        # Archiver l'ancien fichier s'il existe
        self.archive_existing_file(json_path)
        
        # Enregistrer les nouvelles données
        try:
            os.makedirs(robot_path, exist_ok=True)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(combined_content, f, ensure_ascii=False, indent=4)
            
            # Cacher le dossier
            self.hide_file(robot_path)
            
            # Afficher un message de confirmation stylé
            self.show_confirmation_message(json_file)
        except Exception as e:
            QMessageBox.critical(self, self.tr("Erreur"), 
                               self.tr(f"Impossible d'enregistrer le fichier: {str(e)}"))
    
    def prepare_content(self, media_data, group_data, json_file, button_index):
        """Prépare le contenu selon le type de fichier et le bouton cliqué"""
        network_data = self.social_networks[self.current_network]
        display_name = network_data['display_name']
        
        # Structure de base différente selon le réseau social
        if display_name == "Facebook":
            if json_file == "data.json":
                return {
                    "posts": [{
                        "text": f"{media[1]}\n\n{media[2]}",
                        "image": media[3]
                    } for media in media_data],
                    "groups": [group[2] for group in group_data]
                }
            elif json_file == "data1.json":
                return {
                    "stories": [{
                        "text": media[1],
                        "image": media[3]
                    } for media in media_data],
                    "groups": [group[2] for group in group_data]
                }
        
        elif display_name == "WhatsApp":
            if json_file == "contacts.json":
                return {
                    "contacts": [{
                        "name": group[1],
                        "number": group[2].split('/')[-1]  # Exemple d'extraction de numéro
                    } for group in group_data]
                }
            elif json_file == "groups.json":
                return {
                    "groups": [group[2] for group in group_data]
                }
        
        # Ajouter d'autres cas pour les autres réseaux sociaux...
        
        # Par défaut, retourner une structure générique
        return {
            "media": [{
                "id": media[0],
                "name": media[1],
                "description": media[2],
                "path": media[3]
            } for media in media_data],
            "groups": [{
                "id": group[0],
                "name": group[1],
                "link": group[2]
            } for group in group_data]
        }
    
    def archive_existing_file(self, file_path):
        """Archive le fichier existant s'il existe"""
        if os.path.exists(file_path):
            try:
                # Créer un nom d'archive avec la date actuelle
                archive_name = f"{os.path.splitext(file_path)[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                os.rename(file_path, archive_name)
            except Exception as e:
                print(f"Impossible d'archiver le fichier: {str(e)}")
    
    def hide_file(self, file_path):
        """Cache un fichier ou un dossier avec les attributs 'hidden' et 'system'."""
        if os.path.exists(file_path):
            try:
                ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04)
            except:
                pass
    
    def show_confirmation_message(self, json_file):
        """Affiche un message de confirmation stylé avec un bouton de test"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(self.tr("Succès"))
        msg.setText(self.tr(f"Les données ont été envoyées avec succès au fichier {json_file}"))
        
        # Ajouter un bouton de test
        test_button = msg.addButton(self.tr("Tester le Robot"), QMessageBox.ActionRole)
        test_button.setIcon(QIcon("icons/test.png"))
        
        # Ajouter un bouton OK
        msg.addButton(QMessageBox.Ok)
        
        # Appliquer un style
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
        """)
        
        # Afficher la boîte de dialogue
        ret = msg.exec_()
        
        # Si le bouton de test est cliqué
        if msg.clickedButton() == test_button:
            self.test_robot()
    
    def test_robot(self):
        """Teste le robot sélectionné"""
        if not self.current_network or not self.current_robot:
            QMessageBox.warning(self, self.tr("Erreur"), 
                              self.tr("Veuillez sélectionner un réseau social et un robot."))
            return
        
        # Implémentez ici la logique de test du robot
        QMessageBox.information(self, self.tr("Test du Robot"), 
                              self.tr(f"Test du robot {self.current_robot} en cours..."))
    
    def get_media_data(self, category_ids):
        """Récupère les données des médias pour les catégories sélectionnées."""
        if not category_ids:
            return []
            
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
        if not category_ids:
            return []
            
        query = """
            SELECT g.id, g.name, g.link, g.remarks, g.description, g.keywords
            FROM groups g
            WHERE g.category_group_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        self.cursor.execute(query, category_ids)
        return self.cursor.fetchall()
    
    def closeEvent(self, event):
        """Ferme la connexion à la base de données."""
        self.conn.close()
        event.accept()



import os
import sqlite3
import json
import ctypes
from datetime import datetime
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
                            QListWidgetItem, QPushButton, QMessageBox, QComboBox, 
                            QTextEdit, QTabWidget, QWidget, QGroupBox, QFormLayout)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class UpdateRobotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Robot Manager Pro")
        self.setWindowIcon(QIcon("icons/robot.png"))
        self.setFixedSize(1000, 750)
        
        # Connexion à la base de données
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        
        # Détection des réseaux sociaux et robots disponibles
        self.social_networks = self.detect_social_networks()
        self.current_network = None
        self.current_robot = None
        
        # Styles
        self.setup_styles()
        
        # Layout principal
        main_layout = QVBoxLayout()
        
        # 1. Sélection du réseau social et robot
        self.setup_network_robot_selection(main_layout)
        
        # 2. Sélection des catégories (en ligne)
        categories_layout = QHBoxLayout()
        self.setup_category_selection(categories_layout)
        main_layout.addLayout(categories_layout)
        
        # 3. Visualisation et édition des données
        self.setup_data_editor(main_layout)
        
        # 4. Boutons d'action
        self.setup_action_buttons(main_layout)
        
        self.setLayout(main_layout)
    
    def setup_styles(self):
        """Configure les styles CSS modernes"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial;
            }
            QGroupBox {
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
                color: #333;
            }
            QListWidget {
                background: white;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QTextEdit {
                background: white;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Consolas';
                font-size: 12px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 120px;
            }
            QComboBox {
                padding: 6px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                min-width: 200px;
            }
            QLabel {
                color: #444;
                font-size: 14px;
            }
            #send_button {
                background-color: #4CAF50;
                color: white;
            }
            #cancel_button {
                background-color: #f44336;
                color: white;
            }
            #close_button {
                background-color: #2196F3;
                color: white;
            }
        """)
    
    def detect_social_networks(self):
        """Détecte les réseaux sociaux et robots disponibles"""
        networks = {
            "bon": {
                "name": "Facebook",
                "json_structure": {
                    "data.json": {
                        "posts": [{
                            "text": "{nom}\n\n{description}",
                            "image": "{preview_path}"
                        }],
                        "groups": ["{link}"]
                    },
                    "data1.json": {
                        "stories": [{
                            "text": "{nom}",
                            "image": "{preview_path}"
                        }]
                    }
                }
            },
            "wabon": {
                "name": "WhatsApp",
                "json_structure": {
                    "data.json": {
                        "contacts": ["{link}"],
                        "messages": ["{description}"]
                    }
                }
            },
            "instabon": {
                "name": "Instagram",
                "json_structure": {
                    "data.json": {
                        "posts": [{
                            "caption": "{nom}",
                            "image": "{preview_path}"
                        }]
                    }
                }
            }
        }
        
        detected_networks = {}
        base_path = "C:\\"
        
        for folder, config in networks.items():
            path = os.path.join(base_path, folder)
            if os.path.exists(path):
                robots = [d for d in os.listdir(path) 
                         if os.path.isdir(os.path.join(path, d)) and d.startswith("robot")]
                if robots:
                    detected_networks[path] = {
                        "name": config["name"],
                        "robots": sorted(robots),
                        "json_structure": config["json_structure"]
                    }
        
        return detected_networks
    
    def setup_network_robot_selection(self, layout):
        """Configure la sélection du réseau social et du robot"""
        group = QGroupBox("Sélection du Robot")
        form = QFormLayout()
        
        # Sélection réseau social
        self.network_combo = QComboBox()
        self.network_combo.addItem("Choisissez un réseau social")
        
        # Sélection robot
        self.robot_combo = QComboBox()
        self.robot_combo.addItem("Choisissez un robot")
        
        # Remplissage des combobox
        self.network_paths = []
        for path, data in self.social_networks.items():
            self.network_combo.addItem(data["name"])
            self.network_paths.append(path)
        
        # Connexions des signaux
        self.network_combo.currentIndexChanged.connect(self.update_robots)
        self.robot_combo.currentIndexChanged.connect(self.load_robot_data)
        
        form.addRow("Réseau social:", self.network_combo)
        form.addRow("Robot:", self.robot_combo)
        group.setLayout(form)
        layout.addWidget(group)
    
    def update_robots(self, index):
        """Met à jour la liste des robots selon le réseau sélectionné"""
        self.robot_combo.clear()
        self.robot_combo.addItem("Choisissez un robot")
        
        if index == 0:
            return
            
        self.current_network = self.network_paths[index-1]
        network_data = self.social_networks[self.current_network]
        
        for robot in network_data["robots"]:
            self.robot_combo.addItem(robot)
    
    def setup_category_selection(self, layout):
        """Configure la sélection des catégories"""
        # Catégories médias
        media_group = QGroupBox("Catégories de Médias")
        media_layout = QVBoxLayout()
        self.media_list = QListWidget()
        self.media_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_media_categories()
        media_layout.addWidget(self.media_list)
        media_group.setLayout(media_layout)
        layout.addWidget(media_group)
        
        # Catégories groupes
        group_group = QGroupBox("Catégories de Groupes")
        group_layout = QVBoxLayout()
        self.group_list = QListWidget()
        self.group_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_group_categories()
        group_layout.addWidget(self.group_list)
        group_group.setLayout(group_layout)
        layout.addWidget(group_group)
    
    def setup_data_editor(self, layout):
        """Configure l'éditeur de données"""
        group = QGroupBox("Édition des Données")
        vbox = QVBoxLayout()
        
        # Onglets pour chaque fichier JSON
        self.tabs = QTabWidget()
        
        # Création dynamique des onglets
        self.json_editors = {}
        if self.current_network:
            network_data = self.social_networks[self.current_network]
            for json_file in network_data["json_structure"]:
                tab = QWidget()
                editor = QTextEdit()
                editor.setFont(QFont("Consolas", 10))
                self.json_editors[json_file] = editor
                
                layout = QVBoxLayout()
                layout.addWidget(editor)
                tab.setLayout(layout)
                self.tabs.addTab(tab, json_file)
        
        vbox.addWidget(self.tabs)
        group.setLayout(vbox)
        layout.addWidget(group)
    
    def setup_action_buttons(self, layout):
        """Configure les boutons d'action"""
        hbox = QHBoxLayout()
        
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))
        self.cancel_button.clicked.connect(self.reject)
        
        self.close_button = QPushButton("Fermer")
        self.close_button.setObjectName("close_button")
        self.close_button.setIcon(QIcon("icons/close.png"))
        self.close_button.clicked.connect(self.close)
        
        self.send_button = QPushButton("Envoyer au Robot")
        self.send_button.setObjectName("send_button")
        self.send_button.setIcon(QIcon("icons/send.png"))
        self.send_button.clicked.connect(self.send_to_robot)
        
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        hbox.addWidget(self.close_button)
        hbox.addWidget(self.send_button)
        
        layout.addLayout(hbox)
    
    def load_media_categories(self):
        """Charge les catégories de médias depuis la base"""
        self.cursor.execute("SELECT id, name FROM category WHERE est_supprime = 0")
        for cat_id, cat_name in self.cursor.fetchall():
            item = QListWidgetItem(cat_name)
            item.setData(Qt.UserRole, cat_id)
            self.media_list.addItem(item)
    
    def load_group_categories(self):
        """Charge les catégories de groupes depuis la base"""
        self.cursor.execute("SELECT id, name FROM category_group WHERE est_supprime = 0")
        for cat_id, cat_name in self.cursor.fetchall():
            item = QListWidgetItem(cat_name)
            item.setData(Qt.UserRole, cat_id)
            self.group_list.addItem(item)
    
    def load_robot_data(self, index):
        """Charge les données du robot sélectionné"""
        if index == 0 or not self.current_network:
            return
            
        self.current_robot = self.robot_combo.currentText()
        network_data = self.social_networks[self.current_network]
        
        # Mise à jour des onglets
        self.tabs.clear()
        self.json_editors = {}
        
        for json_file, structure in network_data["json_structure"].items():
            tab = QWidget()
            editor = QTextEdit()
            editor.setFont(QFont("Consolas", 10))
            self.json_editors[json_file] = editor
            
            # Charger le fichier s'il existe
            json_path = os.path.join(self.current_network, self.current_robot, json_file)
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        editor.setPlainText(json.dumps(data, indent=4, ensure_ascii=False))
                    except:
                        editor.setPlainText("Fichier JSON invalide")
            else:
                # Nouvelle structure vide
                editor.setPlainText(json.dumps(structure, indent=4, ensure_ascii=False))
            
            layout = QVBoxLayout()
            layout.addWidget(editor)
            tab.setLayout(layout)
            self.tabs.addTab(tab, json_file)
    
    def send_to_robot(self):
        """Envoie les données au robot"""
        if not self.current_network or not self.current_robot:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un réseau et un robot")
            return
            
        # Récupérer les sélections
        media_cats = [item.data(Qt.UserRole) for item in self.media_list.selectedItems()]
        group_cats = [item.data(Qt.UserRole) for item in self.group_list.selectedItems()]
        
        if not media_cats and not group_cats:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner au moins une catégorie")
            return
        
        # Récupérer les données de la base
        media_data = self.get_media_data(media_cats)
        group_data = self.get_group_data(group_cats)
        
        # Préparer les dossiers
        robot_path = os.path.join(self.current_network, self.current_robot)
        os.makedirs(robot_path, exist_ok=True)
        
        # Sauvegarder chaque fichier JSON
        network_data = self.social_networks[self.current_network]
        
        for json_file, editor in self.json_editors.items():
            try:
                # Archiver l'ancien fichier
                self.archive_file(robot_path, json_file)
                
                # Sauvegarder le nouveau
                json_path = os.path.join(robot_path, json_file)
                with open(json_path, 'w', encoding='utf-8') as f:
                    # Remplacer les placeholders avec les vraies données
                    content = self.generate_content(
                        json.loads(editor.toPlainText()),
                        media_data,
                        group_data
                    )
                    json.dump(content, f, indent=4, ensure_ascii=False)
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur avec {json_file}: {str(e)}")
                continue
        
        # Cacher le dossier
        self.hide_folder(robot_path)
        
        # Confirmation
        self.show_confirmation()
    
    def generate_content(self, template, media_data, group_data):
        """Génère le contenu final en remplaçant les placeholders"""
        if isinstance(template, list):
            return [self.generate_content(item, media_data, group_data) for item in template]
        elif isinstance(template, dict):
            return {k: self.generate_content(v, media_data, group_data) for k, v in template.items()}
        elif isinstance(template, str):
            # Remplacer les médias
            for media in media_data:
                template = template.replace("{nom}", media[1]).replace("{description}", media[2]).replace("{preview_path}", media[3])
            # Remplacer les groupes
            for group in group_data:
                template = template.replace("{link}", group[2])
            return template
        else:
            return template
    
    def archive_file(self, folder, filename):
        """Archive un fichier existant avec timestamp"""
        file_path = os.path.join(folder, filename)
        if os.path.exists(file_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = os.path.join(folder, f"{os.path.splitext(filename)[0]}_{timestamp}.json")
            os.rename(file_path, archive_path)
    
    def hide_folder(self, path):
        """Cache le dossier avec attributs système"""
        if os.path.exists(path):
            try:
                ctypes.windll.kernel32.SetFileAttributesW(path, 0x02 | 0x04)
            except:
                pass
    
    def show_confirmation(self):
        """Affiche le message de confirmation avec option de test"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Succès")
        msg.setText("Données envoyées avec succès au robot !")
        
        test_btn = msg.addButton("Tester le Robot", QMessageBox.ActionRole)
        test_btn.setIcon(QIcon("icons/test.png"))
        
        ok_btn = msg.addButton(QMessageBox.Ok)
        ok_btn.setText("Continuer")
        
        msg.exec_()
        
        if msg.clickedButton() == test_btn:
            self.test_robot()
    
    def test_robot(self):
        """Lance le test du robot"""
        QMessageBox.information(self, "Test Robot", 
                              f"Test du robot {self.current_robot} en cours...")
    
    def get_media_data(self, category_ids):
        """Récupère les médias des catégories sélectionnées"""
        if not category_ids:
            return []
            
        query = """
            SELECT id, nom, description, preview_path 
            FROM media 
            WHERE category_id IN ({}) AND est_supprime = 0
        """.format(",".join("?" * len(category_ids)))
        self.cursor.execute(query, category_ids)
        return self.cursor.fetchall()
    
    def get_group_data(self, category_ids):
        """Récupère les groupes des catégories sélectionnées"""
        if not category_ids:
            return []
            
        query = """
            SELECT id, name, link, remarks 
            FROM groups 
            WHERE category_group_id IN ({}) AND est_supprime = 0
        """.format(",".join("?" * len(category_ids)))
        self.cursor.execute(query, category_ids)
        return self.cursor.fetchall()
    
    def closeEvent(self, event):
        """Ferme proprement la connexion à la base"""
        self.conn.close()
        event.accept()


import os
import sqlite3
import json
import ctypes
from datetime import datetime
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
                            QListWidgetItem, QPushButton, QMessageBox, QComboBox, 
                            QTextEdit, QTabWidget, QWidget, QGroupBox, QFormLayout)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class UpdateRobotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Robot Manager Pro")
        self.setWindowIcon(QIcon("icons/robot.png"))
        self.setFixedSize(1000, 750)
        
        # Connexion à la base de données
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        
        # Détection des réseaux sociaux et robots disponibles
        self.social_networks = self.detect_social_networks()
        self.current_network = None
        self.current_robot = None
        
        # Layout principal
        main_layout = QVBoxLayout()
        
        # 1. Sélection du réseau social et robot
        self.setup_network_robot_selection(main_layout)
        
        # 2. Sélection des catégories (en ligne)
        categories_layout = QHBoxLayout()
        self.setup_category_selection(categories_layout)
        main_layout.addLayout(categories_layout)
        
        # 3. Visualisation et édition des données
        self.setup_data_editor(main_layout)
        
        # 4. Boutons d'action
        self.setup_action_buttons(main_layout)
        
        self.setLayout(main_layout)
        self.setup_styles()
    
    def setup_styles(self):
        """Configure les styles CSS modernes"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial;
            }
            QGroupBox {
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
                color: #333;
            }
            QListWidget {
                background: white;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QTextEdit {
                background: white;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Consolas';
                font-size: 12px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 120px;
            }
            QComboBox {
                padding: 6px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                min-width: 200px;
            }
            QLabel {
                color: #444;
                font-size: 14px;
            }
            #send_button {
                background-color: #4CAF50;
                color: white;
            }
            #cancel_button {
                background-color: #f44336;
                color: white;
            }
            #close_button {
                background-color: #2196F3;
                color: white;
            }
        """)
    
    def detect_social_networks(self):
        """Détecte les réseaux sociaux et robots disponibles"""
        networks = {
            "bon": {
                "name": "Facebook",
                "json_structure": {
                    "data.json": {
                        "posts": [{
                            "text": "{nom}\n\n{description}",
                            "image": "{preview_path}"
                        }],
                        "groups": ["{link}"]
                    },
                    "data1.json": {
                        "stories": [{
                            "text": "{nom}",
                            "image": "{preview_path}"
                        }]
                    }
                }
            },
            "wabon": {
                "name": "WhatsApp",
                "json_structure": {
                    "data.json": {
                        "contacts": ["{link}"],
                        "messages": ["{description}"]
                    }
                }
            },
            "instabon": {
                "name": "Instagram",
                "json_structure": {
                    "data.json": {
                        "posts": [{
                            "caption": "{nom}",
                            "image": "{preview_path}"
                        }]
                    }
                }
            }
        }
        
        detected_networks = {}
        base_path = "C:\\"
        
        for folder, config in networks.items():
            path = os.path.join(base_path, folder)
            if os.path.exists(path):
                robots = [d for d in os.listdir(path) 
                         if os.path.isdir(os.path.join(path, d)) and d.startswith("robot")]
                if robots:
                    detected_networks[path] = {
                        "name": config["name"],
                        "robots": sorted(robots),
                        "json_structure": config["json_structure"]
                    }
        
        return detected_networks
    
    def setup_network_robot_selection(self, layout):
        """Configure la sélection du réseau social et du robot"""
        group = QGroupBox("Sélection du Robot")
        form = QFormLayout()
        
        # Sélection réseau social
        self.network_combo = QComboBox()
        self.network_combo.addItem("Choisissez un réseau social")
        
        # Sélection robot
        self.robot_combo = QComboBox()
        self.robot_combo.addItem("Choisissez un robot")
        
        # Remplissage des combobox
        self.network_paths = []
        for path, data in self.social_networks.items():
            self.network_combo.addItem(data["name"])
            self.network_paths.append(path)
        
        # Connexions des signaux
        self.network_combo.currentIndexChanged.connect(self.update_robots)
        self.robot_combo.currentIndexChanged.connect(self.load_robot_data)
        
        form.addRow("Réseau social:", self.network_combo)
        form.addRow("Robot:", self.robot_combo)
        group.setLayout(form)
        layout.addWidget(group)
    
    def update_robots(self, index):
        """Met à jour la liste des robots selon le réseau sélectionné"""
        self.robot_combo.clear()
        self.robot_combo.addItem("Choisissez un robot")
        
        if index == 0:
            return
            
        self.current_network = self.network_paths[index-1]
        network_data = self.social_networks[self.current_network]
        
        for robot in network_data["robots"]:
            self.robot_combo.addItem(robot)
    
    def setup_category_selection(self, layout):
        """Configure la sélection des catégories"""
        # Catégories médias
        media_group = QGroupBox("Catégories de Médias")
        media_layout = QVBoxLayout()
        self.media_list = QListWidget()
        self.media_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_media_categories()
        media_layout.addWidget(self.media_list)
        media_group.setLayout(media_layout)
        layout.addWidget(media_group)
        
        # Catégories groupes
        group_group = QGroupBox("Catégories de Groupes")
        group_layout = QVBoxLayout()
        self.group_list = QListWidget()
        self.group_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_group_categories()
        group_layout.addWidget(self.group_list)
        group_group.setLayout(group_layout)
        layout.addWidget(group_group)
    
    def setup_data_editor(self, layout):
        """Configure l'éditeur de données"""
        group = QGroupBox("Édition des Données")
        vbox = QVBoxLayout()
        
        # Onglets pour chaque fichier JSON
        self.tabs = QTabWidget()
        self.json_editors = {}
        
        vbox.addWidget(self.tabs)
        group.setLayout(vbox)
        layout.addWidget(group)
    
    def setup_action_buttons(self, layout):
        """Configure les boutons d'action"""
        hbox = QHBoxLayout()
        
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))
        self.cancel_button.clicked.connect(self.reject)
        
        self.close_button = QPushButton("Fermer")
        self.close_button.setObjectName("close_button")
        self.close_button.setIcon(QIcon("icons/close.png"))
        self.close_button.clicked.connect(self.close)
        
        self.send_button = QPushButton("Envoyer au Robot")
        self.send_button.setObjectName("send_button")
        self.send_button.setIcon(QIcon("icons/send.png"))
        self.send_button.clicked.connect(self.send_to_robot)
        
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        hbox.addWidget(self.close_button)
        hbox.addWidget(self.send_button)
        
        layout.addLayout(hbox)
    
    def load_media_categories(self):
        """Charge les catégories de médias depuis la base"""
        self.cursor.execute("SELECT id, name FROM category")
        for cat_id, cat_name in self.cursor.fetchall():
            item = QListWidgetItem(cat_name)
            item.setData(Qt.UserRole, cat_id)
            self.media_list.addItem(item)
    
    def load_group_categories(self):
        """Charge les catégories de groupes depuis la base"""
        self.cursor.execute("SELECT id, name FROM category_group")
        for cat_id, cat_name in self.cursor.fetchall():
            item = QListWidgetItem(cat_name)
            item.setData(Qt.UserRole, cat_id)
            self.group_list.addItem(item)
    
    def load_robot_data(self, index):
        """Charge les données du robot sélectionné"""
        if index == 0 or not self.current_network:
            return
            
        self.current_robot = self.robot_combo.currentText()
        network_data = self.social_networks[self.current_network]
        
        # Mise à jour des onglets
        self.tabs.clear()
        self.json_editors = {}
        
        for json_file, structure in network_data["json_structure"].items():
            tab = QWidget()
            editor = QTextEdit()
            editor.setFont(QFont("Consolas", 10))
            self.json_editors[json_file] = editor
            
            # Charger le fichier s'il existe
            json_path = os.path.join(self.current_network, self.current_robot, json_file)
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        editor.setPlainText(json.dumps(data, indent=4, ensure_ascii=False))
                    except:
                        editor.setPlainText("Fichier JSON invalide")
            else:
                # Nouvelle structure vide
                editor.setPlainText(json.dumps(structure, indent=4, ensure_ascii=False))
            
            layout = QVBoxLayout()
            layout.addWidget(editor)
            tab.setLayout(layout)
            self.tabs.addTab(tab, json_file)
    
    def send_to_robot(self):
        """Envoie les données au robot"""
        if not self.current_network or not self.current_robot:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un réseau et un robot")
            return
            
        # Récupérer les sélections
        media_cats = [item.data(Qt.UserRole) for item in self.media_list.selectedItems()]
        group_cats = [item.data(Qt.UserRole) for item in self.group_list.selectedItems()]
        
        if not media_cats and not group_cats:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner au moins une catégorie")
            return
        
        # Récupérer les données de la base
        media_data = self.get_media_data(media_cats)
        group_data = self.get_group_data(group_cats)
        
        # Préparer les dossiers
        robot_path = os.path.join(self.current_network, self.current_robot)
        os.makedirs(robot_path, exist_ok=True)
        
        # Sauvegarder chaque fichier JSON
        network_data = self.social_networks[self.current_network]
        
        for json_file, editor in self.json_editors.items():
            try:
                # Archiver l'ancien fichier
                self.archive_file(robot_path, json_file)
                
                # Sauvegarder le nouveau
                json_path = os.path.join(robot_path, json_file)
                with open(json_path, 'w', encoding='utf-8') as f:
                    # Remplacer les placeholders avec les vraies données
                    content = self.generate_content(
                        json.loads(editor.toPlainText()),
                        media_data,
                        group_data
                    )
                    json.dump(content, f, indent=4, ensure_ascii=False)
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur avec {json_file}: {str(e)}")
                continue
        
        # Cacher le dossier
        self.hide_folder(robot_path)
        
        # Confirmation
        self.show_confirmation()
    
    def generate_content(self, template, media_data, group_data):
        """Génère le contenu final en remplaçant les placeholders"""
        if isinstance(template, list):
            return [self.generate_content(item, media_data, group_data) for item in template]
        elif isinstance(template, dict):
            return {k: self.generate_content(v, media_data, group_data) for k, v in template.items()}
        elif isinstance(template, str):
            # Remplacer les médias
            for media in media_data:
                template = template.replace("{nom}", media[1]).replace("{description}", media[2]).replace("{preview_path}", media[3])
            # Remplacer les groupes
            for group in group_data:
                template = template.replace("{link}", group[2])
            return template
        else:
            return template
    
    def archive_file(self, folder, filename):
        """Archive un fichier existant avec timestamp"""
        file_path = os.path.join(folder, filename)
        if os.path.exists(file_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = os.path.join(folder, f"{os.path.splitext(filename)[0]}_{timestamp}.json")
            os.rename(file_path, archive_path)
    
    def hide_folder(self, path):
        """Cache le dossier avec attributs système"""
        if os.path.exists(path):
            try:
                ctypes.windll.kernel32.SetFileAttributesW(path, 0x02 | 0x04)
            except:
                pass
    
    def show_confirmation(self):
        """Affiche le message de confirmation avec option de test"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Succès")
        msg.setText("Données envoyées avec succès au robot !")
        
        test_btn = msg.addButton("Tester le Robot", QMessageBox.ActionRole)
        test_btn.setIcon(QIcon("icons/test.png"))
        
        ok_btn = msg.addButton(QMessageBox.Ok)
        ok_btn.setText("Continuer")
        
        msg.exec_()
        
        if msg.clickedButton() == test_btn:
            self.test_robot()
    
    def test_robot(self):
        """Lance le test du robot"""
        QMessageBox.information(self, "Test Robot", 
                              f"Test du robot {self.current_robot} en cours...")
    
    def get_media_data(self, category_ids):
        """Récupère les médias des catégories sélectionnées"""
        if not category_ids:
            return []
            
        query = """
            SELECT id, nom, description, preview_path 
            FROM media 
            WHERE category_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        self.cursor.execute(query, category_ids)
        return self.cursor.fetchall()
    
    def get_group_data(self, category_ids):
        """Récupère les groupes des catégories sélectionnées"""
        if not category_ids:
            return []
            
        query = """
            SELECT id, name, link, remarks 
            FROM groups 
            WHERE category_group_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        self.cursor.execute(query, category_ids)
        return self.cursor.fetchall()
    
    def closeEvent(self, event):
        """Ferme proprement la connexion à la base"""
        self.conn.close()
        event.accept()



    def send_to_robot(self):
        """Envoie les données au robot dans le format exact demandé"""
        if not self.current_network or not self.current_robot:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un réseau et un robot")
            return
            
        # Récupérer les sélections
        media_cats = [item.data(Qt.UserRole) for item in self.media_list.selectedItems()]
        group_cats = [item.data(Qt.UserRole) for item in self.group_list.selectedItems()]
        
        if not media_cats and not group_cats:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner au moins une catégorie")
            return
        
        # Récupérer les données de la base
        media_data = self.get_formatted_media_data(media_cats)
        group_data = self.get_formatted_group_data(group_cats)
        
        # Préparer les dossiers
        robot_path = os.path.join(self.current_network, self.current_robot)
        os.makedirs(robot_path, exist_ok=True)
        
        # Créer les structures JSON exactes comme demandé
        data_json = {
            "posts": media_data,
            "groups": group_data
        }
        
        data1_json = {
            "posts": [{
                "text": media['nom'],  # Juste le nom pour data1.json
                "image": media['preview_path']
            } for media in self.get_raw_media_data(media_cats)],
            "groups": group_data  # Même structure de groupes
        }
        
        # Sauvegarder les fichiers
        try:
            # Archiver les anciens fichiers
            self.archive_file(robot_path, "data.json")
            self.archive_file(robot_path, "data1.json")
            
            # Enregistrer data.json
            with open(os.path.join(robot_path, "data.json"), 'w', encoding='utf-8') as f:
                json.dump(data_json, f, indent=4, ensure_ascii=False)
            
            # Enregistrer data1.json
            with open(os.path.join(robot_path, "data1.json"), 'w', encoding='utf-8') as f:
                json.dump(data1_json, f, indent=4, ensure_ascii=False)
            
            # Cacher le dossier
            self.hide_folder(robot_path)
            
            # Message de confirmation
            self.show_confirmation()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement: {str(e)}")

    def get_formatted_media_data(self, category_ids):
        """Récupère les médias formatés exactement comme demandé pour data.json"""
        if not category_ids:
            return []
        
        query = """
            SELECT m.nom, m.description, m.preview_path, mt.type
            FROM media m
            JOIN media_type mt ON m.type_id = mt.id
            WHERE m.category_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        
        self.cursor.execute(query, category_ids)
        media_items = self.cursor.fetchall()
        
        formatted_media = []
        for nom, description, preview_path, media_type in media_items:
            # Formatage exact comme dans votre exemple
            formatted_media.append({
                "text": f"{nom}\n\n{description}",
                "image": preview_path
            })
        
        return formatted_media

    def get_raw_media_data(self, category_ids):
        """Récupère les données brutes des médias pour data1.json"""
        if not category_ids:
            return []
        
        query = """
            SELECT m.nom, m.preview_path
            FROM media m
            WHERE m.category_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        
        self.cursor.execute(query, category_ids)
        return [{"nom": nom, "preview_path": preview_path} 
                for nom, preview_path in self.cursor.fetchall()]

    def get_formatted_group_data(self, category_ids):
        """Récupère les liens de groupes formatés"""
        if not category_ids:
            return []
        
        query = """
            SELECT link 
            FROM groups 
            WHERE category_group_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        
        self.cursor.execute(query, category_ids)
        return [link for (link,) in self.cursor.fetchall()]

    def archive_file(self, folder, filename):
        """Archive un fichier existant avec la date"""
        file_path = os.path.join(folder, filename)
        if os.path.exists(file_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"{filename.split('.')[0]}_{timestamp}.json"
            os.rename(file_path, os.path.join(folder, archive_name))

    def hide_folder(self, path):
        """Cache le dossier du robot"""
        if os.path.exists(path):
            try:
                ctypes.windll.kernel32.SetFileAttributesW(path, 0x02 | 0x04)
            except:
                pass

    def show_confirmation(self):
        """Affiche un message de confirmation stylé avec option de test"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Succès")
        msg.setText("Les données ont été envoyées avec succès !")
        
        # Bouton de test
        test_btn = msg.addButton("Tester le Robot", QMessageBox.ActionRole)
        test_btn.setIcon(QIcon("icons/test.png"))
        
        # Bouton OK
        ok_btn = msg.addButton(QMessageBox.Ok)
        ok_btn.setText("Continuer")
        
        # Style du message
        msg.setStyleSheet("""
            QMessageBox {
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLabel {
                color: #333;
            }
        """)
        
        msg.exec_()
        
        if msg.clickedButton() == test_btn:
            self.test_robot()

    def test_robot(self):
        """Teste le robot sélectionné"""
        QMessageBox.information(self, "Test", 
                            f"Fonction de test pour {self.current_robot} à implémenter")







    def send_to_robot(self):
        """Envoie les données au robot dans les formats exacts demandés"""
        if not self.current_network or not self.current_robot:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un réseau et un robot")
            return
            
        # Récupérer les sélections
        media_cats = [item.data(Qt.UserRole) for item in self.media_list.selectedItems()]
        group_cats = [item.data(Qt.UserRole) for item in self.group_list.selectedItems()]
        
        if not media_cats and not group_cats:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner au moins une catégorie")
            return
        
        # Récupérer les données formatées
        media_data = self.get_media_data(media_cats)
        group_data = self.get_group_data(group_cats)
        
        # Préparer les dossiers
        robot_path = os.path.join(self.current_network, self.current_robot)
        os.makedirs(robot_path, exist_ok=True)
        
        # Format pour data.json (original)
        data_json = {
            "posts": [{
                "text": f"{media[1]}\n\n{media[2]}",
                "image": media[3]
            } for media in media_data],
            "groups": group_data
        }
        
        # Nouveau format exact pour data1.json
        data1_json = {
            "posts": [self.generate_arabic_english_post(media) for media in media_data],
            "images": [media[3] for media in media_data],  # Toutes les images
            "groups": group_data
        }
        
        # Sauvegarder les fichiers
        try:
            # Archiver les anciens fichiers
            self.archive_file(robot_path, "data.json")
            self.archive_file(robot_path, "data1.json")
            
            # Enregistrer data.json
            with open(os.path.join(robot_path, "data.json"), 'w', encoding='utf-8') as f:
                json.dump(data_json, f, indent=4, ensure_ascii=False)
            
            # Enregistrer data1.json
            with open(os.path.join(robot_path, "data1.json"), 'w', encoding='utf-8') as f:
                json.dump(data1_json, f, indent=4, ensure_ascii=False)
            
            # Cacher le dossier
            self.hide_folder(robot_path)
            
            # Message de confirmation
            self.show_confirmation()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement: {str(e)}")

    def generate_arabic_english_post(self, media):
        """Génère le texte de post bilingue arabe/anglais"""
        nom = media[1]
        description = media[2]
        preview_path = media[3]
        
        # Exemple de template bilingue - à adapter avec vos données réelles
        return (
            f"{nom}\n\n"
            f"{description}\n\n"
            "شحن سريع إلى العالم العربي مباشرة من تركيا.\n"
            f"WhatsApp: https://wa.me/+905432103215\n"
            f"Email: contact@example.com\n"
            f"Website: https://www.example.com\n\n"
            "Fast shipping to the Arab world directly from Turkey.\n"
            f"WhatsApp: https://wa.me/+905432103215\n"
            f"Email: contact@example.com\n"
            f"Website: https://www.example.com\n\n"
            "#hydraulic #machinery #صناعة_تركية"
        )

    def get_media_data(self, category_ids):
        """Récupère les médias depuis la base de données"""
        if not category_ids:
            return []
        
        query = """
            SELECT id, nom, description, preview_path, type_id 
            FROM media 
            WHERE category_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        
        self.cursor.execute(query, category_ids)
        return self.cursor.fetchall()

    def get_group_data(self, category_ids):
        """Récupère les liens de groupes"""
        if not category_ids:
            return []
        
        query = """
            SELECT link 
            FROM groups 
            WHERE category_group_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        
        self.cursor.execute(query, category_ids)
        return [link for (link,) in self.cursor.fetchall()]





    def send_to_robot(self):
        """Version corrigée qui génère les fichiers JSON comme demandé"""
        try:
            # Vérification de sélection
            if self.robot_combo.currentIndex() == 0:
                raise Exception("Veuillez sélectionner un robot")
                
            # Récupération des IDs sélectionnés
            media_cats = [item.data(Qt.UserRole) for item in self.media_list.selectedItems()]
            group_cats = [item.data(Qt.UserRole) for item in self.group_list.selectedItems()]
            
            if not media_cats and not group_cats:
                raise Exception("Veuillez sélectionner au moins une catégorie")

            # 1. Récupération des données depuis la base
            media_data = self.get_complete_media_data(media_cats)
            group_links = self.get_group_links(group_cats)
            
            # 2. Préparation des structures JSON
            data_json = {
                "posts": [{
                    "text": f"{item['nom']}\n\n{item['description']}",
                    "image": item['preview_path']
                } for item in media_data],
                "groups": group_links
            }
            
            data1_json = {
                "posts": [self.generate_bilingual_post(item) for item in media_data],
                "images": [item['preview_path'] for item in media_data],
                "groups": group_links
            }
            
            # 3. Enregistrement des fichiers
            robot_path = os.path.join(self.current_network, self.current_robot)
            os.makedirs(robot_path, exist_ok=True)
            
            # Archive les anciens fichiers
            self.archive_existing_files(robot_path)
            
            # Enregistre les nouveaux fichiers
            with open(os.path.join(robot_path, "data.json"), 'w', encoding='utf-8') as f:
                json.dump(data_json, f, indent=4, ensure_ascii=False)
                
            with open(os.path.join(robot_path, "data1.json"), 'w', encoding='utf-8') as f:
                json.dump(data1_json, f, indent=4, ensure_ascii=False)
            
            # Cache le dossier
            self.set_hidden_attribute(robot_path)
            
            # Confirmation
            self.show_success_message()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de l'envoi: {str(e)}")

    def get_complete_media_data(self, category_ids):
        """Récupère TOUS les champs nécessaires depuis la table media"""
        if not category_ids:
            return []
        
        query = f"""
            SELECT 
                m.id,
                m.nom,
                m.description,
                m.preview_path,
                m.contact_info,
                m.whatsapp_link,
                m.website_url,
                c.name as category_name
            FROM media m
            JOIN category c ON m.category_id = c.id
            WHERE m.category_id IN ({','.join('?'*len(category_ids))})
        """
        
        self.cursor.execute(query, category_ids)
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def get_group_links(self, category_ids):
        """Récupère uniquement les liens des groupes"""
        if not category_ids:
            return []
        
        query = f"""
            SELECT link FROM groups 
            WHERE category_group_id IN ({','.join('?'*len(category_ids))})
        """
        self.cursor.execute(query, category_ids)
        return [row[0] for row in self.cursor.fetchall()]

    def generate_bilingual_post(self, media_item):
        """Génère le texte bilingue arabe/anglais avec tous les détails"""
        return (
            f"{media_item['nom']}\n\n"
            f"{media_item['description']}\n\n"
            f"شحن سريع إلى العالم العربي مباشرة من تركيا.\n"
            f"واتساب: {media_item['whatsapp_link']}\n"
            f"البريد الإلكتروني: {media_item['contact_info']}\n"
            f"الموقع: {media_item['website_url']}\n\n"
            f"Fast shipping to the Arab world directly from Turkey.\n"
            f"WhatsApp: {media_item['whatsapp_link']}\n"
            f"Email: {media_item['contact_info']}\n"
            f"Website: {media_item['website_url']}\n\n"
            "#hydraulic #machinery #صناعة_تركية"
        )

    def archive_existing_files(self, folder):
        """Archive les fichiers existants avec un timestamp"""
        for filename in ["data.json", "data1.json"]:
            path = os.path.join(folder, filename)
            if os.path.exists(path):
                new_name = f"{filename.split('.')[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                os.rename(path, os.path.join(folder, new_name))

    def set_hidden_attribute(self, path):
        """Définit les attributs cachés sur le dossier"""
        try:
            ctypes.windll.kernel32.SetFileAttributesW(path, 2)
        except:
            pass

    def show_success_message(self):
        """Affiche un message de confirmation moderne"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Succès")
        msg.setText("Les données ont été envoyées avec succès!")
        
        test_btn = msg.addButton("Tester le Robot", QMessageBox.ActionRole)
        test_btn.setIcon(QIcon("icons/test.png"))
        
        msg.addButton(QMessageBox.Ok)
        msg.exec_()
        
        if msg.clickedButton() == test_btn:
            self.test_robot()






    def send_to_robot(self):
        """Version finale adaptée à votre schéma exact"""
        try:
            # Vérifications
            if not self.current_network or self.robot_combo.currentIndex() == 0:
                raise Exception("Veuillez sélectionner un réseau social et un robot")

            media_cats = [item.data(Qt.UserRole) for item in self.media_list.selectedItems()]
            group_cats = [item.data(Qt.UserRole) for item in self.group_list.selectedItems()]

            if not media_cats and not group_cats:
                raise Exception("Veuillez sélectionner au moins une catégorie")

            # 1. Récupération des données
            media_data = self.get_media_data(media_cats)
            group_links = self.get_group_links(group_cats)

            # 2. Préparation des contacts (à adapter selon votre DB)
            contact_info = "contact@example.com"  # Valeur par défaut
            whatsapp_link = "https://wa.me/+905123456789"  # Valeur par défaut
            website_url = "https://www.example.com"  # Valeur par défaut

            # 3. Génération des JSON
            data_json = {
                "posts": [{
                    "text": f"{m['nom']}\n\n{m['description']}",
                    "image": m['preview_path']
                } for m in media_data],
                "groups": group_links
            }

            data1_json = {
                "posts": [
                    f"{m['nom']}\n\n{m['description']}\n\n"
                    f"شحن سريع إلى العالم العربي مباشرة من تركيا.\n"
                    f"واتساب: {whatsapp_link}\n"
                    f"البريد الإلكتروني: {contact_info}\n"
                    f"الموقع: {website_url}\n\n"
                    f"Fast shipping to the Arab world directly from Turkey.\n"
                    f"WhatsApp: {whatsapp_link}\n"
                    f"Email: {contact_info}\n"
                    f"Website: {website_url}\n\n"
                    "#hydraulic #machinery #صناعة_تركية"
                    for m in media_data
                ],
                "images": [m['preview_path'] for m in media_data],
                "groups": group_links
            }

            # 4. Sauvegarde
            robot_path = os.path.join(self.current_network, self.current_robot)
            os.makedirs(robot_path, exist_ok=True)

            with open(os.path.join(robot_path, "data.json"), 'w', encoding='utf-8') as f:
                json.dump(data_json, f, indent=4, ensure_ascii=False)

            with open(os.path.join(robot_path, "data1.json"), 'w', encoding='utf-8') as f:
                json.dump(data1_json, f, indent=4, ensure_ascii=False)

            # 5. Confirmation
            QMessageBox.information(self, "Succès", "Données envoyées avec succès!")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {str(e)}")

    def get_media_data(self, category_ids):
        """Récupère les médias selon votre schéma exact"""
        if not category_ids:
            return []

        query = f"""
            SELECT 
                m.id,
                m.nom,
                m.description,
                m.preview_path,
                mt.type as media_type
            FROM media m
            JOIN media_type mt ON m.type_id = mt.id
            WHERE m.category_id IN ({','.join('?'*len(category_ids))})
        """
        self.cursor.execute(query, category_ids)
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def get_group_links(self, category_ids):
        """Récupère les liens de groupes"""
        if not category_ids:
            return []

        query = f"""
            SELECT link FROM groups 
            WHERE category_group_id IN ({','.join('?'*len(category_ids))})
            AND link IS NOT NULL
        """
        self.cursor.execute(query, category_ids)
        return [row[0] for row in self.cursor.fetchall() if row[0]]




    def send_to_robot(self):
        """Version finale testée et corrigée"""
        try:
            # 1. Vérifications initiales
            if not self.current_network or self.robot_combo.currentIndex() == 0:
                raise Exception("Sélectionnez un réseau social et un robot")

            # 2. Récupération des sélections
            selected_media_cats = [item.data(Qt.UserRole) for item in self.media_list.selectedItems()]
            selected_group_cats = [item.data(Qt.UserRole) for item in self.group_list.selectedItems()]

            if not selected_media_cats and not selected_group_cats:
                raise Exception("Sélectionnez au moins une catégorie")

            # 3. DEBUG: Vérification des catégories sélectionnées
            print(f"Catégories médias sélectionnées: {selected_media_cats}")
            print(f"Catégories groupes sélectionnées: {selected_group_cats}")

            # 4. Récupération des données
            media_data = self.get_filtered_media_data(selected_media_cats)
            group_links = self.get_unique_group_links(selected_group_cats)

            # 5. DEBUG: Vérification des données récupérées
            print(f"{len(media_data)} médias trouvés")
            print(f"{len(group_links)} groupes uniques trouvés")

            # 6. Préparation des contacts (à adapter)
            CONTACT_INFO = "contact@example.com"
            WHATSAPP_LINK = "https://wa.me/+905123456789"
            WEBSITE_URL = "https://www.example.com"

            # 7. Génération des JSON
            data_json = {
                "posts": [{
                    "text": f"{m['nom']}\n\n{m['description']}" if m['description'] else m['nom'],
                    "image": m['preview_path']
                } for m in media_data],
                "groups": group_links
            }

            data1_json = {
                "posts": [
                    f"{m['nom']}\n\n{m['description']}\n\n"  # Partie française/anglaise
                    f"شحن سريع إلى العالم العربي مباشرة من تركيا.\n"
                    f"واتساب: {WHATSAPP_LINK}\n"
                    f"البريد الإلكتروني: {CONTACT_INFO}\n"
                    f"الموقع: {WEBSITE_URL}\n\n"
                    f"Fast shipping to the Arab world directly from Turkey.\n"
                    f"WhatsApp: {WHATSAPP_LINK}\n"
                    f"Email: {CONTACT_INFO}\n"
                    f"Website: {WEBSITE_URL}\n\n"
                    "#hydraulic #machinery #صناعة_تركية"
                    for m in media_data
                ],
                "images": [m['preview_path'] for m in media_data],
                "groups": group_links
            }

            # 8. Enregistrement
            robot_path = os.path.join(self.current_network, self.current_robot)
            os.makedirs(robot_path, exist_ok=True)

            with open(os.path.join(robot_path, "data.json"), 'w', encoding='utf-8') as f:
                json.dump(data_json, f, indent=4, ensure_ascii=False)

            with open(os.path.join(robot_path, "data1.json"), 'w', encoding='utf-8') as f:
                json.dump(data1_json, f, indent=4, ensure_ascii=False)

            # 9. Confirmation
            QMessageBox.information(self, "Succès", 
                                f"Données envoyées:\n- {len(media_data)} médias\n- {len(group_links)} groupes")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de l'envoi:\n{str(e)}")
            import traceback
            traceback.print_exc()

    def get_filtered_media_data(self, category_ids):
        """Récupère les médias avec vérification approfondie"""
        if not category_ids:
            return []

        query = f"""
            SELECT 
                m.id,
                m.nom,
                COALESCE(m.description, '') as description,
                m.preview_path
            FROM media m
            WHERE m.category_id IN ({','.join('?'*len(category_ids))})
            AND m.preview_path IS NOT NULL
            AND m.preview_path != ''
        """
        
        self.cursor.execute(query, category_ids)
        columns = [desc[0] for desc in self.cursor.description]
        media = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        
        # Vérification supplémentaire des chemins d'accès
        return [m for m in media if os.path.exists(m['preview_path'])]

    def get_unique_group_links(self, category_ids):
        """Récupère les liens de groupes sans doublons"""
        if not category_ids:
            return []

        query = f"""
            SELECT DISTINCT link 
            FROM groups 
            WHERE category_group_id IN ({','.join('?'*len(category_ids))})
            AND link IS NOT NULL
            AND link != ''
        """
        self.cursor.execute(query, category_ids)
        return [row[0] for row in self.cursor.fetchall()]










    def send_to_robot(self):
        """Version finale testée qui fonctionne avec votre schéma de base"""
        try:
            # 1. Vérification des sélections
            if not self.has_valid_selections():
                return

            # 2. Récupération des IDs sélectionnés
            media_cat_ids = [item.data(Qt.UserRole) for item in self.media_list.selectedItems()]
            group_cat_ids = [item.data(Qt.UserRole) for item in self.group_list.selectedItems()]

            # 3. Récupération des données
            media_data = self.get_complete_media_data(media_cat_ids)
            group_data = self.get_valid_group_links(group_cat_ids)

            # 4. DEBUG: Affichage des données récupérées
            print(f"Médias trouvés: {len(media_data)}")
            print(f"Groupes trouvés: {len(group_data)}")

            # 5. Génération des JSON
            data_json = {
                "posts": self.format_posts_for_data(media_data),
                "groups": group_data
            }

            data1_json = {
                "posts": self.format_posts_for_data1(media_data),
                "images": [m['preview_path'] for m in media_data],
                "groups": group_data
            }

            # 6. Enregistrement
            self.save_robot_files(data_json, data1_json)

            # 7. Confirmation
            self.show_success_message(len(media_data), len(group_data))

        except Exception as e:
            self.show_error_message(e)

    def has_valid_selections(self):
        """Vérifie que les sélections sont valides"""
        if not self.current_network or self.robot_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un réseau social et un robot")
            return False
            
        if not self.media_list.selectedItems() and not self.group_list.selectedItems():
            QMessageBox.warning(self, "Erreur", "Sélectionnez au moins une catégorie")
            return False
            
        return True



    def get_complete_media_data(self, category_ids):
        """Récupère TOUS les médias valides pour les catégories sélectionnées (non supprimées)"""
        if not category_ids:
            print("Aucune catégorie sélectionnée.")
            return []

        placeholders = ','.join('?' for _ in category_ids)

        query = f"""
            SELECT 
                m.id,
                m.nom,
                COALESCE(m.description, '') as description,
                m.preview_path,
                m.type_id,
                m.category_id,
                c.name as category_name,
                c.label as category_label
            FROM media m
            INNER JOIN category c ON m.category_id = c.id
            WHERE m.category_id IN ({placeholders})
            AND m.est_supprime = 0
            AND m.preview_path IS NOT NULL
            AND m.preview_path != ''
        """

        try:
            self.cursor.execute(query, category_ids)
            rows = self.cursor.fetchall()

            if not rows:
                print("⚠️ Aucun média trouvé dans la base de données pour les catégories fournies.")
                return []

            columns = [desc[0] for desc in self.cursor.description]
            media_items = [dict(zip(columns, row)) for row in rows]

            print(f"✅ Médias trouvés en base : {len(media_items)}")

            # Vérification de l'existence des fichiers
            valid_media = []
            for media in media_items:
                if os.path.exists(media['preview_path']):
                    valid_media.append(media)
                else:
                    print(f"❌ Fichier introuvable : {media['preview_path']} (media id: {media['id']})")

            print(f"✅ Médias valides (fichiers existants) : {len(valid_media)}")

            if not valid_media:
                print("⚠️ Tous les chemins de preview sont invalides ou les fichiers sont absents.")

            return valid_media

        except Exception as e:
            print(f"❌ Erreur lors de l'exécution de la requête : {e}")
            return []








    def get_valid_group_links(self, category_ids):
        """Récupère les liens de groupes uniques et valides"""
        if not category_ids:
            return []

        query = f"""
            SELECT DISTINCT g.link 
            FROM groups g
            WHERE g.category_group_id IN ({','.join('?'*len(category_ids))})
            AND g.link IS NOT NULL
            AND g.link != ''
        """
        self.cursor.execute(query, category_ids)
        return [row[0] for row in self.cursor.fetchall()]

    def format_posts_for_data(self, media_data):
        """Formatage pour data.json"""
        return [{
            "text": f"{item['nom']}\n\n{item['description']}".strip(),
            "image": item['preview_path']
        } for item in media_data]

    def format_posts_for_data1(self, media_data):
        """Formatage bilingue pour data1.json"""
        posts = []
        for item in media_data:
            post_text = (
                f"{item['nom']}\n\n{item['description']}\n\n"
                f"شحن سريع إلى العالم العربي مباشرة من تركيا.\n"
                f"واتساب: https://wa.me/+905123456789\n"
                f"البريد الإلكتروني: contact@example.com\n"
                f"الموقع: https://www.example.com\n\n"
                f"Fast shipping to the Arab world directly from Turkey.\n"
                f"WhatsApp: https://wa.me/+905123456789\n"
                f"Email: contact@example.com\n"
                f"Website: https://www.example.com\n\n"
                "#hydraulic #machinery #صناعة_تركية"
            )
            posts.append(post_text.strip())
        return posts

    def save_robot_files(self, data_json, data1_json):
        """Enregistre les fichiers JSON dans le dossier du robot"""
        robot_path = os.path.join(self.current_network, self.current_robot)
        os.makedirs(robot_path, exist_ok=True)

        # Archive les anciens fichiers
        for fname in ['data.json', 'data1.json']:
            if os.path.exists(os.path.join(robot_path, fname)):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                os.rename(
                    os.path.join(robot_path, fname),
                    os.path.join(robot_path, f"{fname.split('.')[0]}_{timestamp}.json")
                )

        # Enregistre les nouveaux fichiers
        with open(os.path.join(robot_path, 'data.json'), 'w', encoding='utf-8') as f:
            json.dump(data_json, f, indent=4, ensure_ascii=False)

        with open(os.path.join(robot_path, 'data1.json'), 'w', encoding='utf-8') as f:
            json.dump(data1_json, f, indent=4, ensure_ascii=False)

        # Cache le dossier
        try:
            ctypes.windll.kernel32.SetFileAttributesW(robot_path, 2)
        except:
            pass

    def show_success_message(self, media_count, group_count):
        """Affiche un message de confirmation détaillé"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Succès")
        msg.setText(
            f"Données envoyées avec succès!\n\n"
            f"- Médias envoyés: {media_count}\n"
            f"- Groupes envoyés: {group_count}"
        )
        
        test_btn = msg.addButton("Tester le Robot", QMessageBox.ActionRole)
        test_btn.setIcon(QIcon("icons/test.png"))
        
        msg.addButton(QMessageBox.Ok)
        msg.exec_()
        
        if msg.clickedButton() == test_btn:
            self.test_robot()

    def show_error_message(self, error):
        """Affiche un message d'erreur détaillé"""
        QMessageBox.critical(
            self, 
            "Erreur", 
            f"Une erreur est survenue:\n{str(error)}\n\n"
            "Vérifiez que:\n"
            "- Les catégories sélectionnées contiennent des médias\n"
            "- Les chemins des médias sont valides"
        )
        import traceback
        traceback.print_exc()



class UpdateRobotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Robot Manager Pro")
        self.setWindowIcon(QIcon("icons/robot.png"))
        self.setFixedSize(1000, 750)
        
        # Connexion à la base de données
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        
        # Détection des réseaux sociaux et robots disponibles
        self.social_networks = self.detect_social_networks()
        self.current_network = None
        self.current_robot = None
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # 1. Sélection du réseau social et robot (maintenant sur une seule ligne)
        self.setup_network_robot_selection(main_layout)
        
        # 2. Sélection des catégories (en ligne)
        categories_layout = QHBoxLayout()
        categories_layout.setSpacing(20)
        self.setup_category_selection(categories_layout)
        main_layout.addLayout(categories_layout)
        
        # 3. Visualisation et édition des données
        self.setup_data_editor(main_layout)
        
        # 4. Boutons d'action
        self.setup_action_buttons(main_layout)
        
        self.setLayout(main_layout)
        self.setup_styles()


    
    def detect_social_networks(self):
        """Détecte les réseaux sociaux et robots disponibles"""
        networks = {
            "bon": {
                "name": "Facebook",
                "json_structure": {
                    "data.json": {
                        "posts": [{
                            "text": "{nom}\n\n{description}",
                            "image": "{preview_path}"
                        }],
                        "groups": ["{link}"]
                    },
                    "data1.json": {
                        "stories": [{
                            "text": "{nom}",
                            "image": "{preview_path}"
                        }]
                    }
                }
            },
            "wabon": {
                "name": "WhatsApp",
                "json_structure": {
                    "data.json": {
                        "contacts": ["{link}"],
                        "messages": ["{description}"]
                    }
                }
            },
            "instabon": {
                "name": "Instagram",
                "json_structure": {
                    "data.json": {
                        "posts": [{
                            "caption": "{nom}",
                            "image": "{preview_path}"
                        }]
                    }
                }
            }
        }
        
        detected_networks = {}
        base_path = "C:\\"
        
        for folder, config in networks.items():
            path = os.path.join(base_path, folder)
            if os.path.exists(path):
                robots = [d for d in os.listdir(path) 
                         if os.path.isdir(os.path.join(path, d)) and d.startswith("robot")]
                if robots:
                    detected_networks[path] = {
                        "name": config["name"],
                        "robots": sorted(robots),
                        "json_structure": config["json_structure"]
                    }
        
        return detected_networks
    
    def setup_styles(self):
        """Configure les styles CSS modernes"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial;
            }
            QGroupBox {
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                padding-bottom: 10px;
                font-weight: bold;
                color: #333;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QListWidget {
                background: white;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QTextEdit {
                background: white;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Consolas';
                font-size: 12px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 120px;
                border: none;
            }
            QComboBox {
                padding: 6px 12px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                min-width: 200px;
                height: 32px;
            }
            QLabel {
                color: #444;
                font-size: 14px;
            }
            #send_button {
                background-color: #4CAF50;
                color: white;
            }
            #send_button:hover {
                background-color: #45a049;
            }
            #cancel_button {
                background-color: #f44336;
                color: white;
            }
            #cancel_button:hover {
                background-color: #d32f2f;
            }
            #close_button {
                background-color: #2196F3;
                color: white;
            }
            #close_button:hover {
                background-color: #0b7dda;
            }
            QTabWidget::pane {
                border: 1px solid #dcdcdc;
                border-radius: 5px;
            }
            QTabBar::tab {
                padding: 8px 12px;
                background: #e9e9e9;
                border: 1px solid #dcdcdc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #2196F3;
            }
        """)
    
    def setup_network_robot_selection(self, layout):
        """Configure la sélection du réseau social et du robot sur une seule ligne"""
        group = QGroupBox("Sélection du Robot")
        hbox = QHBoxLayout()
        hbox.setSpacing(20)
        
        # Sélection réseau social
        network_label = QLabel("Réseau social:")
        self.network_combo = QComboBox()
        self.network_combo.addItem("Choisissez un réseau social")
        
        # Sélection robot
        robot_label = QLabel("Robot:")
        self.robot_combo = QComboBox()
        self.robot_combo.addItem("Choisissez un robot")
        
        # Remplissage des combobox
        self.network_paths = []
        for path, data in self.social_networks.items():
            self.network_combo.addItem(data["name"])
            self.network_paths.append(path)
        
        # Connexions des signaux
        self.network_combo.currentIndexChanged.connect(self.update_robots)
        self.robot_combo.currentIndexChanged.connect(self.load_robot_data)
        
        # Ajout des widgets dans un layout horizontal
        hbox.addWidget(network_label)
        hbox.addWidget(self.network_combo, 1)
        hbox.addWidget(robot_label)
        hbox.addWidget(self.robot_combo, 1)
        hbox.addStretch()
        
        group.setLayout(hbox)
        layout.addWidget(group)
    
    def update_robots(self, index):
        """Met à jour la liste des robots selon le réseau sélectionné"""
        self.robot_combo.clear()
        self.robot_combo.addItem("Choisissez un robot")
        
        if index == 0:
            self.current_network = None
            self.update_send_button_text()
            return
            
        self.current_network = self.network_paths[index-1]
        network_data = self.social_networks[self.current_network]
        
        for robot in network_data["robots"]:
            self.robot_combo.addItem(robot)
        
        self.update_send_button_text()
    
    def update_send_button_text(self):
        """Met à jour le texte du bouton d'envoi selon le réseau sélectionné"""
        if self.current_network and self.robot_combo.currentIndex() > 0:
            network_name = self.social_networks[self.current_network]["name"]
            self.send_button.setText(f"Envoyer vers {network_name}")
        else:
            self.send_button.setText("Envoyer au Robot")


    
    def load_media_categories(self):
        """Charge les catégories de médias depuis la base"""
        self.cursor.execute("SELECT id, name FROM category")
        for cat_id, cat_name in self.cursor.fetchall():
            item = QListWidgetItem(cat_name)
            item.setData(Qt.UserRole, cat_id)
            self.media_list.addItem(item)


    def setup_category_selection(self, layout):
        """Configure la sélection des catégories"""
        # Catégories médias
        media_group = QGroupBox("Catégories de Médias")
        media_layout = QVBoxLayout()
        self.media_list = QListWidget()
        self.media_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_media_categories()
        media_layout.addWidget(self.media_list)
        media_group.setLayout(media_layout)
        layout.addWidget(media_group, 1)
        
        # Catégories groupes
        group_group = QGroupBox("Catégories de Groupes")
        group_layout = QVBoxLayout()
        self.group_list = QListWidget()
        self.group_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_group_categories()
        group_layout.addWidget(self.group_list)
        group_group.setLayout(group_layout)
        layout.addWidget(group_group, 1)
    
    def load_group_categories(self):
        """Charge les catégories de groupes depuis la base"""
        self.cursor.execute("SELECT id, name FROM category_group")
        for cat_id, cat_name in self.cursor.fetchall():
            item = QListWidgetItem(cat_name)
            item.setData(Qt.UserRole, cat_id)
            self.group_list.addItem(item)

    def setup_data_editor(self, layout):
        """Configure l'éditeur de données"""
        group = QGroupBox("Édition des Données")
        vbox = QVBoxLayout()
        
        # Onglets pour chaque fichier JSON
        self.tabs = QTabWidget()
        self.json_editors = {}
        
        vbox.addWidget(self.tabs)
        group.setLayout(vbox)
        layout.addWidget(group, 1)
    
    def setup_action_buttons(self, layout):
        """Configure les boutons d'action"""
        hbox = QHBoxLayout()
        hbox.setSpacing(15)
        
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))
        self.cancel_button.clicked.connect(self.reject)
        
        self.close_button = QPushButton("Fermer")
        self.close_button.setObjectName("close_button")
        self.close_button.setIcon(QIcon("icons/close.png"))
        self.close_button.clicked.connect(self.close)
        
        self.send_button = QPushButton("Envoyer au Robot")
        self.send_button.setObjectName("send_button")
        self.send_button.setIcon(QIcon("icons/send.png"))
        self.send_button.clicked.connect(self.send_to_robot)
        
        hbox.addWidget(self.cancel_button)
        hbox.addStretch(1)
        hbox.addWidget(self.close_button)
        hbox.addWidget(self.send_button)
        
        layout.addLayout(hbox)
    
    def load_robot_data(self, index):
        """Charge les données du robot sélectionné"""
        if index == 0 or not self.current_network:
            self.current_robot = None
            self.update_send_button_text()
            return
            
        self.current_robot = self.robot_combo.currentText()
        self.update_send_button_text()
        
        network_data = self.social_networks[self.current_network]
        
        # Mise à jour des onglets
        self.tabs.clear()
        self.json_editors = {}
        
        for json_file, structure in network_data["json_structure"].items():
            tab = QWidget()
            editor = QTextEdit()
            editor.setFont(QFont("Consolas", 10))
            self.json_editors[json_file] = editor
            
            # Charger le fichier s'il existe
            json_path = os.path.join(self.current_network, self.current_robot, json_file)
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        editor.setPlainText(json.dumps(data, indent=4, ensure_ascii=False))
                    except:
                        editor.setPlainText("Fichier JSON invalide")
            else:
                # Nouvelle structure vide
                editor.setPlainText(json.dumps(structure, indent=4, ensure_ascii=False))
            
            layout = QVBoxLayout()
            layout.addWidget(editor)
            tab.setLayout(layout)
            self.tabs.addTab(tab, json_file)
    
    def send_to_robot(self):
        """Version finale testée qui fonctionne avec votre schéma de base"""
        try:
            # 1. Vérification des sélections
            if not self.has_valid_selections():
                return

            # 2. Récupération des IDs sélectionnés
            media_cat_ids = [item.data(Qt.UserRole) for item in self.media_list.selectedItems()]
            group_cat_ids = [item.data(Qt.UserRole) for item in self.group_list.selectedItems()]

            # 3. Récupération des données
            media_data = self.get_complete_media_data(media_cat_ids)
            group_data = self.get_valid_group_links(group_cat_ids)

            # 4. DEBUG: Affichage des données récupérées
            print(f"Médias trouvés: {len(media_data)}")
            print(f"Groupes trouvés: {len(group_data)}")

            # 5. Génération des JSON
            data_json = {
                "posts": self.format_posts_for_data(media_data),
                "groups": group_data
            }

            data1_json = {
                "posts": self.format_posts_for_data1(media_data),
                "images": [m['preview_path'] for m in media_data],
                "groups": group_data
            }

            # 6. Enregistrement
            self.save_robot_files(data_json, data1_json)

            # 7. Confirmation
            self.show_success_message(len(media_data), len(group_data))

        except Exception as e:
            self.show_error_message(e)

    def has_valid_selections(self):
        """Vérifie que les sélections sont valides"""
        if not self.current_network or self.robot_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un réseau social et un robot")
            return False
            
        if not self.media_list.selectedItems() and not self.group_list.selectedItems():
            QMessageBox.warning(self, "Erreur", "Sélectionnez au moins une catégorie")
            return False
            
        return True

    def get_complete_media_data(self, category_ids):
        """Récupère TOUS les médias valides pour les catégories sélectionnées (non supprimées)"""
        if not category_ids:
            print("Aucune catégorie sélectionnée.")
            return []

        placeholders = ','.join('?' for _ in category_ids)

        query = f"""
            SELECT 
                m.id,
                m.nom,
                COALESCE(m.description, '') as description,
                m.preview_path,
                m.type_id,
                m.category_id,
                c.name as category_name,
                c.label as category_label
            FROM media m
            INNER JOIN category c ON m.category_id = c.id
            WHERE m.category_id IN ({placeholders})
            AND m.est_supprime = 0
            AND m.preview_path IS NOT NULL
            AND m.preview_path != ''
        """

        try:
            self.cursor.execute(query, category_ids)
            rows = self.cursor.fetchall()

            if not rows:
                print("⚠️ Aucun média trouvé dans la base de données pour les catégories fournies.")
                return []

            columns = [desc[0] for desc in self.cursor.description]
            media_items = [dict(zip(columns, row)) for row in rows]

            print(f"✅ Médias trouvés en base : {len(media_items)}")

            # Vérification de l'existence des fichiers
            valid_media = []
            for media in media_items:
                if os.path.exists(media['preview_path']):
                    valid_media.append(media)
                else:
                    print(f"❌ Fichier introuvable : {media['preview_path']} (media id: {media['id']})")

            print(f"✅ Médias valides (fichiers existants) : {len(valid_media)}")

            if not valid_media:
                print("⚠️ Tous les chemins de preview sont invalides ou les fichiers sont absents.")

            return valid_media

        except Exception as e:
            print(f"❌ Erreur lors de l'exécution de la requête : {e}")
            return []

    def get_valid_group_links(self, category_ids):
        """Récupère les liens de groupes uniques et valides"""
        if not category_ids:
            return []

        query = f"""
            SELECT DISTINCT g.link 
            FROM groups g
            WHERE g.category_group_id IN ({','.join('?'*len(category_ids))})
            AND g.link IS NOT NULL
            AND g.link != ''
        """
        self.cursor.execute(query, category_ids)
        return [row[0] for row in self.cursor.fetchall()]

    def format_posts_for_data(self, media_data):
        """Formatage pour data.json"""
        return [{
            "text": f"{item['nom']}\n\n{item['description']}".strip(),
            "image": item['preview_path']
        } for item in media_data]

    def format_posts_for_data1(self, media_data):
        """Formatage bilingue pour data1.json"""
        posts = []
        for item in media_data:
            post_text = (
                f"{item['nom']}\n\n{item['description']}\n\n"
                f"شحن سريع إلى العالم العربي مباشرة من تركيا.\n"
                f"واتساب: https://wa.me/+905123456789\n"
                f"البريد الإلكتروني: contact@example.com\n"
                f"الموقع: https://www.example.com\n\n"
                f"Fast shipping to the Arab world directly from Turkey.\n"
                f"WhatsApp: https://wa.me/+905123456789\n"
                f"Email: contact@example.com\n"
                f"Website: https://www.example.com\n\n"
                "#hydraulic #machinery #صناعة_تركية"
            )
            posts.append(post_text.strip())
        return posts

    def save_robot_files(self, data_json, data1_json):
        """Enregistre les fichiers JSON dans le dossier du robot"""
        robot_path = os.path.join(self.current_network, self.current_robot)
        os.makedirs(robot_path, exist_ok=True)

        # Archive les anciens fichiers
        for fname in ['data.json', 'data1.json']:
            if os.path.exists(os.path.join(robot_path, fname)):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                os.rename(
                    os.path.join(robot_path, fname),
                    os.path.join(robot_path, f"{fname.split('.')[0]}_{timestamp}.json")
                )

        # Enregistre les nouveaux fichiers
        with open(os.path.join(robot_path, 'data.json'), 'w', encoding='utf-8') as f:
            json.dump(data_json, f, indent=4, ensure_ascii=False)

        with open(os.path.join(robot_path, 'data1.json'), 'w', encoding='utf-8') as f:
            json.dump(data1_json, f, indent=4, ensure_ascii=False)

        # Cache le dossier
        try:
            ctypes.windll.kernel32.SetFileAttributesW(robot_path, 2)
        except:
            pass

    def show_success_message(self, media_count, group_count):
        """Affiche un message de confirmation détaillé"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Succès")
        msg.setText(
            f"Données envoyées avec succès!\n\n"
            f"- Médias envoyés: {media_count}\n"
            f"- Groupes envoyés: {group_count}"
        )
        
        test_btn = msg.addButton("Tester le Robot", QMessageBox.ActionRole)
        test_btn.setIcon(QIcon("icons/test.png"))
        
        msg.addButton(QMessageBox.Ok)
        msg.exec_()
        
        if msg.clickedButton() == test_btn:
            self.test_robot()

    def show_error_message(self, error):
        """Affiche un message d'erreur détaillé"""
        QMessageBox.critical(
            self, 
            "Erreur", 
            f"Une erreur est survenue:\n{str(error)}\n\n"
            "Vérifiez que:\n"
            "- Les catégories sélectionnées contiennent des médias\n"
            "- Les chemins des médias sont valides"
        )
        import traceback
        traceback.print_exc()

    def closeEvent(self, event):
        """Ferme proprement la connexion à la base"""
        self.conn.close()
        event.accept()






class UpdateRobotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Robot Manager Pro"))
        self.setWindowIcon(QIcon("icons/robot.png"))
        self.setFixedSize(1000, 750)
        
        # Database connection
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        
        # Detect available social networks
        self.social_networks = self.detect_social_networks()
        self.current_network = None
        self.current_robot = None
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # 1. Network and robot selection (single line)
        self.setup_network_robot_selection(main_layout)
        
        # 2. Categories selection
        categories_layout = QHBoxLayout()
        categories_layout.setSpacing(20)
        self.setup_category_selection(categories_layout)
        main_layout.addLayout(categories_layout)
        
        # 3. Data editor
        self.setup_data_editor(main_layout)
        
        # 4. Action buttons
        self.setup_action_buttons(main_layout)
        
        self.setLayout(main_layout)
        self.setup_styles()
    def detect_social_networks(self):
        """Détecte les réseaux sociaux et robots disponibles"""
        networks = {
            "bon": {
                "name": "Facebook",
                "json_structure": {
                    "data.json": {
                        "posts": [{
                            "text": "{nom}\n\n{description}",
                            "image": "{preview_path}"
                        }],
                        "groups": ["{link}"]
                    },
                    "data1.json": {
                        "stories": [{
                            "text": "{nom}",
                            "image": "{preview_path}"
                        }]
                    }
                }
            },
            "wabon": {
                "name": "WhatsApp",
                "json_structure": {
                    "data.json": {
                        "contacts": ["{link}"],
                        "messages": ["{description}"]
                    }
                }
            },
            "instabon": {
                "name": "Instagram",
                "json_structure": {
                    "data.json": {
                        "posts": [{
                            "caption": "{nom}",
                            "image": "{preview_path}"
                        }]
                    }
                }
            }
        }
        
        detected_networks = {}
        base_path = "C:\\"
        
        for folder, config in networks.items():
            path = os.path.join(base_path, folder)
            if os.path.exists(path):
                robots = [d for d in os.listdir(path) 
                         if os.path.isdir(os.path.join(path, d)) and d.startswith("robot")]
                if robots:
                    detected_networks[path] = {
                        "name": config["name"],
                        "robots": sorted(robots),
                        "json_structure": config["json_structure"]
                    }
        
        return detected_networks
        
    def tr(self, text):
        """Translation method (can be connected to actual translation system)"""
        return text
    
    def setup_styles(self):
        """Configure modern CSS styles"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial;
            }
            QGroupBox {
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                padding-bottom: 10px;
                font-weight: bold;
                color: #333;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QListWidget {
                background: white;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QTextEdit {
                background: white;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Consolas';
                font-size: 12px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 120px;
                border: none;
            }
            QComboBox {
                padding: 6px 12px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                min-width: 200px;
                height: 32px;
            }
            QLabel {
                color: #444;
                font-size: 14px;
            }
            #send_button {
                background-color: #4CAF50;
                color: white;
            }
            #send_button:hover {
                background-color: #45a049;
            }
            #cancel_button {
                background-color: #f44336;
                color: white;
            }
            #cancel_button:hover {
                background-color: #d32f2f;
            }
            #close_button {
                background-color: #2196F3;
                color: white;
            }
            #close_button:hover {
                background-color: #0b7dda;
            }
            QTabWidget::pane {
                border: 1px solid #dcdcdc;
                border-radius: 5px;
            }
            QTabBar::tab {
                padding: 8px 12px;
                background: #e9e9e9;
                border: 1px solid #dcdcdc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #2196F3;
            }
        """)
    
    def setup_network_robot_selection(self, layout):
        """Setup network and robot selection on single line"""
        group = QGroupBox(self.tr("Robot Selection"))
        hbox = QHBoxLayout()
        hbox.setSpacing(20)
        
        # Network selection
        network_label = QLabel(self.tr("Social Network:"))
        self.network_combo = QComboBox()
        self.network_combo.addItem(self.tr("Select a social network"))
        
        # Robot selection
        robot_label = QLabel(self.tr("Robot:"))
        self.robot_combo = QComboBox()
        self.robot_combo.addItem(self.tr("Select a robot"))
        
        # Fill comboboxes
        self.network_paths = []
        for path, data in self.social_networks.items():
            self.network_combo.addItem(data["name"])
            self.network_paths.append(path)
        
        # Connect signals
        self.network_combo.currentIndexChanged.connect(self.update_robots)
        self.robot_combo.currentIndexChanged.connect(self.load_robot_data)
        
        # Add widgets to horizontal layout
        hbox.addWidget(network_label)
        hbox.addWidget(self.network_combo, 1)
        hbox.addWidget(robot_label)
        hbox.addWidget(self.robot_combo, 1)
        hbox.addStretch()
        
        group.setLayout(hbox)
        layout.addWidget(group)
    
    def update_robots(self, index):
        """Update robots list based on selected network"""
        self.robot_combo.clear()
        self.robot_combo.addItem(self.tr("Select a robot"))
        
        if index == 0:
            self.current_network = None
            self.update_send_button_text()
            return
            
        self.current_network = self.network_paths[index-1]
        network_data = self.social_networks[self.current_network]
        
        for robot in network_data["robots"]:
            self.robot_combo.addItem(robot)
        
        self.update_send_button_text()
    
    def update_send_button_text(self):
        """Update send button text based on selected network"""
        if self.current_network and self.robot_combo.currentIndex() > 0:
            network_name = self.social_networks[self.current_network]["name"]
            self.send_button.setText(self.tr(f"Send to {network_name}"))
        else:
            self.send_button.setText(self.tr("Send to Robot"))
    
    def setup_category_selection(self, layout):
        """Setup categories selection"""
        # Media categories
        media_group = QGroupBox(self.tr("Media Categories"))
        media_layout = QVBoxLayout()
        self.media_list = QListWidget()
        self.media_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_media_categories()
        media_layout.addWidget(self.media_list)
        media_group.setLayout(media_layout)
        layout.addWidget(media_group, 1)
        
        # Group categories
        group_group = QGroupBox(self.tr("Group Categories"))
        group_layout = QVBoxLayout()
        self.group_list = QListWidget()
        self.group_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_group_categories()
        group_layout.addWidget(self.group_list)
        group_group.setLayout(group_layout)
        layout.addWidget(group_group, 1)
    
    def setup_data_editor(self, layout):
        """Setup data editor"""
        group = QGroupBox(self.tr("Data Editor"))
        vbox = QVBoxLayout()
        
        # Tabs for JSON files
        self.tabs = QTabWidget()
        self.json_editors = {}
        
        vbox.addWidget(self.tabs)
        group.setLayout(vbox)
        layout.addWidget(group, 1)
    
    def setup_action_buttons(self, layout):
        """Setup action buttons"""
        hbox = QHBoxLayout()
        hbox.setSpacing(15)
        
        self.cancel_button = QPushButton(self.tr("Cancel"))
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))
        self.cancel_button.clicked.connect(self.reject)
        
        self.close_button = QPushButton(self.tr("Close"))
        self.close_button.setObjectName("close_button")
        self.close_button.setIcon(QIcon("icons/close.png"))
        self.close_button.clicked.connect(self.close)
        
        self.send_button = QPushButton(self.tr("Send to Robot"))
        self.send_button.setObjectName("send_button")
        self.send_button.setIcon(QIcon("icons/send.png"))
        self.send_button.clicked.connect(self.execute_send_operation)
        
        hbox.addWidget(self.cancel_button)
        hbox.addStretch(1)
        hbox.addWidget(self.close_button)
        hbox.addWidget(self.send_button)
        
        layout.addLayout(hbox)
    
    def execute_send_operation(self):
        """Execute the appropriate send operation based on selected network"""
        if not self.current_network or self.robot_combo.currentIndex() == 0:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Please select a network and robot"))
            return
            
        network_name = self.social_networks[self.current_network]["name"]
        
        if network_name == "Facebook":
            self.send_to_robot_facebook()
        elif network_name == "WhatsApp":
            self.send_to_robot_whatsapp()
        elif network_name == "Instagram":
            self.send_to_robot_instagram()
        else:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Unsupported network"))
    
    def send_to_robot_facebook(self):
        """Send data to Facebook robot"""
        try:
            if not self.has_valid_selections():
                return

            media_cat_ids = [item.data(Qt.UserRole) for item in self.media_list.selectedItems()]
            group_cat_ids = [item.data(Qt.UserRole) for item in self.group_list.selectedItems()]

            media_data = self.get_complete_media_data(media_cat_ids)
            group_data = self.get_valid_group_links(group_cat_ids)

            # Facebook-specific JSON structure
            data_json = {
                "posts": self.format_posts_for_facebook(media_data),
                "groups": group_data
            }

            data1_json = {
                "stories": self.format_stories_for_facebook(media_data),
                "groups": group_data
            }

            self.save_robot_files(data_json, data1_json)
            self.show_success_message(len(media_data), len(group_data))

        except Exception as e:
            self.show_error_message(e)
    
    def send_to_robot_whatsapp(self):
        """Send data to WhatsApp robot"""
        try:
            if not self.has_valid_selections():
                return

            media_cat_ids = [item.data(Qt.UserRole) for item in self.media_list.selectedItems()]
            group_cat_ids = [item.data(Qt.UserRole) for item in self.group_list.selectedItems()]

            media_data = self.get_complete_media_data(media_cat_ids)
            group_data = self.get_valid_group_links(group_cat_ids)

            # WhatsApp-specific JSON structure
            data_json = {
                "contacts": group_data,
                "messages": [self.format_message_for_whatsapp(m) for m in media_data]
            }

            self.save_robot_files(data_json, {})
            self.show_success_message(len(media_data), len(group_data))

        except Exception as e:
            self.show_error_message(e)
    
    def send_to_robot_instagram(self):
        """Send data to Instagram robot"""
        try:
            if not self.has_valid_selections():
                return

            media_cat_ids = [item.data(Qt.UserRole) for item in self.media_list.selectedItems()]
            group_cat_ids = [item.data(Qt.UserRole) for item in self.group_list.selectedItems()]

            media_data = self.get_complete_media_data(media_cat_ids)
            group_data = self.get_valid_group_links(group_cat_ids)

            # Instagram-specific JSON structure
            data_json = {
                "posts": [self.format_post_for_instagram(m) for m in media_data],
                "stories": [self.format_story_for_instagram(m) for m in media_data],
                "hashtags": ["#insta", "#social"]
            }

            self.save_robot_files(data_json, {})
            self.show_success_message(len(media_data), len(group_data))

        except Exception as e:
            self.show_error_message(e)
    
    def format_posts_for_facebook(self, media_data):
        """Format posts for Facebook"""
        return [{
            "text": f"{item['nom']}\n\n{item['description']}".strip(),
            "image": item['preview_path'],
            "timestamp": datetime.now().isoformat()
        } for item in media_data]
    
    def format_stories_for_facebook(self, media_data):
        """Format stories for Facebook"""
        return [{
            "text": item['nom'],
            "image": item['preview_path'],
            "duration": 10
        } for item in media_data]
    
    def format_message_for_whatsapp(self, media_item):
        """Format message for WhatsApp"""
        return (
            f"{media_item['nom']}\n\n"
            f"{media_item['description']}\n\n"
            f"Contact: +123456789\n"
            f"More info: example.com"
        )
    
    def format_post_for_instagram(self, media_item):
        """Format post for Instagram"""
        return {
            "caption": f"{media_item['nom']} #insta",
            "image": media_item['preview_path'],
            "location": "Turkey"
        }
    
    def format_story_for_instagram(self, media_item):
        """Format story for Instagram"""
        return {
            "image": media_item['preview_path'],
            "duration": 7,
            "mentions": []
        }
    
    def load_robot_data(self, index):
        """Load data for selected robot"""
        if index == 0 or not self.current_network:
            self.current_robot = None
            self.update_send_button_text()
            return
            
        self.current_robot = self.robot_combo.currentText()
        self.update_send_button_text()
        
        network_data = self.social_networks[self.current_network]
        
        # Update tabs
        self.tabs.clear()
        self.json_editors = {}
        
        for json_file, structure in network_data["json_structure"].items():
            tab = QWidget()
            editor = QTextEdit()
            editor.setFont(QFont("Consolas", 10))
            self.json_editors[json_file] = editor
            
            # Load file if exists
            json_path = os.path.join(self.current_network, self.current_robot, json_file)
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        editor.setPlainText(json.dumps(data, indent=4, ensure_ascii=False))
                    except:
                        editor.setPlainText(self.tr("Invalid JSON file"))
            else:
                # New empty structure
                editor.setPlainText(json.dumps(structure, indent=4, ensure_ascii=False))
            
            layout = QVBoxLayout()
            layout.addWidget(editor)
            tab.setLayout(layout)
            self.tabs.addTab(tab, json_file)
    
    def has_valid_selections(self):
        """Check if selections are valid"""
        if not self.current_network or self.robot_combo.currentIndex() == 0:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Please select a network and robot"))
            return False
            
        if not self.media_list.selectedItems() and not self.group_list.selectedItems():
            QMessageBox.warning(self, self.tr("Error"), self.tr("Please select at least one category"))
            return False
            
        return True

    def get_complete_media_data(self, category_ids):
        """Get all valid media for selected categories"""
        if not category_ids:
            return []

        placeholders = ','.join('?' for _ in category_ids)

        query = f"""
            SELECT 
                m.id,
                m.nom,
                COALESCE(m.description, '') as description,
                m.preview_path,
                m.type_id,
                m.category_id,
                c.name as category_name,
                c.label as category_label
            FROM media m
            INNER JOIN category c ON m.category_id = c.id
            WHERE m.category_id IN ({placeholders})
            AND m.est_supprime = 0
            AND m.preview_path IS NOT NULL
            AND m.preview_path != ''
        """

        try:
            self.cursor.execute(query, category_ids)
            rows = self.cursor.fetchall()

            if not rows:
                return []

            columns = [desc[0] for desc in self.cursor.description]
            media_items = [dict(zip(columns, row)) for row in rows]

            # Verify file existence
            return [m for m in media_items if os.path.exists(m['preview_path'])]

        except Exception as e:
            print(f"Database error: {e}")
            return []

    def get_valid_group_links(self, category_ids):
        """Get unique and valid group links"""
        if not category_ids:
            return []

        query = f"""
            SELECT DISTINCT g.link 
            FROM groups g
            WHERE g.category_group_id IN ({','.join('?'*len(category_ids))})
            AND g.link IS NOT NULL
            AND g.link != ''
        """
        self.cursor.execute(query, category_ids)
        return [row[0] for row in self.cursor.fetchall()]

    def save_robot_files(self, data_json, data1_json):
        """Save JSON files to robot folder"""
        robot_path = os.path.join(self.current_network, self.current_robot)
        os.makedirs(robot_path, exist_ok=True)

        # Archive existing files
        for fname in ['data.json', 'data1.json']:
            if os.path.exists(os.path.join(robot_path, fname)):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                os.rename(
                    os.path.join(robot_path, fname),
                    os.path.join(robot_path, f"{fname.split('.')[0]}_{timestamp}.json")
                )

        # Save new files
        with open(os.path.join(robot_path, 'data.json'), 'w', encoding='utf-8') as f:
            json.dump(data_json, f, indent=4, ensure_ascii=False)

        if data1_json:  # Only save if not empty
            with open(os.path.join(robot_path, 'data1.json'), 'w', encoding='utf-8') as f:
                json.dump(data1_json, f, indent=4, ensure_ascii=False)

        # Hide folder
        try:
            ctypes.windll.kernel32.SetFileAttributesW(robot_path, 2)
        except:
            pass

    def show_success_message(self, media_count, group_count):
        """Show success message"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(self.tr("Success"))
        msg.setText(
            self.tr("Data sent successfully!\n\n"
                  "- Media sent: {}\n"
                  "- Groups sent: {}").format(media_count, group_count)
        )
        
        test_btn = msg.addButton(self.tr("Test Robot"), QMessageBox.ActionRole)
        test_btn.setIcon(QIcon("icons/test.png"))
        
        msg.addButton(QMessageBox.Ok)
        msg.exec_()
        
        if msg.clickedButton() == test_btn:
            self.test_robot()

    def show_error_message(self, error):
        """Show error message"""
        QMessageBox.critical(
            self, 
            self.tr("Error"), 
            self.tr("An error occurred:\n{}\n\n"
                  "Please verify that:\n"
                  "- Selected categories contain media\n"
                  "- Media paths are valid").format(str(error))
        )

    def test_robot(self):
        """Test robot functionality"""
        QMessageBox.information(
            self,
            self.tr("Test Robot"),
            self.tr("Testing robot {}...").format(self.current_robot)
        )

    def load_media_categories(self):
        """Load media categories from database"""
        self.cursor.execute("SELECT id, name FROM category")
        for cat_id, cat_name in self.cursor.fetchall():
            item = QListWidgetItem(self.tr(cat_name))
            item.setData(Qt.UserRole, cat_id)
            self.media_list.addItem(item)
    
    def load_group_categories(self):
        """Load group categories from database"""
        self.cursor.execute("SELECT id, name FROM category_group")
        for cat_id, cat_name in self.cursor.fetchall():
            item = QListWidgetItem(self.tr(cat_name))
            item.setData(Qt.UserRole, cat_id)
            self.group_list.addItem(item)
    
    def closeEvent(self, event):
        """Close database connection"""
        self.conn.close()
        event.accept()














class UpdateRobotDialognext(QDialog):
    """
    Boîte de dialogue pour envoyer des données au robot avec sélection des catégories.
    Design moderne avec fonctionnalités avancées et feedback visuel.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Envoyer des données au Robot")
        self.setWindowIcon(QIcon("icons/robot.png"))
        self.setMinimumSize(600, 650)  # Taille responsive
        
        # Connexion à la base de données
        self.db_path = Path(DB_PATH)
        self.conn = None
        self.cursor = None
        self._connect_db()
        
        # Configuration de l'interface
        self._setup_ui()
        self._apply_styles()
        
        # Chargement initial des données
        self.load_categories()

    def _connect_db(self):
        """Établit la connexion à la base de données avec gestion d'erreur."""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.cursor = self.conn.cursor()
            self._check_tables()
        except sqlite3.Error as e:
            QMessageBox.critical(
                self, 
                "Erreur de base de données", 
                f"Impossible de se connecter à la base de données:\n{str(e)}"
            )
            self.reject()

    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Titre avec icône
        title_layout = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(QIcon("icons/robot.png").pixmap(32, 32))
        title_layout.addWidget(title_icon)
        
        title_label = QLabel("Envoyer des données au Robot")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        main_layout.addLayout(title_layout)

        # Sélection des catégories de médias
        media_group = QVBoxLayout()
        media_group.setSpacing(8)
        
        media_label = QLabel("Catégories de médias:")
        media_label.setStyleSheet("font-weight: bold;")
        media_group.addWidget(media_label)
        
        self.media_category_list = QListWidget()
        self.media_category_list.setSelectionMode(QListWidget.MultiSelection)
        self.media_category_list.setMinimumHeight(150)
        media_group.addWidget(self.media_category_list)
        
        # Bouton sélection/désélection
        media_buttons = QHBoxLayout()
        select_all_media = QPushButton("Tout sélectionner")
        select_all_media.clicked.connect(lambda: self._select_all(self.media_category_list))
        media_buttons.addWidget(select_all_media)
        
        deselect_all_media = QPushButton("Tout désélectionner")
        deselect_all_media.clicked.connect(lambda: self._deselect_all(self.media_category_list))
        media_buttons.addWidget(deselect_all_media)
        media_group.addLayout(media_buttons)
        
        main_layout.addLayout(media_group)

        # Séparateur
        separator = QLabel()
        separator.setStyleSheet("background-color: #e2e8f0; height: 1px;")
        main_layout.addWidget(separator)

        # Sélection des catégories de groupes
        group_layout = QVBoxLayout()
        group_layout.setSpacing(8)
        
        group_label = QLabel("Catégories de groupes:")
        group_label.setStyleSheet("font-weight: bold;")
        group_layout.addWidget(group_label)
        
        self.group_category_list = QListWidget()
        self.group_category_list.setSelectionMode(QListWidget.MultiSelection)
        self.group_category_list.setMinimumHeight(150)
        group_layout.addWidget(self.group_category_list)
        
        # Bouton sélection/désélection
        group_buttons = QHBoxLayout()
        select_all_groups = QPushButton("Tout sélectionner")
        select_all_groups.clicked.connect(lambda: self._select_all(self.group_category_list))
        group_buttons.addWidget(select_all_groups)
        
        deselect_all_groups = QPushButton("Tout désélectionner")
        deselect_all_groups.clicked.connect(lambda: self._deselect_all(self.group_category_list))
        group_buttons.addWidget(deselect_all_groups)
        group_layout.addLayout(group_buttons)
        
        main_layout.addLayout(group_layout)

        # Boutons d'action
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.send_button = QPushButton("Envoyer au Robot")
        self.send_button.setIcon(QIcon("icons/send.png"))
        self.send_button.clicked.connect(self._send_to_robot)
        button_layout.addWidget(self.send_button)
        
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def _apply_styles(self):
        """Applique les styles CSS modernes avec thème robotique."""
        self.setStyleSheet("""
            QDialog {
                background-color: #f8fafc;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QListWidget {
                font-size: 14px;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                background-color: white;
                padding: 5px;
                outline: none;
            }
            
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f5f9;
            }
            
            QListWidget::item:selected {
                background-color: #e0e7ff;
                color: #1e40af;
                border-radius: 4px;
            }
            
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 6px;
                min-width: 120px;
                transition: all 0.2s;
            }
            
            #send_button {
                background-color: #4f46e5;
                color: white;
                border: none;
            }
            
            #send_button:hover {
                background-color: #4338ca;
            }
            
            #send_button:pressed {
                background-color: #3730a3;
            }
            
            #cancel_button {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #cbd5e1;
            }
            
            #cancel_button:hover {
                background-color: #e2e8f0;
            }
            
            #cancel_button:pressed {
                background-color: #cbd5e1;
            }
        """)
        
        self.send_button.setObjectName("send_button")
        self.cancel_button.setObjectName("cancel_button")

    def _check_tables(self):
        """Vérifie si les tables nécessaires existent."""
        tables = ["category", "media", "media_type", "groups"]
        for table in tables:
            self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not self.cursor.fetchone():
                raise sqlite3.OperationalError(f"Table {table} manquante")

    def load_categories(self):
        """Charge les catégories depuis la base de données."""
        try:
            self.cursor.execute("SELECT id, name, label FROM category ORDER BY name")
            categories = self.cursor.fetchall()
            
            for cat_id, name, label in categories:
                display_text = f"{label} ({name})" if label else name
                
                # Catégories médias
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, cat_id)
                self.media_category_list.addItem(item)
                
                # Catégories groupes
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, cat_id)
                self.group_category_list.addItem(item)
                
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement:\n{str(e)}")

    def _select_all(self, list_widget):
        """Sélectionne tous les éléments d'une liste."""
        for i in range(list_widget.count()):
            list_widget.item(i).setSelected(True)

    def _deselect_all(self, list_widget):
        """Désélectionne tous les éléments d'une liste."""
        list_widget.clearSelection()

    def _send_to_robot(self):
        """Gère l'envoi des données au robot avec validation."""
        media_cats = [item.data(Qt.UserRole) for item in self.media_category_list.selectedItems()]
        group_cats = [item.data(Qt.UserRole) for item in self.group_category_list.selectedItems()]

        if not media_cats and not group_cats:
            QMessageBox.warning(self, "Sélection vide", "Veuillez sélectionner au moins une catégorie")
            return

        # Confirmation avant envoi
        confirm = QMessageBox.question(
            self,
            "Confirmation",
            f"Envoyer {len(media_cats)} catégorie(s) média et {len(group_cats)} catégorie(s) groupe ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.No:
            return

        # Récupération des données
        try:
            media_data = self._get_media_data(media_cats) if media_cats else []
            group_data = self._get_group_data(group_cats) if group_cats else []
            
            # Envoi au robot (simulé ici)
            success = self._transfer_data(media_data, group_data)
            
            if success:
                QMessageBox.information(
                    self,
                    "Succès",
                    f"Données envoyées avec succès:\n"
                    f"- {len(media_data)} médias\n"
                    f"- {len(group_data)} groupes",
                    QMessageBox.Ok
                )
                self.accept()
            else:
                QMessageBox.warning(self, "Erreur", "Échec de l'envoi des données")
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'envoi:\n{str(e)}")

    def _get_media_data(self, category_ids):
        """Récupère les données médias pour les catégories sélectionnées."""
        query = """
            SELECT m.id, m.nom, m.description, m.preview_path, mt.type, c.name as category
            FROM media m
            JOIN media_type mt ON m.type_id = mt.id
            JOIN category c ON m.category_id = c.id
            WHERE m.category_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        self.cursor.execute(query, category_ids)
        return self.cursor.fetchall()

    def _get_group_data(self, category_ids):
        """Récupère les données groupes pour les catégories sélectionnées."""
        query = """
            SELECT g.id, g.link, g.remarks, g.description, g.keywords, c.name as category
            FROM groups g
            JOIN category c ON g.category_id = c.id
            WHERE g.category_id IN ({})
        """.format(",".join("?" * len(category_ids)))
        self.cursor.execute(query, category_ids)
        return self.cursor.fetchall()

    def _transfer_data(self, media_data, group_data):
        """
        Simule le transfert des données au robot.
        En production, remplacer par l'appel réel à FileTransferApp.
        """
        print(f"Transfert de {len(media_data)} médias et {len(group_data)} groupes")
        # Ici vous intégreriez FileTransferApp et FileTransferApp2
        return True  # Simule un succès

    def closeEvent(self, event):
        """Ferme proprement la connexion à la base de données."""
        if self.conn:
            self.conn.close()
        event.accept()

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QAbstractItemView, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QAbstractItemView,
                             QPushButton, QHBoxLayout, QTableWidgetItem, QMessageBox)
from PyQt5.QtGui import QIcon


class ManageCategoriesDialog(QDialog):
    """
    Boîte de dialogue pour gérer les catégories de médias avec une interface moderne.
    Permet d'ajouter, supprimer et visualiser les catégories.
    """
    
    def __init__(self, media_manager, parent=None):
        super().__init__(parent)
        self.media_manager = media_manager
        
        # Configuration de la fenêtre
        self._setup_ui()
        self._apply_styles()
        
        # Remplissage initial des catégories
        self.populate_categories()

    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        self.setWindowTitle("Gestion des catégories")
        self.setWindowIcon(QIcon("icons/category.png"))
        self.setFixedSize(800, 500)  # Taille légèrement augmentée pour meilleure lisibilité

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Configuration du tableau
        self.category_list = QTableWidget(self)
        self.category_list.setColumnCount(4)
        self.category_list.setHorizontalHeaderLabels(['ID', 'Nom', 'Libellé', 'Description'])
        self.category_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.category_list.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # Ajustement des colonnes
        self.category_list.horizontalHeader().setStretchLastSection(True)
        self.category_list.setColumnWidth(0, 80)  # ID
        self.category_list.setColumnWidth(1, 150)  # Nom
        
        main_layout.addWidget(self.category_list)

        # Boutons d'action
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.add_button = QPushButton(' Ajouter', self)
        self.add_button.setIcon(QIcon("icons/add.png"))
        self.add_button.clicked.connect(self.add_category)
        
        self.delete_button = QPushButton(' Supprimer', self)
        self.delete_button.setIcon(QIcon("icons/delete.png"))
        self.delete_button.clicked.connect(self.delete_category)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()  # Pousse les boutons à gauche

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def _apply_styles(self):
        """Applique les styles CSS modernes."""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QTableWidget {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                font-size: 14px;
                selection-background-color: #e3f2fd;
                selection-color: #000;
                gridline-color: #e5e7eb;
            }
            
            QHeaderView::section {
                background-color: #3b82f6;
                color: white;
                padding: 12px;
                font-size: 14px;
                font-weight: 500;
                border: none;
                border-radius: 0;
            }
            
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 6px;
                border: none;
                min-width: 100px;
            }
            
            QPushButton:hover {
                opacity: 0.9;
            }
            
            #add_button {
                background-color: #10b981;
                color: white;
            }
            
            #add_button:hover {
                background-color: #0d9f6e;
            }
            
            #delete_button {
                background-color: #ef4444;
                color: white;
            }
            
            #delete_button:hover {
                background-color: #dc2626;
            }
            
            QMessageBox {
                background-color: white;
            }
        """)
        
        # Application des noms d'objets pour le style spécifique
        self.add_button.setObjectName("add_button")
        self.delete_button.setObjectName("delete_button")

    def populate_categories(self):
        """Remplit la liste des catégories avec les données actuelles."""
        categories = self.media_manager.load_categories()
        self.category_list.setRowCount(len(categories))
        self.category_list.setSortingEnabled(False)  # Désactive le tri pendant le remplissage

        for row, category in enumerate(categories):
            items = [
                QTableWidgetItem(str(category['id'])),
                QTableWidgetItem(category['name']),
                QTableWidgetItem(category.get('label', '')),
                QTableWidgetItem(category.get('description', ''))
            ]
            
            # Désactivation de l'édition directe
            for item in items:
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                
            for col, item in enumerate(items):
                self.category_list.setItem(row, col, item)

        self.category_list.setSortingEnabled(True)  # Réactive le tri
        self.category_list.sortByColumn(0, Qt.AscendingOrder)  # Trie par ID

    def add_category(self):
        """Ouvre une boîte de dialogue pour ajouter une nouvelle catégorie."""
        dialog = AddCategoryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name, label, description = dialog.get_category_data()
            if not name.strip():
                QMessageBox.warning(
                    self, 
                    'Champ requis', 
                    'Le nom de la catégorie est obligatoire.',
                    QMessageBox.Ok
                )
                return
                
            try:
                self.media_manager.add_category(name, label, description)
                self.populate_categories()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Erreur',
                    f"Une erreur est survenue :\n{str(e)}",
                    QMessageBox.Ok
                )

    def delete_category(self):
        """Supprime la catégorie sélectionnée après confirmation."""
        selected_row = self.category_list.currentRow()
        if selected_row < 0:
            QMessageBox.information(
                self,
                'Aucune sélection',
                'Veuillez sélectionner une catégorie à supprimer.',
                QMessageBox.Ok
            )
            return
            
        category_id = int(self.category_list.item(selected_row, 0).text())
        
        if self.media_manager.has_media_in_category(category_id):
            QMessageBox.warning(
                self, 
                'Opération impossible', 
                'Cette catégorie contient des médias.\nVeuillez d\'abord supprimer les médias associés.',
                QMessageBox.Ok
            )
            return
            
        confirm = QMessageBox.question(
            self,
            'Confirmation',
            'Êtes-vous sûr de vouloir supprimer définitivement cette catégorie ?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                self.media_manager.delete_category(category_id)
                self.populate_categories()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Erreur',
                    f"Échec de la suppression :\n{str(e)}",
                    QMessageBox.Ok
                )

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QMessageBox
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, 
                             QDialogButtonBox, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class AddCategoryDialog(QDialog):
    """
    Boîte de dialogue pour ajouter une nouvelle catégorie avec validation des entrées.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self._setup_ui()
        self._apply_styles()
        
    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        self.setWindowTitle("Nouvelle catégorie")
        self.setWindowIcon(QIcon("icons/add.png"))
        self.setFixedSize(450, 250)  # Taille légèrement augmentée
        
        # Layout principal avec marges
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 20)
        layout.setSpacing(15)
        
        # Configuration des champs de saisie
        self._setup_input_fields(layout)
        
        # Configuration des boutons
        self._setup_buttons(layout)
        
        self.setLayout(layout)
    
    def _setup_input_fields(self, layout):
        """Configure les champs de saisie."""
        # Champ nom (obligatoire)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nom * (requis)")
        self.name_input.setToolTip("Le nom identifiant de la catégorie (champ obligatoire)")
        self.name_input.setClearButtonEnabled(True)
        
        # Champ libellé
        self.label_input = QLineEdit(self)
        self.label_input.setPlaceholderText("Libellé (affichage)")
        self.label_input.setToolTip("Nom affiché pour la catégorie (optionnel)")
        self.label_input.setClearButtonEnabled(True)
        
        # Champ description
        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Description")
        self.description_input.setToolTip("Description détaillée de la catégorie (optionnel)")
        self.description_input.setClearButtonEnabled(True)
        
        # Ajout des champs au layout
        layout.addWidget(self.name_input)
        layout.addWidget(self.label_input)
        layout.addWidget(self.description_input)
    
    def _setup_buttons(self, layout):
        """Configure les boutons de dialogue."""
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, 
            Qt.Horizontal, 
            self
        )
        
        # Personnalisation des boutons
        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setIcon(QIcon("icons/check.png"))
        ok_button.setText("Valider")
        ok_button.setObjectName("okButton")
        
        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setIcon(QIcon("icons/cancel.png"))
        cancel_button.setObjectName("cancelButton")
        
        # Connexions des signaux
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
    
    def _apply_styles(self):
        """Applique les styles CSS modernes."""
        self.setStyleSheet("""
            QDialog {
                background-color: #f8fafc;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                background-color: white;
                selection-background-color: #3b82f6;
                selection-color: white;
            }
            
            QLineEdit:focus {
                border: 1px solid #3b82f6;
                background-color: #f0f7ff;
            }
            
            QLineEdit[required="true"] {
                border-left: 3px solid #3b82f6;
            }
            
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 6px;
                border: none;
                min-width: 90px;
            }
            
            #okButton {
                background-color: #10b981;
                color: white;
            }
            
            #okButton:hover {
                background-color: #0d9f6e;
            }
            
            #okButton:pressed {
                background-color: #047857;
            }
            
            #cancelButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #cbd5e1;
            }
            
            #cancelButton:hover {
                background-color: #e2e8f0;
            }
            
            #cancelButton:pressed {
                background-color: #cbd5e1;
            }
            
            QToolTip {
                background-color: #1e293b;
                color: white;
                padding: 5px;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        
        # Marquer le champ nom comme requis pour le style
        self.name_input.setProperty("required", "true")
        self.name_input.style().polish(self.name_input)
    
    def validate_and_accept(self):
        """Valide les entrées avant d'accepter."""
        name = self.name_input.text().strip()
        
        if not name:
            self._show_error("Champ requis", "Le nom de la catégorie est obligatoire.")
            self.name_input.setFocus()
            return
        
        if len(name) > 50:
            self._show_error("Nom trop long", "Le nom ne doit pas dépasser 50 caractères.")
            return
            
        self.accept()
    
    def _show_error(self, title, message):
        """Affiche un message d'erreur stylisé."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #1e293b;
            }
        """)
        msg.exec_()
    
    def get_category_data(self):
        """
        Retourne les données saisies sous forme de tuple.
        Returns:
            tuple: (nom, libellé, description)
        """
        return (
            self.name_input.text().strip(),
            self.label_input.text().strip(),
            self.description_input.text().strip()
        ) 
    



from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QAbstractItemView, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QAbstractItemView,
                             QPushButton, QHBoxLayout, QTableWidgetItem, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class ManageTypesDialog(QDialog):
    """
    Boîte de dialogue pour gérer les types de médias avec une interface moderne.
    Permet d'ajouter, supprimer et visualiser les types de médias.
    """
    
    def __init__(self, media_manager, parent=None):
        super().__init__(parent)
        self.media_manager = media_manager
        
        # Configuration de la fenêtre
        self._setup_ui()
        self._apply_styles()
        
        # Remplissage initial des types
        self.populate_types()

    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        self.setWindowTitle("Gestion des types de médias")
        self.setWindowIcon(QIcon("icons/types.png"))
        self.setFixedSize(900, 600)  # Taille optimisée pour l'affichage

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Configuration du tableau
        self.type_list = QTableWidget(self)
        self.type_list.setColumnCount(4)
        self.type_list.setHorizontalHeaderLabels(['ID', 'Type', 'Libellé', 'Description'])
        self.type_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.type_list.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # Optimisation de l'affichage du tableau
        self.type_list.horizontalHeader().setStretchLastSection(True)
        self.type_list.setColumnWidth(0, 80)  # ID
        self.type_list.setColumnWidth(1, 150)  # Type
        self.type_list.verticalHeader().setVisible(False)
        
        main_layout.addWidget(self.type_list)

        # Boutons d'action
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.add_button = QPushButton(' Ajouter un type', self)
        self.add_button.setIcon(QIcon("icons/add.png"))
        self.add_button.clicked.connect(self.add_type)
        
        self.delete_button = QPushButton(' Supprimer', self)
        self.delete_button.setIcon(QIcon("icons/delete.png"))
        self.delete_button.clicked.connect(self.delete_type)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()  # Pousse les boutons à gauche

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def _apply_styles(self):
        """Applique les styles CSS modernes."""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QTableWidget {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                font-size: 14px;
                selection-background-color: #e3f2fd;
                selection-color: #000;
                gridline-color: #e5e7eb;
            }
            
            QHeaderView::section {
                background-color: #7c3aed;
                color: white;
                padding: 12px;
                font-size: 14px;
                font-weight: 500;
                border: none;
                border-radius: 0;
            }
            
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 6px;
                border: none;
                min-width: 120px;
            }
            
            QPushButton:hover {
                opacity: 0.9;
            }
            
            #add_button {
                background-color: #10b981;
                color: white;
            }
            
            #add_button:hover {
                background-color: #0d9f6e;
            }
            
            #delete_button {
                background-color: #ef4444;
                color: white;
            }
            
            #delete_button:hover {
                background-color: #dc2626;
            }
            
            QMessageBox {
                background-color: white;
            }
        """)
        
        # Application des noms d'objets pour le style spécifique
        self.add_button.setObjectName("add_button")
        self.delete_button.setObjectName("delete_button")

    def populate_types(self):
        """Remplit la liste des types avec les données actuelles."""
        types = self.media_manager.load_types()
        self.type_list.setRowCount(len(types))
        self.type_list.setSortingEnabled(False)  # Désactive le tri pendant le remplissage

        for row, type_ in enumerate(types):
            items = [
                QTableWidgetItem(str(type_['id'])),
                QTableWidgetItem(type_['type']),
                QTableWidgetItem(type_.get('label', '')),
                QTableWidgetItem(type_.get('description', ''))
            ]
            
            # Désactivation de l'édition directe
            for item in items:
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                
            for col, item in enumerate(items):
                self.type_list.setItem(row, col, item)

        self.type_list.setSortingEnabled(True)  # Réactive le tri
        self.type_list.sortByColumn(0, Qt.AscendingOrder)  # Trie par ID

    def add_type(self):
        """Ouvre une boîte de dialogue pour ajouter un nouveau type."""
        dialog = AddTypeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            type_, label, description = dialog.get_type_data()
            if not type_.strip():
                QMessageBox.warning(
                    self, 
                    'Champ requis', 
                    'Le type de média ne peut pas être vide.',
                    QMessageBox.Ok
                )
                return
                
            try:
                self.media_manager.add_type(type_, label, description)
                self.populate_types()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Erreur',
                    f"Une erreur est survenue :\n{str(e)}",
                    QMessageBox.Ok
                )

    def delete_type(self):
        """Supprime le type sélectionné après confirmation."""
        selected_row = self.type_list.currentRow()
        if selected_row < 0:
            QMessageBox.information(
                self,
                'Aucune sélection',
                'Veuillez sélectionner un type à supprimer.',
                QMessageBox.Ok
            )
            return
            
        type_id = int(self.type_list.item(selected_row, 0).text())
        
        if self.media_manager.has_media_in_type(type_id):
            QMessageBox.warning(
                self, 
                'Opération impossible', 
                'Ce type contient des médias.\nVeuillez d\'abord supprimer les médias associés.',
                QMessageBox.Ok
            )
            return
            
        confirm = QMessageBox.question(
            self,
            'Confirmation',
            'Êtes-vous sûr de vouloir supprimer définitivement ce type ?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                self.media_manager.delete_type(type_id)
                self.populate_types()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Erreur',
                    f"Échec de la suppression :\n{str(e)}",
                    QMessageBox.Ok
                )
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QMessageBox
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, 
                             QDialogButtonBox, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class AddTypeDialog(QDialog):
    """
    Boîte de dialogue pour ajouter un nouveau type de média avec validation des entrées.
    Style moderne cohérent avec l'application.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self._setup_ui()
        self._apply_styles()
        
    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        self.setWindowTitle("Nouveau type de média")
        self.setWindowIcon(QIcon("icons/add.png"))
        self.setFixedSize(450, 280)  # Taille légèrement augmentée
        
        # Layout principal avec marges
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 20)
        layout.setSpacing(15)
        
        # Configuration des champs de saisie
        self._setup_input_fields(layout)
        
        # Configuration des boutons
        self._setup_buttons(layout)
        
        self.setLayout(layout)
    
    def _setup_input_fields(self, layout):
        """Configure les champs de saisie avec des tooltips explicatifs."""
        # Champ type (obligatoire)
        self.type_input = QLineEdit(self)
        self.type_input.setPlaceholderText("Type * (requis)")
        self.type_input.setToolTip("Identifiant technique du type (ex: 'image', 'video')")
        self.type_input.setClearButtonEnabled(True)
        self.type_input.setProperty("required", "true")
        
        # Champ libellé
        self.label_input = QLineEdit(self)
        self.label_input.setPlaceholderText("Libellé (affichage)")
        self.label_input.setToolTip("Nom affiché pour le type (ex: 'Image', 'Vidéo')")
        self.label_input.setClearButtonEnabled(True)
        
        # Champ description
        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Description")
        self.description_input.setToolTip("Description détaillée du type de média")
        self.description_input.setClearButtonEnabled(True)
        
        # Ajout des champs au layout
        layout.addWidget(self.type_input)
        layout.addWidget(self.label_input)
        layout.addWidget(self.description_input)
    
    def _setup_buttons(self, layout):
        """Configure les boutons de dialogue avec style personnalisé."""
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, 
            Qt.Horizontal, 
            self
        )
        
        # Personnalisation des boutons
        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setIcon(QIcon("icons/check.png"))
        ok_button.setText("Valider")
        ok_button.setObjectName("okButton")
        
        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setIcon(QIcon("icons/cancel.png"))
        cancel_button.setObjectName("cancelButton")
        
        # Connexions des signaux
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
    
    def _apply_styles(self):
        """Applique les styles CSS modernes avec une touche violette."""
        self.setStyleSheet("""
            QDialog {
                background-color: #f8fafc;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                background-color: white;
                selection-background-color: #7c3aed;
                selection-color: white;
            }
            
            QLineEdit:focus {
                border: 1px solid #7c3aed;
                background-color: #f5f3ff;
            }
            
            QLineEdit[required="true"] {
                border-left: 3px solid #7c3aed;
            }
            
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 6px;
                border: none;
                min-width: 90px;
            }
            
            #okButton {
                background-color: #7c3aed;
                color: white;
            }
            
            #okButton:hover {
                background-color: #6d28d9;
            }
            
            #okButton:pressed {
                background-color: #5b21b6;
            }
            
            #cancelButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #cbd5e1;
            }
            
            #cancelButton:hover {
                background-color: #e2e8f0;
            }
            
            #cancelButton:pressed {
                background-color: #cbd5e1;
            }
            
            QToolTip {
                background-color: #1e293b;
                color: white;
                padding: 5px;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        
        # Actualise le style pour prendre en compte les propriétés
        self.type_input.style().polish(self.type_input)
    
    def validate_and_accept(self):
        """Valide les entrées avant d'accepter."""
        type_text = self.type_input.text().strip()
        
        if not type_text:
            self._show_error("Champ requis", "Le type de média est obligatoire.")
            self.type_input.setFocus()
            return
        
        if not type_text.islower() or ' ' in type_text:
            self._show_error("Format incorrect", 
                            "Le type doit être en minuscules sans espaces (ex: 'video', 'audio').")
            return
            
        if len(type_text) > 30:
            self._show_error("Trop long", 
                            "Le type ne doit pas dépasser 30 caractères.")
            return
            
        self.accept()
    
    def _show_error(self, title, message):
        """Affiche un message d'erreur stylisé."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #1e293b;
            }
        """)
        msg.exec_()
    
    def get_type_data(self):
        """
        Retourne les données saisies sous forme de tuple.
        Returns:
            tuple: (type, libellé, description)
        """
        return (
            self.type_input.text().strip().lower(),
            self.label_input.text().strip(),
            self.description_input.text().strip()
        )
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QAbstractItemView, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QAbstractItemView,
                            QPushButton, QHBoxLayout, QTableWidgetItem, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class ManageArchivesDialog(QDialog):
    """
    Boîte de dialogue pour gérer les médias archivés avec une interface moderne.
    Permet de restaurer ou supprimer définitivement des médias archivés.
    """
    
    def __init__(self, media_manager, user_choice, parent=None):
        super().__init__(parent)
        self.media_manager = media_manager
        self.user_choice = user_choice
        
        # Configuration de la fenêtre
        self._setup_ui()
        self._apply_styles()
        
        # Remplissage initial des archives
        self.populate_archives()

    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        self.setWindowTitle("Gestion des archives")
        self.setWindowIcon(QIcon("icons/archive.png"))
        self.setFixedSize(900, 600)  # Taille optimisée

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Configuration du tableau
        self.archive_list = QTableWidget(self)
        self.archive_list.setColumnCount(5)  # Ajout d'une colonne pour la date d'archivage
        self.archive_list.setHorizontalHeaderLabels(['ID', 'Nom', 'Description', 'Catégorie', 'Archivé le'])
        self.archive_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.archive_list.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # Optimisation de l'affichage du tableau
        self.archive_list.horizontalHeader().setStretchLastSection(True)
        self.archive_list.setColumnWidth(0, 80)  # ID
        self.archive_list.setColumnWidth(1, 200)  # Nom
        self.archive_list.verticalHeader().setVisible(False)
        
        main_layout.addWidget(self.archive_list)

        # Boutons d'action
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.restore_button = QPushButton(' Restaurer', self)
        self.restore_button.setIcon(QIcon("icons/restore.png"))
        self.restore_button.clicked.connect(self.restore_media)
        
        self.delete_button = QPushButton(' Supprimer définitivement', self)
        self.delete_button.setIcon(QIcon("icons/delete_forever.png"))  # Icône différente pour suppression permanente
        self.delete_button.clicked.connect(self.delete_media)
        
        button_layout.addWidget(self.restore_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()  # Pousse les boutons à gauche

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def _apply_styles(self):
        """Applique les styles CSS modernes avec thème orange/rouge."""
        self.setStyleSheet("""
            QDialog {
                background-color: #fff7ed;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QTableWidget {
                background-color: white;
                border: 1px solid #f3e8d3;
                border-radius: 8px;
                font-size: 14px;
                selection-background-color: #ffedd5;
                selection-color: #000;
                gridline-color: #f3e8d3;
            }
            
            QHeaderView::section {
                background-color: #f97316;
                color: white;
                padding: 12px;
                font-size: 14px;
                font-weight: 500;
                border: none;
                border-radius: 0;
            }
            
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 6px;
                border: none;
                min-width: 120px;
            }
            
            QPushButton:hover {
                opacity: 0.9;
            }
            
            #restore_button {
                background-color: #22c55e;
                color: white;
            }
            
            #restore_button:hover {
                background-color: #16a34a;
            }
            
            #delete_button {
                background-color: #ef4444;
                color: white;
            }
            
            #delete_button:hover {
                background-color: #dc2626;
            }
            
            QMessageBox {
                background-color: white;
            }
        """)
        
        # Application des noms d'objets pour le style spécifique
        self.restore_button.setObjectName("restore_button")
        self.delete_button.setObjectName("delete_button")

    def populate_archives(self):
        """Remplit la liste des archives avec les données actuelles."""
        archives = self.media_manager.load_archives(self.user_choice)
        self.archive_list.setRowCount(len(archives))
        self.archive_list.setSortingEnabled(False)  # Désactive le tri pendant le remplissage

        for row, archive in enumerate(archives):
            items = [
                QTableWidgetItem(str(archive['id'])),
                QTableWidgetItem(archive['nom']),
                QTableWidgetItem(archive.get('description', '')),
                QTableWidgetItem(archive.get('categorie', '')),
                QTableWidgetItem(archive.get('archived_date', 'Inconnue'))
            ]
            
            # Désactivation de l'édition directe
            for item in items:
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                
            for col, item in enumerate(items):
                self.archive_list.setItem(row, col, item)

        self.archive_list.setSortingEnabled(True)  # Réactive le tri
        self.archive_list.sortByColumn(4, Qt.DescendingOrder)  # Trie par date d'archivage récente

    def restore_media(self):
        """Restaure le média sélectionné après confirmation."""
        selected_row = self.archive_list.currentRow()
        if selected_row < 0:
            QMessageBox.information(
                self,
                'Aucune sélection',
                'Veuillez sélectionner un média à restaurer.',
                QMessageBox.Ok
            )
            return
            
        media_id = int(self.archive_list.item(selected_row, 0).text())
        media_name = self.archive_list.item(selected_row, 1).text()
        
        confirm = QMessageBox.question(
            self,
            'Confirmation de restauration',
            f'Êtes-vous sûr de vouloir restaurer "{media_name}" ?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                self.media_manager.restore_media(media_id, self.user_choice)
                self.populate_archives()
                QMessageBox.information(
                    self,
                    'Restauration réussie',
                    f'Le média "{media_name}" a été restauré avec succès.',
                    QMessageBox.Ok
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Erreur',
                    f"Échec de la restauration :\n{str(e)}",
                    QMessageBox.Ok
                )

    def delete_media(self):
        """Supprime définitivement le média sélectionné après confirmation."""
        selected_row = self.archive_list.currentRow()
        if selected_row < 0:
            QMessageBox.information(
                self,
                'Aucune sélection',
                'Veuillez sélectionner un média à supprimer.',
                QMessageBox.Ok
            )
            return
            
        media_id = int(self.archive_list.item(selected_row, 0).text())
        media_name = self.archive_list.item(selected_row, 1).text()
        
        # Boîte de dialogue de confirmation plus détaillée
        confirm_box = QMessageBox(self)
        confirm_box.setIcon(QMessageBox.Warning)
        confirm_box.setWindowTitle('Confirmation de suppression')
        confirm_box.setText(f'Suppression définitive de "{media_name}"')
        confirm_box.setInformativeText('Cette action est irréversible. Continuer ?')
        confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_box.setDefaultButton(QMessageBox.No)
        
        # Style personnalisé pour la boîte de confirmation
        confirm_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #1e293b;
            }
        """)
        
        if confirm_box.exec_() == QMessageBox.Yes:
            try:
                self.media_manager.delete_media(media_id)
                self.populate_archives()
                QMessageBox.information(
                    self,
                    'Suppression réussie',
                    f'Le média "{media_name}" a été définitivement supprimé.',
                    QMessageBox.Ok
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Erreur',
                    f"Échec de la suppression :\n{str(e)}",
                    QMessageBox.Ok
                )
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtCore import Qt, QSize


class PreviewDialog(QDialog):
    """
    Boîte de dialogue d'aperçu des médias avec support pour images et vidéos.
    Style moderne avec animations et interactions améliorées.
    """
    
    def __init__(self, media_path, description, parent=None):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.media_path = media_path
        self.description = description
        self.movie = None  # Pour les GIFs
        
        # Configuration de la fenêtre
        self._setup_ui()
        self._apply_styles()
        self._load_media()

    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        self.setWindowTitle("Aperçu du média")
        self.setWindowIcon(QIcon("icons/preview.png"))
        self.setMinimumSize(600, 600)  # Taille minimale responsive
        
        # Layout principal avec marges
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Description du média avec style
        self.description_label = QLabel(self.description, self)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label)
        
        # Zone d'aperçu avec cadre
        self.preview_container = QLabel(self)
        self.preview_container.setAlignment(Qt.AlignCenter)
        self.preview_container.setStyleSheet("background-color: #f0f0f0; border-radius: 8px;")
        layout.addWidget(self.preview_container, 1)  # Facteur d'expansion
        
        # Bouton de fermeture
        self.close_button = QPushButton("Fermer", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button, 0, Qt.AlignRight)
        
        self.setLayout(layout)

    def _apply_styles(self):
        """Applique les styles CSS modernes."""
        self.setStyleSheet("""
            QDialog {
                background-color: #f8fafc;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QLabel {
                font-size: 15px;
                color: #334155;
            }
            
            #description_label {
                font-size: 16px;
                font-weight: 500;
                color: #1e293b;
                padding: 10px;
                background-color: #f1f5f9;
                border-radius: 6px;
            }
            
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 6px;
                background-color: #3b82f6;
                color: white;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #2563eb;
            }
            
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        
        self.description_label.setObjectName("description_label")

    def _load_media(self):
        """Charge et affiche le média selon son type."""
        if self.media_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            self._show_image()
        elif self.media_path.lower().endswith('.gif'):
            self._show_gif()
        elif self.media_path.lower().endswith(('.mp4', '.avi', '.mov')):
            self._show_video_placeholder()
        else:
            self._show_unknown_format()

    def _show_image(self):
        """Affiche une image avec redimensionnement intelligent."""
        pixmap = QPixmap(self.media_path)
        
        # Redimensionnement proportionnel
        container_size = self.preview_container.size()
        scaled_pixmap = pixmap.scaled(
            container_size.width() - 40, 
            container_size.height() - 40,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        self.preview_container.setPixmap(scaled_pixmap)

    def _show_gif(self):
        """Affiche une animation GIF."""
        self.movie = QMovie(self.media_path)
        self.movie.setScaledSize(QSize(
            self.preview_container.width() - 40,
            self.preview_container.height() - 40
        ))
        self.preview_container.setMovie(self.movie)
        self.movie.start()

    def _show_video_placeholder(self):
        """Affiche un placeholder pour les vidéos avec icône."""
        placeholder = QLabel(self.preview_container)
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setPixmap(QIcon("icons/video.png").pixmap(128, 128))
        
        text = QLabel("Prévisualisation vidéo non supportée", self.preview_container)
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet("font-size: 16px; color: #64748b; margin-top: 10px;")
        
        layout = QVBoxLayout(self.preview_container)
        layout.addWidget(placeholder)
        layout.addWidget(text)
        layout.setAlignment(Qt.AlignCenter)

    def _show_unknown_format(self):
        """Affiche un message pour les formats non reconnus."""
        self.preview_container.setText("Format de média non supporté")
        self.preview_container.setStyleSheet("""
            font-size: 16px;
            color: #ef4444;
        """)

    def resizeEvent(self, event):
        """Redimensionne le média lors du resize de la fenêtre."""
        super().resizeEvent(event)
        if self.movie:
            self.movie.setScaledSize(QSize(
                self.preview_container.width() - 40,
                self.preview_container.height() - 40
            ))
        elif hasattr(self, 'pixmap'):
            self._show_image()

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

