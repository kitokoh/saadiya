import os
import subprocess
import platform
import sys

def is_python_installed():
    """Vérifie si Python est installé."""
    try:
        output = subprocess.check_output(["python", "--version"], stderr=subprocess.STDOUT)
        print(f"Python est déjà installé : {output.decode().strip()}")
        return True
    except FileNotFoundError:
        return False

def install_python_windows():
    """Installe Python sur Windows."""
    print("Installation de Python sur Windows...")
    python_installer_url = "https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe"
    installer_path = os.path.join(os.getcwd(), "python_installer.exe")

    # Télécharger le programme d'installation
    subprocess.run(["curl", "-L", python_installer_url, "-o", installer_path], check=True)

    # Exécuter le programme d'installation
    subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"], check=True)

    print("Python a été installé avec succès.")

def install_python_linux():
    """Installe Python sur Linux."""
    print("Installation de Python sur Linux...")
    subprocess.run(["sudo", "apt-get", "install", "python3"], check=True)
    print("Python a été installé avec succès.")

def install_python_macos():
    """Installe Python sur macOS."""
    print("Installation de Python sur macOS...")
    subprocess.run(["brew", "install", "python"], check=True)
    print("Python a été installé avec succès.")

def main():
    """Point d'entrée principal du module."""
    if is_python_installed():
        print("Aucune installation requise.")
        return

    os_type = platform.system()

    if os_type == "Windows":
        install_python_windows()
    elif os_type == "Linux":
        install_python_linux()
    elif os_type == "Darwin":  # macOS
        install_python_macos()
    else:
        print("Système d'exploitation non pris en charge.")

if __name__ == "__main__":
    main()
