import hashlib
import json
import os
import re
import sys
from PyQt5.QtCore import Qt, QTranslator, QLocale, QUrl, QSize
from PyQt5.QtGui import (QFont, QPixmap, QIcon, QDesktopServices, 
                         QColor, QLinearGradient, QPainter, QRegExpValidator)
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel,
    QMessageBox, QHBoxLayout, QComboBox, QFrame, QSizePolicy, 
    QInputDialog, QSpacerItem, QGraphicsDropShadowEffect, QApplication
)
from mail.mail_in_to_in import Mailer1
from mail.mail_in_to_out import Mailer2
import firebase_admin
from firebase_admin import auth, credentials
from google_auth_oauthlib.flow import Flow
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import QPropertyAnimation

# Configuration des chemins
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
os.makedirs(user_data_dir, exist_ok=True)

class GradientFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 700)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#4361ee"))
        gradient.setColorAt(1, QColor("#3a0ca3"))
        painter.fillRect(self.rect(), gradient)
        painter.end()

class RegisterModule(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.init_firebase()
        self.setup_google_auth()
        self.set_styles()
        self.add_shadows()
        self.setup_validators()
        self.translator = QTranslator()
        self.init_language()

    def setup_ui(self):
        """Configure l'interface utilisateur moderne"""
        self.setWindowTitle(self.tr("Créer un compte"))
        self.setWindowIcon(QIcon('resources/icons/878952-Hornet-Secure.ico'))
        self.setFixedSize(1000, 700)
        self.setStyleSheet("background-color: #f5f7fa;")

        # Layout principal
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Section gradient (côté gauche)
        self.setup_gradient_section(main_layout)

        # Section formulaire (côté droit)
        self.setup_form_section(main_layout)

    def setup_gradient_section(self, main_layout):
        """Configure la section avec dégradé moderne"""
        gradient_frame = GradientFrame()
        gradient_frame.setFixedWidth(450)

        content_layout = QVBoxLayout(gradient_frame)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(30)

        # Logo moderne
        logo_label = QLabel()
        logo_pixmap = QPixmap("resources/icons/logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # Texte d'accroche
        title_label = QLabel(self.tr("Rejoignez notre communauté"))
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                margin-top: 20px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)

        subtitle_label = QLabel(self.tr("Créez votre compte en quelques secondes"))
        subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 16px;
                margin-bottom: 30px;
            }
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)

        # Image illustrative
        image_label = QLabel()
        pixmap = QPixmap("resources/images/register_illustration.png")
        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)

        # Ajout des éléments
        content_layout.addWidget(logo_label)
        content_layout.addWidget(title_label)
        content_layout.addWidget(subtitle_label)
        content_layout.addWidget(image_label)
        content_layout.addStretch()

        main_layout.addWidget(gradient_frame)

    def setup_form_section(self, main_layout):
        """Configure la section formulaire moderne"""
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 0;
            }
        """)
        form_frame.setFixedWidth(550)

        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(60, 50, 60, 50)
        form_layout.setSpacing(25)

        # Titre du formulaire
        form_title = QLabel(self.tr("Commençons l'aventure"))
        form_title.setStyleSheet("""
            QLabel {
                color: #2b2d42;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        form_title.setAlignment(Qt.AlignLeft)

        form_subtitle = QLabel(self.tr("Remplissez les champs ci-dessous"))
        form_subtitle.setStyleSheet("""
            QLabel {
                color: #8d99ae;
                font-size: 14px;
                margin-bottom: 30px;
            }
        """)
        form_subtitle.setAlignment(Qt.AlignLeft)

        form_layout.addWidget(form_title)
        form_layout.addWidget(form_subtitle)

        # Formulaire
        self.setup_input_fields(form_layout)

        # Checkbox conditions
        self.terms_checkbox = QCheckBox(self.tr("J'accepte les conditions d'utilisation"))
        self.terms_checkbox.setCursor(Qt.PointingHandCursor)
        form_layout.addWidget(self.terms_checkbox)

        # Bouton d'inscription
        signup_btn = QPushButton(self.tr("S'inscrire maintenant"))
        signup_btn.setCursor(Qt.PointingHandCursor)
        signup_btn.setMinimumHeight(50)
        signup_btn.clicked.connect(self.handle_classic_signup)
        self.signup_button = signup_btn

        form_layout.addWidget(signup_btn)
        form_layout.addSpacing(15)

        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("border-color: #edf2f4;")

        or_label = QLabel(self.tr("OU"))
        or_label.setStyleSheet("""
            QLabel {
                color: #8d99ae;
                font-size: 12px;
                background-color: white;
                padding: 0 15px;
            }
        """)
        or_label.setAlignment(Qt.AlignCenter)

        sep_layout = QHBoxLayout()
        sep_layout.addWidget(separator)
        sep_layout.addWidget(or_label)
        sep_layout.addWidget(separator)

        form_layout.addLayout(sep_layout)
        form_layout.addSpacing(15)

        # Boutons sociaux
        self.setup_social_buttons(form_layout)

        # Lien de connexion
        self.setup_login_link(form_layout)

        main_layout.addWidget(form_frame)

    def setup_input_fields(self, layout):
        """Configure les champs de saisie modernes"""
        # Nom d'utilisateur
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(self.tr("Nom d'utilisateur"))
        self.username_input.setMinimumHeight(50)
        self.username_input.setProperty("class", "input-field")

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText(self.tr("Adresse e-mail"))
        self.email_input.setMinimumHeight(50)
        self.email_input.setProperty("class", "input-field")

        # Mot de passe
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(self.tr("Mot de passe (8 caractères minimum)"))
        self.password_input.setMinimumHeight(50)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setProperty("class", "input-field")

        # Confirmation mot de passe
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText(self.tr("Confirmer le mot de passe"))
        self.confirm_password_input.setMinimumHeight(50)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setProperty("class", "input-field")

        # Licence
        self.licence_combo = QComboBox()
        self.licence_combo.addItems([
            self.tr("Version d'essai (gratuite)"),
            self.tr("Abonnement mensuel - 9.99€"),
            self.tr("Abonnement annuel - 99.99€"),
            self.tr("Licence perpétuelle - 299.99€")
        ])
        self.licence_combo.setMinimumHeight(50)
        self.licence_combo.setProperty("class", "combo-field")

        # Ajout des champs
        layout.addWidget(self.username_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.licence_combo)

    def setup_social_buttons(self, layout):
        """Configure les boutons de connexion sociale"""
        google_btn = QPushButton(self.tr("Continuer avec Google"))
        google_btn.setIcon(QIcon("resources/icons/google-icon.png"))
        google_btn.setIconSize(QSize(24, 24))
        google_btn.setCursor(Qt.PointingHandCursor)
        google_btn.setMinimumHeight(50)
        google_btn.setProperty("class", "social-btn")
        google_btn.clicked.connect(self.handle_google_auth)

        facebook_btn = QPushButton(self.tr("Continuer avec Facebook"))
        facebook_btn.setIcon(QIcon("resources/icons/facebook-icon.png"))
        facebook_btn.setIconSize(QSize(24, 24))
        facebook_btn.setCursor(Qt.PointingHandCursor)
        facebook_btn.setMinimumHeight(50)
        facebook_btn.setProperty("class", "social-btn")
        # facebook_btn.clicked.connect(self.handle_facebook_auth)

        layout.addWidget(google_btn)
        layout.addWidget(facebook_btn)

    def setup_login_link(self, layout):
        """Configure le lien de connexion"""
        login_layout = QHBoxLayout()
        login_layout.setContentsMargins(0, 20, 0, 0)
        login_layout.setSpacing(5)

        account_label = QLabel(self.tr("Vous avez déjà un compte ?"))
        account_label.setStyleSheet("color: #8d99ae; font-size: 14px;")

        login_link = QPushButton(self.tr("Se connecter"))
        login_link.setStyleSheet("""
            QPushButton {
                color: #4361ee;
                font-size: 14px;
                font-weight: bold;
                border: none;
                background: transparent;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        login_link.setCursor(Qt.PointingHandCursor)
        login_link.clicked.connect(self.show_login)

        login_layout.addWidget(account_label)
        login_layout.addWidget(login_link)
        login_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(login_layout)

    def set_styles(self):
        """Définit les styles CSS modernes"""
# Ajoutez ce code dans la méthode set_styles de votre classe RegisterModule

        self.setStyleSheet("""
            /* Style général */
            QDialog {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }

            /* Champs de saisie */
            QLineEdit {
                padding: 0 20px;
                border: 2px solid #edf2f4;
                border-radius: 10px;
                font-size: 15px;
                background-color: #f8f9fa;
                color: #2b2d42;
            }

            QLineEdit:focus {
                border-color: #4361ee;
                background-color: white;
            }

            /* Combo box */
            QComboBox {
                padding: 0 15px;
                border: 2px solid #edf2f4;
                border-radius: 10px;
                font-size: 15px;
                background-color: #f8f9fa;
                color: #2b2d42;
            }

            QComboBox:hover {
                border-color: #adb5bd;
            }

            QComboBox:focus {
                border-color: #4361ee;
            }

            /* Bouton principal */
            QPushButton {
                background-color: #4361ee;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 25px;
            }

            QPushButton:hover {
                background-color: #3a56d4;
            }

            QPushButton:pressed {
                background-color: #3a0ca3;
            }

            /* Boutons sociaux */
            .social-btn {
                background-color: white;
                color: #2b2d42;
                border: 2px solid #edf2f4;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 500;
                padding: 0 20px;
            }

            .social-btn:hover {
                background-color: #f8f9fa;
                border-color: #dee2e6;
            }

            .social-btn:pressed {
                background-color: #e9ecef;
            }

            /* Checkbox */
            QCheckBox {
                color: #4a4e69;
                font-size: 14px;
                spacing: 10px;
            }

            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #adb5bd;
                border-radius: 4px;
            }

            QCheckBox::indicator:checked {
                background-color: #4361ee;
                border: 2px solid #4361ee;
            }
        """)


    def add_shadows(self):
        """Ajoute des ombres portées pour un effet de profondeur"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.signup_button.setGraphicsEffect(shadow)

    def setup_validators(self):
        """Configure les validateurs pour les champs de saisie"""
        # Validateur pour le nom d'utilisateur (lettres, chiffres, underscores)
        username_regex = QRegExp("[a-zA-Z0-9_]+")
        username_validator = QRegExpValidator(username_regex, self.username_input)
        self.username_input.setValidator(username_validator)

        # Validateur pour l'email
        email_regex = QRegExp("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}")
        email_validator = QRegExpValidator(email_regex, self.email_input)
        self.email_input.setValidator(email_validator)

    def init_firebase(self):
        """Initialise la connexion Firebase"""
        try:
            cred_path = os.path.join(user_data_dir, 'resources', 'firebase', 'credentials.json')
            if not firebase_admin._apps and os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'initialiser Firebase: {str(e)}")

    def setup_google_auth(self):
        """Configure l'authentification Google"""
        try:
            client_secret_path = os.path.join(user_data_dir, 'resources', 'firebase', 'client_secret.json')
            if os.path.exists(client_secret_path):
                self.flow = Flow.from_client_secrets_file(
                    client_secret_path,
                    scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 
                           'https://www.googleapis.com/auth/userinfo.profile'],
                    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
                )
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Configuration Google Auth échouée: {str(e)}")

    def handle_google_auth(self):
        """Gère l'authentification Google"""
        try:
            auth_url, _ = self.flow.authorization_url(prompt='consent')
            QDesktopServices.openUrl(QUrl(auth_url))
            self.show_google_code_dialog()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur d'authentification Google: {str(e)}")

    def show_google_code_dialog(self):
        """Affiche une boîte de dialogue pour entrer le code Google"""
        code, ok = QInputDialog.getText(
            self,
            self.tr("Authentification Google"),
            self.tr("Veuillez entrer le code d'autorisation Google:"),
            QLineEdit.Normal
        )

        if ok and code:
            self.process_google_token(code)

    def process_google_token(self, code):
        """Traite le token Google et crée le compte"""
        try:
            self.flow.fetch_token(code=code)
            credentials = self.flow.credentials
            id_info = auth.verify_id_token(credentials.id_token)

            email = id_info['email']
            username = id_info.get('name', email.split('@')[0])

            if not self.terms_checkbox.isChecked():
                QMessageBox.warning(self, "Conditions requises", "Vous devez accepter les conditions d'utilisation")
                return

            # Création du compte Firebase
            user_record = auth.create_user(
                uid=id_info['sub'],
                email=email,
                display_name=username
            )

            # Enregistrement local
            user_data = self.load_user_data()
            user_data.append({
                "uid": user_record.uid,
                "username": username,
                "email": email,
                "auth_method": "google",
                "license": "free",
                "created_at": firebase_admin._utils.datetime_to_timestamp(firebase_admin._utils.datetime.datetime.utcnow())
            })
            self.save_user_data(user_data)

            # Envoi d'email
            Mailer1().send_email_to_user(email, 'welcome_google')

            QMessageBox.information(
                self,
                self.tr("Bienvenue !"),
                self.tr("Votre compte Google a été créé avec succès !")
            )
            self.accept()

        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Erreur"),
                self.tr(f"Une erreur est survenue: {str(e)}")
            )

    def handle_classic_signup(self):
        """Gère l'inscription classique par email/mot de passe"""
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_password_input.text().strip()
        license_type = self.licence_combo.currentText()

        if not self.terms_checkbox.isChecked():
            QMessageBox.warning(self, "Conditions requises", "Vous devez accepter les conditions d'utilisation")
            return

        if not self.validate_form(username, email, password, confirm):
            return

        try:
            # Création du compte Firebase
            user_record = auth.create_user(
                email=email,
                password=password,
                display_name=username
            )

            # Enregistrement local
            user_data = self.load_user_data()
            user_data.append({
                "uid": user_record.uid,
                "username": username,
                "email": email,
                "password": self.hash_password(password),
                "auth_method": "email",
                "license": license_type,
                "created_at": firebase_admin._utils.datetime_to_timestamp(firebase_admin._utils.datetime.datetime.utcnow())
            })
            self.save_user_data(user_data)

            # Envoi d'emails
            Mailer1().send_email_to_user(email, 'welcome')
            Mailer2().send_email(email_type="new_user_notification")

            QMessageBox.information(
                self,
                self.tr("Bienvenue !"),
                self.tr("Votre compte a été créé avec succès !")
            )
            self.accept()

        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Erreur"),
                self.tr(f"Une erreur est survenue: {str(e)}")
            )

    def validate_form(self, username, email, password, confirm):
        """Valide les données du formulaire"""
        errors = []
        
        if len(username) < 3:
            errors.append("Le nom d'utilisateur doit contenir au moins 3 caractères")
            
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Veuillez entrer une adresse email valide")
            
        if len(password) < 8:
            errors.append("Le mot de passe doit contenir au moins 8 caractères")
            
        if password != confirm:
            errors.append("Les mots de passe ne correspondent pas")
            
        if self.user_exists(username, email, self.load_user_data()):
            errors.append("Un compte avec ce nom d'utilisateur ou email existe déjà")
            
        if errors:
            QMessageBox.warning(
                self,
                "Erreurs de validation",
                "\n".join(f"• {error}" for error in errors)
            )
            return False
            
        return True

    def load_user_data(self):
        """Charge les données utilisateur depuis le fichier JSON"""
        data_path = os.path.join(user_data_dir, 'resources', 'data', 'users.json')
        try:
            os.makedirs(os.path.dirname(data_path), exist_ok=True)
            if os.path.exists(data_path):
                with open(data_path, 'r') as f:
                    return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return []

    def save_user_data(self, data):
        """Sauvegarde les données utilisateur dans un fichier JSON"""
        data_path = os.path.join(user_data_dir, 'resources', 'data', 'users.json')
        try:
            with open(data_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {str(e)}")

    def user_exists(self, username, email, user_data):
        """Vérifie si un utilisateur existe déjà"""
        return any(u for u in user_data if u.get('username') == username or u.get('email') == email)

    def hash_password(self, password):
        """Hash le mot de passe avec SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def show_login(self):
        """Ouvre la fenêtre de connexion"""
        from login import LoginModule  # Import local pour éviter les dépendances circulaires
        self.login_window = LoginModule()
        self.login_window.show()
        self.close()

    def init_language(self):
        """Initialise la langue de l'interface"""
        try:
            settings_path = os.path.join(user_data_dir, 'resources', 'settings.json')
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    lang = settings.get('language', 'fr')
            else:
                lang = 'fr'  # Français par défaut
            
            self.load_translation(lang)
        except Exception as e:
            print(f"Erreur de chargement de la langue: {str(e)}")

    def load_translation(self, lang):
        """Charge le fichier de traduction"""
        translation_dir = os.path.join(user_data_dir, 'resources', 'lang')
        translation_file = f"register_{lang}.qm"
        translation_path = os.path.join(translation_dir, lang, 'ui', translation_file)
        
        if os.path.exists(translation_path):
            if self.translator.load(translation_path):
                QApplication.instance().installTranslator(self.translator)
            else:
                print(f"Échec du chargement de la traduction: {translation_path}")

    def retranslateUi(self):
        """Retraduit l'interface lorsque la langue change"""
        # Titres
        self.setWindowTitle(self.tr("Créer un compte"))
        
        # Boutons
        self.signup_button.setText(self.tr("S'inscrire maintenant"))
        
        # Placeholders
        self.username_input.setPlaceholderText(self.tr("Nom d'utilisateur"))
        self.email_input.setPlaceholderText(self.tr("Adresse e-mail"))
        self.password_input.setPlaceholderText(self.tr("Mot de passe (8 caractères minimum)"))
        self.confirm_password_input.setPlaceholderText(self.tr("Confirmer le mot de passe"))
        
        # Items de la combobox
        self.licence_combo.clear()
        self.licence_combo.addItems([
            self.tr("Version d'essai (gratuite)"),
            self.tr("Abonnement mensuel - 9.99€"),
            self.tr("Abonnement annuel - 99.99€"),
            self.tr("Licence perpétuelle - 299.99€")
        ])

    def setup_input_fields(self, layout):
        """Configure les champs de saisie avec des améliorations UX"""
        # Nom d'utilisateur avec icône
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(self.tr("Nom d'utilisateur"))
        self.username_input.setMinimumHeight(50)
        self.username_input.setProperty("class", "input-field")
        self.add_input_icon(self.username_input, "resources/icons/user.png")

        # Email avec icône
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText(self.tr("Adresse e-mail"))
        self.email_input.setMinimumHeight(50)
        self.email_input.setProperty("class", "input-field")
        self.add_input_icon(self.email_input, "resources/icons/email.png")

        # Mot de passe avec icône et bouton de visibilité
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(self.tr("Mot de passe (8 caractères minimum)"))
        self.password_input.setMinimumHeight(50)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setProperty("class", "input-field")
        self.add_input_icon(self.password_input, "resources/icons/lock.png")
        self.add_visibility_toggle(self.password_input)

        # Confirmation mot de passe avec icône et bouton de visibilité
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText(self.tr("Confirmer le mot de passe"))
        self.confirm_password_input.setMinimumHeight(50)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setProperty("class", "input-field")
        self.add_input_icon(self.confirm_password_input, "resources/icons/lock.png")
        self.add_visibility_toggle(self.confirm_password_input)

        # Licence avec style amélioré
        self.licence_combo = QComboBox()
        self.licence_combo.addItems([
            self.tr("Version d'essai (gratuite)"),
            self.tr("Abonnement mensuel - 9.99€"),
            self.tr("Abonnement annuel - 99.99€"),
            self.tr("Licence perpétuelle - 299.99€")
        ])
        self.licence_combo.setMinimumHeight(50)
        self.licence_combo.setProperty("class", "combo-field")
        
        # Ajout des champs avec espacement
        layout.addWidget(self.username_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.licence_combo)

    def add_input_icon(self, input_field, icon_path):
        """Ajoute une icône à gauche d'un champ de saisie"""
        if os.path.exists(icon_path):
            input_field.setStyleSheet(f"""
                QLineEdit {{
                    padding-left: 40px;
                    background-image: url({icon_path});
                    background-position: left center;
                    background-repeat: no-repeat;
                    background-origin: content;
                    padding-left: 40px;
                }}
            """)

    def add_visibility_toggle(self, input_field):
        """Ajoute un bouton de visibilité pour les champs de mot de passe"""
        toggle_button = QPushButton()
        toggle_button.setCursor(Qt.PointingHandCursor)
        toggle_button.setCheckable(True)
        toggle_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                padding: 0;
            }
        """)
        
        # Définir les icônes
        toggle_button.setIcon(QIcon("resources/icons/eye-closed.png"))
        toggle_button.setIconSize(QSize(20, 20))
        
        # Positionner le bouton à droite
        layout = QHBoxLayout(input_field)
        layout.setContentsMargins(0, 0, 10, 0)
        layout.addStretch()
        layout.addWidget(toggle_button)
        
        # Connecter le signal
        toggle_button.toggled.connect(lambda checked: self.toggle_password_visibility(input_field, toggle_button, checked))

    def toggle_password_visibility(self, input_field, button, show):
        """Basculer la visibilité du mot de passe"""
        if show:
            input_field.setEchoMode(QLineEdit.Normal)
            button.setIcon(QIcon("resources/icons/eye-open.png"))
        else:
            input_field.setEchoMode(QLineEdit.Password)
            button.setIcon(QIcon("resources/icons/eye-closed.png"))

    def handle_classic_signup(self):
        """Gère l'inscription avec des feedbacks visuels améliorés"""
        # Désactiver le bouton pendant le traitement
        self.signup_button.setEnabled(False)
        self.signup_button.setText(self.tr("Traitement en cours..."))
        
        # Animation de chargement
        loading_animation = QPropertyAnimation(self.signup_button, b"iconSize")
        loading_animation.setDuration(1000)
        loading_animation.setLoopCount(-1)  # Infini
        loading_animation.setStartValue(QSize(0, 0))
        loading_animation.setEndValue(QSize(20, 20))
        loading_animation.start()

        try:
            # Le reste de la méthode existante...
            username = self.username_input.text().strip()
            email = self.email_input.text().strip()
            password = self.password_input.text().strip()
            confirm = self.confirm_password_input.text().strip()
            license_type = self.licence_combo.currentText()

            if not self.terms_checkbox.isChecked():
                QMessageBox.warning(self, "Conditions requises", "Vous devez accepter les conditions d'utilisation")
                return

            if not self.validate_form(username, email, password, confirm):
                return

            # Création du compte Firebase
            user_record = auth.create_user(
                email=email,
                password=password,
                display_name=username
            )

            # Enregistrement local
            user_data = self.load_user_data()
            user_data.append({
                "uid": user_record.uid,
                "username": username,
                "email": email,
                "password": self.hash_password(password),
                "auth_method": "email",
                "license": license_type,
                "created_at": firebase_admin._utils.datetime_to_timestamp(firebase_admin._utils.datetime.datetime.utcnow())
            })
            self.save_user_data(user_data)

            # Envoi d'emails
            Mailer1().send_email_to_user(email, 'welcome')
            Mailer2().send_email(email_type="new_user_notification")

            # Message de succès amélioré
            success_msg = QMessageBox()
            success_msg.setIconPixmap(QPixmap("resources/icons/success.png").scaled(64, 64))
            success_msg.setWindowTitle(self.tr("Bienvenue !"))
            success_msg.setText(self.tr("Votre compte a été créé avec succès !"))
            success_msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                    border-radius: 10px;
                }
                QLabel {
                    color: #2b2d42;
                    font-size: 14px;
                }
            """)
            success_msg.exec_()
            
            self.accept()

        except Exception as e:
            # Message d'erreur amélioré
            error_msg = QMessageBox()
            error_msg.setIconPixmap(QPixmap("resources/icons/error.png").scaled(64, 64))
            error_msg.setWindowTitle(self.tr("Erreur"))
            error_msg.setText(self.tr(f"Une erreur est survenue: {str(e)}"))
            error_msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                    border-radius: 10px;
                }
                QLabel {
                    color: #2b2d42;
                    font-size: 14px;
                }
            """)
            error_msg.exec_()
            
        finally:
            # Réactiver le bouton
            loading_animation.stop()
            self.signup_button.setEnabled(True)
            self.signup_button.setText(self.tr("S'inscrire maintenant"))
            self.signup_button.setIcon(QIcon())

    def validate_form(self, username, email, password, confirm):
        """Valide les données du formulaire avec des feedbacks visuels"""
        errors = []
        
        # Réinitialiser les styles
        for field in [self.username_input, self.email_input, 
                     self.password_input, self.confirm_password_input]:
            field.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #edf2f4;
                    background-color: #f8f9fa;
                }
            """)
        
        if len(username) < 3:
            errors.append("Le nom d'utilisateur doit contenir au moins 3 caractères")
            self.highlight_error(self.username_input)
            
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Veuillez entrer une adresse email valide")
            self.highlight_error(self.email_input)
            
        if len(password) < 8:
            errors.append("Le mot de passe doit contenir au moins 8 caractères")
            self.highlight_error(self.password_input)
            
        if password != confirm:
            errors.append("Les mots de passe ne correspondent pas")
            self.highlight_error(self.password_input)
            self.highlight_error(self.confirm_password_input)
            
        if self.user_exists(username, email, self.load_user_data()):
            errors.append("Un compte avec ce nom d'utilisateur ou email existe déjà")
            self.highlight_error(self.username_input)
            self.highlight_error(self.email_input)
            
        if errors:
            # Créer un message d'erreur stylisé
            error_box = QMessageBox()
            error_box.setIconPixmap(QPixmap("resources/icons/warning.png").scaled(64, 64))
            error_box.setWindowTitle("Erreurs de validation")
            
            # Liste à puces des erreurs
            error_text = "<ul>"
            for error in errors:
                error_text += f"<li>{error}</li>"
            error_text += "</ul>"
            
            error_box.setTextFormat(Qt.RichText)
            error_box.setText(error_text)
            error_box.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                    border-radius: 10px;
                }
                QLabel {
                    color: #2b2d42;
                    font-size: 14px;
                }
            """)
            error_box.exec_()
            return False
            
        return True

    def highlight_error(self, field):
        """Met en évidence un champ en erreur"""
        field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ef233c;
                background-color: #fff0f1;
            }
        """)
        
        # Animation de tremblement
        animation = QPropertyAnimation(field, b"pos")
        animation.setDuration(100)
        animation.setKeyValueAt(0, field.pos())
        animation.setKeyValueAt(0.2, field.pos() + QPoint(-3, 0))
        animation.setKeyValueAt(0.4, field.pos() + QPoint(3, 0))
        animation.setKeyValueAt(0.6, field.pos() + QPoint(-3, 0))
        animation.setKeyValueAt(0.8, field.pos() + QPoint(3, 0))
        animation.setKeyValueAt(1, field.pos())
        animation.start()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterModule()
    window.show()
    sys.exit(app.exec_())






import hashlib  # Pour le hachage des mots de passe
import json
import os
import re
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout, QComboBox
)

from mail.mail_in_to_in import Mailer1  # Importer la classe Mailer1
from mail.mail_in_to_out import Mailer2  # Importer la classe Mailer1
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from translation import TranslatorManager  # Importer le gestionnaire de traductions

user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QVBoxLayout,QDialog, QWidget
import os
class RegisterModule(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
                # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        # Mise en page principale
        self.setWindowTitle(self.tr("Créer un compte"))
        self.setWindowIcon(QIcon('resources/icons/878952-Hornet-Secure.ico'))  # Spécifiez le chemin de l'icône

        self.setFixedSize(700, 500)
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Zone pour l'image
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("resources/images/7.jpg").scaled(450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.layout.addWidget(self.image_label)

            # Mise en page pour le formulaire
        form_layout = QVBoxLayout()

        # Titre du formulaire
        title_label = QLabel(self.tr("Créer un compte"))
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title_label)

        # Champ de saisie pour le nom d'utilisateur
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText(self.tr("Nom d'utilisateur"))
        self.username_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.username_input)

        # Champ de saisie pour le mot de passe
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText(self.tr("Mot de passe"))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.password_input)

        # Champ de confirmation du mot de passe
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText(self.tr("Confirmer le mot de passe"))
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.confirm_password_input)

        # Champ de saisie pour l'e-mail (obligatoire)
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText(self.tr("Adresse e-mail"))
        self.email_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.email_input)

        # Champ "Licence" avec une liste déroulante
        self.licence_input = QComboBox(self)
        self.licence_input.addItems([
            self.tr("demo"),
            self.tr("annuelle"),
            self.tr("mensuelle"),
            self.tr("lifetime")
        ])  # Ajout des options
        self.licence_input.setCurrentText("demo")  # Sélection par défaut

        # Appliquer un style personnalisé tout en utilisant input_style
        self.licence_input.setStyleSheet(self.input_style() + """
            QComboBox {
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #007BFF;  /* Bordure bleue pour un design soigné */
                background-color: #F8F9FA;  /* Fond clair */
                font-size: 14px;
                transition: border-color 0.3s ease, box-shadow 0.3s ease;
            }

            QComboBox:hover {
                border-color: #0056b3;  /* Bordure bleue plus foncée lors du survol */
            }

            QComboBox:focus {
                border-color: #0056b3;  /* Bordure bleue foncée quand le champ est sélectionné */
                box-shadow: 0 0 8px rgba(0, 86, 179, 0.4);  /* Ombre douce pour la mise en avant */
            }

            QComboBox::drop-down {
                border: none;  /* Retirer la bordure du menu déroulant */
                background-color: #FFFFFF;  /* Fond blanc pour le menu déroulant */
            }

            QComboBox::down-arrow {
                image: url('resources/icons/telgrampng.png');  /* Icône personnalisée pour la flèche */
            }
        """)

        # Ajouter le champ de sélection à la mise en page
        form_layout.addWidget(self.licence_input)

                # Bouton de création de compte
        self.signup_button = QPushButton(self.tr("Créer un compte"), self)
        self.signup_button.setStyleSheet(self.button_style())
        self.signup_button.clicked.connect(self.create_account)
        form_layout.addWidget(self.signup_button)

        # Ajouter le layout du formulaire à la mise en page principale
        self.layout.addLayout(form_layout)


        # Spacer pour centrer le formulaire
        form_layout.addStretch()
    def switch_language(self, language):
        """Permet de changer la langue."""
        # if language == "en":
        #     self.translator.load("resources/lang/en_US/ui/register_translated.qm")
        # elif language == "fr":
        #     self.translator.load("resources/lang/fr_FR/ui/register_translated.qm")
        # elif language == "tr":
        #     self.translator.load("resources/lang/tr_TR/ui/register_translated.qm")
        # elif language == "ar":
        #     self.translator.load("resources/lang/ar_AR/ui/register_translated.qm")

        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','ui','register_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','ui','register_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','ui','register_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','ui','register_translated.qm'))
        elif language == "pt":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','pt_BR','ui','register_translated.qm'))

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
        # """Recharge les textes traduits dans l'interface."""
        # self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # # Par exemple, pour les actions du menu :
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))
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
                'pt': 'pt',

            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)

    def input_style(self):
        """Retourne le style CSS pour les champs de saisie."""
        return """
            QLineEdit {
                padding: 10px;
                border-radius: 8px; /* Bordures arrondies pour un aspect moderne */
                border: 1px solid #007BFF; /* Bordure bleue par défaut */
                background-color: #FFFFFF; /* Fond blanc */
                font-size: 14px; /* Taille de police confortable */
                color: #333333; /* Texte sombre pour une meilleure lisibilité */
                margin-bottom: 20px; /* Espacement entre les champs */
                transition: border-color 0.3s ease, box-shadow 0.3s ease; /* Transition douce */
            }

            QLineEdit:focus {
                border: 1px solid #0056b3; /* Bordure bleue plus foncée lorsqu'en focus */
                box-shadow: 0 0 8px rgba(0, 86, 179, 0.6); /* Ombre pour accentuer l'état actif */
            }

            QLineEdit:disabled {
                background-color: #f2f2f2; /* Fond gris clair pour les champs désactivés */
                border: 1px solid #cccccc; /* Bordure grise pour les champs désactivés */
                color: #999999; /* Texte gris pour les champs désactivés */
            }

            QLineEdit::placeholder {
                color: #888888; /* Couleur grise pour le texte du placeholder */
                font-style: italic; /* Texte en italique pour le placeholder */
            }
        """


    def button_style(self):
        return """
            QPushButton {
                background: linear-gradient(45deg, #007BFF, #0056b3);
                color: blue;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 30px;
                border-radius: 8px;
                border: 2px solid #0056b3;
                transition: background-color 0.3s, transform 0.2s;
            }

            QPushButton:hover {
                background: linear-gradient(45deg, #0056b3, #003d7a);
                transform: scale(1.05);
            }

            QPushButton:pressed {
                background: linear-gradient(45deg, #003d7a, #002b56);
                transform: scale(0.98);
            }

            QPushButton:focus {
                outline: none;
            }
        """

    def load_user_data(self):
        """Charge les données des utilisateurs depuis le fichier JSON."""
        try:
            with open(os.path.join(user_data_dir, 'resources', 'data','users.json'), 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_user_data(self, user_data):
        """Enregistre les données des utilisateurs dans le fichier JSON."""
        with open(os.path.join(user_data_dir, 'resources', 'data','users.json'), 'w') as file:
            json.dump(user_data, file, indent=4)  # Ajouter un indent pour plus de lisibilité

    def validate_email(self, email):
        """Vérifie si l'adresse e-mail est valide."""
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email)

    def user_exists(self, username, email, user_data):
        """Vérifie si l'utilisateur ou l'e-mail existe déjà."""
        return any(user['username'] == username or user['email'] == email for user in user_data)

    def hash_password(self, password):
        """Renvoie le hash SHA256 du mot de passe."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_account(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        email = self.email_input.text().strip()

        if not username or not password or not confirm_password or not email:
           # QMessageBox.warning(self, self.tr("Erreur"), self.tr("Veuillez remplir tous les champs obligatoires."))
            QMessageBox.warning(
                self, 
                self.tr("⚠️ Warning - Missing Information"), 
                self.tr("Please fill in all required fields to proceed."))

            return

        if password != confirm_password:
         #   QMessageBox.warning(self, self.tr("Erreur"), self.tr("Les mots de passe ne correspondent pas."))
            QMessageBox.warning(
                    self, 
                    self.tr("⚠️ Error - Password Mismatch"), 
                    self.tr("The passwords entered do not match. Please check and try again.")
                )

            return

        if len(username) < 3:
            QMessageBox.warning(
                self,
                self.tr("⚠️ Error - Username Too Short"),
                self.tr("The username must be at least 3 characters long. Please enter a longer username.")
            )
            return

        if len(password) < 6:
            QMessageBox.warning(
                self,
                self.tr("⚠️ Error - Password Too Short"),
                self.tr("The password must be at least 6 characters long. Please choose a more secure password.")
            )
            return

        if not self.validate_email(email):
            QMessageBox.warning(
                self,
                self.tr("⚠️ Error - Invalid Email Address"),
                self.tr("The entered email address is invalid. Please enter a correct email address.")
            )
            return

        user_data = self.load_user_data()

        if self.user_exists(username, email, user_data):
            QMessageBox.warning(
                self,
                self.tr("⚠️ Error - Username or Email Already Taken"),
                self.tr("This username or email address is already in use. Please choose a different one.")
            )
            return


        # Chiffrement du mot de passe
        hashed_password = self.hash_password(password)

        # Enregistrer le nouvel utilisateur avec e-mail et mot de passe haché
        user_data.append({"username": username, "password": hashed_password, "email": email})
        self.save_user_data(user_data)

        # Envoi d'un e-mail de confirmation
        mailer = Mailer1()
        mailer.send_email_to_user(user_email=email,email_type= 'mail4')
        mailer2 = Mailer2()
        mailer2.send_email(email_type="admin_message2",extra_subject=None)  # Exemple d'envoi d'e-mail


       # QMessageBox.information(self, self.tr("Succès"), self.tr("Compte créé avec succès ! Vous pouvez maintenant vous connecter."))
        QMessageBox.information(
                    self, 
                    self.tr("🎉 Success - Welcome!"), 
                    self.tr("Your account has been created successfully!\n\n"
                            "✨ You’re now ready to explore our features and enhance your strategies.\n\n"
                            "👉 Log in now to begin your journey with us!"))
                
       
        self.clear_fields()
        self.accept()

        #self.close()  # Fermez le formulaire après la création réussie du compte

    def clear_fields(self):
        """Réinitialise les champs de saisie."""
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.email_input.clear()


import hashlib
import sqlite3
import os
import re
from datetime import datetime
from PyQt5.QtCore import Qt, QTranslator, QLocale, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton, 
                            QLabel, QMessageBox, QHBoxLayout, QComboBox, QWidget)
from PyQt5.QtWidgets import QFrame

# class RegisterModule(QDialog):

#     registration_success = pyqtSignal(str)  # Signal avec le nom d'utilisateur
    


#     def create_input_field(self, placeholder, icon_name, is_password):
#         """Crée un champ de saisie stylisé"""
#         frame = QFrame()
#         frame.setStyleSheet("""
#             QFrame {
#                 background-color: #F5F8FA;
#                 border-radius: 8px;
#                 border: 2px solid #2D74DA;
#             }
#         """)
        
