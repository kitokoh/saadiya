import os
import ctypes
import subprocess
import sys

# Vérifier si le script est déjà exécuté avec des droits administratifs
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Fonction pour définir les permissions sur les dossiers
def set_permissions():
    try:
        # Donner des permissions de lecture et d'écriture à l'utilisateur sur C:\Bon et C:\Program Files
        subprocess.run(['icacls', r'C:\Bon', '/grant', f'{os.getlogin()}:F'], check=True)
        subprocess.run(['icacls', r'C:\Program Files', '/grant', f'{os.getlogin()}:F'], check=True)
        print("Permissions modifiées avec succès.")
    except Exception as e:
        print(f"Erreur lors de la modification des permissions: {e}")

# Si l'utilisateur n'est pas administrateur, relancer le script avec des droits d'admin
if not is_admin():
    try:
        # Relancer le script avec des droits admin
        script = sys.executable  # Chemin vers l'exécutable Python actuel
        subprocess.run(['runas', '/noprofile', '/user:Administrator', f'{script}'] + sys.argv)
    except Exception as e:
        print(f"Échec de l'élévation des droits: {e}")
else:
    # Si l'utilisateur est admin, exécuter le script normalement
    print("Exécution avec des droits administratifs.")
    set_permissions()
    # Vous pouvez ici appeler votre script principal
