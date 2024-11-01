from imports import *

class AddMedia:
    def __init__(self, media_folder):
                # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        self.media_folder = media_folder
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','add_media_install_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','add_media_install_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','modules','add_media_install_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','modules','add_media_install_translated.qm'))

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

    def add_media(self):
        # Options de la boîte de dialogue
        options = QFileDialog.Options()
        options |= QFileDialog.ExistingFiles

        # Boîte de dialogue pour sélectionner des fichiers
        files, _ = QFileDialog.getOpenFileNames(None, self.tr("Sélectionnez les fichiers à ajouter"), "", 
                                                self.tr("Images (*.png *.jpg *.jpeg);;Vidéos (*.mp4);;Tous les fichiers (*)"), options=options)
        if files:
            self._move_and_rename_files(files)

    def _move_and_rename_files(self, files):
        try:
            # Vérifier les fichiers existants dans le dossier des médias
            existing_files = [f for f in os.listdir(self.media_folder) if f.split('.')[0].isdigit()]
            max_number = max([int(f.split('.')[0]) for f in existing_files], default=0)

            # Déplacer et renommer les fichiers
            for file in files:
                max_number += 1
                new_file_name = f"{max_number}{os.path.splitext(file)[1]}"
                new_file_path = os.path.join(self.media_folder, new_file_name)
                shutil.copy(file, new_file_path)

            # Afficher un message de confirmation
            QMessageBox.information(None, self.tr("Médias ajoutés"), 
                                    self.tr(f"{len(files)} fichiers ont été ajoutés avec succès!"), QMessageBox.Ok)

        except Exception as e:
            # Gérer les erreurs et afficher un message d'erreur
            QMessageBox.critical(None, self.tr("Erreur"), 
                                 self.tr(f"Une erreur est survenue lors de l'ajout des fichiers : {str(e)}"), QMessageBox.Ok)

    def tr(self, message):
        # Méthode pour la traduction
        return message