#         layout = QHBoxLayout(frame)
#         layout.setContentsMargins(5, 5, 5, 5)
        
#         # Icône
#         icon_label = QLabel()
#         icon_label.setPixmap(QPixmap(f"resources/icons/{icon_name}").scaled(20, 20))
#         layout.addWidget(icon_label)
        
#         # Champ de saisie
#         field = QLineEdit()
#         field.setPlaceholderText(placeholder)
#         field.setStyleSheet("""
#             QLineEdit {
#                 border: none;
#                 background: transparent;
#                 font-size: 14px;
#                 padding: 5px;
#             }
#         """)
        
#         if is_password:
#             field.setEchoMode(QLineEdit.Password)
#             # Bouton pour afficher/masquer le mot de passe
#             toggle_btn = QPushButton()
#             toggle_btn.setIcon(QIcon("resources/icons/eye.png"))
#             toggle_btn.setStyleSheet("border: none; background: transparent;")
#             toggle_btn.setCheckable(True)
#             toggle_btn.toggled.connect(
#                 lambda state, f=field: f.setEchoMode(QLineEdit.Normal if state else QLineEdit.Password))
#             layout.addWidget(field)
#             layout.addWidget(toggle_btn)
#         else:
#             layout.addWidget(field)
        
#         return frame

