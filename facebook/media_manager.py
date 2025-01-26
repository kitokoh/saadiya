import json
import os
from PyQt5.QtCore import Qt, QTimer, QLocale
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox
from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QPushButton,
                             QVBoxLayout, QWidget, QLabel, QMessageBox, QHeaderView, QMenu,
                             QAbstractItemView, QLineEdit, QHBoxLayout, QDialog, QDialogButtonBox,
                             QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QApplication, QCheckBox,

                             QStackedWidget, QTableWidgetSelectionRange, QComboBox)

from aiModel.dialogPromp import PromptDialog
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
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','media_manager_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','media_manager_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','modules','media_manager_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','modules','media_manager_translated.qm'))

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
        self.user_choice = 'media1'

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
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','media_manager_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','media_manager_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','modules','media_manager_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','modules','media_manager_translated.qm'))
        elif language == "pt":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','pt_BR','modules','media_manager_translated.qm'))

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
                'pt': 'pt',

            }

            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)
    
    def get_media_text(media_choice):
        # Dictionnaire pour mapper les valeurs
        media_map = {
            'media1': 'text1',
            'media2': 'text2',
            'media3': 'text3',
            'media4': 'text4'
        }
        # Retourner le texte correspondant ou un texte par défaut si la clé n'existe pas
        return media_map.get(media_choice, 'Texte inconnu')

    def load_json(self):
        def get_media_text(media_choice):
            # Dictionnaire pour mapper les valeurs
            media_map = {
                'media1': 'text1',
                'media2': 'text2',
                'media3': 'text3',
                'media4': 'text4'
            }
            # Retourner le texte correspondant ou un texte par défaut si la clé n'existe pas
            return media_map.get(media_choice, 'Texte inconnu')

        # Définir le chemin du fichier JSON
        self.json_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-FB-Robot', 'text', get_media_text(self.user_choice), 'data.json')

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
        def get_media_text(media_choice):
            # Dictionnaire pour mapper les valeurs
            media_map = {
                'media1': 'text1',
                'media2': 'text2',
                'media3': 'text3',
                'media4': 'text4'
            }
            # Retourner le texte correspondant ou un texte par défaut si la clé n'existe pas
            return media_map.get(media_choice, 'Texte inconnu')

        self.json_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-FB-Robot', 'text',  get_media_text(self.user_choice), 'data.json')

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
            #self.media_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-FB-Robot', 'media', self.user_choice)
            if self.user_choice:
                try:
                    self.media_folder = os.path.join(
                        os.path.expanduser('~'), 
                        'Downloads', 
                        'AI-FB-Robot', 
                        'media', 
                        self.user_choice
                    )
                    if not os.path.exists(self.media_folder):
                        os.makedirs(self.media_folder)
                except Exception as e:
                    print(f"Erreur lors de la création du chemin : {e}")

            else:
                print("Erreur : Aucun choix utilisateur disponible.")
                
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


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMenu, QMessageBox, QDialog, QDialogButtonBox, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
import json
import cv2  # Pour extraire une frame des vidéos

class MediaTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('AI Medias Management')
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f4;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-size: 18px;
                color: #333;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
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

        layout = QVBoxLayout(self)

        # Header
        header = QLabel("AI Medias Management")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #007BFF;")
        layout.addWidget(header)

        # Search and Add Media
        top_layout = QHBoxLayout()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Rechercher...")
        self.search_field.setStyleSheet("padding: 8px; font-size: 14px; border-radius: 5px; border: 1px solid #ddd;")
        top_layout.addWidget(self.search_field)

        self.add_media_button = QPushButton("Ajouter Media")
        self.add_media_button.setStyleSheet("background-color: #28a745;")
        self.add_media_button.clicked.connect(self.add_new_media)
        top_layout.addWidget(self.add_media_button)

        layout.addLayout(top_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Nom', 'Description', 'Preview', 'Action'])
        self.table.setStyleSheet("QTableWidget { border: 1px solid #ddd; }")
        layout.addWidget(self.table)

        # Pagination
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Précédent")
        self.prev_button.setStyleSheet("background-color: #6c757d;")
        self.prev_button.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Suivant")
        self.next_button.setStyleSheet("background-color: #6c757d;")
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)

        layout.addLayout(pagination_layout)

        self.populate_table()

    def populate_table(self):
        # Exemple de données
        self.media_list = [
            {'nom': 'image1.jpg', 'description': 'Description 1', 'preview_path': 'path/to/image1.jpg'},
            {'nom': 'video1.mp4', 'description': 'Description 2', 'preview_path': 'path/to/video1.mp4'}
        ]
        self.table.setRowCount(len(self.media_list))

        for row, media in enumerate(self.media_list):
            self.table.setItem(row, 0, QTableWidgetItem(media['nom']))
            self.table.setItem(row, 1, QTableWidgetItem(media['description']))

            # Afficher un thumbnail pour la prévisualisation
            preview_label = QLabel()
            if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
                pixmap = QPixmap(media['preview_path']).scaled(100, 100, Qt.KeepAspectRatio)
                preview_label.setPixmap(pixmap)
            elif media['nom'].endswith('.mp4'):
                # Extraire une frame de la vidéo pour en faire un thumbnail
                cap = cv2.VideoCapture(media['preview_path'])
                ret, frame = cap.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    height, width, channel = frame.shape
                    bytes_per_line = 3 * width
                    q_img = QPixmap.fromImage(QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888))
                    preview_label.setPixmap(q_img.scaled(100, 100, Qt.KeepAspectRatio))
                cap.release()
            preview_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 2, preview_label)

            # Bouton "Action" avec un menu déroulant
            action_button = QPushButton('Action')
            action_button.setStyleSheet("""
                QPushButton {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 12px;
                    font-size: 14px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QPushButton:pressed {
                    background-color: #004080;
                }
            """)
            action_button.setMenu(self.create_action_menu(media))
            self.table.setCellWidget(row, 3, action_button)

    def create_action_menu(self, media):
        menu = QMenu()
        
        # Option "Éditer"
        edit_action = menu.addAction(QIcon('resources/icons/edit.png'), 'Éditer')
        edit_action.triggered.connect(lambda: self.update_media(media))
        
        # Option "Supprimer"
        delete_action = menu.addAction(QIcon('resources/icons/delete.png'), 'Supprimer')
        delete_action.triggered.connect(lambda: self.delete_media(media))
        
        # Option "Aperçu"
        preview_action = menu.addAction(QIcon('resources/icons/preview.png'), 'Aperçu')
        preview_action.triggered.connect(lambda: self.show_preview(media['preview_path']))
        
        # Option "Détail"
        detail_action = menu.addAction(QIcon('resources/icons/detail.png'), 'Détail')
        detail_action.triggered.connect(lambda: self.show_detail(media))
        
        return menu

    def delete_media(self, media):
        # Supprimer le média de la liste et de la table
        confirm = QMessageBox.question(self, 'Confirmation', f'Êtes-vous sûr de vouloir supprimer {media["nom"]} ?', QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.media_list.remove(media)
            self.populate_table()  # Rafraîchir la table immédiatement

    def show_detail(self, media):
        # Afficher une boîte de dialogue avec les détails du média
        dialog = QDialog(self)
        dialog.setWindowTitle('Détails du Média')
        layout = QVBoxLayout()
        
        detail_text = QTextEdit()
        detail_text.setText(f"Nom: {media['nom']}\nDescription: {media['description']}\nChemin: {media['preview_path']}")
        detail_text.setReadOnly(True)
        layout.addWidget(detail_text)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec_()


    def show_update_modal(self):
        """Affiche le modal pour choisir une action."""
        if self.remember_choice is not None:
            # Exécute directement l'action mémorisée
            if self.remember_choice == "text":
                self.add_json_text()
            elif self.remember_choice == "robot":
                self.send_json1()
            return

        # Modal personnalisé
        dialog = UpdateRobotDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Récupérer le choix et exécuter l'action
            choice, remember = dialog.get_choice()
            if choice == "text":
                self.add_json_text()
            elif choice == "robot":
                self.send_json1()
            if remember:
                self.remember_choice = choice

    def get_media_text(media_choice):
        # Dictionnaire pour mapper les valeurs
        media_map = {
            'media1': 'text1',
            'media2': 'text2',
            'media3': 'text3',
            'media4': 'text4'
        }
        # Retourner le texte correspondant ou un texte par défaut si la clé n'existe pas
        return media_map.get(media_choice, 'Texte inconnu')



    def on_instance_changed(self):
        # Logique combinée pour sauvegarder le choix et rafraîchir le tableau
        self.user_choice = self.instance_combo.currentText()  # Sauvegarde du choix
        self.refresh_table()  # Mise à jour du tableau

    def save_user_choice(self):
        # Récupérer le texte sélectionné et le stocker
        self.user_choice = self.instance_combo.currentText()
        print(f"Choix de l'utilisateur: {self.user_choice}")
    # Méthode pour assombrir les couleurs lors du survol
    def darken_color(self, color):
        # Convertir la couleur hexadécimale en valeurs RGB, puis réduire légèrement chaque composant pour un effet "sombre".
        hex_color = color.lstrip('#')
        r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        return f'#{max(r - 20, 0):02X}{max(g - 20, 0):02X}{max(b - 20, 0):02X}'

    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','media_manager_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','media_manager_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','modules','media_manager_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','modules','media_manager_translated.qm'))

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
        
        media_folder_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-FB-Robot', 'media')

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
        #self.media_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-FB-Robot', 'media', self.user_choice)
        if self.user_choice:
            try:
                self.media_folder = os.path.join(
                    os.path.expanduser('~'), 
                    'Downloads', 
                    'AI-FB-Robot', 
                    'media', 
                    self.user_choice
                )
                if not os.path.exists(self.media_folder):
                    os.makedirs(self.media_folder)
            except Exception as e:
                print(f"Erreur lors de la création du chemin : {e}")

        else:
            print("Erreur : Aucun choix utilisateur disponible.")

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

    def create_action_menu1(self, media):
        menu = QMenu()

        # Action Edit
        edit_action = menu.addAction(QIcon('resources/icons/edit.png'), self.tr('Edit'))
        edit_action.setIconVisibleInMenu(True)
        edit_action.triggered.connect(lambda: self.update_media(media))

        # Action Supprimer
        delete_action = menu.addAction(QIcon('resources/icons/delete.png'), self.tr('Supprimer'))
        delete_action.setIconVisibleInMenu(True)
        delete_action.triggered.connect(lambda: self.delete_media(media))

        # Action Aperçu
        preview_action = menu.addAction(QIcon('resources/icons/preview.png'), self.tr('Aperçu'))
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

    def add_new_promt(self):
        #dialog = UpdateMediaDialog(media, self)
        dialog = PromptDialog()
        if dialog.exec_():
           # self.save_description(media)
            self.populate_table()

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
        self.setWindowIcon(QIcon('resources/icons/robot-256.png'))  # Icône de la fenêtre

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
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','media_manager_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','media_manager_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','modules','media_manager_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','modules','media_manager_translated.qm'))

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

class UpdateRobotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Choose an Action"))
        self.setFixedSize(500, 350)
        self.choice = None
        self.remember = False

        self.setStyleSheet("""
            QDialog {
                background-color: #F9FAFB;
                border-radius: 20px;
                border: 2px solid #E4E7EB;
                padding: 20px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 15px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:pressed {
                background-color: #1C5983;
            }
            QLabel {
                color: #2C3E50;
                font-size: 14px;
            }
            QCheckBox {
                color: #7F8C8D;
                font-size: 14px;
            }
        """)

        self.translator = QTranslator()
        self.init_language()  # Initialize language settings
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        self.setWindowIcon(QIcon('resources/icons/robot-256.png'))  # Set dialog icon

        # Title
        title = QLabel(self.tr("Update Your Robot"))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel(self.tr(
            "Please choose one of the options below to update your robot. "
            "You can also save your choice to avoid being prompted again."
        ))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("font-size:8px; color: #7F8C8D;")
        layout.addWidget(subtitle)

        # Option buttons with descriptions
        button_layout = QVBoxLayout()
        button_layout.setSpacing(9)

        # Option 1: Text Update Only
        text_button = QPushButton(self.tr("Text Update Only"))
        text_button.setStyleSheet("background-color: #28A745;")
        text_button.clicked.connect(lambda: self.select_choice("text"))
        button_layout.addWidget(text_button)

        text_desc = QLabel(self.tr(
            "This option updates only the text associated with your robot. "
            "Other parameters will remain unchanged."
        ))
        text_desc.setWordWrap(True)
        text_desc.setStyleSheet("font-size: 13px; color: #7F8C8D;")
        button_layout.addWidget(text_desc)

        # Option 2: Complete Robot Update
        robot_button = QPushButton(self.tr("Complete Robot Update"))
        robot_button.setStyleSheet("background-color: #FD7E14;")
        robot_button.clicked.connect(lambda: self.select_choice("robot"))
        button_layout.addWidget(robot_button)

        robot_desc = QLabel(self.tr(
            "This option performs a full update of your robot, including text "
            "and all associated parameters."
        ))
        robot_desc.setWordWrap(True)
        robot_desc.setStyleSheet("font-size: 13px; color: #7F8C8D;")
        button_layout.addWidget(robot_desc)

        layout.addLayout(button_layout)

        # Checkbox to remember the choice
        self.remember_checkbox = QCheckBox(self.tr("Remember my choice for future updates"))
        layout.addWidget(self.remember_checkbox, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def select_choice(self, choice):
        """Record the user's choice and close the dialog."""
        self.choice = choice
        self.remember = self.remember_checkbox.isChecked()
        self.accept()

    def get_choice(self):
        """Return the selected choice and whether it should be remembered."""
        return self.choice, self.remember

    def switch_language(self, language):
        """Switch the application's language."""
        language_path = os.path.join(user_data_dir, 'resources', 'lang', language, 'modules', 'media_manager_translated.qm')
        if os.path.exists(language_path):
            self.translator.load(language_path)
            QApplication.instance().installTranslator(self.translator)
            self.save_language_choice(language)
            self.retranslate_ui()
        else:
            QMessageBox.warning(self, "Language Error", f"Language file for '{language}' not found.")

    def save_language_choice(self, language):
        """Save the user's language preference to a JSON file."""
        preferences = {'language': language}
        settings_path = os.path.join(user_data_dir, 'resources', 'settings.json')
        with open(settings_path, 'w') as f:
            json.dump(preferences, f)

    def retranslate_ui(self):
        """Retranslate the interface when the language is switched."""
        self.setWindowTitle(self.tr("Choose an Action"))
        # Retranslate other text if needed.

    def init_language(self):
        """Initialize the default language based on system or user preference."""
        settings_path = os.path.join(user_data_dir, 'resources', 'settings.json')
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')
        else:
            system_locale = QLocale.system().name()[:2]
            language_map = {'en': 'en', 'fr': 'fr', 'tr': 'tr', 'ar': 'ar'}
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
