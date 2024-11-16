from mail.importer import *
class Mailer3:
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
        """Charge la langue préférée de l'utilisateur depuis 'settings.json' (non crypté)."""
        _current_folder = os.getcwd()
        user_data_dir1 = os.path.dirname(_current_folder)
        user_data_dir = os.path.join(user_data_dir1, 'lang', 'resources')
        settings_path = os.path.join(user_data_dir, 'settings.json')
        if not os.path.exists(settings_path):
            raise FileNotFoundError(f"Le fichier 'settings.json' est introuvable.")
        
        settings_data = self.load_plain_file(settings_path)
        self.language = settings_data.get("language", "en")  # Par défaut "en"

    # def load_email_content(self):
    #     """Charge le contenu des e-mails depuis le fichier contentmail.json."""
    #     email_content_path = os.path.join(user_data_dir, 'contentmail.json')
    #     if not os.path.exists(email_content_path):
    #         raise FileNotFoundError(f"Le fichier 'contentmail.json' est introuvable.")
    #     self.email_content = self.load_plain_file(email_content_path)
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

    def send_email_with_attachments(self, email_type, extra_subject=None, extra_body=None, attachments=None):
        """
        Envoie un e-mail stylisé avec des pièces jointes et une signature professionnelle.
        """
        to_email = self.find_user_email()
        if not to_email:
            print("Aucun utilisateur correspondant dans 'users.json'.")
            return

        if email_type not in self.email_content:
            print(f"Le type d'e-mail '{email_type}' n'existe pas dans 'contentmail.json'.")
            return

        subject = self.email_content[email_type]['subject'].format(username=self.session["username"])
        body = self.email_content[email_type]['body'].format(username=self.session["username"])
        if extra_subject:
            subject += f" - {extra_subject}"
        if extra_body:
            body += f"\n\n{extra_body}"

        signature = """
        <br><br>
        <hr>
        <p style="font-family: Arial, sans-serif; font-size: 12px; color: #555;">
            Cordialement,<br>
            <strong>Nova360Pro Team</strong><br>
            <a href="https://www.nova360pro.com">www.nova360pro.com</a>
        </p>
        """
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f6f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    padding: 20px;
                }}
                .email-header {{
                    background-color: #0078D7;
                    color: #ffffff;
                    padding: 20px;
                    border-radius: 8px 8px 0 0;
                    text-align: center;
                }}
                .email-content {{
                    padding: 20px;
                    font-size: 16px;
                    line-height: 1.6;
                    color: #555;
                }}
                .signature {{
                    margin-top: 20px;
                    border-top: 1px solid #eee;
                    padding-top: 10px;
                    font-size: 14px;
                    color: #777;
                }}
                .btn {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #0078D7;
                    color: #ffffff;
                    border-radius: 4px;
                    text-decoration: none;
                    font-weight: bold;
                    margin-top: 20px;
                }}
                .btn:hover {{
                    background-color: #005bb5;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h2>Hello, {self.session['username']}</h2>
                </div>
                <div class="email-content">
                    <p>{body.replace(chr(10), '<br>')}</p>
                    <a href="https://www.nova360pro.com" class="btn">Marketing Automation</a>
                    <div class="signature">
                        <p>Cordialement,<br>
                        <strong>Nova360Pro Team</strong><br>
                        <a href="https://www.nova360pro.com">www.nova360pro.com</a></p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        # Création de l'objet MIMEMultipart pour l'email
        message = MIMEMultipart()
        message['From'] = self.credentials['username']
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(html_body, 'html'))

        # Ajouter les pièces jointes si elles existent
        if attachments:
            for file_path in attachments:
                if os.path.isfile(file_path):
                    try:
                        print(f"Ajout de la pièce jointe: {file_path}")
                        with open(file_path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename="{os.path.basename(file_path)}"'
                        )
                        message.attach(part)
                    except Exception as e:
                        print(f"Erreur lors de l'ajout de la pièce jointe '{file_path}': {e}")
                else:
                    print(f"Fichier '{file_path}' introuvable.")

        # Tentative d'envoi de l'email
        try:
            print(f"Tentative de connexion au serveur SMTP {self.credentials['server']}...")
            with smtplib.SMTP(self.credentials['server'], int(self.credentials['port'])) as server:
                server.set_debuglevel(1)  # Active le mode debug SMTP pour afficher toutes les étapes de la connexion
                print("Tentative de démarrer TLS...")
                server.starttls()
                print(f"Connexion TLS établie. Tentative de connexion avec l'utilisateur {self.credentials['username']}...")
                server.login(self.credentials['username'], self.credentials['password'])
                print(f"Connexion réussie. Envoi de l'email à {to_email}...")
                server.sendmail(self.credentials['username'], to_email, message.as_string())
                print(f"E-mail de type '{email_type}' envoyé à {to_email} avec succès !")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'e-mail: {e}")

# Utilisation de la classe Mailer1
if __name__ == "__main__":
    mailer = Mailer3()
    
    # Envoi d'un e-mail simple
    mailer.send_email_with_attachments(
        email_type="mail1",
        attachments=["D:\\gestion\\entreeJeux\\KpsPlastic\\hayvancilik\\catalogKps.pdf"]
    )