#     def get_combo_style(self):
#         """Retourne le style CSS pour la combo box"""
#         return """
#             QComboBox {
#                 padding: 10px;
#                 border-radius: 8px;
#                 border: 2px solid #2D74DA;
#                 background-color: #F5F8FA;
#                 font-size: 14px;
#             }
#             QComboBox:hover {
#                 border-color: #1A59A0;
#             }
#             QComboBox::drop-down {
#                 border: none;
#                 width: 30px;
#             }
#             QComboBox::down-arrow {
#                 image: url('resources/icons/telgrampng.png');
#             }
#         """

#     def get_button_style(self):
#         """Retourne le style CSS pour les boutons"""
#         return """
#             QPushButton {
#                 background-color: #2D74DA;
#                 color: white;
#                 padding: 12px;
#                 border-radius: 8px;
#                 font-size: 16px;
#                 font-weight: bold;
#                 border: 2px solid #1A59A0;
#             }
#             QPushButton:hover {
#                 background-color: #1A59A0;
#             }
#             QPushButton:pressed {
#                 background-color: #154273;
#             }
#         """


#     def init_translations(self):
#         """Initialise le système de traduction"""
#         self.translator = QTranslator()
#         self.translator_manager = TranslatorManager()
#         self.translator_manager.load_translations()
        
