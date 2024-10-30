import os
import sys

# Définir le répertoire d'entrée et de sortie pour PyArmor
input_directory = r'..\installFBrobotPy'
output_directory = os.path.join(os.getenv('USERPROFILE'), 'userdata', 'compil')
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

# Ajouter le répertoire utilisateur au sys.path pour permettre les imports absolus
if user_data_dir not in sys.path:
    sys.path.append(user_data_dir)

# Fonction pour créer les fichiers __init__.py dans tous les sous-dossiers nécessaires
def ensure_init_files(directory):
    for root, dirs, files in os.walk(directory):
        if '__init__.py' not in files:
            # Créer un fichier __init__.py vide dans le dossier courant
            open(os.path.join(root, '__init__.py'), 'a').close()

# S'assurer que tous les sous-dossiers contiennent un __init__.py
ensure_init_files(user_data_dir)

# Construire la commande avec les paramètres souhaités
command = f'pyarmor gen -i {input_directory} --output={user_data_dir}'

# Exécuter la commande
os.system(command)
