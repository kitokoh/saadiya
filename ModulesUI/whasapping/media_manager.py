import json
import json
import os
import os
# Function to retrieve data from the database and save JSON
import os
import shutil
import sqlite3
import sqlite3
import sqlite3
import sqlite3
import sqlite3
import time
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, QTimer, QLocale
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QFileDialog, QMessageBox, QApplication
)
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QPushButton,
                             QVBoxLayout, QWidget, QLabel, QMessageBox, QHeaderView, QMenu,
                             QAbstractItemView, QLineEdit, QHBoxLayout, QDialog, QDialogButtonBox,
                             QStackedWidget, QTableWidgetSelectionRange, QComboBox)
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QTableWidget,
                             QAbstractItemView, QHeaderView, QLabel, QMessageBox, QDialog, QFormLayout,
                             QDialogButtonBox)
from datetime import datetime
import os
import sqlite3
import logging

from imports import *
from installFBrobotPy import updatejson
from installFBrobotPy.sendatajson import FileTransferApp
from installFBrobotPy.sendatajson2 import FileTransferApp2
from installFBrobotPy.sendatajson3 import FileTransferApp3
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from ui.footer import FooterSection
from ui.header import HeaderSection
from ui.secondry_menu import SecondaryMenu
from update_media_dialog import UpdateMediaDialog

stylesheet = """
QWidget {
    background-color: #222222;
    color: #FFFFFF;
    font-family: Arial, sans-serif;
    font-size: 14px;
}

QHeaderView::section {
    background-color: #333333;
    color: #FFFFFF;
    font-weight: bold;
    border: 1px solid #444444;
    padding: 4px;
    text-align: center;
}

QTableWidget {
    gridline-color: #444444;
    border: 1px solid #555555;
}

QTableWidget::item:selected {
    background-color: #555555;
    color: #FFFFFF;
}

QPushButton {
    background-color: #333333;
    color: #FFFFFF;
    border: 1px solid #555555;
    border-radius: 5px;
    padding: 6px 12px;
}

QPushButton:hover {
    background-color: #444444;
}

QPushButton:pressed {
    background-color: #555555;
}

QLineEdit, QTextEdit {
    background-color: #333333;
    color: #FFFFFF;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 4px;
}

QScrollBar:vertical, QScrollBar:horizontal {
    background: #333333;
    border: 1px solid #555555;
    width: 12px;
    height: 12px;
}

QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: #444444;
    border-radius: 6px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    background: #555555;
    border-radius: 4px;
    width: 10px;
    height: 10px;
}
"""

