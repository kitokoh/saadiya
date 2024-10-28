from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit,
    QFileDialog, QFrame, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor
from PyQt5.QtCore import Qt
import re
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
class UpdateMediaDialog(QDialog):
    def __init__(self, media, parent=None):

                # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()


        super().__init__(parent)
        self.setWindowTitle(self.tr(f'Éditer Média: {media["nom"]}'))
        self.media = media
        self.setFixedSize(600, 400)

        # Palette pour le fond
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Partie gauche : Zone de texte pour la description
        left_layout = QVBoxLayout()
        
        # Titre
        title = QLabel(self.tr("Mise à jour du Média"))
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color: #007BFF;")
        left_layout.addWidget(title)

        # Sous-titre
        subtitle = QLabel(self.tr("Veuillez mettre à jour les informations ci-dessous."))
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setStyleSheet("color: #555;")
        left_layout.addWidget(subtitle)

        # Zone de texte pour la description
        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText(self.tr("Entrez une description (incluant des hashtags et des contacts)..."))
        self.description_input.setText(media['description'])
        left_layout.addWidget(self.description_input)

        # Indications pour la description
        instructions = QLabel(self.tr("Instructions : Veuillez ajouter une description, au moins un hashtag, et vos contacts."))
        instructions.setFont(QFont("Arial", 10))
        instructions.setStyleSheet("color: #888;")
        left_layout.addWidget(instructions)

        # Bouton pour parcourir les fichiers
        self.browse_button = QPushButton(self.tr('Parcourir Image/Vidéo'), self)
        self.browse_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 5px; padding: 10px;")
        self.browse_button.clicked.connect(self.change_image)
        left_layout.addWidget(self.browse_button)

        # Boutons d'enregistrement et d'annulation
        button_layout = QHBoxLayout()
        self.save_button = QPushButton(self.tr('Enregistrer'), self)
        self.save_button.setStyleSheet("background-color: #28A745; color: white; border-radius: 5px; padding: 10px;")
        self.save_button.clicked.connect(self.save_changes)
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton(self.tr('Annuler'), self)
        self.cancel_button.setStyleSheet("background-color: #DC3545; color: white; border-radius: 5px; padding: 10px;")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        left_layout.addLayout(button_layout)
        self.layout.addLayout(left_layout)

        # Partie droite : Zone d'aperçu
        self.preview_frame = QFrame(self)
        self.preview_frame.setStyleSheet("border: 1px solid #007BFF; border-radius: 5px; padding: 10px; background: white;")
        self.layout.addWidget(self.preview_frame)

        self.media_preview = QLabel(self)
        self.media_preview.setAlignment(Qt.AlignCenter)
        self.media_preview.setFixedHeight(300)
        self.layout.addWidget(self.media_preview)

        # Affichage du média
        self.display_media()
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/modules/main_fb_robot_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/modules/main_fb_robot_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/modules/main_fb_robot_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/modules/main_fb_robot_translated.qm")

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
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
        self.instance_action.setText(self.tr('Instance'))
        self.media_action.setText(self.tr('Médias'))
        self.group_action.setText(self.tr('Groupes'))
        self.about_action.setText(self.tr('About'))
        self.certificate_action.setText(self.tr('Certif'))
        self.language_menu.setTitle(self.tr('Langue'))

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

    def display_media(self):
        """ Affiche l'aperçu du média en fonction de son type """
        if self.media['nom'].endswith(('.png', '.jpg', '.jpeg')):
            pixmap = QPixmap(self.media['preview_path']).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.media_preview.setPixmap(pixmap)
        elif self.media['nom'].endswith('.mp4'):
            self.media_preview.setText(self.tr('Vidéo : ') + self.media['nom'])

    def change_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, self.tr("Sélectionner une image ou vidéo"), "", 
            self.tr("Fichiers Image (*.png *.jpg *.jpeg);;Fichiers Vidéo (*.mp4)"))
        if file_name:
            if file_name.endswith(('.png', '.jpg', '.jpeg')):
                pixmap = QPixmap(file_name).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.media_preview.setPixmap(pixmap)
                self.media['preview_path'] = file_name
            elif file_name.endswith('.mp4'):
                self.media_preview.setText(self.tr('Vidéo : ') + file_name)
                self.media['preview_path'] = file_name

    def save_changes(self):
        description_text = self.description_input.toPlainText()
        if not self.validate_description(description_text):
            return
        self.media['description'] = description_text
        self.accept()

    def validate_description(self, description):
        if not re.search(r'#\w+', description):
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("La description doit contenir au moins un hashtag."))
            return False
        if not re.search(r'(\+?\d{1,3}[- ]?)?\(?\d{1,4}?\)?[- ]?\d{1,4}[- ]?\d{1,4}[- ]?\d{1,9}', description) and not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', description):
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("La description doit contenir un contact valide (numéro de téléphone ou email)."))
            return False
        return True
