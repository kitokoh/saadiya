# tryton_installer.py
from Installsweb.base_installer import BaseInstaller

class TrytonInstaller(BaseInstaller):
    def __init__(self, install_path="/opt/tryton"):
        super().__init__("Tryton", install_path)

    def install(self):
        self.create_directory()
        self.run_command("sudo apt install -y python3-pip postgresql")
        self.run_command("pip3 install trytond tryton")
        self.run_command("pip3 install trytond_account trytond_party trytond_product")
