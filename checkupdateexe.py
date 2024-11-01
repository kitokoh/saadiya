import sys
import requests
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMessageBox

class UpdateManager:
    def __init__(self, current_version, update_url):
        self.current_version = current_version
        self.update_url = update_url

    def check_for_updates(self):
        try:
            response = requests.get(self.update_url)
            response.raise_for_status()  # Vérifie les erreurs de requête

            update_info = response.json()
            latest_version = update_info['version']

            if self.current_version < latest_version:
                self.prompt_update(update_info)
            else:
                print("Votre application est à jour.")
        except Exception as e:
            print(f"Erreur lors de la vérification des mises à jour: {e}")

    def prompt_update(self, update_info):
        # Afficher un message pour informer l'utilisateur
        message_box = QMessageBox()
        message_box.setWindowTitle("Mise à jour disponible")
        message_box.setText(f"Une nouvelle version ({update_info['version']}) est disponible.")
        message_box.setInformativeText(update_info['changelog'])
        message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        result = message_box.exec_()
        
        if result == QMessageBox.Ok:
            self.download_update(update_info['download_url'])

    def download_update(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Vérifie les erreurs de requête
            
            # Sauvegarder le fichier téléchargé
            update_file_path = os.path.join(os.getcwd(), "update_file.exe")
            with open(update_file_path, 'wb') as f:
                f.write(response.content)

            # Lancer l'installateur ou mettre à jour l'application
            subprocess.run([update_file_path], check=True)
        except Exception as e:
            print(f"Erreur lors du téléchargement de la mise à jour: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    current_version = "1.0.0"  # Version actuelle de votre application
    update_url = "http://example.com/update.json"  # URL de votre fichier JSON de mise à jour

    updater = UpdateManager(current_version, update_url)
    updater.check_for_updates()

    sys.exit(app.exec_())
