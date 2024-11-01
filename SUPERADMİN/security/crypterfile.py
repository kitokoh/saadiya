import os
from cryptography.fernet import Fernet

class PythonFileEncryptor:
    def __init__(self, directory, key=None):
        self.directory = directory
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def save_key(self, filename='secret.key'):
        """Sauvegarde la clé de chiffrement dans un fichier."""
        with open(filename, 'wb') as key_file:
            key_file.write(self.key)
        print(f"Clé sauvegardée dans {filename}")

    def encrypt_file(self, file_path):
        """Chiffre un fichier donné."""
        with open(file_path, 'rb') as file:
            plaintext = file.read()
        
        ciphertext = self.cipher.encrypt(plaintext)

        with open(file_path, 'wb') as file:
            file.write(ciphertext)
        print(f"Fichier chiffré : {file_path}")

    def encrypt_all_py_files(self):
        """Chiffre tous les fichiers .py dans le répertoire donné."""
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.py'):
                    self.encrypt_file(os.path.join(root, file))

    def decrypt_file(self, file_path):
        """Déchiffre un fichier donné."""
        with open(file_path, 'rb') as file:
            ciphertext = file.read()
        
        plaintext = self.cipher.decrypt(ciphertext)

        with open(file_path, 'wb') as file:
            file.write(plaintext)
        print(f"Fichier déchiffré : {file_path}")

if __name__ == "__main__":
    directory = input("Entrez le chemin du répertoire contenant les fichiers .py à chiffrer : ")
    
    encryptor = PythonFileEncryptor(directory)
    encryptor.save_key()  # Sauvegarde la clé pour le déchiffrement ultérieur
    encryptor.encrypt_all_py_files()  # Chiffre tous les fichiers .py
