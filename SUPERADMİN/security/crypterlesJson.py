import os
import json
from cryptography.fernet import Fernet

# Chemin vers le répertoire contenant les fichiers JSON
# _current_folder = os.getcwd()
# user_data_dir1 = os.path.dirname(_current_folder)
# user_data_dir = os.path.join(user_data_dir1, 'lang', 'resources', 'data')
# user_data_dir = os.path.join(user_data_dir1, 'lang', 'resources', 'data')
_current_folder = os.getcwd()
#user_data_dir1 = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

user_data_dir1 = os.path.dirname(_current_folder)
user_data_dir = os.path.join(user_data_dir1, 'lang', 'resources', 'data')
key_data_dir = os.path.join(user_data_dir1, 'lang', 'resources')
# Chargement de la clé de chiffrement
with open(os.path.join(key_data_dir, 'key.key'), 'rb') as key_file:
    key = key_file.read()
fernet = Fernet(key)

def encrypt_json(file_path):
    """Chiffre le contenu du fichier JSON et l'écrit de nouveau."""
    if os.path.getsize(file_path) == 0:
        print(f"Le fichier {file_path} est vide. Impossible de le chiffrer.")
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)  # Charger le JSON
        except json.JSONDecodeError as e:
            print(f"Erreur lors de la lecture de {file_path}: {e}")
            return

    # Convertir en chaîne JSON et chiffrer
    data_str = json.dumps(data)
    encrypted_data = fernet.encrypt(data_str.encode())

    # Écrire les données chiffrées dans le fichier (en mode binaire)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)
    print(f"{file_path} chiffré avec succès.")

# Liste des fichiers JSON à chiffrer
json_files = [
    "settings.json", 
    "email_content_en.json", 
    "email_content_ar.json", 
    "email_content_tr.json", 
    "send_mailme.json", 
    "email_content_fr.json", 
    "email_content_pt.json"
]

# Chiffrement des fichiers JSON
for json_file in json_files:
    file_path = os.path.join(user_data_dir, json_file)
    if os.path.exists(file_path):
        encrypt_json(file_path)
    else:
        print(f"Fichier {json_file} introuvable dans {user_data_dir}.")
