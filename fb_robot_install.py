import sys
import os
import sqlite3
import ctypes
import subprocess
import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QFrame

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit,
                             QHBoxLayout, QMessageBox, QDialog, QComboBox, QProgressBar)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtWidgets import QMessageBox
from cryptography.fernet import Fernet
from datetime import datetime
from ui.header import HeaderSection  # Import du header
from ui.footer import FooterSection  # Import du footer

# Importation des modules de scripts
from installFBrobotPy import createFolder, system, dossiers, copieMediaDemo, majenv, geninfo
from installFBrobotPy import generedemolicence, updatejson, Visibleinstance, verificateur
from installFBrobotPy import cleTobureau, demarrageAuto, sendLog, invisibleinstance
from installFBrobotPy import affiheMessage, mailSucces, secureChrome

from installFBrobotPy.demarrageAuto import InstallerApp
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
from media_manager import MediaTable

#pour changer la destinationet developper en local c  ext ici que ca se passe 
#user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
# _curentfolder = os.getcwd()  # Ou définissez-le comme un chemin spécifique si nécessaire

# # Définir le chemin du dossier userdata
# user_data_dir = os.path.join(_curentfolder)
def load_encrypted_data(file_path):
        """Charge et déchiffre les données à partir d'un fichier."""
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        
        # Charger la clé de chiffrement
        with open(os.path.join(user_data_dir, 'resources', 'data','key.key'), 'rb') as key_file:
            key = key_file.read()
        
        # Déchiffrer les données
        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')
def get_serial_number():
    """Essaie de récupérer le numéro de série via différentes méthodes."""
    try:
        serial_number = os.popen("wmic bios get serialnumber").read().strip().split("\n")[1].strip()
        if serial_number:
            return serial_number
    except IndexError:
        pass
    
    try:
        serial_number = os.popen("powershell (Get-WmiObject win32_bios).SerialNumber").read().strip()
        return serial_number
    except IndexError:
        print("Erreur : Impossible de récupérer le numéro de série via PowerShell.")
        return None

# Worker thread to execute scripts without blocking the GUI
class ScriptWorker(QThread):
    log_signal = pyqtSignal(str, str)  # message, level
    progress_signal = pyqtSignal(int)

    def __init__(self, scripts):
        super().__init__()
                # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        self.scripts = scripts
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','fb_robot_install_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','fb_robot_install_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','modules','fb_robot_install_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','modules','fb_robot_install_translated.qm'))

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
        pass
        #self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))

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

    def run(self):
        total_scripts = len(self.scripts)
        for i, (friendly_message, script) in enumerate(self.scripts):
            if os.path.exists(script):
                self.log_signal.emit(friendly_message, "info")
                # Execute the script
                try:
# Option spécifique pour masquer la console sous Windows (Win32 et Win64)

                    # Exécution du script sans affichage de la console
                    #subprocess.run(['python', script], stderr=subprocess.STDOUT)
                    #subprocess.run(['runas', '/user:Administrator', 'python ' + script], stderr=subprocess.STDOUT)

                    subprocess.run(['python', script], creationflags=subprocess.CREATE_NO_WINDOW, stderr=subprocess.STDOUT)
                    
                    #subprocess.run(['python', script], check=True)
                    #subprocess.Popen([sys.executable, script],creationflags=subprocess.CREATE_NO_WINDOW )

                    #self.face_main = FbRobot()  # Remplacez ceci par votre classe de page d'accueil
                    #self.face_main.show()

                

                    self.log_signal.emit(self.tr(f"Étape {i+1}/{total_scripts} : {friendly_message} réussie."), "success")
                except subprocess.CalledProcessError:
                    self.log_signal.emit(self.tr(f"Étape {i+1}/{total_scripts} : {friendly_message} échouée."), "error")
                    self.log_signal.emit(self.tr(f"Étape {i+1}/{subprocess.SubprocessError} : {friendly_message} échouée."), "error")

                # Update progress
                progress = int(((i + 1) / total_scripts) * 100)
                self.progress_signal.emit(progress)
            else:
                self.log_signal.emit(self.tr(f"Étape {i+1}/{total_scripts} : Le script {script} est introuvable."), "error")
                progress = int(((i + 1) / total_scripts) * 100)
                self.progress_signal.emit(progress)
        # Signal to indicate completion
        self.log_signal.emit(self.tr("Installation terminée avec succès."), "success")
        self.progress_signal.emit(100)