#         # Charger la langue par défaut
#         settings_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya", "settings.json")
#         if os.path.exists(settings_path):
#             with open(settings_path) as f:
#                 lang = json.load(f).get('language', 'fr')
#                 self.switch_language(lang)

#     def switch_language(self, language):
#         """Change la langue de l'interface"""
#         translations_path = os.path.join(
#             os.path.expanduser("~"), 
#             "AppData", "Roaming", "saadiya", 
#             "resources", "lang", 
#             f"{language}_{language.upper()}", 
#             "ui", "register_translated.qm"
#         )
        
#         if os.path.exists(translations_path):
#             self.translator.load(translations_path)
#             QApplication.instance().installTranslator(self.translator)
#             self.retranslate_ui()

#     def retranslate_ui(self):
#         """Retraduit l'interface"""
#         self.setWindowTitle(self.tr("Créer un compte"))
#         # Mettre à jour les autres éléments textuels si nécessaire

#     def validate_inputs(self):
#         """Valide tous les champs du formulaire"""
#         username = self.username_input.findChild(QLineEdit).text().strip()
#         password = self.password_input.findChild(QLineEdit).text()
#         confirm_password = self.confirm_password_input.findChild(QLineEdit).text()
#         email = self.email_input.findChild(QLineEdit).text().strip()
#         license_type = self.license_combo.currentText()
        