def create_media_table():

    roaming_path = os.getenv('APPDATA')

    # Construire le chemin complet vers le fichier modules.db
    resources_folder = os.path.join(roaming_path, 'saadiya', 'resources')
    db_path = os.path.join(resources_folder, 'media.db')

    # Vérifier si le dossier existe, sinon le créer
    if not os.path.exists(resources_folder):
        os.makedirs(resources_folder)

    # Se connecter à la base de données
    
    conn = sqlite3.connect(db_path)    
    #conn = sqlite3.connect('media.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            path TEXT NOT NULL,
            category TEXT,
            type TEXT,
            hashtags TEXT,
            contact TEXT
        )
    ''')
    conn.commit()
    conn.close()
class SearchFilterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by Name or Description")
        self.filter_by = QComboBox()
        self.filter_by.addItem("All")
        self.filter_by.addItem("Category")
        self.filter_by.addItem("Type")
        # layout.addWidget(self.search_bar)
        # layout.addWidget(self.filter_by)
        self.setLayout(layout)
class HeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.title = QLabel("AI Media Manager")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
       # layout.addWidget(self.title)
        self.setLayout(layout)        
class PreviewDialog(QDialog):
    def __init__(self, media_path, description, parent=None):
        # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        super().__init__(parent)
        # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()

        self.setWindowTitle(self.tr("Aperçu du Média"))

        layout = QVBoxLayout()

        # Ajoutez une étiquette pour la description
        description_label = QLabel(self.tr(description))
        layout.addWidget(description_label)

        # Ajoutez un QLabel pour afficher l'image ou un lecteur vidéo
        if media_path.endswith(('.png', '.jpg', '.jpeg')):
            media_label = QLabel()
            media_label.setPixmap(QPixmap(media_path))  # Assurez-vous que QPixmap est importé
            layout.addWidget(media_label)
        else:
            # Gérer les vidéos ici si nécessaire
            media_label = QLabel(self.tr("Aperçu vidéo non disponible."))  # Remplacer par un lecteur vidéo si nécessaire
            layout.addWidget(media_label)

        # Ajoutez un bouton pour fermer le dialog
        close_button = QPushButton(self.tr("Fermer"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssappro','media_manager_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','whatssappro','media_manager_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','whatssappro','media_manager_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','whatssappro','media_manager_translated.qm'))

        # Installer le traducteur pour appliquer la nouvelle langue
        QApplication.instance().installTranslator(self.translator)

        # Sauvegarder le choix de l'utilisateur
        self.save_language_choice(language)

        # Réappliquer la traduction sur tous les éléments visibles de l'interface
        self.retranslateUi()

    def save_language_choice(self, language):
        """Sauvegarde le choix de langue de l'utilisateur dans un fichier JSON."""
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
            json.dump(preferences, f)

    def retranslateUi(self):
        """Recharge les textes traduits dans l'interface."""
        #self.setWindowTitle(self.tr("Aperçu du Média"))
        pass
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()

    def init_language(self):
        """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
        # Vérifiez si le fichier de préférences existe
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')  # Par défaut à l'anglais si non trouvé
        else:
            # Obtenir le code de langue du système
            system_locale = QLocale.system().name()[:2]  # Par exemple: 'fr', 'en', 'tr', etc.

            # Dictionnaire pour mapper les codes de langue aux traductions
            language_map = {
                'en': 'en',
                'fr': 'fr',
                'tr': 'tr',
                'ar': 'ar',
            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)



class AddMedia(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🚀 Add Media")
        self.setFixedSize(800, 700)  # Augmenté pour accueillir l'image
        self.setWindowIcon(QIcon("resources/icons/rocket.png"))
        self.setStyleSheet(self.load_stylesheet())
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout()  # Layout principal pour diviser l'espace en deux colonnes
        
        # ======= COLONNE GAUCHE : Image/GIF =======
        media_preview_layout = QVBoxLayout()
        self.media_preview_label = QLabel()
        self.media_preview_label.setFixedSize(300, 400)  # Cadre fixe pour le média
        self.media_preview_label.setStyleSheet("""
            QLabel {
                border: 2px solid #00ffff;
                border-radius: 10px;
                background-color: #1a1a3f;
            }
        """)
        self.media_preview_label.setAlignment(Qt.AlignCenter)
        self.media_preview_label.setText("Media Preview\n(Upload a GIF/PNG)")
        self.media_preview_label.setFont(QFont("Orbitron", 12, QFont.Bold))
        self.media_preview_label.setStyleSheet("color: #ffffff; text-align: center;")
        media_preview_layout.addWidget(self.media_preview_label)
        main_layout.addLayout(media_preview_layout)

        # ======= COLONNE DROITE : Formulaire =======
        form_layout = QVBoxLayout()

        # Header avec style futuriste
        header_label = QLabel("🛠️ Add Your Media")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Orbitron", 22, QFont.Bold))
        header_label.setStyleSheet("color: #00ffff; text-shadow: 0px 0px 10px #00ffff; margin-bottom: 20px;")
        form_layout.addWidget(header_label)

        # Media Path
        self.media_label = QLabel("🔗 Media Path:")
        self.media_label.setStyleSheet("color: #ffffff; font-size: 14px;")
        self.media_path = QLineEdit()
        self.media_path.setPlaceholderText("Select your media file...")
        self.media_path.setStyleSheet("color: #00ff00;")
        self.browse_button = QPushButton("Browse")
        self.browse_button.setIcon(QIcon("resources/icons/folder.png"))
        self.browse_button.setStyleSheet("border: 2px solid #00ffff;")
        self.browse_button.clicked.connect(self.browse_media)
        media_layout = QHBoxLayout()
        media_layout.addWidget(self.media_path)
        media_layout.addWidget(self.browse_button)
        form_layout.addWidget(self.media_label)
        form_layout.addLayout(media_layout)

        # Description
        self.description_label = QLabel("📝 Description:")
        self.description_label.setStyleSheet("color: #ffffff; font-size: 14px;")
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Add a brief description...")
        form_layout.addWidget(self.description_label)
        form_layout.addWidget(self.description_input)

        # Category
        self.category_label = QLabel("📂 Category:")
        self.category_label.setStyleSheet("color: #ffffff; font-size: 14px;")
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Enter media category...")
        form_layout.addWidget(self.category_label)
        form_layout.addWidget(self.category_input)

        # Bouton "Add Media" ultra-stylé
        self.add_button = QPushButton("✅ Add Media")
        self.add_button.setIcon(QIcon("resources/icons/check.png"))
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #00ffff;
                color: #000;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #00ff00;
                border-radius: 8px;
                padding: 10px;
                text-shadow: 0px 0px 5px #ffffff;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #000;
            }
        """)
        self.add_button.clicked.connect(self.add_media_to_db)
        form_layout.addWidget(self.add_button)

        # Ajout des deux colonnes au layout principal
        main_layout.addLayout(form_layout)

        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)

    def browse_media(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Media File", "", "Images (*.png *.jpg *.gif);;All Files (*)", options=options)
        if file_path:
            self.media_path.setText(file_path)
            self.load_media_preview(file_path)

    def load_media_preview(self, file_path):
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(self.media_preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.media_preview_label.setPixmap(pixmap)
    def add_media_to_db(self):
        media_path = self.media_path.text()
        description = self.description_input.toPlainText()
        category = self.category_input.text()
        media_type = self.type_input.text()
        hashtags = self.hashtags_input.text()
        contact = self.contact_input.text()

        if not media_path:
            QMessageBox.warning(self, "Warning", "Please select a media file.")
            return

        dest_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'wa-ia-robot')
        os.makedirs(dest_dir, exist_ok=True)
        media_name = os.path.basename(media_path)
        dest_path = os.path.join(dest_dir, media_name)
        shutil.copy(media_path, dest_path)


        roaming_path = os.getenv('APPDATA')

        # Construire le chemin complet vers le fichier modules.db
        resources_folder = os.path.join(roaming_path, 'saadiya', 'resources')
        db_path = os.path.join(resources_folder, 'media.db')

        # Vérifier si le dossier existe, sinon le créer
        if not os.path.exists(resources_folder):
            os.makedirs(resources_folder)

        # Se connecter à la base de données
        
        conn = sqlite3.connect(db_path)


       # conn = sqlite3.connect('media.db')

        


        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO media (name, description, path, category, type, hashtags, contact)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (media_name, description, dest_path, category, media_type, hashtags, contact))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Media added successfully!")
        self.close()


    def add_media_to_db(self):
        media_path = self.media_path.text()
        description = self.description_input.toPlainText()
        category = self.category_input.text()

        if not media_path:
            QMessageBox.warning(self, "Warning", "Please select a media file.")
            return

        dest_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'wa-ia-robot')
        os.makedirs(dest_dir, exist_ok=True)
        media_name = os.path.basename(media_path)
        dest_path = os.path.join(dest_dir, media_name)
        shutil.copy(media_path, dest_path)

        roaming_path = os.getenv('APPDATA')

        # Construire le chemin complet vers le fichier modules.db
        resources_folder = os.path.join(roaming_path, 'saadiya', 'resources')
        db_path = os.path.join(resources_folder, 'media.db')

        # Vérifier si le dossier existe, sinon le créer
        if not os.path.exists(resources_folder):
            os.makedirs(resources_folder)

        # Se connecter à la base de données
        
        conn = sqlite3.connect(db_path)

        #conn = sqlite3.connect('media.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO media (name, description, path, category)
            VALUES (?, ?, ?, ?)
        ''', (media_name, description, dest_path, category))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Media added successfully!")
        self.close()

    def load_stylesheet(self):
        return """
            QDialog {
                background-color: #0d0d1f;
                border: 2px solid #00ffff;
                border-radius: 15px;
            }
            QLabel {
                font-family: Orbitron, sans-serif;
            }
            QLineEdit, QTextEdit {
                background-color: #1a1a3f;
                color: #ffffff;
                border: 2px solid #00ffff;
                border-radius: 10px;
                padding: 8px;
            }
            QLineEdit::placeholderText, QTextEdit::placeholderText {
                color: #7f7fff;
            }
        """



