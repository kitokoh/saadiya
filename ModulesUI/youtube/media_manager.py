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
from installFBrobotPy.sendatajson2 import FileTransferApp2
from installFBrobotPy.sendatajson3 import FileTransferApp3
from installFBrobotPy import updatejson
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
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))

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

        #self.setWindowTitle(self.tr("Ajouter Média"))
        #self.setGeometry(100, 100, 400, 300)

        #layout = QVBoxLayout()
        #add_button = QPushButton(self.tr("Ajouter Média"))
       # add_button.clicked.connect(self.add_media)
        #layout.addWidget(add_button)

        #self.setLayout(layout)

    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))

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
        # Définir le chemin du fichier JSON
        self.json_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-YTB-Robot', 'text', 'text1', 'data.json')

        # Vérifier si le fichier et le dossier existent, sinon les créer
        if not os.path.exists(self.json_file):
            # Créer le dossier parent si nécessaire
            os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
            # Créer un fichier JSON avec du contenu par défaut
            with open(self.json_file, 'w') as f:
                json.dump({"posts": []}, f)

        # Charger et retourner le contenu JSON
        with open(self.json_file, 'r') as f:
            return json.load(f)

    def update_json(self, media_data):
        self.json_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-YTB-Robot', 'text', 'text1', 'data.json')

        with open(self.json_file, 'w') as f:
            json.dump(media_data, f)

    def add_media(self):
        options = QFileDialog.Options()

        # Ouvrir une boîte de dialogue pour sélectionner les fichiers média
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            self.tr("Sélectionnez des fichiers média"), 
            "", 
            "Images (*.png *.jpg *.jpeg);;Vidéos (*.mp4 *.mov)", 
            options=options
        )

        if files:
            # Charger les données JSON actuelles
            media_data = self.load_json()
            max_key = 0

            # Trouver le plus grand identifiant dans les noms de fichiers existants
            for media in media_data['posts']:
                try:
                    key = int(media['image'].split('\\')[-1].split('.')[0])
                    if key > max_key:
                        max_key = key
                except ValueError:
                    continue  # Ignore les erreurs de conversion en nombre

            # Préparer le dossier cible
            self.media_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-YTB-Robot', 'media', 'media1')
            if not os.path.exists(self.media_folder):
                os.makedirs(self.media_folder, exist_ok=True)

            # Copier chaque fichier sélectionné avec un nouveau nom
            for file_path in files:
                extension = os.path.splitext(file_path)[1]
                max_key += 1
                new_name = f"{max_key}{extension}"
                new_path = os.path.join(self.media_folder, new_name)

                shutil.copy(file_path, new_path)

                # Ajouter les informations du média dans le fichier JSON
                media_data['posts'].append({
                    "text": self.tr("Description du média"),
                    "image": new_path
                })

            # Mettre à jour le fichier JSON
            self.update_json(media_data)
            QMessageBox.information(self, self.tr("Succès"), self.tr("Média ajouté avec succès !"))



