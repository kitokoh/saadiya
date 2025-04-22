# erpnext_installer.py
from Installsweb.base_installer import BaseInstaller

class ERPNextInstaller(BaseInstaller):
    def __init__(self, install_path="/opt/erpnext"):
        super().__init__("ERPNext", install_path)

    def install(self):
        self.create_directory()
        self.run_command("sudo apt-get install -y python3-dev mariadb-server redis-server")
        self.run_command("sudo systemctl start mariadb")
        self.run_command("sudo mysql_secure_installation")
        self.run_command("git clone https://github.com/frappe/bench.git", cwd=self.install_path)
        self.run_command("sudo pip3 install -e bench", cwd=self.install_path)
        self.run_command("bench init frappe-bench --frappe-branch version-14", cwd=self.install_path)
