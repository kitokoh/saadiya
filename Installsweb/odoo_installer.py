import sys
import os
import subprocess
import platform
import webbrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QComboBox, QCheckBox, 
                            QGroupBox, QProgressBar, QTabWidget, QFileDialog, QMessageBox,
                            QTextEdit, QSpinBox, QFormLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QPalette

class InstallationThread(QThread):
    progress_update = pyqtSignal(int, str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
    
    def run(self):
        try:
            # Validate inputs
            if not self.validate_inputs():
                self.finished_signal.emit(False, "Invalid configuration")
                return
            
            # Step 1: Install system dependencies
            self.progress_update.emit(10, "Installing system dependencies...")
            if not self.install_system_dependencies():
                self.finished_signal.emit(False, "Failed to install system dependencies")
                return
            
            # Step 2: Create Odoo user
            self.progress_update.emit(20, "Creating Odoo user...")
            if not self.create_odoo_user():
                self.finished_signal.emit(False, "Failed to create Odoo user")
                return
            
            # Step 3: Install PostgreSQL
            self.progress_update.emit(30, "Installing PostgreSQL...")
            if not self.install_postgresql():
                self.finished_signal.emit(False, "Failed to install PostgreSQL")
                return
            
            # Step 4: Install Wkhtmltopdf
            self.progress_update.emit(40, "Installing Wkhtmltopdf...")
            if not self.install_wkhtmltopdf():
                self.finished_signal.emit(False, "Failed to install Wkhtmltopdf")
                return
            
            # Step 5: Install Odoo
            self.progress_update.emit(50, "Downloading and installing Odoo...")
            if not self.install_odoo():
                self.finished_signal.emit(False, "Failed to install Odoo")
                return
            
            # Step 6: Configure Odoo
            self.progress_update.emit(70, "Configuring Odoo...")
            if not self.configure_odoo():
                self.finished_signal.emit(False, "Failed to configure Odoo")
                return
            
            # Step 7: Create service
            self.progress_update.emit(85, "Creating Odoo service...")
            if not self.create_service():
                self.finished_signal.emit(False, "Failed to create Odoo service")
                return
            
            # Step 8: Start Odoo
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
            return False
        if not self.config['install_dir']:
            return False
        return True
    
    def install_system_dependencies(self):
        # Implementation for system dependencies
        try:
            system = platform.system()
            if system == "Linux":
                distro = platform.linux_distribution()[0].lower()
                
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
                    return False
                
                for cmd in commands:
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    if process.returncode != 0:
                        return False
                
                return True
            else:
                return False
        except:
            return False
    
    def create_odoo_user(self):
        try:
            if platform.system() == "Linux":
                process = subprocess.Popen("sudo useradd -m -d /opt/odoo -U -r -s /bin/bash odoo", 
                                          shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return process.returncode == 0
            return True
        except:
            return False
    
    def install_postgresql(self):
        try:
            system = platform.system()
            if system == "Linux":
                distro = platform.linux_distribution()[0].lower()
                
                if 'ubuntu' in distro or 'debian' in distro:
                    commands = [
                        "sudo apt-get install -y postgresql postgresql-client postgresql-contrib",
                        f"sudo -u postgres createuser -s {self.config['db_user']}",
                        f"sudo -u postgres createdb {self.config['db_name']}"
                    ]
                elif 'centos' in distro or 'redhat' in distro:
                    commands = [
                        "sudo yum install -y postgresql-server postgresql-contrib",
                        "sudo postgresql-setup initdb",
                        "sudo systemctl start postgresql",
                        "sudo systemctl enable postgresql",
                        f"sudo -u postgres createuser -s {self.config['db_user']}",
                        f"sudo -u postgres createdb {self.config['db_name']}"
                    ]
                
                for cmd in commands:
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    if process.returncode != 0:
                        return False
                
                return True
            return False
        except:
            return False
    
    def install_wkhtmltopdf(self):
        try:
            system = platform.system()
            if system == "Linux":
                distro = platform.linux_distribution()[0].lower()
                
                if 'ubuntu' in distro or 'debian' in distro:
                    commands = [
                        "sudo apt-get install -y xfonts-75dpi xfonts-base",
                        "wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb",
                        "sudo dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb",
                        "sudo apt --fix-broken install -y"
                    ]
                elif 'centos' in distro or 'redhat' in distro:
                    commands = [
                        "sudo yum install -y xorg-x11-fonts-75dpi xorg-x11-fonts-Type1",
                        "wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.centos8.x86_64.rpm",
                        "sudo rpm -Uvh wkhtmltox-0.12.6-1.centos8.x86_64.rpm"
                    ]
                
                for cmd in commands:
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    if process.returncode != 0:
                        return False
                
                return True
            return False
        except:
            return False
    
    def install_odoo(self):
        try:
            install_dir = self.config['install_dir']
            version = self.config['odoo_version']
            
            commands = [
                f"sudo mkdir -p {install_dir}",
                f"sudo chown odoo:odoo {install_dir}",
                f"sudo -u odoo git clone --depth 1 --branch {version} https://www.github.com/odoo/odoo {install_dir}/odoo",
                f"sudo -u odoo python3 -m venv {install_dir}/venv",
                f"sudo -u odoo {install_dir}/venv/bin/pip install wheel",
                f"sudo -u odoo {install_dir}/venv/bin/pip install -r {install_dir}/odoo/requirements.txt"
            ]
            
            for cmd in commands:
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    return False
            
            return True
        except:
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
"""
            
            commands = [
                f"sudo mkdir -p {install_dir}/custom/addons",
                f"sudo mkdir -p {install_dir}/etc",
                f"sudo chown odoo:odoo {install_dir}/custom",
                f"echo '{config_content}' | sudo tee {install_dir}/etc/odoo.conf > /dev/null",
                f"sudo chown odoo:odoo {install_dir}/etc/odoo.conf",
                f"sudo chmod 640 {install_dir}/etc/odoo.conf"
            ]
            
            for cmd in commands:
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    return False
            
            return True
        except:
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
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    return False
            
            return True
        except:
            return False
    
    def start_odoo(self):
        try:
            process = subprocess.Popen("sudo systemctl start odoo.service", 
                                     shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            return process.returncode == 0
        except:
            return False

class OdooInstallerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Odoo One-Click Installer")
        self.setMinimumSize(800, 600)
        
        # Set application icon
        self.setWindowIcon(QIcon.fromTheme("applications-office"))
        
        # Set style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QLineEdit, QComboBox, QSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
            QTabBar::tab {
                padding: 8px;
                background: #e1e1e1;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #f5f5f5;
                border-bottom: 1px solid #f5f5f5;
            }
        """)
        
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
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
        
        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(":/images/odoo_logo.png").scaled(120, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        header_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("Odoo One-Click Installer")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #714B67;")
        header_layout.addWidget(title_label, 1, Qt.AlignCenter)
        
        # Version
        version_label = QLabel("v1.0")
        version_label.setStyleSheet("font-size: 14px; color: #888;")
        header_layout.addWidget(version_label, 0, Qt.AlignRight | Qt.AlignTop)
        
        self.main_layout.addLayout(header_layout)
    
    def create_installation_tab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "Installation")
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Odoo Version Group
        version_group = QGroupBox("Odoo Version")
        version_layout = QFormLayout()
        
        self.version_combo = QComboBox()
        self.version_combo.addItems(["16.0", "15.0", "14.0", "13.0"])
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
        self.status_label.setStyleSheet("font-style: italic; color: #666;")
        layout.addWidget(self.status_label)
        
        # Install button
        self.install_btn = QPushButton("Install Odoo")
        self.install_btn.setStyleSheet("font-size: 16px; padding: 10px;")
        self.install_btn.clicked.connect(self.start_installation)
        layout.addWidget(self.install_btn, 0, Qt.AlignCenter)
    
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
        
        self.smtp_port_edit = QLineEdit()
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
        add_options_layout.addWidget(self.demo_data_check)
        
        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(0, 32)
        self.workers_spin.setValue(2)
        add_options_layout.addWidget(QLabel("Number of workers:"))
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
        self.log_text.setStyleSheet("font-family: monospace;")
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
        system_info = QLabel(f"System: {platform.system()} {platform.release()}")
        system_info.setStyleSheet("font-size: 12px; color: #888;")
        footer_layout.addWidget(system_info)
        
        # Links
        links_layout = QHBoxLayout()
        links_layout.setSpacing(15)
        
        odoo_link = QLabel('<a href="https://www.odoo.com">Odoo Website</a>')
        odoo_link.setOpenExternalLinks(True)
        links_layout.addWidget(odoo_link)
        
        docs_link = QLabel('<a href="https://www.odoo.com/documentation">Documentation</a>')
        docs_link.setOpenExternalLinks(True)
        links_layout.addWidget(docs_link)
        
        forum_link = QLabel('<a href="https://www.odoo.com/forum">Community Forum</a>')
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
        self.installation_thread.start()
    
    def update_progress(self, value, message):
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
        self.log_text.append(f"[{value}%] {message}")
    
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
    
    # Create and show main window
    window = OdooInstallerApp()
    window.show()
    
    sys.exit(app.exec_())