import json
import os
import requests


class AutoUpdater:
    def __init__(self, current_version):
        self.current_version = current_version
        self.update_url = "https://yourserver.com/version_info.json"

    def check_for_updates(self):
        try:
            response = requests.get(self.update_url)
            update_info = response.json()
            latest_version = update_info["version"]
            download_url = update_info["download_url"]

            if self.current_version < latest_version:
                print(f"Nouvelle version disponible: {latest_version}")
                self.download_and_install(download_url)
            else:
                print("L'application est à jour.")
        except Exception as e:
            print(f"Erreur lors de la vérification de mise à jour: {e}")

    def download_and_install(self, download_url):
        response = requests.get(download_url, stream=True)
        with open("update_installer.exe", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Téléchargement terminé. Installation en cours...")
        os.startfile("update_installer.exe")  # Lance l'installateur

# Utilisation
updater = AutoUpdater(current_version="1.0.0")
updater.check_for_updates()
