import os
import subprocess
import platform
import ctypes

def is_git_installed():
    """Vérifie si Git est installé."""
    try:
        output = subprocess.check_output(["git", "--version"], stderr=subprocess.STDOUT)
        print(f"Git est déjà installé : {output.decode().strip()}")
        return True
    except FileNotFoundError:
        return False

def install_git_windows():
    """Installe Git sur Windows."""
    print("Installation de Git sur Windows...")
    git_installer_url = "https://github.com/git-for-windows/git/releases/latest/download/Git-Installer.exe"
    installer_path = os.path.join(os.getcwd(), "git_installer.exe")

    # Télécharger le programme d'installation
    subprocess.run(["curl", "-L", git_installer_url, "-o", installer_path], check=True)

    # Exécuter le programme d'installation sans afficher la console
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.run([installer_path, "/VERYSILENT", "/NORESTART"], startupinfo=startupinfo, check=True)

    print("Git a été installé avec succès.")

    # Supprimer l'installeur après installation
    if os.path.exists(installer_path):
        os.remove(installer_path)
        print("Le programme d'installation a été supprimé.")

def install_git_linux():
    """Installe Git sur Linux."""
    print("Installation de Git sur Linux...")
    subprocess.run(["sudo", "apt-get", "install", "git"], check=True)
    print("Git a été installé avec succès.")

def install_git_macos():
    """Installe Git sur macOS."""
    print("Installation de Git sur macOS...")
    subprocess.run(["brew", "install", "git"], check=True)
    print("Git a été installé avec succès.")

def run_as_admin(script_path):
    """Exécute le script Python en tant qu'administrateur sans afficher la console."""
    try:
        # Obtenir le handle de l'application courante
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "python.exe", script_path, None, 1)
    except Exception as e:
        print(f"Erreur lors de l'exécution en tant qu'administrateur : {e}")

def main():
    """Point d'entrée principal du module."""
    if is_git_installed():
        print("Aucune installation requise.")
        return

    os_type = platform.system()

    if os_type == "Windows":
        run_as_admin(__file__)  # Exécute le script actuel en tant qu'administrateur
        install_git_windows()
    elif os_type == "Linux":
        install_git_linux()
    elif os_type == "Darwin":  # macOS
        install_git_macos()
    else:
        print("Système d'exploitation non pris en charge.")

if __name__ == "__main__":
    main()