class MediaTable(QWidget):
    def __init__(self, parent=None):
        # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        super().__init__(parent)
        self.media_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-YTB-Robot', 'media', 'media1')
        self.json_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-YTB-Robot', 'text', 'text1', 'data.json')
        self.media_manager = AddMedia(parent=self)

        self.media_list = self.load_media()
        self.page_size = 10
        self.current_page = 0

        # UI Setup
        layout = QVBoxLayout(self)

        # Ajouter le header
        header = HeaderSection(self, title=self.tr("AI Medias Management"), app_name=self.tr("Nova360 AI"), slogan=self.tr("AI Marketing & Management Auto"))
        layout.addWidget(header)

        # Ajouter le menu secondaire
        self.secondary_menu = SecondaryMenu(self)
        self.secondary_menu.menu_selected.connect(self.change_content)
        layout.addWidget(self.secondary_menu)

        # Disposition horizontale pour le titre, la recherche et le bouton "Ajouter"
        top_layout = QHBoxLayout()

        # Label "Liste des media"
        media_label = QLabel(self.tr("Liste des media:"), self)
        media_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #003366;")
        top_layout.addWidget(media_label)

        # Barre de recherche
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText(self.tr("Rechercher..."))
        self.search_field.textChanged.connect(self.filter_table)
        self.search_field.setStyleSheet("""
            QLineEdit {
                padding: 6px;
                font-size: 14px;
                border: 1px solid #007BFF;
                border-radius: 5px;
            }
        """)
        top_layout.addWidget(self.search_field)

        # Dropdown pour les instances
        self.instance_combo = QComboBox(self)
        self.instance_combo.addItems(self.get_instance_list())
        self.instance_combo.currentIndexChanged.connect(self.refresh_table)
        self.instance_combo.setStyleSheet("padding: 5px; font-size: 14px; border-radius: 5px;")
        top_layout.addWidget(self.instance_combo)

        # Fonction pour styliser les boutons avec des couleurs spécifiques
        def style_button(button, color):
            button.setFixedSize(120, 35)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                    font-weight: bold;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
                }}
            """)

        # Boutons stylisés
        self.add_gmini_button = QPushButton(self.tr('AI Description'), self)
        style_button(self.add_gmini_button, "#007BFF")  # Bleu
        self.add_gmini_button.clicked.connect(self.add_new_media)
        top_layout.addWidget(self.add_gmini_button)

        self.add_media_button = QPushButton(self.tr('Ajouter Media'), self)
        style_button(self.add_media_button, "#007BFF")  # Bleu
        self.add_media_button.clicked.connect(self.add_new_media)
        top_layout.addWidget(self.add_media_button)

        self.add_text_button = QPushButton(self.tr('Ajouter Text'), self)
        style_button(self.add_text_button, "#28A745")  # Vert
        self.add_text_button.clicked.connect(self.add_json_text)
        top_layout.addWidget(self.add_text_button)

        self.update_json_button = QPushButton(self.tr('update robot'), self)
        style_button(self.update_json_button, "#FD7E14")  # Orange
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
                font-size: 14px;
                font-weight: bold;
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
        style_button(self.prev_button, "#6c757d")  # Gris
        self.prev_button.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_button)

        self.next_button = QPushButton(self.tr('Suivant'), self)
        style_button(self.next_button, "#6c757d")  # Gris
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

    # Méthode pour assombrir les couleurs lors du survol
    def darken_color(self, color):
        # Convertir la couleur hexadécimale en valeurs RGB, puis réduire légèrement chaque composant pour un effet "sombre".
        hex_color = color.lstrip('#')
        r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        return f'#{max(r - 20, 0):02X}{max(g - 20, 0):02X}{max(b - 20, 0):02X}'

    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))

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
        media_folder_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-YTB-Robot', 'media')

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

    def load_media(self):
        self.media_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-YTB-Robot', 'media', 'media1')

        # Vérifier si le dossier existe
        if not os.path.exists(self.media_folder):
            print("Dossier de médias introuvable.")
            return [{"nom": self.tr("Aucun média disponible"), "description": "", "preview_path": ""}]

        media_files = [f for f in os.listdir(self.media_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.mp4'))]
        
        # Vérifier si la liste de fichiers média est vide
        if not media_files:
            print("Liste vide")
            return [{"nom": "Aucun média disponible", "description": "", "preview_path": ""}]

        # Charger le fichier JSON si disponible
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                json_data = json.load(f)
        else:
            json_data = {'posts': []}

        # Créer la liste des médias
        media_list = []
        for media in media_files:
            media_info = {
                'nom': media,
                'description': '',
                'preview_path': os.path.join(self.media_folder, media)
            }
            # Associer une description si disponible dans le fichier JSON
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
            if not isinstance(media, dict):
                print(self.tr("Erreur : L'élément de media_list n'est pas un dictionnaire."))
                return
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
            action_button.setStyleSheet("""
                QPushButton {
                    background-color: #2F4F9B;  /* Bleu foncé */
                    color: white;
                    border-radius: 8px;
                    padding: 8px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1D2E5B;
                }
                QPushButton:pressed {
                    background-color: #16224A;
                }
            """)
            self.table.setCellWidget(row, 3, action_button)

    def create_action_menu(self, media):
        menu = QMenu()

        # Action Edit
        edit_action = menu.addAction(QIcon('resources/icons/Hopstarter-Soft-Scraps-Edit-Document.256.png'), self.tr('Edit'))
        edit_action.setIconVisibleInMenu(True)
        edit_action.triggered.connect(lambda: self.update_media(media))

        # Action Supprimer
        delete_action = menu.addAction(QIcon('resources/icons/delete.png'), self.tr('Supprimer'))
        delete_action.setIconVisibleInMenu(True)
        delete_action.triggered.connect(lambda: self.delete_media(media))

        # Action Aperçu
        preview_action = menu.addAction(QIcon('resources/icons/camera-icon-59.png'), self.tr('Aperçu'))
        preview_action.setIconVisibleInMenu(True)
        preview_action.triggered.connect(lambda: self.show_preview(media['preview_path']))

        # Style du menu
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #CCCCCC;
                padding: 5px;
                font-size: 14px;
            }
            QMenu::item {
                padding: 8px 12px;
            }
            QMenu::item:selected {
                background-color: #F2F2F2;
            }
        """)

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
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssaping','fb_robot_install_translated.qm'))

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
        self.setWindowTitle(self.tr('AI YTB ROBOT Pro'))
        self.resize(900, 600)
        self.setCentralWidget(MediaTable(self))

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
