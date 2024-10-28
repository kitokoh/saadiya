# import sys
# import os
# import subprocess
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QLabel, QMessageBox
# )
# from PyQt5.QtCore import QTimer

# class PythonScriptRunnerApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#         self.run_script()  # Exécute le script au démarrage

#     def initUI(self):
#         self.setWindowTitle("Exécuter le Script Python")
#         self.setGeometry(100, 100, 300, 100)  # Dimension de la fenêtre

#         self.label = QLabel("Exécution du script en cours...", self)
#         self.label.setGeometry(10, 10, 280, 30)  # Positionnement de l'étiquette

#     def run_script(self):
#         # Chemins pour l'environnement virtuel et le script Python
#         env_path = r"C:\bon\robot1\env1\Scripts\activate"
#         script_path = r"C:\bon\robot1\mailapresinstall.py"

#         try:
#             # Commande pour exécuter le script dans l'environnement virtuel
#             command = f'cmd /c "{env_path} && python {script_path}"'
#             result = subprocess.run(command, shell=True, capture_output=True, text=True)

#             # Affiche le résultat de l'exécution du script
#             if result.returncode == 0:
#                # QMessageBox.information(self, "Succès", "Le script a été exécuté avec succès !")
#                 print(result.stdout)  # Affiche la sortie standard
#             else:
#                 QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de l'exécution du script.")
#                 print(result.stderr)  # Affiche l'erreur si elle existe

#         except Exception as e:
#             QMessageBox.critical(self, "Erreur", f"Une erreur inattendue est survenue : {str(e)}")

#         # Ferme l'application après 1 seconde
#         QTimer.singleShot(0, self.close)




# def main():
#     app = QApplication(sys.argv)

#     # Création et affichage de l'application
#     ex = PythonScriptRunnerApp()
#     ex.show()

#     sys.exit(app.exec_())
    
# if __name__ == "__main__":
#     main()  # Appelle la fonction main si le script est exécuté directement
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from cryptography.fernet import Fernet
import logging
import os
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

# Configuration du fichier de log

# Fonction pour décrypter les informations avec Fernet
def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data).decode()

# Fonction pour attacher des fichiers à l'email
def attach_files(msg, attachments):
    for file in attachments:
        try:
            with open(file, 'rb') as attachment_file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment_file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file)}')
                msg.attach(part)
            logging.info(f"Fichier joint : {file}")
        except Exception as e:
            logging.error(f"Erreur lors de la jointure du fichier {file} : {e}")
            print(f"Erreur lors de la jointure du fichier {file} : {e}")

# Fonction pour envoyer un email à l'utilisateur avec des pièces jointes
def send_email_to_user(username, user_email, subject, body, attachments):
    try:
        # Charger la clé de cryptage
        with open(os.path.join(user_data_dir, "resources","data" ,"key.key"), 'rb') as key_file:
            key = key_file.read()

        # Lire les informations cryptées du serveur, adresse email et mot de passe
        smtp_server = decrypt_file(os.path.join(user_data_dir, "resources","data" ,"server.txt"), key)
        sender_email = decrypt_file(os.path.join(user_data_dir, "resources","data" ,"adress.txt"), key)
        sender_password = decrypt_file(os.path.join(user_data_dir, "resources","data" ,"tes.txt"), key)

        # Créer le message e-mail
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = user_email
        msg['Subject'] = subject

        # Personnaliser le contenu du corps du message
        body_formatted = body.format(username=username)
        msg.attach(MIMEText(body_formatted, 'plain'))

        # Attacher les fichiers si fournis
        if attachments:
            attach_files(msg, attachments)

        # Envoyer l'email
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()  # Démarrer le chiffrement TLS
            server.login(sender_email, sender_password)  # Se connecter au serveur
            server.sendmail(sender_email, user_email, msg.as_string())  # Envoyer l'e-mail

        logging.info(f"E-mail envoyé à {user_email} avec succès.")
        print(f"E-mail envoyé à {user_email} avec succès.")

    except Exception as e:
        logging.error(f"Erreur lors de l'envoi de l'email : {e}")
        print(f"Erreur lors de l'envoi de l'email : {e}")

# Fonction principale pour envoyer un mail à chaque utilisateur
def main():
    try:
        # Charger les utilisateurs depuis le fichier users.json
        with open(os.path.join(user_data_dir, "resources","data" ,"users.json"), 'r') as users_file:
            users = json.load(users_file)

        # Charger le contenu des emails depuis email_content.json
        with open(os.path.join(user_data_dir, "resources","data" ,"email_content.json"), 'r') as email_file:
            email_content = json.load(email_file)

        # Choisir le type de mail à envoyer, par exemple 'mail1' ou 'mail2'
        mail_type = 'mail1'  # Ici, on envoie un mail de confirmation de compte
        subject = email_content[mail_type]['subject']
        body = email_content[mail_type]['body']
        attachments = email_content[mail_type].get('attachments', [])  # Lire les pièces jointes

        # Envoyer un email à chaque utilisateur
        for user in users:
            username = user['username']  # Nom d'utilisateur
            user_email = user['email']   # Adresse e-mail

            # Envoyer l'e-mail avec pièces jointes
            send_email_to_user(username, user_email, subject, body, attachments)

    except FileNotFoundError as fnf_error:
        logging.error(f"Fichier manquant : {fnf_error}")
        print(f"Erreur : fichier manquant - {fnf_error}")
    except Exception as e:
        logging.error(f"Erreur : {e}")
        print(f"Erreur : {e}")

if __name__ == '__main__':
    main()
