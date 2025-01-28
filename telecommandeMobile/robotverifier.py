import os
from pathlib import Path

class RobotVerifier:
    def __init__(self):
        # Détecter le dossier "Documents" de l'utilisateur
        self.base_dir = self.get_user_documents_folder()
    
    @staticmethod
    def get_user_documents_folder():
        """Retourne le chemin du dossier 'Documents' de l'utilisateur en fonction du système."""
        try:
            # Pour Windows, macOS, et Linux
            home_dir = Path.home()
            documents_folder = home_dir / "Documents"  # Par défaut pour Windows/Linux/macOS
            return documents_folder if documents_folder.exists() else home_dir
        except Exception as e:
            print(f"Erreur lors de la détection du dossier utilisateur : {e}")
            return Path.home()
    
    def verify_and_execute(self, folder_name, file_name, callback):
        """
        Vérifie si un dossier et un fichier existent, puis exécute un callback.

        :param folder_name: Nom du dossier à vérifier.
        :param file_name: Nom du fichier à vérifier dans le dossier.
        :param callback: Fonction à exécuter si les vérifications réussissent.
        """
        target_folder = self.base_dir / folder_name
        target_file = target_folder / file_name
        
        # Vérifier l'existence du dossier
        if not target_folder.exists():
            print(f"Dossier non trouvé : {target_folder}")
            return
        
        # Vérifier l'existence du fichier
        if not target_file.exists():
            print(f"Fichier non trouvé : {target_file}")
            return
        
        # Si tout est correct, exécuter le callback
        print(f"Dossier et fichier trouvés. Exécution de la fonction {callback.__name__}.")
        callback()

# Exemple d'utilisation
def execute_robot_function():
    print("La fonction du robot est exécutée avec succès!")

robot_verifier = RobotVerifier()
robot_verifier.verify_and_execute("robot1", "python.txt", execute_robot_function)
