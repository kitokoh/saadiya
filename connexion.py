from imports import *
class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Se connecter")
        self.setStyleSheet("background-color: #f0f0f0;")  # Couleur de fond
        # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()

        
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self.create_header()
        self.create_login_form()
        self.create_footer()

    def create_header(self):
        header = QLabel("Bienvenue dans Mon Application")
        header.setFont(QFont("Arial", 24))
        header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(header)

    def create_login_form(self):
        form_layout = QVBoxLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setFixedWidth(300)
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        self.layout.addWidget(self.password_input)

        login_button = QPushButton("Se connecter")
        login_button.setFont(QFont("Arial", 14))
        login_button.clicked.connect(self.login)
        self.layout.addWidget(login_button)

        create_account_button = QPushButton("Créer un compte")
        create_account_button.setFont(QFont("Arial", 14))
        create_account_button.clicked.connect(self.create_account)
        self.layout.addWidget(create_account_button)
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','fb_robot_install_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','fb_robot_install_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','fb_robot_install_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','fb_robot_install_translated.qm'))

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

    def create_footer(self):
        footer = QLabel("© 2024 Mon Application. Tous droits réservés.")
        footer.setFont(QFont("Arial", 10))
        footer.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(footer)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # Logique de connexion ici
        if username == "admin" and password == "admin":  # Remplacez par votre logique de vérification
            QMessageBox.information(self, "Connexion réussie", "Bienvenue, " + username + "!")
        else:
            QMessageBox.warning(self, "Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")

    def create_account(self):
        # Logique pour rediriger vers la création de compte
        QMessageBox.information(self, "Créer un compte", "Redirection vers la page de création de compte.")

