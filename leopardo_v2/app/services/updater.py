import requests
from packaging import version
from PyQt5.QtWidgets import QMessageBox

class UpdaterService:
    def __init__(self, parent=None, current_version="1.0.0"):
        self.parent = parent
        self.current_version = current_version
        self.update_url = "https://leopardo-ai.web.app/version.json"

    def check_for_updates(self):
        try:
            response = requests.get(self.update_url)
            response.raise_for_status()
            latest_version_info = response.json()
            latest_version = latest_version_info.get("version")

            if latest_version and version.parse(latest_version) > version.parse(self.current_version):
                self.prompt_update(latest_version)
        except requests.exceptions.RequestException as e:
            print(f"Error checking for updates: {e}")
        except (ValueError, KeyError) as e:
            print(f"Error parsing version info: {e}")

    def prompt_update(self, new_version):
        QMessageBox.information(
            self.parent,
            "Update Available",
            f"A new version ({new_version}) is available. Please visit our website to download the latest version."
        )