#         errors = []
        
#         # Validation du nom d'utilisateur
#         if len(username) < 3:
#             errors.append(self.tr("Le nom d'utilisateur doit contenir au moins 3 caractères"))
#         elif not re.match(r'^[a-zA-Z0-9_]+$', username):
#             errors.append(self.tr("Le nom d'utilisateur ne peut contenir que des lettres, chiffres et underscores"))
        
#         # Validation du mot de passe
#         if len(password) < 8:
#             errors.append(self.tr("Le mot de passe doit contenir au moins 8 caractères"))
#         elif password != confirm_password:
#             errors.append(self.tr("Les mots de passe ne correspondent pas"))
        
#         # Validation de l'email
#         if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
#             errors.append(self.tr("L'adresse email n'est pas valide"))
        
#         # Vérification des doublons dans la DB
#         try:
#             self.cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
#             if self.cursor.fetchone():
#                 errors.append(self.tr("Ce nom d'utilisateur ou email est déjà utilisé"))
#         except sqlite3.Error as e:
#             errors.append(self.tr("Erreur de vérification des données"))
#             print(f"Erreur DB: {e}")
        
#         if errors:
#             QMessageBox.warning(self, self.tr("Erreurs de validation"), "\n".join(errors))
#             return False
        
#         return True

#     def handle_registration(self):
#         """Gère le processus d'inscription"""
#         if not self.validate_inputs():
#             return
            
