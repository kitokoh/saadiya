# import os
# import random
# import subprocess
# import sys
# from datetime import datetime
# from PyQt5 import QtWidgets, uic
# from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo


# class LicenseGeneratorApp(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(LicenseGeneratorApp, self).__init__()
#         uic.loadUi('interface.ui', self)  # Charger l'interface à partir d'un fichier .ui

#         self.licence_folder = "C:\\bon"
#         self.licence_file = "test.txt"
#         self.generate_button.clicked.connect(self.generate_license)

#         self.translator = QTranslator(self)
#         self.setup_translations()

#     def setup_translations(self):
#         locale = QLocale.system().name()
#         if self.translator.load(locale, QLibraryInfo.location(QLibraryInfo.TranslationsPath)):
#             QtWidgets.QApplication.instance().installTranslator(self.translator)

#     def generate_license(self):
#         error_flag = 0

#         # Créer le dossier C:\bon s'il n'existe pas
#         if not os.path.exists(self.licence_folder):
#             try:
#                 os.makedirs(self.licence_folder)
#             except Exception as e:
#                 QtWidgets.QMessageBox.critical(self, "Erreur", f"[ERROR] - Impossible de créer le dossier {self.licence_folder}.")
#                 return

#         # Supprimer test.txt s'il existe déjà
#         licence_file_path = os.path.join(self.licence_folder, self.licence_file)
#         if os.path.exists(licence_file_path):
#             try:
#                 os.remove(licence_file_path)
#             except Exception as e:
#                 QtWidgets.QMessageBox.critical(self, "Erreur", f"[ERROR] - Impossible de supprimer l'ancien fichier {self.licence_file}.")
#                 error_flag = 1

#         # Récupérer le numéro de série de l'ordinateur
#         serial = self.get_serial_number()
#         if not serial:
#             QtWidgets.QMessageBox.critical(self, "Erreur", "[ERROR] - Impossible de récupérer le numéro de série de l'ordinateur.")
#             error_flag = 1
#             return

#         # Récupérer l'adresse MAC
#         mac = self.get_mac_address()
#         if not mac:
#             QtWidgets.QMessageBox.critical(self, "Erreur", "[ERROR] - Impossible de récupérer l'adresse MAC valide.")
#             error_flag = 1
#             return

#         # Récupérer la date et l'heure actuelles
#         current_datetime = self.get_current_datetime()

#         # Récupérer le nom de l'utilisateur actuel
#         username = os.getlogin()

#         # Générer une chaîne aléatoire de 500 caractères
#         rand_str = self.generate_random_string(500)

#         # Composer la licence
#         licence = f"001{serial}:{mac}{current_datetime}{username}{rand_str}"

#         # Enregistrer la licence dans test.txt
#         try:
#             with open(licence_file_path, 'w') as licence_file:
#                 licence_file.write(licence)
#         except Exception as e:
#             QtWidgets.QMessageBox.critical(self, "Erreur", f"[ERROR] - Impossible d'écrire dans {self.licence_file}.")
#             error_flag = 1
#             return

#         # Message de succès
#         #QtWidgets.QMessageBox.information(self, "Succès", f"[SUCCES] - La licence a été générée et enregistrée dans {self.licence_folder}\\{self.licence_file}.")

#         if error_flag:
#             QtWidgets.QMessageBox.warning(self, "Échec", "[ECHEC] - Une erreur s'est produite pendant l'exécution du script.")
#         else:
#             QtWidgets.QMessageBox.information(self, "Fin", "[FIN] - Script exécuté avec succès.")

#     def get_serial_number(self):
#         try:
#             serial = subprocess.check_output("wmic bios get serialnumber", shell=True).decode().split("\n")[1].strip()
#             return serial
#         except Exception:
#             return None

