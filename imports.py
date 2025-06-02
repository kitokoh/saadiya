# imports.py
import json
import logging
import os
import platform
import shutil
import smtplib
import subprocess
import sys
from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from cryptography.fernet import Fernet
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from checklicence import LicenseChecker
from statistique.nombredegrup import GroupCounter
from statistique.stat import Dashboard
from translation import TranslatorManager  # Importer le gestionnaire de traductions


def get_user_data_dir():
    os_name = platform.system()  # Detect the operating system
    if os_name == "Windows":
        # Use the AppData/Roaming directory for Windows
        user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
    elif os_name == "Darwin":
        # Use the Library/Application Support directory for macOS
        user_data_dir = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "saadiya")
    else:
        # For other OS (like Linux), use ~/.local/share
        user_data_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "saadiya")
    
    # Create the directory if it doesn't exist
    os.makedirs(user_data_dir, exist_ok=True)
    return user_data_dir

# Usage
user_data_dir = get_user_data_dir()
#pour changer la destinationet developper en local c  ext ici que ca se passe 
#j utilise ce ligne de code dans mon application  pyqt pour le .exe propose moi le code qui 
#permet de generer aussi le .dmg et met des condition de maniere a ceque si nous somme face a un os 
#alors ca utiliste tel lien et si on est en face d un .exe ca utilise ca 
DB_PATH = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'groups333.db')
# DB_PATH_links = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'links1.db')
# DB_PATH_prompts = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'prompts1.db')
# DB_PATH_management = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'management.db')

# DB_PATH_prompts_archiv = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'prompts_backup.db')

# DB_PATH_prompt_command = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'prompts1.db')
DB_PATH_prompt_command = DB_PATH
# DB_PATH_notes = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'notess.db')
DB_PATH_links = DB_PATH
DB_PATH_prompts = DB_PATH
DB_PATH_notes = DB_PATH     
DB_PATH_prompts_archiv = DB_PATH
DB_PATH_management = DB_PATH
DB_PATH_instances = DB_PATH
DB_PATH_finances = DB_PATH
DB_PATH_contacts = DB_PATH
DB_PATH_licence = DB_PATH
DB_PATH_update = DB_PATH
DB_PATH_status = DB_PATH
DB_PATH_multilingual_text1 = DB_PATH

DB_PATH_demarrage = DB_PATH
DB_PATH_Home = DB_PATH
DB_PATH_mail = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'mailsms.db')

APP_INFO_FILE = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'APP_INFO_FILE.json')
# DB_PATH_update = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'update.db')
#user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
# _curentfolder = os.getcwd()  # Ou définissez-le comme un chemin spécifique si nécessaire

# # # Définir le chemin du dossier userdata
# user_data_dir = os.path.join(_curentfolder)