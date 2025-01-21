
from mail.importer import*
# # # Chemins des répertoires et des fichiers
# # _current_folder = os.getcwd()
# # user_data_dir1 = os.path.dirname(_current_folder)
# # user_data_dir = os.path.join(user_data_dir1, 'lang', 'resources', 'data')
# #_current_folder = os.getcwd()
# user_data_dir1 = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

# #user_data_dir1 = os.path.dirname(_current_folder)
# user_data_dir = os.path.join(user_data_dir1,  'resources', 'data')
# key_data_dir = os.path.join(user_data_dir1,  'resources')
class Mailer2:
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
        # _current_folder = os.getcwd()
        # user_data_dir1 = os.path.dirname(_current_folder)
        # user_data_dir = os.path.join(user_data_dir1, 'lang', 'resources')

        settings_path = os.path.join(key_data_dir, 'settings.json')
        if not os.path.exists(settings_path):
            raise FileNotFoundError(f"Le fichier 'settings.json' est introuvable.")
        
        settings_data = self.load_plain_file(settings_path)
        self.language = settings_data.get("language", "en")  # Par défaut "en"

    def load_email_content(self):
        """Charge le contenu des e-mails dans la langue de l'utilisateur depuis le fichier JSON approprié (crypté)."""
        email_content_path = os.path.join(user_data_dir, f'send_mailme.json')
        if not os.path.exists(email_content_path):
            raise FileNotFoundError(f"Le fichier 'send_mailme.json' est introuvable.")
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

    # def get_mac_address(self):
    #     """Retourne l'adresse MAC de la machine."""
    #     mac_address = None
    #     for interface, addrs in psutil.net_if_addrs().items():
    #         for addr in addrs:
    #             if addr.family == socket.AF_LINK:
    #                 mac_address = addr.address
    #                 break
    #         if mac_address:
    #             break
    #     return mac_address

    def get_mac_address(self):
        """Retourne l'adresse MAC de la première interface réseau active trouvée, ou None si aucune n'est disponible."""
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                # Vérifie si l'adresse est de type MAC (AF_LINK)
                if addr.family == getattr(socket, 'AF_LINK', None) or addr.family == psutil.AF_LINK:
                    return addr.address  # Retourne immédiatement la première adresse MAC trouvée
        return None  # Retourne None si aucune adresse MAC n'est trouvée
    def get_ip_address(self):
        """Retourne l'adresse IP de la première interface réseau active trouvée, ou None si aucune n'est disponible."""
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                # Vérifie si l'adresse est de type IP (AF_INET pour IPv4)
                if addr.family == socket.AF_INET:
                    return addr.address  # Retourne immédiatement la première adresse IP trouvée
        return None  # Retourne None si aucune adresse IP n'est trouvée

    # def send_email(self, email_type, extra_subject=None, extra_body=None):
    #     """Envoie un e-mail à l'utilisateur actif basé sur le type d'e-mail, avec des options supplémentaires."""
    #     to_email = "turk.novatech@gmail.com"  # Adresse fixe pour l'envoi des mails
    #     if not to_email:
    #         print("Aucun utilisateur correspondant dans 'users.json'.")
    #         return

    #     # Vérification du type d'e-mail dans le contenu d'e-mail
    #     if email_type not in self.email_content:
    #         print(f"Le type d'e-mail '{email_type}' n'existe pas dans 'send_mailme.json'.")
    #         return

    #     # Préparation du sujet et du corps de l'e-mail
    #     subject = self.email_content[email_type]['subject'].format(username=self.session["username"])
    #     if extra_subject:
    #         subject += f" - {extra_subject}"

    #     if 'body' in self.email_content[email_type]:
    #         body = self.email_content[email_type]['body'].format(username=self.session["username"])
    #     else:
    #         print(f"Erreur: La clé 'body' est manquante pour le type d'e-mail '{email_type}'.")
    #         return

    #     # Ajout du texte supplémentaire au corps de l'e-mail
    #     if extra_body:
    #         body += f"\n\n{extra_body}"

    #     # Récupération des informations supplémentaires
    #     mac_address = self.get_mac_address()
    #     ip_address = self.get_ip_address()

        
    #     user_info = {
    #         "email": self.find_user_email(),
    #         "username": self.session["username"],
    #         "langue": self.language,
    #         "ip_address": mac_address,
    #         "mac_address": ip_address,
    #     }

    #     # Ajout des informations sur l'utilisateur au corps de l'e-mail
    #     body += f"\n\nInformation sur l'utilisateur:\n{json.dumps(user_info, indent=4)}"

    #     # Utiliser MIMEMultipart pour gérer l'encodage UTF-8
    #     message = MIMEMultipart()
    #     message['From'] = self.credentials['username']
    #     message['To'] = to_email
    #     message['Subject'] = subject

    #     # Ajouter le corps de l'e-mail
    #     message.attach(MIMEText(body, 'plain', 'utf-8'))

    #     # Envoyer l'e-mail
    #     try:
    #         with smtplib.SMTP(self.credentials['server'], self.credentials['port']) as server:
    #             server.starttls()
    #             server.login(self.credentials['username'], self.credentials['password'])
    #             server.sendmail(self.credentials['username'], to_email, message.as_string())
    #             print(f"Email envoyé à {to_email}")
    #     except Exception as e:
    #         print(f"Erreur lors de l'envoi de l'e-mail : {e}")



    def send_email(self, email_type, extra_subject=None, extra_body=None): 
        """Envoie un e-mail à l'utilisateur actif basé sur le type d'e-mail, avec des options supplémentaires."""
        to_email = "turk.novatech@gmail.com"  # Adresse fixe pour l'envoi des mails
        if not to_email:
            print("Aucun utilisateur correspondant dans 'users.json'.")
            return

        # Vérification du type d'e-mail dans le contenu d'e-mail
        if email_type not in self.email_content:
            print(f"Le type d'e-mail '{email_type}' n'existe pas dans 'send_mailme.json'.")
            return

        # Préparation du sujet et du corps de l'e-mail
        subject = self.email_content[email_type]['subject'].format(username=self.session["username"])
        if extra_subject:
            subject += f" - {extra_subject}"

        # Utiliser un defaultdict pour les variables manquantes
        user_data = defaultdict(lambda: "inconnu", {
            "username": self.session["username"],
            "licence_type": self.session.get("licence_type"),
            "expiry_date": self.session.get("expiry_date")
        })

        if 'body' in self.email_content[email_type]:
            body = self.email_content[email_type]['body'].format_map(user_data)
        else:
            print(f"Erreur: La clé 'body' est manquante pour le type d'e-mail '{email_type}'.")
            return

        # Ajout du texte supplémentaire au corps de l'e-mail
        if extra_body:
            body += f"\n\n{extra_body}"

        # Récupération des informations supplémentaires
        mac_address = self.get_mac_address()
        ip_address = self.get_ip_address()

        user_info = {
            "email": self.find_user_email(),
            "username": self.session["username"],
            "langue": self.language,
            "ip_address": ip_address,
            "mac_address": mac_address,
        }

        # Ajout des informations sur l'utilisateur au corps de l'e-mail
        body += f"\n\nInformation sur l'utilisateur:\n{json.dumps(user_info, indent=4)}"

        # Utiliser MIMEMultipart pour gérer l'encodage UTF-8
        message = MIMEMultipart()
        message['From'] = self.credentials['username']
        message['To'] = to_email
        message['Subject'] = subject

        # Ajouter le corps de l'e-mail
        message.attach(MIMEText(body, 'plain', 'utf-8'))

        # Envoyer l'e-mail
        try:
            with smtplib.SMTP(self.credentials['server'], self.credentials['port']) as server:
                server.starttls()
                server.login(self.credentials['username'], self.credentials['password'])
                server.sendmail(self.credentials['username'], to_email, message.as_string())
                print(f"Email envoyé à {to_email}")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'e-mail : {e}")

# Test du mailer en utilisant un type d'e-mail
if __name__ == "__main__":
    mailer = Mailer2()
    mailer.send_email(email_type="admin_message1")  # Exemple d'envoi d'e-mail


