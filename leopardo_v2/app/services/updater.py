import requests
import subprocess
import os
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
            installer_url = latest_version_info.get("url")

            if latest_version and version.parse(latest_version) > version.parse(self.current_version):
                self.prompt_update(latest_version, installer_url)
        except requests.exceptions.RequestException as e:
            print(f"Error checking for updates: {e}")
        except (ValueError, KeyError) as e:
            print(f"Error parsing version info: {e}")

    def prompt_update(self, new_version, installer_url):
        reply = QMessageBox.information(
            self.parent,
            "Update Available",
            f"A new version ({new_version}) is available. Do you want to download and install it now?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.download_and_install(installer_url)

    def download_and_install(self, installer_url):
        try:
            response = requests.get(installer_url, stream=True)
            response.raise_for_status()

            # Save the installer to a temporary file
            installer_path = os.path.join(os.path.expanduser("~"), "leopardo_v2_installer.exe")
            with open(installer_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Run the installer
            subprocess.Popen([installer_path])

            # Close the current application
            if self.parent:
                self.parent.close()

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self.parent, "Error", f"Failed to download the update: {e}")
        except IOError as e:
            QMessageBox.critical(self.parent, "Error", f"Failed to save the update: {e}")
