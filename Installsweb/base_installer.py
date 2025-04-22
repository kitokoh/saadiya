# base_installer.py
import os
import subprocess

class BaseInstaller:
    def __init__(self, name, install_path):
        self.name = name
        self.install_path = install_path

    def run_command(self, command, cwd=None):
        print(f"[{self.name}] Exécution : {command}")
        try:
            subprocess.run(command, shell=True, check=True, cwd=cwd)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"[{self.name}] Erreur : {e}")

    def create_directory(self):
        if not os.path.exists(self.install_path):
            os.makedirs(self.install_path)
