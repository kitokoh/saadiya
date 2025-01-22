import json
import os
import psutil  # Pour obtenir l'adresse MAC
import smtplib
import socket  # Ajoutez cette ligne en haut de votre script
from collections import defaultdict
from cryptography.fernet import Fernet
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Chemins des répertoires et des fichiers
#_current_folder = os.getcwd()
user_data_dir1 = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

#user_data_dir1 = os.path.dirname(_current_folder)
user_data_dir = os.path.join(user_data_dir1, 'resources', 'data')
key_data_dir = os.path.join(user_data_dir1, 'resources')
