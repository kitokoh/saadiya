import os
from cryptography.fernet import Fernet

class PythonFileDecryptor:
    def __init__(self, directory, key_file='secret.key'):
        self.directory = directory
        self.key_file = key_file
        self.key = self.load_key()
        self.cipher = Fernet(self.key)

    def load_key(self):
        """Charge la clé de chiffrement à partir d'un fichier."""
        with open(self.key_file, 'rb') as key_file:
            return key_file.read()

    def decrypt_file(self, file_path):
        """Déchiffre un fichier donné."""
        with open(file_path, 'rb') as file:
            ciphertext = file.read()
        
        plaintext = self.cipher.decrypt(ciphertext)

        with open(file_path, 'wb') as file:
            file.write(plaintext)
        print(f"Fichier déchiffré : {file_path}")

    def decrypt_all_py_files(self):
        """Déchiffre tous les fichiers .py dans le répertoire donné."""
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.py'):
                    self.decrypt_file(os.path.join(root, file))

if __name__ == "__main__":
    directory = input("Entrez le chemin du répertoire contenant les fichiers .py à déchiffrer : ")
    key_file = input("Entrez le nom du fichier de clé (par défaut 'secret.key') : ") or 'secret.key'
    
    decryptor = PythonFileDecryptor(directory, key_file)
    decryptor.decrypt_all_py_files()  # Déchiffre tous les fichiers .py
