# Déchiffrer un fichier
import os
from cryptography.fernet import Fernet

# Générer une clé de chiffrement et l'enregistrer
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

# Charger la clé de chiffrement depuis le fichier
def load_key():
    return open("secret.key", "rb").read()

# Crypter un fichier
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        original = file.read()
    
    encrypted = fernet.encrypt(original)
    
    with open(file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted)

# Crypter tous les fichiers dans un dossier donné
def encrypt_directory(directory):
    key = load_key() if os.path.exists("secret.key") else generate_key()
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):  # Assurez-vous que c'est un fichier
            encrypt_file(file_path, key)
            print(f"Fichier crypté : {file_path}")

if __name__ == "__main__":
    resources_directory = "chemin/vers/votre/dossier/resources"  # Remplacez par le chemin de votre dossier
    encrypt_directory(resources_directory)


def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as encrypted_file:
        encrypted = encrypted_file.read()
    
    decrypted = fernet.decrypt(encrypted)
    
    with open(file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted)

# Déchiffrer tous les fichiers dans un dossier donné
def decrypt_directory(directory):
    key = load_key()
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):  # Assurez-vous que c'est un fichier
            decrypt_file(file_path, key)
            print(f"Fichier décrypté : {file_path}")

if __name__ == "__main__":
    resources_directory = "chemin/vers/votre/dossier/resources"  # Remplacez par le chemin de votre dossier
    decrypt_directory(resources_directory)
