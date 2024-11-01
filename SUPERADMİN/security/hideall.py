import os
import subprocess

class DirectoryHider:
    def __init__(self):
        self.suffixes = [' bon', ' wabon']  # Suffixes à rechercher
        self.downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')  # Dossier de téléchargements
        self.roaming_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'saadia')  # Dossier Saadia

    def hide_directory(self, path):
        """Rend un dossier et ses sous-dossiers invisibles."""
        try:
            subprocess.run(['attrib', '+h', path], check=True)  # +h pour cacher le dossier
            print(f"Le dossier {path} a été rendu invisible.")
        except Exception as e:
            print(f"Erreur lors de la tentative de rendre le dossier {path} invisible : {e}")

    def hide_directories_in_c(self):
        """Cache les dossiers dans C: ayant les suffixes spécifiés."""
        c_path = 'C:\\'
        for suffix in self.suffixes:
            for root, dirs, _ in os.walk(c_path):
                for dir_name in dirs:
                    if dir_name.endswith(suffix):
                        full_path = os.path.join(root, dir_name)
                        self.hide_directory(full_path)

    def hide_downloads_robot_directories(self):
        """Cache les dossiers dans le dossier Téléchargements se terminant par -Robot."""
        for dir_name in os.listdir(self.downloads_path):
            if dir_name.endswith('-Robot'):
                full_path = os.path.join(self.downloads_path, dir_name)
                self.hide_directory(full_path)

    def hide_saadia_directory(self):
        """Cache le dossier Saadia dans le répertoire Roaming."""
        if os.path.exists(self.roaming_path):
            self.hide_directory(self.roaming_path)

    def hide_specific_directories(self):
        """Exécute l'ensemble des opérations de masquage de dossiers."""
        self.hide_directories_in_c()
        self.hide_downloads_robot_directories()
        self.hide_saadia_directory()

if __name__ == "__main__":
    hider = DirectoryHider()  # Créer une instance de DirectoryHider
    hider.hide_specific_directories()  # Exécuter la méthode pour cacher les dossiers
