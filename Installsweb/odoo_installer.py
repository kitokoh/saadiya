import sys
import os
import subprocess
import platform
import webbrowser
import shutil
import urllib.request
import tempfile
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QLineEdit, QComboBox, QCheckBox, QGroupBox, QProgressBar, 
                            QTabWidget, QFileDialog, QMessageBox, QTextEdit, QSpinBox, 
                            QFormLayout, QApplication)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QPalette
from PyQt5.QtWidgets import QWidget

class InstallationThread(QThread):
    progress_update = pyqtSignal(int, str)
    finished_signal = pyqtSignal(bool, str)
    log_signal = pyqtSignal(str)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
    
    def run(self):
        try:
            # Validate inputs
            if not self.validate_inputs():
                self.finished_signal.emit(False, "Invalid configuration")
                return
            
            # Step 1: Install Chocolatey if not present
            self.progress_update.emit(5, "Setting up Chocolatey package manager...")
            if not self.install_chocolatey():
                self.finished_signal.emit(False, "Failed to install Chocolatey")
                return
            
            # # Step 2: Install system dependencies
            # self.progress_update.emit(15, "Installing system dependencies...")
            # if not self.install_system_dependencies():
            #     self.finished_signal.emit(False, "Failed to install system dependencies")
            #     return
            # Step 2: Install system dependencies
            self.progress_update.emit(15, "Installation des dépendances système...")
            if not self.install_system_dependencies():
                error_msg = """
    Échec de l'installation des dépendances système.
    Causes possibles :
    1. Connexion Internet instable
    2. Chocolatey non installé correctement
    3. Droits administrateur insuffisants
    Veuillez vérifier les logs pour plus de détails.
    """
                self.finished_signal.emit(False, error_msg)
                return
                        
            # Step 3: Install and configure PostgreSQL
            self.progress_update.emit(30, "Installing PostgreSQL...")
            if not self.install_postgresql():
                self.finished_signal.emit(False, "Failed to install PostgreSQL")
                return
            
            # Step 4: Install Wkhtmltopdf if selected
            if self.config['install_wkhtmltopdf']:
                self.progress_update.emit(45, "Installing Wkhtmltopdf...")
                if not self.install_wkhtmltopdf():
                    self.finished_signal.emit(False, "Failed to install Wkhtmltopdf")
                    return
            
            # Step 5: Install Odoo
            self.progress_update.emit(60, "Downloading and installing Odoo...")
            if not self.install_odoo():
                self.finished_signal.emit(False, "Failed to install Odoo")
                return
            
            # Step 6: Configure Odoo
            self.progress_update.emit(75, "Configuring Odoo...")
            if not self.configure_odoo():
                self.finished_signal.emit(False, "Failed to configure Odoo")
                return
            
            # Step 7: Create startup scripts
            self.progress_update.emit(85, "Creating startup scripts...")
            if not self.create_startup_scripts():
                self.finished_signal.emit(False, "Failed to create startup scripts")
                return
            
            # Step 8: Create Windows service if selected
            if self.config['create_service']:
                self.progress_update.emit(90, "Creating Windows service...")
                if not self.create_windows_service():
                    self.finished_signal.emit(False, "Failed to create Windows service")
                    return
            
            # Step 9: Start Odoo if selected
            if self.config['start_service']:
                self.progress_update.emit(95, "Starting Odoo...")
                if not self.start_odoo():
                    self.finished_signal.emit(False, "Failed to start Odoo")
                    return
            
            self.progress_update.emit(100, "Installation completed successfully!")
            self.finished_signal.emit(True, "Odoo installed successfully")
            
        except Exception as e:
            self.finished_signal.emit(False, f"Error during installation: {str(e)}")
    
    def validate_inputs(self):
        if not self.config['odoo_version']:
            self.log_signal.emit("Error: Odoo version not selected")
            return False
        if not self.config['install_dir']:
            self.log_signal.emit("Error: Installation directory not specified")
            return False
        if not self.config['admin_password']:
            self.log_signal.emit("Error: Admin password not set")
            return False
        return True
    def install_chocolatey(self):
        try:
            # Vérifier si Chocolatey est déjà installé
            process = subprocess.Popen("choco --version", shell=True, 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate()
            
            if process.returncode != 0:
                self.log_signal.emit("Installation de Chocolatey...")
                
                # Télécharger et exécuter le script d'installation
                install_script = """
    [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    """
                # Écrire le script dans un fichier temporaire
                with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as tmp:
                    tmp.write(install_script.encode('utf-8'))
                    tmp_path = tmp.name
                
                # Exécuter le script PowerShell avec les droits admin
                cmd = [
                    'powershell.exe', 
                    '-ExecutionPolicy', 'Bypass', 
                    '-NoProfile', 
                    '-File', 
                    tmp_path
                ]
                
                self.log_signal.emit("Exécution de l'installation Chocolatey...")
                process = subprocess.Popen(cmd, shell=True, 
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                
                # Supprimer le fichier temporaire
                os.unlink(tmp_path)
                
                if process.returncode != 0:
                    self.log_signal.emit("Échec de l'installation de Chocolatey")
                    self.log_signal.emit(stderr.decode().strip())
                    return False
                
                # Mettre à jour le PATH manuellement
                self.log_signal.emit("Mise à jour des variables d'environnement...")
                chocolatey_path = os.path.join(os.environ['ProgramData'], 'chocolatey', 'bin')
                os.environ['PATH'] += os.pathsep + chocolatey_path
                
                # Vérifier que Chocolatey est maintenant disponible
                process = subprocess.Popen("choco --version", shell=True, 
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                
                if process.returncode != 0:
                    self.log_signal.emit("Chocolatey n'est toujours pas disponible après installation")
                    return False
                
            self.log_signal.emit(f"Chocolatey est installé (version: {stdout.decode().strip()})")
            return True
            
        except Exception as e:
            self.log_signal.emit(f"Erreur lors de l'installation de Chocolatey: {str(e)}")
            return False
        
        
    def install_chocolatey1(self):
        try:
            # Check if Chocolatey is already installed
            process = subprocess.Popen("choco --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate()
            
            if process.returncode != 0:
                self.log_signal.emit("Installing Chocolatey package manager...")
                cmd = (
                    'Set-ExecutionPolicy Bypass -Scope Process -Force; '
                    '[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; '
                    'iex ((New-Object System.Net.WebClient).DownloadString("https://community.chocolatey.org/install.ps1"))'
                )
                process = subprocess.Popen(["powershell", "-Command", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                
                if process.returncode != 0:
                    self.log_signal.emit("Failed to install Chocolatey")
                    self.log_signal.emit(stderr.decode().strip())
                    return False
                
                # Refresh environment variables
                subprocess.call("refreshenv", shell=True)
            
            return True
        except Exception as e:
            self.log_signal.emit(f"Error installing Chocolatey: {str(e)}")
            return False
    
    def install_system_dependencies(self):
        try:
            self.log_signal.emit("Vérification des dépendances système...")
            
            # Liste des paquets Chocolatey requis avec vérifications
            packages = [
                ("git", "git --version"),
                ("python3", "python --version"),
                ("pip", "python -m pip --version"),
                ("nodejs", "node --version"),
                ("libjpeg-turbo", None),  # Vérification plus complexe
                ("openssl", "openssl version"),
                ("visualstudio2022-workload-vctools", None)
            ]

            # Installer chaque paquet avec vérification
            for pkg, check_cmd in packages:
                if check_cmd and self.check_command_available(check_cmd):
                    self.log_signal.emit(f"{pkg} est déjà installé - on passe")
                    continue

                self.log_signal.emit(f"Installation de {pkg} via Chocolatey...")
                cmd = f"choco install -y {pkg}"
                process = subprocess.Popen(cmd, shell=True, 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True)
                
                # Affichage en temps réel
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.log_signal.emit(output.strip())
                
                if process.returncode != 0:
                    self.log_signal.emit(f"Échec de l'installation de {pkg}")
                    return False

            # Installation des dépendances Python
            python_deps = [
                ("pip", "python -m pip install --upgrade pip setuptools wheel"),
                ("pywin32", "python -m pip install pywin32"),
                ("psycopg2", "python -m pip install psycopg2-binary")
            ]

            for name, cmd in python_deps:
                self.log_signal.emit(f"Installation de {name}...")
                process = subprocess.Popen(cmd, shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True)
                
                # Affichage en temps réel
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.log_signal.emit(output.strip())
                
                if process.returncode != 0:
                    self.log_signal.emit(f"Échec de l'installation de {name}")
                    return False

            return True

        except Exception as e:
            self.log_signal.emit(f"Erreur critique dans install_system_dependencies: {str(e)}")
            return False

    def check_command_available(self, command):
        """Vérifie si une commande est disponible"""
        try:
            process = subprocess.Popen(command, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            process.communicate()
            return process.returncode == 0
        except:
            return False
        

    def verify_chocolatey(self):
        """Vérifie que Chocolatey est correctement installé et dans le PATH"""
        try:
            process = subprocess.Popen("choco --version", shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            return process.returncode == 0
        except:
            return False   
    def install_postgresql(self):
        try:
            # Install PostgreSQL with Chocolatey
            cmd = "choco install -y postgresql --params '/Password:{}'".format(self.config['admin_password'])
            self.log_signal.emit(f"Executing: {cmd}")
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_signal.emit("Failed to install PostgreSQL")
                self.log_signal.emit(stderr.decode().strip())
                return False
            
            # Add PostgreSQL to PATH
            postgres_path = os.path.join(os.environ["ProgramFiles"], "PostgreSQL", "latest", "bin")
            os.environ["PATH"] += os.pathsep + postgres_path
            
            # Initialize database and create user
            init_cmds = [
                f'psql -U postgres -c "CREATE USER {self.config["db_user"]} WITH SUPERUSER PASSWORD \'{self.config["admin_password"]}\'"',
                f'psql -U postgres -c "CREATE DATABASE {self.config["db_name"]} OWNER {self.config["db_user"]}"'
            ]
            
            for cmd in init_cmds:
                self.log_signal.emit(f"Executing: {cmd}")
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    self.log_signal.emit(f"Command failed: {cmd}")
                    self.log_signal.emit(stderr.decode().strip())
                    # Continue even if fails (might already exist)
            
            return True
        except Exception as e:
            self.log_signal.emit(f"Error installing PostgreSQL: {str(e)}")
            return False
    
    def install_wkhtmltopdf(self):
        try:
            # Download and install wkhtmltopdf
            temp_dir = tempfile.gettempdir()
            wkhtmltopdf_url = "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.msvc2015-win64.exe"
            installer_path = os.path.join(temp_dir, "wkhtmltopdf.exe")
            
            self.log_signal.emit(f"Downloading wkhtmltopdf from {wkhtmltopdf_url}")
            urllib.request.urlretrieve(wkhtmltopdf_url, installer_path)
            
            # Silent install
            cmd = f"{installer_path} /S"
            self.log_signal.emit(f"Executing: {cmd}")
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_signal.emit("Failed to install Wkhtmltopdf")
                self.log_signal.emit(stderr.decode().strip())
                return False
            
            # Add to PATH
            wkhtmltopdf_path = os.path.join("C:", "Program Files", "wkhtmltopdf", "bin")
            os.environ["PATH"] += os.pathsep + wkhtmltopdf_path
            
            return True
        except Exception as e:
            self.log_signal.emit(f"Error installing Wkhtmltopdf: {str(e)}")
            return False
    
    def install_odoo(self):
        try:
            install_dir = self.config['install_dir']
            version = self.config['odoo_version']
            
            # Create directory if not exists
            if not os.path.exists(install_dir):
                os.makedirs(install_dir)
            
            # Clone Odoo repository
            if os.path.exists(os.path.join(install_dir, "odoo")):
                self.log_signal.emit("Removing existing Odoo directory...")
                shutil.rmtree(os.path.join(install_dir, "odoo"))
            
            cmd = f'git clone --depth 1 --branch {version} https://www.github.com/odoo/odoo "{os.path.join(install_dir, "odoo")}"'
            self.log_signal.emit(f"Executing: {cmd}")
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_signal.emit("Failed to clone Odoo repository")
                self.log_signal.emit(stderr.decode().strip())
                return False
            
            # Create virtual environment
            venv_path = os.path.join(install_dir, "venv")
            if os.path.exists(venv_path):
                shutil.rmtree(venv_path)
            
            cmd = f'python -m venv "{venv_path}"'
            self.log_signal.emit(f"Executing: {cmd}")
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_signal.emit("Failed to create virtual environment")
                self.log_signal.emit(stderr.decode().strip())
                return False
            
            # Install requirements
            pip_path = os.path.join(venv_path, "Scripts", "pip")
            requirements_path = os.path.join(install_dir, "odoo", "requirements.txt")
            
            cmds = [
                f'"{pip_path}" install --upgrade pip setuptools wheel',
                f'"{pip_path}" install -r "{requirements_path}"',
                f'"{pip_path}" install psycopg2-binary pywin32'
            ]
            
            for cmd in cmds:
                self.log_signal.emit(f"Executing: {cmd}")
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    self.log_signal.emit(f"Command failed: {cmd}")
                    self.log_signal.emit(stderr.decode().strip())
                    return False
            
            return True
        except Exception as e:
            self.log_signal.emit(f"Error installing Odoo: {str(e)}")
            return False
    
    def configure_odoo(self):
        try:
            install_dir = self.config['install_dir']
            config_content = f"""
[options]
admin_passwd = {self.config['admin_password']}
db_host = localhost
db_port = 5432
db_user = {self.config['db_user']}
db_password = {self.config['admin_password']}
db_name = {self.config['db_name']}
addons_path = {os.path.join(install_dir, "odoo", "addons")},{os.path.join(install_dir, "custom", "addons")}
xmlrpc_port = {self.config['port']}
data_dir = {os.path.join(install_dir, "data")}
"""
            
            # SMTP configuration
            if self.config['smtp_host']:
                config_content += f"""
smtp_server = {self.config['smtp_host']}
smtp_port = {self.config['smtp_port']}
smtp_user = {self.config['smtp_user']}
smtp_password = {self.config['smtp_pass']}
smtp_ssl = {'true' if str(self.config['smtp_port']) in ['465', '587'] else 'false'}
"""
            
            # Workers configuration
            if self.config['workers'] > 0:
                config_content += f"""
workers = {self.config['workers']}
"""
            
            # Demo data
            config_content += f"""
without_demo = {'false' if self.config['demo_data'] else 'true'}
"""
            
            # Create directories
            os.makedirs(os.path.join(install_dir, "custom", "addons"), exist_ok=True)
            os.makedirs(os.path.join(install_dir, "etc"), exist_ok=True)
            os.makedirs(os.path.join(install_dir, "data"), exist_ok=True)
            
            # Write config file
            config_path = os.path.join(install_dir, "etc", "odoo.conf")
            with open(config_path, "w") as f:
                f.write(config_content)
            
            return True
        except Exception as e:
            self.log_signal.emit(f"Error configuring Odoo: {str(e)}")
            return False
    
    def create_startup_scripts(self):
        try:
            install_dir = self.config['install_dir']
            
            # Create batch file
            bat_content = f"""
@echo off
call "{os.path.join(install_dir, "venv", "Scripts", "activate")}"
python "{os.path.join(install_dir, "odoo", "odoo-bin")}" -c "{os.path.join(install_dir, "etc", "odoo.conf")}"
pause
"""
            bat_path = os.path.join(install_dir, "start_odoo.bat")
            with open(bat_path, "w") as f:
                f.write(bat_content)
            
            # Create PowerShell script
            ps_content = f"""
$env:Path += ";{os.path.join(install_dir, "venv", "Scripts")}"
& "{os.path.join(install_dir, "venv", "Scripts", "python")}" "{os.path.join(install_dir, "odoo", "odoo-bin")}" -c "{os.path.join(install_dir, "etc", "odoo.conf")}"
Read-Host -Prompt "Press Enter to exit"
"""
            ps_path = os.path.join(install_dir, "start_odoo.ps1")
            with open(ps_path, "w") as f:
                f.write(ps_content)
            
            return True
        except Exception as e:
            self.log_signal.emit(f"Error creating startup scripts: {str(e)}")
            return False
    
    def create_windows_service(self):
        try:
            install_dir = self.config['install_dir']
            
            # Install pywin32 service utilities if not present
            cmd = f'"{os.path.join(install_dir, "venv", "Scripts", "pip")}" install pywin32'
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate()
            
            # Create service script
            service_script = f"""
import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import os
import sys

class OdooService(win32serviceutil.ServiceFramework):
    _svc_name_ = "Odoo"
    _svc_display_name_ = "Odoo Server"
    _svc_description_ = "Odoo ERP Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.process:
            self.process.terminate()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        odoo_path = r"{os.path.join(install_dir, "odoo", "odoo-bin")}"
        config_path = r"{os.path.join(install_dir, "etc", "odoo.conf")}"
        python_path = r"{os.path.join(install_dir, "venv", "Scripts", "python.exe")}"
        
        self.process = subprocess.Popen(
            [python_path, odoo_path, "-c", config_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.process.wait()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(OdooService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(OdooService)
"""
            service_script_path = os.path.join(install_dir, "odoo_service.py")
            with open(service_script_path, "w") as f:
                f.write(service_script)
            
            # Install the service
            cmd = f'"{os.path.join(install_dir, "venv", "Scripts", "python")}" "{service_script_path}" install'
            self.log_signal.emit(f"Executing: {cmd}")
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_signal.emit("Failed to install Windows service")
                self.log_signal.emit(stderr.decode().strip())
                return False
            
            # Start the service
            cmd = f'"{os.path.join(install_dir, "venv", "Scripts", "python")}" "{service_script_path}" start'
            self.log_signal.emit(f"Executing: {cmd}")
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_signal.emit("Failed to start Windows service")
                self.log_signal.emit(stderr.decode().strip())
                return False
            
            return True
        except Exception as e:
            self.log_signal.emit(f"Error creating Windows service: {str(e)}")
            return False
    
    def start_odoo(self):
        try:
            install_dir = self.config['install_dir']
            
            if self.config['create_service']:
                # Start via service
                cmd = 'net start Odoo'
            else:
                # Start via batch file in new window
                bat_path = os.path.join(install_dir, "start_odoo.bat")
                cmd = f'start cmd /k "{bat_path}"'
            
            self.log_signal.emit(f"Executing: {cmd}")
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_signal.emit("Failed to start Odoo")
                self.log_signal.emit(stderr.decode().strip())
                return False
            
            return True
        except Exception as e:
            self.log_signal.emit(f"Error starting Odoo: {str(e)}")
            return False

class InstallerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Odoo One-Click Installer for Windows")
        self.setMinimumSize(900, 700)
        
        # Set application icon
        self.setWindowIcon(QIcon.fromTheme("applications-office"))
        
        # Modern style
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                color: #495057;
                font-weight: bold;
            }
            QPushButton {
                background-color: #007bff;
                border: none;
                color: white;
                padding: 8px 16px;
                text-align: center;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QPushButton#installButton {
                background-color: #28a745;
                font-size: 16px;
                padding: 10px 24px;
            }
            QPushButton#installButton:hover {
                background-color: #218838;
            }
            QLineEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 1px solid #80bdff;
                outline: none;
            }
            QProgressBar {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #28a745;
                width: 10px;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 5px;
                background: white;
                margin-top: 5px;
            }
            QTabBar::tab {
                padding: 8px 12px;
                background: #e9ecef;
                border: 1px solid #dee2e6;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
                margin-bottom: -1px;
            }
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QLabel {
                color: #495057;
            }
            QLabel#titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLabel#statusLabel {
                font-style: italic;
                color: #6c757d;
            }
        """)
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Header
        self.create_header()
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_installation_tab()
        self.create_configuration_tab()
        self.create_log_tab()
        
        # Footer
        self.create_footer()
        
        # Initialize installation thread
        self.installation_thread = None
    
    def create_header(self):
        header_layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("Odoo One-Click Installer for Windows")
        title_label.setObjectName("titleLabel")
        header_layout.addWidget(title_label, 1, Qt.AlignCenter)
        
        # System info
        system_info = QLabel(f"Windows {platform.release()} | {platform.architecture()[0]}")
        system_info.setStyleSheet("font-size: 12px; color: #6c757d;")
        header_layout.addWidget(system_info, 0, Qt.AlignRight | Qt.AlignTop)
        
        self.main_layout.addLayout(header_layout)
    
    def create_installation_tab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "Installation")
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Odoo Version Group
        version_group = QGroupBox("Odoo Version")
        version_layout = QFormLayout()
        version_layout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        
        self.version_combo = QComboBox()
        self.version_combo.addItems(["17.0", "16.0", "15.0", "14.0"])
        self.version_combo.setCurrentIndex(0)
        version_layout.addRow("Select Odoo Version:", self.version_combo)
        
        version_group.setLayout(version_layout)
        layout.addWidget(version_group)
        
        # Installation Directory Group
        dir_group = QGroupBox("Installation Directory")
        dir_layout = QHBoxLayout()
        
        self.dir_edit = QLineEdit(os.path.join(os.environ["ProgramFiles"], "Odoo"))
        self.dir_edit.setPlaceholderText("Enter installation directory")
        dir_layout.addWidget(self.dir_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(browse_btn)
        
        dir_group.setLayout(dir_layout)
        layout.addWidget(dir_group)
        
        # Database Configuration Group
        db_group = QGroupBox("Database Configuration")
        db_layout = QFormLayout()
        db_layout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        
        self.db_name_edit = QLineEdit("odoo")
        self.db_name_edit.setPlaceholderText("Database name")
        db_layout.addRow("Database Name:", self.db_name_edit)
        
        self.db_user_edit = QLineEdit("postgres")
        self.db_user_edit.setPlaceholderText("Database user")
        db_layout.addRow("Database User:", self.db_user_edit)
        
        self.admin_pass_edit = QLineEdit()
        self.admin_pass_edit.setPlaceholderText("Admin password")
        self.admin_pass_edit.setEchoMode(QLineEdit.Password)
        db_layout.addRow("Admin Password:", self.admin_pass_edit)
        
        db_group.setLayout(db_layout)
        layout.addWidget(db_group)
        
        # Options Group
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        
        self.install_wkhtmltopdf_check = QCheckBox("Install Wkhtmltopdf (required for PDF reports)")
        self.install_wkhtmltopdf_check.setChecked(True)
        options_layout.addWidget(self.install_wkhtmltopdf_check)
        
        self.create_service_check = QCheckBox("Create Windows service (recommended)")
        self.create_service_check.setChecked(True)
        options_layout.addWidget(self.create_service_check)
        
        self.start_service_check = QCheckBox("Start Odoo after installation")
        self.start_service_check.setChecked(True)
        options_layout.addWidget(self.start_service_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready to install")
        self.status_label.setObjectName("statusLabel")
        layout.addWidget(self.status_label)
        
        # Install button
        self.install_btn = QPushButton("Install Odoo")
        self.install_btn.setObjectName("installButton")
        self.install_btn.clicked.connect(self.start_installation)
        layout.addWidget(self.install_btn, 0, Qt.AlignCenter)
        
        layout.addStretch()
    
    def create_configuration_tab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "Configuration")
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Port Configuration Group
        port_group = QGroupBox("Port Configuration")
        port_layout = QFormLayout()
        
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1024, 65535)
        self.port_spin.setValue(8069)
        port_layout.addRow("Odoo Port:", self.port_spin)
        
        port_group.setLayout(port_layout)
        layout.addWidget(port_group)
        
        # Email Configuration Group
        email_group = QGroupBox("Email Configuration")
        email_layout = QFormLayout()
        
        self.smtp_host_edit = QLineEdit()
        self.smtp_host_edit.setPlaceholderText("smtp.example.com")
        email_layout.addRow("SMTP Host:", self.smtp_host_edit)
        
        self.smtp_port_edit = QLineEdit("587")
        self.smtp_port_edit.setPlaceholderText("587")
        email_layout.addRow("SMTP Port:", self.smtp_port_edit)
        
        self.smtp_user_edit = QLineEdit()
        self.smtp_user_edit.setPlaceholderText("user@example.com")
        email_layout.addRow("SMTP User:", self.smtp_user_edit)
        
        self.smtp_pass_edit = QLineEdit()
        self.smtp_pass_edit.setPlaceholderText("password")
        self.smtp_pass_edit.setEchoMode(QLineEdit.Password)
        email_layout.addRow("SMTP Password:", self.smtp_pass_edit)
        
        email_group.setLayout(email_layout)
        layout.addWidget(email_group)
        
        # Additional Options Group
        add_options_group = QGroupBox("Additional Options")
        add_options_layout = QVBoxLayout()
        
        self.demo_data_check = QCheckBox("Load demo data")
        self.demo_data_check.setChecked(True)
        add_options_layout.addWidget(self.demo_data_check)
        
        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(0, 32)
        self.workers_spin.setValue(2)
        add_options_layout.addWidget(QLabel("Number of workers (0 for default):"))
        add_options_layout.addWidget(self.workers_spin)
        
        add_options_group.setLayout(add_options_layout)
        layout.addWidget(add_options_group)
        
        # Save button
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_configuration)
        layout.addWidget(save_btn, 0, Qt.AlignRight)
        
        layout.addStretch()
    
    def create_log_tab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "Log")
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("font-family: 'Courier New', monospace;")
        layout.addWidget(self.log_text)
        
        # Log controls
        controls_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Clear Log")
        clear_btn.clicked.connect(self.clear_log)
        controls_layout.addWidget(clear_btn)
        
        save_log_btn = QPushButton("Save Log to File")
        save_log_btn.clicked.connect(self.save_log)
        controls_layout.addWidget(save_log_btn)
        
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
    
    def create_footer(self):
        footer_layout = QHBoxLayout()
        
        # System info
        system_info = QLabel(f"Python {platform.python_version()} | PyQt5 | {platform.architecture()[0]}")
        system_info.setStyleSheet("font-size: 12px; color: #6c757d;")
        footer_layout.addWidget(system_info)
        
        # Links
        links_layout = QHBoxLayout()
        links_layout.setSpacing(15)
        
        odoo_link = QLabel('<a href="https://www.odoo.com" style="color: #007bff; text-decoration: none;">Odoo Website</a>')
        odoo_link.setOpenExternalLinks(True)
        links_layout.addWidget(odoo_link)
        
        docs_link = QLabel('<a href="https://www.odoo.com/documentation" style="color: #007bff; text-decoration: none;">Documentation</a>')
        docs_link.setOpenExternalLinks(True)
        links_layout.addWidget(docs_link)
        
        forum_link = QLabel('<a href="https://www.odoo.com/forum" style="color: #007bff; text-decoration: none;">Community Forum</a>')
        forum_link.setOpenExternalLinks(True)
        links_layout.addWidget(forum_link)
        
        footer_layout.addLayout(links_layout)
        
        self.main_layout.addLayout(footer_layout)
    
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Installation Directory", os.environ["ProgramFiles"])
        if directory:
            self.dir_edit.setText(directory)
    
    def start_installation(self):
        # Get configuration from UI
        config = {
            'odoo_version': self.version_combo.currentText(),
            'install_dir': self.dir_edit.text(),
            'db_name': self.db_name_edit.text(),
            'db_user': self.db_user_edit.text(),
            'admin_password': self.admin_pass_edit.text(),
            'port': self.port_spin.value(),
            'install_wkhtmltopdf': self.install_wkhtmltopdf_check.isChecked(),
            'create_service': self.create_service_check.isChecked(),
            'start_service': self.start_service_check.isChecked(),
            'demo_data': self.demo_data_check.isChecked(),
            'workers': self.workers_spin.value(),
            'smtp_host': self.smtp_host_edit.text(),
            'smtp_port': self.smtp_port_edit.text(),
            'smtp_user': self.smtp_user_edit.text(),
            'smtp_pass': self.smtp_pass_edit.text()
        }
        
        # Validate configuration
        if not config['install_dir']:
            QMessageBox.warning(self, "Error", "Please specify an installation directory")
            return
        
        if not config['admin_password']:
            QMessageBox.warning(self, "Error", "Please set an admin password")
            return
        
        # Disable UI during installation
        self.set_ui_enabled(False)
        self.log_text.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("Starting installation...")
        
        # Create and start installation thread
        self.installation_thread = InstallationThread(config)
        self.installation_thread.progress_update.connect(self.update_progress)
        self.installation_thread.finished_signal.connect(self.installation_finished)
        self.installation_thread.log_signal.connect(self.log_message)
        self.installation_thread.start()
    
    def update_progress(self, value, message):
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
        self.log_text.append(f"[{value}%] {message}")
    
    def log_message(self, message):
        self.log_text.append(message)
    
    def installation_finished(self, success, message):
        self.set_ui_enabled(True)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.progress_bar.setValue(100)
            self.status_label.setText("Installation completed successfully!")
            self.log_text.append("Installation completed successfully!")
            
            # Offer to open Odoo in browser
            reply = QMessageBox.question(self, "Odoo Installed", 
                                      "Odoo has been successfully installed. Would you like to open it in your browser now?",
                                      QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                webbrowser.open(f"http://localhost:{self.port_spin.value()}")
        else:
            QMessageBox.critical(self, "Error", message)
            self.status_label.setText(f"Installation failed: {message}")
            self.log_text.append(f"ERROR: {message}")
    
    def set_ui_enabled(self, enabled):
        self.tab_widget.setEnabled(enabled)
        self.install_btn.setEnabled(enabled)
    
    def save_configuration(self):
        QMessageBox.information(self, "Success", "Configuration saved successfully")
    
    def clear_log(self):
        self.log_text.clear()
    
    def save_log(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Log File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.log_text.toPlainText())
                QMessageBox.information(self, "Success", "Log saved successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save log: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Check if running on supported platform
    if platform.system() not in ['Windows']:
        QMessageBox.critical(None, "Unsupported Platform", 
                            "This installer only supports Windows.\n"
                            "Linux and macOS are not supported in this version.")
        sys.exit(1)
    
    # Check if running as administrator
    try:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            QMessageBox.critical(None, "Administrator Rights Required", 
                                "This installer requires administrator privileges.\n"
                                "Please restart the installer as Administrator.")
            sys.exit(1)
    except:
        pass
    
    # Create and show dialog
    dialog = InstallerDialog()
    dialog.show()
    
    sys.exit(app.exec_())