class LicenseDialog(QDialog):
    def __init__(self, parent=None):
        self.translator = QTranslator()
        self.init_language()  
        super().__init__(parent)
        self.setWindowTitle(self.tr("Demander une licence"))
        self.setFixedSize(300, 150)
        layout = QVBoxLayout()

        label = QLabel(self.tr("Choisissez votre type de licence :"))
        layout.addWidget(label)

        self.combo_box = QComboBox()
        self.combo_box.addItems(["Mensuelle", "Annuelle", "Lifetime"])
        layout.addWidget(self.combo_box)

        submit_btn = QPushButton(self.tr("Envoyer la demande"))
        submit_btn.clicked.connect(self.submit_license_request)
        layout.addWidget(submit_btn)

        self.setLayout(layout)
                # Initialiser le traducteur
# Initialisation de la langue après la création des actions
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','fb_robot_install_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','fb_robot_install_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','modules','fb_robot_install_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','modules','fb_robot_install_translated.qm'))

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
        pass
        #self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))

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




 
    def submit_license_request(self):
        self.chosen_license = self.combo_box.currentText()

        # Afficher un pop-up explicatif
        QMessageBox.information(
            self,
            "Demande de licence",
            "Votre demande de licence est en cours d'envoi. "
            "Veuillez patienter un instant pendant que nous vous enverrons votre licence par email.",
            QMessageBox.Ok
        )

        # Envoyer l'email
        if self.send_license_email():
            QMessageBox.information(
                self,
                "Licence envoyée",
                "Votre licence a été envoyée avec succès. Veuillez vérifier votre boîte de réception.",
                QMessageBox.Ok
            )
        else:
            QMessageBox.warning(
                self,
                "Erreur d'envoi",
                "Une erreur s'est produite lors de l'envoi de votre licence. Veuillez réessayer.",
                QMessageBox.Ok
            )

    def load_encrypted_data(file_path):
            """Charge et déchiffre les données à partir d'un fichier."""
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()
            
            # Charger la clé de chiffrement
            with open(os.path.join(user_data_dir, 'resources', 'data','key.key'), 'rb') as key_file:
                key = key_file.read()
            
            # Déchiffrer les données
            cipher = Fernet(key)
            decrypted_data = cipher.decrypt(encrypted_data)
            return decrypted_data.decode('utf-8')



    def send_license_email(self):
        """Envoie l'email de licence à l'utilisateur."""
        try:
            # Charger les informations d'envoi
            server = load_encrypted_data(os.path.join(user_data_dir, 'resources', 'data','server.txt'))
            sender_email = load_encrypted_data(os.path.join(user_data_dir, 'resources', 'data','adress.txt'))
            password = load_encrypted_data(os.path.join(user_data_dir, 'resources', 'data','tes.txt'))
            
            receiver_email = "turk.novatech@gmail.com"  # Destinataire fixe
            serial_number = get_serial_number()  # Récupérer le numéro de série de l'ordinateur

            subject = "Demande de licence"
            body = (f"Bonjour,\n\n"
                    f"Nous avons reçu une demande de licence pour : {self.chosen_license}.\n"
                    f"Numéro de série de l'ordinateur : {serial_number}\n"
                    f"Veuillez traiter la  demande.\n\n"
                    "Merci de votre confiance.\n")

            # Créer le message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Se connecter au serveur SMTP et envoyer l'email
            with smtplib.SMTP(server, 587) as smtp_server:
                smtp_server.starttls()  # Activer la sécurité
                smtp_server.login(sender_email, password)
                smtp_server.send_message(msg)

            return True  # Email envoyé avec succès
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email: {str(e)}")
            return False  # Échec de l'envoi