#     def get_mac_address(self):
#         try:
#             mac = subprocess.check_output("getmac /fo csv /nh", shell=True).decode().split(",")[0].replace('"', '').strip()
#             if mac != "N/A":
#                 return mac
#             else:
#                 return None
#         except Exception:
#             return None

#     def get_current_datetime(self):
#         now = datetime.now()
#         return now.strftime("%d%m%Y%H%M")

#     def generate_random_string(self, length):
#         chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
#         return ''.join(random.choice(chars) for _ in range(length))




# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     window = LicenseGeneratorApp()
#     window.show()
#     sys.exit(app.exec_())
    
# if __name__ == "__main__":
#     main()  # Appelle la fonction main si le script est exécuté directement

# import os
# import random
# import subprocess
# import sys
# from datetime import datetime
# import time

# class LicenseGenerator:
#     def __init__(self):
#         self.licence_folder = "C:\\bon"
#         self.licence_file = "test.txt"

#     def generate_license(self):
#         error_flag = 0

#         # Créer le dossier C:\bon s'il n'existe pas
#         if not os.path.exists(self.licence_folder):
#             try:
#                 os.makedirs(self.licence_folder)
#             except Exception as e:
#                 print(f"[ERROR] - Impossible de créer le dossier {self.licence_folder}.")
#                 return

#         # Supprimer test.txt s'il existe déjà
#         licence_file_path = os.path.join(self.licence_folder, self.licence_file)
#         if os.path.exists(licence_file_path):
#             try:
#                 os.remove(licence_file_path)
#             except Exception as e:
#                 print(f"[ERROR] - Impossible de supprimer l'ancien fichier {self.licence_file}.")
#                 error_flag = 1

#         # Récupérer le numéro de série de l'ordinateur
#         serial = self.get_serial_number()
#         if not serial:
#             print("[ERROR] - Impossible de récupérer le numéro de série de l'ordinateur.")
#             error_flag = 1
#             return

#         # Récupérer l'adresse MAC
#         mac = self.get_mac_address()
#         if not mac:
#             print("[ERROR] - Impossible de récupérer l'adresse MAC valide.")
#             error_flag = 1
#             return

#         # Récupérer la date et l'heure actuelles
#         current_datetime = self.get_current_datetime()

#         # Récupérer le nom de l'utilisateur actuel
#         username = os.getlogin()

#         # Générer une chaîne aléatoire de 500 caractères
#         rand_str = self.generate_random_string(500)

#         # Composer la licence
#         licence = f"001{serial}:{mac}{current_datetime}{username}{rand_str}"

#         # Enregistrer la licence dans test.txt
#         try:
#             with open(licence_file_path, 'w') as licence_file:
#                 licence_file.write(licence)
#         except Exception as e:
#             print(f"[ERROR] - Impossible d'écrire dans {self.licence_file}.")
#             error_flag = 1
#             return

#         # Message de succès
#         if error_flag:
#             print("[ÉCHEC] - Une erreur s'est produite pendant l'exécution du script.")
#         else:
#             print(f"[SUCCÈS] - La licence a été générée et enregistrée dans {self.licence_folder}\\{self.licence_file}.")
        
#         # Pause avant la fermeture
#         print("Le script se termine dans 2 secondes...")
#         time.sleep(2)

#     def get_serial_number(self):
#         try:
#             serial = subprocess.check_output("wmic bios get serialnumber", shell=True).decode().split("\n")[1].strip()
#             return serial
#         except Exception:
#             return None

#     def get_mac_address(self):
#         try:
#             mac = subprocess.check_output("getmac /fo csv /nh", shell=True).decode().split(",")[0].replace('"', '').strip()
#             if mac != "N/A":
#                 return mac
#             else:
#                 return None
#         except Exception:
#             return None

#     def get_current_datetime(self):
#         now = datetime.now()
#         return now.strftime("%d%m%Y%H%M")

#     def generate_random_string(self, length):
#         chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
#         return ''.join(random.choice(chars) for _ in range(length))


