
from mail.importer import *


# # Chemins des répertoires et des fichiers
# _current_folder = os.getcwd()
# user_data_dir1 = os.path.dirname(_current_folder)
# user_data_dir = os.path.join(user_data_dir1, 'lang', 'resources', 'data')
# Chemins des répertoires et des fichiers
#_current_folder = os.getcwd()
user_data_dir1 = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

#ser_data_dir1 = os.path.dirname(_current_folder)
user_data_dir = os.path.join(user_data_dir1, 'resources', 'data')
key_data_dir = os.path.join(user_data_dir1, 'resources')
class Mailer1:
    def __init__(self):
        """Initialise les paramètres et charge les informations nécessaires."""
        self.load_credentials()
        self.load_language()
        self.load_email_content()
        self.load_users()
        self.load_session()

    def decrypt_data(self, encrypted_data, key):
        """Déchiffre les données cryptées (utile pour d'autres fichiers)."""
        f = Fernet(key)
        return f.decrypt(encrypted_data).decode()

    def load_encrypted_file(self, file_path):
        """Charge et déchiffre le contenu d'un fichier JSON crypté (utile pour d'autres fichiers)."""
        with open(os.path.join(key_data_dir, 'key.key'), 'rb') as key_file:
            key = key_file.read()

        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        decrypted_data = self.decrypt_data(encrypted_data, key)
        return json.loads(decrypted_data)

    def load_plain_file(self, file_path):
        """Charge un fichier JSON non crypté."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def load_credentials(self):
        """Lit et déchiffre les identifiants de connexion depuis des fichiers texte cryptés."""
        with open(os.path.join(key_data_dir, 'key.key'), 'rb') as key_file:
            key = key_file.read()

        with open(os.path.join(user_data_dir, "server.txt"), 'rb') as f:
            encrypted_server = f.read().strip()
        with open(os.path.join(user_data_dir, "adress.txt"), 'rb') as f:
            encrypted_username = f.read().strip()
        with open(os.path.join(user_data_dir, "tes.txt"), 'rb') as f:
            encrypted_password = f.read().strip()

        self.credentials = {
            "server": self.decrypt_data(encrypted_server, key),
            "username": self.decrypt_data(encrypted_username, key),
            "password": self.decrypt_data(encrypted_password, key),
            "port": 587  # Modifier si nécessaire
        }

    def load_language(self):
        _current_folder = os.getcwd()
        user_data_dir1 = os.path.dirname(_current_folder)
        user_data_dir = os.path.join(user_data_dir1, 'lang', 'resources')
        """Charge la langue préférée de l'utilisateur depuis 'settings.json' (non crypté)."""
        settings_path = os.path.join(key_data_dir, 'settings.json')
        if not os.path.exists(settings_path):
            raise FileNotFoundError(f"Le fichier 'settings.json' est introuvable.")
        
        settings_data = self.load_plain_file(settings_path)
        self.language = settings_data.get("language", "en")  # Par défaut "en"

    def load_email_content(self):
        """Charge le contenu des e-mails dans la langue de l'utilisateur depuis le fichier JSON approprié (crypté)."""
        email_content_path = os.path.join(user_data_dir, f'email_content_{self.language}.json')
        if not os.path.exists(email_content_path):
            raise FileNotFoundError(f"Le fichier 'email_content_{self.language}.json' est introuvable.")
        self.email_content = self.load_encrypted_file(email_content_path)

    def load_users(self):
        """Charge les informations des utilisateurs depuis le fichier 'users.json' (non crypté)."""
        users_path = os.path.join(user_data_dir, 'users.json')
        if not os.path.exists(users_path):
            raise FileNotFoundError(f"Le fichier 'users.json' est introuvable.")
        self.users = self.load_plain_file(users_path)

    def load_session(self):
        """Charge la session active de l'utilisateur depuis 'session.json' (non crypté)."""
        session_path = os.path.join(user_data_dir, 'session.json')
        if not os.path.exists(session_path):
            raise FileNotFoundError(f"Le fichier 'session.json' est introuvable.")
        self.session = self.load_plain_file(session_path)

    def find_user_email(self):
        """Recherche l'e-mail de l'utilisateur actif à partir de 'session.json' et 'users.json'."""
        session_username = self.session.get("username")
        for user in self.users:
            if user["username"] == session_username:
                return user["email"]
        return None

    def send_email(self, email_type,extra_subject=None, extra_body=None):
        """Envoie un e-mail à l'utilisateur actif basé sur le type d'e-mail."""
        to_email = self.find_user_email()
        if not to_email:
            print("Aucun utilisateur correspondant dans 'users.json'.")
            return

        # Vérification du type d'e-mail dans le contenu d'e-mail
        if email_type not in self.email_content:
            print(f"Le type d'e-mail '{email_type}' n'existe pas dans 'email_content_{self.language}.json'.")
            return

        # Préparation du sujet et du corps de l'e-mail
        subject = self.email_content[email_type]['subject'].format(username=self.session["username"])
        body = self.email_content[email_type]['body'].format(username=self.session["username"])
        if extra_subject:
            subject += f" - {extra_subject}"
        
                # Ajout du texte supplémentaire au corps de l'e-mail
        if extra_body:
            body += f"\n\n{extra_body}"

        # Utiliser MIMEMultipart pour gérer l'encodage UTF-8
        message = MIMEMultipart()
        message['From'] = self.credentials['username']
        message['To'] = to_email
        message['Subject'] = subject

        # Ajouter le corps du message avec UTF-8
        message.attach(MIMEText(f"To {self.session['username']},\n\n{body}\n\nCordialement,\n\nNova360 AI Team", 'plain', 'utf-8'))

        # Envoi de l'e-mail
        try:
            with smtplib.SMTP(self.credentials['server'], int(self.credentials['port'])) as server:
                server.starttls()
                server.login(self.credentials['username'], self.credentials['password'])
                server.sendmail(self.credentials['username'], to_email, message.as_string())
                print(f"Email de type '{email_type}' envoyé à {to_email} avec succès !")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'e-mail: {e}")
    
    


    def send_email_to_user(self, user_email, email_type, extra_subject=None, extra_body=None):
        """Envoie un e-mail basé sur le type d'e-mail spécifié pour un utilisateur particulier."""
        
        # Vérifie si l'e-mail spécifié existe dans le contenu des e-mails
        if email_type not in self.email_content:
            print(f"Le type d'e-mail '{email_type}' n'existe pas dans 'email_content_{self.language}.json'.")
            return

        # Préparation du sujet et du corps de l'e-mail
        subject = self.email_content[email_type]['subject'].format(username=self.session["username"])
        body = self.email_content[email_type]['body'].format(username=self.session["username"])
        
        # Ajouter des informations supplémentaires au sujet et au corps, si fournies
        if extra_subject:
            subject += f" - {extra_subject}"
        if extra_body:
            body += f"\n\n{extra_body}"

        # Construction de l'e-mail avec encodage UTF-8
        message = MIMEMultipart()
        message['From'] = self.credentials['username']
        message['To'] = user_email
        message['Subject'] = subject

        # Attache le corps de l'e-mail avec salutation
        message.attach(MIMEText(f"Bonjour {self.session['username']},\n\n{body}\n\nCordialement,\n\nNova360Pro Team", 'plain', 'utf-8'))

        # Envoi de l'e-mail
        try:
            with smtplib.SMTP(self.credentials['server'], int(self.credentials['port'])) as server:
                server.starttls()
                server.login(self.credentials['username'], self.credentials['password'])
                server.sendmail(self.credentials['username'], user_email, message.as_string())
                print(f"E-mail de type '{email_type}' envoyé à {user_email} avec succès !")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'e-mail: {e}")

        # def send_emailPj(self, email_type, extra_subject=None, extra_body=None, attachments=None):
        #     """
        #     Sends an email to the active user based on the email type, with optional extra content and attachments.

        #     Parameters:
        #     - email_type (str): The type of email to send (e.g., 'welcome', 'alert').
        #     - extra_subject (str, optional): Additional text to include in the email subject.
        #     - extra_body (str, optional): Additional text to include in the email body.
        #     - attachments (list, optional): List of file paths to attach to the email.
        #     """

        #     # Get the recipient email address
        #     to_email = self.find_user_email()
        #     if not to_email:
        #         print("No matching user found in 'users.json'.")
        #         return

        #     # Check if the email type exists in the email content configuration
        #     if email_type not in self.email_content:
        #         print(f"Email type '{email_type}' does not exist in 'email_content_{self.language}.json'.")
        #         return

        #     # Prepare the subject and body of the email
        #     subject = self.email_content[email_type]['subject'].format(username=self.session["username"])
        #     body = self.email_content[email_type]['body'].format(username=self.session["username"])

        #     # Add extra subject and body content if provided
        #     if extra_subject:
        #         subject += f" - {extra_subject}"
        #     if extra_body:
        #         body += f"\n\nAdditional Information:\n{extra_body}"

        #     # Include user information (username and MAC address)
        #     mac_address = self.get_mac_address()
        #     user_info = {
        #         "email": self.find_user_email(),
        #         "username": self.session["username"],
        #         "mac_address": mac_address,
        #     }

        #     # Append user information and signature to the email body
        #     body += f"\n\nUser Information:\n{user_info}\n\nBest regards,\nNova360Pro Team"

        #     # Create the email message with UTF-8 encoding
        #     message = MIMEMultipart()
        #     message['From'] = self.credentials['username']
        #     message['To'] = to_email
        #     message['Subject'] = subject

        #     # Attach the email body
        #     message.attach(MIMEText(body, 'plain', 'utf-8'))

        #     # Add attachments if provided
        #     if attachments:
        #         for file_path in attachments:
        #             if os.path.isfile(file_path):
        #                 try:
        #                     with open(file_path, 'rb') as attachment:
        #                         mime_base = MIMEBase('application', 'octet-stream')
        #                         mime_base.set_payload(attachment.read())
        #                         encoders.encode_base64(mime_base)
        #                         mime_base.add_header(
        #                             'Content-Disposition',
        #                             f'attachment; filename="{os.path.basename(file_path)}"'
        #                         )
        #                         message.attach(mime_base)
        #                 except Exception as e:
        #                     print(f"Error attaching file '{file_path}': {e}")
        #             else:
        #                 print(f"File '{file_path}' not found.")

        #     # Send the email
        #     try:
        #         with smtplib.SMTP(self.credentials['server'], int(self.credentials['port'])) as server:
        #             server.starttls()
        #             server.login(self.credentials['username'], self.credentials['password'])
        #             server.sendmail(self.credentials['username'], to_email, message.as_string())
        #             print(f"Email of type '{email_type}' successfully sent to {to_email}!")
        #     except Exception as e:
        #         print(f"Error while sending email: {e}")
        # # Test du mailer en utilisant un type d'e-mail
# if __name__ == "__main__":
#     mailer = Mailer1()
#     mailer.send_email(email_type="mail1")

#     # Envoi d'un e-mail avec une pièce jointe
# # self.send_email(
# #     "alert",
# #     extra_subject="Important Documents",
# #     extra_body="Please find the attached documents.",
# #     attachments=["C:/path/to/document.pdf", "C:/path/to/image.jpg"]
# # )