class UpdateLicenseDialog(QDialog):
    
    def __init__(self, parent=None):
        self.translator = QTranslator()
        self.init_language()  
        super().__init__(parent)
        
        self.setWindowTitle(self.tr("Mettre à jour la licence"))
        self.setFixedSize(400, 250)
        self.setStyleSheet("background-color: #f0f0f0;")
        # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        layout = QVBoxLayout()
        
        # Créer une bordure autour du formulaire
        frame = QFrame(self)
        frame.setStyleSheet("background-color: #ffffff; border-radius: 10px; padding: 20px;")
        frame_layout = QVBoxLayout(frame)

        label = QLabel(self.tr("Veuillez coller votre code de licence reçu par email :"))
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        frame_layout.addWidget(label)

        self.license_input = QLineEdit(self)
        self.license_input.setPlaceholderText("Code de licence ici...")
        self.license_input.setStyleSheet("padding: 10px; font-size: 12px; border: 1px solid #ccc; border-radius: 5px;")
        frame_layout.addWidget(self.license_input)

        # Créer un bouton pour valider la licence
        validate_btn = QPushButton(self.tr("Valider la licence"))
        validate_btn.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; border: none; border-radius: 5px;")
        validate_btn.clicked.connect(self.validate_license)
        frame_layout.addWidget(validate_btn)

        # Ajouter le cadre au layout principal
        layout.addWidget(frame)

        self.setLayout(layout)
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','fb_robot_install_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','fb_robot_install_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','modules','fb_robot_install_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','modules','fb_robot_install_translated.qm'))

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
        pass
        #self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))

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

    def validate_license(self):
        """Valider et mettre à jour la licence."""
        license_code = self.license_input.text().strip()

        if not license_code:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un code de licence.", QMessageBox.Ok)
            return

        # Enregistrer la licence brute dans un fichier
        instance_number = license_code[-1]  # Dernier chiffre du code de licence
        raw_license_file = f"resources/data/licence{instance_number}.txt"
        
        with open(raw_license_file, 'w') as file:
            file.write(license_code)

        # Décryptage de la licence
        decrypt_char = license_code[-2].lower()  # Avant dernier caractère
        if decrypt_char in ('a', 'b', 'c'):
            self.process_license(decrypt_char, instance_number)
        else:
            QMessageBox.warning(self, "Erreur", "Code de licence invalide.", QMessageBox.Ok)

    def process_license(self, decrypt_char, instance_number):
        """Traite la licence en fonction du caractère de décryptage."""
        # Déterminer le préfixe à utiliser
        if decrypt_char == 'a':
            prefix = "29"
        elif decrypt_char == 'b':
            prefix = "359"
        elif decrypt_char == 'c':
            prefix = "909"

        # Lire le contenu de python.txt
        source_file_path = 'C:/bon/python.txt'
        with open(source_file_path, 'r') as source_file:
            content = source_file.read()

        # Remplacer les trois premiers chiffres du contenu
        updated_content = prefix + content[3:]

        # Créer le dossier robot si nécessaire
        target_directory = f'C:/bon/robot{instance_number}'
        os.makedirs(target_directory, exist_ok=True)

        # Écrire le contenu mis à jour dans le nouveau fichier
        target_file_path = f'{target_directory}/python.txt'
        with open(target_file_path, 'w') as target_file:
            target_file.write(updated_content)

        QMessageBox.information(self, "Succès", "Votre licence a été mise à jour avec succès.", QMessageBox.Ok)

# Fonction pour charger les données cryptées (comme vous l'aviez dans votre exemple)

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Aide"))
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()

        help_text = QLabel(f"""{self.tr('<h2>Aide et Tutoriels</h2>')}
            {self.tr('<p>Bienvenue dans le système de gestion automatisée. Voici quelques instructions pour vous aider :</p>')}
            <ul>
                <li><b>{self.tr("Démarrage Auto")}</b>: {self.tr("programme le demarrage automatisé de l.")}</li>
                <li><b>{self.tr("Démarrer Système")}</b>: {self.tr("Initialise le système.")}</li>
                <li><b>{self.tr("Installer une autre instance")}</b>: {self.tr("Installe une nouvelle instance si le dossier 'robot1' existe.")}</li>
                <li><b>{self.tr("Demander votre licence")}</b>: {self.tr("Demande une licence en choisissant le type souhaité.")}</li>
            </ul>
            {self.tr('<p>Pour toute assistance supplémentaire, veuillez contacter le support technique.</p>')}
        """)
        help_text.setWordWrap(True)
        layout.addWidget(help_text)

        close_btn = QPushButton(self.tr("Fermer"))
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        self.setLayout(layout)
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','fb_robot_install_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','fb_robot_install_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','modules','fb_robot_install_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','modules','fb_robot_install_translated.qm'))

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
        pass
        #self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))

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