class EditMediaDialog(QDialog):
    def __init__(self, media_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Media")
        # Add input fields for editing media data
        # Connect save button to save changes to the database

class DeleteMediaDialog(QDialog):
    def __init__(self, media_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Media")
        # Add confirmation message and buttons to delete media from the database

class ViewMediaDialog(QDialog):
    def __init__(self, media_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("View Media")
        # Display detailed information about the selected media

class PaginationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.page_label = QLabel("Page 1 of 1")
        layout.addWidget(self.prev_button)
        layout.addWidget(self.next_button)
        layout.addWidget(self.page_label)
        self.setLayout(layout)

import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView,
    QHeaderView, QPushButton, QMenu, QLabel, QMessageBox, QLineEdit, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel,
    QPushButton, QMenu, QMessageBox, QAbstractItemView, QHeaderView, QLineEdit, QComboBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sqlite3
import os
import shutil





class EditMediaDialog(QDialog):
    def __init__(self, media_data, parent=None):
        super().__init__(parent)
        self.media_data = media_data
        self.setWindowTitle("Edit Media")
        self.setFixedSize(500, 450)
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("\U0001F4F0 Edit Media Details")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2f3640; margin-bottom: 15px;")
        layout.addWidget(title_label)

        # Form Layout
        form_layout = QFormLayout()

        self.name_field = QLineEdit(self.media_data[0])
        self.category_field = QLineEdit(self.media_data[1])
        self.type_field = QLineEdit(self.media_data[2])
        self.description_field = QTextEdit(self.media_data[3])

        self.name_field.setPlaceholderText("Enter media name")
        self.category_field.setPlaceholderText("Enter category")
        self.type_field.setPlaceholderText("Enter type")
        self.description_field.setPlaceholderText("Enter a detailed description")
        self.description_field.setFixedHeight(100)

        form_layout.addRow("\U0001F4D6 Name:", self.name_field)
        form_layout.addRow("\U0001F4C1 Category:", self.category_field)
        form_layout.addRow("\U0001F4DD Type:", self.type_field)
        form_layout.addRow("\U0001F4CB Description:", self.description_field)

        layout.addLayout(form_layout)

        # Button Box
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        save_button = button_box.button(QDialogButtonBox.Save)
        save_button.setText("\U0001F4BE Save")
        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText("\U0001F6AB Cancel")

        layout.addWidget(button_box)

        self.setLayout(layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 15px;
                padding: 15px;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #34495e;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 8px;
                background-color: #f0f3f4;
                font-size: 14px;
                color: #2c3e50;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #2980b9;
                background-color: #ecf0f1;
            }
            QDialogButtonBox QPushButton {
                background-color: #2980b9;
                color: #ffffff;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #3498db;
            }
            QDialogButtonBox QPushButton:pressed {
                background-color: #1c598a;
            }
        """)

    def get_updated_data(self):
        return (
            self.name_field.text(),
            self.category_field.text(),
            self.type_field.text(),
            self.description_field.toPlainText(),
            self.media_data[4]
        )

class MediaTable(QWidget):
    def __init__(self, search_filter, parent=None):
        super().__init__(parent)
        self.search_filter = search_filter
        self.page_size = 10
        self.current_page = 0
        self.media_data = []
        self.filtered_data = []
        self.setup_ui()
        self.load_media_from_db()
        self.apply_styles()

    def setup_ui1(self):
        # Style général futuriste
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #ffffff;
                font-family: 'Roboto', sans-serif;
            }
            QLineEdit {
                background-color: #2c2c3e;
                border: 1px solid #5e5e6f;
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
                font-size: 14px;
            }
            QComboBox {
                background-color: #2c2c3e;
                border: 1px solid #5e5e6f;
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: #2c2c3e;
                border: 1px solid #5e5e6f;
                color: #ffffff;
                selection-background-color: #5e5e6f;
            }
            QPushButton {
                background-color: #5e5e6f;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7a7a8e;
            }
            QPushButton:disabled {
                background-color: #3e3e4e;
                color: #888888;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QTableWidget {
                background-color: #2c2c3e;
                border: 1px solid #5e5e6f;
                gridline-color: #5e5e6f;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #5e5e6f;
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
        """)

        layout = QVBoxLayout()


 # Add the header
        header = HeaderSection(self, title=self.tr("Media Management"), app_name=self.tr("Leopardo AI"), slogan=self.tr("AI Marketing & Management Auto"))
        layout.addWidget(header)
        # Barre de recherche et boutons
        search_add_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.apply_filters)
        search_add_layout.addWidget(self.search_bar)

        self.filter_by = QComboBox()
        self.filter_by.addItems(["All", "Category"])
        self.filter_by.currentIndexChanged.connect(self.apply_filters)
        search_add_layout.addWidget(self.filter_by)

        self.add_media_button = QPushButton("+ Add Media")
        self.add_media_button.clicked.connect(self.open_add_media_dialog)
        search_add_layout.addWidget(self.add_media_button)



        # Bouton "Update Robot" avec menu déroulant
        self.update_robot_button = QPushButton(self.tr("🚀 Send to Robot"), self)
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

        self.update_robot_button.setMenu(self.create_robot_menu())
        search_add_layout.addWidget(self.update_robot_button)

        layout.addLayout(search_add_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Thumbnail', 'Name', 'Category', 'Type', 'Actions'])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Pagination
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Prev")
        self.prev_button.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_button)

        self.page_label = QLabel("Page 1")
        pagination_layout.addWidget(self.page_label)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)
        layout.addLayout(pagination_layout)
       # Add the footer
        footer = FooterSection(self)
        layout.addWidget(footer)

        self.setLayout(layout)
    def setup_ui(self):
        # Style général futuriste
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Arial', sans-serif;
            }
            QLineEdit {
                background-color: #1e1e1e;
                border: 2px solid #00adb5;
                border-radius: 5px;
                padding: 10px;
                color: #ffffff;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #009688;
            }
            QComboBox {
                background-color: #1e1e1e;
                border: 2px solid #00adb5;
                border-radius: 5px;
                padding: 5px;
                color: #ffffff;
                font-size: 16px;
            }
            QPushButton {
                background-color: #00adb5;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #009688;
            }
            QPushButton:disabled {
                background-color: #3a3a3a;
                color: #888888;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 16px;
            }
            QTableWidget {
                background-color: #1e1e1e;
                border: 1px solid #00adb5;
                color: #e0e0e0;
                gridline-color: #00adb5;
            }
            QHeaderView::section {
                background-color: #00adb5;
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
        """)

        layout = QVBoxLayout()


        header = HeaderSection(self, title=self.tr("Media Management"), app_name=self.tr("Leopardo AI"), slogan=self.tr("AI Marketing & Management Auto"))
        layout.addWidget(header)
        # Barre de recherche et boutons
        search_add_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search...")
        self.search_bar.textChanged.connect(self.apply_filters)
        search_add_layout.addWidget(self.search_bar)

        self.filter_by = QComboBox()
        self.filter_by.addItems(["All", "Category"])
        self.filter_by.currentIndexChanged.connect(self.apply_filters)
        search_add_layout.addWidget(self.filter_by)

        self.add_media_button = QPushButton("🖼️ Add Media")
        self.add_media_button.clicked.connect(self.open_add_media_dialog)
        search_add_layout.addWidget(self.add_media_button)

        # Bouton "Update Robot" avec menu déroulant
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

        self.update_robot_button.setMenu(self.create_robot_menu())
        search_add_layout.addWidget(self.update_robot_button)

        layout.addLayout(search_add_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Thumbnail', 'Name', 'Category', 'Type', 'Actions'])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Pagination
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("⬅️ Prev")
        self.prev_button.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_button)

        self.page_label = QLabel("Page 1")
        self.page_label.setAlignment(Qt.AlignCenter)
        pagination_layout.addWidget(self.page_label)

        self.next_button = QPushButton("➡️ Next")
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)
        layout.addLayout(pagination_layout)


        footer = FooterSection(self)
        layout.addWidget(footer)
        self.setLayout(layout)

    def create_robot_menu(self):
        """Crée un menu déroulant pour le bouton 'Update Robot'."""
        menu = QMenu(self)
        add_message_action = menu.addAction("Add Message")
        add_message_action.triggered.connect(self.generate_and_save_json)

        add_message_selected_action = menu.addAction("Add Message Selected")
        add_message_selected_action.triggered.connect(self.generate_and_save_selected_json)

        return menu
    

    #     dialog = QDialog(self)
    #     dialog.setWindowTitle("Add Media")
    #     dialog.exec_()
    #     self.load_media_from_db()

    def generate_and_save_selected_json(self):
        try:
            # Récupérer les lignes sélectionnées
            selected_rows = self.table.selectionModel().selectedRows()
            if not selected_rows:
                QMessageBox.warning(self, "No Selection", "Please select at least one row to export.")
                return

            selected_data = []
            for row in selected_rows:
                row_index = row.row()
                # Extraire les données de la ligne sélectionnée
                name = self.table.item(row_index, 1).text()
                category = self.table.item(row_index, 2).text()
                type_ = self.table.item(row_index, 3).text()
                path = self.filtered_data[row_index][4]  # Correspond à l'indice du chemin dans `filtered_data`
                description = self.filtered_data[row_index][3]  # Indice de la description
                selected_data.append((name, category, type_, description, path))

            # Préparer les données JSON
            json_data = []
            greetings = ["hello", "hi", "bonjour", "salut", "merhaba"]

            for record in selected_data:
                name, category, type_, description, path = record
                if description:
                    # Ajouter un traitement spécial pour les salutations
                    words = description.split(" ", 1)
                    if len(words) > 1 and words[0].lower() in greetings:
                        text = f"{words[0].capitalize()} {{name}} {words[1]}".strip()
                    else:
                        text = description.strip()
                else:
                    text = "(No description provided)"

                # Construire l'entrée JSON
                json_entry = {
                    "text": text,
                    "image": path if type_.lower() == "image" else None,
                    "pdf": path if type_.lower() == "pdf" else None,
                    "video": path if type_.lower() == "video" else None
                }
                json_data.append(json_entry)

            # Sauvegarder dans le fichier JSON
            base_path = os.path.join("c:/wabon/robot1")
            os.makedirs(base_path, exist_ok=True)
            json_file_path = os.path.join(base_path, "wamessage.json")

            if os.path.exists(json_file_path):
                archive_path = os.path.join(base_path, f"wamessage_archive_{int(time.time())}.json")
                os.rename(json_file_path, archive_path)

            with open(json_file_path, "w", encoding="utf-8") as json_file:
                json.dump(json_data, json_file, indent=4, ensure_ascii=False)

            QMessageBox.information(self, "Success", "Selected rows have been successfully saved to JSON.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")




    def generate_and_save_json(self):
        try:
            print("Connecting to the database...")
            roaming_path = os.getenv('APPDATA')

            # Construire le chemin complet vers le fichier modules.db
            resources_folder = os.path.join(roaming_path, 'saadiya', 'resources')
            db_path = os.path.join(resources_folder, 'media.db')

            # Vérifier si le dossier existe, sinon le créer
            if not os.path.exists(resources_folder):
                os.makedirs(resources_folder)

            # Se connecter à la base de données
            
            conn = sqlite3.connect(db_path)
            #conn = sqlite3.connect('media.db')
            cursor = conn.cursor()
            print("Fetching media data from the database...")
            cursor.execute("SELECT name, category, type, description, path FROM media")
            media_data = cursor.fetchall()
            conn.close()
            print(f"Fetched {len(media_data)} records from the database.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return
        except Exception as e:
            print(f"Unexpected error while fetching data: {e}")
            return

        # Prepare JSON data
        json_data = []
        greetings = ["hello", "hi", "bonjour", "salut", "merhaba"]

        for record in media_data:
            try:
                name, category, type_, description, path = record
                if description:
                    # Check if description starts with a greeting
                    words = description.split(" ", 1)
                    if len(words) > 1 and words[0].lower() in greetings:
                        text = f"{words[0].capitalize()} {{name}} {words[1]}".strip()
                    else:
                        text = description.strip()
                else:
                    text = "(No description provided)"

                # Create JSON entry
                json_entry = {
                    "text": text,
                    "image": path if type_.lower() == "image" else None,
                    "pdf": path if type_.lower() == "pdf" else None,
                    "video": path if type_.lower() == "video" else None
                }
                json_data.append(json_entry)
            except Exception as e:
                print(f"Error processing record {record}: {e}")
                continue

        print(f"Prepared JSON data with {len(json_data)} entries.")

        # File handling for JSON storage
        try:
            print("Handling JSON file storage...")
            base_path = os.path.join("c:/wabon/robot1")
            os.makedirs(base_path, exist_ok=True)
            json_file_path = os.path.join(base_path, "wamessage.json")

            if os.path.exists(json_file_path):
                archive_path = os.path.join(base_path, f"wamessage_archive_{int(time.time())}.json")
                print(f"Renaming existing JSON file to {archive_path}")
                os.rename(json_file_path, archive_path)

            print(f"Saving new JSON data to {json_file_path}...")
            with open(json_file_path, "w", encoding="utf-8") as json_file:
                json.dump(json_data, json_file, indent=4, ensure_ascii=False)

            print(f"it is send to robot youupii.")

            # Show success popup
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Success")
            msg_box.setText("JSON data has been successfully saved!")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

        except OSError as e:
            print(f"File operation error: {e}")
        except Exception as e:
            print(f"Unexpected error while saving JSON: {e}")



    def open_add_media_dialog(self):
        dialog = AddMedia(self)
        if dialog.exec_():
            self.load_media_from_db()
    # def load_media_from_db(self):

    #     roaming_path = os.getenv('APPDATA')

    #     # Construire le chemin complet vers le fichier modules.db
    #     resources_folder = os.path.join(roaming_path, 'saadiya', 'resources')
    #     db_path = os.path.join(resources_folder, 'media.db')

    #     # Vérifier si le dossier existe, sinon le créer
    #     if not os.path.exists(resources_folder):
    #         os.makedirs(resources_folder)

    #     # Se connecter à la base de données
        
    #     conn = sqlite3.connect(db_path)
    #     #conn = sqlite3.connect('media.db')
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT name, category, type, description, path FROM media")
    #     self.media_data = cursor.fetchall()
    #     conn.close()
    #     self.apply_filters()


    logging.basicConfig(level=logging.ERROR)

    def load_media_from_db(self):
        roaming_path = os.getenv('APPDATA')
        resources_folder = os.path.join(roaming_path, 'saadiya', 'resources')
        db_path = os.path.join(resources_folder, 'media.db')

        print("Database path:", db_path)

        # Ensure the resources folder exists
        try:
            if not os.path.exists(resources_folder):
                os.makedirs(resources_folder)
        except OSError as e:
            logging.error("Error creating directory: %s", e)
            return

        # Connect to the database
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Check if the 'media' table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='media'")
            table_exists = cursor.fetchone()

            if not table_exists:
                # Create the 'media' table
                cursor.execute('''
                    CREATE TABLE media (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT,
                        type TEXT,
                        description TEXT,
                        path TEXT NOT NULL
                    )
                ''')
                conn.commit()
                print("Media table created.")

            # Fetch data from the 'media' table
            cursor.execute("SELECT name, category, type, description, path FROM media")
            self.media_data = cursor.fetchall()
            conn.close()
            self.apply_filters()

        except sqlite3.Error as e:
            logging.error("Database error: %s", e)
        except Exception as e:
            logging.error("General error: %s", e)

            


    def apply_filters(self):
        filter_type = self.filter_by.currentText()
        filter_value = self.search_bar.text().strip()

        if filter_type == "Category":
            self.filtered_data = [media for media in self.media_data if media[1].lower() == filter_value.lower()]
        else:
            self.filtered_data = [media for media in self.media_data if filter_value.lower() in media[0].lower()]

        self.current_page = 0
        self.display_media()

    def display_media(self):
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        self.table.setRowCount(len(self.filtered_data[start_idx:end_idx]))

        for row_idx, row_data in enumerate(self.filtered_data[start_idx:end_idx]):
            thumbnail_item = QLabel()
            pixmap = QPixmap(row_data[4])
            pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            thumbnail_item.setPixmap(pixmap)
            self.table.setCellWidget(row_idx, 0, thumbnail_item)

            name_item = QTableWidgetItem(row_data[0])
            category_item = QTableWidgetItem(row_data[1])
            type_item = QTableWidgetItem(row_data[2])
            self.table.setItem(row_idx, 1, name_item)
            self.table.setItem(row_idx, 2, category_item)
            self.table.setItem(row_idx, 3, type_item)

            action_button = self.create_action_button(row_data)
            self.table.setCellWidget(row_idx, 4, action_button)

        total_pages = (len(self.filtered_data) + self.page_size - 1) // self.page_size
        self.page_label.setText(f"Page {self.current_page + 1} of {total_pages}")

    def create_action_button(self, media_data):
        action_button = QPushButton("Actions")
        menu = QMenu()

        show_action = menu.addAction("Show Details")
        show_action.triggered.connect(lambda: self.show_details(media_data))

        edit_action = menu.addAction("Edit")
        edit_action.triggered.connect(lambda: self.edit_media(media_data))

        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_media(media_data))

        action_button.setMenu(menu)
        return action_button

    def show_details(self, media_data):
        details_dialog = QMessageBox(self)
        details_dialog.setWindowTitle("Media Details")
        details_dialog.setText(f"<b>Name:</b> {media_data[0]}<br><b>Category:</b> {media_data[1]}<br><b>Type:</b> {media_data[2]}<br><b>Description:</b> {media_data[3]}<br><b>Path:</b> {media_data[4]}")
        details_dialog.setIcon(QMessageBox.Information)
        details_dialog.exec_()

    def edit_media(self, media_data):
        dialog = EditMediaDialog(media_data, self)
        if dialog.exec_():
            updated_data = dialog.get_updated_data()
            roaming_path = os.getenv('APPDATA')

            # Construire le chemin complet vers le fichier modules.db
            resources_folder = os.path.join(roaming_path, 'saadiya', 'resources')
            db_path = os.path.join(resources_folder, 'media.db')

            # Vérifier si le dossier existe, sinon le créer
            if not os.path.exists(resources_folder):
                os.makedirs(resources_folder)

            # Se connecter à la base de données
            
            conn = sqlite3.connect(db_path)
                        
            #conn = sqlite3.connect('media.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE media
                SET name = ?, category = ?, type = ?, description = ?
                WHERE path = ?
            """, updated_data)
            conn.commit()
            conn.close()
            self.load_media_from_db()

    def delete_media(self, media_data):
        reply = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete '{media_data[0]}'?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            roaming_path = os.getenv('APPDATA')

            # Construire le chemin complet vers le fichier modules.db
            resources_folder = os.path.join(roaming_path, 'saadiya', 'resources')
            db_path = os.path.join(resources_folder, 'media.db')

            # Vérifier si le dossier existe, sinon le créer
            if not os.path.exists(resources_folder):
                os.makedirs(resources_folder)

            # Se connecter à la base de données
            
            conn = sqlite3.connect(db_path)
            
            #conn = sqlite3.connect('media.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM media WHERE name = ?", (media_data[0],))
            conn.commit()
            conn.close()
            self.load_media_from_db()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_media()

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.filtered_data):
            self.current_page += 1
            self.display_media()


    def apply_styles(self):
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #34495e;
                color: #ecf0f1;
                selection-background-color: #2980b9;
                border: 1px solid #7f8c8d;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: none;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #2c3e50;
                border: none;
            }
        """)
        self.add_media_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
                cursor: pointer;
            }
            QPushButton:pressed {
                background-color: #229954;
            }
        """)
        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

    # Méthode pour assombrir les couleurs lors du survol
    def darken_color(self, color):
        # Convertir la couleur hexadécimale en valeurs RGB, puis réduire légèrement chaque composant pour un effet "sombre".
        hex_color = color.lstrip('#')
        r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        return f'#{max(r - 20, 0):02X}{max(g - 20, 0):02X}{max(b - 20, 0):02X}'

    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssappro','media_manager_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','whatssappro','media_manager_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','whatssappro','media_manager_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','whatssappro','media_manager_translated.qm'))

        # Installer le traducteur pour appliquer la nouvelle langue
        QApplication.instance().installTranslator(self.translator)
        
            # Sauvegarder le choix de l'utilisateur
        self.save_language_choice(language)


        # Réappliquer la traduction sur tous les éléments visibles de l'interface
        self.retranslateUi()

    def save_language_choice(self, language):
        """Sauvegarde le choix de langue de l'utilisateur dans un fichier JSON."""
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
            json.dump(preferences, f)
    def retranslateUi(self):
        """Recharge les textes traduits dans l'interface."""
    #######    self.setWindowTitle(self.tr('AI FB ROBOT Pro'))       
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        pass
    def init_language(self):
        """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
        # Vérifiez si le fichier de préférences existe
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')  # Par défaut à l'anglais si non trouvé
        else:
            # Obtenir le code de langue du système
            system_locale = QLocale.system().name()[:2]  # Par exemple: 'fr', 'en', 'tr', etc.

            # Dictionnaire pour mapper les codes de langue aux traductions
            language_map = {
                'en': 'en',
                'fr': 'fr',
                'tr': 'tr',
                'ar': 'ar',
            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)
    def add_json_text (self, *args):
        transfer_app2 = FileTransferApp3()  # envoie le multi images Créer une instance de FileTransferApp
        transfer_app2.start_process()  # Appeler la méthode qui lance le processus   
        updatejson1 = updatejson
        updatejson1.main()

    def send_json1(self, *args):
        transfer_app = FileTransferApp()  # Créer une instance de FileTransferApp
        transfer_app.start_process()  # Appeler la méthode qui lance le processus
        transfer_app2 = FileTransferApp2()  # envoie le multi images Créer une instance de FileTransferApp
        transfer_app2.start_process()  # Appeler la méthode qui lance le processus
            
       
        updatejson1 = updatejson
        updatejson1.main()
# Lancer le transfert de fichiers
    def get_instance_list(self):
        # Chemin du dossier des instances
        media_folder_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-WA-Robot', 'media')

        # Vérifier si le dossier existe
        if not os.path.exists(media_folder_path):
            print("Le dossier des médias est introuvable.")
            return ["Dossier des médias introuvable"]

        # Charger la liste des instances
        instance_folders = [d for d in os.listdir(media_folder_path) if d.startswith('media')]
        
        # Vérifier si la liste est vide
        if not instance_folders:
            print("Liste d'instances vide.")
            return ["Liste d'instances vide"]

        return instance_folders

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Media Manager")
        self.setStyleSheet(stylesheet)
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Header
        header = HeaderWidget()
        layout.addWidget(header)

        # Search and Filter
        self.search_filter = SearchFilterWidget()
        layout.addWidget(self.search_filter)

        # Media Table
        self.media_table = MediaTable(self.search_filter, self)
        layout.addWidget(self.media_table)

        # Pagination
        self.pagination = PaginationWidget()
        layout.addWidget(self.pagination)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect signals and slots
        self.search_filter.search_bar.textChanged.connect(self.media_table.apply_filters)
        self.search_filter.filter_by.currentIndexChanged.connect(self.media_table.apply_filters)
        self.pagination.prev_button.clicked.connect(self.media_table.prev_page)
        self.pagination.next_button.clicked.connect(self.media_table.next_page)
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    create_media_table()  # Create the database table

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())