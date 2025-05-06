import sys
import requests
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMessageBox

CURRENT_VERSION = "1.0.0"
VERSION_URL = "https://your-app.firebaseapp.com/version.json"

def check_for_updates():
    try:
        response = requests.get(VERSION_URL)
        data = response.json()
        latest_version = data["version"]
        download_url = data["url"]

        if latest_version != CURRENT_VERSION:
            reply = QMessageBox.question(
                None,
                "Mise à jour disponible",
                f"Une nouvelle version ({latest_version}) est disponible. Voulez-vous la télécharger maintenant ?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                download_and_install(download_url)
    except Exception as e:
        print("Erreur de mise à jour :", e)

def download_and_install(url):
    try:
        response = requests.get(url, stream=True)
        filename = os.path.join(os.getenv("TEMP"), "new_version.exe")

        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        QMessageBox.information(None, "Téléchargement terminé", "La nouvelle version va maintenant s'installer.")
        subprocess.Popen([filename])
        sys.exit()

    except Exception as e:
        QMessageBox.critical(None, "Erreur", f"Erreur lors du téléchargement : {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    check_for_updates()
    # ... lancement normal de ton app ici
    sys.exit(app.exec_())
