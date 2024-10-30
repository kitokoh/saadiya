import os
import sys

# Ajouter le répertoire parent au sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Définir le chemin du répertoire contenant les fichiers .py
directory_path = r'C:\Users\ibrahim\AppData\Roaming\saadiya\installFBrobotPy'

# Fonction pour s'assurer que tous les sous-répertoires contiennent un __init__.py
def ensure_init_files(directory):
    for root, dirs, files in os.walk(directory):
        if '__init__.py' not in files:
            with open(os.path.join(root, '__init__.py'), 'a'):
                pass  # Crée un fichier __init__.py vide

# Créer les fichiers __init__.py dans tous les sous-répertoires nécessaires
ensure_init_files(directory_path)

# Chercher et remplacer dans chaque fichier .py
for root, dirs, files in os.walk(directory_path):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.readlines()

            # Remplacer l'import
            new_content = []
            for line in content:
                if 'from .pyarmor_runtime_000000 import __pyarmor__' in line:
                    line = line.replace('from .pyarmor_runtime_000000 import __pyarmor__',
                                        'from saadiya.installFBrobotPy.pyarmor_runtime_000000 import __pyarmor__')
                new_content.append(line)

            # Écrire les modifications dans le fichier
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_content)

print("Les imports ont été modifiés avec succès.")
