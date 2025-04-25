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
from PyQt5.QtGui import QIcon, QFont, QPixmap

class DolibarrInstallationThread(QThread):
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
                self.finished_signal.emit(False, "Configuration invalide")
                return
            
            # Step 1: Install Chocolatey if not present
            self.progress_update.emit(5, "Installation de Chocolatey...")
            if not self.install_chocolatey():
                self.finished_signal.emit(False, "Échec de l'installation de Chocolatey")
                return
            
            # Step 2: Install system dependencies
            self.progress_update.emit(20, "Installation des dépendances système...")
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
            
            # Step 3: Install and configure Apache
            self.progress_update.emit(35, "Installation d'Apache...")
            if not self.install_apache():
                self.finished_signal.emit(False, "Échec de l'installation d'Apache")
                return
            
            # Step 4: Install PHP
            self.progress_update.emit(45, "Installation de PHP...")
            if not self.install_php():
                self.finished_signal.emit(False, "Échec de l'installation de PHP")
                return
            
            # Step 5: Install MariaDB
            self.progress_update.emit(55, "Installation de MariaDB...")
            if not self.install_mariadb():
                self.finished_signal.emit(False, "Échec de l'installation de MariaDB")
                return
            
            # Step 6: Install Dolibarr
            self.progress_update.emit(65, "Téléchargement de Dolibarr...")
            if not self.install_dolibarr():
                self.finished_signal.emit(False, "Échec de l'installation de Dolibarr")
                return
            
            # Step 7: Configure Apache for Dolibarr
            self.progress_update.emit(80, "Configuration d'Apache...")
            if not self.configure_apache():
                self.finished_signal.emit(False, "Échec de la configuration d'Apache")
                return
            
            # Step 8: Create database and user
            self.progress_update.emit(85, "Configuration de la base de données...")
            if not self.configure_database():
                self.finished_signal.emit(False, "Échec de la configuration de la base de données")
                return
            
            # Step 9: Final configuration
            self.progress_update.emit(90, "Configuration finale...")
            if not self.final_configuration():
                self.finished_signal.emit(False, "Échec de la configuration finale")
                return
            
            # Step 10: Start services
            self.progress_update.emit(95, "Démarrage des services...")
            if not self.start_services():
                self.finished_signal.emit(False, "Échec du démarrage des services")
                return
            
            self.progress_update.emit(100, "Installation terminée avec succès!")
            self.finished_signal.emit(True, "Dolibarr installé avec succès")
            
        except Exception as e:
            self.finished_signal.emit(False, f"Erreur pendant l'installation: {str(e)}")
    
    def validate_inputs(self):
        if not self.config['dolibarr_version']:
            self.log_signal.emit("Erreur: Version de Dolibarr non sélectionnée")
            return False
        if not self.config['install_dir']:
            self.log_signal.emit("Erreur: Répertoire d'installation non spécifié")
            return False
        if not self.config['admin_password']:
            self.log_signal.emit("Erreur: Mot de passe admin non défini")
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
    
    def install_system_dependencies(self):
        try:
            self.log_signal.emit("Vérification des dépendances système...")
            
            # Liste des paquets Chocolatey requis
            packages = [
                ("git", "git --version"),
                ("vcredist-all", None),
                ("curl", "curl --version")
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
    
    def install_apache(self):
        try:
            self.log_signal.emit("Installation d'Apache...")
            
            # Vérifier si Apache est déjà installé
            if self.check_command_available("httpd -v"):
                self.log_signal.emit("Apache est déjà installé")
                return True
                
            # Installer Apache via Chocolatey
            cmd = "choco install -y apache-httpd --params '/installLocation:C:\Apache24'"
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
                self.log_signal.emit("Échec de l'installation d'Apache")
                return False
            
            # Ajouter Apache au PATH
            apache_path = r"C:\Apache24\bin"
            os.environ["PATH"] += os.pathsep + apache_path
            
            return True
            
        except Exception as e:
            self.log_signal.emit(f"Erreur lors de l'installation d'Apache: {str(e)}")
            return False
    
    def install_php(self):
        try:
            self.log_signal.emit("Installation de PHP...")
            
            # Vérifier si PHP est déjà installé
            if self.check_command_available("php -v"):
                self.log_signal.emit("PHP est déjà installé")
                return True
                
            # Installer PHP via Chocolatey avec les extensions nécessaires
            php_version = "8.1"  # Version compatible avec Dolibarr
            cmd = f"choco install -y php --version={php_version} --params '\"/InstallDir:C:\PHP /ThreadSafe /AddToPath /InstallExtensions\"'"
            
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
                self.log_signal.emit("Échec de l'installation de PHP")
                return False
            
            # Configurer php.ini
            php_ini_path = r"C:\PHP\php.ini"
            if os.path.exists(php_ini_path):
                with open(php_ini_path, 'r') as f:
                    content = f.read()
                
                # Activer les extensions nécessaires
                content = content.replace(';extension=curl', 'extension=curl')
                content = content.replace(';extension=gd', 'extension=gd')
                content = content.replace(';extension=mbstring', 'extension=mbstring')
                content = content.replace(';extension=mysqli', 'extension=mysqli')
                content = content.replace(';extension=openssl', 'extension=openssl')
                content = content.replace(';extension=pdo_mysql', 'extension=pdo_mysql')
                
                # Augmenter les limites
                content = content.replace('max_execution_time = 30', 'max_execution_time = 300')
                content = content.replace('memory_limit = 128M', 'memory_limit = 256M')
                content = content.replace('post_max_size = 8M', 'post_max_size = 32M')
                content = content.replace('upload_max_filesize = 2M', 'upload_max_filesize = 32M')
                
                with open(php_ini_path, 'w') as f:
                    f.write(content)
            
            return True
            
        except Exception as e:
            self.log_signal.emit(f"Erreur lors de l'installation de PHP: {str(e)}")
            return False
    
    def install_mariadb(self):
        try:
            self.log_signal.emit("Installation de MariaDB...")
            
            # Vérifier si MariaDB est déjà installé
            if self.check_command_available("mysql --version"):
                self.log_signal.emit("MariaDB est déjà installé")
                return True
                
            # Installer MariaDB via Chocolatey
            cmd = f"choco install -y mariadb --params '/PASSWORD:{self.config['admin_password']}'"
            
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
                self.log_signal.emit("Échec de l'installation de MariaDB")
                return False
            
            # Ajouter MariaDB au PATH
            mariadb_path = r"C:\Program Files\MariaDB 10.6\bin"
            os.environ["PATH"] += os.pathsep + mariadb_path
            
            return True
            
        except Exception as e:
            self.log_signal.emit(f"Erreur lors de l'installation de MariaDB: {str(e)}")
            return False
    
    def install_dolibarr(self):
        try:
            install_dir = self.config['install_dir']
            version = self.config['dolibarr_version']
            
            # Créer le répertoire si nécessaire
            if not os.path.exists(install_dir):
                os.makedirs(install_dir)
            
            # Télécharger Dolibarr
            self.log_signal.emit(f"Téléchargement de Dolibarr {version}...")
            
            if version == "stable":
                download_url = "https://github.com/Dolibarr/dolibarr/archive/refs/heads/stable.zip"
            else:
                download_url = f"https://github.com/Dolibarr/dolibarr/archive/{version}.zip"
            
            temp_dir = tempfile.gettempdir()
            zip_path = os.path.join(temp_dir, "dolibarr.zip")
            
            # Téléchargement
            urllib.request.urlretrieve(download_url, zip_path)
            
            # Extraire l'archive
            self.log_signal.emit("Extraction de Dolibarr...")
            shutil.unpack_archive(zip_path, install_dir)
            
            # Renommer le dossier
            extracted_dir = os.path.join(install_dir, f"dolibarr-{version}")
            final_dir = os.path.join(install_dir, "dolibarr")
            
            if os.path.exists(final_dir):
                shutil.rmtree(final_dir)
            
            os.rename(extracted_dir, final_dir)
            
            # Créer le répertoire des documents
            documents_dir = os.path.join(install_dir, "documents")
            os.makedirs(documents_dir, exist_ok=True)
            
            # Supprimer le fichier zip temporaire
            os.unlink(zip_path)
            
            return True
            
        except Exception as e:
            self.log_signal.emit(f"Erreur lors de l'installation de Dolibarr: {str(e)}")
            return False
    
    def configure_apache(self):
        try:
            install_dir = self.config['install_dir']
            dolibarr_dir = os.path.join(install_dir, "dolibarr")
            
            # Configurer le VirtualHost pour Dolibarr
            self.log_signal.emit("Configuration d'Apache pour Dolibarr...")
            
            vhost_config = f"""
Listen {self.config['port']}

<VirtualHost *:{self.config['port']}>
    DocumentRoot "{dolibarr_dir}/htdocs"
    ServerName localhost
    
    <Directory "{dolibarr_dir}/htdocs">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    # Configuration PHP
    PHPIniDir "C:/PHP"
    AddHandler application/x-httpd-php .php
    
    # Chemin vers php-cgi.exe
    ScriptAlias /php-cgi/ "C:/PHP/"
    Action application/x-httpd-php "/php-cgi/php-cgi.exe"
    
    # Dossiers à protéger
    <Directory "{dolibarr_dir}/install">
        Require all denied
    </Directory>
    
    <Directory "{dolibarr_dir}/documents">
        Require all denied
    </Directory>
    
    ErrorLog "logs/dolibarr-error.log"
    CustomLog "logs/dolibarr-access.log" common
</VirtualHost>
"""
            # Écrire la configuration
            conf_path = r"C:\Apache24\conf\extra\dolibarr.conf"
            with open(conf_path, 'w') as f:
                f.write(vhost_config)
            
            # Inclure la configuration dans httpd.conf
            httpd_conf_path = r"C:\Apache24\conf\httpd.conf"
            with open(httpd_conf_path, 'r') as f:
                content = f.read()
            
            # Vérifier si l'inclusion est déjà présente
            if f"Include conf/extra/dolibarr.conf" not in content:
                with open(httpd_conf_path, 'a') as f:
                    f.write("\n# Configuration Dolibarr\n")
                    f.write("Include conf/extra/dolibarr.conf\n")
            
            return True
            
        except Exception as e:
            self.log_signal.emit(f"Erreur lors de la configuration d'Apache: {str(e)}")
            return False
    
    def configure_database(self):
        try:
            self.log_signal.emit("Création de la base de données et de l'utilisateur...")
            
            # Commandes SQL
            sql_commands = [
                f"CREATE DATABASE IF NOT EXISTS {self.config['db_name']} CHARACTER SET utf8 COLLATE utf8_general_ci;",
                f"CREATE USER IF NOT EXISTS '{self.config['db_user']}'@'localhost' IDENTIFIED BY '{self.config['admin_password']}';",
                f"GRANT ALL PRIVILEGES ON {self.config['db_name']}.* TO '{self.config['db_user']}'@'localhost';",
                "FLUSH PRIVILEGES;"
            ]
            
            # Exécuter les commandes via mysql
            for cmd in sql_commands:
                full_cmd = f'mysql -u root -p"{self.config["admin_password"]}" -e "{cmd}"'
                
                process = subprocess.Popen(full_cmd, shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True)
                
                stdout, stderr = process.communicate()
                
                if process.returncode != 0:
                    self.log_signal.emit(f"Erreur lors de l'exécution de: {cmd}")
                    self.log_signal.emit(stderr.strip())
                    return False
            
            return True
            
        except Exception as e:
            self.log_signal.emit(f"Erreur lors de la configuration de la base de données: {str(e)}")
            return False
    
    def final_configuration(self):
        try:
            install_dir = self.config['install_dir']
            dolibarr_dir = os.path.join(install_dir, "dolibarr")
            
            self.log_signal.emit("Configuration finale de Dolibarr...")
            
            # Créer le fichier de configuration
            conf_content = f"""<?php
// Dolibarr configuration file
// Version {self.config['dolibarr_version']}

// 1. Database configuration
$dolibarr_main_db_host = 'localhost';
$dolibarr_main_db_port = '3306';
$dolibarr_main_db_name = '{self.config['db_name']}';
$dolibarr_main_db_user = '{self.config['db_user']}';
$dolibarr_main_db_pass = '{self.config['admin_password']}';
$dolibarr_main_db_type = 'mysqli';
$dolibarr_main_db_character_set = 'utf8';
$dolibarr_main_db_collation = 'utf8_general_ci';

// 2. Dolibarr configuration
$dolibarr_main_document_root = '{dolibarr_dir}/htdocs';
$dolibarr_main_url_root = 'http://localhost:{self.config['port']}';
$dolibarr_main_data_root = '{install_dir}/documents';

// 3. Security
$dolibarr_main_authentication = 'dolibarr';
$dolibarr_main_force_https = '0';
$dolibarr_main_prod = '0';

// 4. Performance
$dolibarr_nocsrfcheck = '0';
$dolibarr_main_restrict_os_commands = 'mysqldump, mysql, pg_dump, pgrestore';

// 5. Modules
$dolibarr_main_modules = array();
"""
            # Écrire le fichier conf.php
            conf_path = os.path.join(dolibarr_dir, "htdocs", "conf", "conf.php")
            os.makedirs(os.path.dirname(conf_path), exist_ok=True)
            
            with open(conf_path, 'w') as f:
                f.write(conf_content)
            
            # Configurer les permissions
            documents_dir = os.path.join(install_dir, "documents")
            os.chmod(documents_dir, 0o777)
            
            return True
            
        except Exception as e:
            self.log_signal.emit(f"Erreur lors de la configuration finale: {str(e)}")
            return False
    
    def start_services(self):
        try:
            self.log_signal.emit("Démarrage des services...")
            
            # Démarrer Apache
            cmd = "net start Apache2.4"
            process = subprocess.Popen(cmd, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    universal_newlines=True)
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_signal.emit("Échec du démarrage d'Apache")
                self.log_signal.emit(stderr.strip())
                return False
            
            # Démarrer MariaDB
            cmd = "net start MariaDB"
            process = subprocess.Popen(cmd, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    universal_newlines=True)
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_signal.emit("Échec du démarrage de MariaDB")
                self.log_signal.emit(stderr.strip())
                return False
            
            return True
            
        except Exception as e:
            self.log_signal.emit(f"Erreur lors du démarrage des services: {str(e)}")
            return False

class DolibarrInstallerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Installateur Dolibarr pour Windows")
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
        title_label = QLabel("Installateur Dolibarr pour Windows")
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
        
        # Dolibarr Version Group
        version_group = QGroupBox("Version Dolibarr")
        version_layout = QFormLayout()
        version_layout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        
        self.version_combo = QComboBox()
        self.version_combo.addItems(["stable", "18.0", "17.0", "16.0", "15.0"])
        self.version_combo.setCurrentIndex(0)
        version_layout.addRow("Version de Dolibarr:", self.version_combo)
        
        version_group.setLayout(version_layout)
        layout.addWidget(version_group)
        
        # Installation Directory Group
        dir_group = QGroupBox("Répertoire d'installation")
        dir_layout = QHBoxLayout()
        
        self.dir_edit = QLineEdit(os.path.join(os.environ["ProgramFiles"], "Dolibarr"))
        self.dir_edit.setPlaceholderText("Entrez le répertoire d'installation")
        dir_layout.addWidget(self.dir_edit)
        
        browse_btn = QPushButton("Parcourir...")
        browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(browse_btn)
        
        dir_group.setLayout(dir_layout)
        layout.addWidget(dir_group)
        
        # Database Configuration Group
        db_group = QGroupBox("Configuration de la base de données")
        db_layout = QFormLayout()
        db_layout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        
        self.db_name_edit = QLineEdit("dolibarr")
        self.db_name_edit.setPlaceholderText("Nom de la base de données")
        db_layout.addRow("Nom de la base:", self.db_name_edit)
        
        self.db_user_edit = QLineEdit("dolibarr")
        self.db_user_edit.setPlaceholderText("Utilisateur de la base")
        db_layout.addRow("Utilisateur:", self.db_user_edit)
        
        self.admin_pass_edit = QLineEdit()
        self.admin_pass_edit.setPlaceholderText("Mot de passe admin")
        self.admin_pass_edit.setEchoMode(QLineEdit.Password)
        db_layout.addRow("Mot de passe admin:", self.admin_pass_edit)
        
        db_group.setLayout(db_layout)
        layout.addWidget(db_group)
        
        # Options Group
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        
        self.create_service_check = QCheckBox("Créer un service Windows (recommandé)")
        self.create_service_check.setChecked(True)
        options_layout.addWidget(self.create_service_check)
        
        self.start_service_check = QCheckBox("Démarrer Dolibarr après installation")
        self.start_service_check.setChecked(True)
        options_layout.addWidget(self.start_service_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Prêt à installer")
        self.status_label.setObjectName("statusLabel")
        layout.addWidget(self.status_label)
        
        # Install button
        self.install_btn = QPushButton("Installer Dolibarr")
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
        port_group = QGroupBox("Configuration du port")
        port_layout = QFormLayout()
        
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1024, 65535)
        self.port_spin.setValue(8080)
        port_layout.addRow("Port HTTP:", self.port_spin)
        
        port_group.setLayout(port_layout)
        layout.addWidget(port_group)
        
        # Additional Options Group
        add_options_group = QGroupBox("Options supplémentaires")
        add_options_layout = QVBoxLayout()
        
        self.demo_data_check = QCheckBox("Charger les données de démonstration")
        self.demo_data_check.setChecked(True)
        add_options_layout.addWidget(self.demo_data_check)
        
        add_options_group.setLayout(add_options_layout)
        layout.addWidget(add_options_group)
        
        # Save button
        save_btn = QPushButton("Sauvegarder la configuration")
        save_btn.clicked.connect(self.save_configuration)
        layout.addWidget(save_btn, 0, Qt.AlignRight)
        
        layout.addStretch()
    
    def create_log_tab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "Journal")
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("font-family: 'Courier New', monospace;")
        layout.addWidget(self.log_text)
        
        # Log controls
        controls_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Effacer le journal")
        clear_btn.clicked.connect(self.clear_log)
        controls_layout.addWidget(clear_btn)
        
        save_log_btn = QPushButton("Sauvegarder le journal")
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
        
        dolibarr_link = QLabel('<a href="https://www.dolibarr.org" style="color: #007bff; text-decoration: none;">Site de Dolibarr</a>')
        dolibarr_link.setOpenExternalLinks(True)
        links_layout.addWidget(dolibarr_link)
        
        docs_link = QLabel('<a href="https://wiki.dolibarr.org" style="color: #007bff; text-decoration: none;">Documentation</a>')
        docs_link.setOpenExternalLinks(True)
        links_layout.addWidget(docs_link)
        
        forum_link = QLabel('<a href="https://www.dolibarr.org/forum" style="color: #007bff; text-decoration: none;">Forum communautaire</a>')
        forum_link.setOpenExternalLinks(True)
        links_layout.addWidget(forum_link)
        
        footer_layout.addLayout(links_layout)
        
        self.main_layout.addLayout(footer_layout)
    
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Sélectionnez le répertoire d'installation", os.environ["ProgramFiles"])
        if directory:
            self.dir_edit.setText(directory)
    
    def start_installation(self):
        # Get configuration from UI
        config = {
            'dolibarr_version': self.version_combo.currentText(),
            'install_dir': self.dir_edit.text(),
            'db_name': self.db_name_edit.text(),
            'db_user': self.db_user_edit.text(),
            'admin_password': self.admin_pass_edit.text(),
            'port': self.port_spin.value(),
            'create_service': self.create_service_check.isChecked(),
            'start_service': self.start_service_check.isChecked(),
            'demo_data': self.demo_data_check.isChecked()
        }
        
        # Validate configuration
        if not config['install_dir']:
            QMessageBox.warning(self, "Erreur", "Veuillez spécifier un répertoire d'installation")
            return
        
        if not config['admin_password']:
            QMessageBox.warning(self, "Erreur", "Veuillez définir un mot de passe admin")
            return
        
        # Disable UI during installation
        self.set_ui_enabled(False)
        self.log_text.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("Démarrage de l'installation...")
        
        # Create and start installation thread
        self.installation_thread = DolibarrInstallationThread(config)
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
            QMessageBox.information(self, "Succès", message)
            self.progress_bar.setValue(100)
            self.status_label.setText("Installation terminée avec succès!")
            self.log_text.append("Installation terminée avec succès!")
            
            # Offer to open Dolibarr in browser
            reply = QMessageBox.question(self, "Dolibarr Installé", 
                                      "Dolibarr a été installé avec succès. Voulez-vous l'ouvrir dans votre navigateur maintenant?",
                                      QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                webbrowser.open(f"http://localhost:{self.port_spin.value()}")
        else:
            QMessageBox.critical(self, "Erreur", message)
            self.status_label.setText(f"Échec de l'installation: {message}")
            self.log_text.append(f"ERREUR: {message}")
    
    def set_ui_enabled(self, enabled):
        self.tab_widget.setEnabled(enabled)
        self.install_btn.setEnabled(enabled)
    
    def save_configuration(self):
        QMessageBox.information(self, "Succès", "Configuration sauvegardée avec succès")
    
    def clear_log(self):
        self.log_text.clear()
    
    def save_log(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le journal", "", "Fichiers texte (*.txt);;Tous les fichiers (*)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.toPlainText())
                QMessageBox.information(self, "Succès", "Journal sauvegardé avec succès")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de la sauvegarde du journal: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Check if running on supported platform
    if platform.system() not in ['Windows']:
        QMessageBox.critical(None, "Plateforme non supportée", 
                            "Cet installateur ne fonctionne que sous Windows.\n"
                            "Linux et macOS ne sont pas supportés dans cette version.")
        sys.exit(1)
    
    # Check if running as administrator
    try:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            QMessageBox.critical(None, "Droits administrateur requis", 
                                "Cet installateur nécessite des privilèges d'administrateur.\n"
                                "Veuillez relancer l'installateur en tant qu'Administrateur.")
            sys.exit(1)
    except:
        pass
    
    # Create and show dialog
    dialog = DolibarrInstallerDialog()
    dialog.show()
    
    sys.exit(app.exec_())