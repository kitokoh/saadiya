import os 
import sys
import subprocess
import random
import string
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import QTimer  # Importez QTimer

class LicenseGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.licence_folder = "C:\\bon"
        self.tmp_file = os.path.join(self.licence_folder, "tmp.txt")
        self.log_file = os.path.join(os.path.expanduser("~"), "Desktop", "journalInstallation.txt")
        self.error_flag = 0
        
        self.init_ui()
        self.generate_license()  # Appel automatique de la fonction pour générer la licence

    def init_ui(self):
        layout = QVBoxLayout()

        self.info_label = QLabel("Génération de la licence en cours...")
        layout.addWidget(self.info_label)

        self.setLayout(layout)
        self.setWindowTitle("Générateur de Licence")
        self.show()

    def log(self, message):
        with open(self.log_file, "a") as log_file:
            log_file.write(f"{message}\n")

    def generate_license(self):
        self.log(f"[INFO] - Script démarré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if not os.path.exists(self.licence_folder):
            os.makedirs(self.licence_folder)
            self.log(f"[INFO] - Dossier {self.licence_folder} créé.")

        if os.path.exists(self.tmp_file):
            os.remove(self.tmp_file)
            self.log(f"[INFO] - Ancien fichier {self.tmp_file} supprimé.")

        # Récupération du numéro de série
        serial = self.get_serial_number()
        if not serial:
            self.log("[ERROR] - Impossible de récupérer le numéro de série.")
            self.error_flag = 1

        self.log(f"[INFO] - Numéro de série récupéré : {serial}")

        # Adresse MAC fixe
        mac = "E4-42-A6-3A-AC"
        self.log(f"[INFO] - Adresse MAC fixe : {mac}")

        # Récupération de la date et heure
        formatted_date = self.get_formatted_datetime()
        self.log(f"[INFO] - Date et heure formatées : {formatted_date}")

        # Nom d'utilisateur
        username = os.getenv("USERNAME")
        self.log(f"[INFO] - Nom d'utilisateur : {username}")

        # Génération de chaîne aléatoire
        rand_str = self.generate_random_string(500)
        self.log(f"[INFO] - Chaîne aléatoire générée avec succès.")

        # Stockage des informations dans tmp.txt
        with open(self.tmp_file, "w") as tmp:
            tmp.write(f"serial={serial}\n")
            tmp.write(f"mac={mac}\n")
            tmp.write(f"datetime={formatted_date}\n")
            tmp.write(f"username={username}\n")
            tmp.write(f"randStr={rand_str}\n")

        # Rendre tmp.txt caché et système
        os.system(f'attrib +h +s "{self.tmp_file}"')
        self.log(f"[INFO] - {self.tmp_file} est maintenant caché et marqué comme fichier système.")

        if self.error_flag == 0:
            self.log(f"[INFO] - Script terminé avec succès le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            # Affichage d'un message de succès
            #QMessageBox.information(self, "Succès", "Licence générée avec succès!")
        else:
            self.log(f"[ERROR] - Le script s'est terminé avec des erreurs le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            QMessageBox.critical(self, "Erreur", "Des erreurs se sont produites lors de la génération de la licence.")

        # Utilisation d'un timer pour fermer l'application après 2 secondes
        QTimer.singleShot(20, self.close)  # Ferme l'application après 2 secondes

    def get_serial_number(self):
        try:
            serial = subprocess.check_output("wmic bios get serialnumber", shell=True)
            return serial.decode().strip().split('\n')[1].strip()  # récupérer la deuxième ligne
        except Exception as e:
            self.log(f"[ERROR] - {str(e)}")
            return None

    def get_formatted_datetime(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M")

    def generate_random_string(self, length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LicenseGenerator()
    sys.exit(app.exec_())
