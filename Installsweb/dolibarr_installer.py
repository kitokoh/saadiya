# dolibarr_installer.py
from Installsweb.base_installer import BaseInstaller

class DolibarrInstaller(BaseInstaller):
    def __init__(self, install_path="/var/www/html/dolibarr"):
        super().__init__("Dolibarr", install_path)

    def install(self):
        self.run_command("sudo apt install -y apache2 mysql-server php php-mysql php-cli git unzip")
        self.run_command("sudo systemctl start apache2")
        self.create_directory()
        self.run_command("wget https://sourceforge.net/projects/dolibarr/files/latest/download -O dolibarr.zip", cwd=self.install_path)
        self.run_command("unzip dolibarr.zip", cwd=self.install_path)
        self.run_command("sudo chown -R www-data:www-data .", cwd=self.install_path)