# def main():
#     generator = LicenseGenerator()
#     generator.generate_license()

# if __name__ == "__main__":
#     main()  # Appelle la fonction main si le script est exécuté directement
import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from cryptography.fernet import Fernet
import subprocess
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

# Configuration du logger

def adjust_permissions(directory="resources"):
    """Modifie les permissions du répertoire pour permettre l'écriture et la lecture."""
    try:
        # Commande pour accorder à l'utilisateur courant les droits d'écriture et de lecture
        current_user = os.getlogin()
        command = f'icacls "{directory}" /grant {current_user}:(OI)(CI)F /T'
        subprocess.run(command, shell=True, check=True)
        logging.info(f"Permissions mises à jour pour {current_user} dans {directory}.")
    except Exception as e:
        logging.error(f"Erreur lors de la mise à jour des permissions : {e}")

def decrypt_data(encrypted_data, key):
    """Déchiffre les données cryptées."""
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()

def read_credentials():
    """Lit les informations d'identification cryptées à partir des fichiers texte."""
    try:
        resources_path = os.path.join(user_data_dir , "resources", "data")

        # Lire la clé de chiffrement dans un fichier clé
        with open(os.path.join(resources_path, 'key.key'), 'rb') as key_file:
            key = key_file.read()

        # Lire les informations d'authentification cryptées
        with open(os.path.join(resources_path, "server.txt"), 'rb') as f:
            encrypted_server = f.read().strip()
        with open(os.path.join(resources_path, "adress.txt"), 'rb') as f:
            encrypted_sender_email = f.read().strip()
        with open(os.path.join(resources_path, "tes.txt"), 'rb') as f:
            encrypted_password = f.read().strip()

        # Déchiffrer les informations
        server = decrypt_data(encrypted_server, key)
        sender_email = decrypt_data(encrypted_sender_email, key)
        password = decrypt_data(encrypted_password, key)

        return server, sender_email, password
    except FileNotFoundError as e:
        logging.error(f"Erreur lors de la lecture des informations d'identification : {e}")
        raise

def send_email():
    """Envoie un email avec le fichier journalinstallation.txt en pièce jointe."""
    try:
        # Chemin du fichier journal
        journal_file = os.path.join(user_data_dir, "resources", "journalInstallation.txt")
        
        # Lire les informations d'identification
        server, sender_email, password = read_credentials()

        # Création du message
        recipient_email = "turk.novatech@gmail.com"
        subject = "Rapport installation instances"
        body = "Bonjour,\n\nVeuillez trouver ci-joint le rapport d'installation dewa robot.\n\nCordialement,\nVotre Système"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Ajout du corps de l'email
        msg.attach(MIMEText(body, 'plain'))

        # Ajout de la pièce jointe
        with open(journal_file, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name=os.path.basename(journal_file))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(journal_file)}"'
        msg.attach(part)

        # Connexion au serveur SMTP et envoi du mail
        with smtplib.SMTP(server, 587) as smtp:  # On suppose ici que ton serveur utilise le port 587 (TLS)
            smtp.starttls()  # Si ton serveur nécessite TLS
            smtp.login(sender_email, password)
            smtp.sendmail(sender_email, recipient_email, msg.as_string())

        logging.info("Email envoyé avec succès.")
        
        # Suppression du fichier journal après l'envoi
        os.remove(journal_file)

    except Exception as e:
        logging.error(f"Erreur lors de l'envoi de l'email : {e}")
        try:
            # Cacher le fichier si échec de l'envoi
            os.system(f'attrib +h +s "{journal_file}"')
            logging.info("Fichier caché en raison de l'échec de l'envoi.")
        except Exception as hide_err:
            logging.error(f"Erreur lors du masquage du fichier : {hide_err}")

if __name__ == "__main__":
    adjust_permissions()  # Ajustement des permissions avant l'envoi d'email
    send_email()
