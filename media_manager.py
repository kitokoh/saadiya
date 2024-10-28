import os
import json
from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, 
                             QVBoxLayout, QWidget, QLabel, QMessageBox, QHeaderView,QMenu, 
                             QAbstractItemView, QLineEdit, QHBoxLayout, QDialog, QDialogButtonBox,
                             QStackedWidget, QTableWidgetSelectionRange, QComboBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer, QLocale
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox

from ui.header import HeaderSection  
from ui.footer import FooterSection  
from ui.secondry_menu import SecondaryMenu  
from update_media_dialog import UpdateMediaDialog
from installFBrobotPy.sendatajson import FileTransferApp

from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *

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
            self.translator.load("resources/lang/en_US/modules/media_manager_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/modules/media_manager_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/modules/media_manager_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/modules/media_manager_translated.qm")

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

class AddMedia(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        self.setWindowTitle(self.tr("Ajouter Média"))
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        add_button = QPushButton(self.tr("Ajouter Média"))
        add_button.clicked.connect(self.add_media)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/modules/media_manager_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/modules/media_manager_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/modules/media_manager_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/modules/media_manager_translated.qm")

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
        #self.setWindowTitle(self.tr("Ajouter Média"))
        pass

    def init_language(self):
        """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')
        else:
            system_locale = QLocale.system().name()[:2]

            language_map = {
                'en': 'en',
                'fr': 'fr',
                'tr': 'tr',
                'ar': 'ar',
            }

            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)

    def load_json(self):
        self.json_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-FB-Robot', 'text', 'text1', 'data.json')

        with open(self.json_file, 'r') as f:
            return json.load(f)

    def update_json(self, media_data):
        self.json_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-FB-Robot', 'text', 'text1', 'data.json')

        with open(self.json_file, 'w') as f:
            json.dump(media_data, f)

    def add_media(self):
        options = QFileDialog.Options()

        files, _ = QFileDialog.getOpenFileNames(
            self, 
            self.tr("Sélectionnez des fichiers média"), 
            "", 
            "Images (*.png *.jpg *.jpeg);;Vidéos (*.mp4 *.mov)", 
            options=options
        )

        if files:
            media_data = self.load_json()
            max_key = 0

            for media in media_data['posts']:
                key = int(media['image'].split('\\')[-1].split('.')[0])
                if key > max_key:
                    max_key = key

            for file_path in files:
                extension = os.path.splitext(file_path)[1]
                max_key += 1
                new_name = f"{max_key}{extension}"

                self.media_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-FB-Robot', 'media', 'media1')
                new_path = os.path.join(self.media_folder, new_name)

                shutil.copy(file_path, new_path)

                media_data['posts'].append({
                    "text": self.tr("Description du média"),
                    "image": new_path
                })

            self.update_json(media_data)
            QMessageBox.information(self, self.tr("Succès"), self.tr("Média ajouté avec succès !"))



class MediaTable(QWidget):
    def __init__(self, parent=None):
        # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        super().__init__(parent)
        self.media_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-FB-Robot', 'media', 'media1')
        self.json_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-FB-Robot', 'text','text1' , 'data.json')
        self.media_manager = AddMedia(parent=self)

        self.media_list = self.load_media()
        self.page_size = 10
        self.current_page = 0

        # UI Setup
        layout = QVBoxLayout(self)

        # Ajouter le header
        header = HeaderSection(self, title=self.tr("AI Medias Mangements"), app_name=self.tr("Nova360 AI"), slogan=self.tr("AI Marketing & Management Auto"))
        layout.addWidget(header)

        # Ajouter le menu secondaire
        self.secondary_menu = SecondaryMenu(self)
        self.secondary_menu.menu_selected.connect(self.change_content)
        layout.addWidget(self.secondary_menu)

        # Disposition horizontale pour le titre, la recherche et le bouton "Ajouter"
        top_layout = QHBoxLayout()

        # Label "Liste des media"
        media_label = QLabel(self.tr("Liste des media:"), self)
        media_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        top_layout.addWidget(media_label)

        # Barre de recherche
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText(self.tr("Rechercher..."))
        self.search_field.textChanged.connect(self.filter_table)
        self.search_field.setStyleSheet("padding: 5px; font-size: 14px;")
        top_layout.addWidget(self.search_field)

        # Dropdown pour les instances
        self.instance_combo = QComboBox(self)
        self.instance_combo.addItems(self.get_instance_list())
        self.instance_combo.currentIndexChanged.connect(self.refresh_table)
        top_layout.addWidget(self.instance_combo)

        # Bouton Ajouter Media
        self.add_media_button = QPushButton(self.tr('Ajouter Media'), self)
        self.add_media_button.setFixedSize(120, 30)
        self.add_media_button.setIcon(QIcon('resources/icons/robot-512.png'))
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

        # Bouton Mettre à jour JSON
        self.update_json_button = QPushButton(self.tr('Mettre à jour JSON'), self)
        self.update_json_button.setFixedSize(120, 30)
        self.update_json_button.setIcon(QIcon('resources/icons/robot-512.png'))
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
        self.update_json_button.clicked.connect(lambda: self.send_json1())
        top_layout.addWidget(self.update_json_button)

        layout.addLayout(top_layout)

        # Media Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([self.tr('Nom'), self.tr('Description'), self.tr('Preview'), self.tr('Action')])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
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
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        # Pagination Buttons
        pagination_layout = QHBoxLayout()

        self.prev_button = QPushButton(self.tr('Précédent'), self)
        self.prev_button.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_button)

        self.next_button = QPushButton(self.tr('Suivant'), self)
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)

        layout.addLayout(pagination_layout)

        self.populate_table()

        # Actualisation automatique
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_table)
        self.timer.start(5000)

        # Ajouter le footer
        footer = FooterSection(self)
        layout.addWidget(footer)


    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/modules/media_manager_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/modules/media_manager_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/modules/media_manager_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/modules/media_manager_translated.qm")

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

    def send_json1(self, *args):
        transfer_app = FileTransferApp()  # Créer une instance de FileTransferApp
        transfer_app.start_process()  # Appeler la méthode qui lance le processus
        updatejson1 = updatejson
        updatejson1.main()
# Lancer le transfert de fichiers
    def get_instance_list(self):
        instance_folders = [d for d in os.listdir(os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-FB-Robot', 'media')) if d.startswith('media')]
        return [self.tr(f'Instance {i+1}') for i in range(len(instance_folders))]

    def load_media(self):
        media_files = [f for f in os.listdir(self.media_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.mp4'))]
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                json_data = json.load(f)
        else:
            json_data = {'posts': []}

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

    def add_preview_button(self):
        preview_button = QPushButton(self.tr("Aperçu"))
        #preview_button.clicked.connect(lambda: self.show_preview(selected_media))
        # Ajouter le bouton à votre interface

    def show_preview(self, media_path):
        description = self.tr("Votre description ici")  # Récupérez la description réelle du média
        preview_dialog = PreviewDialog(media_path, description, self)
        preview_dialog.exec_()

    def populate_table(self):
        self.table.setRowCount(len(self.media_list))

        for row, media in enumerate(self.media_list):
            nom_item = QTableWidgetItem(media['nom'])
            nom_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 0, nom_item)

            description_item = QTableWidgetItem(media['description'])
            description_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            description_item.setToolTip(media['description'])
            description_item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.table.setItem(row, 1, description_item)

            preview_label = QLabel()
            if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
                pixmap = QPixmap(media['preview_path']).scaled(150, 150, Qt.KeepAspectRatio)
                preview_label.setPixmap(pixmap)
                preview_label.setFixedHeight(150)
            elif media['nom'].endswith('.mp4'):
                preview_label.setText(self.tr('Video File (Click to Preview)'))
                preview_label.setStyleSheet("background-color: lightgray; padding: 10px; border-radius: 5px;")
                preview_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 2, preview_label)

            action_button = QPushButton(self.tr('Action'))
            action_button.setMenu(self.create_action_menu(media))
            self.table.setCellWidget(row, 3, action_button)

    def create_action_menu(self, media):
        menu = QMenu()
        edit_action = menu.addAction(self.tr('Edit'))
        edit_action.triggered.connect(lambda: self.update_media(media))
        delete_action = menu.addAction(self.tr('Supprimer'))
        delete_action.triggered.connect(lambda: self.delete_media(media))
        preview_action = menu.addAction(self.tr('Aperçu'))
        preview_action.triggered.connect(lambda: self.show_preview(media['preview_path']))
        return menu

    def update_media(self, media):
        dialog = UpdateMediaDialog(media, self)
        if dialog.exec_():
            self.save_description(media)
            self.populate_table()

    def save_description(self, media):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                json_data = json.load(f)
        else:
            json_data = {'posts': []}

        found = False
        for post in json_data['posts']:
            if post['image'] == media['preview_path']:
                post['text'] = media['description']
                found = True
                break

        if not found:
            json_data['posts'].append({
                'text': media['description'],
                'image': media['preview_path']
            })

        with open(self.json_file, 'w') as f:
            json.dump(json_data, f, indent=4)

    def delete_media(self, media):
        msg_box = QMessageBox.question(self, self.tr('Confirmation'), self.tr(f'Êtes-vous sûr de vouloir supprimer {media["nom"]} ?'), QMessageBox.Yes | QMessageBox.No)
        if msg_box == QMessageBox.Yes:
            os.remove(media['preview_path'])
            self.media_list.remove(media)
            self.save_to_json()
            self.populate_table()

    def save_to_json(self):
        json_data = {'posts': []}
        for media in self.media_list:
            json_data['posts'].append({
                'text': media['description'],
                'image': media['preview_path']
            })

        with open(self.json_file, 'w') as f:
            json.dump(json_data, f, indent=4)

    def add_new_media(self):
        new_media = self.media_manager.add_media()
        if new_media:
            self.media_list.append(new_media)
            self.populate_table()

    def filter_table(self):
        search_text = self.search_field.text().lower()
        filtered_media = [media for media in self.media_list if search_text in media['nom'].lower() or search_text in media['description'].lower()]
        self.table.setRowCount(len(filtered_media))

        for row, media in enumerate(filtered_media):
            self.table.setItem(row, 0, QTableWidgetItem(media['nom']))
            self.table.setItem(row, 1, QTableWidgetItem(media['description']))

            preview_label = QLabel()
            if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
                pixmap = QPixmap(media['preview_path']).scaled(150, 150, Qt.KeepAspectRatio)
                preview_label.setPixmap(pixmap)
                preview_label.setFixedHeight(150)
            elif media['nom'].endswith('.mp4'):
                preview_label.setText(self.tr('Video File (Click to Preview)'))
                preview_label.setStyleSheet("background-color: lightgray; padding: 10px; border-radius: 5px;")
                preview_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 2, preview_label)

            action_button = QPushButton(self.tr('Action'))
            action_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: 2px solid #0056b3;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
                transition: background-color 0.3s, border-color 0.3s, transform 0.3s;
            }
            QPushButton:hover {
                background-color: #0056b3;
                border-color: #004085;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #004085;
                border-color: #002752;
            }
        """)
            action_button.setMenu(self.create_action_menu(media))
            self.table.setCellWidget(row, 3, action_button)

    def refresh_table(self):
        self.media_list = self.load_media()
        self.populate_table()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.populate_table()

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.media_list):
            self.current_page += 1
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

    def update_json(self, data, file_path='data/media.json'):
        """Met à jour le fichier JSON avec les nouvelles données."""
        try:
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(self.tr("Les données ont été mises à jour dans {file_path}."))
        except Exception as e:
            print(self.tr(f"Erreur lors de la mise à jour du fichier JSON : {e}"))

class UpdateMediaDialog1(QDialog):
    def __init__(self, media, parent=None):
        # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        super().__init__(parent)
        self.media = media
        self.setWindowTitle(self.tr("Mettre à jour le Média"))

        layout = QVBoxLayout(self)

        self.label = QLabel(self.tr("Description :"), self)
        layout.addWidget(self.label)

        self.description_input = QLineEdit(self)
        self.description_input.setText(media['description'])
        layout.addWidget(self.description_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/modules/media_manager_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/modules/media_manager_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/modules/media_manager_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/modules/media_manager_translated.qm")

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
        #self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        self.label.setText(self.tr("Description :"))

    def init_language(self):
        """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')  # Par défaut à l'anglais si non trouvé
        else:
            # Obtenir le code de langue du système
            system_locale = QLocale.system().name()[:2]

            # Dictionnaire pour mapper les codes de langue aux traductions
            language_map = {
                'en': 'en',
                'fr': 'fr',
                'tr': 'tr',
                'ar': 'ar',
            }

            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)

    def accept(self):
        self.media['description'] = self.description_input.text()
        super().accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        self.resize(900, 600)
        self.setCentralWidget(MediaTable(self))

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