class FbRobot(QtWidgets.QWidget):
    def __init__(self):
       # self.conditional_btn_premium = QPushButton(self)

        super().__init__()
                # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()

        self.settings_file = os.path.join(user_data_dir, 'resources', 'data', 'settings.json')

        self.load_settings()
        self.initUI()

    def initUI(self):
        # Configuration de la fenêtre principale
                # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        self.setWindowTitle(self.tr('Yönetim Uygulaması Pro'))
        self.showFullScreen()
        #self.setGeometry(100, 100, 1000, 700)
        self.setWindowIcon(QIcon('resources/icons/robot-512.png'))  # Icône de la fenêtre
        
        #mes variables 
        self.instance_name = None
        self.instance_type = None
        self.facebook_user_name = None
        self.licence_request_date = None
        # Layout principal
        self.main_layout = QVBoxLayout()
        # Ajouter le header
        header = HeaderSection(self, title="FBK Robot Install Instances", app_name="FB ROBOT AI", slogan="AI Marketing & Management Auto")
        self.main_layout.addWidget(header)
        # Titre et sous-titre
        title_label = QLabel(self.tr("Système de Gestion Automatisée"))
        subtitle_label = QLabel(self.tr("Optimisez, installez et gérez vos environnements avec facilité."))
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        subtitle_label.setStyleSheet("font-size: 16px; color: #34495e;")
        self.main_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(subtitle_label, alignment=Qt.AlignCenter)

        # Layout horizontal pour les boutons en haut
        self.btn_layout = QHBoxLayout()
