# import os
# import random
# import subprocess
# import sys
# from datetime import datetime
# from PyQt5 import QtWidgets, uic
# from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo


# class LicenseGeneratorApp(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(LicenseGeneratorApp, self).__init__()
#         uic.loadUi('interface.ui', self)  # Charger l'interface à partir d'un fichier .ui

#         self.licence_folder = "C:\\bon"
#         self.licence_file = "test.txt"
#         self.generate_button.clicked.connect(self.generate_license)

#         self.translator = QTranslator(self)
#         self.setup_translations()

#     def setup_translations(self):
#         locale = QLocale.system().name()
#         if self.translator.load(locale, QLibraryInfo.location(QLibraryInfo.TranslationsPath)):
#             QtWidgets.QApplication.instance().installTranslator(self.translator)

#     def generate_license(self):
#         error_flag = 0

#         # Créer le dossier C:\bon s'il n'existe pas
#         if not os.path.exists(self.licence_folder):
#             try:
#                 os.makedirs(self.licence_folder)
#             except Exception as e:
#                 QtWidgets.QMessageBox.critical(self, "Erreur", f"[ERROR] - Impossible de créer le dossier {self.licence_folder}.")
#                 return

#         # Supprimer test.txt s'il existe déjà
#         licence_file_path = os.path.join(self.licence_folder, self.licence_file)
#         if os.path.exists(licence_file_path):
#             try:
#                 os.remove(licence_file_path)
#             except Exception as e:
#                 QtWidgets.QMessageBox.critical(self, "Erreur", f"[ERROR] - Impossible de supprimer l'ancien fichier {self.licence_file}.")
#                 error_flag = 1

#         # Récupérer le numéro de série de l'ordinateur
#         serial = self.get_serial_number()
#         if not serial:
#             QtWidgets.QMessageBox.critical(self, "Erreur", "[ERROR] - Impossible de récupérer le numéro de série de l'ordinateur.")
#             error_flag = 1
#             return

#         # Récupérer l'adresse MAC
#         mac = self.get_mac_address()
#         if not mac:
#             QtWidgets.QMessageBox.critical(self, "Erreur", "[ERROR] - Impossible de récupérer l'adresse MAC valide.")
#             error_flag = 1
#             return

#         # Récupérer la date et l'heure actuelles
#         current_datetime = self.get_current_datetime()

#         # Récupérer le nom de l'utilisateur actuel
#         username = os.getlogin()

#         # Générer une chaîne aléatoire de 500 caractères
#         rand_str = self.generate_random_string(500)

#         # Composer la licence
#         licence = f"001{serial}:{mac}{current_datetime}{username}{rand_str}"

#         # Enregistrer la licence dans test.txt
#         try:
#             with open(licence_file_path, 'w') as licence_file:
#                 licence_file.write(licence)
#         except Exception as e:
#             QtWidgets.QMessageBox.critical(self, "Erreur", f"[ERROR] - Impossible d'écrire dans {self.licence_file}.")
#             error_flag = 1
#             return

#         # Message de succès
#         #QtWidgets.QMessageBox.information(self, "Succès", f"[SUCCES] - La licence a été générée et enregistrée dans {self.licence_folder}\\{self.licence_file}.")

#         if error_flag:
#             QtWidgets.QMessageBox.warning(self, "Échec", "[ECHEC] - Une erreur s'est produite pendant l'exécution du script.")
#         else:
#             QtWidgets.QMessageBox.information(self, "Fin", "[FIN] - Script exécuté avec succès.")

#     def get_serial_number(self):
#         try:
#             serial = subprocess.check_output("wmic bios get serialnumber", shell=True).decode().split("\n")[1].strip()
#             return serial
#         except Exception:
#             return None

#     def get_mac_address(self):
#         try:
#             mac = subprocess.check_output("getmac /fo csv /nh", shell=True).decode().split(",")[0].replace('"', '').strip()
#             if mac != "N/A":
#                 return mac
#             else:
#                 return None
#         except Exception:
#             return None

#     def get_current_datetime(self):
#         now = datetime.now()
#         return now.strftime("%d%m%Y%H%M")

#     def generate_random_string(self, length):
#         chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
#         return ''.join(random.choice(chars) for _ in range(length))




# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     window = LicenseGeneratorApp()
#     window.show()
#     sys.exit(app.exec_())
    
# if __name__ == "__main__":
#     main()  # Appelle la fonction main si le script est exécuté directement

import os
import random
import subprocess
import sys
from datetime import datetime
import time

class LicenseGenerator:
    def __init__(self):
        self.licence_folder = "C:\\bon"
        self.licence_file = "test.txt"

    def generate_license(self):
        error_flag = 0

        # Créer le dossier C:\bon s'il n'existe pas
        if not os.path.exists(self.licence_folder):
            try:
                os.makedirs(self.licence_folder)
            except Exception as e:
                print(f"[ERROR] - Impossible de créer le dossier {self.licence_folder}.")
                return

        # Supprimer test.txt s'il existe déjà
        licence_file_path = os.path.join(self.licence_folder, self.licence_file)
        if os.path.exists(licence_file_path):
            try:
                os.remove(licence_file_path)
            except Exception as e:
                print(f"[ERROR] - Impossible de supprimer l'ancien fichier {self.licence_file}.")
                error_flag = 1

        # Récupérer le numéro de série de l'ordinateur
        serial = self.get_serial_number()
        if not serial:
            print("[ERROR] - Impossible de récupérer le numéro de série de l'ordinateur.")
            error_flag = 1
            return

        # Récupérer l'adresse MAC
        mac = self.get_mac_address()
        if not mac:
            print("[ERROR] - Impossible de récupérer l'adresse MAC valide.")
            error_flag = 1
            return

        # Récupérer la date et l'heure actuelles
        current_datetime = self.get_current_datetime()

        # Récupérer le nom de l'utilisateur actuel
        username = os.getlogin()

        # Générer une chaîne aléatoire de 500 caractères
        rand_str = self.generate_random_string(500)

        # Composer la licence
        licence = f"001{serial}:{mac}{current_datetime}{username}{rand_str}"

        # Enregistrer la licence dans test.txt
        try:
            with open(licence_file_path, 'w') as licence_file:
                licence_file.write(licence)
        except Exception as e:
            print(f"[ERROR] - Impossible d'écrire dans {self.licence_file}.")
            error_flag = 1
            return

        # Message de succès
        if error_flag:
            print("[ÉCHEC] - Une erreur s'est produite pendant l'exécution du script.")
        else:
            print(f"[SUCCÈS] - La licence a été générée et enregistrée dans {self.licence_folder}\\{self.licence_file}.")
        
        # Pause avant la fermeture
        print("Le script se termine dans 2 secondes...")
        time.sleep(2)

    def get_serial_number(self):
        try:
            serial = subprocess.check_output("wmic bios get serialnumber", shell=True).decode().split("\n")[1].strip()
            return serial
        except Exception:
            return None

    def get_mac_address(self):
        try:
            mac = subprocess.check_output("getmac /fo csv /nh", shell=True).decode().split(",")[0].replace('"', '').strip()
            if mac != "N/A":
                return mac
            else:
                return None
        except Exception:
            return None

    def get_current_datetime(self):
        now = datetime.now()
        return now.strftime("%d%m%Y%H%M")

    def generate_random_string(self, length):
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(random.choice(chars) for _ in range(length))


def main():
    generator = LicenseGenerator()
    generator.generate_license()

if __name__ == "__main__":
    main()  # Appelle la fonction main si le script est exécuté directement
