import os
import sys
from datetime import datetime
import ctypes
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

def has_write_permission(file_path):
    """Vérifie si le programme a la permission d'écrire dans le fichier spécifié."""
    try:
        with open(file_path, 'a'):
            pass
        return True
    except IOError:
        return False

def is_hidden(filepath):
    """Vérifie si le fichier est caché sur Windows."""
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
        return attrs & (2 | 4)  # FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM
    except Exception as e:
        return False

def update_env_files(base_dir='C:/bon'):
    log_file_path = os.path.join(user_data_dir, "resources", "journalinstallation.txt")

    log("Démarrage de la mise à jour des fichiers .env dans le dossier C:/bon.")

    # Initialisation du fichier log
    with open(log_file_path, 'a') as log_file:
        log_file.write("\n===========================================\n")
        log_file.write(f"Mise à jour commencée le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Récupération du nom d'utilisateur courant avec getenv
    user_name = os.getenv('USERNAME')

    # Lister les dossiers robotX
    folders = [folder for folder in os.listdir(base_dir) if folder.startswith('robot') and os.path.isdir(os.path.join(base_dir, folder))]

    if not folders:
        log("Aucun dossier 'robotX' trouvé dans C:/bon.")
        return

    log(f"{len(folders)} dossiers trouvés : {', '.join(folders)}.")

    log_content = ""

    # Boucle pour mettre à jour chaque dossier robotX
    for folder_name in folders:
        folder_path = os.path.join(base_dir, folder_name)
        env_file = os.path.join(folder_path, '.env')

        # Gérer les dossiers cachés ou systèmes
        if is_hidden(folder_path):
            log_content += f"Le dossier {folder_name} est caché ou système. Passer au suivant.\n"
            continue

        # Vérification de l'existence du fichier .env
        if not os.path.exists(env_file):
            log_content += f"Le fichier .env pour {folder_name} n'existe pas. Création du fichier.\n"
        else:
            log_content += f"Fichier .env trouvé pour {folder_name}. Mise à jour.\n"

        # Vérifier les permissions d'écriture sur le fichier .env
        if not has_write_permission(env_file):
            log_content += f"ERREUR : Permission refusée pour écrire dans {env_file}.\n"
            continue

        try:
            # Forcer la réécriture du fichier .env
            with open(env_file, 'w') as f:
                robot_number = folder_name[5:]  # Extraction du numéro de robot
                f.write(f'CHROME_FOLDER="C:\\\\Users\\\\{user_name}\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\User Data\\\\Profil {robot_number}"\n')
                f.write('WAIT_MIN=5\n')
                f.write('PROFILE=Default\n')
                f.write('PUBLISH_LABEL=Post\n')
                f.write('VISIT_LABEL=Visit\n')

            log_content += f"Fichier .env mis à jour pour {folder_name} à {datetime.now().strftime('%H:%M:%S')}.\n"
        except Exception as e:
            log_content += f"ERREUR : Impossible de mettre à jour le fichier .env pour {folder_name}. Détails : {e}\n"

    # Écrire le contenu du log dans le fichier
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_content)
        log_file.write(f"Mise à jour terminée à {datetime.now().strftime('%H:%M:%S')}.\n")

    log("Toutes les mises à jour sont terminées.")

def log(message):
    """Affiche un message dans la console"""
    print(message)

def main():
    update_env_files()

if __name__ == '__main__':
    main()