#         username = self.username_input.findChild(QLineEdit).text().strip()
#         password = self.password_input.findChild(QLineEdit).text()
#         email = self.email_input.findChild(QLineEdit).text().strip()
#         license_type = self.license_combo.currentText()
        
#         try:
#             # Hachage du mot de passe
#             hashed_pwd = hashlib.sha256(password.encode()).hexdigest()
            
#             # Création du token de vérification
#             verification_token = hashlib.sha256(f"{username}{email}{datetime.now()}".encode()).hexdigest()
            
#             # Insertion dans la DB
#             self.cursor.execute("""
#                 INSERT INTO users (username, password_hash, email, license_type, verification_token)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (username, hashed_pwd, email, license_type, verification_token))
            
#             self.conn.commit()
            
#             # Envoi des emails
#             Mailer1().send_email_to_user(
#                 user_email=email,
#                 email_type='welcome',
#                 extra_data={'username': username, 'token': verification_token}
#             )
            
#             Mailer2().send_email(
#                 email_type="new_user_notification",
#                 extra_subject=f"Nouvel utilisateur: {username}"
#             )
            
#             # Message de succès
#             QMessageBox.information(
#                 self, 
#                 self.tr("🎉 Inscription réussie !"), 
#                 self.tr("""Votre compte a été créé avec succès !
                
