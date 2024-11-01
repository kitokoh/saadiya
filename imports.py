# imports.py
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtGui import QIcon
import sys
import json
import os  
import shutil
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from translation import TranslatorManager  # Importer le gestionnaire de traductions

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from cryptography.fernet import Fernet
import subprocess

#pour changer la destinationet developper en local c  ext ici que ca se passe 
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
#_curentfolder = os.getcwd()  # Ou définissez-le comme un chemin spécifique si nécessaire

# # Définir le chemin du dossier userdata
#user_data_dir = os.path.join(_curentfolder)