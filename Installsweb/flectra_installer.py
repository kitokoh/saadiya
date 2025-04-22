# flectra_installer.py
from Installsweb.base_installer import BaseInstaller

class FlectraInstaller(BaseInstaller):
    def __init__(self, install_path="/opt/flectra"):
        super().__init__("Flectra", install_path)

    def install(self):
        self.create_directory()
        self.run_command("sudo apt install -y postgresql wget git python3-pip")
        self.run_command("wget https://github.com/flectrahq/flectra/archive/refs/heads/master.zip -O flectra.zip", cwd=self.install_path)
        self.run_command("unzip flectra.zip", cwd=self.install_path)
        self.run_command("pip3 install -r flectra-master/requirements.txt", cwd=self.install_path)