# Ajouter les boutons conditionnels
        self.install_button = QPushButton(self)
        self.update_conditional_buttons()  # Mettez à jour les boutons en fonction des conditions
        self.install_button.setStyleSheet(""" 
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        self.install_button.setText(self.tr("Installer une instance de démo"))
        self.add_new_instance_to_db("demo","user 1",datetime.now().strftime("%Y-%m-%d"))
  # Utilisation de self.tr()
        self.install_button.clicked.connect(self.run_conditional_script)
        self.btn_layout.addWidget(self.install_button)  # Ajoutez le bouton au layout

        # Ajouter les boutons conditionnels supplémentaires
        self.conditional_btn_premium = QPushButton(self)
        self.update_conditional_premium()

        self.conditional_btn_premium.setStyleSheet(""" 
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ec7063;
            }
        """)
        self.conditional_btn_premium.setText(self.tr("Demande Licence"))  # Utilisation de self.tr()
        self.conditional_btn_premium.clicked.connect(self.request_license)

        self.btn_layout.addWidget(self.conditional_btn_premium)

        # Créer les boutons avec icônes et les ajouter au layout
        buttons = [
            (self.tr('Tutoriel'), 'Delacro-Id-Start-Menu.256.png', self.run_menu),
            (self.tr('Start Robot'), 'frpro-demoİnstall.png', self.run_system)
        ]

        for text, icon, function in buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(f'resources/icons/{icon}'))
            btn.setStyleSheet(""" 
                QPushButton {
                    background-color: #2980b9;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #3498db;
                }
            """)
            btn.clicked.connect(function)
            self.btn_layout.addWidget(btn)

       # Ajouter un bouton d'aide
        help_btn = QPushButton(self.tr('Valider licence'), self)  # Utilisation de self.tr()
        help_btn.setIcon(QIcon('resources/icons/information-icon-6055-Windows.ico'))
        help_btn.setStyleSheet(""" 
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #bdc3c7;
            }
        """)
        help_btn.clicked.connect(self.show_help)
        self.btn_layout.addWidget(help_btn)

        #Ajouter un bouton de changement de thème

        self.main_layout.addLayout(self.btn_layout)

        # Barre de progression
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(""" 
            QProgressBar {
                border: 2px solid #ecf0f1;
                border-radius: 5px;
                text-align: center;
                color: #2c3e50;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
                width: 20px;
            }
        """)
        self.main_layout.addWidget(self.progress_bar)

        # Layout horizontal pour la console et l'image
        self.console_image_layout = QHBoxLayout()

        # Console de logs en bas (design amélioré)
        self.log_console = QTextEdit(self)
        self.log_console.setReadOnly(True)
        self.log_console.setStyleSheet(""" 
            font-size: 14px; 
            background-color: #2c3e50; 
            color: #ecf0f1; 
            padding: 10px;
            border: 1px solid #34495e;
            border-radius: 5px;
        """)
        self.console_image_layout.addWidget(self.log_console)

        # Image à droite de la console
        self.right_image_label = QLabel(self)
        self.right_image_label.setPixmap(QPixmap('resources/images/7.jpg').scaled(400, 700, Qt.KeepAspectRatio))
        self.console_image_layout.addWidget(self.right_image_label)

        self.main_layout.addLayout(self.console_image_layout)

        # Initialisation du système de notifications
        self.init_tray()

        # Charger les notifications sonores
        self.success_sound = QSound('resources/sounds/success.wav')
        self.error_sound = QSound('resources/sounds/error.wav')

        # Appliquer le thème initial
        if self.theme == 'dark':
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

        # Ajouter les notifications à la barre système
        self.tray_icon.show()

        # Ajouter un timer pour mettre à jour les boutons conditionnels
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_conditional_buttons)
        self.timer.start(500)  # Mettre à jour toutes les 5 secondes

        # Ajouter sauvegarde automatique à la fermeture
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.destroyed.connect(self.save_settings)
        self.add_new_instance_to_db("demo","user 1",datetime.now().strftime("%Y-%m-%d"))
        # Ajouter le footer
        footer = FooterSection(self)
        self.main_layout.addWidget(footer)

        #self.media_table = QLabel(MediaTable(self))  # Remplacez par votre widget MediaTable réel

        # Définir la mise en page principale
        self.setLayout(self.main_layout)

    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','fb_robot_install_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','fb_robot_install_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','modules','fb_robot_install_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','modules','fb_robot_install_translated.qm'))

        # Installer le traducteur pour appliquer la nouvelle langue
        QApplication.instance().installTranslator(self.translator)
        
            # Sauvegarder le choix de l'utilisateur
        self.save_language_choice(language)


        # Réappliquer la traduction sur tous les éléments visibles de l'interface
        self.retranslateUi()
    def clear_main_layout(self):
        # Supprimer tous les widgets de main_layout
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        

    def show_media_table1(self):
        # Supprimer tous les widgets dans main_layout
        self.clear_main_layout()

        # Ajouter media_table dans main_layout
        self.main_layout.addWidget(self.media_table)
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
        #self.conditional_btn_premium.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))
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
    
    def update_conditional_premium(self):
        if os.path.exists(r'C:\Bon\robot1\python.txt'):
            self.conditional_btn_premium.setText(self.tr("Update licence"))  # Utilisation de self.tr()
        else: 
            self.conditional_btn_premium.setText(self.tr("Demande Licence"))  # Utilisation de self.tr()

    def update_conditional_buttons(self):
        if os.path.exists(r'C:\Bon\robot1'):
            self.install_button.setText(self.tr("Installer une autre instance"))  # Utilisation de self.tr()
            self.add_new_instance_to_db("Premium instance","user 1",datetime.now().strftime("%Y-%m-%d"))
 
        else:
            self.instance_name= "instance Demo"

            self.install_button.setText(self.tr("Installer une instance de démo"))  # Utilisation de self.tr()

    def init_tray(self):
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('resources/icons/robot-512.png'))
        self.tray_icon.setVisible(True)
        tray_menu = QtWidgets.QMenu()

        restore_action = tray_menu.addAction(self.tr("Restaurer"))  # Utilisation de self.tr()
        restore_action.triggered.connect(self.show_normal)

        quit_action = tray_menu.addAction(self.tr("Quitter"))  # Utilisation de self.tr()
        quit_action.triggered.connect(QtWidgets.qApp.quit)

        self.tray_icon.setContextMenu(tray_menu)

    def show_normal(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def toggle_theme(self):
        if self.theme == 'light':
            self.apply_dark_theme()
            self.theme = 'dark'
            self.theme_btn.setText(self.tr('Mode Clair'))  # Utilisation de self.tr()
        else:
            self.apply_light_theme()
            self.theme = 'light'
            self.theme_btn.setText(self.tr('Mode Sombre'))  # Utilisation de self.tr()
        self.save_settings()

    def apply_dark_theme(self):
        self.setStyleSheet(""" 
            QWidget {
                background-color: #34495e;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 1px solid #2980b9;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QProgressBar {
                border: 2px solid #ecf0f1;
                border-radius: 5px;
                text-align: center;
                color: #ecf0f1;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
                width: 20px;
            }
            QTextEdit {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
        """)

    def apply_light_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
                color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 1px solid #2980b9;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QProgressBar {
                border: 2px solid #2c3e50;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
                width: 20px;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #2c3e50;
            }
        """)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.theme = settings.get('theme', 'light')
                    self.license_type = settings.get('license_type', None)
            except json.JSONDecodeError:
                self.theme = 'light'
                self.license_type = None
        else:
            self.theme = 'light'
            self.license_type = None

    def save_settings(self):
        settings = {
            'theme': self.theme,
            'license_type': getattr(self, 'license_type', None)
        }
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            self.log(self.tr("Erreur lors de la sauvegarde des paramètres : {e}").format(e=e), "error")

    def log(self, message, level="info"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        colors = {
            "success": "#2ecc71",  # Vert
            "error": "#e74c3c",    # Rouge
            "info": "#3498db",     # Bleu
            "warning": "#f1c40f"   # Jaune
        }
        color = colors.get(level, "#ecf0f1")  # Couleur par défaut
        self.log_console.append(f"<span style='color: {color};'>{timestamp} - {self.tr(message)}</span>")

    # Fonctions pour les autres boutons
    def run_menu(self):
        self.log(self.tr('Lancement du menu principal...'), "info")
        # Simuler un démarrage avec un message utilisateur
        dialog = HelpDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            chosen_license = dialog.chosen_license
            self.license_type = chosen_license
            self.log(self.tr(f"Licence {chosen_license} demandée."), "info")
            self.save_settings()
            self.show_notification(self.tr(f"Licence {chosen_license} demandée avec succès !"), "info")


    def run_system(self):
        self.log(self.tr('Démarrage du système en cours...'), "info")
        if os.path.exists(os.path.join(user_data_dir, 'installFBrobotPy', 'start.py')):
            try:
                #subprocess.run(['python', 'installFBrobotPy/start.py'], check=True)
                start_script_path = os.path.join(user_data_dir, 'installFBrobotPy', 'start.py')

                subprocess.run(['python', start_script_path], creationflags=subprocess.CREATE_NO_WINDOW, stderr=subprocess.STDOUT)

                #self.face_main = FbRobot()  # Remplacez ceci par votre classe de page d'accueil
                #self.face_main.show()
                #self.setCentralWidget(InstallerApp(self))

        
                self.log(self.tr("Le système a démarré avec succès !"), "success")
                self.show_notification(self.tr("Le système a démarré avec succès !"), "success")
            except subprocess.CalledProcessError:
                self.log(self.tr("Erreur lors du démarrage du système."), "error")
                self.show_notification(self.tr("Erreur lors du démarrage du système."), "error")
        else:
            self.log(self.tr("Le fichier Système est introuvable !"), "error")
            self.show_notification(self.tr("Le fichier Système est introuvable !"), "error")

    def run_conditional_script(self):
        # Liste des scripts à exécuter successivement avec des messages conviviaux
        # scripts = [
        #     (self.tr('verification permissions...'), 'installFBrobotPy/permission.py'),

        #     (self.tr('verification du language...'), 'installFBrobotPy/installGithub.py'),
        #     (self.tr('Verification de system versionnage...'), 'installFBrobotPy/installpython.py'),

        #     (self.tr('Création du dossier de l\'instance...'), 'installFBrobotPy/createFolder.py'),
        #     (self.tr('Initialisation du système...'), 'installFBrobotPy/system.py'),
        #     (self.tr('Organisation des fichiers...'), 'installFBrobotPy/dossiers.py'),
        #     (self.tr('Copie des fichiers média...'), 'installFBrobotPy/copieMediaDemo.py'),
        #     (self.tr('Génération des informations...'), 'installFBrobotPy/geninfo.py'),
        #     (self.tr('Installation de la licence de démo...'), 'installFBrobotPy/generedemolicence.py'),
        #     (self.tr('Mise à jour des configurations...'), 'installFBrobotPy/updatejson.py'),
        #     (self.tr('Finalisation de l\'installation...'), 'installFBrobotPy/Visibleinstance.py'),
        #     (self.tr('Mise à jour de l\'environnement...'), 'installFBrobotPy/majenv.py'),

        #     (self.tr('Vérification du système...'), 'installFBrobotPy/verificateur.py'),
        #     (self.tr('Configuration du bureau...'), 'installFBrobotPy/cletobureau.py'),
        #     (self.tr('Envoi des logs...'), 'installFBrobotPy/sendlog.py'),

        #     (self.tr('Visibilité du dossier...'), 'installFBrobotPy/invisibleinstance.py'),

        #     (self.tr('Affichage du message...'), 'installFBrobotPy/affiheMessage.py'), 
        #     (self.tr('Envoi du mail de succès...'), 'installFBrobotPy/mailSucces.py'),
        #     (self.tr('Rendre invisible bon...'), 'installFBrobotPy/invisibleinstance.py'),
        #     (self.tr('Secure chorme to connect  d\'installation...'), 'installFBrobotPy/secureChrome.py')
        # ]

# Définir le répertoire des données utilisateur
       # user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "NomDeVotreApplication", "resources")

        # Créer une liste de scripts avec les chemins complets
        scripts = [
            (self.tr('verification permissions...'), os.path.join(user_data_dir, 'installFBrobotPy', 'permission.py')),
            (self.tr('verification du language...'), os.path.join(user_data_dir, 'installFBrobotPy', 'installGithub.py')),
            (self.tr('Verification de system versionnage...'), os.path.join(user_data_dir, 'installFBrobotPy', 'installpython.py')),
            (self.tr('Création du dossier de l\'instance...'), os.path.join(user_data_dir, 'installFBrobotPy', 'createFolder.py')),
            (self.tr('Initialisation du système...'), os.path.join(user_data_dir, 'installFBrobotPy', 'system.py')),
            (self.tr('Organisation des fichiers...'), os.path.join(user_data_dir, 'installFBrobotPy', 'dossiers.py')),
            (self.tr('Copie des fichiers média...'), os.path.join(user_data_dir, 'installFBrobotPy', 'copieMediaDemo.py')),
            (self.tr('Génération des informations...'), os.path.join(user_data_dir, 'installFBrobotPy', 'geninfo.py')),
            (self.tr('Installation de la licence de démo...'), os.path.join(user_data_dir, 'installFBrobotPy', 'generedemolicence.py')),
            (self.tr('Mise à jour des configurations...'), os.path.join(user_data_dir, 'installFBrobotPy', 'updatejson.py')),
            (self.tr('Finalisation de l\'installation...'), os.path.join(user_data_dir, 'installFBrobotPy', 'Visibleinstance.py')),
            (self.tr('Mise à jour de l\'environnement...'), os.path.join(user_data_dir, 'installFBrobotPy', 'majenv.py')),
            (self.tr('Vérification du système...'), os.path.join(user_data_dir, 'installFBrobotPy', 'verificateur.py')),
            (self.tr('Configuration du bureau...'), os.path.join(user_data_dir, 'installFBrobotPy', 'cletobureau.py')),
            (self.tr('Envoi des logs...'), os.path.join(user_data_dir, 'installFBrobotPy', 'sendlog.py')),
            (self.tr('Visibilité du dossier...'), os.path.join(user_data_dir, 'installFBrobotPy', 'invisibleinstance.py')),
            (self.tr('Affichage du message...'), os.path.join(user_data_dir, 'installFBrobotPy', 'affiheMessage.py')),
            (self.tr('Envoi du mail de succès...'), os.path.join(user_data_dir, 'installFBrobotPy', 'mailSucces.py')),
            (self.tr('Rendre invisible bon...'), os.path.join(user_data_dir, 'installFBrobotPy', 'invisibleinstance.py')),
            (self.tr('Secure chorme to connect d\'installation...'), os.path.join(user_data_dir, 'installFBrobotPy', 'secureChrome.py'))
        ]

        # Initialize worker thread
        self.worker = ScriptWorker(scripts)
        self.worker.log_signal.connect(self.log)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.start()

    def request_license(self):
        # Affichage du formulaire pour demander la licence
        dialog = LicenseDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            chosen_license = dialog.chosen_license
            self.license_type = chosen_license
            self.log(self.tr(f"Licence {chosen_license} demandée."), "info")
            self.save_settings()
            self.show_notification(self.tr(f"Licence {chosen_license} demandée avec succès !"), "info")

    def show_help(self):
        # Affichage de la fenêtre d'aide
        help_dialog = UpdateLicenseDialog(self)
        help_dialog.exec_()

    def show_notification(self, message, level="info"):
        if level == "info" or level == "success":
            icon = QtWidgets.QSystemTrayIcon.Information
        elif level == "error":
            icon = QtWidgets.QSystemTrayIcon.Critical
        else:
            icon = QtWidgets.QSystemTrayIcon.Information
        self.tray_icon.showMessage(self.tr('Notification'), self.tr(message), icon, 3000)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        if value >= 100:
            self.log(self.tr("Installation terminée avec succès."), "success")
            self.show_notification(self.tr("Installation terminée avec succès !"), "success")
               # Optionnel : Rediriger vers une autre vue, si nécessaire
            #self.setCentralWidget(FbRobot())
            #self.timer.start(3000)  # Mettre à jour toutes les 5 secondes

            #self.show_media_table()


    
    def add_new_instance_to_db(instance_name, instance_type, facebook_user_name, licence_request_date):
        try:
            conn = sqlite3.connect(os.path.join(user_data_dir, 'resources', 'data', 'nova360.db'))
            cursor = conn.cursor()

            # Insertion dans la table `instances`
            cursor.execute("""
                INSERT INTO instances (name, type)
                VALUES (?, ?)
            """, (instance_name, instance_type))
            instance_id = cursor.lastrowid  # Récupérer l'ID de l'instance insérée

            # Insertion dans la table `facebook_users`
            cursor.execute("""
                INSERT INTO facebook_users (name, instance_id)
                VALUES (?, ?)
            """, (facebook_user_name, instance_id))

            # Insertion dans la table `licences`
            cursor.execute("""
                INSERT INTO licences (instance_id, request_date)
                VALUES (?, ?)
            """, (instance_id, licence_request_date))

            # Sauvegarder les changements dans la base de données
            conn.commit()

            #QMessageBox.information(None, self.tr("Succès"), self.tr("Nouvelle instance ajoutée avec succès."))
            
        except sqlite3.Error as e:
            # Si une erreur survient, on annule les changements et on affiche une alerte
            conn.rollback()
            #QMessageBox.critical(None, self.tr("Erreur"), f"{self.tr('Erreur lors de l\'ajout de l\'instance :')} {e}")
            
        finally:
            # Fermer la connexion à la base de données
            conn.close()
    def on_submit(self):
        # Récupérer les valeurs des champs de texte et stocker la date d'aujourd'hui pour licence_request_date
        self.instance_name = self.instance_name_input.text()
        self.instance_type = self.instance_type_input.text()
        self.facebook_user_name = self.facebook_user_input.text()
        self.licence_request_date = datetime.now().strftime("%Y-%m-%d")
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = FbRobot()
    window.show()
    sys.exit(app.exec_())
