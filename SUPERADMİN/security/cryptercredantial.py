from cryptography.fernet import Fernet
from translation import TranslatorManager  # Importer le gestionnaire de traductions

# Générer une clé et l'enregistrer dans key.key
key = Fernet.generate_key()
with open('resources/data/key.key', 'wb') as key_file:
    key_file.write(key)

# Utiliser cette clé pour chiffrer les informations
cipher = Fernet(key)

# Crypter les données du serveur
server_info = "mail.turknovatech.com".encode()
encrypted_server = cipher.encrypt(server_info)
with open('resources/data/server.txt', 'wb') as server_file:
    server_file.write(encrypted_server)

# Crypter l'adresse e-mail
sender_email = "info@turknovatech.com".encode()
encrypted_email = cipher.encrypt(sender_email)
with open('resources/data/adress.txt', 'wb') as email_file:
    email_file.write(encrypted_email)

# Crypter le mot de passe
password = "7LdXDMXLkQ7G".encode()
encrypted_password = cipher.encrypt(password)
with open('resources/data/tes.txt', 'wb') as password_file:
    password_file.write(encrypted_password)
