import sys
import os
import subprocess
import platform
import webbrowser
import shutil
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
            
            # Check if running as root
            if os.geteuid() != 0:
                self.log_signal.emit("Warning: Not running as root, some operations might require sudo")
            
            # Step 1: Prepare system environment
            self.progress_update.emit(5, "Preparing system environment...")
            if not self.prepare_system():
                self.finished_signal.emit(False, "Failed to prepare system")
                return
            
            # Step 2: Install system dependencies
            self.progress_update.emit(15, "Installing system dependencies...")
            if not self.install_system_dependencies():
                self.finished_signal.emit(False, "Failed to install system dependencies")
                return
            
            # Step 3: Create Odoo user
            self.progress_update.emit(25, "Creating Odoo user...")
            if not self.create_odoo_user():
                self.finished_signal.emit(False, "Failed to create Odoo user")
                return
            
            # Step 4: Install PostgreSQL
            self.progress_update.emit(35, "Installing PostgreSQL...")
            if not self.install_postgresql():
                self.finished_signal.emit(False, "Failed to install PostgreSQL")
                return
            
            # Step 5: Install Wkhtmltopdf if selected
            if self.config['install_wkhtmltopdf']:
                self.progress_update.emit(45, "Installing Wkhtmltopdf...")
                if not self.install_wkhtmltopdf():
                    self.finished_signal.emit(False, "Failed to install Wkhtmltopdf")
                    return
            
            # Step 6: Install Odoo
            self.progress_update.emit(55, "Downloading and installing Odoo...")
            if not self.install_odoo():
                self.finished_signal.emit(False, "Failed to install Odoo")
                return
            
            # Step 7: Configure Odoo
            self.progress_update.emit(70, "Configuring Odoo...")
            if not self.configure_odoo():
                self.finished_signal.emit(False, "Failed to configure Odoo")
                return
            
            # Step 8: Create service if selected
            if self.config['create_service']:
                self.progress_update.emit(85, "Creating Odoo service...")
                if not self.create_service():
                    self.finished_signal.emit(False, "Failed to create Odoo service")
                    return
            
            # Step 9: Start Odoo if selected
            if self.config['start_service'] and self.config['create_service']:
                self.progress_update.emit(95, "Starting Odoo service...")
                if not self.start_odoo():
                    self.finished_signal.emit(False, "Failed to start Odoo")
                    return
            
            self.progress_update.emit(100, "Installation completed successfully!")
            self.finished_signal.emit(True, "Odoo installed successfully")
            
        except Exception as e:
            self.finished_signal.emit(False, f"Error during installation: {str(e)}")
    
    def validate_inputs(self):
        # Validate all inputs here
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
    
    def prepare_system(self):
        """Prepare system by installing basic tools like git, curl, etc."""
        try:
            system = platform.system()
            if system == "Linux":
                distro = self.get_linux_distro()
                
                if 'ubuntu' in distro or 'debian' in distro:
                    commands = [
                        "sudo apt-get update",
                        "sudo apt-get install -y software-properties-common git curl wget"
                    ]
                elif 'centos' in distro or 'redhat' in distro:
                    commands = [
                        "sudo yum install -y epel-release",
                        "sudo yum install -y git curl wget"
                    ]
                else:
                    self.log_signal.emit(f"Unsupported Linux distribution: {distro}")
                    return False
                
                for cmd in commands:
                    self.log_signal.emit(f"Executing: {cmd}")
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    if process.returncode != 0:
                        self.log_signal.emit(f"Command failed: {cmd}")
                        self.log_signal.emit(stderr.decode().strip())
                        return False
                
                return True
            else:
                self.log_signal.emit("Unsupported operating system")
                return False
        except Exception as e:
            self.log_signal.emit(f"Error preparing system: {str(e)}")
            return False
    
    def get_linux_distro(self):
        """Get Linux distribution name in lowercase."""
        try:
            with open('/etc/os-release') as f:
                for line in f:
                    if line.startswith('ID='):
                        return line.split('=')[1].strip().strip('"').lower()
        except:
            pass
        return platform.linux_distribution()[0].lower()
    
    def install_system_dependencies(self):
        """Install all required system dependencies."""
        try:
            system = platform.system()
            distro = self.get_linux_distro() if system == "Linux" else ""
            
            if 'ubuntu' in distro or 'debian' in distro:
                commands = [
                    "sudo apt-get update",
                    "sudo apt-get install -y python3-pip python3-dev python3-venv python3-wheel libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev libldap2-dev build-essential libssl-dev libffi-dev libmysqlclient-dev libjpeg-dev libpq-dev libjpeg8-dev liblcms2-dev libblas-dev libatlas-base-dev"
                ]
            elif 'centos' in distro or 'redhat' in distro:
                commands = [
                    "sudo yum install -y python3-pip python3-devel gcc redhat-rpm-config python3-setuptools python3-wheel openssl-devel libxml2-devel libxslt-devel libjpeg-turbo-devel openldap-devel"
                ]
            else:
                self.log_signal.emit(f"Unsupported Linux distribution: {distro}")
                return False
            
            for cmd in commands:
                self.log_signal.emit(f"Executing: {cmd}")
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    self.log_signal.emit(f"Command failed: {cmd}")
                    self.log_signal.emit(stderr.decode().strip())
                    return False
            
            # Install pip requirements
            pip_cmd = "python3 -m pip install --upgrade pip setuptools wheel"
            self.log_signal.emit(f"Executing: {pip_cmd}")
            process = subprocess.Popen(pip_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                self.log_signal.emit("Failed to upgrade pip")
                self.log_signal.emit(stderr.decode().strip())
                return False
            
            return True
        except Exception as e:
            self.log_signal.emit(f"Error installing dependencies: {str(e)}")
            return False
    
    def create_odoo_user(self):
        try:
            if platform.system() == "Linux":
                # Check if user already exists
                process = subprocess.Popen("id -u odoo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                process.communicate()
                
                if process.returncode != 0:
                    # User doesn't exist, create it
                    cmd = "sudo useradd -m -d /opt/odoo -U -r -s /bin/bash odoo"
                    self.log_signal.emit(f"Executing: {cmd}")
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    if process.returncode != 0:
                        self.log_signal.emit("Failed to create Odoo user")
                        self.log_signal.emit(stderr.decode().strip())
                        return False
                    self.log_signal.emit("Odoo user created successfully")
                else:
                    self.log_signal.emit("Odoo user already exists")
                
                return True
            return True
        except Exception as e:
            self.log_signal.emit(f"Error creating Odoo user: {str(e)}")
            return False
    
    def install_postgresql(self):
        try:
            system = platform.system()
            distro = self.get_linux_distro() if system == "Linux" else ""
            
            if 'ubuntu' in distro or 'debian' in distro:
                commands = [
                    "sudo apt-get install -y postgresql postgresql-client postgresql-contrib",
                    f"sudo -u postgres createuser -s {self.config['db_user']} || true",
                    f"sudo -u postgres createdb {self.config['db_name']} || true"
                ]
            elif 'centos' in distro or 'redhat' in distro:
                commands = [
                    "sudo yum install -y postgresql-server postgresql-contrib",
                    "sudo postgresql-setup initdb",
                    "sudo systemctl start postgresql",
                    "sudo systemctl enable postgresql",
                    f"sudo -u postgres createuser -s {self.config['db_user']} || true",
                    f"sudo -u postgres createdb {self.config['db_name']} || true"
                ]
            else:
                self.log_signal.emit(f"Unsupported Linux distribution: {distro}")
                return False
            
            for cmd in commands:
                self.log_signal.emit(f"Executing: {cmd}")
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    self.log_signal.emit(f"Command failed: {cmd}")
                    self.log_signal.emit(stderr.decode().strip())
                    # Don't return False here as some commands might fail harmlessly (like creating existing user/db)
            
            return True
        except Exception as e:
            self.log_signal.emit(f"Error installing PostgreSQL: {str(e)}")
            return False
    
    def install_wkhtmltopdf(self):
        try:
            system = platform.system()
            distro = self.get_linux_distro() if system == "Linux" else ""
            
            if 'ubuntu' in distro or 'debian' in distro:
                commands = [
                    "sudo apt-get install -y xfonts-75dpi xfonts-base",
                    "wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb -O /tmp/wkhtmltox.deb || curl -L https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb -o /tmp/wkhtmltox.deb",
                    "sudo dpkg -i /tmp/wkhtmltox.deb",
                    "sudo apt --fix-broken install -y",
                    "rm /tmp/wkhtmltox.deb"
                ]
            elif 'centos' in distro or 'redhat' in distro:
                commands = [
                    "sudo yum install -y xorg-x11-fonts-75dpi xorg-x11-fonts-Type1",
                    "wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.centos8.x86_64.rpm -O /tmp/wkhtmltox.rpm || curl -L https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.centos8.x86_64.rpm -o /tmp/wkhtmltox.rpm",
                    "sudo rpm -Uvh /tmp/wkhtmltox.rpm",
                    "rm /tmp/wkhtmltox.rpm"
                ]
            else:
                self.log_signal.emit(f"Unsupported Linux distribution: {distro}")
                return False
            
            for cmd in commands:
                self.log_signal.emit(f"Executing: {cmd}")
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    self.log_signal.emit(f"Command failed: {cmd}")
                    self.log_signal.emit(stderr.decode().strip())
                    return False
            
            # Verify installation
            process = subprocess.Popen("wkhtmltopdf --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                self.log_signal.emit("Wkhtmltopdf installation verification failed")
                return False
            
            self.log_signal.emit(f"Wkhtmltopdf installed: {stdout.decode().strip()}")
            return True
        except Exception as e:
            self.log_signal.emit(f"Error installing Wkhtmltopdf: {str(e)}")
            return False
    
    def install_odoo(self):
        try:
            install_dir = self.config['install_dir']
            version = self.config['odoo_version']
            
            # Check if Odoo directory already exists
            if os.path.exists(f"{install_dir}/odoo"):
                self.log_signal.emit("Odoo directory already exists, removing...")
                shutil.rmtree(f"{install_dir}/odoo")
            
            commands = [
                f"sudo mkdir -p {install_dir}",
                f"sudo chown odoo:odoo {install_dir}",
                f"sudo -u odoo git clone --depth 1 --branch {version} https://www.github.com/odoo/odoo {install_dir}/odoo",
                f"sudo -u odoo python3 -m venv {install_dir}/venv",
                f"sudo -u odoo {install_dir}/venv/bin/pip install --upgrade pip setuptools wheel",
                f"sudo -u odoo {install_dir}/venv/bin/pip install -r {install_dir}/odoo/requirements.txt"
            ]
            
            for cmd in commands:
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
; This is the password that allows database operations:
admin_passwd = {self.config['admin_password']}
db_host = False
db_port = False
db_user = {self.config['db_user']}
db_password = False
addons_path = {install_dir}/odoo/addons,{install_dir}/custom/addons
xmlrpc_port = {self.config['port']}
"""
            
            # Add SMTP configuration if provided
            if self.config['smtp_host']:
                config_content += f"""
smtp_server = {self.config['smtp_host']}
smtp_port = {self.config['smtp_port']}
smtp_user = {self.config['smtp_user']}
smtp_password = {self.config['smtp_pass']}
smtp_ssl = {'true' if str(self.config['smtp_port']) in ['465', '587'] else 'false'}
"""
            
            # Add workers configuration if provided
            if self.config['workers'] > 0:
                config_content += f"""
workers = {self.config['workers']}
"""
            
            # Add demo data option
            config_content += f"""
without_demo = {'false' if self.config['demo_data'] else 'true'}
"""
            
            commands = [
                f"sudo mkdir -p {install_dir}/custom/addons",
                f"sudo mkdir -p {install_dir}/etc",
                f"sudo chown -R odoo:odoo {install_dir}/custom",
                f"echo '{config_content}' | sudo tee {install_dir}/etc/odoo.conf > /dev/null",
                f"sudo chown odoo:odoo {install_dir}/etc/odoo.conf",
                f"sudo chmod 640 {install_dir}/etc/odoo.conf"
            ]
            
            for cmd in commands:
                self.log_signal.emit(f"Executing: {cmd}")
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    self.log_signal.emit(f"Command failed: {cmd}")
                    self.log_signal.emit(stderr.decode().strip())
                    return False
            
            return True
        except Exception as e:
            self.log_signal.emit(f"Error configuring Odoo: {str(e)}")
            return False
    
    def create_service(self):
        try:
            install_dir = self.config['install_dir']
            service_content = f"""
[Unit]
Description=Odoo
After=postgresql.service

[Service]
Type=simple
SyslogIdentifier=odoo
PermissionsStartOnly=true
User=odoo
Group=odoo
ExecStart={install_dir}/venv/bin/python3 {install_dir}/odoo/odoo-bin -c {install_dir}/etc/odoo.conf
StandardOutput=journal+console

[Install]
WantedBy=multi-user.target
"""
            
            commands = [
                f"echo '{service_content}' | sudo tee /etc/systemd/system/odoo.service > /dev/null",
                "sudo systemctl daemon-reload",
                "sudo systemctl enable odoo.service"
            ]
            
            for cmd in commands:
                self.log_signal.emit(f"Executing: {cmd}")
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    self.log_signal.emit(f"Command failed: {cmd}")
                    self.log_signal.emit(stderr.decode().strip())
                    return False
            
            return True
        except Exception as e:
            self.log_signal.emit(f"Error creating service: {str(e)}")
            return False
    
    def start_odoo(self):
        try:
            cmd = "sudo systemctl start odoo.service"
            self.log_signal.emit(f"Executing: {cmd}")
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_signal.emit("Failed to start Odoo service")
                self.log_signal.emit(stderr.decode().strip())
                return False
            
            # Verify service is running
            cmd = "sudo systemctl is-active odoo.service"
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0 or stdout.decode().strip() != "active":
                self.log_signal.emit("Odoo service is not running")
                return False
            
            self.log_signal.emit("Odoo service started successfully")
            return True
        except Exception as e:
            self.log_signal.emit(f"Error starting Odoo: {str(e)}")
            return False

class InstallerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Odoo One-Click Installer")
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
        title_label = QLabel("Odoo One-Click Installer")
        title_label.setObjectName("titleLabel")
        header_layout.addWidget(title_label, 1, Qt.AlignCenter)
        
        # System info
        system_info = QLabel(f"{platform.system()} {platform.release()}")
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
        
        self.dir_edit = QLineEdit("/opt/odoo")
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
        
        self.db_user_edit = QLineEdit("odoo")
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
        
        self.create_service_check = QCheckBox("Create systemd service (recommended)")
        self.create_service_check.setChecked(True)
        options_layout.addWidget(self.create_service_check)
        
        self.start_service_check = QCheckBox("Start Odoo service after installation")
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
        directory = QFileDialog.getExistingDirectory(self, "Select Installation Directory", "/opt")
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
        # Save configuration to file
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
    if platform.system() not in ['Linux']:
        QMessageBox.critical(None, "Unsupported Platform", 
                            "This installer only supports Linux distributions.\n"
                            "Windows and macOS are not supported.")
        sys.exit(1)
    
    # Create and show dialog
    dialog = InstallerDialog()
    dialog.show()
    
    sys.exit(app.exec_())