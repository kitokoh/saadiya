# axelor_installer.py
from Installsweb.base_installer import BaseInstaller

class AxelorInstaller(BaseInstaller):
    def __init__(self, install_path="/opt/axelor"):
        super().__init__("Axelor", install_path)

    def install(self):
        self.create_directory()
        self.run_command("sudo apt install -y openjdk-11-jdk maven")
        self.run_command("git clone https://github.com/axelor/axelor-open-suite.git", cwd=self.install_path)
        self.run_command("cd axelor-open-suite && ./gradlew build", cwd=self.install_path)
