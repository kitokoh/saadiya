import os
import json
from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, 
                             QVBoxLayout, QWidget, QLabel, QMessageBox, QHeaderView, 
                             QAbstractItemView, QLineEdit, QHBoxLayout, QDialog, QDialogButtonBox,
                             QStackedWidget, QTableWidgetSelectionRange)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer,QLocale
from ui.header import HeaderSection  # Import du header
from ui.footer import FooterSection  # Import du footer
from ui.secondry_menu import SecondaryMenu  # Assurez-vous d'importer votre nouvelle classe
#from group_manager import GroupTable

from update_media_dialog import UpdateMediaDialog
from add_media import AddMedia
class MediaTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.media_folder = os.path.join(os.path.expanduserself.tr(self.tr(('~'))), 'Downloads', 'AI-FB-Robot', 'media', 'media1')
        self.json_file = os.path.join(os.path.expanduserself.tr(self.tr(('~'))), 'Downloads', 'AI-FB-Robot', 'text', 'data.json')
        self.media_manager = AddMedia(self.media_folder)  # Créez une instance de MediaManager

        self.media_list = self.load_media()
        self.page_size = 10  # Nombre de lignes par page
        self.current_page = 0

        # UI Setup
        layout = QVBoxLayout(self)

        # Ajouter le header
        header = HeaderSection(self, title="AI Medias Mangements", app_name="Nova360 AI", slogan="AI Marketing & Management Auto")
        layout.addWidget(header)
 # Ajouter le menu secondaire
        self.secondary_menu = SecondaryMenu(self)
        self.secondary_menu.menu_selected.connect(self.change_content)  # Connecter le signal
                # Menu secondaire
        #self.secondary_menu = SecondaryMenu(self)
        #self.secondary_menu.menu_selected.connect(self.change_content)  # Connecter le signal
        layout.addWidget(self.secondary_menu)  # Ajouter le menu secondaire

        #layout.addWidget(self.secondary_menu)
        # Disposition horizontale pour le titre, la recherche et le bouton "Ajouter"
        top_layout = QHBoxLayout()
        # Ajouter le menu secondaire

        # Label "Liste des media"
        media_label = QLabel("Liste des media:", self)
        media_label.setStyleSheetself.tr(self.tr(("font-size: 20px; font-weight: bold;")))
        top_layout.addWidget(media_label)

        # Barre de recherche
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderTextself.tr(self.tr(("Rechercher...")))
        self.search_field.textChanged.connect(self.filter_table)
        self.search_field.setStyleSheetself.tr(self.tr(("padding: 5px; font-size: 14px;")))
        top_layout.addWidget(self.search_field)

        # Bouton Ajouter Media (ajusté en taille et icône)
        self.add_media_button = QPushButton('Ajouter Media', self)
        self.add_media_button.setFixedSize(120, 30)
        self.add_media_button.setIcon(QIconself.tr(self.tr(('resources/icons/robot-512.png'))))  # Spécifiez le chemin de votre icône ici
        self.add_media_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.add_media_button.clicked.connect(self.add_new_media)
        top_layout.addWidget(self.add_media_button)

        layout.addLayout(top_layout)

        # Media Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Nom', 'Description', 'Preview', 'Action'])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Resize column 'Nom'
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Stretch column 'Description'
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Resize column 'Preview'
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Resize column 'Action'
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setStyleSheet(""" 
            QTableWidget {
                border: 1px solid #007BFF;
                border-radius: 5px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #007BFF;
                color: white;
                padding: 10px;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)

        self.table.setSortingEnabled(True)  # Activer le tri
        layout.addWidget(self.table)

        # Pagination Buttons
        pagination_layout = QHBoxLayout()
        
        self.prev_button = QPushButton('Précédent', self)
        self.prev_button.setIcon(QIconself.tr(self.tr(('resources/icons/robot-512.png'))))  # Spécifiez le chemin de votre icône ici
        self.prev_button.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_button)

        self.next_button = QPushButton('Suivant', self)
        self.next_button.setIcon(QIconself.tr(self.tr(('resources/icons/robot-512.png'))))  # Spécifiez le chemin de votre icône ici
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)
        
        layout.addLayout(pagination_layout)

        self.populate_table()

        # Actualisation automatique
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_table)
        self.timer.start(5000)  # Rafraîchir toutes les 5 secondes

        # Ajouter le footer
        footer = FooterSection(self)
        layout.addWidget(footer)
    def init_language(self):
        """Initialise la langue par défaut à celle du système."""
        system_locale = QLocale.system().name()[:2]
        self.switch_language(system_locale)

    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.loadself.tr(self.tr(("lang/en_US/modules/media_manager.qm")))
        elif language == "fr":
            self.translator.loadself.tr(self.tr(("lang/fr_FR/modules/media_manager.qm")))
        elif language == "tr":
            self.translator.loadself.tr(self.tr(("lang/tr_TR/modules/media_manager.qm")))
        elif language == "ar":
            self.translator.loadself.tr(self.tr(("lang/ar_AR/modules/media_manager.qm")))
        QApplication.instance().installTranslator(self.translator)
        self.retranslateUi()

    def load_media(self):
        # Load media files from the directory
        media_files = [f for f in os.listdir(self.media_folder) if f.endswith(self.tr(self.tr(('.png', '.jpg', '.jpeg', '.mp4'))))]

        # Load descriptions from the JSON file
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                json_data = json.load(f)
        else:
            json_data = {'posts': []}

        # Create a list of dictionaries containing media info
        media_list = []
        for media in media_files:
            media_info = {
                'nom': media,
                'description': '',
                'preview_path': os.path.join(self.media_folder, media)
            }
            for post in json_data['posts']:
                if post['image'] == media_info['preview_path']:
                    media_info['description'] = post['text']
                    break
            media_list.append(media_info)

        return media_list

    def populate_table(self):
        # Paginate the table based on the current page
        start = self.current_page * self.page_size
        end = start + self.page_size
        visible_media = self.media_list[start:end]

        self.table.setRowCount(len(visible_media))

        for row, media in enumerate(visible_media):
            # Nom column (File name with extension)
            nom_item = QTableWidgetItem(media['nom'])
            nom_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 0, nom_item)

            # Description column
            description_item = QTableWidgetItem(media['description'])
            description_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            description_item.setToolTip(media['description'])
            description_item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.table.setItem(row, 1, description_item)

            # Preview column (Image or Video)
            preview_label = QLabel()
            if media['nom'].endswith(self.tr(self.tr(('.png', '.jpg', '.jpeg')))):
                pixmap = QPixmap(media['preview_path']).scaled(150, 150, Qt.KeepAspectRatio)
                preview_label.setPixmap(pixmap)
                preview_label.setFixedHeight(150)  # Ajustement de la hauteur
            elif media['nom'].endswithself.tr(self.tr(('.mp4'))):
                preview_label.setTextself.tr(self.tr(('Video File (Click to Preview)')))
                preview_label.setStyleSheetself.tr(self.tr(("background-color: lightgray; padding: 10px; border-radius: 5px;")))
                preview_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 2, preview_label)

            # Action column (Edit button)
            edit_button = QPushButtonself.tr(self.tr(('Edit')))
            edit_button.clicked.connect(lambda checked, m=media: self.update_media(m))
            self.table.setCellWidget(row, 3, edit_button)

    def update_media(self, media):
        dialog = UpdateMediaDialog(media, self)
        if dialog.exec_():
            self.save_description(media)
            self.populate_table()

    def save_description(self, media):
        # Load the existing JSON data
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                json_data = json.load(f)
        else:
            json_data = {'posts': []}

        # Update or add media entry
        for post in json_data['posts']:
            if post['image'] == media['preview_path']:
                post['text'] = media['description']
                break
        else:
            json_data['posts'].append({
                'text': media['description'],
                'image': media['preview_path']
            })

        with open(self.json_file, 'w') as f:
            json.dump(json_data, f, indent=4)

    def add_new_media(self):
        self.media_manager.add_media()  # Appeler la méthode d'ajout de médias
        self.refresh_table()  # Rafraîchir la liste après l'ajout
       # QMessageBox.information(self, self.tr(self.tr("Ajout de média")),  "Fonctionnalité d'ajout de média à implémenter.", QMessageBox.Ok)

    def filter_table(self):
        search_text = self.search_field.text().lower()
        self.media_list = [media for media in self.load_media() if search_text in media['nom'].lower() or search_text in media['description'].lower()]
        self.populate_table()

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.media_list):
            self.current_page += 1
            self.populate_table()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.populate_table()

    def refresh_table(self):
        self.media_list = self.load_media()
        self.populate_table()
    def change_content(self, menu_name):
        if menu_name == "media":
            self.populate_table()  # Affiche la table des médias
        elif menu_name == "groups":
            # Ajoutez le code pour afficher les groupes
            pass
        elif menu_name == "instances":
            # Ajoutez le code pour afficher les instances
            pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitleself.tr(self.tr(('AI FB ROBOT Pro')))
        self.resize(900, 600)
        self.setCentralWidget(MediaTable(self))

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())