# Un email de confirmation vous a été envoyé à {email}.

# Vous pouvez maintenant vous connecter et commencer à utiliser Leopardo AI.""").format(email=email)
#             )
            
#             self.registration_success.emit(username)
#             self.accept()
            
#         except sqlite3.Error as e:
#             QMessageBox.critical(
#                 self, 
#                 self.tr("Erreur"), 
#                 self.tr("Une erreur est survenue lors de la création du compte. Veuillez réessayer.")
#             )
#             print(f"Erreur DB: {e}")

#     def clear_form(self):
#         """Réinitialise le formulaire"""
#         self.username_input.findChild(QLineEdit).clear()
#         self.password_input.findChild(QLineEdit).clear()
#         self.confirm_password_input.findChild(QLineEdit).clear()
#         self.email_input.findChild(QLineEdit).clear()
#         self.license_combo.setCurrentIndex(0)

#     def closeEvent(self, event):
#         """Gère la fermeture de la fenêtre"""
#         self.conn.close()
#         super().closeEvent(event)




#     registration_success = pyqtSignal(str)  # Signal avec le nom d'utilisateur
    
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         # Configuration DB
#         self.db_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya", "data", "users.db")
        
#         # Initialisation dans le bon ordre
#         self.init_db()  # Doit être appelé en premier
#         self.init_ui()
#         self.init_translations()

#     def init_db(self):
#         """Initialise la base de données SQLite"""
#         try:
#             os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
#             self.conn = sqlite3.connect(self.db_path)
#             self.cursor = self.conn.cursor()
            
#             # Création des tables si elles n'existent pas
#             # Création des tables si elles n'existent pas
#             self.cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS users (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     username TEXT UNIQUE NOT NULL,
#                     password_hash TEXT NOT NULL,
#                     email TEXT UNIQUE NOT NULL,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     last_login TIMESTAMP,
#                     is_active BOOLEAN DEFAULT 1,
#                     failed_attempts INTEGER DEFAULT 0,
#                     verification_token TEXT,
#                     license_type TEXT NOT NULL,
#                     license_expiration TIMESTAMP,
#                     is_verified BOOLEAN DEFAULT 0,
#                     is_locked BOOLEAN DEFAULT 0,
#                     lockout_time TIMESTAMP,
#                     last_active TIMESTAMP


#                 )
#             """)


#             self.cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS licenses (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     name TEXT UNIQUE NOT NULL,
#                     duration_days INTEGER,
#                     price REAL,
#                     features TEXT
#                 )
#             """)
            


#             self.cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS sessions (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     user_id INTEGER REFERENCES users(id),
#                     session_token TEXT UNIQUE NOT NULL,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     expires_at TIMESTAMP NOT NULL,
#                     is_valid BOOLEAN DEFAULT 1,
#                     session_timeout INTEGER DEFAULT 14400,
#                     session_start TIMESTAMP,
#                     session_end TIMESTAMP,  
#                     session_valid BOOLEAN DEFAULT 1,
#                     session_expiration TIMESTAMP,
#                     session_last_active TIMESTAMP
#                 )
#             """)       

#             # Insertion des licences par défaut si nécessaire
#             self.cursor.execute("SELECT COUNT(*) FROM licenses")
#             if self.cursor.fetchone()[0] == 0:
#                 licenses = [
#                     ("demo", 7, 0.0, "Fonctionnalités de base"),
#                     ("mensuelle", 30, 9.99, "Accès complet mensuel"),
#                     ("annuelle", 365, 99.99, "Accès complet annuel"),
#                     ("lifetime", None, 299.99, "Accès permanent")
#                 ]
#                 self.cursor.executemany(
#                     "INSERT INTO licenses (name, duration_days, price, features) VALUES (?, ?, ?, ?)",
#                     licenses
#                 )
            
#             self.conn.commit()
            
#         except sqlite3.Error as e:
#             print(f"Erreur lors de l'initialisation de la base de données: {e}")
#             # Fallback: recréer la connexion
#             self.conn = sqlite3.connect(self.db_path)
#             self.cursor = self.conn.cursor()

#     def init_ui(self):
#         """Initialise l'interface utilisateur"""
#         self.setWindowTitle(self.tr("Créer un compte"))
#         self.setWindowIcon(QIcon('resources/icons/878952-Hornet-Secure.ico'))
#         self.setFixedSize(700, 500)
        
#         # Layout principal
#         main_layout = QHBoxLayout(self)
#         main_layout.setContentsMargins(0, 0, 0, 0)
        
#         # Image de fond (50%)
#         self.image_label = QLabel()
#         self.image_label.setPixmap(QPixmap("resources/images/7.jpg").scaled(
#             350, 500, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
#         main_layout.addWidget(self.image_label)
        
#         # Formulaire (50%)
#         form_frame = QFrame()
#         form_frame.setStyleSheet("""
#             QFrame {
#                 background-color: rgba(255, 255, 255, 0.95);
#                 border-radius: 10px;
#             }
#         """)
        
#         form_layout = QVBoxLayout(form_frame)
#         form_layout.setContentsMargins(30, 30, 30, 30)
#         form_layout.setSpacing(15)
        
#         # Titre
#         title = QLabel(self.tr("Créer un compte"))
#         title.setStyleSheet("""
#             font-size: 24px;
#             font-weight: bold;
#             color: #2c3e50;
#         """)
#         title.setAlignment(Qt.AlignCenter)
#         form_layout.addWidget(title)
        
#         # Champs de formulaire
#         fields = [
#             (self.tr("Nom d'utilisateur"), "user.png", False),
#             (self.tr("Mot de passe"), "lock.png", True),
#             (self.tr("Confirmer le mot de passe"), "lock.png", True),
#             (self.tr("Adresse e-mail"), "email.png", False)
#         ]
        
#         self.username_input = self.create_input_field(*fields[0])
#         self.password_input = self.create_input_field(*fields[1])
#         self.confirm_password_input = self.create_input_field(*fields[2])
#         self.email_input = self.create_input_field(*fields[3])
        
#         form_layout.addWidget(self.username_input)
#         form_layout.addWidget(self.password_input)
#         form_layout.addWidget(self.confirm_password_input)
#         form_layout.addWidget(self.email_input)
        
#         # Liste déroulante des licences
#         self.license_combo = QComboBox()
#         self.license_combo.setStyleSheet(self.get_combo_style())
#         self.populate_license_combo()  # Appelé après l'initialisation de la DB
#         form_layout.addWidget(self.license_combo)
        
#         # Bouton d'inscription
#         self.register_btn = QPushButton(self.tr("Créer un compte"))
#         self.register_btn.setStyleSheet(self.get_button_style())
#         self.register_btn.clicked.connect(self.handle_registration)
#         form_layout.addWidget(self.register_btn)
        
#         main_layout.addWidget(form_frame)

#     def populate_license_combo(self):
#         """Remplit la liste déroulante des licences"""
#         try:
#             # Vérification que le curseur est bien initialisé
#             if not hasattr(self, 'cursor') or not self.cursor:
#                 self.init_db()  # Réinitialisation si nécessaire
                
#             self.cursor.execute("SELECT name FROM licenses ORDER BY price")
#             licenses = self.cursor.fetchall()
            
#             self.license_combo.clear()
#             for license in licenses:
#                 self.license_combo.addItem(license[0])
            
#             # Sélection par défaut sur "demo"
#             index = self.license_combo.findText("demo")
#             if index >= 0:
#                 self.license_combo.setCurrentIndex(index)
                
#         except sqlite3.Error as e:
#             print(f"Erreur lors du chargement des licences: {e}")
#             # Solution de repli avec des valeurs par défaut
#             self.license_combo.clear()
#             self.license_combo.addItems(["demo", "mensuelle", "annuelle", "lifetime"])
#             self.license_combo.setCurrentIndex(0)
            
#             # Tentative de réparation de la base de données
#             try:
#                 self.init_db()
#             except Exception as e:
#                 print(f"Échec de la réinitialisation de la base de données: {e}")

#     # ... (le reste des méthodes reste inchangé)
